import random
from colorama import Fore, Style

# === AGENTEN-NAMEN SAMMLUNG ===
AGENT_NAMES = [
    # James Bond Figuren
    "Bond", "Moneypenny", "Q", "Felix Leiter", "Jinx", "Elektra King", "Vesper", "Blofeld", "May Day",

    # Matrix Figuren
    "Neo", "Trinity", "Morpheus", "Smith", "Oracle", "Niobe", "Cypher", "Seraph",

    # Historische / reale Spione
    "Reilly", "Sorge", "Cicero", "Virginia Hall", "Philby", "Garbo", "Fuchs", "Zorge", "Mata Hari", "Dusko",

    # Griechische Götter
    "Zeus", "Athena", "Apollo", "Artemis", "Hermes", "Hades", "Ares", "Dionysus", "Persephone", "Nyx",

    # Römische / mythologische Figuren
    "Jupiter", "Mars", "Venus", "Mercury", "Minerva", "Neptune", "Vesta", "Diana", "Pluto", "Juno",

    # Moderne Codenamen
    "Cipher", "Specter", "Rift", "Echo", "Shadow", "Quantum", "Halo", "Flux", "Ghost", "Zero",
    "Pulse", "Vector", "Nova", "Proxy", "Byte", "Vortex", "Warden", "Sable", "Onyx", "Phantom"
]

# === FARBEN ===
COLORS = [
    Fore.GREEN, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, 
    Fore.YELLOW, Fore.RED, Fore.WHITE, Fore.LIGHTBLACK_EX
]

# === FUNKTIONEN ===
def pick_agent_name(used_names: set) -> str:
    """Wählt einen zufälligen, noch nicht vergebenen Agentennamen oder fügt Zahl hinzu."""
    available = [n for n in AGENT_NAMES if n not in used_names]
    if available:
        name = random.choice(available)
    else:
        # Wenn alle Namen belegt sind → generiere eindeutigen Namen
        name = f"Agent-{random.choice(AGENT_NAMES)}-{random.randint(100,999)}"
    used_names.add(name)
    return f"Agent {name}"

def get_agent_color(agent_name: str) -> str:
    """Bestimmt eine deterministische Farbe basierend auf dem Agentennamen."""
    return COLORS[hash(agent_name) % len(COLORS)]

def format_message(agent_name: str, message: str, timestamp: str, width: int = 70) -> str:
    """Formatiert die Nachricht farbig und mit sauberem Layout."""
    color = get_agent_color(agent_name)
    msg = f"[{timestamp}] {agent_name}: {message}"
    # Schneide oder umbreche, falls zu lang
    if len(msg) > width:
        msg = msg[:width-3] + "..."
    return f"{color}{msg}{Style.RESET_ALL}"

def reset_color():
    """Setzt Farbe zurück (falls nötig beim Log-Ende oder Fehler)."""
    print(Style.RESET_ALL, end="")

# === OPTIONALE DEKO FUNKTION ===
def print_agent_banner(agent_name: str):
    """Optionaler, ästhetischer Banner bei neuer Verbindung"""
    color = get_agent_color(agent_name)
    line = "=" * 50
    print(f"{color}\n{line}\n🔗 {agent_name} connected\n{line}{Style.RESET_ALL}")
