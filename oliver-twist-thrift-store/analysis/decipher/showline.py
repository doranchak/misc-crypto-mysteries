import sys, cv2, numpy as np, boot
def show(page,li,j0=None,j1=None,out=None,scale=1.6,pad=18,numbers=True,band=None):
    pcs=boot.lines_of(page)[li]; flat=boot.A[page]['flat']
    j0=0 if j0 is None else j0; j1=len(pcs) if j1 is None else j1
    sel=pcs[j0:j1]
    x0=max(0,int(min(p['x'] for p in sel))-pad); x1=min(flat.shape[1],int(max(p['x']+p['w'] for p in sel))+pad)
    cy=np.median([p['y']+p['h']/2 for p in pcs]); mh=np.median([p['h'] for p in pcs])
    y0=max(0,int(cy-1.15*mh)-24); y1=min(flat.shape[0],int(cy+1.1*mh))
    c=cv2.cvtColor(flat[y0:y1,x0:x1],cv2.COLOR_GRAY2BGR)
    c=cv2.resize(c,None,fx=scale,fy=scale,interpolation=cv2.INTER_CUBIC)
    if numbers:
        for j in range(j0,j1):
            p=pcs[j]; cx=int((p['x']+p['w']/2-x0)*scale); ty=int((p['y']-y0)*scale)-4
            ty=max(12,min(ty,c.shape[0]-6))
            col=(0,0,255) if j%2==0 else (255,90,0)
            rx0=int((p['x']-x0)*scale); rx1=int((p['x']+p['w']-x0)*scale); ry0=int((p['y']-y0)*scale); ry1=int((p['y']+p['h']-y0)*scale)
            cv2.rectangle(c,(rx0,ry0),(rx1,ry1),col,1)
            cv2.putText(c,str(j),(cx-8,max(12,ry0-4)),cv2.FONT_HERSHEY_SIMPLEX,.55,col,1,cv2.LINE_AA)
    if out: cv2.imwrite(out,c)
    return c
if __name__=='__main__':
    page=sys.argv[1]; li=int(sys.argv[2]); j0=int(sys.argv[3]); j1=int(sys.argv[4]); out=sys.argv[5]
    show(page,li,j0,j1,out)
