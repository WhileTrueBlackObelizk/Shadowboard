# src/crypto/encryption.py
import os
import base64
from cryptography.fernet import Fernet

# --- SHARED KEY ---
# Produktion: setze per ENV (empfohlen), z.B. export SHADOWBOARD_SHARED_KEY=...
env_key = os.environ.get("SHADOWBOARD_SHARED_KEY", None)

if env_key:
    # falls als base64-string übergeben
    SHARED_KEY = env_key.encode() if isinstance(env_key, str) else env_key
else:
    # Development default: feste key (nur für Lab / Demo). Ändere das nicht im produktiven Einsatz.
    SHARED_KEY = b"K2IQDNnuWtd4ZG4kg1G7BP5VfCblkq7LZj8D1P0Ynto="

fernet = Fernet(SHARED_KEY)

def generate_key() -> bytes:
    """Generiert einen neuen Fernet-Key (Base64-bytes)"""
    return Fernet.generate_key()

def encrypt_message(message: str) -> bytes:
    """Verschlüsselt eine Nachricht (Rückgabe: bytes)."""
    if isinstance(message, str):
        message = message.encode()
    return fernet.encrypt(message)

def decrypt_message(encrypted: bytes) -> str:
    """Entschlüsselt eine Nachricht (Eingabe: bytes) -> str"""
    if isinstance(encrypted, str):
        # falls fälschlicherweise ein string ankommt, versuche bytes
        encrypted = encrypted.encode()
    return fernet.decrypt(encrypted).decode()
