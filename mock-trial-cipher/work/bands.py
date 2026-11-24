import cv2, numpy as np, sys
S=4
im = cv2.imread('original.png',0)
big = cv2.resize(im,None,fx=S,fy=S,interpolation=cv2.INTER_CUBIC)
y0=int(sys.argv[1]); y1=int(sys.argv[2])
t=cv2.cvtColor(big[y0*S:y1*S,100:2400],cv2.COLOR_GRAY2BGR)
for xx in range(0,t.shape[1],200):
    cv2.line(t,(xx,0),(xx,10),(0,0,255),2)
for yy in range(y0,y1,10):
    cv2.putText(t,str(yy),(0,(yy-y0)*S+6),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),1)
cv2.imwrite('work/band.png',t)
print(t.shape)
