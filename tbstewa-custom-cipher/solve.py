#!/usr/bin/env python3
"""
Stage 2: turn the algebraic nullspace into candidate keys, decode, rank by English-ness.
Usage: python3 -I solve.py cipher.txt [minlen] [corpus_dir]
"""
import sys, os, glob, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from collections import Counter
from algebraic_attack import *

def crt(a5, a19):
    # x = a5 mod 5, x = a19 mod 19
    for x in range(95):
        if x % 5 == a5 % 5 and x % 19 == a19 % 19:
            return x

def candidate_keys(c, minlen):
    cum = Cum(c)
    pairs = repeated_pairs(c, minlen)
    rows = [row_for(c, cum, i, j) for i, j in pairs]
    per_field = {}
    for p in (5, 19):
        ns, rk = nullspace_mod(rows, N + 1, p)
        assert len(ns) == 2, (p, len(ns))
        half = pow(2, -1, p)
        const = [1] * N + [half]               # the symmetric "all labels equal" solution
        # pick the basis vector that is not a multiple of const, then strip const component
        u = None
        for v in ns:
            # is v a multiple of const?
            k = v[0]
            if any((v[t] - k * const[t]) % p for t in range(N + 1)):
                u = v; break
        assert u is not None
        # normalise so that u's component along const is 0 at label index 0
        k = u[0]
        u = [(u[t] - k * const[t]) % p for t in range(N + 1)]
        per_field[p] = (u, const)
    return per_field, len(pairs)

def build_keys(per_field):
    """Yield (shift_pair, L list of 95 ints, init) for all 95 shifts; only permutations kept."""
    u5, w5 = per_field[5]; u19, w19 = per_field[19]
    out = []
    for b5 in range(5):
        for b19 in range(19):
            v5 = [(a + b5 * w) % 5 for a, w in zip(u5, w5)]
            v19 = [(a + b19 * w) % 19 for a, w in zip(u19, w19)]
            L = [crt(v5[s], v19[s]) for s in range(N)]
            init = crt(v5[N], v19[N])
            if sorted(L) == list(range(N)):
                out.append(((b5, b19), L, init))
    return out

def decrypt_with(cipher, L, init):
    inv = [0] * N
    for s, l in enumerate(L):
        inv[l] = s
    prev = init
    res = []
    for ch in cipher:
        cv = L[ord(ch) - 32]
        dv = (cv - prev) % N
        res.append(chr(inv[dv] + 32))
        prev = dv
    return ''.join(res)

# ---- tiny English scorer: char trigram model from corpus -------------------
def train(corpus_dir, limit=4_000_000):
    tri = Counter(); bi = Counter()
    seen = 0
    for f in sorted(glob.glob(corpus_dir + '/*.txt')):
        t = open(f, errors='ignore').read().replace('\r', '').replace('\n', ' ')
        t = ''.join(ch if 32 <= ord(ch) < 127 else ' ' for ch in t)
        for i in range(len(t) - 2):
            tri[t[i:i + 3]] += 1
            bi[t[i:i + 2]] += 1
        seen += len(t)
        if seen > limit: break
    return tri, bi

def score(text, tri, bi):
    s = 0.0
    for i in range(len(text) - 2):
        s += math.log((tri.get(text[i:i + 3], 0) + 0.1) / (bi.get(text[i:i + 2], 0) + 9.5))
    return s / (len(text) - 2)

if __name__ == '__main__':
    path = sys.argv[1]; minlen = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    corpus = sys.argv[3] if len(sys.argv) > 3 else None
    c = load(path)
    pf, npairs = candidate_keys(c, minlen)
    keys = build_keys(pf)
    print(f'pairs={npairs}; candidate keys that are valid permutations: {len(keys)} / 95')
    if corpus:
        tri, bi = train(corpus)
        ranked = []
        for sh, L, init in keys:
            pt = decrypt_with(c, L, init)
            ranked.append((score(pt, tri, bi), sh, L, init, pt))
        ranked.sort(reverse=True)
        for sc, sh, L, init, pt in ranked[:5]:
            print(f'{sc:.3f} shift={sh} init={init}  {pt[:200]!r}')
        best = ranked[0]
        json.dump({'shift': best[1], 'sbox_forward': best[2], 'init': best[3], 'plaintext': best[4],
                   'scores': [(r[0], r[1]) for r in ranked]}, open('result.json', 'w'))
