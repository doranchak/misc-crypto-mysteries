# b2R line 16 piece 15 = the tall glyph of line 15 (between its I and N) fused with the dot/foot of line 16's R. Split it.
import pickle, numpy as np, cv2
A=pickle.load(open('allpieces.pkl','rb'))
L=A['b2R']['lines']
p=L[16][15]; r=L[16][14]
m=(p['mask']>0).astype(np.uint8); n,lab,st,_=cv2.connectedComponentsWithStats(m,connectivity=8)
big=1+int(np.argmax(st[1:,4])); mb=(lab==big).astype(np.uint8)*255
x0,y0=int(p['x']),int(p['y'])
ys,xs=np.nonzero(mb); bx0,by0,bx1,by1=xs.min(),ys.min(),xs.max()+1,ys.max()+1
newp=dict(p); newp['mask']=mb[by0:by1,bx0:bx1]; newp['x']=np.int64(x0+bx0); newp['y']=np.int64(y0+by0); newp['w']=np.int64(bx1-bx0); newp['h']=np.int64(by1-by0)
newp['cx']=newp['x']+newp['w']/2; newp['cy']=newp['y']+newp['h']/2
# the leftover fragments (R's dot and foot) go to line 16's R piece (index 14)
rest=((lab>0)&(lab!=big)).astype(np.uint8)*255
rx0,ry0=int(r['x']),int(r['y'])
ux0=min(rx0,x0); uy0=min(ry0,y0); ux1=max(rx0+int(r['w']),x0+int(p['w'])); uy1=max(ry0+int(r['h']),y0+int(p['h']))
full=np.zeros((uy1-uy0,ux1-ux0),np.uint8)
rm=(r['mask']>0).astype(np.uint8)*255; full[ry0-uy0:ry0-uy0+rm.shape[0],rx0-ux0:rx0-ux0+rm.shape[1]]|=rm
full[y0-uy0:y0-uy0+rest.shape[0],x0-ux0:x0-ux0+rest.shape[1]]|=rest
rx0,ry0=ux0,uy0
ys,xs=np.nonzero(full); fx0,fy0,fx1,fy1=xs.min(),ys.min(),xs.max()+1,ys.max()+1
r2=dict(r); r2['mask']=full[fy0:fy1,fx0:fx1]; r2['x']=np.int64(rx0+fx0); r2['y']=np.int64(ry0+fy0); r2['w']=np.int64(fx1-fx0); r2['h']=np.int64(fy1-fy0); r2['cx']=r2['x']+r2['w']/2; r2['cy']=r2['y']+r2['h']/2
print('R',(int(r['x']),int(r['y']),int(r['w']),int(r['h'])),'->',(int(r2['x']),int(r2['y']),int(r2['w']),int(r2['h'])),'new',(int(newp['x']),int(newp['y']),int(newp['w']),int(newp['h'])))
L[16][14]=r2; del L[16][15]
# insert the glyph into line 15 in x order
l15=L[15]; k=next(i for i,q in enumerate(l15) if q['x']>newp['x']); print('insert at',k,'of',len(l15)); l15.insert(k,newp)
pickle.dump(A,open('allpieces.pkl','wb'))
