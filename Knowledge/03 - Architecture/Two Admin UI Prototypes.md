---
tags: [architecture, ui]
status: Working Decision
---

# Two Admin UI Prototypes

BantayAralan has **two independently-built, fully working admin-UI prototypes**, both against the same mock SQLite schema, both implementing Dashboard / Events & Logs / Event Detail:

| | `admin-ui/` | `desktop-app/` |
|---|---|---|
| Tech | Flask (Python) + vanilla HTML/CSS/JS | PySide6 (Qt for Python), no browser/HTTP |
| Run modes | Browser tab (`run_web.py`) or `pywebview`-wrapped window (`run_desktop.py`) | Native OS window only (`run.py`) |
| Data layer | `backend/db.py` + `backend/seed.py`, SQLite via Flask routes | `app/data.py` — ported copy of the same schema/seeding, called in-process |
| Status | Implemented, kept as reference/alternative | Implemented, **current primary prototype** |
| Why it exists | Original click-through prototype after a Figma design pass was cut short by an MCP rate limit | Built because the user specifically wanted "an application only, instead of an app that views the web" |

The two do **not** share a codebase or a running process — `desktop-app/app/data.py` is described in its own comments as "ported" from `admin-ui/backend/db.py` + `seed.py`, with Flask-specific code removed. Changing the schema in one does not change the other; see [[06 - Database]].

## Status
**Working Decision** — `desktop-app` is primary, `admin-ui` is kept as reference. Reason given in the repo: explicit user preference for a real native application over a browser-viewed one.

## May this change?
Not indicated either way in current docs.

## Related
- [[System Architecture]]
- [[06 - Database]]
- [[Admin UI (Browser Prototype)]]
- [[Desktop App (Native Prototype)]]
- [[Desktop App as Primary Admin UI Prototype]]
