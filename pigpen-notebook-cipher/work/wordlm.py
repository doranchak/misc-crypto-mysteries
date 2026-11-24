import re, math, numpy as np, sys
sys.path.insert(0,'/Users/doranchak/projects/github/misc-crypto-mysteries/pigpen-notebook-cipher')
import lm
FREQ='/private/tmp/claude-501/-Users-doranchak-projects-github-misc-crypto-mysteries/a6b9d5a7-9ec4-49ac-acc3-b0b160245894/scratchpad/count_1w.txt'
TOPN=60000
_cnt={}; _tot=0
for i,line in enumerate(open(FREQ)):
    w,c=line.split('\t'); c=int(c); _tot+=c
    if i<TOPN: _cnt[w.upper()]=c
LOGTOT=math.log(_tot)
T4=lm.get().reshape(-1); V=27
common1={'A','I'}
common2=set('AM AN AS AT BE BY DO GO HE IF IN IS IT ME MY NO OF ON OR SO TO UP US WE OH'.split())
def lmw(w):
    a=np.array([26]+[ord(c)-65 for c in w]+[26])
    if len(a)<4: return -8.0
    i=((a[:-3]*V+a[1:-2])*V+a[2:-1])*V+a[3:]
    return float(T4[i].sum())
_cache={}
def wscore(w):
    r=_cache.get(w)
    if r is not None: return r
    L=len(w)
    if L==1: r= -4.0 if w in common1 else -16.0
    elif L==2: r= -6.0 if w in common2 else -15.0
    else:
        c=_cnt.get(w)
        if c: r=math.log(c)-LOGTOT+4.0   # shift so frequent words ~ +? ; the=-2.7+4
        else: r=-17.0+0.6*lmw(w)
    _cache[w]=r
    return r
if __name__=='__main__':
    for w in ['THE','WILLOWS','ALL','XQZ','SHE','OCCAME','BECAME','HIM']: print(w, round(wscore(w),2))
