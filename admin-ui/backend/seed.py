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


if __name__ == "__main__":
    seed(force=True)
    print("Seeded mock events.")
