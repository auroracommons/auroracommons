#!/usr/bin/env python3
"""Generate the dated today line in the home page's first screen.

Move 6 of the vision appeal study pass: one dated sentence, produced by
the record's own machinery, never typed by hand. Every count in the
sentence is read from a source inside this repository at run time:

- Ground totals (listings standing, places) are parsed from life.html,
  the page in this repo where those totals are recorded from the
  Ground boards.
- The Foundations count is the number of records in foundations.json.
- The progress count is the number of dated entries in PROGRESS.md.

The sentence is written into index.html between the today:begin and
today:end markers. The script refuses to write anything if a source
does not match the shape it expects, so a stale or shifted source
fails loudly instead of printing a wrong count.

Run: python3 tools/today_line.py
"""

import datetime
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def fail(msg):
    print("today_line: " + msg, file=sys.stderr)
    sys.exit(1)


def ground_totals():
    life = (ROOT / "life.html").read_text(encoding="utf-8")
    anchor = life.find("<h3>Ground, the body</h3>")
    if anchor < 0:
        fail("life.html: Ground heading not found")
    para = re.search(r"<p>(.*?)</p>", life[anchor:], flags=re.S)
    if not para:
        fail("life.html: Ground paragraph not found")
    nums = [int(n) for n in re.findall(r'<span class="rub">(\d+)</span>', para.group(1))]
    # The recorded sentence runs: total listings, seed listings, board
    # listings, board places, total places. The line needs the two totals.
    if len(nums) < 2:
        fail("life.html: Ground paragraph carries too few counts")
    return nums[0], nums[-1]


def foundations_count():
    data = json.loads((ROOT / "foundations.json").read_text(encoding="utf-8"))
    if not isinstance(data, list) or not data:
        fail("foundations.json: expected a non-empty list of records")
    return len(data)


def progress_count():
    text = (ROOT / "PROGRESS.md").read_text(encoding="utf-8")
    n = len(re.findall(r"^## ", text, flags=re.M))
    if n == 0:
        fail("PROGRESS.md: no dated entries found")
    return n


def main():
    listings, places = ground_totals()
    findings = foundations_count()
    entries = progress_count()
    today = datetime.date.today()
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    date_str = "%s %d, %d" % (months[today.month - 1], today.day, today.year)

    line = (
        'Today, <span class="rub">' + date_str + '</span>: '
        '<span class="rub">' + str(listings) + '</span> listings for food, shelter, '
        'and health help stand checked in Ground, across '
        '<span class="rub">' + str(places) + '</span> places, every one against its '
        'provider\'s own page; '
        '<span class="rub">' + str(findings) + '</span> findings stand in Foundations, '
        'each with its source named; and '
        '<span class="rub">' + str(entries) + '</span> entries stand in the public '
        'progress log. Each count can be checked where it is kept: the Ground and '
        'Foundations pages and the log linked in the record below.'
    )

    path = ROOT / "index.html"
    page = path.read_text(encoding="utf-8")
    pattern = re.compile(
        r'(<!-- today:begin -->\n).*?(\n\s*<!-- today:end -->)', re.S)
    if not pattern.search(page):
        fail("index.html: today markers not found")
    new_page = pattern.sub(
        lambda m: m.group(1) + '    <p class="today" id="today-line">'
        + line + '</p>' + m.group(2),
        page, count=1)
    path.write_text(new_page, encoding="utf-8")
    print("today_line: wrote the line for " + date_str
          + " (listings " + str(listings) + ", places " + str(places)
          + ", findings " + str(findings) + ", entries " + str(entries) + ")")


if __name__ == "__main__":
    main()
