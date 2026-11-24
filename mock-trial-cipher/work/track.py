import json, cv2, numpy as np
S=4
im = cv2.imread('original.png',0)
big = cv2.resize(im,None,fx=S,fy=S,interpolation=cv2.INTER_CUBIC)
blur = cv2.GaussianBlur(big,(0,0),3)
bw = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,61,12)
boxes=json.load(open('work/boxes.json'))
bs=[b[:4] for b in boxes]
# global merge: same row & x-overlap
bs.sort(key=lambda b:b[0])
changed=True
while changed:
    changed=False
    out=[]
    used=[False]*len(bs)
    for i,a in enumerate(bs):
        if used[i]: continue
        for j in range(i+1,len(bs)):
            if used[j]: continue
            b=bs[j]
            if abs((a[1]+a[3]/2)-(b[1]+b[3]/2))>45: continue
            ox=min(a[0]+a[2],b[0]+b[2])-max(a[0],b[0])
            if ox>0.45*min(a[2],b[2]) and max(a[0]+a[2],b[0]+b[2])-min(a[0],b[0])<125:
                x0=min(a[0],b[0]);y0=min(a[1],b[1]);x1=max(a[0]+a[2],b[0]+b[2]);y1=max(a[1]+a[3],b[1]+b[3])
                a=[x0,y0,x1-x0,y1-y0]; used[j]=True; changed=True
        used[i]=True; out.append(a)
    bs=sorted(out,key=lambda b:b[0])
# split wide
final=[]
for b in bs:
    x,y,w,h=b
    if w>135 and w<700:
        n=max(2,int(round(w/80)))
        proj=(bw[y:y+h,x:x+w]>0).sum(axis=0).astype(float)
        proj=np.convolve(proj,np.ones(9)/9,'same')
        cuts=[0]
        for q in range(1,n):
            tgt=int(w*q/n); lo=max(cuts[-1]+40,tgt-30); hi=min(w-40,tgt+30)
            if hi<=lo: continue
            cuts.append(lo+int(np.argmin(proj[lo:hi])))
        cuts.append(w)
        for a,bb in zip(cuts[:-1],cuts[1:]): final.append([x+a,y,bb-a,h])
    else: final.append(b)
print(len(bs),len(final))
json.dump(final,open('work/gboxes.json','w'))
