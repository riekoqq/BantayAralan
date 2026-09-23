"""Top-level window: persistent sidebar + a stacked content area that swaps
between Dashboard / Events & Logs / Event Detail.
"""
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel,
    QPushButton, QStackedWidget, QSizePolicy,
)

from . import data, icons, theme
from .views import DashboardView, EventsView, EventDetailView

NAV_ITEMS = [
    ("dashboard", "Dashboard", "grid"),
    ("events", "Events && Logs", "list"),
]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BantayAralan — Admin")
        self.resize(1280, 840)
        self.setMinimumSize(1024, 680)

        root = QWidget()
        root.setObjectName("Root")
        self.setCentralWidget(root)
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.active_section = "dashboard"
        self.nav_buttons = {}
        root_layout.addWidget(self._build_sidebar())

        self.stack = QStackedWidget()
        root_layout.addWidget(self.stack, stretch=1)

        self.current_view = None
        self.go_dashboard()

        QTimer.singleShot(200, self._refresh_status)

    # -------------------------------------------------------------- sidebar
    def _build_sidebar(self) -> QFrame:
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setAttribute(Qt.WA_StyledBackground, True)
        sidebar.setFixedWidth(theme.SIDEBAR_WIDTH)
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(theme.SPACE_LG, theme.SPACE_XL, theme.SPACE_LG, theme.SPACE_LG)
        layout.setSpacing(theme.SPACE_LG)

        wordmark = QHBoxLayout()
        wordmark.setSpacing(theme.SPACE_SM)
        mark = QLabel()
        mark.setFixedSize(26, 26)
        mark.setStyleSheet(f"background: {theme.BRAND}; border-radius: 13px;")
        wordmark.addWidget(mark)
        name = QLabel("BantayAralan")
        name.setObjectName("Wordmark")
        wordmark.addWidget(name)
        wordmark.addStretch()
        layout.addLayout(wordmark)

        nav_col = QVBoxLayout()
        nav_col.setSpacing(theme.SPACE_XS)
        for key, label, icon_name in NAV_ITEMS:
            btn = QPushButton(f"  {label}")
            btn.setObjectName("NavItem")
            btn.setCursor(Qt.PointingHandCursor)
            btn.setIcon(icons.icon(icon_name, theme.TEXT_TERTIARY, 18))
            btn.clicked.connect(lambda _, k=key: self._on_nav(k))
            nav_col.addWidget(btn)
            self.nav_buttons[key] = btn
        layout.addLayout(nav_col)

        layout.addStretch()

        self.status_box = QFrame()
        self.status_box.setObjectName("StatusBox")
        self.status_box.setAttribute(Qt.WA_StyledBackground, True)
        self.status_layout = QVBoxLayout(self.status_box)
        self.status_layout.setContentsMargins(theme.SPACE_MD, theme.SPACE_MD, theme.SPACE_MD, theme.SPACE_MD)
        self.status_layout.setSpacing(4)
        loading = QLabel("Loading status…")
        loading.setObjectName("StatusLine")
        self.status_layout.addWidget(loading)
        layout.addWidget(self.status_box)

        self._update_nav_styles()
        return sidebar

    def _update_nav_styles(self):
        for key, btn in self.nav_buttons.items():
            btn.setProperty("active", "true" if key == self.active_section else "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def _refresh_status(self):
        while self.status_layout.count():
            item = self.status_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        try:
            status = data.get_status()
        except Exception:
            lbl = QLabel("Status unavailable")
            lbl.setObjectName("StatusLine")
            self.status_layout.addWidget(lbl)
            return

        def line(text, ok=True):
            row = QHBoxLayout()
            row.setSpacing(6)
            dot = QLabel()
            dot.setFixedSize(6, 6)
            dot.setStyleSheet(f"background: {theme.SUCCESS if ok else theme.WARNING}; border-radius: 3px;")
            row.addWidget(dot)
            text_lbl = QLabel(text)
            text_lbl.setObjectName("StatusLine")
            row.addWidget(text_lbl)
            row.addStretch()
            wrap = QWidget()
            wrap.setLayout(row)
            return wrap

        self.status_layout.addWidget(line(f"Camera: {'Connected' if status['camera_connected'] else 'Disconnected'}", status["camera_connected"]))
        self.status_layout.addWidget(line(f"Detection: {'Running' if status['detection_running'] else 'Stopped'}", status["detection_running"]))
        self.status_layout.addWidget(line("Last event: recently" if status["last_event_at"] else "Last event: none yet"))

    # ------------------------------------------------------------- routing
    def _on_nav(self, key: str):
        if key == "dashboard":
            self.go_dashboard()
        elif key == "events":
            self.go_events()

    def _set_view(self, widget: QWidget, section: str):
        old = self.current_view
        self.stack.addWidget(widget)
        self.stack.setCurrentWidget(widget)
        if old is not None:
            self.stack.removeWidget(old)
            if hasattr(old, "cleanup"):
                old.cleanup()
            old.deleteLater()
        self.current_view = widget
        self.active_section = section
        self._update_nav_styles()

    def go_dashboard(self):
        view = DashboardView(self.go_events, self.go_event_detail)
        self._set_view(view, "dashboard")

    def go_events(self, category: str = "all"):
        view = EventsView(self.go_event_detail, initial_category=category)
        self._set_view(view, "events")

    def go_event_detail(self, event_id: int):
        view = EventDetailView(event_id, self.go_events)
        self._set_view(view, "events")
