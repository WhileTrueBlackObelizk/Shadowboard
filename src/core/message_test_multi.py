import os
import sys
import socket
import ssl
import threading
import logging
import time
import subprocess
from shutil import get_terminal_size
from src.crypto.encryption import encrypt_message, decrypt_message
from src.core.agents import pick_agent_name

# ---------------------------
# Terminal & Farben
# ---------------------------
from colorama import Fore, Style, init
init(autoreset=True)

# ---------------------------
# Logging
# ---------------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler()])

# ---------------------------
# Agenten-Name
# ---------------------------
used_names = set()
agent_name = pick_agent_name(used_names)
used_names.add(agent_name)

# ---------------------------
# Server-Konfig
# ---------------------------
SERVER_IP = "127.0.0.1"
SERVER_PORT = 4430

# ---------------------------
# Terminalgröße setzen (1/4 Mac Bildschirm)
# ---------------------------
def set_terminal_large_screen():
    try:
        output = subprocess.check_output(
            ["osascript", "-e", 'tell application "Finder" to get bounds of window of desktop'],
            text=True
        )
        x1, y1, x2, y2 = map(int, output.strip().split(", "))
        screen_width = x2 - x1
        screen_height = y2 - y1

        # 2/3 Bildschirmgröße in Zeilen/Spalten
        rows = max(15, int(screen_height / 16 * 0.66))
        cols = max(40, int(screen_width / 8 * 0.66))

        os.system(f"printf '\\e[8;{rows};{cols}t'")
    except Exception as e:
        logging.warning(f"⚠️ Terminalgröße konnte nicht gesetzt werden: {e}")


set_terminal_large_screen()

# ---------------------------
# Screen & Banner
# ---------------------------
def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")

def print_centered(text):
    cols, _ = get_terminal_size()
    for line in text.split("\n"):
        print(line.center(cols))

def intro_animation():
    banner = r"""
███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗██████╗  ██████╗  █████╗ ██████╗ ██████╗ 
██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║██╔══██╗██╔═══██╗██╔══██╗██╔══██╗██╔══██╗
███████╗███████║███████║██║  ██║██║   ██║██║ █╗ ██║██████╔╝██║   ██║███████║██████╔╝██║  ██║
╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║██╔══██╗██║   ██║██╔══██║██╔══██╗██║  ██║
███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚═════╝  ╚═════╝  ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝
"""
    clear_screen()
    print_centered(banner)
    print("\n")
    for line in [
        "🟢 Willkommen zum SHADOWBOARD Multi-User Chat",
        f"🕵️ Dein Agenten-Name: {agent_name}",
        "⚡ Need-to-Know:",
        "- Alle Nachrichten sind verschlüsselt",
        "- Einfach tippen und Enter drücken",
        "- Viel Spaß!"
    ]:
        print_centered(line)
        time.sleep(0.5)
    print("\n")
    time.sleep(0.5)

# ---------------------------
# Pseudo-Fenster / Chat Bubble
# ---------------------------
def chat_bubble(msg, sender=""):
    cols, _ = get_terminal_size()
    width = min(max(len(line) for line in msg.split("\n")) + 4, cols - 10)
    top = "┌" + "─" * (width - 2) + "┐"
    bottom = "└" + "─" * (width - 2) + "┘"
    middle = "\n".join([f"│ {line.ljust(width - 4)} │" for line in msg.split("\n")])
    if sender:
        sender_line = f"🧑 {sender}".ljust(width)
        return f"{sender_line}\n{top}\n{middle}\n{bottom}"
    return f"{top}\n{middle}\n{bottom}"

# ---------------------------
# Nachrichten empfangen
# ---------------------------
def receive_messages(sock):
    while True:
        try:
            data = sock.recv(4096)
            if data:
                try:
                    msg = decrypt_message(data)
                    print(chat_bubble(msg, "Client"))
                except Exception:
                    logging.warning("❌ Fehler beim Entschlüsseln der Nachricht")
        except Exception as e:
            logging.error(f"Fehler beim Empfangen: {e}")
            break

# ---------------------------
# Main
# ---------------------------
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
                    msg = input(f"{agent_name}: ")
                    if not msg.strip():
                        continue
                    encrypted = encrypt_message(msg)
                    secure_sock.sendall(encrypted)
                    print(chat_bubble(msg, agent_name))

    except KeyboardInterrupt:
        logging.info("🛑 Client beendet.")
    except Exception as e:
        logging.error(f"❌ Fehler: {e}")

if __name__ == "__main__":
    main()
