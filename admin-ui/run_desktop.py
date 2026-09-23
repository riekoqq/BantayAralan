"""Run BantayAralan admin UI as a desktop window (desktop deployment form).

Requires the optional 'pywebview' dependency:

    pip install pywebview
    python run_desktop.py

This wraps the exact same Flask app + frontend used by run_web.py in a
native OS window instead of a browser tab -- same information architecture,
same API, same mock data. Packaging this into a standalone .exe is
documented in README.md under "Packaging".
"""
import threading

from backend.app import create_app

HOST = "127.0.0.1"
PORT = 5058


def main():
    try:
        import webview
    except ImportError:
        raise SystemExit(
            "pywebview is not installed. Run: pip install pywebview\n"
            "(This desktop-window launcher is optional -- run_web.py works without it.)"
        )

    app = create_app()

    def run_flask():
        app.run(host=HOST, port=PORT, debug=False, use_reloader=False)

    thread = threading.Thread(target=run_flask, daemon=True)
    thread.start()

    webview.create_window(
        "BantayAralan -- Admin",
        f"http://{HOST}:{PORT}/",
        width=1440,
        height=900,
        min_size=(1024, 700),
    )
    webview.start()


if __name__ == "__main__":
    main()
