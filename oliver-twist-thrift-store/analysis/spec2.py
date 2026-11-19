import cv2, numpy as np, pickle, sys
from sklearn.cluster import SpectralClustering
from glyphlib import norm_img
pieces=pickle.load(open('seg/pieces.pkl','rb'))
D=pickle.load(open('seg/chamfer_D.pkl','rb'))
k=int(sys.argv[1]); nn=int(sys.argv[2])
N=len(pieces)
# local-scaling affinity with kNN sparsification
srt=np.sort(D,axis=1)
sig=srt[:,7]+1e-6
Aff=np.exp(-(D**2)/(sig[:,None]*sig[None,:]))
mask=np.zeros_like(Aff,bool)
idx=np.argsort(D,axis=1)[:,1:nn+1]
for i in range(N): mask[i,idx[i]]=True
mask=mask|mask.T
Aff=Aff*mask
sc=SpectralClustering(n_clusters=k,affinity='precomputed',random_state=0,assign_labels='cluster_qr')
cl=sc.fit_predict(Aff)
for p,c in zip(pieces,cl): p['cl3']=int(c)
pickle.dump(pieces,open('seg/pieces_cl3.pkl','wb'))
rimgs=[norm_img(p['mask'],40) for p in pieces]
order=sorted(range(k), key=lambda c:-(cl==c).sum())
cell=52; rows=[]
for c in order:
    idx=[i for i in range(N) if cl[i]==c]
    sel=idx[:: max(1,len(idx)//28)][:28]
    row=np.zeros((cell,cell*30),np.uint8)
    cv2.putText(row,str(c),(2,24),cv2.FONT_HERSHEY_SIMPLEX,0.7,255,2)
    cv2.putText(row,'n%d'%len(idx),(2,46),cv2.FONT_HERSHEY_SIMPLEX,0.45,255,1)
    for j,i in enumerate(sel):
        row[:,cell*(j+1):cell*(j+2)]=cv2.resize(rimgs[i],(cell,cell),interpolation=cv2.INTER_AREA)
    rows.append(row)
for p in range(0,len(rows),12):
    cv2.imwrite('seg/sp_%d.png'%(p//12), 255-np.vstack(rows[p:p+12]))
print(sorted([int((cl==c).sum()) for c in range(k)],reverse=True))
