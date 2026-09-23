async function renderInsights(root) {
  const state = { tab: "statistics" };

  root.innerHTML = `
    <div class="page-header">
      <h1 class="page-title">Insights &amp; Statistics</h1>
      <p class="page-subtitle">Accumulated event history, reviewed periodically -- not a real-time alert feed.</p>
    </div>
    <div class="tab-row" id="insights-tabs"></div>
    <div id="insights-body">${skeletonGrid("card", 3)}</div>
  `;

  const tabs = [
    ["statistics", "Statistics"],
    ["classroom-insights", "Classroom Insights"],
    ["suggestions", "Suggestions"],
  ];

  function renderTabRow() {
    root.querySelector("#insights-tabs").innerHTML = tabs.map(([value, label]) =>
      `<button class="tab ${value === state.tab ? "selected" : ""}" data-tab="${value}">${label}</button>`
    ).join("");
  }

  async function showTab(tab) {
    state.tab = tab;
    renderTabRow();
    const body = root.querySelector("#insights-body");
    body.innerHTML = skeletonGrid("card", 3);
    try {
      if (tab === "statistics") await renderStatisticsTab(body);
      else if (tab === "classroom-insights") await renderClassroomInsightsTab(body);
      else await renderSuggestionsTab(body);
    } catch (err) {
      body.innerHTML = errorStateHtml({
        title: "Unable to load this data",
        desc: "The admin UI couldn't reach the backend. Check that the app server is running and try again.",
      });
      body.querySelector('[data-action="retry"]')?.addEventListener("click", () => showTab(tab));
    }
  }

  root.querySelector("#insights-tabs").addEventListener("click", (e) => {
    const btn = e.target.closest("[data-tab]");
    if (btn) showTab(btn.dataset.tab);
  });

  await showTab(state.tab);
}

async function renderStatisticsTab(body) {
  const stats = await Api.statistics();
  const trend = stats.trend_pct;
  const trendLabel = trend == null ? "Not enough prior data yet" : `${trend > 0 ? "+" : ""}${trend}% vs. previous ${stats.window_days} days`;
  body.innerHTML = `
    ${disclaimerHtml(`Computed from recorded events in the last ${stats.window_days} days. Reviewed periodically, not a live feed.`)}
    <div class="stat-grid">
      ${statCardHtml("Events (this period)", stats.events_this_period, trendLabel)}
      ${statCardHtml("Total Events (all time)", stats.total_events_all_time)}
      ${Object.entries(stats.by_category_this_period).map(([cat, n]) =>
        `<div class="stat-card by-category">${categoryBadgeHtml({ category: cat })}<span class="stat-number" style="font-size:20px">${n}</span></div>`
      ).join("")}
    </div>
  `;
}

async function renderClassroomInsightsTab(body) {
  const data = await Api.insights();
  if (!data.insights || data.insights.length === 0) {
    body.innerHTML = emptyStateHtml({
      icon: "lightbulb",
      title: "Not enough data yet",
      desc: "Classroom insights appear here once enough events have been recorded to identify a pattern.",
    });
    return;
  }
  body.innerHTML = `
    ${disclaimerHtml("Simple, rule-based observations derived from recorded events -- not a validated behavioral analysis.")}
    <ul class="insight-list">
      ${data.insights.map((text) => `<li class="insight-item">${iconHtml("lightbulb", "var(--brand-primary)", 18)}<span>${text}</span></li>`).join("")}
    </ul>
  `;
}

async function renderSuggestionsTab(body) {
  const data = await Api.suggestions();
  if (!data.suggestions || data.suggestions.length === 0) {
    body.innerHTML = emptyStateHtml({
      icon: "lightbulb",
      title: "No suggestions yet",
      desc: "Suggestions appear here once recurring conditions show up in recorded events.",
    });
    return;
  }
  body.innerHTML = `
    ${disclaimerHtml("Suggestions are generated from recurring patterns in recorded events. They are not clinically or scientifically validated recommendations -- use professional judgment.")}
    <div class="suggestion-list">
      ${data.suggestions.map((s) => `
        <div class="suggestion-card">
          ${categoryBadgeHtml({ category: s.category })}
          <p class="suggestion-text">${s.suggestion}</p>
          <p class="suggestion-count">${s.count} recorded event${s.count === 1 ? "" : "s"} this period</p>
        </div>`).join("")}
    </div>
  `;
}
