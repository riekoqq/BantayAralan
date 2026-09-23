"""Flask app for the BantayAralan admin UI demo.

Serves a small JSON API backed by mock/seeded SQLite data, plus the static
frontend (HTML/CSS/JS). There is no camera, detection model, or real video
pipeline behind this -- see CLAUDE.md files for implementation status.
"""
from datetime import datetime, timedelta
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory, Response

from .db import connection, init_db, CATEGORY_LABELS
from .seed import seed

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

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
        return jsonify({
            "camera_connected": True,
            "detection_running": True,
            "database_ok": True,
            "last_event_at": last["occurred_at"] if last else None,
        })

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

    @app.get("/api/events/<int:event_id>/snapshot.svg")
    def snapshot_placeholder(event_id):
        with connection() as conn:
            row = conn.execute("SELECT * FROM events WHERE id = ?", (event_id,)).fetchone()
        if row is None or not row["snapshot_available"]:
            return Response(status=404)
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
        data["snapshot_url"] = f"/api/events/{row['id']}/snapshot.svg" if row["snapshot_available"] else None
    return data


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
