---
tags: [ui, admin-ui]
status: Implemented
---

# Admin UI (Browser Prototype)

`admin-ui/` — the **sole and primary** BantayAralan admin UI. Full detail: [admin-ui/CLAUDE.md](../../admin-ui/CLAUDE.md), [admin-ui/README.md](../../admin-ui/README.md).

## Stack
Flask backend (`backend/app.py`) serving a small JSON API + static frontend; plain HTML/CSS/JS frontend (`frontend/`) with hash-based routing (`#/dashboard`, `#/events`, `#/events/<id>`, `#/headcount`, `#/insights`), no build step, no framework.

## Screens
Dashboard, Events & Logs, Event Detail, Head Count (aggregate start/end-of-class counts), and Insights & Statistics (Statistics / Classroom Insights / Suggestions tabs), plus a Detection Enable/Disable control in the sidebar. See [admin-ui/CLAUDE.md](../../admin-ui/CLAUDE.md) for the routes/tables behind each.

## Two run modes, one codebase
- `run_web.py` — plain browser tab, `http://127.0.0.1:5057`.
- `run_desktop.py` — native window via optional `pywebview` dependency.

Both serve the exact same Flask app + frontend, which is how "web app + desktop app, same information architecture" is satisfied for this prototype without maintaining two UIs.

## Design tokens
CSS custom properties in `frontend/css/tokens.css` (`--cat-*-fg/bg` per category, `--space-*`, `--radius-*`, semantic `--bg-*`/`--text-*`) — carried over from an earlier, abandoned Figma design pass (cut short by a Figma Starter-plan MCP rate limit).

## Status
**Implemented** as a UI/UX prototype with mock data — **sole and primary
admin UI**. A separate native prototype ([[Desktop App (Native Prototype)]])
was primary for a period and was removed 2026-09-23; see
[[Two Admin UI Prototypes]] (historical) and
[[Web Application as Sole Admin UI]].

## Related
- [[Desktop App (Native Prototype)]] (historical)
- [[06 - Database]]
- [[Evidence System]]
