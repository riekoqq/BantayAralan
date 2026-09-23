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
    evidence_note TEXT                  -- shown when evidence is unavailable
);

-- Aggregate student head counts at the beginning/end of a class session.
-- Aggregate only -- no student names, IDs, or per-student rows anywhere.
CREATE TABLE IF NOT EXISTS head_counts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_date TEXT NOT NULL,           -- ISO date (YYYY-MM-DD)
    point TEXT NOT NULL CHECK (point IN ('start', 'end')),
    count INTEGER NOT NULL,
    recorded_at TEXT NOT NULL           -- ISO 8601 timestamp
);

-- Single persisted row: whether detection/event-generation is enabled.
-- Gates event generation only -- cameras, monitoring, and head counting
-- are independent of this flag (see admin-ui/CLAUDE.md).
CREATE TABLE IF NOT EXISTS detection_state (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    enabled INTEGER NOT NULL DEFAULT 1,
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
    ensure_detection_state()


def ensure_detection_state():
    """Make sure the single detection_state row exists, defaulting to enabled."""
    with connection() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO detection_state (id, enabled, updated_at) VALUES (1, 1, ?)",
            (datetime.now().isoformat(timespec="seconds"),),
        )


def is_seeded() -> bool:
    with connection() as conn:
        row = conn.execute("SELECT COUNT(*) AS n FROM events").fetchone()
        return row["n"] > 0
