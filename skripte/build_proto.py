#!/usr/bin/env python3
"""Baut den Prototyp-mdBook Proto/ aus RAW/ und Rohmaterial/src/.

Aufruf im Projektordner: python3 skripte/build_proto.py && mdbook build Proto
"""
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
RAW = ROOT / "RAW"
ROH = ROOT / "Rohmaterial" / "src"
OUT = ROOT / "Proto" / "src"
LEHR = ROOT / "Proto" / "lehrtext"  # von der KI aus dem Rohmaterial abgeleitete Lehrbuch-Elemente
OUT.mkdir(parents=True, exist_ok=True)

HINWEIS = ("*Prototyp: Dieses Kapitel wurde mit Unterstützung von Künstlicher Intelligenz aus den "
           "Rohfassungen des Autors (`RAW/`) und der KI-gestützten Web-Recherche (`Rohmaterial/`) "
           "zusammengestellt. Abschnitte „Kernaussagen des Autors“ stammen vom Menschen, alle übrigen "
           "Abschnitte aus der KI-Recherche (Transparenzhinweis gemäß Art. 50 EU AI Act).*")

# Reihenfolge und Zuordnung der Themenkapitel
KAPITEL = [
    ("Dokument_erstellen_software.md", "Dokumente"),
    ("Markdown.md", "Markdown"),
    ("CLI_Werkzeuge.md", "CLI-Werkzeuge"),
    ("Desktop.md", "Desktop-Anwendungen"),
    ("Webframework.md", "Webframeworks"),
    ("Sprachmodel.md", "Sprachmodelle"),
    ("KI_AGENT.md", "KI-Coding-Agents"),
    ("Fertige_Plattformen.md", "Fertige Plattformen"),
    ("Werkzeuge.md", "Werkzeugübersicht"),
]
# Bei diesen Kapiteln wandert Abschnitt 1 (allgemeine Grundprinzipien) in ein eigenes Kapitel
GRUNDPRINZIP_AUS = {"CLI_Werkzeuge.md", "Desktop.md", "Webframework.md"}


def raw_parts(name):
    text = (RAW / name).read_text(encoding="utf-8").strip("\n")
    lines = text.splitlines()
    title = lines[0][2:].strip()
    body = "\n".join(lines[1:]).strip("\n")
    # Überschriften des Autors um eine Ebene absenken (## -> ###)
    body = re.sub(r"^(#+) ", lambda m: "#" + m.group(1) + " ", body, flags=re.M)
    return title, body


def roh_sections(name):
    """Liefert die ##-Abschnitte des Rohmaterials als Liste (Titel, Inhalt)."""
    text = (ROH / name).read_text(encoding="utf-8")
    parts = re.split(r"^## ", text, flags=re.M)[1:]
    out = []
    for p in parts:
        head, _, body = p.partition("\n")
        head = re.sub(r"^\d+\.\s*", "", head).strip()
        body = re.sub(r"^(### )\d+\.\d+\s+", r"\1", body, flags=re.M)  # „### 2.1 Go“ -> „### Go“
        body = re.sub(r"\n---\s*$", "", body.strip("\n")).strip("\n")
        out.append((head, body))
    return out


TIPP_HINWEIS = ("*KI-Vorschlag: Die folgenden Tipps wurden automatisch aus dem Vergleich von Rohfassung "
                "und Recherche abgeleitet. Sie sind Anregungen, keine Vorgaben; der Autor entscheidet.*")
# Kapitel, in denen die ###-Überschriften der Analyse einzelne Technologien sind (Abgleich per Name).
# Bei den übrigen Kapiteln (Sprachmodelle) sind es Themenblöcke, die nur aufgelistet werden.
TECHNOLOGIE_KAPITEL = {"Dokument_erstellen_software.md", "CLI_Werkzeuge.md", "Desktop.md", "Webframework.md",
                       "KI_AGENT.md", "Fertige_Plattformen.md"}


ALIASE = {"Go": ["Golang"], "bubblewrap": ["bwrap"]}  # andere Schreibweisen desselben Begriffs


def namen(ueberschrift):
    """Zerlegt „Java: Swing und JavaFX“ in Suchbegriffe (Java, Swing, JavaFX)."""
    ueberschrift = re.sub(r"`|\([^)]*\)", "", ueberschrift)  # Klammern sind Zusätze/Aliase
    teile = re.split(r"\s+und\s+|\s+\+\s+|\s+oder\s+|[:,/]", ueberschrift)
    return [re.sub(r"\s+\d+$", "", t.strip()) for t in teile if t.strip()]  # Versionsnummer weglassen


def erwaehnt(begriff, text):
    return any(re.search(r"(?<![\w+#])" + re.escape(b) + r"(?![\w+#])", text, flags=re.I)
               for b in [begriff] + ALIASE.get(begriff, []))


def schreibtipps(name, raw_body, sections):
    """Leitet Tipps zum Weiterschreiben aus Rohfassung und Rohmaterial ab."""
    woerter_raw = len(raw_body.split())
    woerter_roh = sum(len(b.split()) for _, b in sections)
    raw_ueberschriften = re.findall(r"^#+ (.+)$", raw_body, flags=re.M)
    analyse = [b for h, b in sections if h.startswith(("Analyse", "Detaillierte Analyse", "Best Practices"))]
    themen = [h for b in analyse for h in re.findall(r"^#{3,4} (.+)$", b, flags=re.M)]
    if name == "Fertige_Plattformen.md":
        # Die Technologien stehen hier unter den Kategorien eine Ebene tiefer.
        themen = [h for b in analyse for h in re.findall(r"^#### (.+)$", b, flags=re.M)]

    z = [TIPP_HINWEIS, "",
         f"**Stand:** Die Rohfassung hat {woerter_raw} Wörter, das Rohmaterial dazu {woerter_roh}. "
         "Die Recherche bietet also deutlich mehr Stoff, als der Artikel bisher nutzt."
         if woerter_roh > 3 * woerter_raw else
         f"**Stand:** Die Rohfassung hat {woerter_raw} Wörter, das Rohmaterial dazu {woerter_roh}."]
    if raw_ueberschriften:
        z.append("**Bisherige Gliederung des Autors:** " + ", ".join(f"„{h}“" for h in raw_ueberschriften) + ".")
    else:
        z.append("**Gliederung:** Die Rohfassung hat noch keine Zwischenüberschriften. "
                 "Eine Gliederung vor dem Fließtext erleichtert das Weiterschreiben.")

    if name in TECHNOLOGIE_KAPITEL and themen:
        begriffe = list(dict.fromkeys(n for t in themen for n in namen(t)))
        da = [b for b in begriffe if erwaehnt(b, raw_body)]
        fehlt = [b for b in begriffe if b not in da]
        if da:
            z.append("**Schon im Artikel genannt (jeweils ausbauen):** " + ", ".join(da) + ".")
        if fehlt:
            z.append("**In der Recherche behandelt, im Artikel noch nicht genannt:** " + ", ".join(fehlt) +
                     ". Entscheide, ob sie in den Artikel gehören oder bewusst fehlen sollen.")
    elif themen:
        z.append("**Themenblöcke der Recherche als mögliche Abschnitte:** " + "; ".join(themen) + ".")

    z += ["", "**Checkliste für jeden Abschnitt:**",
          "* Kernaussage in einem Satz am Anfang nennen.",
          "* Das Auswahlkriterium „läuft noch in 20 Jahren“ begründen: Abwärtskompatibilität, Lizenz, "
          "Verbreitung, statisch gebundene Programme.",
          "* Mindestens ein kleines, lauffähiges Beispiel mit Befehlen oder Code (unverändert prüfen).",
          "* Eigene Erfahrung und Begründung des Autors deutlich vom Recherchestoff trennen.",
          "* Für jede Tatsachenbehauptung die Quelle aus dem Rohmaterial mit URL angeben.",
          "* Mit einem kurzen Fazit oder einer Empfehlung schließen und auf verwandte Kapitel verweisen.",
          f"* Weiterführende Ideen stehen im [Ausblick](Ausblick.md)."]
    return "\n\n".join(z).replace("\n\n\n\n", "\n\n").replace("\n\n* ", "\n* ")


LEHR_HINWEIS = ("*KI-Lehrtext: Dieser Abschnitt wurde von einer KI aus dem Rohmaterial abgeleitet. "
                "Er stammt nicht vom Autor und ist ein Vorschlag.*")
LEHR_VORN = ["Lernziele"]  # direkt nach dem Autorentext
LEHR_HINTEN = ["Vergleich auf einen Blick", "Zusammenfassung", "Kontrollfragen"]  # vor den Schreibtipps
URL_RE = r"https?://[^\s)*,]+"


def urls_in(text):
    return {u.rstrip(".") for u in re.findall(URL_RE, text)}


def lehrtext(name):
    """Liest Proto/lehrtext/<name> als {Überschrift: Inhalt}. Jede URL muss im Rohmaterial stehen."""
    pfad = LEHR / name
    if not pfad.exists():
        return {}
    text = pfad.read_text(encoding="utf-8")
    fremd = urls_in(text) - urls_in((ROH / name).read_text(encoding="utf-8"))
    if fremd:
        sys.exit(f"Lehrtext {name}: Quellen nicht im Rohmaterial: {sorted(fremd)}")
    out = {}
    for p in re.split(r"^## ", text, flags=re.M)[1:]:
        head, _, body = p.partition("\n")
        out[head.strip()] = body.strip("\n")
    unbekannt = set(out) - set(LEHR_VORN + LEHR_HINTEN)
    if unbekannt:
        sys.exit(f"Lehrtext {name}: unbekannte Abschnitte: {sorted(unbekannt)}")
    return out


def werkzeugtabelle(sections):
    """Baut aus den Aufzählungen der Analyse (Werkzeuge.md) je Kategorie eine Übersichtstabelle."""
    out = []
    for head, body in sections:
        if not head.startswith("Detaillierte Analyse"):
            continue
        zeilen, eintrag = [], None
        for line in body.splitlines() + ["### "]:
            m = re.match(r"\* \*\*(.+?)(?: \((.*)\))?:\*\*", line)
            if line.startswith("### ") or m:
                if eintrag:
                    zeilen.append(eintrag)
                eintrag = None
            if line.startswith("### "):
                if zeilen:
                    out += ["| Werkzeug | Einordnung laut Recherche | Quelle |", "|---|---|---|"]
                    out += [f"| {n} | {e or '–'} | {'<' + q + '>' if q else '–'} |" for n, e, q in zeilen]
                    out.append("")
                zeilen = []
                if line[4:].strip():
                    out += [f"**{line[4:].strip()}**", ""]
            elif m:
                eintrag = [m.group(1).replace("|", "\\|"), (m.group(2) or "").replace("|", "\\|"), ""]
            if eintrag and not eintrag[2]:
                u = re.search(URL_RE, line)
                if u:
                    eintrag[2] = u.group(0).rstrip(".")
    return "\n".join(out).strip("\n")


def shift(body):
    """Überschriften eine Ebene tiefer setzen (### -> ####)."""
    return re.sub(r"^(#+) ", lambda m: "#" + m.group(1) + " ", body, flags=re.M)


def datei(name, title, content):
    (OUT / name).write_text(f"# {title}\n\n{HINWEIS}\n\n{content.strip()}\n\n{HINWEIS}\n",
                            encoding="utf-8")


grundprinzipien, ausblick, quellen, summary_kapitel = [], [], [], []

for name, kurz in KAPITEL:
    title, raw_body = raw_parts(name)
    sections = roh_sections(name)
    teile = ["## Kernaussagen des Autors", raw_body or "*Die Rohfassung enthält bisher nur die Überschrift.*"]
    lehr = lehrtext(name)
    if name == "Werkzeuge.md" and lehr:
        lehr.setdefault("Vergleich auf einen Blick", werkzeugtabelle(sections))
    for h in LEHR_VORN:
        if lehr.get(h):
            teile += [f"## {h}", LEHR_HINWEIS, lehr[h]]
    for i, (head, body) in enumerate(sections):
        if head.startswith("Weitere mögliche Themen"):
            ausblick.append((title, name, body))
            continue
        if i == 0 and name in GRUNDPRINZIP_AUS:
            grundprinzipien.append((kurz, head, body))
            teile.append(f"> Die allgemeinen Grundlagen zu diesem Thema stehen im Kapitel "
                         f"[Grundprinzipien langlebiger Software](Grundprinzipien.md).")
            continue
        if head.startswith("Alternative"):
            head = "Alternativen und ähnliche Software"
        teile += [f"## {head}", body]
    for h in LEHR_HINTEN:
        if lehr.get(h):
            teile += [f"## {h}", LEHR_HINWEIS, lehr[h]]
    teile += ["## Tipps zum Weiterschreiben", schreibtipps(name, raw_body, sections)]
    datei(name, title, "\n\n".join(teile))
    summary_kapitel.append((title, name))
    urls = sorted(set(re.findall(r"https?://[^\s)*,]+", (ROH / name).read_text(encoding="utf-8"))))
    quellen.append((title, [u.rstrip(".") for u in urls]))

# Grundprinzipien
gp = ["Dieses Kapitel fasst die themenübergreifenden Grundlagen aus der Recherche zusammen, "
      "die für CLI-Werkzeuge, Desktop-Anwendungen und Webframeworks gleichermaßen gelten."]
for kurz, head, body in grundprinzipien:
    gp += [f"## {kurz}: {head}", shift(body)]
datei("Grundprinzipien.md", "Grundprinzipien langlebiger Software", "\n\n".join(gp))

# Ausblick
ab = ["Sammlung aller in der Recherche vorgeschlagenen Vertiefungsthemen, geordnet nach Kapitel. "
      "Sie dienen als Kandidaten für künftige Rohfassungen in `RAW/`."]
for title, name, body in ausblick:
    body = re.sub(r"^Folgende .*?:\s*\n", "", body, flags=re.S | re.M, count=1)
    ab += [f"## Zu „{title}“", f"*Kapitel: [{title}]({name})*", body]
datei("Ausblick.md", "Ausblick: Weitere mögliche Themen", "\n\n".join(ab))

# Quellenverzeichnis
qv = ["Alle in der Recherche genannten Quellen, geordnet nach Kapitel (automatisch extrahiert)."]
for title, urls in quellen:
    qv += [f"## {title}", "\n".join(f"* <{u}>" for u in urls)]
datei("Quellen.md", "Quellenverzeichnis", "\n\n".join(qv))

# Vorwort (Autorentext unverändert)
vt, vb = raw_parts("Vorwort.md")
datei("Vorwort.md", vt, "## Kernaussagen des Autors\n\n" + vb)

# SUMMARY
lines = ["# Summary", "", "[Vorwort](Vorwort.md)", "",
         "# Grundlagen", "", "- [Grundprinzipien langlebiger Software](Grundprinzipien.md)", "",
         "# Dokumente erstellen", ""]
def eintrag(name):
    t = dict((n, t) for t, n in summary_kapitel)[name]
    return f"- [{t}]({name})"
lines += [eintrag("Dokument_erstellen_software.md"), eintrag("Markdown.md"), "", "# Programmieren für 20 Jahre", "",
          eintrag("CLI_Werkzeuge.md"), eintrag("Desktop.md"), eintrag("Webframework.md"), "",
          "# Arbeiten mit Sprachmodellen", "", eintrag("Sprachmodel.md"), eintrag("KI_AGENT.md"), "",
          "# Lernplattformen und Code-Ausführung", "", eintrag("Fertige_Plattformen.md"),
          eintrag("Werkzeuge.md"), "",
          "# Anhang", "", "- [Ausblick: Weitere mögliche Themen](Ausblick.md)",
          "- [Quellenverzeichnis](Quellen.md)", ""]
(OUT / "SUMMARY.md").write_text("\n".join(lines), encoding="utf-8")

(ROOT / "Proto" / "book.toml").write_text(
    '[book]\nauthors = ["Thorsten Klöhn"]\nlanguage = "de"\nsrc = "src"\n'
    'title = "Prototyp – Programmiersprachen Lernen"\n', encoding="utf-8")
print("fertig:", sorted(p.name for p in OUT.iterdir()))
