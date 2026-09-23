---
tags: [ui, ux]
---

# UI UX Overview

Current working direction for the BantayAralan admin interface — verified
against the implemented web application, [[Admin UI (Browser Prototype)]].
A separate native desktop prototype ([[Desktop App (Native Prototype)]])
existed through 2026-09-23 and was removed once the finalized prototype
paper settled the direction as web-only; it's kept only as historical
reference (see [[Two Admin UI Prototypes]]). See also [[UI Requirements]]
for the requirement-style list.

## Confirmed, implemented working directions
- Admin-only interface — no student-facing UI anywhere in the repo.
- No login/logout flow — intentionally out of scope ("admin-only, single deployment, no user management").
- Five screens: Dashboard, Events & Logs (event history), Event Detail, Head Count, and Insights & Statistics (Statistics / Classroom Insights / Suggestions tabs).
- A Detection Enable/Disable control (sidebar) gates event generation only — not cameras, not the app, not head counting.
- Event Detail shows screenshot evidence and video evidence in separate tabs.
- Every event card/row shows category, date/time, and a short description.
- **No live camera feed on the Dashboard** — Dashboard shows summaries and recent events only. This is called out explicitly as a constraint to preserve in `admin-ui/CLAUDE.md`.
- Head Count is **aggregate only** — beginning/end-of-class counts, no per-student rows, names, or IDs. Recorded exclusively by a background scheduler at configured times — no manual-entry form exists — see [[Automated Head-Count Scheduler]] and [[Manual Head-Count Entry Removed]].
- Copy avoids real-time-alert framing — continuous monitoring reviewed periodically (events/reports), not instant alerts.
- One classroom only — no multi-classroom/multi-camera selector.
- Category badges are never color-only — always icon + text label.
- A light/dark theme toggle (sidebar) — default light, persisted per-browser, applies instantly, no hardcoded colors anywhere (see [[Admin UI (Browser Prototype)]] → Design tokens).

## Unresolved / not settled
- **No event-status field** (New/Reviewed/Resolved) exists today — explicitly called an intentional omission "per the design brief" in `admin-ui/CLAUDE.md`, but also explicitly flagged there as something not to add "without checking with the user first," implying it's not permanently closed. See [[No Event-Status Field]].
- **Retention/expiry UI**: `admin-ui/CLAUDE.md` says not to add a "retention countdown / auto-delete UI" because "evidence retention policy is an open decision" — but see [[12 - Open Questions]] for a conflict between that and other current guidance.
- **Head-count duplicate handling, statistics/insights methodology, and the detection toggle's exact backend scope** are all explicitly open per `Prototype Paper Changes.md` — see [[12 - Open Questions]].

## Status
**Implemented** for the confirmed items above; **Under Consideration** for event-status, retention display, and the three open items just above.

## Related
- [[Admin UI (Browser Prototype)]]
- [[Desktop App (Native Prototype)]] (historical)
- [[UI Requirements]]
- [[Two Admin UI Prototypes]] (historical)
- [[Event Model]]
- [[Automated Head-Count Scheduler]]
- [[Manual Head-Count Entry Removed]]
- [[12 - Open Questions]]
