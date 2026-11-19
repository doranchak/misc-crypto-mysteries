import cv2, numpy as np, json, sys
OT='/Users/doranchak/projects/github/misc-crypto-mysteries/oliver-twist-thrift-store/'
def ink(img,blur=1.5,k=0.62):
    g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) if img.ndim==3 else img
    g=cv2.GaussianBlur(g,(0,0),blur)
    bg=cv2.GaussianBlur(g,(0,0),40)
    n=cv2.divide(g,bg,scale=200)   # background-normalised
    _,th=cv2.threshold(n,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    return (th>0).astype(np.uint8)
def comps(mask,minarea=120,dil=(1,1)):
    m=mask
    if dil!=(1,1): m=cv2.dilate(mask,np.ones(dil,np.uint8))
    n,lab,st,cen=cv2.connectedComponentsWithStats(m,connectivity=8)
    out=[(int(st[i,0]),int(st[i,1]),int(st[i,2]),int(st[i,3]),int(st[i,4])) for i in range(1,n) if st[i,4]>=minarea]
    return sorted(out)
def overlay(img,boxes,out,scale=1.0):
    c=img.copy() if img.ndim==3 else cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    for k,(x,y,w,h,a) in enumerate(boxes):
        cv2.rectangle(c,(x,y),(x+w,y+h),(0,0,255),2); cv2.putText(c,str(k),(x,max(14,y-4)),cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,0,0),2)
    c=cv2.resize(c,None,fx=scale,fy=scale,interpolation=cv2.INTER_AREA); cv2.imwrite(out,c)
