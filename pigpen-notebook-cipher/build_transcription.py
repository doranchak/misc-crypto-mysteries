"""Build the machine-readable transcription from decode.py and embed it in index.html.

Writes transcription.json and (re)generates the block between
<!-- TRANSCRIPTION:BEGIN --> and <!-- TRANSCRIPTION:END --> in index.html.
Run:  /opt/homebrew/bin/python3.11 -I build_transcription.py
"""
import html, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import decode  # noqa: E402  (KEY, LINES, seg)

EXPECTED = ("IN EXACLY ONE MINUETE THE OFFICE PHONE WILL RING AND ILL BE SENT TO THE OFFICE "
            "WHERE MY ADOPTIVE FAMILY WILL COME COLLECT ME. I ACCEPT WITH GRATTITUDE.")

# One-character stroke tokens (the ASCII shorthand used in decode.py).
TOKENS = {
    "U": "open-top box ⊔",
    "b": "open-bottom box Π, no hook",
    "N": "open-bottom box Π with a small hook at the bottom right",
    "C": "\"[\" bracket (open right)",
    "E": "\"[\" bracket with an inner dash",
    "5": "Γ-like hooked variant of the \"[\" bracket",
    "L": "L shape",
    "O": "square",
    "o": "round \"o\"",
    "A": "Λ (lambda / caret)",
    "V": "V",
    "<": "\"<\" chevron",
    ">": "\">\" chevron",
    "T": "inverted T ⊥",
    "h": "short hook ↘",
    "7": "dash on top of a slash (\"7\" shape)",
    "c": "small open arc / Π-like glyph",
    "|": "vertical stroke",
    "-": "horizontal dash",
    "\\": "backslash stroke",
    "/": "slash stroke",
}

# (line index, word index) -> caution about that word as a whole
WORD_NOTES = {
    (1, 1): "EXACLY: spelled as the glyphs read (no T); may be a misspelling or a stroke-grouping error.",
    (2, 1): "MINUETE: spelled as the glyphs read (extra E); may be a misspelling or a stroke-grouping error.",
    (8, 2): "ADOPTIVE: V is partly hidden under the circle strokes and the final E is hidden by the circle.",
    (12, 0): "GRATTITUDE: spelled as the glyphs read (extra T); may be a misspelling or a stroke-grouping error.",
}
# single-occurrence glyphs whose letter value rests on one example
LOW_CONF = {"7": "X occurs once", "-/": "S occurs once", "c-": "V occurs once, partly obscured"}

LINE_IDS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "b1", "b2"]
LINE_IMGS = [f"lines/L{n:02d}.jpg" for n in range(1, 11)] + ["lines/B1.jpg", "lines/B2.jpg"]
PERIOD_AFTER = {(10, 2), (12, 0)}  # (line, word) followed by a full stop in the photo


def describe(glyph):
    return " + ".join(TOKENS[c] for c in glyph)


def build():
    lines, used, plain_words = [], {}, []
    for li, (words, lid, img) in enumerate(zip(decode.LINES, LINE_IDS, LINE_IMGS), 1):
        out_words = []
        for wi, w in enumerate(words):
            glyphs = decode.seg(w)
            plain = "".join(decode.KEY[g] for g in glyphs)
            for g in glyphs:
                used[g] = decode.KEY[g]
            entry = {"glyphs": glyphs, "plain": plain}
            if (li, wi) in PERIOD_AFTER:
                entry["period_after"] = True
            if (li, wi) in WORD_NOTES:
                entry["note"] = WORD_NOTES[(li, wi)]
            low = sorted({LOW_CONF[g] for g in glyphs if g in LOW_CONF})
            if low:
                entry["low_confidence"] = low
            out_words.append(entry)
            plain_words.append(plain + ("." if (li, wi) in PERIOD_AFTER else ""))
        lines.append({"id": lid, "image": img, "words": out_words})
    plaintext = " ".join(plain_words)
    assert plaintext == EXPECTED, plaintext
    key = {g: {"letter": used[g], "shape": describe(g)} for g in sorted(used, key=lambda g: (used[g], g))}
    by_letter = {}
    for g, v in key.items():
        by_letter.setdefault(v["letter"], []).append(g)
    return {
        "format": "pigpen-notebook-cipher-transcription/1",
        "source_image": "original.png",
        "plaintext": plaintext,
        "how_to_read": (
            "Hand transcription, line by line. Each word is a list of glyphs; each glyph is a string of "
            "one-character stroke tokens (see token_alphabet) written left to right, so a pre-stroke such as "
            "the | of P comes before the chevron and a trailing mark comes after the shape. Glyphs are "
            "delimited explicitly because the raw stroke strings are ambiguous (e.g. 'h|' = W vs 'h' + '|'). "
            "glyph_to_letter is the substitution key; decoding is glyph_to_letter[glyph] for every glyph."),
        "provenance": (
            "Strokes were read by eye from the photo, then several readings (line 6 word 3, end of line 8, the "
            "backslash on the second Λ of FAMILY, the first glyph of line 10) were revised after a plaintext "
            "hypothesis existed, so this transcription is not fully independent of the decipherment. "
            "Letters J, K, Q, Z do not occur."),
        "token_alphabet": TOKENS,
        "glyph_to_letter": {g: v["letter"] for g, v in key.items()},
        "glyph_shape": {g: v["shape"] for g, v in key.items()},
        "letter_to_glyphs": dict(sorted(by_letter.items())),
        "lines": lines,
    }


def dumps(o, ind=0, width=110):
    """JSON with short sub-objects kept on one line."""
    flat = json.dumps(o, ensure_ascii=False)
    if len(flat) + ind <= width or not isinstance(o, (dict, list)):
        return flat
    pad = " " * (ind + 2)
    if isinstance(o, dict):
        body = ",\n".join(f"{pad}{json.dumps(k, ensure_ascii=False)}: {dumps(v, ind + 2, width)}" for k, v in o.items())
        return "{\n" + body + "\n" + " " * ind + "}"
    body = ",\n".join(pad + dumps(v, ind + 2, width) for v in o)
    return "[\n" + body + "\n" + " " * ind + "]"


def compact(data):
    rows = []
    for ln in data["lines"]:
        ws = []
        for w in ln["words"]:
            ws.append(",".join(w["glyphs"]) + ("." if w.get("period_after") else ""))
        rows.append(f'{ln["id"]:>2}: ' + "  ".join(ws))
    return "\n".join(rows)


def section(data, text):
    emb = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c").replace("&", "\\u0026")
    return f"""<!-- TRANSCRIPTION:BEGIN (generated by build_transcription.py) -->
<h2 id="machine-readable">Machine-readable transcription</h2>
<p class="note">One entry per word, one string per glyph, strokes written left to right. Glyphs are delimited
explicitly (the raw stroke strings are ambiguous in a few places, e.g. <code>h|</code> = W vs <code>h</code> + <code>|</code>).
Glyphs are comma-separated, words are separated by spaces, a trailing <code>.</code> is a full stop in the photo.
The same data is in <a href="transcription.json">transcription.json</a> and in the
<code>&lt;script type="application/json" id="transcription"&gt;</code> block of this page (token alphabet,
key, and per-word plaintext with low-confidence flags).</p>
<p class="note"><b>Caveat:</b> strokes were read by eye, and a few readings (line 6 word 3, the end of line 8, the
backslash on the second Λ of FAMILY, the first glyph of line 10) were revised after the plaintext was known, so this
transcription is not fully independent of the decipherment. S, X and V rest on one occurrence each.</p>
<pre class="tx" id="tx-compact">{html.escape(text)}</pre>
<p><button type="button" id="tx-copy-compact">Copy compact text</button>
<button type="button" id="tx-copy-json">Copy JSON</button>
<a href="transcription.json" download>Download transcription.json</a></p>
<script type="application/json" id="transcription">{emb}</script>
<script>
(function(){{
  function cp(id,btn,fn){{document.getElementById(btn).addEventListener('click',function(){{
    var t=fn(); (navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).catch(function(){{
      var a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();
      document.execCommand('copy');a.remove();}});}});}}
  cp('tx-compact','tx-copy-compact',function(){{return document.getElementById('tx-compact').textContent;}});
  cp('transcription','tx-copy-json',function(){{
    return JSON.stringify(JSON.parse(document.getElementById('transcription').textContent),null,1);}});
}})();
</script>
<!-- TRANSCRIPTION:END -->"""


def main():
    data = build()
    text = compact(data)
    (HERE / "transcription.json").write_text(dumps(data) + "\n", encoding="utf-8")
    (HERE / "transcription.txt").write_text(text + "\n", encoding="utf-8")
    page = HERE / "index.html"
    src = page.read_text(encoding="utf-8")
    block = section(data, text)
    b, e = "<!-- TRANSCRIPTION:BEGIN", "<!-- TRANSCRIPTION:END -->"
    if b in src:
        i, j = src.index(b), src.index(e) + len(e)
        src = src[:i] + block + src[j:]
    else:
        anchor = "<h2>How it was solved</h2>"
        assert anchor in src
        src = src.replace(anchor, block + "\n" + anchor, 1)
    if ".tx{" not in src:
        src = src.replace(".note{color:#555;font-size:.93rem}",
                          ".note{color:#555;font-size:.93rem}\n"
                          ".tx{background:#f6f6f6;border:1px solid #ddd;padding:.6rem .8rem;overflow-x:auto;font:.9rem/1.5 ui-monospace,monospace}\n"
                          "button{font:inherit;font-size:.9rem;margin-right:.5rem}", 1)
    page.write_text(src, encoding="utf-8")
    print(text)
    print(f"glyph types: {len(data['glyph_to_letter'])}, letters: {len(data['letter_to_glyphs'])}")


if __name__ == "__main__":
    main()
