"""Background scheduler that automatically triggers the class-start and
final head counts at the configured times (see schedule_config.py).

Design:
- Runs as a single daemon thread, started once from create_app() (see
  app.py). It never blocks Flask's request-handling thread(s) -- this
  mirrors how a camera-processing loop would run alongside a GUI, kept
  deliberately separate from any detection logic (there is none yet).
- Ticks every SCHEDULER_POLL_SECONDS; each tick re-derives every event's
  status from the database and the clock -- there is no separate
  "already fired" flag that could go stale, so a process restart or a new
  calendar day naturally resets state (see "Daily reset" in
  admin-ui/CLAUDE.md).
- An event fires only if it was reached *while the app was running*:
  app_start_time <= event_time_today <= now. If the app starts after an
  event's time has already passed today, that event is marked "missed"
  instead of firing retroactively. This implements the three startup cases
  from the spec: starting before/between/after the two scheduled times.
- Each event fires at most once per class_date, because firing means
  writing a head_counts row for that (class_date, point) -- once that row
  exists, the event reads back as "complete" and is never re-triggered.
- The actual head-count *value* is a placeholder simulated capture, since
  there is no real camera/detection pipeline in this repo yet (see
  Knowledge/12 - Open Questions.md). Swapping in a real detector later
  means replacing _capture_head_count() only.
"""
import os
import random
import threading
import time as time_module
from datetime import datetime

from . import db
from . import schedule_config as cfg

# Poll faster under a test-time override so manual testing doesn't need to
# wait long between ticks -- see admin-ui/CLAUDE.md "Testing the scheduler".
SCHEDULER_POLL_SECONDS = 2 if os.environ.get("BANTAY_TEST_TIME") else 15

_state_lock = threading.Lock()
_runtime_status = {ev["key"]: "waiting" for ev in cfg.HEADCOUNT_EVENTS}
_app_start_time = None
_started = False


def _now() -> datetime:
    """Real current time, unless BANTAY_TEST_TIME overrides it.

    BANTAY_TEST_TIME is a development/testing-only override -- never set it
    in production. Accepts "YYYY-MM-DD HH:MM:SS" or just "HH:MM[:SS]" (today's
    real calendar date is used with the given time). See admin-ui/CLAUDE.md.
    """
    override = os.environ.get("BANTAY_TEST_TIME")
    if not override:
        return datetime.now()
    override = override.strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%H:%M:%S", "%H:%M"):
        try:
            parsed = datetime.strptime(override, fmt)
        except ValueError:
            continue
        if fmt.startswith("%H"):
            return datetime.combine(datetime.now().date(), parsed.time())
        return parsed
    return datetime.now()


def _capture_head_count() -> int:
    """PLACEHOLDER: simulates a detected aggregate head count.

    Not tied to any real camera frame or model output -- replace this with
    a real call into the detection/tracking pipeline once one exists. The
    real duplicate-counting/individual-distinction mechanism is explicitly
    still an open question (Knowledge/12 - Open Questions.md).
    """
    return random.randint(24, 32)


def _tick():
    now = _now()
    class_date = now.date().isoformat()

    for ev in cfg.HEADCOUNT_EVENTS:
        key = ev["key"]
        event_dt = datetime.combine(now.date(), ev["time"])

        if db.get_head_count(class_date, ev["point"]) is not None:
            with _state_lock:
                _runtime_status[key] = "complete"
            continue

        if now < event_dt:
            with _state_lock:
                _runtime_status[key] = "waiting"
            continue

        if _app_start_time is not None and _app_start_time <= event_dt:
            # Reached while running -- fire it.
            with _state_lock:
                _runtime_status[key] = "performing"
            try:
                count = _capture_head_count()
                db.upsert_head_count(class_date, ev["point"], count, source="scheduled")
                with _state_lock:
                    _runtime_status[key] = "complete"
            except Exception:
                with _state_lock:
                    _runtime_status[key] = "waiting"  # retry on the next tick
        else:
            # App started after this event's scheduled time -- don't fire
            # retroactively, just recognize it as missed for today.
            with _state_lock:
                _runtime_status[key] = "missed"


def _loop():
    while True:
        try:
            _tick()
        except Exception:
            pass  # never let the background loop crash the app; next tick retries
        time_module.sleep(SCHEDULER_POLL_SECONDS)


def start():
    """Start the background scheduler thread. Safe to call more than once."""
    global _app_start_time, _started
    if _started:
        return
    _started = True
    _app_start_time = _now()
    thread = threading.Thread(target=_loop, name="headcount-scheduler", daemon=True)
    thread.start()


def get_schedule_status() -> dict:
    """Current status of today's scheduled head-count events, for the API."""
    now = _now()
    class_date = now.date().isoformat()
    with _state_lock:
        statuses = dict(_runtime_status)

    events = []
    for ev in cfg.HEADCOUNT_EVENTS:
        row = db.get_head_count(class_date, ev["point"])
        events.append({
            "key": ev["key"],
            "label": ev["label"],
            "scheduled_time": ev["time"].strftime("%I:%M %p").lstrip("0"),
            "status": statuses.get(ev["key"], "waiting"),
            "detected_count": row["count"] if row else None,
            "recorded_at": row["recorded_at"] if row else None,
            "source": row["source"] if row else None,
        })
    return {"class_date": class_date, "events": events}
