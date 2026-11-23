"""Colour/size analysis of the glitched rules text.

Part 1  hue-cluster the original screenshot (../images/rules-original.png) -> inventory of every styled span,
        crop each piece for the report (../images/crops/).
Part 2  align the pieces with ../rules/corrupted.txt (using ../rules/styles.py) and measure where each piece sits.
Part 3  test the hypothesis "pieces that share a style were one styled word/phrase before the text was chopped up":
        - try every ordering of each style group and look for English;
        - Monte-Carlo null: random chunks of the same sizes drawn from the garbled text itself.
Writes ../data/style_analysis.json.   Run from scripts/ with /opt/homebrew/bin/python3.11.
"""
import sys, json, itertools, random, colorsys, os
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
sys.path.insert(0, '../rules')
from styles import STYLES

CORR = open('../rules/corrupted.txt').read().splitlines()
OUT = {}

# ---------------------------------------------------------------- part 1: pixel inventory
im = np.array(Image.open('../images/rules-original.png').convert('RGB')).astype(int)
mx, mn = im.max(2), im.min(2)
col = ((mx - mn) > 50) & (mx > 90)
col[:100] = False                       # skip the "Characters (0)" header / red panel title bar
hue = np.zeros(col.shape)
for y, x in zip(*np.nonzero(col)):
    hue[y, x] = colorsys.rgb_to_hsv(*(im[y, x] / 255))[0] * 360
classes = [('red', -1, 20), ('red2', 340, 361), ('yellow', 20, 70), ('blue', 170, 210), ('purple', 260, 300)]
comps = []
for name, lo, hi in classes:
    m = col & (hue > lo) & (hue <= hi)
    lab, n = ndi.label(ndi.binary_dilation(m, iterations=3, structure=np.ones((3, 3))))
    for i in range(1, n + 1):
        ys, xs = np.nonzero((lab == i) & m)
        if len(ys) < 4: continue
        comps.append(dict(cls='red' if name.startswith('red') else name, x0=int(xs.min()), x1=int(xs.max()), y0=int(ys.min()), y1=int(ys.max()),
                          h=int(ys.max() - ys.min() + 1), px=int(len(ys)),
                          rgb=[int(v) for v in im[ys, xs].mean(0)]))
comps.sort(key=lambda c: (c['y0'], c['x0']))
for c in comps:
    big = c['h'] >= 14 and c['cls'] in ('red', 'blue')
    c['kind'] = {'purple': 'P', 'yellow': 'Y'}.get(c['cls']) or (('R' if c['cls'] == 'red' else 'B') if big else 'E')
OUT['components'] = comps
from collections import Counter
OUT['component_counts'] = dict(Counter(c['kind'] for c in comps))
print('styled spans found in screenshot:', OUT['component_counts'])

# ---------------------------------------------------------------- part 2: align with the text
def locate_one(par, pattern):
    import re
    m = re.fullmatch(r'(.*?)\{(.*?)\}(.*)', pattern, flags=re.S)
    pre, core, post = m.groups()
    i = par.find(pre + core + post)
    assert i >= 0, pattern
    assert par.find(pre + core + post, i + 1) < 0, ('ambiguous', pattern)
    return i + len(pre), i + len(pre) + len(core)

offs = [0]
for p in CORR: offs.append(offs[-1] + len(p) + 1)       # offset of each paragraph in the concatenated garble
pieces = []
for pi, pat, st in STYLES:
    a, b = locate_one(CORR[pi], pat)
    pieces.append(dict(par=pi + 1, text=CORR[pi][a:b], style=st, a=a, b=b, g=offs[pi] + a))
import re
errs = [dict(par=pi + 1, a=m.start(), g=offs[pi] + m.start()) for pi, p in enumerate(CORR) for m in re.finditer('error', p, flags=re.I)]
OUT['pieces'] = pieces
OUT['n_errors'] = len(errs)
OUT['error_positions'] = errs
counts = Counter(p['style'] for p in pieces)
print('aligned pieces:', dict(counts), '+', len(errs), 'errors')
assert counts['P'] == OUT['component_counts']['P'] and counts['R'] == OUT['component_counts']['R'] and counts['B'] == OUT['component_counts']['B']
assert len(errs) == OUT['component_counts']['E']

# ---------------------------------------------------------------- part 3: do same-style pieces reunite?
words = {}
for i, l in enumerate(open('/Users/doranchak/projects/github/zkc-server/data/english_words__practicalcryptography.txt')):
    if i >= 30000: break
    words[l.split()[0].lower()] = i
DICT = set(words)
def segs(s, maxw, minlen=3):
    """all ways to cut s into <= maxw dictionary words (each >= minlen letters)"""
    out = []
    def rec(i, acc):
        if i == len(s):
            out.append(list(acc)); return
        if len(acc) == maxw: return
        for j in range(i + minlen, len(s) + 1):
            if s[i:j] in DICT:
                acc.append(s[i:j]); rec(j, acc); acc.pop()
    rec(0, [])
    return out

def reunite(chunks, maxw):
    hits = []
    for perm in itertools.permutations(range(len(chunks))):
        s = ''.join(c for k in perm for c in chunks[k] if c.isalpha()).lower()
        for sg in segs(s, maxw):
            hits.append((perm, sg))
    return hits

groups = {st: [p['text'] for p in pieces if p['style'] == st] for st in 'PRB'}
res = {}
for st, ch in groups.items():
    # the red group is {"Do't", "n"}: the n has to be spliced INTO "Do't" (a contiguous chunk), so test insertions
    if st == 'R':
        base, ins = "Do't", 'n'
        cands = [base[:i] + ins + base[i:] for i in range(len(base) + 1)]
        CONTRACTIONS = {"don't"}          # apostrophe position matters: "Do'nt" is not a contraction
        res[st] = dict(chunks=ch, candidates=cands, word_candidates=[c for c in cands if c.lower() in CONTRACTIONS])
    else:
        hits = reunite(ch, 2)
        res[st] = dict(chunks=ch, n_orderings=len(list(itertools.permutations(ch))),
                       hits=[dict(order=[ch[k] for k in perm], words=sg) for perm, sg in hits])
# blue group {A, ye}: only two orderings exist; the capital A decides between them
res['B']['orderings'] = {'Aye': 'capital A is word-initial (natural)', 'yeA': 'would be "yea" with a capital A in the middle (unnatural)'}
OUT['reunite'] = res
print({k: (v.get('word_candidates') or [h['words'] for h in v.get('hits', [])]) for k, v in res.items()})

# Monte-Carlo null for the purple group: same chunk sizes, drawn from the garbled text itself
random.seed(20261123)
text = ''.join(CORR)
sizes = [len(t) for t in groups['P']]
N = 100000
hit = 0
for _ in range(N):
    while True:
        starts = [random.randrange(len(text) - s) for s in sizes]
        spans = sorted((a, a + s) for a, s in zip(starts, sizes))
        if all(spans[i][1] <= spans[i + 1][0] for i in range(3)): break
    ch = [text[a:a + s] for a, s in zip(starts, sizes)]
    if 'error' in ''.join(ch).lower(): continue
    if reunite(ch, 2): hit += 1
OUT['mc_purple'] = dict(trials=N, hits=hit, sizes=sizes)
print('Monte Carlo purple null:', hit, 'of', N)

# ---------------------------------------------------------------- displacement of the pieces
def where(pc): return f"¶{pc['par']} char {pc['a']}"
OUT['displacement'] = {st: [dict(par=p['par'], text=p['text'], g=p['g']) for p in pieces if p['style'] == st] for st in 'PRB'}
for st in 'PRB': print(st, [(p['text'], p['par'], p['g']) for p in pieces if p['style'] == st])

# ---------------------------------------------------------------- crops for the report
os.makedirs('../images/crops', exist_ok=True)
src = Image.open('../images/rules-original.png').convert('RGB')
names = {}
for c in comps:
    if c['kind'] in 'PRB':
        # match to a piece by order of style then x/y: label crop by its aligned text
        pass
# match components to pieces by style & reading order (y, then x); pieces are listed in STYLES in (P,P,P,P,R,R,B,B) order,
# so sort pieces by their approximate screen order using paragraph order of the screenshot
paraorder = {2: 0, 3: 1, 4: 2, 5: 3, 6: 4}      # not needed; labelling is done by hand below
labels = {   # (kind, approximate x0,y0) -> text, verified against the 4x crops
    ('P', 235, 315): 'tes:', ('P', 1165, 509): 'tional', ('P', 914, 545): 'no', ('P', 127, 606): 'Addi',
    ('R', 328, 310): 'n', ('R', 116, 422): "Do't", ('B', 859, 359): 'ye', ('B', 689, 500): 'A',
}
crop_info = []
for c in comps:
    if c['kind'] not in 'PRB': continue
    key = next(k for k in labels if k[0] == c['kind'] and abs(k[1] - c['x0']) < 6 and abs(k[2] - c['y0']) < 6)
    t = labels[key]
    pad_x, pad_y = 70, 14
    box = (max(0, c['x0'] - pad_x), max(0, c['y0'] - pad_y - 4), min(src.width, c['x1'] + pad_x), min(src.height, c['y1'] + pad_y))
    cr = src.crop(box)
    cr = cr.resize((cr.width * 3, cr.height * 3), Image.LANCZOS)
    fn = f"{c['kind']}_{t.replace(':', 'colon').replace(chr(39), 'apos')}.png"
    cr.save('../images/crops/' + fn)
    crop_info.append(dict(kind=c['kind'], text=t, file='images/crops/' + fn, box=box))
OUT['crops'] = crop_info
json.dump(OUT, open('../data/style_analysis.json', 'w'), indent=1, ensure_ascii=False)
print('wrote ../data/style_analysis.json;', len(crop_info), 'crops')
