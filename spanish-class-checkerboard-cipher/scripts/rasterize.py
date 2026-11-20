"""Rasterize each red glyph (component) onto a p=47px lattice: 0 empty, 1 square, 2 diagonal stroke.
Writes figures/red_matrices.json.  Run: /opt/homebrew/bin/python3.11 -I scripts/rasterize.py"""
import cv2, numpy as np, json, os, itertools
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
im=cv2.imread(os.path.join(ROOT,'pic1.jpeg'))
B,G,R=[im[:,:,i].astype(int) for i in range(3)]
red45=((R-G>45)&(R-B>20)).astype(np.uint8); red45[:1300]=0; red45[2330:]=0
d=cv2.dilate(red45,cv2.getStructuringElement(cv2.MORPH_RECT,(25,25)))
n,lab,st,cen=cv2.connectedComponentsWithStats(d)
marks=json.load(open(os.path.join(ROOT,'figures','red_marks.json')))
P=47.0; DIAG=P*np.sqrt(2)
def comp_of(x,y):
    xi,yi=int(round(x)),int(round(y))
    l=lab[min(max(yi,0),lab.shape[0]-1),min(max(xi,0),lab.shape[1]-1)]
    if l: return int(l)
    # nearest
    r=40
    sub=lab[max(0,yi-r):yi+r,max(0,xi-r):xi+r]; v=sub[sub>0]
    return int(np.bincount(v).argmax()) if len(v) else 0
G={}
for s in marks['squares']:
    c=comp_of(s['x'],s['y']); G.setdefault(c,{'sq':[],'st':[],'other':[]})['sq'].append((s['x'],s['y']))
for s in marks['strokes']:
    c=comp_of((s['x0']+s['x1'])/2,(s['y0']+s['y1'])/2)
    t='st' if 25<s['ang']<75 and s['len']>35 else 'other'
    G.setdefault(c,{'sq':[],'st':[],'other':[]})[t].append(s)
out={}
for c,g in sorted(G.items()):
    if c==0: continue
    sq=np.array(g['sq']).reshape(-1,2)
    stk=g['st']
    # candidate lattice offsets
    best=None
    pts_sq=sq
    ends=[]
    for s in stk:
        ends.append((s['x0'],s['y0'])); ends.append((s['x1'],s['y1']))
    ends=np.array(ends).reshape(-1,2)
    for ox in np.arange(0,P,3):
        for oy in np.arange(0,P,3):
            cost=0
            if len(pts_sq):
                fx=((pts_sq[:,0]-ox)/P-0.5); fy=((pts_sq[:,1]-oy)/P-0.5)
                cost+=np.sum(np.abs(fx-np.round(fx))+np.abs(fy-np.round(fy)))
            if len(ends):
                fx=((ends[:,0]-ox)/P); fy=((ends[:,1]-oy)/P)
                cost+=0.5*np.sum(np.abs(fx-np.round(fx))+np.abs(fy-np.round(fy)))
            if best is None or cost<best[0]: best=(cost,ox,oy)
    _,ox,oy=best
    cells={}
    for x,y in pts_sq:
        cells[(int(np.floor((y-oy)/P)),int(np.floor((x-ox)/P)))]=1
    for s in stk:
        k=max(1,int(round((s['len']+10)/DIAG)))
        xs=np.linspace(s['x0'],s['x1'],2*k+1)[1::2]; ys=np.linspace(s['y0'],s['y1'],2*k+1)[1::2]
        for x,y in zip(xs,ys):
            key=(int(np.floor((y-oy)/P)),int(np.floor((x-ox)/P)))
            if key not in cells: cells[key]=2
    if not cells: continue
    r0=min(k[0] for k in cells); c0=min(k[1] for k in cells)
    r1=max(k[0] for k in cells); c1=max(k[1] for k in cells)
    M=[[cells.get((r,cc),0) for cc in range(c0,c1+1)] for r in range(r0,r1+1)]
    x,y,w,h,a=st[c]
    out[c]={'matrix':M,'n_sq':len(pts_sq),'n_st':len(stk),'bbox':[int(x),int(y),int(w),int(h)],'cost':float(best[0]),'other':len(g['other'])}
json.dump(out,open(os.path.join(ROOT,'figures','red_matrices.json'),'w'))
for c,v in sorted(out.items(),key=lambda kv:(kv[1]['bbox'][1]//220,kv[1]['bbox'][0])):
    M=v['matrix']
    print(c,f"{len(M)}x{len(M[0])}",'sq',v['n_sq'],'st',v['n_st'],'oth',v['other'])
    print('\n'.join('   '+''.join('.#\\'[x] for x in row) for row in M))
