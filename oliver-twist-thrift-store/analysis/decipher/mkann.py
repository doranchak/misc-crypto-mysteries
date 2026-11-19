import sys; sys.path.insert(0,'..')
import cv2, numpy as np, pickle
import boot, strips
def annotated(page,li,out=None,scale=1.25,halfw=1100,minh=None):
    pcs_all=boot.lines_of(page)[li]
    flat=boot.A[page]['flat'] if page!='b1' else pickle.load(open('b1_pieces.pkl','rb'))['flat']
    mh,mw=(60,28) if page=='b1' else (45,18)
    pcs=[(j,p) for j,p in enumerate(pcs_all) if p['h']>=mh and p['w']>=mw]
    xs=np.array([p['cx'] for _,p in pcs]); ys=np.array([p['cy'] for _,p in pcs])
    hm=np.median([p['h'] for _,p in pcs]); up=int(1.0*hm); dn=int(0.8*hm)
    deg=min(2,max(1,len(pcs)//6)); co=np.polyfit(xs,ys,deg)
    x0=int(max(0,xs.min()-70)); x1=int(min(flat.shape[1],xs.max()+70)); W=x1-x0; H=up+dn
    X=np.tile(np.arange(x0,x1,dtype=np.float32),(H,1))
    base=np.polyval(co,np.arange(x0,x1)).astype(np.float32)
    Y=np.tile(np.arange(-up,dn,dtype=np.float32)[:,None],(1,W))+base[None,:]
    img=cv2.remap(flat,X,Y,cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)
    img=cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    for j,p in pcs:
        bx=int(p['cx']-x0); by=int(np.polyval(co,p['cx'])-p['cy']); cyy=int(up+(p['cy']-np.polyval(co,p['cx'])))
        x_a=int(p['x']-x0); x_b=int(p['x']+p['w']-x0); y_a=int(cyy-p['h']/2); y_b=int(cyy+p['h']/2)
        col=(0,0,255) if j%2==0 else (255,0,0)
        cv2.rectangle(img,(x_a,y_a),(x_b,y_b),col,1)
        cv2.putText(img,str(j),(x_a,max(10,y_a-2)),cv2.FONT_HERSHEY_SIMPLEX,0.45,col,1)
    parts=[img[:,:W//2+60],img[:,W-(W//2+60):]] if W>halfw+150 else [img]
    wm=max(p.shape[1] for p in parts)
    parts=[cv2.copyMakeBorder(p,0,4,0,wm-p.shape[1],cv2.BORDER_CONSTANT,value=(255,255,255)) for p in parts]
    o=np.vstack(parts); o=cv2.resize(o,None,fx=scale,fy=scale,interpolation=cv2.INTER_CUBIC)
    return o
if __name__=='__main__':
    page=sys.argv[1]; lis=[int(a) for a in sys.argv[2:]]
    ims=[annotated(page,li) for li in lis]
    wm=max(i.shape[1] for i in ims)
    ims=[cv2.copyMakeBorder(i,0,8,0,wm-i.shape[1],cv2.BORDER_CONSTANT,value=(255,255,255)) for i in ims]
    cv2.imwrite(f'../lines/{page}_A{lis[0]:02d}.png',np.vstack(ims))
