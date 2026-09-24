---
tags: [hardware]
status: Working Decision (camera model) / Proposal Requirement (rest)
---

# Hardware

Most items below are still from the proposal's working draft — **no hardware integration exists in this repository**; nothing here has been procured, tested, or connected to any code. One item is now a confirmed team decision (2026-09-24, communicated directly by the project team, not yet reflected in the proposal PDF or prototype paper text).

## Confirmed (Working Decision, 2026-09-24)
- **Camera model: TP-Link VIGI C320I** — a PoE (Power over Ethernet) dome network camera. Communicated directly by the project team; not yet written into the proposal or prototype paper documents.
- **Open sub-question**: whether this same model covers *both* proposed camera roles (ceiling-mounted behavior camera and top-down clutter/alignment camera) or only one of them — not specified when this decision was communicated. Don't assume both roles use this model until confirmed.
- **Networking implication**: a PoE camera implies a PoE switch/injector and Ethernet-based ingest (not USB or direct analog capture) — this is an inference from the camera choice, not yet independently confirmed as the project's networking plan. Camera ingest protocol (e.g., RTSP/ONVIF, common for PoE IP cameras like this one) is still not documented anywhere as a project decision — see [[12 - Open Questions]].

## Components (proposed, still otherwise unspecified)
- **Ceiling-mounted camera** — captures student behavior across the classroom.
- **Top-down camera** — detects clutter and monitors desk/seat alignment.
- **Computer/laptop** — processes video input and runs the system.

## Not documented anywhere yet
- Whether the TP-Link VIGI C320I covers one or both camera roles.
- The camera's ingest/streaming protocol as actually used by this project (the model itself typically supports RTSP/ONVIF, but no project document confirms which is used).
- Minimum processing-hardware specs (CPU/GPU) needed to run the detection/tracking pipeline in real time.
- Physical mounting/installation details beyond "ceiling-mounted" and "top-down."

Do not assume specifications beyond what's listed above — see [[12 - Open Questions]] for "final camera POV" as an unresolved item.

## Status
**Working Decision**: camera model (TP-Link VIGI C320I, PoE). **Proposal Requirement**, still unspecified: everything else in this note.

## Related
- [[04 - Computer Vision]]
- [[System Architecture]]
- [[12 - Open Questions]]
