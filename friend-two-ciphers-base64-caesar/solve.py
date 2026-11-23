#!/usr/bin/env python3
"""Solve the friend's two-cipher puzzle: Caesar on letters (digits untouched) + Base64.

Run:  /opt/homebrew/bin/python3.11 solve.py
"""
import base64, string

CT = "FQrvSQXyIGviSQPtmw9jmiL0kQEqnQPslQEqm3BroGFuSQFdmRB5"
U, L = string.ascii_uppercase, string.ascii_lowercase

def rot(x, n):
    """Shift letters by n (case preserved); digits, '+', '/', '=' unchanged."""
    return x.translate(str.maketrans(U + L, U[n % 26:] + U[:n % 26] + L[n % 26:] + L[:n % 26]))

def printable(b):
    return all(32 <= c < 127 for c in b)

# 1. brute force all 26 Caesar shifts on the whole string, then Base64-decode
print("shift  Base64 text after shift                              decoded")
hits = []
for n in range(26):
    t = rot(CT, n)
    try:
        d = base64.b64decode(t + "=" * (-len(t) % 4), validate=True)
    except Exception as e:
        d = None
    ok = d is not None and printable(d)
    if ok:
        hits.append((n, t, d))
    print(f"{n:>5}  {t:<52}  {d.decode('latin1') if ok else '-'}")

assert len(hits) == 1
n, b64, pt = hits[0]
print("\nSolution: Caesar +%d (= -%d) then Base64" % (n, 26 - n))
print("Base64 :", b64)
print("Plain  :", pt.decode())

# 2. round-trip: plaintext -> Base64 -> Caesar +10 must reproduce the ciphertext
enc = rot(base64.b64encode(pt).decode(), 26 - n)
print("Re-encode matches ciphertext:", enc == CT)

# 3. the "two halves" idea: try every split point, Caesar+Base64 on one side only
print("\nSplit test (does either side alone give text while the other is junk?):")
for k in range(8, len(CT) - 8):
    for side, part in (("L", CT[:k]), ("R", CT[k:])):
        for s in range(26):
            t = rot(part, s)
            try:
                d = base64.b64decode(t + "=" * (-len(t) % 4), validate=True)
            except Exception:
                continue
            if len(d) >= 6 and printable(d) and s != n:
                print("  extra hit", k, side, s, d)
print("  (no hits other than shift %d on the whole string)" % n)
