import socket
import ssl
import logging
from src.crypto.encryption import encrypt_message, decrypt_message, SHARED_KEY

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

SERVER_IP = "127.0.0.1"
SERVER_PORT = 4430

def main():
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE  # Für Tests: self-signed Zertifikat

    try:
        with socket.create_connection((SERVER_IP, SERVER_PORT)) as sock:
            with context.wrap_socket(sock, server_hostname=SERVER_IP) as secure_sock:
                logging.info(f"✅ Verbunden mit {SERVER_IP}:{SERVER_PORT}")

                while True:
                    msg = input("🧠 Deine Nachricht: ")
                    if not msg.strip():
                        continue

                    # Nachricht verschlüsseln
                    encrypted = encrypt_message(msg)

                    # Bytes direkt senden
                    secure_sock.sendall(encrypted)

                    # Antwort vom Server
                    try:
                        data = secure_sock.recv(4096)
                        if data:
                            # Daten vom Server sind unverschlüsselt (Relay sendet ACK)
                            logging.info(f"🧠 Antwort vom Server: {data.decode('utf-8', errors='ignore')}")
                    except Exception as e:
                        logging.error(f"Fehler beim Empfangen: {e}")

    except ConnectionRefusedError:
        logging.error(f"❌ Verbindung zu {SERVER_IP}:{SERVER_PORT} verweigert. Relay läuft?")
    except KeyboardInterrupt:
        logging.info("🛑 Client beendet.")

if __name__ == "__main__":
    main()
