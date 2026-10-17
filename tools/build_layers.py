#!/usr/bin/env python3
"""Generate layers.json, the seven acts as data for agents.

One object per layer: its need, its act, the door line a person would
say, the first step that takes under a minute, its proof sentence, and
its links. The source is site.json, the same file the record pages
read, so the agent layer and the human pages cannot drift apart.

The generator also checks the home page: every act's door line and
first step must stand in index.html's visible text, in the same
words. If the page and the data disagree, the script fails loudly
and writes nothing, the way tools/today_line.py refuses a stale
source.

Each act also carries a placement, the Direction 4 setting for what
its band on the home page holds: A, the proof in full in the band;
B, the first step, with the proof one tap away in a fold inside the
band; C, just the marker. The setting stands in site.json, and this
script checks the band's markup against it, so a band flipped by
hand without its setting fails the build instead of drifting. All
seven bands stand at B since the Direction 4 build of October 17,
2026; Joshua flips a band by changing its setting here and its
markup to match.

Run: python3 tools/build_layers.py
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def fail(msg):
    print("build_layers: " + msg, file=sys.stderr)
    sys.exit(1)


def visible_text(html):
    text = re.sub(r"<script.*?</script>|<style>.*?</style>", " ", html, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text)


def main():
    site = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))
    acts = site.get("acts")
    if not isinstance(acts, list) or len(acts) != 7:
        fail("site.json: expected the seven acts")

    home_html = (ROOT / "index.html").read_text(encoding="utf-8")
    home = visible_text(home_html)
    layers = []
    for act in sorted(acts, key=lambda a: a["layer"]):
        for field in ("need", "act", "door", "first_step", "proof",
                      "see", "check", "unlocks"):
            if not act.get(field):
                fail("site.json: layer %s is missing %s"
                     % (act.get("layer"), field))
        for field in ("door", "first_step"):
            if act[field] not in home:
                fail("index.html: layer %s %s not found in the home "
                     "page's visible text: %s"
                     % (act["layer"], field, act[field][:60]))
        placement = act.get("placement")
        if placement not in ("A", "B", "C"):
            fail("site.json: layer %s placement must be A, B, or C"
                 % act["layer"])
        band = re.search(
            r'<article class="stratum[^"]*" id="layer-%d"[^>]*>'
            r'(.*?)</article>' % act["layer"], home_html, flags=re.S)
        if not band:
            fail("index.html: no band found for layer %s"
                 % act["layer"])
        tag = band.group(0)[:band.group(0).index(">") + 1]
        body = band.group(1)
        if 'data-placement="%s"' % placement not in tag:
            fail("index.html: layer %s band is not marked placement "
                 "%s as site.json sets it" % (act["layer"], placement))
        fold_at = body.find('<details class="fold">')
        proof_at = body.find('<p class="proof">')
        if placement == "A":
            if proof_at < 0 or 0 <= fold_at < proof_at:
                fail("index.html: layer %s is set to A, the proof in "
                     "full, but its proof stands inside a fold"
                     % act["layer"])
        elif placement == "B":
            if '<p class="first">' not in body or fold_at < 0 \
                    or proof_at < fold_at:
                fail("index.html: layer %s is set to B, the first "
                     "step, but its first step or its folded proof "
                     "is missing" % act["layer"])
        else:
            if proof_at >= 0 or '<p class="first">' in body:
                fail("index.html: layer %s is set to C, just the "
                     "marker, but the band carries more"
                     % act["layer"])
        layers.append({
            "layer": act["layer"],
            "need": act["need"],
            "act": act["act"],
            "door": act["door"],
            "first_step": act["first_step"],
            "proof": act["proof"],
            "unlocks": act["unlocks"],
            "see": act["see"],
            "check": act["check"],
            "placement": placement,
        })

    out = {
        "generated_from": "site.json by tools/build_layers.py; "
                          "do not edit by hand",
        "organization": site["organization"],
        "rule": site["rule"],
        "about": "One object per layer of Topsoil Commons: the need, "
                 "the act, the door line a person would say, the "
                 "first step that takes under a minute, the proof "
                 "sentence, and where to see it and check it.",
        "layers": layers,
    }
    path = ROOT / "layers.json"
    path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8")
    print("build_layers: wrote layers.json with %d layers, each "
          "checked against the home page" % len(layers))


if __name__ == "__main__":
    main()
