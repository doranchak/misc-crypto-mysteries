import sys
from collections import Counter
W=[]
for i,line in enumerate(open('/Users/doranchak/projects/github/misc-crypto-mysteries/skydrop-scroll-puzzle/data/words60k.txt')):
    w=line.split()[0]
    if w.isalpha() and (len(w)>2 or w in('A','I','OF','TO','IN','ON','AT','BY','OR','DO','GO','NO','SO','UP','US','WE','ME','MY','IT','IS','AN','AS','BE','HE','OH','OX')): W.append((w.upper(),i))
    if i>40000: break
def ana(target,maxw=3,minlen=2,limit=60):
    T=Counter(target.upper().replace(' ',''))
    cand=[(w,i,Counter(w)) for w,i in W if not (Counter(w)-T)]
    out=[]
    def rec(rem,start,acc,score):
        if not +rem: out.append((score,' '.join(acc))); return
        if len(acc)>=maxw: return
        for j in range(start,len(cand)):
            w,i,c=cand[j]
            if not (c-rem): rec(rem-c,j,acc+[w],score+i)
    rec(T,0,[],0)
    out.sort()
    return out[:limit]
for t in sys.argv[1:]:
    print('==',t)
    for s,a in ana(t): print('  ',a)
