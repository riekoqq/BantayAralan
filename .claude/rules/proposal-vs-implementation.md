---
description: How to talk about BantayAralan features that originate from the research proposal
globs: ["**/*.md", "**/*.py"]
---

# Proposal vs. implementation

`Team8_BantayAralan-Proposal.docx.pdf` is a **working draft**, not a finalized
spec — it will be revised by the project owners. The repository's source code
(once it exists) is the only authority for what the system actually does
today.

When describing, implementing, or reviewing any feature that originates from
the proposal, label it with one of:

- `Implemented`
- `Partially implemented`
- `Planned`
- `Proposal requirement`
- `Expected by current working draft`
- `Not yet implemented`
- `Under consideration`
- `Unclear`
- `Deprecated`
- `Changed from proposal`

Rules:

1. Never state a proposal feature is implemented unless you can point to the
   specific file/function that implements it.
2. If the proposal and the code disagree, document both sides — do not
   silently "fix" one to match the other.
3. Do not modify the proposal PDF to match the code, or the code to match the
   proposal, unless explicitly asked to do so.
4. If uncertain which status applies, write `Unclear` and state what you
   checked before concluding that.
5. Do not carry proposal wording forward as if it were a permanent
   requirement once the project owners provide an updated/finalized proposal
   — re-derive status labels from the newer document.
