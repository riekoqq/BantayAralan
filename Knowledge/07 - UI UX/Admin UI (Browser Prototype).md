---
tags: [ui, admin-ui]
status: Implemented
---

# Admin UI (Browser Prototype)

`admin-ui/` — the earlier of the two working admin-UI prototypes. Full detail: [admin-ui/CLAUDE.md](../../admin-ui/CLAUDE.md), [admin-ui/README.md](../../admin-ui/README.md).

## Stack
Flask backend (`backend/app.py`) serving a small JSON API + static frontend; plain HTML/CSS/JS frontend (`frontend/`) with hash-based routing (`#/dashboard`, `#/events`, `#/events/<id>`), no build step, no framework.

## Two run modes, one codebase
- `run_web.py` — plain browser tab, `http://127.0.0.1:5057`.
- `run_desktop.py` — native window via optional `pywebview` dependency.

Both serve the exact same Flask app + frontend, which is how "web app + desktop app, same information architecture" is satisfied for this prototype without maintaining two UIs.

## Design tokens
CSS custom properties in `frontend/css/tokens.css` (`--cat-*-fg/bg` per category, `--space-*`, `--radius-*`, semantic `--bg-*`/`--text-*`) — carried over from an earlier, abandoned Figma design pass (cut short by a Figma Starter-plan MCP rate limit).

## Status
**Implemented** as a UI/UX prototype with mock data. Kept as a reference/alternative — superseded as primary prototype by [[Desktop App (Native Prototype)]]. See [[Two Admin UI Prototypes]].

## Related
- [[Desktop App (Native Prototype)]]
- [[06 - Database]]
- [[Evidence System]]
