"""Pattern (isomorph) search: which Polish words fit the repeat structure of the
cipher words, and which title/W1 pairs are mutually consistent under a simple
one-glyph-one-letter substitution?"""
import sys, itertools, collections
WL = sys.argv[1]
words = []
for line in open(WL, encoding='utf-8'):
    w, f = line.split()
    if w.isalpha():
        words.append((w.lower(), int(f)))
freq = dict(words)

def pattern(seq):
    m = {}; out = []
    for s in seq:
        if s not in m: m[s] = len(m)
        out.append(m[s])
    return tuple(out)

# glyph transcriptions (one token per glyph)
T_noTilde = ['N','V','A','S','Ib','Bx','Y','Bx']
T_tilde   = ['N','V','A','S','Ib','Bx','~','Y','Bx']
W1 = ['b','r','Bx','Ib','Tinv','Y','Bd','Bx']

by_pat = collections.defaultdict(list)
for w, f in words:
    by_pat[pattern(w)].append((w, f))

def consistent(glyphs, word, m):
    m = dict(m); inv = {v: k for k, v in m.items()}
    for g, c in zip(glyphs, word):
        if g in m and m[g] != c: return None
        if c in inv and inv[c] != g: return None
        m[g] = c; inv[c] = g
    return m

for name, T in [('title(no ~)', T_noTilde), ('title(~ = letter)', T_tilde)]:
    cands_T = by_pat[pattern(T)]
    cands_W = by_pat[pattern(W1)]
    print(f'== {name}: {len(cands_T)} title-pattern words, {len(cands_W)} W1-pattern words')
    pairs = []
    for tw, tf in cands_T:
        m = consistent(T, tw, {})
        for ww, wf in cands_W:
            if consistent(W1, ww, m) is not None:
                pairs.append((min(tf, wf), tw, ww))
    pairs.sort(reverse=True)
    for p in pairs[:40]: print('  ', p)
