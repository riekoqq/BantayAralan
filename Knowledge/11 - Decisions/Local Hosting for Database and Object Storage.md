# Local Hosting for Database and Object Storage

## Status
Working Decision (2026-09-24)

## Decision
The database and evidence object storage (screenshots and video clips) will be
hosted **locally, on-premises**, on the same processing machine (or local
network) as the rest of the system — not on a cloud database service or a
cloud object-storage bucket (e.g. not AWS RDS/S3, not a managed Postgres/Mongo
service, not GCS/Azure Blob).

## Reason
Stated directly by the project team: hosting locally avoids recurring cloud
database and object-storage bucket costs. No other rationale (e.g. latency,
data residency requirements beyond cost) was given.

## What this confirms/changes
- [[06 - Database]] — SQLite was already the implemented choice; this decision
  confirms it also stays local going forward rather than migrating to a
  managed cloud database as the system grows.
- [[Evidence System]] — real evidence (screenshot/video) storage, once built,
  will be local files/local object storage, not a cloud bucket. This decides
  the *hosting location* only — it does **not** resolve the still-open
  evidence-retention *policy* question (how long to keep it), which remains
  open — see [[12 - Open Questions]].

## Alternatives
- A managed cloud database (e.g. a hosted Postgres/MySQL) and a cloud object
  store (e.g. S3-compatible bucket) — rejected specifically to avoid ongoing
  hosting costs for a single-classroom deployment.

## May Change?
Yes, same as any working decision — e.g. if the project expands to multiple
classrooms/sites and centralized access becomes more valuable than avoiding
cloud costs.

## Change Trigger
Further explicit direction from the project team/adviser.

## Related
- [[06 - Database]]
- [[Evidence System]]
- [[08 - Hardware]]
- [[Camera Model and Detection Model Version Confirmed]]
- [[12 - Open Questions]]
