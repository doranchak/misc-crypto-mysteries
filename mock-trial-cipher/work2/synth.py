import sys, random
sys.path.insert(0,'/Users/doranchak/projects/github/misc-crypto-mysteries/need-assistance-with-cipher/work2')
from lib import *
base='/Users/doranchak/projects/github/misc-crypto-mysteries/'
CORP=open(base+'need-assistance-with-cipher/work/corpus_clean.txt').read().split()
LET='ABCDEFGHIKLMNOPRSTUVWXY'  # 23 letters + Z,Q merged below
def norm(w): return w.replace('J','I').replace('Q','K').replace('Z','S')
def synth_mono(seed,nwords=139,K=24):
    rnd=random.Random(seed); s=rnd.randrange(0,len(CORP)-nwords)
    words=[norm(w) for w in CORP[s:s+nwords]]
    letters=sorted(set(''.join(words))); 
    cls=list(range(K)); rnd.shuffle(cls)
    m={l:cls[i] for i,l in enumerate(letters)}
    g=[m[c] for w in words for c in w]
    ws=[1 if j==0 else 0 for w in words for j in range(len(w))]
    return words,g,ws
def synth_walk(seed,a=5,b=5,nwords=139,K=24,reset='word'):
    rnd=random.Random(seed)
    M=a*b
    letters='ABCDEFGHIKLMNOPQRSTUVWXYZ'  # 25 letters (J->I)
    cells=list(range(M)); rnd.shuffle(cells)
    cellof={l:cells[i] for i,l in enumerate(letters)}
    M_,D,home,S=torus_steps(a,b)
    # glyph class -> displacement (injective into M displacements)
    disps=list(range(M)); rnd.shuffle(disps)
    dd=disps[:K]; inv={d:i for i,d in enumerate(dd)}
    words=[];g=[];ws=[];rs=[]
    s=rnd.randrange(0,len(CORP)-3*nwords)
    i=s
    while len(words)<nwords:
        w=CORP[i].replace('J','I'); i+=1
        cur=home; seq=[]; ok=True
        for c in w:
            t=cellof[c]
            # need displacement d with S[cur][d]==t
            d=[x for x in range(D) if S[cur][x]==t][0]
            if d not in inv: ok=False;break
            seq.append(inv[d]); cur=t
        if not ok: continue
        words.append(w)
        for j,x in enumerate(seq): g.append(x); ws.append(1 if j==0 else 0); rs.append(1 if j==0 else 0)
    return words,g,ws,rs,dd,cellof
if __name__=='__main__':
    which=sys.argv[1]; seed=int(sys.argv[2]); restarts=int(sys.argv[3]); iters=int(sys.argv[4])
    d='/Users/doranchak/projects/github/misc-crypto-mysteries/need-assistance-with-cipher/work2/tmp'
    os.makedirs(d,exist_ok=True)
    if which=='mono':
        words,g,ws=synth_mono(seed)
        write_data(f'{d}/s_mono{seed}.txt',g,[0]*len(g),ws,24)
        write_steps(f'{d}/s_ident.txt',24,24,0,[[0]*24 for _ in range(24)])
        r=run(f'{d}/s_mono{seed}.txt',f'{d}/s_ident.txt',0,restarts,iters,seed)
    else:
        words,g,ws,rs,dd,cellof=synth_walk(seed)
        write_data(f'{d}/s_walk{seed}.txt',g,rs,ws,24)
        write_steps(f'{d}/s_t55.txt',*torus_steps(5,5))
        r=run(f'{d}/s_walk{seed}.txt',f'{d}/s_t55.txt',1,restarts,iters,seed)
    plain=' '.join(words)
    dec=r['text']
    acc=sum(1 for a,b in zip(plain.replace(' ',''),dec.replace(' ','')) if a==b)/len(plain.replace(' ',''))
    print(which,seed,'score',r['score'],'letters',len(plain.replace(' ','')),'acc',round(acc,3))
    print('P:',plain[:120]); print('D:',dec[:120])
