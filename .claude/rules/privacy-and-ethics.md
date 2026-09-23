---
description: Non-negotiable privacy/ethics constraints for any CV or data-handling code in BantayAralan
globs: ["**/*.py"]
---

# Privacy & ethics constraints

These constraints come from the current working-draft proposal and must be
preserved in any implementation unless the project owners explicitly change
them:

- No facial recognition or student-identity recognition of any kind.
- No long-term psychological or behavioral profiling of individual students.
- Monitoring stays event-based (specific disruptive-behavior or cleanliness
  events), not continuous identity-linked tracking of individuals over time.
- The system supports teacher decision-making; it does not replace teacher
  authority or make disciplinary decisions on its own.
- Captured snapshots/evidence must not be usable to identify individual
  students beyond what's necessary for the teacher to review the logged
  event.

Do not add facial recognition, identity tracking, or behavioral-profiling
features even if they would be technically straightforward to add on top of
an existing detection/tracking pipeline. If a request would require any of
this, flag it back to the user instead of implementing it silently.
