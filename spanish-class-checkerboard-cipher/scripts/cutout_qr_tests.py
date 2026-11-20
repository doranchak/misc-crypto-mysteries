"""Tests of (a) red glyphs as cutouts / grille over the black shapes, (b) QR / 2-D-code assembly of the black shapes.
Writes figures/cutout_qr_results.json and figures/cutout_examples.jpg.
Run: /opt/homebrew/bin/python3.11 -I scripts/cutout_qr_tests.py"""
import cv2, numpy as np, json, os, itertools, random
from PIL import Image, ImageDraw, ImageFont
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
im=cv2.imread(os.path.join(ROOT,'pic1.jpeg')); g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
B,G,R=[im[:,:,i].astype(int) for i in range(3)]
black=((g<100)&~((R-G)>40)).astype(np.uint8)
redm=((R-G>45)&(R-B>20)).astype(np.uint8); redm[:1300]=0; redm[2330:]=0
BOX={'t1':(87,401,437,807),'t2':(476,404,921,816),'t3':(880,398,1198,681),'t4':(1243,402,1667,791),'t5':(1742,426,2217,809),'t6':(2278,464,2832,779),
'u1':(106,917,392,1302),'u2':(440,901,710,1255),'b1':(258,2438,535,2811),'b2':(589,2414,928,2792),'b3':(983,2388,1347,2746),'b4':(1377,2394,1684,2722),
'b5':(1785,2379,2083,2709),'b6':(2169,2368,2482,2708),'b7':(371,2917,1419,3500)}
def tight(k):
    a,b,c,d=BOX[k]; sub=black[b+15:d-15,a+15:c-15]; ys,xs=np.where(sub>0); return sub[ys.min():ys.max()+1,xs.min():xs.max()+1]
res={}
# ---------------- Q1: how much "ink" is there; would it fit a QR / DM? ----------------
CELL=58.0
area=sum(float(tight(k).sum()) for k in BOX)/CELL**2
res['black_ink_in_cells']=round(area,1)
qr={ver:(4*ver+17)**2 for ver in range(1,7)}
res['qr_modules_total']={f'v{v}':n for v,n in qr.items()}
res['qr_half_dark']={f'v{v}':round(n/2) for v,n in qr.items()}
print('black ink, in 58px cells:',res['black_ink_in_cells'],' | QR modules total (half dark):',{f'v{v}':(n,round(n/2)) for v,n in qr.items()})
# ---------------- Q2: standard decoders on the black layout and on re-assemblies ----------------
det=cv2.QRCodeDetector()
def try_qr(img,label):
    ok=0
    for scale in (1.0,0.5,0.35,0.25):
        for inv in (False,True):
            x=cv2.resize(img,None,fx=scale,fy=scale,interpolation=cv2.INTER_AREA)
            x=255-x if inv else x
            x=cv2.copyMakeBorder(x,40,40,40,40,cv2.BORDER_CONSTANT,value=255)
            try:
                val,pts,_=det.detectAndDecode(x)
            except Exception: val,pts=None,None
            if pts is not None and val: ok+=1
    return ok
board_black=(255-black*255).astype(np.uint8)
res['qr_decode_hits']={'whole_board_black_only':try_qr(board_black,'board'),
                       'top_block':try_qr(board_black[330:1320],'top'),'bottom_block':try_qr(board_black[2330:3560],'bottom')}
both=(255-np.clip(black*255+redm*255,0,255)).astype(np.uint8)
res['qr_decode_hits']['black_plus_red_as_black']=try_qr(both,'both')
print('OpenCV QR decode hits:',res['qr_decode_hits'])
# finder-pattern search: any 1:1:3:1:1 run ratios along rows/cols in a binarised, cell-sampled black image
def finder_score(bitmap):
    """count rows/cols whose run-length pattern looks like 1:1:3:1:1 (dark,light,dark,light,dark) at any scale"""
    def runs(v):
        out=[];c=v[0];n=1
        for x in v[1:]:
            if x==c: n+=1
            else: out.append((c,n)); c=x;n=1
        out.append((c,n)); return out
    hits=0
    for line in list(bitmap)+list(bitmap.T):
        r=runs(list(line))
        for i in range(len(r)-4):
            seg=r[i:i+5]
            if seg[0][0]!=1: continue
            u=sum(n for _,n in seg)/7.0
            if u<4: continue
            tgt=[1,1,3,1,1]
            if all(abs(n/u-t)<0.5 for (_,n),t in zip(seg,tgt)): hits+=1
    return hits
fh={}
for k in BOX:
    m=cv2.resize(tight(k)*255,None,fx=0.25,fy=0.25,interpolation=cv2.INTER_AREA)>100
    fh[k]=finder_score(m.astype(np.uint8))
res['finder_pattern_runs_found']=fh
print('1:1:3:1:1 finder-like runs per glyph:',fh)
# ---------------- Q3: cutout test: red glyphs as windows over black glyph; letter-form score ----------------
font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',60,index=1) if os.path.exists('/System/Library/Fonts/Helvetica.ttc') else ImageFont.load_default()
LET='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
def letter_templates(gw=5,gh=7):
    T={}
    for ch in LET:
        img=Image.new('L',(90,90),0); d=ImageDraw.Draw(img); d.text((10,0),ch,fill=255,font=font)
        a=np.array(img); ys,xs=np.where(a>128)
        a=a[ys.min():ys.max()+1,xs.min():xs.max()+1].astype(np.float32)/255
        T[ch]=cv2.resize(a,(gw,gh),interpolation=cv2.INTER_AREA)>0.45
    return T
TPL=letter_templates()
def letter_score(mask,gw=5,gh=7):
    ys,xs=np.where(mask>0)
    if len(ys)<20: return 0.0,None
    a=mask[ys.min():ys.max()+1,xs.min():xs.max()+1].astype(np.float32)
    best=(0,None)
    for rot in range(4):
        for flip in (False,True):
            b=np.rot90(a,rot); b=b[:,::-1] if flip else b
            for polarity in (False,True):
                c=cv2.resize(b,(gw,gh),interpolation=cv2.INTER_AREA)>0.5
                if polarity: c=~c
                for ch,t in TPL.items():
                    s=(c==t).mean()
                    if s>best[0]: best=(s,(ch,rot,flip,polarity))
    return best
# null for the letter score: random bitmaps with the same density as the black glyphs
rng=np.random.default_rng(3)
def null_scores(n=300):
    out=[]
    for _ in range(n):
        a=(rng.random((6,6))<0.5).astype(np.uint8); a=cv2.resize(a,(60,60),interpolation=cv2.INTER_NEAREST)
        out.append(letter_score(a)[0])
    return np.array(out)
nl=null_scores()
bl={k:letter_score(tight(k))[0] for k in BOX}
res['letter_form_black_alone']={'glyph_scores':{k:round(v,3) for k,v in bl.items()},'random_6x6_null_mean':round(float(nl.mean()),3),'null_95pct':round(float(np.percentile(nl,95)),3),'null_max':round(float(nl.max()),3)}
print('letter-form score (best over 36 templates x 16 orientations/polarities): glyphs',{k:round(v,2) for k,v in bl.items()},' null mean/95%/max',round(nl.mean(),2),round(np.percentile(nl,95),2),round(nl.max(),2))
# red as window mask: each red glyph (components, dilated) rescaled to the black cell size, slid over each black glyph.
# Quality filters: revealed black area >= 1.5 cells, template set excludes I/1 (degenerate bars); null = same pipeline with the
# red window masks rotated/mirrored at random (same shapes, wrong geometry).
for bad in ('I','1'): TPL.pop(bad,None)
d=cv2.dilate(redm,cv2.getStructuringElement(cv2.MORPH_RECT,(25,25)))
n,lab,st,cen=cv2.connectedComponentsWithStats(d)
reds=[]
for i in range(1,n):
    x,y,w,h,a=st[i]
    if a<2500: continue
    m=((lab[y:y+h,x:x+w]==i)&(redm[y:y+h,x:x+w]>0)).astype(np.uint8); reds.append((i,m))
S=CELL/46.0
def windows(m):
    mm=cv2.resize(m,None,fx=S,fy=S,interpolation=cv2.INTER_NEAREST)
    filled=cv2.morphologyEx(mm,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15)))
    cnts,hier=cv2.findContours(filled,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
    win=np.zeros_like(filled)
    for c,h in zip(cnts,hier[0]):
        if h[3]!=-1: cv2.drawContours(win,[c],-1,1,-1)
    return win
WIN={i:windows(m) for i,m in reds}
WIN={i:w for i,w in WIN.items() if w.sum()>=2500}      # at least ~ 1 window
MINREV=1.5*CELL*CELL*0.6
def run(winmap,seed=None,transform=False):
    r=random.Random(seed); out=[]
    for k in BOX:
        bk=tight(k); bh,bw=bk.shape
        for i,win0 in winmap.items():
            win=win0
            if transform:
                win=np.rot90(win0,r.randrange(4)); 
                if r.random()<0.5: win=win[:,::-1]
                win=np.ascontiguousarray(win)
            mh,mw=win.shape
            for oy in range(-mh+40,bh-40,29):
                for ox in range(-mw+40,bw-40,29):
                    y0,x0=max(0,oy),max(0,ox); y1,x1=min(bh,oy+mh),min(bw,ox+mw)
                    if y1-y0<60 or x1-x0<60: continue
                    wv=win[y0-oy:y1-oy,x0-ox:x1-ox]
                    rev=(bk[y0:y1,x0:x1]&wv)
                    if rev.sum()<MINREV: continue
                    sc,info=letter_score(rev)
                    out.append((sc,k,i,ox,oy,info))
    return out
obs=run(WIN); obs.sort(key=lambda r:-r[0])
nulls=[]
for sd in range(3):
    nl_=run(WIN,seed=sd,transform=True); nulls.append(np.array([a[0] for a in nl_]))
o=np.array([a[0] for a in obs])
res['cutout']={'n_trials':len(obs),'best':[(round(float(a[0]),3),a[1],int(a[2]),int(a[3]),int(a[4]),a[5]) for a in obs[:5]],
 'observed_mean':round(float(o.mean()),3),'observed_p99':round(float(np.percentile(o,99)),3),'observed_max':round(float(o.max()),3),
 'null_means':[round(float(x.mean()),3) for x in nulls],'null_p99':[round(float(np.percentile(x,99)),3) for x in nulls],'null_max':[round(float(x.max()),3) for x in nulls],
 'null_trials':[int(len(x)) for x in nulls]}
print('cutout trials',len(obs),'observed mean/p99/max',res['cutout']['observed_mean'],res['cutout']['observed_p99'],res['cutout']['observed_max'])
print('rotated/mirrored-window null: mean',res['cutout']['null_means'],'p99',res['cutout']['null_p99'],'max',res['cutout']['null_max'])
print('top observed:',res['cutout']['best'][:3])
# save the 6 best composites for the report
ex=[]
for sc,k,i,ox,oy,info in obs[:6]:
    bk=tight(k); win=WIN[i]; bh,bw=bk.shape; mh,mw=win.shape
    canvas=np.full((bh,bw,3),255,np.uint8); canvas[bk>0]=(160,160,160)
    y0,x0=max(0,oy),max(0,ox); y1,x1=min(bh,oy+mh),min(bw,ox+mw)
    wv=win[y0-oy:y1-oy,x0-ox:x1-ox]; rev=(bk[y0:y1,x0:x1]&wv)
    sub=canvas[y0:y1,x0:x1]; sub[rev>0]=(0,0,0); sub[(wv>0)&(rev==0)]=(180,180,255)
    t=cv2.resize(canvas,None,fx=0.45,fy=0.45,interpolation=cv2.INTER_AREA)
    t=cv2.copyMakeBorder(t,22,4,4,4,cv2.BORDER_CONSTANT,value=(235,235,235)); cv2.putText(t,f'{k}+red{i} {sc:.2f} {info[0] if info else ""}',(4,16),cv2.FONT_HERSHEY_SIMPLEX,0.45,(0,0,150),1); ex.append(t)
H=max(t.shape[0] for t in ex); W_=max(t.shape[1] for t in ex)
ex=[cv2.copyMakeBorder(t,0,H-t.shape[0],0,W_-t.shape[1],cv2.BORDER_CONSTANT,value=(235,235,235)) for t in ex]
cv2.imwrite(os.path.join(ROOT,'figures','cutout_examples.jpg'),np.vstack([np.hstack(ex[:3]),np.hstack(ex[3:6])]),[cv2.IMWRITE_JPEG_QUALITY,88])
json.dump(res,open(os.path.join(ROOT,'figures','cutout_qr_results.json'),'w'),indent=1,default=str)
