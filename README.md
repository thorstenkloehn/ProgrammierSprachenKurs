# Programmiersprachen Lernen

Ein Buch über das Erlernen von Programmiersprachen, erstellt mit [mdBook](https://rust-lang.github.io/mdBook/).

## Projektstruktur

| Pfad         | Inhalt                                                                                 |
|--------------|----------------------------------------------------------------------------------------|
| `book.toml`  | Konfiguration des Buchs (Titel, Autor, Quellverzeichnis)                               |
| `src/`       | Fertige Kapitel des Buchs                                                              |
| `src/SUMMARY.md` | Inhaltsverzeichnis – legt fest, welche Kapitel in welcher Reihenfolge erscheinen   |
| `RAW/`       | Rohfassungen von Artikeln, die noch nicht ins Buch übernommen wurden (nicht versioniert) |
| `book/`      | Build-Ausgabe von `mdbook build` (nicht versioniert, nicht von Hand bearbeiten)        |
| `AGENTS.md`  | Anweisungen für KI-Assistenten, die am Projekt mitarbeiten                             |

## Arbeitsablauf: vom Rohtext zum Kapitel

Jeder Artikel entsteht zuerst als Rohfassung und wird dann in das Buch übernommen.

1. **Rohfassung schreiben** – Der Text wird als Markdown-Datei in `RAW/` abgelegt, z. B. `RAW/Vorwort.md`.
2. **Korrektur** – Rechtschreibung, Grammatik und Zeichensetzung werden geprüft und verbessert (mit Unterstützung von KI). Stil, Inhalt und Ton des Autors bleiben unverändert. Die Datei in `RAW/` wird dabei nicht verändert.
3. **Übernahme nach `src/`** – Die korrigierte Fassung wird unter demselben Dateinamen in `src/` gespeichert, z. B. `src/Vorwort.md`.
4. **Transparenzhinweis einfügen** – Direkt unter der Kapitelüberschrift (`# …`) und als letzte Zeile der Datei steht jeweils dieser Hinweis:

   ```markdown
   *Dieser Text wurde von einem Menschen verfasst. Rechtschreibung und Grammatik wurden mit Unterstützung von Künstlicher Intelligenz geprüft und korrigiert (Transparenzhinweis gemäß Art. 50 EU AI Act).*
   ```

5. **Inhaltsverzeichnis ergänzen** – Das Kapitel wird in `src/SUMMARY.md` eingetragen:

   ```markdown
   [Vorwort](Vorwort.md)
   ```

6. **Buch bauen und prüfen** – siehe unten.

## Buch bauen

Voraussetzung: [mdBook installieren](https://rust-lang.github.io/mdBook/guide/installation.html), z. B. mit `cargo install mdbook`.

```bash
mdbook serve --open   # lokale Vorschau mit automatischem Neuladen
mdbook build          # erzeugt das fertige Buch in book/
```
