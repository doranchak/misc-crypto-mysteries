import sys, json, pickle, numpy as np, importlib.util
import boot, decode as dc, selftrain as st
import decode2 as d2new
spec=importlib.util.spec_from_file_location('d2old','decode2_prev.py'); d2old=importlib.util.module_from_spec(spec); spec.loader.exec_module(d2old)
FS=json.load(open('fixed_spans.json'))
lab=boot.build_train(boot.load_ver()); st.lab_ver=lab
PARAMS={'m2.5':(2.5,2.0,1.2,99.0,0.2,True,False),'m2.5+skipN1.5':(2.5,2.0,1.5,99.0,0.2,True,True),'m2.5+skipN0.8':(2.5,2.0,0.8,99.0,0.2,True,True),
 'm2.0+skipN1.5':(2.0,2.0,1.5,99.0,0.25,True,True),'m3.5+skipN1.5':(3.5,2.0,1.5,99.0,0.2,True,True)}
CONFIGS=[('old',d2old)]+[(k,d2new) for k in PARAMS]
res={k:[0,0] for k,_ in CONFIGS}; per=[]
for page,ls in FS.items():
    for li,spans in ls.items():
        li=int(li); pcs=boot.lines_of(page)[li]
        words=[(i,j,w) for i,j,w in spans]
        if sum(j-i for i,j,w in words)<0.6*len(pcs): continue
        excl=[k for k in lab if boot.meta[k][0]==page and boot.meta[k][1]==li]
        lab2={k:v for k,v in lab.items() if k not in set(excl)}
        trn=np.array(sorted(lab2)); tl=[lab2[i] for i in trn]; clf=st.fit(lab2)
        lp=st.line_logp(page,li,clf,trn,tl)
        gaps=boot.gaps_of(pcs); medw=boot.medw_of(page)
        for name,d2 in CONFIGS:
            kw=dict(widths=[p['w'] for p in pcs]) if name!='old' else {}
            if name!='old': d2new.MERGE_BASE,d2new.MERGE_G,d2new.SKIP_NARROW,d2new.SKIP_WIDE,d2new.MERGE_MAXGAP=PARAMS[name][:5]; kw.update(merge=PARAMS[name][5],skip=PARAMS[name][6])
            o,_=d2.decode_bigram(lp,gaps,medw,K=8,**kw)
            got={(i,j):w for i,j,w in o}
            ok=sum(1 for i,j,w in words if got.get((i,j))==w)
            res[name][0]+=ok; res[name][1]+=len(words)
            per.append((name,page,li,ok,len(words)))
        
print(res)
