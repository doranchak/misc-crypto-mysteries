import numpy as np, re, os
CORP='/Users/doranchak/projects/github/misc-crypto-mysteries/need-assistance-with-cipher/work/corpus_clean.txt'
def build():
    txt=open(CORP).read().upper()
    txt=re.sub(r'[^A-Z ]',' ',txt); txt=re.sub(r' +',' ',txt).strip()
    s=np.array([26 if c==' ' else ord(c)-65 for c in txt],dtype=np.int64)
    V=27
    c4=np.zeros(V**4); c3=np.zeros(V**3); c2=np.zeros(V**2)
    i4=((s[:-3]*V+s[1:-2])*V+s[2:-1])*V+s[3:]
    np.add.at(c4,i4,1)
    i3=(s[:-2]*V+s[1:-1])*V+s[2:]; np.add.at(c3,i3,1)
    i2=s[:-1]*V+s[1:]; np.add.at(c2,i2,1)
    c1=np.bincount(s,minlength=V).astype(float)
    p1=(c1+1)/(c1.sum()+V)
    p2=(c2.reshape(V,V)+0.5*0+0.01)/(c2.reshape(V,V).sum(1,keepdims=True)+0.01*V)
    # interpolate
    p2=(c2.reshape(V,V)+p1[None,:]*2)/(c2.reshape(V,V).sum(1,keepdims=True)+2)
    c3r=c3.reshape(V,V,V)
    p3=(c3r+p2[None,:,:]*2)/(c3r.sum(2,keepdims=True)+2)
    c4r=c4.reshape(V,V,V,V)
    p4=(c4r+p3[None,:,:,:]*2)/(c4r.sum(3,keepdims=True)+2)
    return np.log(p4).astype(np.float32)
_cache='/private/tmp/claude-501/-Users-doranchak-projects-github-misc-crypto-mysteries/a6b9d5a7-9ec4-49ac-acc3-b0b160245894/scratchpad/lm4.npy'
def get():
    if os.path.exists(_cache): return np.load(_cache)
    t=build(); np.save(_cache,t); return t
