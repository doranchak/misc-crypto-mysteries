import numpy as np, cv2, sys
st=np.load('work/strips.npy')
half=int(sys.argv[1]); js=[int(a) for a in sys.argv[2:]]
x0,x1=[(60,1260),(1160,2400)][half]
ims=[]
for j in js:
    t=cv2.cvtColor(st[j][:,x0:x1],cv2.COLOR_GRAY2BGR)
    cv2.putText(t,f'L{j}',(2,18),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
    for xx in range(0,t.shape[1],200):
        cv2.line(t,(xx,t.shape[0]-1),(xx,t.shape[0]-10),(0,0,255),2)
    ims.append(t); ims.append(np.full((4,t.shape[1],3),150,np.uint8))
cv2.imwrite('work/clean.png',np.vstack(ims))
