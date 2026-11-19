import sys, json, pickle, base64, collections
import numpy as np, cv2
import boot, decode as dc, lat
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
def b64jpg(img,q=80):
    ok,buf=cv2.imencode('.jpg',img,[cv2.IMWRITE_JPEG_QUALITY,q]); return base64.b64encode(buf).decode()
lab=boot.build_train(boot.load_ver()); meta=boot.meta
ids=[i for i in lab if len(lab[i])==1]
X=np.array([lat.F(meta[i][0],meta[i][1],meta[i][2]) for i in ids]); y=np.array([lab[i] for i in ids])
groups=[meta[i][0]+str(meta[i][1]) for i in ids]
prob=np.zeros(len(ids)); agree=np.zeros(len(ids),bool)
for tr,te in GroupKFold(8).split(X,y,groups):
    clf=LogisticRegression(C=5,max_iter=2000).fit(X[tr],y[tr]); P=clf.predict_proba(X[te]); cl=list(clf.classes_)
    for k,t in enumerate(te):
        if y[t] in cl: prob[t]=P[k][cl.index(y[t])]
        agree[t]=(clf.classes_[P[k].argmax()]==y[t])
FL={'b1':pickle.load(open('b1_pieces.pkl','rb'))['flat']}
for t in ['b2L','b2R','b3L','b3R']: FL[t]=boot.A[t]['flat']
def tile_of(i,pad=14,H=84):
    m=meta[i]; p=boot.lines_of(m[0])[m[1]][m[2]]; fl=FL[m[0]]
    x0=max(0,p['x']-pad); y0=max(0,p['y']-pad); x1=min(fl.shape[1],p['x']+p['w']+pad); y1=min(fl.shape[0],p['y']+p['h']+pad)
    t=fl[y0:y1,x0:x1]; s=H/t.shape[0]; t=cv2.resize(t,(max(8,int(t.shape[1]*s)),H),interpolation=cv2.INTER_AREA)
    return b64jpg(t,82)
alpha={}
for L in "ABCDEFGHIJKLMNOPQRSTUVWXYZ'":
    cand=[k for k in range(len(ids)) if y[k]==L]
    cand.sort(key=lambda k:-(prob[k]+0.15*agree[k]+0.1*(meta[ids[k]][0]!='b1')))
    alpha[L]=dict(n=len(cand),tiles=[tile_of(ids[k]) for k in cand[:6]])
FS=json.load(open('fixed_spans.json')); joined=collections.defaultdict(list)
def add(form,page,li,i,j):
    pcs=boot.lines_of(page)[int(li)][i:j]; fl=FL[page]; pad=14
    x0=max(0,min(p['x'] for p in pcs)-pad); x1=min(fl.shape[1],max(p['x']+p['w'] for p in pcs)+pad)
    y0=max(0,min(p['y'] for p in pcs)-pad); y1=min(fl.shape[0],max(p['y']+p['h'] for p in pcs)+pad)
    t=fl[y0:y1,x0:x1]; s=84/t.shape[0]; t=cv2.resize(t,(max(8,int(t.shape[1]*s)),84),interpolation=cv2.INTER_AREA); joined[form].append(b64jpg(t,82))
for page,ls in FS.items():
    for li,spans in ls.items():
        for i,j,w in spans:
            if w=='AND' and j-i==1: add('AND',page,li,i,j)
            if w=='THE' and j-i==1: add('THE',page,li,i,j)
            if w.endswith('ING') and j-i>=2 and len(w)>5: add('ING',page,li,j-2,j)
            if w in ('THIS','THAN','THAT','THIRTY') and j-i>=3: add('TH',page,li,i,i+1)
            if w in ('WHENEVER','WHAT','WHILE','WHERE'): add('WH',page,li,i,i+1)
for page,ls in json.load(open('explicit_labels.json')).items():
    for li,d in ls.items():
        for j,ch in d.items():
            if ch=='WH': add('WH',page,li,int(j),int(j)+1)
# page-1 tiles for fused pairs (blue key units)
S=4.725; units=pickle.load(open('blue_units.pkl','rb'))
img=cv2.imread('/Users/doranchak/projects/github/misc-crypto-mysteries/oliver-twist-thrift-store/book1.jpeg',0)
g=cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8)).apply(img)
by=collections.defaultdict(list)
for ln,r in units.items():
    for u,c in r: by[u].append((ln,c))
for L in ['CH','GH','ST','OU','CK','OO']:
    for ln,c in by.get(L,[])[:3]:
        cx=int(c['cx']*S); cy=int((c['cy']+22)*S); W,H=190,200
        x0=max(0,cx-W//2); y0=max(0,cy-H//2-10); t=g[y0:y0+H,x0:x0+W]
        t=cv2.copyMakeBorder(t,0,H-t.shape[0],0,W-t.shape[1],cv2.BORDER_CONSTANT,value=255)
        t=cv2.resize(t,(int(t.shape[1]*0.42),84),interpolation=cv2.INTER_AREA); joined[L].append(b64jpg(t,82))
# tiles for glyph units read from the aligned glyph boxes of pages 2-3 (SH, doubled letters, OU, OO)
RP=json.load(open('report_pages.json'))
for unit in ['SH','EE','TT','LL','SS','FF','CC','OU','OO']:
    joined[unit]=[]
    for pg in ('b2L','b2R','b3L','b3R'):
        for ln in RP[pg]['lines']:
            for gb in ln['glyphs']:
                if gb['t']==unit and gb['f'] in ('V','K'):
                    fl=FL[pg]; pad=10; x0=max(0,int(gb['x'])-pad); y0=max(0,int(gb['y'])-pad); x1=min(fl.shape[1],int(gb['x']+gb['w'])+pad); y1=min(fl.shape[0],int(gb['y']+gb['h'])+pad)
                    t=fl[y0:y1,x0:x1]; sc=84/t.shape[0]; t=cv2.resize(t,(max(8,int(t.shape[1]*sc)),84),interpolation=cv2.INTER_AREA); joined[unit].append(b64jpg(t,82))
joined={k:v[:6] for k,v in joined.items()}
json.dump(dict(alpha=alpha,joined=joined),open('report_alpha.json','w'))
print({k:(v['n'],len(v['tiles'])) for k,v in alpha.items()}); print({k:len(v) for k,v in joined.items()})
