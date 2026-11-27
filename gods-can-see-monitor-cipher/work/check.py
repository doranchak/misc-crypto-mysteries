import sys,random
sys.argv=[sys.argv[0]]
import wsolve as W
TXM=("N O F A P | T O | P O W E R | I M B A L A N C E S / "
     "O N L Y | T O | C O N S E N T I N G | J O Y F U L / "
     "B E A U T Y | amp | A E S T E T I C S")
gs=W.groups(TXM)
# score of the true key (identity mapping on these letter-named classes)
ident={s:s for g in gs for s in g if s!='amp'}
print('true-key score',round(sum(W.seg_score(''.join(g)) for g in gs if g!=['amp']),1))
print(W.render(gs,ident))
# blind solver on the merged transcription (letters relabelled to opaque symbols)
syms=sorted(ident); rnd=random.Random(7); lab=dict(zip(syms,['g%02d'%i for i in range(len(syms))]))
gsb=[['amp'] if g==['amp'] else [lab[s] for s in g] for g in gs]
best=None
for seed in range(10):
    sc,k=W.solve(gsb,iters=60000,seed=seed)
    print(round(sc,1),W.render(gsb,k)); 
    if best is None or sc>best[0]: best=(sc,k)
flat=[s for g in gsb for s in g if s!='amp']
nb=[]
for ns in range(10):
    r=random.Random(100+ns); f=flat[:]; r.shuffle(f); it=iter(f)
    gn=[['amp'] if g==['amp'] else [next(it) for _ in g] for g in gsb]
    b=max(W.solve(gn,iters=60000,seed=s)[0] for s in range(4))
    nb.append(round(b,1))
print('null bests',sorted(nb))
