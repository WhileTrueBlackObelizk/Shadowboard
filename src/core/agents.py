import random
from colorama import Fore, Style

# --- Agenten-Namen ---
AGENT_NAMES = [
    # James Bond Figuren
    "Bond", "Moneypenny", "Q", "Felix Leiter", "Jinx", "Elektra King",

    # Matrix Figuren
    "Neo", "Trinity", "Morpheus", "Smith", "Oracle", "Niobe",

    # Berühmte Agenten der Geschichte
    "Hendriksen", "Cicero", "Tully", "Reilly", "Sorge", "Virginia Hall",

    # Griechische Götter
    "Zeus", "Athena", "Apollo", "Artemis", "Hermes", "Hades", "Ares", "Dionysus",

    # Römische Idole / Götter
    "Jupiter", "Mars", "Venus", "Mercury", "Minerva", "Neptune", "Vesta", "Diana"
]

COLORS = [Fore.GREEN, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.YELLOW, Fore.RED]

# --- Funktionen ---
def pick_agent_name(used_names: set) -> str:
    """Wählt einen zufälligen, noch nicht vergebenen Agentennamen"""
    available = [name for name in AGENT_NAMES if name not in used_names]
    if not available:
        return f"Agent {random.choice(AGENT_NAMES)}"
    return f"Agent {random.choice(available)}"

def get_agent_color(agent_name: str) -> str:
    """Deterministische Farbe basierend auf Agentennamen"""
    return COLORS[hash(agent_name) % len(COLORS)]

def format_message(agent_name: str, message: str, timestamp: str) -> str:
    """Formatiert die Nachricht farbig für die Konsole"""
    color = get_agent_color(agent_name)
    return f"{color}[{timestamp}] {agent_name}: {message}{Style.RESET_ALL}"
