import itertools, json, sys
sys.path.insert(0,'.')
from collections import Counter
C="YERSSTEMTOBTINGCKSUBVPASU"
def hits(p,c):
    cc=Counter(c[i:i+2] for i in range(len(c)-1)); h=0
    for i in range(len(p)-1):
        b=p[i:i+2]
        if cc[b]>0: cc[b]-=1; h+=1
    return h
res=[]
for ws in (["SUBVERTING","SYSTEM","BACKUPS","TO"],["SUBVERTING","SYSTEMS","BACKUP","TO"]):
    for perm in itertools.permutations(ws):
        p="".join(perm); assert sorted(p)==sorted(C)
        res.append((hits(p,C)," ".join(perm)))
res.sort(key=lambda r:-r[0])
for h,s in res: print(h,s)
json.dump(res,open('../data/orders.json','w'))
