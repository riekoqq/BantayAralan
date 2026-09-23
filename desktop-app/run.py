"""BantayAralan admin UI -- native desktop application (PySide6).

No browser, no HTTP server, no webview: this is a real native GUI app that
reads/writes a local SQLite file directly in-process.

    pip install -r requirements.txt
    python run.py
"""
import sys

from PySide6.QtWidgets import QApplication

from app import data, theme
from app.main_window import MainWindow


def main():
    data.seed()  # no-op if already seeded

    app = QApplication(sys.argv)
    app.setStyleSheet(theme.STYLESHEET)
    app.setApplicationName("BantayAralan")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
