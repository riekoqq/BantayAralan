# Camera Model and Detection Model Version Confirmed

## Status
Working Decision (2026-09-24)

## Decision
Two previously-undocumented technical choices were confirmed directly by the
project team while producing the final capstone master document
(`DOC-CAP-FINAL-2026-008`):
1. **Camera model**: TP-Link VIGI C320I, a PoE (Power over Ethernet) dome
   network camera.
2. **Detection model version**: **YOLOv8**, superseding the proposal PDF's
   YOLO11m.

## Reason
Not independently justified in this repository — both were stated as
already-decided facts by the project team, without additional rationale
recorded. This note exists so the decision is traceable to a date and isn't
lost or silently contradicted elsewhere in the vault.

## What changed
- [[08 - Hardware]] — added the confirmed camera model under a new
  "Confirmed (Working Decision, 2026-09-24)" section; left open whether it
  covers one or both proposed camera roles (ceiling behavior camera vs.
  top-down clutter/alignment camera).
- [[04 - Computer Vision]] — added a "Model version — Changed from
  proposal" note; YOLOv8 is now treated as current, YOLO11m as superseded
  proposal text.
- [[00 - Project Overview]], [[System Architecture]] — updated summary
  tables/diagrams to say YOLOv8 instead of YOLO11m, and to note the
  confirmed camera model.

## Not changed (deliberately)
- `Team8_BantayAralan-Proposal.docx.pdf` and `Knowledge/01 - Research/*.md`
  notes that summarize the *original proposal document's* text still say
  YOLO11m — those notes describe what that historical document says, not
  the project's current direction, so they were left as accurate summaries
  of that document rather than edited to match the new decision.

## Open questions this does not resolve
- Whether the TP-Link VIGI C320I is used for one or both camera roles.
- The camera's actual ingest/streaming protocol as used by this project
  (commonly RTSP/ONVIF for this class of PoE camera, but not confirmed).
- Any other hardware spec (processing PC, mounting) — still undocumented.

See [[12 - Open Questions]].

## May Change?
Yes, same as any working decision — update this note and the files above if
either choice changes again.

## Change Trigger
Further explicit direction from the project team/adviser.

## Related
- [[08 - Hardware]]
- [[04 - Computer Vision]]
- [[12 - Open Questions]]
