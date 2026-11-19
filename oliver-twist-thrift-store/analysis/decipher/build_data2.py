import sys, json, pickle, base64, re
import numpy as np, cv2
import boot, strips, selftrain as st, align, label1
SP_LT=label1.LT
FD=pickle.load(open('final_decode.pkl','rb'))
import os
GM=json.load(open('glyph_map.json')) if os.path.exists('glyph_map.json') else {}
EXTRA=json.load(open('extra_glyphs.json')) if os.path.exists('extra_glyphs.json') else {}   # words whose pieces were lost: explicit boxes (flat-page pixels)
lab=boot.build_train(boot.load_ver()); st.lab_ver=lab
trn=np.array(sorted(lab)); tl=[lab[i] for i in trn]; clf=st.fit(lab)
B1flat=pickle.load(open('b1_pieces.pkl','rb'))['flat']
flats={'b1':B1flat}
for t in ['b2L','b2R','b3L','b3R']: flats[t]=boot.A[t]['flat']
def b64jpg(img,q=66):
    ok,buf=cv2.imencode('.jpg',img,[cv2.IMWRITE_JPEG_QUALITY,q]); return base64.b64encode(buf).decode()
tracks=[(126,0.0084),(308,-0.0174),(509,0.0101),(690,0.0),(856,-0.0137),(1072,0.0023),(1269,0.0077),(1458,0.0058),(1616,0.0),(1781,-0.0251),(1997,-0.0308),(2195,-0.0121),(2350,0.0041)]
PT1=["I BOUGHT THIS BOOK ON THE DAY","OF SEAN FLECKENSTEIN'S WED","DING AT THE LEACH BOTANICAL","GARDENS","THE DATE IS JUNE NINTH 1996",
     "TODAY MY FRIEND SEAN MARIED","GWENETH LURID I WENT TO THE","CEREMONY WITH MELANIE BUD","AND NICK","IT'S REALY RATHER FITING THAT I",
     "PURCHASED THIS BOOK TODAY I'VE","BEEN THINKING ABOUT GETTING A SPECIAL","BOOK TO CHRONICLE MY TRIALS AND"]
SKIP=set()
# block-hand digit headings (digit key = the row on photo 5: 1 2 3 4 5 6 7 8 9 0): YYMMDD . HH:MM
HEADS={'b3R:0':dict(pieces=list(range(10)),digits='9606111831',text='960611.18:31'),
       'b3L:3':dict(pieces=list(range(4,14)),digits='9606111811',text='960611.18:11')}
def straighten_line(flat,pcs):
    pc=[dict(cx=p['x']+p['w']/2,cy=p['y']+p['h']/2,h=p['h']) for p in pcs]
    hm=float(np.median([p['h'] for p in pc]))
    out,(x0,x1,co)=strips.straighten(flat,pc,up=int(0.95*hm),dn=int(0.80*hm))
    return out,x0
def make_strip(out,x0,glyphs,band=46,maxw=1050):
    f=min(1.0,maxw/out.shape[1]); 
    im=cv2.resize(out,None,fx=f,fy=f,interpolation=cv2.INTER_AREA) if f<1 else out
    h=im.shape[0]; im=np.vstack([im,np.full((band,im.shape[1]),255,np.uint8)])
    sg=[[round((g['x']+g['w']/2-x0)*f,1),g['t'],g['f'],g['c'],round(g['w']*f,1)] for g in glyphs]
    return im,h,sg,im.shape[1]-0
pages={}
for t,fl in flats.items():
    h,w=fl.shape; sc=min(1.0,1300/w); im=cv2.resize(fl,(int(w*sc),int(h*sc)),interpolation=cv2.INTER_AREA)
    pages[t]=dict(img=b64jpg(im,66),w=w,h=h,scale=sc,lines=[])
def word_obj(t,f,c,gl):
    xa=min(g['x'] for g in gl); xb=max(g['x']+g['w'] for g in gl); ya=min(g['y'] for g in gl); yb=max(g['y']+g['h'] for g in gl)
    return dict(t=t,x=float(xa),y=float(ya-38),w=float(xb-xa),h=float(yb-ya),f=f,c=float(c))
# ---------------------------------------------------------------- page 1 (key)
for li,text in enumerate(PT1):
    pcs_all=boot.lines_of('b1')[li]
    pcs=[p for p in pcs_all if p['h']>=60 and p['w']>=28]; pcs.sort(key=lambda p:p['x'])
    # logP for these pieces: use whole-line logP and index map
    lp_all=st.line_logp('b1',li,clf,trn,tl); idxmap={id(p):k for k,p in enumerate(pcs_all)}
    lp=np.array([lp_all[idxmap[id(p)]] for p in pcs])
    toks=text.split(); digits=None
    if toks[-1] in ('199?','1996'): digits=toks.pop()
    words=[w.replace('.','') for w in toks]
    letters=''.join(words)
    xs=None
    if li<12:
        LT=SP_LT[li]; xs=[]; k=0
        for ch in letters:
            if ch=="'": xs.append(None)
            else: xs.append(LT[k][1] if k<len(LT) else None); k+=1
    brk=set(); pos=0
    for w in words: brk.add(pos); pos+=len(w)
    items,cost=align.align(pcs,lp,letters,xs=xs,breaks=brk)
    boxes=align.merge_boxes(pcs,items)
    glyphs=[]; wobjs=[]
    # word spans over letter index
    starts=[]; pos=0
    for w in words: starts.append((pos,pos+len(w),w)); pos+=len(w)
    for (xx,yy,ww,hh,tt,it,k0) in boxes:
        glyphs.append(dict(x=float(xx),y=float(yy),w=float(ww),h=float(hh),t=tt,f='K',c=1.0,k0=k0))
    for a,b,w in starts:
        gl=[g for g in glyphs if a<=g['k0']<b]
        if gl: wobjs.append(word_obj(w,'K',1.0,gl))
    if digits:
        lastx=max([g['x']+g['w'] for g in glyphs]) if glyphs else 0
        right=[p for p in pcs if p['x']>=lastx-5 and p['h']>=90]
        right=sorted(sorted(right,key=lambda p:-p['w']*p['h'])[:4],key=lambda p:p['x'])
        for p,ch in zip(right,"1996"):     # block-hand digits: 1,9,9 given by the key, the 4th (6) read from the digit row on photo 5
            glyphs.append(dict(x=float(p['x']),y=float(p['y']),w=float(p['w']),h=float(p['h']),t=ch,f='K' if ch!='6' else 'V',c=1.0,k0=999))
        if right: wobjs.append(word_obj('1996','V',1.0,[g for g in glyphs if g['k0']==999]))
    out,x0=straighten_line(B1flat,pcs)
    im,h,sg,sw=make_strip(out,x0,glyphs)
    pages['b1']['lines'].append(dict(sw=sw,i=li,n=li+1,words=wobjs,glyphs=[{k:v for k,v in g.items() if k!='k0'} for g in glyphs],strip=b64jpg(im,66),sh=h,sg=sg,
        boxes=[[int(p['x']),int(p['y']),int(p['w']),int(p['h'])] for p in pcs_all]))
# ---------------------------------------------------------------- pages 2-3
for page in ['b2L','b2R','b3L','b3R']:
    flat=flats[page]; seq=0
    for li,pcs in enumerate(boot.lines_of(page)):
        key=f'{page}:{li}'
        if key in HEADS:
            H=HEADS[key]; sel=[pcs[j] for j in H['pieces']]
            out,x0=straighten_line(flat,sel); seq+=1
            glyphs=[dict(x=float(p['x']),y=float(p['y']),w=float(p['w']),h=float(p['h']),t=d,f='V',c=1.0) for p,d in zip(sel,H['digits'])]
            wo=word_obj(H['text'],'V',1.0,glyphs)
            im,h,sg,sw=make_strip(out,x0,glyphs)
            pages[page]['lines'].append(dict(sw=sw,i=li,n=seq,words=[wo],glyphs=glyphs,strip=b64jpg(im,66),sh=h,sg=sg,boxes=[[int(p['x']),int(p['y']),int(p['w']),int(p['h'])] for p in pcs]))
            continue
        if key not in FD or key in SKIP: continue
        pcs2=[p for p in pcs if p['h']>=45 and p['w']>=18]
        virt=[dict(x=g['box'][0],y=g['box'][1],w=g['box'][2],h=g['box'][3]) for ex in EXTRA.get(key,[]) for g in ex['glyphs']]
        try: out,x0=straighten_line(flat,pcs2+virt)
        except Exception: continue
        seq+=1
        lp=st.line_logp(page,li,clf,trn,tl)
        glyphs=[]; wobjs=[]
        for (i,j,w,f,c) in FD[key]:
            seg=pcs[i:j]
            if not seg: continue
            if key=='b2R:1' and False: pass
            items=None; direct=[]
            if key in GM:   # hand-specified glyph partition (user-verified reading): [pieces..., text]  or  {box,t,p} (explicit box in page pixels)
                k0=0; its=[]; dd=[]
                for x in GM[key]:
                    if isinstance(x,dict): anchor=x['p'][0]; txt=x['t']
                    else: anchor=x[0]; txt=x[-1]
                    if i<=anchor<j:
                        if isinstance(x,dict): dd.append((x['box'],txt,k0))
                        else: its.append((tuple(p-i for p in x[:-1]),txt,k0))
                        k0+=len(txt)
                if (its or dd) and ''.join(t for _,t,_ in sorted(its+[(None,t,k) for _,t,k in dd],key=lambda a:a[2]))==w.upper(): items=its; direct=dd
            if items is None: items,_=align.align(seg,lp[i:j],w.upper())
            boxes=align.merge_boxes(seg,items) if items else []; gl=[]
            for (xx,yy,ww,hh,tt,it,k0) in boxes:
                gl.append(dict(x=float(xx),y=float(yy),w=float(ww),h=float(hh),t=tt,f=f,c=float(c)))
            for (bx,txt,k0) in direct:
                gl.append(dict(x=float(bx[0]),y=float(bx[1]),w=float(bx[2]),h=float(bx[3]),t=txt,f=f,c=float(c)))
            glyphs+=gl
            if gl: wobjs.append(word_obj(w.upper(),f,c,gl))
        for ex in EXTRA.get(key,[]):
            gl=[dict(x=float(g['box'][0]),y=float(g['box'][1]),w=float(g['box'][2]),h=float(g['box'][3]),t=g['t'],f='V',c=1.0) for g in ex['glyphs']]
            glyphs+=gl; wobjs.append(word_obj(ex['word'],'V',1.0,gl))
        wobjs.sort(key=lambda w:w['x'])
        glyphs.sort(key=lambda g:g['x'])
        im,h,sg,sw=make_strip(out,x0,glyphs)
        pages[page]['lines'].append(dict(sw=sw,i=li,n=seq,words=wobjs,glyphs=glyphs,strip=b64jpg(im,66),sh=h,sg=sg,
            boxes=[[int(p['x']),int(p['y']),int(p['w']),int(p['h'])] for p in pcs]))
# b3L lines 21 (THIS IS ALL WORTHWHILE) and 20 (I AM READY TO) are the left and right halves of ONE text line: read 21 first
L=pages['b3L']['lines']; a=[k for k,x in enumerate(L) if x['i']==20]; c=[k for k,x in enumerate(L) if x['i']==21]
if a and c and a[0]<c[0]: L[a[0]],L[c[0]]=L[c[0]],L[a[0]]
for k,x in enumerate(L): x['n']=k+1
json.dump(pages,open('report_pages.json','w'))
print({t:len(v['lines']) for t,v in pages.items()})
