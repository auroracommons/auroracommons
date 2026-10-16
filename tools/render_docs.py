#!/usr/bin/env python3
"""Render the record documents as pages on this site.

Choice of tool: a small renderer written for this repo in the Python
standard library. No markdown package and no pandoc is installed on the
build machine, and the record documents use a small plain subset of
markdown (headings, paragraphs, lists, one table form, bold, code, and
links), so a standard library renderer covers the whole set and adds no
dependency a future builder must install.

The markdown files stay the single source. Each page here is a build
product of its markdown file: run this script after a document changes
and commit the pages it writes. Links between the documents in this set
are rewritten to the matching page address, so a reader moving through
the record stays on the site. Each page carries one small source tag
under its title naming the markdown file kept on GitHub.

Human surface split: each page shows plain content first. A whole block
moves to a closing section headed "For agents and builders" when the
block is technical apparatus: it contains a code span, a hash string of
16 or more hex characters, or it is a short pointer line whose whole
content is a file name used as prose (a word ending in .md, .json,
.py, .js, or .ts). A longer block that mixes plain prose with one such
file reference stays on the surface when moving it would break the
document's sense, and the script prints one line for every such
judgment. The progress log is dense with short commit ids throughout,
so it uses a rendition instead: a short plain summary on the surface,
with the newest entry's date and heading read from the file itself,
and the whole document complete underneath. Any other document whose
split would leave fewer than two blocks on the surface falls back to
the same rendition handling.

The script also builds record.html, one page carrying the whole
written record, section by section, under the same split rules.

Run: python3 tools/render_docs.py
"""

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DOCS = [
    ("PROGRESS.md", "progress.html"),
    ("ECOSYSTEM.md", "ecosystem.html"),
    ("NEEDS.md", "needs.html"),
    ("DEMOCRACY.md", "democracy.html"),
    ("PARTICIPATION.md", "participation.html"),
    ("REGISTRY.md", "registry.html"),
    ("OPEN_TABLE.md", "open-table.html"),
    ("LEDGER.md", "ledger.html"),
    ("INTENTIONS.md", "intentions.html"),
    ("FUNDS.md", "funds.html"),
    ("FUNDS_LEDGER.md", "funds-ledger.html"),
    ("INTERACTIONS.md", "interactions.html"),
]

# The whole written record on one page, in this order: the markdown
# file, the plain name shown to readers, and the section anchor.
RECORD_ORDER = [
    ("TIMELINE.md", "The long arc", "record-timeline"),
    ("ECOSYSTEM.md", "The charter", "record-ecosystem"),
    ("NEEDS.md", "The needs map", "record-needs"),
    ("DEMOCRACY.md", "Democracy", "record-democracy"),
    ("PARTICIPATION.md", "Participation", "record-participation"),
    ("REGISTRY.md", "The registry", "record-registry"),
    ("OPEN_TABLE.md", "The open table", "record-open-table"),
    ("LEDGER.md", "The ledger", "record-ledger"),
    ("INTENTIONS.md", "Intentions", "record-intentions"),
    ("PROGRESS.md", "The progress log", "record-progress"),
    ("INTERACTIONS.md", "Interactions", "record-interactions"),
    ("FUNDS.md", "Funds", "record-funds"),
    ("FUNDS_LEDGER.md", "The funds ledger", "record-funds-ledger"),
]

BLOB = "https://github.com/topsoilcommons/topsoilcommons/blob/main/"
SITE = "https://topsoilcommons.org/"

ORIENTATION = ("Part of the Record: the written record of Topsoil "
               "Commons, on one page each.")

# One plain sentence per document, used as the page description in the
# head (meta description, og:description, twitter:description). Keyed
# by markdown file name, like DOCS.
DESCRIPTIONS = {
    "PROGRESS.md": "The public progress log of Topsoil Commons, with "
                   "what was done, what the proof shows, what broke, "
                   "and what comes next.",
    "ECOSYSTEM.md": "The charter of Topsoil Commons, an open source "
                    "ecosystem of free basic tools built around "
                    "human needs.",
    "NEEDS.md": "The Ascent, a map of human needs in the order they "
                "hold each other up, and the work that serves each "
                "layer.",
    "DEMOCRACY.md": "How Topsoil Commons makes decisions, with one "
                    "person and one voice, under its one rule.",
    "PARTICIPATION.md": "How people take part in Topsoil Commons, "
                        "with the tiers of involvement and the rules "
                        "for counting them.",
    "REGISTRY.md": "The Commons Registry, a public map of every "
                   "person and group in Topsoil Commons and what "
                   "they serve.",
    "OPEN_TABLE.md": "The Open Table, the three doors anyone can use "
                     "to contribute to Topsoil Commons.",
    "LEDGER.md": "The Ledger, a public record of verified work in "
                 "Topsoil Commons, with the evidence for each entry.",
    "INTENTIONS.md": "The stated intentions of Topsoil Commons, "
                     "written in public so anyone can hold the work "
                     "to them.",
    "FUNDS.md": "How money would move in Topsoil Commons, stated in "
                "the open before any money moves.",
    "FUNDS_LEDGER.md": "The funds ledger, a public record of every "
                       "amount Topsoil Commons receives and spends.",
    "INTERACTIONS.md": "The public log of interactions with Topsoil "
                       "Commons, with each submission and its result.",
}

RECORD_DESCRIPTION = ("The whole written record of Topsoil Commons "
                      "on one page, section by section.")

PAGE_OF = dict(DOCS)
# Any link target naming one of these files becomes its page address.
TARGETS = {}
for md_name, page_name in DOCS:
    TARGETS[md_name] = page_name
    TARGETS[BLOB + md_name] = page_name


def rewrite_url(url):
    base = url.split("#", 1)[0]
    frag = ("#" + url.split("#", 1)[1]) if "#" in url else ""
    if base in TARGETS:
        return TARGETS[base] + frag
    return url


def inline(text):
    # Code spans first, held aside so their text is never formatted.
    codes = []

    def hold(match):
        codes.append(match.group(1))
        return "\x00%d\x00" % (len(codes) - 1)

    text = re.sub(r"`([^`]+)`", hold, text)
    text = html.escape(text, quote=False)

    def link(match):
        label, url = match.group(1), match.group(2)
        return '<a href="%s">%s</a>' % (
            html.escape(rewrite_url(url), quote=True), label)

    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", text)

    def restore(match):
        return "<code>%s</code>" % html.escape(
            codes[int(match.group(1))], quote=False)

    return re.sub(r"\x00(\d+)\x00", restore, text)


def is_table_row(line):
    return line.strip().startswith("|") and line.strip().endswith("|")


def split_row(line):
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def render_blocks(md_text, shift=0):
    """Render markdown to a list of HTML blocks.

    shift demotes every heading by that many levels, so a document can
    sit inside a section of a larger page (record.html) and keep the
    heading order sound.
    """
    lines = md_text.split("\n")
    out = []
    title = None
    i = 0
    para = []

    def flush_para():
        if para:
            out.append("<p>%s</p>" % inline(" ".join(para)))
            del para[:]

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        heading = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if heading:
            flush_para()
            level = len(heading.group(1))
            text = heading.group(2).strip()
            if title is None and level == 1:
                title = text
            else:
                tag = "h%d" % min(6, (2 if level <= 2 else 3) + shift)
                out.append("<%s>%s</%s>" % (tag, inline(text), tag))
            i += 1
            continue
        if is_table_row(line) and i + 1 < len(lines) and re.match(
                r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            flush_para()
            head = split_row(line)
            i += 2
            body = []
            while i < len(lines) and is_table_row(lines[i]):
                body.append(split_row(lines[i]))
                i += 1
            parts = ["<table>", "<thead><tr>"]
            parts += ["<th>%s</th>" % inline(c) for c in head]
            parts.append("</tr></thead>")
            parts.append("<tbody>")
            for row in body:
                parts.append("<tr>" + "".join(
                    "<td>%s</td>" % inline(c) for c in row) + "</tr>")
            parts.append("</tbody>")
            parts.append("</table>")
            out.append("\n".join(parts))
            continue
        if re.match(r"^\s*([-*])\s+", line):
            flush_para()
            items = []
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append(re.sub(r"^\s*[-*]\s+", "", lines[i]).strip())
                i += 1
            out.append("<ul>\n" + "\n".join(
                "<li>%s</li>" % inline(it) for it in items) + "\n</ul>")
            continue
        if re.match(r"^\s*\d+[.)]\s+", line):
            flush_para()
            items = []
            while i < len(lines) and re.match(r"^\s*\d+[.)]\s+", lines[i]):
                items.append(
                    re.sub(r"^\s*\d+[.)]\s+", "", lines[i]).strip())
                i += 1
            out.append("<ol>\n" + "\n".join(
                "<li>%s</li>" % inline(it) for it in items) + "\n</ol>")
            continue
        if stripped.startswith(">"):
            flush_para()
            quote = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip().lstrip(">").strip())
                i += 1
            out.append("<blockquote><p>%s</p></blockquote>"
                       % inline(" ".join(quote)))
            continue
        if re.match(r"^\s*(-{3,}|\*{3,})\s*$", line):
            flush_para()
            out.append("<hr>")
            i += 1
            continue
        if stripped == "":
            flush_para()
            i += 1
            continue
        para.append(stripped)
        i += 1
    flush_para()
    return title, out


def render(md_text):
    title, blocks = render_blocks(md_text)
    return title, "\n".join(blocks)


FILE_TOKEN = re.compile(r"\b[\w-]+\.(?:md|json|py|js|ts)\b")
HEX_LONG = re.compile(r"\b[0-9a-f]{16,}\b")


def block_text(block):
    return html.unescape(re.sub(r"<[^>]+>", " ", block))


def split_blocks(blocks):
    """Split rendered blocks into surface blocks and apparatus blocks.

    Returns (surface, apparatus, notes). Relative order is preserved
    inside each list, and no block is reworded: relocation only.
    """
    surface = []
    apparatus = []
    notes = []
    for idx, block in enumerate(blocks):
        if block.startswith("<h"):
            surface.append(block)
            continue
        text = block_text(block)
        words = text.split()
        files = FILE_TOKEN.findall(text)
        if "<code>" in block:
            apparatus.append(block)
            notes.append("block %d moved underneath: it contains a "
                         "code span" % idx)
        elif HEX_LONG.search(text):
            apparatus.append(block)
            notes.append("block %d moved underneath: it contains a "
                         "hash string of 16 or more hex characters" % idx)
        elif files and len(words) <= 14:
            apparatus.append(block)
            notes.append("block %d moved underneath: a short pointer "
                         "line whose whole content is the file "
                         "reference %s" % (idx, files[0]))
        elif files:
            surface.append(block)
            notes.append("block %d kept on the surface: plain prose "
                         "that mixes one file reference (%s) with "
                         "human content, and moving it would break "
                         "the document's sense" % (idx, files[0]))
        else:
            surface.append(block)
    return surface, apparatus, notes


def newest_entry(md_text):
    """The date and heading of the newest progress entry, from the file.

    Entries are headed with a level two heading of the form
    "October 15, 2026: some heading", newest first.
    """
    for line in md_text.split("\n"):
        match = re.match(r"^##\s+(.*)$", line.strip())
        if match:
            heading = match.group(1).strip()
            if ": " in heading:
                date, rest = heading.split(": ", 1)
                return date.strip(), rest.strip()
            return "", heading
    return "", ""


def rendition_blocks(md_name, md_text, blocks):
    """The plain surface used when a document is shown by rendition."""
    if md_name == "PROGRESS.md":
        date, heading = newest_entry(md_text)
        out = ["<p>This page is the progress log: the public record of "
               "the work, what was done, what the proof shows, what "
               "broke, and what comes next, updated every work session "
               "with the newest entry first.</p>"]
        if date and heading:
            out.append("<p>The newest entry is dated %s, and its "
                       "heading is: %s.</p>" % (
                           html.escape(date, quote=False),
                           html.escape(heading, quote=False)))
        elif heading:
            out.append("<p>The newest entry is headed: %s.</p>"
                       % html.escape(heading, quote=False))
        out.append("<p>The full log stands underneath, word for "
                   "word.</p>")
        return out
    # Any other document: one plain line taken from its own opening,
    # the first paragraph of the document itself.
    for block in blocks:
        if block.startswith("<p>"):
            text = re.sub(r"\s+", " ", block_text(block)).strip()
            return ["<p>%s</p>" % html.escape(text, quote=False)]
    return []


def surface_and_tech(md_name, md_text, shift=0):
    """Return (title, handling, surface blocks, tech blocks, notes)."""
    title, blocks = render_blocks(md_text, shift=shift)
    if md_name == "PROGRESS.md":
        return (title, "rendition",
                rendition_blocks(md_name, md_text, blocks), blocks,
                ["the progress log is dense with short commit ids and "
                 "file references throughout, so the whole document "
                 "stands underneath a plain rendition"])
    surface, apparatus, notes = split_blocks(blocks)
    if len(surface) < 2:
        return (title, "rendition (fallback: the split would leave "
                "fewer than two blocks on the surface)",
                rendition_blocks(md_name, md_text, blocks), blocks,
                notes)
    return title, "split", surface, apparatus, notes


def tech_section(md_name, tech_blocks, level=2):
    tag = "h%d" % level
    parts = ['<section class="tech">',
             "<%s>For agents and builders</%s>" % (tag, tag),
             '<p><a href="%s%s">The full text and source of this '
             'document, kept on GitHub</a>.</p>' % (BLOB, md_name)]
    parts += tech_blocks
    parts.append("</section>")
    return "\n".join(parts)


CSS = """  :root{
    --bg:#fbfaf7; --ink:#1b1e23; --soft:#5a6068; --line:#e4e0d6;
    --accent:#1b1e23; --rub:#9e2b25;
  }
  header{padding:28px 0 4px}
  h1{font-size:44px;letter-spacing:-1.2px;margin:14px 0 8px;font-weight:800;line-height:1.12}
  .source{font-size:13px;color:var(--soft);margin:0 0 10px}
  .source a{color:var(--accent);text-decoration:none;font-weight:600}
  .source a:hover{text-decoration:underline}
  .orientation{font-size:15px;margin:0 0 4px}
  .doc{padding:18px 0 4px;max-width:760px}
  .doc p{font-size:16px;margin:0 0 14px}
  .doc h2{font-size:25px;letter-spacing:-.5px;margin:34px 0 10px;font-weight:800}
  .doc h3{font-size:19px;letter-spacing:-.3px;margin:26px 0 8px;font-weight:800}
  .doc h4{font-size:16px;margin:22px 0 8px;font-weight:800}
  .doc ul,.doc ol{font-size:16px;margin:0 0 14px;padding-left:24px}
  .doc li{margin:0 0 6px}
  .doc a{color:var(--accent);font-weight:600}
  .doc table{border-collapse:collapse;width:100%;font-size:15px;margin:0 0 16px}
  .doc th,.doc td{border-top:1px solid var(--line);padding:9px 12px 9px 0;text-align:left;vertical-align:top}
  .doc thead th{border-top:0}
  .doc code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.92em}
  .doc blockquote{margin:0 0 14px;padding-left:16px;border-left:3px solid var(--line)}
  .tech{border-top:1px solid var(--line);margin-top:36px;padding-top:4px}
  .contents{font-size:16px;margin:0 0 14px;padding-left:24px}
  .contents li{margin:0 0 6px}
  section.record-doc{border-top:1px solid var(--line);margin-top:36px;padding-top:4px}
  footer{padding:54px 0 62px;margin-top:46px;
    color:var(--soft);font-size:14px}
  footer a{color:var(--accent);text-decoration:none;font-weight:600}
  .endline{margin:0;padding:0 0 54px}
  @media (max-width:560px){h1{font-size:32px}}"""

BAR_LINKS = [
    ("Ground", "https://topsoilcommons.github.io/ground/"),
    ("Still", "https://topsoilcommons.github.io/still/"),
    ("Atlas", "https://topsoilcommons.github.io/atlas/"),
    ("Cohort", "https://topsoilcommons.github.io/cohort/"),
    ("Graph", "https://topsoilcommons.github.io/graph/"),
    ("Machine", "https://topsoilcommons.github.io/machine/"),
    ("Lumen", "https://topsoilcommons.github.io/lumen/"),
]


def bar(current=None):
    lines = ['<nav class="commons-bar" aria-label="Topsoil Commons sites">',
             '  <a class="brand" href="%s"><svg class="bar-mark" viewBox="0 0 24 24" width="17" height="17" aria-hidden="true" focusable="false" style="flex:none;align-self:center;margin-right:7px"><g fill="currentColor"><rect x="4" y="2.5" width="16" height="2"/><rect x="4" y="5.5" width="16" height="2"/><rect x="4" y="8.5" width="16" height="2"/><rect x="4" y="11.5" width="4.5" height="8"/><rect x="15.5" y="11.5" width="4.5" height="8"/><rect x="2" y="20.5" width="20" height="2.2"/></g></svg>Topsoil Commons</a>' % SITE]
    if current:
        lines.append('  <span class="current" aria-current="page">%s '
                     '(you are here)</span>' % html.escape(current))
    lines.append('  <a href="%sfoundations.html">Foundations</a>' % SITE)
    lines += ['  <a href="%s">%s</a>' % (url, name)
              for name, url in BAR_LINKS]
    lines.append("</nav>")
    return "\n".join(lines)


SKIP_LINK = '<a class="skip" href="#main">Skip to the content</a>'

FOOTER = """<footer>
  <p>One rule: raise the floor beneath everyone.</p>
  <p>Advised by Groundskeeper.</p>
  <p><a href="https://www.linkedin.com/company/topsoil-commons/">Topsoil Commons on LinkedIn</a></p>
</footer>"""


def page(md_name, page_name, title, body):
    short = title if title else md_name
    desc = html.escape(DESCRIPTIONS[md_name], quote=True)
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="%s%s">
<meta name="theme-color" content="#fbfaf7">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Topsoil Commons">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:url" content="%s%s">
<meta property="og:image" content="https://topsoilcommons.org/assets/aurora-logo.png">
<meta property="og:image:width" content="1600">
<meta property="og:image:height" content="1600">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="%s">
<meta name="twitter:description" content="%s">
<meta name="twitter:image" content="https://topsoilcommons.org/assets/aurora-logo.png">
<link rel="stylesheet" href="assets/commons.css">
<style>
%s
</style>
</head>
<body>
%s
%s
<div class="wrap">
<header>
  <h1>%s</h1>
  <p class="source">Source: %s, kept on <a href="%s%s">GitHub</a>.</p>
  <p class="orientation">%s</p>
</header>
<main class="doc" id="main">
%s
</main>
%s
<p class="endline">That is everything. The page ends here.</p>
</div>
</body>
</html>
""" % (html.escape(short), desc, SITE, page_name,
       html.escape(short), desc, SITE, page_name,
       html.escape(short), desc, CSS, SKIP_LINK, bar(short),
       html.escape(short), md_name, BLOB, md_name, ORIENTATION, body,
       FOOTER)


def ecosystem_opening():
    """Sentences copied word for word from ECOSYSTEM.md itself.

    The first sentence of the destination paragraph, and the aim
    sentence from the complete system section, both read from the file
    at build time.
    """
    text = (ROOT / "ECOSYSTEM.md").read_text(encoding="utf-8")
    lines = text.split("\n")
    destination = ""
    for i, line in enumerate(lines):
        if line.strip() == "## The destination":
            para = []
            for follow in lines[i + 1:]:
                if follow.strip() == "":
                    if para:
                        break
                    continue
                para.append(follow.strip())
            destination = " ".join(para)
            break
    first = destination[:destination.find(". ") + 1] if ". " in \
        destination else destination
    aim = ""
    match = re.search(r"The aim is [^.]*\.", text)
    if match:
        aim = match.group(0)
    return [s for s in (first, aim) if s]


def record_page(sections):
    opening = "\n".join("<p>%s</p>" % html.escape(s, quote=False)
                        for s in ecosystem_opening())
    contents = "\n".join(
        '      <li><a href="#%s">%s</a></li>' % (slug, name)
        for _md, name, slug in RECORD_ORDER)
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Record</title>
<meta name="description" content="%s">
<link rel="canonical" href="%srecord.html">
<meta name="theme-color" content="#fbfaf7">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Topsoil Commons">
<meta property="og:title" content="The Record">
<meta property="og:description" content="%s">
<meta property="og:url" content="%srecord.html">
<meta property="og:image" content="https://topsoilcommons.org/assets/aurora-logo.png">
<meta property="og:image:width" content="1600">
<meta property="og:image:height" content="1600">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="The Record">
<meta name="twitter:description" content="%s">
<meta name="twitter:image" content="https://topsoilcommons.org/assets/aurora-logo.png">
<link rel="stylesheet" href="assets/commons.css">
<style>
%s
</style>
</head>
<body>
%s
%s
<div class="wrap">
<header>
  <h1 id="top">The Record</h1>
</header>
<main class="doc" id="main">
%s
<p>Raise the floor beneath everyone.</p>
<h2>Contents</h2>
<nav aria-label="Contents of the record">
  <ul class="contents">
%s
  </ul>
</nav>
%s
</main>
%s
<p class="endline">That is everything. The page ends here.</p>
</div>
</body>
</html>
""" % (html.escape(RECORD_DESCRIPTION, quote=True), SITE,
       html.escape(RECORD_DESCRIPTION, quote=True), SITE,
       html.escape(RECORD_DESCRIPTION, quote=True), CSS, SKIP_LINK,
       bar("The Record"), opening, contents,
       "\n".join(sections), FOOTER)


def main():
    for md_name, page_name in DOCS:
        source = ROOT / md_name
        if not source.exists():
            print("render_docs: missing %s" % md_name, file=sys.stderr)
            sys.exit(1)
        md_text = source.read_text(encoding="utf-8")
        title, handling, surface, tech, notes = surface_and_tech(
            md_name, md_text)
        if not title:
            print("render_docs: %s has no title heading" % md_name,
                  file=sys.stderr)
            sys.exit(1)
        body = "\n".join(surface + [tech_section(md_name, tech)])
        (ROOT / page_name).write_text(
            page(md_name, page_name, title, body), encoding="utf-8")
        print("render_docs: %s -> %s [%s]" % (md_name, page_name,
                                              handling))
        for note in notes:
            print("render_docs:   %s: %s" % (md_name, note))

    sections = []
    for md_name, plain_name, slug in RECORD_ORDER:
        source = ROOT / md_name
        if not source.exists():
            print("render_docs: missing %s" % md_name, file=sys.stderr)
            sys.exit(1)
        md_text = source.read_text(encoding="utf-8")
        _title, handling, surface, tech, notes = surface_and_tech(
            md_name, md_text, shift=1)
        parts = ['<section class="record-doc" id="%s">' % slug,
                 "<h2>%s</h2>" % plain_name,
                 '<p class="source">Source: %s, kept on '
                 '<a href="%s%s">GitHub</a>.</p>' % (md_name, BLOB,
                                                     md_name)]
        parts += surface
        parts.append(tech_section(md_name, tech, level=3))
        parts.append('<p><a href="#top">Back to the top</a></p>')
        parts.append("</section>")
        sections.append("\n".join(parts))
        print("render_docs: record.html section %s [%s]" % (md_name,
                                                            handling))
        for note in notes:
            print("render_docs:   record %s: %s" % (md_name, note))
    (ROOT / "record.html").write_text(record_page(sections),
                                      encoding="utf-8")
    print("render_docs: record.html written")


if __name__ == "__main__":
    main()
