#!/usr/bin/env python3
"""Zeigt, welche Rohfassungen in RAW/ seit der letzten Rohmaterial-Recherche geändert wurden.

So muss der Skill rohmaterial-recherche nur neue oder geänderte Artikel bearbeiten.
Der Stand liegt in Rohmaterial/.stand.json (Hash je Artikel, Rohmaterial/ ist in .gitignore).

Aufruf (im Projektordner):
  python3 skripte/geaendert.py                    geänderte Artikel auflisten
  python3 skripte/geaendert.py --merken A.md B.md  Stand für diese Artikel speichern
                                                   (nach erfolgreicher Recherche)
  python3 skripte/geaendert.py --merken-alle       Stand für alle Artikel speichern
Rückgabewert 0 = nichts zu tun, 1 = es gibt geänderte Artikel.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "RAW"
ROH = ROOT / "Rohmaterial" / "src"
STAND = ROOT / "Rohmaterial" / ".stand.json"
AUSNAHMEN = {"Vorwort.md"}


def artikel():
    return sorted(f.name for f in RAW.glob("*.md") if f.name not in AUSNAHMEN)


def hash_von(name):
    return hashlib.sha256((RAW / name).read_bytes()).hexdigest()[:16]


def lade():
    try:
        return json.loads(STAND.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def speichere(stand):
    STAND.parent.mkdir(parents=True, exist_ok=True)
    STAND.write_text(json.dumps(stand, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def main(argv):
    stand = lade()
    if argv and argv[0] in ("--merken", "--merken-alle"):
        namen = artikel() if argv[0] == "--merken-alle" else [Path(a).name for a in argv[1:]]
        if not namen:
            print("Bitte Dateinamen angeben oder --merken-alle verwenden.", file=sys.stderr)
            return 2
        for n in namen:
            if not (RAW / n).exists():
                print(f"FEHLER: {n} nicht in RAW/ gefunden.", file=sys.stderr)
                return 2
            stand[n] = hash_von(n)
            print(f"Stand gemerkt: {n}")
        speichere(stand)
        return 0

    zu_tun = []
    for n in artikel():
        if not (ROH / n).exists():
            zu_tun.append((n, "neu (kein Rohmaterial vorhanden)"))
        elif stand.get(n) != hash_von(n):
            zu_tun.append((n, "geändert" if n in stand else "Stand unbekannt"))
    for n in stand:
        if n not in artikel():
            print(f"Hinweis: {n} steht im Stand, aber nicht mehr in RAW/ (Abschnitt im Rohmaterial ggf. streichen, vorher den Autor fragen).")
    if not zu_tun:
        print("Nichts zu tun: Alle Artikel sind seit der letzten Recherche unverändert.")
        return 0
    for n, grund in zu_tun:
        print(f"{n}: {grund}")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
