import sys, numpy as np
import boot, decode as dc, selftrain as st
lab=boot.build_train(boot.load_ver()); st.lab_ver=lab
trn=np.array(sorted(lab)); tl=[lab[i] for i in trn]; clf=st.fit(lab)
def top(page,li,k=3):
    lp=st.line_logp(page,li,clf,trn,tl); pcs=boot.lines_of(page)[li]; out=[]
    for j in range(len(pcs)):
        o=np.argsort(-lp[j])[:k]
        out.append(' '.join(f'{dc.SYM[t]}{np.exp(lp[j,t])*100:.0f}' for t in o))
    return out
if __name__=='__main__':
    page=sys.argv[1]
    for li in map(int,sys.argv[2:]):
        pcs=boot.lines_of(page)[li]
        print(f'--- {page}:{li} ({len(pcs)} pieces)')
        t=top(page,li)
        for j,(p,s) in enumerate(zip(pcs,t)): print(f'{j:2d} x{int(p["x"]):4d} w{int(p["w"]):3d} h{int(p["h"]):3d}  {s}')
