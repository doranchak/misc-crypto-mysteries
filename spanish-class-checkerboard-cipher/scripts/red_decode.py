"""Ternary (3-row) reading of the red glyphs with the mapping found by scripts/decode_base3.py:
   cell: empty=0, stroke=1, square=2;  column value = top + 3*middle + 9*bottom;  1..26 = a..z, 0 = space.
Variants of the stroke->cell rasterization are compared by number of common English words recovered.
Run: /opt/homebrew/bin/python3.11 -I scripts/red_decode.py <corpus_dir>"""
import cv2, numpy as np, json, os, sys, collections, re, unicodedata
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORP=sys.argv[1]
im=cv2.imread(os.path.join(ROOT,'pic1.jpeg'))
B,G,R=[im[:,:,i].astype(int) for i in range(3)]
red45=((R-G>45)&(R-B>20)).astype(np.uint8); red45[:1300]=0; red45[2330:]=0
DIL=int(os.environ.get('DIL','25'))
d=cv2.dilate(red45,cv2.getStructuringElement(cv2.MORPH_RECT,(DIL,DIL)))
n,lab,st,cen=cv2.connectedComponentsWithStats(d)
marks=json.load(open(os.path.join(ROOT,'figures',os.environ.get('MARKS','red_marks.json'))))
def norm(t):
    t=unicodedata.normalize('NFD',t.lower()); t=''.join(c for c in t if unicodedata.category(c)!='Mn'); return re.sub('[^a-z ]',' ',t)
en=collections.Counter(norm(open(os.path.join(CORP,'en.txt')).read()).split())
COMMON={w for w,_ in en.most_common(3000)}|{'a','i'}
def line_of(y): return 1 if y<1560 else 2 if y<1780 else 3 if y<2000 else 4
def comp_of(x,y):
    xi,yi=int(round(x)),int(round(y)); l=lab[min(max(yi,0),lab.shape[0]-1),min(max(xi,0),lab.shape[1]-1)]
    if l: return int(l)
    r=40; sub=lab[max(0,yi-r):yi+r,max(0,xi-r):xi+r]; v=sub[sub>0]; return int(np.bincount(v).argmax()) if len(v) else 0
G_={}
for s in marks['squares']: G_.setdefault(comp_of(s['x'],s['y']),{'sq':[],'st':[]})['sq'].append((s['x'],s['y']))
for s in marks['strokes']:
    if 25<s['ang']<75 and s['len']>35: G_.setdefault(comp_of((s['x0']+s['x1'])/2,(s['y0']+s['y1'])/2),{'sq':[],'st':[]})['st'].append(s)
def build(P=47.0,mode='snap',endw=0.5):
    DIAG=P*np.sqrt(2); info={}
    for c,g in G_.items():
        if c==0: continue
        sq=np.array(g['sq']).reshape(-1,2)
        ends=np.array([[s['x0'],s['y0']] for s in g['st']]+[[s['x1'],s['y1']] for s in g['st']]).reshape(-1,2)
        best=None
        for ox in np.arange(0,P,3):
            for oy in np.arange(0,P,3):
                cost=0
                if len(sq):
                    fx=(sq[:,0]-ox)/P-0.5; fy=(sq[:,1]-oy)/P-0.5; cost+=np.sum(abs(fx-np.round(fx))+abs(fy-np.round(fy)))
                if len(ends):
                    fx=(ends[:,0]-ox)/P; fy=(ends[:,1]-oy)/P; cost+=endw*np.sum(abs(fx-np.round(fx))+abs(fy-np.round(fy)))
                if best is None or cost<best[0]: best=(cost,ox,oy)
        _,ox,oy=best; cells={}
        for x,y in sq: cells[(int(np.floor((y-oy)/P)),int(np.floor((x-ox)/P)))]=2
        for s in g['st']:
            if mode=='snap':
                i0=int(round((s['x0']-ox)/P)); j0=int(round((s['y0']-oy)/P)); i1=int(round((s['x1']-ox)/P)); j1=int(round((s['y1']-oy)/P))
                k=max(abs(i1-i0),abs(j1-j0),1)
                for t in range(k): cells.setdefault((j0+t,i0+t),1)
            else:
                k=max(1,int(round((s['len']+10)/DIAG)))
                xs=np.linspace(s['x0'],s['x1'],2*k+1)[1::2]; ys=np.linspace(s['y0'],s['y1'],2*k+1)[1::2]
                for x,y in zip(xs,ys): cells.setdefault((int(np.floor((y-oy)/P)),int(np.floor((x-ox)/P))),1)
        if not cells: continue
        r0=min(k[0] for k in cells); r1=max(k[0] for k in cells); c0=min(k[1] for k in cells); c1=max(k[1] for k in cells)
        x,y,w,h,a=st[c]
        info[c]=dict(cells=cells,oy=oy,r0=r0,r1=r1,c0=c0,c1=c1,line=line_of(y+h/2),cx=x+w/2)
    frames={}
    for c,v in info.items():
        if v['r1']-v['r0']==2: frames.setdefault(v['line'],[]).append((v['cx'],v['oy']+v['r0']*P))
    def frame_top(L,x):
        f=frames[L]; xs=np.array([a for a,_ in f]); ys=np.array([b for _,b in f]); w=1/(np.abs(xs-x)+150.0)**2
        return float((w*ys).sum()/w.sum())
    out=[]
    for c,v in sorted(info.items(),key=lambda kv:(kv[1]['line'],kv[1]['cx'])):
        if v['r1']-v['r0']==2: rowoff=v['r0']
        else: rowoff=int(round((frame_top(v['line'],v['cx'])-v['oy'])/P))
        cols=[[v['cells'].get((rowoff+r,cc),0) for r in range(3)] for cc in range(v['c0'],v['c1']+1)]
        out.append((v['line'],c,cols))
    return out
def text_of(cols):
    s=''
    for top,mid,bot in cols:
        v=top+3*mid+9*bot; s+=' ' if v==0 else chr(96+v)
    return s
if __name__=='__main__':
    for P in (44.0,46.0,47.0,48.0,50.0):
        for mode in ('snap','len'):
            for endw in (0.25,0.5,1.0):
                rows=build(P,mode,endw)
                toks=[t for _,_,cols in rows for t in text_of(cols).split()]
                hits=sum(1 for t in toks if len(t)>=3 and t in COMMON)+sum(1 for t in toks if t in ('a','i'))
                print(f'P={P} mode={mode} endw={endw}: tokens {len(toks)}, recognised common words {hits}')
