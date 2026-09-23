"""Generates realistic mock events for the admin UI demo.

All data here is synthetic. No student names, IDs, or identifying imagery
are stored anywhere in this project -- see the privacy rules in
.claude/rules/privacy-and-ethics.md at the repo root.
"""
import random
from datetime import datetime, timedelta

from .db import connection, init_db, is_seeded

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

# Roughly matches real-world detection mix: most events have full evidence.
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
        minutes_ago = rng.randint(2, 60 * 24 * 7)  # up to 7 days back
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

    seed_headcounts(force=force, seed_value=seed_value)


def seed_headcounts(force: bool = False, sessions: int = 10, seed_value: int = 20260921):
    """Synthetic aggregate head-count sessions -- beginning/end of class only.

    Aggregate counts, no student identity of any kind. Mirrors the events
    seeding pattern: deterministic via a fixed-seed Random, no-op if rows
    already exist unless force=True.
    """
    with connection() as conn:
        already = conn.execute("SELECT COUNT(*) AS n FROM head_counts").fetchone()["n"] > 0
    if already and not force:
        return

    rng = random.Random(seed_value + 1)  # distinct stream from event seeding
    today = datetime.now().date()
    rows = []
    for days_ago in range(sessions, 0, -1):
        class_date = (today - timedelta(days=days_ago)).isoformat()
        start_count = rng.randint(24, 32)
        end_count = max(0, start_count - rng.randint(0, 4))
        # source='scheduled' -- head counts are exclusively automated now,
        # so seeded history should read the same way real history would.
        rows.append((class_date, "start", start_count, f"{class_date}T07:55:00", "scheduled"))
        rows.append((class_date, "end", end_count, f"{class_date}T15:10:00", "scheduled"))

    with connection() as conn:
        if force:
            conn.execute("DELETE FROM head_counts")
        conn.executemany(
            "INSERT INTO head_counts (class_date, point, count, recorded_at, source) VALUES (?, ?, ?, ?, ?)",
            rows,
        )


if __name__ == "__main__":
    seed(force=True)
    print("Seeded mock events and head counts.")
