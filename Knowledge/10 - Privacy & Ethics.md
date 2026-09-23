---
tags: [privacy, ethics]
status: Working Decision
---

# Privacy & Ethics

Consolidates the proposal's ethical framing with the enforceable rule already in place at `.claude/rules/privacy-and-ethics.md` (that file remains the actively-enforced version for Claude Code — this note is the knowledge/context behind it, not a replacement).

## Core constraints (from the proposal and current project guidance)
- No facial recognition or student-identity recognition of any kind.
- No long-term psychological or behavioral profiling of individual students — monitoring is event-based (specific incidents), not continuous identity-linked tracking.
- The system supports teacher decision-making; it does not replace teacher authority or make disciplinary decisions on its own.
- Captured snapshots/evidence must not be usable to identify individual students beyond what's necessary for the teacher to review the logged event.
- Objective 5 of the proposal ("ethical data protocols") and research question 5 both make privacy a first-class research goal, not an afterthought — see [[Research Questions & Objectives]].

## Current implementation practice
`admin-ui/` (the sole admin UI) honors this by construction: mock data, seed scripts, and generated placeholder imagery contain no student names, IDs, or identifying content anywhere (`admin-ui/README.md`, "Privacy" section) — same for the aggregate-only Head Count feature. There is no facial-recognition or identity-tracking code anywhere in the repository to remove or restrict — the constraint is currently satisfied trivially because no real capture pipeline exists yet.

## What this means for future work
If/when a real detection pipeline is added, this constraint must be preserved even though it would be "technically straightforward" to add identity tracking on top of pose estimation/tracking. Any request that would require facial recognition, identity tracking, or behavioral profiling should be flagged back to the project owners rather than implemented silently — this is stated explicitly in `.claude/rules/privacy-and-ethics.md`.

## Status
**Working Decision** — stated as important by the project owners; may be revisited only through explicit direction from them, not inferred from a feature request.

## Related
- [[Privacy Requirements]]
- [[Scope and Limitations]]
- [[Evidence System]]
- `.claude/rules/privacy-and-ethics.md`
