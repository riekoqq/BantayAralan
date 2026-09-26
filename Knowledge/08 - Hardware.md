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

## Confirmed (Working Decision, 2026-09-26)
- **Network switch: TP-Link TL-SG1005LP** — a 5-port Gigabit desktop switch with 4 PoE+ ports (40 W total PoE budget). Communicated directly by the project team. Confirms the PoE-switch inference above as an actual hardware choice rather than just an implication of the camera model.
- **Processing PC — full specification**, communicated directly by the project team:
  - **CPU**: AMD Ryzen 5 5600
  - **GPU**: NVIDIA GeForce RTX 2060
  - **RAM**: 16 GB, 3200 MHz (Team Group Vulcan Z)
  - **Storage**: 256 GB M.2 SSD (Team Group TM8PS7512G) + 1 TB HDD (Seagate ST31000524AS)
  - Form factor (desktop vs. laptop) is not explicitly stated; the discrete-GPU + separate SSD/HDD configuration implies a desktop tower, but this is an inference, not a confirmed fact.

## Components (proposed, still otherwise unspecified)
- **Ceiling-mounted camera** — captures student behavior across the classroom.
- **Top-down camera** — detects clutter and monitors desk/seat alignment.
- **Computer** — processes video input and runs the system. CPU/GPU/RAM/storage are now confirmed (above); exact form factor (desktop/laptop) and which drive (SSD vs. HDD) would host the database/evidence store are not.

## Not documented anywhere yet
- Whether the TP-Link VIGI C320I covers one or both camera roles.
- The camera's ingest/streaming protocol as actually used by this project (the model itself typically supports RTSP/ONVIF, but no project document confirms which is used).
- Processing PC's physical form factor, and which drive (the 256 GB SSD or the 1 TB HDD) is intended to host the local database/evidence store.
- Physical mounting/installation details beyond "ceiling-mounted" and "top-down."

Do not assume specifications beyond what's listed above — see [[12 - Open Questions]] for "final camera POV" as an unresolved item.

## Status
**Working Decision**: camera model (TP-Link VIGI C320I, PoE), network switch (TL-SG1005LP), processing PC (Ryzen 5 5600 / RTX 2060 / 16 GB RAM / 256 GB SSD + 1 TB HDD). **Proposal Requirement**, still unspecified: everything else in this note.

## Related
- [[04 - Computer Vision]]
- [[System Architecture]]
- [[12 - Open Questions]]
- [[Network Switch and Processing PC Specs Confirmed]]
