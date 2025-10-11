#!/bin/bash
# -----------------------------------------
# SHADOWBOARD Setup für macOS
# Erstellt virtuelle Umgebung und installiert alle Dependencies
# -----------------------------------------

# Repository Root ermitteln
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR" || exit

# Virtuelle Umgebung erstellen
if [ ! -d "venv" ]; then
    echo "⚡ Erstelle virtuelle Umgebung..."
    python3 -m venv venv
else
    echo "✅ Virtuelle Umgebung existiert bereits."
fi

# Virtuelle Umgebung aktivieren
source venv/bin/activate

# pip aktualisieren
pip install --upgrade pip

# Requirements installieren
if [ -f requirements.txt ]; then
    echo "⚡ Installiere Dependencies..."
    pip install -r requirements.txt
else
    echo "⚠️ requirements.txt nicht gefunden! Bitte prüfen."
fi

# Start-Skripte ausführbar machen
chmod +x start_relay.sh
chmod +x start_client.sh

echo "🎉 Setup abgeschlossen!"
echo "Relay starten: ./start_relay.sh"
echo "Client starten: ./start_client.sh"
