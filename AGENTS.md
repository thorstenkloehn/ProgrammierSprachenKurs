# AGENTS.md

mdBook-Projekt „Programmiersprachen Lernen“ (Konfiguration: `book.toml`).

## Verzeichnisse

- `src/` – Kapitel des Buchs; `src/SUMMARY.md` legt Inhaltsverzeichnis und Reihenfolge fest.
- `RAW/` – Rohfassungen von Buchartikeln, an denen der Autor weiterarbeitet. Nicht Teil des gebauten Buchs.
- `book/` – Build-Ausgabe von `mdbook build` (in `.gitignore`), nicht von Hand bearbeiten.

## Arbeitsablauf: RAW → src

1. Rohfassung aus `RAW/` lesen.
2. Rechtschreibung, Grammatik und Zeichensetzung prüfen und verbessern. Stil nicht ändern, Inhalt und Ton des Autors beibehalten, nichts hinzudichten.
3. Die Korrekturen auch in der Rohfassung in `RAW/` übernehmen (ohne Transparenzhinweis), damit der Autor an der korrigierten Fassung weiterarbeiten kann.
4. Ergebnis unter demselben Dateinamen in `src/` speichern.
5. Kapitel in `src/SUMMARY.md` eintragen.

### Aktualisierung einer Rohfassung

Die Rohfassungen in `RAW/` bleiben dauerhaft bestehen, damit der Autor daran weiterarbeiten kann. Wird eine Rohfassung aktualisiert, wird die Endfassung in `src/` entsprechend aktualisiert:

1. Rohfassung aus `RAW/` erneut vollständig lesen.
2. Wie oben nur Rechtschreibung, Grammatik und Zeichensetzung korrigieren – kein anderer Stil, nichts hinzudichten – und die Korrekturen auch in der Rohfassung in `RAW/` übernehmen.
3. Die Endfassung in `src/` mit dem aktuellen Inhalt der Rohfassung neu erstellen – Ergänzungen, Änderungen und Streichungen werden übernommen.
4. Transparenzhinweis als Kopf- und Fußzeile in `src/` beibehalten.
5. `src/SUMMARY.md` prüfen und bei Bedarf anpassen.

## Transparenzhinweis

Jeder Artikel in `src/` (außer `SUMMARY.md`) erhält als Kopf- und Fußzeile – an beiden Stellen identisch – folgenden Hinweis. Kopfzeile: direkt unter der Kapitelüberschrift (`# …`). Fußzeile: letzte Zeile der Datei.

```markdown
*Dieser Text wurde von einem Menschen verfasst. Rechtschreibung und Grammatik wurden mit Unterstützung von Künstlicher Intelligenz geprüft und korrigiert (Transparenzhinweis gemäß Art. 50 EU AI Act).*
```
