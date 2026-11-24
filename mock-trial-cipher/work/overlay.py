import json, cv2, numpy as np
S=4
d=json.load(open('work/lines.json'))
boxes=d['boxes']; lines=d['lines']; centers=d['centers']
im = cv2.imread('original.png',0)
big = cv2.resize(im,None,fx=S,fy=S,interpolation=cv2.INTER_CUBIC)
vis=cv2.cvtColor(big,cv2.COLOR_GRAY2BGR)
assigned=set(i for l in lines for i in l)
cols=[(0,0,255),(255,0,0),(0,160,0),(200,0,200)]
for j,l in enumerate(lines):
    for k,i in enumerate(l):
        x,y,w,h=boxes[i][:4]
        cv2.rectangle(vis,(x,y),(x+w,y+h),cols[j%4],2)
        cv2.putText(vis,f'{k}',(x+2,y+14),cv2.FONT_HERSHEY_SIMPLEX,0.55,cols[j%4],2)
for i,b in enumerate(boxes):
    if i not in assigned:
        x,y,w,h=b[:4]
        cv2.rectangle(vis,(x,y),(x+w,y+h),(0,200,255),2)
cv2.imwrite('work/overlay_full.png',vis)
for j,c in enumerate(centers):
    y0=max(0,int((c-22)*S)); y1=int((c+22)*S)
    cv2.imwrite(f'work/line_{j:02d}.png',vis[y0:y1,:])
