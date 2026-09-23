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
- The admin UI's own framework question is now settled (web/Flask — [[Web Application as Sole Admin UI]]) and PySide6 is no longer used anywhere in the repo, but that does **not** answer this separate question about the eventual CV-pipeline system's GUI.
- Related: [[Admin UI GUI Framework — PySide6 for the Prototype]], [[04 - Computer Vision]]

## Head-count duplicate-counting / individual-distinction mechanism
- `Prototype Paper Changes.md` open issue 2: no technique is specified for avoiding double-counting or distinguishing students within a camera frame while keeping the count aggregate-only.
- `admin-ui`'s current implementation uses a placeholder policy (last recorded value per date+point wins) purely for its manual-entry form — this is not a proposed answer to the real detection-side question.
- Related: [[Admin UI (Browser Prototype)]], `admin-ui/CLAUDE.md`

## Statistical/pattern-analysis methodology for insights & suggestions
- `Prototype Paper Changes.md` open issue 3: no formula, threshold, or analysis frequency is defined for turning accumulated event history into classroom insights and suggestions.
- `admin-ui`'s current implementation uses simple, clearly-labeled rule-based thresholds (most-frequent category, ±20% week-over-week) purely to give the UI real, non-fabricated data to show — not a proposed answer to this question. See `SUGGESTION_MAP`/`_compute_insights()` in `admin-ui/backend/app.py`.
- Related: [[Admin UI (Browser Prototype)]]

## Detection-toggle exact implementation scope
- `Prototype Paper Changes.md` open issue 4: what exactly continues to run while detection is disabled (beyond "not the cameras, not the whole application, not head counting") is not finalized.
- `admin-ui`'s current implementation persists a single enabled/disabled flag (`detection_state` table) that the UI reads/writes; there is no real detection pipeline yet for this flag to actually gate.
- Related: [[Admin UI (Browser Prototype)]], `admin-ui/CLAUDE.md`

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

## Resolved
- **Web application vs. desktop-primary direction** — was open (see
  `Prototype Paper Changes.md` open issue 1). **Resolved 2026-09-23**: the
  finalized prototype paper settled this in favor of a web application;
  `desktop-app/` was removed. See [[Web Application as Sole Admin UI]].

## Related
- `11 - Decisions/`
- [[00 - Project Overview]]
