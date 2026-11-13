#!/usr/bin/env python3
"""
Collect everything the HTML report needs into report_data.json.
Run after solve.py has produced result.json:
    python3 -I build_data.py /path/to/corpus_dir
"""
import sys, os, json, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)
from algebraic_attack import *
from solve import candidate_keys, build_keys, decrypt_with, train, score

corpus = sys.argv[1]
cipher = load('cipher.txt')
res = json.load(open('result.json'))
plain = res['plaintext']

# --- A. unknown-dimension (nullity) vs. minimum repeat length, full ciphertext
cum = Cum(cipher)
by_minlen = []
for ml in (10, 8, 7, 6, 5, 4):
    pairs = repeated_pairs(cipher, ml)
    rows = [row_for(cipher, cum, i, j) for i, j in pairs]
    r = {}
    for p in (5, 19):
        ns, rk = nullspace_mod(rows, N + 1, p)
        r[p] = (rk, len(ns))
    by_minlen.append({'minlen': ml, 'equations': len(pairs),
                      'rank5': r[5][0], 'null5': r[5][1], 'rank19': r[19][0], 'null19': r[19][1]})
    print(by_minlen[-1], flush=True)

# --- B. nullity vs. ciphertext prefix length (F_19 only; F_5 behaves identically)
xs = list(range(500, 3500, 250)) + [3792]
series = {4: [], 5: []}
for n in xs:
    c = cipher[:n]
    cm = Cum(c)
    for ml in (4, 5):
        pairs = repeated_pairs(c, ml)
        rows = [row_for(c, cm, i, j) for i, j in pairs]
        ns, rk = nullspace_mod(rows, N + 1, 19)
        series[ml].append({'n': n, 'equations': len(pairs), 'rank': rk, 'nullity': len(ns)})
    print(n, series[4][-1]['nullity'], series[5][-1]['nullity'], flush=True)

# --- C. all 95 candidate keys scored
pf, npairs = candidate_keys(cipher, 5)
keys = build_keys(pf)
tri, bi = train(corpus)
cands = []
for sh, L, init in keys:
    pt = decrypt_with(cipher, L, init)
    cands.append({'shift': list(sh), 'score': score(pt, tri, bi), 'snippet': pt[:64]})
cands.sort(key=lambda d: -d['score'])
for k, d in enumerate(cands):
    d['rank'] = k + 1

# --- D. highlights for the aligned view
the_hits = [i for i in range(1, len(cipher) - 3) if cipher[i:i + 4] == 'VdP/']
the_ok = [i for i in the_hits if plain[i - 1:i + 4] == ' the ']
blk = 'Yellow, black. ' * 4
pidx = plain.find(blk.rstrip())
cidx = cipher.find('|nu5\\R$98>C:1f6' * 4)

inv = [0] * 95
for s, l in enumerate(res['sbox_forward']):
    inv[l] = s

data = {
    'cipher': cipher, 'plain': plain,
    'init': res['init'], 'forward': res['sbox_forward'], 'inverse': inv,
    'by_minlen': by_minlen, 'series': {str(k): v for k, v in series.items()},
    'candidates': cands,
    'the_hits': the_hits, 'the_ok': len(the_ok),
    'block': {'plain_start': pidx, 'cipher_start': cidx, 'length': 60},
    'stats': {'cipher_len': len(cipher), 'pairs5': npairs, 'distinct_symbols': len(set(cipher)),
              'double_backslashes': cipher.count('\\\\')},
}
json.dump(data, open('report_data.json', 'w'))
print('the-hits', len(the_hits), 'verified as " the "', len(the_ok), 'block', data['block'])
