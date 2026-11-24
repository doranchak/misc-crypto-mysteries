import json, cv2, numpy as np
S=4
im = cv2.imread('original.png',0)
big = cv2.resize(im,None,fx=S,fy=S,interpolation=cv2.INTER_CUBIC)
blur = cv2.GaussianBlur(big,(0,0),3)
bw = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,61,12)
d=json.load(open('work/lines.json'))
boxes=d['boxes']; centers=d['centers']
lines2=json.load(open('work/lines2.json'))
newlines=[]
for j,idx in enumerate(lines2):
    bs=[boxes[i][:4] for i in idx]
    bs.sort(key=lambda b:b[0])
    # merge boxes with large x-overlap
    merged=[]
    for b in bs:
        if merged:
            a=merged[-1]
            ox=min(a[0]+a[2],b[0]+b[2])-max(a[0],b[0])
            if ox>0.45*min(a[2],b[2]) and max(a[0]+a[2],b[0]+b[2])-min(a[0],b[0])<125:
                x0=min(a[0],b[0]);y0=min(a[1],b[1]);x1=max(a[0]+a[2],b[0]+b[2]);y1=max(a[1]+a[3],b[1]+b[3])
                merged[-1]=[x0,y0,x1-x0,y1-y0]
                continue
        merged.append(list(b))
    # split wide boxes
    out=[]
    for b in merged:
        x,y,w,h=b
        if w>135:
            n=int(round(w/80))
            n=max(n,2)
            proj=(bw[y:y+h,x:x+w]>0).sum(axis=0).astype(float)
            proj=np.convolve(proj,np.ones(9)/9,'same')
            cuts=[0]
            for q in range(1,n):
                tgt=int(w*q/n)
                lo=max(cuts[-1]+40,tgt-30); hi=min(w-40,tgt+30)
                if hi<=lo: continue
                c=lo+int(np.argmin(proj[lo:hi]))
                cuts.append(c)
            cuts.append(w)
            for a,bb in zip(cuts[:-1],cuts[1:]):
                out.append([x+a,y,bb-a,h])
        else:
            out.append(b)
    newlines.append(out)
    print(j,len(idx),len(merged),len(out))
json.dump(newlines,open('work/lines3.json','w'))
