import sys, math
sys.path.insert(0, ".")
from hopcipher import *

MSG = {"friday": ("YOU HAVE FOUND THE SECRET ", FRIDAY), "spiral": ("THANK GOD ITS FRIDAY", SPIRAL)}

def filler_stats(h, msg_len):
    z = n = 0
    for j, c in enumerate(h, 1):
        if j <= msg_len: continue
        m = 54 - j
        assert 1 <= c <= m
        if m > 1:
            z += (c - (m + 1) / 2) / math.sqrt((m * m - 1) / 12); n += 1
    return z / math.sqrt(n)

def ablations():
    rows = []
    h, _ = decode(SPIRAL); rows.append(("Spiral, rules as stated", "".join(map(sym, h[:22])), "English"))
    h, _ = decode(SPIRAL, cross_start=False); rows.append(("Spiral, A1 not crossed out", "".join(map(sym, h[:22])), "breaks at hop 5"))
    colorder = [c + str(r) for c in COLS for r in range(1, 7)]
    P = {colorder[k]: SPIRAL_ORDER[k] for k in range(54)}
    h, _ = decode(P, order=colorder); rows.append(("Spiral filled column-major", "".join(map(sym, h[:22])), f"loop closes after {len(h)+1} of 54 cells"))
    P = {NAMES[k]: SPIRAL_ORDER[::-1][k] for k in range(54)}
    h, _ = decode(P); rows.append(("Spiral read inward (reversed)", "".join(map(sym, h[:22])), f"loop closes after {len(h)+1} of 54 cells"))
    h, _ = decode(FRIDAY, cross_start=False); rows.append(("Friday, A1 not crossed out", "".join(map(sym, h[:22])), "breaks at hop 3"))
    h, _ = decode(FRIDAY); rows.append(("Friday, rules as stated", "".join(map(sym, h[:22])), "English"))
    return rows

if __name__ == "__main__":
    for nm, (txt, P) in MSG.items():
        h, last = decode(P)
        assert encode(h) == P and last == "A1" and len(h) == 53
        got = "".join(map(sym, h[:len(txt)]))
        assert got == txt, (got, txt)
        assert max(h[:len(txt)]) <= 27
        print(f"{nm}: {got!r}; round-trip OK; max message hop {max(h[:len(txt)])}; "
              f"filler z={filler_stats(h, len(txt)):.2f}; filler={''.join(map(sym, h[len(txt):]))}")
    for r in ablations(): print(r)
