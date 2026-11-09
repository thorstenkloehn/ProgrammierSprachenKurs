# Anleitung: Optimale Prompts & Arbeitsabläufe ohne Probleme

Diese Anleitung enthält die besten, direkt kopierbaren Prompts für dein Projekt – optimiert für **wenig Tokenverbrauch**, **klare Ergebnisse** und **null Konflikte** zwischen Rohmaterial, Rohfassung (`RAW/`) und fertigem Buch (`src/`).

---

## Überblick: Welcher Ordner hat welche Aufgabe?

| Ordner / Datei | Zweck | Wer arbeitet darin? |
| :--- | :--- | :--- |
| **`RAW/`** | Deine eigenen Rohfassungen („Single Source of Truth") | **Du** schreibst hier; die KI korrigiert hier nur Rechtschreibung/Grammatik nach [AGENTS.md](AGENTS.md). |
| **`src/`** | Fertige Buchkapitel (inkl. Transparenzhinweis & `SUMMARY.md`) | Wird ausschließlich über die Aufträge in [AGENTS.md](AGENTS.md) aus `RAW/` erzeugt. |
| **`Rohmaterial/`** | Eigenes mdBook mit Web-Recherchen, Quellen-URLs, Alternativen & Themenideen | Wird über den Skill `rohmaterial-recherche` ([.agents/skills/rohmaterial-recherche/SKILL.md](.agents/skills/rohmaterial-recherche/SKILL.md)) befüllt. |
| **`AGENTS.md`** | Feste Regeln für Rechtschreibkorrektur und Buchübernahme (`RAW/` $\rightarrow$ `src/`) | Wird automatisch bei jedem Chat im Hintergrund geladen. |

---

## Teil 1: Web-Recherche ins `Rohmaterial/`-Buch ausführen

Der Skill **`rohmaterial-recherche`** sucht im Web nach Fakten, Quellen mit URL, alternativer Software und weiteren Buchthemen und baut daraus das separate mdBook im Ordner `Rohmaterial/`.

### 1.1 Sparsamster Prompt: Nur einen einzelnen Artikel recherchieren (Empfohlen!)
Wenn du in `RAW/` einen neuen Artikel angelegt oder erweitert hast, recherchiere **nur diese eine Datei**. Das spart rund 80 % Tokens und geht am schnellsten:

```text
Nutze den Skill rohmaterial-recherche nur für RAW/Desktop.md und aktualisiere das mdBook in Rohmaterial/.
```
*(Ersetze `RAW/Desktop.md` einfach durch die gewünschte Datei.)*

### 1.2 Noch sparsamer: Nur einen neuen Stichpunkt im Rohmaterial ergänzen
Wenn `Rohmaterial/src/CLI_Werkzeuge.md` schon existiert und du nur einen neuen Punkt (z. B. eine weitere Sprache) ergänzen lassen willst, ohne die ganze Datei neu zu schreiben:

```text
Recherchiere im Web mit Quelle und URL zum Punkt „Zig“ aus RAW/CLI_Werkzeuge.md und ergänze ihn als neuen Abschnitt in Rohmaterial/src/CLI_Werkzeuge.md. Führe danach mdbook build in Rohmaterial/ aus.
```

### 1.3 Komplett-Lauf: Alle Artikel in `RAW/` (außer `Vorwort.md`) recherchieren
Nur nötig, wenn du das gesamte `Rohmaterial/`-Buch von Grund auf neu aufbauen möchtest:

```text
@[google.md]
```
*(Oder ausgeschrieben: `Nutze den Skill rohmaterial-recherche für alle Artikel in RAW/ (außer Vorwort.md).`)*

---

## Teil 2: Vom `Rohmaterial/` zur eigenen Rohfassung in `RAW/`

Wenn du die Web-Recherche im Browser gelesen hast (siehe Teil 4) und nun dein eigenes Kapitel in `RAW/` schreibst, hast du zwei Möglichkeiten:

1. **Du schreibst selbst in `RAW/<Datei>.md`** und nutzt die Fakten und Links aus `Rohmaterial/` als Spickzettel.
2. **Du lässt dir für ein neues Thema zuerst nur eine Gliederung vorschlagen** (ohne dass die KI ungefragt in `src/` schreibt):

```text
Lies Rohmaterial/src/Webframework.md und schlage mir im Chat eine klare Gliederung für meinen Artikel RAW/Webframework.md vor. Verändere noch keine Dateien.
```

---

## Teil 3: Rohfassungen aus `RAW/` korrigieren & ins Hauptbuch (`src/`) übernehmen

Für diese Schritte gelten automatisch die strengen Regeln aus [AGENTS.md](AGENTS.md) (nur Rechtschreibung, Grammatik und Zeichensetzung; dein Stil und Inhalt bleiben zu 100 % erhalten).

### 3.1 Nur einen einzelnen Absatz in `RAW/` korrigieren (Auftrag A – extrem tokensparend)
Ideal, während du noch an einem langen Kapitel schreibst und nur die neuen Absätze prüfen lassen möchtest (`src/` bleibt dabei noch unberührt):

```text
Korrigiere in RAW/Desktop.md nach Auftrag A aus AGENTS.md nur den Abschnitt unter „## Rust“.
```

### 3.2 Fertigen Artikel aus `RAW/` ins Hauptbuch `src/` übernehmen (Auftrag B)
Wenn ein Artikel in `RAW/` fertig ist oder überarbeitet wurde und ins richtige Buch (`src/` + `src/SUMMARY.md` + `mdbook build`) übernommen werden soll:

```text
Übernimm RAW/Desktop.md nach Auftrag B in AGENTS.md ins Buch.
```

### 3.3 Mehrere Artikel auf einmal ins Hauptbuch übernehmen
```text
Übernimm RAW/CLI_Werkzeuge.md und RAW/Webframework.md nach Auftrag B in AGENTS.md ins Buch.
```

### 3.4 Einen Artikel wieder aus dem Hauptbuch entfernen (Auftrag C)
Löscht das Kapitel aus `src/` und `src/SUMMARY.md`, behält aber deine Rohfassung in `RAW/`:

```text
Entferne src/Desktop.md nach Auftrag C in AGENTS.md aus dem gebauten Buch (Rohfassung in RAW/ behalten).
```

---

## Teil 4: Beide Bücher im Browser ansehen (Terminalbefehle)

Du hast jetzt **zwei getrennte mdBooks** im Projekt, die sich niemals gegenseitig überschreiben:

### 1. Hauptbuch ansehen (`src/` $\rightarrow$ `book/`)
Im Hauptordner `/home/thorsten/ProgrammierSprachenKurs` im Terminal ausführen:
```bash
mdbook serve --open
```
*(Öffnet das Hauptbuch unter `http://localhost:3000` im Browser.)*

### 2. Rohmaterial-Buch ansehen (`Rohmaterial/src/` $\rightarrow$ `Rohmaterial/book/`)
Im Terminal ausführen:
```bash
mdbook serve Rohmaterial --open -p 3001
```
*(Startet das Rohmaterial-Buch auf Port `3001` unter `http://localhost:3001`, sodass du beide Bücher gleichzeitig nebeneinander im Browser geöffnet haben kannst!)*

---

## Teil 5: Arbeiten mit Visual Studio Code (VS Code) – Beste Tipps, um den Tokenverbrauch massiv zu senken

Wenn du dieses Projekt in **Visual Studio Code** (oder einer VS-Code-basierten Umgebung wie Antigravity / Cursor / Claude Code Extension) bearbeitest, entscheiden ein paar Handgriffe darüber, ob du für dieselbe Arbeit **500 Tokens oder 20.000 Tokens** verbrauchst.

### 1. Text im Editor markieren statt ganze Datei neu prüfen lassen (spart bis zu 90 % Tokens!)
Wenn du in `RAW/` an einem längeren Kapitel schreibst und nur zwei neue Absätze hinzugefügt hast:
1. Markiere mit der Maus im VS-Code-Editor **nur die neuen Absätze** in deiner `RAW/`-Datei.
2. Füge die Auswahl in den KI-Chat ein (je nach Erweiterung z. B. mit `Strg+L` oder Rechtsklick) und schreibe:
   ```text
   Korrigiere nur diesen markierten Abschnitt nach Auftrag A in AGENTS.md.
   ```
* **Warum das Tokens spart:** Der Assistent kennt sofort die exakte Zeilennummer, liest nicht die komplette Datei und tauscht nur diese wenigen Zeilen aus, statt das ganze Kapitel neu auszugeben.

### 2. Nicht benötigte Editor-Tabs schließen (`Strg+W` / `Strg+K W`)
* **Wichtiger Hintergrund:** Viele KI-Erweiterungen in VS Code hängen die **aktuell geöffnete Datei** (und manchmal auch zuletzt geöffnete Tabs) automatisch im Hintergrund an jede deiner Chat-Nachrichten an!
* Wenn du gerade im Tab `Rohmaterial/src/Desktop.md` (15 KB) bist, aber eigentlich eine kurze Frage zu `RAW/Vorwort.md` stellst, liest die KI im Hintergrund oft unnötig die große Rohmaterial-Datei mit.
* **Tipp:** Schließe große Dateien aus `Rohmaterial/` nach dem Lesen mit **`Strg+W`** (oder schließe alle Tabs mit **`Strg+K` und danach `W`**) und öffne immer nur die `RAW/`-Datei, an der du gerade arbeitest.

### 3. `mdbook build` und Vorschau selbst im VS-Code-Terminal oder per Vorschau nutzen (kostet 0 Tokens!)
Jedes Mal, wenn du im KI-Chat schreibst *„Bitte führe mdbook build aus"*, verbraucht der KI-Aufruf samt Einlesen der Terminal-Ausgabe rund **1.000 bis 2.000 Tokens**.
* **Kostenlose Alternative 1 – Live-Markdown-Vorschau in VS Code:**
  Drücke in einer geöffneten `RAW/`-Datei einfach **`Strg+K`** und direkt danach **`V`** (oder `Strg+Umschalt+V`). VS Code öffnet rechts daneben eine Live-Vorschau deines Artikels in Echtzeit – komplett ohne KI und ohne Build.
* **Kostenlose Alternative 2 – Integriertes VS-Code-Terminal (`Strg+Ö` oder `` Strg+` ``):**
  Starte einmalig unten im VS-Code-Terminal `mdbook serve --open`. Solange dieses Terminal offen bleibt, baut `mdbook` dein Buch bei jedem Speichern (`Strg+S`) automatisch im Hintergrund neu – für **0 Tokens**.

### 4. Die Ordner `book/` und `Rohmaterial/book/` in VS Code von der Suche ausschließen
Wenn `mdbook build` läuft, entstehen in `book/` und `Rohmaterial/book/` große Dateien wie `searchindex.js` (**über 800 KB!**) und `highlight.js`. Wenn VS Code oder ein KI-Agent das Projekt durchsucht, fressen diese generierten Dateien enorm viele Tokens.
* Lege im Projekt (falls gewünscht) die Datei `.vscode/settings.json` mit folgendem Inhalt an, damit VS Code und KI-Suchen die gebauten HTML-Ordner ignorieren:
  ```json
  {
    "search.exclude": {
      "**/book/**": true,
      "**/Rohmaterial/book/**": true
    },
    "files.watcherExclude": {
      "**/book/**": true,
      "**/Rohmaterial/book/**": true
    }
  }
  ```

### 5. Nach jedem erledigten Kapitel auf „Neuer Chat" (`+`) klicken
Das ist die **wichtigste Sparregel überhaupt**:
* KI-Chats haben kein kostenloses Gedächtnis. Bei deiner **1. Nachricht** im Chat zahlst du z. B. 2.000 Tokens. Bei der **10. Nachricht** im selben Chat wird der gesamte bisherige Verlauf (Nachricht 1 bis 9 samt allen gelesenen Dateien!) im Hintergrund noch einmal mitgeschickt – du zahlst dann plötzlich 25.000 Tokens für eine einzige kurze Frage!
* **Goldene Regel in VS Code:** Sobald ein Auftrag erledigt ist (z. B. `RAW/Desktop.md` wurde nach `src/` übernommen), klicke oben im KI-Fenster auf **`+` (Neuer Chat)** oder tippe `/compact`. Da deine Texte sicher in `RAW/` und `src/` auf der Festplatte liegen, geht nichts verloren und der Tokenzähler startet wieder bei null.

---

## Zusammenfassung: 5 goldene Regeln für problemloses Arbeiten & minimalen Tokenverbrauch

1. **Immer den genauen Dateinamen nennen (`@RAW/CLI_Werkzeuge.md`):** Schreibe nie pauschal „korrigiere meine Dateien", sondern nenne immer genau die eine Datei oder markiere den Absatz in VS Code.
2. **Neuer Chat (`+`) nach jeder abgeschlossenen Aufgabe:** Verhindert, dass alte Kapitel und Suchergebnisse bei jeder weiteren Nachricht immer wieder mitberechnet werden.
3. **Passendes Modell wählen (wie in `RAW/Sprachmodel.md`):**
   * **Web-Recherche (`rohmaterial-recherche`) & schnelle Absatz-Korrekturen:** Schnelles, sparsames Modell (z. B. *Gemini Flash*, *Gemini Argon (Medium)*, *Claude Haiku/Sonnet*).
   * **Komplexe Buchgliederung & tiefes Lektorat:** Großes Modell (z. B. *Claude Opus* oder *Gemini Pro/Argon*).
4. **Keine Sorge vor großen Ordnern auf der Festplatte:** Dateien in `RAW/`, `src/` und `Rohmaterial/` verbrauchen im Ruhezustand **0 Tokens**, solange sie nicht im Editor als aktiver Kontext offen sind oder im Prompt erwähnt werden.
5. **Skill gezielt pro Datei aufrufen:** Nutze `Nutze den Skill rohmaterial-recherche nur für RAW/<Datei>.md`, statt jedes Mal alle Kapitel neu durchsuchen zu lassen.
