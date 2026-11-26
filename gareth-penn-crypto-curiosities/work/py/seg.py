import math, sys, heapq
sys.path.insert(0,'.')
from penn import BITS
def load_words(n=60000, extra=()):
    W={}
    for i,line in enumerate(open('/Users/doranchak/projects/github/misc-crypto-mysteries/skydrop-scroll-puzzle/data/words60k.txt')):
        if i>=n: break
        w,c=line.split(); 
        if w.isalpha(): W[w.upper()]=int(c)
    tot=sum(W.values())
    LP={w:math.log10(c/tot) for w,c in W.items()}
    for w in open('/usr/share/dict/propernames').read().split():
        if w.isalpha(): LP.setdefault(w.upper(), -7.0)
    for w in extra: LP[w.upper()]=-5.0
    # single letters other than A, I are unlikely
    for c in 'BCDEFGHJKLMNOPQRSTUVWXYZ': LP[c]=-9.0
    return LP
def build_trie(LP):
    T={}
    for w,lp in LP.items():
        b=''.join(BITS[c] for c in w)
        T.setdefault(b,[]).append((lp,w))
    for b in T: T[b].sort(reverse=True); T[b]=T[b][:6]
    maxlen=max(len(b) for b in T)
    return T,maxlen
def segment(B, T, maxlen, K=30, open_end=False, lead0=4):
    """K-best segmentations of bitstring B into dictionary words. open_end: last word may extend past B (truncated)."""
    best=[[] for _ in range(len(B)+1)]
    starts=[]
    for z in range(lead0+1):
        best[0].append((0.0,[] ,z))
    # handle leading zeros by prefixing
    results=[]
    for z in range(lead0+1):
        BB='0'*z+B
        beam=[[] for _ in range(len(BB)+1)]
        beam[0]=[(0.0,())]
        for i in range(len(BB)):
            if not beam[i]: continue
            beam[i]=heapq.nlargest(K,beam[i])
            for L in range(1,min(maxlen,len(BB)-i)+1):
                key=BB[i:i+L]
                if key in T:
                    for lp,w in T[key][:3]:
                        for s,ws in beam[i]:
                            beam[i+L].append((s+lp,ws+(w,)))
            if open_end:
                # allow final word whose encoding starts with remaining suffix
                rem=BB[i:]
                if len(rem)>=3:
                    for b,lst in PREFIX.get(rem,[]) if False else []:
                        pass
        for s,ws in heapq.nlargest(K,beam[len(BB)]):
            results.append((s,z,' '.join(ws)))
    results.sort(reverse=True)
    seen=set(); out=[]
    for r in results:
        if r[2] not in seen: seen.add(r[2]); out.append(r)
    return out[:K]
if __name__=='__main__':
    LP=load_words(extra=['OHARE','MIKE','ZODIAC','PENN','GARETH','RADIAN','OHARES'])
    T,ml=build_trie(LP)
    for arg in sys.argv[1:]:
        B = bin(int(arg))[2:] if arg.isdigit() else arg
        print('==',arg,B)
        for s,z,ws in segment(B,T,ml,K=25): print(f'{s:8.2f} lead0={z} {ws}')
