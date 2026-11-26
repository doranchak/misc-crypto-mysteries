"""Cell-by-cell accounting of the Past and Future word search (20x15)."""
from grid import GRID_ROWS, R, C, DIRS
DIRV = {v: k for k, v in DIRS.items()}

# (word, row, col, dir, category)  -- 0-based row/col
WORDS = [
    ("NINETEEN", 0, 9, "E", "number"), ("NINE", 0, 11, "W", "number"),
    ("THREE", 1, 6, "S", "number"), ("THREE", 11, 19, "W", "number"),
    ("ELEVEN", 7, 0, "S", "number"), ("TWELVE", 8, 17, "W", "number"),
    ("FIVE", 9, 4, "E", "number"), ("ZERO", 14, 6, "W", "number"),
    ("NORTH", 3, 5, "W", "direction"), ("WEST", 6, 9, "W", "direction"),
    ("LILAC", 0, 7, "W", "colour"), ("LEMON", 4, 7, "NE", "colour"), ("SAPPHIRE", 14, 12, "E", "colour"),
    ("WATER", 4, 19, "W", "place"), ("DIVIDE", 6, 11, "SE", "place"), ("PEAKS", 7, 7, "W", "place"),
    ("QUARRY", 12, 13, "E", "place"), ("DIRT", 10, 19, "W", "place"), ("RAIL", 2, 18, "W", "place"),
    ("STATE", 6, 7, "SE", "place"), ("ESTATE", 5, 6, "W", "place"),
    ("COUNT", 1, 0, "S", "other"), ("ROUND", 2, 1, "E", "other"), ("WALK", 10, 10, "W", "other"),
    ("SQUARE", 11, 9, "E", "other"),
]
# hidden message: (plain words, list of cells in reading order)
def span(r, c0, c1): return [(r, c) for c in range(c0, c1 + 1)]
MSG = [
    ("THERE", span(1, 1, 5)), ("ARE", span(1, 7, 9)), ("FIVE CLUES", span(1, 11, 19)),
    ("IN", span(2, 7, 8)), ("THIS", span(2, 10, 13)),
    ("WORD SEARCH", span(3, 10, 18) + [(3, 9)]),          # one of the O's at (3,9)/(3,19)
    ("BUT DO", span(4, 1, 5)), ("NOT TELL", span(4, 8, 14)),
    ("ANYONE", [(5, 8), (5, 9), (5, 10), (5, 11), (5, 13), (5, 12)]),  # one O of (5,7),(5,12),(5,14)
    ("LINE", span(5, 15, 18)),
    ("THEM UP", span(6, 0, 5)), ("THERE ARE", span(6, 12, 19)),
    ("NO", span(7, 1, 2)), ("SPECIAL", span(7, 13, 19)),
    ("BENDS OR", span(8, 1, 6) + [(8, 8)]),               # one O of (8,6)/(8,7)
    ("TURNS", [(8, 18), (8, 19)] + span(9, 1, 3)),
    ("JUST", span(9, 15, 18)), ("REMAIN", span(10, 1, 6)), ("STEADY TO", span(11, 1, 8)),
    ("COMPLETE", span(12, 1, 8)), ("THE", span(12, 10, 12)), ("MISSION", span(13, 0, 6)),
]
AMBIG_O = [(3, 9), (3, 19), (5, 7), (5, 12), (5, 14), (8, 6), (8, 7)]  # 3 message O's + 4 spare O's, interchangeable
STATES = {(9, 8): "TN", (9, 9): "TN", (9, 11): "NC", (9, 12): "NC", (10, 12): "SC", (10, 13): "SC"}

def cells_of(w, r, c, d):
    dr, dc = DIRV[d]
    out = []
    for k, ch in enumerate(w):
        rr, cc = r + dr * k, c + dc * k
        assert GRID_ROWS[rr][cc] == ch, (w, rr, cc)
        out.append((rr, cc))
    return out

def classify():
    word_cells = {}
    for w, r, c, d, cat in WORDS:
        for cell in cells_of(w, r, c, d):
            word_cells.setdefault(cell, []).append(w)
    msg_cells = {}
    for txt, cells in MSG:
        letters = sorted(GRID_ROWS[r][c] for r, c in cells)
        assert letters == sorted(txt.replace(" ", "")), (txt, letters)
        for cell in cells:
            assert cell not in msg_cells, cell
            msg_cells[cell] = txt
    cls = {}
    for r in range(R):
        for c in range(C):
            ch = GRID_ROWS[r][c]
            inw, inm = (r, c) in word_cells, (r, c) in msg_cells
            assert not (inw and inm), ((r, c), word_cells.get((r, c)), msg_cells.get((r, c)))
            if (r, c) in AMBIG_O: cls[(r, c)] = "ambig"
            elif inw: cls[(r, c)] = "word"
            elif inm: cls[(r, c)] = "msg"
            elif (r, c) in STATES: cls[(r, c)] = "state"
            elif ch == "O" and 1 <= r <= 12: cls[(r, c)] = "spareO"
            else: cls[(r, c)] = "random"
    return word_cells, msg_cells, cls

if __name__ == "__main__":
    import collections
    wc, mc, cls = classify()
    print(collections.Counter(cls.values()))
    print("spare O definite:", sum(1 for v in cls.values() if v == "spareO"), "+ 4 of the 7 ambiguous O's")
    for r in range(R):
        print(" ".join({"word": "w", "msg": "m", "ambig": "?", "state": "S", "spareO": "o", "random": "."}[cls[(r, c)]] for c in range(C)), "  ",
              "".join(GRID_ROWS[r][c] for c in range(C) if cls[(r, c)] == "random"))
    # message in reading order
    order = sorted(MSG, key=lambda m: min(m[1]))
    print(" ".join(t for t, _ in order))
