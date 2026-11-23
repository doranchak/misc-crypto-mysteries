"""Minimum common string partition (MCSP): fewest chunks such that the plain, cut into that many pieces,
can be re-ordered to give the cipher. Exact search (iterative deepening + memo). Case-insensitive, spaces removed."""
import sys, json
sys.setrecursionlimit(10000)
LINES = {
 "line1": ("UFDAILD TOSER ATAAE LOD", "FAILED TO LOAD USER DATA"),
 "line2": ("YERSSTEMTO BTING CKSUBVP ASU", "SUBVERTING SYSTEM BACKUPS TO"),
 "line3": ("cesriPosng", "Processing"),
}
def mcsp(plain, cipher):
    n=len(plain)
    for K in range(1,n+1):
        memo=set()
        sol=[]
        def go(pos,mask,left):
            if pos==n: return True
            if left==0: return False
            key=(pos,mask,left)
            if key in memo: return False
            # remaining letters must fit: need at least ceil(rem/max_len) chunks, skip
            for L in range(n-pos,0,-1):
                seg=cipher[pos:pos+L]
                for s in range(0,n-L+1):
                    if plain[s:s+L]==seg:
                        m=((1<<L)-1)<<s
                        if mask&m: continue
                        sol.append((pos,s,L))
                        if go(pos+L,mask|m,left-1): return True
                        sol.pop()
            memo.add(key); return False
        if go(0,0,K): return K,list(sol)
res={}
for name,(cipher,plain) in LINES.items():
    c=cipher.replace(" ","").upper(); p=plain.replace(" ","").upper()
    K,sol=mcsp(p,c)
    # verify
    rebuilt_c="".join(p[s:s+L] for (pos,s,L) in sol)
    used=sorted((s,L) for (pos,s,L) in sol)
    cov="".join(p[s:s+L] for s,L in used)
    assert rebuilt_c==c and cov==p, name
    res[name]=dict(K=K,tiles=sol,n=len(p))
    print(name,"n=",len(p),"min chunks=",K, [p[s:s+L] for (pos,s,L) in sol])
json.dump(res,open('../data/tiling.json','w'),indent=1)
