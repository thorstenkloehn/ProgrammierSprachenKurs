#!/usr/bin/env python3
"""Mechanische Abschlussprüfung für Rohmaterial/ (ersetzt die manuelle Prüfung im Skill).

Prüft ohne KI:
  1. Jeder inhaltliche Punkt hat im Block eine Quelle mit vollständiger URL
     (ausgenommen die Abschnitte „Weitere mögliche Themen“, das sind Vorschläge).
  2. Alle URLs sind erreichbar (Netzwerk nötig; --offline überspringt das).
  3. Alle Artikel aus RAW/ (außer Vorwort.md) stehen genau einmal in Rohmaterial/src/SUMMARY.md,
     Vorwort.md steht nicht darin.
  4. RAW/, src/ und die Haupt-book.toml sind laut git unverändert (nur Hinweis, nicht Fehler).
  5. mdbook build in Rohmaterial/ läuft fehlerfrei (--kein-build überspringt das).

Aufruf (im Projektordner):
  python3 skripte/rohmaterial_pruefen.py [--offline] [--kein-build]
Rückgabewert 0 = in Ordnung, 1 = Fehler gefunden.
"""
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "RAW"
ROH = ROOT / "Rohmaterial" / "src"
URL = re.compile(r"https?://[^\s)>\]*`]+")
fehler, warnungen = [], []


def bloecke(text):
    """Zerlegt in (Abschnitt, Überschrift des Blocks, Block); Block = Aufzählungspunkt samt Einrückung."""
    abschnitt, aus = "", []
    zeilen = text.split("\n")
    i = 0
    while i < len(zeilen):
        z = zeilen[i]
        if z.startswith("## "):
            abschnitt = z[3:]
        m = re.match(r"^\* (.*)", z)
        if m:
            block = [z]
            i += 1
            while i < len(zeilen) and (zeilen[i].startswith("  ") or zeilen[i] == ""):
                if zeilen[i] == "" and (i + 1 >= len(zeilen) or not zeilen[i + 1].startswith("  ")):
                    break
                block.append(zeilen[i])
                i += 1
            aus.append((abschnitt, m.group(1)[:60], "\n".join(block)))
            continue
        i += 1
    return aus


def pruefe_quellen(urls_gesamt):
    for datei in sorted(ROH.glob("*.md")):
        if datei.name == "SUMMARY.md":
            continue
        text = datei.read_text(encoding="utf-8")
        for abschnitt, kopf, block in bloecke(text):
            if abschnitt.lower().startswith("weitere mögliche themen"):
                continue
            # Quelle-Zeilen sind selbst Blöcke („* **Quelle:** …“) und gehören zum Elternpunkt.
            if kopf.startswith("**Quelle"):
                continue
            if not URL.search(block):
                fehler.append(f"{datei.name} [{abschnitt[:40]}]: Punkt ohne Quelle/URL: „{kopf}…“")
        for u in URL.findall(text):
            u = u.rstrip(".,;:")
            if re.match(r"https?://(127\.0\.0\.1|localhost)", u):
                continue  # lokale Beispieladressen sind keine Quellen
            urls_gesamt.setdefault(u, set()).add(datei.name)


def erreichbar(url):
    kopf = {"User-Agent": "Mozilla/5.0 (rohmaterial_pruefen)"}
    for methode in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, headers=kopf, method=methode)
            with urllib.request.urlopen(req, timeout=15) as r:
                return url, r.status, None
        except urllib.error.HTTPError as e:
            if methode == "HEAD" and e.code in (400, 403, 405, 501):
                continue
            return url, e.code, None
        except Exception as e:  # Netzwerkfehler, Zertifikat, Timeout
            if methode == "HEAD":
                continue
            return url, None, str(e)[:60]
    return url, None, "unbekannt"


def pruefe_links(urls):
    with ThreadPoolExecutor(max_workers=8) as ex:
        for url, status, err in ex.map(erreichbar, sorted(urls)):
            dateien = ", ".join(sorted(urls[url]))
            if status is None:
                warnungen.append(f"Nicht abrufbar ({err}): {url}  [{dateien}]")
            elif status in (401, 403, 429):
                warnungen.append(f"Nicht prüfbar (HTTP {status}, Zugriff verweigert): {url}  [{dateien}]")
            elif status >= 400:
                fehler.append(f"Link kaputt (HTTP {status}): {url}  [{dateien}]")


def pruefe_summary():
    pfad = ROH / "SUMMARY.md"
    if not pfad.exists():
        fehler.append("Rohmaterial/src/SUMMARY.md fehlt.")
        return
    eintraege = re.findall(r"\]\(([^)]+\.md)\)", pfad.read_text(encoding="utf-8"))
    for e in set(eintraege):
        if eintraege.count(e) > 1:
            fehler.append(f"SUMMARY.md: {e} steht {eintraege.count(e)}-mal in der Liste.")
        if not (ROH / e).exists():
            fehler.append(f"SUMMARY.md: Eintrag {e} hat keine Datei.")
    if "Vorwort.md" in eintraege:
        fehler.append("SUMMARY.md: Vorwort.md darf im Rohmaterial nicht vorkommen.")
    for f in sorted(RAW.glob("*.md")):
        if f.name != "Vorwort.md" and f.name not in eintraege:
            fehler.append(f"SUMMARY.md: {f.name} aus RAW/ fehlt im Rohmaterial-Inhaltsverzeichnis.")


def pruefe_git():
    if shutil.which("git") is None:
        return
    r = subprocess.run(["git", "status", "--porcelain", "--", "RAW", "src", "book.toml"],
                       cwd=ROOT, capture_output=True, text=True)
    if r.stdout.strip():
        warnungen.append("git meldet Änderungen an RAW/, src/ oder book.toml (nur ein Hinweis, falls "
                         "sie beabsichtigt sind):\n  " + r.stdout.strip().replace("\n", "\n  "))


def pruefe_build():
    if shutil.which("mdbook") is None:
        fehler.append("mdbook ist nicht verfügbar; der Build wurde nicht ausgeführt.")
        return
    r = subprocess.run(["mdbook", "build"], cwd=ROOT / "Rohmaterial", capture_output=True, text=True)
    ausgabe = r.stderr + r.stdout
    if r.returncode != 0 or not (ROOT / "Rohmaterial" / "book" / "index.html").exists():
        fehler.append("mdbook build in Rohmaterial/ ist fehlgeschlagen:\n" + ausgabe.strip())
    elif "WARN" in ausgabe or "ERROR" in ausgabe:
        warnungen.append("mdbook build mit Warnungen:\n" + ausgabe.strip())


def main(argv):
    if not ROH.exists():
        print("FEHLER: Rohmaterial/src/ existiert nicht.", file=sys.stderr)
        return 1
    urls = {}
    pruefe_quellen(urls)
    if "--offline" not in argv:
        pruefe_links(urls)
    pruefe_summary()
    pruefe_git()
    if "--kein-build" not in argv:
        pruefe_build()
    print(f"Geprüft: {len(urls)} URLs in {len([f for f in ROH.glob('*.md') if f.name != 'SUMMARY.md'])} Dateien"
          + (" (Links nicht geprüft: --offline)" if "--offline" in argv else "") + ".")
    for w in warnungen:
        print("HINWEIS:", w)
    for f in fehler:
        print("FEHLER:", f, file=sys.stderr)
    if not fehler:
        print("In Ordnung.")
    return 1 if fehler else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
