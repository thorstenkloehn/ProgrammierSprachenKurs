---
name: proto-erstellung
description: >-
  Baut das Prototyp-mdBook im Ordner Proto/ aus den Rohfassungen in RAW/ und der
  Web-Recherche in Rohmaterial/src/ (Lehrbuch-Prototyp mit Grundprinzipien, Ausblick,
  Quellenverzeichnis und Tipps, wie die Prototyp-Artikel noch geschrieben werden sollen).
  Aktivieren, wenn der Benutzer nach Proto, Prototyp-Buch, Proto.md, Aktualisierung von
  Proto/ oder skripte/build_proto.py fragt.
---

# Skill: Prototyp-Buch (`Proto/`)

Ablauf gemäß `Proto.md`: `RAW/` und `Rohmaterial/src/` lesen, alles extrahieren und ordnen, daraus ein umfassendes Lehrbuch-mdBook als Prototyp in `Proto/` erzeugen.

## Grundregeln

1. **Nur `Proto/` ändern.** `RAW/`, `src/`, `Rohmaterial/` und die Haupt-`book.toml` bleiben unangetastet. `Proto/` wird komplett generiert, nie von Hand bearbeitet (Änderungen gehen in das Skript).
2. **Autorentext unverändert:** Inhalte aus `RAW/` erscheinen wörtlich im Abschnitt „Kernaussagen des Autors“ (Überschriften nur eine Ebene tiefer). Alles aus der KI-Recherche steht in eigenen, getrennten Abschnitten. Nichts vermischen, nichts hinzudichten.
3. **Transparenzhinweis:** Jede Kapiteldatei erhält den Prototyp-Hinweis (Konstante `HINWEIS` im Skript) unter der Überschrift und als letzte Zeile.
4. **Quellen bleiben erhalten:** Jede Aussage aus `Rohmaterial/` behält ihre URL.
5. **Sprache:** Deutsch.

## Ablauf

### Schritt 1: Voraussetzungen prüfen
- `RAW/*.md` und `Rohmaterial/src/*.md` lesen bzw. auflisten. Fehlt zu einem Artikel das Rohmaterial, den Benutzer informieren und ggf. zuerst den Skill `rohmaterial-recherche` vorschlagen.
- Neue Artikel in `RAW/` müssen in der Liste `KAPITEL` (und ggf. `GRUNDPRINZIP_AUS`) in `skripte/build_proto.py` sowie in der SUMMARY-Gliederung des Skripts ergänzt werden.

### Schritt 2: Generieren
```bash
python3 skripte/build_proto.py && cd Proto && mdbook build
```
Das Skript erzeugt in `Proto/src/`: Kapitel je Artikel, `Grundprinzipien.md`, `Ausblick.md`, `Quellen.md`, `Vorwort.md`, `SUMMARY.md` und `Proto/book.toml`.
Jedes Themenkapitel enthält am Ende den Abschnitt „Tipps zum Weiterschreiben“ (`schreibtipps()` im Skript): Wortzahlen, Abgleich der Rohfassung mit den recherchierten Technologien (genannt / fehlt) und eine Checkliste, als KI-Vorschlag gekennzeichnet.

### Schritt 3: Lehrbuch-Inhalt und Schreibtipps ergänzen
Das Skript erzeugt den Abschnitt „Tipps zum Weiterschreiben“ automatisch (Funktion `schreibtipps()`, Konstante `TECHNOLOGIE_KAPITEL`, Tabelle `ALIASE`). Bei neuen Artikeln prüfen, ob sie in `TECHNOLOGIE_KAPITEL` gehören und ob Schreibvarianten in `ALIASE` fehlen. Die Tipps nie in `RAW/` schreiben.

### Schritt 4: Prüfung
- `mdbook build` läuft fehlerfrei, `Proto/book/index.html` existiert. Ist `mdbook` nicht verfügbar oder schlägt fehl, dies mitteilen.
- Jeder Text aus `RAW/` kommt unverändert im Kapitel vor (Stichprobe per `diff`/`grep`).
- Jede Kapiteldatei hat den Hinweis genau zweimal (Kopf und Fuß).
- Kein Kapitel doppelt in `Proto/src/SUMMARY.md`; alle Links lösen auf.
- `git status`: Änderungen nur in `Proto/` und ggf. `skripte/build_proto.py`.

### Schritt 5: Bericht
Kurz auf Deutsch: neue/geänderte Kapitel, fehlendes Rohmaterial, vermutete Fehler in `RAW/` (nur melden, nicht ändern).
