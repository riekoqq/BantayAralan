# Desktop App as Primary Admin UI Prototype

## Status
**Reversed 2026-09-23** — see [[Web Application as Sole Admin UI]] for the
current decision. The finalized prototype paper settled the project's
open web-vs-desktop question in favor of a web application; `desktop-app/`
was removed from the repository. This record is kept for its reasoning
history, not as current guidance.

## Decision (as originally made — no longer current)
`desktop-app/` (PySide6 native app) is the primary admin-UI prototype going forward. `admin-ui/` (Flask + vanilla JS) remains in the repository as a reference/alternative, not deleted, not actively developed as primary.

## Reason
The user specifically wanted "an application only, instead of an app that views the web" — i.e., a genuine native OS window with no browser, HTTP server, or webview involved, as opposed to `admin-ui`'s browser-tab/webview-wrapped approach.

## Alternatives
- Keep `admin-ui` (Flask + webview via `pywebview`) as the only prototype — rejected because it still "views the web" under the hood even in its desktop-window run mode.
- Tkinter for the native GUI — not chosen; the proposal itself left the eventual GUI framework as Tkinter-or-PyQt undecided (see [[Admin UI GUI Framework — PySide6 for the Prototype]]), and PySide6 was chosen specifically for this admin-UI prototype.

## May Change?
Not indicated in current docs.

## Change Trigger
Not documented — would presumably follow further direction from the user/adviser.

## Related
- [[Two Admin UI Prototypes]]
- [[Desktop App (Native Prototype)]]
- [[Admin UI GUI Framework — PySide6 for the Prototype]]
- [[Web Application as Sole Admin UI]]
