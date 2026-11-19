import sys, json, collections, html
import numpy as np, cv2
import boot, decode as dc, keyglyphs as kg
D=boot.D; meta=boot.meta; idx=boot.idx
lab=boot.build_train(boot.load_ver())
P=json.load(open('report_pages.json'))
LETTERS='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
def cands_for(sym,pages=('b2L','b2R','b3L','b3R')):
    return [i for i,l in lab.items() if l==sym and meta[i][0] in pages]
def pick(cands,n=2):
    if not cands: return []
    if len(cands)<=n: return cands[:n]
    sub=D[np.ix_(cands,cands)]; k=min(4,len(cands)-1)
    typ=np.sort(sub,1)[:,1:k+1].mean(1)
    order=np.argsort(typ); first=order[0]; chosen=[first]
    pool=order[:max(n+2,int(0.6*len(cands)))]
    while len(chosen)<n:
        best=max((q for q in pool if q not in chosen),key=lambda q:min(sub[q,c] for c in chosen))
        chosen.append(best)
    return [cands[c] for c in chosen]
def piece_of(i): m=meta[i]; return m[0],boot.lines_of(m[0])[m[1]][m[2]],(m[1],m[2])
def render(page,pcs,sig=0.9,thrf=0.92,eps=0.5):
    keep,up=kg.trace(page,pcs,sig=sig,thrf=thrf)
    r=kg.to_path(keep,up,eps=eps)
    if r: r['page']=page
    return r
ex={}
for L in LETTERS:
    ids=pick(cands_for(L),2)
    ex[L]=[render(*piece_of(i)[:2] if False else (piece_of(i)[0],[piece_of(i)[1]])) for i in ids]
    ex[L]=[r for r in ex[L] if r]
# apostrophe
ids=pick(cands_for("'"),2); ex["'"]=[render(piece_of(i)[0],[piece_of(i)[1]]) for i in ids]
# fused units from the aligner's glyph boxes in the report (verified / key words only, pages 2-3 preferred)
def glyph_boxes(sym,pages,flags=('V','K'),want_len=None):
    out=[]
    for pg in pages:
        for ln in P[pg]['lines']:
            for g in ln['glyphs']:
                if g['t']==sym and g['f'] in flags: out.append((pg,ln['i'],g))
    return out
def render_box(pg,g,li=None,pad=2):
    x,y,w,h=int(g['x']),int(g['y']),int(g['w']),int(g['h'])
    pcs=[]
    if li is not None:
        for p in boot.lines_of(pg)[li]:
            cx=p['x']+p['w']/2; cy=p['y']+p['h']/2
            if x-4<=cx<=x+w+4 and y-4<=cy<=y+h+4: pcs.append(p)
    if not pcs: pcs=[dict(x=x,y=y,w=w,h=h,mask=np.ones((h,w),np.uint8))]
    return render(pg,pcs,sig=0.9,thrf=0.92)
FUSED=[('TH',['b2L','b2R','b3L','b3R']),('THE',['b2L','b2R','b3L','b3R']),('AND',['b2L','b2R','b3L','b3R']),('WH',['b2R','b3L','b3R']),
       ('ING',['b2L','b2R','b3L','b3R']),('CH',['b1']),('GH',['b2R','b3L','b3R']),('ST',['b2L','b2R','b3L','b3R']),('OO',['b1'])]
fx={}
for sym,pages in FUSED:
    c=glyph_boxes(sym,pages)
    if sym!='WH': c=sorted(c,key=lambda t:abs(t[2]['w']-np.median([q[2]['w'] for q in c])))
    fx[sym]=[r for r in (render_box(pg,g,li) for pg,li,g in c[:2]) if r]
    print(sym,len(c),[ (pg,li) for pg,li,g in c[:2]])
fx['CH']=[render('b2R',[boot.lines_of('b2R')[0][1]])]   # CHAPTER: the C and H are one fused glyph (piece 0 of that line is gutter shadow)
json.dump(dict(ex=ex,fx=fx),open('key_glyphs.json','w'))
print({k:len(v) for k,v in ex.items()}, {k:len(v) for k,v in fx.items()})
