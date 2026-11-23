import sys
from collections import Counter
def solve(letters_str, wordlist, maxw, minlen=3, short=(), limit=None):
    target=Counter(letters_str.lower())
    ks=sorted(target)
    idx={k:i for i,k in enumerate(ks)}
    SH=4  # 4 bits per letter; guard bit = 8
    G=sum(8<<(SH*i) for i in range(len(ks)))
    def enc(c): return sum(v<<(SH*idx[k]) for k,v in c.items())
    T=enc(target)
    W={}
    for w in set(wordlist):
        if not w.isalpha(): continue
        c=Counter(w)
        if c-target: continue
        if len(w)<minlen and w not in short: continue
        W[w]=enc(c)
    words=sorted(W)
    by_letter={k:[w for w in words if k in w] for k in ks}
    rank={k:len(by_letter[k]) for k in ks}
    res=set()
    def dfs(rem,cur):
        if rem==0:
            res.add(tuple(sorted(cur))); return
        if len(cur)>=maxw: return
        # rarest remaining letter
        best=None
        for k in ks:
            if (rem>>(SH*idx[k]))&7:
                if best is None or rank[k]<rank[best]: best=k
        for w in by_letter[best]:
            e=W[w]
            if ((rem|G)-e)&G==G:
                cur.append(w); dfs(rem-e,cur); cur.pop()
    dfs(T,[])
    return sorted(res), len(words)
if __name__=="__main__":
    L2="YERSSTEMTO BTING CKSUBVP ASU".replace(" ","")
    src=[w.strip().lower() for w in open('/Users/doranchak/projects/github/polyalphabetic/OxfordEnglishWords.txt')]
    extra="backups backup subverting system systems restoring restore rebooting".split()
    short=set("a i to of by in on at is it as be do go if me my no or so up us we an am he".split())
    for n in (int(sys.argv[1]),):
        r,nw=solve(L2,src+extra,n,3,short)
        print(n,nw,len(r),file=sys.stderr)
        for x in r: print(" ".join(x))
