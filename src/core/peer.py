import socket
import threading
from src.crypto.encryption import encrypt_message, decrypt_message

class SecurePeer:
    def __init__(self, host, port, key, is_server=False):
        self.host = host
        self.port = port
        self.key = key
        self.is_server = is_server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        if self.is_server:
            self.sock.bind((self.host, self.port))
            self.sock.listen(5)
            print(f"🛡️  Secure server listening on {self.host}:{self.port}")
            while True:
                conn, addr = self.sock.accept()
                print(f"🔗 Connection from {addr}")
                threading.Thread(target=self.handle_client, args=(conn,)).start()
        else:
            self.sock.connect((self.host, self.port))
            print(f"🛰️  Connected securely to {self.host}:{self.port}")
            threading.Thread(target=self.listen).start()
            self.chat_loop()

    def handle_client(self, conn):
        while True:
            try:
                data = conn.recv(4096)
                if not data:
                    break
                plaintext = decrypt_message(self.key, data)
                print(f"\n💬 {plaintext}")
            except Exception as e:
                print(f"⚠️ Connection error: {e}")
                break

    def listen(self):
        while True:
            try:
                data = self.sock.recv(4096)
                if not data:
                    break
                plaintext = decrypt_message(self.key, data)
                print(f"\n💬 {plaintext}")
            except Exception as e:
                print(f"⚠️ Listen error: {e}")
                break

    def chat_loop(self):
        try:
            while True:
                msg = input("> ")
                if msg.lower() in ("exit", "quit"):
                    break
                ciphertext = encrypt_message(self.key, msg)
                self.sock.sendall(ciphertext)
        except KeyboardInterrupt:
            print("\n🛑 Chat closed")
