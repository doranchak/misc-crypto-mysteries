import sys
W=[]
for line in open('/Users/doranchak/projects/github/misc-crypto-mysteries/skydrop-scroll-puzzle/data/words60k.txt'):
    w,c=line.split(); W.append((w,int(c)))
def pat(s):
    m={};out=[]
    for ch in s:
        if ch not in m: m[ch]=len(m)
        out.append(m[ch])
    return tuple(out)
for cw in sys.argv[1:]:
    p=pat(cw)
    hits=[(w,c) for w,c in W if len(w)==len(cw) and pat(w)==p]
    print(cw,len(hits),' '.join(w for w,c in hits[:40]))
