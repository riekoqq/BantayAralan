const HEADCOUNT_SCHEDULE_POLL_MS = 20000;

const HEADCOUNT_STATUS_TEXT = {
  waiting: (ev) => `Waiting for ${ev.label} (${ev.scheduled_time})`,
  performing: () => "Performing Head Count…",
  complete: (ev) => `${ev.label} Complete`,
  missed: () => "Missed -- app started after the scheduled time",
};

async function renderHeadcount(root) {
  root.innerHTML = `
    <div class="page-header">
      <h1 class="page-title">Head Count</h1>
      <p class="page-subtitle">Aggregate student head counts recorded at the beginning and near the end of a class session -- not attendance identification. No names or IDs are recorded.</p>
    </div>
    <div class="section-header">
      <h2 class="section-title">Today's Scheduled Head Counts</h2>
    </div>
    <div id="headcount-schedule">${skeletonGrid("card", 2)}</div>

    <div class="section-header" style="margin-top: var(--space-2xl)">
      <h2 class="section-title">Manual Entry</h2>
    </div>
    <p class="disclaimer-note">The two counts above happen automatically at their scheduled times. Use this form only to add or correct a count by hand.</p>
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

  async function loadSchedule() {
    const container = root.querySelector("#headcount-schedule");
    if (!container) return; // navigated away
    try {
      const schedule = await Api.headcountSchedule();
      if (!document.body.contains(container)) return; // navigated away mid-fetch
      renderScheduleCards(container, schedule);
    } catch (err) {
      if (document.body.contains(container)) {
        container.innerHTML = errorStateHtml({
          title: "Unable to load today's schedule",
          desc: "The admin UI couldn't reach the backend. Check that the app server is running and try again.",
        });
      }
    }
  }

  async function loadSessions() {
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
      container.querySelector('[data-action="retry"]')?.addEventListener("click", loadSessions);
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
      await Promise.all([loadSessions(), loadSchedule()]);
    } catch (err) {
      feedback.innerHTML = `<p class="form-error">Couldn't save this count. Check that the app server is running and try again.</p>`;
    } finally {
      btn.disabled = false;
    }
  });

  loadSchedule();
  loadSessions();

  // Poll the schedule while this page is open, so an automatic head count
  // shows up without a manual refresh. Self-cancels once the view is
  // navigated away (its container leaves the DOM) -- app.js's router
  // replaces #view-root wholesale on every navigation with no per-view
  // cleanup hook, so this guard is what stops the interval from leaking.
  const pollTimer = setInterval(() => {
    if (!document.body.contains(root)) {
      clearInterval(pollTimer);
      return;
    }
    loadSchedule();
  }, HEADCOUNT_SCHEDULE_POLL_MS);
}

function renderScheduleCards(container, schedule) {
  container.innerHTML = `
    <div class="schedule-grid">
      ${schedule.events.map(scheduleCardHtml).join("")}
    </div>`;
}

function scheduleCardHtml(ev) {
  const statusText = (HEADCOUNT_STATUS_TEXT[ev.status] || HEADCOUNT_STATUS_TEXT.waiting)(ev);
  const detected = ev.detected_count != null ? ev.detected_count : null;
  return `
    <div class="schedule-card status-${ev.status}">
      <div class="schedule-card-header">
        <span class="schedule-status-dot"></span>
        <span class="schedule-card-title">${ev.label}</span>
      </div>
      <p class="schedule-status-text">${statusText}</p>
      <dl class="schedule-details">
        <div><dt>Expected</dt><dd>${"—"}</dd></div>
        <div><dt>Detected</dt><dd>${detected != null ? detected : "—"}</dd></div>
        <div><dt>Scheduled Time</dt><dd>${ev.scheduled_time}</dd></div>
        <div><dt>Status</dt><dd>${ev.status === "complete" ? "Complete" : ev.status === "missed" ? "Missed" : ev.status === "performing" ? "In Progress" : "Pending"}</dd></div>
      </dl>
    </div>`;
}

function renderSessions(container, sessions) {
  if (!sessions || sessions.length === 0) {
    container.innerHTML = emptyStateHtml({
      icon: "users",
      title: "No head counts recorded yet",
      desc: "Scheduled counts will appear here automatically, or record one by hand above.",
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
  const startLabel = start != null ? `${start}${session.start.source === "scheduled" ? " (auto)" : ""}` : "Not recorded";
  const endLabel = end != null ? `${end}${session.end.source === "scheduled" ? " (auto)" : ""}` : "Not recorded";
  return `
    <div class="event-row headcount-row">
      <div class="row-desc">
        <p class="title">${session.class_date}</p>
        <p class="sub">Beginning: ${startLabel} &bull; Before end: ${endLabel}</p>
      </div>
      <div class="col-date">${diffLabel}</div>
    </div>`;
}
