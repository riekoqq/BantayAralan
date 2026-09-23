"""SQLite access for the BantayAralan admin UI demo.

This stores mock event data only. It is not connected to any camera, model,
or detection pipeline -- see ../CLAUDE.md and the project root CLAUDE.md for
what is and is not implemented.
"""
import sqlite3
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


def is_seeded() -> bool:
    with connection() as conn:
        row = conn.execute("SELECT COUNT(*) AS n FROM events").fetchone()
        return row["n"] > 0
