import base64
from cryptography.fernet import Fernet

# 🔐 Gemeinsamer Schlüssel (wird bei Start generiert)
# In der finalen Version kann dieser Schlüssel in einer Datei gespeichert werden, damit Relay + Client denselben verwenden.
def generate_key():
    return Fernet.generate_key()

# Temporär: beide nutzen denselben Key beim Start
SHARED_KEY = generate_key()
fernet = Fernet(SHARED_KEY)

def encrypt_message(message: str) -> bytes:
    """Verschlüsselt eine Nachricht (Rückgabe: bytes)"""
    return fernet.encrypt(message.encode())

def decrypt_message(encrypted: bytes) -> str:
    """Entschlüsselt eine Nachricht (Eingabe: bytes)"""
    return fernet.decrypt(encrypted).decode()
