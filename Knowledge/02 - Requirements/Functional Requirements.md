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

## Implemented (admin UI only)
| Requirement | Status | Where |
|---|---|---|
| Dashboard: summary stats, recent events, category breakdown | Implemented (mock data) | `admin-ui/frontend/js/views/dashboard.js` |
| Events & Logs: filter by category/date range, search, sort | Implemented (mock data) | `admin-ui/backend/app.py` `list_events` |
| Event Detail: description, timestamp, screenshot tab, video tab | Implemented (mock/simulated evidence) | `admin-ui/frontend/js/views/eventDetail.js` |
| Head Count: aggregate beginning/end-of-class counts | Implemented (real form, seeded + user-entered data) | `admin-ui/frontend/js/views/headcount.js`, `/api/headcounts` |
| Detection Enable/Disable | Implemented (real, persisted; no pipeline to actually gate yet) | `admin-ui/frontend/js/app.js` `renderStatusBox()`, `/api/detection-state` |
| Statistics / Classroom Insights / Suggestions | Implemented (real aggregation + simple rule-based logic over mock data) | `admin-ui/frontend/js/views/insights.js`, `/api/statistics`, `/api/insights`, `/api/suggestions` |
| System status panel (camera/monitoring/detection) | Implemented; camera/monitoring are **hardcoded-true mock values**, detection reflects the real toggle | `admin-ui/backend/app.py` `status()` |

## Status
**Mixed** — see each row. `admin-ui/` implements the *review/browse/record*
side of the system against synthetic (and some user-entered) data; none of
the *detection* side exists. A separate `desktop-app/` prototype
implemented the same three original screens and was removed 2026-09-23 —
see [[Web Application as Sole Admin UI]].

## Related
- [[Research Questions & Objectives]]
- [[UI UX Overview]]
- [[04 - Computer Vision]]
- [[Non-Functional Requirements]]
