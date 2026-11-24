import json, cv2, numpy as np, sys
S=4
im = cv2.imread('original.png',0)
big = cv2.resize(im,None,fx=S,fy=S,interpolation=cv2.INTER_CUBIC)
d=json.load(open('work/tracked.json')); bs=d['boxes']; lines=d['lines']
T=104
def thumb(b,k,gap):
    x,y,w,h=b
    pad=10
    c=big[max(0,y-pad):y+h+pad, max(0,x-pad):x+w+pad]
    m=max(c.shape[:2]); sc=(T-16)/m
    c=cv2.resize(c,(max(1,int(c.shape[1]*sc)),max(1,int(c.shape[0]*sc))),interpolation=cv2.INTER_AREA)
    t=np.full((T+14,T),255,np.uint8)
    oy=14+(T-c.shape[0])//2; ox=(T-c.shape[1])//2
    t[oy:oy+c.shape[0],ox:ox+c.shape[1]]=c
    t=cv2.cvtColor(t,cv2.COLOR_GRAY2BGR)
    cv2.putText(t,str(k),(2,11),cv2.FONT_HERSHEY_SIMPLEX,0.45,(0,0,255),1)
    cv2.rectangle(t,(0,0),(T-1,T+13),(200,200,200),1)
    if gap: cv2.rectangle(t,(0,0),(5,T+13),(0,0,255),-1)
    return t
def line_rows(j,per=13):
    ch=lines[j]
    ts=[]
    for k,i in enumerate(ch):
        b=bs[i]
        gap=False
        if k>0:
            p=bs[ch[k-1]]; gap=(b[0]-(p[0]+p[2]))>38
        ts.append(thumb(b,k,gap))
    rows=[]
    for s in range(0,len(ts),per):
        r=ts[s:s+per]
        while len(r)<per: r.append(np.full_like(ts[0],255))
        row=np.hstack(r)
        cv2.putText(row,f'L{j}',(2,T+10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2)
        rows.append(row)
    return rows
if __name__=='__main__':
    js=[int(a) for a in sys.argv[1:]]
    rows=[]
    for j in js: rows+=line_rows(j)
    cv2.imwrite('work/thumbs.png',np.vstack(rows)); print(np.vstack(rows).shape)
