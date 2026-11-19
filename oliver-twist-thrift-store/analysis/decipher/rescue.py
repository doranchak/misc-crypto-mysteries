import sys; sys.path.insert(0,'.'); sys.path.insert(0,'..')
import cv2, numpy as np, pickle
import glyphlib, final_b2 as fb, strips, boot
def mask_new(th):
    th=th.copy(); th[180:790,805:1900]=0; th[790:900,1060:1900]=0; return th
tag='b2R'
name,box,rot,mk=strips.CFG[tag]
reg,flat,lab,units=fb.extract(name,box,rot,mask_new)
w_old=67.0
ps=fb.pieces_from_units(tag,lab,units,0.8*w_old)
for p in ps: p['cx']=p['x']+p['w']/2; p['cy']=p['y']+p['h']/2
ps=[p for p in ps if p['h']>=45 and p['w']>=18 and (p['mask']>0).sum()>=250]
inl={(p['x'],p['y'],p['w'],p['h']) for l in boot.lines_of(tag) for p in l}
new=[p for p in ps if (p['x'],p['y'],p['w'],p['h']) not in inl]
print(len(ps),len(new))
for p in new:
    if 640<p['x']<1100 and 150<p['y']<900: print(p['x'],p['y'],p['w'],p['h'])
pickle.dump([{k:v for k,v in p.items()} for p in new],open('rescue_b2R_new.pkl','wb'))
