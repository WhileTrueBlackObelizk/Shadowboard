import unittest
from cryptography.fernet import Fernet
from src.crypto.encryption import SHARED_KEY

class TestKeyExchange(unittest.TestCase):
    def test_shared_key_encryption(self):
        """Stellt sicher, dass zwei Peers mit dem gleichen Schlüssel Nachrichten austauschen können"""
        f1 = Fernet(SHARED_KEY)
        f2 = Fernet(SHARED_KEY)

        msg_client1 = "Hallo von Client 1"
        msg_client2 = "Hallo von Client 2"

        encrypted1 = f1.encrypt(msg_client1.encode())
        encrypted2 = f2.encrypt(msg_client2.encode())

        decrypted1 = f2.decrypt(encrypted1).decode()
        decrypted2 = f1.decrypt(encrypted2).decode()

        self.assertEqual(decrypted1, msg_client1)
        self.assertEqual(decrypted2, msg_client2)

if __name__ == "__main__":
    unittest.main()
