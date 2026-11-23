import sys, math
sys.path.insert(0,'.')
from anagram_fast import solve
F='/Users/doranchak/projects/github/zkc-server/data/english_words__practicalcryptography.txt'
N=int(sys.argv[2]); maxw=int(sys.argv[1])
freq={}; tot=0
for i,l in enumerate(open(F)):
    w,c=l.split(); c=int(c); freq[w.lower()]=c; tot+=c
    if i>=N: break
bad=set("egypt vietnam gov turkey kgb gms pvc tubing gibson yts uvpc".split())
words=[w for w in freq if w not in bad and (len(w)>=3 or w in ("to","of","by","in","on","at","is","it","as","be","do","go","if","me","my","no","or","so","up","us","we","an","am","he","a","i"))]
r,nw=solve("YERSSTEMTO BTING CKSUBVP ASU".replace(" ",""),words,maxw,1,set(["a","i","to","of","by","in","on","at","is","it","as","be","do","go","if","me","my","no","or","so","up","us","we","an","am","he"]))
print(nw,"words",len(r),"solutions",file=sys.stderr)
def score(s): return sum(math.log(freq[w]/tot) for w in s)
r.sort(key=score,reverse=True)
import json
json.dump([(round(score(s),2),list(s)) for s in r],open(f'../data/rank_{maxw}_{N}.json','w'))
for s in r[:40]: print(round(score(s),1)," ".join(s))
print('--- with system/backup')
for s in r:
    if any(w in s for w in ("system","systems","backup","backups")): print(round(score(s),1)," ".join(s))
