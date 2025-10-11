```markdown
# SHADOWBOARD Multi-User Chat

🟢 **Verschlüsselter Chat für kleine Gruppen (z. B. Klasse, Team, Projekte)**  

- Alle Nachrichten sind **verschlüsselt**
- Jeder User bekommt automatisch einen **Agenten-Namen**
- Läuft über einen **Relay-Server**, der Nachrichten weiterleitet  

---

## 🛠 Vorbereitung

1. **Repository klonen / Dateien herunterladen**  

   ```bash
   git clone (URL)
   cd Shadowboard
   ```

2. **Python-Umgebung aktivieren**  

   ```bash
   source venv/bin/activate
   ```

3. **Python-Module installieren**

   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Server starten (eine Person)

1. In das Projektverzeichnis wechseln:

   ```bash
   cd ~/Shadowboard
   ```

2. SSL-Zertifikate erstellen (nur einmal nötig):

   ```bash
   openssl req -x509 -newkey rsa:4096 -keyout src/core/certs/server.key -out src/core/certs/server.crt -days 365 -nodes
   ```

3. Relay starten:

   ```bash
   python3 src/core/relay_multi.py
   ```

> Der Server wartet nun auf Clients.

---

## 💻 Clients starten (alle anderen)

1. In das Projektverzeichnis wechseln:

   ```bash
   cd ~/Shadowboard
   ```

2. Python-Umgebung aktivieren:

   ```bash
   source venv/bin/activate
   ```

3. Client starten:

   ```bash
   python3 src/core/message_test_multi.py
   ```

4. Dein Agenten-Name wird automatisch angezeigt (z. B. `AGENT Alpha`).
5. Einfach tippen und Enter drücken – deine Nachricht wird **verschlüsselt** an alle anderen Clients geschickt.

---

## ⚡ Hinweise

- **Zertifikate:** Nur der Server benötigt sie.
- **Agenten-Namen:** Werden automatisch vergeben, keine manuelle Eingabe nötig.
- **Beenden:** Mit `Ctrl+C` beendet ihr Server oder Client.

---

## 📦 Anforderungen

In deiner `requirements.txt` sollten mindestens folgende Pakete stehen:

```
cryptography
colorama
```

---

## 🖼 Übersicht

```text
            +----------------+
            |  Relay Server  |
            +--------+-------+
                     |
          -----------------------
          |                     |
   Client 1                Client 2
   AGENT Alpha             AGENT Lone Wolf
```

Alle Clients kommunizieren **verschlüsselt** über den Relay-Server.

---

## 🟢 Tipps

- Startet immer **zuerst den Server**, sonst können sich Clients nicht verbinden.
- Alle Nachrichten sind verschlüsselt, es ist **keine weitere Installation nötig**.
```
