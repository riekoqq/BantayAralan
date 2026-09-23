"""Small inline icon set, ported from the web prototype's icons.js.

SVG strings are rasterized on demand via QtSvg -- no icon font, no bundled
image assets, matches the design 1:1 across both prototypes.
"""
from PySide6.QtCore import QByteArray, QSize, Qt
from PySide6.QtGui import QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer

ICONS = {
    "standing": lambda c: f'<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="6" r="3" stroke="{c}" stroke-width="2"/><path d="M12 11v7M8 20l4-2 4 2M9 14h6" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "trash": lambda c: f'<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M5 7h14M9 7V5a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2m-9 0 1 12a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2l1-12" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "misaligned": lambda c: f'<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="3.5" y="3.5" width="9" height="9" rx="1.5" stroke="{c}" stroke-width="2"/><rect x="12.5" y="11.5" width="8" height="8" rx="1.5" stroke="{c}" stroke-width="2"/></svg>',
    "other": lambda c: f'<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 21V3h13l-2.5 4L17 11H6" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "grid": lambda c: f'<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="3" y="3" width="8" height="8" rx="1.5" stroke="{c}" stroke-width="2"/><rect x="13" y="3" width="8" height="8" rx="1.5" stroke="{c}" stroke-width="2"/><rect x="3" y="13" width="8" height="8" rx="1.5" stroke="{c}" stroke-width="2"/><rect x="13" y="13" width="8" height="8" rx="1.5" stroke="{c}" stroke-width="2"/></svg>',
    "list": lambda c: f'<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01" stroke="{c}" stroke-width="2" stroke-linecap="round"/></svg>',
    "search": lambda c: f'<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="11" cy="11" r="7" stroke="{c}" stroke-width="2"/><path d="m20 20-3.5-3.5" stroke="{c}" stroke-width="2" stroke-linecap="round"/></svg>',
    "chevron_right": lambda c: f'<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="m9 6 6 6-6 6" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "chevron_left": lambda c: f'<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="m15 6-6 6 6 6" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "camera": lambda c: f'<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="3" y="7" width="18" height="13" rx="2" stroke="{c}" stroke-width="2"/><path d="M8 7 9.5 4h5L16 7" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="12" cy="13.5" r="3.5" stroke="{c}" stroke-width="2"/></svg>',
    "play": lambda c: f'<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M8 5v14l11-7L8 5Z" fill="{c}"/></svg>',
    "pause": lambda c: f'<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="6" y="5" width="4" height="14" rx="1" fill="{c}"/><rect x="14" y="5" width="4" height="14" rx="1" fill="{c}"/></svg>',
    "volume": lambda c: f'<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M5 9v6h4l5 4V5L9 9H5Z" fill="{c}"/><path d="M17 9a4 4 0 0 1 0 6" stroke="{c}" stroke-width="2" stroke-linecap="round"/></svg>',
    "fullscreen": lambda c: f'<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 9V5h4M20 9V5h-4M4 15v4h4M20 15v4h-4" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "fullscreen_exit": lambda c: f'<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M9 4v4H5M15 4v4h4M9 20v-4H5M15 20v-4h4" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "alert_circle": lambda c: f'<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="9" stroke="{c}" stroke-width="2"/><path d="M12 8v5M12 16h.01" stroke="{c}" stroke-width="2" stroke-linecap="round"/></svg>',
    "inbox": lambda c: f'<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 12h4l2 3h4l2-3h4" stroke="{c}" stroke-width="2" stroke-linejoin="round"/><path d="M5.5 6h13l1.5 6v7a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1v-7l1.5-6Z" stroke="{c}" stroke-width="2" stroke-linejoin="round"/></svg>',
}


def pixmap(name: str, color: str, size: int = 16) -> QPixmap:
    svg = ICONS.get(name, ICONS["other"])(color)
    renderer = QSvgRenderer(QByteArray(svg.encode("utf-8")))
    pm = QPixmap(size, size)
    pm.fill(Qt.transparent)
    painter = QPainter(pm)
    renderer.render(painter)
    painter.end()
    return pm


def icon(name: str, color: str, size: int = 16) -> QIcon:
    return QIcon(pixmap(name, color, size))
