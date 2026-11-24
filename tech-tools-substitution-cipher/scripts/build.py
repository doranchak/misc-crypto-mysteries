#!/usr/bin/env python3
"""Build the machine-readable transcription files and the HTML report.

Inputs  (in ../data):  cell_labels.json  glyph_info.json  key.json
Outputs (in ../data):  transcription.json  transcription.csv  cipher_rows.txt  plaintext.txt
        (in ..)     :  index.html

Run:  python3 scripts/build.py
"""
import csv
import html
import json
import os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")

SOURCE_URL = "https://www.reddit.com/r/codes/comments/1reqrgy/a_code_abt_the_cultural_use_of_advanced_tech_tools/"
SOURCE_USER = "u/ChiameraKrther"
HINT = "A code abt the cultural use of advanced tech tools. Substitution encryption, but with 3 variants for each, and +1 for vowels."
VOWELS = set("aeiou")

# The decoded text split into words, spelled exactly as the glyphs decode.
READING = ("the technology of ai shouldnt be a thing to fear and reject it should instead be embraced and used "
           "intelligently but cultural themes of precived danger seem to stop our creativity without it being a "
           "rational fear which makes it a phobia of ai this is wasted potential understanding deep concepts in ai "
           "we are wasting valuable time worrying about catastrophizing events which is just as likely to occure as "
           "in cohesive religous myths that has never nor will ever happeen due to a lack in chemical and physical "
           "empirical evidence thus a prime example of why we should stop fearing our own technological creations").split()

PUNCTUATED = ("The technology of AI shouldn't be a thing to fear and reject it, should instead be embraced and used "
              "intelligently, but cultural themes of precived danger seem to stop our creativity without it being a "
              "rational fear, which makes it a phobia of AI. This is wasted potential: understanding deep concepts in "
              "AI, we are wasting valuable time worrying about catastrophizing events which is just as likely to "
              "occure as in cohesive religous myths that has never nor will ever happeen due to a lack in chemical "
              "and physical empirical evidence. Thus a prime example of why we should stop fearing our own "
              "technological creations.")


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)


def main():
    cells = load("cell_labels.json")
    info = load("glyph_info.json")
    key = load("key.json")

    plain = "".join(c["letter"] for c in cells)
    assert plain == "".join(READING), "READING does not match the decoded letters"
    assert len(cells) == 507

    # ---- transcription.json -------------------------------------------------
    out_cells = []
    for c in cells:
        out_cells.append({
            "index": c["index"], "row": c["row"], "col": c["col"],
            "glyph": c["glyph"], "letter": c["letter"], "letter_by_shape": c["letter_by_shape"],
            "bbox_xyxy": c["bbox"], "note": c["note"],
        })
    letter_counts = Counter(c["letter"] for c in cells if c["letter"])
    trans = {
        "source": {"url": SOURCE_URL, "author": SOURCE_USER, "hint": HINT},
        "image": "images/cipher.png",
        "image_size_wh": [2124, 716],
        "layout": {"rows": 13, "cols": 42, "cells": 507,
                   "note": "Rows 1-12 have 42 glyphs each, row 13 has 3. Read left to right, top to bottom. "
                           "bbox_xyxy is in pixels of images/cipher.png (x0, y0, x1, y1)."},
        "glyphs": info,
        "key": key,
        "plaintext_letters": plain,
        "plaintext_words": READING,
        "cells": out_cells,
    }
    with open(os.path.join(DATA, "transcription.json"), "w", encoding="utf-8") as f:
        json.dump(trans, f, ensure_ascii=False)

    with open(os.path.join(DATA, "transcription.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["index", "row", "col", "glyph", "letter", "letter_by_shape", "x0", "y0", "x1", "y1", "note"])
        for c in cells:
            w.writerow([c["index"], c["row"], c["col"], c["glyph"], c["letter"], c["letter_by_shape"], *c["bbox"], c["note"]])

    rows_txt = []
    for r in range(1, 14):
        rows_txt.append(" ".join(c["glyph"] for c in cells if c["row"] == r))
    with open(os.path.join(DATA, "cipher_rows.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(rows_txt) + "\n")

    with open(os.path.join(DATA, "plaintext.txt"), "w", encoding="utf-8") as f:
        f.write(plain.upper() + "\n\n" + " ".join(READING).upper() + "\n\n" + PUNCTUATED + "\n")

    # ---- statistics for the report -------------------------------------------
    special = [c for c in cells if c["note"] and c["glyph"] in ("TRI_OVERWRITTEN", "SCRIBBLE", "DASH_THICK")]
    merged = [c for c in cells if c["note"] and c["glyph"] not in ("TRI_OVERWRITTEN", "SCRIBBLE", "DASH_THICK")]
    regular = {l: [g for g in gs if g not in ("TRI_OVERWRITTEN", "SCRIBBLE", "DASH_THICK")] for l, gs in key.items()}
    variant_rows = []
    for l in "abcdefghijklmnopqrstuvwxyz":
        cap = 4 if l in VOWELS else 3
        used = len(regular[l])
        variant_rows.append((l, cap, used, letter_counts.get(l, 0)))

    page = render_html(cells, info, key, variant_rows, special, merged, letter_counts)
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)
    print("wrote data/*, index.html;", len(plain), "letters")


def render_html(cells, info, key, variant_rows, special, merged, letter_counts):
    e = html.escape
    payload = {
        "cells": [[c["row"], c["col"], c["glyph"], c["letter"], c["bbox"], c["note"]] for c in cells],
        "info": {g: {"letter": v["letter"], "rep": v["rep"], "count": v["count"], "approx": v["approx"],
                     "description": v["description"]} for g, v in info.items()},
        "key": key,
    }
    words_html = " ".join(READING).upper()
    vrows = "".join(
        f"<tr><td class='l'>{l.upper()}</td><td>{cap}</td><td>{used}</td><td>{n}</td></tr>"
        for l, cap, used, n in variant_rows)
    anomalies = "".join(
        f"<li><b>Row {c['row']}, col {c['col']}</b> ({e(c['glyph'])}): {e(c['note'])} "
        f"Letter by shape alone: <b>{c['letter_by_shape'].upper()}</b>; read as: <b>{(c['letter'] or '(skipped)').upper()}</b>.</li>"
        for c in special)
    merged_html = "".join(
        f"<li>Row {c['row']}, col {c['col']}: {e(c['note'])}</li>" for c in merged)
    template = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
    return (template
            .replace("{{SOURCE_URL}}", SOURCE_URL)
            .replace("{{SOURCE_USER}}", SOURCE_USER)
            .replace("{{HINT}}", e(HINT))
            .replace("{{WORDS}}", e(words_html))
            .replace("{{PUNCT}}", e(PUNCTUATED))
            .replace("{{VARIANT_ROWS}}", vrows)
            .replace("{{ANOMALIES}}", anomalies)
            .replace("{{MERGED}}", merged_html)
            .replace("{{PAYLOAD}}", json.dumps(payload, ensure_ascii=False)))


if __name__ == "__main__":
    main()
