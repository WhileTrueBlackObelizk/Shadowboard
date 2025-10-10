import os
import ssl
import socket
import logging

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

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))
        sock.listen(5)
        logging.info(f"🚀 Starte Relay auf {host}:{port}")

        while True:
            client_conn, addr = sock.accept()
            logging.info(f"🔗 Verbindung von {addr}")
            try:
                # SSL auf die einzelne Verbindung anwenden
                with context.wrap_socket(client_conn, server_side=True) as ssock:
                    data = ssock.recv(4096)
                    if data:
                        decoded = data.decode("utf-8", errors="ignore")
                        logging.info(f"📩 Empfangene Daten: {decoded}")
                        # Antwort an Client senden (Unicode-fähig)
                        response = "✅ Nachricht empfangen!"
                        ssock.sendall(response.encode("utf-8"))
            except Exception as e:
                logging.error(f"Fehler bei Verbindung {addr}: {e}")
            finally:
                client_conn.close()

if __name__ == "__main__":
    main()
