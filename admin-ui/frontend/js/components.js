const CATEGORY_ICON = { standing: "standing", trash: "trash", misaligned: "misaligned", other: "other" };
const CATEGORY_COLOR = {
  standing: "var(--cat-standing-fg)",
  trash: "var(--cat-trash-fg)",
  misaligned: "var(--cat-misaligned-fg)",
  other: "var(--cat-other-fg)",
};
const CATEGORY_SHORT_LABEL = { standing: "Standing", trash: "Trash", misaligned: "Misaligned Seat", other: "Other" };

function categoryBadgeHtml(event) {
  const icon = CATEGORY_ICON[event.category] || "other";
  const color = CATEGORY_COLOR[event.category] || "var(--cat-other-fg)";
  const label = CATEGORY_SHORT_LABEL[event.category] || event.category_label;
  return `<span class="badge cat-${event.category}">${iconHtml(icon, color, 14)}${label}</span>`;
}

function evidenceTagHtml(event) {
  const map = {
    both: "Video + Snapshot Available",
    snapshot_only: "Snapshot Available",
    video_only: "Video Available",
    unavailable: "Evidence Unavailable",
  };
  const text = map[event.evidence_kind] || "Evidence Unavailable";
  const cls = event.evidence_kind === "unavailable" ? "evidence-tag unavailable" : "evidence-tag";
  return `<span class="${cls}"><span class="dot"></span>${text}</span>`;
}

function eventCardHtml(event) {
  return `
    <article class="event-card" data-event-id="${event.id}" role="button" tabindex="0">
      ${categoryBadgeHtml(event)}
      <h3 class="title">${event.title}</h3>
      <p class="desc">${event.description}</p>
      <div class="datetime">${event.date_label} &bull; ${event.time_label}</div>
      ${evidenceTagHtml(event)}
    </article>`;
}

function eventRowHtml(event) {
  return `
    <div class="event-row" data-event-id="${event.id}" role="button" tabindex="0">
      ${categoryBadgeHtml(event)}
      <div class="row-desc">
        <p class="title">${event.title}</p>
        <p class="sub">${event.description}</p>
      </div>
      <div class="col-date">${event.date_label}</div>
      <div class="col-time">${event.time_label}</div>
      ${evidenceTagHtml(event)}
      <span class="chevron">${iconHtml("chevronRight", "var(--text-tertiary)", 16)}</span>
    </div>`;
}

function statCardHtml(label, number, sub) {
  return `
    <div class="stat-card">
      <span class="stat-label">${label}</span>
      <span class="stat-number">${number}</span>
      ${sub ? `<span class="stat-sub">${sub}</span>` : ""}
    </div>`;
}

function skeletonGrid(kind, count) {
  return Array.from({ length: count }).map(() => `<div class="skeleton skeleton-${kind}"></div>`).join("");
}

function emptyStateHtml({ icon = "inbox", title, desc }) {
  return `
    <div class="state-panel">
      <div class="state-icon">${iconHtml(icon, "currentColor", 36)}</div>
      <p class="state-title">${title}</p>
      <p class="state-desc">${desc}</p>
    </div>`;
}

function errorStateHtml({ title = "Something went wrong", desc = "Please try again.", retryLabel = "Retry" } = {}) {
  return `
    <div class="state-panel error">
      <div class="state-icon">${iconHtml("alertCircle", "currentColor", 36)}</div>
      <p class="state-title">${title}</p>
      <p class="state-desc">${desc}</p>
      <button class="btn btn-secondary" data-action="retry">${retryLabel}</button>
    </div>`;
}

function attachEventCardNavigation(root) {
  root.querySelectorAll("[data-event-id]").forEach((el) => {
    const go = () => { window.location.hash = `#/events/${el.dataset.eventId}`; };
    el.addEventListener("click", go);
    el.addEventListener("keydown", (e) => { if (e.key === "Enter") go(); });
  });
}
