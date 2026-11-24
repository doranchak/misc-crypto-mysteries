import json, cv2, numpy as np
from sklearn.cluster import KMeans
S=4
d=json.load(open('lines.json')); boxes=d['boxes']
im = cv2.imread('../original.png',0)
big = cv2.resize(im,None,fx=S,fy=S,interpolation=cv2.INTER_CUBIC)
blur=cv2.GaussianBlur(big,(0,0),2)
lab=np.load('cl_lab.npy'); items=json.load(open('cl_items.json'))
sel=[t for t,(j,k,i) in enumerate(items) if lab[t] in (2,11,13,19)]
feats=[];crops=[]
for t in sel:
    j,k,i=items[t]; x,y,w,h=boxes[i][:4]
    c=blur[y:y+h,x:x+w]
    r=cv2.resize(c,(48,24),interpolation=cv2.INTER_AREA)
    feats.append((255-r.astype(float)).flatten()/255)
    crops.append(cv2.resize(big[y:y+h,x:x+w],(144,72),interpolation=cv2.INTER_AREA))
X=np.array(feats)
km=KMeans(n_clusters=3,n_init=10,random_state=1).fit(X)
for c in range(3):
    idx=np.where(km.labels_==c)[0]
    print(c,len(idx))
    tiles=[crops[i] for i in idx[:40]]
    while len(tiles)%8: tiles.append(np.full((72,144),255,np.uint8))
    m=np.vstack([np.hstack(tiles[r:r+8]) for r in range(0,len(tiles),8)])
    cv2.imwrite(f'rsplit_{c}.png',m)
