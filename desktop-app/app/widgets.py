"""Small reusable widgets shared across views -- the native-app equivalent
of admin-ui/frontend/js/components.js.
"""
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QWidget, QSizePolicy,
)

from . import icons, theme


class ClickableFrame(QFrame):
    clicked = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


def make_badge(category: str) -> QFrame:
    colors = theme.CATEGORY_COLORS.get(category, theme.CATEGORY_COLORS["other"])
    from .data import CATEGORY_SHORT_LABELS

    frame = QFrame()
    frame.setObjectName("Badge")
    frame.setAttribute(Qt.WA_StyledBackground, True)
    frame.setStyleSheet(f"QFrame#Badge {{ background: {colors['bg']}; border-radius: {theme.RADIUS_FULL}px; }}")
    layout = QHBoxLayout(frame)
    layout.setContentsMargins(10, 5, 12, 5)
    layout.setSpacing(6)

    icon_label = QLabel()
    icon_label.setPixmap(icons.pixmap(colors["icon"], colors["fg"], 13))
    layout.addWidget(icon_label)

    text = QLabel(CATEGORY_SHORT_LABELS.get(category, category.title()))
    text.setObjectName("BadgeText")
    text.setStyleSheet(f"color: {colors['fg']};")
    layout.addWidget(text)
    frame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    return frame


EVIDENCE_LABELS = {
    "both": "Video + Snapshot Available",
    "snapshot_only": "Snapshot Available",
    "video_only": "Video Available",
    "unavailable": "Evidence Unavailable",
}


def make_evidence_tag(event: dict) -> QFrame:
    kind = event["evidence_kind"]
    unavailable = kind == "unavailable"
    frame = QFrame()
    frame.setObjectName("EvidenceTag")
    frame.setProperty("unavailable", "true" if unavailable else "false")
    frame.setAttribute(Qt.WA_StyledBackground, True)
    layout = QHBoxLayout(frame)
    layout.setContentsMargins(9, 4, 9, 4)
    layout.setSpacing(6)

    dot = QLabel()
    dot.setFixedSize(6, 6)
    color = theme.TEXT_TERTIARY if unavailable else theme.SUCCESS
    dot.setStyleSheet(f"background: {color}; border-radius: 3px;")
    layout.addWidget(dot)

    text = QLabel(EVIDENCE_LABELS[kind])
    text.setObjectName("EvidenceText")
    text.setProperty("unavailable", "true" if unavailable else "false")
    layout.addWidget(text)
    frame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    return frame


def stat_card(label: str, number, sub: str = None, badge_category: str = None) -> QFrame:
    frame = QFrame()
    frame.setObjectName("Card")
    frame.setAttribute(Qt.WA_StyledBackground, True)
    layout = QVBoxLayout(frame)
    layout.setContentsMargins(theme.SPACE_LG, theme.SPACE_LG, theme.SPACE_LG, theme.SPACE_LG)
    layout.setSpacing(4)

    if badge_category:
        row = QHBoxLayout()
        row.addWidget(make_badge(badge_category))
        row.addStretch()
        num = QLabel(str(number))
        num.setStyleSheet(f"font-size: 20px; font-weight: 700; color: {theme.TEXT_PRIMARY};")
        row.addWidget(num)
        layout.addLayout(row)
        return frame

    lbl = QLabel(label.upper())
    lbl.setObjectName("StatLabel")
    layout.addWidget(lbl)
    num = QLabel(str(number))
    num.setObjectName("StatNumber")
    layout.addWidget(num)
    if sub:
        sub_lbl = QLabel(sub)
        sub_lbl.setObjectName("StatSub")
        layout.addWidget(sub_lbl)
    return frame


def event_card(event: dict, on_click) -> ClickableFrame:
    frame = ClickableFrame()
    frame.setObjectName("Card")
    frame.setAttribute(Qt.WA_StyledBackground, True)
    layout = QVBoxLayout(frame)
    layout.setContentsMargins(theme.SPACE_LG, theme.SPACE_LG, theme.SPACE_LG, theme.SPACE_LG)
    layout.setSpacing(theme.SPACE_SM)

    layout.addWidget(make_badge(event["category"]), alignment=Qt.AlignLeft)

    title = QLabel(event["title"])
    title.setObjectName("EventTitle")
    layout.addWidget(title)

    desc = QLabel(event["description"])
    desc.setObjectName("EventDesc")
    desc.setWordWrap(True)
    layout.addWidget(desc)

    meta = QLabel(f"{event['date_label']}  •  {event['time_label']}")
    meta.setObjectName("EventMeta")
    layout.addWidget(meta)

    layout.addWidget(make_evidence_tag(event), alignment=Qt.AlignLeft)

    frame.clicked.connect(lambda: on_click(event["id"]))
    return frame


def event_row(event: dict, on_click) -> ClickableFrame:
    frame = ClickableFrame()
    frame.setObjectName("EventRow")
    frame.setAttribute(Qt.WA_StyledBackground, True)
    layout = QHBoxLayout(frame)
    layout.setContentsMargins(theme.SPACE_LG, theme.SPACE_MD, theme.SPACE_LG, theme.SPACE_MD)
    layout.setSpacing(theme.SPACE_LG)

    badge = make_badge(event["category"])
    badge.setMinimumWidth(140)
    layout.addWidget(badge)

    desc_col = QVBoxLayout()
    desc_col.setSpacing(2)
    title = QLabel(event["title"])
    title.setObjectName("EventTitle")
    title.setStyleSheet("font-size: 13.5px;")
    desc_col.addWidget(title)
    sub = QLabel(event["description"])
    sub.setObjectName("EventMeta")
    sub.setStyleSheet(f"font-size: 12px; color: {theme.TEXT_TERTIARY};")
    desc_col.addWidget(sub)
    desc_wrap = QWidget()
    desc_wrap.setLayout(desc_col)
    desc_wrap.setMinimumWidth(160)
    layout.addWidget(desc_wrap, stretch=1)

    date_lbl = QLabel(event["date_label"])
    date_lbl.setMinimumWidth(150)
    date_lbl.setStyleSheet(f"font-size: 13px; color: {theme.TEXT_SECONDARY};")
    layout.addWidget(date_lbl)

    time_lbl = QLabel(event["time_label"])
    time_lbl.setMinimumWidth(85)
    time_lbl.setStyleSheet(f"font-size: 13px; color: {theme.TEXT_SECONDARY};")
    layout.addWidget(time_lbl)

    layout.addWidget(make_evidence_tag(event))

    chevron = QLabel()
    chevron.setPixmap(icons.pixmap("chevron_right", theme.TEXT_TERTIARY, 16))
    layout.addWidget(chevron)

    frame.clicked.connect(lambda: on_click(event["id"]))
    return frame


def state_panel(icon_name: str, title: str, desc: str, error: bool = False,
                 retry_callback=None) -> QWidget:
    wrap = QWidget()
    layout = QVBoxLayout(wrap)
    layout.setAlignment(Qt.AlignCenter)
    layout.setSpacing(8)
    layout.setContentsMargins(48, 64, 48, 64)

    icon_lbl = QLabel()
    color = theme.DANGER if error else theme.TEXT_TERTIARY
    icon_lbl.setPixmap(icons.pixmap(icon_name, color, 36))
    icon_lbl.setAlignment(Qt.AlignCenter)
    layout.addWidget(icon_lbl)

    title_lbl = QLabel(title)
    title_lbl.setObjectName("StateTitle")
    title_lbl.setAlignment(Qt.AlignCenter)
    layout.addWidget(title_lbl)

    desc_lbl = QLabel(desc)
    desc_lbl.setObjectName("StateDesc")
    desc_lbl.setAlignment(Qt.AlignCenter)
    desc_lbl.setWordWrap(True)
    desc_lbl.setMaximumWidth(360)
    layout.addWidget(desc_lbl, alignment=Qt.AlignCenter)

    if retry_callback:
        btn = QPushButton("Retry")
        btn.setObjectName("SecondaryButton")
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(retry_callback)
        layout.addWidget(btn, alignment=Qt.AlignCenter)

    return wrap


def clear_layout(layout):
    while layout.count():
        item = layout.takeAt(0)
        w = item.widget()
        if w is not None:
            w.deleteLater()
        elif item.layout() is not None:
            clear_layout(item.layout())
