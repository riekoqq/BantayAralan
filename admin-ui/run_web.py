"""Run BantayAralan admin UI as a plain web app (browser-based deployment form).

    python run_web.py

Opens http://127.0.0.1:5057 and starts the Flask dev server.
"""
import threading
import webbrowser

from backend.app import create_app

HOST = "127.0.0.1"
PORT = 5057


def main():
    app = create_app()
    url = f"http://{HOST}:{PORT}/"
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    print(f"BantayAralan admin UI running at {url}")
    app.run(host=HOST, port=PORT, debug=False)


if __name__ == "__main__":
    main()
