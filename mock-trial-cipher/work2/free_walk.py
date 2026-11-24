import sys, os, random, json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from walkmodels import *
from multiprocessing import Pool
import numpy as np
LAY={
 'polybius5x5_noJ':('ABCDEFGHIKLMNOPQRSTUVWXYZ',(5,5)),
 'polybius5x5_noQ':('ABCDEFGHIJKLMNOPRSTUVWXYZ',(5,5)),
 'alpha2x13':('ABCDEFGHIJKLMNOPQRSTUVWXYZ',(13,2)),
 'ring26':('ABCDEFGHIJKLMNOPQRSTUVWXYZ',(26,1)),
 'qwerty3x9':('QWERTYUIOASDFGHJKZXCVBNMPL',(9,3)),   # approximate keyboard rows 9/9/8 (26 letters padded)
 'rev_ring26':('ZYXWVUTSRQPONMLKJIHGFEDCBA',(26,1)),
}
flat=''.join(''.join(l) for l in CHUNKS); al=sorted(set(flat)); ix={c:i for i,c in enumerate(al)}
def stream_of(chunks):
    g=[];rs=[];ws=[]
    for l in chunks:
        for c in l:
            for j,ch in enumerate(c): g.append(ix[ch]); rs.append(1 if j==0 else 0); ws.append(1 if j==0 else 0)
    return g,rs,ws
def job(a):
    name,shuf=a
    letters,(w,h)=LAY[name]
    chunks=CHUNKS
    if shuf:
        rng=random.Random(shuf); f=list(flat); rng.shuffle(f); it=iter(f)
        chunks=[[''.join(next(it) for _ in c) for c in l] for l in CHUNKS]
    g,rs,ws=stream_of(chunks)
    tag=f'fw_{name}_{shuf}_{os.getpid()}'
    p=f'{HERE}/tmp/{tag}.txt'; write_data(p,g,rs,ws,len(al))
    M,D,home,S=torus_steps(w,h) if h>1 else cyclic_steps(w)
    sp=f'{HERE}/tmp/{tag}_s.txt'; write_steps(sp,M,D,home,S)
    lf=f'{HERE}/tmp/{tag}_l.txt'; open(lf,'w').write(' '.join(str(ord(c)-65) for c in letters[:M]))
    env=dict(os.environ); env['CD']='1'; env['LFIX']=lf; env['NOZERO']='1'
    out=subprocess.run([HERE+'/wsolve',p,sp,'1','3000','1',str(7+shuf)],capture_output=True,text=True,env=env,cwd=HERE).stdout
    for f in (p,sp,lf): os.remove(f)
    sc=float(out.split()[1]); txt=[l for l in out.splitlines() if l.startswith('T ')][0][2:]
    return name,shuf,sc,txt
if __name__=='__main__':
    tasks=[(n,s) for n in LAY for s in range(0,7)]
    with Pool(17) as p: res=p.map(job,tasks)
    for n in LAY:
        real=[r for r in res if r[0]==n and r[1]==0][0]
        nul=[r[2] for r in res if r[0]==n and r[1]>0]
        print(n,'real',round(real[2],1),'null',round(np.mean(nul),1),'sd',round(np.std(nul),1),'gap',round(real[2]-np.mean(nul),1))
        print('   ',real[3][:90])
