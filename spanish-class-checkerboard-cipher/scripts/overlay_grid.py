"""Draw each red glyph's fitted 3-row lattice + decoded letters over the photo (verification aid).
Run: /opt/homebrew/bin/python3.11 -I scripts/overlay_grid.py <corpus_dir> <outdir>"""
import sys, os
import cv2, numpy as np
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import red_decode as rd
ROOT=rd.ROOT; OUT=sys.argv[2]; os.makedirs(OUT,exist_ok=True)
P=46.0
# re-run build but capture lattice params
import types
info_all={}
def build_with_params(P=46.0,endw=0.5):
    DIAG=P*np.sqrt(2); info={}
    for c,g in rd.G_.items():
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
            i0=int(round((s['x0']-ox)/P)); j0=int(round((s['y0']-oy)/P)); i1=int(round((s['x1']-ox)/P)); j1=int(round((s['y1']-oy)/P))
            k=max(abs(i1-i0),abs(j1-j0),1)
            for t in range(k): cells.setdefault((j0+t,i0+t),1)
        if not cells: continue
        r0=min(k[0] for k in cells); r1=max(k[0] for k in cells); c0=min(k[1] for k in cells); c1=max(k[1] for k in cells)
        x,y,w,h,a=rd.st[c]
        info[c]=dict(cells=cells,ox=ox,oy=oy,r0=r0,r1=r1,c0=c0,c1=c1,line=rd.line_of(y+h/2),cx=x+w/2)
    return info
info=build_with_params(P)
frames={}
for c,v in info.items():
    if v['r1']-v['r0']==2: frames.setdefault(v['line'],[]).append((v['cx'],v['oy']+v['r0']*P))
def frame_top(L,x):
    f=frames[L]; xs=np.array([a for a,_ in f]); ys=np.array([b for _,b in f]); w=1/(np.abs(xs-x)+150.0)**2
    return float((w*ys).sum()/w.sum())
vis=rd.im.copy()
for c,v in info.items():
    rowoff=v['r0'] if v['r1']-v['r0']==2 else int(round((frame_top(v['line'],v['cx'])-v['oy'])/P))
    x0=v['ox']+v['c0']*P; y0=v['oy']+rowoff*P; ncol=v['c1']-v['c0']+1
    word=''
    for ci in range(ncol):
        col=[v['cells'].get((rowoff+r,v['c0']+ci),0) for r in range(3)]
        val=col[0]+3*col[1]+9*col[2]; ch=' ' if val==0 else chr(96+val); word+=ch
        cx=int(x0+ci*P)
        cv2.rectangle(vis,(cx,int(y0)),(int(cx+P),int(y0+3*P)),(255,120,0),2)
        cv2.putText(vis,ch if ch!=' ' else '_',(cx+8,int(y0)-8),cv2.FONT_HERSHEY_SIMPLEX,1.1,(200,0,0),3)
    cv2.putText(vis,str(c),(int(x0),int(y0+3*P+30)),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,0),2)
for L,(ya,yb) in {1:(1290,1620),2:(1520,1840),3:(1740,2060),4:(1960,2340)}.items():
    for h,(xa,xb) in enumerate([(0,1100),(1000,2100),(2000,3060)]):
        cv2.imwrite(os.path.join(OUT,f'line{L}_{h}.png'),vis[ya:yb,xa:xb])
print('ok')
