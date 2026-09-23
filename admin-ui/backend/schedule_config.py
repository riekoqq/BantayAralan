"""Centralized class-schedule / head-count timing configuration.

To retarget a different class schedule, change the four times below --
nothing else in the scheduler (backend/scheduler.py) needs editing. Don't
scatter schedule times anywhere else in the codebase.
"""
from datetime import time

CLASS_START = time(11, 0)
CLASS_END = time(15, 0)
CLASS_START_HEADCOUNT_TIME = time(11, 15)
FINAL_HEADCOUNT_TIME = time(14, 45)

# Ordered list the scheduler iterates over. `point` matches the head_counts
# table's `point` column (see backend/db.py).
HEADCOUNT_EVENTS = [
    {
        "key": "class_start",
        "point": "start",
        "time": CLASS_START_HEADCOUNT_TIME,
        "label": "Class Start Head Count",
    },
    {
        "key": "final",
        "point": "end",
        "time": FINAL_HEADCOUNT_TIME,
        "label": "Final Head Count",
    },
]
