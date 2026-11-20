"""Build 3-row ternary words from red glyphs.  0 = empty, 1 = square, 2 = diagonal stroke.
Each glyph (connected component) -> 3 x ncols matrix; row frame comes from the line's 3-row glyphs.
Writes figures/red_words.json.   Run: /opt/homebrew/bin/python3.11 -I scripts/red_words.py"""
import cv2, numpy as np, json, os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
im=cv2.imread(os.path.join(ROOT,'pic1.jpeg'))
B,G,R=[im[:,:,i].astype(int) for i in range(3)]
red45=((R-G>45)&(R-B>20)).astype(np.uint8); red45[:1300]=0; red45[2330:]=0
d=cv2.dilate(red45,cv2.getStructuringElement(cv2.MORPH_RECT,(25,25)))
n,lab,st,cen=cv2.connectedComponentsWithStats(d)
marks=json.load(open(os.path.join(ROOT,'figures','red_marks.json')))
P=47.0; DIAG=P*np.sqrt(2)
def comp_of(x,y):
    xi,yi=int(round(x)),int(round(y))
    l=lab[min(max(yi,0),lab.shape[0]-1),min(max(xi,0),lab.shape[1]-1)]
    if l: return int(l)
    r=40; sub=lab[max(0,yi-r):yi+r,max(0,xi-r):xi+r]; v=sub[sub>0]
    return int(np.bincount(v).argmax()) if len(v) else 0
G={}
for s in marks['squares']:
    c=comp_of(s['x'],s['y']); G.setdefault(c,{'pts':[]})['pts'].append(('sq',s['x'],s['y'],s['x'],s['y']))
for s in marks['strokes']:
    if not(25<s['ang']<75 and s['len']>35): continue
    c=comp_of((s['x0']+s['x1'])/2,(s['y0']+s['y1'])/2)
    k=max(1,int(round((s['len']+10)/DIAG)))
    xs=np.linspace(s['x0'],s['x1'],2*k+1)[1::2]; ys=np.linspace(s['y0'],s['y1'],2*k+1)[1::2]
    for x,y in zip(xs,ys): G.setdefault(c,{'pts':[]})['pts'].append(('st',x,y,s['x0'],s['y0']))
def line_of(y): return 1 if y<1560 else 2 if y<1780 else 3 if y<2000 else 4
info={}
for c,g in G.items():
    if c==0: continue
    pts=g['pts']
    sq=np.array([[p[1],p[2]] for p in pts if p[0]=='sq']).reshape(-1,2)
    ends=np.array([[p[3],p[4]] for p in pts if p[0]=='st']).reshape(-1,2)
    best=None
    for ox in np.arange(0,P,3):
        for oy in np.arange(0,P,3):
            cost=0
            if len(sq):
                fx=(sq[:,0]-ox)/P-0.5; fy=(sq[:,1]-oy)/P-0.5; cost+=np.sum(abs(fx-np.round(fx))+abs(fy-np.round(fy)))
            if len(ends):
                fx=(ends[:,0]-ox)/P; fy=(ends[:,1]-oy)/P; cost+=0.5*np.sum(abs(fx-np.round(fx))+abs(fy-np.round(fy)))
            if best is None or cost<best[0]: best=(cost,ox,oy)
    _,ox,oy=best
    cells={}
    for p in pts:
        key=(int(np.floor((p[2]-oy)/P)),int(np.floor((p[1]-ox)/P)))
        if p[0]=='sq': cells[key]=1
        elif key not in cells: cells[key]=2
    r0=min(k[0] for k in cells); r1=max(k[0] for k in cells); c0=min(k[1] for k in cells); c1=max(k[1] for k in cells)
    x,y,w,h,a=st[c]
    info[c]=dict(cells=cells,ox=ox,oy=oy,r0=r0,r1=r1,c0=c0,c1=c1,bbox=(int(x),int(y),int(w),int(h)),line=line_of(y+h/2),cx=x+w/2)
# frame per line from 3-row glyphs
frames={}
for c,v in info.items():
    if v['r1']-v['r0']==2: frames.setdefault(v['line'],[]).append((v['cx'],v['oy']+v['r0']*P))
for L in frames: frames[L].sort()
def frame_top(L,x):
    f=frames[L]; xs=np.array([a for a,_ in f]); ys=np.array([b for _,b in f])
    w=1/(np.abs(xs-x)+150.0)**2
    return float((w*ys).sum()/w.sum())
words={1:[],2:[],3:[],4:[]}; warn=0
for c,v in sorted(info.items(),key=lambda kv:(kv[1]['line'],kv[1]['cx'])):
    L=v['line']
    if v['r1']-v['r0']==2: rowoff=v['r0']  # absolute row index of top frame row
    else:
        ft=frame_top(L,v['cx']); rowoff=int(round((ft-v['oy'])/P))
    cols=[]
    for cc in range(v['c0'],v['c1']+1):
        col=[]
        for rr in range(3):
            col.append(v['cells'].get((rowoff+rr,cc),0))
        cols.append(col)
    out_of=[k for k in v['cells'] if not(rowoff<=k[0]<=rowoff+2)]
    if out_of: warn+=1
    words[L].append(dict(comp=c,cols=cols,out_of_frame=len(out_of)))
print('glyphs with marks outside 3-row frame:',warn)
json.dump(words,open(os.path.join(ROOT,'figures','red_words.json'),'w'))
tot=0
for L in (1,2,3,4):
    print('--- line',L)
    for w in words[L]:
        s=' '.join(''.join('.#\\'[x] for x in col) for col in w['cols'])
        print(f"{w['comp']:3d}{'!' if w['out_of_frame'] else ' '} {s}"); tot+=len(w['cols'])
print('total columns',tot)
