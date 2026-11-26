"""Count SJP word forms fitting the title/heading as each key constraint is added."""
import sys, re
ws = [w.strip() for w in open(sys.argv[1], encoding='utf-8') if w.strip().isalpha() and w.strip().islower()]
def pattern(s):
    m = {}; return tuple(m.setdefault(c, len(m)) for c in s)
T = 'K O M U N I K A C J A'.split()     # glyph tokens: big-I == serifed I, dot, N*, V, A, S, I, box, ~, 4, box
pt = pattern(T)
w11 = [w for w in ws if len(w) == 11]
s0 = [w for w in w11 if pattern(w) == pt]
s1 = [w for w in s0 if w[1] == 'o' and w[5] == 'i']
s2 = [w for w in s1 if w[7] == 'a']
s3 = [w for w in s2 if w[4] == 'n']
print('title: 11-letter forms', len(w11), '| repeat pattern', len(s0), '| +o,i', len(s1), '| +box=a', len(s2), '| +A=n', len(s3), s3)
print('   +o,i,a list:', s2)
W = 'P R A K T Y Q A'.split()         # heading: b r box I ⊥ 4 blob box (blob free)
used = set('oeęaąnisw ldgzżkmucj'.replace(' ', ''))
w8 = [w for w in ws if len(w) == 8]
c0 = [w for w in w8 if w[2] == 'a' and w[7] == 'a' and w[3] == 'k']
c1 = [w for w in c0 if all(w[i] not in used for i in (0, 1, 4, 5)) and len({w[0], w[1], w[4], w[5]}) == 4]
print('heading: 8-letter forms', len(w8), '| ..ak...a', len(c0), '| new glyphs = unused letters', len(c1), c1)
