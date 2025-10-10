import unittest
from src.crypto.encryption import encrypt_message, decrypt_message

class TestEncryption(unittest.TestCase):
    def test_encrypt_decrypt(self):
        msg = "Hallo Welt"
        encrypted = encrypt_message(msg)
        decrypted = decrypt_message(encrypted)
        self.assertEqual(msg, decrypted)

if __name__ == "__main__":
    unittest.main()
