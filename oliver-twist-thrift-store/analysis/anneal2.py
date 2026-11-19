import numpy as np, pickle, random, math, sys, collections
words,meta=pickle.load(open('seg/words_cl2.pkl','rb'))
logtri=pickle.load(open('lm/logtri.pkl','rb'))
A='abcdefghijklmnopqrstuvwxyz'
cnt=collections.Counter(c for w in words for c in w)
syms=sorted(cnt)
S=max(syms)+1
words_of=collections.defaultdict(list)
for wi,w in enumerate(words):
    for c in set(w): words_of[c].append(wi)
LAM=float(sys.argv[2]) if len(sys.argv)>2 else 1.0
def wscore(w,m):
    a=b=0; s=0.0
    for c in w:
        x=m[c]; s+=logtri[a,b,x]; a,b=b,x
    return s+logtri[a,b,0]
def hscore(m):
    N=collections.Counter()
    for c in syms: N[m[c]]+=cnt[c]
    return sum(cnt[c]*math.log(cnt[c]/N[m[c]]) for c in syms)
def run(seed,iters=50000,T0=3.0,T1=0.1):
    rng=random.Random(seed)
    m=[0]*S
    for c in syms: m[c]=rng.randint(1,26)
    ws=[wscore(w,m) for w in words]
    cur=sum(ws)+LAM*hscore(m)
    best=(cur,m[:])
    for it in range(iters):
        T=T0*(T1/T0)**(it/iters)
        c=rng.choice(syms); old=m[c]
        if rng.random()<0.35:
            d=rng.choice(syms)
            if d==c or m[d]==m[c]: continue
            m[c],m[d]=m[d],m[c]
            aff=set(words_of[c])|set(words_of[d])
            new={wi:wscore(words[wi],m) for wi in aff}
            delta=sum(new[wi]-ws[wi] for wi in aff)  # swap doesn't change H
            if delta>=0 or rng.random()<math.exp(delta/T):
                for wi in aff: ws[wi]=new[wi]
                cur+=delta
            else: m[c],m[d]=m[d],m[c]
        else:
            nl=rng.randint(1,26)
            if nl==old: continue
            h0=hscore(m)
            m[c]=nl
            aff=words_of[c]
            new={wi:wscore(words[wi],m) for wi in aff}
            delta=sum(new[wi]-ws[wi] for wi in aff)+LAM*(hscore(m)-h0)
            if delta>=0 or rng.random()<math.exp(delta/T):
                for wi in aff: ws[wi]=new[wi]
                cur+=delta
            else: m[c]=old
        if cur>best[0]: best=(cur,m[:])
    return best
if __name__=='__main__':
    res=[]
    for seed in range(int(sys.argv[1])):
        b=run(seed); res.append(b); print(seed,round(b[0],1),flush=True)
    res.sort(key=lambda t:-t[0]); m=res[0][1]
    pickle.dump(res,open('seg/anneal2_res.pkl','wb'))
    used=collections.Counter(); 
    for c in syms: used[A[m[c]-1]]+=cnt[c]
    print(sorted(used.items(),key=lambda t:-t[1]))
    for wi in range(0,50): print(''.join(A[m[c]-1] for c in words[wi]),end=' ')
    print()
