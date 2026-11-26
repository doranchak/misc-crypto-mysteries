import sys
from grid import *
words=set()
for line in open('/usr/share/dict/words'):
    w=line.strip()
    if len(w)>=4 and w.isalpha(): words.add(w.upper())
hits=[]
for w in words:
    f=find_all(w)
    for h in f: hits.append((len(w),w,h))
hits.sort(reverse=True)
for L,w,h in hits:
    if L>=5: print(L,w,h)
