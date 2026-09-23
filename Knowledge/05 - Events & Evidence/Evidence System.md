---
tags: [events, evidence]
---

# Evidence System

Each event can (in the data model) have a screenshot and/or a video as evidence. Today, **all evidence is simulated or generated placeholder content** — no real camera imagery exists anywhere in the repository.

## Current implementation (Implemented, simulated)
- **Snapshot evidence**: `admin-ui` serves a generated placeholder SVG per event (`/api/events/<id>/snapshot.svg`, built in `backend/app.py`'s `_placeholder_svg`); `desktop-app` draws an equivalent placeholder at runtime with `QPainter` (`app/snapshot.py`). Neither is a real camera frame.
- **Video evidence**: fully simulated in both UIs — `admin-ui`'s `renderVideoTab` (`frontend/js/views/eventDetail.js`) fakes playback with a JS timer; `desktop-app`'s `app/video_player.py` does the same with a `QTimer`, though its fullscreen toggle is genuinely real OS behavior. No actual video file or codec is involved in either.
- **Evidence availability mix**: seeded with `EVIDENCE_WEIGHTS` (~68% both, ~16% snapshot only, ~6% video only, ~10% unavailable) to exercise the "Evidence Unavailable" UI state realistically.

## What real evidence capture would require (documented, not built)
Per both subsystem READMEs' "Video evidence — backend requirements" sections:
1. A rolling per-camera frame buffer, so a clip can include time *before* the triggering event.
2. Cutting a clip spanning a defined window around the trigger (e.g. -10s/+10s).
3. Encoding and storing the clip, with a retention/storage strategy — **unresolved**, see [[12 - Open Questions]].
4. Associating the clip with the event row (e.g. a `video_path` column next to `snapshot_available`).
5. Serving it so a real `<video>` element (web) or Qt Multimedia (`QMediaPlayer`/`QVideoWidget`, desktop) can seek/scrub it. Both UIs are structured so this swap is a contained change (`renderVideoTab`, `video_player.py`).

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
