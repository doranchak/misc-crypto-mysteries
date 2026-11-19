import cv2, numpy as np, pickle
from skimage.morphology import skeletonize
from scipy.ndimage import distance_transform_edt
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform
from glyphlib import norm_img
pieces=pickle.load(open('seg/pieces.pkl','rb'))
SZ=40
def skel_canvas(mask):
    h,w=mask.shape
    s=(SZ-6)/max(h,w)
    nh,nw=max(2,int(round(h*s*3))),max(2,int(round(w*s*3)))
    r=cv2.resize(mask,(nw,nh),interpolation=cv2.INTER_AREA)>100
    sk=skeletonize(r)
    ys,xs=np.nonzero(sk)
    ys=ys/3.0; xs=xs/3.0
    oy,ox=(SZ-nh/3.0)/2,(SZ-nw/3.0)/2
    pts=np.stack([ys+oy,xs+ox],1)
    return pts
N=len(pieces)
S=np.zeros((N,SZ*SZ),np.float32); Dt=np.zeros((N,SZ*SZ),np.float32)
for i,p in enumerate(pieces):
    pts=skel_canvas(p['mask'])
    img=np.zeros((SZ,SZ),bool)
    yy=np.clip(np.round(pts[:,0]).astype(int),0,SZ-1); xx=np.clip(np.round(pts[:,1]).astype(int),0,SZ-1)
    img[yy,xx]=True
    d=distance_transform_edt(~img)
    Dt[i]=np.minimum(d,6).ravel()
    S[i]=img.ravel()/max(1,img.sum())
A=S@Dt.T      # A[i,j] = mean over pts of i of Dt_j
D=A+A.T
np.fill_diagonal(D,0)
# add aspect / size terms
asp=np.array([min(p['w']/p['h'],2.5) for p in pieces])
med={'b1':112,'b3L':90,'b3R':84}
hh=np.array([min(p['h']/med[p['page']],1.8) for p in pieces])
nd=np.array([p['ndots'] for p in pieces],float)
D=D+0.8*np.abs(asp[:,None]-asp[None,:])+0.8*np.abs(hh[:,None]-hh[None,:])+0.6*np.abs(nd[:,None]-nd[None,:])
pickle.dump(D,open('seg/chamfer_D.pkl','wb'))
Z=linkage(squareform(D,checks=False),'average')
pickle.dump(Z,open('seg/chamfer_Z.pkl','wb'))
for k in (26,34,45):
    cl=fcluster(Z,k,'maxclust')
    n=np.bincount(cl)[1:]
    print(k,'sizes',sorted(n,reverse=True)[:12],'singletons',(n<4).sum())
