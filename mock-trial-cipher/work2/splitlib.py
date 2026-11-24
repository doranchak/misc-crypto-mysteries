import sys, os, random, subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from walkmodels import *
def stream(chunks=None):
    chunks=chunks or CHUNKS
    flat=''.join(''.join(l) for l in chunks)
    al=sorted(set(flat)); ix={c:i for i,c in enumerate(al)}
    toks=[];ws=[]
    for l in chunks:
        for c in l:
            for j,ch in enumerate(c): toks.append(ix[ch]); ws.append(1 if j==0 else 0)
    return toks,ws,al,ix
def run_split(toks,ws,K,split,restarts,iters,seed,T0=4.0,T1=0.15,tag='sp'):
    p=f'{HERE}/tmp/{tag}_{os.getpid()}.txt'
    write_data(p,toks,[0]*len(toks),ws,K)
    env=dict(os.environ); env['SPLIT']=','.join(f'{c}:{k}' for c,k in split.items())
    out=subprocess.run([HERE+'/wsplit',p,str(restarts),str(iters),str(seed),str(T0),str(T1)],capture_output=True,text=True,env=env,cwd=HERE).stdout
    os.remove(p)
    res={}
    for line in out.splitlines():
        if line.startswith('SCORE'): res['score']=float(line.split()[1])
        elif line.startswith('LAB'): res['lab']=list(map(int,line.split()[1:]))
        elif line.startswith('L '): res['L']=line.split()[1:]
        elif line.startswith('T '): res['text']=line[2:]
    return res
