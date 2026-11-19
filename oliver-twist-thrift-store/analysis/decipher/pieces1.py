import sys; sys.path.insert(0,'..')
import cv2, numpy as np, pickle, collections
import glyphlib, final_b2 as fb
from glyphlib import glyph_mask
# page-1 pieces
reg,flat,lab,units=fb.extract('book1.jpeg',(330,1250,2800,3900),-0.75,None)
w=np.median([u['w'] for u in units])
ps=fb.pieces_from_units('b1',lab,units,0.8*w)
for p in ps: p['cx']=p['x']+p['w']/2; p['cy']=p['y']+p['h']/2
ps=[p for p in ps if p['h']>=50 and p['w']>=20 and p['cy']<2420 and (p['mask']>0).sum()>=300]
print(len(ps))
# tracks (region coords): centers at x=1200 and slopes from earlier per-line fits (approx); assign by nearest to fitted line from chain clusters
tracks=[(126,0.0084),(308,-0.0174),(509,0.0101),(690,0.0),(856,-0.0137),(1072,0.0023),(1269,0.0077),(1458,0.0058),(1616,0.0),(1781,-0.0251),(1997,-0.0308),(2195,-0.0121),(2350,0.0041)]
def ty(i,x): c,s=tracks[i]; return c+s*(x-1200)
lines=[[] for _ in tracks]
for p in ps:
    d=[abs(p['cy']-ty(i,p['cx'])) for i in range(len(tracks))]
    i=int(np.argmin(d))
    if d[i]<75: lines[i].append(p)
for l in lines: l.sort(key=lambda p:p['x'])
print([len(l) for l in lines])
pickle.dump(dict(lines=[[{k:v for k,v in p.items()} for p in l] for l in lines],flat=flat,lab=lab),open('b1_pieces.pkl','wb'))
vis=cv2.cvtColor(flat,cv2.COLOR_GRAY2BGR)
cols=[(0,0,255),(255,0,0)]
for i,l in enumerate(lines):
    for p in l: cv2.rectangle(vis,(p['x'],p['y']),(p['x']+p['w'],p['y']+p['h']),cols[i%2],2)
cv2.imwrite('b1_pieces_ov.png',cv2.resize(vis,None,fx=0.4,fy=0.4))
