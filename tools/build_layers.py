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

    home = visible_text((ROOT / "index.html").read_text(encoding="utf-8"))
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
