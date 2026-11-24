import sys, random, statistics
sys.path.insert(0,'.')
import solve_word as W, solve_mono as S
ws=W.build_words(S.segD)
real=W.solve(ws,restarts=30,iters=5000,seed=1)[1][0]
distinct=[]; seen={}
for w in ws:
    t=tuple(w)
    if t not in seen: seen[t]=len(distinct); distinct.append(list(w))
print('words',len(ws),'distinct',len(distinct))
glyphs=[g for w in distinct for g in w]
rnd=random.Random(21); nulls=[]
for k in range(8):
    g=glyphs[:]; rnd.shuffle(g); it=iter(g)
    nd=[[next(it) for _ in w] for w in distinct]
    w2=[nd[seen[tuple(w)]] for w in ws]
    nulls.append(W.solve(w2,restarts=30,iters=5000,seed=k)[1][0])
print('real',round(real,1),'nulls',[round(x,1) for x in nulls],'mean',round(statistics.mean(nulls),1),'sd',round(statistics.pstdev(nulls),1), 'z',round((real-statistics.mean(nulls))/statistics.pstdev(nulls),1))
