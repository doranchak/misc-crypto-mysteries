import json, cv2, numpy as np
S=4
im = cv2.imread('original.png',0)
big = cv2.resize(im,None,fx=S,fy=S,interpolation=cv2.INTER_CUBIC)
blur = cv2.GaussianBlur(big,(0,0),3)
bw = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,61,12)
# filled blobs: opening with large kernel
k=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15))
op=cv2.morphologyEx(bw,cv2.MORPH_OPEN,k)
n,lab,stats,cent=cv2.connectedComponentsWithStats(op,connectivity=8)
blobs=[]
for i in range(1,n):
    x,y,w,h,a=stats[i]
    if a<900 or a>14000: continue
    if w>200 or h>200: continue
    blobs.append(dict(x=int(x),y=int(y),w=int(w),h=int(h),a=int(a),cx=float(cent[i][0]),cy=float(cent[i][1]),id=i))
print(len(blobs))
vis=cv2.cvtColor(big,cv2.COLOR_GRAY2BGR)
for b in blobs:
    cv2.rectangle(vis,(b['x'],b['y']),(b['x']+b['w'],b['y']+b['h']),(0,0,255),2)
cv2.imwrite('work/blobs_vis.png',vis)
json.dump(blobs,open('work/blobs.json','w'))
# print sorted by y
for b in sorted(blobs,key=lambda b:(round(b['cy']/4/12),b['cx'])):
    print(int(b['cx']/4),int(b['cy']/4),b['w'],b['h'],b['a'])
