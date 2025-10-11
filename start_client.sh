#!/bin/bash
# -----------------------------------------
# Starte Shadowboard Client
# -----------------------------------------

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR" || exit

# Virtuelle Umgebung aktivieren
source venv/bin/activate

# PYTHONPATH setzen
export PYTHONPATH=$(pwd)

# Client starten
python3 src/core/message_test_multi.py
