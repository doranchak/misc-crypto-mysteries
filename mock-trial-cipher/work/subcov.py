import json, subprocess, random, statistics
from collections import Counter
exec(open('experiments.py').read().split("R={}")[0])   # reuse helpers (lines, words, flat, coverage, hc)
R=json.load(open('results.json'))
tri=set('APTQaptq')
g=lambda l:[x for x in l if x not in drop and x!='|']
subs={'arrows only':[t for t in flat if t not in tri],'triangles only':[t for t in flat if t in tri],
 'every 2nd glyph (phase 0)':[t for l in lines for t in g(l)[0::2]],'every 2nd glyph (phase 1)':[t for l in lines for t in g(l)[1::2]],
 'every 3rd glyph (phase 0)':[t for l in lines for t in g(l)[0::3]]}
for k,s in subs.items():
    sc,mp,pt=hc(s,1,40)
    nn=[];cv=[]
    for t in range(6):
        q=s[:]; random.Random(t).shuffle(q); a,b,c=hc(q,t+2,40); nn.append(a); cv.append(coverage(c))
    R['subsets'][k].update(score=sc,coverage=coverage(pt),null_mean=statistics.mean(nn),null_sd=statistics.pstdev(nn),null_cov=statistics.mean(cv))
    print(k,R['subsets'][k])
json.dump(R,open('results.json','w'),indent=1)
