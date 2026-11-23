"""Score every <=4-word dictionary split of line 2 by how many adjacent letter pairs of the (space-stripped) split survive in the cipher."""
import statistics
import json
from collections import Counter
C="YERSSTEMTOBTINGCKSUBVPASU"
def hits(p,c):
    cc=Counter(c[i:i+2] for i in range(len(c)-1)); h=0
    for i in range(len(p)-1):
        b=p[i:i+2]
        if cc[b]>0: cc[b]-=1; h+=1
    return h
rows=[]
for l in open('../data/line2_dictionary_splits_oxford.txt'):
    ws=l.split()
    if not ws: continue
    p="".join(ws).upper()
    assert sorted(p)==sorted(C)
    rows.append((hits(p,C),ws))
rows.sort(key=lambda r:(-r[0],r[1]))
n=len(rows)
top=[r for r in rows if r[0]>=max(h for h,_ in rows)-1]
print(n,"splits;","max",rows[0][0],"median",statistics.median(h for h,_ in rows))
print("splits within 1 of max:",len(top),"; containing 'subverting':",sum('subverting' in ws for h,ws in top))
top20=rows[:20]
print("top 20 containing subverting:",sum('subverting' in ws for h,ws in top20))
print("overall splits containing subverting:",sum('subverting' in ws for h,ws in rows),"of",n)
json.dump(dict(n=n,max=rows[0][0],median=statistics.median(h for h,_ in rows),
  top_within1=len(top),top_within1_sub=sum('subverting' in ws for h,ws in top),
  top20_sub=sum('subverting' in ws for h,ws in top20),all_sub=sum('subverting' in ws for h,ws in rows),
  examples=[" ".join(ws)+f" ({h})" for h,ws in rows[:8]]),open('../data/rank_by_chunks.json','w'),indent=1)
for h,ws in rows[:12]: print(h," ".join(ws))
