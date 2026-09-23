---
tags: [requirements, ui]
---

# UI Requirements

Current working direction for the admin interface (subject to change — not a finalized spec).

- Admin-only interface, single classroom, single deployment.
- No normal login/logout flow unless a future security requirement forces one — see [[12 - Open Questions]].
- Dashboard, Event history (Events & Logs), Event Detail screens.
- Screenshot evidence and video evidence, both potentially attached to one event.
- Event categories, date/time, short event description shown per event.
- **No live camera feed on the Dashboard** — summaries/recent events only.
- **No event-status field** — see [[No Event-Status Field]].
- Desktop application and web application should provide the **same core functionality**, using different deployment environments — currently realized as two independently-built prototypes (not a shared codebase) — see [[Two Admin UI Prototypes]].

All of the above is confirmed against the current admin-UI implementations — see [[UI UX Overview]].

## Status
**Working Decision** for most items above (see `admin-ui/CLAUDE.md` "Important constraints to preserve" and `desktop-app/CLAUDE.md`, which state these as intentional, checked-with-the-user constraints already implemented in code). Evidence retention display and event-status remain flagged decisions — see [[12 - Open Questions]].

## Related
- [[UI UX Overview]]
- [[Functional Requirements]]
- [[No Event-Status Field]]
