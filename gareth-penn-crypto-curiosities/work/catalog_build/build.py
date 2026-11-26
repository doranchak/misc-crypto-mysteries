#!/usr/bin/env python3
"""Build methods.json from part files p*.py (each defines METHODS list) + meta.py (CATEGORIES, GLOSSARY, TIMELINE)."""
import json, math, re, sys, glob, os
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = "/Users/doranchak/projects/github/misc-crypto-mysteries/gareth-penn-crypto-curiosities/work/methods.json"

MORSE = dict(A='01', B='1000', C='1010', D='100', E='0', F='0010', G='110', H='0000', I='00', J='0111',
             K='101', L='0100', M='11', N='10', O='111', P='0110', Q='1101', R='010', S='000', T='1',
             U='001', V='0001', W='011', X='1001', Y='1011', Z='1100')


def bits(s):
    out = ''
    for tok in re.findall(r'[A-Za-z]|\d+|\.', s):
        if tok == '.':
            out += '.'
        elif tok.isdigit():
            out += bin(int(tok))[2:]
        else:
            out += MORSE[tok.upper()]
    return out


def val(s):
    b = bits(s)
    if '.' in b:
        i, f = b.split('.')
        return int(i or '0', 2) + sum(int(c) / 2 ** (k + 1) for k, c in enumerate(f))
    return int(b, 2)


def alpha(s):
    return sum(3 if c == 'E' else ord(c) - 64 for c in s.upper() if c.isalpha())


ENV = {'math': math, 'pi': math.pi, 'sqrt': math.sqrt, 'phi': (1 + 5 ** 0.5) / 2, 'rad': 180 / math.pi}


ENV.update(bits=lambda w: bits(w), val=lambda w: val(w), alpha=lambda w: alpha(w),
           ana=lambda a, b: sorted(re.sub('[^A-Z]', '', a.upper())) == sorted(re.sub('[^A-Z]', '', b.upper())),
           wiz=lambda w: ''.join(chr(155 - ord(c)) if c.isalpha() else c for c in w.upper()))


def binfrac(x, n):
    f = x - math.floor(x)
    s = ''
    for _ in range(n):
        f *= 2
        b = int(f)
        s += str(b)
        f -= b
    return s


def check(c):
    k = c[0]
    if k == 'm':
        g = val(c[1]); return g == c[2], g
    if k == 'mb':
        g = bits(c[1]); return g == c[2], g
    if k == 'rd':
        a, b = bits(c[1]), bits(c[2]); return a == b, a + ' vs ' + b
    if k == 'in':
        h, t = bits(c[1]), bits(c[2]); return t in h, h + ' contains? ' + t
    if k == 'mf':
        g = val(c[1]); return abs(g - c[2]) < 1e-6, g
    if k == 'a':
        g = alpha(c[1]); return g == c[2], g
    if k == 'doy':
        g = date.fromisoformat(c[1]).timetuple().tm_yday; return g == c[2], g
    if k == 'days':
        g = (date.fromisoformat(c[2]) - date.fromisoformat(c[1])).days; return g == c[3], g
    if k == 'b':
        g = bin(c[1])[2:]; return g == c[2], g
    if k == 'ev':
        g = eval(c[1], dict(ENV)); tol = c[3] if len(c) > 3 else 1e-9
        return abs(g - c[2]) <= tol, g
    if k == 'bf':
        x = eval(c[1], dict(ENV)); g = binfrac(x, c[2]); return g == c[3], g
    raise ValueError(c)


def X(i, o, n, *chk, err=False):
    return dict(input=i, output=o, note=n, chk=list(chk), err=err)


def D(widget, preset='', expect=''):
    return dict(widget=widget, preset=preset, expect=expect)


PARTS = [(1, 73), (2, 151), (3, 229), (4, 307), (5, 999)]
OFF = {1: -5, 2: 73, 3: 151, 4: 229, 5: 307}


def t17part(p):
    for part, hi in PARTS:
        if p <= hi:
            return part


def t17pdf(p):
    part = t17part(p)
    return part, p - OFF[part]


def sppdf(p):
    if p <= 17:
        return p + 5
    if p == 18:
        return None
    return p + 4


def cite(c):
    m = re.match(r'^T17:(\[?)(\d+)(\]?)(?:-(\[?)(\d+)(\]?))?(?: (.*))?$', c)
    if m:
        a = int(m.group(2)); b = int(m.group(5)) if m.group(5) else None
        ab = f"{m.group(1)}{a}{m.group(3)}"
        extra = (m.group(7) + ' ') if m.group(7) else ''
        part, pa = t17pdf(a)
        if b:
            bb = f"{m.group(4)}{b}{m.group(6)}"
            _, pb = t17pdf(b)
            return f"T17 {extra}pp.{ab}-{bb} (Part {part}, PDF pp.{pa}-{pb})"
        return f"T17 {extra}p.{ab} (Part {part}, PDF p.{pa})"
    m = re.match(r'^SP:(\d+)(?:-(\d+))?(?: (.*))?$', c)
    if m:
        a = int(m.group(1)); b = int(m.group(2)) if m.group(2) else None
        extra = (' ' + m.group(3)) if m.group(3) else ''
        def pdfs(p):
            q = sppdf(p)
            return f"PDF p.{q}" if q else "Drive jpeg 66937d"
        if b:
            qa, qb = sppdf(a), sppdf(b)
            if qa and qb:
                return f"SP pp.{a}-{b} (PDF pp.{qa}-{qb}){extra}"
            return f"SP pp.{a}-{b}{extra}"
        return f"SP p.{a} ({pdfs(a)}){extra}"
    return c


WIDGETS = set("morse redivision gematria wizard grid17 calendar dayofyear cubes squares nines rebus radian base anagram transposition hypotenuse none".split())

PRIV = [r'\b\d{3}-\d{2}-\d{4}\b', r'\b\d{3}-\d{4}\b', r'6266', r'2128', r'0670', r'Abbot', r'Russell St', r'0451', r'7945',
        r'117-32', r'Linda Ave', r'22nd Avenue', r'362-3999', r'Hearst', r'Kingsbury', r'Webster St', r'Lincoln St', r'Capitol St',
        r'138-38', r'13035792', r'117322128']


def main():
    ns = {'X': X, 'D': D}
    exec(open(os.path.join(HERE, 'meta.py')).read(), ns)
    cats = ns['CATEGORIES']; gloss = ns['GLOSSARY']; tl = ns['TIMELINE']
    catids = {c['id'] for c in cats}
    methods = []
    for f in sorted(glob.glob(os.path.join(HERE, 'p[0-9]*.py'))):
        pns = {'X': X, 'D': D}
        exec(open(f).read(), pns)
        for m in pns['METHODS']:
            m['_file'] = os.path.basename(f)
            methods.append(m)
    if os.path.exists(os.path.join(HERE, 'zpatch.py')):
        zns = {'X': X, 'D': D}
        exec(open(os.path.join(HERE, 'zpatch.py')).read(), zns)
        byid = {m['id']: m for m in methods}
        remap = {}
        for pid, pe in zns['PATCH'].items():
            if pid not in byid:
                print('PATCH target missing', pid); continue
            m = byid[pid]
            for c in pe.get('cite', []):
                if c not in m['citations']:
                    m['citations'].append(c)
            for e in pe.get('examples', []):
                if len(m['examples']) < 6:
                    m['examples'].append(e)
                else:
                    print('PATCH example dropped (6 max)', pid, e['input'])
            if pe.get('rules_add'):
                m['rules'] = m['rules'].rstrip() + ' ' + pe['rules_add']
            if pe.get('summary_add'):
                m['summary'] = m['summary'].rstrip() + ' ' + pe['summary_add']
            if pe.get('first_seen'):
                m['first_seen'] = pe['first_seen']
            if pe.get('name'):
                m['name'] = pe['name']
        for pid, pe in zns['PATCH'].items():
            tgt_id = pe.get('merge_into')
            if not tgt_id:
                continue
            src = byid[pid]; tgt = byid[tgt_id]
            tgt['rules'] = tgt['rules'].rstrip() + f" Variant ({src['name']}): {src['summary']} {src['rules']}"
            for e in src['examples']:
                if len(tgt['examples']) < 6:
                    tgt['examples'].append(e)
                else:
                    tgt['rules'] = tgt['rules'].rstrip() + f" Example: {e['input']} -> {e['output']}" + (f" ({e['note']})" if e['note'] else '')
                    print('MERGE example folded into rules', pid, '->', tgt_id, e['input'])
            for c in src['citations']:
                if c not in tgt['citations']:
                    tgt['citations'].append(c)
            tgt['related'] = list(dict.fromkeys(tgt.get('related', []) + [r for r in src.get('related', []) if r != tgt_id]))
            remap[pid] = tgt_id
            methods.remove(src)
        for m in methods:
            m['related'] = list(dict.fromkeys(remap.get(r, r) for r in m.get('related', [])))
    ids = [m['id'] for m in methods]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        print('DUPLICATE IDS', dup); sys.exit(1)
    idset = set(ids)
    nfail = 0; nver = 0; nex = 0
    out = []
    for m in methods:
        assert m['category'] in catids, (m['id'], m['category'])
        assert m['demo']['widget'] in WIDGETS, (m['id'], m['demo'])
        assert 1 <= len(m['examples']) <= 6, (m['id'], len(m['examples']))
        exs = []
        for e in m['examples']:
            nex += 1
            ok = None
            if e['chk']:
                res = [check(c) for c in e['chk']]
                ok = all(r[0] for r in res)
                if not ok:
                    nfail += 1
                    print(f"CHECK FAIL {m['id']}: {e['input']} -> {[r for r in res]}")
            if e['err']:
                ok = False
            elif ok:
                nver += 1
            exs.append(dict(input=e['input'], output=e['output'], note=e['note'], verified=ok))
        rel = [r for r in m.get('related', []) if r in idset and r != m['id']]
        missing = [r for r in m.get('related', []) if r not in idset]
        if missing:
            print('missing related', m['id'], missing)
        out.append(dict(id=m['id'], name=m['name'], category=m['category'], summary=m['summary'],
                        rules=m['rules'], examples=exs, claims=m['claims'], first_seen=m['first_seen'],
                        citations=[cite(c) for c in m['citations']], demo=m['demo'], related=rel))
    data = dict(categories=cats, methods=out, glossary=gloss, timeline=tl)
    s = json.dumps(data, ensure_ascii=False, indent=1)
    for p in PRIV:
        for mm in re.finditer(p, s):
            ctx = s[max(0, mm.start() - 60):mm.end() + 60].replace('\n', ' ')
            print('PRIVACY HIT', p, '::', ctx)
    from collections import Counter
    print('categories', len(cats), 'methods', len(out), 'examples', nex, 'verified', nver, 'fails', nfail,
          'glossary', len(gloss), 'timeline', len(tl))
    print(Counter(m['category'] for m in out))
    for c in cats:
        if not any(m['category'] == c['id'] for m in out):
            print('EMPTY CATEGORY', c['id'])
    if '--write' in sys.argv:
        open(OUT, 'w').write(s)
        print('wrote', OUT)


if __name__ == '__main__':
    main()
