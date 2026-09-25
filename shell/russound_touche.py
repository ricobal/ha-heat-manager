#!/usr/bin/env python3
"""Envoie une ou plusieurs touches chiffre (0-9) au Russound via la passerelle RNET IP/série.

Remplace le flux Node-RED « Radio Russound » (2026-09-25).
Toutes les touches partent sur une seule connexion, à quelques ms d'intervalle,
comme le faisait Node-RED (le tuner attend la fréquence tapée d'un trait).
Usage : python3 russound_touche.py <chiffres, ex. 10590> [--dry-run]
"""
import socket
import sys
import time

HOTE = "192.168.1.74"
PORT = 4999
ECART = 0.005  # secondes entre deux touches


def trame(chiffre: int) -> bytes:
    # Événement clavier RNET : touche 1..9 = 0x01..0x09, touche 0 = 0x0A
    code = 0x0A if chiffre == 0 else chiffre
    corps = [0xF0, 0x00, 0x7D, 0x00, 0x00, 0x00, 0x70, 0x05, 0x02, 0x02,
             0x00, 0x00, code, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01]
    somme = (sum(corps) + len(corps)) & 0x7F
    return bytes(corps + [somme, 0xF7])


def main() -> int:
    if len(sys.argv) < 2 or not sys.argv[1].isdigit() or len(sys.argv[1]) > 8:
        print("usage: russound_touche.py <chiffres> [--dry-run]", file=sys.stderr)
        return 2
    trames = [trame(int(c)) for c in sys.argv[1]]
    if "--dry-run" in sys.argv:
        for t in trames:
            print(t.hex(" ").upper())
        return 0
    with socket.create_connection((HOTE, PORT), timeout=3) as s:
        for t in trames:
            s.sendall(t)
            time.sleep(ECART)
        time.sleep(0.05)
    return 0


if __name__ == "__main__":
    sys.exit(main())
