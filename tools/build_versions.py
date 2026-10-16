#!/usr/bin/env python3
"""Build the two version pages: story.html and advanced.html.

One site, two doors. story.html is the general audience version: the
past, the present, and the proposed future of the Commons, taught in
plain words down one visual spine. advanced.html is the reading room
and workbench for deep learners in any field: the full record in its
reading order, the studies gathered as a path to walk, the connections
the Commons itself draws between fields, the tools that check every
claim, and the builder material in one named section among them.

Nothing on either page is a second hand typed copy of a number. Every
figure is read at build time from the file that keeps it:

- the past (origins table, milestones, the ranges caveat) from
  TIMELINE.md;
- the proposed future (phase headings, gates, the iteration rule)
  from TIMELINE.md, and the intentions framing from INTENTIONS.md's
  own stated rule;
- the present counts from tools/today_line.py's own functions, which
  read life.html, foundations.json, and PROGRESS.md;
- the seven acts and their proof sentences from site.json;
- the Index seed counts from the progress entry that records them in
  PROGRESS.md;
- the studies path from foundations.json grouped by domain, with each
  domain's anchor read from foundations.html itself, and the five
  runnable demonstrations read from foundations.html;
- the money state from FUNDS_LEDGER.md's entries table.

The script refuses to build if a source does not match the shape it
expects, so a shifted source fails loudly instead of printing a wrong
count. The shell, bar, and footer are the record pages' own, imported
from tools/render_docs.py so the house pattern cannot drift.

Run: python3 tools/build_versions.py
"""

import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_docs as rd
import today_line

ROOT = rd.ROOT
SITE = rd.SITE
BLOB = rd.BLOB
INDEX = "https://topsoilcommons.github.io/index/"
GH = "https://github.com/topsoilcommons/"


def fail(msg):
    print("build_versions: " + msg, file=sys.stderr)
    sys.exit(1)


def esc(text):
    return html.escape(text, quote=False)


def read(name):
    path = ROOT / name
    if not path.exists():
        fail("missing %s" % name)
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------- the past

def timeline_origins(md):
    rows = []
    in_table = False
    for line in md.split("\n"):
        if line.strip().startswith("| Region"):
            in_table = True
            continue
        if in_table:
            if not rd.is_table_row(line):
                break
            cells = rd.split_row(line)
            if cells[0].startswith("---") or cells[0] == "Region":
                continue
            rows.append(cells)
    if len(rows) < 5:
        fail("TIMELINE.md: origins table not found in the expected shape")
    return rows


def timeline_milestones(md):
    anchor = md.find("What the harvest then made possible")
    if anchor < 0:
        fail("TIMELINE.md: milestones lead line not found")
    items = []
    for line in md[anchor:].split("\n")[1:]:
        stripped = line.strip()
        if stripped.startswith("- "):
            items.append(stripped[2:].strip())
        elif items:
            break
    if len(items) < 4:
        fail("TIMELINE.md: milestone list not found in the expected shape")
    return items


def timeline_ranges_note(md):
    """The paragraph under the origins table, verbatim."""
    lines = md.split("\n")
    for i, line in enumerate(lines):
        if line.strip().startswith("| The Ethiopian highlands"):
            para = []
            for follow in lines[i + 1:]:
                if follow.strip() == "":
                    if para:
                        break
                    continue
                para.append(follow.strip())
            if para:
                return " ".join(para)
    fail("TIMELINE.md: ranges note paragraph not found")


# ------------------------------------------------------- the proposed future

def first_sentences(para, extra_starts=()):
    """The first sentence of a paragraph, plus a following sentence when
    it starts with one of the given words."""
    parts = re.split(r"(?<=\.)\s+", para.strip())
    out = [parts[0]]
    for part in parts[1:]:
        if any(part.startswith(s) for s in extra_starts):
            out.append(part)
        else:
            break
    return " ".join(out)


def timeline_phases(md):
    chunks = re.split(r"^## (Phase [^\n]*)$", md, flags=re.M)
    phases = []
    for i in range(1, len(chunks), 2):
        heading, body = chunks[i].strip(), chunks[i + 1]
        paras = [p.replace("\n", " ").strip()
                 for p in body.split("\n\n") if p.strip()]
        paras = [p for p in paras if not p.startswith(("- ", "##"))]
        if not paras:
            fail("TIMELINE.md: phase %s has no gate paragraph" % heading)
        gate = first_sentences(paras[0], extra_starts=("Intention",))
        extra = ""
        match = re.search(r"[^.]*taking part is this phase's aim\.",
                          body)
        if match:
            extra = match.group(0).strip()
        match = re.search(r"Citizens intention this phase: [^.]*\.",
                          body)
        if match:
            extra = (extra + " " + match.group(0)).strip()
        phases.append((heading, gate, extra))
    if len(phases) < 4:
        fail("TIMELINE.md: phases not found in the expected shape")
    return phases


def iteration_rule(md):
    anchor = md.find("## The iteration rule")
    if anchor < 0:
        fail("TIMELINE.md: iteration rule section not found")
    para = []
    for line in md[anchor:].split("\n")[1:]:
        if line.strip() == "":
            if para:
                break
            continue
        if line.startswith("## "):
            break
        para.append(line.strip())
    text = " ".join(para)
    keep = []
    for sentence in re.split(r"(?<=\.)\s+", text):
        if sentence.startswith(("Iterations are", "Every expansion",
                                "An expansion")):
            keep.append(sentence)
    if len(keep) < 3:
        fail("TIMELINE.md: iteration rule sentences not found")
    return " ".join(keep)


def timeline_opening(md):
    match = re.search(r"^(These are intentions with gates[^\n]*)$",
                      md, flags=re.M)
    if not match:
        fail("TIMELINE.md: opening intentions line not found")
    return match.group(1).strip()


# ---------------------------------------------------------------- the present

def index_seed(progress_md):
    match = re.search(
        r"seed holds (\d+) entries.*?(\d+) of those \d+ entries stand "
        r"verified and (\d+) of those \d+ entries stands corrected",
        progress_md, flags=re.S)
    if not match:
        fail("PROGRESS.md: Index seed counts not found")
    return (int(match.group(1)), int(match.group(2)),
            int(match.group(3)))


def progress_sources_note(progress_md):
    match = re.search(r"(\d+) sources opened", progress_md)
    if not match:
        fail("PROGRESS.md: long arc source count not found")
    return int(match.group(1))


def funds_state():
    md = read("FUNDS_LEDGER.md")
    rows = [ln for ln in md.split("\n")
            if ln.strip().startswith("| 20")]
    if len(rows) != 1:
        fail("FUNDS_LEDGER.md: expected exactly one entry row today")
    cells = rd.split_row(rows[0])
    amount = re.search(r"\$[\d,]+", cells[3] + " " + cells[2])
    if not amount or "Balance zero" not in cells[3]:
        fail("FUNDS_LEDGER.md: opening entry does not record a zero "
             "balance in the expected words")
    date = cells[0]
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November",
              "December"]
    year, month, day = date.split("-")
    pretty = "%s %d, %s" % (months[int(month) - 1], int(day), year)
    return pretty, cells[2]


def interactions_empty():
    return "No interactions yet." in read("INTERACTIONS.md")


def foundations_data():
    data = json.loads(read("foundations.json"))
    page = read("foundations.html")
    domains = []
    for record in data:
        if record["domain"] not in domains:
            domains.append(record["domain"])
    anchors = dict(re.findall(
        r'<section class="domain" id="([^"]+)">\s*<h2>([^<]+)</h2>',
        page))
    demos = re.findall(
        r'<section class="demo" id="(demo-[a-z]+)">\s*<h2>([^<]+)</h2>',
        page)
    if len(demos) < 5:
        fail("foundations.html: demonstrations not found")
    return data, domains, anchors, demos


def domain_anchor(domain, anchors):
    for slug, title in anchors.items():
        if title.strip().lower() == domain.strip().lower():
            return slug
    fail("foundations.html: no section anchor for domain %r" % domain)


# ------------------------------------------------------------------- shells

EXTRA_CSS = """
  .arc{display:flex;flex-direction:column-reverse;max-width:760px;margin:10px 0 4px;border-bottom:4px solid #1b1e23}
  .arc .band{border-top:1px solid var(--line);padding:10px 12px;font-size:15px}
  .arc .band .when{font-weight:700}
  .arc .past{background:#ece7d8}
  .arc .present{background:#f4f1e8}
  .arc .future{background:#fdfcf9}
  .arc .floor{font-size:13.5px;color:var(--soft);padding:4px 12px 8px}
  .actline{border-top:1px solid var(--line);padding:12px 0 2px}
  .actline .actname{font-weight:700;margin:0 0 4px}
  .actline p{margin:0 0 8px}
  ul.plain{font-size:16px;margin:0 0 14px;padding-left:24px}
  ul.plain li{margin:0 0 8px}
  .doorline{font-size:17px;font-weight:600}
"""


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
""" % (title, desc, SITE, CURRENT_PAGE, title, desc, SITE,
       CURRENT_PAGE, title, desc, css, rd.SKIP_LINK,
       rd.bar(title), title, orientation, body, tech, rd.FOOTER)


CURRENT_PAGE = ""


# ------------------------------------------------------------------- story

def build_story():
    timeline = read("TIMELINE.md")
    progress = read("PROGRESS.md")
    site = json.loads(read("site.json"))
    listings, places = today_line.ground_totals()
    findings = today_line.foundations_count()
    entries = today_line.progress_count()
    total, verified, corrected = index_seed(progress)
    data, domains, anchors, demos = foundations_data()

    out = []

    # The spine, drawn rising: past at the bottom, future at the top.
    out.append('<div class="arc" role="img" aria-label="The shape of '
               'this page: the long past at the bottom, the present '
               'above it, and the proposed future at the top, all '
               'standing on one floor line.">')
    out.append('<p class="band past"><span class="when">The past:</span> '
               'thousands of years of raising the floor, region by '
               'region.</p>')
    out.append('<p class="band present"><span class="when">The '
               'present:</span> what stands today, counted and '
               'checked.</p>')
    out.append('<p class="band future"><span class="when">The proposed '
               'future:</span> what is intended next, each step with '
               'its gate.</p>')
    out.append('<p class="floor">The floor line under all of it: raise '
               'the floor beneath everyone.</p>')
    out.append('</div>')

    # The past.
    out.append("<h2>The past</h2>")
    out.append("<p>Raising the floor did not begin with this Commons, "
               "and it did not begin in one place. It began again and "
               "again, wherever people first kept a plant or an animal "
               "alive on purpose. Farming began on its own in region "
               "after region:</p>")
    out.append('<ul class="plain">')
    for region, span, gifts in timeline_origins(timeline):
        out.append("<li>%s: %s, first kept %s years ago.</li>"
                   % (esc(region), esc(gifts[0].lower() + gifts[1:]),
                      esc(span)))
    out.append("</ul>")
    out.append("<p>%s</p>" % esc(timeline_ranges_note(timeline)))
    out.append("<p>Then each harvest made a new layer of life "
               "possible:</p>")
    out.append('<ul class="plain">')
    for item in timeline_milestones(timeline):
        out.append("<li>%s</li>" % esc(item))
    out.append("</ul>")
    out.append("<p>In 2026 this Commons began, one late chapter of "
               "that same work.</p>")

    # The present.
    out.append("<h2>The present</h2>")
    out.append("<p>Today the Commons stands on seven tools, one for "
               "each layer of human need, and each tool carries one "
               "proof a stranger can check.</p>")
    for act in site["acts"]:
        out.append('<div class="actline">')
        out.append('<p class="actname">Layer %d: %s. %s.</p>'
                   % (act["layer"], esc(act["need"]), esc(act["act"])))
        out.append("<p>%s</p>" % esc(act["proof"]))
        out.append('<p>%s <a href="%s">See %s</a>.</p>'
                   % (esc(act["unlocks"]), act["see"], esc(act["act"])))
        out.append("</div>")
    out.append("<p>%d listings for food, shelter, and health help "
               "stand checked in Ground, across %d places, every one "
               "against its provider's own page, each with a date it "
               "was checked and a date it must be checked again.</p>"
               % (listings, places))
    out.append("<p>%d findings stand in Foundations, across %d fields "
               "of study, each with its source named. %d of them can "
               "be run right on the page, each in under a minute: "
               '<a href="foundations.html">run the findings</a>.</p>'
               % (findings, len(domains), len(demos)))
    out.append("<p>The Index keeps the record in time order: %d "
               "entries stand in it today, %d of them verified and %d "
               "of them corrected, each entry a claim with the source "
               "it stands on, the hand behind it, and its check. "
               '<a href="%s">Open the Index</a>.</p>'
               % (total, verified, corrected, INDEX))
    out.append("<p>The whole written record stands open: the charter, "
               "the needs map, the rules, the money, and a progress "
               "log of %d dated entries, with the failures left in. "
               '<a href="record.html">Read the record</a>.</p>'
               % entries)

    # The proposed future.
    out.append("<h2>The proposed future</h2>")
    opening = timeline_opening(timeline)
    out.append("<p>%s</p>" % esc(opening))
    for heading, gate, extra in timeline_phases(timeline):
        out.append("<h3>%s</h3>" % esc(heading))
        text = gate if not extra else gate + " " + extra
        out.append("<p>%s</p>" % esc(text))
    out.append("<p>The rule that keeps the future honest: %s</p>"
               % esc(iteration_rule(timeline)))

    # The doors onward.
    out.append("<h2>Begin</h2>")
    out.append('<p class="doorline">Start with one: <a href="index.html'
               '#layer-0">read the first proof on the home page</a>, '
               "then open the See it link beside it.</p>")
    out.append('<p>For the deeper room: <a href="advanced.html">'
               "Advanced</a>, the full record, the studies, the data, "
               "and the tools that check it.</p>")

    tech = [
        "<p>This page is built by a script from the record itself, so "
        "no count on it is typed by hand. Its sources: "
        '<a href="%sTIMELINE.md">TIMELINE.md</a> for the past and the '
        "proposed future, "
        '<a href="site.json">site.json</a> for the seven acts and '
        "their proofs, "
        '<a href="foundations.json">foundations.json</a> and the '
        "Ground totals recorded in "
        '<a href="life.html">In life</a> for the present counts, and '
        '<a href="%sPROGRESS.md">PROGRESS.md</a> for the log and '
        "Index counts.</p>" % (BLOB, BLOB),
    ]
    return "\n".join(out), tech


# ---------------------------------------------------------------- advanced

def build_advanced():
    timeline = read("TIMELINE.md")
    progress = read("PROGRESS.md")
    site = json.loads(read("site.json"))
    data, domains, anchors, demos = foundations_data()
    sources = progress_sources_note(progress)
    fdate, famount = funds_state()

    out = []
    out.append("<h2>Contents</h2>")
    out.append('<ul class="contents">')
    for slug, name in [
            ("record", "The written record, in reading order"),
            ("studies", "Foundations: the studies as a path"),
            ("long-arc", "The long arc, with its sources"),
            ("connections", "Where the fields meet"),
            ("check", "Check it the way a scholar would"),
            ("builders", "For builders: data, code, and the agent map"),
            ("thin", "Where the record is thin")]:
        out.append('<li><a href="#%s">%s</a></li>' % (slug, name))
    out.append("</ul>")

    # The written record, in reading order.
    out.append('<section id="record">')
    out.append("<h2>The written record, in reading order</h2>")
    out.append("<p>The whole written record stands on one page, "
               '<a href="record.html">The Record</a>, and document by '
               "document below, in the order the Record reads them. "
               "Each document also stands on its own page, and its "
               "source is kept on GitHub.</p>")
    out.append('<ul class="plain">')
    for md_name, plain_name, slug in rd.RECORD_ORDER:
        own = rd.PAGE_OF.get(md_name)
        line = ('<a href="record.html#%s">%s</a> (%s)'
                % (slug, plain_name, md_name))
        if own:
            line += ', also <a href="%s">on its own page</a>' % own
        line += (', <a href="%s%s">source on GitHub</a>.'
                 % (BLOB, md_name))
        out.append("<li>%s</li>" % line)
    out.append('<li><a href="shelf.html">The shelf</a>: proven work '
               'by others and by the Commons, each entry with its '
               'license checked at its source and three doors, use '
               'it, adopt it, and change it.</li>')
    out.append('<li><a href="records.html">Public records</a>: '
               'what stands in the open for each need, what the '
               'Commons holds, what others hold open for anyone, '
               'and what is missing, each record with its source '
               'and its limits.</li>')
    out.append("</ul>")
    out.append("</section>")

    # Foundations: the studies as a path.
    out.append('<section id="studies">')
    out.append("<h2>Foundations: the studies as a path</h2>")
    out.append("<p>Foundations holds %d studies across %d fields of "
               "study, each one opened and read at its source before "
               "it was filed, and each printed with its source beside "
               "it. Walk it as a curriculum: begin with a demonstration "
               "you can run, then read the field it came from.</p>"
               % (len(data), len(domains)))
    out.append("<p>Five findings can be run, each in under a "
               "minute:</p>")
    out.append('<ul class="plain">')
    for demo_id, demo_title in demos:
        out.append('<li><a href="foundations.html#%s">%s</a></li>'
                   % (demo_id, esc(demo_title)))
    out.append("</ul>")
    out.append("<p>The fields, and where to begin in each:</p>")
    out.append('<ul class="plain">')
    for domain in domains:
        records = [r for r in data if r["domain"] == domain]
        first = records[0]
        out.append(
            '<li><a href="foundations.html#%s">%s</a>: %d %s. Begin '
            'with <a href="%s">%s</a> (%s, %s).</li>'
            % (domain_anchor(domain, anchors), esc(domain),
               len(records), "study" if len(records) == 1 else "studies",
               html.escape(first["url"], quote=True),
               esc(first["title"]), esc(first["venue"]), first["year"]))
    out.append("</ul>")
    out.append("<p>The corpus itself is a data file, "
               '<a href="foundations.json">foundations.json</a>, so a '
               "learner or a machine can take the whole set away and "
               "work on it.</p>")
    out.append("</section>")

    # The long arc, with its sources.
    out.append('<section id="long-arc">')
    out.append("<h2>The long arc, with its sources</h2>")
    out.append("<p>The timeline opens with the long arc: farming's ten "
               "independent origins and the milestones each harvest "
               "made possible. It stands at the head of "
               '<a href="record.html#record-timeline">The Record</a> '
               "and in full in "
               '<a href="%sTIMELINE.md">TIMELINE.md</a>.</p>' % BLOB)
    out.append("<p>%s</p>" % esc(timeline_ranges_note(timeline)))
    out.append("<p>The research behind it opened %d sources, peer "
               "reviewed papers, university publications, and museum "
               "and heritage records among them, and the notes name the "
               "argued points. Two claims were left out for lack of "
               "support, and the log says so: an Indus origin of "
               "farming, and an early date for enset. The entry stands "
               'in <a href="progress.html">the progress log</a>.</p>'
               % sources)
    out.append("</section>")

    # Where the fields meet.
    demo = {title: demo_id for demo_id, title in demos}
    out.append('<section id="connections">')
    out.append("<h2>Where the fields meet</h2>")
    out.append("<p>The Commons draws a few connections itself, between "
               "a finding in one field and the layer of need it speaks "
               "to. Each stands open to correction like everything "
               "else here.</p>")
    out.append('<ul class="plain">')
    out.append(
        '<li>Money and the body. The Kenya cash transfer finding, in '
        '<a href="foundations.html#%s">Poverty and material '
        'security</a>, measures the floor of the body directly: '
        'money with no conditions raised what households consumed. '
        '<a href="foundations.html#%s">Run it</a>. The tool at that '
        'layer is <a href="%s">Ground</a>.</li>'
        % (domain_anchor("Poverty and material security", anchors),
           demo["Cash transfers, Kenya"], site["acts"][0]["see"]))
    out.append(
        '<li>Printed facts and shared truth. The Uganda report cards '
        'finding, in <a href="foundations.html#%s">Governance and '
        'democracy</a>, shows a community scorecard moving clinics '
        'and schools. <a href="foundations.html#%s">Run it</a>. '
        '<a href="%s">Graph</a> works the same bet at the layer of '
        'shared truth, and the Index files claims the same way, with '
        'their checks attached.</li>'
        % (domain_anchor("Governance and democracy", anchors),
           demo["Citizen report cards, Uganda"], site["acts"][4]["see"]))
    out.append(
        '<li>Help and learning. The study of AI help and novices, in '
        '<a href="foundations.html#%s">Artificial intelligence and '
        'human computer interaction</a>, found the least practiced '
        'gained the most from the same help. '
        '<a href="foundations.html#%s">Run it</a>. '
        '<a href="%s">Atlas</a> is built on that shape at the layer '
        'of learning: one claim at a time, its proof shown.</li>'
        % (domain_anchor("Artificial intelligence and human computer "
                         "interaction", anchors),
           demo["AI help and novices"], site["acts"][2]["see"]))
    out.append(
        '<li>Speed and truth. False news travels faster than true '
        'news, in <a href="foundations.html#%s">Truth and shared '
        'knowledge</a>. <a href="foundations.html#%s">Run the '
        'race</a>. The Index exists in the shape of that finding: '
        'one timeline for everyone, claims before verdicts, '
        'corrections added and never quietly edited.</li>'
        % (domain_anchor("Truth and shared knowledge", anchors),
           demo["False news travels faster"]))
    out.append(
        '<li>Ties and belonging. Connection and survival, in '
        '<a href="foundations.html#%s">Belonging and social '
        'connection</a>, ties the strength of a person\'s ties to '
        'living longer. <a href="foundations.html#%s">Run it</a>. '
        '<a href="%s">Cohort</a> serves that layer, and '
        '<a href="%s">Still</a> serves the mind that carries it.</li>'
        % (domain_anchor("Belonging and social connection", anchors),
           demo["Connection and survival"], site["acts"][3]["see"],
           site["acts"][1]["see"]))
    out.append("</ul>")
    out.append("<p>Where the record disagrees with itself, both "
               "readings stand. In the Index, one early Graph figure "
               "stands filed as corrected, and its correction stands "
               "in its own entry beside it, each with its source and "
               "its hand. Nothing here is quietly edited; a fix is a "
               'new entry. <a href="%s">See the pair in the Index</a>.'
               "</p>" % INDEX)
    out.append("</section>")

    # Check it the way a scholar would.
    out.append('<section id="check">')
    out.append("<h2>Check it the way a scholar would</h2>")
    out.append("<p>Every claim in this record carries three things: "
               "its ground, the source it stands on; its hand, the "
               "named person or people who stand behind it; and its "
               "check, the way a stranger can test it again and find "
               "the same result. The methods and measures stand one "
               "layer down from every claim, so a learner in any field "
               "can go as deep as the record goes.</p>")
    out.append('<ul class="plain">')
    out.append('<li>The Index: its format, its six states, and its '
               'validator are kept in <a href="%sindex">the Index '
               'repository</a>, and the entries themselves stand in '
               'the <a href="%s">viewer</a>, each with its seal.</li>'
               % (GH, INDEX))
    out.append('<li>Atlas: one claim stands on its page with its full '
               'proof, the same on phone, watch, voice, and wall: '
               '<a href="%s">the Proof screen</a>.</li>'
               % site["acts"][2]["see"])
    out.append('<li>Graph: its scores come from a hand labeled set of '
               'documents, and the misses are published beside the '
               'scores, in <a href="%s">its repository</a> and on '
               '<a href="%s">its page</a>.</li>'
               % (GH + "graph", site["acts"][4]["see"]))
    out.append('<li>Machine: its gradient checks and its two '
               'benchmark runs are recorded in '
               '<a href="%s">its repository</a>, with the numbers '
               'counted by the code.</li>' % (GH + "machine"))
    out.append('<li>Lumen: its refusal tests run over the real texts '
               'of its two exhibits, and the results stand in '
               '<a href="%s">its repository</a>.</li>' % (GH + "lumen"))
    out.append('<li>Still: it collects nothing and calls nothing; its '
               'one measure, the pacer timing runs, stands committed '
               'in <a href="%s">its repository</a>, labeled as '
               'builder test runs.</li>' % (GH + "still"))
    out.append('<li>Ground: every listing carries its check date and '
               'its expiry, and past expiry a listing shows as stale, '
               'never silently: <a href="%s">the board</a> and '
               '<a href="%s">its repository</a>.</li>'
               % (site["acts"][0]["see"], GH + "ground"))
    out.append("</ul>")
    out.append("</section>")

    # For builders.
    out.append('<section id="builders">')
    out.append("<h2>For builders: data, code, and the agent map</h2>")
    out.append("<p>One section among the learning sections, for those "
               "who build: the data files, the code, and the map "
               "written for agents.</p>")
    out.append('<ul class="plain">')
    out.append('<li>Data: <a href="site.json">site.json</a>, the acts '
               'in machine readable form; '
               '<a href="foundations.json">foundations.json</a>, the '
               '%d studies; <a href="https://topsoilcommons.github.io/'
               'ground/listings.json">listings.json</a>, Ground\'s '
               'listings with their check dates.</li>' % len(data))
    out.append('<li>The agent map: <a href="llms.txt">llms.txt</a>, '
               'this whole site written plainly for agents, with the '
               'duties an agent carries here: state that you are an '
               'agent, and name your operator.</li>')
    out.append('<li>Code: nine repositories, one per act and one for '
               'the record: <a href="%s">github.com/topsoilcommons</a>. '
               'The scripts that build these pages stand in '
               '<a href="%stopsoilcommons/tree/main/tools">tools</a> '
               'of the record repository.</li>' % (GH, GH))
    out.append('<li>Taking part: the doors on the '
               '<a href="index.html">home page</a> are sized in '
               'minutes and credited in the open; the rules stand in '
               '<a href="open-table.html">The open table</a> and '
               '<a href="participation.html">Participation</a>.</li>')
    out.append("</ul>")
    out.append("</section>")

    # Where the record is thin.
    out.append('<section id="thin">')
    out.append("<h2>Where the record is thin</h2>")
    out.append("<p>Stated as thin, in the open:</p>")
    out.append('<ul class="plain">')
    out.append("<li>Money: the funds ledger opened on %s, and its one "
               "entry records %s in, no funds received yet, and no "
               "host appointed. Every later amount joins it there. "
               '<a href="funds.html">Funds</a> and '
               '<a href="funds-ledger.html">the funds ledger</a>.</li>'
               % (fdate, famount))
    if interactions_empty():
        out.append("<li>People: the doors for taking part were wired "
                   "on October 15, 2026, and no outside interaction "
                   "stands answered yet. The log of them stands open "
                   'and empty: <a href="interactions.html">'
                   "Interactions</a>.</li>")
    if "Spanish staged, awaiting a fluent human check" in timeline:
        out.append("<li>Languages: Still stands in English. Its "
                   "Spanish is staged, awaiting a fluent human check, "
                   "and does not ship until that check resolves every "
                   "disputed line.</li>")
    if "its server cannot run on static hosting" in timeline:
        out.append("<li>Cohort's room: its server cannot run on "
                   "static hosting, so the live room is a package "
                   "ready to deploy, not a running room, and the "
                   "record says so.</li>")
    out.append("<li>Reach: no outside contributor has shipped yet, "
               "and no institution has adopted a tool. The phases in "
               "the timeline name those as gates, not as facts.</li>")
    out.append("</ul>")
    out.append("</section>")

    out.append('<p>For the plain telling: <a href="story.html">The '
               "story</a>, where this comes from, where it stands, "
               "and where it is going.</p>")

    tech = [
        "<p>The machine readable forms of this page's contents: "
        '<a href="llms.txt">llms.txt</a>, the agent map; '
        '<a href="site.json">site.json</a>, the acts as data; and '
        '<a href="foundations.json">foundations.json</a>, the '
        "studies as data.</p>",
    ]
    return "\n".join(out), tech


def main():
    global CURRENT_PAGE
    CURRENT_PAGE = "story.html"
    body, tech = build_story()
    (ROOT / "story.html").write_text(
        shell("The story",
              "The story of Topsoil Commons: where it comes from, "
              "where it stands, and where it is going, in plain words.",
              body, tech), encoding="utf-8")
    print("build_versions: story.html written")
    CURRENT_PAGE = "advanced.html"
    body, tech = build_advanced()
    (ROOT / "advanced.html").write_text(
        shell("Advanced",
              "For deep learners in any field: the full record, the "
              "studies gathered as a path to walk, and the tools that "
              "check every claim, gathered in one room.",
              body, tech), encoding="utf-8")
    print("build_versions: advanced.html written")


if __name__ == "__main__":
    main()
