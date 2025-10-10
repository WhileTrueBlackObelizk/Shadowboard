import os
import ssl
import socket
import logging
from datetime import datetime

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

# --- Zertifikatspfade ---
CERT_DIR = os.path.join(os.path.dirname(__file__), "certs")
SERVER_CERT = os.path.join(CERT_DIR, "server.crt")
SERVER_KEY = os.path.join(CERT_DIR, "server.key")

def check_certificates():
    """Prüft, ob die benötigten Zertifikatsdateien existieren."""
    if not os.path.exists(SERVER_CERT) or not os.path.exists(SERVER_KEY):
        logging.error("❌ SSL-Zertifikate fehlen!")
        logging.info("Bitte führe folgenden Befehl im Projektordner aus:")
        logging.info("")
        logging.info("  openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.crt -days 365 -nodes")
        logging.info("  mkdir -p src/core/certs && mv server.crt src/core/certs/ && mv server.key src/core/certs/")
        logging.info("")
        raise SystemExit(1)

def create_ssl_context():
    """Erstellt und konfiguriert SSL-Kontext."""
    check_certificates()
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=SERVER_CERT, keyfile=SERVER_KEY)
    return context

def main():
    """Startet den Relay-Server."""
    context = create_ssl_context()
    host, port = "0.0.0.0", 4430

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.bind((host, port))
        sock.listen(5)
        logging.info(f"🚀 Starte Relay auf {host}:{port}")

        with context.wrap_socket(sock, server_side=True) as ssock:
            while True:
                conn, addr = ssock.accept()
                logging.info(f"🔗 Verbindung von {addr}")
                try:
                    data = conn.recv(1024)
                    if not data:
                        continue
                    logging.info(f"📩 Empfangene Daten: {data.decode(errors='ignore')}")
                    conn.sendall(b"ACK\n")
                except Exception as e:
                    logging.error(f"Fehler bei Verbindung {addr}: {e}")
                finally:
                    conn.close()

if __name__ == "__main__":
    main()
