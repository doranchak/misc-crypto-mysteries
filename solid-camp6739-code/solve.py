#!/usr/bin/env python3
"""Decode the u/Solid-Camp6739 triple-number cipher (r/codes 1xxzoe6).

Every token is  a-b-c  with (a,b) one of (24,30), (28,35), (32,40)  [= 4k-5k, k=6,7,8]
and c an odd number that steps by 6 from one letter to the next inside a group.

Key (verified against all 172 tokens; Q, X are interpolated, Z extrapolated):
  group 24-30 : A..E   c = 47 + 6*i
  group 28-35 : F..O   c = 19 + 6*i
  group 32-40 : P..Y   c = 21 + 6*i

The same key as one formula (x = 0 for A ... 25 for Z):
  v = 3x + 14;  q = v // 29;  r = v % 29
  token = (24 + 4q) - (30 + 5q) - (19 + 2r)
"""
import collections, re, string, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ALPHA = string.ascii_uppercase

def table_key():
    """Explicit lookup table: token -> letter (A..Y)."""
    spec = [((24, 30), 47, "ABCDE"), ((28, 35), 19, "FGHIJKLMNO"), ((32, 40), 21, "PQRSTUVWXY")]
    return {f"{a}-{b}-{base + 6*i}": ch for (a, b), base, letters in spec for i, ch in enumerate(letters)}

def formula_token(ch):
    x = ALPHA.index(ch)
    q, r = divmod(3*x + 14, 29)
    return f"{24 + 4*q}-{30 + 5*q}-{19 + 2*r}"

def words(text):
    return [w.split() for w in re.findall(r'/([^/]+)/', text) if w.strip()]

def main():
    text = (HERE / "cipher.txt").read_text()
    tbl = table_key()
    # 1. the one-line formula reproduces the explicit table for every letter A..Y
    assert all(tbl[formula_token(ch)] == ch for ch in ALPHA[:25])
    print("formula == table for A..Y;  Z ->", formula_token("Z"))

    # 2. decode
    ws = words(text)
    plain = ["".join(tbl.get(t, "?") for t in w) for w in ws]
    sentence = " ".join(plain)
    (HERE / "plaintext.txt").write_text(sentence + "\n")
    print(sentence)

    # 3. stats
    toks = [t for w in ws for t in w]
    letters = [tbl[t] for t in toks]
    cnt = collections.Counter(letters)
    n = len(letters)
    ic = sum(c*(c-1) for c in cnt.values()) / (n*(n-1))
    print(f"words={len(ws)} tokens={n} distinct={len(cnt)} unknown={sum('?' in w for w in plain)}")
    print(f"index of coincidence = {ic:.4f}  (English ~0.067, random ~0.038)")
    print("attested:", "".join(sorted(cnt)), "| not in text:", "".join(c for c in ALPHA if c not in cnt))
    print("single-letter words:", collections.Counter(w[0] for w in plain if len(w) == 1))
    # c-values per group (what first gave the arithmetic away)
    for g in ("24-30", "28-35", "32-40"):
        print(g, sorted({int(t.split('-')[2]) for t in toks if t.startswith(g)}))

if __name__ == "__main__":
    sys.exit(main())
