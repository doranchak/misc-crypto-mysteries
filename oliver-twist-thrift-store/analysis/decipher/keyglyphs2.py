# whole-glyph tracing: ink inside an aligner glyph box (clipped to dilated pieces that touch the box)
import json, numpy as np, cv2
import boot, keyglyphs as kg
P=json.load(open('report_pages.json'))
def pieces_hit(page,li,x,y,w,h,need_center=False):
    out=[]
    for p in boot.lines_of(page)[li]:
        px0,py0,px1,py1=p['x'],p['y'],p['x']+p['w'],p['y']+p['h']
        ix=min(px1,x+w)-max(px0,x); iy=min(py1,y+h)-max(py0,y)
        if ix>0 and iy>0 and ix*iy>=0.25*p['w']*p['h']*0+1: out.append(p)
    return out
def trace_box(page,pcs,box=None,up=4,pad=14,dil=7,minarea=18,sig=0.9,thrf=0.92):
    flat=kg.FL[page]; H,W=flat.shape
    x0=min(p['x'] for p in pcs); y0=min(p['y'] for p in pcs); x1=max(p['x']+p['w'] for p in pcs); y1=max(p['y']+p['h'] for p in pcs)
    if box: x0=min(x0,box[0]); y0=min(y0,box[1]); x1=max(x1,box[0]+box[2]); y1=max(y1,box[1]+box[3])
    X0=max(0,int(x0)-pad); Y0=max(0,int(y0)-pad); X1=min(W,int(x1)+pad); Y1=min(H,int(y1)+pad)
    crop=flat[Y0:Y1,X0:X1]
    thr,_=cv2.threshold(crop,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    g=cv2.resize(crop,None,fx=up,fy=up,interpolation=cv2.INTER_CUBIC); g=cv2.GaussianBlur(g,(0,0),up*sig)
    bw=(g<thr*thrf).astype(np.uint8)*255
    m=np.zeros(crop.shape,np.uint8)
    for p in pcs:
        ys,xs=int(p['y'])-Y0,int(p['x'])-X0; mk=(p['mask']>0).astype(np.uint8)*255; hh,ww=mk.shape
        sy0,sx0=max(0,ys),max(0,xs); sy1,sx1=min(m.shape[0],ys+hh),min(m.shape[1],xs+ww)
        if sy1>sy0 and sx1>sx0: m[sy0:sy1,sx0:sx1]|=mk[sy0-ys:sy1-ys,sx0-xs:sx1-xs]
    m=cv2.dilate(m,np.ones((dil,dil),np.uint8)); mu=cv2.resize(m,(g.shape[1],g.shape[0]),interpolation=cv2.INTER_NEAREST)
    bw=cv2.bitwise_and(bw,mu)
    if box:   # clip to the glyph's own rectangle
        bx0=int((box[0]-X0)*up); by0=int((box[1]-Y0)*up); bx1=int((box[0]+box[2]-X0)*up); by1=int((box[1]+box[3]-Y0)*up)
        r=np.zeros_like(bw); r[max(0,by0):max(0,by1),max(0,bx0):max(0,bx1)]=255; bw=cv2.bitwise_and(bw,r)
    n,lab,st,_=cv2.connectedComponentsWithStats(bw,connectivity=8); keep=np.zeros_like(bw)
    tot=sum(st[i,4] for i in range(1,n)) or 1
    for i in range(1,n):
        if st[i,4]<minarea*up*up: continue
        if box:   # a small fragment cut by the box edge is a neighbour's stroke, not part of this glyph
            cx0,cy0,cw,ch=st[i,0],st[i,1],st[i,2],st[i,3]
            on_edge=(cx0<=bx0+up) or (cx0+cw>=bx1-up)
            if on_edge and st[i,4]<0.18*tot: continue
        keep[lab==i]=255
    return keep,up
def render_glyph(page,li,box,eps=0.5,clip=True):
    x,y,w,h=box
    pcs=pieces_hit(page,li,x,y,w,h)
    if not pcs: return None
    keep,up=trace_box(page,pcs,box=(x,y,w,h) if clip else None)
    r=kg.to_path(keep,up,eps=eps)
    if r: r['page']=page; r['keep']=keep
    return r
def bitmap(r,h=120):
    k=r['keep']; ys,xs=np.nonzero(k); k=k[ys.min():ys.max()+1,xs.min():xs.max()+1]
    s=h/k.shape[0]; k=cv2.resize(k,None,fx=s,fy=s,interpolation=cv2.INTER_AREA)
    return 255-k
