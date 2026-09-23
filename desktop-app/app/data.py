"""Mock data layer for the BantayAralan native desktop app.

Same schema and seeding approach as the earlier web prototype
(../../admin-ui/backend/db.py + seed.py), ported here with no Flask/HTTP
dependency -- the GUI calls these functions directly, in-process.

This stores mock event data only. It is not connected to any camera, model,
or detection pipeline -- see ../CLAUDE.md and the project root CLAUDE.md.
"""
import random
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DB_PATH = DATA_DIR / "bantayaralan.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL CHECK (category IN ('standing', 'trash', 'misaligned', 'other')),
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    occurred_at TEXT NOT NULL,
    video_available INTEGER NOT NULL DEFAULT 0,
    snapshot_available INTEGER NOT NULL DEFAULT 0,
    evidence_note TEXT
);
"""

CATEGORY_LABELS = {
    "standing": "Standing",
    "trash": "Trash / Scattered Objects",
    "misaligned": "Misaligned Seat",
    "other": "Other",
}
CATEGORY_SHORT_LABELS = {
    "standing": "Standing",
    "trash": "Trash",
    "misaligned": "Misaligned Seat",
    "other": "Other",
}

CATEGORY_CONTENT = {
    "standing": [
        ("Standing Detected", "Student standing in classroom area"),
        ("Standing Detected", "Prolonged standing detected near the back row"),
        ("Standing Detected", "Standing behavior detected during instruction time"),
    ],
    "trash": [
        ("Trash Detected", "Scattered paper detected near a seating area"),
        ("Trash Detected", "Trash accumulation detected on the classroom floor"),
        ("Clutter Detected", "Loose materials detected outside the storage zone"),
    ],
    "misaligned": [
        ("Misaligned Seat", "Seat position exceeded the configured alignment threshold"),
        ("Misaligned Table", "Table position exceeded the configured alignment threshold"),
        ("Misaligned Seat", "Chair left out of position after a class changeover"),
    ],
    "other": [
        ("Unusual Activity Detected", "Motion detected outside the scheduled class period"),
        ("Classroom Event Flagged", "Activity pattern flagged for teacher review"),
    ],
}

EVIDENCE_WEIGHTS = [
    ("both", 0.68),
    ("snapshot_only", 0.16),
    ("video_only", 0.06),
    ("unavailable", 0.10),
]

UNAVAILABLE_NOTES = [
    "Snapshot could not be retrieved from storage for this event.",
    "Evidence capture failed for this event.",
    "Evidence file is missing from the local store.",
]


# --------------------------------------------------------------- connection
@contextmanager
def connection():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with connection() as conn:
        conn.executescript(SCHEMA)


def is_seeded() -> bool:
    with connection() as conn:
        return conn.execute("SELECT COUNT(*) AS n FROM events").fetchone()["n"] > 0


# --------------------------------------------------------------------- seed
def _pick_evidence(rng: random.Random):
    roll = rng.random()
    cumulative = 0.0
    for kind, weight in EVIDENCE_WEIGHTS:
        cumulative += weight
        if roll <= cumulative:
            return kind
    return "both"


def seed(force: bool = False, count: int = 42, seed_value: int = 20260921):
    init_db()
    if is_seeded() and not force:
        return

    rng = random.Random(seed_value)
    now = datetime.now()
    categories = list(CATEGORY_CONTENT.keys())
    rows = []
    for _ in range(count):
        category = rng.choice(categories)
        title, description = rng.choice(CATEGORY_CONTENT[category])
        minutes_ago = rng.randint(2, 60 * 24 * 7)
        occurred_at = (now - timedelta(minutes=minutes_ago)).isoformat(timespec="seconds")
        evidence_kind = _pick_evidence(rng)
        video_available = 1 if evidence_kind in ("both", "video_only") else 0
        snapshot_available = 1 if evidence_kind in ("both", "snapshot_only") else 0
        evidence_note = rng.choice(UNAVAILABLE_NOTES) if evidence_kind == "unavailable" else None
        rows.append((category, title, description, occurred_at, video_available, snapshot_available, evidence_note))

    with connection() as conn:
        if force:
            conn.execute("DELETE FROM events")
        conn.executemany(
            """
            INSERT INTO events
                (category, title, description, occurred_at, video_available, snapshot_available, evidence_note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )


# ---------------------------------------------------------------- read API
def _serialize(row) -> dict:
    occurred = datetime.fromisoformat(row["occurred_at"])
    evidence_kind = (
        "both" if row["video_available"] and row["snapshot_available"] else
        "snapshot_only" if row["snapshot_available"] else
        "video_only" if row["video_available"] else
        "unavailable"
    )
    return {
        "id": row["id"],
        "category": row["category"],
        "category_label": CATEGORY_LABELS[row["category"]],
        "category_short_label": CATEGORY_SHORT_LABELS[row["category"]],
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


def get_summary() -> dict:
    with connection() as conn:
        total = conn.execute("SELECT COUNT(*) AS n FROM events").fetchone()["n"]
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
        today = conn.execute("SELECT COUNT(*) AS n FROM events WHERE occurred_at >= ?", (today_start,)).fetchone()["n"]
        by_category = {
            cat: conn.execute("SELECT COUNT(*) AS n FROM events WHERE category = ?", (cat,)).fetchone()["n"]
            for cat in CATEGORY_LABELS
        }
        recent_rows = conn.execute("SELECT * FROM events ORDER BY occurred_at DESC LIMIT 6").fetchall()
    return {
        "total_events": total,
        "events_today": today,
        "by_category": by_category,
        "recent": [_serialize(r) for r in recent_rows],
    }


def get_status() -> dict:
    with connection() as conn:
        last = conn.execute("SELECT occurred_at FROM events ORDER BY occurred_at DESC LIMIT 1").fetchone()
    return {
        "camera_connected": True,
        "detection_running": True,
        "database_ok": True,
        "last_event_at": last["occurred_at"] if last else None,
    }


def list_events(category="all", date_range="all", query="", sort="newest", limit=50, offset=0) -> dict:
    clauses, params = [], []
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
    return {"total": total, "limit": limit, "offset": offset, "events": [_serialize(r) for r in rows]}


def get_event(event_id: int):
    with connection() as conn:
        row = conn.execute("SELECT * FROM events WHERE id = ?", (event_id,)).fetchone()
    return _serialize(row) if row else None
