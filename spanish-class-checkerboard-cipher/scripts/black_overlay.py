"""Overlay the fitted big-cell grid + decoded letters on every black glyph (verification aid)."""
import sys, os, numpy as np, cv2
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import black_ternary as bt
OUT=sys.argv[1]; os.makedirs(OUT,exist_ok=True)
tiles=[]
for k in bt.BOX:
    sub=bt.tight(k); H,W=sub.shape
    # recompute the same fit but keep geometry
    best=None
    for p in bt.PITCH.get(k,range(54,67)):
        nr=int(round(H/p)); nc=int(round(W/p))
        if nr>6: continue
        for ox in range(-int(p*0.45),int(p*0.2),4):
            for oy in range(-int(p*0.45),int(p*0.2),4):
                o=bt.occ(sub,p,ox,oy,nr+1,nc+1); sc=np.mean(np.abs(o-0.5))
                if best is None or sc>best[0]: best=(sc,p,ox,oy,o)
    sc,p,ox,oy,o0=best
    o=np.clip((o0-0.15)/0.7,0,1)
    rows=np.where(o.max(1)>0.5)[0]; cols=np.where(o.max(0)>0.5)[0]
    r0,c0=rows.min(),cols.min(); oc=o[r0:rows.max()+1,c0:cols.max()+1]
    b=None
    for sr in range(0,5):
        for cp in (0,1):
            r=bt.bigcells(oc,sr,cp)
            if r is None: continue
            if b is None or r[1]<b[0]: b=(r[1],sr,cp,r[0])
    cost,sr,cp,cols_=b
    img=cv2.cvtColor((255-sub*255).astype(np.uint8),cv2.COLOR_GRAY2BGR)
    S=1.0
    # small-cell grid origin in pixels:
    gx=ox+c0*p-cp*p; gy=oy+r0*p-sr*p
    first=0  # leading blank columns were trimmed in cols_, recompute offset: find first non-empty col in untrimmed grid
    # draw small grid faint, big grid strong
    nbig=int((W-gx)/(2*p))+2
    for j in range(7):
        y=int(gy+j*p); cv2.line(img,(0,y),(W,y),(255,200,150) if j%2 else (255,120,0),1 if j%2 else 2)
    for i in range(int((W-gx)/p)+2):
        x=int(gx+i*p); cv2.line(img,(x,0),(x,H),(255,200,150) if i%2 else (255,120,0),1 if i%2 else 2)
    txt=''.join(bt.letter([c[0] for c in col]) for col in cols_)
    img=cv2.copyMakeBorder(img,34,6,6,6,cv2.BORDER_CONSTANT,value=(235,235,235))
    cv2.putText(img,f'{k}: {txt!r}',(8,24),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,180),2)
    s=min(1.0,380/max(img.shape[:2])); img=cv2.resize(img,None,fx=s,fy=s,interpolation=cv2.INTER_AREA)
    tiles.append(img)
H=max(t.shape[0] for t in tiles); Wd=max(t.shape[1] for t in tiles)
tiles=[cv2.copyMakeBorder(t,0,H-t.shape[0],0,Wd-t.shape[1],cv2.BORDER_CONSTANT,value=(235,235,235)) for t in tiles]
while len(tiles)%4: tiles.append(np.full_like(tiles[0],235))
sheet=np.vstack([np.hstack(tiles[i:i+4]) for i in range(0,len(tiles),4)])
cv2.imwrite(os.path.join(OUT,'black_grid.png'),sheet); print(sheet.shape)
