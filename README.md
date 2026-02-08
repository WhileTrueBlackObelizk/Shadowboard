# SHADOWBOARD Multi-User Chat

🟢 **Verschlüsselter Chat für kleine Gruppen (z. B. Klasse, Team, Projekte)**  

- Alle Nachrichten sind **verschlüsselt**
- Jeder User bekommt automatisch einen **Agenten-Namen**
- Läuft über einen **Relay-Server**, der Nachrichten weiterleitet  

---

## 🛠 Schnelleinstieg (5 Minuten)

### Schritt 1: Projekt vorbereiten
```bash
cd Shadowboard
source venv/bin/activate
pip install -r requirements.txt
```

### Schritt 2: SSL-Zertifikate erstellen (nur einmal)
```bash
openssl req -x509 -newkey rsa:4096 -keyout src/core/certs/server.key -out src/core/certs/server.crt -days 365 -nodes
```

---

## 🚀 Server starten (eine Person macht das)

Öffne ein Terminal und führe aus:
```bash
cd Shadowboard
source venv/bin/activate
python3 -m src.core.relay_multi
```

✅ Der Server läuft jetzt und wartet auf Clients.

---

## 💻 Clients starten (alle anderen)

Öffne ein **neues Terminal** für jeden Client und führe aus:
```bash
cd Shadowboard
source venv/bin/activate
python3 -m src.core.message_test_multi
```

✅ Jeder Client bekommt automatisch einen **Agenten-Namen** (z. B. `AGENT Alpha`)  
✅ Einfach tippen, Enter drücken – fertig! Die Nachricht wird verschlüsselt an alle anderen gesendet.

---

## 📋 Zusammenfassung

| Wer | Was | Befehl |
|-----|-----|--------|
| **1 Person** | Server starten | `python3 -m src.core.relay_multi` |
| **Alle anderen** | Client starten | `python3 -m src.core.message_test_multi` |

---

## ⚡ Wichtig

- ⚠️ **Zuerst den Server starten**, dann die Clients
- 🔐 **Alle Nachrichten sind verschlüsselt** – keine zusätzlichen Einstellungen nötig
- 🏃 **Beenden:** Mit `Ctrl+C` könnt ihr Server oder Client beenden
- 🤖 **Agenten-Namen:** Werden automatisch vergeben (keine Eingabe nötig)

---

## 🖼 Wie es funktioniert

```
            +----------------+
            |  Relay Server  |
            +--------+-------+
                     |
          -----------------------
          |                     |
   Client 1                Client 2
   AGENT Alpha             AGENT Lone Wolf
```

Alle Clients kommunizieren über den Relay-Server, alles ist verschlüsselt.

---

## 📦 Anforderungen

```
cryptography
colorama
```
