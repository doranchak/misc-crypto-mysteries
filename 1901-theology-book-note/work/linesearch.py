import sys, collections, math, itertools
WL=sys.argv[1]; MINF=int(sys.argv[2]) if len(sys.argv)>2 else 30
words=[(l.split()[0].lower(),int(l.split()[1])) for l in open(WL,encoding='utf-8') if l.split()[0].isalpha()]
words=[(w,f) for w,f in words if f>=MINF]
def pattern(seq):
    m={};return tuple(m.setdefault(s,len(m)) for s in seq)
bp=collections.defaultdict(list)
for w,f in words: bp[pattern(w)].append((w,f))
def cons(gl,word,m,inv):
    m=dict(m);inv=dict(inv)
    for g,c in zip(gl,word):
        if g in m:
            if m[g]!=c: return None
        else:
            if c in inv: return None
            m[g]=c;inv[c]=g
    return m,inv
def solve(specs,keep=15):
    order=sorted(range(len(specs)),key=lambda i:len(bp[pattern(specs[i])]))
    best=[]
    def rec(k,m,inv,chosen,score):
        if k==len(order):
            best.append((score,[chosen[i] for i in range(len(specs))]))
            if len(best)>200000: raise StopIteration
            return
        i=order[k]
        for w,f in bp[pattern(specs[i])]:
            r=cons(specs[i],w,m,inv)
            if r: 
                c=dict(chosen);c[i]=w
                rec(k+1,r[0],r[1],c,score+math.log(f))
    try: rec(0,{},{},{},0.0)
    except StopIteration: pass
    best.sort(reverse=True)
    return len(best),best[:keep]
T_opts={'T8':'N V A S I B Y B','T9':'N V A S I B T Y B'}
W1_opts={'W1_8':'b r B I U Y D B','W1_7':'b r B I Y D B'}
W2_opts={'W2_8':'O G J H i L S i','W2_9':'O G d J H i L S i'}
W3='E S Z'; W4='L D'
W5_opts={'W5_3':'F J Z','W5_4':'F d J Z'}
for t,w1,w2,w5 in itertools.product(T_opts,W1_opts,W2_opts,W5_opts):
    if ('9' in w2)!=('4' in w5): continue   # dot treated consistently
    specs=[T_opts[t].split(),W1_opts[w1].split(),W2_opts[w2].split(),W3.split(),W4.split(),W5_opts[w5].split()]
    n,b=solve(specs,8)
    print(f'## {t} {w1} {w2} {w5}: {n} solutions')
    for s,ws in b: print(f'   {s:7.1f}  '+' | '.join(ws))
