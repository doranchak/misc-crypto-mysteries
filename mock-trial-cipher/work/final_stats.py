import json, math, subprocess, random, statistics
from collections import Counter
lines=[l.split() for l in open('transcript_v2.txt')]
drop=set('X - ? _'.split())
glyph=[[t for t in l if t not in ('|',)+tuple(drop)] for l in lines]
flat=[t for l in glyph for t in l]
N=len(flat); c=Counter(flat)
ic=sum(v*(v-1) for v in c.values())/(N*(N-1))
H=-sum(v/N*math.log2(v/N) for v in c.values())
print('N',N,'classes',len(c),'IC',round(ic,4),'entropy',round(H,3))
# words
words=[]
for l in lines:
    w=[]
    for t in l:
        if t=='|':
            if w: words.append(w); w=[]
        elif t not in drop: w.append(t)
    if w: words.append(w)
wl=Counter(len(w) for w in words); print('words',len(words),sorted(wl.items()))
wc=Counter(''.join(w) for w in words); print(wc.most_common(12))
bg=Counter()
for w in words:
    for a,b in zip(w,w[1:]): bg[a+b]+=1
print(bg.most_common(15))
# english word length distribution from corpus
txt=open('corpus_clean.txt').read().split(); el=Counter(min(len(w),12) for w in txt); tot=sum(el.values())
print('english',[(k,round(100*v/tot,1)) for k,v in sorted(el.items())])
json.dump(dict(N=N,classes=len(c),IC=ic,H=H,freq=c.most_common(),wordlen=sorted(wl.items()),words=len(words),topwords=wc.most_common(12),topbigrams=bg.most_common(15)),open('stats.json','w'))
