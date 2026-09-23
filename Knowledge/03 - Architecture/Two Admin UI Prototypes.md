---
tags: [architecture, ui, historical]
status: Historical / Superseded
---

# Two Admin UI Prototypes

> **Historical.** This note describes a period (through 2026-09-23) when
> BantayAralan had two parallel admin-UI prototypes. `desktop-app/` was
> **removed** on 2026-09-23 once the finalized prototype paper settled the
> project direction as web-only — see
> [[Web Application as Sole Admin UI]] and `Prototype Paper Changes.md`.
> `admin-ui/` is now the sole admin UI. The content below is preserved for
> project-history reference; don't treat it as describing the current repo.

BantayAralan **had two independently-built, fully working admin-UI prototypes** (through 2026-09-23), both against the same mock SQLite schema, both implementing Dashboard / Events & Logs / Event Detail:

| | `admin-ui/` | `desktop-app/` |
|---|---|---|
| Tech | Flask (Python) + vanilla HTML/CSS/JS | PySide6 (Qt for Python), no browser/HTTP |
| Run modes | Browser tab (`run_web.py`) or `pywebview`-wrapped window (`run_desktop.py`) | Native OS window only (`run.py`) |
| Data layer | `backend/db.py` + `backend/seed.py`, SQLite via Flask routes | `app/data.py` — ported copy of the same schema/seeding, called in-process |
| Status | Implemented, kept as reference/alternative | Implemented, **current primary prototype** |
| Why it exists | Original click-through prototype after a Figma design pass was cut short by an MCP rate limit | Built because the user specifically wanted "an application only, instead of an app that views the web" |

The two do **not** share a codebase or a running process — `desktop-app/app/data.py` is described in its own comments as "ported" from `admin-ui/backend/db.py` + `seed.py`, with Flask-specific code removed. Changing the schema in one does not change the other; see [[06 - Database]].

## Status
**Historical.** `desktop-app` was primary for a period, then removed
2026-09-23 in favor of `admin-ui` as sole UI — see
[[Desktop App as Primary Admin UI Prototype]] (reversed) and
[[Web Application as Sole Admin UI]] (current decision).

## May this change?
The current decision ([[Web Application as Sole Admin UI]]) could itself be
revisited by the project team/adviser, same as any working decision — but
there is no plan to restore a separate desktop app noted anywhere.

## Related
- [[System Architecture]]
- [[06 - Database]]
- [[Admin UI (Browser Prototype)]]
- [[Desktop App (Native Prototype)]]
- [[Desktop App as Primary Admin UI Prototype]]
- [[Web Application as Sole Admin UI]]
