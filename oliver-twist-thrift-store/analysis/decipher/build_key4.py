# adds SH + doubled-letter glyphs (EE TT LL SS FF CC) + OU (re-picked) and the ten block-hand digits to key_glyphs.json
import json, numpy as np, cv2, statistics
import boot, keyglyphs as kg, keyglyphs2 as k2
P=json.load(open('report_pages.json')); G=json.load(open('key_glyphs.json'))
def cands(unit,pages=('b2L','b2R','b3L','b3R')):
    out=[]
    for pg in pages:
        for ln in P[pg]['lines']:
            for g in ln['glyphs']:
                if g['t']==unit and g['f'] in ('V','K'): out.append((pg,ln['i'],g))
    return out
def pick(unit,n=2):
    c=cands(unit)
    if not c: return []
    med=statistics.median(g['w'] for _,_,g in c)
    c.sort(key=lambda t:abs(t[2]['w']-med))
    res=[]; seen=set()
    for pg,li,g in c:
        if (pg,li) in seen and len(c)>n: continue
        seen.add((pg,li)); res.append((pg,li,g))
        if len(res)==n: break
    return res
MANP={'OO':['b3L:16:941','b3R:9:1424'],'FF':['b2R:4:159','b3L:9:1277'],'CC':['b2R:3:1340','b2R:8:1055']}
def bykey(unit,keys):
    out=[]
    for k in keys:
        pg,li,x=k.split(':'); li=int(li); x=int(x)
        for ln in P[pg]['lines']:
            if ln['i']==li:
                for g in ln['glyphs']:
                    if g['t']==unit and int(g['x'])==x: out.append((pg,li,g))
    return out
for unit in ['SH','EE','TT','LL','SS','FF','CC','OU','OO']:
    out=[]
    for pg,li,g in (bykey(unit,MANP[unit]) if unit in MANP else pick(unit)):
        r=k2.render_glyph(pg,li,(g['x'],g['y'],g['w'],g['h']))
        if r: r.pop('keep'); out.append(r)
    G['fx'][unit]=out; print(unit,len(cands(unit)),len(out),[(r['page'],round(r['w']),round(r['h'])) for r in out])
# ---- block-hand digits from the row on photo 5
OT='/Users/doranchak/projects/github/misc-crypto-mysteries/oliver-twist-thrift-store/'
im=cv2.imread(OT+'book5.jpeg',0)
rb=[(84,96,93,115),(304,98,65,110),(482,85,91,123),(653,80,95,114),(842,79,88,109),(1022,81,64,109),(1149,86,67,125),(1316,80,86,133),(1475,81,77,120),(1671,96,73,119)]
dig={}
for (x,y,w,h),d in zip(rb,'1234567890'):
    X0,Y0=500+x-10,2150+y-10; c=im[Y0:Y0+h+20,X0:X0+w+20]
    thr,_=cv2.threshold(c,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    up=4; g=cv2.resize(c,None,fx=up,fy=up,interpolation=cv2.INTER_CUBIC); g=cv2.GaussianBlur(g,(0,0),up*0.8)
    bw=((g<thr*0.9)).astype(np.uint8)*255
    n,lab,st,_=cv2.connectedComponentsWithStats(bw,connectivity=8); keep=np.zeros_like(bw)
    for i in range(1,n):
        if st[i,4]>=40*up*up: keep[lab==i]=255
    r=kg.to_path(keep,up,eps=0.5)
    r['page']='b2R'; dig[d]=r
G['digits']=dig
json.dump(G,open('key_glyphs.json','w')); print('digits',{k:(round(v['w']),round(v['h'])) for k,v in dig.items()})
