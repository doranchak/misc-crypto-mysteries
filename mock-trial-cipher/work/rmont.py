import json, cv2, numpy as np
S=4
d=json.load(open('work/lines.json'))
boxes=d['boxes']
im = cv2.imread('original.png',0)
big = cv2.resize(im,None,fx=S,fy=S,interpolation=cv2.INTER_CUBIC)
lab=np.load('work/cl_lab.npy'); items=json.load(open('work/cl_items.json'))
# choose clusters with mostly right-arrow: 2, 11, 13, 19 (kmeans ids may vary) -> show for those clusters
import sys
cl=[int(a) for a in sys.argv[1:]]
tiles=[]
for t,(j,k,i) in enumerate(items):
    if lab[t] in cl:
        x,y,w,h=boxes[i][:4]
        c=big[y:y+h,x:x+w]
        c=cv2.resize(c,(160,80),interpolation=cv2.INTER_CUBIC)
        cv2.putText(c,f'{j}.{k}',(2,12),cv2.FONT_HERSHEY_SIMPLEX,0.4,0,1)
        tiles.append(c)
cols=8
while len(tiles)%cols: tiles.append(np.full((80,160),255,np.uint8))
rows=[np.hstack(tiles[r:r+cols]) for r in range(0,len(tiles),cols)]
m=np.vstack(rows[:14])
cv2.imwrite('work/rmont.png',m); print(len(tiles),m.shape)
