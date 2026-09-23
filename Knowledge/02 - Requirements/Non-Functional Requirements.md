---
tags: [requirements, quality]
---

# Non-Functional Requirements

Proposal-derived quality targets, mapped from [[Evaluation Standards]] (ISO/IEC 25010 / 23053:2022 / 25023:2016) — status: **Proposal Requirement** throughout, since there is no detection system to measure against yet.

| Quality attribute | Proposal intent |
|---|---|
| Accuracy / detection accuracy | Correctly identify classroom behaviors and objects (no numeric target stated in the proposal itself, only cited literature ranges of ~95–97% from related work) |
| Response time / processing speed | Real-time frame processing; FPS and latency to be measured |
| Learnability / usability | Teachers should be able to use the interface without extensive training |
| Fault tolerance / reliability | Continuous operation under normal and unexpected conditions; failure rate tracked |
| Security / data protection | Protect student data against unauthorized access — see [[Privacy Requirements]] |
| Resource utilization | CPU/memory load during AI detection kept reasonable (no numeric target stated) |

The admin-UI prototypes have not been evaluated against any of these — no automated test suite exists for either (see each subsystem's `CLAUDE.md` "Commands" section); verification so far has been manual click-through. See [[09 - Testing & Evaluation]].

## Status
**Proposal Requirement** (targets), **Not Yet Implemented** (measurement).

## Related
- [[Evaluation Standards]]
- [[09 - Testing & Evaluation]]
- [[Functional Requirements]]
