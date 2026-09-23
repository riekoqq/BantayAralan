// Dark-mode preference: persisted in localStorage, applied via a
// data-theme attribute on <html> that tokens.css reacts to instantly --
// see the "dark theme" block in frontend/css/tokens.css. The actual FOUC
// (flash of light-before-dark) is prevented by an inline script in
// index.html's <head> that runs before any CSS paints; this file is the
// full get/set/toggle API used everywhere else (the sidebar toggle).
const Theme = {
  KEY: "bantayaralan-theme",
  get() {
    try {
      return localStorage.getItem(Theme.KEY) === "dark" ? "dark" : "light";
    } catch (e) {
      return "light";
    }
  },
  set(theme) {
    document.documentElement.dataset.theme = theme;
    try {
      localStorage.setItem(Theme.KEY, theme);
    } catch (e) {
      // Private browsing / blocked storage -- theme still applies for this
      // page view, it just won't persist across reloads.
    }
  },
  toggle() {
    Theme.set(Theme.get() === "dark" ? "light" : "dark");
  },
};
