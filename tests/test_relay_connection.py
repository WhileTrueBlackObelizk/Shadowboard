import unittest
import socket
import ssl

SERVER_IP = "127.0.0.1"
SERVER_PORT = 4430

class TestRelayConnection(unittest.TestCase):
    def test_connection(self):
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        with socket.create_connection((SERVER_IP, SERVER_PORT)) as sock:
            with context.wrap_socket(sock, server_hostname=SERVER_IP) as secure_sock:
                self.assertIsNotNone(secure_sock)

if __name__ == "__main__":
    unittest.main()
