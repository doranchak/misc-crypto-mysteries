"""Black glyphs read as the same ternary column code at 2x scale.
Big cell = 2x2 small cells: solid block = square (2); top-left + bottom-right only = stroke (1); empty = 0.
Glyph = 3 big rows x n big columns; letter = top + 3*mid + 9*bottom (a=1..z=26, 0 = space).  Soft (occupancy-based) classification.
Run: /opt/homebrew/bin/python3.11 -I scripts/black_ternary.py"""
import cv2, numpy as np, json, os, sys
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
im=cv2.imread(os.path.join(ROOT,'pic1.jpeg')); g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
B,G,R=[im[:,:,i].astype(int) for i in range(3)]
black=((g<100)&~((R-G)>40)).astype(np.uint8)
BOX={'t1':(87,401,437,807),'t2':(476,404,921,816),'t3':(880,398,1198,681),'t4':(1243,402,1667,791),'t5':(1742,426,2217,809),'t6':(2278,464,2832,779),
'u1':(106,917,392,1302),'u2':(440,901,710,1255),'b1':(258,2438,535,2811),'b2':(589,2414,928,2792),'b3':(983,2388,1347,2746),'b4':(1377,2394,1684,2722),
'b5':(1785,2379,2083,2709),'b6':(2169,2368,2482,2708),'b7':(371,2917,1419,3500)}
PITCH={'b7':range(84,106)}
def tight(k):
    a,b,c,d=BOX[k]; sub=black[b+15:d-15,a+15:c-15]; ys,xs=np.where(sub>0); return sub[ys.min():ys.max()+1,xs.min():xs.max()+1]
def occ(sub,p,ox,oy,nr,nc):
    out=np.zeros((nr,nc))
    for j in range(nr):
        for i in range(nc):
            x0=int(round(ox+i*p)); y0=int(round(oy+j*p)); a=sub[max(0,y0):max(0,y0+int(p)),max(0,x0):max(0,x0+int(p))]
            out[j,i]=a.mean() if a.size>0 else 0
    return out
def small_occ(k):
    sub=tight(k); H,W=sub.shape; best=None
    for p in PITCH.get(k,range(54,67)):
        nr=int(round(H/p)); nc=int(round(W/p))
        if nr>6: continue
        for ox in range(-int(p*0.45),int(p*0.2),4):
            for oy in range(-int(p*0.45),int(p*0.2),4):
                o=occ(sub,p,ox,oy,nr+1,nc+1); sc=np.mean(np.abs(o-0.5))
                if best is None or sc>best[0]: best=(sc,p,ox,oy,o)
    sc,p,ox,oy,o=best
    o=np.clip((o-0.15)/0.7,0,1)       # soften: ink fractions -> 0..1 occupancy
    rows=np.where(o.max(1)>0.5)[0]; cols=np.where(o.max(0)>0.5)[0]
    return o[rows.min():rows.max()+1,cols.min():cols.max()+1],p
PROTO={0:np.array([0,0,0,0]),2:np.array([1,1,1,1]),1:np.array([1,0,0,1])}   # tl,tr,bl,br
def bigcells(o,shift_r,cpar):
    H,W=o.shape; Hp=6; Wp=W+cpar+2
    pad=np.zeros((Hp+2,Wp+2)); 
    if shift_r+H>6: return None
    pad[shift_r:shift_r+H,cpar:cpar+W]=o
    nc=(Wp+1)//2; cols=[]; cost=0.0
    for bc in range(nc):
        col=[]
        for br in range(3):
            blk=pad[2*br:2*br+2,2*bc:2*bc+2]
            v=np.array([blk[0,0],blk[0,1],blk[1,0],blk[1,1]]) if blk.shape==(2,2) else np.zeros(4)
            cs={s:np.abs(v-pr).sum() for s,pr in PROTO.items()}
            s=min(cs,key=cs.get); cost+=cs[s]; col.append((s,cs[s]))
        cols.append(col)
    while cols and all(c[0]==0 and c[1]<0.6 for c in cols[-1]): cols.pop()
    while cols and all(c[0]==0 and c[1]<0.6 for c in cols[0]): cols.pop(0)
    return cols,cost
def letter(col):
    v=col[0]+3*col[1]+9*col[2]
    return ' ' if v==0 else chr(96+v) if v<=26 else '?'
if __name__=='__main__':
    out={}
    for k in BOX:
        o,p=small_occ(k); best=None
        for sr in range(0,5):
            for cp in (0,1):
                r=bigcells(o,sr,cp)
                if r is None: continue
                cols,cost=r
                cand=(cost,sr,cp,cols)
                if best is None or cand[0]<best[0]: best=cand
        cost,sr,cp,cols=best
        txt=''.join(letter([c[0] for c in col]) for col in cols)
        unc=[round(max(c[1] for c in col),1) for col in cols]
        out[k]=dict(pitch=p,small_shape=list(o.shape),cost=round(cost,2),text=txt,col_uncertainty=unc,cells=[[c[0] for c in col] for col in cols])
        print(f'{k:3s} pitch {p:3d} small {o.shape[::-1]} cost {cost:5.2f}  text {txt!r:12}  per-column worst-block cost {unc}')
    json.dump(out,open(os.path.join(ROOT,'figures','black_ternary.json'),'w'))
