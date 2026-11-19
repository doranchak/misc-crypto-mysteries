import sys, json, pickle, numpy as np
import boot, decode as dc, decode2 as d2, selftrain as st
lab=boot.build_train(boot.load_ver())
st.lab_ver=lab
trn=np.array(sorted(lab)); tl=[lab[i] for i in trn]; clf=st.fit(lab)
FS=json.load(open('fixed_spans.json'))
import os
FG=json.load(open('forced_suggest.json')) if os.path.exists('forced_suggest.json') else {}
# block-hand numeral header lines (not letters): never decoded
EXCL={('b3R',0),('b3L',3)}
# trailing pieces that are gutter shadow / page-edge blotches, not glyphs: line -> number of pieces to keep
NMAX={('b3R',13):25}
def decode_line(page,li,minpieces=5):
    pcs=boot.lines_of(page)[li]
    if (page,li) in NMAX: pcs=pcs[:NMAX[(page,li)]]
    if (page,li) in EXCL: return None
    if len(pcs)<minpieces: return None
    lp=st.line_logp(page,li,clf,trn,tl)[:len(pcs)]
    gaps=boot.gaps_of(pcs); medw=boot.medw_of(page)
    fixed=sorted([tuple(x)+('V',) for x in FS.get(page,{}).get(str(li),[])]+[tuple(x)+('G',) for x in FG.get(page,{}).get(str(li),[])])
    out=[]; pos=0
    def seg(a,b):
        if b<=a: return []
        o,_=d2.decode_bigram(lp[a:b],gaps[a:b-1],medw,K=8,widths=[p['w'] for p in pcs[a:b]])
        res=[]
        for i,j,w in o:
            if w=='': continue
            L=j-i
            vs=[v for v in dc.variants(w.upper()) if len(v)==L] if not w.islower() else []
            if vs:
                best=max(vs,key=lambda v:sum(lp[a+i+t,v[t]] for t in range(L)))
                conf=float(np.mean([np.exp(lp[a+i+t,best[t]]) for t in range(L)]))
            else:
                conf=float(np.mean(np.exp(lp[a+i:a+j,:26].max(1))))
            res.append((a+i,a+j,w,'D',round(conf,2)))
        return res
    for (i,j,w,fl) in fixed:
        out+=seg(pos,i); pos=j
        if w=='': continue          # pieces that are shadow / blotches / unused: no output
        out.append((i,j,w,'V',1.0) if fl=='V' else (i,j,w,'D',0.4))
    out+=seg(pos,len(pcs))
    # a one-piece 'word' with near-zero confidence is a fragment of a split glyph: fold it into the touching neighbour, else drop it
    changed=True
    while changed:
        changed=False
        for n,(i,j,w,f,c) in enumerate(out):
            if f=='D' and j-i==1 and c<0.1:
                p=pcs[i]; gp=(p['x']-(pcs[i-1]['x']+pcs[i-1]['w'])) if i>0 else 1e9; gn=(pcs[i+1]['x']-(p['x']+p['w'])) if i+1<len(pcs) else 1e9
                lim=0.25*medw
                if n>0 and out[n-1][1]==i and gp<=lim and gp<=gn:
                    a=out[n-1]; out[n-1]=(a[0],j,a[2],a[3],a[4]); del out[n]
                elif n+1<len(out) and out[n+1][0]==j and gn<=lim:
                    b=out[n+1]; out[n+1]=(i,b[1],b[2],b[3],b[4]); del out[n]
                else: del out[n]
                changed=True; break
    return out
if __name__=='__main__':
    res={}
    for page in ['b2L','b2R','b3L','b3R']:
        for li in range(len(boot.lines_of(page))):
            o=decode_line(page,li)
            if o: res[f'{page}:{li}']=o
    pickle.dump(res,open('final_decode.pkl','wb'))
    for k,o in res.items():
        print(k,' '.join((w if f=='V' else w.lower() if False else w+('?' if c<0.55 else '')) for i,j,w,f,c in o))
