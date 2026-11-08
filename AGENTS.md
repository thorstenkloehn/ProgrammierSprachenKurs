# AGENTS.md

mdBook-Projekt „Programmiersprachen Lernen“ (Konfiguration: `book.toml`).

## Verzeichnisse

- `RAW/` – Rohfassungen des Autors und Quelle aller Artikel („Single Source of Truth“). Sie bleiben dauerhaft bestehen, damit der Autor daran weiterarbeiten kann. Nicht Teil des gebauten Buchs.
- `src/` – Endfassungen der Artikel. Sie werden ausschließlich über die Aufträge unten geändert, nie frei von Hand. Ausnahme: `src/SUMMARY.md` (Inhaltsverzeichnis und Reihenfolge) wird nur in `src/` gepflegt und hat keine Rohfassung.
- `book/` – Build-Ausgabe von `mdbook build` (in `.gitignore`), nie bearbeiten.

## Grundsatz

`src/<Datei>.md` entspricht genau der korrigierten `RAW/<Datei>.md` plus den zwei Transparenzhinweisen. Weitere Unterschiede gibt es nicht.

## Korrekturregeln (gelten für alle Aufträge)

- Nur Rechtschreibung, Grammatik und Zeichensetzung korrigieren. Stil, Ton und Inhalt des Autors beibehalten, nichts hinzudichten.
- Codebeispiele, Befehle, URLs und Dateinamen unverändert lassen. Vermutete Fehler darin separat melden.
- Bei unklaren Formulierungen nachfragen, statt die Bedeutung zu verändern.
- Nur die beauftragten Artikel bzw. Abschnitte bearbeiten.

## Aufträge

### A) Einzelnen Textabschnitt korrigieren

Nur den angegebenen oder markierten Abschnitt in `RAW/` korrigieren. Keine Übernahme nach `src/`, keine Änderung an `src/SUMMARY.md`.

### B) Artikel übernehmen oder aktualisieren

Gilt für neue und für überarbeitete Rohfassungen gleichermaßen.

1. Rohfassung aus `RAW/` vollständig lesen.
2. Nach den Korrekturregeln korrigieren und die Korrekturen in der Rohfassung in `RAW/` speichern (ohne Transparenzhinweis).
3. `src/` unter demselben Dateinamen aus der korrigierten Rohfassung neu erstellen – Ergänzungen, Änderungen und Streichungen werden übernommen – und die beiden Transparenzhinweise einfügen (siehe unten).
4. `src/SUMMARY.md` pflegen: Titel exakt aus der `# `-Hauptüberschrift übernehmen. Neue Kapitel am Ende der Liste einfügen, außer der Benutzer nennt eine andere Stelle. Vorhandene Einträge nicht doppelt anlegen, bei geänderter Überschrift den Titel anpassen. Fehlt die `# `-Überschrift, nachfragen.
5. Prüfung durchführen (siehe unten) und `mdbook build` ausführen. Falls der Befehl nicht verfügbar ist oder fehlschlägt, dies mitteilen.

### C) Artikel entfernen

Nur auf ausdrücklichen Auftrag: Datei in `src/` und den Eintrag in `src/SUMMARY.md` löschen, danach `mdbook build` ausführen. Die Rohfassung in `RAW/` nur löschen, wenn der Benutzer das ausdrücklich verlangt.

## Prüfung nach der Übernahme

- Ein Vergleich von `RAW/<Datei>.md` und `src/<Datei>.md` zeigt nur die beiden Transparenzhinweise als Unterschied.
- Jeder Transparenzhinweis steht genau einmal: unter der Kapitelüberschrift und als letzte Zeile der Datei.
- Kein Kapitel steht doppelt in `src/SUMMARY.md`.

## Transparenzhinweis

Jeder Artikel in `src/` (außer `SUMMARY.md`) erhält als Kopf- und Fußzeile – an beiden Stellen identisch – folgenden Hinweis. Kopfzeile: direkt unter der Kapitelüberschrift (`# …`), getrennt durch eine Leerzeile. Fußzeile: letzte Zeile der Datei.

```markdown
*Dieser Text wurde von einem Menschen verfasst. Rechtschreibung und Grammatik wurden mit Unterstützung von Künstlicher Intelligenz geprüft und korrigiert (Transparenzhinweis gemäß Art. 50 EU AI Act).*
```
