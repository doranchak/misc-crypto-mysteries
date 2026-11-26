import re, collections
D='/private/tmp/claude-501/-Users-doranchak-projects-github-misc-crypto-mysteries/6559da2e-315e-4764-b182-03e1130553e5/scratchpad/dl/people.tsv'
def key(s): return ''.join(sorted(c for c in s.upper() if c.isalpha()))
idx=collections.defaultdict(set)
for line in open(D,encoding='utf-8'):
    f=line.rstrip('\n').split('\t')
    m=re.match(r'"(.*)"@en',f[0])
    if not m: continue
    name=m.group(1)
    b=f[1][1:5] if len(f)>1 and f[1] else ''; d=f[2][1:5] if len(f)>2 and f[2] else ''
    idx[key(name)].add(f'{name} ({b}-{d})')
    # surname only and first name only variants
    parts=name.split()
    if len(parts)>=2: idx[key(parts[-1])].add(f'[surname] {name} ({b}-{d})')
for L in [l.strip() for l in open('lines.txt') if l.strip()]:
    h=idx.get(key(L))
    if h: print(f'{L:28s} -> {sorted(h)[:6]}')
