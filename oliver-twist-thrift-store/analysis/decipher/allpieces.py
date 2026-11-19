import sys; sys.path.insert(0,'..')
import cv2, numpy as np, pickle, collections
import glyphlib, final_b2 as fb, strips
res={}
for tag in ['b2L','b2R','b3L','b3R']:
    name,box,rot,mk=strips.CFG[tag]
    reg,flat,lab,units=fb.extract(name,box,rot,strips.mask_b2R if mk=='b2R' else None)
    w=np.median([u['w'] for u in units])
    ps=fb.pieces_from_units(tag,lab,units,0.8*w)
    for p in ps: p['cx']=p['x']+p['w']/2; p['cy']=p['y']+p['h']/2
    ps=[p for p in ps if p['h']>=45 and p['w']>=18 and (p['mask']>0).sum()>=250]
    lines=[l for l in strips.chain_lines(ps,tol=0.5,maxdx=300) if len(l)>=2]
    lines.sort(key=lambda l:np.mean([p['cy'] for p in l]))
    res[tag]=dict(flat=flat,lines=lines,medw=float(np.median([p['w'] for p in ps])),medh=float(np.median([p['h'] for p in ps])))
    print(tag,len(ps),[len(l) for l in lines])
    vis=cv2.cvtColor(flat,cv2.COLOR_GRAY2BGR)
    for i,l in enumerate(lines):
        for p in l: cv2.rectangle(vis,(p['x'],p['y']),(p['x']+p['w'],p['y']+p['h']),(0,0,255) if i%2==0 else (255,0,0),2)
        cv2.putText(vis,str(i+1),(int(l[0]['x'])-5,int(l[0]['y'])),cv2.FONT_HERSHEY_SIMPLEX,1.6,(0,160,0),4)
    cv2.imwrite(f'{tag}_pieces_ov.png',cv2.resize(vis,None,fx=0.5,fy=0.5))
pickle.dump(res,open('allpieces.pkl','wb'))
