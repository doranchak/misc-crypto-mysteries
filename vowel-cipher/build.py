#!/usr/bin/env python3
"""Generate index.html for the vowel cipher report.  Run: python3.11 -I build.py"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from solve import A, CT, CT_ORIG, CODEBOOK, KEY, REVERSE, VOWELS, decode  # noqa: E402

pairs = [(a, int(b)) for a, b in re.findall(r"([A-Z])(\d)", CT)]

# ---------- step-by-step table ----------
rows = []
word_no = 0
for n, (l, d) in enumerate(pairs, 1):
    if (l, d) in REVERSE:
        pt = REVERSE[(l, d)]
        base = {v: k for k, v in KEY.items()}[l]
        run = A[A.index(base):A.index(base) + d]
        rows.append(
            f'<tr><td>{n}</td><td class="mono">{l}{d}</td><td class="mono">{l} &rarr; {base}</td>'
            f'<td>{d}</td><td class="mono">{" ".join(run)}</td><td class="pt mono"><b>{pt}</b></td><td></td></tr>')
    elif (l, d) == ("V", 5):
        rows.append(
            f'<tr class="sp"><td>{n}</td><td class="mono">{l}{d}</td><td class="mono">V &rarr; A</td>'
            f'<td>{d}</td><td class="mono">A B C D E</td><td class="mono"><i>space</i></td>'
            f'<td>spare code (A+4 would be E, but E is already <span class="mono">O1</span>)</td></tr>')
    else:
        rows.append(
            f'<tr class="sp"><td>{n}</td><td class="mono">{l}{d}</td><td class="mono">V &rarr; A</td>'
            f'<td>{d}</td><td class="mono">A B C D E F</td><td class="mono"><i>end?</i></td>'
            f'<td>spare code (A+5 would be F, but F is already <span class="mono">O2</span>)</td></tr>')
steps = "\n".join(rows)

# ---------- codebook grid ----------
used = set(pairs)
cb = []
for v in VOWELS:
    cells = []
    i0 = A.index(v)
    for k in range(1, 7):
        code = (KEY[v], k)
        if code in REVERSE:
            ch = REVERSE[code]
            cls = "u" if code in used else ""
            cells.append(f'<td class="{cls}"><span class="mono c">{KEY[v]}{k}</span><span class="p">{ch}</span></td>')
        else:
            cls = "spare u" if code in used else "spare"
            cells.append(f'<td class="{cls}"><span class="mono c">{KEY[v]}{k}</span><span class="p">&middot;</span></td>')
    cb.append(f'<tr><th>{v} <span class="arrow">&rarr;</span> <span class="mono">{KEY[v]}</span></th>{"".join(cells)}</tr>')
codebook = "\n".join(cb)

# ---------- ciphertext strip, coloured by word ----------
strip = []
word = 0
for l, d in pairs:
    if (l, d) == ("V", 5):
        strip.append('<span class="tok sep">V5</span>')
        word += 1
    elif (l, d) == ("V", 6):
        strip.append('<span class="tok end">V6</span>')
    else:
        strip.append(f'<span class="tok w{word % 2}">{l}{d}</span>')
strip_html = "".join(strip)

pt_strip = []
word = 0
for l, d in pairs:
    if (l, d) == ("V", 5):
        pt_strip.append('<span class="tok sep">&nbsp;</span>')
        word += 1
    elif (l, d) == ("V", 6):
        pt_strip.append('<span class="tok end">?</span>')
    else:
        pt_strip.append(f'<span class="tok w{word % 2}">{REVERSE[(l, d)]}</span>')
pt_strip_html = "".join(pt_strip)

REDDIT_URL = "https://www.reddit.com/r/ciphers/s/tGyZUbWSzY"
REDDIT_USER = "u/killmealready145"


def frag(name):
    """Read a visualizer fragment and fill in the ciphertext placeholders."""
    with open(os.path.join(HERE, name)) as fh:
        return fh.read().replace("%%CT%%", CT).replace("%%CT_ORIG%%", CT_ORIG)


viz_css, viz_html, viz_js = frag("visualizer.css"), frag("visualizer.html"), frag("visualizer.js")

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Vowel cipher &mdash; solved: THIS IS A VOWEL CIPHER</title>
<style>
  :root {{
    --bg:#fafaf8; --fg:#1d1d1b; --muted:#6b6b66; --line:#dcdcd4; --card:#fff;
    --accent:#0b6e4f; --accent-bg:#e3f3ec; --warn:#a4400f; --warn-bg:#fbeadf;
    --c0:#d6e4ff; --c1:#ffe3c4; --spare:#efeee9;
    --mono: Menlo,Consolas,"DejaVu Sans Mono",ui-monospace,monospace;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{ --bg:#17181a; --fg:#e8e8e3; --muted:#9a9a92; --line:#333537; --card:#1f2022;
      --accent:#5fd1a2; --accent-bg:#173326; --warn:#f0a070; --warn-bg:#3a2416;
      --c0:#24385e; --c1:#5a3b17; --spare:#2a2b2d; }}
  }}
  *{{box-sizing:border-box}}
  body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif}}
  main{{max-width:980px;margin:0 auto;padding:32px 20px 80px}}
  h1{{font-size:1.6rem;margin:0 0 4px}}
  h2{{font-size:1.15rem;margin:40px 0 8px;padding-top:8px;border-top:1px solid var(--line)}}
  p{{margin:8px 0}} .sub{{color:var(--muted);margin-bottom:20px}}
  code,.mono{{font-family:var(--mono);font-size:.9em}}
  .card{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin:12px 0}}
  .answer{{background:var(--accent-bg);border-color:var(--accent)}}
  .answer .pt{{font-size:1.5rem;font-weight:700;letter-spacing:.04em;margin-top:2px}}
  .label{{font-size:.75rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-bottom:4px}}
  .ctline{{font-family:var(--mono);word-break:break-all;font-size:.95rem}}
  .note{{background:var(--warn-bg);border:1px solid var(--warn);border-radius:8px;padding:10px 14px;font-size:.92rem;margin:12px 0}}
  .strip{{display:flex;flex-wrap:wrap;gap:4px;margin:6px 0}}
  .tok{{font-family:var(--mono);font-size:.95rem;min-width:2.2em;text-align:center;padding:4px 6px;border-radius:6px;border:1px solid var(--line)}}
  .tok.w0{{background:var(--c0)}} .tok.w1{{background:var(--c1)}}
  .tok.sep{{background:var(--spare);color:var(--muted);border-style:dashed}}
  .tok.end{{background:var(--warn-bg);border-color:var(--warn);color:var(--warn)}}
  table{{border-collapse:collapse;width:100%;font-size:.88rem}}
  th,td{{border-bottom:1px solid var(--line);padding:4px 8px;text-align:left;vertical-align:top}}
  th{{color:var(--muted);font-weight:600}}
  tr.sp td{{background:var(--spare)}}
  .pt{{color:var(--accent)}}
  table.cb td{{text-align:center;padding:6px 4px;width:12%}}
  table.cb td .c{{display:block;font-size:.75rem;color:var(--muted)}}
  table.cb td .p{{display:block;font-size:1.25rem;font-weight:700}}
  table.cb td.u{{background:var(--accent-bg)}}
  table.cb td.spare .p{{color:var(--muted);font-weight:400}}
  table.cb td.spare.u{{background:var(--warn-bg)}}
  table.cb th{{white-space:nowrap}} .arrow{{color:var(--muted)}}
  label.field{{display:block;margin:10px 0 2px;font-size:.85rem;color:var(--muted)}}
  input[type=text]{{width:100%;font-family:var(--mono);font-size:.9rem;padding:8px 10px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--fg)}}
  .out{{font-family:var(--mono);padding:10px 12px;background:var(--bg);border:1px dashed var(--line);border-radius:6px;word-break:break-all;white-space:pre-wrap;min-height:2.6em}}
  ul{{margin:6px 0 6px 20px;padding:0}} li{{margin:3px 0}}
  a{{color:var(--accent)}}
{viz_css}
</style>
</head>
<body>
<main>
<h1>Vowel cipher &mdash; solved</h1>
<p class="sub">Ciphertext of 23 letter+digit pairs. The cipher letters <b>V O W E L</b> stand for the five vowels, and each digit counts letters forward from that vowel.</p>
<p class="sub" style="margin-top:-12px">Source: puzzle posted by <b>{REDDIT_USER}</b> on r/ciphers, <a href="{REDDIT_URL}">&ldquo;very first cipher go brrrr&rdquo;</a>. &middot; <a href="#visualizer">Jump to the interactive visualizer</a></p>

<div class="card">
  <div class="label">Ciphertext (typo corrected)</div>
  <div class="ctline">{CT}</div>
  <div class="label" style="margin-top:10px">As first posted (typo)</div>
  <div class="ctline">{CT_ORIG}</div>
  <p class="sub" style="margin:8px 0 0;font-size:.85rem">In monospace the letter O looks like a zero. There are no zeros here: digits only run 1&ndash;6, so <span class="mono">O4</span> is the letter O followed by 4.</p>
</div>

<div class="card answer">
  <div class="label">Plaintext</div>
  <div class="pt">THIS IS A VOWEL CIPHER</div>
  <p style="margin-top:6px;font-size:.92rem">The last pair, <span class="mono">V6</span>, is a spare code with no letter value. It is probably an end-of-message or punctuation marker; see <a href="#v6">the V6 caveat</a>.</p>
</div>

<div class="strip">{strip_html}</div>
<div class="strip">{pt_strip_html}</div>
<p class="sub" style="margin-top:2px">Blue/orange alternate by word. Dashed boxes are <span class="mono">V5</span>, which behaves as the word space in all four places a word break is needed.</p>

<h2>1. How the cipher works</h2>
<ul>
  <li><b>Five cipher letters, five vowels.</b> The ciphertext uses exactly five distinct letters: E, L, O, V, W. Taken in the order A, E, I, O, U they spell the keyword <b>V&middot;O&middot;W&middot;E&middot;L</b>: A&rarr;V, E&rarr;O, I&rarr;W, O&rarr;E, U&rarr;L.</li>
  <li><b>The digit is a position in the run that starts at that vowel.</b> Every plaintext letter belongs to the run of the nearest vowel at or before it (A&ndash;D belong to A, E&ndash;H to E, I&ndash;N to I, O&ndash;T to O, U&ndash;Z to U). It is written as <i>the vowel's key letter + its 1-based position in that run</i>. So the vowel itself is digit 1: <span class="mono">W1</span> = I, <span class="mono">E6</span> = O,P,Q,R,S,<b>T</b> = T.</li>
  <li><b>Spare codes.</b> A and E only own four letters each, so digits 5 and 6 on V and O would run into the next vowel and are never the canonical code of any letter. The cipher uses two of these: <span class="mono">V5</span> as a word space and <span class="mono">V6</span> once at the end.</li>
</ul>

<h2>2. Codebook</h2>
<p>Green cells are codes that appear in this message; a dot marks a spare code. Orange = a spare code that was used.</p>
<table class="cb">
<tr><th>vowel &rarr; cipher letter</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th></tr>
{codebook}
</table>

<h2>3. Step-by-step decode</h2>
<table>
<tr><th>#</th><th>pair</th><th>key letter &rarr; vowel</th><th>digit</th><th>run from vowel</th><th>letter</th><th>note</th></tr>
{steps}
</table>

<h2>4. Why I trust it</h2>
<ul>
  <li><b>Search.</b> I tried all 120 ways to assign the five cipher letters to A, E, I, O, U, reading each digit as a forward or backward offset (240 models) and scored each by dictionary-word segmentation. One reading was clearly English: <span class="mono">THISEISEAEVOWELECIPHERF</span> (score 94). The runner-up scored 78 and read <span class="mono">JBAKEAKEIETOSEXEGANBELD</span>, which is gibberish.</li>
  <li><b>The key says what the message says.</b> The assignment that wins is A&rarr;V, E&rarr;O, I&rarr;W, O&rarr;E, U&rarr;L, which spells <i>VOWEL</i>, and the plaintext is "this is a <i>vowel</i> cipher".</li>
  <li><b>Canonical codes everywhere else.</b> The brute-force reading has an extra <span class="mono">E</span> between each pair of words. But under the rule that a letter is coded from its nearest vowel at or before it, a real E is always <span class="mono">O1</span> (as in VOWEL and CIPHER). The four extra Es are all <span class="mono">V5</span> (A+4), a non-canonical way to write E, and they sit exactly where the word breaks go. The other 18 codes are all canonical.</li>
  <li><b>The typo confirms the model.</b> The originally posted <span class="mono">L5</span> decodes to <b>Y</b> and makes the word <i>VOYEL</i>. <span class="mono">L3</span> (= W) gives VOWEL, which is the corrected ciphertext.</li>
</ul>

<h2 id="v6">5. The V6 caveat</h2>
<div class="note">The final <span class="mono">V6</span> is not a letter code under the model: A+5 would be F, but F is already <span class="mono">O2</span>. It occurs only once, at the very end, so its meaning can't be confirmed from this message. The most natural reading is an end-of-message mark or a period, in the same family as <span class="mono">V5</span> = space. The spare codes the scheme leaves free are <span class="mono">V5</span>, <span class="mono">V6</span>, <span class="mono">O5</span> and <span class="mono">O6</span>, which would be enough for a space plus a few punctuation marks. If the encoder instead meant a literal F, the text would read "THIS IS A VOWEL CIPHERF", which is not a word. I could not read the <a href="{REDDIT_URL}">Reddit thread</a> (automated access is blocked), so anything the poster said there about <span class="mono">V6</span> is not reflected here. In the visualizer below you can map <span class="mono">V6</span> to a period or to the arithmetic letter F and see the effect.</div>

{viz_html}

<p class="sub" style="margin-top:32px">Source: <b>{REDDIT_USER}</b> on r/ciphers, <a href="{REDDIT_URL}">{REDDIT_URL}</a>. Code: <a href="solve.py">solve.py</a> (decoder + brute-force check) and <a href="build.py">build.py</a> (generates this page from <a href="visualizer.html">visualizer.html</a>, <a href="visualizer.css">visualizer.css</a> and <a href="visualizer.js">visualizer.js</a>).</p>
</main>
<script>
{viz_js}
</script>
</body>
</html>
"""

with open(os.path.join(HERE, "index.html"), "w") as f:
    f.write(html)
print("wrote index.html", len(html), "bytes")
