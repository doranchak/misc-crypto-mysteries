import numpy as np, math
import decode as dc
LI=dc.LI
GROUPS={'TH','THE','AND','ING','ION','CH','ST','CK','GH','OU','OO','NG','IN','ND','OUGH','CC','FF','PP','SS','TT','LL','EE','RR','NN','MM','DD','GG','ZZ','IO','NT','EN','WH','NE','SH'}
def single_cost(lp,ch):
    k=LI.get(ch)
    return 6.0 if k is None else min(6.0,-float(lp[k]))
def group_cost(lp,s):
    if len(s)==1: return single_cost(lp,s)
    if s in LI: return min(6.0,-float(lp[LI[s]]))+0.5
    return 1.0+0.6*(len(s)-2)+0.5*min(single_cost(lp,ch) for ch in s)
def align(P,logP,letters,xs=None,xw=35.0,skipP=2.2,skipL=5.0,pairC=0.6,breaks=()):
    """returns items=[(piece_index_tuple, letters)] in reading order. Letters that get no own glyph are attached to a neighbouring item."""
    m=len(P); n=len(letters); INF=1e9
    cx=[p['x']+p['w']/2 for p in P]
    medw=float(np.median([p['w'] for p in P])) if P else 60.0
    def pos_cost(j,k):
        if xs is None or xs[k] is None: return 0.0
        return min(4.0,0.8*((cx[j]-xs[k])/xw)**2)
    def pair_extra(j):   # None if pieces j, j+1 cannot form one glyph; else extra cost (small when they overlap in x)
        a,b=P[j],P[j+1]; gap=b['x']-(a['x']+a['w'])
        if gap>0.7*medw: return None
        ov=min(a['x']+a['w'],b['x']+b['w'])-max(a['x'],b['x'])
        if ov>0: return 0.2+0.7*max(0.0,1-ov/(0.5*min(a['w'],b['w'])))
        return 0.9+1.0*gap/medw
    def skip_cost(j):
        p=P[j]; c=skipP
        if p['w']<0.5*medw: c=1.3
        for q in (P[j-1] if j>0 else None, P[j+1] if j+1<m else None):
            if q is None: continue
            ov=min(p['x']+p['w'],q['x']+q['w'])-max(p['x'],q['x'])
            if ov>0.5*min(p['w'],q['w']): c=min(c,0.7)
        return c
    sp=[skip_cost(j) for j in range(m)]
    starts=set(breaks)|{0}; ends=set(sorted(starts)[1:])|{n}
    dp=np.full((m+1,n+1),INF); dp[0,0]=0.0; bp={}
    for j in range(m+1):
        for k in range(n+1):
            c0=dp[j,k]
            if c0>=INF: continue
            if j<m:
                if c0+sp[j]<dp[j+1,k]: dp[j+1,k]=c0+sp[j]; bp[(j+1,k)]=('sp',)
                for g in (1,2,3,4):
                    if k+g>n: break
                    s=letters[k:k+g]
                    if g>1 and (s not in GROUPS or any((k+t) in breaks for t in range(1,g))): continue
                    c=group_cost(logP[j],s)+sum(pos_cost(j,k+t) for t in range(g))/g
                    if s in ('THE','AND') and k in starts and (k+g) in ends: c-=1.5
                    if c0+c<dp[j+1,k+g]: dp[j+1,k+g]=c0+c; bp[(j+1,k+g)]=('m',g)
                    pe=pair_extra(j) if (j+1<m and "'" not in s) else None
                    if pe is not None:
                        c2=min(group_cost(logP[j],s),group_cost(logP[j+1],s))+pe+sum(pos_cost(j,k+t) for t in range(g))/g
                        if c0+c2<dp[j+2,k+g]: dp[j+2,k+g]=c0+c2; bp[(j+2,k+g)]=('p',g)
            if k<n and c0+skipL<dp[j,k+1]: dp[j,k+1]=c0+skipL; bp[(j,k+1)]=('sl',)
    items=[]; orphans=[]
    j,k=m,n
    while (j,k)!=(0,0):
        op=bp[(j,k)]
        if op[0]=='sp': j-=1
        elif op[0]=='sl': orphans.append(k-1); k-=1
        elif op[0]=='m': g=op[1]; items.append([(j-1,),letters[k-g:k],k-g]); j-=1; k-=g
        else: g=op[1]; items.append([(j-2,j-1),letters[k-g:k],k-g]); j-=2; k-=g
    items.reverse()
    for kidx in sorted(orphans):
        # attach to the item holding the next letter (else previous)
        tgt=None
        for it in items:
            if it[2]>kidx: tgt=it; break
        if tgt is None and items: tgt=items[-1]
        if tgt is not None:
            if tgt[2]>kidx: tgt[1]=letters[kidx]+tgt[1]; tgt[2]=kidx
            else: tgt[1]=tgt[1]+letters[kidx]
    return [(tuple(it[0]),it[1],it[2]) for it in items],dp[m,n]
def merge_boxes(P,items):
    """boxes for each item (union of its pieces plus overlapping unused neighbours); returns [(x,y,w,h,text,pieces)]"""
    used={j for it,_,_ in items for j in it}; m=len(P); out=[]
    for it,t,k0 in items:
        b=[min(P[j]['x'] for j in it),min(P[j]['y'] for j in it),max(P[j]['x']+P[j]['w'] for j in it),max(P[j]['y']+P[j]['h'] for j in it)]
        out.append([b,t,it,k0])
    for j in range(m):
        if j in used: continue
        p=P[j]
        for o in out:
            b=o[0]; ov=min(p['x']+p['w'],b[2])-max(p['x'],b[0])
            if ov>0.5*min(p['w'],b[2]-b[0]):
                b[0]=min(b[0],p['x']); b[1]=min(b[1],p['y']); b[2]=max(b[2],p['x']+p['w']); b[3]=max(b[3],p['y']+p['h']); break
    return [(b[0],b[1],b[2]-b[0],b[3]-b[1],t,it,k0) for b,t,it,k0 in out]
