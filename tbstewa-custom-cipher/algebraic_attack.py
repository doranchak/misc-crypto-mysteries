#!/usr/bin/env python3
"""
Ciphertext-only algebraic attack on tbstewa's custom autokey/S-box cipher.

Cipher (from crypt.py), with S = keyed permutation of 0..94:
    S[c_i] = S[p_i] + S[p_{i-1}]   (mod 95),   S[p_{-1}] := init

Write L = S (label of each ASCII symbol), x_i = L(p_i), y_i = L(c_i).
    y_i = x_i + x_{i-1}      =>      x_i = (-1)^i * (A_i - init),
    A_i = sum_{t<=i} (-1)^t * y_t        (only depends on the CIPHERTEXT and L)

Key observation: if the ciphertext contains a repeated substring
    c[i..i+m-1] == c[j..j+m-1]
then x_{i+k} - x_{j+k} = (-1)^k * d for a constant d.  For real English
(m large enough) d == 0, i.e. the plaintext repeats too, and therefore
    x_i == x_j      <=>      (-1)^i (A_i - init) - (-1)^j (A_j - init) == 0
which is a LINEAR, HOMOGENEOUS equation in the 96 unknowns (L[0..94], init)
whose coefficients are read straight off the ciphertext.

Stack many such equations, solve over F_5 and F_19 (95 = 5*19), and the
nullspace is 2-D: the constant vector (a symmetry of the equality pattern)
plus the true key.  The constant direction leaves 95 candidate keys, one per
shift, and exactly one of them decodes to English.
"""
import sys, json
from itertools import combinations

N = 95

def load(path):
    return open(path).read().rstrip('\n')

def repeated_pairs(c, minlen):
    """Return list of (i, j, m): c[i:i+m] == c[j:j+m] (i<j), keeping maximal-ish repeats.
    For every distinct repeated substring of length minlen we pair the first
    occurrence with each later one (the equation depends only on the start)."""
    n = len(c)
    d = {}
    for i in range(n - minlen + 1):
        d.setdefault(c[i:i + minlen], []).append(i)
    pairs = []
    for k, occ in d.items():
        if len(occ) > 1:
            for j in occ[1:]:
                pairs.append((occ[0], j))
    return pairs

def row_for(c, cum, i, j):
    """Coefficient row (length 96) of  x_i - x_j  in unknowns (L[0..94], init).
    cum[i] = dict-free list: coefficient vector of A_i (length 95) -> built lazily."""
    ri = cum(i); rj = cum(j)
    si = 1 if i % 2 == 0 else -1
    sj = 1 if j % 2 == 0 else -1
    row = [0] * (N + 1)
    for s in range(N):
        row[s] = si * ri[s] - sj * rj[s]
    row[N] = -si + sj          # init coefficient
    return row

class Cum:
    """Lazy prefix coefficient vectors of A_i (alternating sums by symbol)."""
    def __init__(self, c):
        self.c = c
        self.vecs = []
        cur = [0] * N
        for t, ch in enumerate(c):
            cur[ord(ch) - 32] += 1 if t % 2 == 0 else -1
            self.vecs.append(cur[:])
    def __call__(self, i):
        return self.vecs[i]

def nullspace_mod(rows, ncols, p):
    """Nullspace of the row-space over F_p. Returns list of basis vectors."""
    M = [[x % p for x in r] for r in rows]
    piv_cols = []
    r = 0
    for col in range(ncols):
        pr = None
        for k in range(r, len(M)):
            if M[k][col] % p:
                pr = k; break
        if pr is None:
            continue
        M[r], M[pr] = M[pr], M[r]
        inv = pow(M[r][col], -1, p)
        M[r] = [(v * inv) % p for v in M[r]]
        for k in range(len(M)):
            if k != r and M[k][col]:
                f = M[k][col]
                M[k] = [(a - f * b) % p for a, b in zip(M[k], M[r])]
        piv_cols.append(col)
        r += 1
        if r == len(M):
            break
    free = [c for c in range(ncols) if c not in piv_cols]
    basis = []
    for fc in free:
        v = [0] * ncols
        v[fc] = 1
        for ri, pc in enumerate(piv_cols):
            v[pc] = (-M[ri][fc]) % p
        basis.append(v)
    return basis, len(piv_cols)

def rank_mod(rows, ncols, p):
    return nullspace_mod(rows, ncols, p)[1]

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else 'cipher.txt'
    minlen = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    c = load(path)
    cum = Cum(c)
    pairs = repeated_pairs(c, minlen)
    print(f'len={len(c)}  minlen={minlen}  pairs={len(pairs)}')
    rows = [row_for(c, cum, i, j) for i, j in pairs]
    for p in (5, 19):
        ns, rk = nullspace_mod(rows, N + 1, p)
        print(f'F_{p}: rank={rk}  nullity={len(ns)} (expect 2 if fully determined)')
