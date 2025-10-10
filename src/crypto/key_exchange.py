from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend

# === RSA Key Management ===

def generate_rsa_keypair():
    """Erzeugt ein RSA-Schlüsselpaar (2048 Bit)"""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key


def export_private_key(private_key, path):
    """Private Key sicher als PEM speichern"""
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(path, "wb") as f:
        f.write(pem)


def export_public_key(public_key, path):
    """Public Key als PEM speichern"""
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(path, "wb") as f:
        f.write(pem)


def load_private_key(path):
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(
            f.read(), password=None, backend=default_backend()
        )


def load_public_key(path):
    with open(path, "rb") as f:
        return serialization.load_pem_public_key(f.read(), backend=default_backend())


# === AES Key Exchange ===

def encrypt_key_for_recipient(aes_key: bytes, recipient_public_key):
    """AES-Key mit dem Public Key des Empfängers verschlüsseln"""
    encrypted = recipient_public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted


def decrypt_received_key(encrypted_key: bytes, private_key):
    """Empfangenen AES-Key mit eigenem Private Key entschlüsseln"""
    decrypted = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted
