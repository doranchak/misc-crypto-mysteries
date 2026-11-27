#!/usr/bin/env python3
"""Build index.html for the r/codes post "Anyone recognize this code?" (marker on a monitor bezel).

Run with /opt/homebrew/bin/python3.11 (needs opencv-python + numpy).
Glyph boxes are hand-checked, in the coordinates of the photo after deskewing it by
-2.6 degrees about its centre (the bezel is tilted in the photo).
"""
import html, json, os
from collections import Counter, OrderedDict

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PHOTO = os.path.join(HERE, "monitor.jpg")
IMG = os.path.join(HERE, "img")
os.makedirs(IMG, exist_ok=True)
THREAD = "https://www.reddit.com/r/codes/comments/1y6pz29/anyone_recognize_this_code/"
USER = "https://www.reddit.com/user/DrunkensAndDragons/"

im = cv2.imread(PHOTO)
h, w = im.shape[:2]
M = cv2.getRotationMatrix2D((w / 2, h / 2), -2.6, 1.0)
rot = cv2.warpAffine(im, M, (w, h), borderValue=(255, 255, 255))


def enhance(img, clip=2.5, tiles=(16, 16)):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l = cv2.createCLAHE(clipLimit=clip, tileGridSize=tiles).apply(l)
    return cv2.cvtColor(cv2.merge([l, a, b]), cv2.COLOR_LAB2BGR)


rot_e = enhance(rot)
# the right end of line 2 is in shadow: denoise + stronger local contrast there
dim = rot[440:620, 2300:2796].copy()
dim = cv2.fastNlMeansDenoisingColored(dim, None, 6, 6, 7, 21)
rot_dim = rot_e.copy()
rot_dim[440:620, 2300:2796] = enhance(dim, clip=3.0, tiles=(4, 8))

# ---------------------------------------------------------------- glyphs
# (line, index, letter, x0, x1, y0, y1, shape-class name)
L1, L2, L3, L2D = (392, 535), (520, 642), (648, 757), (478, 598)
L3R = (626, 739)  # right half of line 3 sits closer to the bezel edge
G = [
    (1, 1, "N", 225, 425, *L1, "ring on a Z-stroke"), (1, 2, "O", 425, 480, *L1, "dot"),
    (1, 3, "F", 495, 600, *L1, "crossed loop over triangle"), (1, 4, "A", 615, 695, *L1, "head-loop-stem"),
    (1, 5, "P", 695, 775, *L1, "head-loop-triangle"),
    (1, 6, "T", 910, 1045, *L1, "arch over triangle"), (1, 7, "O", 1045, 1105, *L1, "dot"),
    (1, 8, "P", 1215, 1300, *L1, "head-loop-triangle"), (1, 9, "O", 1300, 1355, *L1, "dot"),
    (1, 10, "W", 1365, 1440, *L1, "loop on stem, arms up"), (1, 11, "E", 1440, 1535, *L1, "ring with two strokes"),
    (1, 12, "R", 1560, 1650, *L1, "head-loop-stem with tick"),
    (1, 13, "I", 1755, 1890, *L1, "ring on a bar"), (1, 14, "M", 1885, 1955, *L1, "A with looped crossbar"),
    (1, 15, "B", 1970, 2055, *L1, "8 with blobs and tick"), (1, 16, "A", 2060, 2115, *L1, "head-loop-stem"),
    (1, 17, "L", 2115, 2215, *L1, "loop and flag"), (1, 18, "A", 2230, 2305, *L1, "head-loop-stem (legs)"),
    (1, 19, "N", 2300, 2410, *L1, "ring on a Z-stroke (joined)"), (1, 20, "C", 2415, 2515, *L1, "ring with tail"),
    (1, 21, "E", 2525, 2630, *L1, "ring with two strokes"), (1, 22, "S", 2630, 2760, *L1, "§ with top bar"),
    (2, 1, "O", 240, 300, *L2, "dot"), (2, 2, "N", 315, 445, *L2, "ring on a Z-stroke"),
    (2, 3, "L", 445, 565, *L2, "loop and flag"), (2, 4, "Y", 580, 685, *L2, "stem, ring, wings"),
    (2, 5, "T", 795, 925, *L2, "arch over triangle"), (2, 6, "O", 940, 995, *L2, "dot"),
    (2, 7, "C", 1140, 1230, *L2, "ring with tail"), (2, 8, "O", 1235, 1290, *L2, "dot"),
    (2, 9, "N", 1300, 1435, *L2, "ring on a Z-stroke"), (2, 10, "S", 1430, 1522, *L2, "§ with top bar"),
    (2, 11, "E", 1505, 1600, *L2, "ring with two strokes"), (2, 12, "N", 1595, 1725, *L2, "ring on a Z-stroke"),
    (2, 13, "T", 1740, 1855, *L2, "arch over triangle (kite)"), (2, 14, "I", 1865, 2005, *L2, "ring on a bar"),
    (2, 15, "N", 2005, 2140, *L2, "ring on a Z-stroke"), (2, 16, "G", 2150, 2275, *L2, "ring with hooked tail"),
    (2, 17, "J", 2360, 2470, *L2D, "bars and hook"), (2, 18, "O", 2475, 2518, *L2D, "dot"),
    (2, 19, "Y", 2512, 2595, *L2D, "stem, ring, wings"), (2, 20, "F", 2592, 2650, *L2D, "crossed loop over triangle"),
    (2, 21, "U", 2645, 2705, *L2D, "loop with rising stem"), (2, 22, "L", 2700, 2790, *L2D, "loop and flag"),
    (3, 1, "B", 230, 312, *L3, "8 with blobs and tick"), (3, 2, "E", 312, 405, *L3, "ring with two strokes"),
    (3, 3, "A", 418, 478, *L3, "head-loop-stem"), (3, 4, "U", 478, 535, *L3, "loop with rising stem"),
    (3, 5, "T", 535, 655, *L3, "arch over triangle (winged)"), (3, 6, "Y", 655, 765, *L3, "stem, ring, wings"),
    (3, 7, "&", 875, 975, *L3, "ampersand"),
    (3, 8, "A", 1058, 1115, *L3R, "head-loop-stem"), (3, 9, "E", 1115, 1195, *L3R, "ring with two strokes"),
    (3, 10, "S", 1195, 1265, *L3R, "§ with top bar"), (3, 11, "T", 1265, 1368, *L3R, "arch over triangle"),
    (3, 12, "E", 1372, 1460, *L3R, "ring with two strokes"), (3, 13, "T", 1468, 1588, *L3R, "arch over triangle"),
    (3, 14, "I", 1588, 1705, *L3R, "ring on a bar"), (3, 15, "C", 1705, 1785, *L3R, "ring with tail"),
    (3, 16, "S", 1780, 1858, *L3R, "§ with top bar"),
]
DIM = {(2, i) for i in range(17, 23)}
# words: (line, first index, last index)
WORDS = [(1, 1, 5), (1, 6, 7), (1, 8, 12), (1, 13, 22),
         (2, 1, 4), (2, 5, 6), (2, 7, 16), (2, 17, 22),
         (3, 1, 6), (3, 7, 7), (3, 8, 16)]
gl = {(g[0], g[1]): g for g in G}

TILE_H = 120  # stored height (shown at 60 css px)


def tile(g, name):
    ln, i, letter, x0, x1, y0, y1, _ = g
    src = rot_dim if (ln, i) in DIM else rot_e
    c = src[y0:y1, x0:x1]
    s = TILE_H / c.shape[0]
    c = cv2.resize(c, (max(1, round(c.shape[1] * s)), TILE_H), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(os.path.join(IMG, name), c, [cv2.IMWRITE_JPEG_QUALITY, 88])
    return "img/" + name, c.shape[1] // 2, TILE_H // 2


tiles = {}
for g in G:
    tiles[(g[0], g[1])] = tile(g, f"g{g[0]}_{g[1]:02d}.jpg")

# display photo + deskewed strip
disp = cv2.resize(im, (1400, round(h * 1400 / w)), interpolation=cv2.INTER_AREA)
cv2.imwrite(os.path.join(IMG, "photo.jpg"), disp, [cv2.IMWRITE_JPEG_QUALITY, 84])
strip = rot_dim[372:800, 200:2796]
strip = cv2.resize(strip, (1600, round(strip.shape[0] * 1600 / strip.shape[1])), interpolation=cv2.INTER_AREA)
cv2.imwrite(os.path.join(IMG, "strip.jpg"), strip, [cv2.IMWRITE_JPEG_QUALITY, 86])

# ---------------------------------------------------------------- lines
word_text = []
line_html = OrderedDict()
for ln, a, b in WORDS:
    gs = [gl[(ln, i)] for i in range(a, b + 1)]
    word = "".join(g[2] for g in gs)
    word_text.append((ln, word))
    cells = []
    for g in gs:
        src, tw, th = tiles[(g[0], g[1])]
        cls = "gt dim" if (g[0], g[1]) in DIM else "gt"
        cells.append(f'<figure class="{cls}"><img src="{src}" width="{tw}" height="{th}" alt="glyph {g[0]}.{g[1]}, read as {html.escape(g[2])}" title="L{g[0]}.{g[1]}: {html.escape(g[7])}">'
                     f'<figcaption>{html.escape(g[2])}</figcaption></figure>')
    sic = ' <span class="sic">[sic]</span>' if word == "AESTETICS" else ""
    line_html.setdefault(ln, []).append(f'<div class="word"><div class="glyphs">{"".join(cells)}</div><div class="wl">{html.escape(word)}{sic}</div></div>')
lines_block = "".join(f'<div class="bline"><span class="ln">{ln}</span>{"".join(ws)}</div>' for ln, ws in line_html.items())

# ---------------------------------------------------------------- key
DESC = {
    "A": "Filled head over a small loop on a stem (like ♀). Also drawn with two little legs (L1.18) and with the loop squeezed shut (L3.8).",
    "B": "An 8 with filled blobs at top and bottom and a tick to the right.",
    "C": "Small ring with a tail to the right (o–).",
    "E": "Ring with two strokes to the right (o=). In L1.21 the upper stroke floats free.",
    "F": "Loop crossed by a bar, over a filled down-pointing triangle; the crossed loop is like a cursive f. The second F (L2.20) is in shadow.",
    "G": "Ring whose tail runs right and then turns down.",
    "I": "Ring threaded on a horizontal bar (–o–).",
    "J": "Two short bars, then a hook like a 9. Only once, in the shadowed end of line 2.",
    "L": "Loop at lower left rising into a filled triangle: a looped ℓ with a flag.",
    "M": "An A shape with a loop where the crossbar would be.",
    "N": "Ring on a Z-shaped stroke: the left end hooks down, the right end hooks up. In L1.19 the left hook is replaced by the stroke joining it to the A before it.",
    "O": "A filled dot.",
    "P": "Filled head, loop, and a filled triangle hanging down to the left.",
    "R": "The A shape (head, loop, stem) with a tick to the right.",
    "S": "A §-like squiggle with a bar across the top.",
    "T": "Filled down-pointing triangle with an arch or loop on top. Drawn compact as a kite (L2.13) and spread out like wings (L3.5).",
    "U": "Loop at the bottom with a stem rising on the right (like ꝺ).",
    "W": "Loop on a stem with two arms raised (like ψ).",
    "Y": "Stem on top, then a ring, then two filled wings.",
    "&": "An ordinary ampersand.",
}
letters_all = "".join(g[2] for g in G)
counts = Counter(letters_all)
words_with = {}
for ln, word in word_text:
    for ch in set(word):
        words_with.setdefault(ch, []).append(word)
key_rows = []
enc = {}
REP = {"A": (1, 4), "B": (3, 1), "C": (1, 20), "E": (3, 9), "F": (1, 3), "G": (2, 16), "I": (1, 13), "J": (2, 17),
       "L": (2, 3), "M": (1, 14), "N": (2, 2), "O": (2, 1), "P": (1, 5), "R": (1, 12), "S": (3, 10), "T": (1, 6),
       "U": (3, 4), "W": (1, 10), "Y": (2, 4), "&": (3, 7)}
for letter in sorted(REP, key=lambda c: (c == "&", c)):
    occ = [g for g in G if g[2] == letter]
    imgs = "".join(f'<img src="{tiles[(g[0], g[1])][0]}" width="{tiles[(g[0], g[1])][1]}" height="{tiles[(g[0], g[1])][2]}" alt="{letter}" title="L{g[0]}.{g[1]}">' for g in occ)
    ws = ", ".join(sorted(set(words_with.get(letter, [])), key=lambda x: [wd for _, wd in word_text].index(x)))
    key_rows.append(f'<tr><td class="L">{html.escape(letter)}</td><td class="occ">{imgs}</td><td>{html.escape(DESC[letter])}</td>'
                    f'<td class="ws">{html.escape(ws)}</td><td class="n">{counts[letter]}</td></tr>')
    src, tw, th = tiles[REP[letter]]
    enc[letter] = {"src": src, "w": tw, "h": th}
missing = [c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if c not in REP]
n_glyphs = len(G)
n_letters = len([c for c in REP if c != "&"])
multi = sum(1 for c, ws in words_with.items() if c != "&" and len(set(ws)) >= 2)
singles = sorted(c for c, ws in words_with.items() if c != "&" and len(set(ws)) < 2)

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Marker code on a monitor bezel: deciphered</title>
<style>
:root{{--bg:#fbfaf7;--panel:#fff;--ink:#1f2328;--muted:#667085;--line:#e5e1d8;--soft:#f3f0e8;
  --accent:#7a3e9d;--blue:#2a6f97;--good:#2f7d4f;--good-soft:#e1f1e7;--warn:#a16207;--warn-soft:#fbefd0;
  --bezel:#d9d9db;--marker:#8e3fb0;--mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace}}
@media (prefers-color-scheme:dark){{:root{{--bg:#14171a;--panel:#1b1f23;--ink:#e6e8ea;--muted:#9aa4af;--line:#2c333a;
  --soft:#22272c;--accent:#c79be3;--blue:#6db3dc;--good:#6cc08b;--good-soft:#1c3025;--warn:#e0b050;--warn-soft:#3a3018;--bezel:#c9c9cc}}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}}
header,main{{max-width:1180px;margin:0 auto;padding:0 22px}}
header{{padding-top:28px}}
h1{{font-size:27px;margin:0 0 4px;letter-spacing:-.01em}}
.sub{{color:var(--muted);font-size:14px}}
h2{{font-size:21px;margin:0 0 8px}}
section{{margin-top:40px}}
a{{color:var(--blue)}}
.status{{display:inline-block;background:var(--good-soft);color:var(--good);border:1px solid var(--good);border-radius:6px;padding:5px 10px;font-weight:600;margin-top:12px}}
.muted{{color:var(--muted)}} .small{{font-size:13px}}
code{{font-family:var(--mono);background:var(--soft);padding:1px 5px;border-radius:4px;font-size:13px}}
.answer{{background:linear-gradient(#e4e4e6,#cfcfd2);color:var(--marker);border-radius:10px;padding:22px 26px;font:700 24px/1.55 "Marker Felt","Chalkboard SE",ui-rounded,sans-serif;
  letter-spacing:.07em;white-space:pre-line;border:1px solid #b9b9bd}}
.answer .sic{{opacity:.7;font-weight:400;font-size:15px;letter-spacing:0;color:#444}}
.reading{{margin-top:10px;font-size:15.5px}}
figure{{margin:0}}
.photo img{{width:100%;height:auto;border-radius:8px;border:1px solid var(--line);display:block}}
.photo figcaption{{font-size:13px;color:var(--muted);margin-top:6px}}
.twocol{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:22px;align-items:start}}
@media (max-width:860px){{.twocol{{grid-template-columns:1fr}}}}
.bline{{display:flex;flex-wrap:wrap;gap:12px 22px;align-items:flex-end;padding:14px 0;border-bottom:1px solid var(--line)}}
.bline .ln{{width:22px;color:var(--muted);font-size:12px;align-self:center}}
.word{{display:flex;flex-direction:column;align-items:center}}
.glyphs{{display:flex;gap:3px;align-items:flex-end;background:var(--bezel);padding:4px;border-radius:6px}}
.gt img{{display:block;border-radius:3px}}
.gt figcaption{{text-align:center;font:700 13px var(--mono);color:#333;margin-top:2px}}
.gt.dim figcaption{{color:#a16207}}
.wl{{margin-top:5px;font-size:16px;font-weight:700;letter-spacing:.12em;color:var(--accent)}}
.wl .sic{{font-weight:400;font-size:12px;letter-spacing:0;color:var(--muted)}}
table{{border-collapse:collapse;width:100%;background:var(--panel);border:1px solid var(--line);border-radius:8px;overflow:hidden;font-size:14px}}
th,td{{padding:6px 10px;border-bottom:1px solid var(--line);text-align:left;vertical-align:middle}}
th{{background:var(--soft);font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.03em}}
tr:last-child td{{border-bottom:0}}
td.L{{font:700 20px var(--mono);color:var(--accent);width:44px;text-align:center}}
td.occ{{background:var(--bezel);width:330px}} td.occ img{{height:44px;width:auto;margin:2px;border-radius:3px;vertical-align:middle}}
td.ws{{font-size:12.5px;color:var(--muted);width:200px}}
td.n,th.n{{text-align:right;font-variant-numeric:tabular-nums;width:54px}}
ol.steps li,ul.notes li{{margin:7px 0}}
.note{{background:var(--warn-soft);border-left:4px solid var(--warn);padding:8px 12px;border-radius:4px;font-size:14px}}
.stat{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin-top:12px}}
.card{{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:10px 14px}}
.card b{{display:block;font-size:22px;color:var(--accent)}}
.card span{{font-size:13px;color:var(--muted)}}
#enc-in{{width:100%;font:16px var(--mono);padding:8px 10px;border:1px solid var(--line);border-radius:6px;background:var(--panel);color:var(--ink);text-transform:uppercase}}
#enc-out{{background:var(--bezel);border-radius:10px;padding:14px;margin-top:10px;min-height:80px;display:flex;flex-wrap:wrap;align-items:flex-end;gap:2px 1px}}
#enc-out img{{height:48px;width:auto;border-radius:2px}}
#enc-out .sp{{width:24px}} #enc-out .br{{flex-basis:100%;height:6px}}
#enc-out .x{{height:48px;min-width:26px;display:inline-flex;align-items:center;justify-content:center;color:#555;border:1px dashed #777;border-radius:3px;font:600 18px var(--mono);padding:0 4px}}
footer{{max-width:1180px;margin:50px auto 60px;padding:0 22px;font-size:13px;color:var(--muted)}}
</style>
</head>
<body>
<header>
<h1>Marker code on a monitor bezel: deciphered</h1>
<div class="sub">Source: <a href="{THREAD}">“Anyone recognize this code?”</a>, r/codes, posted by <a href="{USER}">u/DrunkensAndDragons</a>. Photo from that post.
The poster's context: <i>“Written in marker directly on computer monitor. There is another note on computer in english, same marker, that says ‘the gods can see that which you can see’.
So a personal reminder to not look at bad things on the internet?”</i></div>
<div class="status">Solved: a home-made alphabet, one glyph per letter, in plain English</div>
</header>
<main>

<section id="answer">
<h2>What it says</h2>
<div class="answer">NOFAP TO POWER IMBALANCES
ONLY TO CONSENTING JOYFUL
BEAUTY &amp; AESTETICS <span class="sic">[sic: aesthetics, written without the H]</span></div>
<p class="reading">With punctuation: <b>“NoFap to power imbalances. Only to consenting, joyful beauty &amp; aesthetics.”</b></p>
<p>The poster's guess was close. It is a personal rule about what not to look at online. <i>NoFap</i> is the online pledge and community for abstaining from masturbation (“fap” is slang for it).
The note narrows that pledge: nothing involving power imbalances, only material that is consenting and joyful, “beauty &amp; aesthetics”.
That fits the English note in the same marker, “the gods can see that which you can see”.</p>
<p class="muted small">All {n_glyphs} glyphs fit one key: {n_letters} letters plus the &amp;, with nothing left over and no glyph read two ways.
The weakest spot is the shadowed end of line 2 (JOYFUL), but its O, Y, U and L are glyphs that already appear in clearer words (see <a href="#loose">loose ends</a>).</p>
</section>

<section id="photo" class="twocol">
<figure class="photo"><a href="monitor.jpg"><img src="img/photo.jpg" alt="the purple marker writing on the silver bottom bezel of an Apple display"></a>
<figcaption>The post's photo: purple marker on the silver bottom bezel of an Apple display (click for full size).</figcaption></figure>
<div>
<h2>How it was cracked</h2>
<ol class="steps">
<li><b>Gaps give word lengths.</b> The three lines split into words of 5·2·5·10 / 4·2·10·6 / 6·&amp;·9 glyphs. The lone <b>&amp;</b> is an ordinary ampersand, so the text is probably English.</li>
<li><b>A repeated short word.</b> The 2-glyph word <i>arch-over-triangle + dot</i> appears in the same place on lines 1 and 2. Guess <b>TO</b> (dot = O).</li>
<li><b>A crib that checks itself.</b> The 10-glyph word in line 2 has the repeat pattern <code>a b c d e c f g c h</code> (the Z-stroke ring at 3rd, 6th and 9th place).
Of the seven words in a 60,000-word English list with that pattern, only <b>CONSENTING</b> has O 2nd and T 7th. Those two letters were already fixed by TO.</li>
<li><b>The rest falls out.</b> With C O N S E T I G known, line 1's 10-glyph word reads I?BAL?NCES = <b>IMBALANCES</b>, and line 3 reads B E A U T Y = <b>BEAUTY</b> and A E S T E T I C S.
Line 2 starts O N L Y = <b>ONLY</b>, and its last word O Y ? U L can only be <b>JOYFUL</b>.</li>
<li><b>Line 1.</b> Now only four glyphs are unknown: N O ? A ? / ? O ? E ? before IMBALANCES. The crossed loop at the start is the same glyph as the 4th letter of JOYFUL, so it is <b>F</b>.
That gives <b>NOFAP</b> and <b>POWER</b>, and “power imbalances” is a common phrase.</li>
</ol>
<figure class="photo" style="margin-top:12px"><img src="img/strip.jpg" alt="the three lines of glyphs, straightened and contrast-enhanced">
<figcaption>The writing straightened (rotated 2.6°) and contrast-enhanced. The right end of line 2 is in shadow on the original.</figcaption></figure>
</div>
</section>

<section id="lines">
<h2>Line by line</h2>
<p class="muted small">Every glyph is cut from the photo, with its letter under it. Hover over a glyph for its position (L<i>line</i>.<i>glyph</i>). Amber letters are in the shadowed end of line 2.</p>
{lines_block}
</section>

<section id="key">
<h2>The alphabet</h2>
<p>Every occurrence of each letter, cut from the photo. Some glyphs look like dressed-up Latin letters (B like an 8, S like §, F a crossed loop like a cursive f, L a looped ℓ, W like ψ, O a plain dot); others look made up.
I checked Theban, Agrippa's Celestial, Malachim, Daedric, Atlantean, Kryptonian and Unown, and none of them matches, so this looks like the writer's own alphabet.</p>
<table>
<thead><tr><th>Letter</th><th>Every occurrence</th><th>Shape</th><th>Words it appears in</th><th class="n">Count</th></tr></thead>
<tbody>
{''.join(key_rows)}
</tbody></table>
<p class="muted small">Not used on the monitor, so unknown: {' '.join(missing)}.</p>
</section>

<section id="checks">
<h2>How sure is this?</h2>
<div class="stat">
<div class="card"><b>{n_glyphs} / {n_glyphs}</b><span>glyphs decoded with one key; no glyph has two readings</span></div>
<div class="card"><b>{multi} of {n_letters}</b><span>letters occur in two or more different words, so they are cross-checked (only {' '.join(singles)} appear in a single word)</span></div>
<div class="card"><b>4 of 10</b><span>blind solver restarts found exactly this key, which was also the top score</span></div>
<div class="card"><b>−135 vs ≤ −215</b><span>solver score for this text vs. the best of 10 shuffled-glyph controls</span></div>
</div>
<p>Blind check: I replaced the {n_letters} letter classes with anonymous symbols and kept the word gaps. A simulated-annealing solver, given no cribs, scored each candidate key by how well every group splits into common English words.
It found exactly this key in 4 of 10 restarts, and no other key scored as high. The same solver run on shuffled glyphs (same symbols and word lengths, order randomised) never scored better than −215, against −135 here.</p>
<p class="note">Caveat: the blind check uses my final grouping of glyph shapes into letters. A few of those groupings were settled with the decoding in hand: the joined N at L1.19, the legged A at L1.18 and squeezed A at L3.8, the kite and winged T at L2.13 and L3.5, and the shadowed F at L2.20.
The decisive steps don't depend on them. TO, CONSENTING, IMBALANCES and BEAUTY come from glyphs that are clearly the same shape.</p>
</section>

<section id="loose">
<h2>Loose ends</h2>
<ul class="notes">
<li><b>AESTETICS.</b> The last word has nine glyphs, A‑E‑S‑T‑E‑T‑I‑C‑S. Both T's are the same arch-over-triangle glyph used in TO and CONSENTING, and there is no extra glyph between them. So the H is missing on the monitor itself, not lost in the decoding (compare the US spelling <i>esthetics</i>).</li>
<li><b>Shadowed end of line 2.</b> The last six glyphs, JOYFUL, sit where the bezel is in shadow and the photo is soft.
O (dot), Y (stem-ring-wings), U (loop with rising stem) and L (loop and flag) match their clearer copies elsewhere. The 4th glyph is a blurred loop-with-bar of the same outline as the F at L1.3, and the first is a hook with two bars on its left; J is its only occurrence.
“?OY?UL” has no other English fit, so the word itself is secure even though the J and F glyphs are not well seen.</li>
<li><b>Variant forms.</b> A is drawn three ways and T three ways (see the alphabet table). N loses its left hook where it is joined to the A before it in IMBALANCES. In line 1 one E's upper stroke floats free of the ring.
None of these changes the reading of any word.</li>
<li><b>Not ink.</b> A whitish smudge sits in the gap after the first TO in line 1, and a faint grey dash sits above the E at the start of line 3. Neither is purple marker, and neither is needed for any word.</li>
</ul>
</section>

<section id="encode">
<h2>Write in it</h2>
<p class="muted small">Type text to render it with glyphs cut from the photo. Letters the monitor never uses ({' '.join(missing)}) show as dashed boxes.</p>
<input id="enc-in" value="The gods can see that which you can see" maxlength="140" aria-label="text to encode">
<div id="enc-out" aria-live="polite"></div>
</section>

</main>
<footer>
Photo and question: <a href="{USER}">u/DrunkensAndDragons</a> on <a href="{THREAD}">r/codes</a>.
Page generated by <code>build_report.py</code> from <code>monitor.jpg</code>. Solver and checks are in <code>work/</code>.
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
    else {{ const s=document.createElement('span'); s.className='x'; s.textContent=ch; s.title='not on the monitor'; out.appendChild(s); }}
  }}
}}
inp.addEventListener('input', render); render();
</script>
</body>
</html>
"""

with open(os.path.join(HERE, "index.html"), "w") as f:
    f.write(page)
print("wrote index.html;", n_glyphs, "glyphs;", n_letters, "letters;", "letters in 2+ distinct words:", multi)
print("plaintext:", " / ".join(" ".join(wd for l, wd in word_text if l == ln) for ln in (1, 2, 3)))
