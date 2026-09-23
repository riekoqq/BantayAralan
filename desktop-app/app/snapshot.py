"""Generates placeholder 'snapshot evidence' images -- the native-app
equivalent of admin-ui/backend/app.py's `_placeholder_svg`. Drawn directly
with QPainter so no bundled image assets are needed.

No real camera imagery is used anywhere in this prototype.
"""
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QPixmap, QColor, QFont, QPen

from . import theme

LABELS = {
    "standing": "Classroom camera view (behavior)",
    "trash": "Top-down camera view (clutter)",
    "misaligned": "Top-down camera view (seat alignment)",
    "other": "Classroom camera view",
}


def make_snapshot_pixmap(category: str, width: int = 640, height: int = 360) -> QPixmap:
    color = theme.CATEGORY_COLORS.get(category, theme.CATEGORY_COLORS["other"])["fg"]
    pm = QPixmap(width, height)
    pm.fill(QColor(theme.GRAY_100))

    painter = QPainter(pm)
    painter.setRenderHint(QPainter.Antialiasing)

    pen = QPen(QColor(color))
    pen.setWidth(3)
    painter.setPen(pen)
    cx, cy = width / 2, height / 2 - 20
    painter.drawEllipse(QRectF(cx - 34, cy - 34, 68, 68))
    painter.drawRect(QRectF(cx - 24, cy - 20, 48, 40))

    painter.setPen(QColor(theme.TEXT_SECONDARY))
    painter.setFont(QFont(theme.FONT_FAMILY.split(",")[0], 11))
    label = LABELS.get(category, LABELS["other"])
    painter.drawText(QRectF(0, cy + 50, width, 20), Qt.AlignCenter, f"{label} — mock evidence placeholder")

    painter.setPen(QColor(theme.TEXT_TERTIARY))
    painter.setFont(QFont(theme.FONT_FAMILY.split(",")[0], 10))
    painter.drawText(QRectF(0, cy + 72, width, 20), Qt.AlignCenter, "No real classroom imagery. No students identified.")

    painter.end()
    return pm
