---
tags: [architecture, head-count, scheduling]
status: Implemented
---

# Automated Head-Count Scheduler

`admin-ui/backend/scheduler.py` + `admin-ui/backend/schedule_config.py` —
a background thread that automatically records the beginning-of-class and
end-of-class aggregate head counts at configured times, with no button
click required. Added after the initial Head Count feature (which was
manual-entry only); see [[Web Application as Sole Admin UI]] for when Head
Count itself was introduced.

## Why this exists

The finalized prototype paper's Head Count requirement (RQ2/O2, see
`Prototype Paper Changes.md`) describes head counting as automatic —
happening at the beginning and near the end of a class session — not
something a teacher manually triggers each time. This scheduler is the
implementation of that requirement at the UI/data layer, ahead of any real
detection pipeline.

## Configuration — `admin-ui/backend/schedule_config.py`

All schedule times live in one place, nowhere else:

```python
CLASS_START = time(11, 0)
CLASS_END = time(15, 0)
CLASS_START_HEADCOUNT_TIME = time(11, 15)
FINAL_HEADCOUNT_TIME = time(14, 45)

HEADCOUNT_EVENTS = [
    {"key": "class_start", "point": "start", "time": CLASS_START_HEADCOUNT_TIME, "label": "Class Start Head Count"},
    {"key": "final", "point": "end", "time": FINAL_HEADCOUNT_TIME, "label": "Final Head Count"},
]
```

To retarget a different class schedule, edit only this file. `point`
matches the `head_counts.point` column ([[06 - Database]]).

## Trigger loop — `admin-ui/backend/scheduler.py`

- `scheduler.start()` is called once from `create_app()`
  (`admin-ui/backend/app.py`). It spawns a single daemon thread
  (`threading.Thread(..., daemon=True)`) running `_loop()`, which calls
  `_tick()` every `SCHEDULER_POLL_SECONDS` (15s normally, 2s when
  `BANTAY_TEST_TIME` is set — see Testing below). This thread never touches
  Flask's request-handling thread(s).
- **`_tick()` re-derives status from the database every time**, not from an
  in-memory "already fired" flag:
  1. If `db.get_head_count(class_date, point)` already returns a row for
     today → status `complete`. This is what makes each event fire *at
     most once per day* and gives the **daily reset** for free — a new
     calendar date has no row yet, so yesterday's completion can never
     block today, with no explicit reset code needed anywhere.
  2. Else if `now < event_time_today` → status `waiting`.
  3. Else (the event's time has passed and it's not recorded yet) — see
     "Missed vs. triggered" below.
- On trigger, status briefly becomes `performing`, `scheduler._capture_head_count()`
  is called (see Placeholder below), the result is written via
  `db.upsert_head_count(class_date, point, count, source="scheduled")`,
  and status becomes `complete`. Any exception during capture/write resets
  status to `waiting` so the next tick retries — the loop itself is wrapped
  in a broad `except Exception: pass` so one bad tick can never crash the
  background thread.

## Missed vs. triggered (startup / restart behavior)

An event auto-fires **only if it was reached while the app was already
running**:

```
app_start_time <= event_time_today <= now   →  fire it
event_time_today < app_start_time            →  mark "missed", don't fire retroactively
```

`app_start_time` is captured once, in `scheduler.start()`. This single
comparison implements all three startup cases from the spec without any
special-cased date logic:
- App running continuously, clock reaches 11:15 → fires normally.
- App starts fresh at, say, 1:00 PM (after 11:15, before 14:45) → the
  11:15 event is marked `missed` (app started after its time), the 14:45
  event still fires normally when reached.
- App starts after 14:45 → both events are `missed` for today; nothing
  fires until tomorrow (a new `class_date` with no rows yet).

## Placeholder capture value

`scheduler._capture_head_count()` returns `random.randint(24, 32)` — **not
tied to any real camera frame or model output**. There is no detection
pipeline in this repo (see [[04 - Computer Vision]], Not Yet Implemented).
Swapping in a real detector later means replacing this one function; the
rest of the scheduler (timing, storage, status, API) needs no change. The
real duplicate-counting/individual-distinction mechanism a genuine detector
would need is an explicitly open question — see [[12 - Open Questions]].

## API surface

- `GET /api/headcount-schedule` (`admin-ui/backend/app.py` →
  `scheduler.get_schedule_status()`) — for each configured event: `key`,
  `label`, `scheduled_time`, `status` (`waiting` / `performing` /
  `complete` / `missed`), `detected_count`, `recorded_at`, `source`.
- The existing `GET`/`POST /api/headcounts` (manual entry) and this route
  share the same underlying `head_counts` table and `db.upsert_head_count()`
  helper — see [[06 - Database]].

## Frontend

`admin-ui/frontend/js/views/headcount.js`'s `renderHeadcount()` shows
"Today's Scheduled Head Counts" as two status cards (`scheduleCardHtml()`),
polling `/api/headcount-schedule` every 20s while the page is open (the
interval self-cancels via a `document.body.contains(root)` check once the
user navigates away — the app has no per-view cleanup hook otherwise, see
[[UI UX Overview]]). Cards show Expected (always blank — no expected-count
feature exists, don't invent one), Detected, Scheduled Time, and Status.
The manual-entry form is kept alongside for correcting/overriding a count
by hand. The sidebar status box (`renderStatusBox()` in
`admin-ui/frontend/js/app.js`) also shows a one-line summary of today's
scheduler state on every page.

## Testing without waiting for 11:15 AM / 2:45 PM

`BANTAY_TEST_TIME` env var overrides `scheduler._now()` (accepts
`"HH:MM:SS"` using today's real date, or a full `"YYYY-MM-DD HH:MM:SS"`).
Never set this in a real deployment. See `admin-ui/CLAUDE.md` → "Testing
the scheduler" for the exact three-case test commands (idle-before-both,
fires-class-start-while-running, starts-late-at-14:45-so-class-start-is-missed-and-final-fires).

## Status
**Implemented** (trigger logic, storage, API, UI). **Not Yet Implemented**:
any real detected value (placeholder random int only). **Open**: real
duplicate-count handling for an actual detector — see
[[12 - Open Questions]].

## Related
- [[06 - Database]]
- [[Web Application as Sole Admin UI]]
- [[04 - Computer Vision]]
- [[12 - Open Questions]]
- [[UI UX Overview]]
