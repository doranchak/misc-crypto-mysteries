"""Regenerates every figure and number used in index.html from pic1.jpeg.
Run:  /opt/homebrew/bin/python3.11 -I scripts/make_figures.py   (from the task folder)
"""
import cv2, numpy as np, json, itertools, os
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
FIG=os.path.join(ROOT,'figures'); os.makedirs(FIG,exist_ok=True)
im=cv2.imread(os.path.join(ROOT,'pic1.jpeg'))
g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
B,G,R=[im[:,:,i].astype(int) for i in range(3)]
black=((g<100)&~((R-G)>40)).astype(np.uint8)
red=((R-G>45)&(R-B>20)).astype(np.uint8); red[:1300]=0; red[2330:]=0

# ---- black glyph boxes (found by dilating the black mask 45px and taking connected components)
BOX={'t1':(87,401,437,807),'t2':(476,404,921,816),'t3':(880,398,1198,681),'t4':(1243,402,1667,791),
't5':(1742,426,2217,809),'t6':(2278,464,2832,779),'u1':(106,917,392,1302),'u2':(440,901,710,1255),
'b1':(258,2438,535,2811),'b2':(589,2414,928,2792),'b3':(983,2388,1347,2746),'b4':(1377,2394,1684,2722),
'b5':(1785,2379,2083,2709),'b6':(2169,2368,2482,2708),'b7':(371,2917,1419,3500)}
def tight(k):
    a,b,c,d=BOX[k]; sub=black[b+15:d-15,a+15:c-15]
    ys,xs=np.where(sub>0); return sub[ys.min():ys.max()+1,xs.min():xs.max()+1]
def sim(a,b,S=80):
    A=cv2.resize(a.astype(np.float32),(S,S),interpolation=cv2.INTER_AREA)>0.4
    Bm=cv2.resize(b.astype(np.float32),(S,S),interpolation=cv2.INTER_AREA)>0.4
    return float((A&Bm).sum()/(A|Bm).sum())
ks=[k for k in BOX if k!='b7']
pairs=sorted([(round(sim(tight(a),tight(b)),2),a,b) for a,b in itertools.combinations(ks,2)],reverse=True)
print('black glyph best matches',pairs[:6])

# contact sheet of black glyphs
tiles=[]
for k in BOX:
    a,b,c,d=BOX[k]; t=im[b-10:d+10,a-10:c+10].copy()
    s=300/max(t.shape[:2]); t=cv2.resize(t,None,fx=s,fy=s,interpolation=cv2.INTER_AREA)
    t=cv2.copyMakeBorder(t,26,6,6,6,cv2.BORDER_CONSTANT,value=(235,235,235))
    col=(0,0,200) if k in('t1','b1') else (200,120,0) if k in('b2','b6') else (60,60,60)
    cv2.putText(t,k,(8,20),cv2.FONT_HERSHEY_SIMPLEX,0.7,col,2); tiles.append(t)
H=max(t.shape[0] for t in tiles); W=max(t.shape[1] for t in tiles)
tiles=[cv2.copyMakeBorder(t,0,H-t.shape[0],0,W-t.shape[1],cv2.BORDER_CONSTANT,value=(235,235,235)) for t in tiles]
tiles+= [np.full_like(tiles[0],235)]
rows=[np.hstack(tiles[i:i+4]) for i in range(0,16,4)]
cv2.imwrite(os.path.join(FIG,'black_glyphs.jpg'),np.vstack(rows),[cv2.IMWRITE_JPEG_QUALITY,85])
# repeat pairs
def pair(k1,k2,name):
    ts=[]
    for k in (k1,k2):
        a,b,c,d=BOX[k]; t=im[b-10:d+10,a-10:c+10]; s=330/t.shape[0]; ts.append(cv2.resize(t,None,fx=s,fy=s,interpolation=cv2.INTER_AREA))
    Hh=max(t.shape[0] for t in ts); ts=[cv2.copyMakeBorder(t,0,Hh-t.shape[0],0,8,cv2.BORDER_CONSTANT,value=(235,235,235)) for t in ts]
    cv2.imwrite(os.path.join(FIG,name),np.hstack(ts),[cv2.IMWRITE_JPEG_QUALITY,88])
pair('t1','b1','pair_t1_b1.jpg'); pair('b2','b6','pair_b2_b6.jpg')

# ---- red components
d=cv2.dilate(red,cv2.getStructuringElement(cv2.MORPH_RECT,(25,25)))
n,lab,st,cen=cv2.connectedComponentsWithStats(d)
comps=[]
for i in range(1,n):
    x,y,w,h,a=st[i]; cy=y+h/2
    line=1 if cy<1560 else 2 if cy<1780 else 3 if cy<2000 else 4
    comps.append((line,x,i))
comps.sort(); order=[c[2] for c in comps]
print('red components',len(order))
# census of primitives
def holes_of(i):
    m=((lab==i)&(red>0)).astype(np.uint8); m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,np.ones((7,7),np.uint8))
    cn,hi=cv2.findContours(m,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
    return sum(1 for c,h in zip(cn,hi[0]) if h[3]!=-1 and cv2.contourArea(c)>500)
hol={i:holes_of(i) for i in order}
print('closed-square holes',sum(hol.values()))
# contact sheets per line
for line in (1,2,3,4):
    ids=[c[2] for c in comps if c[0]==line]; ts=[]
    for i in ids:
        x,y,w,h,a=st[i]; t=im[max(0,y-10):y+h+10,max(0,x-10):x+w+10].copy()
        cv2.putText(t,str(i),(3,22),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,0),2); ts.append(t)
    Hh=max(t.shape[0] for t in ts)
    row=[cv2.copyMakeBorder(t,0,Hh-t.shape[0],0,8,cv2.BORDER_CONSTANT,value=(120,120,120)) for t in ts]
    half=(len(row)+1)//2; a=np.hstack(row[:half]); b2=np.hstack(row[half:])
    Wd=max(a.shape[1],b2.shape[1])
    a=cv2.copyMakeBorder(a,0,0,0,Wd-a.shape[1],cv2.BORDER_CONSTANT,value=(120,120,120))
    b2=cv2.copyMakeBorder(b2,0,0,0,Wd-b2.shape[1],cv2.BORDER_CONSTANT,value=(120,120,120))
    cv2.imwrite(os.path.join(FIG,f'red_line{line}.jpg'),np.vstack([a,b2]),[cv2.IMWRITE_JPEG_QUALITY,85])
# red repeat similarity
feats={}
for i in order:
    x,y,w,h,a=st[i]; m=((lab[y:y+h,x:x+w]==i)&(red[y:y+h,x:x+w]>0)).astype(np.uint8)
    feats[i]=(cv2.dilate(m,np.ones((9,9),np.uint8)),w,h)
def rsim(i,j,S=96):
    mi,wi,hi=feats[i]; mj,wj,hj=feats[j]
    if abs(wi/hi-wj/hj)>0.35*(wi/hi): return 0
    a=cv2.resize(mi,(S,S),interpolation=cv2.INTER_AREA)>0; c=cv2.resize(mj,(S,S),interpolation=cv2.INTER_AREA)>0
    return float((a&c).sum()/max(1,(a|c).sum()))
simple={2,10,18,32,37,45,52,57,19,17,30,23,60,11,14,36,46}
cx=[(round(rsim(i,j),2),i,j) for i,j in itertools.combinations(order,2) if i not in simple and j not in simple and rsim(i,j)>0.6]
cx.sort(reverse=True); print('composite repeats',cx[:6])
ts=[]
for a_,b_ in ((4,56),(15,58),(16,38)):
    pr=[]
    for i in (a_,b_):
        x,y,w,h,a=st[i]; t=im[max(0,y-10):y+h+10,max(0,x-10):x+w+10]; s=220/t.shape[0]
        t=cv2.resize(t,None,fx=s,fy=s,interpolation=cv2.INTER_AREA); cv2.putText(t,str(i),(3,18),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,0,0),2); pr.append(t)
    ts.append(np.hstack([cv2.copyMakeBorder(t,0,0,0,10,cv2.BORDER_CONSTANT,value=(120,120,120)) for t in pr]))
Wd=max(t.shape[1] for t in ts)
ts=[cv2.copyMakeBorder(t,0,10,0,Wd-t.shape[1],cv2.BORDER_CONSTANT,value=(120,120,120)) for t in ts]
cv2.imwrite(os.path.join(FIG,'red_repeats.jpg'),np.vstack(ts),[cv2.IMWRITE_JPEG_QUALITY,88])

# hole overlay
rr=((R-G>40)&(R-B>15)).astype(np.uint8); rr[:1300]=0; rr[2330:]=0
m=cv2.morphologyEx(rr,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(11,11)))
cn,hi=cv2.findContours(m,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
vis=im.copy(); nh=0
for c,h in zip(cn,hi[0]):
    if h[3]!=-1 and 600<cv2.contourArea(c)<6000:
        M=cv2.moments(c); cv2.circle(vis,(int(M['m10']/M['m00']),int(M['m01']/M['m00'])),14,(0,160,0),-1); nh+=1
print('closed holes (second threshold)',nh)
v=vis[1280:2360]; cv2.imwrite(os.path.join(FIG,'red_squares_detected.jpg'),cv2.resize(v,None,fx=0.8,fy=0.8),[cv2.IMWRITE_JPEG_QUALITY,85])
# sheared red
crop=im[1280:2330]; h,w=crop.shape[:2]; k=1.19; off=k*h
out=cv2.warpAffine(crop,np.float32([[1,-k,off],[0,1,0]]),(int(w+off),h),borderValue=(200,200,200))
cv2.imwrite(os.path.join(FIG,'red_sheared.jpg'),cv2.resize(out,None,fx=0.7,fy=0.7),[cv2.IMWRITE_JPEG_QUALITY,85])
# annotated overview
ov=im.copy()
def lab_(txt,x,y,col=(200,0,0)): cv2.putText(ov,txt,(x,y),cv2.FONT_HERSHEY_SIMPLEX,2.2,col,5)
for k,(a,b,c,d_) in BOX.items():
    cv2.rectangle(ov,(a-10,b-10),(c+10,d_+10),(200,0,0),5); lab_(k,a,b-18)
for line,(y0,y1) in {1:(1340,1560),2:(1560,1790),3:(1790,2010),4:(2000,2300)}.items():
    cv2.rectangle(ov,(20,y0),(3040,y1),(0,140,0),4); lab_(f'red {line}',30,y0-8,(0,120,0))
cv2.rectangle(ov,(2680,3000),(3000,3500),(0,0,0),1)
cv2.imwrite(os.path.join(FIG,'overview_annotated.jpg'),cv2.resize(ov,None,fx=0.4,fy=0.4),[cv2.IMWRITE_JPEG_QUALITY,85])
json.dump({'red_components':len(order),'holes':sum(hol.values())},open(os.path.join(FIG,'numbers.json'),'w'))

# ---- black glyphs rotated 0 / -45 / +45 degrees (diagonal-lattice test)
blk=black*255; tl=[]
for k in [k for k in BOX if k!='b7']:
    sub=tight(k)*255; S=max(sub.shape)+40
    cv_=np.zeros((S,S),np.uint8); y0=(S-sub.shape[0])//2; x0=(S-sub.shape[1])//2; cv_[y0:y0+sub.shape[0],x0:x0+sub.shape[1]]=sub
    row=[]
    for ang in (0,-45,45):
        rot=cv2.warpAffine(cv_,cv2.getRotationMatrix2D((S/2,S/2),ang,1.0),(S,S)); row.append(cv2.resize(255-rot,(220,220)))
    t=np.hstack(row); cv2.putText(t,k,(3,18),cv2.FONT_HERSHEY_SIMPLEX,0.6,0,2); tl.append(t)
cv2.imwrite(os.path.join(FIG,'rot_sheet.png'),np.vstack([np.hstack(tl[i:i+2]) for i in range(0,14,2)]))
