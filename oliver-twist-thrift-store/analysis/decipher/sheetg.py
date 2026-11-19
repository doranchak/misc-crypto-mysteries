import sys, json, cv2, numpy as np, boot
def crop(page,li,pcsidx,pad=10,H=110,ctx=0):
    pcs=boot.lines_of(page)[li]; flat=boot.A[page]['flat']
    sel=[pcs[j] for j in pcsidx]
    x0=int(min(p['x'] for p in sel))-pad-ctx; x1=int(max(p['x']+p['w'] for p in sel))+pad+ctx
    cy=np.median([p['y']+p['h']/2 for p in pcs]); mh=np.median([p['h'] for p in pcs])
    y0=int(cy-1.0*mh); y1=int(cy+1.0*mh)
    x0=max(0,x0); y0=max(0,y0); x1=min(flat.shape[1],x1); y1=min(flat.shape[0],y1)
    c=flat[y0:y1,x0:x1]
    s=H/c.shape[0]
    c=cv2.resize(c,None,fx=s,fy=s,interpolation=cv2.INTER_CUBIC)
    c=cv2.cvtColor(c,cv2.COLOR_GRAY2BGR)
    # mark selected pieces
    for p in sel:
        a=int((p['x']-x0)*s); b=int((p['x']+p['w']-x0)*s); ya=int((p['y']-y0)*s); yb=int((p['y']+p['h']-y0)*s)
        cv2.rectangle(c,(a,max(0,ya)),(b,min(c.shape[0]-1,yb)),(0,0,255),1)
    return c
def sheet(entries,out,cols=6,H=110,ctx=0,label=True):
    tiles=[]
    for e in entries:
        page,li,idx,tag=e
        c=crop(page,li,idx,H=H,ctx=ctx)
        if label:
            lab=np.full((16,c.shape[1],3),255,np.uint8); cv2.putText(lab,f'{tag} {page}:{li}:{idx[0]}',(1,12),cv2.FONT_HERSHEY_SIMPLEX,.38,(200,0,0),1,cv2.LINE_AA)
            c=np.vstack([lab,c])
        tiles.append(c)
    rows=[]; 
    for r in range(0,len(tiles),cols):
        row=tiles[r:r+cols]; h=max(t.shape[0] for t in row)
        row=[np.vstack([t,np.full((h-t.shape[0],t.shape[1],3),255,np.uint8)]) if t.shape[0]<h else t for t in row]
        row=[np.hstack([t,np.full((h,6,3),180,np.uint8)]) for t in row]
        rows.append(np.hstack(row))
    W=max(r.shape[1] for r in rows)
    rows=[np.hstack([r,np.full((r.shape[0],W-r.shape[1],3),255,np.uint8)]) for r in rows]
    img=np.vstack(rows); cv2.imwrite(out,img); return img.shape
