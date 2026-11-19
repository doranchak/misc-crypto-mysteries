import pickle, collections, math, random, sys
import numpy as np
words,meta=pickle.load(open('seg/words_cl2.pkl','rb'))
fam={14:'phi',29:'dot',33:'Yb',32:'F',31:'3',25:'Zb',22:'Zd',24:'pr',9:'+',1:'V',10:'/.',16:'WS',11:'WS',35:'h7',13:'h7',21:'h7',12:'h7',30:'M7',17:'M7',28:'cb',27:'Yl'}
# keep only words whose pieces are all 'reliable' clusters
W=[]
for w in words:
    if all(c in fam for c in w): W.append([fam[c] for c in w])
print('clean words',len(W),'letters',sum(len(w) for w in W))
fams=sorted({f for w in W for f in w}); fid={f:i for i,f in enumerate(fams)}
Wi=[[fid[f] for f in w] for w in W]
logtri=pickle.load(open('lm/logtri_en.pkl','rb')); A='abcdefghijklmnopqrstuvwxyz'
cnt=collections.Counter(c for w in Wi for c in w)
words_of=collections.defaultdict(list)
for wi,w in enumerate(Wi):
    for c in set(w): words_of[c].append(wi)
def wscore(w,m):
    a=b=0;s=0.0
    for c in w:
        x=m[c]; s+=logtri[a,b,x]; a,b=b,x
    return s+logtri[a,b,0]
anch={fid['Yb']:'e',fid['dot']:'h',fid['phi']:'a',fid['Yl']:'t'}
anch={k:A.index(v)+1 for k,v in anch.items()}
def run(seed,iters=20000):
    rng=random.Random(seed)
    m=[0]*len(fams)
    nfree=[c for c in range(len(fams)) if c not in anch]
    letters=[l for l in range(1,27) if l not in anch.values()]
    rng.shuffle(letters)
    for c,l in anch.items(): m[c]=l
    for c,l in zip(nfree,letters): m[c]=l   # bijection
    ws=[wscore(w,m) for w in Wi]; cur=sum(ws); best=(cur,m[:])
    for it in range(iters):
        T=2.5*(0.05/2.5)**(it/iters)
        c=rng.choice(nfree); d=rng.choice(nfree)
        if c==d: continue
        m[c],m[d]=m[d],m[c]
        aff=set(words_of[c])|set(words_of[d])
        new={wi:wscore(Wi[wi],m) for wi in aff}
        delta=sum(new[wi]-ws[wi] for wi in aff)
        if delta>=0 or rng.random()<math.exp(delta/T):
            for wi in aff: ws[wi]=new[wi]
            cur+=delta
            if cur>best[0]: best=(cur,m[:])
        else: m[c],m[d]=m[d],m[c]
    return best
res=sorted([run(s) for s in range(12)],key=lambda t:-t[0])
print([round(r[0]) for r in res])
m=res[0][1]
print({fams[c]:A[m[c]-1] for c in range(len(fams))})
for w in Wi[:80]: print(''.join(A[m[c]-1] for c in w),end=' ')
print()
