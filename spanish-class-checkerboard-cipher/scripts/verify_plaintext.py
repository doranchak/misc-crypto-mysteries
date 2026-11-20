"""Align the independent photo transcription (scripts/red_decode.py, black_ternary.py) with the full plaintext
(decipherment supplied by the researcher) column by column.  Writes figures/verify_alignment.json.
Run: /opt/homebrew/bin/python3.11 -I scripts/verify_plaintext.py <corpus_dir>"""
import sys, os, json
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE); sys.path.insert(0,HERE)
import red_decode as rd
RED_LINES=["YEAH READ THE TITLE THIS MORNING I DECIDED TO LEARN A NEW",
           "CIPHER AND FOR SOME REASON I REALLY LIKED IT AND",
           "CAUGHT ONTO IT WITH INCREDIBLE SPEED SINCE NOBODY WILL",
           "EVER READ THIS IM GONNA SHARE A SECRET WITH YOU"]
def trits(v): return (v%3,(v//3)%3,v//9)
def cost(exp_v,obs):
    t=trits(exp_v); c=0.0
    for a,b in zip(t,obs):
        if a==b: continue
        c+=0.7 if (a and b) else 1.0
    return c
def align(exp,obs,indel=1.7):
    n,m=len(exp),len(obs); D=np.zeros((n+1,m+1)); B=np.zeros((n+1,m+1),int)
    D[:,0]=np.arange(n+1)*indel; D[0,:]=np.arange(m+1)*indel
    for i in range(1,n+1):
        for j in range(1,m+1):
            opts=(D[i-1,j-1]+cost(exp[i-1],obs[j-1]),D[i-1,j]+indel,D[i,j-1]+indel)
            k=int(np.argmin(opts)); D[i,j]=opts[k]; B[i,j]=k
    i,j=n,m; pairs=[]
    while i>0 or j>0:
        if i>0 and j>0 and B[i,j]==0: pairs.append((i-1,j-1)); i-=1; j-=1
        elif i>0 and (j==0 or B[i,j]==1): pairs.append((i-1,None)); i-=1
        else: pairs.append((None,j-1)); j-=1
    return pairs[::-1]
res={'red':{},'black':{}}
for P in (46.0,47.0):
    rows=rd.build(P,'snap',0.5)
    tot=dict(expected=0,exact=0,one_trit=0,two_plus=0,missing=0,extra=0)
    perline=[]
    for L in (1,2,3,4):
        obs=[(c[0]+3*c[1]+9*c[2]) for l,_,cols in rows if l==L for c in cols]
        exp=[ord(ch)-64 for ch in RED_LINES[L-1] if ch!=' ']
        obs_t=[ (v%3,(v//3)%3,v//9) for v in obs]
        pairs=align(exp,obs_t)
        d=dict(expected=len(exp),exact=0,one_trit=0,two_plus=0,missing=0,extra=0)
        for i,j in pairs:
            if i is None: d['extra']+=1
            elif j is None: d['missing']+=1
            else:
                c=cost(exp[i],obs_t[j])
                if c==0: d['exact']+=1
                elif c<=1.0: d['one_trit']+=1
                else: d['two_plus']+=1
        perline.append(d)
        for k in tot: tot[k]+=d[k]
    res['red'][f'P={P}']=dict(total=tot,lines=perline)
    print('red P',P,tot,'exact %.0f%%, <=1 trit off %.0f%%'%(100*tot['exact']/tot['expected'],100*(tot['exact']+tot['one_trit'])/tot['expected']))
# black
BT=json.load(open(os.path.join(ROOT,'figures','black_ternary.json')))
EXP={'t1':'IM','t2':'BOR','t3':'ED','t4':'AND','t5':'HAVE','t6':'STUFF','u1':'TO','u2':'DO','b1':'IM','b2':'THE','b3':'ONE','b4':'WHO','b5':'BROS','b6':'THE','b7':'MIRROR'}
tot=dict(expected=0,exact=0,one_trit=0,two_plus=0,missing=0,extra=0); per={}
for k,w in EXP.items():
    obs=[c for c in BT[k]['cells']]; obs_t=[tuple(c) for c in obs]
    exp=[ord(ch)-64 for ch in w]
    pairs=align(exp,obs_t)
    d=dict(expected=len(exp),exact=0,one_trit=0,two_plus=0,missing=0,extra=0)
    for i,j in pairs:
        if i is None: d['extra']+=1
        elif j is None: d['missing']+=1
        else:
            c=cost(exp[i],obs_t[j])
            if c==0: d['exact']+=1
            elif c<=1.0: d['one_trit']+=1
            else: d['two_plus']+=1
    per[k]=d
    for kk in tot: tot[kk]+=d[kk]
res['black']=dict(total=tot,glyphs=per)
print('black',tot,'exact %.0f%%, <=1 trit off %.0f%%'%(100*tot['exact']/tot['expected'],100*(tot['exact']+tot['one_trit'])/tot['expected']))
json.dump(res,open(os.path.join(ROOT,'figures','verify_alignment.json'),'w'),indent=1)
