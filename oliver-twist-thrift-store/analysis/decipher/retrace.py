"""Re-trace single key glyphs straight from the flattened full-resolution pages embedded in ../../glyph-editor.html.

The original tracer (keyglyphs2.py) needed the segmentation pickles; this one only needs the page images
(same coordinates as PAGES in report.html / the glyph boxes) and takes a hand-chosen rectangle, so it can be
used to repair or add a key exemplar when the pickles are not available.

trace_rect(page, (x, y, w, h)) -> dict(d=svg path, w, h, page)   (same format as key_glyphs.json entries)
"""
import json, base64, os, functools
import numpy as np, cv2

HERE = os.path.dirname(os.path.abspath(__file__))
EDITOR = os.path.join(HERE, '..', '..', 'glyph-editor.html')


@functools.lru_cache(maxsize=None)
def pages():
    s = open(EDITOR).read()
    i = s.find('const DATA=') + len('const DATA=')
    j = s.find('\nconst KEY_REAL=')
    D = json.loads(s[i:j].rstrip().rstrip(';'))
    out = {}
    for p in D['pages']:
        out[p['id']] = cv2.imdecode(np.frombuffer(base64.b64decode(p['full']), np.uint8), cv2.IMREAD_GRAYSCALE)
    return out


def to_path(keep, up, eps=0.35):
    """bitmap -> SVG path (evenodd), identical to keyglyphs.to_path (copied: that module needs the pickles to import)."""
    ys, xs = np.nonzero(keep)
    if len(ys) == 0:
        return None
    bx0, by0, bx1, by1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    k = keep[by0:by1, bx0:bx1]
    k = cv2.copyMakeBorder(k, 2, 2, 2, 2, cv2.BORDER_CONSTANT, value=0)
    cs, _ = cv2.findContours(k, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    d = []
    for c in cs:
        if len(c) < 8:
            continue
        a = cv2.approxPolyDP(c, up * eps, True)
        if len(a) < 3:
            continue
        pts = [((q[0][0] - 2) / up, (q[0][1] - 2) / up) for q in a]
        d.append('M' + ' '.join(f'{x:.1f} {y:.1f}' for x, y in pts) + 'Z')
    return dict(d=''.join(d), w=(bx1 - bx0) / up, h=(by1 - by0) / up)


def trace_rect(page, rect, up=4, pad=14, sig=0.9, thrf=0.92, minarea=18, exclude=(), keep_edge=True, eps=0.5):
    """rect = (x, y, w, h) in flat-page coordinates: everything dark inside it is the glyph.
    exclude = rectangles (x, y, w, h) whose ink is removed (a neighbour's stroke running into the box)."""
    flat = pages()[page]
    H, W = flat.shape
    x, y, w, h = rect
    X0 = max(0, int(x) - pad); Y0 = max(0, int(y) - pad); X1 = min(W, int(x + w) + pad); Y1 = min(H, int(y + h) + pad)
    crop = flat[Y0:Y1, X0:X1]
    thr, _ = cv2.threshold(crop, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    g = cv2.resize(crop, None, fx=up, fy=up, interpolation=cv2.INTER_CUBIC)
    g = cv2.GaussianBlur(g, (0, 0), up * sig)
    bw = (g < thr * thrf).astype(np.uint8) * 255
    r = np.zeros_like(bw)
    bx0 = int((x - X0) * up); by0 = int((y - Y0) * up); bx1 = int((x + w - X0) * up); by1 = int((y + h - Y0) * up)
    r[max(0, by0):max(0, by1), max(0, bx0):max(0, bx1)] = 255
    bw = cv2.bitwise_and(bw, r)
    for (ex, ey, ew, eh) in exclude:
        bw[max(0, int((ey - Y0) * up)):max(0, int((ey + eh - Y0) * up)), max(0, int((ex - X0) * up)):max(0, int((ex + ew - X0) * up))] = 0
    n, lab, st, _ = cv2.connectedComponentsWithStats(bw, connectivity=8)
    keep = np.zeros_like(bw)
    for i in range(1, n):
        if st[i, 4] >= minarea * up * up:
            keep[lab == i] = 255
    res = to_path(keep, up, eps=eps)
    if res:
        res['page'] = page
        res['keep'] = keep
    return res


def bitmap(res, h=120):
    k = res['keep']
    ys, xs = np.nonzero(k)
    k = k[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    s = h / k.shape[0]
    return 255 - cv2.resize(k, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
