import sys, os, random, itertools, json, subprocess, collections
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from lib import *
LINES=load_lines()
# drop unknown glyphs X ? - from the stream
DROP=set('X?-')
CHUNKS=[[ ''.join(ch for ch in c if ch not in DROP) for c in l] for l in LINES]
CHUNKS=[[c for c in l if c] for l in CHUNKS]
DIR={'R':(1,0),'r':(1,0),'P':(1,0),'p':(1,0),'L':(-1,0),'l':(-1,0),'Q':(-1,0),'q':(-1,0),
     'U':(0,-1),'A':(0,-1),'a':(0,-1),'D':(0,1),'d':(0,1),'T':(0,1),'t':(0,1),
     'S':(1,1),'W':(-1,1),'N':(1,-1),'b':(1,1),'j':(1,-1),'u':(0,1)}
STYLE={'R':'dbl','L':'dbl','r':'thin','l':'thin','U':'thin','D':'thin','d':'foot',
       'P':'fill','Q':'fill','A':'fill','T':'fill','p':'hol','q':'hol','a':'hol','t':'hol',
       'S':'thin','W':'thin','N':'thin','b':'thin','j':'thin','u':'foot'}
def glyph_move(ch,mult,hsem,vsem,esem):
    """returns ('t',dx,dy) translation or ('fx',),('fy',) flips"""
    if ch=='H':  return hsem
    if ch=='V':  return vsem
    if ch=='E':  return esem
    dx,dy=DIR[ch]; m=mult[STYLE[ch]]
    return ('t',dx*m,dy*m)
def simulate(chunks,grid,wrap,mult,hsem,vsem,esem,home,reset='word'):
    a,b=grid   # a columns (x), b rows (y)
    cells=[];ws=[]
    x,y=home
    first=True
    for li,l in enumerate(chunks):
        for ci,c in enumerate(l):
            for j,ch in enumerate(c):
                if (reset=='word' and j==0) or (reset=='line' and ci==0 and j==0) or first:
                    x,y=home; first=False
                mv=glyph_move(ch,mult,hsem,vsem,esem)
                if mv[0]=='t':
                    nx,ny=x+mv[1],y+mv[2]
                    if wrap=='torus': nx%=a; ny%=b
                    else: nx=min(max(nx,0),a-1); ny=min(max(ny,0),b-1)
                    x,y=nx,ny
                elif mv[0]=='fx': x=a-1-x
                elif mv[0]=='fy': y=b-1-y
                cells.append(y*a+x); ws.append(1 if j==0 else 0)
    return cells,ws
def solve_tokens(cells,ws,K,tag,restarts=4,iters=200000,seed=1,lm='lm4.bin'):
    d=HERE+'/tmp'; os.makedirs(d,exist_ok=True)
    # compress token ids
    ids={c:i for i,c in enumerate(sorted(set(cells)))}
    toks=[ids[c] for c in cells]
    if len(ids)>26: return None
    p=f'{d}/{tag}.txt'
    write_data(p,toks,[0]*len(toks),ws,len(ids))
    sp=f'{d}/ident.txt'
    if not os.path.exists(sp): write_steps(sp,26,26,0,[[0]*26 for _ in range(26)])
    r=run(p,sp,0,restarts,iters,seed)
    os.remove(p)
    r['ncells']=len(ids)
    return r
def shuffled_stream(cells_or_glyphs,rng):
    x=list(cells_or_glyphs); rng.shuffle(x); return x
