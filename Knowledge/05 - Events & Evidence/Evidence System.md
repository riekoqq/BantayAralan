---
tags: [events, evidence]
---

# Evidence System

Each event can (in the data model) have a screenshot and/or a video as evidence. Today, **all evidence is simulated or generated placeholder content** — no real camera imagery exists anywhere in the repository.

## Current implementation (Implemented, simulated)
- **Snapshot evidence**: `admin-ui` serves a generated placeholder SVG per event (`/api/events/<id>/snapshot.svg`, built in `backend/app.py`'s `_placeholder_svg`) — not a real camera frame. (A removed `desktop-app/` prototype drew an equivalent placeholder with `QPainter` — see [[Web Application as Sole Admin UI]].)
- **Video evidence**: fully simulated — `admin-ui`'s `renderVideoTab` (`frontend/js/views/eventDetail.js`) fakes playback with a JS timer. No actual video file or codec is involved.
- **Evidence availability mix**: seeded with `EVIDENCE_WEIGHTS` (~68% both, ~16% snapshot only, ~6% video only, ~10% unavailable) to exercise the "Evidence Unavailable" UI state realistically.

## What real evidence capture would require (documented, not built)
Per `admin-ui/README.md`'s "Video evidence — backend requirements" section:
1. A rolling per-camera frame buffer, so a clip can include time *before* the triggering event.
2. Cutting a clip spanning a defined window around the trigger (e.g. -10s/+10s).
3. Encoding and storing the clip, with a retention/storage strategy — **unresolved**, see [[12 - Open Questions]].
4. Associating the clip with the event row (e.g. a `video_path` column next to `snapshot_available`).
5. Serving it so a real `<video>` element can seek/scrub it — `admin-ui` is structured so this swap is a contained change (`renderVideoTab`).

## Working direction (per current project guidance — not finalized)
- Video evidence is planned/desired.
- Evidence — video and screenshot — is currently intended to be retained **indefinitely**. **This conflicts with existing repo documentation**, which calls retention an open, unresolved decision — see [[12 - Open Questions]] for the unresolved conflict; do not treat "indefinite retention" as settled without checking there first.

## Status
**Implemented** (simulated UI only), **Not Yet Implemented** (real capture/storage), retention policy **Unclear** (see [[12 - Open Questions]]).

## Related
- [[Event Model]]
- [[06 - Database]]
- [[10 - Privacy & Ethics]]
- [[12 - Open Questions]]
