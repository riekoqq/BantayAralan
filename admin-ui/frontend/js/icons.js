// Small inline icon set (kept dependency-free -- no icon font/library).
const Icons = {
  standing: (c) => `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="6" r="3" stroke="${c}" stroke-width="2"/><path d="M12 11v7M8 20l4-2 4 2M9 14h6" stroke="${c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
  trash: (c) => `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M5 7h14M9 7V5a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2m-9 0 1 12a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2l1-12" stroke="${c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
  misaligned: (c) => `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="3.5" y="3.5" width="9" height="9" rx="1.5" stroke="${c}" stroke-width="2"/><rect x="12.5" y="11.5" width="8" height="8" rx="1.5" stroke="${c}" stroke-width="2"/></svg>`,
  other: (c) => `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 21V3h13l-2.5 4L17 11H6" stroke="${c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
  grid: (c) => `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="3" y="3" width="8" height="8" rx="1.5" stroke="${c}" stroke-width="2"/><rect x="13" y="3" width="8" height="8" rx="1.5" stroke="${c}" stroke-width="2"/><rect x="3" y="13" width="8" height="8" rx="1.5" stroke="${c}" stroke-width="2"/><rect x="13" y="13" width="8" height="8" rx="1.5" stroke="${c}" stroke-width="2"/></svg>`,
  list: (c) => `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01" stroke="${c}" stroke-width="2" stroke-linecap="round"/></svg>`,
  search: (c) => `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="11" cy="11" r="7" stroke="${c}" stroke-width="2"/><path d="m20 20-3.5-3.5" stroke="${c}" stroke-width="2" stroke-linecap="round"/></svg>`,
  chevronRight: (c) => `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="m9 6 6 6-6 6" stroke="${c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
  chevronLeft: (c) => `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="m15 6-6 6 6 6" stroke="${c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
  camera: (c) => `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="3" y="7" width="18" height="13" rx="2" stroke="${c}" stroke-width="2"/><path d="M8 7 9.5 4h5L16 7" stroke="${c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="12" cy="13.5" r="3.5" stroke="${c}" stroke-width="2"/></svg>`,
  play: (c) => `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M8 5v14l11-7L8 5Z" fill="${c}"/></svg>`,
  pause: (c) => `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="6" y="5" width="4" height="14" rx="1" fill="${c}"/><rect x="14" y="5" width="4" height="14" rx="1" fill="${c}"/></svg>`,
  volume: (c) => `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M5 9v6h4l5 4V5L9 9H5Z" fill="${c}"/><path d="M17 9a4 4 0 0 1 0 6" stroke="${c}" stroke-width="2" stroke-linecap="round"/></svg>`,
  fullscreen: (c) => `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 9V5h4M20 9V5h-4M4 15v4h4M20 15v4h-4" stroke="${c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
  alertCircle: (c) => `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="9" stroke="${c}" stroke-width="2"/><path d="M12 8v5M12 16h.01" stroke="${c}" stroke-width="2" stroke-linecap="round"/></svg>`,
  inbox: (c) => `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 12h4l2 3h4l2-3h4" stroke="${c}" stroke-width="2" stroke-linejoin="round"/><path d="M5.5 6h13l1.5 6v7a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1v-7l1.5-6Z" stroke="${c}" stroke-width="2" stroke-linejoin="round"/></svg>`,
};

function iconHtml(name, color, size = 16) {
  const fn = Icons[name] || Icons.other;
  return `<span style="display:inline-flex;width:${size}px;height:${size}px;flex-shrink:0;color:${color}">${fn(color)}</span>`;
}
