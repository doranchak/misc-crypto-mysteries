import sys, json, numpy as np
import boot, decode as dc, decode2 as d2, selftrain as st
lab=dict(st.lab_ver); trn=np.array(sorted(lab)); tl=[lab[i] for i in trn]; clf=st.fit(lab)
def decode_fixed(page,li,fixed,K=8):
    """fixed: list of (i,j,WORD) with j exclusive (piece indexes in boot lines)."""
    lp=st.line_logp(page,li,clf,trn,tl)
    pcs=boot.lines_of(page)[li]; gaps=boot.gaps_of(pcs); medw=boot.medw_of(page)
    fixed=sorted(fixed); out=[]; pos=0; prev='<S>'
    def seg(a,b):
        if b<=a: return []
        sub=lp[a:b]; g=gaps[a:b-1]
        o,_=d2.decode_bigram(sub,g,medw,K=K)
        return [(i+a,j+a,w) for i,j,w in o]
    for (i,j,w) in fixed:
        out+=seg(pos,i); out.append((i,j,w+'*')); pos=j
    out+=seg(pos,len(pcs))
    return out
if __name__=='__main__':
    page=sys.argv[1]; li=int(sys.argv[2]); fx=json.loads(sys.argv[3])
    o=decode_fixed(page,li,[(a,b,w) for a,b,w in fx])
    print(' '.join(f'{w}[{i}-{j-1}]' for i,j,w in o))
