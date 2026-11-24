import json, cv2, numpy as np
S=4
d=json.load(open('work/lines.json'))
boxes=d['boxes']; centers=d['centers']
# add extra lines for handwriting-free check later
im = cv2.imread('original.png',0)
big = cv2.resize(im,None,fx=S,fy=S,interpolation=cv2.INTER_CUBIC)
vis=cv2.cvtColor(big,cv2.COLOR_GRAY2BGR)
lines2=[]
for j,c in enumerate(centers):
    idx=[i for i,b in enumerate(boxes) if abs(b[5]/S-c)<19]
    idx.sort(key=lambda i:boxes[i][0])
    lines2.append(idx)
json.dump(lines2,open('work/lines2.json','w'))
for j,idx in enumerate(lines2):
    c=centers[j]
    y0=max(0,int((c-24)*S)); y1=int((c+24)*S)
    for half,(x0,x1) in enumerate([(100,1300),(1180,2400)]):
        t=vis[y0:y1,x0:x1].copy()
        for k,i in enumerate(idx):
            x,y,w,h=boxes[i][:4]
            if x+w<x0 or x>x1: continue
            col=(0,0,255) if k%2==0 else (255,0,0)
            cv2.rectangle(t,(x-x0,y-y0),(x-x0+w,y-y0+h),col,1)
            cv2.putText(t,f'{k}',(x-x0+2,y-y0-3 if y-y0>14 else y-y0+h+14),cv2.FONT_HERSHEY_SIMPLEX,0.6,col,2)
        cv2.imwrite(f'work/L{j:02d}_{half}.png',t)
    print(j,c,len(idx))
