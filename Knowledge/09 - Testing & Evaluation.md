---
tags: [testing, evaluation]
---

# Testing & Evaluation

Two very different things, kept separate: what the proposal *plans* to measure once a detection system exists, and what testing has *actually* happened on the code in this repository.

## Planned (Proposal Requirement — not yet executed)
Quantitative experimental evaluation against ISO/IEC 25010, 23053:2022, and 25023:2016 (full detail: [[Evaluation Standards]]): accuracy, precision, recall, FPS, latency, failure rate, resource utilization — plus pre/post-implementation teacher surveys (5-point Likert) on usability and effectiveness. See [[Methodology]] for the four-phase procedure this belongs to. None of this has been run — there is no detection system to evaluate and no recorded teacher deployment.

## Actual testing done (Implemented, informal)
`admin-ui` (the sole admin UI) has no automated test suite. Verification so
far, per `admin-ui/CLAUDE.md`: manual click-through in a live browser —
dashboard, filters, search, category tabs, empty/no-results states, event
detail with available/unavailable evidence, simulated video playback, the
scheduled head-count status cards, detection toggle (persists across
navigation), all three Insights & Statistics tabs, light/dark theme
toggle, and responsive/mobile layout. ("Manual click-through" here means
*how the UI itself was tested* by a person — unrelated to the
now-removed manual head-count entry feature; see
[[Manual Head-Count Entry Removed]].)

The automated head-count scheduler ([[Automated Head-Count Scheduler]]) has
its own dedicated test mechanism, since it can't practically be tested by
waiting for real clock time: a `BANTAY_TEST_TIME` environment variable
overrides the scheduler's clock, letting each of the three startup cases
(idle-before-both, fires-while-running, starts-late-so-marked-missed) be
exercised in seconds. Never set in production — see `admin-ui/CLAUDE.md` →
"Testing the scheduler" for the exact commands.

**CV model testing** is separate from the above and tracked in
`detection/dataset/README.md`'s round log, not here — each training
round's validation numbers plus, where done, a follow-up live-camera
check, either visual-only (`detection/live_view.py`, no database writes)
or end-to-end (`detection/monitor.py --show`, writes real events into
`admin-ui`). The round log is explicit that validation numbers alone have
repeatedly looked better than live testing confirmed: round 4's
`standing`, mAP50 0.995 on paper, found live 2026-09-30 to not detect
people other than the one in its training photos; a follow-up end-to-end
test 2026-10-01 separately found `trash` misreading a cast shadow as
clutter, a different false-positive mode than the person's-clothing
confusion seen in every prior round — see [[04 - Computer Vision]] for
the current status summary.

A separate `desktop-app/` prototype was syntax-checked and launched
successfully but never fully click-tested visually before it was removed
2026-09-23 — see [[Web Application as Sole Admin UI]].

Quick syntax-check command:
```bash
python -m py_compile run_web.py run_desktop.py backend/*.py   # admin-ui
```

## Status
Planned evaluation: **Not Yet Implemented**. Actual UI testing:
**Implemented, manual only** — no automated tests exist.

## Related
- [[Evaluation Standards]]
- [[Methodology]]
- [[04 - Computer Vision]]
- [[Automated Head-Count Scheduler]]
- [[Manual Head-Count Entry Removed]]
