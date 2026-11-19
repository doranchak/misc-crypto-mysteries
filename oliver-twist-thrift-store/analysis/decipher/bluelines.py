import pickle, numpy as np
comps=pickle.load(open('blue_comps.pkl','rb'))
cs=[dict(x=c[0],y=c[1],w=c[2],h=c[3],cx=c[0]+c[2]/2,cy=c[1]+c[3]/2) for c in comps]
cs.sort(key=lambda c:c['cx'])
par=list(range(len(cs)))
def find(a):
    while par[a]!=a: par[a]=par[par[a]]; a=par[a]
    return a
for i,c in enumerate(cs):
    best=None
    for j in range(i-1,-1,-1):
        q=cs[j]; dx=c['cx']-q['cx']
        if dx>75: break
        dy=abs(c['cy']-q['cy'])
        if dy<9:
            sc=dx+4*dy
            if best is None or sc<best[0]: best=(sc,j)
    if best: par[find(i)]=find(best[1])
import collections
g=collections.defaultdict(list)
for i,c in enumerate(cs): g[find(i)].append(c)
lines=sorted([sorted(v,key=lambda c:c['cx']) for v in g.values()],key=lambda l:np.mean([c['cy'] for c in l]))
for l in lines: print(len(l), int(np.mean([c['cy'] for c in l])), int(l[0]['x']), int(l[-1]['x']+l[-1]['w']))
pickle.dump(lines,open('blue_lines.pkl','wb'))
