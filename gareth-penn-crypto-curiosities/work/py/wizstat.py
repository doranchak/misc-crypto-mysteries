from collections import Counter
from puzzles import P
import random, string, itertools
random.seed(7)
def wizL(s):
    c=Counter(x for x in s.upper() if x.isalpha())
    for a in 'ABCDEFGHIJKLM':
        b=chr(155-ord(a)); k=min(c[a],c[b]); c[a]-=k; c[b]-=k
    return +c
# null 1: uniform random letters; null 2: shuffle-preserving? use English-ish? use uniform (conservative for rare-letter heavy strings)
NS=20000
cache={}
def pval(n,r):
    if n not in cache:
        cache[n]=sorted(sum(wizL(''.join(random.choice(string.ascii_uppercase) for _ in range(n))).values()) for _ in range(NS))
    arr=cache[n]; import bisect
    return bisect.bisect_right(arr,r)/NS, arr[NS//2]
rows=[]
for k,s in P.items():
    L=''.join(x for x in s.upper() if x.isalpha())
    if len(L)<12: continue
    r=sum(wizL(L).values()); p,med=pval(len(L),r)
    rows.append((p,k,len(L),r,med))
for p,k,n,r,med in sorted(rows):
    print(f'{k:22s} n={n:3d} residue={r:3d} null-median={med:3d} p={p:.4f}')
