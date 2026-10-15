#!/usr/bin/env python3
"""Build the counts by domain table on the Foundations page.

The table reads foundations.json, the same file the page's own index of
papers is built from, so the counts and the papers below them cannot
drift apart. Run this after foundations.json changes, and commit the
page it writes.

Run: python3 tools/build_foundations_table.py
"""

import json
import sys
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BEGIN = "<!-- domain-counts:begin -->"
END = "<!-- domain-counts:end -->"


def main():
    data = json.loads((ROOT / "foundations.json").read_text(encoding="utf-8"))
    counts = OrderedDict()
    for record in data:
        counts[record["domain"]] = counts.get(record["domain"], 0) + 1
    rows = "\n".join(
        "    <tr><td>%s</td><td>%d</td></tr>" % (domain, count)
        for domain, count in counts.items())
    table = """%s
  <table class="counts-table">
    <thead><tr><th scope="col">Field of study</th><th scope="col">Studies</th></tr></thead>
    <tbody>
%s
    </tbody>
  </table>
  <p class="count">Key: each row is one field of study, and the number beside it counts the studies in that field on this page. The counts were checked on October 15, 2026. The studies stand below, one line each, under their field.</p>
%s""" % (BEGIN, rows, END)

    path = ROOT / "foundations.html"
    page = path.read_text(encoding="utf-8")
    if BEGIN in page and END in page:
        before, rest = page.split(BEGIN, 1)
        _, after = rest.split(END, 1)
        page = before + table + after
    else:
        anchor = "</section>\n\n<section class=\"domain\""
        if anchor not in page:
            print("build_foundations_table: anchor not found",
                  file=sys.stderr)
            sys.exit(1)
        page = page.replace(anchor, table + "\n</section>\n\n<section class=\"domain\"", 1)
        # The table belongs inside the index head section, before its close.
        # The replace above placed it right at the close; that is the spot.
    path.write_text(page, encoding="utf-8")
    print("build_foundations_table: %d findings across %d domains"
          % (len(data), len(counts)))


if __name__ == "__main__":
    main()
