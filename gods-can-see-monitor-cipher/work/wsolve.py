import math,random,sys,collections
# --- transcription (class names), groups separated by '|', lines by '/'
TX=("Zo dot CrossTri Phead HLT | ArchTri dot | HLT dot Psi Alpha PheadT | Obar Aloop Head8T Phead LoopTri HeadLegs Ou Oright Alpha Sbar / "
    "dot Zo LoopTri StemWings | ArchTri dot | Oright dot Zo Sbar Alpha Zo ArchTri Obar Zo OrDown | Xeq9 dot StemWings Unk1 Dee LoopTri / "
    "Head8T Alpha Phead Dee Angel StemWings | amp | Pin Alpha Sbar ArchTri Alpha ArchTri Obar Oright Sbar")
def groups(tx,drop_unk=False):
    gs=[]
    for line in tx.split('/'):
        for g in line.split('|'):
            t=g.split()
            if t: gs.append(t)
    return gs
WL={}
tot=0
for line in open('/Users/doranchak/projects/github/misc-crypto-mysteries/skydrop-scroll-puzzle/data/words60k.txt'):
    w,c=line.split(); c=int(c)
    if not w.isalpha(): continue
    if len(w)==1 and w not in ('A','I'): continue
    WL[w]=WL.get(w,0)+c; tot+=c
LP={w:math.log(c/tot) for w,c in WL.items()}
MAXL=max(len(w) for w in LP)
OOV=-30.0; SPLIT=-4.0
def seg_score(s):
    # best segmentation of string s into dictionary words
    n=len(s); best=[-1e18]*(n+1); best[0]=0.0
    for i in range(1,n+1):
        for j in range(max(0,i-MAXL),i):
            w=s[j:i]; lp=LP.get(w)
            if lp is None:
                lp=OOV*(i-j) if i-j<=2 else None
                if lp is None: continue
            v=best[j]+lp+(SPLIT if j>0 else 0)
            if v>best[i]: best[i]=v
    return best[n]
def seg_words(s):
    n=len(s); best=[(-1e18,None)]*(n+1); best[0]=(0.0,None)
    for i in range(1,n+1):
        for j in range(max(0,i-MAXL),i):
            w=s[j:i]; lp=LP.get(w)
            if lp is None:
                lp=OOV*(i-j) if i-j<=2 else None
                if lp is None: continue
            v=best[j][0]+lp+(SPLIT if j>0 else 0)
            if v>best[i][0]: best[i]=(v,j)
    out=[];i=n
    while i>0:
        j=best[i][1]; out.append(s[j:i]); i=j
    return ' '.join(reversed(out))
FIXED={'amp':None}
def solve(gs,iters=40000,seed=0,T0=6.0,fixed=None):
    rnd=random.Random(seed)
    syms=sorted({s for g in gs for s in g if s!='amp'})
    letters=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    key={s:letters[i] for i,s in enumerate(rnd.sample(range(26),len(syms)))} if True else None
    key=dict(zip(syms,rnd.sample(letters,len(syms))))
    if fixed: 
        for s,l in fixed.items():
            for t,v in list(key.items()):
                if v==l and t!=s: key[t]=key[s]
            key[s]=l
    def score(k):
        tot=0.0
        for g in gs:
            if g==['amp']: continue
            tot+=seg_score(''.join(k[s] for s in g))
        return tot
    cur=score(key); best=(cur,dict(key))
    for it in range(iters):
        T=T0*(1-it/iters)+0.05
        k2=dict(key)
        s=rnd.choice(syms)
        if fixed and s in fixed: continue
        l=rnd.choice(letters)
        other=[t for t,v in k2.items() if v==l]
        if other:
            if fixed and other[0] in fixed: continue
            k2[other[0]]=k2[s]
        k2[s]=l
        sc=score(k2)
        if sc>cur or rnd.random()<math.exp((sc-cur)/T):
            key,cur=k2,sc
            if cur>best[0]: best=(cur,dict(key))
    return best
def render(gs,key):
    return ' | '.join('&' if g==['amp'] else seg_words(''.join(key[s] for s in g)) for g in gs)
if __name__=='__main__':
    gs=groups(TX)
    mode=sys.argv[1] if len(sys.argv)>1 else 'real'
    nrun=int(sys.argv[2]) if len(sys.argv)>2 else 6
    iters=int(sys.argv[3]) if len(sys.argv)>3 else 20000
    if mode=='null':
        flat=[s for g in gs for s in g if s!='amp']
        rnd=random.Random(int(sys.argv[4]) if len(sys.argv)>4 else 1)
        rnd.shuffle(flat); it=iter(flat)
        gs=[['amp'] if g==['amp'] else [next(it) for _ in g] for g in gs]
    res=[]
    for seed in range(nrun):
        sc,k=solve(gs,iters=iters,seed=seed)
        res.append((sc,k)); print(round(sc,1),render(gs,k),flush=True)
