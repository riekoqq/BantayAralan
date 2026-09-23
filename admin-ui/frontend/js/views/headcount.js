async function renderHeadcount(root) {
  root.innerHTML = `
    <div class="page-header">
      <h1 class="page-title">Head Count</h1>
      <p class="page-subtitle">Aggregate student head counts recorded at the beginning and near the end of a class session -- not attendance identification. No names or IDs are recorded.</p>
    </div>
    <div class="headcount-form" id="headcount-form">
      <div class="headcount-field">
        <label for="hc-start">Beginning of class</label>
        <div class="headcount-input-row">
          <input type="number" id="hc-start" min="0" step="1" placeholder="e.g. 28" />
          <button class="btn btn-primary" data-point="start">Record</button>
        </div>
      </div>
      <div class="headcount-field">
        <label for="hc-end">Before end of class</label>
        <div class="headcount-input-row">
          <input type="number" id="hc-end" min="0" step="1" placeholder="e.g. 26" />
          <button class="btn btn-primary" data-point="end">Record</button>
        </div>
      </div>
    </div>
    <div id="headcount-feedback"></div>
    <div class="section-header">
      <h2 class="section-title">Recent Sessions</h2>
    </div>
    <div id="headcount-sessions">${skeletonGrid("row", 4)}</div>
  `;

  const feedback = root.querySelector("#headcount-feedback");

  async function load() {
    const container = root.querySelector("#headcount-sessions");
    container.innerHTML = skeletonGrid("row", 4);
    try {
      const data = await Api.headcounts();
      renderSessions(container, data.sessions);
    } catch (err) {
      container.innerHTML = errorStateHtml({
        title: "Unable to load head count history",
        desc: "The admin UI couldn't reach the backend. Check that the app server is running and try again.",
      });
      container.querySelector('[data-action="retry"]')?.addEventListener("click", load);
    }
  }

  root.querySelector("#headcount-form").addEventListener("click", async (e) => {
    const btn = e.target.closest("button[data-point]");
    if (!btn) return;
    const point = btn.dataset.point;
    const input = root.querySelector(point === "start" ? "#hc-start" : "#hc-end");
    const count = parseInt(input.value, 10);
    if (!Number.isInteger(count) || count < 0) {
      feedback.innerHTML = `<p class="form-error">Enter a whole number of 0 or more.</p>`;
      return;
    }
    btn.disabled = true;
    try {
      await Api.recordHeadcount(point, count);
      feedback.innerHTML = "";
      input.value = "";
      await load();
    } catch (err) {
      feedback.innerHTML = `<p class="form-error">Couldn't save this count. Check that the app server is running and try again.</p>`;
    } finally {
      btn.disabled = false;
    }
  });

  load();
}

function renderSessions(container, sessions) {
  if (!sessions || sessions.length === 0) {
    container.innerHTML = emptyStateHtml({
      icon: "users",
      title: "No head counts recorded yet",
      desc: "Record a beginning-of-class and end-of-class count above to see session history here.",
    });
    return;
  }
  container.innerHTML = `
    <div class="event-list">
      ${sessions.map(headcountRowHtml).join("")}
    </div>`;
}

function headcountRowHtml(session) {
  const start = session.start ? session.start.count : null;
  const end = session.end ? session.end.count : null;
  const diff = start != null && end != null ? end - start : null;
  const diffLabel = diff == null
    ? "—"
    : diff === 0 ? "No change" : diff > 0 ? `+${diff}` : `${diff}`;
  return `
    <div class="event-row headcount-row">
      <div class="row-desc">
        <p class="title">${session.class_date}</p>
        <p class="sub">Beginning: ${start ?? "Not recorded"} &bull; Before end: ${end ?? "Not recorded"}</p>
      </div>
      <div class="col-date">${diffLabel}</div>
    </div>`;
}
