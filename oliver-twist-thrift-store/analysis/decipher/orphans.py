import sys; sys.path.insert(0,'.'); sys.path.insert(0,'..')
import cv2, numpy as np, pickle
import glyphlib, final_b2 as fb, strips, boot
def mask_new(th):
    th=th.copy(); th[180:790,805:1900]=0; th[790:900,1060:1900]=0; return th
out={}
for tag in ['b2L','b2R','b3L','b3R']:
    name,box,rot,mk=strips.CFG[tag]
    reg,flat,lab,units=fb.extract(name,box,rot,strips.mask_b2R if mk=='b2R' else None)
    w=np.median([u['w'] for u in units])
    ps=fb.pieces_from_units(tag,lab,units,0.8*w)
    for p in ps: p['cx']=p['x']+p['w']/2; p['cy']=p['y']+p['h']/2
    ps=[p for p in ps if p['h']>=45 and p['w']>=18 and (p['mask']>0).sum()>=250]
    inl={(p['x'],p['y'],p['w'],p['h']) for l in boot.lines_of(tag) for p in l}
    orph=[p for p in ps if (p['x'],p['y'],p['w'],p['h']) not in inl]
    print(tag,'w',w,'pieces',len(ps),'in lines',len(inl),'orphans',len(orph))
    out[tag]=dict(w=float(w),orph=[(p['x'],p['y'],p['w'],p['h']) for p in orph])
    for p in orph: print('   ',p['x'],p['y'],p['w'],p['h'])
pickle.dump(out,open('orph.pkl','wb'))
