from grid import *
import itertools
words=set()
for fn in ['/usr/share/dict/words','/usr/share/dict/propernames']:
    for line in open(fn):
        w=line.strip()
        if len(w)>=4 and w.isalpha(): words.add(w.upper())
# all strings in grid lines in all 8 directions, then check substrings
lines=[]
for r in range(R):
    for c in range(C):
        for (dr,dc),name in DIRS.items():
            # only start of lines
            pr,pc=r-dr,c-dc
            if 0<=pr<R and 0<=pc<C: continue
            s='';cells=[]
            rr,cc=r,c
            while 0<=rr<R and 0<=cc<C:
                s+=GRID_ROWS[rr][cc];cells.append((rr,cc));rr+=dr;cc+=dc
            lines.append((s,cells,name))
found={}
for s,cells,name in lines:
    for i in range(len(s)):
        for j in range(i+4,len(s)+1):
            sub=s[i:j]
            if sub in words:
                found.setdefault(sub,[]).append((cells[i],name))
import collections
byl=collections.defaultdict(list)
for w in found: byl[len(w)].append(w)
for L in sorted(byl,reverse=True):
    print(L, ' '.join(sorted(byl[L])))
