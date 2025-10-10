import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# ======================================================
#  AES-GCM ENCRYPTION MODULE
# ======================================================
#  Funktionen:
#   - generate_key() -> bytes
#   - encrypt_message(key: bytes, plaintext: str) -> str
#   - decrypt_message(key: bytes, ciphertext_b64: str) -> str
# ======================================================


def generate_key() -> bytes:
    """Erzeugt einen neuen 256-Bit AES-Schlüssel."""
    return AESGCM.generate_key(bit_length=256)


def encrypt_message(key: bytes, plaintext: str) -> str:
    """
    Verschlüsselt eine Nachricht mit AES-256-GCM.
    Gibt einen Base64-kodierten String zurück (Nonce + Ciphertext).
    """
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  # 96-Bit Nonce
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)
    combined = nonce + ciphertext
    return base64.b64encode(combined).decode()


def decrypt_message(key: bytes, ciphertext_b64: str) -> str:
    """
    Entschlüsselt eine AES-256-GCM verschlüsselte Nachricht (Base64 Input).
    Gibt den Klartext zurück.
    """
    aesgcm = AESGCM(key)
    combined = base64.b64decode(ciphertext_b64.encode())
    nonce, ciphertext = combined[:12], combined[12:]
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext.decode()