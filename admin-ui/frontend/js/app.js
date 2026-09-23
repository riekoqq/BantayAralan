const ROUTES = {
  dashboard: { label: "Dashboard", icon: "grid" },
  events: { label: "Events & Logs", icon: "list" },
};

function currentSection() {
  const hash = window.location.hash.replace(/^#\//, "");
  if (hash.startsWith("events")) return "events";
  return "dashboard";
}

function renderSidebar() {
  const active = currentSection();
  const sidebar = document.getElementById("sidebar");
  sidebar.innerHTML = `
    <div class="wordmark"><div class="mark"></div><span>BantayAralan</span></div>
    <nav class="nav-group">
      <a class="nav-item ${active === "dashboard" ? "active" : ""}" href="#/dashboard">
        ${iconHtml("grid", active === "dashboard" ? "#fff" : "var(--text-tertiary)", 18)} Dashboard
      </a>
      <a class="nav-item ${active === "events" ? "active" : ""}" href="#/events">
        ${iconHtml("list", active === "events" ? "#fff" : "var(--text-tertiary)", 18)} Events &amp; Logs
      </a>
    </nav>
    <div class="sidebar-spacer"></div>
    <div class="system-status" id="system-status">
      <div class="status-line"><span class="status-dot"></span> Loading status…</div>
    </div>
  `;

  const mobileNav = document.getElementById("mobile-nav");
  mobileNav.innerHTML = `
    <a class="${active === "dashboard" ? "active" : ""}" href="#/dashboard">Dashboard</a>
    <a class="${active === "events" ? "active" : ""}" href="#/events">Events</a>
  `;

  Api.status().then((s) => {
    const el = document.getElementById("system-status");
    if (!el) return;
    el.innerHTML = `
      <div class="status-line"><span class="status-dot ${s.camera_connected ? "" : "warn"}"></span> Camera: ${s.camera_connected ? "Connected" : "Disconnected"}</div>
      <div class="status-line"><span class="status-dot ${s.detection_running ? "" : "warn"}"></span> Detection: ${s.detection_running ? "Running" : "Stopped"}</div>
      <div class="status-line"><span class="status-dot"></span> Last event: ${s.last_event_at ? "recently" : "none yet"}</div>
    `;
  }).catch(() => {
    const el = document.getElementById("system-status");
    if (el) el.innerHTML = `<div class="status-line"><span class="status-dot warn"></span> Status unavailable</div>`;
  });
}

function parseHash() {
  const hash = window.location.hash.replace(/^#\/?/, "");
  const parts = hash.split("/").filter(Boolean);
  return parts;
}

async function route() {
  renderSidebar();
  const root = document.getElementById("view-root");
  const parts = parseHash();

  if (parts[0] === "events" && parts[1]) {
    await renderEventDetail(root, parts[1]);
    return;
  }
  if (parts[0] === "events") {
    await renderEvents(root);
    return;
  }
  await renderDashboard(root);
}

window.addEventListener("hashchange", route);
window.addEventListener("DOMContentLoaded", () => {
  if (!window.location.hash) window.location.hash = "#/dashboard";
  route();
});
