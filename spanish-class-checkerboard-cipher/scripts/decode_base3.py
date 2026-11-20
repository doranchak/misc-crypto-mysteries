"""Base-3 / base-2 decoding battery on the red ternary words (figures/red_words.json).
Corpus files (es.txt, en.txt: plain Wikipedia text) are read from the path given as argv[1].
Run: /opt/homebrew/bin/python3.11 -I scripts/decode_base3.py <corpus_dir>"""
import json, sys, os, re, math, itertools, collections, unicodedata, random
import numpy as np
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORP=sys.argv[1]
W=json.load(open(os.path.join(ROOT,'figures','red_words.json')))
words=[[tuple(c) for c in w['cols']] for L in '1234' for w in W[L]]
def norm(t):
    t=unicodedata.normalize('NFD',t.lower()); t=''.join(c for c in t if unicodedata.category(c)!='Mn')
    return re.sub('[^a-z ]',' ',t)
LM={}
for lang in ('es','en'):
    txt=norm(open(os.path.join(CORP,lang+'.txt')).read())
    ws=[w for w in txt.split() if w]
    big=np.ones((27,27)); 
    idx=lambda ch:26 if ch==' ' else ord(ch)-97
    for w in ws:
        s=' '+w+' '
        for a,b in zip(s,s[1:]): big[idx(a),idx(b)]+=1
    big=np.log(big/big.sum(1,keepdims=True))
    LM[lang]=(big,collections.Counter(ws))
def score_words(ws_letters,lang):
    big=LM[lang][0]; tot=0; n=0
    for w in ws_letters:
        s=' '+w+' '
        for a,b in zip(s,s[1:]):
            tot+=big[26 if a==' ' else ord(a)-97, 26 if b==' ' else ord(b)-97]; n+=1
    return tot/max(1,n)
def word_hits(ws_letters,lang,minlen=2):
    c=LM[lang][1]; top={w for w,_ in c.most_common(2000)}
    return sum(1 for w in ws_letters if len(w)>=minlen and w in top)
# ---------- natural base-3 readings -------------
ES27='abcdefghijklmnnopqrstuvwxyz'  # n-tilde collapsed to n
alphabets={'A=0..Z=25,26=space':lambda v:' ' if v==26 else chr(97+v) if v<26 else '?',
           '0=space,A=1..Z=26':lambda v:' ' if v==0 else chr(96+v),
           'Spanish27 a..n,ñ,o..z (0-based)':lambda v:ES27[v],
           'Spanish27 with 0=space (ñ dropped)':lambda v:' ' if v==0 else (ES27[v-1] if v<=26 else '?')}
def decode(digit_map,top_msd,alpha):
    out=[]
    for w in words:
        s=''
        for col in w:
            d=[digit_map[x] for x in col]
            if not top_msd: d=d[::-1]
            v=d[0]*9+d[1]*3+d[2]
            s+=alpha(v)
        out.append(s)
    return out
rng=random.Random(5)
rows=[]
for perm in itertools.permutations(range(3)):
    for top_msd in (True,False):
        for an,af in alphabets.items():
            dec=decode(perm,top_msd,af)
            letters=[w.replace(' ','') for w in dec]
            sc={l:score_words([w for w in letters if w],l) for l in ('es','en')}
            rows.append((perm,top_msd,an,sc,dec))
# null: random permutations of the 27 column values
def null_scores(lang,n=400):
    vals=list(range(27)); res=[]
    for _ in range(n):
        p=vals[:]; rng.shuffle(p)
        m={}
        out=[]
        for w in words:
            s=''
            for col in w:
                v=sum(x*3**(2-i) for i,x in enumerate(col)); 
                if v not in m: m[v]=p[v]
                s+=chr(97+(m[v]%26))
            out.append(s)
        res.append(score_words(out,lang))
    return np.array(res)
nul={l:null_scores(l) for l in ('es','en')}
print('null mean/sd (random mapping): es',round(nul['es'].mean(),3),round(nul['es'].std(),3),' en',round(nul['en'].mean(),3),round(nul['en'].std(),3))
best=[]
for perm,top,an,sc,dec in rows:
    z={l:(sc[l]-nul[l].mean())/nul[l].std() for l in sc}
    best.append((max(z.values()),perm,top,an,z,dec))
best.sort(key=lambda r:-r[0])
print('\nNATURAL base-3 readings, ranked by best language z-score (out of',len(best),'):')
for b in best[:6]:
    print(round(b[0],2),'digitmap(empty,square,stroke)->',b[1],'top is MSD' if b[2] else 'bottom is MSD',b[3],{k:round(v,2) for k,v in b[4].items()})
    print('    ',' '.join(b[5][:14]))
json.dump([(float(b[0]),list(b[1]),b[2],b[3],b[5]) for b in best[:10]],open(os.path.join(ROOT,'figures','base3_natural_top.json'),'w'))
# ---------- substitution hill-climb (column type -> letter) -------------
types=sorted({c for w in words for c in w}); tix={t:i for i,t in enumerate(types)}
seqs=[[tix[c] for c in w] for w in words]
def hillclimb(seqs,lang,iters=4000,restarts=6,seed=0):
    r=random.Random(seed); big=LM[lang][0]; best_all=(-1e9,None)
    nt=len(types)
    for _ in range(restarts):
        m=[r.randrange(26) for _ in range(nt)]
        def sc(m):
            tot=0;n=0
            for w in seqs:
                s=[26]+[m[x] for x in w]+[26]
                for a,b in zip(s,s[1:]): tot+=big[a,b]; n+=1
            return tot/n
        cur=sc(m)
        for _ in range(iters):
            i=r.randrange(nt); old=m[i]; m[i]=r.randrange(26); new=sc(m)
            if new>=cur: cur=new
            else: m[i]=old
        if cur>best_all[0]: best_all=(cur,m[:])
    return best_all
res={}
for lang in ('es','en'):
    sc,m=hillclimb(seqs,lang)
    ctrl=[]
    flat=[x for s in seqs for x in s]
    for k in range(12):
        r=random.Random(100+k); f=flat[:]; r.shuffle(f); it=iter(f)
        sh=[[next(it) for _ in s] for s in seqs]
        ctrl.append(hillclimb(sh,lang,iters=4000,restarts=3,seed=k)[0])
    res[lang]=(sc,m,ctrl)
    dec=[''.join(chr(97+m[x]) for x in s) for s in seqs]
    print(f'\nSUBSTITUTION ({lang}): best score {sc:.3f}; shuffled-control best scores mean {np.mean(ctrl):.3f} sd {np.std(ctrl):.3f}  z={(sc-np.mean(ctrl))/np.std(ctrl):.2f}')
    print('   ',' '.join(dec[:18]))
json.dump({l:{'score':v[0],'control_mean':float(np.mean(v[2])),'control_sd':float(np.std(v[2]))} for l,v in res.items()},open(os.path.join(ROOT,'figures','base3_subst.json'),'w'))
