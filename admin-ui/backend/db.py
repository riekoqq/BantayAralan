"""SQLite access for the BantayAralan admin UI demo.

This stores mock event data only. It is not connected to any camera, model,
or detection pipeline -- see ../CLAUDE.md and the project root CLAUDE.md for
what is and is not implemented.
"""
import sqlite3
from datetime import datetime
from pathlib import Path
from contextlib import contextmanager

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DB_PATH = DATA_DIR / "bantayaralan.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL CHECK (category IN ('standing', 'trash', 'misaligned', 'other')),
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    occurred_at TEXT NOT NULL,          -- ISO 8601 timestamp
    video_available INTEGER NOT NULL DEFAULT 0,
    snapshot_available INTEGER NOT NULL DEFAULT 0,
    evidence_note TEXT,                 -- shown when evidence is unavailable
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'resolved'))
);

-- Aggregate student head counts at the beginning/end of a class session.
-- Aggregate only -- no student names, IDs, or per-student rows anywhere.
CREATE TABLE IF NOT EXISTS head_counts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_date TEXT NOT NULL,           -- ISO date (YYYY-MM-DD)
    point TEXT NOT NULL CHECK (point IN ('start', 'end')),
    count INTEGER NOT NULL,
    recorded_at TEXT NOT NULL,          -- ISO 8601 timestamp
    source TEXT NOT NULL DEFAULT 'scheduled' CHECK (source IN ('manual', 'scheduled'))
);

-- Single persisted row: whether detection/event-generation is enabled,
-- per category (trash, standing) -- separate toggles so disabling one
-- doesn't gate the other. Gates event generation only -- cameras,
-- monitoring, and head counting are independent of these flags (see
-- admin-ui/CLAUDE.md). Only `trash` and `standing` have real detectors
-- (see detection/monitor.py); `misaligned`/`other` have no toggle since
-- nothing generates those automatically.
CREATE TABLE IF NOT EXISTS detection_state (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    trash_enabled INTEGER NOT NULL DEFAULT 1,
    standing_enabled INTEGER NOT NULL DEFAULT 1,
    updated_at TEXT NOT NULL
);
"""

CATEGORY_LABELS = {
    "standing": "Standing",
    "trash": "Trash / Scattered Objects",
    "misaligned": "Misaligned Seat",
    "other": "Other",
}


def get_connection():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@contextmanager
def connection():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with connection() as conn:
        conn.executescript(SCHEMA)
    _migrate_head_counts_source_column()
    _migrate_events_status_column()
    _migrate_detection_state_columns()
    ensure_detection_state()


def ensure_detection_state():
    """Make sure the single detection_state row exists, defaulting to both
    categories enabled."""
    with connection() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO detection_state (id, trash_enabled, standing_enabled, updated_at) "
            "VALUES (1, 1, 1, ?)",
            (datetime.now().isoformat(timespec="seconds"),),
        )


def _migrate_detection_state_columns():
    """Split the old single `enabled` column (pre-2026-10-01, one toggle for
    every category) into `trash_enabled`/`standing_enabled`. Carries the old
    combined value over to both new columns so a toggle that was off stays
    off for both rather than silently re-enabling anything. The old `enabled`
    column is left in place, unused -- dropping it isn't worth the risk for
    a mock/demo database.
    """
    with connection() as conn:
        cols = {row["name"] for row in conn.execute("PRAGMA table_info(detection_state)")}
        if "enabled" in cols and "trash_enabled" not in cols:
            conn.execute("ALTER TABLE detection_state ADD COLUMN trash_enabled INTEGER NOT NULL DEFAULT 1")
            conn.execute("ALTER TABLE detection_state ADD COLUMN standing_enabled INTEGER NOT NULL DEFAULT 1")
            conn.execute("UPDATE detection_state SET trash_enabled = enabled, standing_enabled = enabled")


def _migrate_head_counts_source_column():
    """Add head_counts.source to a pre-existing DB file created before this
    column existed. SQLite has no "ADD COLUMN IF NOT EXISTS", so check first.
    """
    with connection() as conn:
        cols = {row["name"] for row in conn.execute("PRAGMA table_info(head_counts)")}
        if "source" not in cols:
            conn.execute(
                "ALTER TABLE head_counts ADD COLUMN source TEXT NOT NULL DEFAULT 'manual'"
            )


def _migrate_events_status_column():
    """Add events.status to a pre-existing DB file created before this column
    existed. SQLite has no "ADD COLUMN IF NOT EXISTS", so check first. New
    rows already get 'active' from the column default; this only backfills
    old rows, which are historical/seeded events, not currently-open ones.
    """
    with connection() as conn:
        cols = {row["name"] for row in conn.execute("PRAGMA table_info(events)")}
        if "status" not in cols:
            conn.execute(
                "ALTER TABLE events ADD COLUMN status TEXT NOT NULL DEFAULT 'active'"
            )
            conn.execute("UPDATE events SET status = 'resolved'")


def is_seeded() -> bool:
    with connection() as conn:
        row = conn.execute("SELECT COUNT(*) AS n FROM events").fetchone()
        return row["n"] > 0


_DETECTION_STATE_COLUMNS = {"trash": "trash_enabled", "standing": "standing_enabled"}


def is_category_detection_enabled(category: str) -> bool:
    """Read the sidebar/mobile per-category Detection toggle's current
    value. Used by detection/monitor.py and monitor_trash.py to decide
    whether to open new events -- see those scripts' callers for why this
    only gates *new* events, not already-tracked ones being resolved.
    Categories with no toggle of their own (misaligned, other -- nothing
    generates those automatically) always read as enabled."""
    column = _DETECTION_STATE_COLUMNS.get(category)
    if column is None:
        return True
    with connection() as conn:
        row = conn.execute(f"SELECT {column} FROM detection_state WHERE id = 1").fetchone()
        return bool(row[column]) if row else True


def set_category_detection_enabled(category: str, enabled: bool) -> None:
    column = _DETECTION_STATE_COLUMNS.get(category)
    if column is None:
        raise ValueError(f"no detection toggle for category: {category!r}")
    with connection() as conn:
        conn.execute(
            f"UPDATE detection_state SET {column} = ?, updated_at = ? WHERE id = 1",
            (1 if enabled else 0, datetime.now().isoformat(timespec="seconds")),
        )


# ------------------------------------------------------------------ events
def insert_event(
    category: str,
    title: str,
    description: str,
    occurred_at: str = None,
    video_available: int = 0,
    snapshot_available: int = 0,
    evidence_note: str = None,
) -> int:
    """Insert a new event with status='active'. Returns the new row's id.

    Used by detection/monitor_trash.py (a manual, one-off script -- see its
    own docstring) as the only real, non-seed caller so far. Position/
    tracking state that decides *when* to call this lives in that script's
    own memory, not in this table -- see Knowledge/05 - Events & Evidence/
    Event Model.md for why no bbox/frame linkage is stored here.
    """
    occurred_at = occurred_at or datetime.now().isoformat(timespec="seconds")
    with connection() as conn:
        cur = conn.execute(
            """
            INSERT INTO events
                (category, title, description, occurred_at, video_available, snapshot_available, evidence_note, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'active')
            """,
            (category, title, description, occurred_at, video_available, snapshot_available, evidence_note),
        )
        return cur.lastrowid


def resolve_event(event_id: int):
    """Mark one event resolved (e.g. the tracked item is no longer detected)."""
    with connection() as conn:
        conn.execute("UPDATE events SET status = 'resolved' WHERE id = ?", (event_id,))


def list_active_events(category: str = None):
    """Active (unresolved) events, newest first. Used by monitor_trash.py to
    rebuild its in-memory tracked-location state on startup, not by the web
    UI (which reads events via app.py's own /api/events query)."""
    with connection() as conn:
        if category:
            return conn.execute(
                "SELECT * FROM events WHERE status = 'active' AND category = ? ORDER BY occurred_at DESC",
                (category,),
            ).fetchall()
        return conn.execute(
            "SELECT * FROM events WHERE status = 'active' ORDER BY occurred_at DESC"
        ).fetchall()


# ------------------------------------------------------------- head counts
def upsert_head_count(class_date: str, point: str, count: int, source: str = "scheduled") -> str:
    """Record one head-count reading, replacing any prior reading for the
    same (class_date, point). Last write wins -- see
    Knowledge/12 - Open Questions.md (duplicate-count handling is open).
    Head counts are recorded exclusively by the automated scheduler
    (backend/scheduler.py) -- there is no manual-entry caller anymore.
    Returns the recorded_at timestamp.
    """
    now = datetime.now().isoformat(timespec="seconds")
    with connection() as conn:
        conn.execute("DELETE FROM head_counts WHERE class_date = ? AND point = ?", (class_date, point))
        conn.execute(
            "INSERT INTO head_counts (class_date, point, count, recorded_at, source) VALUES (?, ?, ?, ?, ?)",
            (class_date, point, count, now, source),
        )
    return now


def get_head_count(class_date: str, point: str):
    """Return the sqlite3.Row for this (class_date, point), or None if not yet recorded."""
    with connection() as conn:
        return conn.execute(
            "SELECT count, recorded_at, source FROM head_counts WHERE class_date = ? AND point = ?",
            (class_date, point),
        ).fetchone()
