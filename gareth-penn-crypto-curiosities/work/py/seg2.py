import math, sys, heapq
sys.path.insert(0,'.')
from penn import BITS
from seg import load_words, build_trie
from decimal import Decimal, getcontext
getcontext().prec=60
LP=load_words(extra=['OHARE','MIKE','ZODIAC','PENN','GARETH','RADIAN','OHARES','DIABLO','VALLEJO','BERRYESSA','RIVERSIDE','HARVARD','BERKELEY','ODEA','CAMBRIDGE','NAPA'])
T,ML=build_trie(LP)
PRE={}
for b,lst in T.items():
    for L in range(1,len(b)):
        PRE.setdefault(b[:L],[]).extend(lst[:1])
for p in PRE: PRE[p]=sorted(PRE[p],reverse=True)[:3]
def seg(B,K=40,lead0=4,open_end=True,mark=None):
    res=[]
    for z in range(lead0+1):
        BB='0'*z+B
        beam=[[] for _ in range(len(BB)+1)]; beam[0]=[(0.0,())]
        fin=[]
        for i in range(len(BB)):
            if not beam[i]: continue
            beam[i]=heapq.nlargest(K,beam[i])
            for L in range(1,min(ML,len(BB)-i)+1):
                key=BB[i:i+L]
                if key in T:
                    for lp,w in T[key][:3]:
                        for s,ws in beam[i]: beam[i+L].append((s+lp,ws+((w,i+L),)))
            if open_end and len(BB)-i>=2:
                for lp,w in PRE.get(BB[i:],[]):
                    for s,ws in beam[i]: fin.append((s+lp,ws+((w+'~',len(BB)),)))
        fin += beam[len(BB)]
        for s,ws in heapq.nlargest(K,fin):
            # mark binary point
            out=[]
            for w,end in ws: out.append(w)
            res.append((s,z,' '.join(out)))
    res.sort(reverse=True); seen=set(); o=[]
    for r in res:
        if r[2] not in seen: seen.add(r[2]); o.append(r)
    return o[:K]
def frac_bits(f, n=44):
    x=Decimal('0.'+f); b=''
    for i in range(n):
        x*=2
        if x>=1: b+='1'; x-=1
        else: b+='0'
    return b
if __name__=='__main__':
    for s in sys.argv[1:]:
        if '.' in s:
            a,f=s.split('.')
            nb = int(len(f)*3.32)   # bits supported by decimal precision
            B=bin(int(a))[2:]+frac_bits(f,nb); pt=len(bin(int(a))[2:])
            print('==',s,'bits',B[:pt]+'.'+B[pt:])
        else:
            B=bin(int(s))[2:]; print('==',s,B)
        for sc,z,ws in seg(B): print(f'{sc:8.2f} z={z} {ws}')
