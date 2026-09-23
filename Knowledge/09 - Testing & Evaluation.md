---
tags: [testing, evaluation]
---

# Testing & Evaluation

Two very different things, kept separate: what the proposal *plans* to measure once a detection system exists, and what testing has *actually* happened on the code in this repository.

## Planned (Proposal Requirement — not yet executed)
Quantitative experimental evaluation against ISO/IEC 25010, 23053:2022, and 25023:2016 (full detail: [[Evaluation Standards]]): accuracy, precision, recall, FPS, latency, failure rate, resource utilization — plus pre/post-implementation teacher surveys (5-point Likert) on usability and effectiveness. See [[Methodology]] for the four-phase procedure this belongs to. None of this has been run — there is no detection system to evaluate and no recorded teacher deployment.

## Actual testing done (Implemented, informal)
Neither `admin-ui` nor `desktop-app` has an automated test suite. Verification so far, per each subsystem's `CLAUDE.md`:
- **`admin-ui`**: manual click-through in a live browser — dashboard, filters, search, category tabs, empty/no-results states, event detail with available/unavailable evidence, simulated video playback, responsive/mobile layout.
- **`desktop-app`**: syntax-compiled all modules (`python -m py_compile`), launched in the background with no startup traceback, confirmed a successfully seeded database — but **not** a full visual click-through (native OS windows weren't screenshot-able by the tools used at build time). A real visual pass is flagged as still needed.

Quick syntax-check commands exist for both:
```bash
python -m py_compile run_web.py run_desktop.py backend/*.py   # admin-ui
python -m py_compile run.py app/*.py                          # desktop-app
```

## Status
Planned evaluation: **Not Yet Implemented**. Actual UI testing: **Implemented, manual only** — no automated tests exist for either prototype.

## Related
- [[Evaluation Standards]]
- [[Methodology]]
- [[04 - Computer Vision]]
