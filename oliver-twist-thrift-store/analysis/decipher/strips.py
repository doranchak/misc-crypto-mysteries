import sys; sys.path.insert(0,'..')
import cv2, numpy as np, pickle, collections
import glyphlib, final_b2 as fb
CFG={'b2L':('book2.jpeg',(330,40,2050,1350),-4.75,None),
     'b2R':('book2.jpeg',(2050,150,3950,2750),-1.0,'b2R'),
     'b3L':('book3.jpeg',(30,700,1950,2750),-4.25,None),
     'b3R':('book3.jpeg',(1900,150,3950,2750),-1.75,None)}
def mask_b2R(th):
    th=th.copy(); th[80+100:760+100,640:1900]=0; return th
def chain_lines(ps,tol=0.5,maxdx=330):
    ps=sorted(ps,key=lambda p:p['cx']); hmed=np.median([p['h'] for p in ps]); par=list(range(len(ps)))
    def find(a):
        while par[a]!=a: par[a]=par[par[a]]; a=par[a]
        return a
    for i,p in enumerate(ps):
        best=None
        for j in range(i-1,-1,-1):
            q=ps[j]; dx=p['cx']-q['cx']
            if dx>maxdx: break
            dy=abs(p['cy']-q['cy'])
            if dx<5 and dy<5: continue
            if dy<tol*hmed:
                sc=dx+3*dy
                if best is None or sc<best[0]: best=(sc,j)
        if best: par[find(i)]=find(best[1])
    comps=collections.defaultdict(list)
    for i,p in enumerate(ps): comps[find(i)].append(p)
    return [sorted(c,key=lambda p:p['x']) for c in comps.values()]
def prep(tag):
    name,box,rot,mk=CFG[tag]
    reg,flat,lab,units=fb.extract(name,box,rot,mask_b2R if mk=='b2R' else None)
    for u in units: u['cx']=u['x']+u['w']/2; u['cy']=u['y']+u['h']/2
    units=[u for u in units if u['h']>=45]
    lines=[l for l in chain_lines(units) if len(l)>=3]
    lines.sort(key=lambda l:np.mean([p['cy'] for p in l]))
    return flat,lines
def straighten(flat,pcs,up=95,dn=85,deg=2):
    xs=np.array([p['cx'] for p in pcs]); ys=np.array([p['cy'] for p in pcs])
    deg=min(deg,max(1,len(pcs)//6))
    co=np.polyfit(xs,ys,deg)
    x0=int(max(0,xs.min()-80)); x1=int(min(flat.shape[1],xs.max()+80))
    W=x1-x0; H=up+dn
    X=np.tile(np.arange(x0,x1,dtype=np.float32),(H,1))
    base=np.polyval(co,np.arange(x0,x1)).astype(np.float32)
    Y=np.tile(np.arange(-up,dn,dtype=np.float32)[:,None],(1,W))+base[None,:]
    out=cv2.remap(flat,X,Y,cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)
    return out,(x0,x1,co)
if __name__=='__main__':
    for tag in sys.argv[1:]:
        flat,lines=prep(tag)
        cv2.imwrite(f'../lines/{tag}_flat.png',flat)
        pickle.dump([[dict(x=int(p['x']),y=int(p['y']),w=int(p['w']),h=int(p['h'])) for p in l] for l in lines],open(f'../lines/{tag}_units.pkl','wb'))
        vis=cv2.cvtColor(flat,cv2.COLOR_GRAY2BGR)
        for i,l in enumerate(lines):
            for p in l: cv2.rectangle(vis,(p['x'],p['y']),(p['x']+p['w'],p['y']+p['h']),(0,0,255),2)
            cv2.putText(vis,str(i+1),(int(l[0]['x'])-5,int(l[0]['y'])),cv2.FONT_HERSHEY_SIMPLEX,1.6,(255,0,0),4)
        cv2.imwrite(f'../lines/{tag}_ov.png',cv2.resize(vis,None,fx=0.7,fy=0.7))
        print(tag,[len(l) for l in lines])
