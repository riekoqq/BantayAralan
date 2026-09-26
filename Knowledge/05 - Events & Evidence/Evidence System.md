---
tags: [events, evidence]
---

# Evidence System

Each event can (in the data model) have a screenshot and/or a video as evidence. Today, **all evidence is simulated or generated placeholder content** — no real camera imagery exists anywhere in the repository.

## Current implementation
- **Snapshot evidence — partially real as of 2026-09-26**: `admin-ui` serves
  `/api/events/<id>/snapshot`. For seeded/mock events this is still a
  generated placeholder SVG (`backend/app.py`'s `_placeholder_svg`) — not a
  real camera frame. (A removed `desktop-app/` prototype drew an equivalent
  placeholder with `QPainter` — see [[Web Application as Sole Admin UI]].)
  But for real events created by `detection/monitor_trash.py`, this now
  serves an **actual captured frame** (`admin-ui/data/snapshots/<id>.jpg`,
  with the triggering detection box drawn on it) — see
  [[Trash Monitoring Integration]]. Same URL either way; the route checks
  whether a real file exists and falls back to the placeholder if not.
  **No face/identity redaction is applied** to these real captures — see
  the privacy caveat in [[Trash Monitoring Integration]] and
  [.claude/rules/privacy-and-ethics.md](../../.claude/rules/privacy-and-ethics.md);
  this is a known, flagged gap, not an oversight.
- **Video evidence**: fully simulated — `admin-ui`'s `renderVideoTab` (`frontend/js/views/eventDetail.js`) fakes playback with a JS timer. No actual video file or codec is involved, for either mock or real events.
- **Evidence availability mix**: seeded events use `EVIDENCE_WEIGHTS` (~68% both, ~16% snapshot only, ~6% video only, ~10% unavailable) to exercise the "Evidence Unavailable" UI state realistically. Real `monitor_trash.py` events always have `video_available=0` (no video capture exists) and `snapshot_available=1` only when the frame save succeeds.

## What real evidence capture would require (documented, not built)
Per `admin-ui/README.md`'s "Video evidence — backend requirements" section:
1. A rolling per-camera frame buffer, so a clip can include time *before* the triggering event.
2. Cutting a clip spanning a defined window around the trigger (e.g. -10s/+10s).
3. Encoding and storing the clip. The storage *location* is now decided — local disk/local object storage, not a cloud bucket, per [[Local Hosting for Database and Object Storage]] — but the retention *policy* (how long to keep it) remains **unresolved**, see [[12 - Open Questions]].
4. Associating the clip with the event row (e.g. a `video_path` column next to `snapshot_available`).
5. Serving it so a real `<video>` element can seek/scrub it — `admin-ui` is structured so this swap is a contained change (`renderVideoTab`).

## Working direction (per current project guidance — not finalized)
- Video evidence is planned/desired.
- Evidence — video and screenshot — is currently intended to be retained **indefinitely**. **This conflicts with existing repo documentation**, which calls retention an open, unresolved decision — see [[12 - Open Questions]] for the unresolved conflict; do not treat "indefinite retention" as settled without checking there first.

## Status
**Partially implemented**: snapshot evidence is now Implemented (real
capture) for `trash` events via `detection/monitor_trash.py`; still
simulated-only for every other category. Video evidence remains **Not Yet
Implemented** (fully simulated) for all events. Retention policy
**Unclear** (see [[12 - Open Questions]]) — real snapshot files are
currently kept indefinitely by default (nothing deletes them), which is
worth revisiting once that policy question is actually resolved.

## Related
- [[Event Model]]
- [[06 - Database]]
- [[10 - Privacy & Ethics]]
- [[12 - Open Questions]]
- [[Trash Monitoring Integration]]
