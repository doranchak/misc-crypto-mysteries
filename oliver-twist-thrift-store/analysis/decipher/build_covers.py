import json, base64, cv2, numpy as np
import cover_seg as cs
OT=cs.OT
def b64jpg(img,q=70):
    ok,buf=cv2.imencode('.jpg',img,[cv2.IMWRITE_JPEG_QUALITY,q]); return base64.b64encode(buf).decode()
def norm_gray(img):
    g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) if img.ndim==3 else img
    bg=cv2.GaussianBlur(g,(0,0),45); n=cv2.divide(g,bg,scale=215)
    return np.clip(n,0,255).astype(np.uint8)
def word(t,f,gl=None,box=None):
    if gl:
        xa=min(g['x'] for g in gl); xb=max(g['x']+g['w'] for g in gl); ya=min(g['y'] for g in gl); yb=max(g['y']+g['h'] for g in gl)
    else: xa,ya,w,h=box; xb=xa+w; yb=ya+h
    return dict(t=t,x=float(xa),y=float(ya-38),w=float(xb-xa),h=float(yb-ya),f=f,c=1.0)
def line(n,i,crop,ox,oy,glyphs,words,band=46,maxw=1050,lbox=None):
    # strip = crop of the line region (not straightened); glyph coords are page-local
    xs=[g['x'] for g in glyphs]+([lbox[0]] if lbox else []); xe=[g['x']+g['w'] for g in glyphs]+([lbox[0]+lbox[2]] if lbox else [])
    ys=[g['y'] for g in glyphs]+([lbox[1]] if lbox else []); ye=[g['y']+g['h'] for g in glyphs]+([lbox[1]+lbox[3]] if lbox else [])
    x0=max(0,int(min(xs))-20); x1=min(crop.shape[1],int(max(xe))+20); y0=max(0,int(min(ys))-20); y1=min(crop.shape[0],int(max(ye))+20)
    out=crop[y0:y1,x0:x1]; f=min(1.0,maxw/out.shape[1])
    im=cv2.resize(out,None,fx=f,fy=f,interpolation=cv2.INTER_AREA) if f<1 else out
    h=im.shape[0]; im=np.vstack([im,np.full((band,im.shape[1]),255,np.uint8)])
    sg=[[round((g['x']+g['w']/2-x0)*f,1),g['t'],g['f'],g['c'],round(g['w']*f,1)] for g in glyphs]
    return dict(wo=(len(glyphs)==0),sw=im.shape[1],i=i,n=n,words=words,glyphs=glyphs,strip=b64jpg(im,66),sh=h,sg=sg,boxes=[[int(g['x']),int(g['y']),int(g['w']),int(g['h'])] for g in glyphs])
def page(crop,lines):
    h,w=crop.shape; sc=min(1.0,1300/w); im=cv2.resize(crop,(int(w*sc),int(h*sc)),interpolation=cv2.INTER_AREA)
    return dict(img=b64jpg(im,68),w=w,h=h,scale=sc,lines=lines)
def G(x,y,w,h,t,f='V'): return dict(x=float(x),y=float(y),w=float(w),h=float(h),t=t,f=f,c=1.0)
pages={}
# ------------------------------------------------ photo 4, left page: JAMES ANDERSEN
im4=cv2.imread(OT+'book4.jpeg'); g4=norm_gray(im4); s=4032/1400
PX,PY=420,780; crop=g4[PY:PY+560,PX:PX+1500]
ox,oy=int(225*s),int(335*s); reg=im4[oy:int(395*s),ox:int(600*s)]
bx=cs.comps(cs.ink(reg),minarea=80,dil=(5,5))
def U(idx):
    b=[bx[i] for i in idx]; x0=min(t[0] for t in b); y0=min(t[1] for t in b); x1=max(t[0]+t[2] for t in b); y1=max(t[1]+t[3] for t in b); return [x0,y0,x1-x0,y1-y0]
spec=[('J',[0,1]),('A',[2]),('M',[3]),('E',[4]),('S',[5,6]),('A',[7,8]),('NDER',[9,10]),('S',[11]),('E',[12]),('N',[13])]
gl=[]
for t,idx in spec:
    x,y,w,h=U(idx)
    if len(t)==1: gl.append(G(x+ox-PX,y+oy-PY,w,h,t))
    else:
        k=len(t)
        for j,ch in enumerate(t): gl.append(G(x+ox-PX+w*j/k,y+oy-PY,w/k,h,ch))
wj=[word('JAMES','V',gl[:5]),word('ANDERSEN','V',gl[5:])]
pages['b4L']=page(crop,[line(1,0,crop,PX,PY,gl,wj)])
# ------------------------------------------------ photo 4, right page
PX,PY=2250,520; crop=g4[PY:PY+2180,PX:PX+1780]
L=[]
big=[2498-PX,1677-PY,1350,675]; med=[2923-PX,2145-PY,640,175]; sm=[2966-PX,2433-PY,680,165]
L.append(line(1,0,crop,PX,PY,[],[word('D??IAN','V',box=big)],lbox=big))
L.append(line(2,1,crop,PX,PY,[],[word('DESIGNS','V',box=med)],lbox=med))
L.append(line(3,2,crop,PX,PY,[],[word('JIMANDERSEN','V',box=sm)],lbox=sm))
dg=[(3140,2540,40,100,'1'),(3182,2540,45,100,'9'),(3232,2540,40,100,'9'),(3267,2540,52,104,'6')]
gl=[G(x-PX,y-PY,w,h,t) for x,y,w,h,t in dg]
L.append(line(4,3,crop,PX,PY,gl,[word('1996','V',gl)]))
pages['b4R']=page(crop,L)
# ------------------------------------------------ photo 5: block-glyph digit row
im5=cv2.imread(OT+'book5.jpeg'); g5=norm_gray(im5)
PX,PY=420,2100; crop=g5[PY:PY+340,PX:PX+1900]
rb=[(84,96,93,115),(304,98,65,110),(482,85,91,123),(653,80,95,114),(842,79,88,109),(1022,81,64,109),(1149,86,67,125),(1316,80,86,133),(1475,81,77,120),(1671,96,73,119)]
gl=[G(x+500-PX,y+2150-PY,w,h,d) for (x,y,w,h),d in zip(rb,'1234567890')]
pages['b5']=page(crop,[line(1,0,crop,PX,PY,gl,[word('1234567890','V',gl)])])
json.dump(pages,open('report_pages_covers.json','w'))
print({k:(len(v['lines']),v['w'],v['h']) for k,v in pages.items()})
# debug overlay
for k,v in pages.items():
    pass
