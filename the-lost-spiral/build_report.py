#!/usr/bin/env python3
"""Build index.html (self-contained apart from lost-spiral.png and the thread PDF link)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hopcipher import *
from verify import ablations, filler_stats

HERE = os.path.dirname(os.path.abspath(__file__))
coords = json.load(open(os.path.join(HERE, "spiral_coords.json")))
fh, _ = decode(FRIDAY)
sh, _ = decode(SPIRAL)
DATA = {
    "friday": {"ptr": FRIDAY, "msgLen": 26},
    "spiral": {"ptr": SPIRAL, "msgLen": 20, "coords": coords},
    "ablations": ablations(),
    "z": {"friday": round(filler_stats(fh, 26), 2), "spiral": round(filler_stats(sh, 20), 2)},
}

TEMPLATE = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
html = TEMPLATE.replace("__DATA__", json.dumps(DATA, separators=(",", ":")))
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(html)
print("wrote index.html", len(html), "bytes")
