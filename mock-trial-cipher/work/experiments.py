"""Reproduces every number in the report. Needs ./hc, ./hc2 (compile hc.c/hc2.c), five.bin (make_ngram.py), corpus_clean.txt."""
import json, random, subprocess, statistics, sys
from collections import Counter
lines=[l.split() for l in open('transcript_v2.txt')]
drop=set('X - ? _'.split())
words=[]
for l in lines:
    w=[]
    for t in l:
        if t=='|':
            if w: words.append(w); w=[]
        elif t not in drop: w.append(t)
    if w: words.append(w)
flat=[t for w in words for t in w]
txt=open('corpus_clean.txt').read().split(); wcnt=Counter(txt)
vocab={w for w,c in wcnt.items() if c>=8 and len(w)>=4}
def coverage(s):
    n=len(s); best=[0]*(n+1)
    for i in range(1,n+1):
        best[i]=best[i-1]
        for L in range(4,13):
            if i-L>=0 and s[i-L:i] in vocab: best[i]=max(best[i],best[i-L]+L)
    return best[n]/n
def hc(seq,seed=1,restarts=40,iters=250000,fix=None,prog='./hc'):
    allc=Counter(seq); syms=sorted(allc,key=lambda s:-allc[s]); idx={s:i for i,s in enumerate(syms)}
    open('tmp_x.txt','w').write(' '.join(str(idx[t]) for t in seq))
    env=None
    if fix:
        import os; env=dict(os.environ,FIX=','.join(f'{idx[s]}:{L}' for s,L in fix.items()))
        prog='./hc2'
    out=subprocess.run([prog,'tmp_x.txt',str(restarts),str(iters),str(seed)],capture_output=True,text=True,env=env).stdout.split('\n')
    score=float(out[0].split()[1]); mp={}
    for p in out[1].split():
        i,L=p.split(':'); mp[syms[int(i)]]=L
    return score,mp,out[2]
R={}
sc,mp,pt=hc(flat,1,60); R['free']=dict(score=sc,coverage=coverage(pt),mapping=mp,plain=pt)
r25=[hc(flat,t+20,25)[0] for t in range(8)]
R['real_25restarts']=(statistics.mean(r25),statistics.pstdev(r25))
def nullstats(gen,n=8,restarts=25):
    s=[]
    for t in range(n):
        r=random.Random(t); seq=gen(r); s.append(hc(seq,t+3,restarts)[0])
    return statistics.mean(s),statistics.pstdev(s)
def gshuffle(r):
    f=flat[:]; r.shuffle(f); return f
R['null_glyph_shuffle']=nullstats(gshuffle)
R['null_chunk_shuffle']=nullstats(lambda r:[t for w in r.sample(words,len(words)) for t in w])
R['null_within_chunk_shuffle']=nullstats(lambda r:[t for w in words for t in r.sample(w,len(w))])
R['null_reverse_each_chunk']=nullstats(lambda r:[t for w in words for t in w[::-1]],n=3)
R['reversed_stream']=hc(flat[::-1],1,60)[0]
# shuffled coverage
cov=[]
for t in range(8):
    f=flat[:]; random.Random(t).shuffle(f); cov.append(coverage(hc(f,t+3,25)[2]))
R['null_coverage']=(statistics.mean(cov),statistics.pstdev(cov))
# cribs
sc,mp,pt=hc(flat,5,60,fix={'A':'T','U':'H','R':'E'}); R['crib_the']=dict(score=sc,coverage=coverage(pt),mapping=mp,plain=pt)
sc2,mp2,pt2=hc(flat,6,60,fix={'A':'A','U':'R','R':'E','V':'N','P':'D'}); R['crib_are_and']=dict(score=sc2,coverage=coverage(pt2),mapping=mp2)
# subsets
tri=set('APTQaptq')
subs={'arrows only':[t for t in flat if t not in tri],'triangles only':[t for t in flat if t in tri],
      'every 2nd glyph (phase 0)':[t for l in lines for t in [x for x in l if x not in drop and x!='|'][0::2]],
      'every 2nd glyph (phase 1)':[t for l in lines for t in [x for x in l if x not in drop and x!='|'][1::2]],
      'every 3rd glyph (phase 0)':[t for l in lines for t in [x for x in l if x not in drop and x!='|'][0::3]]}
R['subsets']={}
for k,s in subs.items():
    r=hc(s,1,40)[0]
    nn=[]
    for t in range(4):
        q=s[:]; random.Random(t).shuffle(q); nn.append(hc(q,t+2,25)[0])
    R['subsets'][k]=dict(n=len(s),score=r,null_mean=statistics.mean(nn),null_sd=statistics.pstdev(nn))
# simulation calibration
raw=open('corpus_clean.txt').read().replace(' ','')
R['sim']={}
for noise in (0.0,0.1,0.2,0.3):
    cs=[]
    for t in range(5):
        r=random.Random(100+t); st=r.randrange(0,len(raw)-600); pl=raw[st:st+543]
        perm=list(range(26)); r.shuffle(perm); sym=[perm[ord(c)-65] for c in pl]
        sym=[(r.randrange(26) if r.random()<noise else s) for s in sym]
        out=hc([str(s) for s in sym],t+1,40)[2]
        cs.append(coverage(out))
    R['sim'][str(noise)]=statistics.mean(cs)
json.dump(R,open('results.json','w'),indent=1)
for k,v in R.items():
    print(k, v if not isinstance(v,dict) or 'plain' not in v else {kk:vv for kk,vv in v.items() if kk!='plain'})
