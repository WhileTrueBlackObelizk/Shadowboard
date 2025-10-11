import os
import socket
import ssl
import threading
import logging
import time
from shutil import get_terminal_size
from src.crypto.encryption import encrypt_message, decrypt_message
from src.core.agents import pick_agent_name

# ---------------------------
# Terminal & Farben
# ---------------------------
from colorama import Fore, Style, init
init(autoreset=True)

# ---------------------------
# Logging
# ---------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

# ---------------------------
# Agenten-Name
# ---------------------------
used_names = set()
agent_name = pick_agent_name(used_names)
used_names.add(agent_name)

# ---------------------------
# Server-Konfig
# ---------------------------
HOST, PORT = "0.0.0.0", 4430

# ---------------------------
# Zertifikate
# ---------------------------
CERT_DIR = os.path.join(os.path.dirname(__file__), "certs")
SERVER_CERT = os.path.join(CERT_DIR, "server.crt")
SERVER_KEY = os.path.join(CERT_DIR, "server.key")

def check_certificates():
    if not os.path.exists(SERVER_CERT) or not os.path.exists(SERVER_KEY):
        logging.error("❌ SSL-Zertifikate fehlen!")
        logging.info("Bitte erstelle die Zertifikate:")
        logging.info("  openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.crt -days 365 -nodes")
        raise SystemExit(1)

# ---------------------------
# Terminalfunktionen
# ---------------------------
def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")

def print_centered(text):
    cols, _ = get_terminal_size()
    for line in text.split("\n"):
        print(line.center(cols))

def position_terminal(x, y, width, height):
    def position_terminal(x=0, y=0, width=120, height=40):
        """
        Versucht, die Terminalgröße auf Breite x Höhe zu setzen.
        Mac-Terminal unterstützt dies nur teilweise.
        """
    try:
        # Setzt Zeilen und Spalten
        os.system(f"printf '\e[8;{height};{width}t'")
        # Optional: könnte hier noch x/y verschieben, funktioniert aber nur in iTerm2 via Applescript
    except Exception as e:
        logging.warning(f"Terminalgröße konnte nicht gesetzt werden: {e}")


# ---------------------------
# Intro & Banner
# ---------------------------
def intro_animation():
    shadow_banner = r"""
    
  █████████  █████   █████  █████████  ██████████      ███████   █████   ███   █████
 ███░░░░░███░░███   ░░███  ███░░░░░███░░███░░░░███   ███░░░░░███░░███   ░███  ░░███ 
░███    ░░░  ░███    ░███ ░███    ░███ ░███   ░░███ ███     ░░███░███   ░███   ░███ 
░░█████████  ░███████████ ░███████████ ░███    ░███░███      ░███░███   ░███   ░███ 
 ░░░░░░░░███ ░███░░░░░███ ░███░░░░░███ ░███    ░███░███      ░███░░███  █████  ███  
 ███    ░███ ░███    ░███ ░███    ░███ ░███    ███ ░░███     ███  ░░░█████░█████░   
░░█████████  █████   ██████████   ███████████████   ░░░███████░     ░░███ ░░███     
 ░░░░░░░░░  ░░░░░   ░░░░░░░░░░   ░░░░░░░░░░░░░░░      ░░░░░░░        ░░░   ░░░      
 ███████████     ███████     █████████  ███████████  ██████████                     
░░███░░░░░███  ███░░░░░███  ███░░░░░███░░███░░░░░███░░███░░░░███                    
 ░███    ░███ ███     ░░███░███    ░███ ░███    ░███ ░███   ░░███                   
 ░██████████ ░███      ░███░███████████ ░██████████  ░███    ░███                   
 ░███░░░░░███░███      ░███░███░░░░░███ ░███░░░░░███ ░███    ░███                   
 ░███    ░███░░███     ███ ░███    ░███ ░███    ░███ ░███    ███                    
 ███████████  ░░░███████░  █████   ██████████   ███████████████                     
░░░░░░░░░░░     ░░░░░░░   ░░░░░   ░░░░░░░░░░   ░░░░░░░░░░░░░░░                      
                                                                                    
                                                                                    
                                                                                                                                                                                                                                               
"""
    clear_screen()
    print_centered(shadow_banner)
    print("\n")
    print_centered("🌙 Willkommen im SHADOWBOARD Big Daddy")
    print_centered(f"🕵️ Dein Agenten-Name: {agent_name}")
    print_centered("⚡ Alle Nachrichten sind verschlüsselt, du bist der HOST.")
    print_centered("Erstelle dir nun mit einem weiteren Terminal ein Client zum kommunizieren.")
    time.sleep(1)
    print("\n")

# ---------------------------
# Pseudo-Fenster
# ---------------------------
def chat_bubble(msg, sender=""):
    cols, _ = get_terminal_size()
    width = min(max(len(line) for line in msg.split("\n")) + 4, cols - 10)
    top = "┌" + "─" * (width - 2) + "┐"
    bottom = "└" + "─" * (width - 2) + "┘"
    middle = "\n".join([f"│ {line.ljust(width - 4)} │" for line in msg.split("\n")])
    if sender:
        sender_line = f"🧑 {sender}".ljust(width)
        return f"{sender_line}\n{top}\n{middle}\n{bottom}"
    return f"{top}\n{middle}\n{bottom}"

# ---------------------------
# Client-Verbindungen
# ---------------------------
def handle_client(conn, addr):
    logging.info(f"🔗 Verbindung von {addr}")
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            logging.info(f"📩 Empfangene Daten: {data.decode(errors='ignore')}")
            conn.sendall(b"ACK\n")
    except Exception as e:
        logging.error(f"Fehler bei Verbindung {addr}: {e}")
    finally:
        conn.close()

# ---------------------------
# Main
# ---------------------------
def main():
    position_terminal(0, 0, width=120, height=40)
    intro_animation()
    check_certificates()

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=SERVER_CERT, keyfile=SERVER_KEY)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen(5)
        logging.info(f"🚀 Starte Relay auf {HOST}:{PORT}")

        while True:
            conn, addr = sock.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
