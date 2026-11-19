import cv2, numpy as np, pickle
k=cv2.imread('/Users/doranchak/projects/github/misc-crypto-mysteries/oliver-twist-thrift-store/key.jpg')
b,g,r=[k[:,:,i].astype(int) for i in range(3)]
m=((b-r>70)&(b-g>60)).astype(np.uint8)*255
print(m.sum()/255)
cv2.imwrite('blue_mask.png',cv2.resize(m,None,fx=2,fy=2,interpolation=cv2.INTER_NEAREST))
n,lab,st,cen=cv2.connectedComponentsWithStats(cv2.dilate(m,np.ones((2,2),np.uint8)),8)
comps=[(int(st[i][0]),int(st[i][1]),int(st[i][2]),int(st[i][3]),int(st[i][4])) for i in range(1,n) if st[i][4]>=6]
print(len(comps))
pickle.dump(comps,open('blue_comps.pkl','wb'))
