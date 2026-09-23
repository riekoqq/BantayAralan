# Admin UI GUI Framework — PySide6 for the Prototype

## Status
Working Decision (scoped to the admin-UI prototype only — does not resolve a separate open question)

## Decision
The native admin-UI prototype (`desktop-app/`) is built with PySide6 (Qt for Python).

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
