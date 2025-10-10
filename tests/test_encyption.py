from src.crypto.encyption import generate_key, encrypt_message, decrypt_message

def test_encryption_cycle():
    key = generate_key()
    msg = "Hallo sichere Welt!"
    encrypted = encrypt_message(key, msg)
    decrypted = decrypt_message(key, encrypted)
    assert decrypted == msg
    print("✅ AES-GCM funktioniert:", decrypted)

if __name__ == "__main__":
    test_encryption_cycle()
