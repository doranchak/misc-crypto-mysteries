#!/usr/bin/env python3
"""Build ../index.html (report + visualizer) from data.py.

Run:  python3 work/build_report.py   (from the puzzle folder, or anywhere)
"""
import json, os, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import data  # noqa: E402

OUT = os.path.join(HERE, '..', 'index.html')


def slope(page, cell):
    # measured from the ruled lines: page 1 drops ~9 px over 540 px; page 2 drops 16 px (top) to 9 px (bottom)
    return 0.017 if page == 1 else 0.030 - 0.013 * cell / 16


def build_page(page, rules, lines):
    out = []
    for li, entry in enumerate(lines):
        cell, words = entry[0], entry[1]
        override = entry[2] if len(entry) > 2 else None
        s = slope(page, cell)
        ws = []
        for (x0, x1, text, kind, note) in words:
            if override:
                y0, y1 = override
                poly = [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]
            else:
                pt, pb = (0, 9) if page == 1 else (3, 5)   # page-1 writing sags below its ruled line
                t = lambda x: rules[cell] + s * (x - 290) + pt
                b = lambda x: rules[cell + 1] + s * (x - 290) + pb
                poly = [[x0, round(t(x0))], [x1, round(t(x1))], [x1, round(b(x1))], [x0, round(b(x0))]]
            ws.append({'x0': x0, 'x1': x1, 'text': text, 'kind': kind, 'note': note, 'poly': poly})
        xs0 = min(w['x0'] for w in ws); xs1 = max(w['x1'] for w in ws)
        if override:
            band = [xs0 - 6, override[0], xs1 + 6, override[1]]
        else:
            band = [xs0 - 6, round(rules[cell] + min(0, s * (xs0 - 290)) - 6),
                    xs1 + 6, round(rules[cell + 1] + max(s * (xs1 - 290), 0) + 8)]
        out.append({'cell': cell, 'words': ws, 'band': band})
    return out


pages = {
    '1': {'img': 'page%201.webp', 'w': 1080, 'h': 1440, 'lines': build_page(1, data.PAGE1_RULES, data.PAGE1)},
    '2': {'img': 'page%202.webp', 'w': 1080, 'h': 1112, 'lines': build_page(2, data.PAGE2_RULES, data.PAGE2)},
}

# letter statistics (legible, non-annotation words only)
cnt = Counter()
for p in pages.values():
    for ln in p['lines']:
        for w in ln['words']:
            if w['kind'] in ('w', 'u', 'i', 's'):
                cnt.update(c for c in w['text'] if c.isalpha())
total = sum(cnt.values())
nwords = sum(1 for p in pages.values() for ln in p['lines'] for w in ln['words'] if w['kind'] in ('w', 'u', 'i'))

payload = {
    'pages': pages,
    'reading1': data.READING1,
    'reading2': data.READING2,
    'counts': dict(cnt),
    'total': total,
    'nwords': nwords,
}

html = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
html = html.replace('__DATA__', json.dumps(payload, ensure_ascii=False))
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(html)
print('wrote', os.path.abspath(OUT), 'glyphs:', total, 'words:', nwords)
