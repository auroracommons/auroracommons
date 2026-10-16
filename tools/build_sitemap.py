#!/usr/bin/env python3
"""Build sitemap.xml for the profile site.

The page list comes from the same source the doc renderer uses, so the
sitemap cannot drift from the site: the hand kept pages stand in PAGES
below, and every rendered record page is read from render_docs.DOCS,
the list tools/render_docs.py renders from the markdown record.

Run: python3 tools/build_sitemap.py
Use --check to compare the committed sitemap with a fresh build.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_docs as rd

ROOT = rd.ROOT
SITE = rd.SITE

# Hand kept public pages of this site, in the order a reader meets them.
PAGES = [
    "",
    "foundations.html",
    "life.html",
    "record.html",
    "story.html",
    "advanced.html",
    "shelf.html",
]


def page_urls():
    urls = [SITE + page for page in PAGES]
    urls.extend(SITE + html_name for _md, html_name in rd.DOCS)
    return urls


def render():
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for url in page_urls():
        lines.append("  <url><loc>%s</loc></url>" % url)
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main(argv):
    rendered = render()
    path = ROOT / "sitemap.xml"
    if "--check" in argv:
        if not path.exists() or path.read_text(encoding="utf-8") != rendered:
            print("FAIL sitemap.xml: it differs from the page list")
            return 1
        print("PASS sitemap.xml: it matches the page list, %d pages"
              % len(page_urls()))
        return 0
    path.write_text(rendered, encoding="utf-8")
    print("Wrote sitemap.xml with %d pages" % len(page_urls()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
