import sys, json, pickle, collections
import numpy as np, cv2
import boot, decode as dc
FL={'b1':pickle.load(open('b1_pieces.pkl','rb'))['flat']}
for t in ['b2L','b2R','b3L','b3R']: FL[t]=boot.A[t]['flat']
MEDH={'b1':112.0,'b2L':72.0,'b2R':72.0,'b3L':80.0,'b3R':80.0}
def trace(page,pcs,up=4,pad=14,dil=7,minarea=30,sig=0.5,thrf=1.0):
    flat=FL[page]; H,W=flat.shape
    x0=min(p['x'] for p in pcs); y0=min(p['y'] for p in pcs); x1=max(p['x']+p['w'] for p in pcs); y1=max(p['y']+p['h'] for p in pcs)
    X0=max(0,int(x0)-pad); Y0=max(0,int(y0)-pad); X1=min(W,int(x1)+pad); Y1=min(H,int(y1)+pad)
    crop=flat[Y0:Y1,X0:X1]
    thr,_=cv2.threshold(crop,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    g=cv2.resize(crop,None,fx=up,fy=up,interpolation=cv2.INTER_CUBIC)
    g=cv2.GaussianBlur(g,(0,0),up*sig)
    bw=(g<thr*thrf).astype(np.uint8)*255
    m=np.zeros(crop.shape,np.uint8)
    for p in pcs:
        ys,xs=int(p['y'])-Y0,int(p['x'])-X0; mk=(p['mask']>0).astype(np.uint8)*255
        hh,ww=mk.shape; m[max(0,ys):ys+hh,max(0,xs):xs+ww]|=mk[max(0,-ys):max(0,-ys)+(m.shape[0]-max(0,ys)),max(0,-xs):max(0,-xs)+(m.shape[1]-max(0,xs))][:m.shape[0]-max(0,ys),:m.shape[1]-max(0,xs)]
    m=cv2.dilate(m,np.ones((dil,dil),np.uint8)); mu=cv2.resize(m,(g.shape[1],g.shape[0]),interpolation=cv2.INTER_NEAREST)
    bw=cv2.bitwise_and(bw,mu)
    n,lab,st,_=cv2.connectedComponentsWithStats(bw,connectivity=8)
    keep=np.zeros_like(bw)
    for i in range(1,n):
        if st[i,4]>=minarea*up*up: keep[lab==i]=255
    return keep,up
def to_path(keep,up,eps=0.35):
    ys,xs=np.nonzero(keep)
    if len(ys)==0: return None
    bx0,by0,bx1,by1=xs.min(),ys.min(),xs.max()+1,ys.max()+1
    k=keep[by0:by1,bx0:bx1]
    k=cv2.copyMakeBorder(k,2,2,2,2,cv2.BORDER_CONSTANT,value=0)
    cs,_=cv2.findContours(k,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE)
    d=[]
    for c in cs:
        if len(c)<8: continue
        a=cv2.approxPolyDP(c,up*eps,True)
        if len(a)<3: continue
        pts=[((q[0][0]-2)/up,(q[0][1]-2)/up) for q in a]
        d.append('M'+' '.join(f'{x:.1f} {y:.1f}' for x,y in pts)+'Z')
    return dict(d=''.join(d),w=(bx1-bx0)/up,h=(by1-by0)/up)
