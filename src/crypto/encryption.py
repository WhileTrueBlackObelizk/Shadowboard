import base64
from cryptography.fernet import Fernet

# 🔐 Gemeinsamer Key für alle Clients
SHARED_KEY = b"K2IQDNnuWtd4ZG4kg1G7BP5VfCblkq7LZj8D1P0Ynto="  # <--- hier deinen Key einfügen
fernet = Fernet(SHARED_KEY)

def encrypt_message(message: str) -> bytes:
    """Verschlüsselt eine Nachricht (Rückgabe: bytes)"""
    return fernet.encrypt(message.encode())

def decrypt_message(encrypted: bytes) -> str:
    """Entschlüsselt eine Nachricht (Eingabe: bytes)"""
    return fernet.decrypt(encrypted).decode()


