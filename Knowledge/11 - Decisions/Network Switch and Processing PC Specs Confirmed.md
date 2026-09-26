# Network Switch and Processing PC Specs Confirmed

## Status
Working Decision (2026-09-26)

## Decision
Several more previously-undocumented hardware choices were confirmed
directly by the project team while this vault's Feasibility Study
(`Documentation/Feasibility Study.md`) was being prepared:

1. **Network switch**: TP-Link TL-SG1005LP — a 5-port Gigabit desktop
   switch with 4 PoE+ ports (40 W total PoE power budget).
2. **Processing PC — full specification**:
   - **CPU**: AMD Ryzen 5 5600
   - **GPU**: NVIDIA GeForce RTX 2060
   - **RAM**: 16 GB, 3200 MHz (Team Group Vulcan Z), purchased at
     approximately ₱2,000 before the DRAM price crisis (team-reported
     purchase context, not a repeatable price quote)
   - **Storage**: 256 GB M.2 SSD (Team Group TM8PS7512G) + 1 TB HDD
     (Seagate ST31000524AS)
   - Form factor (desktop tower vs. laptop) is not stated beyond "PC";
     assume desktop given the discrete-GPU + separate-SSD/HDD
     configuration, but this is an inference, not a confirmed fact.

## Reason
Not independently justified in this repository — all items were stated as
already-decided/already-owned facts by the project team, without
additional rationale recorded, following the same pattern as
[[Camera Model and Detection Model Version Confirmed]].

## What changed
- [[08 - Hardware]] — the "processing PC" row moved from **Unclear** to
  **Working Decision** for CPU/GPU/RAM/storage; only physical form factor
  and mounting remain undocumented.
- `Documentation/Feasibility Study.md` — Sections 3.1 (Hardware), 3.4
  (Performance), 5.1 (Initial hardware costs), and 10 (Assumptions and
  Evidence Gaps) updated to reflect the confirmed full spec instead of
  treating the processing PC as an open question.

## Not changed (deliberately)
- `Team8_BantayAralan-Proposal.docx.pdf` — never edited, per explicit
  standing instruction; it remains historical proposal text (originally
  undecided on GUI/hardware specifics) regardless of any later confirmed
  decision.
- `BantayAralan-Prototype-Paper` / `DOC-CAP-FINAL-2026-008` — updated
  separately where their own hardware sections reference specs; see those
  documents' own revision history for what changed and when.

## Open questions this does not resolve
- Whether the TL-SG1005LP's 4 PoE+ ports are enough for the project's
  final camera count.
- Whether the RTX 2060 + Ryzen 5 5600 + 16 GB RAM combination is
  sufficient for real-time YOLOv8 + ByteTrack inference at the project's
  eventual camera count/resolution — no benchmark exists in this
  repository; this note only records what hardware exists, not how it
  performs.
- Desktop vs. laptop form factor, and whether this PC is dedicated to
  BantayAralan or shared with other use.
- The 256 GB SSD (OS/application drive, presumably) plus 1 TB HDD implies
  a likely storage split (OS/fast access vs. bulk evidence storage), but
  no document states which drive would actually hold the local SQLite
  database or evidence files — flagged as unconfirmed, not assumed here.

See [[12 - Open Questions]].

## May Change?
Yes, same as any working decision — update this note and [[08 - Hardware]]
if any of these specs change.

## Change Trigger
Further explicit direction from the project team/adviser.

## Related
- [[08 - Hardware]]
- [[Camera Model and Detection Model Version Confirmed]]
- [[04 - Computer Vision]]
- [[12 - Open Questions]]
