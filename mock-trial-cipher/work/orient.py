import json, cv2, numpy as np
S=4
im = cv2.imread('original.png',0)
big = cv2.resize(im,None,fx=S,fy=S,interpolation=cv2.INTER_CUBIC)
blur = cv2.GaussianBlur(big,(0,0),3)
bw = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,61,12)
k=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(13,13))
op=cv2.morphologyEx(bw,cv2.MORPH_OPEN,k)
d=json.load(open('work/tracked.json')); bs=d['boxes']; lines=d['lines']
def orient(mask):
    ys,xs=np.nonzero(mask)
    if len(xs)<300: return None
    x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max()
    w=x1-x0+1;h=y1-y0+1
    m=mask[y0:y1+1,x0:x1+1]>0
    # row widths & col heights
    rw=m.sum(axis=1).astype(float); ch=m.sum(axis=0).astype(float)
    # trend: correlation with position
    ry=np.arange(h); cx=np.arange(w)
    ty=np.corrcoef(ry,rw)[0,1] if rw.std()>0 else 0   # >0: widens downward => apex up
    tx=np.corrcoef(cx,ch)[0,1] if ch.std()>0 else 0   # >0: taller to the right => apex left
    return ty,tx,w,h,int(m.sum())
res=[]
for j,ch in enumerate(lines):
    for k,i in enumerate(ch):
        x,y,w,h=bs[i]
        m=op[y:y+h,x:x+w]
        o=orient(m)
        if o is None: continue
        ty,tx,ww,hh,a=o
        if a<700: continue
        # label
        if abs(ty)>=abs(tx): lab='A' if ty>0 else 'T'
        else: lab='Q' if tx>0 else 'P'
        res.append((j,k,lab,round(ty,2),round(tx,2),a))
json.dump(res,open('work/orient.json','w'))
from collections import Counter
print(len(res),Counter(r[2] for r in res))
for j in range(26):
    print(j,' '.join(f'{r[1]}{r[2]}' for r in res if r[0]==j))
