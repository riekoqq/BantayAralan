const Api = {
  async summary() {
    const r = await fetch("/api/summary");
    if (!r.ok) throw new Error("summary_failed");
    return r.json();
  },
  async status() {
    const r = await fetch("/api/status");
    if (!r.ok) throw new Error("status_failed");
    return r.json();
  },
  async events(params = {}) {
    const qs = new URLSearchParams(params).toString();
    const r = await fetch(`/api/events${qs ? `?${qs}` : ""}`);
    if (!r.ok) throw new Error("events_failed");
    return r.json();
  },
  async event(id) {
    const r = await fetch(`/api/events/${id}`);
    if (!r.ok) {
      if (r.status === 404) throw new Error("not_found");
      throw new Error("event_failed");
    }
    return r.json();
  },
  async headcounts() {
    const r = await fetch("/api/headcounts");
    if (!r.ok) throw new Error("headcounts_failed");
    return r.json();
  },
  async headcountSchedule() {
    const r = await fetch("/api/headcount-schedule");
    if (!r.ok) throw new Error("headcount_schedule_failed");
    return r.json();
  },
  async detectionState() {
    const r = await fetch("/api/detection-state");
    if (!r.ok) throw new Error("detection_state_failed");
    return r.json();
  },
  async setDetectionState(enabled) {
    const r = await fetch("/api/detection-state", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ enabled }),
    });
    if (!r.ok) throw new Error("set_detection_state_failed");
    return r.json();
  },
  async statistics() {
    const r = await fetch("/api/statistics");
    if (!r.ok) throw new Error("statistics_failed");
    return r.json();
  },
  async insights() {
    const r = await fetch("/api/insights");
    if (!r.ok) throw new Error("insights_failed");
    return r.json();
  },
  async suggestions() {
    const r = await fetch("/api/suggestions");
    if (!r.ok) throw new Error("suggestions_failed");
    return r.json();
  },
};
