#!/usr/bin/env python3
import socket
import ssl
import threading
from src.crypto.encryption import encrypt_message, decrypt_message, generate_key

HOST = "localhost"   # Relay Host
PORT = 4430          # Relay Port

# Für Testzwecke: gemeinsamer AES-Key
AES_KEY = generate_key()

def listen(sock):
    """Thread: empfangene Nachrichten vom Relay lesen"""
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                break
            plaintext = decrypt_message(AES_KEY, data.rstrip(b'\n'))
            print(f"\n💬 Nachricht empfangen: {plaintext}")
        except Exception as e:
            print(f"⚠️ Fehler beim Empfang: {e}")
            break

def main():
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE  # für Test lokal; später CA prüfen

    with socket.create_connection((HOST, PORT)) as sock:
        with context.wrap_socket(sock, server_hostname=HOST) as ssock:
            print(f"✅ Mit Relay verbunden: {HOST}:{PORT}")

            # Thread zum Empfangen starten
            threading.Thread(target=listen, args=(ssock,), daemon=True).start()

            # Eingabe/Chat-Loop
            try:
                while True:
                    msg = input("> ")
                    if msg.lower() in ("exit", "quit"):
                        break
                    ciphertext = encrypt_message(AES_KEY, msg)
                    ssock.sendall(ciphertext + b'\n')
            except KeyboardInterrupt:
                print("\n🛑 Client beendet")

if __name__ == "__main__":
    main()
