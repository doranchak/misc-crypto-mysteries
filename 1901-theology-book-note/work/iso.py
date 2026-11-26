import sys,collections
WL=sys.argv[1]
words=[(l.split()[0].lower(),int(l.split()[1])) for l in open(WL,encoding='utf-8') if l.split()[0].isalpha()]
def pattern(seq):
    m={};return tuple(m.setdefault(s,len(m)) for s in seq)
bp=collections.defaultdict(list)
for w,f in words: bp[pattern(w)].append((w,f))
def cons(gl,word,m):
    m=dict(m);inv={v:k for k,v in m.items()}
    for g,c in zip(gl,word):
        if g in m and m[g]!=c: return None
        if c in inv and inv[c]!=g: return None
        m[g]=c;inv[c]=g
    return m
def joint(specs,topn=30,minf=20):
    # specs: list of glyph lists; returns consistent combos ranked by min freq
    res=[]
    def rec(i,m,chosen,fmin):
        if i==len(specs):
            res.append((fmin,chosen));return
        for w,f in bp[pattern(specs[i])]:
            if f<minf: break
            m2=cons(specs[i],w,m)
            if m2 is not None: rec(i+1,m2,chosen+[w],min(fmin,f))
    rec(0,{},[],10**12)
    res.sort(reverse=True)
    return res[:topn]
