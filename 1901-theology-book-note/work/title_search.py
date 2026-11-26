"""Title/heading search under the user's segmentation: title = [Ɪ-like big I][dot=o] + 9 glyphs.
Bold glyph tokens:
  title: I0 O N V A S I X T Y X     (I0 = big initial; tested both as == I and as free)
  W1   : b r X I U Y D X
Known from the thin-pen key: O=o (dot), S=i.  Optional: X(box)=a, A in {n,s}, D=a.
"""
import sys, collections, re
SJP, FREQ = sys.argv[1], sys.argv[2]
freq = {}
for l in open(FREQ, encoding='utf-8'):
    p = l.split()
    if len(p) == 2: freq[p[0]] = int(p[1])
words = [w.strip() for w in open(SJP, encoding='utf-8') if w.strip().isalpha() and w.strip().islower()]
bylen = collections.defaultdict(list)
for w in words: bylen[len(w)].append(w)

def fit(gl, w, m):
    m = dict(m); inv = {v: k for k, v in m.items()}
    for g, c in zip(gl, w):
        if g in m:
            if m[g] != c: return None
        else:
            if c in inv: return None
            m[g] = c; inv[c] = g
    return m

def run(title, w1, fixed, label, top=25):
    res = []
    for tw in bylen[len(title)]:
        m = fit(title, tw, fixed)
        if m is None: continue
        hits = [ww for ww in bylen[len(w1)] if fit(w1, ww, m) is not None]
        res.append((freq.get(tw, 0), tw, sorted(hits, key=lambda x: -freq.get(x, 0))[:6], len(hits)))
    res.sort(key=lambda r: (-(r[3] > 0), -r[0]))
    print(f'== {label}: {len(res)} title words; with a W1 partner: {sum(1 for r in res if r[3])}')
    for f, tw, hs, n in res[:top]:
        print(f'   {tw:14s} f={f:<7d} W1 partners({n}): {" ".join(hs)}')

T11 = 'I O N V A S I X T Y X'.split()          # big initial == serifed I
T11f = 'I0 O N V A S I X T Y X'.split()        # big initial free
T10 = 'O N V A S I X T Y X'.split()            # roman numeral I. then word o+9
W1 = 'b r X I U Y D X'.split()
base = {'O': 'o', 'S': 'i'}
run(T11, W1, base, 'T11 big-I = Ɪ, O=o, S=i')
run(T11, W1, {**base, 'X': 'a'}, 'T11 + box=a')
run(T11f, W1, {**base, 'X': 'a'}, 'T11 free initial + box=a', 15)
run(T10, W1, base, 'T10 (roman I.) o+9, S=i', 15)
