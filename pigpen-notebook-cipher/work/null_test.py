import sys, random
sys.path.insert(0,'.')
from solve_mono import *
toks=build_stream(LINES)
real=solve(toks,restarts=16,iters=15000,seed=3)[1][0]/len(toks)
print('real',round(real,3))
rnd=random.Random(5)
nulls=[]
glyphs=[t for t in toks if t]
for k in range(6):
    g=glyphs[:]; rnd.shuffle(g); it=iter(g)
    t2=[None if t is None else next(it) for t in toks]
    nulls.append(solve(t2,restarts=16,iters=15000,seed=k)[1][0]/len(t2))
print('nulls',[round(x,3) for x in nulls])
