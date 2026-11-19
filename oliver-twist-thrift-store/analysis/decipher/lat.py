import pickle, numpy as np, cv2, collections, sys, json
from skimage.feature import hog
from sklearn.linear_model import LogisticRegression
import boot, decode as dc
SP='/private/tmp/claude-501/-Users-doranchak-projects-github-misc-crypto-mysteries/19d89b9d-5003-435e-9fdc-b7411d73b6b1/scratchpad/'
FL={'b1':pickle.load(open('b1_pieces.pkl','rb'))['flat']}
for t in ['b2L','b2R','b3L','b3R']: FL[t]=boot.A[t]['flat']
def mask_feat(p,size=40):
    m=p['mask']; h,w=m.shape; s=(size-6)/max(h,w)
    r=cv2.resize(m,(max(1,int(w*s)),max(1,int(h*s))),interpolation=cv2.INTER_AREA)
    c=np.zeros((size,size),np.uint8); oy=(size-r.shape[0])//2; ox=(size-r.shape[1])//2
    c[oy:oy+r.shape[0],ox:ox+r.shape[1]]=r
    c=cv2.GaussianBlur(c,(3,3),0)
    return hog(c.astype(np.float32)/255,orientations=9,pixels_per_cell=(8,8),cells_per_block=(2,2))
def tile_feat(page,p,W=120,H=170):
    flat=FL[page]
    cx=int(p['cx']); cy=int(p['cy']); x0=max(0,cx-W//2); y0=max(0,cy-H//2)
    t=flat[y0:y0+H,x0:x0+W]; t=cv2.copyMakeBorder(t,0,H-t.shape[0],0,W-t.shape[1],cv2.BORDER_CONSTANT,value=200)
    t=cv2.resize(t,(48,68),interpolation=cv2.INTER_AREA); t=255-t.astype(np.float32); t=(t-t.mean())/(t.std()+1e-6)
    return hog(t,orientations=9,pixels_per_cell=(8,8),cells_per_block=(2,2))
def hog64(p):
    m=p['mask']; h,w=m.shape; sz=64; s=(sz-4)/max(h,w); r=cv2.resize(m,(max(1,int(w*s)),max(1,int(h*s))),interpolation=cv2.INTER_AREA)
    c=np.zeros((sz,sz),np.float32); oy=(sz-r.shape[0])//2; ox=(sz-r.shape[1])//2; c[oy:oy+r.shape[0],ox:ox+r.shape[1]]=r/255.0
    c=cv2.GaussianBlur(c,(3,3),0)
    return hog(c,orientations=12,pixels_per_cell=(8,8),cells_per_block=(2,2))
def feat(page,p): return np.concatenate([mask_feat(p),tile_feat(page,p),hog64(p)])
CACHE={}
def F(page,li,j):
    k=(page,li,j)
    if k not in CACHE: CACHE[k]=feat(page,boot.lines_of(page)[li][j])
    return CACHE[k]
def train(ver):
    lab=boot.build_train(ver)
    X=[];y=[]
    for i,l in lab.items():
        m=boot.meta[i]; X.append(F(m[0],m[1],m[2])); y.append(l)
    cnt=collections.Counter(y)
    keep=[k for k,l in enumerate(y) if len(l)==1]
    X=np.array([X[k] for k in keep]); y=[y[k] for k in keep]
    clf=LogisticRegression(C=5,max_iter=3000); clf.fit(X,y)
    return clf
def lattice(clf,page,li,topk=3):
    pcs=boot.lines_of(page)[li]; medw=boot.medw_of(page)
    out=[]
    for j,p in enumerate(pcs):
        if p['h']<(60 if page=='b1' else 45) or p['w']<(28 if page=='b1' else 18): continue
        pr=clf.predict_proba([F(page,li,j)])[0]; o=np.argsort(-pr)[:topk]
        out.append((j,p,[(clf.classes_[k],pr[k]) for k in o]))
    return out
def show(clf,page,li,topk=3):
    L=lattice(clf,page,li,topk); medw=boot.medw_of(page); s=[]
    prev=None
    for j,p,c in L:
        if prev is not None:
            gap=p['x']-(prev['x']+prev['w'])
            s.append(' | ' if gap>0.42*medw else ' ')
        s.append(f"{j}:"+'/'.join(a for a,_ in c))
        prev=p
    return ''.join(s)
if __name__=='__main__':
    ver=boot.load_ver(); clf=train(ver)
    page=sys.argv[1]
    for li in [int(a) for a in sys.argv[2:]]:
        print(li,show(clf,page,li))
