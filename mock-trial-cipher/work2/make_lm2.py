#!/opt/homebrew/bin/python3.11
"""Interpolated (Jelinek-Mercer) word-aware 4-gram LM -> lm4.bin"""
import re, collections, numpy as np
base='/Users/doranchak/projects/github/misc-crypto-mysteries/'
texts=[open(base+'need-assistance-with-cipher/work/corpus_clean.txt').read()]
for f in ['spanish-class-checkerboard-cipher/corpus/en.txt','spanish-class-checkerboard-cipher/corpus/en_big.txt']:
    texts.append(open(base+f).read())
words=[]
for t in texts:
    t=re.sub(r'[^A-Za-z ]+',' ',t).upper(); words+=t.split()
C=[np.zeros(27**k) for k in (1,2,3,4)]
def enc(s): return [26 if c==' ' else ord(c)-65 for c in s]
for i in range(0,len(words),200):
    v=np.array(enc(' '+' '.join(words[i:i+200])+' '))
    for k in (1,2,3,4):
        if len(v)<k: continue
        idx=np.zeros(len(v)-k+1,dtype=np.int64)
        for j in range(k): idx=idx*27+v[j:len(v)-k+1+j]
        np.add.at(C[k-1],idx,1)
# conditional probs
P1=(C[0]+0.5)/(C[0].sum()+13.5)
def cond(Ck,Ckm1,k,prev):
    # P(d|ctx) = Ck[ctx*27+d]/Ckm1[ctx]
    return None
P=[None]*4
P[0]=P1
c2=C[1].reshape(27,27); n1=c2.sum(1,keepdims=True)
P2=np.where(n1>0,c2/np.maximum(n1,1),P1[None,:])
c3=C[2].reshape(27,27,27); n2=c3.sum(2,keepdims=True)
P3=np.where(n2>0,c3/np.maximum(n2,1),P2[None,:,:])
c4=C[3].reshape(27,27,27,27); n3=c4.sum(3,keepdims=True)
P4=np.where(n3>0,c4/np.maximum(n3,1),P3[None,:,:,:])
# JM weights depend on context count for 3-context
w4=n3/(n3+3.0)   # more weight to 4gram when context is frequent
w3=n2/(n2+3.0)
w2=n1/(n1+3.0)
Pi2=w2*P2+(1-w2)*P1[None,:]
Pi3=w3*P3+(1-w3)*Pi2[None,:,:]
Pi4=w4*P4+(1-w4)*Pi3[None,:,:,:]
Pi4=0.9*Pi4+0.1/27
lm=np.log(Pi4).astype(np.float32)
lm.tofile('lm4.bin')
print(lm.shape, lm.mean())
