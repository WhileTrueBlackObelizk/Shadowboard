from src.crypto.encryption import generate_key
from src.core.peer import SecurePeer
import threading, time

key = generate_key()

# Starte Server in Thread
server = SecurePeer("127.0.0.1", 5555, key, is_server=True)
threading.Thread(target=server.start, daemon=True).start()

# Warte kurz, dann Client verbinden
time.sleep(1)
client = SecurePeer("127.0.0.1", 5555, key)
threading.Thread(target=client.start, daemon=True).start()
