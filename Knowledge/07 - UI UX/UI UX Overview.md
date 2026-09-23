---
tags: [ui, ux]
---

# UI UX Overview

Current working direction for the BantayAralan admin interface — verified against the two implemented prototypes, [[Admin UI (Browser Prototype)]] and [[Desktop App (Native Prototype)]]. See also [[UI Requirements]] for the requirement-style list.

## Confirmed, implemented working directions
- Admin-only interface — no student-facing UI anywhere in the repo.
- No login/logout flow — intentionally out of scope in both prototypes ("admin-only, single deployment, no user management").
- Three screens: Dashboard, Events & Logs (event history), Event Detail.
- Event Detail shows screenshot evidence and video evidence in separate tabs.
- Every event card/row shows category, date/time, and a short description.
- **No live camera feed on the Dashboard** — Dashboard shows summaries and recent events only. This is called out explicitly as a constraint to preserve in both subsystem `CLAUDE.md` files.
- One classroom only — no multi-classroom/multi-camera selector anywhere in either UI.
- Desktop application and web application provide the same core functionality (Dashboard/Events/Event Detail, same data model) but via **two separately-built codebases**, not one shared frontend — see [[Two Admin UI Prototypes]].
- Category badges are never color-only — always icon + text label, in both implementations.

## Unresolved / not settled
- **No event-status field** (New/Reviewed/Resolved) exists today — explicitly called an intentional omission "per the design brief" in both `CLAUDE.md` files, but also explicitly flagged there as something not to add "without checking with the user first," implying it's not permanently closed. See [[No Event-Status Field]].
- **Retention/expiry UI**: both `CLAUDE.md` files say not to add a "retention countdown / auto-delete UI" because "evidence retention policy is an open decision" — but see [[12 - Open Questions]] for a conflict between that and other current guidance.

## Status
**Implemented** for the confirmed items above; **Under Consideration** for event-status and retention display.

## Related
- [[Admin UI (Browser Prototype)]]
- [[Desktop App (Native Prototype)]]
- [[UI Requirements]]
- [[Two Admin UI Prototypes]]
- [[Event Model]]
- [[12 - Open Questions]]
