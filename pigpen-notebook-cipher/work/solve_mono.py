import sys, random, math, numpy as np
sys.path.insert(0,'.')
import lm
from transcript import LINES
T=lm.get().reshape(-1); V=27
SHAPES=set("UNCLOAVE<>oTQ5c")
def segD(w):
    g=[];cur=None
    for t in w:
        if t=='.': continue
        if t in SHAPES:
            if cur: g.append(cur)
            cur=[t,0]
        else:
            if cur is None: cur=['*',1]
            else: cur[1]+=1
    if cur: g.append(cur)
    return [s+('+' if m else '') for s,m in g]
def build_stream(lines, drop=()):
    toks=[]  # symbol strings; None for space
    for li,l in enumerate(lines):
        if li in drop: continue
        for w in l:
            toks += segD(w); toks.append(None)
    return toks
def solve(toks, restarts=30, iters=30000, seed=1, nletters=26):
    syms=sorted(set(t for t in toks if t))
    idx={s:i for i,s in enumerate(syms)}
    seq=np.array([-1 if t is None else idx[t] for t in toks])
    n=len(syms); rnd=random.Random(seed)
    isw=(seq==-1)
    def score(m):
        a=np.where(isw,26,m[np.where(isw,0,seq)])
        a=np.concatenate([[26],a])  # leading space
        i=((a[:-3]*V+a[1:-2])*V+a[2:-1])*V+a[3:]
        return T[i].sum()
    best=(-1e9,None)
    for r in range(restarts):
        letters=list(range(26)); rnd.shuffle(letters)
        m=np.array(letters[:n]) if n<=26 else np.array([rnd.randrange(26) for _ in range(n)])
        cur=score(m); temp0=2.0
        for it in range(iters):
            temp=temp0*(1-it/iters)+0.02
            m2=m.copy()
            if rnd.random()<0.4:
                i=rnd.randrange(n)
                if n<=26:
                    used=set(m2.tolist()); free=[x for x in range(26) if x not in used]
                    if not free: continue
                    m2[i]=rnd.choice(free)
                else:
                    m2[i]=rnd.randrange(26)
            else:
                i,j=rnd.sample(range(n),2); m2[i],m2[j]=m2[j],m2[i]
            s2=score(m2)
            if s2>=cur or rnd.random()<math.exp((s2-cur)/temp):
                m,cur=m2,s2
                if cur>best[0]: best=(cur,m.copy())
    return syms,best
def render(toks,syms,m):
    d={s:chr(65+int(m[i])) for i,s in enumerate(syms)}
    return ''.join(' ' if t is None else d[t] for t in toks)
if __name__=='__main__':
    toks=build_stream(LINES)
    syms,(sc,m)=solve(toks, restarts=int(sys.argv[1]) if len(sys.argv)>1 else 20, iters=int(sys.argv[2]) if len(sys.argv)>2 else 20000)
    n=sum(1 for t in toks if t)
    print('score/char',sc/len(toks)); print(render(toks,syms,m)); print({s:chr(65+int(m[i])) for i,s in enumerate(syms)})
