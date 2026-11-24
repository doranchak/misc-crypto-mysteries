import json, cv2, numpy as np, sys
S=4
im = cv2.imread('original.png',0)
big = cv2.resize(im,None,fx=S,fy=S,interpolation=cv2.INTER_CUBIC)
vis0=cv2.cvtColor(big,cv2.COLOR_GRAY2BGR)
centers=json.load(open('work/lines.json'))['centers']
half=int(sys.argv[1]); js=[int(a) for a in sys.argv[2:]]
x0,x1=[(60,1260),(1160,2400)][half]
ims=[]
for j in js:
    c=centers[j]
    y0=max(0,int((c-20)*S)); y1=int((c+20)*S)
    t=vis0[y0:y1,x0:x1].copy()
    cv2.putText(t,f'L{j}',(2,18),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
    # x ticks every 100 big px
    for xx in range(0,t.shape[1],200):
        cv2.line(t,(xx,t.shape[0]-1),(xx,t.shape[0]-12),(0,0,255),2)
    ims.append(t)
    ims.append(np.full((6,t.shape[1],3),180,np.uint8))
cv2.imwrite('work/clean.png',np.vstack(ims))
