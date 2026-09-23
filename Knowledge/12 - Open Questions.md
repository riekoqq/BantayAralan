---
tags: [open-questions]
---

# Open Questions

Unresolved items surfaced while migrating project context. None of these should be treated as answered — check here before assuming a direction, and update this note (don't silently resolve elsewhere) when the project owners decide one.

## Evidence retention policy — conflicting signals
- Current stated working direction: evidence (video + screenshot) is intended to be retained **indefinitely**.
- However, `admin-ui/CLAUDE.md` and `desktop-app/CLAUDE.md` both say not to add a "retention countdown / auto-delete UI" because "evidence retention policy is an open decision (see root CLAUDE.md 'Open decisions')" — but the current root `CLAUDE.md` **has no section called "Open decisions"** (checked directly; it does not exist in the current file). Either that section was removed at some point without updating the cross-references, or retention is not actually settled as "indefinite" the way the working direction states.
- **Not resolved here.** Confirm with the project owners whether retention is (a) indefinite as stated, (b) still genuinely open as the `CLAUDE.md` files imply, or (c) something in between (e.g. indefinite by default, but deletable by the admin).
- Related: [[Evidence System]]

## Final GUI framework for the integrated CV + GUI system
- Proposal: "Tkinter or PyQt — undecided in the draft," for the eventual detection+GUI system.
- Prototype built with PySide6 for the *admin UI only* — not confirmed as the answer to the proposal's own question.
- Related: [[Admin UI GUI Framework — PySide6 for the Prototype]], [[04 - Computer Vision]]

## Whether an event-status field will be added
- Currently absent by design, but both subsystem `CLAUDE.md` files explicitly leave the door open ("don't add one without checking with the user first").
- Related: [[No Event-Status Field]]

## Final video evidence implementation
- Both UIs simulate video playback; no real capture/encode/store/serve pipeline is designed in detail anywhere in the repo (see [[Evidence System]] "What real evidence capture would require" — a plausible approach is documented, not a decided one).

## Final camera point-of-view / hardware specs
- The proposal only says "ceiling-mounted" and "top-down" — no model, resolution, FOV, or exact mounting details are specified anywhere.
- Related: [[08 - Hardware]]

## Final detection thresholds
- The proposal mentions alignment is checked "against defined thresholds" without giving values; no thresholds exist anywhere since no detection code exists yet.
- Related: [[04 - Computer Vision]]

## Final event categories
- The current schema has four: `standing`, `trash`, `misaligned`, `other`. The proposal's narrative only explicitly names three (standing, trash, misaligned furniture) — `other` is an implementation addition not discussed in the proposal text. Not confirmed whether `other` is a deliberate permanent catch-all or a placeholder.
- Related: [[Event Model]]

## Whether authentication will ever be necessary
- Currently explicitly out of scope ("admin-only, single deployment, no user management"). Not discussed whether a multi-teacher or multi-classroom deployment (which might need it) is ever in scope.
- Related: [[UI Requirements]]

## Deployment architecture beyond the two current prototypes
- Both prototypes assume a single machine running everything locally against a local SQLite file. No documented plan exists for how a future integrated CV pipeline + admin UI would be deployed (same machine? separate processing PC feeding a UI over a network? one combined app replacing both prototypes?).

## Adviser-approved changes
- No record exists in this repository of any thesis-adviser consultation outcome yet. Treat the entire proposal as unreviewed-by-adviser working draft until a note appears under `13 - Meeting Notes/` saying otherwise.

## Related
- `11 - Decisions/`
- [[00 - Project Overview]]
