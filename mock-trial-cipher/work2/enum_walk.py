import sys, os, itertools, random, json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from walkmodels import *
from multiprocessing import Pool
def task(args):
    name,cfg,shuf=args
    grid,wrap,mult,hsem,vsem,esem,home,reset=cfg
    chunks=CHUNKS
    if shuf is not None:
        rng=random.Random(shuf)
        flat=list(''.join(''.join(l) for l in chunks)); rng.shuffle(flat)
        it=iter(flat); chunks=[[ ''.join(next(it) for _ in c) for c in l] for l in chunks]
    cells,ws=simulate(chunks,grid,wrap,mult,hsem,vsem,esem,home,reset)
    r=solve_tokens(cells,ws,0,f'{name}_{os.getpid()}',restarts=4,iters=200000,seed=7)
    if r is None: return (name,shuf,None)
    cov=coverage(r['text'])
    return (name,shuf,dict(score=r['score'],ncells=r['ncells'],cov=cov,text=r['text'][:150]))
if __name__=='__main__':
    grids=[((5,5),'torus'),((5,5),'clamp'),((6,4),'torus'),((2,13),'torus'),((3,8),'torus'),((4,6),'clamp')]
    hv=[('stay',('t',0,0),('t',0,0)),('mirror',('fx',),('fy',)),('two',('t',2,0),('t',0,2))]
    tasks=[]
    # baseline mono
    for mdl in itertools.product([1,2],repeat=5):
        mult=dict(zip(['dbl','thin','foot','fill','hol'],mdl))
        for (grid,wrap) in grids:
            for hvn,hs,vs in hv:
                home=(grid[0]//2,grid[1]//2) if wrap=='clamp' else (0,0)
                name=f"{grid[0]}x{grid[1]}{wrap[0]}_m{''.join(map(str,mdl))}_hv{hvn}"
                cfg=(grid,wrap,mult,hs,vs,('fx',),home,'word')
                tasks.append((name,cfg,None))
    print(len(tasks),'tasks',flush=True)
    with Pool(17) as p: res=p.map(task,tasks,chunksize=4)
    json.dump(res,open('walk_enum_real.json','w'))
    ok=[r for r in res if r[2]]
    ok.sort(key=lambda r:-r[2]['score'])
    for r in ok[:15]: print(r[0],round(r[2]['score'],1),r[2]['ncells'],r[2]['cov'])
