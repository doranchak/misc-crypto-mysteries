import json, cv2, numpy as np
from sklearn.cluster import KMeans
S=4
d=json.load(open('work/lines.json'))
boxes=d['boxes']; lines=d['lines']
im = cv2.imread('original.png',0)
big = cv2.resize(im,None,fx=S,fy=S,interpolation=cv2.INTER_CUBIC)
blur=cv2.GaussianBlur(big,(0,0),2)
items=[]
for j,l in enumerate(lines):
    for k,i in enumerate(l):
        x,y,w,h=boxes[i][:4]
        if w>130 or w<45 or h<45 or h>150: continue
        items.append((j,k,i))
feats=[];crops=[]
for j,k,i in items:
    x,y,w,h=boxes[i][:4]
    c=blur[y:y+h,x:x+w]
    # pad to square preserving aspect
    m=max(w,h)
    sq=np.full((m,m),255,np.uint8)
    sq[(m-h)//2:(m-h)//2+h,(m-w)//2:(m-w)//2+w]=c
    r=cv2.resize(sq,(32,32),interpolation=cv2.INTER_AREA)
    crops.append(cv2.resize(sq,(64,64),interpolation=cv2.INTER_AREA))
    f=(255-r.astype(float)).flatten()/255
    feats.append(np.concatenate([f,[w/h*0.5, w/100]]))
X=np.array(feats)
print(X.shape)
km=KMeans(n_clusters=36,n_init=10,random_state=0).fit(X)
lab=km.labels_
np.save('work/cl_lab.npy',lab)
json.dump(items,open('work/cl_items.json','w'))
# montage
rows=[]
for c in range(36):
    idx=np.where(lab==c)[0]
    tiles=[crops[t] for t in idx[:16]]
    while len(tiles)<16: tiles.append(np.full((64,64),255,np.uint8))
    row=np.hstack(tiles)
    rows.append(row)
    print(c,len(idx))
# 3 montages
for p in range(3):
    m=np.vstack(rows[p*12:(p+1)*12])
    cv2.imwrite(f'work/montage_{p}.png',m)
