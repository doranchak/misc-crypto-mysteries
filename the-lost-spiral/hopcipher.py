"""Hop-count pointer cipher used by u/ViezeVingertjes' "Thank god its friday!" (r/codes 1wjxj5u)
and by "The Lost Spiral".

Cells of a 9x6 grid are numbered in book order (A1,B1..I1,A2..I6).  Every cell stores a pointer to
another cell and the pointers form one 54-cycle.  Start at A1, follow the pointer, count the hops in
book order (wrapping I6->A1) over cells that are NOT yet crossed out, counting the destination.
hops 1..26 = A..Z, 27 = space.  Cross the destination out and repeat.
"""
COLS = "ABCDEFGHI"
NAMES = [COLS[c] + str(r) for r in range(1, 7) for c in range(9)]      # book order
POS = {n: i for i, n in enumerate(NAMES)}

FRIDAY_ROWS = """H3 E2 D4 B4 H1 F5 G3 F3 A5
A4 I2 I4 D6 A3 B3 A1 D3 E3
C4 C1 E4 I6 G6 H5 F6 E5 H4
C5 G2 D1 D5 H6 C2 B2 G5 D2
A6 C3 F4 C6 I1 B5 E1 B1 E6
B6 H2 G4 I5 I3 F2 F1 A2 G1""".split("\n")
FRIDAY = {NAMES[k]: lab for k, lab in enumerate(" ".join(FRIDAY_ROWS).split())}

# The Lost Spiral, nodes in order from the X outward (traced by following the dashed connectors).
SPIRAL_ORDER = ("C3 E4 G1 A2 A5 G2 B5 F5 D2 H4 F6 I6 F4 H6 H2 D3 E6 I3 I5 H1 B4 E3 I1 C2 G4 D4 G5 E2 C4 H5 "
                "B3 C5 E1 F1 E5 F3 I2 D6 C1 A1 H3 C6 A4 B1 G3 B2 F2 A6 A3 D1 D5 B6 I4 G6").split()
SPIRAL = {NAMES[k]: lab for k, lab in enumerate(SPIRAL_ORDER)}          # node k = cell k (book order)


def sym(n):
    return " " if n == 27 else chr(64 + n) if 1 <= n <= 26 else "?"


def decode(ptr, order=NAMES, start="A1", cross_start=True):
    """Return (hops, closing_pointer).  Stops when the next pointer leads somewhere already visited."""
    pos = {n: i for i, n in enumerate(order)}
    crossed = {start} if cross_start else set()
    seen = {start}
    cur, hops = start, []
    while ptr[cur] not in seen:
        tgt, i, n = ptr[cur], pos[cur], 0
        while True:
            i = (i + 1) % len(order)
            if order[i] in crossed:
                continue
            n += 1
            if order[i] == tgt:
                break
        hops.append(n)
        crossed.add(tgt); seen.add(tgt); cur = tgt
    return hops, ptr[cur]


def encode(hops, start="A1"):
    """Inverse of decode(): rebuild the pointer grid from hop counts; the last cell points back to start."""
    crossed, cur, ptr = {start}, start, {}
    for n in hops:
        i, k = POS[cur], 0
        while True:
            i = (i + 1) % 54
            if NAMES[i] in crossed:
                continue
            k += 1
            if k == n:
                break
        ptr[cur] = NAMES[i]; crossed.add(NAMES[i]); cur = NAMES[i]
    ptr[cur] = start
    return ptr
