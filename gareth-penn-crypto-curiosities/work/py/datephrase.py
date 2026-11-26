import json, re, collections, itertools, datetime
from collections import Counter
import sys; sys.path.insert(0,"/Users/doranchak/projects/github/misc-crypto-mysteries/gareth-penn-crypto-curiosities/work/py")
from states import STATES
G='/private/tmp/claude-501/-Users-doranchak-projects-github-misc-crypto-mysteries/6559da2e-315e-4764-b182-03e1130553e5/scratchpad/dl/cities500.txt'
ONES='ZERO ONE TWO THREE FOUR FIVE SIX SEVEN EIGHT NINE TEN ELEVEN TWELVE THIRTEEN FOURTEEN FIFTEEN SIXTEEN SEVENTEEN EIGHTEEN NINETEEN'.split()
TENS={2:'TWENTY',3:'THIRTY',4:'FORTY',5:'FIFTY',6:'SIXTY',7:'SEVENTY',8:'EIGHTY',9:'NINETY'}
ORD={'ONE':'FIRST','TWO':'SECOND','THREE':'THIRD','FIVE':'FIFTH','EIGHT':'EIGHTH','NINE':'NINTH','TWELVE':'TWELFTH'}
def card(n):
    if n<20: return ONES[n]
    t,o=divmod(n,10); return TENS[t]+('' if o==0 else ONES[o])
def ordn(n):
    w=card(n)
    for k,v in ORD.items():
        if w.endswith(k): return w[:-len(k)]+v
    if w.endswith('Y'): return w[:-1]+'IETH'
    return w+'TH'
def years(y):
    out={ 'TWOTHOUSAND'+('' if y==2000 else card(y-2000)) }
    if y>=2010: out.add('TWENTY'+card(y-2000))
    out.add(card(y//100)+('HUNDRED' if y%100==0 else card(y%100)) if y<2000 else 'TWENTY'+('HUNDRED' if y%100==0 else card(y%100)) if y%100>=10 else 'TWENTYOH'+card(y%100))
    return out
MONTHS='JANUARY FEBRUARY MARCH APRIL MAY JUNE JULY AUGUST SEPTEMBER OCTOBER NOVEMBER DECEMBER'.split()
def C(s): return Counter(c for c in s.upper() if c.isalpha())
def key(c): return ''.join(sorted(c.elements()))
# place index (US)
pidx=collections.defaultdict(set)
for line in open(G,encoding='utf-8'):
    f=line.split('\t')
    if f[8]!='US' or f[10] not in STATES: continue
    name=f[2]
    if not re.fullmatch(r"[A-Za-z .'-]+",name): continue
    st=STATES[f[10]]
    pidx[key(C(name+st))].add(f'{name}, {st}')
    pidx[key(C(name+f[10]))].add(f'{name} {f[10]}')
    pidx[key(C(name))].add(f'{name} ({f[10]})')
for st,full in STATES.items(): pass
V=json.load(open('verses.json'))
d0=datetime.date(2000,1,1); found=0
datephr=[]
for i in range((datetime.date(2035,12,31)-d0).days+1):
    d=d0+datetime.timedelta(i)
    for y in years(d.year):
        for dw in (card(d.day),ordn(d.day)):
            for pre in ('','DATE','ON','DATEON'):
                for at in ('AT','','IN'):
                    datephr.append((f'{d.isoformat()} {pre}|{dw}|{y}|{at}', C(pre+MONTHS[d.month-1]+dw+y+at)))
print('date phrases',len(datephr))
for k,s in V.items():
    vc=C(s); hits=[]
    for lab,dc in datephr:
        if dc-vc: continue
        rem=vc-dc
        h=pidx.get(key(rem))
        if h: hits.append((lab,sorted(h)[:4]))
    print(k, len(hits), hits[:6])
