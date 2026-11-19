import numpy as np, pickle, random, math, sys, collections
words0,meta=pickle.load(open('seg/words_cl2.pkl','rb'))
logtri=pickle.load(open('lm/logtri_en.pkl','rb'))
A='abcdefghijklmnopqrstuvwxyz'
fam={14:'phi',26:'phi',29:'dot',34:'dot',18:'dot',32:'F',31:'3',25:'Zb',22:'Zd',24:'pr',5:'pr',9:'+',1:'V',10:'/.',16:'WS',11:'WS',35:'h7',13:'h7',21:'h7',12:'h7',30:'M7',17:'M7',33:'Yb',27:'Yl',28:'cb',20:'Rn',8:'Rn',3:'/',4:'/'}
famid={}
def fid(c):
    f=fam.get(c,'c%d'%c)
    if f not in famid: famid[f]=len(famid)
    return famid[f]
words=[[fid(c) for c in w] for w in words0]
names={v:k for k,v in famid.items()}
S=len(famid)
cnt=collections.Counter(c for w in words for c in w)
syms=sorted(cnt)
anchors={}
for arg in sys.argv[2:]:
    f,l=arg.split('='); anchors[famid[f]]=A.index(l)+1
words_of=collections.defaultdict(list)
for wi,w in enumerate(words):
    for c in set(w): words_of[c].append(wi)
LAM=float(sys.argv[1])
def wscore(w,m):
    a=b=0; s=0.0
    for c in w:
        x=m[c]; s+=logtri[a,b,x]; a,b=b,x
    return s+logtri[a,b,0]
def hscore(m):
    N=collections.Counter()
    for c in syms: N[m[c]]+=cnt[c]
    return sum(cnt[c]*math.log(cnt[c]/N[m[c]]) for c in syms)
free=[c for c in syms if c not in anchors]
def run(seed,iters=40000,T0=3.0,T1=0.1):
    rng=random.Random(seed)
    m=[0]*S
    for c in syms: m[c]=anchors.get(c,rng.randint(1,26))
    ws=[wscore(w,m) for w in words]
    cur=sum(ws)+LAM*hscore(m); best=(cur,m[:])
    for it in range(iters):
        T=T0*(T1/T0)**(it/iters)
        c=rng.choice(free); old=m[c]
        nl=rng.randint(1,26)
        if nl==old: continue
        h0=hscore(m); m[c]=nl
        aff=words_of[c]
        new={wi:wscore(words[wi],m) for wi in aff}
        delta=sum(new[wi]-ws[wi] for wi in aff)+LAM*(hscore(m)-h0)
        if delta>=0 or rng.random()<math.exp(delta/T):
            for wi in aff: ws[wi]=new[wi]
            cur+=delta
        else: m[c]=old
        if cur>best[0]: best=(cur,m[:])
    return best
res=[run(s) for s in range(8)]
res.sort(key=lambda t:-t[0])
print('scores',[round(r[0]) for r in res])
m=res[0][1]
print({names[c]:A[m[c]-1] for c in syms})
for wi in range(0,45): print(''.join(A[m[c]-1] for c in words[wi]),end=' ')
print()
