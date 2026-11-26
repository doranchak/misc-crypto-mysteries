import json, re, collections
D='/private/tmp/claude-501/-Users-doranchak-projects-github-misc-crypto-mysteries/6559da2e-315e-4764-b182-03e1130553e5/scratchpad/dl/cities500.txt'
STATES={'AL':'Alabama','AK':'Alaska','AZ':'Arizona','AR':'Arkansas','CA':'California','CO':'Colorado','CT':'Connecticut','DE':'Delaware','FL':'Florida','GA':'Georgia','HI':'Hawaii','ID':'Idaho','IL':'Illinois','IN':'Indiana','IA':'Iowa','KS':'Kansas','KY':'Kentucky','LA':'Louisiana','ME':'Maine','MD':'Maryland','MA':'Massachusetts','MI':'Michigan','MN':'Minnesota','MS':'Mississippi','MO':'Missouri','MT':'Montana','NE':'Nebraska','NV':'Nevada','NH':'New Hampshire','NJ':'New Jersey','NM':'New Mexico','NY':'New York','NC':'North Carolina','ND':'North Dakota','OH':'Ohio','OK':'Oklahoma','OR':'Oregon','PA':'Pennsylvania','RI':'Rhode Island','SC':'South Carolina','SD':'South Dakota','TN':'Tennessee','TX':'Texas','UT':'Utah','VT':'Vermont','VA':'Virginia','WA':'Washington','WV':'West Virginia','WI':'Wisconsin','WY':'Wyoming'}
def key(s): return ''.join(sorted(c for c in s.upper() if c.isalpha()))
idx=collections.defaultdict(set)
for line in open(D,encoding='utf-8'):
    f=line.split('\t'); name=f[2]; cc=f[8]; a1=f[10]; pop=int(f[14] or 0)
    if not re.fullmatch(r"[A-Za-z .'-]+",name): continue
    idx[key(name)].add(f'{name} [{cc}/{a1}] pop{pop}')
    if cc=='US' and a1 in STATES:
        idx[key(name+STATES[a1])].add(f'{name}, {STATES[a1]}')
        idx[key(name+a1)].add(f'{name} {a1}')
V=json.load(open('verses.json'))
lines=set()
for v in V.values():
    pass
LINES=[l.strip() for l in open('lines.txt') if l.strip()]
for L in LINES:
    k=key(L)
    hits=idx.get(k)
    if hits: print(f'{L:28s} -> {sorted(hits)[:8]}')
