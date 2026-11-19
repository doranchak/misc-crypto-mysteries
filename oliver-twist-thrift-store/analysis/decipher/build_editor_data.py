import sys, json, pickle, base64, re
import numpy as np, cv2
sys.path.insert(0,'..')
import strips
OT='/Users/doranchak/projects/github/misc-crypto-mysteries/oliver-twist-thrift-store/'
html=open(OT+'report.html').read()
m=re.search(r'const PAGES=(\{.*?\});\nconst ALPHA=',html,re.S)
REP=json.loads(m.group(1))
B1=pickle.load(open('b1_pieces.pkl','rb')); A=pickle.load(open('allpieces.pkl','rb'))
flats={'b1':B1['flat']}; lines_of={'b1':B1['lines']}
for t in ['b2L','b2R','b3L','b3R']: flats[t]=A[t]['flat']; lines_of[t]=A[t]['lines']
NAMES={'b1':'Page 1 (photo 1)','b2L':'Spread 2 · left page (photo 2)','b2R':'Spread 2 · right page (photo 2)','b3L':'Spread 3 · left page (photo 3)','b3R':'Spread 3 · right page (photo 3)'}
INCL={'b1':list(range(13)),'b2L':[4,5,6,7,8,9,10],'b2R':list(range(18)),
      'b3L':[3,5,6,7,9,11,13,14,15,16,18,19,20,21,22,23],'b3R':[0]+list(range(1,7))+list(range(8,21))}
def b64(img,q=62):
    ok,buf=cv2.imencode('.jpg',img,[cv2.IMWRITE_JPEG_QUALITY,q]); return base64.b64encode(buf).decode()
def merge_pieces(pcs):
    pcs=sorted(pcs,key=lambda p:p['x']); out=[]
    for p in pcs:
        q=dict(x=p['x'],y=p['y'],w=p['w'],h=p['h'])
        if out:
            o=out[-1]; ov=min(o['x']+o['w'],q['x']+q['w'])-max(o['x'],q['x'])
            if ov>0.6*min(o['w'],q['w']):
                x0=min(o['x'],q['x']); y0=min(o['y'],q['y']); x1=max(o['x']+o['w'],q['x']+q['w']); y1=max(o['y']+o['h'],q['y']+q['h'])
                o.update(x=x0,y=y0,w=x1-x0,h=y1-y0); continue
        out.append(q)
    return out
pages=[]
for page in ['b1','b2L','b2R','b3L','b3R']:
    flat=flats[page]; H,W=flat.shape
    ow=700; osc=ow/W; ov=cv2.resize(flat,(ow,int(H*osc)),interpolation=cv2.INTER_AREA)
    refmap={L['i']:L['words'] for L in REP[page]['lines']}
    mh,mw=(60,28) if page=='b1' else (45,18)
    lines=[]; n=0
    for li in INCL[page]:
        pcs=[p for p in lines_of[page][li] if p['h']>=mh and p['w']>=mw]
        if page=='b3L':   # drop spine-shading noise (same rules as the first pipeline, y shifted for the larger box)
            pcs=[p for p in pcs if p['x']>=30 and not (p['x']<140 and (p['y']<640 or p['y']>1730)) and not (p['x']>1600 and p['w']/p['h']>2.2)]
        if len(pcs)<2: continue
        n+=1
        pc=[dict(cx=p['x']+p['w']/2,cy=p['y']+p['h']/2,h=p['h']) for p in pcs]
        hm=float(np.median([p['h'] for p in pc]))
        up=int(1.0*hm)
        out,(x0,x1,co)=strips.straighten(flat,pc,up=up,dn=int(1.0*hm))
        mp=merge_pieces(pcs); boxes=[]; ms=[]
        for p in mp:
            cx=p['x']+p['w']/2; cy=p['y']+p['h']/2; yc=up+(cy-np.polyval(co,cx))
            boxes.append([round(float(p['x']-x0),1),round(float(yc-p['h']/2),1),round(float(p['w']),1),round(float(p['h']),1)])
            ms.append(round(float(cx-x0),1))
        ref=[[w['t'],w['f'],round(w.get('c',1.0),2)] for w in refmap.get(li,[])]
        xs=[p['x'] for p in pcs]; xe=[p['x']+p['w'] for p in pcs]; ys=[p['y'] for p in pcs]; ye=[p['y']+p['h'] for p in pcs]
        rect=[round(min(xs)*osc,1),round(min(ys)*osc,1),round((max(xe)-min(xs))*osc,1),round((max(ye)-min(ys))*osc,1)]
        frect=[round(float(min(xs)),1),round(float(min(ys)),1),round(float(max(xe)-min(xs)),1),round(float(max(ye)-min(ys)),1)]
        lines.append(dict(id=f'{page}:{li}',n=n,w=int(out.shape[1]),h=int(out.shape[0]),img=b64(out),m=ms,boxes=boxes,ref=ref,rect=rect,frect=frect))
    # full-resolution page image (flat coordinates = piece coordinates) for the free letter boxes
    pages.append(dict(id=page,name=NAMES[page],overview=b64(ov,60),ow=ow,oh=int(ov.shape[0]),lines=lines,full=b64(flat,50),fw=int(W),fh=int(H),fs=1.0))
    print(page,len(lines),'lines',sum(len(l['img']) for l in lines)//1000,'KB',sum(len(l['m']) for l in lines),'markers')
json.dump(dict(pages=pages),open('editor_data.json','w'),separators=(',',':'))
