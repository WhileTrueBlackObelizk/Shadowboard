# src/core/relay_multi.py
import os
import socket
import ssl
import threading
import logging
import time
import json
from shutil import get_terminal_size
from src.crypto.encryption import decrypt_message 
from src.crypto.encryption import encrypt_message
from src.core.agents import pick_agent_name
from src.core.banner import print_banner

# Terminal-Farben
from colorama import init
init(autoreset=True)

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Agent Name (Host)
used_names = set()
agent_name = pick_agent_name(used_names)
used_names.add(agent_name)

# Server config
HOST, PORT = "0.0.0.0", 4430

# SSL certs
CERT_DIR = os.path.join(os.path.dirname(__file__), "certs")
SERVER_CERT = os.path.join(CERT_DIR, "server.crt")
SERVER_KEY = os.path.join(CERT_DIR, "server.key")

def check_certificates():
    if not os.path.exists(SERVER_CERT) or not os.path.exists(SERVER_KEY):
        logging.error("❌ SSL-Zertifikate fehlen!")
        logging.info("Bitte erstelle die Zertifikate (Projekt-Root):")
        logging.info("  openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.crt -days 365 -nodes")
        logging.info("  mkdir -p src/core/certs && mv server.crt src/core/certs/ && mv server.key src/core/certs/")
        raise SystemExit(1)

# simple banner
def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")

def print_centered(text):
    cols, _ = get_terminal_size()
    for line in text.split("\n"):
        print(line.center(cols))


def intro_animation():
    clear_screen()
    print_banner()
    print("\n")
    print_centered("🌙 Willkommen im SHADOWBOARD")
    print_centered(f"🕵️ Host-Agent: {agent_name}")
    print_centered("⚡ Relay läuft und leitet verschlüsselte Nachrichten weiter")
    print("\n")
    time.sleep(1)

    print("\n")

# store connections for potential admin-broadcast later
connected_clients = set()
conn_lock = threading.Lock()

def safe_add_conn(conn):
    with conn_lock:
        connected_clients.add(conn)

def safe_remove_conn(conn):
    with conn_lock:
        if conn in connected_clients:
            connected_clients.remove(conn)

def handle_client(conn, addr):
    logging.info(f"🔗 Verbindung von {addr}")
    safe_add_conn(conn)
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break

            # Log a short preview
            try:
                import base64
                preview = base64.b64encode(data)[:60].decode()
            except Exception:
                preview = str(data)[:60]
            logging.info(f"📩 Verschlüsselte Daten empfangen ({len(data)} Bytes) preview={preview}")

            # Entschlüsseln optional nur für Relay Logging
            try:
                plaintext = decrypt_message(data)
                logging.info(f"💬 Entschlüsselt von {addr}: {plaintext}")
            except Exception:
                logging.debug("⚠️ Entschlüsselung fehlgeschlagen (Relay liest nur mit)")

            # --- Broadcast an alle anderen Clients ---
            with conn_lock:
                for c in connected_clients:
                    if c != conn:  # nicht zurück an Sender
                        try:
                            c.sendall(data)
                        except:
                            connected_clients.remove(c)

            # ACK entfernen → nicht mehr zurück an Sender

    except Exception as e:
        logging.error(f"Fehler bei Verbindung {addr}: {e}")
    finally:
        safe_remove_conn(conn)
        conn.close()
        logging.info(f"🔌 Verbindung {addr} geschlossen")


def main():
    # Banner + checks
    intro_animation()
    check_certificates()

    # create ssl context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=SERVER_CERT, keyfile=SERVER_KEY)

    # socket serve
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen(5)
        logging.info(f"🚀 Starte Relay auf {HOST}:{PORT}")

        while True:
            conn, addr = sock.accept()
            # wrap socket with ssl server side
            try:
                secure_conn = context.wrap_socket(conn, server_side=True)
            except Exception as e:
                logging.error(f"SSL-Wrap fehlgeschlagen: {e}")
                conn.close()
                continue
            threading.Thread(target=handle_client, args=(secure_conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
