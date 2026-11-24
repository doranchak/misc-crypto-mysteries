import json, cv2, numpy as np
S=4
im = cv2.imread('original.png',0)
big = cv2.resize(im,None,fx=S,fy=S,interpolation=cv2.INTER_CUBIC)
blur = cv2.GaussianBlur(big,(0,0),3)
bw = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,61,12)
k=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15))
op=cv2.morphologyEx(bw,cv2.MORPH_OPEN,k)
n,lab,stats,cent=cv2.connectedComponentsWithStats(op,connectivity=8)
d=json.load(open('work/tracked.json')); bs=d['boxes']; lines=d['lines']
def orient(mask):
    ys,xs=np.nonzero(mask)
    x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max()
    w=x1-x0+1;h=y1-y0+1
    m=mask[y0:y1+1,x0:x1+1]>0
    rw=m.sum(axis=1).astype(float); ch=m.sum(axis=0).astype(float)
    ty=np.corrcoef(np.arange(h),rw)[0,1] if rw.std()>0 else 0
    tx=np.corrcoef(np.arange(w),ch)[0,1] if ch.std()>0 else 0
    return ty,tx,w,h
out={}
for i in range(1,n):
    x,y,w,h,a=stats[i]
    if a<900 or a>14000 or w>200 or h>200: continue
    m=(lab[y:y+h,x:x+w]==i).astype(np.uint8)
    ty,tx,ww,hh=orient(m)
    if abs(ty)>=abs(tx): o='A' if ty>0 else 'T'
    else: o='Q' if tx>0 else 'P'
    cx=x+w/2; cy=y+h/2
    # find line/box
    found=None
    for j,ch in enumerate(lines):
        for kk,bi in enumerate(ch):
            bx,by,bw_,bh=bs[bi]
            if bx<=cx<=bx+bw_ and by<=cy<=by+bh:
                found=(j,kk); break
        if found: break
    out[i]=dict(x=int(x),y=int(y),w=int(w),h=int(h),a=int(a),o=o,ty=round(ty,2),tx=round(tx,2),line=found[0] if found else None,k=found[1] if found else None)
json.dump(out,open('work/fblobs.json','w'))
byline={}
for i,v in out.items():
    byline.setdefault(v['line'],[]).append(v)
for j in sorted(byline,key=lambda z:(z is None,z)):
    vs=sorted(byline[j],key=lambda v:v['x'])
    print(j,' '.join(f"{v['k']}{v['o']}" for v in vs))
# contact sheet of blobs in order
tiles=[]
for j in sorted(byline,key=lambda z:(z is None,z)):
    for v in sorted(byline[j],key=lambda v:v['x']):
        c=big[max(0,v['y']-12):v['y']+v['h']+12,max(0,v['x']-12):v['x']+v['w']+12]
        c=cv2.resize(c,(90,90),interpolation=cv2.INTER_AREA)
        t=cv2.cvtColor(c,cv2.COLOR_GRAY2BGR)
        cv2.putText(t,f"{j}.{v['k']}{v['o']}",(2,12),cv2.FONT_HERSHEY_SIMPLEX,0.45,(0,0,255),1)
        tiles.append(t)
cols=14
while len(tiles)%cols: tiles.append(np.full((90,90,3),255,np.uint8))
m=np.vstack([np.hstack(tiles[r:r+cols]) for r in range(0,len(tiles),cols)])
cv2.imwrite('work/fblobs.png',m); print(m.shape,len(out))
