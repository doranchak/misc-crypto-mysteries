import numpy as np
from PIL import Image
im=np.asarray(Image.open('scans/img-010.png').convert('L')).astype(float)
# coin front region
sub=im[250:860,180:780]
# coin face is light gray (~170); hands dark (~80). find coin center via bright disk
mask=sub>120
ys,xs=np.nonzero(mask)
cy,cx=ys.mean(),xs.mean(); R=np.sqrt(mask.sum()/np.pi)
print('disk center',cx,cy,'radius',R)
Y,X=np.mgrid[0:sub.shape[0],0:sub.shape[1]]
rr=np.hypot(X-cx,Y-cy)
dark=(sub<110)&(rr<R*0.85)
ys,xs=np.nonzero(dark)
# hub: small circle near center; find pixels with r>40 to isolate hands
ang=np.degrees(np.arctan2(xs-cx, -(ys-cy)))%360   # clockwise from 12 o'clock
r=np.hypot(xs-cx,ys-cy)
sel=r>45
for lo,hi,name in [(0,90,'upper hand'),(90,270,'lower hand')]:
    m=sel&(ang>=lo)&(ang<hi)
    px,py=xs[m],ys[m]
    # PCA line fit
    P=np.stack([px,py],1).astype(float); mu=P.mean(0)
    u,s,vt=np.linalg.svd(P-mu); d=vt[0]
    # orient away from center
    if np.dot(d,mu-[cx,cy])<0: d=-d
    a=np.degrees(np.arctan2(d[0],-d[1]))%360
    tip=P[np.argmax(np.hypot(P[:,0]-cx,P[:,1]-cy))]
    print(name,'n=',m.sum(),'bearing(cw from 12)=%.1f'%a,'length=%.0f'%np.hypot(tip[0]-cx,tip[1]-cy), 'mean r=%.0f'%r[m].mean())
hub=(r<45)
hx,hy=xs[hub].mean(),ys[hub].mean()
print('hub center',hx,hy,'offset from disk center',hx-cx,hy-cy)
r2=np.hypot(xs-hx,ys-hy); ang2=np.degrees(np.arctan2(xs-hx,-(ys-hy)))%360
for lo,hi,name in [(0,90,'upper'),(90,270,'lower')]:
    m=(r2>30)&(ang2>=lo)&(ang2<hi)
    print(name,'max length from hub %.0f'%r2[m].max(),'tip bearing %.1f'%ang2[m][np.argmax(r2[m])])
print('coin radius',R)
