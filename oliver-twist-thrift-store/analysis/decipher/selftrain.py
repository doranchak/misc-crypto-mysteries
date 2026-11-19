import sys, pickle, numpy as np, collections, math, json, time
import boot, decode as dc, lat, decode2 as d2
from sklearn.linear_model import LogisticRegression
meta=boot.meta; idx=boot.idx
ver=boot.load_ver()
lab_ver=boot.build_train(ver)             # piece index -> letter(s) from verified lines + page1
Fcache={}
def F(i):
    if i not in Fcache: Fcache[i]=lat.F(meta[i][0],meta[i][1],meta[i][2])
    return Fcache[i]
def fit(lab):
    ids=[i for i in lab if len(lab[i])==1]
    X=np.array([F(i) for i in ids]); y=[lab[i] for i in ids]
    clf=LogisticRegression(C=5,max_iter=2000).fit(X,y)
    return clf
def line_logp(page,li,clf,trn,tl,mix=0.5):
    pcs=boot.lines_of(page)[li]
    kn=np.array([np.exp(dc.knn_logp(boot.D,idx[(page,li,j)],trn,tl)) for j in range(len(pcs))])
    pr=clf.predict_proba(np.array([F(idx[(page,li,j)]) for j in range(len(pcs))]))
    lr=np.full((len(pcs),dc.NS),1e-4)
    for c,cl in enumerate(clf.classes_): lr[:,dc.LI[cl]]=pr[:,c]
    lr/=lr.sum(1,keepdims=True)
    p=(1-mix)*kn+mix*lr; return np.log(p/p.sum(1,keepdims=True))
def decode_labels(page,li,logP):
    pcs=boot.lines_of(page)[li]
    o,sc=d2.decode_bigram(logP,boot.gaps_of(pcs),boot.medw_of(page))
    labs={}; conf={}
    for i,j,w in o:
        if w.islower(): continue
        L=j-i
        vs=[v for v in dc.variants(w) if len(v)==L]
        if not vs: continue
        best=max(vs,key=lambda v:sum(logP[i+t,v[t]] for t in range(L)))
        s=sum(logP[i+t,best[t]] for t in range(L))/L
        for t in range(L): labs[i+t]=dc.SYM[best[t]]
        conf[(i,j)]=(w,s)
    return labs,conf,o
if __name__=='__main__':
    pages=['b2R','b3R','b3L']
    unver=[(p,li) for p in pages for li in range(len(boot.lines_of(p))) if len(boot.lines_of(p)[li])>=8 and not (p in ver and str(li) in ver[p])]
    vlines=[(p,int(l)) for p,ls in ver.items() for l in ls]
    pseudo={}
    for it in range(3):
        t0=time.time()
        # evaluation: fold over verified lines (train on lab_ver minus line + pseudo)
        base=dict(lab_ver)
        for k,v in pseudo.items(): base[k]=v
        ok=0;tot=0
        for (p,l) in vlines:
            lab={k:v for k,v in base.items() if not (meta[k][0]==p and meta[k][1]==l)}
            trn=np.array(sorted(lab)); tl=[lab[i] for i in trn]
            clf=fit(lab)
            lp=line_logp(p,l,clf,trn,tl)
            labs,conf,o=decode_labels(p,l,lp)
            for j,ch in labs.items():
                k=idx[(p,l,j)]
                if k in lab_ver and len(lab_ver[k])==1: tot+=1; ok+=(ch==lab_ver[k])
        print('iter',it,'verified-piece decode acc',ok/max(1,tot),tot,'pseudo',len(pseudo),round(time.time()-t0))
        sys.stdout.flush()
        # pseudo-label unverified lines with global classifier
        trn=np.array(sorted(base)); tl=[base[i] for i in trn]; clf=fit(base)
        new={}
        for (p,li) in unver:
            lp=line_logp(p,li,clf,trn,tl)
            labs,conf,o=decode_labels(p,li,lp)
            for (i,j),(w,s) in conf.items():
                if j-i>=3 and s>-0.9 and dc.vocab.get(w,-30)>-11.5:
                    for t in range(i,j): new[idx[(p,li,t)]]=labs[t]
        pseudo=new
    pickle.dump(pseudo,open('pseudo.pkl','wb'))
