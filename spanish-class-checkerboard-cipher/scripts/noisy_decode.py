"""Noisy-channel decoding of the red ternary columns into English words.
obs column -> (top,mid,bottom) trits; letter L (a=1..z=26) -> base-3 digits (top + 3*mid + 9*bottom).
Cost = trit mismatch (empty<->mark 1.0, square<->stroke 0.7) + indel + word-frequency prior.
Run: /opt/homebrew/bin/python3.11 -I scripts/noisy_decode.py <corpus_dir> [marks_json]"""
import sys, os, re, math, collections, unicodedata, json
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
CORP=sys.argv[1]
import red_decode as rd
def norm(t):
    t=unicodedata.normalize('NFD',t.lower()); t=''.join(c for c in t if unicodedata.category(c)!='Mn'); return re.sub("[^a-z ]",' ',t.replace("'",''))
cnt=collections.Counter()
for f in ('en.txt','en_big.txt'):
    p=os.path.join(CORP,f)
    if os.path.exists(p): cnt.update(norm(open(p).read()).split())
web2={w.strip().lower() for w in open('/usr/share/dict/words') if w.strip().isalpha()}
extra="yeah im ive ill dont cant thats youre youve wont didnt isnt gonna wanna gotta ok okay lol hey hi hello thanks thank please cipher codes code reddit class spanish teacher board whiteboard puzzle solve message secret read title really like liked some reason".split()
common="the be to of and a in that have i it for not on with he as you do at this but his by from they we say her she or an will my one all would there their what so up out if about who get which go me when make can like time no just him know take people into year your good some could them see other than then now look only come its over think also back after use two how our work first well way even new want because any these give day most us".split()
VOC=set(w for w,c in cnt.items() if c>=2 and 1<=len(w)<=9)|set(common)|set(extra)
VOC={w for w in VOC if len(w)>=2 or w in ('a','i')}
total=sum(cnt.values())
def wcost(w):
    c=cnt.get(w,0)
    if w in common: c=max(c,300)
    if w in extra: c=max(c,30)
    return -math.log((c+0.3)/total)
def trit(v): return (v%3,(v//3)%3,v//9)    # (top,mid,bottom)
def colcost(letter_v,obs):     # letter value 1..26 ; obs = (top,mid,bot)
    t=trit(letter_v); c=0.0
    for a,b in zip(t,obs):
        if a==b: continue
        c+= 0.7 if (a!=0 and b!=0) else 1.0
    return c
CC=np.array([[colcost(v,(o%3,(o//3)%3,o//9)) for o in range(27)] for v in range(27)])   # [letter value][obs value]
byLen=collections.defaultdict(list)
for w in VOC: byLen[len(w)].append(w)
LW={L:(np.array([[ord(ch)-96 for ch in w] for w in ws]),ws,np.array([wcost(w) for w in ws])) for L,ws in byLen.items()}
INDEL=1.7; LAMBDA=float(os.environ.get('LAMBDA','0.55')); SKIP=2.0; EMPTYSKIP=0.0
def align(Lw,ws_arr,obs):
    """Levenshtein of each word (rows of ws_arr) against obs (list of obs values) -> costs vector"""
    n,L=ws_arr.shape; m=len(obs)
    D=np.zeros((n,L+1,m+1))
    D[:,:,0]=(np.arange(L+1)*INDEL)[None,:]; D[:,0,:]=(np.arange(m+1)*INDEL)[None,:]
    for i in range(1,L+1):
        for j in range(1,m+1):
            sub=D[:,i-1,j-1]+CC[ws_arr[:,i-1],obs[j-1]]
            D[:,i,j]=np.minimum(sub,np.minimum(D[:,i-1,j]+INDEL,D[:,i,j-1]+INDEL))
    return D[:,L,m]
def decode_line(obs):
    n=len(obs); INF=1e9
    best=[INF]*(n+1); back=[None]*(n+1); best[0]=0.0
    for i in range(1,n+1):
        # skip obs[i-1]
        sk=EMPTYSKIP if obs[i-1]==0 else SKIP
        if best[i-1]+sk<best[i]: best[i]=best[i-1]+sk; back[i]=(i-1,None,sk)
        for m in range(1,10):
            j=i-m
            if j<0: break
            window=obs[j:i]
            if all(o==0 for o in window): continue
            for L in range(max(1,m-2),min(9,m+2)+1):
                if L not in LW: continue
                arr,ws,wc=LW[L]
                costs=align(L,arr,window)+LAMBDA*wc
                k=int(np.argmin(costs))
                tot=best[j]+costs[k]
                if tot<best[i]: best[i]=tot; back[i]=(j,ws[k],costs[k])
    out=[]; i=n
    while i>0:
        j,w,c=back[i]; out.append((w,j,i,c)); i=j
    return out[::-1],best[n]
if __name__=='__main__':
    rows=rd.build(46.0,'snap',0.5)
    full=[]
    for L in (1,2,3,4):
        obs=[]; bounds=[]
        for l,c,cols in rows:
            if l!=L: continue
            for col in cols: obs.append(col[0]+3*col[1]+9*col[2])
            bounds.append(len(obs))
        res,tot=decode_line(obs)
        txt=' '.join(w if w else '·' for w,_,_,_ in res)
        print(f'line {L}: cost {tot:.1f}\n   {txt}')
        full.append(txt)
    json.dump(full,open(os.path.join(HERE,'..','figures','noisy_decode.json'),'w'))
