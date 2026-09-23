---
tags: [ui, admin-ui]
status: Implemented
---

# Admin UI (Browser Prototype)

`admin-ui/` — the **sole and primary** BantayAralan admin UI. Full detail: [admin-ui/CLAUDE.md](../../admin-ui/CLAUDE.md), [admin-ui/README.md](../../admin-ui/README.md).

## Stack
Flask backend (`backend/app.py`) serving a small JSON API + static frontend; plain HTML/CSS/JS frontend (`frontend/`) with hash-based routing (`#/dashboard`, `#/events`, `#/events/<id>`, `#/headcount`, `#/insights`), no build step, no framework.

## Screens
Dashboard, Events & Logs, Event Detail, Head Count (aggregate start/end-of-class counts — automatically scheduled, plus a manual-entry form; see [[Automated Head-Count Scheduler]]), and Insights & Statistics (Statistics / Classroom Insights / Suggestions tabs), plus a Detection Enable/Disable control and a dark-mode toggle in the sidebar. See [admin-ui/CLAUDE.md](../../admin-ui/CLAUDE.md) for the routes/tables behind each.

## Two run modes, one codebase
- `run_web.py` — plain browser tab, `http://127.0.0.1:5057`.
- `run_desktop.py` — native window via optional `pywebview` dependency.

Both serve the exact same Flask app + frontend, which is how "web app + desktop app, same information architecture" is satisfied for this prototype without maintaining two UIs.

## Design tokens and dark mode
CSS custom properties in `frontend/css/tokens.css` (`--cat-*-fg/bg` per category, `--space-*`, `--radius-*`, semantic `--bg-*`/`--text-*`/`--border-*`/`--status-*`) — carried over from an earlier, abandoned Figma design pass (cut short by a Figma Starter-plan MCP rate limit). The semantic layer (not the raw `--gray-*` neutral scale) is redefined under a `:root[data-theme="dark"]` block for **Dark Mode**: a sidebar toggle (`frontend/js/theme.js`, `renderSidebar()` in `app.js`) flips a `data-theme` attribute on `<html>`, persisted per-browser in `localStorage` (`bantayaralan-theme`), applied instantly with no reload. A small inline script in `index.html`'s `<head>` applies a saved dark preference before first paint to avoid a light-then-dark flash. Default is light. No component hardcodes a color — everything goes through these tokens, so both themes stay in sync automatically.

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
- [[Automated Head-Count Scheduler]]
