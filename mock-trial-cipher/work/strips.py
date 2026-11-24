import json, cv2, numpy as np, sys
S=4
im = cv2.imread('original.png',0)
big = cv2.resize(im,None,fx=S,fy=S,interpolation=cv2.INTER_CUBIC)
lines=json.load(open('work/lines3.json'))
H=112
strips={}
fits={}
for j,bs in enumerate(lines):
    xs=np.array([b[0]+b[2]/2 for b in bs]); ys=np.array([b[1]+b[3]/2 for b in bs])
    keep=np.ones(len(xs),bool)
    for _ in range(3):
        p=np.polyfit(xs[keep],ys[keep],1)
        res=np.abs(ys-np.polyval(p,xs))
        keep=res<max(25,np.median(res)*2.5)
    p=np.polyfit(xs[keep],ys[keep],1)
    fits[j]=p.tolist()
    # shear: new_y = y - (a*x + b) + H/2
    a,b=p
    M=np.array([[1,0,0],[-a,1,-b+H/2]],dtype=np.float32)
    strip=cv2.warpAffine(big,M,(big.shape[1],H),flags=cv2.INTER_CUBIC,borderValue=255)
    strips[j]=strip
json.dump(fits,open('work/fits.json','w'))
np.save('work/strips.npy',np.array([strips[j] for j in range(len(lines))]))
print({j:round(fits[j][0],3) for j in fits})
