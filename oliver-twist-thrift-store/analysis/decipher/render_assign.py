import sys, json, cv2, numpy as np, boot
def render(page,li,items,out=None,scale=0.75,title=''):
    pcs=boot.lines_of(page)[li]; flat=boot.A[page]['flat']
    xs0=min(p['x'] for p in pcs); xs1=max(p['x']+p['w'] for p in pcs)
    cy=np.median([p['y']+p['h']/2 for p in pcs]); mh=np.median([p['h'] for p in pcs])
    x0=max(0,int(xs0)-10); x1=min(flat.shape[1],int(xs1)+10)
    y0=max(0,int(min(p["y"] for p in pcs))-8); y1=min(flat.shape[0],int(max(p["y"]+p["h"] for p in pcs))+8)
    c=cv2.cvtColor(flat[y0:y1,x0:x1],cv2.COLOR_GRAY2BGR)
    c=cv2.resize(c,None,fx=scale,fy=scale,interpolation=cv2.INTER_AREA)
    pad=34; canvas=np.full((c.shape[0]+pad+16,c.shape[1],3),255,np.uint8); canvas[16:16+c.shape[0]]=c
    cv2.putText(canvas,title,(2,11),cv2.FONT_HERSHEY_SIMPLEX,.42,(150,0,0),1,cv2.LINE_AA)
    used=set()
    for n,(it,t,k0) in enumerate(items):
        xa=min(pcs[j]['x'] for j in it); xb=max(pcs[j]['x']+pcs[j]['w'] for j in it)
        ya=min(pcs[j]['y'] for j in it); yb=max(pcs[j]['y']+pcs[j]['h'] for j in it)
        col=(0,0,255) if n%2==0 else (255,60,0)
        cv2.rectangle(canvas,(int((xa-x0)*scale),16+int((ya-y0)*scale)),(int((xb-x0)*scale),16+int((yb-y0)*scale)),col,1)
        cx=int(((xa+xb)/2-x0)*scale)
        cv2.putText(canvas,t,(cx-6*len(t),16+c.shape[0]+22),cv2.FONT_HERSHEY_SIMPLEX,.62,col,2,cv2.LINE_AA)
        cv2.putText(canvas,str(min(it)),(cx-8,16+c.shape[0]+9),cv2.FONT_HERSHEY_SIMPLEX,.32,(90,90,90),1,cv2.LINE_AA)
        used|=set(it)
    if out: cv2.imwrite(out,canvas)
    return canvas
def stack(imgs,out):
    W=max(i.shape[1] for i in imgs)
    imgs=[np.hstack([i,np.full((i.shape[0],W-i.shape[1],3),255,np.uint8)]) for i in imgs]
    cv2.imwrite(out,np.vstack(imgs))
