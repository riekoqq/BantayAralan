"""Simulated video-evidence player.

Real, interactive controls (play/pause, scrub, time, volume button,
fullscreen -- which genuinely toggles the app window's fullscreen state).
There is no actual video file or codec behind it: playback is a QTimer
driving a fake progress bar over a fixed duration. See
../README.md -> "Video evidence -- backend requirements" for what a real
implementation would need.
"""
from PySide6.QtCore import Qt, QTimer, QRectF
from PySide6.QtGui import QPainter, QPixmap, QColor
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton, QSlider, QSizePolicy,
)

from . import icons, theme
from .snapshot import make_snapshot_pixmap

DURATION_MS = 8000  # simulated clip length
TICK_MS = 200


def _dimmed_pixmap(source: QPixmap, size, opacity: float = 0.5) -> QPixmap:
    scaled = source.scaled(size[0], size[1], Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
    out = QPixmap(size[0], size[1])
    out.fill(QColor(theme.GRAY_900))
    painter = QPainter(out)
    painter.setOpacity(opacity)
    x = (size[0] - scaled.width()) // 2
    y = (size[1] - scaled.height()) // 2
    painter.drawPixmap(x, y, scaled)
    painter.end()
    return out


class VideoPlayer(QWidget):
    STAGE_SIZE = (600, 338)

    def __init__(self, event: dict, parent=None):
        super().__init__(parent)
        self.event = event
        self.elapsed_ms = 0
        self.playing = False

        self.timer = QTimer(self)
        self.timer.setInterval(TICK_MS)
        self.timer.timeout.connect(self._tick)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ---- stage ----
        self.stage = QFrame()
        self.stage.setObjectName("VideoStage")
        self.stage.setAttribute(Qt.WA_StyledBackground, True)
        self.stage.setFixedHeight(self.STAGE_SIZE[1])
        stage_layout = QVBoxLayout(self.stage)
        stage_layout.setContentsMargins(0, 0, 0, 0)

        self.bg_label = QLabel(self.stage)
        self.bg_label.setAlignment(Qt.AlignCenter)
        pm = make_snapshot_pixmap(event["category"], *self.STAGE_SIZE)
        self.bg_label.setPixmap(_dimmed_pixmap(pm, self.STAGE_SIZE, 0.55))
        self.bg_label.setGeometry(0, 0, *self.STAGE_SIZE)

        self.timestamp_badge = QLabel(f"Recorded around {event['time_label']}", self.stage)
        self.timestamp_badge.setObjectName("TimestampBadge")
        self.timestamp_badge.setAttribute(Qt.WA_StyledBackground, True)
        self.timestamp_badge.adjustSize()
        self.timestamp_badge.move(14, 14)

        self.play_btn = QPushButton(self.stage)
        self.play_btn.setObjectName("PlayCircle")
        self.play_btn.setFixedSize(56, 56)
        self.play_btn.setCursor(Qt.PointingHandCursor)
        self.play_btn.setIcon(icons.icon("play", theme.GRAY_900, 22))
        self.play_btn.setIconSize(self.play_btn.size() * 0.4)
        self.play_btn.move((self.STAGE_SIZE[0] - 56) // 2, (self.STAGE_SIZE[1] - 56) // 2)
        self.play_btn.clicked.connect(self.play)

        layout.addWidget(self.stage)

        # ---- controls ----
        controls = QFrame()
        controls.setObjectName("VideoControls")
        controls.setAttribute(Qt.WA_StyledBackground, True)
        controls_layout = QVBoxLayout(controls)
        controls_layout.setContentsMargins(theme.SPACE_MD, theme.SPACE_SM, theme.SPACE_MD, theme.SPACE_SM)
        controls_layout.setSpacing(6)

        self.track = QSlider(Qt.Horizontal)
        self.track.setObjectName("VideoTrack")
        self.track.setRange(0, DURATION_MS)
        self.track.setValue(0)
        self.track.sliderMoved.connect(self._seek)
        controls_layout.addWidget(self.track)

        row = QHBoxLayout()
        left = QHBoxLayout()
        left.setSpacing(theme.SPACE_MD)
        self.toggle_btn = QPushButton()
        self.toggle_btn.setObjectName("IconButton")
        self.toggle_btn.setCursor(Qt.PointingHandCursor)
        self.toggle_btn.setIcon(icons.icon("play", "#FFFFFF", 16))
        self.toggle_btn.clicked.connect(self.toggle)
        left.addWidget(self.toggle_btn)
        self.time_label = QLabel("00:00 / 00:08")
        self.time_label.setObjectName("VideoTime")
        left.addWidget(self.time_label)
        row.addLayout(left)
        row.addStretch()

        right = QHBoxLayout()
        right.setSpacing(theme.SPACE_MD)
        vol_btn = QPushButton()
        vol_btn.setObjectName("IconButton")
        vol_btn.setIcon(icons.icon("volume", "#FFFFFF", 16))
        vol_btn.setCursor(Qt.PointingHandCursor)
        right.addWidget(vol_btn)
        self.fs_btn = QPushButton()
        self.fs_btn.setObjectName("IconButton")
        self.fs_btn.setIcon(icons.icon("fullscreen", "#FFFFFF", 16))
        self.fs_btn.setCursor(Qt.PointingHandCursor)
        self.fs_btn.clicked.connect(self._toggle_fullscreen)
        right.addWidget(self.fs_btn)
        row.addLayout(right)
        controls_layout.addLayout(row)

        layout.addWidget(controls)

        disclaimer = QLabel(
            "Demo playback is simulated for this design preview — real event video "
            "capture, storage, and retrieval is a planned capability. See README.md."
        )
        disclaimer.setObjectName("VideoDisclaimer")
        disclaimer.setWordWrap(True)
        disclaimer.setContentsMargins(theme.SPACE_MD, theme.SPACE_SM, theme.SPACE_MD, 0)
        layout.addWidget(disclaimer)

    # ------------------------------------------------------------ playback
    def play(self):
        self.playing = True
        self.play_btn.hide()
        self.toggle_btn.setIcon(icons.icon("pause", "#FFFFFF", 16))
        self.timer.start()

    def pause(self):
        self.playing = False
        self.toggle_btn.setIcon(icons.icon("play", "#FFFFFF", 16))
        self.timer.stop()

    def toggle(self):
        if self.elapsed_ms == 0 and not self.playing:
            self.play_btn.hide()
        self.pause() if self.playing else self.play()

    def _tick(self):
        self.elapsed_ms = min(DURATION_MS, self.elapsed_ms + TICK_MS)
        self.track.setValue(self.elapsed_ms)
        self._update_time_label()
        if self.elapsed_ms >= DURATION_MS:
            self.pause()
            self.play_btn.show()
            self.elapsed_ms = 0
            self.track.setValue(0)
            self._update_time_label()

    def _seek(self, value):
        self.elapsed_ms = value
        self._update_time_label()
        self.play_btn.hide()

    def _update_time_label(self):
        def fmt(ms):
            s = ms // 1000
            return f"{s // 60:02d}:{s % 60:02d}"
        self.time_label.setText(f"{fmt(self.elapsed_ms)} / {fmt(DURATION_MS)}")

    def _toggle_fullscreen(self):
        window = self.window()
        if window.isFullScreen():
            window.showNormal()
            self.fs_btn.setIcon(icons.icon("fullscreen", "#FFFFFF", 16))
        else:
            window.showFullScreen()
            self.fs_btn.setIcon(icons.icon("fullscreen_exit", "#FFFFFF", 16))

    def stop_timer(self):
        self.timer.stop()
