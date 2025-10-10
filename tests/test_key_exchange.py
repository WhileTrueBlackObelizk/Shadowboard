from src.crypto.key_exchange import *
from src.crypto.encryption import generate_key

# 1️⃣ Schlüsselpaar erzeugen
priv, pub = generate_rsa_keypair()

# 2️⃣ AES-Key generieren
aes_key = generate_key()

# 3️⃣ AES-Key verschlüsseln & wieder entschlüsseln
enc_key = encrypt_key_for_recipient(aes_key, pub)
dec_key = decrypt_received_key(enc_key, priv)

assert aes_key == dec_key
print("✅ RSA-Key-Austausch funktioniert!")
