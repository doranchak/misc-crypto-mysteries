import sys, json, pickle, numpy as np
import boot, decode as dc, selftrain as st
lab=boot.build_train(boot.load_ver()); st.lab_ver=lab
def run(spans,K=10):
    trn=np.array(sorted(lab)); tl=[lab[i] for i in trn]; clf=st.fit(lab)
    for page,li,i,j in spans:
        pcs=boot.lines_of(page)[li]
        # hold the line's own labels out to avoid self-fit
        ex={k for k in lab if boot.meta[k][0]==page and boot.meta[k][1]==li}
        lab2={k:v for k,v in lab.items() if k not in ex}
        trn2=np.array(sorted(lab2)); tl2=[lab2[x] for x in trn2]; clf2=st.fit(lab2)
        lp=st.line_logp(page,li,clf2,trn2,tl2)
        sl=lp[i:j]; out=[]
        for n in (j-i,j-i-1):
            if n not in dc.WA: continue
            idx,lf,ws=dc.WA[n]
            if n==j-i:
                s=sl[np.arange(n)[None,:],idx].sum(1)
                for t in np.argsort(-(s+0.3*lf))[:K*3]: out.append((float(s[t]+0.3*lf[t]),ws[t],n))
            else:
                # one merge among adjacent pieces
                A0=sl[np.arange(n)[None,:],idx]; A1=sl[np.arange(1,n+1)[None,:],idx]
                N=idx.shape[0]; pre=np.concatenate([np.zeros((N,1)),np.cumsum(A0,1)],1); suf=np.concatenate([np.cumsum(A1[:,::-1],1)[:,::-1],np.zeros((N,1))],1)
                best=np.full(N,-1e9)
                for t in range(n): best=np.maximum(best,pre[:,t]+np.maximum(A0[:,t],A1[:,t])+suf[:,t+1]-1.5)
                s=best
                for t in np.argsort(-(s+0.3*lf))[:K*3]: out.append((float(s[t]+0.3*lf[t]),ws[t],n))
        seen=set(); res=[]
        for sc,w,n in sorted(out,reverse=True):
            if w in seen: continue
            seen.add(w); res.append((round(sc,1),w))
        print(page,li,i,j,res[:K])
if __name__=='__main__':
    spans=[tuple([a.split(':')[0]]+[int(x) for x in a.split(':')[1:]]) for a in sys.argv[1:]]
    run(spans)
