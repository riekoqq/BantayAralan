---
tags: [requirements, ui]
---

# UI Requirements

Current working direction for the admin interface (subject to change — not a finalized spec).

- Admin-only interface, single classroom, single deployment.
- No normal login/logout flow unless a future security requirement forces one — see [[12 - Open Questions]].
- Dashboard, Events & Logs, Event Detail, Head Count, and Insights &
  Statistics screens, plus a Detection Enable/Disable control.
- Screenshot evidence and video evidence, both potentially attached to one event.
- Event categories, date/time, short event description shown per event.
- **No live camera feed on the Dashboard** — summaries/recent events only.
- **No event-status field** — see [[No Event-Status Field]].
- A light/dark theme toggle, default light, persisted per-browser.
- ~~Desktop application and web application should provide the same core
  functionality, using different deployment environments — currently
  realized as two independently-built prototypes (not a shared codebase).~~
  **No longer applicable.** The finalized prototype paper settled this in
  favor of a single web application; the native desktop prototype was
  removed 2026-09-23 — see [[Web Application as Sole Admin UI]] and
  [[Two Admin UI Prototypes]] (now historical). `admin-ui/`'s own two run
  modes (`run_web.py`, `run_desktop.py`) are two windows onto the *same*
  web app, not two separate UIs.

All of the above is confirmed against the current admin-UI implementation — see [[UI UX Overview]].

## Status
**Working Decision** for most items above (see `admin-ui/CLAUDE.md` "Important constraints to preserve", which states these as intentional, checked-with-the-user constraints already implemented in code). Evidence retention display and event-status remain flagged decisions — see [[12 - Open Questions]].

## Related
- [[UI UX Overview]]
- [[Functional Requirements]]
- [[No Event-Status Field]]
- [[Web Application as Sole Admin UI]]
- [[Automated Head-Count Scheduler]]
