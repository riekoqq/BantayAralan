---
tags: [research, standards, quality]
status: Proposal Requirement
---

# Evaluation Standards (ISO/IEC 25010, 23053:2022, 25023:2016)

The proposal specifies three ISO/IEC standards to frame how the system's quality and performance will be measured.

## ISO/IEC 25010 — Product Quality
| Characteristic | Sub-characteristic | What it measures for BantayAralan |
|---|---|---|
| Functional Suitability | Accuracy | Correct detection and reporting of classroom behavior |
| Performance Efficiency | Response Time | Speed/resource usage during video processing and AI detection |
| Usability | Learnability | How easily teachers navigate the interface without extensive training |
| Reliability | Fault Tolerance | Operating correctly under normal and unexpected conditions |
| Security | Data Protection | Protecting student data against unauthorized access/breaches |

## ISO/IEC 23053:2022 — AI/ML System Framework
| Characteristic | Sub-characteristic | What it measures |
|---|---|---|
| Functional Suitability | Detection Accuracy | % of classroom behaviors correctly identified by the AI component |
| Performance Efficiency | Processing Speed | Average frame processing time, CPU load, memory usage |
| Reliability | Failure Rate | System failures during extended operation |
| Resource Utilization | System Load | Computational resource use during AI detection tasks |

## ISO/IEC 25023:2016 — Quantitative Quality Metrics
Covers AI model training and output accuracy, system-integration interface compatibility, and lifecycle/version-control management — furnishes measurable indicators (average detection time, accuracy, CPU/memory consumption) for the categories above.

## Status
**Proposal Requirement.** These are the standards the proposal intends to use for future quantitative evaluation of a working detection system; no measurement against them has occurred yet since no detection system exists. See [[09 - Testing & Evaluation]] for the current (informal, UI-only) testing reality.

## Related
- [[Methodology]]
- [[09 - Testing & Evaluation]]
