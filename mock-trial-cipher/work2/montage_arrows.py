import json, cv2, numpy as np
tr=json.load(open('../work/tracked.json')); bs=tr['boxes']
im=cv2.imread('../original.png'); S=4
big=cv2.resize(im,None,fx=S,fy=S,interpolation=cv2.INTER_CUBIC)
g=cv2.cvtColor(big,cv2.COLOR_BGR2GRAY)
items=[]
for j,ch in enumerate(tr['lines']):
    for k,i in enumerate(ch):
        x,y,w,h=bs[i]
        if w>=1.2*h and 60<=w<=170 and h<=120 and y>0:
            items.append((j+1,k,x,y,w,h))
print(len(items))
cw,chh=190,140
cols=8
rows=(len(items)+cols-1)//cols
M=np.full((rows*chh,cols*cw,3),255,np.uint8)
for n,(j,k,x,y,w,h) in enumerate(items):
    cx,cy=x+w//2,y+h//2
    crop=big[max(0,cy-chh//2+10):cy+chh//2-10, max(0,cx-cw//2+5):cx+cw//2-5]
    r,c=divmod(n,cols)
    M[r*chh:r*chh+crop.shape[0], c*cw:c*cw+crop.shape[1]]=crop
    cv2.putText(M,f'{j}.{k}',(c*cw+3,r*chh+14),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1)
half=rows//2
cv2.imwrite('mont_a.png',M[:half*chh]); cv2.imwrite('mont_b.png',M[half*chh:])
json.dump(items,open('arrow_items.json','w'))
