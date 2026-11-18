#!/usr/bin/env python3
"""Evidence that the recovered key really yields Esperanto.
Usage: python3 evidence.py path/to/epo_sentences.tsv   ->  writes evidence.json
 * letter-frequency comparison (decoded cipher vs. the corpus)
 * vocabulary coverage of the decoded words
"""
import sys, re, json, collections
import numpy as np

HERE = __file__.rsplit('/', 1)[0] if '/' in __file__ else '.'
corpus = sys.argv[1]
key = json.load(open(f'{HERE}/key.json'))['key']
key['22'] = 'h'; key['25'] = 'z'           # hand corrections, see index.html "Caveats"

vocab = collections.Counter()
letters = collections.Counter()
for line in open(corpus, encoding='utf8'):
    p = line.rstrip('\n').split('\t')
    if len(p) < 3: continue
    for w in re.findall(r"[a-zĉĝĥĵŝŭ]+", p[2].lower()):
        if any(c in 'qwxy' for c in w): continue
        vocab[w] += 1
        for ch in w: letters[ch] += 1

t = open(f'{HERE}/cipher.txt', encoding='utf8').read().replace('’', "'").replace('1326', '13.26')
words = [w.split('.') for w in re.findall(r"[0-9'A-Z]+(?:\.[0-9'A-Z]+)*", t)]
LIT = {'D', 'Z', 'B', 'ST', 'E'}
plain = [''.join(key[x] for x in reversed(w)) for w in words if not any(x in LIT for x in w)]

cnt = collections.Counter(key[x] for w in words for x in w if x in key)
tot = sum(cnt.values()); T = sum(letters.values())
rows = [(k, 100 * cnt[k] / tot, 100 * letters[k] / T) for k in sorted(cnt, key=lambda k: -cnt[k])]
r = float(np.corrcoef([x[1] for x in rows], [x[2] for x in rows])[0, 1])

LABELS = {'adm', 'do', 'kpt', 'zlm', 'kadm', 'rdo'}
NAMES = {'raus', 'lilith', 'pontes', 'ramov', 'pratt', 'erebus', 'antonio', 'roland', 'david', 'lee', 'kepler'}
ordinary = [w for w in plain if w not in LABELS and w not in NAMES]
attested = [w for w in ordinary if w in vocab]
missing = sorted({w for w in ordinary if w not in vocab})
out = dict(rows=rows, pearson=r, n_words=len(plain),
           n_labels=sum(w in LABELS for w in plain), n_names=sum(w in NAMES for w in plain),
           n_ordinary=len(ordinary), n_attested=len(attested), missing=missing,
           n_sentences_corpus=sum(1 for _ in open(corpus, encoding='utf8')))
json.dump(out, open(f'{HERE}/evidence.json', 'w'), ensure_ascii=False, indent=1)
print({k: v for k, v in out.items() if k != 'rows'})
