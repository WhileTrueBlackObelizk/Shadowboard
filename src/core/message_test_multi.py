# src/core/message_test_multi.py
import os
import ssl
import socket
import threading
import logging
import time
import json
import sys
from shutil import get_terminal_size
from src.crypto.encryption import encrypt_message, decrypt_message
from src.core.agents import pick_agent_name
from colorama import Fore, Style, init
from src.core.banner import print_banner

init(autoreset=True)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

used_names = set()
agent_name = pick_agent_name(used_names)
used_names.add(agent_name)

SERVER_IP = "127.0.0.1"
SERVER_PORT = 4430


def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")


def print_centered(text):
    cols, _ = get_terminal_size()
    for line in text.split("\n"):
        print(line.center(cols))



def intro_animation():
    clear_screen()
    print_banner()
    print_centered("🟢 Verbinden mit dem SHADOWBOARD...")
    print_centered(f"🕵️ Dein Agenten-Name: {agent_name}")
    print("\n")
    time.sleep(1)



def safe_print(sender, message, self_name):
    """Druckt eine neue Zeile, ohne input() zu zerstören"""
    cols, _ = get_terminal_size()
    text = f"{sender}: {message}".strip()

    # Cursor nach links + Zeile löschen (damit input-Zeile verschwindet)
    sys.stdout.write("\r\033[K")

    if sender == self_name:
        # rechte Seite leicht eingerückt + Farbe
        print(Fore.CYAN + text.rjust(cols) + Style.RESET_ALL)
    else:
        print(Fore.WHITE + text.ljust(cols) + Style.RESET_ALL)

    # Eingabezeile erneut anzeigen
    sys.stdout.write(f"{agent_name}: ")
    sys.stdout.flush()


def receive_messages(sock):
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                break

            payload = json.loads(decrypt_message(data))
            sender = payload["sender"]
            message = payload["message"]

            # Nicht eigene Nachricht ausgeben
            if sender != agent_name:
                safe_print(sender, message, agent_name)

        except Exception as e:
            logging.error(f"Fehler beim Empfangen: {e}")
            break


def main():
    intro_animation()
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    try:
        with socket.create_connection((SERVER_IP, SERVER_PORT)) as sock:
            with context.wrap_socket(sock, server_hostname=SERVER_IP) as secure_sock:
                logging.info(f"✅ Verbunden mit {SERVER_IP}:{SERVER_PORT}")
                threading.Thread(target=receive_messages, args=(secure_sock,), daemon=True).start()

                while True:
                    msg = input(f"{agent_name}: ").strip()
                    if not msg:
                        continue

                    payload = {"sender": agent_name, "message": msg}
                    encrypted_payload = encrypt_message(json.dumps(payload))
                    secure_sock.sendall(encrypted_payload)

                    # Eigene Nachricht anzeigen
                    safe_print(agent_name, msg, agent_name)

    except KeyboardInterrupt:
        logging.info("🛑 Client beendet.")
    except Exception as e:
        logging.error(f"❌ Fehler: {e}")


if __name__ == "__main__":
    main()
