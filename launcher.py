import webbrowser
import threading
import time

from ui.dashboard.app import app


def abrir_navegador():
    time.sleep(3)
    webbrowser.open("http://127.0.0.1:5050")


if __name__ == "__main__":
    print("[+] Iniciando SentinelX SOC...")
    print("[+] Subindo servidor na porta 5050...")

    threading.Thread(target=abrir_navegador, daemon=True).start()

    app.run(
        host="127.0.0.1",
        port=5050,
        debug=False,
        use_reloader=False
    )