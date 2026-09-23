const ROUTES = {
  dashboard: { label: "Dashboard", icon: "grid" },
  events: { label: "Events & Logs", icon: "list" },
  headcount: { label: "Head Count", icon: "users" },
  insights: { label: "Insights & Statistics", icon: "barChart" },
};

function currentSection() {
  const hash = window.location.hash.replace(/^#\//, "");
  if (hash.startsWith("events")) return "events";
  if (hash.startsWith("headcount")) return "headcount";
  if (hash.startsWith("insights")) return "insights";
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
      <a class="nav-item ${active === "headcount" ? "active" : ""}" href="#/headcount">
        ${iconHtml("users", active === "headcount" ? "#fff" : "var(--text-tertiary)", 18)} Head Count
      </a>
      <a class="nav-item ${active === "insights" ? "active" : ""}" href="#/insights">
        ${iconHtml("barChart", active === "insights" ? "#fff" : "var(--text-tertiary)", 18)} Insights &amp; Statistics
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
    <a class="${active === "headcount" ? "active" : ""}" href="#/headcount">Head Count</a>
    <a class="${active === "insights" ? "active" : ""}" href="#/insights">Insights</a>
  `;

  renderStatusBox();
}

function renderStatusBox() {
  const el = document.getElementById("system-status");
  if (!el) return;
  Api.status().then((s) => {
    if (!document.getElementById("system-status")) return;
    el.innerHTML = `
      <div class="status-line"><span class="status-dot ${s.camera_connected ? "" : "warn"}"></span> Camera: ${s.camera_connected ? "Connected" : "Disconnected"}</div>
      <div class="status-line"><span class="status-dot ${s.monitoring_active ? "" : "warn"}"></span> Monitoring: ${s.monitoring_active ? "Active" : "Inactive"}</div>
      <div class="status-line detection-toggle-line">
        <button class="toggle-switch ${s.detection_enabled ? "on" : ""}" id="detection-toggle" role="switch" aria-checked="${s.detection_enabled}" aria-label="Toggle detection">
          <span class="toggle-thumb"></span>
        </button>
        <span>Detection: ${s.detection_enabled ? "Enabled" : "Disabled"}</span>
      </div>
      <div class="status-line"><span class="status-dot"></span> Last event: ${s.last_event_at ? "recorded" : "none yet"}</div>
      <p class="status-note">Cameras and head counting keep running either way.</p>
    `;
    document.getElementById("detection-toggle")?.addEventListener("click", async (e) => {
      const btn = e.currentTarget;
      btn.disabled = true;
      try {
        await Api.setDetectionState(!s.detection_enabled);
        renderStatusBox();
      } catch (err) {
        btn.disabled = false;
      }
    });
  }).catch(() => {
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
  if (parts[0] === "headcount") {
    await renderHeadcount(root);
    return;
  }
  if (parts[0] === "insights") {
    await renderInsights(root);
    return;
  }
  await renderDashboard(root);
}

window.addEventListener("hashchange", route);
window.addEventListener("DOMContentLoaded", () => {
  if (!window.location.hash) window.location.hash = "#/dashboard";
  route();
});
