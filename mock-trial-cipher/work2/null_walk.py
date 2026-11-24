import sys, os, json, itertools, random
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from enum_walk import *
import numpy as np
real=json.load(open('walk_enum_real.json'))
ok=[r for r in real if r[2]]
ok.sort(key=lambda r:-r[2]['score'])
top=[r[0] for r in ok[:8]]
# also best per grid
seen={}
for r in ok:
    k=r[0].split('_')[0]
    if k not in seen: seen[k]=r
for k,r in seen.items():
    if r[0] not in top: top.append(r[0])
def cfg_from(name):
    g,m,h=name.split('_'); a,b=g[:-1].split('x'); wrap='torus' if g[-1]=='t' else 'clamp'
    grid=(int(a),int(b)); mdl=[int(c) for c in m[1:]]
    mult=dict(zip(['dbl','thin','foot','fill','hol'],mdl))
    hvn=h[2:]; hv={'stay':(('t',0,0),('t',0,0)),'mirror':(('fx',),('fy',)),'two':(('t',2,0),('t',0,2))}[hvn]
    home=(grid[0]//2,grid[1]//2) if wrap=='clamp' else (0,0)
    return (grid,wrap,mult,hv[0],hv[1],('fx',),home,'word')
if __name__=='__main__':
    tasks=[(n,cfg_from(n),s) for n in top for s in range(1,9)]
    with Pool(17) as p: res=p.map(task,tasks)
    by={}
    for n,s,r in res:
        if r: by.setdefault(n,[]).append(r['score'])
    realsc={r[0]:r[2]['score'] for r in ok}
    print('baseline mono (24 classes): real -2030.3 null -2281 (sd 14) -> gap +251')
    for n in top:
        v=by.get(n,[])
        print(n,'ncells',dict((r[0],r[2]['ncells']) for r in ok)[n],'real',round(realsc[n],1),'null',round(np.mean(v),1),'sd',round(np.std(v),1),'gap',round(realsc[n]-np.mean(v),1))
