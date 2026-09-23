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
};
