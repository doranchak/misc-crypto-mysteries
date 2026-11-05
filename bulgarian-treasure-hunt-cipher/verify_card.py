#!/usr/bin/env python3
"""Check grid.txt against the photo of the card (card.jpg) by classifying each glyph.

Needs Pillow (pip install pillow). Pure-Python connected-component labelling,
so it takes a few seconds.

Usage:  python3 verify_card.py [card.jpg] [grid.txt]
"""
import sys
from pathlib import Path
from PIL import Image

here = Path(__file__).parent
photo = sys.argv[1] if len(sys.argv) > 1 else here / 'card.jpg'
grid_path = sys.argv[2] if len(sys.argv) > 2 else here / 'grid.txt'

# Work at a fixed width so the size thresholds below are independent of the photo's resolution.
W = 1046
img = Image.open(photo).convert('L')
H = round(img.size[1] * W / img.size[0])
img = img.resize((W, H), Image.LANCZOS)
px = img.load()
dark = [[px[x, y] < 165 for x in range(W)] for y in range(H)]

# 8-connected components of dark pixels. Each glyph (ring, disc or half-disc) is one component.
seen = [[False] * W for _ in range(H)]
glyphs = []
for y0 in range(H):
    for x0 in range(W):
        if not dark[y0][x0] or seen[y0][x0]:
            continue
        stack, pts = [(x0, y0)], []
        seen[y0][x0] = True
        while stack:
            x, y = stack.pop()
            pts.append((x, y))
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H and dark[ny][nx] and not seen[ny][nx]:
                        seen[ny][nx] = True
                        stack.append((nx, ny))
        if len(pts) <= 60:
            continue  # specks
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        w, h = max(xs) - min(xs) + 1, max(ys) - min(ys) + 1
        if not (35 <= w <= 70 and 35 <= h <= 70):
            continue  # scratches / merged blobs
        cx, cy, r = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, min(w, h) / 2
        left = right = nl = nr = 0
        for y in range(int(cy - r), int(cy + r) + 1):
            for x in range(int(cx - r), int(cx + r) + 1):
                if ((x - cx) ** 2 + (y - cy) ** 2) ** .5 <= .8 * r and 0 <= x < W and 0 <= y < H:
                    if x < cx - .1 * r:
                        nl += 1; left += dark[y][x]
                    elif x > cx + .1 * r:
                        nr += 1; right += dark[y][x]
        fl, fr = left / nl, right / nr
        if fl > .7 and fr > .7:   ch = '●'
        elif fl < .3 and fr < .3: ch = '○'
        elif fl > .7 and fr < .3: ch = '◐'   # left half black
        elif fr > .7 and fl < .3: ch = '◑'   # right half black
        else:                     ch = '?'
        glyphs.append((cx, cy, ch))

glyphs.sort(key=lambda g: g[1])
rows = []
for g in glyphs:  # group into rows by y
    if rows and abs(g[1] - sum(q[1] for q in rows[-1]) / len(rows[-1])) < 25:
        rows[-1].append(g)
    else:
        rows.append([g])
photo_rows = [[c[2] for c in sorted(r, key=lambda g: g[0])] for r in rows]
want = [line.split() for line in Path(grid_path).read_text(encoding='utf-8').splitlines() if line.strip()]

print(f'glyphs found in photo: {len(glyphs)} in {len(photo_rows)} rows {[len(r) for r in photo_rows]}')
bad = 0
for i, (a, b) in enumerate(zip(photo_rows, want), 1):
    diffs = [j + 1 for j in range(max(len(a), len(b))) if j >= len(a) or j >= len(b) or a[j] != b[j]]
    bad += len(diffs)
    print(f'row {i:2d}:', 'matches' if not diffs else f'differs at columns {diffs}')
print(f'\n{sum(map(len, want)) - bad} of {sum(map(len, want))} glyphs in {Path(grid_path).name} match the photo')
sys.exit(1 if bad or len(photo_rows) != len(want) else 0)
