import sys, math
sys.path.insert(0,'.')
from anagram_fast import solve
F='/Users/doranchak/projects/github/zkc-server/data/english_words__practicalcryptography.txt'
freq={};tot=0
for i,l in enumerate(open(F)):
    w,c=l.split(); c=int(c); freq[w.lower()]=c; tot+=c
    if i>=30000: break
short={"a","i","to","of","by","in","on","at","is","it","as","be","do","go","if","me","my","no","or","so","up","us","we","an","am","he"}
bad=set("gov kgb gms pvc pto tup ebay bupa abs ambs".split())
words=[w for w in freq if w not in bad and (len(w)>=3 or w in short)]
R="SYSTEMBACKUPSTO"
out=[]
for n in (2,3,4):
    r,nw=solve(R,words,n,1,short)
    out+=r
import json
def score(s): return sum(math.log(freq[w]/tot) for w in s)
out=sorted(set(out),key=score,reverse=True)
print(len(out),"splits of the 15-letter remainder")
for s in out[:45]: print(round(score(s),1)," ".join(s))
print("... natural-looking containing system/backup:")
for s in out:
    if any(w.startswith(("system","backup")) for w in s): print(round(score(s),1)," ".join(s))
