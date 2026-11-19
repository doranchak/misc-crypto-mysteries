import cv2, numpy as np
BASE='/Users/doranchak/projects/github/misc-crypto-mysteries/oliver-twist-thrift-store/'

def load_region(name, box, rot=0.0):
    img = cv2.imread(BASE+name, 0)
    x0,y0,x1,y1 = box
    reg = img[y0:y1, x0:x1].copy()
    if rot:
        h,w = reg.shape
        M = cv2.getRotationMatrix2D((w/2,h/2), rot, 1.0)
        reg = cv2.warpAffine(reg, M, (w,h), borderMode=cv2.BORDER_REPLICATE)
    return reg

def binarize(reg, block=101, C=22):
    blur = cv2.GaussianBlur(reg,(5,5),0)
    th = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,block,C)
    th = cv2.morphologyEx(th, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
    return th

def components(th, min_area=40):
    n, lab, stats, cent = cv2.connectedComponentsWithStats(th, 8)
    comps=[]
    for i in range(1,n):
        x,y,w,h,a = stats[i]
        if a<min_area: continue
        comps.append(dict(id=i,x=int(x),y=int(y),w=int(w),h=int(h),area=int(a),cx=float(cent[i][0]),cy=float(cent[i][1])))
    return comps, lab

def merge_contained(comps, lab, dot_max=1600):
    """merge comps whose bbox lies inside another comp's bbox (dot inside ring)"""
    comps = sorted(comps, key=lambda c:-c['area'])
    hosts=[]; absorbed={}
    for c in comps:
        host=None
        for b in hosts:
            if (c['x']>=b['x']-3 and c['y']>=b['y']-3 and c['x']+c['w']<=b['x']+b['w']+3 and c['y']+c['h']<=b['y']+b['h']+3
                and c['area']<dot_max and c['area']<0.5*b['area']):
                host=b;break
        if host is not None:
            absorbed[host['id']].append(c['id'])
        else:
            hosts.append(c); absorbed[c['id']]=[c['id']]
    out=[]
    for b in hosts:
        ids=absorbed[b['id']]
        mask = np.isin(lab[b['y']:b['y']+b['h'], b['x']:b['x']+b['w']], ids)
        out.append(dict(ids=ids,x=b['x'],y=b['y'],w=b['w'],h=b['h'],area=int(mask.sum()),
                        cx=b['cx'],cy=b['cy'],ndots=len(ids)-1,
                        kind='glyph' if (b['area']>=300 and max(b['w'],b['h'])>=40) else 'dot'))
    return out

def glyph_mask(lab, g):
    return np.isin(lab[g['y']:g['y']+g['h'], g['x']:g['x']+g['w']], g['ids']).astype(np.uint8)*255

def norm_img(mask, size=32, pad=2):
    h,w = mask.shape
    s = (size-2*pad)/max(h,w)
    nh,nw = max(1,int(round(h*s))), max(1,int(round(w*s)))
    r = cv2.resize(mask,(nw,nh),interpolation=cv2.INTER_AREA)
    canvas = np.zeros((size,size),np.uint8)
    oy,ox=(size-nh)//2,(size-nw)//2
    canvas[oy:oy+nh,ox:ox+nw]=r
    return canvas

def best_angle(th, rng=np.arange(-8,8.01,0.25)):
    best=None
    h,w=th.shape
    for a in rng:
        M=cv2.getRotationMatrix2D((w/2,h/2),a,1.0)
        r=cv2.warpAffine(th,M,(w,h))
        v=r.sum(axis=1).astype(float).var()
        if best is None or v>best[0]: best=(v,a)
    return best[1]
