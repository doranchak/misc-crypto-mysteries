"""(1) Permutation test: natural base-3 mapping vs random column->letter assignments (English word hits).
(2) Base-2 battery: every way of collapsing the 3 cell states to bits, many chunkings/bit orders.
Run: /opt/homebrew/bin/python3.11 -I scripts/significance_and_base2.py <corpus_dir>"""
import sys, os, re, collections, itertools, random, json, unicodedata, math
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE); sys.path.insert(0,HERE)
CORP=sys.argv[1]
W=json.load(open(os.path.join(ROOT,'figures','red_words.json')))
words=[[tuple(c) for c in w['cols']] for L in '1234' for w in W[L]]
def norm(t):
    t=unicodedata.normalize('NFD',t.lower()); t=''.join(c for c in t if unicodedata.category(c)!='Mn'); return re.sub('[^a-z ]',' ',t)
cnt=collections.Counter()
for f in ('en.txt','en_big.txt'):
    p=os.path.join(CORP,f)
    if os.path.exists(p): cnt.update(norm(open(p).read()).split())
TOP={w for w,_ in cnt.most_common(3000) if len(w)>=3}
def hits(strings):
    toks=[t for s in strings for t in s.split() if len(t)>=3]
    return sum(1 for t in toks if t in TOP), sum(len(t) for t in toks if t in TOP)
# natural mapping: value = top + 3*mid + 9*bottom, empty0 stroke1 square2, a=1..z=26, 0=space
def natural(ws,dmap=(0,2,1),bottom_msd=True):
    out=[]
    for w in ws:
        s=''
        for col in w:
            d=[dmap[x] for x in col]
            if bottom_msd: d=d[::-1]
            v=d[0]*9+d[1]*3+d[2]; s+=' ' if v==0 else (chr(96+v) if v<=26 else '?')
        out.append(s)
    return out
nat=natural(words,(0,2,1),True)   # digitmap: empty->0, square->2, stroke->1 ; bottom row = most significant
print('NATURAL base-3 mapping (stroke=1, square=2, bottom row most significant, a=1..z=26, 0=space)')
print('  word hits (>=3 letters, in 3000 most common corpus words): %d tokens / %d letters'%hits(nat))
# null: random bijections of the 27 column values -> letters (a..z + space)
rng=random.Random(11); vals=list(range(27)); null=[];nullL=[]
types=sorted({tuple(c) for w in words for c in w})
for _ in range(5000):
    p=vals[:]; rng.shuffle(p); m={}
    out=[]
    for w in words:
        s=''
        for col in w:
            v=sum(col[i]*3**(2-i) for i in range(3)); s+=' ' if p[v]==0 else chr(96+p[v]) if p[v]<=26 else '?'
        out.append(s)
    h=hits(out); null.append(h[0]); nullL.append(h[1])
null=np.array(null); nullL=np.array(nullL)
h=hits(nat)
print('  random bijections (n=5000): mean %.2f, sd %.2f, max %d; P(null >= observed) = %.4f'%(null.mean(),null.std(),null.max(),(null>=h[0]).mean()))
print('  letters in hit words: observed %d vs null mean %.1f, max %d'%(h[1],nullL.mean(),nullL.max()))
json.dump({'tokens':h[0],'letters':h[1],'null_mean':float(null.mean()),'null_sd':float(null.std()),'null_max':int(null.max()),'p':float((null>=h[0]).mean()),'null_letters_max':int(nullL.max())},open(os.path.join(ROOT,'figures','base3_significance.json'),'w'))
# ---------------- base-2 battery ------------------
big=np.ones((27,27)); 
txt=norm(open(os.path.join(CORP,'en.txt')).read())
for w in txt.split():
    s=' '+w+' '
    for a,b in zip(s,s[1:]): big[26 if a==' ' else ord(a)-97,26 if b==' ' else ord(b)-97]+=1
big=np.log(big/big.sum(1,keepdims=True))
def lm(s):
    t=0;n=0
    for a,b in zip(s,s[1:]):
        if not(a.isalpha() or a==' ') or not(b.isalpha() or b==' '): continue
        t+=big[26 if a==' ' else ord(a)-97,26 if b==' ' else ord(b)-97]; n+=1
    return t/max(1,n)
def stream(cells_by_word,rowmajor):
    bits=[]
    for w in cells_by_word:
        cols=w
        if rowmajor: seq=[cols[c][r] for r in range(3) for c in range(len(cols))]
        else: seq=[cols[c][r] for c in range(len(cols)) for r in range(3)]
        bits.append(seq)
    return bits
results=[]
states=[0,1,2]
for assign in itertools.product((0,1,None),repeat=3):   # what empty/square/stroke mean: 0, 1, or skipped
    vs=[a for a in assign if a is not None]
    if 0 not in vs or 1 not in vs: continue
    for rowmajor in (False,True):
        for per_word in (False,True):
            seqs=stream(words,rowmajor)
            def conv(seq):
                return [assign[x] for x in seq if assign[x] is not None]
            if per_word: units=[conv(s) for s in seqs]
            else: units=[sum((conv(s) for s in seqs),[])]
            for chunk in (5,6,7,8):
                for lsb in (False,True):
                    out=[]
                    for u in units:
                        s=''
                        for i in range(0,len(u)-chunk+1,chunk):
                            b=u[i:i+chunk]; v=int(''.join(map(str,b[::-1] if lsb else b)),2)
                            if chunk==5: s+=chr(96+v) if 1<=v<=26 else ' '
                            else:
                                ch=chr(v) if 32<=v<127 else '?'
                                s+=ch
                        out.append(s)
                    joined=' '.join(out)
                    if chunk==5: sc=lm(joined)
                    else: sc=sum(1 for c in joined if c.isalpha())/max(1,len(joined))   # fraction of decoded characters that are letters (spaces excluded)
                    results.append((sc,chunk,assign,'row' if rowmajor else 'col','per-word' if per_word else 'whole','lsb' if lsb else 'msb',joined[:60]))
five=[r for r in results if r[1]==5]; asc=[r for r in results if r[1]!=5]
five.sort(key=lambda r:-r[0]); asc.sort(key=lambda r:-r[0])
print('\nBASE-2 battery: %d variants'%len(results))
print(' best 5-bit (letter bigram log-lik; English text typically about -2.3, random about -3.3):')
for r in five[:3]: print('   %.2f'%r[0],r[2:6],repr(r[6]))
print(' best 6/7/8-bit (fraction of decoded chars that are letters; English ASCII text ~0.80, random bytes ~0.2):')
for r in asc[:3]: print('   %.2f'%r[0],r[1],r[2:6],repr(r[6]))
json.dump({'n_variants':len(results),'best5':[(r[0],r[1],r[2],r[3],r[4],r[5]) for r in five[:3]],'bestasc':[(r[0],r[1],r[2],r[3],r[4],r[5]) for r in asc[:3]]},open(os.path.join(ROOT,'figures','base2_battery.json'),'w'))
