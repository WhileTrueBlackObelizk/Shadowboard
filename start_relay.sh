#!/bin/bash
# -----------------------------------------
# Starte Relay-Server
# -----------------------------------------

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR" || exit

# Virtuelle Umgebung aktivieren
source venv/bin/activate

# PYTHONPATH setzen
export PYTHONPATH=$(pwd)

# Relay starten
python3 src/core/relay_multi.py
