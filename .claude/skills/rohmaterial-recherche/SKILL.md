---
name: rohmaterial-recherche
description: >-
  Führt eine strukturierte Web-Recherche zu den Themen der Artikel im Ordner RAW/
  (außer Vorwort.md) durch, fasst die Ergebnisse in eigenen Worten mit Quellen-URLs
  zusammen, ergänzt alternative Software sowie weitere Buchthemen und baut daraus
  ein eigenes mdBook im Ordner Rohmaterial/. Aktivieren, wenn der Benutzer nach
  Rohmaterial-Recherche, Web-Suche zu RAW-Artikeln, Aktualisierung von Rohmaterial/
  oder der Ausführung von google.md fragt.
---

# Skill: Rohmaterial-Recherche (`Rohmaterial/`)

Dieser Skill beschreibt den mehrstufigen Ablauf, um zu den Rohfassungen in `RAW/` fundiertes Hintergrundwissen im Web zu recherchieren und als eigenes, lesbares mdBook im Ordner `Rohmaterial/` aufzubereiten.

## Grundregeln

1. **Hauptbuch unangetastet lassen:** Die Dateien des Hauptbuchs in `RAW/` und `src/` sowie die Haupt-`book.toml` dürfen durch diesen Recherche-Skill **nicht verändert** werden.
2. **Ausnahme `Vorwort.md`:** Die Datei `RAW/Vorwort.md` wird bei der Recherche übersprungen (sofern der Benutzer nicht ausdrücklich etwas anderes verlangt).
3. **Eigene Worte & Quellenpflicht:** Alle gefundenen Inhalte werden in eigenen Worten auf Deutsch zusammengefasst. Zu **jedem inhaltlichen Punkt** muss direkt die verwendete Quelle mit vollständiger URL angegeben werden.
4. **Quellenqualität:** Primärquellen (offizielle Dokumentation, Spezifikationen, Projekt-Repositories, Release-Hinweise) haben Vorrang vor Blogs und Foren. Bei Quellen, die sich ändern können (Versionen, Lizenzen, Support-Zeiträume), das Abrufdatum angeben, z. B. `(abgerufen am 2026-11-09)`. Nicht erreichbare oder nicht gelesene Seiten dürfen nicht als Quelle erscheinen.
5. **Keine Änderung an `RAW/`:** Vermutete Fehler oder überholte Aussagen in einer Rohfassung werden nur gemeldet (siehe Schritt 5), nie dort korrigiert.
6. **Ignorierter Ordner:** `Rohmaterial/` und `Rohmaterial/book/` stehen in `.gitignore` und werden nicht committet.
7. **Zwei Kopien synchron halten:** Dieser Skill liegt identisch in `.claude/skills/rohmaterial-recherche/SKILL.md` und `.agents/skills/rohmaterial-recherche/SKILL.md`. Jede Änderung wird in beiden Dateien vorgenommen.

---

## Ablauf Schritt für Schritt

### Schritt 1: Themen aus `RAW/` erfassen
1. Liste alle Markdown-Dateien im Ordner `RAW/` auf (ohne `Vorwort.md`). Falls der Benutzer nur bestimmte Artikel benennt, bearbeite nur diese.
2. Lies den aktuellen Inhalt der betreffenden Dateien in `RAW/`, um alle genannten Sprachen, Frameworks, Werkzeuge und Fragestellungen zu erfassen.

### Schritt 2: Web-Recherche durchführen
Nutze `WebSearch` (zuerst Modus „standard“, „extended“ nur bei dünnen oder veralteten Treffern) und `WebFetch`, um Seiten wirklich zu lesen. Unabhängige Suchanfragen werden gleichzeitig abgesetzt.

Suche im Web gezielt zu den Themen jedes Artikels nach:
- Hintergrundfakten, Architekturprinzipien, Lizenzmodellen und Langzeitstabilität (z. B. 10–20 Jahre Horizont, Abwärtskompatibilität, statische Binärdateien),
- offiziellen Dokumentationen und verlässlichen Fachartikeln,
- vergleichbarer und alternativer Software bzw. Programmiersprachen,
- weiterführenden Themen, die im jeweiligen Buchkapitel noch behandelt werden könnten.

### Schritt 3: Ergebnisse in `Rohmaterial/src/<Datei>.md` speichern
Erstelle oder aktualisiere für jeden untersuchten Artikel aus `RAW/<Datei>.md` die gleichnamige Datei unter `Rohmaterial/src/<Datei>.md`.

**Vorhandene Dateien:** Eine bestehende Datei wird nicht komplett neu geschrieben. Lies sie zuerst, ergänze neue Punkte, aktualisiere veraltete Angaben samt Quelle und behalte unveränderte, noch gültige Abschnitte samt URLs. Wird ein Thema aus dem `RAW`-Artikel entfernt, den Benutzer fragen, ob der zugehörige Abschnitt gestrichen werden soll. Ist nur ein einzelner Punkt beauftragt, nur diesen Abschnitt ändern.

Gliederung:

1. **Grundanforderungen / Kernproblem des Themas** (mit Quellen + URLs)
2. **Detaillierte Analyse aller im `RAW`-Artikel genannten Technologien/Werkzeuge** (in eigenen Worten zusammengefasst, jeweils mit `* **Quelle:** <Titel>: <URL>` direkt beim Punkt)
3. **Alternative und ähnliche Software / Technologien** (konkrete Vorschläge mit Einordnung sowie Quellen + URLs)
4. **Weitere mögliche Themen für das Buch** (Vorschläge für zusätzliche Abschnitte, Praxisbeispiele oder Vertiefungen)

### Schritt 4: Eigenes mdBook in `Rohmaterial/` pflegen und bauen
1. Stelle sicher, dass `Rohmaterial/book.toml` existiert:
   ```toml
   [book]
   authors = ["Thorsten Klöhn"]
   language = "de"
   src = "src"
   title = "Rohmaterial – Programmiersprachen Lernen"
   ```
2. Aktualisiere `Rohmaterial/src/SUMMARY.md`, sodass alle recherchierten Artikel in `Rohmaterial/src/` verlinkt sind (Reihenfolge passend zur `src/SUMMARY.md` des Hauptbuchs, ohne `Vorwort.md`).
3. Führe im Ordner `Rohmaterial/` den Build aus:
   ```bash
   cd Rohmaterial && mdbook build
   ```
4. Prüfe, ob `mdbook build` fehlerfrei durchläuft und die HTML-Ausgabe unter `Rohmaterial/book/index.html` erzeugt wurde.
5. Bei Fehlschlag (z. B. `mdbook` nicht installiert, Build-Fehler, kaputte Links in `SUMMARY.md`) dies dem Benutzer mit der Fehlermeldung mitteilen und nicht als erfolgreich darstellen.

### Schritt 5: Faktencheck der Rohfassung
Widerspricht die Recherche einer Aussage in `RAW/<Datei>.md` (veraltete Version, falsche Eigenschaft, eingestellte Software), vermerke das im Rohmaterial in einem Hinweis `> **Hinweis zur Rohfassung:** …` mit Quelle und URL und nenne es im Bericht. `RAW/` bleibt unverändert; der Autor entscheidet.

### Schritt 6: Abschlussprüfung
- Jeder inhaltliche Punkt in `Rohmaterial/src/*.md` hat direkt eine Quelle mit vollständiger URL.
- Jede Quelle wurde tatsächlich abgerufen und ist erreichbar.
- Alle recherchierten Artikel stehen in `Rohmaterial/src/SUMMARY.md`, ohne Doppelungen und ohne `Vorwort.md`.
- `git status` zeigt keine Änderungen an `RAW/`, `src/` und der Haupt-`book.toml`.

### Schritt 7: Bericht an den Benutzer
Kurze Antwort auf Deutsch: welche Artikel neu oder aktualisiert wurden, welche Themen offen blieben, Ergebnis von `mdbook build`, vermutete Fehler in `RAW/` (Schritt 5).
