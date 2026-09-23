# No Event-Status Field

## Status
Working Decision

## Decision
The event data model and both admin-UI prototypes intentionally omit an event-status field (e.g. New / Reviewed / Resolved). No status tracking exists in the `events` table or either UI.

## Reason
Stated as intentional "per the design brief" in `admin-ui/CLAUDE.md`. No further rationale (e.g. why status tracking was excluded from the brief) is recorded in this repository.

## Alternatives
Not documented — no alternative status models are discussed in current project files.

## May Change?
Possibly — both `CLAUDE.md` files explicitly instruct "don't add one without checking with the user first," implying this could change with the user's input, unlike a fully closed decision.

## Change Trigger
Explicit confirmation from the user before adding any event-status field.

## Related
- [[Event Model]]
- [[UI Requirements]]
- [[12 - Open Questions]]
