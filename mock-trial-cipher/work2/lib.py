import json, subprocess, os, random, re, collections, tempfile, sys
HERE=os.path.dirname(os.path.abspath(__file__))
T=json.load(open(HERE+'/../transcript.json'))
CLASSES=sorted(T['alphabet'].keys())
VOC=set(open(HERE+'/vocab.txt').read().split())
WEB2=None
def web2():
    global WEB2
    if WEB2 is None:
        WEB2=set(w.upper() for w in open('/usr/share/dict/web2').read().split() if w.isalpha() and len(w)>=4)
    return WEB2

def load_lines(drop_unknown=True):
    """returns list of lines; each line = list of chunks; chunk = string of class codes. '?' and 'X' and '-' kept as classes."""
    out=[]
    for L in T['lines']:
        out.append([c for c in L['chunks']])
    return out

def alphabet_of(lines):
    s=sorted(set(''.join(''.join(l) for l in lines)))
    return s

def make_data(lines, reset='word', alpha=None):
    """glyph stream with reset flags. reset in {'word','line','never'}"""
    alpha=alpha or alphabet_of(lines)
    ix={c:i for i,c in enumerate(alpha)}
    g=[];rs=[];ws=[]
    first=True
    for l in lines:
        lf=True
        for c in l:
            for j,ch in enumerate(c):
                g.append(ix[ch]); ws.append(1 if j==0 else 0)
                r=0
                if reset=='word' and j==0: r=1
                if reset=='line' and j==0 and lf: r=1
                if reset=='never' and len(g)==1: r=1
                rs.append(r)
            lf=False
    return g,rs,ws,alpha

def write_data(path,g,rs,ws,K):
    with open(path,'w') as f:
        f.write(f"{len(g)} {K}\n")
        for a,b,c in zip(g,rs,ws): f.write(f"{a} {b} {c}\n")

def torus_steps(a,b):
    M=a*b
    S=[[ (((i//b+j//b)%a)*b+((i%b+j%b)%b)) for j in range(M)] for i in range(M)]
    return M,M,0,S
def cyclic_steps(M):
    return M,M,0,[[ (i+j)%M for j in range(M)] for i in range(M)]
def write_steps(path,M,D,home,S):
    with open(path,'w') as f:
        f.write(f"{M} {D} {home}\n")
        for row in S: f.write(' '.join(map(str,row))+'\n')

def run(data_path,step_path,mode,restarts,iters,seed,dfix=None,T0=4.0,T1=0.15,cwd=HERE):
    env=dict(os.environ)
    if dfix is not None:
        p=data_path+'.dfix'; open(p,'w').write(' '.join(map(str,dfix))); env['DFIX']=p
    out=subprocess.run([HERE+'/wsolve',data_path,step_path,str(mode),str(restarts),str(iters),str(seed),str(T0),str(T1)],capture_output=True,text=True,env=env,cwd=HERE).stdout
    res={}
    for line in out.splitlines():
        if line.startswith('SCORE'): res['score']=float(line.split()[1])
        elif line.startswith('D '): res['D']=list(map(int,line.split()[1:]))
        elif line.startswith('B '): res['B']=list(map(int,line.split()[1:]))
        elif line.startswith('L '): res['L']=line.split()[1:]
        elif line.startswith('T '): res['text']=line[2:]
    return res

def coverage(text):
    ws=text.split()
    v=sum(len(w) for w in ws if w in VOC and (len(w)>=3 or w in('A','I')))
    tot=sum(len(w) for w in ws)
    w2=web2()
    long=[w for w in ws if len(w)>=4]
    hit=sum(1 for w in long if w in w2 or w in VOC)
    return dict(vocab_letters=v/tot, long_hit=hit/max(1,len(long)), nlong=len(long))
