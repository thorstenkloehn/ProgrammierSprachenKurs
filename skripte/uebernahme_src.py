#!/usr/bin/env python3
"""Auftrag B aus AGENTS.md: übernimmt Rohfassungen aus RAW/ nach src/.

Voraussetzung: Die Rohfassung in RAW/ ist bereits korrigiert (Rechtschreibung, Grammatik).
Das Skript ändert RAW/ nie. Es
  1. erzeugt src/<Datei>.md = RAW/<Datei>.md plus zwei Transparenzhinweise,
  2. pflegt src/SUMMARY.md (Titel aus der „# “-Überschrift, neue Kapitel am Ende),
  3. prüft das Ergebnis und
  4. führt „mdbook build“ aus.

Aufruf (im Projektordner):
  python3 skripte/uebernahme_src.py                 alle Artikel aus RAW/
  python3 skripte/uebernahme_src.py Desktop.md      nur diese Artikel
  python3 skripte/uebernahme_src.py --pruefen       nur prüfen, nichts schreiben
  python3 skripte/uebernahme_src.py --kein-build    ohne mdbook build
Rückgabewert 0 = alles in Ordnung, 1 = Fehler oder Abweichungen.
"""
import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "RAW"
SRC = ROOT / "src"
SUMMARY = SRC / "SUMMARY.md"

HINWEIS = ("*Dieser Text wurde von einem Menschen verfasst. Rechtschreibung und Grammatik wurden mit "
           "Unterstützung von Künstlicher Intelligenz geprüft und korrigiert "
           "(Transparenzhinweis gemäß Art. 50 EU AI Act).*")
EINTRAG = re.compile(r"^(\s*(?:[-*]\s+)?)\[(.*)\]\((.*\.md)\)\s*$")

fehler, meldungen, aenderungen = [], [], []


def titel_von(raw_zeilen, name):
    if not raw_zeilen or not raw_zeilen[0].startswith("# "):
        fehler.append(f"{name}: Die „# “-Hauptüberschrift fehlt in der ersten Zeile. Bitte beim Autor nachfragen.")
        return None
    return raw_zeilen[0][2:].strip()


def erzeuge_src(raw_zeilen):
    """H1, Leerzeile, Hinweis, Leerzeile, Rest der Rohfassung, Leerzeile, Hinweis."""
    rest = raw_zeilen[1:]
    while rest and rest[0] == "":
        rest.pop(0)
    while rest and rest[-1] == "":
        rest.pop()
    zeilen = [raw_zeilen[0], "", HINWEIS, ""] + rest
    zeilen += ["", HINWEIS] if rest else [HINWEIS]
    return "\n".join(zeilen) + "\n"


def ohne_leerzeilen_dubletten(text):
    return re.sub(r"\n{2,}", "\n\n", text.strip("\n"))


def pruefe_unterschied(name, raw_text, src_text):
    """Raw und src dürfen sich nur durch die beiden Hinweise unterscheiden."""
    zeilen = src_text.split("\n")
    anzahl = zeilen.count(HINWEIS)
    if anzahl != 2:
        fehler.append(f"{name}: Der Transparenzhinweis steht {anzahl}-mal statt genau zweimal.")
        return
    if len(zeilen) < 3 or zeilen[2] != HINWEIS:
        fehler.append(f"{name}: Der Hinweis steht nicht direkt unter der Kapitelüberschrift.")
    if src_text.rstrip("\n").split("\n")[-1] != HINWEIS:
        fehler.append(f"{name}: Der Hinweis ist nicht die letzte Zeile der Datei.")
    ohne = "\n".join(z for z in zeilen if z != HINWEIS)
    if ohne_leerzeilen_dubletten(ohne) != ohne_leerzeilen_dubletten(raw_text):
        fehler.append(f"{name}: src/ weicht über die Transparenzhinweise hinaus von RAW/ ab.")


def lies_summary():
    if not SUMMARY.exists():
        return ["# Summary", ""]
    return SUMMARY.read_text(encoding="utf-8").split("\n")


def pflege_summary(titel_je_datei, schreiben):
    zeilen = lies_summary()
    while zeilen and zeilen[-1] == "":
        zeilen.pop()
    vorhanden = {}
    for i, z in enumerate(zeilen):
        m = EINTRAG.match(z)
        if m:
            vorhanden.setdefault(m.group(3), []).append(i)
    for datei, idx in vorhanden.items():
        if len(idx) > 1:
            fehler.append(f"SUMMARY.md: Das Kapitel {datei} steht {len(idx)}-mal in der Liste.")
        if not (SRC / datei).exists():
            fehler.append(f"SUMMARY.md: Eintrag {datei} hat keine Datei in src/.")
    for datei, titel in titel_je_datei.items():
        if datei in vorhanden:
            i = vorhanden[datei][0]
            m = EINTRAG.match(zeilen[i])
            if m.group(2) != titel:
                meldungen.append(f"SUMMARY.md: Titel von {datei} geändert: „{m.group(2)}“ → „{titel}“")
                aenderungen.append(datei)
                zeilen[i] = f"{m.group(1)}[{titel}]({datei})"
        else:
            meldungen.append(f"SUMMARY.md: Neues Kapitel am Ende: {datei} („{titel}“)")
            aenderungen.append(datei)
            zeilen.append(f"[{titel}]({datei})")
    if schreiben:
        SUMMARY.write_text("\n".join(zeilen) + "\n", encoding="utf-8")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("dateien", nargs="*", help="Dateinamen in RAW/ (Standard: alle)")
    p.add_argument("--pruefen", action="store_true", help="nur prüfen, nichts schreiben")
    p.add_argument("--kein-build", action="store_true", help="mdbook build überspringen")
    a = p.parse_args()

    namen = [Path(d).name for d in a.dateien] or sorted(f.name for f in RAW.glob("*.md"))
    for n in namen:
        if not (RAW / n).exists():
            fehler.append(f"{n}: nicht in RAW/ gefunden.")
    namen = [n for n in namen if (RAW / n).exists()]

    titel_je_datei = {}
    for n in namen:
        raw_text = (RAW / n).read_text(encoding="utf-8")
        raw_zeilen = raw_text.split("\n")
        titel = titel_von(raw_zeilen, n)
        if titel is None:
            continue
        neu = erzeuge_src(raw_zeilen[:])
        ziel = SRC / n
        alt = ziel.read_text(encoding="utf-8") if ziel.exists() else None
        if alt != neu:
            meldungen.append(f"src/{n}: {'neu erstellt' if alt is None else 'aktualisiert'}")
            aenderungen.append(n)
            if not a.pruefen:
                ziel.write_text(neu, encoding="utf-8")
        pruefe_unterschied(n, raw_text, neu if not a.pruefen else (alt if alt is not None else neu))
        titel_je_datei[n] = titel

    pflege_summary(titel_je_datei, schreiben=not a.pruefen)

    if not a.kein_build and not a.pruefen:
        if shutil.which("mdbook") is None:
            fehler.append("mdbook ist nicht verfügbar; der Build wurde nicht ausgeführt.")
        else:
            r = subprocess.run(["mdbook", "build"], cwd=ROOT, capture_output=True, text=True)
            if r.returncode != 0 or not (ROOT / "book" / "index.html").exists():
                fehler.append("mdbook build ist fehlgeschlagen:\n" + (r.stderr or r.stdout).strip())
            elif "WARN" in r.stderr + r.stdout or "ERROR" in r.stderr + r.stdout:
                meldungen.append("mdbook build: mit Warnungen durchgelaufen.")
            else:
                meldungen.append("mdbook build: fehlerfrei.")

    if a.pruefen and meldungen:
        meldungen.insert(0, "(Nur Prüfung: Folgendes würde geändert.)")
    for m in meldungen:
        print(m)
    for f in fehler:
        print("FEHLER:", f, file=sys.stderr)
    if not meldungen and not fehler:
        print("Alles aktuell: src/ entspricht RAW/ plus Transparenzhinweisen.")
    # Im Prüfmodus gelten ausstehende Änderungen als Abweichung.
    return 1 if fehler or (a.pruefen and aenderungen) else 0


if __name__ == "__main__":
    sys.exit(main())
