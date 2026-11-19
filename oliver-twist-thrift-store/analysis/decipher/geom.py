"""Per-word geometry for the plain side-by-side view (build_index.py).

Reads PAGES out of ../../report.html (words with boxes + glyph boxes) and returns, for every
page, a list of lines; each line has a fitted baseline through the glyph centres (centre y,
slope) and each word has: centre on that baseline, slot width, key.
"""
import json, re, math, statistics as st

OT = '/Users/doranchak/projects/github/misc-crypto-mysteries/oliver-twist-thrift-store/'
ORDER = ['b1', 'b2L', 'b2R', 'b3L', 'b3R', 'b4L', 'b4R', 'b5']
NAMES = {'b1': 'Page 1 (photo 1)', 'b2L': 'Spread 2, left page (photo 2)', 'b2R': 'Spread 2, right page (photo 2)',
         'b3L': 'Spread 3, left page (photo 3)', 'b3R': 'Spread 3, right page (photo 3)',
         'b4L': 'Inside cover, left page (photo 4)', 'b4R': 'Title page, right page (photo 4)',
         'b5': 'Back cover digit row (photo 5)'}
# stored lines that are really ONE physical line (page, n of first part, n of second part); the report
# lists "THIS IS ALL WORTHWHILE" (n=13) and "I AM READY TO" (n=14) separately.
MERGE = {('b3L', 13): 14}


def load_pages():
    s = open(OT + 'report.html').read()
    i = s.find('const PAGES=')
    j = s.find('\n', i)
    return json.loads(s[i + len('const PAGES='):j].rstrip(';'))


def lsfit(pts):
    n = len(pts)
    if n == 0:
        return 0.0, 0.0
    if n < 3:
        return sum(p[1] for p in pts) / n, 0.0
    mx = sum(p[0] for p in pts) / n
    my = sum(p[1] for p in pts) / n
    sxx = sum((p[0] - mx) ** 2 for p in pts)
    sxy = sum((p[0] - mx) * (p[1] - my) for p in pts)
    b = sxy / sxx if sxx else 0.0
    return my - b * mx, b


def robust_fit(pts, tol):
    a, b = lsfit(pts)
    for _ in range(2):
        keep = [p for p in pts if abs(p[1] - (a + b * p[0])) < tol]
        if len(keep) >= 3:
            a, b = lsfit(keep)
    return a, b


def wtext(w):
    return w['t'] + ('?' if w['f'] == 'D' and w['c'] < 0.55 else '')


def build():
    P = load_pages()
    out = []
    for key in ORDER:
        p = P[key]
        lines = p['lines']
        # merge physical lines
        byn = {L['n']: L for L in lines}
        used = set()
        phys = []
        for L in lines:
            if L['n'] in used:
                continue
            k2 = MERGE.get((key, L['n']))
            if k2 and k2 in byn:
                M = byn[k2]
                used.add(k2)
                first, second = sorted([L, M], key=lambda q: q['words'][0]['x'])
                phys.append(dict(n=L['n'], wo=L.get('wo'), words=first['words'] + second['words'],
                                 glyphs=first['glyphs'] + second['glyphs']))
            else:
                phys.append(dict(n=L['n'], wo=L.get('wo'), words=L['words'], glyphs=L['glyphs']))
        plines = []
        for L in phys:
            if not L['words']:
                continue
            gl = L['glyphs']
            hs = sorted(g['h'] for g in gl)
            H = hs[len(hs) // 2] if hs else statistics_h(L['words'])
            words = []
            for w in L['words']:
                x0, x1 = w['x'], w['x'] + w['w']
                gs = [g for g in gl if x0 - 2 <= g['x'] + g['w'] / 2 <= x1 + 2]
                words.append(dict(t=wtext(w), f=w['f'], c=w['c'], x0=x0, x1=x1, y0=w['y'], y1=w['y'] + w['h'], gs=gs))
            if L['wo'] or not gl:
                # lettering lines (covers): no glyph fit, the word box itself is the cipher word
                for w in words:
                    w.update(cx=(w['x0'] + w['x1']) / 2, cy=(w['y0'] + w['y1']) / 2, H=w['y1'] - w['y0'], ang=0.0,
                             box=(w['x0'], w['y0'], w['x1'], w['y1']))
                plines.append(dict(n=L['n'], words=words, wo=True, H=H))
                continue
            pts = [(g['x'] + g['w'] / 2, g['y'] + g['h'] / 2) for g in gl]
            a, b = robust_fit(pts, 0.5 * H)
            ang = math.degrees(math.atan(b))
            for w in words:
                cx = (w['x0'] + w['x1']) / 2
                cy = a + b * cx
                if w['gs']:   # follow a wavy / curved line: add most of the word's own offset from the straight fit
                    r = st.median([(g['y'] + g['h'] / 2) - (a + b * (g['x'] + g['w'] / 2)) for g in w['gs']])
                    cy += 0.8 * max(-0.6 * H, min(0.6 * H, r))
                w.update(cx=cx, cy=cy, H=H, ang=ang, box=None)
            plines.append(dict(n=L['n'], words=words, wo=False, H=H, a=a, b=b, ang=ang, pts=pts))
        out.append(dict(key=key, name=NAMES[key], img=p['img'], w=p['w'], h=p['h'], lines=plines))
    return out


def statistics_h(words):
    return st.median(w['h'] for w in words)


if __name__ == '__main__':
    for pg in build():
        print('==', pg['key'], pg['w'], pg['h'])
        for L in pg['lines']:
            if L['wo']:
                print(' ', L['n'], 'wo', [(w['t'], [round(v) for v in w['box']]) for w in L['words']])
                continue
            res = [abs(p[1] - (L['a'] + L['b'] * p[0])) / L['H'] for p in L['pts']]
            wres = []
            for w in L['words']:
                if w['gs']:
                    r = st.median([(g['y'] + g['h'] / 2) - (L['a'] + L['b'] * (g['x'] + g['w'] / 2)) for g in w['gs']])
                    wres.append(r / L['H'])
            print('  n=%2d ang=%6.2f H=%4.0f nw=%d ng=%d  max|res|/H=%.2f  word-median-res/H max=%.2f  %s' % (
                L['n'], L['ang'], L['H'], len(L['words']), len(L['pts']), max(res), max(abs(r) for r in wres) if wres else 0,
                ' '.join(w['t'] for w in L['words'])[:40]))
