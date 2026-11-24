import sys
sys.path.insert(0,'.')
import solve_word as W, solve_mono as S
from transcript import LINES
ws=W.build_words(S.segD)
best=None
for seed in range(1,6):
    syms,(sc,m)=W.solve(ws,restarts=30,iters=5000,seed=seed)
    d={s:chr(65+m[i]) for i,s in enumerate(syms)}
    print(seed, round(sc,1), ' '.join(''.join(d[g] for g in w) for w in ws))
    if best is None or sc>best[0]: best=(sc,d)
print()
d=best[1]
for li,l in enumerate(LINES,1):
    out=[]
    for w in l:
        g=S.segD(w); out.append(''.join(d[x] for x in g))
    print(li, ' | '.join(f'{w} -> {o}' for w,o in zip(l,out)))
print(sorted(d.items()))
