#!/usr/bin/env python3
"""Build records.html, the public records page.

The page gathers, for each layer of the Ascent in order, what the
Commons' own record holds for that need, the public records held by
others that a person can use today, and what is missing or thin,
stated plainly. A last section holds curiosity and wants, which sit
above the needs map. Needs come first on purpose.

Every Commons record is composed here from the files that already
carry it: site.json for the acts and their proof sentences,
foundations.json for the studies, and shelf.json for the exhibits.
The records held by others, the gap lines, the story lines, and the
limits lines stand in records.json, each with its source. The counts
in each section's small visual are counted from that section's own
composed records, so the picture and the prose cannot drift.

Run: python3 tools/build_records.py
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
  .rec{border-top:1px solid var(--line);padding:12px 0 2px}
  .rec .recname{font-weight:700;margin:0 0 4px}
  .rec p{margin:0 0 8px}
  .kinds{margin:10px 0 4px}
  .kindrow{display:flex;align-items:center;gap:10px;margin:3px 0}
  .kindlabel{flex:0 0 11em}
  .kindbar{height:12px;background:var(--ink);min-width:2px}
  .kindcount{flex:0 0 auto}
"""

CURRENT_PAGE = "records.html"

# The filing of Foundations fields under the needs they serve first.
# Every field in foundations.json must appear exactly once, or the
# build fails rather than guess.
DOMAIN_LAYER = {
    "Poverty and material security": 0,
    "Food systems and agriculture": 0,
    "Housing and homelessness": 0,
    "Health and the body": 0,
    "Water and sanitation": 0,
    "Disability and inclusion": 0,
    "Pain": 0,
    "Aging": 0,
    "Energy access": 0,
    "Environment and climate adaptation": 0,
    "Mind and mental health": 1,
    "Sleep": 1,
    "Addiction and recovery": 1,
    "Grief and loss": 1,
    "Learning and education": 2,
    "Early childhood": 2,
    "Language and communication": 2,
    "Libraries": 2,
    "Play": 2,
    "Belonging and social connection": 3,
    "Cooperation and collective action": 3,
    "Migration and refuge": 3,
    "Public space": 3,
    "Truth and shared knowledge": 4,
    "Local news": 4,
    "Governance and democracy": 4,
    "Law and justice": 4,
    "Artificial intelligence and human computer interaction": 5,
    "Digital access": 5,
    "Work and livelihoods": 5,
    "Economics and incentives": 5,
    "Savings": 5,
    "Debt": 5,
    "Insurance": 5,
    "Repair": 5,
    "Craft and making": 5,
    "Meaning, values, and human flourishing": 6,
    "Music": 6,
}

# Which shelf exhibits stand in which layer section.
SHELF_OF_LAYER = {
    0: ["Ground"],
    1: ["Still"],
    2: ["Atlas"],
    3: ["Cohort"],
    4: ["Graph", "The Index"],
    5: ["Machine"],
    6: ["Lumen"],
}

KIND_LABEL = {
    "commons": "The Commons' own",
    "outside": "Held by others",
    "gap": "Missing or thin",
}


def fail(msg):
    print("build_records: " + msg, file=sys.stderr)
    sys.exit(1)


def esc(text):
    return html.escape(text, quote=False)


def read_json(name):
    path = ROOT / name
    if not path.exists():
        fail("missing %s" % name)
    return json.loads(path.read_text(encoding="utf-8"))


def shell(title, orientation, body, tech_lines):
    css = rd.CSS.replace("  @media", EXTRA_CSS + "  @media", 1)
    tech = "\n".join(
        ['<section class="tech">', "<h2>For agents and builders</h2>"]
        + tech_lines + ["</section>"])
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
<meta property="og:site_name" content="Topsoil Commons">
<meta property="og:title" content="%s">
<meta property="og:url" content="%s%s">
<meta property="og:image" content="https://topsoilcommons.github.io/topsoilcommons/assets/aurora-logo.png">
<meta property="og:image:width" content="1600">
<meta property="og:image:height" content="1600">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="%s">
<meta name="twitter:image" content="https://topsoilcommons.github.io/topsoilcommons/assets/aurora-logo.png">
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
  <p class="source">Built from <a href="records.json">records.json</a>, <a href="site.json">site.json</a>, <a href="foundations.json">foundations.json</a>, and <a href="shelf.json">shelf.json</a> by tools/build_records.py.</p>
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
""" % (title, title, SITE, CURRENT_PAGE, title, css, rd.SKIP_LINK,
       rd.bar(title), title, orientation, body, tech, rd.FOOTER)


def foundations_by_layer(studies):
    counts = {}
    fields = {}
    for paper in studies:
        domain = paper["domain"]
        if domain not in DOMAIN_LAYER:
            fail("foundations.json: field not filed under any layer: %s"
                 % domain)
        layer = DOMAIN_LAYER[domain]
        counts[domain] = counts.get(domain, 0) + 1
        fields.setdefault(layer, []).append(domain)
    present = set(p["domain"] for p in studies)
    for domain in present:
        if domain not in DOMAIN_LAYER:
            fail("foundations.json: field not filed: %s" % domain)
    return counts, fields


def layer_records(layer_no, act, studies, counts, fields, shelf_by_name):
    """Compose the Commons' own records for one layer."""
    records = []
    records.append({
        "kind": "commons",
        "name": act["act"],
        "line": act["proof"],
        "keeper": "Topsoil Commons",
        "source": act["see"],
    })
    domains = sorted(set(fields.get(layer_no, [])))
    n_studies = sum(counts[d] for d in domains)
    records.append({
        "kind": "commons",
        "name": "Foundations, the studies under this need",
        "line": ("Foundations holds %d studies in %d fields filed "
                 "under this need, each one opened at its source and "
                 "printed with its source beside it."
                 % (n_studies, len(domains))),
        "keeper": "Topsoil Commons",
        "source": SITE + "foundations.html",
    })
    for name in SHELF_OF_LAYER[layer_no]:
        entry = shelf_by_name[name]
        records.append({
            "kind": "commons",
            "name": "On the shelf: " + entry["name"],
            "line": entry["line"],
            "keeper": entry["maintainer"],
            "source": entry["try"],
        })
    return records


def thinness_gap(layer_no, counts, fields):
    domains = sorted(set(fields.get(layer_no, [])))
    single = [d for d in domains if counts[d] == 1]
    if not single:
        return None
    return {
        "kind": "gap",
        "name": "Thin in the studies",
        "line": ("Of the %d fields of study filed under this need in "
                 "Foundations, %d rest on one study each. One study "
                 "is a beginning, and the record counts it as one."
                 % (len(domains), len(single))),
        "keeper": "Topsoil Commons",
        "source": SITE + "foundations.html",
    }


def record_html(record, checked):
    out = ['<div class="rec">']
    out.append('<p class="recname">%s</p>' % esc(record["name"]))
    out.append("<p>%s</p>" % esc(record["line"]))
    if record["kind"] == "gap":
        out.append(
            '<p>Ground: <a href="%s">the record it stands in</a>, '
            "checked %s.</p>"
            % (html.escape(record["source"], quote=True), checked))
    else:
        out.append(
            '<p>Kept by %s. Source: <a href="%s">%s</a>, checked %s.</p>'
            % (esc(record["keeper"]),
               html.escape(record["source"], quote=True),
               esc(record["source"].replace("https://", "")), checked))
    out.append("</div>")
    return out


def kinds_visual(records, checked):
    tally = {}
    for record in records:
        tally[record["kind"]] = tally.get(record["kind"], 0) + 1
    biggest = max(tally.values())
    out = ['<div class="kinds">']
    for kind in ("commons", "outside", "gap"):
        if kind not in tally:
            continue
        width = int(round(100.0 * tally[kind] / biggest))
        out.append(
            '<div class="kindrow"><span class="kindlabel">%s</span>'
            '<span class="kindbar" style="width:%d%%"></span>'
            '<span class="kindcount">%d</span></div>'
            % (KIND_LABEL[kind], width, tally[kind]))
    out.append("</div>")
    out.append(
        "<p>Key: each bar counts the records of one kind in this "
        "section, counted from this section's own records on %s. "
        "The longest bar is the largest count in the section, and "
        "the rest are drawn to the same scale.</p>" % checked)
    return out, tally


def section_html(heading, subline, story, records, limits, checked):
    out = ["<h2>%s</h2>" % esc(heading)]
    if subline:
        out.append("<p>%s</p>" % esc(subline))
    out.append("<p>%s</p>" % esc(story))
    visual, _tally = kinds_visual(records, checked)
    out.extend(visual)
    for kind, sub in (("commons", "What the Commons holds"),
                      ("outside", "Held by others, open to anyone"),
                      ("gap", "Missing or thin")):
        group = [r for r in records if r["kind"] == kind]
        if not group:
            continue
        out.append("<h3>%s</h3>" % sub)
        for record in group:
            out.extend(record_html(record, checked))
    out.append("<p>%s</p>" % esc(limits))
    return out


def build():
    data = read_json("records.json")
    checked = data["checked"]
    site = read_json("site.json")
    studies = read_json("foundations.json")
    shelf = read_json("shelf.json")
    counts, fields = foundations_by_layer(studies)
    shelf_by_name = {}
    others_count = 0
    for group in shelf["groups"]:
        for entry in group["entries"]:
            shelf_by_name[entry["name"]] = entry
            if group["id"] == "others":
                others_count += 1
    acts = {a["layer"]: a for a in site["acts"]}
    layer_data = {l["layer"]: l for l in data["layers"]}
    if sorted(layer_data) != list(range(7)):
        fail("records.json: expected layers 0 to 6")

    totals = {"commons": 0, "outside": 0, "gap": 0}
    out = []
    out.append(
        "<p>Every figure on this page names its source and its "
        "limits. The records stand in the order of the needs they "
        "serve, needs first, and curiosity after, the way the needs "
        "map itself is built.</p>")

    sections = []
    for layer_no in range(7):
        act = acts[layer_no]
        spec = layer_data[layer_no]
        records = layer_records(layer_no, act, studies, counts,
                                fields, shelf_by_name)
        for entry in spec["outside"]:
            records.append(dict(entry, kind="outside"))
        for entry in spec["gaps"]:
            records.append(dict(entry, kind="gap"))
        thin = thinness_gap(layer_no, counts, fields)
        if thin:
            records.append(thin)
        for record in records:
            totals[record["kind"]] += 1
        need = act["need"]
        heading = need[0].upper() + need[1:]
        sections.extend(section_html(
            heading,
            "Layer %d of the Ascent. %s" % (layer_no, act["unlocks"]),
            spec["story"], records, spec["limits"], checked))

    # Curiosity and wants, above the map.
    curiosity = data["curiosity"]
    crecords = [
        {"kind": "commons", "name": "The long arc",
         "line": ("Ten beginnings of farming in ten places, told as "
                  "ranges of years with the doubt printed beside "
                  "them, and six turns from stored food to this "
                  "Commons. Wonder with its ground showing."),
         "keeper": "Topsoil Commons",
         "source": SITE + "record.html"},
        {"kind": "commons", "name": "Atlas, one claim in full",
         "line": acts[2]["proof"],
         "keeper": "Topsoil Commons",
         "source": acts[2]["see"]},
        {"kind": "outside", "name": "The shelf of standing work",
         "line": ("The shelf holds %d standing works by others, "
                  "each one proven work that anyone can use, adopt, "
                  "or change, with its license read at its source."
                  % others_count),
         "keeper": "Topsoil Commons",
         "source": SITE + "shelf.html"},
    ]
    for record in crecords:
        totals[record["kind"]] += 1
    sections.extend(section_html(
        "Above the needs: curiosity and wants", None,
        curiosity["story"], crecords, curiosity["limits"], checked))

    total = sum(totals.values())
    out.append(
        "<p>This page holds %d records in all, counted on %s: %d "
        "records of the Commons' own, %d records held by others and "
        "open to anyone, and %d records of what is missing or thin. "
        "They stand in eight sections: one for each of the seven "
        "layers of need, and one for curiosity and wants, which sit "
        "above the needs in the Commons' own map.</p>"
        % (total, checked, totals["commons"], totals["outside"],
           totals["gap"]))
    out.extend(sections)

    tech = []
    tech.append(
        "<p>This page is generated by tools/build_records.py from "
        "records.json, site.json, foundations.json, and shelf.json, "
        "so the page and its data are one source. The Commons' own "
        "records are composed at build time from those files: the "
        "acts and their proof sentences from site.json, the study "
        "counts from foundations.json, and the shelf exhibits from "
        "shelf.json. Nothing on the surface is typed by hand where a "
        "file already carries it.</p>")
    tech.append(
        "<p>Foundations fields are filed under the need each study "
        "serves first. The filing, with the counts it produced on "
        "%s:</p>" % checked)
    tech.append('<ul class="plain">')
    for layer_no in range(7):
        domains = sorted(set(fields.get(layer_no, [])))
        n_studies = sum(counts[d] for d in domains)
        parts = ", ".join("%s (%d)" % (d, counts[d]) for d in domains)
        tech.append("<li>Layer %d: %d studies in %d fields. %s.</li>"
                    % (layer_no, n_studies, len(domains), parts))
    tech.append("</ul>")
    tech.append(
        "<p>Every outside source on this page was opened on %s, "
        "before its record was written. One source tried for this "
        "page did not answer on %s and was left out: the Internet "
        "Sacred Text Archive, at sacred-texts.com. No link was "
        "invented to fill its place. The Bureau of Labor Statistics "
        "page was read in full the same day; it turns away the "
        "scripted fetch used to check links, and its record says so "
        "on the surface.</p>" % (checked, checked))
    return "\n".join(out), tech


def main():
    body, tech = build()
    (ROOT / "records.html").write_text(
        shell("Public records",
              "What stands in the open for each need a person has: "
              "what the Commons holds, what others hold open for "
              "anyone, and what is missing, each with its source "
              "and its limits.",
              body, tech), encoding="utf-8")
    print("build_records: records.html written")


if __name__ == "__main__":
    main()
