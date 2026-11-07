# AGENTS.md

mdBook-Projekt „Programmiersprachen Lernen“ (Konfiguration: `book.toml`).

## Verzeichnisse

- `src/` – Kapitel des Buchs; `src/SUMMARY.md` legt Inhaltsverzeichnis und Reihenfolge fest.
- `RAW/` – Rohfassungen von Buchartikeln, die noch nicht als Kapitel nach `src/` übernommen wurden. Nicht Teil des gebauten Buchs.
- `book/` – Build-Ausgabe von `mdbook build` (in `.gitignore`), nicht von Hand bearbeiten.

## Arbeitsablauf: RAW → src

1. Rohfassung aus `RAW/` lesen; die Datei in `RAW/` bleibt unverändert.
2. Rechtschreibung, Grammatik und Zeichensetzung prüfen und verbessern. Stil nicht ändern, Inhalt und Ton des Autors beibehalten.
3. Ergebnis unter demselben Dateinamen in `src/` speichern.
4. Kapitel in `src/SUMMARY.md` eintragen.

## Transparenzhinweis

Jeder Artikel in `src/` (außer `SUMMARY.md`) erhält als Kopf- und Fußzeile – an beiden Stellen identisch – folgenden Hinweis. Kopfzeile: direkt unter der Kapitelüberschrift (`# …`). Fußzeile: letzte Zeile der Datei.

```markdown
*Dieser Text wurde von einem Menschen verfasst. Rechtschreibung und Grammatik wurden mit Unterstützung von Künstlicher Intelligenz geprüft und korrigiert (Transparenzhinweis gemäß Art. 50 EU AI Act).*
```
