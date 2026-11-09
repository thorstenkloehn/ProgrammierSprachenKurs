# Sprachmodell

*Dieser Text wurde von einem Menschen verfasst. Rechtschreibung und Grammatik wurden mit Unterstützung von Künstlicher Intelligenz geprüft und korrigiert (Transparenzhinweis gemäß Art. 50 EU AI Act).*

Wie Sprachmodelle am besten eingesetzt werden und wie man ein Lehrbuch schreibt: Hier ist der richtige Einsatz.

| Schritte                                              | Empfohlenes Modell                                                                                 |
|-------------------------------------------------------|----------------------------------------------------------------------------------------------------|
| Recherche und Arbeit mit eigenen Unterlagen           | Gemini 4 Argon, Gemini 3.1 Pro, Gemini 3.8 Flash oder Grok                                         |
| Gliederung und Rohfassung                             | Claude Fable 5.1, Claude Opus 5.5, GPT-6.1 Sol oder DeepSeek                                       |
| Rohfassung der Kapitel                                | Claude Opus 5.5, Claude Fable 5.1 oder Mistral Large                                               |
| Codebeispiele, Projektpflege und Lektorat nach Regeln | Gemini 4 Argon oder DeepSeek                                                                       |
| Gegenlesen durch ein zweites Modell                   | GPT-6.1 Sol, Gemini 4 Argon oder Grok (wenn Claude geschrieben hat), sonst Claude Opus 5.5         |
| Laufende Korrektur einzelner Kapitel                  | Claude Sonnet 5.5, Claude Haiku 5.5, Gemini 4 Argon, Gemini 3.8 Flash oder Mistral                 |

Wie Sprachmodelle am besten für ein Code-Projekt eingesetzt werden:

| Schritte                                             | Empfohlenes Modell                                                                                 |
|------------------------------------------------------|----------------------------------------------------------------------------------------------------|
| Architektur, Planung und Systemdesign                | Claude Opus 5.5, Claude Fable 5.1, GPT-6.1 Sol oder Gemini 4 Argon                                 |
| Gesamte Codebasis analysieren (großer Kontext)       | Gemini 4 Argon oder Gemini 3.1 Pro                                                                 |
| Neue Funktionen und Module programmieren             | Claude Sonnet 5.5, Claude Opus 5.5, Gemini 4 Argon oder DeepSeek                                   |
| Fehlersuche (Debugging) und komplexe Probleme lösen  | Claude Opus 5.5, GPT-6.1 Sol, Gemini 4 Argon oder DeepSeek                                         |
| Code-Review durch ein zweites Modell                 | GPT-6.1 Sol oder Gemini 4 Argon (wenn Claude programmiert hat), sonst Claude Opus 5.5              |
| Refactoring, Unit-Tests und schnelle Anpassungen     | Claude Sonnet 5.5, Claude Haiku 5.5, Gemini 4 Argon oder Gemini 3.8 Flash                          |
| Dokumentation (README, API-Docs, Kommentare)         | Claude Sonnet 5.5, Gemini 3.1 Pro oder Mistral Large                                               |

## Hier ist ein Beispiel
Erstelle den Ordner Rohmaterial. Nutze ein Sprachmodell von oben aus der Kategorie „Recherche und Arbeit mit eigenen Unterlagen“. Ich nutze Gemini 3.8 Flash mit dem Prompt: „Suche zum folgenden Thema: AI. Extrahiere alles, was du findest, und speichere die Inhalte im Ordner Rohmaterial und Quellcode.“

Jetzt sagen wir: Erstelle einen Prompt, bitte ein mdBook-Buch erstellen, wo die Daten vom Ordner Rohfassung sind. Bitte nur eine Gliederung und ein Inhaltsverzeichnis (SUMMARY.md) schreiben, sonst nichts. Für wen das Buch ist: Zielgruppe ist das Sprachmodell Claude Opus 5.5.

*Dieser Text wurde von einem Menschen verfasst. Rechtschreibung und Grammatik wurden mit Unterstützung von Künstlicher Intelligenz geprüft und korrigiert (Transparenzhinweis gemäß Art. 50 EU AI Act).*
