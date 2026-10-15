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
    ("INTERACTIONS.md", "interactions.html"),
]

BLOB = "https://github.com/auroracommons/auroracommons/blob/main/"
SITE = "https://auroracommons.github.io/auroracommons/"

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


def render(md_text):
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
                tag = "h2" if level <= 2 else "h3"
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
    return title, "\n".join(out)


CSS = """  :root{
    --bg:#fbfaf7; --ink:#1b1e23; --soft:#5a6068; --line:#e4e0d6;
    --accent:#1b1e23; --rub:#9e2b25;
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    line-height:1.5;-webkit-font-smoothing:antialiased}
  .wrap{max-width:980px;margin:0 auto;padding:0 20px}
  header{padding:28px 0 4px}
  h1{font-size:44px;letter-spacing:-1.2px;margin:14px 0 8px;font-weight:800;line-height:1.12}
  .source{font-size:13px;color:var(--soft);margin:0 0 10px}
  .source a{color:var(--accent);text-decoration:none;font-weight:600}
  .source a:hover{text-decoration:underline}
  .doc{padding:18px 0 4px;max-width:760px}
  .doc p{font-size:16px;margin:0 0 14px}
  .doc h2{font-size:25px;letter-spacing:-.5px;margin:34px 0 10px;font-weight:800}
  .doc h3{font-size:19px;letter-spacing:-.3px;margin:26px 0 8px;font-weight:800}
  .doc ul,.doc ol{font-size:16px;margin:0 0 14px;padding-left:24px}
  .doc li{margin:0 0 6px}
  .doc a{color:var(--accent);font-weight:600}
  .doc table{border-collapse:collapse;width:100%;font-size:15px;margin:0 0 16px}
  .doc th,.doc td{border-top:1px solid var(--line);padding:9px 12px 9px 0;text-align:left;vertical-align:top}
  .doc thead th{border-top:0}
  .doc code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.92em}
  .doc blockquote{margin:0 0 14px;padding-left:16px;border-left:3px solid var(--line)}
  footer{padding:54px 0 62px;margin-top:46px;border-top:1px solid var(--line);
    color:var(--soft);font-size:14px}
  footer a{color:var(--accent);text-decoration:none;font-weight:600}
  .endline{text-align:center;font-size:15px;color:var(--ink);margin:0;padding:0 0 54px}
  .commons-bar{display:flex;flex-wrap:wrap;gap:4px 18px;align-items:baseline;max-width:980px;margin:0 auto;padding:10px 20px 8px;font-size:14px;border-bottom:1px solid var(--line)}
  .commons-bar .brand{font-weight:800;color:var(--ink);text-decoration:none;margin-right:4px}
  .commons-bar a{color:var(--ink);text-decoration:none}
  .commons-bar a:hover{text-decoration:underline}
  .commons-bar .current{font-weight:700}
  @media (max-width:560px){h1{font-size:32px}}"""

BAR_LINKS = [
    ("Ground", "https://auroracommons.github.io/ground/"),
    ("Still", "https://auroracommons.github.io/still/"),
    ("Atlas", "https://auroracommons.github.io/atlas/"),
    ("Cohort", "https://auroracommons.github.io/cohort/"),
    ("Graph", "https://auroracommons.github.io/graph/"),
    ("Machine", "https://auroracommons.github.io/machine/"),
    ("Lumen", "https://auroracommons.github.io/lumen/"),
]


def page(md_name, page_name, title, body):
    short = title if title else md_name
    bar = ['<nav class="commons-bar" aria-label="Aurora Commons sites">',
           '  <a class="brand" href="%s">Aurora Commons</a>' % SITE,
           '  <span class="current" aria-current="page">%s</span>'
           % html.escape(short)]
    bar += ['  <a href="%s">%s</a>' % (url, name) for name, url in BAR_LINKS]
    bar.append("</nav>")
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="theme-color" content="#fbfaf7">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Aurora Commons">
<meta property="og:title" content="%s">
<meta property="og:url" content="%s%s">
<meta property="og:image" content="https://auroracommons.github.io/auroracommons/assets/aurora-logo.png">
<meta property="og:image:width" content="1600">
<meta property="og:image:height" content="1600">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="%s">
<meta name="twitter:image" content="https://auroracommons.github.io/auroracommons/assets/aurora-logo.png">
<style>
%s
</style>
</head>
<body>
%s
<div class="wrap">
<header>
  <h1>%s</h1>
  <p class="source">Source: %s, kept on <a href="%s%s">GitHub</a>.</p>
</header>
<main class="doc">
%s
</main>
<footer>
  <p>One rule: raise the floor beneath everyone.</p>
  <p>Advised by Groundskeeper.</p>
  <p><a href="https://www.linkedin.com/company/aurora-commons-io/">Aurora Commons on LinkedIn</a></p>
</footer>
<p class="endline">That is everything. The page ends here.</p>
</div>
</body>
</html>
""" % (html.escape(short), html.escape(short), SITE, page_name,
       html.escape(short), CSS, "\n".join(bar), html.escape(short),
       md_name, BLOB, md_name, body)


def main():
    for md_name, page_name in DOCS:
        source = ROOT / md_name
        if not source.exists():
            print("render_docs: missing %s" % md_name, file=sys.stderr)
            sys.exit(1)
        title, body = render(source.read_text(encoding="utf-8"))
        if not title:
            print("render_docs: %s has no title heading" % md_name,
                  file=sys.stderr)
            sys.exit(1)
        (ROOT / page_name).write_text(
            page(md_name, page_name, title, body), encoding="utf-8")
        print("render_docs: %s -> %s" % (md_name, page_name))


if __name__ == "__main__":
    main()
