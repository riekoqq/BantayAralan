const EVENTS_PAGE_SIZE = 12;

async function renderEvents(root, initialQuery = {}) {
  const state = {
    category: initialQuery.category || "all",
    range: initialQuery.range || "all",
    q: initialQuery.q || "",
    sort: initialQuery.sort || "newest",
    offset: 0,
  };

  root.innerHTML = `
    <div class="page-header">
      <h1 class="page-title">Events &amp; Logs</h1>
      <p class="page-subtitle">Complete chronological record of detected events for this classroom.</p>
    </div>
    <div class="toolbar">
      <div class="search-field">
        ${iconHtml("search", "var(--text-tertiary)", 16)}
        <input type="text" id="search-input" placeholder="Search events…" value="${state.q}" />
      </div>
      <select class="filter-select" id="range-select">
        <option value="all">All time</option>
        <option value="today">Today</option>
        <option value="7d">Last 7 days</option>
      </select>
      <select class="filter-select" id="sort-select">
        <option value="newest">Newest first</option>
        <option value="oldest">Oldest first</option>
      </select>
    </div>
    <div class="tab-row" id="tab-row"></div>
    <div id="events-body">${skeletonGrid("row", 6)}</div>
  `;

  root.querySelector("#range-select").value = state.range;
  root.querySelector("#sort-select").value = state.sort;
  renderTabs(root.querySelector("#tab-row"), state.category);

  const body = root.querySelector("#events-body");
  let debounceTimer = null;

  async function load() {
    body.innerHTML = skeletonGrid("row", 6);
    try {
      const params = { sort: state.sort, limit: EVENTS_PAGE_SIZE, offset: state.offset };
      if (state.category !== "all") params.category = state.category;
      if (state.range !== "all") params.range = state.range;
      if (state.q) params.q = state.q;
      const data = await Api.events(params);
      renderList(body, data, state);
    } catch (err) {
      body.innerHTML = errorStateHtml({
        title: "Unable to load events",
        desc: "The admin UI couldn't reach the backend. Check that the app server is running and try again.",
      });
      body.querySelector('[data-action="retry"]')?.addEventListener("click", load);
    }
  }

  root.querySelector("#tab-row").addEventListener("click", (e) => {
    const tab = e.target.closest("[data-category]");
    if (!tab) return;
    state.category = tab.dataset.category;
    state.offset = 0;
    renderTabs(root.querySelector("#tab-row"), state.category);
    load();
  });

  root.querySelector("#range-select").addEventListener("change", (e) => {
    state.range = e.target.value; state.offset = 0; load();
  });
  root.querySelector("#sort-select").addEventListener("change", (e) => {
    state.sort = e.target.value; state.offset = 0; load();
  });
  root.querySelector("#search-input").addEventListener("input", (e) => {
    clearTimeout(debounceTimer);
    const value = e.target.value;
    debounceTimer = setTimeout(() => { state.q = value; state.offset = 0; load(); }, 300);
  });

  load();
}

function renderTabs(container, active) {
  const tabs = [
    ["all", "All"], ["standing", "Standing"], ["trash", "Trash"],
    ["misaligned", "Misaligned Seats"], ["other", "Other"],
  ];
  container.innerHTML = tabs.map(([value, label]) =>
    `<button class="tab ${value === active ? "selected" : ""}" data-category="${value}">${label}</button>`
  ).join("");
}

function renderList(body, data, state) {
  if (data.events.length === 0) {
    const filtered = state.category !== "all" || state.range !== "all" || state.q;
    body.innerHTML = filtered
      ? emptyStateHtml({ icon: "search", title: "No events match your filters", desc: "Try a different category, date range, or search term." })
      : emptyStateHtml({ title: "No events detected for this period", desc: "Detected classroom events will appear here as they happen." });
    return;
  }

  const list = document.createElement("div");
  list.className = "event-list";
  list.innerHTML = data.events.map(eventRowHtml).join("");

  const totalPages = Math.max(1, Math.ceil(data.total / EVENTS_PAGE_SIZE));
  const currentPage = Math.floor(data.offset / EVENTS_PAGE_SIZE) + 1;
  const pagination = document.createElement("div");
  pagination.className = "pagination";
  pagination.innerHTML = `
    <span>${data.total} event${data.total === 1 ? "" : "s"} &bull; page ${currentPage} of ${totalPages}</span>
    <div style="display:flex;gap:8px">
      <button data-dir="prev" ${data.offset === 0 ? "disabled" : ""}>Previous</button>
      <button data-dir="next" ${data.offset + EVENTS_PAGE_SIZE >= data.total ? "disabled" : ""}>Next</button>
    </div>`;

  body.innerHTML = "";
  body.appendChild(list);
  body.appendChild(pagination);
  attachEventCardNavigation(body);

  pagination.addEventListener("click", (e) => {
    const btn = e.target.closest("button[data-dir]");
    if (!btn) return;
    if (btn.dataset.dir === "prev") state.offset = Math.max(0, state.offset - EVENTS_PAGE_SIZE);
    else state.offset += EVENTS_PAGE_SIZE;
    const body2 = document.getElementById("events-body");
    body2.innerHTML = skeletonGrid("row", 6);
    Api.events({
      sort: state.sort, limit: EVENTS_PAGE_SIZE, offset: state.offset,
      ...(state.category !== "all" ? { category: state.category } : {}),
      ...(state.range !== "all" ? { range: state.range } : {}),
      ...(state.q ? { q: state.q } : {}),
    }).then((d) => renderList(body2, d, state));
  });
}
