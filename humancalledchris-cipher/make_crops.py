"""Cut glyph crops (ciphertext + key) and the page image used by index.html."""
import json, os, sys
from PIL import Image, ImageDraw, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from reading_data import COLUMNS, COLUMN_X, KEY_CENTERS  # noqa: E402

SRC = os.path.join(HERE, 'images', 'original.png')
im = Image.open(SRC).convert('RGB')
enh = ImageEnhance.Contrast(im).enhance(1.3)

# ---- page crop for the visualizer --------------------------------------
PAGE_BOX = (2250, 100, 3200, 1850)   # x0, y0, x1, y1 in original pixels
page = im.crop(PAGE_BOX)
page.save(os.path.join(HERE, 'images', 'page.jpg'), quality=88)


def stem_x(col, y):
    (xt, xb) = COLUMN_X[col]
    t = (y - 150) / (1800 - 150)
    return xt + (xb - xt) * max(0, min(1, t))


def refine_stem(col, y0, y1):
    """darkest vertical line near the expected stem inside [y0, y1]"""
    x = int(stem_x(col, (y0 + y1) / 2))
    best, bx = None, x
    g = im.convert('L')
    for dx in range(-35, 36):
        s = 0
        for y in range(y0, y1, 3):
            s += g.getpixel((x + dx, y))
        if best is None or s < best:
            best, bx = s, x + dx
    return bx


os.makedirs(os.path.join(HERE, 'images', 'glyphs'), exist_ok=True)
os.makedirs(os.path.join(HERE, 'images', 'key'), exist_ok=True)

out = {}
HALF_W = 70
for col, items in COLUMNS.items():
    rows = []
    for i, (kind, val, y0, y1, note) in enumerate(items):
        cx = refine_stem(col, y0, y1)
        box = (cx - HALF_W, y0, cx + HALF_W, y1)
        fn = f'images/glyphs/c{col}_{i:02d}.png'
        if kind in ('L', 'B'):
            enh.crop(box).save(os.path.join(HERE, fn))
        rows.append(dict(kind=kind, val=val, note=note,
                         box=[box[0] - PAGE_BOX[0], box[1] - PAGE_BOX[1],
                              box[2] - PAGE_BOX[0], box[3] - PAGE_BOX[1]],
                         img=fn if kind in ('L', 'B') else None))
    out[col] = rows

F = 1.5838
for k, (x, y) in KEY_CENTERS.items():
    x, y = x * F, y * F
    w, h = (75, 80) if not k.isdigit() and k != '.' else (70, 62)
    name = 'dot' if k == '.' else k
    enh.crop((int(x - w), int(y - h), int(x + w), int(y + h))).save(
        os.path.join(HERE, 'images', 'key', f'{name}.png'))

with open(os.path.join(HERE, 'glyph_boxes.json'), 'w') as f:
    json.dump({'page_box': PAGE_BOX, 'page_size': page.size, 'columns': out}, f, indent=1)

# ---- QA contact sheet (not used by the report) -------------------------
if len(sys.argv) > 1:
    cells = [(c, r) for c in out for r in out[c] if r['img']]
    W, H = 140, 150
    per = 12
    sheet = Image.new('RGB', (per * W, ((len(cells) + per - 1) // per) * (H + 20)), 'white')
    d = ImageDraw.Draw(sheet)
    for i, (c, r) in enumerate(cells):
        g = Image.open(os.path.join(HERE, r['img']))
        g.thumbnail((W, H))
        x, y = (i % per) * W, (i // per) * (H + 20)
        sheet.paste(g, (x, y + 20))
        d.text((x + 4, y + 4), f"c{c} {r['val']}", fill='red')
    sheet.save(sys.argv[1])
print('ok')
