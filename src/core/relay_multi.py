import os
import ssl
import socket
import logging
from threading import Thread
from src.crypto.encryption import decrypt_message

# --- Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

CERT_DIR = os.path.join(os.path.dirname(__file__), "certs")
SERVER_CERT = os.path.join(CERT_DIR, "server.crt")
SERVER_KEY = os.path.join(CERT_DIR, "server.key")

HOST, PORT = "0.0.0.0", 4430
clients = []

def check_certificates():
    if not os.path.exists(SERVER_CERT) or not os.path.exists(SERVER_KEY):
        logging.error("❌ SSL-Zertifikate fehlen!")
        raise SystemExit(1)

def broadcast(message, sender):
    for client in clients:
        if client != sender:
            try:
                client.sendall(message)
            except Exception as e:
                logging.error(f"Fehler beim Senden an Client: {e}")

def handle_client(conn, addr):
    logging.info(f"🔗 Neuer Client: {addr}")
    clients.append(conn)
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            try:
                logging.info(f"📩 Empfangene Daten von {addr}: {data[:50]}... (Bytes)")
                broadcast(data, conn)
            except Exception as e:
                logging.error(f"Fehler beim Broadcast: {e}")
    finally:
        logging.info(f"❌ Client getrennt: {addr}")
        clients.remove(conn)
        conn.close()

def main():
    check_certificates()
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=SERVER_CERT, keyfile=SERVER_KEY)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen(5)
        logging.info(f"🚀 Starte Multi-User Relay auf {HOST}:{PORT}")

        while True:
            conn, addr = sock.accept()
            secure_conn = context.wrap_socket(conn, server_side=True)
            Thread(target=handle_client, args=(secure_conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
