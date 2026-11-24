import sys, random, statistics
sys.path.insert(0,'.')
import solve_word as W, solve_mono as S
ws=W.build_words(S.segD)
real=W.solve(ws,restarts=30,iters=5000,seed=1)[1][0]
glyphs=[g for w in ws for g in w]
rnd=random.Random(9); nulls=[]
for k in range(6):
    g=glyphs[:]; rnd.shuffle(g); it=iter(g)
    w2=[[next(it) for _ in w] for w in ws]
    nulls.append(W.solve(w2,restarts=30,iters=5000,seed=k)[1][0])
print('real',round(real,1),'nulls',[round(x,1) for x in nulls],'mean',round(statistics.mean(nulls),1),'sd',round(statistics.pstdev(nulls),1))
