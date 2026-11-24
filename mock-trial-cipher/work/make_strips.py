import json, cv2, numpy as np
S=3
im = cv2.imread('../original.png',0)
big = cv2.resize(im,None,fx=S,fy=S,interpolation=cv2.INTER_CUBIC)
d=json.load(open('tracked.json')); bs=d['boxes']; lines=d['lines']
H=40*S
fits=[]
for j,ch in enumerate(lines):
    # box coords are at 4x -> convert to 3x
    xs=np.array([(bs[i][0]+bs[i][2]/2)*S/4 for i in ch]); ys=np.array([(bs[i][1]+bs[i][3]/2)*S/4 for i in ch])
    keep=np.ones(len(xs),bool)
    for _ in range(4):
        p=np.polyfit(xs[keep],ys[keep],1)
        res=np.abs(ys-np.polyval(p,xs)); keep=res<max(18,np.median(res)*2.2)
    p=np.polyfit(xs[keep],ys[keep],1); a,b=p
    M=np.array([[1,0,0],[-a,1,-b+H/2]],dtype=np.float32)
    strip=cv2.warpAffine(big,M,(big.shape[1],H),flags=cv2.INTER_CUBIC,borderValue=255)
    # crop horizontal margins
    strip=strip[:,40:big.shape[1]-20]
    cv2.imwrite(f'../img/line_{j+1:02d}.png',strip)
    fits.append(dict(line=j+1,slope=round(float(a),4),intercept=round(float(b)/S,1)))
json.dump(fits,open('line_fits.json','w'))
print('done',len(fits))
