import sys, numpy as np
import boot, decode as dc, selftrain as st
lab=boot.build_train(boot.load_ver()); st.lab_ver=lab
WHW=[w for w in dc.vocab if w.startswith('WH') or 'WH' in w]
def score(lp,i,j,w):
    best=-1e9
    for v in dc.variants(w):
        L=j-i
        if len(v)==L: best=max(best,sum(lp[i+t,v[t]] for t in range(L)))
        elif len(v)==L-1:
            for m in range(len(v)):
                s=sum(lp[i+t,v[t]] for t in range(m))+max(lp[i+m,v[m]],lp[i+m+1,v[m]])+sum(lp[i+t+1,v[t]] for t in range(m+1,len(v)))-1.5
                best=max(best,s)
    return best
for a in sys.argv[1:]:
    page,li,i,j=a.split(':'); li,i,j=int(li),int(i),int(j)
    ex={k for k in lab if boot.meta[k][0]==page and boot.meta[k][1]==li and boot.meta[k][2] in range(i,j)}
    lab2={k:v for k,v in lab.items() if k not in ex}
    trn=np.array(sorted(lab2)); tl=[lab2[x] for x in trn]; clf=st.fit(lab2)
    lp=st.line_logp(page,li,clf,trn,tl)
    res=sorted(((score(lp,i,j,w)+0.3*dc.vocab.get(w,-18),w) for w in WHW),reverse=True)[:8]
    print(a,[(round(s,1),w) for s,w in res])
