import sys, os, json, random
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from lib import *
from splitlib import run_split
from multiprocessing import Pool
os.environ['NN']='0'
def build(drop):
    lines=load_lines()
    chunks=[[ ''.join(ch for ch in c if ch not in drop) for c in l] for l in lines]
    chunks=[[c for c in l if c] for l in chunks]
    flat=''.join(''.join(l) for l in chunks); al=sorted(set(flat)); ix={c:i for i,c in enumerate(al)}
    toks=[];ws=[]
    for l in chunks:
        for c in l:
            for j,ch in enumerate(c): toks.append(ix[ch]); ws.append(1 if j==0 else 0)
    return chunks,toks,ws,al,ix
def solve(spec,drop,shuf=0,restarts=8,iters=2500000,seeds=12,procs=12):
    chunks,toks,ws,al,ix=build(drop); K=len(al)
    split={ix[s[0]]:int(s[1:]) for s in spec.split(',')} if spec!='none' else {}
    t=toks[:]
    if shuf: random.Random(shuf).shuffle(t)
    return chunks,al,ix,split,t,ws,K
def job(a):
    spec,drop,shuf,seed,restarts,iters=a
    chunks,al,ix,split,t,ws,K=solve(spec,drop,shuf)
    r=run_split(t,ws,K,split,restarts,iters,seed)
    r['cov']=coverage(r['text'])
    return r
if __name__=='__main__':
    spec=sys.argv[1]; drop=set(sys.argv[2]); 
    with Pool(12) as p: rs=p.map(job,[(spec,drop,0,s,8,2500000) for s in range(1,13)])
    rs.sort(key=lambda r:-r['score'])
    chunks,al,ix,split,t,ws,K=solve(spec,drop)
    print(spec,'drop',''.join(drop),[round(r['score'],1) for r in rs[:6]],rs[0]['cov'])
    best=rs[0]
    print(dict(zip(list(al)+['+']*(len(best['L'])-len(al)),best['L'])))
    json.dump(dict(best=best,al=al,split=spec,drop=''.join(drop)),open(f'r4_{spec.replace(",","")}_{"".join(sorted(drop))}.json','w'))
    words=best['text'].split(' '); k=0
    for l in chunks:
        n=len(l); print(' '.join(words[k:k+n])); k+=n
