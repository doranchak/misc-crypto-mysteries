import sys, random, statistics
sys.path.insert(0,'.')
import solve_mono as S
from transcript import LINES
SH=S.SHAPES
def segA(w):
    g=[];cur=''
    for t in w:
        if t=='.': continue
        if t in SH:
            if cur: g.append(cur)
            cur=t
        else: cur+=t
    if cur: g.append(cur)
    return g
def segC(w): return [t for t in w if t!='.']
def segS(w):  # shapes only (marks dropped)
    return [t for t in w if t in SH]
def segM(w):  # marks only
    return [t for t in w if t not in SH and t!='.']
def stream(seg, drop=()):
    toks=[]
    for li,l in enumerate(LINES):
        if li in drop: continue
        for w in l:
            g=seg(w)
            if g: toks+=g; toks.append(None)
    return toks
def run(name, seg, nn=5, restarts=10, iters=12000):
    toks=stream(seg)
    n_sym=len(set(t for t in toks if t))
    syms,(sc,m)=S.solve(toks,restarts=restarts,iters=iters,seed=7)
    real=sc/len(toks)
    rnd=random.Random(11); nulls=[]
    glyphs=[t for t in toks if t]
    for k in range(nn):
        g=glyphs[:]; rnd.shuffle(g); it=iter(g)
        t2=[None if t is None else next(it) for t in toks]
        nulls.append(S.solve(t2,restarts=restarts,iters=iters,seed=k)[1][0]/len(t2))
    mu=statistics.mean(nulls); sd=statistics.pstdev(nulls) or 1e-9
    print(f'{name}: glyphs={len(glyphs)} types={n_sym} real={real:.3f} null={mu:.3f}±{sd:.3f} z={(real-mu)/sd:.1f}')
    print('   ',S.render(toks,syms,m)[:200])
run('A shape+marks',segA)
run('C tokens',segC)
run('D shape+dot',lambda w:S.segD(w))
run('S shapes only',segS)
