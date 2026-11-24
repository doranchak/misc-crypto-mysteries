import sys, os, json, random
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from run4 import *
import numpy as np
DROP=set('d?-jE')
def j2(a):
    spec,shuf,seed=a
    chunks,al,ix,split,t,ws,K=solve(spec,DROP,shuf)
    r=run_split(t,ws,K,split,6,1500000,seed)
    c=coverage(r['text']); return spec,shuf,r['score'],c['vocab_letters'],c['long_hit']
if __name__=='__main__':
    specs=['none','R3','R3,A2','R3,A2,L2']
    jobs=[(s,sh,100+sh) for s in specs for sh in range(0,9)]
    with Pool(17) as p: res=p.map(j2,jobs)
    out={}
    for s in specs:
        real=[r for r in res if r[0]==s and r[1]==0][0]; nul=[r for r in res if r[0]==s and r[1]>0]
        sc=np.array([r[2] for r in nul]); vc=np.array([r[3] for r in nul]); lh=np.array([r[4] for r in nul])
        out[s]=dict(real_score=real[2],null_mean=sc.mean(),null_sd=sc.std(),real_vocab=real[3],null_vocab_mean=vc.mean(),null_vocab_max=vc.max(),real_longhit=real[4],null_longhit_mean=lh.mean(),null_longhit_max=lh.max())
        print(s,{k:round(float(v),3) for k,v in out[s].items()})
    json.dump(out,open('evidence.json','w'),indent=1)
