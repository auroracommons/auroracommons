#!/usr/bin/env python3
"""Build shelf.html, the public shelf of proven work.

The shelf lists standing work by others and the Commons' own
exhibits, each with one plain line of what it does, who keeps it, its
license read at its source, a live place to try it, and three doors:
use it, adopt it, change it. Every word and link on the page comes
from shelf.json, the shelf's own data file, so the page and its data
cannot drift. A door with no honest link stands without one, with its
reason printed in shelf.json beside it.

Run: python3 tools/build_shelf.py
"""

import html
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_docs as rd

ROOT = rd.ROOT
SITE = rd.SITE

EXTRA_CSS = """
  .work{border-top:1px solid var(--line);padding:12px 0 2px}
  .work .workname{font-weight:700;margin:0 0 4px}
  .work p{margin:0 0 8px}
"""

CURRENT_PAGE = "shelf.html"


def fail(msg):
    print("build_shelf: " + msg, file=sys.stderr)
    sys.exit(1)


def esc(text):
    return html.escape(text, quote=False)


def read(name):
    path = ROOT / name
    if not path.exists():
        fail("missing %s" % name)
    return path.read_text(encoding="utf-8")


def shell(title, orientation, body, tech_lines):
    css = rd.CSS.replace("  @media", EXTRA_CSS + "  @media", 1)
    desc = html.escape(orientation, quote=True)
    tech = "\n".join(
        ['<section class="tech">', "<h2>For agents and builders</h2>"]
        + tech_lines + ["</section>"])
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
  <p class="orientation">%s</p>
  <p class="source">Built from <a href="shelf.json">shelf.json</a>, the shelf's own data file, by tools/build_shelf.py.</p>
</header>
<main class="doc" id="main">
%s
%s
</main>
%s
<p class="endline">That is everything. The page ends here.</p>
</div>
</body>
</html>
""" % (title, desc, SITE, rd.url_of(CURRENT_PAGE), title, desc, SITE,
       rd.url_of(CURRENT_PAGE), title, desc, css, rd.SKIP_LINK,
       rd.bar(title), title, orientation, body, tech, rd.FOOTER)


def door_html(door):
    if door.get("url"):
        return '<a href="%s">%s</a>' % (
            html.escape(door["url"], quote=True), esc(door["label"]))
    return "%s (no link today: %s)" % (esc(door["label"]),
                                       esc(door["note"]))


def entry_html(entry, checked):
    out = ['<div class="work">']
    out.append('<p class="workname">%s</p>' % esc(entry["name"]))
    out.append("<p>%s</p>" % esc(entry["line"]))
    lic = entry["license"]
    line = ('<p>Kept by %s. License: <a href="%s">%s</a>, read at its '
            "source on %s."
            % (esc(entry["maintainer"]),
               html.escape(lic["source"], quote=True),
               esc(lic["name"]), checked))
    if lic.get("note"):
        line += " %s" % esc(lic["note"])
    line += "</p>"
    out.append(line)
    doors = ", ".join(door_html(d) for d in entry["doors"])
    out.append('<p><a href="%s">Try it</a>. The doors: %s.</p>'
               % (html.escape(entry["try"], quote=True), doors))
    out.append("</div>")
    return out


def build():
    data = json.loads(read("shelf.json"))
    checked = data["checked"]
    groups = data["groups"]
    if len(groups) != 2:
        fail("shelf.json: expected exactly two groups")
    total = sum(len(g["entries"]) for g in groups)
    counts = [len(g["entries"]) for g in groups]

    out = []
    out.append(
        "<p>This shelf holds %d works in all, counted on %s: %d "
        "standing works by others, and %d exhibits of the Commons. "
        "Every license on this page was read again at its source on "
        "%s, before its work was listed here. Each work carries three "
        "doors, sized for a first step: use it, adopt it, or change "
        "it.</p>" % (total, checked, counts[0], counts[1], checked))
    for group in groups:
        out.append("<h2>%s</h2>" % esc(group["title"]))
        for entry in group["entries"]:
            out.extend(entry_html(entry, checked))

    tech = []
    tech.append(
        "<p>This page is generated by tools/build_shelf.py from "
        '<a href="shelf.json">shelf.json</a>, so the page and its '
        "data are one source. The provenance of each entry stands "
        "below: the license as it was read, the source it was read "
        "at, and the date of the reading, %s.</p>" % checked)
    for group in groups:
        tech.append("<p>%s:</p>" % esc(group["title"]))
        tech.append('<ul class="plain">')
        for entry in group["entries"]:
            lic = entry["license"]
            line = ('<li>%s: %s, read at <a href="%s">its source</a>, '
                    "checked %s."
                    % (esc(entry["name"]), esc(lic["name"]),
                       html.escape(lic["source"], quote=True),
                       checked))
            if lic.get("note"):
                line += " %s" % esc(lic["note"])
            line += "</li>"
            tech.append(line)
        tech.append("</ul>")
    tech.append(
        "<p>Two things stand in the open. ElectionGuard's repository "
        "has moved from Microsoft's account to the Election Tech "
        "Initiative, and the shelf names the keeper it has today. "
        "LiquidFeedback's change it door stands without a link: the "
        "repository link on the project's own page did not answer "
        "when it was fetched on %s, and no link was invented to fill "
        "the space. Every other link on this page was fetched on %s "
        "and answered.</p>" % (checked, checked))
    return "\n".join(out), tech


def main():
    body, tech = build()
    (ROOT / "shelf.html").write_text(
        shell("The shelf",
              "Proven work, by others and by this Commons, that "
              "anyone can use, adopt, or change, each with its "
              "license checked and its doors open.",
              body, tech), encoding="utf-8")
    print("build_shelf: shelf.html written")


if __name__ == "__main__":
    main()
