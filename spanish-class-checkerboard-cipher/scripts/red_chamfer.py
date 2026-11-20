"""Chamfer-distance matching between connected red components (hand-drawn repeats).
Writes figures/red_clusters.json.   Run: /opt/homebrew/bin/python3.11 -I scripts/red_chamfer.py
Component numbering = cv2.connectedComponentsWithStats label order after a 25px dilation of the red mask
(same numbering as figures/red_line*.jpg).  Comp 31 is glare, excluded from clustering."""
import cv2, numpy as np, json, itertools, os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
im=cv2.imread(os.path.join(ROOT,'pic1.jpeg'))
B,G,R=[im[:,:,i].astype(int) for i in range(3)]
red=((R-G>45)&(R-B>20)).astype(np.uint8); red[:1300]=0; red[2330:]=0
d=cv2.dilate(red,cv2.getStructuringElement(cv2.MORPH_RECT,(25,25)))
n,lab,st,cen=cv2.connectedComponentsWithStats(d)
S=120
def prep(i):
    x,y,w,h,a=st[i]; m=((lab[y:y+h,x:x+w]==i)&(red[y:y+h,x:x+w]>0)).astype(np.uint8)
    m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,np.ones((7,7),np.uint8))
    s=S/max(w,h)
    m2=cv2.resize(m*255,(max(1,int(w*s)),max(1,int(h*s))),interpolation=cv2.INTER_AREA)>100
    c=np.zeros((S,S),np.uint8); c[:m2.shape[0],:m2.shape[1]]=m2
    return c,(int(w),int(h))
P={i:prep(i) for i in range(1,n)}
sk={i:(cv2.distanceTransform((1-c).astype(np.uint8),cv2.DIST_L2,3),np.argwhere(c>0)) for i,(c,_) in P.items()}
def cham(i,j):
    di,pi=sk[i]; dj,pj=sk[j]
    return float(max(dj[pi[:,0],pi[:,1]].mean(),di[pj[:,0],pj[:,1]].mean()))
ids=[i for i in range(1,n) if i!=31]
dist=[]
for i,j in itertools.combinations(ids,2):
    wi,hi=P[i][1]; wj,hj=P[j][1]; r=(wi/hi)/(wj/hj)
    if 0.75<r<1.33: dist.append((cham(i,j),i,j))
dist.sort()
out={'n_components':n-1,'distinct_after_excluding_glare':{}}
for thr in (1.5,2.0,2.3,2.7):
    par={i:i for i in ids}
    def f(x):
        while par[x]!=x: par[x]=par[par[x]]; x=par[x]
        return x
    for dd,i,j in dist:
        if dd<=thr: par[f(i)]=f(j)
    cl={}
    for i in ids: cl.setdefault(f(i),[]).append(i)
    out['distinct_after_excluding_glare'][str(thr)]={'types':len(cl),'repeated':sorted(v for v in cl.values() if len(v)>1)}
    print(thr,len(cl),sorted(v for v in cl.values() if len(v)>1))
json.dump(out,open(os.path.join(ROOT,'figures','red_clusters.json'),'w'),indent=1)
