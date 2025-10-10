#!/usr/bin/env python3
# src/core/relay.py
"""
Minimaler TLS-Relay-Server (mTLS).
Relayet zeilen-/newline-terminierte Payloads (opaque bytes) an alle
anderen verbundenen, authentifizierten Clients.

Voraussetzung: server.crt, server.key, ca.crt liegen im selben Verzeichnis
oder Pfade werden angepasst.
"""

import socket
import ssl
import threading
import json
import logging
from datetime import datetime

LOG = logging.getLogger("relay")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

HOST = "0.0.0.0"
PORT = 4430  # non-root; für Produktion 443 verwenden
SERVER_CERT = "server.crt"
SERVER_KEY = "server.key"
CA_CERT = "ca.crt"

# einfache Struktur für aktive Clients
# key: conn object, value: {"addr": (ip,port), "cn": common_name}
clients = {}
clients_lock = threading.Lock()

def get_peer_cn(conn):
    try:
        cert = conn.getpeercert()
        # cert['subject'] ist eine tuple of tuples, traverse to find commonName
        subj = cert.get('subject', ())
        for rdn in subj:
            for k,v in rdn:
                if k.lower() in ('commonname', 'cn'):
                    return v
    except Exception:
        return None
    return None

def broadcast(sender_conn, payload_line):
    """Sende payload_line (bytes, newline-trimmed) an alle anderen Clients."""
    with clients_lock:
        for conn, meta in list(clients.items()):
            if conn is sender_conn:
                continue
            try:
                conn.sendall(payload_line + b'\n')
            except Exception as e:
                LOG.warning("Fehler beim Senden an %s: %s — wird entfernt", meta.get("addr"), e)
                _remove_client(conn)

def _remove_client(conn):
    with clients_lock:
        if conn in clients:
            meta = clients.pop(conn)
            try:
                conn.shutdown(socket.SHUT_RDWR)
            except Exception:
                pass
            try:
                conn.close()
            except Exception:
                pass
            LOG.info("Client entfernt: %s %s", meta.get("cn"), meta.get("addr"))

def handle_client(conn, addr):
    cn = get_peer_cn(conn) or "<unknown>"
    LOG.info("Client verbunden: CN=%s addr=%s", cn, addr)
    with clients_lock:
        clients[conn] = {"addr": addr, "cn": cn, "connected_at": datetime.utcnow().isoformat()}

    try:
        # Wir lesen zeilenweise (newline-terminierte Payloads)
        f = conn.makefile('rb')
        for raw in f:
            if raw is None:
                break
            line = raw.rstrip(b'\n\r')
            if not line:
                continue
            # optional: kleiner sanity-check oder logging
            LOG.debug("Empfangen von %s: %d bytes", cn, len(line))
            # Payload bleibt opaque — Relay liest nicht den Inhalt
            broadcast(conn, line)
    except Exception as e:
        LOG.warning("Client-Handler Fehler (%s): %s", cn, e)
    finally:
        _remove_client(conn)

def main():
    LOG.info("Starte Relay auf %s:%d", HOST, PORT)

    bindsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bindsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    bindsock.bind((HOST, PORT))
    bindsock.listen(32)

    # SSL Context für mTLS
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_cert_chain(certfile=SERVER_CERT, keyfile=SERVER_KEY)
    context.load_verify_locations(CA_CERT)

    try:
        while True:
            newsock, addr = bindsock.accept()
            try:
                connstream = context.wrap_socket(newsock, server_side=True)
                # Optionale zusätzliche AuthZ: nur CNs aus einer Whitelist zulassen
                cn = get_peer_cn(connstream)
                LOG.info("TLS handshake OK. Client CN: %s, addr=%s", cn, addr)
                t = threading.Thread(target=handle_client, args=(connstream, addr), daemon=True)
                t.start()
            except ssl.SSLError as se:
                LOG.warning("SSL Fehler bei Verbindung von %s: %s", addr, se)
                newsock.close()
    except KeyboardInterrupt:
        LOG.info("Relay herunterfahren per KeyboardInterrupt")
    finally:
        LOG.info("Shutting down listener")
        bindsock.close()

if __name__ == "__main__":
    main()
