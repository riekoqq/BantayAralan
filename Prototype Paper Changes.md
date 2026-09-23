# Prototype Paper Changes

This document tracks how [`BantayAralan-Prototype-Paper.docx`](BantayAralan-Prototype-Paper.docx) /
[`.pdf`](BantayAralan-Prototype-Paper.pdf) revises
[`Team8_BantayAralan-Proposal.docx.pdf`](Team8_BantayAralan-Proposal.docx.pdf) (the original
proposal, dated March 29, 2026, which remains unchanged and remains the proposal of
record). The prototype paper is a separate working draft, not yet reviewed by the
thesis adviser, and does not report any implementation results, test data, or survey
findings, because none of the features it describes have been built or evaluated.

Status labels follow [`.claude/rules/proposal-vs-implementation.md`](.claude/rules/proposal-vs-implementation.md):
Implemented / Partially implemented / Planned / Proposal requirement / Under
consideration / Changed from proposal / Not yet implemented / Unclear / Deprecated.

## Change summary table

| Original Concept | Prototype Revision | Sections Affected | Status |
|---|---|---|---|
| Real-time student behavior monitoring with real-time alerts | Continuously operating classroom monitoring system: continuous camera operation, continuous configured detection, but detected conditions become recorded events/reports rather than real-time alerts or instant notifications | Title, Introduction, Research Questions, Objectives, Significance, Scope and Limitations, Figures 1–3, Methods (Research Design, Procedure) | Revised |
| Trash / clutter detection | Broader **out-of-place objects** concept: trash/litter/clutter remain valid examples, extended to classroom materials (notebooks, pens, pencils, etc.) found in inappropriate locations | Introduction, Research Questions, Objectives, Scope, Figures 1–3, Instruments/Tools (Hardware) | Revised |
| No head count / attendance feature | Aggregate student head count at the beginning of class and before the end of class (not individual attendance identification) | Introduction, Research Questions (RQ2), Objectives (O2), Scope, Limitations, Figures 1–3, Data Analysis Plan | Added |
| Continuous detection with no manual override | Manual **Detection Enable/Disable** control, gating only the relevant detection/event-generation logic (not cameras, not the whole application, not head counting) | Introduction, Research Questions (RQ3), Objectives (O3), Scope, Limitations, Instruments/Tools (Software), Figures 1–3 | Added |
| Event logging only, no aggregate analysis | Statistical/pattern analysis of **accumulated event history**, producing classroom insights and suggestions/recommendations for recurring conditions (kept distinct from raw event logging) | Introduction, Research Questions (RQ5), Objectives (O5), Data Analysis Plan, Standard Set, Figures 1–3 | Added |
| GUI framework undecided in the proposal (Tkinter or PyQt); desktop-oriented framing | **Web application** framing; Flask mentioned descriptively as the framework already used by the project's existing `admin-ui/` browser prototype, not as a finalized architectural decision | Title, Scope, Instruments/Tools (Software), Figures 1–3 | Changed from proposal — **see open issue below**, since the project's `desktop-app/` (PySide6) is documented elsewhere as the current primary prototype for the opposite reason |
| No parental/guardian consent requirement stated | Parental/guardian consent required before the system is implemented in any classroom involving students | Significance, Scope, Limitations, Methods (Procedure, Sources of Data, Participants) | Added |
| Event evidence (screenshots) | Event evidence explicitly preserved: screenshot **and** video evidence, date/time, description/details; retention described as indefinite/provisional pending adviser consultation | Figures 1–3, Instruments/Tools, Data Analysis Plan | Unchanged in substance, wording clarified |
| Privacy/ethics principles (no facial recognition, no long-term profiling, event-based only) | Unchanged; explicitly extended to state head counting is aggregate only, with no names, IDs, facial recognition, or individual profiles | Research Questions (RQ6), Objectives (O6), Significance, Scope, Limitations, Methods (Participants) | Unchanged in principle, restated for the new features |
| Research Questions / Objectives (5 each, one feature-mapped set) | Rewritten as a coherent 6-question / 6-objective set covering continuous monitoring, head count, detection toggle, evidence capture, statistical analysis + suggestions, and privacy/consent | Research Questions, Objectives | Changed from proposal |
| References (~32 sources) | Unchanged — no citation removed or fabricated | References | Unchanged — **gap flagged below** |

## Open issues requiring project-team / thesis-adviser input

1. **Web application vs. desktop-primary direction.** ~~The prototype paper presents
   BantayAralan as a web application (grounded in the existing `admin-ui/` Flask
   prototype). This directly conflicts with
   [`Knowledge/11 - Decisions/Desktop App as Primary Admin UI Prototype.md`](<Knowledge/11 - Decisions/Desktop App as Primary Admin UI Prototype.md>),
   which documents `desktop-app/` (PySide6) as the *current primary* admin UI
   prototype specifically because a native, non-web application was wanted. This
   paper does not resolve that conflict — it is an open project decision for the
   team to settle.~~
   **Resolved 2026-09-23**: the project team settled this in favor of the web
   application. `desktop-app/` was removed from the repository; `admin-ui/` is
   now the sole and primary admin UI, and `admin-ui/` was extended to cover
   the paper's remaining IA (Head Count, Detection Enable/Disable,
   Statistics/Classroom Insights/Suggestions). See
   [`Knowledge/11 - Decisions/Web Application as Sole Admin UI.md`](<Knowledge/11 - Decisions/Web Application as Sole Admin UI.md>).
2. **Head-count duplicate-counting / individual-distinction mechanism.** No
   technique is specified for avoiding double-counting or distinguishing students
   within a camera frame while keeping the count aggregate-only. Open technical
   question.
3. **Statistical/pattern-analysis methodology.** No formula, threshold, or analysis
   frequency is defined for turning accumulated event history into classroom
   insights and suggestions. Open implementation decision.
4. **Detection-toggle implementation scope.** What exactly continues to run while
   detection is disabled (beyond "not the cameras, not the whole application, not
   head counting") is not finalized. Open technical question.
5. **Literature gaps.** No citation in the current reference list directly supports:
   classroom student head counting, manual detection enable/disable controls, or
   statistical analysis/suggestion generation from accumulated classroom event data.
   These three prototype features are currently unsupported by dedicated literature;
   no citation was fabricated to fill the gap.
6. **Parental/guardian consent process.** The paper establishes consent as a required
   precondition but does not specify a consent form, procedure, or legal basis —
   left for the project team/adviser to define.
7. **Evidence retention policy.** Stated as indefinite/provisional, subject to
   adviser consultation — not a finalized policy, and no retention regulation is
   assumed.

## Notes on figures

The original proposal's three figures (Conceptual Framework, Block Diagram, System
Flowchart) are embedded images that could not be viewed in the environment used to
prepare this prototype paper (no PDF image renderer was available). The prototype
paper's Figures 1–3 were therefore redrawn from scratch based on the architecture
described in this plan and the original figures' descriptive captions — they do not
visually match the original proposal's diagram style, only its conceptual content,
corrected for the seven changes above.
