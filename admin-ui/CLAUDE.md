# admin-ui — BantayAralan Admin Interface Prototype

Status: **Implemented** (as a UI/UX prototype with mock data — not connected
to any real detection pipeline). This is the **sole and primary** BantayAralan
admin UI — a separate native desktop prototype (`desktop-app/`, PySide6)
existed briefly and was removed on 2026-09-23 once the finalized prototype
paper settled the direction as web-only; see
[Knowledge/11 - Decisions/Web Application as Sole Admin UI.md](<../Knowledge/11 - Decisions/Web Application as Sole Admin UI.md>).
See root [`CLAUDE.md`](../CLAUDE.md) for the project-wide working-draft/
status-label rules; this file assumes you've read those.

## Purpose

A working, click-through admin interface for BantayAralan: Dashboard,
Events & Logs, Event Detail (video + screenshot evidence tabs), Head Count,
and Insights & Statistics (Statistics / Classroom Insights / Suggestions
tabs), plus a Detection Enable/Disable control in the sidebar. Built to
demonstrate the intended UI/UX for the thesis project after the original
Figma-based design pass was cut short by a Figma Starter-plan MCP rate
limit. One classroom, admin-only, no login flow, no student identification
anywhere — per the design brief this was built from.

## Newer sections (added for the finalized prototype paper direction)

- **Head Count** (`frontend/js/views/headcount.js`, `/api/headcounts` (GET
  only), `head_counts` table) — **aggregate** student counts at the
  beginning and near the end of a class session only. Never add
  per-student rows, names, or IDs here. Recorded exclusively by the
  automated scheduler (below) — there is no manual-entry UI or API route
  anymore (removed 2026-09-24; see
  [Knowledge/11 - Decisions/Manual Head-Count Entry Removed.md](<../Knowledge/11 - Decisions/Manual Head-Count Entry Removed.md>)).
  Duplicate handling is a placeholder policy (last recorded value per
  date+point wins) — see
  [Knowledge/12 - Open Questions.md](<../Knowledge/12 - Open Questions.md>).
- **Detection Enable/Disable** (`renderStatusBox()` in `app.js`,
  `/api/detection-state`, `detection_state` table) — a real, persisted
  toggle that gates **event generation only**. The UI must never imply that
  disabling it stops cameras, stops the app, deletes data, or stops head
  counting — `/api/status` reports `camera_connected` and
  `monitoring_active` as separate, always-true fields specifically so the
  sidebar can show those as unaffected.
- **Insights & Statistics** (`frontend/js/views/insights.js`,
  `/api/statistics`, `/api/insights`, `/api/suggestions`) — one page, three
  tabs, computed for real from the `events` table (plain SQL counts/percent
  deltas over a 7-day window, not fabricated numbers). Insights/suggestions
  use a deliberately simple, rule-based `SUGGESTION_MAP`/threshold approach
  in `backend/app.py` — not a validated statistical or behavioral model. Say
  so in the UI (see the `disclaimerHtml()` notes already in `insights.js`)
  and don't strengthen that language without checking with the user first;
  the real methodology is an explicitly open question
  (`Knowledge/12 - Open Questions.md`).
- **Dark Mode** (`frontend/js/theme.js`, `[data-theme="dark"]` block in
  `frontend/css/tokens.css`) — a persisted (localStorage) per-viewer
  preference, default light, toggled from the sidebar. Applies instantly by
  flipping one attribute on `<html>`; no page reload. **Never hardcode a
  color** — always go through the semantic tokens (`--bg-*`, `--text-*`,
  `--border-*`, `--cat-*`, `--status-*`) so both themes stay in sync; the
  dark block in `tokens.css` only overrides that semantic layer, not the
  raw `--gray-*`/`--brand-primary` scale. A FOUC-prevention inline script
  in `index.html`'s `<head>` (before the stylesheets) applies a saved dark
  preference before first paint — keep it in sync with `theme.js`'s
  storage key (`bantayaralan-theme`) if you ever change it.
  **Gotcha that cost real debugging time**: a CSS comment containing a
  literal `*/` substring (e.g. writing `--bg-*/--text-*` in prose) closes
  the comment early and silently truncates everything after it, since CSS
  comments don't nest and browsers drop the resulting garbage without
  throwing any error. If a token/style change in `tokens.css` or
  `styles.css` doesn't seem to apply, check comment/brace balance first:
  `python3 -c "t=open('frontend/css/tokens.css').read(); print(t.count('/*'), t.count('*/'), t.count('{'), t.count('}'))"`.
- **Automated Head-Count Scheduler** (`backend/schedule_config.py`,
  `backend/scheduler.py`) — see the dedicated section below.

## Automated head-count scheduler

Two scheduled events (class-start, final) trigger automatically at
configured times, without any button click — see the finalized prototype
paper's Head Count requirement. Design, in one place per concern:

- **Times**: centralized in `backend/schedule_config.py`
  (`CLASS_START_HEADCOUNT_TIME` = 11:15, `FINAL_HEADCOUNT_TIME` = 14:45,
  plus `CLASS_START`/`CLASS_END`). Change the schedule there only — nothing
  else references a literal time.
- **Trigger loop**: `backend/scheduler.py` runs a single daemon thread
  (`scheduler.start()`, called once from `create_app()`), polling every 15s
  (2s under `BANTAY_TEST_TIME`, see below). It never touches Flask's
  request-handling thread, mirroring how a camera-processing loop would run
  alongside a GUI without blocking it.
- **Idempotence / no repeat triggers**: each tick re-derives status from
  `head_counts` (via `db.get_head_count()`) rather than an in-memory "did I
  already fire" flag — once a row exists for today's (class_date, point),
  the event reads as `complete` and is never re-triggered. This also gives
  the **daily reset** for free: a new calendar date has no row yet, so
  yesterday's completion can never block today.
- **Missed vs. triggered (startup behavior)**: an event only auto-fires if
  it was reached *while the app was running* — `app_start_time <=
  event_time_today <= now`. If the app starts after an event's time has
  already passed today, that event is marked `missed` instead of firing
  retroactively. This is what correctly implements "starting between 11:15
  and 14:45 recognizes class-start already passed and waits for the final
  count" from the spec, without any special-cased date/time logic beyond
  that one comparison.
- **Placeholder capture**: `scheduler._capture_head_count()` is a random
  int simulating a detected count — there is no real camera/detection
  pipeline in this repo (see Context in root `CLAUDE.md`). Swap that one
  function for a real call once a detector exists; nothing else needs to
  change. The resulting row is written via `db.upsert_head_count(...,
  source="scheduled")` — the scheduler is now the *only* caller of this
  helper (a manual-entry API route existed briefly and was removed
  2026-09-24, see [Knowledge/11 - Decisions/Manual Head-Count Entry Removed.md](<../Knowledge/11 - Decisions/Manual Head-Count Entry Removed.md>)).
- **Expected vs. detected**: the GUI only ever shows a detected count.
  There is no expected-student-count feature anywhere in this repo — don't
  invent one; `scheduleCardHtml()` in `headcount.js` hardcodes an em-dash
  for "Expected" on purpose.
- **Testing without waiting for 11:15/14:45**: set `BANTAY_TEST_TIME`
  (accepts `"HH:MM:SS"`, using today's real date, or a full
  `"YYYY-MM-DD HH:MM:SS"`) before starting the app — see "Testing the
  scheduler" under Commands below. Never set this in a real deployment.

## Architecture

- **Backend**: `backend/app.py` — a small Flask app. `create_app()` wires
  routes and calls `init_db()` + `seed()` on startup (idempotent — `seed()`
  no-ops if the DB already has rows). Routes: `/api/summary`, `/api/status`,
  `/api/events`, `/api/events/<id>`, `/api/events/<id>/snapshot.svg`,
  `/api/detection-state` (GET/POST), `/api/headcounts` (GET only — read
  history; no manual-entry write path anymore),
  `/api/headcount-schedule` (GET — today's scheduled-event status),
  `/api/statistics`, `/api/insights`, `/api/suggestions`. `create_app()`
  also starts the background scheduler (`scheduler.start()`).
- **DB**: `backend/db.py` — plain `sqlite3`, three tables: `events`,
  `head_counts` (has a `source` column, `'manual'` or `'scheduled'` — the
  schema still allows `'manual'` for historical/flexibility reasons, but no
  code path writes it anymore; every row is `'scheduled'` going forward),
  `detection_state` (see that file for the exact schema rather than
  duplicating it here). Lives at `data/bantayaralan.db`, created on first
  run.
- **Scheduling**: `backend/schedule_config.py` (times) +
  `backend/scheduler.py` (the background thread/trigger logic) — see
  "Automated head-count scheduler" above.
- **Mock data**: `backend/seed.py` — deterministic-ish random generator
  (fixed seed) producing ~42 synthetic events spread across the last 7 days,
  all 4 categories, with a realistic mix of evidence availability (see
  `EVIDENCE_WEIGHTS`), plus ~10 synthetic head-count sessions
  (`seed_headcounts()`). No student-identifying content anywhere.
- **Frontend**: `frontend/` — plain HTML/CSS/JS, no build step, no
  framework. Hash-based routing (`#/dashboard`, `#/events`,
  `#/events/<id>`, `#/headcount`, `#/insights`) driven by `frontend/js/app.js`.
  Views in `frontend/js/views/*.js` fetch JSON from the Flask API
  (`frontend/js/api.js`) and render via template strings; shared render
  helpers (badges, evidence tags, cards, rows, states) live in
  `frontend/js/components.js`.
- **Two run modes, one codebase**: `run_web.py` (plain browser tab) and
  `run_desktop.py` (native window via optional `pywebview` dependency) both
  serve the exact same Flask app + frontend — this is how "desktop app +
  web app, same information architecture" from the proposal is satisfied
  without maintaining two UIs.

## Design tokens

CSS custom properties in `frontend/css/tokens.css` mirror the token names
used in the (now-abandoned) Figma pass: `--cat-*-fg`/`--cat-*-bg` per event
category, `--space-*`, `--radius-*`, semantic `--bg-*`/`--text-*`. If you
add a new UI element, reuse these variables rather than hardcoding colors or
spacing. The semantic layer (not the raw `--gray-*` scale) is redefined
under a `[data-theme="dark"]` block for Dark Mode — see above.

## Important constraints to preserve

- **No live camera feed on the Dashboard** — it shows summaries/recent
  events only. Don't add a live video/image stream there.
- **Category badges are never color-only** — each one pairs an icon + a
  text label (`categoryBadgeHtml` in `components.js`). Keep that pairing if
  you touch this component.
- **No event-status field** (New/Reviewed/Resolved) — intentionally absent
  per the design brief. Don't add one without checking with the user first.
- **No retention countdown / auto-delete UI** — evidence retention policy is
  an open decision (see root CLAUDE.md "Open decisions"); the UI must not
  imply an expiry that hasn't been decided.
- **No student names/IDs/facial recognition** anywhere — mock data, seed
  script, and placeholder SVGs are all written to stay clear of this; keep
  new mock content the same way. Head Count is aggregate-only for the same
  reason — never add per-student rows.
- **Avoid real-time-alert framing** — copy should read as continuous
  monitoring reviewed periodically (events/reports), not instant alerts or
  live notifications. See `insights.js`'s page subtitle for the pattern.
- **Video evidence is simulated, not real** — `renderVideoTab` in
  `frontend/js/views/eventDetail.js` fakes playback with a JS timer, not an
  actual `<video>` element or file. See `README.md` → "Video evidence —
  backend requirements" before wiring this to anything real.
- **No hardcoded colors** — always use the tokens in `tokens.css` (both the
  light defaults and the `[data-theme="dark"]` overrides) so dark mode
  stays correct automatically. Watch out for the `*/`-inside-a-comment trap
  described under Dark Mode above.
- **No invented "expected" head count** — the Head Count schedule cards
  show only a detected count; leave "Expected" blank until a real
  expected-count feature exists.

## Common failure modes

- If `frontend/index.html` 404s, you're probably running `python
  backend/app.py` directly instead of `run_web.py`/`run_desktop.py` — the
  Flask static route resolves `FRONTEND_DIR` relative to `backend/app.py`'s
  parent, and `create_app()` expects to be imported, not run standalone.
- If mock data looks stale/unchanged after editing `seed.py`, delete
  `data/bantayaralan.db` — `seed()` only populates an empty table.
- Evidence-unavailable rows are intentional (~10% of seeded events per
  `EVIDENCE_WEIGHTS`) — not a bug if you see "Evidence Unavailable" tags.

## Commands

```bash
pip install -r requirements.txt   # Flask only, by default
python run_web.py                 # web app mode — http://127.0.0.1:5057
python run_desktop.py             # desktop window mode — needs `pip install pywebview`
python backend/seed.py            # force-reseed mock data (drops existing rows)
python -m py_compile run_web.py run_desktop.py backend/*.py   # quick syntax check
```

### Testing the scheduler

`BANTAY_TEST_TIME` overrides `scheduler._now()` — never set it in a real
deployment. Delete `data/bantayaralan.db` between runs so each test starts
from a clean day. Poll interval drops to 2s automatically when this is set,
so each case resolves within a few seconds of startup:

```bash
# 1. Idle, before either scheduled time -- both events "waiting"
BANTAY_TEST_TIME="10:00:00" python run_web.py

# 2. App "running through" 11:15 -- class-start auto-fires, final still waits
BANTAY_TEST_TIME="11:15:00" python run_web.py

# 3. App starts fresh at 14:45 -- class-start is marked "missed" (started
#    after its time, not retroactively triggered), final auto-fires
BANTAY_TEST_TIME="14:45:00" python run_web.py
```

Check `/api/headcount-schedule` or the Head Count page after each run. Case
3 is the one that actually exercises the missed-event/startup logic from
the finalized paper's spec — worth checking every time this area changes.

No automated test suite exists yet for this subsystem — testing so far has
been manual (see conversation history: dashboard, filters, search, category
tabs, empty/no-results states, event detail with both available and
unavailable evidence, simulated video playback, and the responsive/mobile
layout were all clicked through and screenshotted in a live browser during
development). If you add tests, this is the place to document how to run
them.
