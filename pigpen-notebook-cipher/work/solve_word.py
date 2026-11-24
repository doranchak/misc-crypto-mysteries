import sys, random, math
sys.path.insert(0,'.')
import wordlm
from transcript import LINES
import solve_mono as S
def build_words(seg, lines=LINES, drop=()):
    ws=[]
    for li,l in enumerate(lines):
        if li in drop: continue
        for w in l:
            g=seg(w)
            if g: ws.append(g)
    return ws
def solve(ws, restarts=40, iters=6000, seed=1, fixed=None):
    syms=sorted(set(g for w in ws for g in w)); n=len(syms); idx={s:i for i,s in enumerate(syms)}
    seqs=[[idx[g] for g in w] for w in ws]
    rnd=random.Random(seed)
    def score(m):
        t=0.0
        for sq in seqs:
            t+=wordlm.wscore(''.join(chr(65+m[x]) for x in sq))
        return t
    best=(-1e18,None)
    for r in range(restarts):
        letters=list(range(26)); rnd.shuffle(letters)
        m=letters[:n] if n<=26 else [rnd.randrange(26) for _ in range(n)]
        cur=score(m)
        for it in range(iters):
            temp=3.0*(1-it/iters)+0.1
            m2=m[:]
            if rnd.random()<0.35:
                i=rnd.randrange(n)
                if n<=26:
                    free=[x for x in range(26) if x not in m2]
                    if not free: continue
                    m2[i]=rnd.choice(free)
                else: m2[i]=rnd.randrange(26)
            else:
                i,j=rnd.sample(range(n),2); m2[i],m2[j]=m2[j],m2[i]
            s2=score(m2)
            if s2>=cur or rnd.random()<math.exp((s2-cur)/temp):
                m,cur=m2,s2
                if cur>best[0]: best=(cur,m[:])
    return syms,best
def show(ws,syms,m):
    d={s:chr(65+m[i]) for i,s in enumerate(syms)}
    return ' '.join(''.join(d[g] for g in w) for w in ws)
if __name__=='__main__':
    ws=build_words(S.segD)
    syms,(sc,m)=solve(ws,restarts=int(sys.argv[1]),iters=int(sys.argv[2]))
    print(sc, sc/len(ws)); print(show(ws,syms,m)); print({s:chr(65+m[i]) for i,s in enumerate(syms)})
