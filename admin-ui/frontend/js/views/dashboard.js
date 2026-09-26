async function renderDashboard(root) {
  root.innerHTML = `
    <div class="page-header">
      <h1 class="page-title">Dashboard</h1>
      <p class="page-subtitle">Overview of detected classroom events. This view shows summaries only -- no live camera feed.</p>
    </div>
    <div class="stat-grid" id="stat-grid">${skeletonGrid("stat", 4)}</div>
    <div class="section-header">
      <h2 class="section-title">Recent Events</h2>
      <a class="section-link" href="#/events">View all &rarr;</a>
    </div>
    <div class="event-grid" id="recent-events">${skeletonGrid("card", 6)}</div>
  `;

  await loadDashboardData(root, { silent: false });
  startPolling(() => loadDashboardData(root, { silent: true }));
}

async function loadDashboardData(root, { silent }) {
  const statGrid = root.querySelector("#stat-grid");
  const recent = root.querySelector("#recent-events");
  if (!statGrid || !recent) return; // navigated away since the poll fired
  try {
    const data = await Api.summary();
    renderStats(statGrid, data);
    renderRecent(recent, data.recent);
  } catch (err) {
    if (silent) return; // don't replace a working view with an error over one missed poll
    statGrid.innerHTML = "";
    recent.innerHTML = errorStateHtml({
      title: "Unable to load dashboard data",
      desc: "The admin UI couldn't reach the backend. Check that the app server is running and try again.",
    });
    recent.querySelector('[data-action="retry"]')?.addEventListener("click", () => renderDashboard(root));
  }
}

function renderStats(container, data) {
  const catLabel = { standing: "Standing", trash: "Trash", misaligned: "Misaligned Seats", other: "Other" };
  container.innerHTML = `
    ${statCardHtml("Total Events", data.total_events, "All recorded events")}
    ${statCardHtml("Events Today", data.events_today)}
    ${Object.entries(data.by_category).map(([cat, n]) =>
      `<div class="stat-card by-category">${categoryBadgeHtml({ category: cat })}<span class="stat-number" style="font-size:20px">${n}</span></div>`
    ).join("")}
  `;
}

function renderRecent(container, events) {
  if (!events || events.length === 0) {
    container.innerHTML = emptyStateHtml({
      title: "No events detected yet",
      desc: "Detected classroom events will appear here once they're recorded.",
    });
    return;
  }
  container.innerHTML = events.map(eventCardHtml).join("");
  attachEventCardNavigation(container);
}
