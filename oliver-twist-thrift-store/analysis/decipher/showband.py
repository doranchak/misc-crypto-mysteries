import sys, cv2, numpy as np, boot
COL=[(0,0,255),(255,90,0),(0,150,0),(200,0,200)]
def band(page,y0,y1,x0,x1,out,scale=1.5):
    flat=boot.A[page]['flat']; c=cv2.cvtColor(flat[y0:y1,x0:x1],cv2.COLOR_GRAY2BGR)
    c=cv2.resize(c,None,fx=scale,fy=scale,interpolation=cv2.INTER_CUBIC)
    for li,l in enumerate(boot.lines_of(page)):
        for j,p in enumerate(l):
            if p['x']+p['w']<x0 or p['x']>x1 or p['y']+p['h']<y0 or p['y']>y1: continue
            col=COL[li%4]
            a=(int((p['x']-x0)*scale),int((p['y']-y0)*scale)); b=(int((p['x']+p['w']-x0)*scale),int((p['y']+p['h']-y0)*scale))
            cv2.rectangle(c,a,b,col,1); cv2.putText(c,f'{li}:{j}',(a[0],max(11,a[1]-3)),cv2.FONT_HERSHEY_SIMPLEX,.45,col,1,cv2.LINE_AA)
    cv2.imwrite(out,c)
if __name__=='__main__':
    page=sys.argv[1]; y0,y1,x0,x1=map(int,sys.argv[2:6]); band(page,y0,y1,x0,x1,sys.argv[6],float(sys.argv[7]) if len(sys.argv)>7 else 1.5)
