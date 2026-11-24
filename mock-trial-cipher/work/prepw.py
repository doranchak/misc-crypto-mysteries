import sys
from collections import Counter
def words_from(path, merge=None, drop=()):
    ws=[]
    for l in open(path):
        w=[]
        for t in l.split():
            if t=='|':
                if w: ws.append(w); w=[]
            elif t in drop: continue
            else:
                w.append(merge.get(t,t) if merge else t)
        if w: ws.append(w)
    return ws
def write(ws,path):
    allc=Counter(t for w in ws for t in w)
    syms=sorted(allc,key=lambda s:-allc[s]); idx={s:i for i,s in enumerate(syms)}
    out=[]
    for w in ws:
        out+= [-1]+[idx[t] for t in w]
    out.append(-1)
    open(path,'w').write(' '.join(map(str,out))+'\n')
    return syms
if __name__=='__main__':
    ws=words_from('transcript_v1.txt',drop=('X','-','?','_'))
    s=write(ws,'cw_all.txt'); print(len(ws),s)
