import sys, os, json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from splitlib import *
from multiprocessing import Pool
os.environ['NN']='0'
chunks=[[ ''.join(ch for ch in c if ch!='d') for c in l] for l in CHUNKS]
chunks=[[c for c in l if c] for l in chunks]
toks,ws,al,ix=stream(chunks); K=len(al); R=ix['R']
def job(a):
    split,seed=a
    r=run_split(toks,ws,K,split,8,2000000,seed)
    return (split,r['score'],r['text'])
if __name__=='__main__':
    jobs=[({R:3},1),({R:2},1),({},1),({R:4},1)]
    for c in al:
        if c!='R': jobs.append(({R:3,ix[c]:2},1))
    with Pool(17) as p: res=p.map(job,jobs)
    inv={v:k for k,v in ix.items()}
    res.sort(key=lambda r:-r[1])
    for split,sc,t in res: print(round(sc,1),{inv[k]:v for k,v in split.items()},coverage(t)['vocab_letters'].__round__(3))
