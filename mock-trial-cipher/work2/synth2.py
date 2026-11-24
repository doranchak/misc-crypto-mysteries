import sys
sys.path.insert(0,'/Users/doranchak/projects/github/misc-crypto-mysteries/need-assistance-with-cipher/work2')
from synth import *
seed=int(sys.argv[1]); restarts=int(sys.argv[2]); useL=sys.argv[3]
d=HERE+'/tmp'
words,g,ws,rs,dd,cellof=synth_walk(seed)
write_data(f'{d}/s_walk{seed}.txt',g,rs,ws,24)
write_steps(f'{d}/s_t55.txt',*torus_steps(5,5))
env=dict(os.environ); env['CD']='1'
if useL=='true':
    lf=[0]*25
    for l,c in cellof.items(): lf[c]=ord(l)-65
    open(f'{d}/lfix.txt','w').write(' '.join(map(str,lf))); env['LFIX']=f'{d}/lfix.txt'
out=subprocess.run([HERE+'/wsolve',f'{d}/s_walk{seed}.txt',f'{d}/s_t55.txt','1',str(restarts),'1',str(seed)],capture_output=True,text=True,env=env,cwd=HERE).stdout
plain=' '.join(words); dec=[l for l in out.splitlines() if l.startswith('T ')][0][2:]
acc=sum(1 for a,b in zip(plain.replace(' ',''),dec.replace(' ','')) if a==b)/len(plain.replace(' ',''))
print(out.splitlines()[0], 'acc',round(acc,3)); print(plain[:100]); print(dec[:100])
