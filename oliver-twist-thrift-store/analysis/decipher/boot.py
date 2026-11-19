import pickle, numpy as np, collections, json, os, math, sys
import decode as dc
LET=dc.LET; LI=dc.LI
d=pickle.load(open('D.pkl','rb')); D=d['D']; meta=d['meta']
A=pickle.load(open('allpieces.pkl','rb'))
B1=pickle.load(open('b1_labeled.pkl','rb'))
idx={(m[0],m[1],m[2]):i for i,m in enumerate(meta)}
def lines_of(page):
    return B1 if page=='b1' else A[page]['lines']
def medw_of(page): return 70.0 if page=='b1' else A[page]['medw']
def gaps_of(pcs): return [pcs[j+1]['x']-(pcs[j]['x']+pcs[j]['w']) for j in range(len(pcs)-1)]
VER='verified.json'
def load_ver(): return json.load(open(VER)) if os.path.exists(VER) else {}
def force_align(logP,text,skipP=4.0,skipL=7.0):
    # text may contain symbols in brackets like [TH] to force a digraph piece
    toks=[]; i=0
    while i<len(text):
        if text[i]=='[':
            j=text.index(']',i); toks.append(text[i+1:j]); i=j+1
        elif text[i].isalpha(): toks.append(text[i]); i+=1
        else: i+=1
    L=toks; m=logP.shape[0]; n=len(L)
    INF=1e9; dp=np.full((m+1,n+1),INF); bp={}; dp[0][0]=0
    for j in range(m+1):
        for i in range(n+1):
            c0=dp[j][i]
            if c0>=INF: continue
            if j<m:
                if c0+skipP<dp[j+1][i]: dp[j+1][i]=c0+skipP; bp[(j+1,i)]='sp'
                if i<n:
                    c=c0-logP[j,LI[L[i]]]-(0.0 if len(L[i])==1 else 0.0)
                    if c<dp[j+1][i+1]: dp[j+1][i+1]=c; bp[(j+1,i+1)]='m'
            if i<n and c0+skipL<dp[j][i+1]: dp[j][i+1]=c0+skipL; bp[(j,i+1)]='sl'
    res={}; j,i=m,n
    while (j,i)!=(0,0):
        op=bp[(j,i)]
        if op=='sp': j-=1
        elif op=='sl': i-=1
        else: res[j-1]=L[i-1]; j-=1; i-=1
    return res,dp[m][n]
def build_train(ver,exclude_page_line=None):
    lab={}
    for i,m in enumerate(meta):
        if m[0]=='b1' and m[3] and len(m[3])==1: lab[i]=m[3]
    # verified lines: forced alignment using current kNN from page-1 labels
    base=np.array(sorted(lab)); bl=[lab[i] for i in base]
    for page,ls in ver.items():
        for li,text in ls.items():
            li=int(li); pcs=lines_of(page)[li]
            logP=np.array([dc.knn_logp(D,idx[(page,li,j)],base,bl) for j in range(len(pcs))])
            res,c=force_align(logP,text)
            for j,ch in res.items(): lab[idx[(page,li,j)]]=ch
    if os.path.exists('explicit_labels.json'):
        for page,ls in json.load(open('explicit_labels.json')).items():
            for li,d in ls.items():
                for j,ch in d.items():
                    k=idx.get((page,int(li),int(j)))
                    if k is not None: lab[k]=ch
    # labels from fixed spans (only when letters == pieces)
    if os.path.exists('fixed_spans.json'):
        fs=json.load(open('fixed_spans.json'))
        for page,ls in fs.items():
            for li,spans in ls.items():
                li=int(li)
                for i,j,w in spans:
                    for v in dc.variants(w):
                        if len(v)==j-i:
                            for t in range(j-i):
                                k=idx.get((page,li,i+t))
                                if k is not None and k not in lab: lab[k]=dc.SYM[v[t]]
                            break
    return lab
def decode_page(page,ver,lines=None,tau=0.6,k=7):
    lab=build_train(ver)
    out={}
    for li,pcs in enumerate(lines_of(page)):
        if lines is not None and li not in lines: continue
        if len(pcs)<4: continue
        ti=np.array([i for i in lab if not (meta[i][0]==page and meta[i][1]==li)]); tl=[lab[i] for i in ti]
        logP=np.array([dc.knn_logp(D,idx[(page,li,j)],ti,tl,tau=tau,k=k) for j in range(len(pcs))])
        o,sc=dc.decode_line(logP,gaps_of(pcs),medw_of(page))
        out[li]=(' '.join(w for _,_,w in o),sc,o)
    return out
if __name__=='__main__':
    page=sys.argv[1]; ver=load_ver()
    res=decode_page(page,ver)
    for li,(t,sc,o) in res.items(): print(page,li,len(lines_of(page)[li]),round(sc,1),t)
