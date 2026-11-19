"""Build ../../index.html: each page photo on the left, the plaintext on the right, every plaintext word
set over the cipher word it stands for (hover / click highlights the pair).

Source data: PAGES in ../../report.html (run build_html2.py first if the decipherment changed).
Geometry: geom.py (fitted line through the glyph centres of every line); font fitting happens in the
page itself (canvas text measurement), see index_template.html.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import geom

HERE = os.path.dirname(os.path.abspath(__file__))
pages = geom.build()

# cover page b4R: the "1996" line sits right under JIMANDERSEN and its box overlaps; clip the upper word so
# the two plaintext words do not collide.
for pg in pages:
    if pg['key'] != 'b4R':
        continue
    wo = [(L, w) for L in pg['lines'] for w in L['words']]
    for L, w in wo:
        if not L['wo']:
            continue
        x0, y0, x1, y1 = w['box']
        for L2, w2 in wo:
            if w2 is w:
                continue
            top = w2['box'][1] if L2['wo'] else w2['cy'] - 0.5 * L2['H']
            ox = min(x1, w2['cx'] + w2['x1'] - w2['x0']) - max(x0, w2['cx'] - (w2['x1'] - w2['x0']))
            if ox > 0 and y0 < top < y1 and top - y0 > 0.4 * (y1 - y0):
                y1 = top
        w['box'] = (x0, y0, x1, y1)
        w['cy'] = (y0 + y1) / 2
        w['H'] = y1 - y0

data = []
for pg in pages:
    lines = []
    for L in pg['lines']:
        ws = []
        for w in L['words']:
            if w['f'] == 'U':
                continue
            if L['wo']:
                x0, y0, x1, y1 = w['box']
                ws.append(dict(t=w['t'], cx=round((x0 + x1) / 2, 1), cy=round((y0 + y1) / 2, 1), sw=round(x1 - x0, 1),
                               bh=round(y1 - y0, 1), ang=0))
            else:
                ws.append(dict(t=w['t'], cx=round(w['cx'], 1), cy=round(w['cy'], 1), sw=round(w['x1'] - w['x0'], 1),
                               bh=round(1.25 * L['H'], 1), ang=round(w['ang'], 2)))
        if ws:
            H = max(w['bh'] for w in ws) if L['wo'] else L['H']
            lines.append(dict(H=round(H, 1), wo=bool(L['wo']), words=ws))
    data.append(dict(key=pg['key'], name=pg['name'], img=pg['img'], w=pg['w'], h=pg['h'], lines=lines))

import keycells as K

# index-only changes on top of the shared cells: the word IS is one fused glyph (listed after AND), and Z only occurs
# as the doubled ZZ of PIZZA (no ZZ exemplar traced yet, so the Z cell stays hatched)
_desc = dict(K.DESC)
_desc['Z'] = 'only as ZZ (PIZZA)'
_jd = list(K.JD)
_jd.insert([k for k, _, _ in _jd].index('AND') + 1, ('IS', 'IS', 'the word \u201cis\u201d'))
LETTERS = K.make_letters(_desc)
JOINED = K.make_joined(_jd)

KEY = """<section id="key">
<h2>Substitution key<small>one handwritten glyph per letter, joined in cursive; printable 16:9 version: <a href="substitution-key.html">substitution-key.html</a></small></h2>
<div class="keycard">
 <h3>Letters: find the glyph, read the letter in its box</h3>
 <div class="kgrid">%(letters)s</div>
 <h3>Single glyphs that stand for two or three letters (and the end-of-sentence mark)</h3>
 <div class="kgrid2">%(joined)s</div>
 <h3>Doubled letters: one glyph for the repeated letter</h3>
 <div class="kgrid2">%(doubles)s</div>
 <h3>Block-hand digits (the row on the back cover, left to right = 1 2 3 4 5 6 7 8 9 0)</h3>
 <div class="kgrid2 kdig">%(digits)s</div>
 <div class="knotes">
  <div><b>Source of the key.</b> Page 1 of the book comes with a partial key (blue letters over the glyphs); every other letter was checked glyph by glyph in words on pages 2&ndash;3 and on the cover pages. Two examples are shown per letter; the hand varies a little.</div>
  <div><b>Cautions.</b> J, V and X are rare; Q has not been seen, and Z only once, as the doubled ZZ of PIZZA. N and E are sometimes cut in two by the joins. Touching neighbours (IN, AN &hellip;) are <i>not</i> special glyphs.</div>
  <div><b>IS.</b> The word IS is written as one fused glyph: a slashed ellipse (the I) with a bar and zig-zag on top (THIS IS ALL, MELANIE IS OCCUPYING). In MELANIE IS A PALE it is written as a separate I and S.</div>
  <div><b>Doubled letters.</b> EE, TT, LL, SS, FF, CC and OO are each drawn as one glyph that looks like the letter with an extra stroke. TT is the T glyph with an extra line through it, and LL is the L glyph with an extra line through it (SEEM, KEEP, FEEL &middot; LITTLE, SITTING, FITTING &middot; STILL, REALLY &middot; MESS, PASSING &middot; OFFSPRING &middot; ACCIDENTAL &middot; GOOD, TOO). PP in APPARENTLY is written as two separate P&rsquo;s, and a few other doubles are ambiguous, so this list is only the pairs seen at least three times with a consistent shape.</div>
  <div><b>Where the digits come from.</b> The back cover carries a row of ten block glyphs. The page-1 key reads the year as &ldquo;1&nbsp;9&nbsp;9&nbsp;?&rdquo;: the first glyph matches the first glyph of the row, and the two repeated glyphs match the ninth, so the row runs 1&hellip;9, 0. The fourth year glyph is then the sixth in the row, <b>6</b>. This is confirmed by the two headings on spread 3, which read <span class="m">960611.18:31</span> and <span class="m">960611.18:11</span> (YYMMDD.HH:MM): year 96, month 06 = June (page 1 says &ldquo;June ninth&rdquo;), day 11, and times 18:11 and 18:31. The title page repeats &ldquo;1996&rdquo;. Digits 2, 3, 4, 5, 7 and 8 rest on the row order only (3 and 8 occur in the time stamps).</div>
  <div><b>Not listed.</b> CK looks fused in one BACK but separate in the other, so it is left out. ION and similar endings are two touching glyphs, not a special one.</div>
 </div>
</div>
</section>""" % dict(letters=LETTERS, joined=JOINED, doubles=K.doubles, digits=K.digits)

tpl = open(os.path.join(HERE, 'index_template.html')).read()
out = tpl.replace('__KEY__', KEY).replace('__DATA__', json.dumps(data, ensure_ascii=False, separators=(',', ':')))
dst = geom.OT + 'index.html'
open(dst, 'w').write(out)
print(dst, len(out), 'bytes;', sum(len(l['words']) for p in data for l in p['lines']), 'words')
