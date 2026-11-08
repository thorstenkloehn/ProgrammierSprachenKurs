# Programmiersprachen Lernen

Ein Buch über das Erlernen von Programmiersprachen, erstellt mit [mdBook](https://rust-lang.github.io/mdBook/).

## Projektstruktur

| Pfad         | Inhalt                                                                                 |
|--------------|----------------------------------------------------------------------------------------|
| `book.toml`  | Konfiguration des Buchs (Titel, Autor, Quellverzeichnis)                               |
| `src/`       | Fertige Kapitel des Buchs                                                              |
| `src/SUMMARY.md` | Inhaltsverzeichnis – legt fest, welche Kapitel in welcher Reihenfolge erscheinen   |
| `RAW/`       | Dauerhaft aufbewahrte Rohfassungen, an denen der Autor weiterarbeitet                   |
| `book/`      | Build-Ausgabe von `mdbook build` (nicht versioniert, nicht von Hand bearbeiten)        |
| `AGENTS.md`  | Anweisungen für KI-Assistenten, die am Projekt mitarbeiten                             |

## Arbeitsablauf: vom Rohtext zum Kapitel

Jeder Artikel entsteht zuerst als Rohfassung und wird dann in das Buch übernommen.

1. **Rohfassung schreiben** – Der Text wird als Markdown-Datei in `RAW/` abgelegt, z. B. `RAW/Vorwort.md`.
2. **Korrektur** – Rechtschreibung, Grammatik und Zeichensetzung werden geprüft und verbessert (mit Unterstützung von KI). Stil, Inhalt und Ton des Autors bleiben unverändert. Die Korrekturen werden auch in der Datei in `RAW/` übernommen, jedoch ohne Transparenzhinweis.
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

Die Rohfassungen bleiben nach der Übernahme dauerhaft in `RAW/` erhalten. Bei einer erneuten Übernahme wird die gesamte aktuelle Rohfassung gelesen und sprachlich korrigiert. Die Fassung in `src/` wird daraus neu erstellt; Ergänzungen, Änderungen und Streichungen werden übernommen. Die beiden Transparenzhinweise bleiben in `src/` erhalten, und das Inhaltsverzeichnis wird bei Bedarf angepasst, ohne Einträge zu duplizieren.

## Prompts für die Arbeit am Buch

Ein Prompt ist ein Arbeitsauftrag an den KI-Assistenten. Die folgenden Texte kannst du im Chat verwenden, während dieses Projekt geöffnet ist. Sie sind keine Terminalbefehle. Ersetze die Beispieldatei `RAW/Vorwort.md` durch die gewünschte Rohfassung.

Die zentralen Regeln stehen in [AGENTS.md](AGENTS.md). Für einzelne Textabschnitte gelten zusätzlich die Regeln in [RAW/AGENTS.md](RAW/AGENTS.md).

### Eine Rohfassung ins Buch übernehmen

```text
Übernimm RAW/Vorwort.md nach dem Ablauf in AGENTS.md ins Buch.
```

Der Assistent liest die vollständige Rohfassung und korrigiert Rechtschreibung, Grammatik und Zeichensetzung. Er übernimmt die Korrekturen auch in `RAW/Vorwort.md`, erstellt `src/Vorwort.md` mit den beiden Transparenzhinweisen und ergänzt das Inhaltsverzeichnis. Anschließend prüft er den Build. Stil, Inhalt und Ton bleiben erhalten.

### Ein vorhandenes Kapitel aktualisieren

```text
Ich habe RAW/Vorwort.md überarbeitet. Aktualisiere das zugehörige Kapitel
in src/ nach dem Ablauf in AGENTS.md.
```

Verwende diesen Prompt, nachdem du eine Rohfassung ergänzt, verändert oder gekürzt hast. Der Assistent liest sie erneut vollständig und übernimmt den aktuellen Inhalt in das Buch. Bereits vorhandene Einträge im Inhaltsverzeichnis werden nicht doppelt angelegt.

### Nur einen Textabschnitt korrigieren

```text
Korrigiere in RAW/Vorwort.md ausschließlich den folgenden Absatz:
„Hier den zu korrigierenden Absatz einsetzen.“
Prüfe nur Rechtschreibung, Grammatik und Zeichensetzung.
```

Der Assistent korrigiert nur den angegebenen Abschnitt in der Rohfassung. Das Kapitel in `src/` und das Inhaltsverzeichnis werden durch diesen Auftrag nicht aktualisiert. Falls deine Oberfläche Textauswahl unterstützt, kannst du stattdessen ausdrücklich auf den markierten Abschnitt verweisen.

### Mehrere Rohfassungen übernehmen

```text
Übernimm RAW/Vorwort.md und RAW/Dokument_erstellen_software.md
nach dem Ablauf in AGENTS.md ins Buch.
```

Der Auftrag gilt für die genannten Artikel. Gib die Dateien ausdrücklich an, damit der Umfang eindeutig ist.

### Den Buch-Build prüfen

```text
Führe mdbook build aus und teile mir mit, ob der Build erfolgreich war.
```

Damit beauftragst du den Assistenten, das Buch zu bauen und das Ergebnis zu melden. Dieser Prompt beauftragt keine Textkorrektur.

## Terminalbefehle

Führe die folgenden Befehle im Terminal aus. Die Befehle zum Bauen und zur Vorschau müssen im Projektverzeichnis stehen, in dem sich `book.toml` befindet.

### mdBook installieren

Voraussetzung ist eine Rust-Installation mit Cargo. Wenn `mdbook` noch nicht installiert ist, installiere es einmalig mit:

```bash
cargo install mdbook
```

Cargo lädt und kompiliert mdBook und installiert den Befehl `mdbook`. Weitere Hinweise stehen in der [Installationsanleitung](https://rust-lang.github.io/mdBook/guide/installation.html).

### Lokale Vorschau starten

```bash
mdbook serve --open
```

`serve` baut das Buch und startet einen lokalen Vorschau-Server. `--open` öffnet die Vorschau im Browser. Bei Änderungen an den Quelldateien wird das Buch automatisch neu gebaut. Die Adresse steht im Terminal. Mit `Strg+C` beendest du den Server.

### Das Buch bauen

```bash
mdbook build
```

Dieser Befehl erstellt das fertige Buch im Verzeichnis `book/` und beendet sich anschließend. Er startet keinen Vorschau-Server. Die erzeugten Dateien werden nicht von Hand bearbeitet; Änderungen erfolgen in `src/` beziehungsweise über den Ablauf aus `RAW/`.
