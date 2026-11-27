#!/usr/bin/env python3
"""Build index.html for the r/Decoders "Weird code on class chalkboard" post.

Run with /opt/homebrew/bin/python3.11 (needs Pillow).
Crops are cut from chalkboard.jpg using hand-checked boxes in original pixel
coordinates (3000x4000 photo).
"""
import base64, html, io, json, os
from collections import Counter
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PHOTO = os.path.join(HERE, "chalkboard.jpg")
IMG = os.path.join(HERE, "img")
os.makedirs(IMG, exist_ok=True)

im = Image.open(PHOTO).convert("RGB")

# ---------------------------------------------------------------- words
# (plaintext word, glyph transcription, box) grouped by board line
LINES = [
    [("THE", "⊥ H ≡", (745, 1235, 1010, 1372)),
     ("10", "1 0", (1095, 1245, 1280, 1360)),
     ("COMMANDS!", "Ↄ ō m m 5 n ᗡ 8 !", (1350, 1262, 2080, 1405))],
    [("I", "!", (780, 1445, 840, 1580)),
     ("SHALL", "8 H 5 7 7", (895, 1460, 1282, 1592)),
     ("NOT", "n ō ⊥", (1315, 1472, 1580, 1592)),
     ("STILL", "8 ⊥ ! 7 7", (1645, 1478, 1990, 1650))],
    [("I", "!", (785, 1645, 835, 1790)),
     ("SHALL", "8 H 5 7 7", (888, 1662, 1248, 1772)),
     ("NOT", "n ō ⊥", (1303, 1662, 1542, 1778)),
     ("KILL", "ꓘ ! 7 7", (1596, 1676, 1858, 1795))],
    [("I", "!", (790, 1868, 835, 1960)),
     ("SHALL", "8 H 5 7 7", (905, 1868, 1312, 1978)),
     ("NOT", "n ō ⊥", (1352, 1868, 1632, 1998))],
    [("COMMIT", "Ↄ ō m m ! ⊥", (1062, 2000, 1592, 2112))],
    [("ADULTERY", "5 ᗡ ∩ 7 ⊥ ≡ 12 4", (1328, 2138, 1870, 2252))],
    [("WE", "W ≡", (808, 2398, 1002, 2522)),
     ("US", "∩ 8", (1052, 2398, 1202, 2512)),
     ("A", "5", (1236, 2400, 1326, 2512)),
     ("STUDENT", "8 ⊥ ∩ ᗡ ≡ n ⊥", (1372, 2398, 1952, 2522))],
    [("REMEMBER", "12 ≡ m ≡ m 13 ≡ 12", (822, 2558, 1652, 2700))],
]

# ---------------------------------------------------------------- key
# letter -> (box of a clean sample, short glyph name, how it is made)
KEY = [
    ("A", (1240, 2405, 1322, 2510), "5", "digit 5 stands in for A"),
    ("B", (1298, 2565, 1402, 2692), "13", "B split apart: stem + bumps = “1” + “3”"),
    ("C", (1068, 2005, 1155, 2100), "Ↄ·", "mirrored C, with a dot inside"),
    ("D", (1617, 2420, 1696, 2525), "ᗡ·", "mirrored D (bowl on the left, stem on the right), with a dot inside"),
    ("E", (912, 2572, 985, 2655), "≡", "E with its spine left off: three bars"),
    ("H", (988, 1470, 1062, 1555), "H", "unchanged"),
    ("I", (785, 1655, 835, 1790), "!", "lower-case i turned upside down (dot at the bottom)"),
    ("K", (1598, 1680, 1695, 1785), "ꓘ", "mirrored K"),
    ("L", (1145, 1878, 1218, 1965), "7", "L turned 180° (⅂), which reads as a 7"),
    ("M", (985, 2568, 1092, 2668), "m", "peaked roof over three legs: a pointed lower-case m"),
    ("N", (1765, 2412, 1876, 2515), "n", "peaked roof over two legs: a pointed lower-case n"),
    ("O", (1468, 1882, 1550, 1985), "ō", "O with a bar over it"),
    ("R", (1520, 2575, 1645, 2690), "12", "R split apart: stem + bowl-and-leg = “1” + “2”"),
    ("S", (1128, 2405, 1198, 2505), "8", "digit 8 stands in for S"),
    ("T", (1460, 2428, 1552, 2512), "⊥", "T turned upside down"),
    ("U", (1060, 2405, 1128, 2500), "∩", "U turned upside down"),
    ("W", (812, 2405, 925, 2518), "W", "unchanged (seen only once)"),
    ("Y", (1785, 2140, 1865, 2250), "4", "a squared-off y shaped like a 4 (Ч); partly covered by the tree"),
]

CONTEXT_BOX = (690, 0, 3000, 1090)       # jail / Cardiac Arrest / policeman
TEXT_BOX = (700, 1180, 2200, 3200)       # whole enciphered block + heart


def save(img, name, maxw=None, q=86):
    if maxw and img.width > maxw:
        img = img.resize((maxw, round(img.height * maxw / img.width)), Image.LANCZOS)
    img.save(os.path.join(IMG, name), quality=q)
    return "img/" + name


def crop(box, name, scale=0.5, q=88):
    c = im.crop(box)
    c = c.resize((max(1, round(c.width * scale)), max(1, round(c.height * scale))), Image.LANCZOS)
    c.save(os.path.join(IMG, name), quality=q)
    return "img/" + name, c.width, c.height


# full photo (display copy) + regions
text_src = save(im.crop(TEXT_BOX), "text-block.jpg", maxw=1000, q=86)
ctx_src = save(im.crop(CONTEXT_BOX), "drawings.jpg", maxw=1100, q=84)

# word crops
word_html = []
wi = 0
for li, line in enumerate(LINES):
    cells = []
    for word, glyphs, box in line:
        src, w, h = crop(box, f"w{wi:02d}.jpg", scale=0.42)
        wi += 1
        cells.append(
            f'<figure class="word"><img src="{src}" width="{w}" height="{h}" alt="{html.escape(word)} in the chalk alphabet">'
            f'<figcaption><span class="gl">{html.escape(glyphs)}</span><b>{html.escape(word)}</b></figcaption></figure>')
    word_html.append(f'<div class="bline"><span class="ln">{li + 1}</span>{"".join(cells)}</div>')

# key crops + glyph data for the encoder
plain_letters = "".join(w for line in LINES for w, _, _ in line if w != "10")
counts = Counter(ch for ch in plain_letters if ch.isalpha())
key_rows, enc = [], {}
for letter, box, name, how in KEY:
    src, w, h = crop(box, f"g_{letter}.jpg", scale=0.62, q=90)
    enc[letter] = {"src": src, "w": w, "h": h}
    key_rows.append(
        f'<tr><td class="L">{letter}</td><td class="gimg"><img src="{src}" width="{w}" height="{h}" alt="glyph for {letter}"></td>'
        f'<td class="gn">{html.escape(name)}</td><td>{html.escape(how)}</td><td class="n">{counts[letter]}</td></tr>')

missing = [c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if c not in dict((k[0], 1) for k in KEY)]

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Weird code on class chalkboard: deciphered</title>
<style>
:root{{--bg:#fbfaf7;--panel:#fff;--ink:#1f2328;--muted:#667085;--line:#e5e1d8;--soft:#f3f0e8;
  --accent:#2f6b55;--blue:#2a6f97;--good:#2f7d4f;--good-soft:#e1f1e7;--warn:#a16207;--warn-soft:#fbefd0;
  --board:#2e4a43;--chalk:#f1e3b4;--mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace}}
@media (prefers-color-scheme:dark){{:root{{--bg:#14171a;--panel:#1b1f23;--ink:#e6e8ea;--muted:#9aa4af;--line:#2c333a;
  --soft:#22272c;--accent:#7cc4a6;--blue:#6db3dc;--good:#6cc08b;--good-soft:#1c3025;--warn:#e0b050;--warn-soft:#3a3018}}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}}
header,main{{max-width:1100px;margin:0 auto;padding:0 22px}}
header{{padding-top:28px}}
h1{{font-size:27px;margin:0 0 4px;letter-spacing:-.01em}}
.sub{{color:var(--muted);font-size:14px}}
h2{{font-size:21px;margin:0 0 8px}}
section{{margin-top:40px}}
a{{color:var(--blue)}}
.status{{display:inline-block;background:var(--good-soft);color:var(--good);border:1px solid var(--good);border-radius:6px;padding:5px 10px;font-weight:600;margin-top:12px}}
.muted{{color:var(--muted)}} .small{{font-size:13px}}
code{{font-family:var(--mono);background:var(--soft);padding:1px 5px;border-radius:4px;font-size:13px}}
.answer{{background:var(--board);color:var(--chalk);border-radius:10px;padding:22px 26px;font:600 22px/1.5 "Chalkboard SE","Comic Sans MS",ui-rounded,sans-serif;
  letter-spacing:.06em;white-space:pre-line;box-shadow:inset 0 0 0 6px #d9d5cc33}}
.answer .sic{{opacity:.75;font-weight:400;font-size:15px;letter-spacing:0}}
.twocol{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:22px;align-items:start}}
@media (max-width:820px){{.twocol{{grid-template-columns:1fr}}}}
figure{{margin:0}}
.photo img{{width:100%;height:auto;border-radius:8px;border:1px solid var(--line);display:block}}
.photo figcaption{{font-size:13px;color:var(--muted);margin-top:6px}}
.bline{{display:flex;flex-wrap:wrap;gap:10px 14px;align-items:flex-end;padding:12px 0;border-bottom:1px solid var(--line)}}
.bline .ln{{width:22px;color:var(--muted);font-size:12px;align-self:center}}
.word img{{display:block;max-width:100%;height:auto;border-radius:5px}}
.word figcaption{{display:flex;flex-direction:column;align-items:center;margin-top:4px}}
.word .gl{{font-family:var(--mono);font-size:12px;color:var(--muted)}}
.word b{{font-size:16px;letter-spacing:.12em;color:var(--accent)}}
table{{border-collapse:collapse;width:100%;background:var(--panel);border:1px solid var(--line);border-radius:8px;overflow:hidden;font-size:14px}}
th,td{{padding:6px 10px;border-bottom:1px solid var(--line);text-align:left;vertical-align:middle}}
th{{background:var(--soft);font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.03em}}
tr:last-child td{{border-bottom:0}}
td.L{{font:700 20px var(--mono);color:var(--accent);width:44px;text-align:center}}
td.gimg{{width:90px}} td.gimg img{{display:block;border-radius:4px}}
td.gn{{font-family:var(--mono);font-size:17px;width:60px}}
td.n,th.n{{text-align:right;font-variant-numeric:tabular-nums;width:60px}}
.groups{{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px;margin-top:14px}}
.card{{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:10px 14px}}
.card h3{{margin:0 0 4px;font-size:14px}}
.card p{{margin:0;font-size:13.5px}}
ul.notes li{{margin:6px 0}}
.note{{background:var(--warn-soft);border-left:4px solid var(--warn);padding:8px 12px;border-radius:4px;font-size:14px}}
#enc-in{{width:100%;font:16px var(--mono);padding:8px 10px;border:1px solid var(--line);border-radius:6px;background:var(--panel);color:var(--ink);text-transform:uppercase}}
#enc-out{{background:var(--board);border-radius:10px;padding:14px;margin-top:10px;min-height:80px;display:flex;flex-wrap:wrap;align-items:flex-end;gap:2px 1px}}
#enc-out img{{height:46px;width:auto;border-radius:2px}}
#enc-out .sp{{width:22px}} #enc-out .br{{flex-basis:100%;height:6px}}
#enc-out .x{{height:46px;min-width:26px;display:inline-flex;align-items:center;justify-content:center;color:#f1e3b4aa;border:1px dashed #f1e3b466;border-radius:3px;font:600 18px var(--mono);padding:0 4px}}
footer{{max-width:1100px;margin:50px auto 60px;padding:0 22px;font-size:13px;color:var(--muted)}}
</style>
</head>
<body>
<header>
<h1>Weird code on class chalkboard: deciphered</h1>
<div class="sub">Source: <a href="https://www.reddit.com/r/Decoders/comments/1y66thf/weird_code_on_class_chalkboard/">“Weird code on class chalkboard”</a>,
r/Decoders, posted by <a href="https://www.reddit.com/user/Heyxlistenx/">u/Heyxlistenx</a>. Photo from that post.</div>
<div class="status">Solved: a home-made “look-alike” alphabet, one glyph per letter</div>
</header>
<main>

<section id="answer">
<h2>What it says</h2>
<div class="answer">THE 10 COMMANDS!
I SHALL NOT STILL <span class="sic">[sic: the commandment is “steal”]</span>
I SHALL NOT KILL
I SHALL NOT COMMIT ADULTERY
WE US A STUDENT
REMEMBER
♥</div>
<p class="muted small">Every glyph on the board fits one key, with no leftovers. The two odd spots, STILL and “WE US”, are written that way on the board and are not decoding errors (see <a href="#loose">loose ends</a>).</p>
</section>

<section id="board" class="twocol">
<figure class="photo"><a href="chalkboard.jpg"><img src="{text_src}" alt="the enciphered block on the chalkboard"></a>
<figcaption>The enciphered block (click for the full 3000×4000 photo).</figcaption></figure>
<div>
<h2>How it was cracked</h2>
<p>Three lines start with the same run of glyphs, <code>! 8H577 nō⊥</code>: a 1-letter word, a 5-letter word ending in a double letter, and a 3-letter word.
That run is <b>I SHALL NOT</b>, and the words after it confirm it: <code>ꓘ!77</code> = KILL and <code>Ↄōmm!⊥ 5ᗡ∩7⊥≡12 4</code> = COMMIT ADULTERY.
The heading <code>⊥H≡ 10 Ↄōmm5nᗡ8!</code> then reads <b>THE 10 COMMANDS!</b>.</p>
<p>Those three lines give the key for 16 letters. The last two lines then read straight off it (<b>WE US A STUDENT / REMEMBER</b>).
The only new glyphs there are <b>W</b>, which is drawn normally, and <code>13</code> = <b>B</b>, which is drawn like the <code>12</code> = R next to it.</p>
<p>There is no key, shift or transposition. Each letter is just drawn in a disguised form: turned upside down, mirrored, broken into pieces, or swapped for a digit that looks a bit like it.</p>
<figure class="photo" style="margin-top:14px"><img src="{ctx_src}" alt="drawings above the code: jail, Cardiac Arrest heart, policeman">
<figcaption>Above the code, the same board has crime-and-punishment cartoons: a stick figure in JAIL, a heart holding handcuffs (“Cardiac Arrest”), and a policeman.
A list of “shall not” rules fits that theme.</figcaption></figure>
</div>
</section>

<section id="lines">
<h2>Line by line</h2>
<p class="muted small">Each word is cut from the photo. Under each word: my glyph transcription, then the plaintext.</p>
{''.join(word_html)}
</section>

<section id="key">
<h2>The alphabet</h2>
<p>Each sample is cut from the board. “Count” is how many times the letter appears in the decoded text.</p>
<table>
<thead><tr><th>Letter</th><th>Glyph</th><th></th><th>How it is made</th><th class="n">Count</th></tr></thead>
<tbody>
{''.join(key_rows)}
</tbody></table>
<p class="muted small">Not on the board, so unknown: {' '.join(missing)}. The heading's “10” is written in ordinary digits: its 0 has no bar, unlike every lettered O.</p>
<div class="groups">
<div class="card"><h3>Turned 180°</h3><p>T → ⊥, U → ∩, i → !, L → 7</p></div>
<div class="card"><h3>Mirrored</h3><p>C → Ↄ, D → ᗡ, K → ꓘ (C and D also get a dot)</p></div>
<div class="card"><h3>Broken apart</h3><p>E → ≡ (no spine), B → 1 3, R → 1 2</p></div>
<div class="card"><h3>Digit stand-ins</h3><p>A → 5, S → 8, Y → 4</p></div>
<div class="card"><h3>Peaked lower case</h3><p>m and n drawn as a roof over 3 or 2 legs</p></div>
<div class="card"><h3>Barely changed</h3><p>O gets an overbar; H and W are drawn normally</p></div>
</div>
</section>

<section id="loose">
<h2>Loose ends</h2>
<ul class="notes">
<li><b>STILL, not STEAL.</b> The word is <code>8⊥!77</code> = S‑T‑I‑L‑L. The writer's E (<code>≡</code>) appears {counts['E']} times elsewhere and is not used here, so the misspelling is on the board, not in the decoding.
It is either a slip (“steal”/“still”) or a joke.</li>
<li><b>“WE US A STUDENT”.</b> <code>∩</code> must be U, because it is the U in both ADULTERY and STUDENT. So <code>∩8</code> can only be US, and the line really does say “WE US A STUDENT / REMEMBER”.
The board does not show what was meant (maybe “we, as a student, remember…”, or deliberately broken English to match the STILL joke).</li>
<li><b>COMMANDS, not COMMANDMENTS.</b> Only eight glyphs follow the 10: <code>Ↄ ō m m 5 n ᗡ 8</code>. A small ✓ touches the foot of the D. It belongs to the trail of check marks below, not to the word.</li>
<li><b>Check marks.</b> About six ✓ marks trail down from the end of line 1, across the end of STILL, toward the trees.
None of them is needed for any word. They may be someone ticking the STILL line, or birds belonging to the moon-and-pines drawing.</li>
<li><b>Specks under the lines</b> are irregular chalk crumbs. They do not line up with the letters and carry no pattern.
The dark band behind THE is an eraser smear. The chalk over it is crisp, so the smear came first.
In THE the T's two strokes don't touch and the H's crossbar is only a dot; on the other lines H has a full crossbar.</li>
<li><b>Small glyph variants.</b> The I in line 4 is a plain stroke with no dot. The first R of REMEMBER has its “2” redrawn. The Y at the end of ADULTERY runs into the base of the left pine.</li>
</ul>
</section>

<section id="encode">
<h2>Write in it</h2>
<p class="muted small">Type text to render it with glyphs cut from the board. Letters the board never uses (F G J P Q V X Z) show as dashed boxes.</p>
<input id="enc-in" value="I shall not steal" maxlength="120" aria-label="text to encode">
<div id="enc-out" aria-live="polite"></div>
</section>

</main>
<footer>
Photo and puzzle: u/Heyxlistenx on <a href="https://www.reddit.com/r/Decoders/comments/1y66thf/weird_code_on_class_chalkboard/">r/Decoders</a>.
Page generated by <code>build_report.py</code> from <code>chalkboard.jpg</code>.
</footer>
<script>
const G = {json.dumps(enc)};
const inp = document.getElementById('enc-in'), out = document.getElementById('enc-out');
function render(){{
  out.textContent = '';
  for (const ch of inp.value.toUpperCase()){{
    if (ch === ' '){{ const s=document.createElement('span'); s.className='sp'; out.appendChild(s); continue; }}
    if (ch === '\\n'){{ const s=document.createElement('span'); s.className='br'; out.appendChild(s); continue; }}
    const g = G[ch];
    if (g){{ const im=document.createElement('img'); im.src=g.src; im.alt=ch; im.title=ch; out.appendChild(im); }}
    else {{ const s=document.createElement('span'); s.className='x'; s.textContent=ch; s.title='not on the board'; out.appendChild(s); }}
  }}
}}
inp.addEventListener('input', render); render();
</script>
</body>
</html>
"""

with open(os.path.join(HERE, "index.html"), "w") as f:
    f.write(page)
print("wrote index.html;", wi, "word crops;", len(KEY), "key glyphs; counts", dict(counts))
