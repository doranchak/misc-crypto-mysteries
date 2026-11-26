"""Decode u/justwantstofeelcute's Z340-inspired art codes (r/codes 1v7ozf5).
cell value = (A1Z26 letter) x (position in message); positions laid out by ORDER."""
from fractions import Fraction

ORDER = [
    [38, 44, 40, 46, 42, 48],
    [26, 32, 28, 34, 30, 36],
    [37, 43, 39, 45, 41, 47],
    [25, 31, 27, 33, 29, 35],
    [14, 20, 16, 22, 18, 24],
    [2, 8, 4, 10, 6, 12],
    [13, 19, 15, 21, 17, 23],
    [1, 7, 3, 9, 5, 11],
]

# transcribed from the images (pic 1 / pic 2), not from the Reddit text
GRID1 = [
    [418, 836, 320, 230, 798, 576],
    [338, 608, 560, 680, 390, 324],
    [518, 387, 780, 360, 369, 564],
    [375, 155, 135, 297, 261, 280],
    [196, 160, 144, 418, 18, 456],
    [30, 40, 20, 90, 54, 96],
    [117, 113, 165, 315, 221, 460],
    [19, 91, 39, 171, 100, 220],
]
GRID2 = [
    [874, 660, 1000, 230, 840, 528],
    [468, 763, 196, 646, 600, 432],
    [444, 645, 39, 1035, 779, 47],
    [475, 279, 243, 33, 232, 35],
    [210, 20, 368, 506, 324, 600],
    [30, 144, 92, 70, 108, 240],
    [325, 95, 315, 252, 85, 23],
    [25, 35, 63, 81, 25, 88],
]

def decode(grid):
    out = {}
    for r in range(8):
        for c in range(6):
            p = ORDER[r][c]; v = grid[r][c]
            q = Fraction(v, p)
            out[p] = (r, c, v, q)
    return out

if __name__ == "__main__":
  for name, g in (("GRID1", GRID1), ("GRID2", GRID2)):
      d = decode(g)
      s = []
      print(name)
      for p in range(1, 49):
          r, c, v, q = d[p]
          ok = q.denominator == 1 and 1 <= q <= 26
          ch = chr(64 + int(q)) if ok else '?'
          s.append(ch)
          if not ok:
              print(f"  pos {p:2d} r{r+1}c{c+1} value {v} / {p} = {float(q):.3f}  <-- non-integer/out of range")
      print("  ", "".join(s))
