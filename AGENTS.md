# AGENTS.md

mdBook-Projekt „Programmiersprachen Lernen“ (Konfiguration: `book.toml`).

## Verzeichnisse

- `src/` – Kapitel des Buchs; `src/SUMMARY.md` legt Inhaltsverzeichnis und Reihenfolge fest. Niemals manuell editieren, `RAW/` ist die alleinige Quelle („Single Source of Truth“).
- `RAW/` – Rohfassungen von Buchartikeln, an denen der Autor arbeitet. Nicht Teil des gebauten Buchs.
- `book/` – Build-Ausgabe von `mdbook build` (in `.gitignore`), nicht von Hand bearbeiten.

## Arbeitsablauf: RAW → src

1. Rohfassung aus `RAW/` lesen.
2. Rechtschreibung, Grammatik und Zeichensetzung prüfen und verbessern. Stil nicht ändern, Inhalt und Ton des Autors beibehalten, nichts hinzudichten.
3. Die Korrekturen auch in der Rohfassung in `RAW/` übernehmen (ohne Transparenzhinweis), damit der Autor an der korrigierten Fassung weiterarbeiten kann.
4. Ergebnis unter demselben Dateinamen in `src/` speichern.
5. Kapitel in `src/SUMMARY.md` eintragen (Titel exakt aus der `# `-Hauptüberschrift übernehmen; am Ende der Liste bzw. nach Rückfrage an der passenden Stelle einfügen).

## Umfang der Bearbeitung

- Nur die beauftragten Artikel bearbeiten.
- **Nur Textabschnitte korrigieren:** Wünscht der Benutzer nur die Korrektur eines bestimmten Abschnitts, erfolgt keine Übernahme nach `src/` und keine Änderung an `SUMMARY.md`.
- Bei unklaren Formulierungen nachfragen, statt die Bedeutung zu verändern.
- Codebeispiele, Befehle, URLs und Dateinamen unverändert lassen. Vermutete Fehler darin separat melden.

### Aktualisierung einer Rohfassung

Die Rohfassungen in `RAW/` bleiben dauerhaft bestehen, damit der Autor daran weiterarbeiten kann. Wird eine Rohfassung aktualisiert, wird die Endfassung in `src/` entsprechend aktualisiert:

1. Rohfassung aus `RAW/` erneut vollständig lesen.
2. Wie oben nur Rechtschreibung, Grammatik und Zeichensetzung korrigieren – kein anderer Stil, nichts hinzudichten – und die Korrekturen auch in der Rohfassung in `RAW/` übernehmen.
3. Die Endfassung in `src/` mit dem aktuellen Inhalt der Rohfassung neu erstellen – Ergänzungen, Änderungen und Streichungen werden übernommen.
4. Transparenzhinweis als Kopf- und Fußzeile in `src/` beibehalten.
5. `src/SUMMARY.md` prüfen und bei Bedarf anpassen.

## Prüfung nach der Übernahme

- Prüfen, dass die Endfassung der korrigierten Rohfassung entspricht, abgesehen von den beiden Transparenzhinweisen.
- Transparenzhinweise genau einmal unter der Kapitelüberschrift und einmal am Dateiende einfügen.
- Vorhandene Einträge in `src/SUMMARY.md` nicht doppelt eintragen.
- Nach Änderungen am Buch `mdbook build` ausführen. Falls der Befehl nicht verfügbar ist oder fehlschlägt, dies mitteilen.

## Transparenzhinweis

Jeder Artikel in `src/` (außer `SUMMARY.md`) erhält als Kopf- und Fußzeile – an beiden Stellen identisch – folgenden Hinweis. Kopfzeile: direkt unter der Kapitelüberschrift (`# …`), getrennt durch eine Leerzeile. Fußzeile: letzte Zeile der Datei.

```markdown
*Dieser Text wurde von einem Menschen verfasst. Rechtschreibung und Grammatik wurden mit Unterstützung von Künstlicher Intelligenz geprüft und korrigiert (Transparenzhinweis gemäß Art. 50 EU AI Act).*
```
