import sys, cv2, numpy as np, boot
# numbered crop of piece range, bbox-based band (handles slanted lines), scale chosen so output width ~ target
def show(page,li,j0,j1,out,target=1700,pad=14):
    pcs=boot.lines_of(page)[li]; flat=boot.A[page]['flat']
    sel=pcs[j0:j1]
    x0=max(0,int(min(p['x'] for p in sel))-pad); x1=min(flat.shape[1],int(max(p['x']+p['w'] for p in sel))+pad)
    y0=max(0,int(min(p['y'] for p in sel))-26); y1=min(flat.shape[0],int(max(p['y']+p['h'] for p in sel))+10)
    c=cv2.cvtColor(flat[y0:y1,x0:x1],cv2.COLOR_GRAY2BGR)
    sc=min(2.2,target/c.shape[1])
    c=cv2.resize(c,None,fx=sc,fy=sc,interpolation=cv2.INTER_CUBIC)
    for j in range(j0,j1):
        p=pcs[j]; col=(0,0,255) if j%2==0 else (255,90,0)
        rx0=int((p['x']-x0)*sc); rx1=int((p['x']+p['w']-x0)*sc); ry0=int((p['y']-y0)*sc); ry1=int((p['y']+p['h']-y0)*sc)
        cv2.rectangle(c,(rx0,ry0),(rx1,ry1),col,1)
        cv2.putText(c,str(j),(rx0+2,max(12,ry0-4)),cv2.FONT_HERSHEY_SIMPLEX,.55,col,1,cv2.LINE_AA)
    cv2.imwrite(out,c); return c.shape
if __name__=='__main__':
    page=sys.argv[1]; li=int(sys.argv[2]); j0=int(sys.argv[3]); j1=int(sys.argv[4]); print(show(page,li,j0,j1,sys.argv[5]))
