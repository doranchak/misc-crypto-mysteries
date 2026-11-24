import sys, random
from collections import Counter
def load(path='transcript_v1.txt'):
    return [l.split() for l in open(path)]
def stream(lines, drop=(), merge=None):
    out=[]
    for l in lines:
        for t in l:
            if t=='|' or t in drop: continue
            if merge and t in merge: t=merge[t]
            out.append(t)
    return out
def write(seq,path):
    syms=sorted(set(seq),key=lambda s:-Counter(seq)[s])
    idx={s:i for i,s in enumerate(syms)}
    open(path,'w').write(' '.join(str(idx[s]) for s in seq)+'\n')
    return syms
if __name__=='__main__':
    lines=load()
    name=sys.argv[1]
    if name=='all': seq=stream(lines)
    elif name=='noR': seq=stream(lines,drop=('R',))
    elif name=='noRX': seq=stream(lines,drop=('R','X','-','?','_'))
    s=write(seq,f'cipher_{name}.txt'); print(name,len(seq),len(s),s)
