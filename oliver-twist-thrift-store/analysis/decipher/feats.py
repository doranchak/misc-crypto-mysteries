import sys; sys.path.insert(0,'..')
import numpy as np, pickle, cv2, collections
import final_b2 as fb
fb.med.update({'b1':112,'b3L':90,'b3R':84,'b2L':100,'b2R':85})
b1=pickle.load(open('b1_labeled.pkl','rb'))
A=pickle.load(open('allpieces.pkl','rb'))
pieces=[]   # flat list with refs
for li,l in enumerate(b1):
    for j,p in enumerate(l):
        q=dict(p); q['page']='b1'; q['line']=li; q['idx']=j; q['ndots']=q.get('ndots',0); pieces.append(q)
for tag in ['b2L','b2R','b3L','b3R']:
    for li,l in enumerate(A[tag]['lines']):
        for j,p in enumerate(l):
            q=dict(p); q['page']=tag; q['line']=li; q['idx']=j; pieces.append(q)
print(len(pieces))
S,Dt=fb.chamfer_feats(pieces)
asp,hh,nd=fb.extra(pieces)
A1=S@Dt.T
D=A1+A1.T
D=D+0.8*np.abs(asp[:,None]-asp[None,:])+0.8*np.abs(hh[:,None]-hh[None,:])+0.6*np.abs(nd[:,None]-nd[None,:])
meta=[(p['page'],p['line'],p['idx'],p.get('label')) for p in pieces]
pickle.dump(dict(D=D.astype(np.float32),meta=meta),open('D.pkl','wb'))
print(D.shape, np.percentile(D,[1,5,50]))
