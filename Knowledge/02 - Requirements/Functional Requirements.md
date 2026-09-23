---
tags: [requirements]
---

# Functional Requirements

Distinguishes what the proposal specifies the finished system should do from what the current admin-UI prototypes actually implement.

## Proposal requirements (not yet implemented)
| Requirement | Status |
|---|---|
| Real-time detection of disruptive behavior (e.g. standing) from a live camera feed | Not yet implemented |
| Real-time detection of clutter/scattered objects | Not yet implemented |
| Real-time seat/table misalignment detection vs. reference positions | Not yet implemented |
| Object tracking across frames (ByteTrack) | Not yet implemented |
| Automatic event logging to a database on detection | Not yet implemented (mock data is pre-seeded, not detector-generated) |
| Automatic snapshot/video capture on event | Not yet implemented (both UIs simulate playback of evidence that doesn't exist) |
| Real-time teacher alerting | Not yet implemented |
| Annotated live video display in GUI | Not yet implemented |

See [[04 - Computer Vision]] and [[Event Model]].

## Implemented (admin UI prototypes only)
| Requirement | Status | Where |
|---|---|---|
| Dashboard: summary stats, recent events, category breakdown | Implemented (mock data) | `admin-ui/frontend/js/views/dashboard.js`, `desktop-app/app/views.py` |
| Events & Logs: filter by category/date range, search, sort | Implemented (mock data) | `admin-ui/backend/app.py` `list_events`, `desktop-app/app/data.py` `list_events` |
| Event Detail: description, timestamp, screenshot tab, video tab | Implemented (mock/simulated evidence) | `admin-ui/frontend/js/views/eventDetail.js`, `desktop-app/app/views.py` |
| System status panel (camera/detection/DB) | Implemented, but **hardcoded-true mock values**, not real status | `admin-ui/backend/app.py` `status()`, `desktop-app/app/data.py` `get_status()` |

## Status
**Mixed** — see each row. The admin UIs implement the *review/browse* side of the system against synthetic data; none of the *detection* side exists.

## Related
- [[Research Questions & Objectives]]
- [[UI UX Overview]]
- [[04 - Computer Vision]]
- [[Non-Functional Requirements]]
