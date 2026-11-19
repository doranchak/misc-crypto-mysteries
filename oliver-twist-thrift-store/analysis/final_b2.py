import cv2, numpy as np, pickle, collections
from skimage.morphology import skeletonize
from scipy.ndimage import distance_transform_edt
import glyphlib
from glyphlib import glyph_mask, merge_contained, components, best_angle
from split import split_unit

def flatten(reg):
    cl=cv2.createCLAHE(clipLimit=3.0,tileGridSize=(6,6)); r2=cl.apply(reg)
    bg=cv2.GaussianBlur(r2,(0,0),35)
    return cv2.divide(r2,bg,scale=200)

def extract(name,box,rot,maskfun=None,block=81,C=14):
    reg=glyphlib.load_region(name,box,rot)
    flat=flatten(reg)
    blur=cv2.GaussianBlur(flat,(5,5),0)
    th=cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,block,C)
    th=cv2.morphologyEx(th,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    if maskfun: th=maskfun(th)
    comps,lab=components(th,min_area=40)
    gl=merge_contained(comps,lab)
    units=[g for g in gl if g['kind']=='glyph' and g['area']>=400 and g['w']<430 and g['h']<260]
    return reg,flat,lab,units

def pieces_from_units(tag,lab,units,m):
    out=[]
    for ui,g in enumerate(units):
        mk=glyph_mask(lab,g)
        sp=split_unit(mk,m) if g['w']>1.5*m else [(0,g['w'])]
        for pi,(a,b) in enumerate(sp):
            sub=mk[:,a:b]; ys,xs=np.nonzero(sub)
            if len(ys)<150: continue
            y0,y1=ys.min(),ys.max()+1; x0,x1=xs.min(),xs.max()+1
            sub=sub[y0:y1,x0:x1]
            out.append(dict(page=tag,unit=ui,pi=pi,np=len(sp),x=g['x']+a+x0,y=g['y']+y0,w=x1-x0,h=y1-y0,
                            cx=g['x']+a+x0+(x1-x0)/2,cy=g['y']+y0+(y1-y0)/2,mask=sub,ndots=g['ndots']))
    return out

SZ=40
def skel_pts(mask):
    h,w=mask.shape; s=(SZ-6)/max(h,w)
    nh,nw=max(2,int(round(h*s*3))),max(2,int(round(w*s*3)))
    r=cv2.resize(mask,(nw,nh),interpolation=cv2.INTER_AREA)>100
    ys,xs=np.nonzero(skeletonize(r)); ys=ys/3.0; xs=xs/3.0
    oy,ox=(SZ-nh/3.0)/2,(SZ-nw/3.0)/2
    return np.stack([ys+oy,xs+ox],1)
def chamfer_feats(ps):
    N=len(ps); S=np.zeros((N,SZ*SZ),np.float32); Dt=np.zeros((N,SZ*SZ),np.float32)
    for i,p in enumerate(ps):
        pts=skel_pts(p['mask']); img=np.zeros((SZ,SZ),bool)
        img[np.clip(np.round(pts[:,0]).astype(int),0,SZ-1),np.clip(np.round(pts[:,1]).astype(int),0,SZ-1)]=True
        Dt[i]=np.minimum(distance_transform_edt(~img),6).ravel(); S[i]=img.ravel()/max(1,img.sum())
    return S,Dt
med={'b1':112,'b3L':90,'b3R':84,'b2L':100,'b2R':85}
def extra(ps):
    asp=np.array([min(p['w']/p['h'],2.5) for p in ps]); hh=np.array([min(p['h']/med[p['page']],1.8) for p in ps]); nd=np.array([p['ndots'] for p in ps],float)
    return asp,hh,nd

if __name__=='__main__':
    # --- b2R : mask out illustration area (region coords = orig - (2050,250))
    def mask_b2R(th):
        th=th.copy(); th[(2690-2050):(3900-2050)] if False else None
        th[80:760, 640:1900]=0   # illustration block (orig x 2690.., y 330..1010)
        return th
    regR,flatR,labR,unitsR=extract('book2.jpeg',(2050,250,3950,2750),-1.0,mask_b2R)
    wR=np.median([u['w'] for u in unitsR]); print('b2R units',len(unitsR),'median w',wR)
    regL,flatL,labL,unitsL=extract('book2.jpeg',(330,150,2050,1350),-4.75,None)
    wL=np.median([u['w'] for u in unitsL]); print('b2L units',len(unitsL),'median w',wL)
    pR=pieces_from_units('b2R',labR,unitsR,0.8*wR); pL=pieces_from_units('b2L',labL,unitsL,0.8*wL)
    print('pieces',len(pR),len(pL))
    pickle.dump(dict(R=(regR,flatR,pR),L=(regL,flatL,pL)),open('seg/b2_pieces.pkl','wb'))
    cv2.imwrite('seg/b2R_flatfull.png',flatR); cv2.imwrite('seg/b2L_flatfull.png',flatL)
    vis=cv2.cvtColor(flatR,cv2.COLOR_GRAY2BGR)
    for p in pR: cv2.rectangle(vis,(p['x'],p['y']),(p['x']+p['w'],p['y']+p['h']),(0,0,255),2)
    cv2.imwrite('seg/b2R_final_ov.png',vis)
    vis=cv2.cvtColor(flatL,cv2.COLOR_GRAY2BGR)
    for p in pL: cv2.rectangle(vis,(p['x'],p['y']),(p['x']+p['w'],p['y']+p['h']),(0,0,255),2)
    cv2.imwrite('seg/b2L_final_ov.png',vis)
