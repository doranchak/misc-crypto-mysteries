import cv2, numpy as np, pickle
from glyphlib import *

def split_unit(mask, m, minfrac=0.5):
    h,w = mask.shape
    n = int(round(w/m))
    if n<2: return [(0,w)]
    P = (mask>0).sum(axis=0).astype(float)
    P = np.convolve(P, np.ones(5)/5, mode='same')
    Pn = P/ (P.max()+1e-9)
    # DP: best[k][x] = min cost with k cuts, last cut at x
    xs = list(range(int(minfrac*m), w-int(minfrac*m)+1))
    INF=1e18
    best = {}
    # k=1 cuts
    prev = {x: (Pn[x] + 0.8*((x-m)/m)**2*0.5, None) for x in xs}
    layers=[prev]
    for k in range(2,n):
        cur={}
        for x in xs:
            bestc=INF;bp=None
            for px,(pc,_) in layers[-1].items():
                wd=x-px
                if wd<minfrac*m or wd>1.7*m: continue
                c=pc+Pn[x]+0.8*((wd-m)/m)**2*0.5
                if c<bestc: bestc=c;bp=px
            if bp is not None: cur[x]=(bestc,bp)
        layers.append(cur)
    # finish
    bestc=INF;bx=None
    for x,(pc,_) in layers[-1].items():
        wd=w-x
        if wd<minfrac*m or wd>1.7*m: continue
        c=pc+0.8*((wd-m)/m)**2*0.5
        if c<bestc: bestc=c;bx=x
    if bx is None:
        # fallback equal split
        return [(int(i*w/n),int((i+1)*w/n)) for i in range(n)]
    cuts=[bx]
    for k in range(len(layers)-1,0,-1):
        bx=layers[k][bx][1]; cuts.append(bx)
    cuts=sorted(cuts)
    edges=[0]+cuts+[w]
    return [(edges[i],edges[i+1]) for i in range(len(edges)-1)]
