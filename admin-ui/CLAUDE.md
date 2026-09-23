# admin-ui — BantayAralan Admin Interface Prototype

Status: **Implemented** (as a UI/UX prototype with mock data — not connected
to any real detection pipeline). See root [`CLAUDE.md`](../CLAUDE.md) for the
project-wide working-draft/status-label rules; this file assumes you've read
those.

## Purpose

A working, click-through admin interface for BantayAralan: Dashboard,
Events & Logs, and Event Detail (video + screenshot evidence tabs). Built to
demonstrate the intended UI/UX for the thesis project after the original
Figma-based design pass was cut short by a Figma Starter-plan MCP rate
limit. One classroom, admin-only, no login flow, no student identification
anywhere — per the design brief this was built from.

## Architecture

- **Backend**: `backend/app.py` — a small Flask app. `create_app()` wires
  routes and calls `init_db()` + `seed()` on startup (idempotent — `seed()`
  no-ops if the DB already has rows).
- **DB**: `backend/db.py` — plain `sqlite3`, one `events` table (see that
  file for the exact schema rather than duplicating it here). Lives at
  `data/bantayaralan.db`, created on first run.
- **Mock data**: `backend/seed.py` — deterministic-ish random generator
  (fixed seed) producing ~42 synthetic events spread across the last 7 days,
  all 4 categories, with a realistic mix of evidence availability (see
  `EVIDENCE_WEIGHTS`). No student-identifying content anywhere.
- **Frontend**: `frontend/` — plain HTML/CSS/JS, no build step, no
  framework. Hash-based routing (`#/dashboard`, `#/events`,
  `#/events/<id>`) driven by `frontend/js/app.js`. Views in
  `frontend/js/views/*.js` fetch JSON from the Flask API (`frontend/js/api.js`)
  and render via template strings; shared render helpers (badges, evidence
  tags, cards, rows, states) live in `frontend/js/components.js`.
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
spacing.

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
  new mock content the same way.
- **Video evidence is simulated, not real** — `renderVideoTab` in
  `frontend/js/views/eventDetail.js` fakes playback with a JS timer, not an
  actual `<video>` element or file. See `README.md` → "Video evidence —
  backend requirements" before wiring this to anything real.

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

No automated test suite exists yet for this subsystem — testing so far has
been manual (see conversation history: dashboard, filters, search, category
tabs, empty/no-results states, event detail with both available and
unavailable evidence, simulated video playback, and the responsive/mobile
layout were all clicked through and screenshotted in a live browser during
development). If you add tests, this is the place to document how to run
them.
