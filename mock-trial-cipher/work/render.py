import json, cv2, numpy as np, sys, os
S=4
im = cv2.imread('original.png',0)
big = cv2.resize(im,None,fx=S,fy=S,interpolation=cv2.INTER_CUBIC)
vis0=cv2.cvtColor(big,cv2.COLOR_GRAY2BGR)
centers=json.load(open('work/lines.json'))['centers']
lines=json.load(open('work/lines3.json'))
labels={}
if os.path.exists('work/labels.json'):
    labels=json.load(open('work/labels.json'))
def render_line(j,half):
    c=centers[j]
    y0=max(0,int((c-24)*S)); y1=int((c+24)*S)
    x0,x1=[(100,1300),(1180,2400)][half]
    t=vis0[y0:y1,x0:x1].copy()
    bs=lines[j]
    lab=labels.get(str(j))
    for k,b in enumerate(bs):
        x,y,w,h=b
        if x+w<x0 or x>x1: continue
        col=(0,0,255) if k%2==0 else (255,0,0)
        cv2.rectangle(t,(x-x0,y-y0),(x-x0+w,y-y0+h),col,1)
        cv2.putText(t,f'{k}',(x-x0+2,max(14,y-y0-3)),cv2.FONT_HERSHEY_SIMPLEX,0.6,col,2)
        if lab and k<len(lab):
            cv2.putText(t,lab[k],(x-x0+w//2-8,y1-y0-6),cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,120,0),2)
    return t
if __name__=='__main__':
    js=[int(a) for a in sys.argv[2:]]
    half=int(sys.argv[1])
    ims=[render_line(j,half) for j in js]
    cv2.imwrite('work/stack.png',np.vstack(ims))
