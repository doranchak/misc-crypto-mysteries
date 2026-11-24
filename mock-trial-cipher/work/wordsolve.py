import random, math, sys
from collections import Counter
txt=open('corpus_clean.txt').read().split()
wc=Counter(txt)
vocab={w:math.log(1+c) for w,c in wc.items() if c>=3 and (len(w)>1 or w in ('A','I'))}
print('vocab',len(vocab),file=sys.stderr)
def load(merge=None,drop=('X','-','?','_')):
    ws=[]
    for l in open('transcript_v1.txt'):
        w=[]
        for t in l.split():
            if t=='|':
                if w: ws.append(w); w=[]
            elif t in drop: continue
            else: w.append(merge.get(t,t) if merge else t)
        if w: ws.append(w)
    return ws
def solve(ws,iters=40000,restarts=12,seed=0,fix=None):
    rnd=random.Random(seed)
    syms=sorted(set(t for w in ws for t in w))
    letters=[chr(65+i) for i in range(26)]
    best=(-1,None)
    uniq=Counter(tuple(w) for w in ws)
    items=list(uniq.items())
    def sc(m):
        s=0.0
        for w,c in items:
            word=''.join(m[t] for t in w)
            v=vocab.get(word)
            if v: s+=v*len(word)**0.5*c
        return s
    for r in range(restarts):
        pool=letters[:]; rnd.shuffle(pool)
        m={s:pool[i] for i,s in enumerate(syms)}
        if fix:
            for s,L in fix.items():
                # swap
                cur=m[s]
                if cur!=L:
                    other=[k for k,v in m.items() if v==L]
                    if other: m[other[0]]=cur
                    m[s]=L
        free=[s for s in syms if not (fix and s in fix)]
        cur=sc(m)
        for it in range(iters):
            T=2.0*(0.02/2.0)**(it/iters)
            a=rnd.choice(free)
            used=set(m.values()); L=rnd.choice(letters)
            if fix and L in fix.values(): continue
            old=m[a]
            if L==old: continue
            other=[k for k,v in m.items() if v==L]
            m[a]=L
            if other: m[other[0]]=old
            ns=sc(m)
            if ns>=cur or math.exp((ns-cur)/T)>rnd.random(): cur=ns
            else:
                m[a]=old
                if other: m[other[0]]=L
        if cur>best[0]: best=(cur,dict(m))
    return best
if __name__=='__main__':
    ws=load()
    b=solve(ws,fix=None if len(sys.argv)<2 else {'A':'T','U':'H','R':'E'})
    print(round(b[0],1))
    m=b[1]; print(m)
    print(' '.join(''.join(m[t] for t in w) for w in ws))
