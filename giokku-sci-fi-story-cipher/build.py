#!/usr/bin/env python3
"""Builds index.html (interactive report) + plaintext.txt from cipher.txt, key.json, evidence.json."""
import re, json, collections

HERE = __file__.rsplit('/', 1)[0] if '/' in __file__ else '.'
key = json.load(open(f'{HERE}/key.json'))['key']
score_rev = json.load(open(f'{HERE}/key.json'))['score']
ev = json.load(open(f'{HERE}/evidence.json'))
key['22'] = 'h'; key['25'] = 'z'                      # hand corrections (see Caveats)
key['–'] = '-'                                         # the hyphen inside the compound word
GREEK = {'D': ('Δ', '4'), 'E': ('Ε', '5'), 'ST': ('ϛ', '6'), 'Z': ('Ζ', '7'), 'B': ('Β', '2')}

raw = open(f'{HERE}/cipher.txt', encoding='utf8').read().replace('’', "'").replace('1326', '13.26')
raw = raw.replace('.(–).', '.–.')                      # dot-joined dash = hyphen inside one word

TOK = re.compile(r"\((?P<p>[^()]+)\)|(?P<w>[0-9'A-Z–]+(?:\.[0-9'A-Z–]+)*)|(?P<f>[\[\]])|(?P<s>-)")
PROPER = {'raus', 'lilith', 'pontes', 'ramov', 'pratt', 'erebus', 'antonio', 'roland', 'david', 'lee',
          'kepler-5627b', 'adm', 'do', 'kpt', 'zlm', 'kadm', 'rdo'}


def decode_word(toks):
    """tokens (cipher order) -> display chips + plaintext word (reversed)"""
    chips = []
    for x in toks:
        if x in GREEK:
            chips.append(dict(n=x, l=GREEK[x][1] if x != 'D' else 'D', lit=True, g=GREEK[x][0]))
        elif x == '–':
            chips.append(dict(n='–', l='-', lit=False, pn=True))
        else:
            chips.append(dict(n=x, l=key[x], lit=False))
    plain = ''.join(c['l'] for c in reversed(chips))
    return chips, plain


paras = []
for block in re.split(r'\n\s*\n', raw.strip()):
    items = []; seq = []
    for mo in TOK.finditer(block):
        if mo.group('w'):
            chips, plain = decode_word(mo.group('w').split('.'))
            items.append(dict(t='w', chips=chips, plain=plain))
        elif mo.group('p'):
            items.append(dict(t='p', ch=mo.group('p')))
        elif mo.group('f'):
            items.append(dict(t='f', ch=mo.group('f')))
        else:
            items.append(dict(t='s'))
    # ---- assemble readable plaintext -------------------------------------------------
    out = ''; prefix = ''; qopen = False; cap = True; prev_sep = True; prev_t = 'f'
    for i, it in enumerate(items):
        t = it['t']
        if t == 's':
            prev_sep = True; continue
        if t == 'f':
            continue
        nxt_sep = i + 1 < len(items) and items[i + 1]['t'] == 's'
        if t == 'p':
            ch = it['ch']
            if ch == '"':
                if not qopen: prefix += '"'; qopen = True; it['open'] = True
                else: out += '"'; qopen = False
            elif ch == '[':
                prefix += '['; it['open'] = True
            elif ch == ']':
                out += ']'
            elif ch in ('–', '-'):
                out += ' ' + ch; it['sa'] = True
            else:
                out += ch
                if ch in '.!?…': cap = True
                if ch == ':' and out.endswith(']:'): cap = True
            prev_sep = False; continue
        w = it['plain']
        if w in PROPER or w.split('-')[0] == 'kepler':
            w = w[0].upper() + w[1:]
        elif cap:
            w = w[0].upper() + w[1:]
        cap = False
        out += (' ' if out else '') + prefix + w
        prefix = ''
        prev_sep = False
    out = out.replace('[', '[').strip()
    paras.append(dict(items=items, plain=out))

EN = [
    "International Space Rescue Fleet, Mothership One. Voice-transcription system activated. Automatic encoding system activated – automatic code selection: code D – welcome!",
    "Date – time: system disabled. Coordinates: system disabled.",
    "[Adm] [Do]: Lee! Report on the status, immediately!",
    "[Kpt] [Zlm]: \"Raus\" has been destroyed, sir! It seems that \"Lilith\" opened fire on it. We tried to contact Captain Pontes, but we received no response.",
    "[Adm] [Do]: Antonio…",
    "[Kpt] [Zlm]: Captain Ramov has withdrawn. He is leading \"Lilith\" out of the gravity field of Kepler-5627b.",
    "[Adm] [Do]: I warned him! I warned him not to defy me!",
    "[Kadm] [Rdo]: What are your orders, sir?",
    "[Adm] [Do]: I will not let that fool leave us! Not when we are so close! Send \"Erebus\"! Bring Ramov back to me, dead or alive!",
    "[Kadm] [Rdo]: David, that is a bad idea.",
    "[Adm] [Do]: Roland, are you ready to die for this? I thought not. Captain Lee, send Captain Pratt immediately!",
    "[Kpt] [Zlm]: Yes, Admiral.",
    "Voice-transcription system deactivated. Automatic encoding system deactivated.",
]
assert len(EN) == len(paras), (len(EN), len(paras))
KIND = ['head', 'head'] + ['talk'] * 10 + ['head']
for p, e, k in zip(paras, EN, KIND):
    p['en'] = e; p['kind'] = k
    p['plain'] = p['plain'].replace('Shstemo', 'shstemo [sic]')

# ---- key table --------------------------------------------------------------------
cnt = collections.Counter()
for p in paras:
    for it in p['items']:
        if it['t'] == 'w':
            for c in it['chips']:
                if not c.get('lit') and not c.get('pn'): cnt[c['n']] += 1
keyrows = []
for i in range(1, 27):
    n = f'{i:02d}'
    acc = [k for k in cnt if "'" in k and k.replace("'", '') == n]
    keyrows.append(dict(n=n, l=key.get(n), c=cnt.get(n, 0),
                        acc=[dict(n=a, l=key[a], c=cnt[a]) for a in acc]))

_t = open(f'{HERE}/cipher.txt', encoding='utf8').read().replace('’', "'").replace('1326', '13.26')
_w = [w.split('.') for w in re.findall(r"[0-9'A-Z]+(?:\.[0-9'A-Z]+)*", _t)]
n_trans = sum(len(w) + 1 for w in _w if not any(x in GREEK for x in w))
DATA = dict(paras=paras, keyrows=keyrows, ev=ev, ll_rev=-2121.0, ll_fwd=-3919.3, n_trans=n_trans)

# ---- plaintext.txt -----------------------------------------------------------------
with open(f'{HERE}/plaintext.txt', 'w', encoding='utf8') as f:
    f.write('SOLUTION - u/Giokku "Encrypted transmission of a dialogue, intercepted from a spaceship"\n')
    f.write('https://www.reddit.com/r/codes/comments/1xx7wn3/encrypted_transmission_of_a_dialogue_intercepted/\n\n')
    f.write('Method: 2-digit numbers -> letters (shuffled 26-letter key), every word spelled backwards, language = Esperanto,\n')
    f.write("apostrophe inside a number = diacritic (0'9=ŭ, 1'9=ŝ, 2'1=ĉ, 0'1=ĝ), digits written as capital Greek numerals.\n\n")
    f.write('KEY  (number -> letter)\n')
    f.write('  ' + '  '.join(f"{r['n']}={r['l'] or '·'}" for r in keyrows) + '\n')
    f.write("  accents: 0'9=ŭ 1'9=ŝ 2'1=ĉ 0'1=ĝ ; Greek numerals: Δ(D)=4 Ε(E)=5 ϛ(ST)=6 Ζ(Z)=7 Β(B)=2\n\n")
    for p in paras:
        f.write(p['plain'] + '\n    ' + p['en'] + '\n\n')

tpl = open(f'{HERE}/template.html', encoding='utf8').read()
html = tpl.replace('/*__DATA__*/null', json.dumps(DATA, ensure_ascii=False))
open(f'{HERE}/index.html', 'w', encoding='utf8').write(html)
print('ok', len(html), 'bytes;', len(paras), 'paragraphs')
for p in paras: print(p['plain'])
