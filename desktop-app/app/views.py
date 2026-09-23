"""The three main screens: Dashboard, Events & Logs, Event Detail.

Each view is built fresh on navigation (no manual state-diffing/refresh
logic) -- MainWindow swaps the QStackedWidget's current widget for a new
instance, mirroring the "re-render per route" approach used in the earlier
web prototype's JS views.
"""
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QFrame, QScrollArea, QSizePolicy, QSpacerItem,
)

from . import data, icons, theme, widgets
from .video_player import VideoPlayer
from .snapshot import make_snapshot_pixmap

CATEGORY_TABS = [
    ("all", "All"), ("standing", "Standing"), ("trash", "Trash"),
    ("misaligned", "Misaligned Seats"), ("other", "Other"),
]


def _scrollable(content: QWidget) -> QScrollArea:
    area = QScrollArea()
    area.setWidgetResizable(True)
    area.setWidget(content)
    return area


def _page_header(title: str, subtitle: str) -> QVBoxLayout:
    layout = QVBoxLayout()
    layout.setSpacing(4)
    t = QLabel(title)
    t.setObjectName("PageTitle")
    layout.addWidget(t)
    s = QLabel(subtitle)
    s.setObjectName("PageSubtitle")
    s.setWordWrap(True)
    layout.addWidget(s)
    return layout


# ============================================================== Dashboard
class DashboardView(QWidget):
    def __init__(self, go_events, go_event_detail, parent=None):
        super().__init__(parent)
        self.go_events = go_events
        self.go_event_detail = go_event_detail

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        content = QWidget()
        self.layout_ = QVBoxLayout(content)
        self.layout_.setContentsMargins(theme.SPACE_2XL, theme.SPACE_2XL, theme.SPACE_2XL, theme.SPACE_2XL)
        self.layout_.setSpacing(theme.SPACE_LG)
        outer.addWidget(_scrollable(content))

        self.layout_.addLayout(_page_header(
            "Dashboard",
            "Overview of detected classroom events. This view shows summaries only — no live camera feed.",
        ))

        self.body = QVBoxLayout()
        self.body.setSpacing(theme.SPACE_LG)
        self.layout_.addLayout(self.body)
        self.layout_.addStretch()

        loading = QLabel("Loading dashboard…")
        loading.setObjectName("StateDesc")
        self.body.addWidget(loading)

        QTimer.singleShot(150, self._load)

    def _load(self):
        widgets.clear_layout(self.body)
        try:
            summary = data.get_summary()
        except Exception:
            self.body.addWidget(widgets.state_panel(
                "alert_circle", "Unable to load dashboard data",
                "Something went wrong reading local data.", error=True,
                retry_callback=self._load,
            ))
            return

        grid = QGridLayout()
        grid.setSpacing(theme.SPACE_LG)
        grid.addWidget(widgets.stat_card("Total Events", summary["total_events"], "All recorded events"), 0, 0)
        grid.addWidget(widgets.stat_card("Events Today", summary["events_today"]), 0, 1)
        cats = list(summary["by_category"].items())
        for i, (cat, n) in enumerate(cats):
            row, col = divmod(i, 2)
            grid.addWidget(widgets.stat_card("", n, badge_category=cat), row + 1, col if i % 2 == 0 else col)
        for c in range(2):
            grid.setColumnStretch(c, 1)
        self.body.addLayout(grid)

        section = QHBoxLayout()
        title = QLabel("Recent Events")
        title.setObjectName("SectionTitle")
        section.addWidget(title)
        section.addStretch()
        view_all = QPushButton("View all →")
        view_all.setObjectName("LinkButton")
        view_all.setCursor(Qt.PointingHandCursor)
        view_all.clicked.connect(lambda: self.go_events())
        section.addWidget(view_all)
        self.body.addLayout(section)

        if not summary["recent"]:
            self.body.addWidget(widgets.state_panel(
                "inbox", "No events detected yet",
                "Detected classroom events will appear here as they happen.",
            ))
            return

        event_grid = QGridLayout()
        event_grid.setSpacing(theme.SPACE_LG)
        for i, ev in enumerate(summary["recent"]):
            row, col = divmod(i, 2)
            event_grid.addWidget(widgets.event_card(ev, self.go_event_detail), row, col)
        for c in range(2):
            event_grid.setColumnStretch(c, 1)
        self.body.addLayout(event_grid)


# ============================================================ Events/Logs
class EventsView(QWidget):
    PAGE_SIZE = 10

    def __init__(self, go_event_detail, initial_category="all", parent=None):
        super().__init__(parent)
        self.go_event_detail = go_event_detail
        self.category = initial_category
        self.date_range = "all"
        self.query = ""
        self.sort = "newest"
        self.offset = 0

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        content = QWidget()
        self.layout_ = QVBoxLayout(content)
        self.layout_.setContentsMargins(theme.SPACE_2XL, theme.SPACE_2XL, theme.SPACE_2XL, theme.SPACE_2XL)
        self.layout_.setSpacing(theme.SPACE_LG)
        outer.addWidget(_scrollable(content))

        self.layout_.addLayout(_page_header(
            "Events && Logs", "Complete chronological record of detected events for this classroom.",
        ))

        toolbar = QHBoxLayout()
        toolbar.setSpacing(theme.SPACE_SM)
        self.search = QLineEdit()
        self.search.setObjectName("SearchField")
        self.search.setPlaceholderText("Search events…")
        self.search.setMaximumWidth(280)
        self._debounce = QTimer(self)
        self._debounce.setSingleShot(True)
        self._debounce.timeout.connect(self._apply_search)
        self.search.textChanged.connect(lambda _: self._debounce.start(300))
        toolbar.addWidget(self.search)

        self.range_box = QComboBox()
        self.range_box.addItem("All time", "all")
        self.range_box.addItem("Today", "today")
        self.range_box.addItem("Last 7 days", "7d")
        self.range_box.currentIndexChanged.connect(self._on_range_changed)
        toolbar.addWidget(self.range_box)

        self.sort_box = QComboBox()
        self.sort_box.addItem("Newest first", "newest")
        self.sort_box.addItem("Oldest first", "oldest")
        self.sort_box.currentIndexChanged.connect(self._on_sort_changed)
        toolbar.addWidget(self.sort_box)
        toolbar.addStretch()
        self.layout_.addLayout(toolbar)

        self.tab_row = QHBoxLayout()
        self.tab_row.setSpacing(theme.SPACE_SM)
        self.tab_buttons = {}
        for value, label in CATEGORY_TABS:
            btn = QPushButton(label)
            btn.setObjectName("Tab")
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda _, v=value: self._on_tab(v))
            self.tab_row.addWidget(btn)
            self.tab_buttons[value] = btn
        self.tab_row.addStretch()
        self.layout_.addLayout(self.tab_row)

        self.body = QVBoxLayout()
        self.body.setSpacing(theme.SPACE_SM)
        self.layout_.addLayout(self.body)
        self.layout_.addStretch()

        self._update_tab_styles()
        QTimer.singleShot(150, self._load)

    def _update_tab_styles(self):
        for value, btn in self.tab_buttons.items():
            btn.setProperty("active", "true" if value == self.category else "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def _on_tab(self, value):
        self.category = value
        self.offset = 0
        self._update_tab_styles()
        self._load()

    def _on_range_changed(self, idx):
        self.date_range = self.range_box.itemData(idx)
        self.offset = 0
        self._load()

    def _on_sort_changed(self, idx):
        self.sort = self.sort_box.itemData(idx)
        self.offset = 0
        self._load()

    def _apply_search(self):
        self.query = self.search.text().strip()
        self.offset = 0
        self._load()

    def _load(self):
        widgets.clear_layout(self.body)
        try:
            result = data.list_events(
                category=self.category, date_range=self.date_range, query=self.query,
                sort=self.sort, limit=self.PAGE_SIZE, offset=self.offset,
            )
        except Exception:
            self.body.addWidget(widgets.state_panel(
                "alert_circle", "Unable to load events",
                "Something went wrong reading local data.", error=True, retry_callback=self._load,
            ))
            return

        if not result["events"]:
            filtered = self.category != "all" or self.date_range != "all" or self.query
            if filtered:
                self.body.addWidget(widgets.state_panel(
                    "search", "No events match your filters",
                    "Try a different category, date range, or search term.",
                ))
            else:
                self.body.addWidget(widgets.state_panel(
                    "inbox", "No events detected for this period",
                    "Detected classroom events will appear here as they happen.",
                ))
            return

        list_frame = QFrame()
        list_frame.setObjectName("EventListContainer")
        list_frame.setAttribute(Qt.WA_StyledBackground, True)
        list_layout = QVBoxLayout(list_frame)
        list_layout.setContentsMargins(0, 0, 0, 0)
        list_layout.setSpacing(0)
        for ev in result["events"]:
            list_layout.addWidget(widgets.event_row(ev, self.go_event_detail))
        self.body.addWidget(list_frame)

        total_pages = max(1, -(-result["total"] // self.PAGE_SIZE))
        current_page = self.offset // self.PAGE_SIZE + 1
        pagination = QHBoxLayout()
        info = QLabel(f"{result['total']} event{'s' if result['total'] != 1 else ''} • page {current_page} of {total_pages}")
        info.setObjectName("EventMeta")
        pagination.addWidget(info)
        pagination.addStretch()
        prev_btn = QPushButton("Previous")
        prev_btn.setObjectName("SecondaryButton")
        prev_btn.setEnabled(self.offset > 0)
        prev_btn.clicked.connect(self._prev_page)
        pagination.addWidget(prev_btn)
        next_btn = QPushButton("Next")
        next_btn.setObjectName("SecondaryButton")
        next_btn.setEnabled(self.offset + self.PAGE_SIZE < result["total"])
        next_btn.clicked.connect(self._next_page)
        pagination.addWidget(next_btn)
        self.body.addLayout(pagination)

    def _prev_page(self):
        self.offset = max(0, self.offset - self.PAGE_SIZE)
        self._load()

    def _next_page(self):
        self.offset += self.PAGE_SIZE
        self._load()


# ============================================================ Event Detail
class EventDetailView(QWidget):
    def __init__(self, event_id: int, go_back, parent=None):
        super().__init__(parent)
        self.event_id = event_id
        self.go_back = go_back
        self.video_player: VideoPlayer | None = None

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        content = QWidget()
        self.layout_ = QVBoxLayout(content)
        self.layout_.setContentsMargins(theme.SPACE_2XL, theme.SPACE_2XL, theme.SPACE_2XL, theme.SPACE_2XL)
        self.layout_.setSpacing(theme.SPACE_LG)
        outer.addWidget(_scrollable(content))

        back = QPushButton("←  Back to Events && Logs")
        back.setObjectName("BackLink")
        back.setCursor(Qt.PointingHandCursor)
        back.clicked.connect(lambda: self.go_back())
        header = QHBoxLayout()
        header.addWidget(back)
        header.addStretch()
        self.layout_.addLayout(header)

        self.body = QHBoxLayout()
        self.body.setSpacing(theme.SPACE_2XL)
        self.layout_.addLayout(self.body)
        self.layout_.addStretch()

        loading = QLabel("Loading event…")
        loading.setObjectName("StateDesc")
        self.body.addWidget(loading)

        QTimer.singleShot(120, self._load)

    def _load(self):
        widgets.clear_layout(self.body)
        event = data.get_event(self.event_id)
        if event is None:
            self.body.addWidget(widgets.state_panel(
                "alert_circle", "Event not found",
                "This event may have been removed, or the reference is incorrect.",
            ))
            return
        self.event = event

        # ---- evidence card (left, wider) ----
        evidence_card = QFrame()
        evidence_card.setObjectName("EvidenceCard")
        evidence_card.setAttribute(Qt.WA_StyledBackground, True)
        evidence_layout = QVBoxLayout(evidence_card)
        evidence_layout.setContentsMargins(0, 0, 0, 0)
        evidence_layout.setSpacing(0)

        tabs_row = QHBoxLayout()
        tabs_row.setSpacing(0)
        self.video_tab_btn = QPushButton("Video Evidence")
        self.video_tab_btn.setObjectName("EvidenceTabBtn")
        self.video_tab_btn.setCursor(Qt.PointingHandCursor)
        self.screenshot_tab_btn = QPushButton("Screenshot Evidence")
        self.screenshot_tab_btn.setObjectName("EvidenceTabBtn")
        self.screenshot_tab_btn.setCursor(Qt.PointingHandCursor)
        self.video_tab_btn.clicked.connect(lambda: self._show_tab("video"))
        self.screenshot_tab_btn.clicked.connect(lambda: self._show_tab("screenshot"))
        tabs_row.addWidget(self.video_tab_btn, stretch=1)
        tabs_row.addWidget(self.screenshot_tab_btn, stretch=1)
        evidence_layout.addLayout(tabs_row)

        self.evidence_body = QVBoxLayout()
        self.evidence_body.setContentsMargins(theme.SPACE_LG, theme.SPACE_LG, theme.SPACE_LG, theme.SPACE_LG)
        evidence_wrap = QWidget()
        evidence_wrap.setLayout(self.evidence_body)
        evidence_layout.addWidget(evidence_wrap)

        self.body.addWidget(evidence_card, stretch=2)

        # ---- info card (right, narrower) ----
        info_card = QFrame()
        info_card.setObjectName("Card")
        info_card.setAttribute(Qt.WA_StyledBackground, True)
        info_card.setMaximumWidth(300)
        info_layout = QVBoxLayout(info_card)
        info_layout.setContentsMargins(theme.SPACE_LG, theme.SPACE_LG, theme.SPACE_LG, theme.SPACE_LG)
        info_layout.setSpacing(theme.SPACE_SM)
        info_layout.addWidget(widgets.make_badge(event["category"]), alignment=Qt.AlignLeft)
        title = QLabel(event["title"])
        title.setStyleSheet(f"font-size: 20px; font-weight: 700; color: {theme.TEXT_PRIMARY};")
        title.setWordWrap(True)
        info_layout.addWidget(title)
        desc = QLabel(event["description"])
        desc.setObjectName("EventDesc")
        desc.setWordWrap(True)
        info_layout.addWidget(desc)
        meta = QLabel(f"{event['date_label']} {event['time_label']}")
        meta.setObjectName("EventMeta")
        info_layout.addWidget(meta)
        info_layout.addWidget(widgets.make_evidence_tag(event), alignment=Qt.AlignLeft)

        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setStyleSheet(f"color: {theme.BORDER_DEFAULT};")
        info_layout.addWidget(divider)
        privacy = QLabel(
            "Shows only what's needed to review this event. No student names, "
            "IDs, or facial-recognition results are captured or displayed."
        )
        privacy.setWordWrap(True)
        privacy.setStyleSheet(f"font-size: 11.5px; color: {theme.TEXT_TERTIARY};")
        info_layout.addWidget(privacy)
        info_layout.addStretch()

        self.body.addWidget(info_card, stretch=1)

        self._show_tab("video")

    def _show_tab(self, tab: str):
        self.video_tab_btn.setProperty("active", "true" if tab == "video" else "false")
        self.screenshot_tab_btn.setProperty("active", "true" if tab == "screenshot" else "false")
        for btn in (self.video_tab_btn, self.screenshot_tab_btn):
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        if self.video_player is not None:
            self.video_player.stop_timer()
        widgets.clear_layout(self.evidence_body)
        self.video_player = None

        if tab == "video":
            if not self.event["video_available"]:
                self.evidence_body.addWidget(widgets.state_panel(
                    "alert_circle", "Evidence unavailable",
                    self.event["evidence_note"] or "Video evidence could not be retrieved for this event.",
                ))
                return
            self.video_player = VideoPlayer(self.event)
            self.evidence_body.addWidget(self.video_player)
        else:
            if not self.event["snapshot_available"]:
                self.evidence_body.addWidget(widgets.state_panel(
                    "alert_circle", "Evidence unavailable",
                    self.event["evidence_note"] or "Snapshot evidence could not be retrieved for this event.",
                ))
                return
            frame = QFrame()
            frame.setObjectName("ScreenshotFrame")
            frame.setAttribute(Qt.WA_StyledBackground, True)
            flayout = QVBoxLayout(frame)
            flayout.setContentsMargins(0, 0, 0, 0)
            flayout.setSpacing(0)
            img = QLabel()
            img.setPixmap(make_snapshot_pixmap(self.event["category"], 600, 338))
            img.setAlignment(Qt.AlignCenter)
            flayout.addWidget(img)
            caption = QLabel(f"Snapshot captured at {self.event['time_label']} on {self.event['date_label']}")
            caption.setObjectName("ScreenshotCaption")
            flayout.addWidget(caption)
            self.evidence_body.addWidget(frame)

    def cleanup(self):
        if self.video_player is not None:
            self.video_player.stop_timer()
