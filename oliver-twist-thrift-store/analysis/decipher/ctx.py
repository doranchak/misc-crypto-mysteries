import sys, boot, numpy as np, cv2, pickle
FL={'b1':pickle.load(open('b1_pieces.pkl','rb'))['flat']}
for t in ['b2L','b2R','b3L','b3R']: FL[t]=boot.A[t]['flat']
def tile(page,li,j,span=3,scale=1.6,label=True):
    pcs=boot.lines_of(page)[li]; fl=FL[page]
    a=pcs[max(0,j-span)]; b=pcs[min(len(pcs)-1,j+span)]
    x0=max(0,int(min(a['x'],b['x'])-30)); x1=int(max(a['x']+a['w'],b['x']+b['w'])+30)
    y0=max(0,int(min(p['y'] for p in pcs[max(0,j-span):j+span+1])-30)); y1=int(max(p['y']+p['h'] for p in pcs[max(0,j-span):j+span+1])+30)
    t=cv2.cvtColor(fl[y0:y1,x0:x1],cv2.COLOR_GRAY2BGR)
    for k in range(max(0,j-span),min(len(pcs),j+span+1)):
        p=pcs[k]; col=(0,0,255) if k==j else (200,120,0)
        cv2.rectangle(t,(int(p['x']-x0),int(p['y']-y0)),(int(p['x']+p['w']-x0),int(p['y']+p['h']-y0)),col,2)
        cv2.putText(t,str(k),(int(p['x']-x0),max(12,int(p['y']-y0)-4)),cv2.FONT_HERSHEY_SIMPLEX,0.6,col,2)
    t=cv2.resize(t,None,fx=scale,fy=scale,interpolation=cv2.INTER_CUBIC)
    if label: cv2.putText(t,f'{page}:{li}:{j}',(4,18),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,0,0),2)
    return t
if __name__=='__main__':
    ts=[tile(a.split(':')[0],int(a.split(':')[1]),int(a.split(':')[2])) for a in sys.argv[2:]]
    W=max(t.shape[1] for t in ts)
    ts=[cv2.copyMakeBorder(t,0,6,0,W-t.shape[1],cv2.BORDER_CONSTANT,value=(255,255,255)) for t in ts]
    cv2.imwrite(sys.argv[1],np.vstack(ts))
