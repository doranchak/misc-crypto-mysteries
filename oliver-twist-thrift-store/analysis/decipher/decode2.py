import sys, pickle, numpy as np, collections, math
import boot, decode as dc, lat
uni,bi,Ntok=pickle.load(open('bigram.pkl','rb'))
def lpb(prev,w,lam=0.6):
    if uni.get(w,0)==0: return -19.0
    pu=(uni.get(w,0)+0.1)/(Ntok+1)
    cb=bi.get((prev,w),0); cp=uni.get(prev,0)
    pb=cb/cp if cp>0 else 0
    return math.log(lam*pb+(1-lam)*pu)
_clf=None
def get_clf(ver):
    global _clf
    _clf=lat.train(ver); return _clf
def piece_logp(page,li,ver,mix_lr=0.5,tau=0.6,k=7):
    lab=boot.build_train(ver)
    pcs=boot.lines_of(page)[li]
    ti=np.array([i for i in lab if not (boot.meta[i][0]==page and boot.meta[i][1]==li)]); tl=[lab[i] for i in ti]
    kn=np.array([np.exp(dc.knn_logp(boot.D,boot.idx[(page,li,j)],ti,tl,tau=tau,k=k)) for j in range(len(pcs))])
    # LR (trained excluding this line)
    X=[];y=[]
    for i,l in zip(ti,tl):
        if len(l)==1: X.append(lat.F(boot.meta[i][0],boot.meta[i][1],boot.meta[i][2])); y.append(l)
    from sklearn.linear_model import LogisticRegression
    clf=LogisticRegression(C=5,max_iter=2000).fit(np.array(X),y)
    Xt=np.array([lat.F(page,li,j) for j in range(len(pcs))]); pr=clf.predict_proba(Xt)
    lr=np.full((len(pcs),dc.NS),1e-4)
    for c,cl in enumerate(clf.classes_): lr[:,dc.LI[cl]]=pr[:,c]
    lr/=lr.sum(1,keepdims=True)
    p=(1-mix_lr)*kn+mix_lr*lr
    return np.log(p/p.sum(1,keepdims=True))
MERGE_BASE=3.5; MERGE_G=2.0; SKIP_NARROW=1.5; SKIP_WIDE=99.0; MERGE_MAXGAP=0.2
def decode_bigram(logP,gaps,medw,K=8,alpha=1.0,gam=1.3,oov=-16.0,maxL=13,beam=6,widths=None,merge=True,skip=True):
    m=logP.shape[0]; g=np.array(gaps)/medw if m>1 else np.array([])
    def bc(k):
        gg=g[k-1]
        if gg>0.5: return 0.0,3.0
        if gg<0.15: return 4.0,0.0
        return 1.5,0.5
    # candidate words per span
    cands={}
    for i in range(m):
        for L in range(1,min(maxL,m-i)+1):
            j=i+L; sl=logP[i:j]; lst=[]
            if L in dc.WA:
                idx,lf,ws=dc.WA[L]
                s=alpha*sl[np.arange(L)[None,:],idx].sum(1)+0.3*lf
                top=np.argpartition(-s,min(K*3,len(s)-1))[:K*3]
                seen={}
                for t in top:
                    w=ws[t]
                    sc=alpha*float(sl[np.arange(L),idx[t]].sum())
                    if w not in seen or sc>seen[w]: seen[w]=sc
                lst=sorted(seen.items(),key=lambda x:-(x[1]+0.3*dc.vocab.get(x[0],-18)))[:K]
            if merge and L>=3 and (L-1) in dc.WA:
                # one glyph split into two touching pieces: word of L-1 letters over L pieces
                idx2,lf2,ws2=dc.WA[L-1]; n=L-1; N=idx2.shape[0]
                A0=sl[np.arange(n)[None,:],idx2]; A1=sl[np.arange(1,n+1)[None,:],idx2]
                pre0=np.concatenate([np.zeros((N,1)),np.cumsum(A0,1)],1); suf1=np.concatenate([np.cumsum(A1[:,::-1],1)[:,::-1],np.zeros((N,1))],1)
                bestm=np.full(N,-1e9)
                for t in range(n):
                    gp=g[i+t]
                    if gp>MERGE_MAXGAP: continue
                    st_=pre0[:,t]+np.maximum(A0[:,t],A1[:,t])+suf1[:,t+1]-(MERGE_BASE+MERGE_G*gp)
                    bestm=np.maximum(bestm,st_)
                if bestm.max()>-1e8:
                    sm=alpha*bestm+0.3*lf2
                    top=np.argpartition(-sm,min(K*3,len(sm)-1))[:K*3]; seen2={}
                    for t_ in top:
                        if bestm[t_]<-1e8: continue
                        w=ws2[t_]; sc=alpha*float(bestm[t_])
                        if w not in seen2 or sc>seen2[w]: seen2[w]=sc
                    lst=lst+sorted(seen2.items(),key=lambda x:-(x[1]+0.3*dc.vocab.get(x[0],-18)))[:K]
            if L>=3:
                bl=sl[:,:26].argmax(1); w=''.join(dc.LET[x] for x in bl).lower()
                lst.append((w,alpha*float(sl[:,:26].max(1).sum())+oov-0.5*L+3.0*0))
            if L==1 and skip:
                narrow=(widths is not None and widths[i]<0.5*medw)
                lst.append(('',-(SKIP_NARROW if narrow else SKIP_WIDE)))
            cands[(i,j)]=lst
    # viterbi with bigram
    states=[{} for _ in range(m+1)]; states[0]={'<S>':(0.0,None)}
    for i in range(m):
        if not states[i]: continue
        for L in range(1,min(maxL,m-i)+1):
            j=i+L; inner=sum(bc(k)[1] for k in range(i+1,j))
            for w,cs in cands[(i,j)]:
                for pw,(ps,_) in states[i].items():
                    brk=bc(i)[0] if i>0 else 0.0
                    wu=w.upper() if w.islower() else w
                    lmv=(0.0 if w=='' else lpb(pw,w)) if not w.islower() else -16.0
                    sc=ps-brk-inner+cs+gam*lmv
                    cur=states[j].get(w)
                    if cur is None or sc>cur[0]: states[j][w]=(sc,(i,pw))
        # prune
        for j in range(i+1,min(m,i+maxL)+1):
            if len(states[j])>beam*3:
                keep=sorted(states[j].items(),key=lambda x:-x[1][0])[:beam*3]; states[j]=dict(keep)
    # backtrack
    if not states[m]: return [],-1e9
    w,(sc,bp)=max(states[m].items(),key=lambda x:x[1][0])
    out=[]; j=m; cur=w; 
    while j>0:
        sc,(i,pw)=states[j][cur]; out.append((i,j,cur)); j=i; cur=pw
    return out[::-1],sc
def run(page,li,ver=None,K=8):
    ver=ver or boot.load_ver()
    logP=piece_logp(page,li,ver)
    pcs=boot.lines_of(page)[li]
    o,sc=decode_bigram(logP,boot.gaps_of(pcs),boot.medw_of(page),K=K)
    return o,sc,logP
if __name__=='__main__':
    page=sys.argv[1]
    for li in [int(a) for a in sys.argv[2:]]:
        o,sc,_=run(page,li)
        print(page,li,len(boot.lines_of(page)[li]),' '.join(w for _,_,w in o))
