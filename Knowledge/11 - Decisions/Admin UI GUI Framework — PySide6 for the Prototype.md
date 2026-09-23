# Admin UI GUI Framework — PySide6 for the Prototype

## Status
Superseded 2026-09-23 (scoped to the admin-UI prototype only — never
resolved the separate CV-pipeline question below, which is still open)

## Update (2026-09-23)
`desktop-app/` (the only place PySide6 was used in this repo) was removed
once the project settled on a web-only admin UI — see
[[Web Application as Sole Admin UI]]. PySide6 is no longer used anywhere in
the repository. This record is kept for its reasoning history. The
separate, still-open question below (the eventual CV-pipeline system's GUI
framework) is unaffected by this and remains unresolved.

## Decision (historical — no longer applicable, PySide6 usage removed)
The native admin-UI prototype (`desktop-app/`, since removed) was built with PySide6 (Qt for Python).

## Reason
Not explicitly stated in the repo beyond enabling "a genuine native desktop GUI... no browser, no HTTP server, and no webview involved" — PySide6 is a mainstream, capable choice for exactly that. No comparison against other native-GUI options is documented.

## Important distinction — this does not resolve the proposal's own open GUI question
The proposal's own "Instruments/Tools" section lists the eventual CV-pipeline system's GUI framework as **"Tkinter or PyQt — undecided in the draft."** PySide6 (used here) is neither exactly the same as PyQt (a different binding to the same underlying Qt library, API-compatible but a separate project) nor Tkinter. It is unclear from current docs whether:
- PySide6 is intended to carry forward as the GUI for the eventual integrated CV+GUI system, or
- The admin-UI prototype's framework choice is independent of that still-open proposal question.

This is preserved as an open question rather than resolved here — see [[12 - Open Questions]].

## Alternatives
Tkinter, PyQt (per the proposal's own undecided framing) — not evaluated against PySide6 in any documented way.

## May Change?
Yes — the proposal's underlying question remains open.

## Change Trigger
Adviser/proposal-owner decision on the final CV-pipeline GUI framework.

## Related
- [[Desktop App (Native Prototype)]]
- [[04 - Computer Vision]]
- [[12 - Open Questions]]
