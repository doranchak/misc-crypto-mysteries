"""Does the scramble preserve local structure (chunk-shuffle) or is it a uniform random permutation?
For each line: plain candidate vs cipher. Statistic = number of adjacent plain letter-pairs (bigrams of the
space-stripped plain) whose same two letters also appear adjacent, in the same order, in the space-stripped cipher
(using multiset counts, so each cipher bigram occurrence can be used once). Compared against uniformly random permutations.
Also: minimum number of chunks (min common string partition, exact via DP search for these sizes)."""
import random, json, sys
from collections import Counter
random.seed(12345)
LINES = {
 "line1": ("UFDAILD TOSER ATAAE LOD", "FAILED TO LOAD USER DATA"),
 "line2": ("YERSSTEMTO BTING CKSUBVP ASU", "SUBVERTING SYSTEM BACKUPS TO"),
 "line3": ("cesriPosng", "Processing"),
}
def strip(s): return s.replace(" ","").upper()
def bigram_hits(plain, cipher):
    c = Counter(cipher[i:i+2] for i in range(len(cipher)-1))
    hits = 0
    for i in range(len(plain)-1):
        b = plain[i:i+2]
        if c[b] > 0:
            c[b] -= 1; hits += 1
    return hits
def min_chunks(plain, cipher):
    """Minimum common string partition: split plain into k substrings that can be rearranged into cipher."""
    n=len(plain); best=[n]
    from functools import lru_cache
    # DFS over cipher positions: choose chunk from plain to place next; use bitmask of used plain positions
    # Simplification: partition plain into chunks (cuts), then check multiset equality of chunks with a greedy tiling of cipher via DFS.
    def tile(chunks):
        # can chunks be concatenated in some order to give cipher?
        cnt=Counter(chunks)
        memo={}
        def go(pos,key):
            if pos==len(cipher): return True
            if (pos,key) in memo: return memo[(pos,key)]
            ok=False
            for ch in set(cnt_from_key(key)):
                if cipher.startswith(ch,pos):
                    k2=remove(key,ch)
                    if go(pos+len(ch),k2): ok=True;break
            memo[(pos,key)]=ok; return ok
        def cnt_from_key(key): return [c for c,v in key if v>0]
        def remove(key,ch): return tuple((c,v-1 if c==ch else v) for c,v in key)
        return go(0,tuple(sorted(cnt.items())))
    for k in range(1,n+1):
        # enumerate cut sets of size k-1
        from itertools import combinations
        for cuts in combinations(range(1,n),k-1):
            pts=(0,)+cuts+(n,)
            chunks=[plain[pts[i]:pts[i+1]] for i in range(k)]
            if tile(chunks): return k,chunks
    return n,list(plain)
out={}
for name,(cipher,plain) in LINES.items():
    c=strip(cipher); p=strip(plain)
    assert sorted(c)==sorted(p), name
    obs=bigram_hits(p,c)
    rnd=[]
    letters=list(p)
    for _ in range(20000):
        random.shuffle(letters)
        rnd.append(bigram_hits(p,"".join(letters)))
    mean=sum(rnd)/len(rnd)
    pval=sum(1 for r in rnd if r>=obs)/len(rnd)
    k=None
    if len(p)<=20:
        pass
    out[name]=dict(plain=plain,cipher=cipher,n=len(p),bigram_hits=obs,random_mean=round(mean,2),p_ge=pval)
    print(name,out[name])
json.dump(out,open('../data/chunk_stats.json','w'),indent=1)
