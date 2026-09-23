async function renderEventDetail(root, id) {
  root.innerHTML = `
    <div class="detail-header">
      <a class="back-link" href="#/dashboard">${iconHtml("chevronLeft", "var(--text-secondary)", 16)} Back</a>
    </div>
    <div class="skeleton skeleton-card" style="height:420px"></div>
  `;

  let event;
  try {
    event = await Api.event(id);
  } catch (err) {
    root.innerHTML = `
      <div class="detail-header">
        <a class="back-link" href="#/events">${iconHtml("chevronLeft", "var(--text-secondary)", 16)} Back to Events &amp; Logs</a>
      </div>
      ${err.message === "not_found"
        ? emptyStateHtml({ icon: "alertCircle", title: "Event not found", desc: "This event may have been removed, or the link is incorrect." })
        : errorStateHtml({ title: "Unable to load this event", desc: "The admin UI couldn't reach the backend. Check that the app server is running and try again." })}
    `;
    root.querySelector('[data-action="retry"]')?.addEventListener("click", () => renderEventDetail(root, id));
    return;
  }

  root.innerHTML = `
    <div class="detail-header">
      <a class="back-link" href="#/events">${iconHtml("chevronLeft", "var(--text-secondary)", 16)} Back to Events &amp; Logs</a>
    </div>
    <div class="detail-grid">
      <div>
        <div class="evidence-card">
          <div class="evidence-tabs" id="evidence-tabs">
            <button class="evidence-tab active" data-tab="video">Video Evidence</button>
            <button class="evidence-tab" data-tab="screenshot">Screenshot Evidence</button>
          </div>
          <div class="evidence-body" id="evidence-body"></div>
        </div>
      </div>
      <div class="info-card">
        ${categoryBadgeHtml(event)}
        <h1 class="title">${event.title}</h1>
        <p class="desc">${event.description}</p>
        <div class="meta">
          <span>${event.date_label}</span>
          <span>${event.time_label}</span>
        </div>
        ${evidenceTagHtml(event)}
        <p class="privacy-note">Shows only what's needed to review this event. No student names, IDs, or facial-recognition results are captured or displayed.</p>
      </div>
    </div>
  `;

  const evidenceBody = root.querySelector("#evidence-body");
  const tabs = root.querySelector("#evidence-tabs");

  function showTab(tab) {
    tabs.querySelectorAll(".evidence-tab").forEach((t) => t.classList.toggle("active", t.dataset.tab === tab));
    if (tab === "video") renderVideoTab(evidenceBody, event);
    else renderScreenshotTab(evidenceBody, event);
  }

  tabs.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-tab]");
    if (btn) showTab(btn.dataset.tab);
  });

  showTab("video");
}

function renderVideoTab(container, event) {
  if (!event.video_available) {
    container.innerHTML = emptyStateHtml({
      icon: "alertCircle",
      title: "Evidence unavailable",
      desc: event.evidence_note || "Video evidence could not be retrieved for this event.",
    });
    return;
  }

  container.innerHTML = `
    <div class="video-player">
      <div class="video-stage">
        ${event.snapshot_url ? `<img src="${event.snapshot_url}" alt="" />` : ""}
        <div class="timestamp-badge">Recorded around ${event.time_label}</div>
        <button class="play-btn" id="play-btn">${iconHtml("play", "var(--gray-900)", 20)}</button>
      </div>
      <div class="video-controls">
        <div class="video-track" id="video-track"><div class="fill" id="video-fill"></div></div>
        <div class="video-control-row">
          <div class="left">
            <button id="toggle-btn">${iconHtml("play", "#fff", 18)}</button>
            <span class="video-time" id="video-time">00:00 / 00:08</span>
          </div>
          <div class="right">
            <button>${iconHtml("volume", "#fff", 18)}</button>
            <button>${iconHtml("fullscreen", "#fff", 18)}</button>
          </div>
        </div>
      </div>
    </div>
    <p class="video-disclaimer">Demo playback is simulated for this design preview -- real event video capture, storage, and retrieval is a planned capability. See the admin-ui CLAUDE.md for backend requirements.</p>
  `;

  const DURATION = 8; // seconds, simulated
  let elapsed = 0;
  let playing = false;
  let timer = null;

  const fill = container.querySelector("#video-fill");
  const timeLabel = container.querySelector("#video-time");
  const playBtn = container.querySelector("#play-btn");
  const toggleBtn = container.querySelector("#toggle-btn");

  function format(t) {
    const m = Math.floor(t / 60).toString().padStart(2, "0");
    const s = Math.floor(t % 60).toString().padStart(2, "0");
    return `${m}:${s}`;
  }
  function update() {
    fill.style.width = `${(elapsed / DURATION) * 100}%`;
    timeLabel.textContent = `${format(elapsed)} / ${format(DURATION)}`;
  }
  function setPlaying(next) {
    playing = next;
    const icon = playing ? "pause" : "play";
    toggleBtn.innerHTML = iconHtml(icon, "#fff", 18);
    playBtn.style.display = playing ? "none" : "flex";
    if (playing) {
      timer = setInterval(() => {
        elapsed += 0.2;
        if (elapsed >= DURATION) { elapsed = DURATION; setPlaying(false); }
        update();
      }, 200);
    } else {
      clearInterval(timer);
    }
  }
  playBtn.addEventListener("click", () => setPlaying(true));
  toggleBtn.addEventListener("click", () => setPlaying(!playing));
  container.querySelector("#video-track").addEventListener("click", (e) => {
    const rect = e.currentTarget.getBoundingClientRect();
    elapsed = Math.max(0, Math.min(DURATION, ((e.clientX - rect.left) / rect.width) * DURATION));
    update();
  });
  update();
}

function renderScreenshotTab(container, event) {
  if (!event.snapshot_available) {
    container.innerHTML = emptyStateHtml({
      icon: "alertCircle",
      title: "Evidence unavailable",
      desc: event.evidence_note || "Snapshot evidence could not be retrieved for this event.",
    });
    return;
  }
  container.innerHTML = `
    <div class="screenshot-viewer">
      <img src="${event.snapshot_url}" alt="Snapshot evidence for this event" />
      <div class="screenshot-caption">Snapshot captured at ${event.time_label} on ${event.date_label}</div>
    </div>
  `;
}
