"""Extract red marks: squares (closed loops) and strokes (leftover diagonal pieces).
Writes figures/red_marks.json and figures/red_marks_overlay.jpg.
Run: /opt/homebrew/bin/python3.11 -I scripts/extract_marks.py"""
import cv2, numpy as np, json, os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
im=cv2.imread(os.path.join(ROOT,'pic1.jpeg'))
B,G,R=[im[:,:,i].astype(int) for i in range(3)]
red=((R-G>40)&(R-B>15)).astype(np.uint8); red[:1300]=0; red[2330:]=0
closed=cv2.morphologyEx(red,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(11,11)))
cn,hi=cv2.findContours(closed,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
sq=[]; ringmask=np.zeros_like(red)
for c,h in zip(cn,hi[0]):
    if h[3]!=-1 and 500<cv2.contourArea(c)<6000:
        M=cv2.moments(c); cx,cy=M['m10']/M['m00'],M['m01']/M['m00']
        x,y,w,hh=cv2.boundingRect(c)
        sq.append(dict(x=cx,y=cy,w=w,h=hh))
        m=np.zeros_like(red); cv2.drawContours(m,[c],-1,1,-1)
        ringmask|=cv2.dilate(m,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(33,33)))
left=(red&(1-ringmask)).astype(np.uint8)
left=cv2.morphologyEx(left,cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
n,lab,st,cen=cv2.connectedComponentsWithStats(left)
strokes=[]
for i in range(1,n):
    if st[i,4]<500: continue
    ys,xs=np.nonzero(lab==i); pts=np.stack([xs,ys],1).astype(float); mu=pts.mean(0)
    u,s,vt=np.linalg.svd(pts-mu,full_matrices=False); d=vt[0]
    if d[1]<0: d=-d
    ang=float(np.degrees(np.arctan2(d[1],d[0])))
    pr=(pts-mu)@d; L=float(pr.max()-pr.min())
    wd=float(((pts-mu)@vt[1]).max()-((pts-mu)@vt[1]).min())
    p0=mu+d*pr.min(); p1=mu+d*pr.max()
    strokes.append(dict(x0=float(p0[0]),y0=float(p0[1]),x1=float(p1[0]),y1=float(p1[1]),ang=ang,len=L,wid=wd,area=int(st[i,4])))
print('squares',len(sq),'strokes pieces',len(strokes))
json.dump(dict(squares=sq,strokes=strokes),open(os.path.join(ROOT,'figures','red_marks.json'),'w'))
vis=im.copy()
for s in sq: cv2.circle(vis,(int(s['x']),int(s['y'])),16,(0,160,0),-1)
for s in strokes:
    col=(255,0,0) if 25<s['ang']<75 else (0,128,255)
    cv2.line(vis,(int(s['x0']),int(s['y0'])),(int(s['x1']),int(s['y1'])),col,7)
cv2.imwrite(os.path.join(ROOT,'figures','red_marks_overlay.jpg'),cv2.resize(vis[1280:2330],None,fx=0.8,fy=0.8),[cv2.IMWRITE_JPEG_QUALITY,85])
