---
tags: [ui, desktop-app]
status: Implemented
---

# Desktop App (Native Prototype)

`desktop-app/` — the current **primary** admin-UI prototype: a genuine native desktop app, no browser/HTTP/webview involved. Full detail: [desktop-app/CLAUDE.md](../../desktop-app/CLAUDE.md), [desktop-app/README.md](../../desktop-app/README.md).

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
**Implemented** as a UI/UX prototype with mock data — current primary prototype.

## Related
- [[Admin UI (Browser Prototype)]]
- [[Two Admin UI Prototypes]]
- [[Desktop App as Primary Admin UI Prototype]]
