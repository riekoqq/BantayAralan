"""Flask app for the BantayAralan admin UI demo.

Serves a small JSON API backed by mock/seeded SQLite data, plus the static
frontend (HTML/CSS/JS). There is no camera, detection model, or real video
pipeline behind this -- see CLAUDE.md files for implementation status.
"""
from datetime import datetime, timedelta
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory, send_file, Response

from . import scheduler
from .db import connection, init_db, CATEGORY_LABELS, DATA_DIR
from .seed import seed

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
SNAPSHOTS_DIR = DATA_DIR / "snapshots"

CATEGORY_ICON_COLOR = {
    "standing": "#B7791F",
    "trash": "#C0344B",
    "misaligned": "#6E4FA6",
    "other": "#475266",
}


def create_app():
    app = Flask(__name__, static_folder=None)
    init_db()
    seed()  # no-op if already seeded
    scheduler.start()  # no-op if already started; runs in its own daemon thread

    # ---------------------------------------------------------------- pages
    @app.get("/")
    def index():
        return send_from_directory(FRONTEND_DIR, "index.html")

    @app.get("/<path:path>")
    def static_files(path):
        return send_from_directory(FRONTEND_DIR, path)

    # ------------------------------------------------------------------ api
    @app.get("/api/summary")
    def summary():
        with connection() as conn:
            total = conn.execute("SELECT COUNT(*) AS n FROM events").fetchone()["n"]
            today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
            today = conn.execute(
                "SELECT COUNT(*) AS n FROM events WHERE occurred_at >= ?", (today_start,)
            ).fetchone()["n"]
            by_category = {}
            for cat in CATEGORY_LABELS:
                n = conn.execute(
                    "SELECT COUNT(*) AS n FROM events WHERE category = ?", (cat,)
                ).fetchone()["n"]
                by_category[cat] = n
            recent_rows = conn.execute(
                "SELECT * FROM events ORDER BY occurred_at DESC LIMIT 6"
            ).fetchall()
        return jsonify({
            "total_events": total,
            "events_today": today,
            "by_category": by_category,
            "recent": [_serialize_event(r) for r in recent_rows],
        })

    @app.get("/api/status")
    def status():
        with connection() as conn:
            last = conn.execute(
                "SELECT occurred_at FROM events ORDER BY occurred_at DESC LIMIT 1"
            ).fetchone()
            detection_row = conn.execute(
                "SELECT enabled FROM detection_state WHERE id = 1"
            ).fetchone()
        # camera_connected/monitoring_active are mock-true -- there is no real
        # camera or pipeline yet. Cameras and continuous monitoring/processing
        # are independent of the detection_enabled toggle, which only gates
        # event generation -- see admin-ui/CLAUDE.md.
        return jsonify({
            "camera_connected": True,
            "monitoring_active": True,
            "detection_enabled": bool(detection_row["enabled"]) if detection_row else True,
            "database_ok": True,
            "last_event_at": last["occurred_at"] if last else None,
        })

    @app.get("/api/detection-state")
    def get_detection_state():
        with connection() as conn:
            row = conn.execute("SELECT enabled, updated_at FROM detection_state WHERE id = 1").fetchone()
        return jsonify({"enabled": bool(row["enabled"]), "updated_at": row["updated_at"]})

    @app.post("/api/detection-state")
    def set_detection_state():
        data = request.get_json(silent=True) or {}
        enabled = data.get("enabled")
        if not isinstance(enabled, bool):
            return jsonify({"error": "invalid_input", "message": "enabled must be a boolean."}), 400
        now = datetime.now().isoformat(timespec="seconds")
        with connection() as conn:
            conn.execute(
                "UPDATE detection_state SET enabled = ?, updated_at = ? WHERE id = 1",
                (1 if enabled else 0, now),
            )
        return jsonify({"enabled": enabled, "updated_at": now})

    # ------------------------------------------------------------ head count
    @app.get("/api/headcounts")
    def list_headcounts():
        limit = min(int(request.args.get("limit", 20)), 100)
        with connection() as conn:
            rows = conn.execute(
                "SELECT class_date, point, count, recorded_at, source FROM head_counts "
                "ORDER BY class_date DESC, point ASC"
            ).fetchall()
        sessions = {}
        for r in rows:
            session = sessions.setdefault(r["class_date"], {"class_date": r["class_date"], "start": None, "end": None})
            session[r["point"]] = {"count": r["count"], "recorded_at": r["recorded_at"], "source": r["source"]}
        sessions_list = sorted(sessions.values(), key=lambda s: s["class_date"], reverse=True)[:limit]
        return jsonify({"sessions": sessions_list})

    # Manual head-count entry has been removed -- all head_counts rows now
    # come exclusively from the automated scheduler (backend/scheduler.py).
    # See Knowledge/03 - Architecture/Automated Head-Count Scheduler.md.

    # ------------------------------------------- automated head-count schedule
    @app.get("/api/headcount-schedule")
    def headcount_schedule():
        return jsonify(scheduler.get_schedule_status())

    # -------------------------------------------------- statistics/insights
    @app.get("/api/statistics")
    def statistics_route():
        return jsonify(_compute_statistics())

    @app.get("/api/insights")
    def insights_route():
        stats = _compute_statistics()
        return jsonify({"insights": _compute_insights(stats), "window_days": stats["window_days"]})

    @app.get("/api/suggestions")
    def suggestions_route():
        stats = _compute_statistics()
        items = [
            {
                "category": cat,
                "category_label": CATEGORY_LABELS[cat],
                "count": n,
                "suggestion": SUGGESTION_MAP[cat],
            }
            for cat, n in stats["by_category_this_period"].items() if n > 0
        ]
        items.sort(key=lambda s: s["count"], reverse=True)
        return jsonify({"suggestions": items, "window_days": stats["window_days"]})

    @app.get("/api/events")
    def list_events():
        category = request.args.get("category", "all")
        date_range = request.args.get("range", "all")  # today | 7d | all
        query = request.args.get("q", "").strip()
        sort = request.args.get("sort", "newest")
        limit = min(int(request.args.get("limit", 50)), 200)
        offset = int(request.args.get("offset", 0))

        clauses = []
        params = []

        if category != "all":
            clauses.append("category = ?")
            params.append(category)

        if date_range == "today":
            start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
            clauses.append("occurred_at >= ?")
            params.append(start)
        elif date_range == "7d":
            start = (datetime.now() - timedelta(days=7)).isoformat()
            clauses.append("occurred_at >= ?")
            params.append(start)

        if query:
            clauses.append("(title LIKE ? OR description LIKE ?)")
            like = f"%{query}%"
            params.extend([like, like])

        where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        order = "ASC" if sort == "oldest" else "DESC"

        with connection() as conn:
            total = conn.execute(f"SELECT COUNT(*) AS n FROM events {where}", params).fetchone()["n"]
            rows = conn.execute(
                f"SELECT * FROM events {where} ORDER BY occurred_at {order} LIMIT ? OFFSET ?",
                params + [limit, offset],
            ).fetchall()

        return jsonify({
            "total": total,
            "limit": limit,
            "offset": offset,
            "events": [_serialize_event(r) for r in rows],
        })

    @app.get("/api/events/<int:event_id>")
    def get_event(event_id):
        with connection() as conn:
            row = conn.execute("SELECT * FROM events WHERE id = ?", (event_id,)).fetchone()
        if row is None:
            return jsonify({"error": "not_found", "message": "Event not found."}), 404
        return jsonify(_serialize_event(row, detail=True))

    @app.get("/api/events/<int:event_id>/snapshot")
    def snapshot(event_id):
        """Real captured frame if detection/monitor_trash.py saved one for
        this event (data/snapshots/<id>.jpg); otherwise the generated
        placeholder icon used by every seeded/mock event. Same URL either
        way -- the browser reads Content-Type, not the path -- so the
        frontend doesn't need to know which kind it's getting."""
        with connection() as conn:
            row = conn.execute("SELECT * FROM events WHERE id = ?", (event_id,)).fetchone()
        if row is None or not row["snapshot_available"]:
            return Response(status=404)
        real_path = SNAPSHOTS_DIR / f"{event_id}.jpg"
        if real_path.exists():
            return send_file(real_path, mimetype="image/jpeg")
        color = CATEGORY_ICON_COLOR.get(row["category"], "#475266")
        svg = _placeholder_svg(color, row["category"])
        return Response(svg, mimetype="image/svg+xml")

    return app


def _serialize_event(row, detail: bool = False):
    occurred = datetime.fromisoformat(row["occurred_at"])
    evidence_kind = (
        "both" if row["video_available"] and row["snapshot_available"] else
        "snapshot_only" if row["snapshot_available"] else
        "video_only" if row["video_available"] else
        "unavailable"
    )
    data = {
        "id": row["id"],
        "category": row["category"],
        "category_label": CATEGORY_LABELS[row["category"]],
        "status": row["status"],
        "title": row["title"],
        "description": row["description"],
        "occurred_at": row["occurred_at"],
        "date_label": occurred.strftime("%B %d, %Y"),
        "time_label": occurred.strftime("%I:%M %p").lstrip("0"),
        "video_available": bool(row["video_available"]),
        "snapshot_available": bool(row["snapshot_available"]),
        "evidence_kind": evidence_kind,
        "evidence_note": row["evidence_note"],
    }
    if detail:
        data["snapshot_url"] = f"/api/events/{row['id']}/snapshot" if row["snapshot_available"] else None
    return data


# Simple, clearly-labeled rule-based text -- not a validated recommendation
# engine. See Knowledge/12 - Open Questions.md ("Statistical/pattern-analysis
# methodology" is explicitly open).
SUGGESTION_MAP = {
    "standing": "Consider a brief mid-class movement break if standing events cluster around the same time of day.",
    "trash": "Consider a quick tidy-up reminder before transitions if trash/scattered-object events recur.",
    "misaligned": "Consider a seat-realignment check at the start of class if misaligned-seat events recur.",
    "other": "Review flagged events individually -- this category covers activity that doesn't fit the other three.",
}


def _compute_statistics(window_days: int = 7) -> dict:
    """Real counts/percentages computed from the (seeded, mock) events table.

    Simple SQL aggregation only -- no invented formula or fabricated numbers.
    """
    now = datetime.now()
    period_start = now - timedelta(days=window_days)
    prev_start = now - timedelta(days=window_days * 2)
    with connection() as conn:
        total_all_time = conn.execute("SELECT COUNT(*) AS n FROM events").fetchone()["n"]
        this_period = conn.execute(
            "SELECT COUNT(*) AS n FROM events WHERE occurred_at >= ?", (period_start.isoformat(),)
        ).fetchone()["n"]
        previous_period = conn.execute(
            "SELECT COUNT(*) AS n FROM events WHERE occurred_at >= ? AND occurred_at < ?",
            (prev_start.isoformat(), period_start.isoformat()),
        ).fetchone()["n"]
        by_category_this_period = {
            cat: conn.execute(
                "SELECT COUNT(*) AS n FROM events WHERE category = ? AND occurred_at >= ?",
                (cat, period_start.isoformat()),
            ).fetchone()["n"]
            for cat in CATEGORY_LABELS
        }

    trend_pct = None
    if previous_period:
        trend_pct = round((this_period - previous_period) / previous_period * 100)

    return {
        "window_days": window_days,
        "total_events_all_time": total_all_time,
        "events_this_period": this_period,
        "events_previous_period": previous_period,
        "trend_pct": trend_pct,
        "by_category_this_period": by_category_this_period,
    }


def _compute_insights(stats: dict) -> list:
    """0-2 short, plainly-derived observations -- empty if there isn't enough data yet."""
    insights = []
    if stats["events_this_period"] == 0:
        return insights

    top_cat, top_n = max(stats["by_category_this_period"].items(), key=lambda kv: kv[1])
    if top_n > 0:
        plural = "" if top_n == 1 else "s"
        insights.append(
            f"{CATEGORY_LABELS[top_cat]} was the most frequent recorded category in the last "
            f"{stats['window_days']} days ({top_n} event{plural})."
        )

    trend = stats["trend_pct"]
    if trend is not None and abs(trend) >= 20:
        direction = "increased" if trend > 0 else "decreased"
        insights.append(
            f"Recorded events {direction} {abs(trend)}% compared to the previous {stats['window_days']} days."
        )

    return insights


def _placeholder_svg(color: str, category: str) -> str:
    label = {
        "standing": "Classroom camera view (behavior)",
        "trash": "Top-down camera view (clutter)",
        "misaligned": "Top-down camera view (seat alignment)",
        "other": "Classroom camera view",
    }.get(category, "Classroom camera view")
    return f"""<svg width=\"640\" height=\"360\" viewBox=\"0 0 640 360\" xmlns=\"http://www.w3.org/2000/svg\">
  <rect width=\"640\" height=\"360\" fill=\"#EEF1F5\"/>
  <g opacity=\"0.5\">
    <circle cx=\"320\" cy=\"160\" r=\"34\" fill=\"none\" stroke=\"{color}\" stroke-width=\"3\"/>
    <path d=\"M296 148h48v40h-48z\" fill=\"none\" stroke=\"{color}\" stroke-width=\"3\"/>
  </g>
  <text x=\"320\" y=\"230\" font-family=\"Arial, sans-serif\" font-size=\"14\" fill=\"#6B7382\" text-anchor=\"middle\">{label} -- mock evidence placeholder</text>
  <text x=\"320\" y=\"252\" font-family=\"Arial, sans-serif\" font-size=\"12\" fill=\"#9AA3B1\" text-anchor=\"middle\">No real classroom imagery. No students identified.</text>
</svg>"""
