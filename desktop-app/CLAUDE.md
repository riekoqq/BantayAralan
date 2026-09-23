# desktop-app — BantayAralan Native Admin Interface

Status: **Implemented** (as a UI/UX prototype with mock data — not connected
to any real detection pipeline). See root [`CLAUDE.md`](../CLAUDE.md) for the
project-wide working-draft/status-label rules; this file assumes you've read
those. See also [`../admin-ui/CLAUDE.md`](../admin-ui/CLAUDE.md) — the
earlier browser-based prototype this one was built to replace ("an
application only, instead of an app that views the web").

## Purpose

A genuine native desktop GUI (PySide6/Qt) implementing the same Dashboard /
Events & Logs / Event Detail admin interface as `../admin-ui`, but with no
browser, no HTTP server, and no webview involved — it's a normal OS window
that talks to a local SQLite file in-process.

## Architecture

- **Entry point**: `run.py` — creates the `QApplication`, applies the global
  stylesheet (`app/theme.py`), seeds mock data, shows `MainWindow`.
- **`app/main_window.py`** — `QMainWindow` with a persistent sidebar
  (wordmark, nav buttons, system-status box) and a `QStackedWidget` content
  area. Navigation (`go_dashboard`/`go_events`/`go_event_detail`) builds a
  **fresh view instance** each time and swaps it into the stack — no
  in-place refresh/diffing logic, mirroring the "re-render per route"
  approach used in `../admin-ui`'s JS.
- **`app/views.py`** — `DashboardView`, `EventsView`, `EventDetailView`.
  Each does its own (tiny, local-sqlite-fast) data load on a short
  `QTimer.singleShot` delay so the loading state is genuinely visible, not
  just written and never shown.
- **`app/data.py`** — the mock data layer: schema, seeding (`seed()`,
  idempotent — no-ops if already seeded), and query functions
  (`get_summary`, `list_events`, `get_event`, `get_status`). Ported from
  `../admin-ui/backend/db.py` + `seed.py`, with the Flask-specific bits
  removed — this is the data layer both prototypes conceptually share.
- **`app/widgets.py`** — shared small widgets (category badge, evidence
  tag, stat card, event card, event row, state panel) — the native
  equivalent of `../admin-ui/frontend/js/components.js`.
- **`app/video_player.py`** — the simulated video-evidence player. Its
  fullscreen button is the one piece of genuinely real OS behavior here —
  it calls `self.window().showFullScreen()`, not a fake state.
- **`app/snapshot.py`** — draws the placeholder "snapshot evidence" image
  with `QPainter` (category-colored icon + caption), no bundled image
  assets.
- **`app/icons.py`** — the same small SVG icon set as
  `../admin-ui/frontend/js/icons.js`, rasterized at runtime via `QtSvg`
  (`QSvgRenderer`) instead of being inlined into HTML.
- **`app/theme.py`** — design tokens as Python constants + one QSS
  stylesheet string, mirroring `../admin-ui/frontend/css/tokens.css`'s
  values so both prototypes read as the same visual language.

## Important constraints to preserve

Same substantive constraints as `../admin-ui/CLAUDE.md` — no live camera
feed on the Dashboard, category badges always icon+label (never color
alone), no event-status field, no retention countdown/auto-delete UI, no
student names/IDs/facial recognition anywhere, video evidence is simulated
and must stay clearly labeled as such until a real capture pipeline exists.

## Common failure modes

- If nothing appears on launch, check the terminal for a traceback before
  assuming it's silently running — `python run.py` blocks in `app.exec()`
  with no console output on success.
- If mock data looks stale after editing `app/data.py`'s `CATEGORY_CONTENT`
  or `EVIDENCE_WEIGHTS`, delete `data/bantayaralan.db` — `seed()` only
  populates an empty table.
- QSS dynamic-property selectors (`[active="true"]` on nav buttons / tabs)
  need `style().unpolish()` + `style().polish()` after `setProperty()` to
  repaint — every place that toggles `active`/`unavailable` in this codebase
  already does this; keep the pattern if you add more toggled states.
- `EventDetailView` and `VideoPlayer` own a `QTimer` — `MainWindow._set_view`
  calls `old.cleanup()` before discarding a view specifically to stop it;
  if you add another view with a running timer, give it a `cleanup()` too.

## Commands

```bash
pip install -r requirements.txt        # PySide6 only, by default
python run.py                          # launch the app
python -m py_compile run.py app/*.py   # quick syntax check
```

No automated test suite exists yet. Verification so far has been: syntax
compiling all modules, launching the app in the background and confirming
no startup traceback plus a successfully seeded `data/bantayaralan.db` file
— **not** a visual on-screen check, since this session's tools can capture
browser-pane screenshots but not arbitrary native OS windows. Do a real
visual pass (launch it, click through Dashboard → Events → filters →
Event Detail → both evidence tabs → fullscreen toggle) before treating this
as fully verified.
