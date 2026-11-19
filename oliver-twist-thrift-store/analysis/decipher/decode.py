import pickle, numpy as np, collections, math
LET='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
SYM=list(LET)+['TH','AND','THE',"'",'WH','SH']      # 26,27,28,29 (29 = apostrophe: small raised loop), 30 = WH (W slash + H loop, one fused glyph), 31 = SH (S + H loop, one fused glyph)
LI={s:i for i,s in enumerate(SYM)}
NS=len(SYM)
vocab=pickle.load(open('vocab.pkl','rb'))
def variants(w):
    vs=[[LI[c] for c in w]]
    if w=='AND': vs.append([27])
    if w=='THE': vs.append([26,4]); vs.append([28])
    elif 'TH' in w:
        a=[]; i=0
        while i<len(w):
            if w[i:i+2]=='TH': a.append(26); i+=2
            else: a.append(LI[w[i]]); i+=1
        vs.append(a)
        if w.startswith('THE') and len(w)>3:
            vs.append([28]+[LI[c] for c in w[3:]])
    if 'WH' in w or 'SH' in w:
        a=[]; i=0
        while i<len(w):
            if w[i:i+2]=='WH': a.append(30); i+=2
            elif w[i:i+2]=='SH': a.append(31); i+=2
            elif w[i:i+2]=='TH': a.append(26); i+=2
            else: a.append(LI[w[i]]); i+=1
        vs.append(a)
    return vs
byl=collections.defaultdict(list)
for w,f in vocab.items():
    for v in variants(w): byl[len(v)].append((w,f,v))
WA={}
for L,lst in byl.items():
    WA[L]=(np.array([v for _,_,v in lst],dtype=np.int16),np.array([f for _,f,_ in lst],dtype=np.float32),[w for w,_,_ in lst])
PRIOR=np.zeros(NS)
PRIOR[:26]=np.log(np.array([8.2,1.5,2.8,4.3,12.7,2.2,2.0,6.1,7.0,0.15,0.8,4.0,2.4,6.7,7.5,1.9,0.1,6.0,6.3,9.1,2.8,1.0,2.4,0.15,2.0,0.07])/100)
PRIOR[26]=math.log(0.03); PRIOR[27]=math.log(0.025); PRIOR[28]=math.log(0.04); PRIOR[29]=math.log(0.012); PRIOR[30]=math.log(0.006); PRIOR[31]=math.log(0.008)
def knn_logp(D,i,train,labels,tau=0.6,k=7,mix=0.25):
    dd=D[i,train]
    nb=np.argsort(dd)[:k]; v=np.full(NS,1e-3)
    for j in nb: v[LI[labels[j]]]+=math.exp(-dd[j]/tau)
    v/=v.sum()
    pr=np.exp(PRIOR); pr/=pr.sum()
    p=(1-mix)*v+mix*pr
    return np.log(p)
def decode_line(logP,gaps,medw,alpha=1.0,beta=0.5,oov=-15.0,maxL=14):
    m=logP.shape[0]
    g=np.array(gaps)/medw if m>1 else np.array([])
    def bcost(k):
        gg=g[k-1]
        if gg>0.5: return 0.0,3.0
        if gg<0.15: return 4.0,0.0
        return 1.5,0.5
    NEG=-1e9
    dp=np.full(m+1,NEG); dp[0]=0.0; bp=[None]*(m+1)
    for i in range(m):
        if dp[i]<=NEG/2: continue
        base=dp[i]
        if i>0: base-=bcost(i)[0]
        for L in range(1,min(maxL,m-i)+1):
            j=i+L
            inner=sum(bcost(k)[1] for k in range(i+1,j))
            sl=logP[i:j]
            s=NEG; w=None
            if L in WA:
                idx,lf,ws=WA[L]
                sc=alpha*sl[np.arange(L)[None,:],idx].sum(1)+beta*lf
                b=int(np.argmax(sc)); s=float(sc[b]); w=ws[b]
            bl=sl[:,:26].argmax(1); so=alpha*sl[:,:26].max(1).sum()+oov-0.6*L
            if so>s and L>=3: s=so; w=''.join(LET[x] for x in bl).lower()
            if w is None: continue
            tot=base+s-inner
            if tot>dp[j]: dp[j]=tot; bp[j]=(i,w,s)
    out=[]; j=m
    while j>0:
        i,w,s=bp[j]; out.append((i,j,w)); j=i
    return out[::-1],dp[m]
