import cv2, numpy as np, pickle, json, base64, collections, math
import glyphlib
from glyphlib import glyph_mask, norm_img
import final_b2 as fb

# ---------- pieces
old=pickle.load(open('seg/pieces_cl3.pkl','rb'))             # b1,b3L,b3R with cl3
b2=pickle.load(open('seg/b2_pieces.pkl','rb'))
newR=b2['R'][2]; newL=b2['L'][2]
# drop junk near illustration in b2R
newR=[p for p in newR if not (p['y']<110 and p['x']>1000) and not (1000<p['x']<1120 and 650<p['y']<730)]
new=newR+newL
# kNN class assignment via Chamfer
So,Do=fb.chamfer_feats(old); Sn,Dn=fb.chamfer_feats(new)
A1=Sn@Do.T; A2=So@Dn.T
D=A1+A2.T
ao,ho,no=fb.extra(old); an,hn,nn=fb.extra(new)
D=D+0.8*np.abs(an[:,None]-ao[None,:])+0.8*np.abs(hn[:,None]-ho[None,:])+0.6*np.abs(nn[:,None]-no[None,:])
cl_old=np.array([p['cl3'] for p in old])
for i,p in enumerate(new):
    nb=np.argsort(D[i])[:7]
    votes=collections.Counter(cl_old[nb])
    p['cl3']=int(votes.most_common(1)[0][0]); p['nnd']=float(D[i][nb[0]])
print('assigned',len(new))
allp=old+new

FAM={14:'phi',26:'phi',29:'dot',34:'dot',18:'dot',33:'Yb',27:'Yl',32:'F',31:'three',25:'Zb',22:'Zd',24:'pr',5:'pr',9:'plus',1:'V',10:'sd',16:'WS',11:'WS',
     35:'h7',13:'h7',21:'h7',12:'h7',30:'M7',17:'M7',28:'cb',20:'Rn',8:'Rn',3:'sl',4:'sl',23:'mix'}
JUNK={0,2,6,15,19,7}
FINFO={ # char, description
 'phi':('ϕ','circle with a vertical slash'),'dot':('⊙','circle with a centre dot'),'Yb':('ɥ','Y-like glyph with a crossbar'),
 'Yl':('ɣ','looped Y / gamma-like glyph'),'F':('ꟻ','7 with a crossbar (reversed F)'),'three':('ʒ','open 3 / ezh'),
 'Zb':('ʓ','barred 7 with S-shaped head'),'Zd':('ƶ','Z with a dot'),'pr':('(','left paren / c, usually with a dot'),
 'plus':('+','plus / cross'),'V':('V','V'),'sd':('⁄','slash with a dot'),'WS':('ꙍ','cursive w joined to S (or 3)'),
 'h7':('ᒣ','7 with a hooked head'),'M7':('ʞ','zig-zag 7 / turned k'),'cb':('ɓ','b-like curl with loop'),
 'Rn':('ʀ','R-hook / arch'),'sl':('|','plain slash stroke'),'mix':('§','mixed (S / V / 7 shapes)')}
def fam(p):
    if p['cl3'] in JUNK: return 'junk'
    return FAM.get(p['cl3'],'mix')
# ---------- lines & words
CFG={'b1':('book1.jpeg',(330,1250,2800,3600),-0.75,33),'b2L':('book2.jpeg',(330,150,2050,1350),-4.75,22),
     'b2R':('book2.jpeg',(2050,250,3950,2750),-1.0,24),'b3L':('book3.jpeg',(30,780,1950,2750),-4.25,24),'b3R':('book3.jpeg',(1900,230,3950,2750),-1.75,24)}
MAXY={'b1':2300}
pages={}
XMIN={'b3L':190}
HEADY={'b3L':150,'b3R':110}
def keep(tag,p):
    if tag=='b3L':
        if p['x']<30: return False
        if p['x']<140 and (p['y']<560 or p['y']>1650): return False
        if p['x']>1600 and p['w']/p['h']>2.2: return False
    return True
def chain_lines(ps):
    ps=sorted(ps,key=lambda p:p['cx'])
    hmed=np.median([p['h'] for p in ps])
    par=list(range(len(ps)))
    def find(a):
        while par[a]!=a: par[a]=par[par[a]]; a=par[a]
        return a
    for i,p in enumerate(ps):
        best=None
        for j in range(i-1,-1,-1):
            q=ps[j]; dx=p['cx']-q['cx']
            if dx>330: break
            dy=abs(p['cy']-q['cy'])
            if dx<5 and dy<5: continue
            if dy<0.5*hmed:
                sc=dx+3*dy
                if best is None or sc<best[0]: best=(sc,j)
        if best: par[find(i)]=find(best[1])
    comps=collections.defaultdict(list)
    for i,p in enumerate(ps): comps[find(i)].append(p)
    lines=[sorted(c,key=lambda p:p['x']) for c in comps.values()]
    return lines
for tag,(name,box,rot,thr) in CFG.items():
    ps=[p for p in allp if p['page']==tag and (tag not in MAXY or p['cy']<MAXY[tag]) and keep(tag,p)]
    lines=chain_lines(ps)
    lines=[l for l in lines if len(l)>=2]
    if tag in HEADY: lines=[l for l in lines if np.mean([p['cy'] for p in l])>HEADY[tag]]
    lines.sort(key=lambda l:np.mean([p['cy'] for p in l]))
    pages[tag]=lines
    print(tag,'lines',len(lines),[len(l) for l in lines])
# ---------- punctuation dots (:. marks)
olddot=pickle.load(open('seg/all_gl.pkl','rb'))
def dots_for(tag):
    if tag in olddot: gl=olddot[tag][0]
    else:
        name,box,rot,thr=CFG[tag]
        mf=None
        if tag=='b2R':
            def mf(th): th=th.copy(); th[80:760,640:1900]=0; return th
        reg,flat,lab,units=fb.extract(name,box,rot,mf)
        # re-extract to get gl with dots
        reg=glyphlib.load_region(name,box,rot); fl=fb.flatten(reg)
        blur=cv2.GaussianBlur(fl,(5,5),0); th=cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,81,14)
        th=cv2.morphologyEx(th,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
        if mf: th=mf(th)
        comps,lab=glyphlib.components(th,40); gl=glyphlib.merge_contained(comps,lab)
    return [g for g in gl if g['kind']=='dot' and 45<=g['area']<=900 and g['w']<45 and g['h']<45]
punct={}
for tag,lines in pages.items():
    dots=dots_for(tag)
    boxes=[p for l in lines for p in l]
    free=[]
    for d in dots:
        inside=any(p['x']-6<=d['cx']<=p['x']+p['w']+6 and p['y']-6<=d['cy']<=p['y']+p['h']+6 for p in boxes)
        if not inside: free.append(d)
    groups=[]
    for d in sorted(free,key=lambda d:d['cx']):
        for g in groups:
            if any(math.hypot(d['cx']-e['cx'],d['cy']-e['cy'])<75 for e in g): g.append(d);break
        else: groups.append([d])
    marks=[]
    for g in groups:
        if len(g)>=2:
            marks.append((float(np.mean([e['cx'] for e in g])),float(np.mean([e['cy'] for e in g])),len(g)))
    punct[tag]=marks
    print(tag,'punct marks',len(marks))
# ---------- words, tokens
THR={k:v[3] for k,v in CFG.items()}
out={}
fam_pos=collections.defaultdict(lambda:collections.Counter())
fam_cnt=collections.Counter(); cl_cnt=collections.Counter()
for tag,lines in pages.items():
    L=[]
    for li,l in enumerate(lines):
        ws=[[l[0]]]
        for i in range(1,len(l)):
            g=l[i]['x']-(l[i-1]['x']+l[i-1]['w'])
            if g>THR[tag]: ws.append([l[i]])
            else: ws[-1].append(l[i])
        cy=np.mean([p['cy'] for p in l]); xs=[p['x'] for p in l]; xe=[p['x']+p['w'] for p in l]
        pm=[m for m in punct[tag] if abs(m[1]-cy)<0.7*np.median([p['h'] for p in l]) and min(xs)-30<=m[0]<=max(xe)+90]
        items=[]
        for wi,w in enumerate(ws):
            items.append(dict(type='w',glyphs=[dict(x=p['x'],y=p['y'],w=p['w'],h=p['h'],c=p['cl3'],f=fam(p)) for p in w],x0=w[0]['x']))
        for m in pm: items.append(dict(type='p',x0=m[0],n=m[2],cx=m[0],cy=m[1]))
        items.sort(key=lambda it:it['x0'])
        L.append(items)
        # stats (words only, non-junk)
        for it in items:
            if it['type']!='w': continue
            fs=[g['f'] for g in it['glyphs'] if g['f']!='junk']
            for i,f in enumerate(fs):
                fam_cnt[f]+=1
                pos='single' if len(fs)==1 else 'first' if i==0 else 'last' if i==len(fs)-1 else 'mid'
                fam_pos[f][pos]+=1
            for g in it['glyphs']: cl_cnt[g['c']]+=1
    out[tag]=L
# ---------- images
def jpeg_b64(img,maxw=1700,q=80):
    h,w=img.shape[:2]; s=min(1.0,maxw/w)
    im=cv2.resize(img,(int(w*s),int(h*s)),interpolation=cv2.INTER_AREA)
    ok,buf=cv2.imencode('.jpg',im,[cv2.IMWRITE_JPEG_QUALITY,q]); return base64.b64encode(buf).decode(),s
data={'pages':{},'fam':{},'cl':{}}
for tag,(name,box,rot,thr) in CFG.items():
    reg=glyphlib.load_region(name,box,rot); fl=fb.flatten(reg)
    b64,s=jpeg_b64(fl)
    data['pages'][tag]=dict(img=b64,scale=s,w=fl.shape[1],h=fl.shape[0],lines=out[tag],punct=punct[tag])
# exemplar thumbs per cluster
def png_b64(m,size=44):
    im=255-norm_img(m,size)
    ok,buf=cv2.imencode('.png',im); return base64.b64encode(buf).decode()
by_cl=collections.defaultdict(list)
for i,p in enumerate(allp): by_cl[p['cl3']].append(p)
Dall=None
for c,ps in by_cl.items():
    sel=ps[:: max(1,len(ps)//4)][:4]
    data['cl'][str(c)]=dict(n=len(ps),fam=FAM.get(c,'junk' if c in JUNK else 'mix'),thumbs=[png_b64(p['mask']) for p in sel])
for f,(ch,desc) in FINFO.items():
    cls=[c for c,ff in FAM.items() if ff==f]
    data['fam'][f]=dict(ch=ch,desc=desc,clusters=cls,n=fam_cnt[f],pos=dict(fam_pos[f]))
pickle.dump(data,open('seg/report_data.pkl','wb'))
print({f:(fam_cnt[f],dict(fam_pos[f])) for f in FINFO})
print('pieces total',sum(fam_cnt.values()))
