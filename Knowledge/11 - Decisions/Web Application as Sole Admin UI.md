# Web Application as Sole Admin UI

## Status
Working Decision (2026-09-23)

## Decision
`admin-ui/` (Flask + vanilla JS web application) is the **sole and primary**
BantayAralan admin UI. `desktop-app/` (PySide6 native prototype) has been
**removed** from the repository, not just demoted.

## Reason
The finalized `BantayAralan-Prototype-Paper` resolves open issue 1 from
`Prototype Paper Changes.md` ("Web application vs. desktop-primary
direction") in favor of a web application, grounded in the already-existing
`admin-ui/` prototype. This directly reverses
[[Desktop App as Primary Admin UI Prototype]], which had made the opposite
call based on an explicit earlier user preference for a native application.

Before deleting `desktop-app/`, its contents were checked for reusable
logic: `app/data.py` was a verified 1:1 port of `admin-ui/backend/db.py` +
`seed.py`; `app/snapshot.py`, `app/icons.py`, and `app/widgets.py` were
verified equivalents of `admin-ui`'s `_placeholder_svg()`, `icons.js`, and
`components.js`. Nothing outside `desktop-app/` imported from it. Nothing
worth porting was found — the deletion carried no functional loss.

At the same time, `admin-ui/` was extended to cover the finalized paper's
remaining IA that neither prototype had yet: aggregate Head Count, a
Detection Enable/Disable control, and a Statistics/Classroom
Insights/Suggestions page — see `admin-ui/CLAUDE.md`.

## Alternatives
- Keep both prototypes, demote `desktop-app/` further instead of deleting —
  rejected because the instruction was explicit: "do not keep `desktop-app/`
  merely for compatibility or historical fallback," and an unused duplicate
  UI implementation would just be dead weight in a one-classroom prototype.
- Rebuild the new features in `desktop-app/` instead of `admin-ui/` —
  rejected; the finalized paper explicitly frames the system as a web
  application (Flask, matching `admin-ui/`'s existing stack).

## May Change?
Yes, in principle, same as any working decision — but there is no
indication anywhere in current docs that a return to a native desktop app
is planned.

## Change Trigger
Further explicit direction from the project team/adviser reopening the
web-vs-desktop question (none recorded as of this writing).

## Related
- [[Desktop App as Primary Admin UI Prototype]] (reversed by this decision)
- [[Two Admin UI Prototypes]] (historical)
- [[Desktop App (Native Prototype)]] (historical — removed)
- [[Admin UI (Browser Prototype)]]
- `Prototype Paper Changes.md` (open issue 1 — now resolved)
