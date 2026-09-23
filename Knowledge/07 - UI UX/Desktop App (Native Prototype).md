---
tags: [ui, desktop-app, historical]
status: Removed
---

# Desktop App (Native Prototype)

> **Removed 2026-09-23.** `desktop-app/` was deleted from the repository
> once the finalized prototype paper settled the project direction as
> web-only — see [[Web Application as Sole Admin UI]] and
> `Prototype Paper Changes.md`. Nothing in it was reusable: its data layer
> was a verified 1:1 port of `admin-ui/backend/db.py`+`seed.py`, and its
> widgets/icons/snapshot code were verified equivalents of `admin-ui`'s own
> JS. This note is preserved for project-history reference only — the
> paths below no longer exist in the working tree.

`desktop-app/` — **was** the primary admin-UI prototype for a period: a genuine native desktop app, no browser/HTTP/webview involved.

## Stack
PySide6 (Qt for Python). `run.py` creates the `QApplication`, applies a global QSS stylesheet (`app/theme.py`), seeds mock data, shows `MainWindow` (`app/main_window.py`) — a persistent sidebar + `QStackedWidget` content area that swaps in a fresh `DashboardView`/`EventsView`/`EventDetailView` (`app/views.py`) per navigation, mirroring the "re-render per route" approach used in `admin-ui`'s JS.

## Notable modules
- `app/data.py` — mock data layer, ported from `admin-ui/backend/db.py` + `seed.py` with Flask-specific code removed.
- `app/widgets.py` — shared widgets (category badge, evidence tag, stat card, event card/row, state panel) — native equivalent of `admin-ui/frontend/js/components.js`.
- `app/video_player.py` — simulated video-evidence player; its fullscreen button is the one piece of genuinely real OS behavior (`self.window().showFullScreen()`).
- `app/snapshot.py` — placeholder "snapshot evidence" image drawn with `QPainter`, no bundled image assets.
- `app/icons.py` — same small SVG icon set as `admin-ui`, rasterized at runtime via `QtSvg`.

## Why it was built
The user specifically wanted "an application only, instead of an app that views the web" — see [[Desktop App as Primary Admin UI Prototype]].

## Verification note
As of the last recorded check, this app had been syntax-checked and launched without a startup traceback, but **not** visually clicked through in that session (native OS windows weren't screenshot-able by the tools available then) — treat a full click-through (Dashboard → Events → filters → Event Detail → both evidence tabs → fullscreen) as still needed before calling it fully verified.

## Status
**Removed** (was **Implemented** as a UI/UX prototype with mock data, and
was the primary prototype, until 2026-09-23).

## Related
- [[Admin UI (Browser Prototype)]]
- [[Two Admin UI Prototypes]] (historical)
- [[Desktop App as Primary Admin UI Prototype]] (reversed)
- [[Web Application as Sole Admin UI]]
