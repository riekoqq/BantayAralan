---
tags: [requirements, privacy]
---

# Privacy Requirements

Requirement-level summary; full discussion and constraint list lives in [[10 - Privacy & Ethics]] and `.claude/rules/privacy-and-ethics.md` — don't duplicate that detail here.

- No facial recognition or student-identity recognition anywhere in the system.
- No long-term psychological/behavioral profiling of individual students.
- Event-based monitoring only, not continuous identity-linked tracking.
- Captured evidence must not identify individual students beyond what a teacher needs to review the event.
- The system supports, never replaces, teacher decision-making authority.

`admin-ui/` (the sole admin UI) satisfies this at the mock-data level (no names/IDs/facial data anywhere in seed scripts, head-count records, or generated placeholder imagery) — see `admin-ui/README.md` "Privacy".

## Status
**Proposal Requirement**, currently honored in the two UI prototypes by construction (nothing identity-linked exists to violate this).

## Related
- [[10 - Privacy & Ethics]]
- [[Evidence System]]
