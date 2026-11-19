import pickle, collections, re, math, sys, unicodedata
words,meta=pickle.load(open('seg/words_cl2.pkl','rb'))
fam={14:'phi',26:'phi',29:'dot',34:'dot',18:'dot',32:'F',31:'3',25:'Zb',22:'Zd',24:'pr',5:'pr',9:'+',1:'V',10:'/.',16:'WS',11:'WS',35:'h7',13:'h7',21:'h7',12:'h7',30:'M7',17:'M7',33:'Yb',27:'Yl',28:'cb',20:'Rn',8:'Rn',3:'/',4:'/'}
W=[[fam.get(c,'c%d'%c) for c in w] for w in words]
# dictionary
freq=collections.Counter()
for f in ('lm/ot.txt','lm/en2.txt'):
    t=open(f,encoding='utf-8',errors='ignore').read().lower()
    for w in re.findall(r"[a-z]+",t): freq[w]+=1
bylen=collections.defaultdict(list)
for w,c in freq.items(): bylen[len(w)].append((w,c))
def match_total(w,M):
    # w: families; M: family->letter ; returns total freq of dict words consistent (repeated unknown fams equal letters; distinct fams distinct letters)
    tot=0
    for dw,c in bylen[len(w)]:
        asg=dict(M); used=set(M.values()); ok=True
        for f,ch in zip(w,dw):
            if f in asg:
                if asg[f]!=ch: ok=False;break
            else:
                if ch in used: ok=False;break
                asg[f]=ch; used.add(ch)
        if ok: tot+=c
    return tot
def rank(M, unknown=None):
    fams=sorted({f for w in W for f in w})
    unknown=[f for f in fams if f not in M]
    out={}
    for f in unknown:
        ws=[w for w in W if f in w and len(w)>=2]
        sc={}
        for L in 'abcdefghijklmnopqrstuvwxyz':
            if L in M.values(): continue
            M2=dict(M); M2[f]=L
            s=0
            for w in ws:
                base=match_total(w,M)+1
                s+=math.log((match_total(w,M2)+1)/base)
            sc[L]=s
        top=sorted(sc.items(),key=lambda t:-t[1])[:4]
        out[f]=(len(ws),top)
    return out
if __name__=='__main__':
    M={}
    for a in sys.argv[1:]:
        f,l=a.split('='); M[f]=l
    for f,(n,top) in sorted(rank(M).items(), key=lambda t:-t[1][0]): print(f,n,[(l,round(s,1)) for l,s in top])
