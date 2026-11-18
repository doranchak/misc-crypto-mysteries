#!/usr/bin/env python3
"""
Solver for u/Giokku's "Encrypted transmission ... intercepted from a spaceship"
https://www.reddit.com/r/codes/comments/1xx7wn3/encrypted_transmission_of_a_dialogue_intercepted/

Model: ciphertext = 2-digit numbers (a shuffled 26-letter key), every word spelled BACKWARDS,
language = Esperanto ("epo", hint 2), apostrophe inside a number = diacritic on that letter.

Usage:  python3 solve.py path/to/epo_sentences.tsv
  (corpus: https://downloads.tatoeba.org/exports/per_language/epo/epo_sentences.tsv.bz2, bunzip2 first)

Steps: (1) build a smoothed (back-off) letter-quadgram model of Esperanto from the corpus,
       (2) hill-climb the number->letter key (random restarts, all swaps), for both reading
           directions and with/without the two crib hints,
       (3) write key.json and plaintext.txt.
"""
import sys, re, json, random, collections
import numpy as np

HERE = __file__.rsplit('/', 1)[0] if '/' in __file__ else '.'
ALPHA = "_abcĉdefgĝhĥijĵklmnoprsŝtuŭvz"        # index 0 = word boundary
IDX = {c: i for i, c in enumerate(ALPHA)}
N = len(ALPHA)


def build_model(corpus):
    c4 = np.zeros((N, N, N, N))
    with open(corpus, encoding='utf8') as f:
        for line in f:
            parts = line.rstrip('\n').split('\t')
            if len(parts) < 3:
                continue
            for w in re.findall(r"[a-zĉĝĥĵŝŭ]+", parts[2].lower()):
                if any(c not in IDX for c in w):
                    continue
                s = [0, 0, 0] + [IDX[c] for c in w] + [0]
                for i in range(len(s) - 3):
                    c4[s[i], s[i+1], s[i+2], s[i+3]] += 1
    c3 = c4.sum(0); c2 = c3.sum(0); c1 = c2.sum(0)
    p1 = (c1 + 1) / (c1 + 1).sum()
    k = 4.0
    cond = lambda cnt, back: (cnt + k * back) / (cnt.sum(-1, keepdims=True) + k)
    p2 = cond(c2, p1[None, :]); p3 = cond(c3, p2[None]); p4 = cond(c4, p3[None])
    return np.log(p4).astype(np.float32)


def parse_cipher(path):
    t = open(path, encoding='utf8').read().replace('’', "'").replace('1326', '13.26')  # typo: missing dot
    raw = re.findall(r"[0-9'A-Z]+(?:\.[0-9'A-Z]+)*", t)
    return t, [w.split('.') for w in raw]


def hillclimb(score, S, nletters, fixed, rng):
    letters = list(range(1, nletters + 1))
    avail = [c for c in letters if c not in fixed.values()]
    rng.shuffle(avail)
    m = np.zeros(S + 1, dtype=np.int64); k = 0
    for s in range(1, S + 1):
        if s in fixed: m[s] = fixed[s]
        else: m[s] = avail[k]; k += 1
    unused = set(avail[k:])
    cur = score(m)
    free = [s for s in range(1, S + 1) if s not in fixed]
    improved = True
    while improved:
        improved = False
        for i, a in enumerate(free):
            for b in free[i+1:]:
                m[a], m[b] = m[b], m[a]
                new = score(m)
                if new > cur + 1e-9: cur = new; improved = True
                else: m[a], m[b] = m[b], m[a]
            for u in list(unused):
                old = m[a]; m[a] = u
                new = score(m)
                if new > cur + 1e-9: cur = new; unused.remove(u); unused.add(old); improved = True
                else: m[a] = old
    return cur, m


def solve(logp, words, syms, mode, hints, restarts=300, seed=5):
    sid = {s: i + 1 for i, s in enumerate(syms)}
    seq = [0, 0, 0]
    for w in words:
        ww = w[::-1] if mode == 'rev' else w
        seq += [sid[x] for x in ww] + [0]
    seq = np.array(seq)
    def score(m):
        l = m[seq]
        return logp[l[:-3], l[1:-2], l[2:-1], l[3:]].sum()
    fixed = {sid['05']: IDX['a'], sid['06']: IDX['f']} if hints else {}
    rng = random.Random(seed)
    best = (-1e18, None)
    for _ in range(restarts):
        b, m = hillclimb(score, len(syms), N - 1, fixed, rng)
        if b > best[0]: best = (b, m.copy())
    return best[0], {s: ALPHA[best[1][sid[s]]] for s in syms}


if __name__ == '__main__':
    corpus = sys.argv[1]
    logp = build_model(corpus)
    text, words_all = parse_cipher(f'{HERE}/cipher.txt')
    LIT = {'D', 'Z', 'B', 'ST', 'E'}               # literal Greek-numeral capitals, handled by hand
    words = [w for w in words_all if not any(x in LIT for x in w)]
    syms = sorted({x for w in words for x in w})
    results = {}
    for mode in ('fwd', 'rev'):
        for hints in (True, False):
            sc, key = solve(logp, words, syms, mode, hints)
            results[(mode, hints)] = (sc, key)
            print(f"{mode:3s} hints={hints!s:5s}  log-likelihood {sc:9.1f}")
    sc, key = results[('rev', True)]
    sc2, key2 = results[('rev', False)]
    print('with/without hints identical key:', key == key2)
    json.dump({'score': float(sc), 'key': key}, open(f'{HERE}/key.json', 'w'), ensure_ascii=False, indent=1)
    # hand corrections: 22 = h (not z) because "Lilith" / "handikapita"; 25 left as z by elimination
    key['22'] = 'h'; key['25'] = 'z'
    def dec(w):
        return ''.join(key.get(x, x) for x in reversed(w.split('.')))
    out = re.sub(r"[0-9'A-Z]+(?:\.[0-9'A-Z]+)*", lambda mo: dec(mo.group(0)), text.replace('’', "'").replace('1326', '13.26'))
    open(f'{HERE}/plaintext.txt', 'w', encoding='utf8').write(out)
    print(out)
