"""Are the word spaces shuffled together with the letters (spaces = ordinary characters), or laid down separately?

New evidence (images/profile-highlighted.png): line 1 has a DOUBLE space between ATAAE and LOD (gap 12 px vs 7 px for a
single space), so line 1 has 4 spaces = the 4 spaces of FAILED TO LOAD USER DATA; line 2 has 3 = SUBVERTING SYSTEM
BACKUPS TO; line 3 has 0 = Processing.  The space counts are conserved.

Tests (all with the space counted as a character, case-insensitive):
  1. neighbouring-pair preservation vs. uniformly random permutations of the same 24/28/10 characters;
  2. pairs that contain a space, on their own;
  3. minimum common string partition (fewest chunks) with spaces as characters;
  4. line 2: rank the 24 word orders by (1) and (3).
Writes ../data/space_chars.json.  Run from scripts/ with /opt/homebrew/bin/python3.11.
"""
import random, json, itertools, sys, time
from collections import Counter
sys.setrecursionlimit(10000)
random.seed(20261123)

LINES = {
    "line1": ("UFDAILD TOSER ATAAE  LOD", "FAILED TO LOAD USER DATA"),     # NB double space, measured from the screenshot
    "line2": ("YERSSTEMTO BTING CKSUBVP ASU", "SUBVERTING SYSTEM BACKUPS TO"),
    "line3": ("cesriPosng", "Processing"),
}

def bigram_hits(plain, cipher, only_space=False):
    c = Counter(cipher[i:i + 2] for i in range(len(cipher) - 1))
    hits = 0
    for i in range(len(plain) - 1):
        b = plain[i:i + 2]
        if only_space and ' ' not in b: continue
        if c[b] > 0:
            c[b] -= 1; hits += 1
    return hits

def mcsp(plain, cipher, maxK=40):
    """fewest chunks (exact); chunk = substring of plain; chunks used at most once each position"""
    n = len(plain)
    for K in range(1, maxK):
        memo = set()
        def go(pos, mask, left):
            if pos == n: return True
            if left == 0: return False
            # prune: remaining cipher chars must fit in `left` chunks at max length (cheap bound)
            key = (pos, mask, left)
            if key in memo: return False
            for L in range(n - pos, 0, -1):
                seg = cipher[pos:pos + L]
                s = plain.find(seg)
                while s >= 0:
                    m = ((1 << L) - 1) << s
                    if not (mask & m):
                        if go(pos + L, mask | m, left - 1): return True
                    s = plain.find(seg, s + 1)
            memo.add(key); return False
        if go(0, 0, K): return K
    return None

out = {}
for name, (cipher, plain) in LINES.items():
    c, p = cipher.upper(), plain.upper()
    assert sorted(c) == sorted(p), (name, 'character multisets (spaces included) differ')
    chars = list(p)
    obs = bigram_hits(p, c)
    obs_sp = bigram_hits(p, c, True)
    n_sp_pairs = sum(1 for i in range(len(p) - 1) if ' ' in p[i:i + 2])
    N = 20000
    rnd = []; rnd_sp = []
    for _ in range(N):
        random.shuffle(chars)
        s = "".join(chars)
        rnd.append(bigram_hits(p, s)); rnd_sp.append(bigram_hits(p, s, True))
    t0 = time.time()
    K = mcsp(p, c)
    out[name] = dict(cipher=cipher, plain=plain, n_chars=len(p), n_spaces=p.count(' '),
                     pairs=len(p) - 1, hits=obs, rand_mean=round(sum(rnd) / N, 2), p=sum(1 for r in rnd if r >= obs) / N,
                     space_pairs=n_sp_pairs, space_hits=obs_sp, space_rand_mean=round(sum(rnd_sp) / N, 2),
                     space_p=sum(1 for r in rnd_sp if r >= obs_sp) / N, K=K, secs=round(time.time() - t0, 1))
    print(name, out[name])

# ---- line 2: all 24 word orders
cipher2, _ = LINES["line2"]
words = ["SUBVERTING", "SYSTEM", "BACKUPS", "TO"]
rows = []
for perm in itertools.permutations(words):
    p = " ".join(perm)
    rows.append(dict(order=p, hits=bigram_hits(p, cipher2.upper()), space_hits=bigram_hits(p, cipher2.upper(), True)))
t0 = time.time()
for r in rows:
    r['K'] = mcsp(r['order'], cipher2.upper(), maxK=20)
rows.sort(key=lambda r: (r['K'], -r['hits']))
out['line2_orders'] = rows
print('line2 orders (spaces as chars), sorted by K then hits  [%.0fs]' % (time.time() - t0))
for r in rows: print(r)
json.dump(out, open('../data/space_chars.json', 'w'), indent=1)
