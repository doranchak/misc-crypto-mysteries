import sys, numpy as np
import boot, decode as dc, selftrain as st, align as al
lab=boot.build_train(boot.load_ver()); st.lab_ver=lab
words={}
for n,(idx,lf,ws) in dc.WA.items():
    for w,f in zip(ws,lf): words[w]=max(words.get(w,-99),float(f))
W=sorted(words)
def prep(page,li,holdout=True):
    ex={k for k in lab if boot.meta[k][0]==page and boot.meta[k][1]==li} if holdout else set()
    lab2={k:v for k,v in lab.items() if k not in ex}
    trn=np.array(sorted(lab2)); tl=[lab2[x] for x in trn]; clf=st.fit(lab2)
    return st.line_logp(page,li,clf,trn,tl)
_G={}
def _one(w):
    try: items,c=al.align(_G['pcs'],_G['sl'],w.upper())
    except Exception: return None
    return (c-0.25*words[w],w)
def rank(page,li,i,j,lp=None,K=15,minlen=1,maxlen=14):
    import multiprocessing as mp
    lp=prep(page,li) if lp is None else lp
    _G['pcs']=boot.lines_of(page)[li][i:j]; _G['sl']=lp[i:j]
    ws=[w for w in W if minlen<=len(w)<=maxlen and w.isalpha() and not (len(w)>1.8*(j-i)+2 or len(w)<0.5*(j-i)-1)]
    with mp.get_context('fork').Pool(8) as pool: out=[r for r in pool.map(_one,ws,chunksize=200) if r]
    out.sort(); return out[:K]
if __name__=='__main__':
    page=sys.argv[1]; lp=prep(page,int(sys.argv[2]))
    for a in sys.argv[2:]:
        pass
    li=int(sys.argv[2])
    for sp in sys.argv[3:]:
        i,j=map(int,sp.split(':')); print(page,li,i,j,[(round(c,1),w) for c,w in rank(page,li,i,j,lp)])
