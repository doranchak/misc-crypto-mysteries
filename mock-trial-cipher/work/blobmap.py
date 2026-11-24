import json, numpy as np
S=4
blobs=json.load(open('work/blobs.json'))
d=json.load(open('work/tracked.json')); bs=d['boxes']; lines=d['lines']
# nearest-box line membership
owner=[]
for b in blobs:
    cx,cy=b['cx'],b['cy']
    best=None
    for j,ch in enumerate(lines):
        for k,i in enumerate(ch):
            x,y,w,h=bs[i]
            bcx,bcy=x+w/2,y+h/2
            dd=np.hypot(cx-bcx,(cy-bcy)*1.3)
            if best is None or dd<best[0]: best=(dd,j,k)
    owner.append(best)
byline={}
for b,o in zip(blobs,owner):
    b['line']=o[1]; b['k']=o[2]; b['dist']=o[0]
    byline.setdefault(o[1],[]).append(b)
tr=[l.split() for l in open('work/transcript_v1.txt')]
for j in range(26):
    bl=sorted(byline.get(j,[]),key=lambda b:b['cx'])
    tf=[t for t in tr[j] if t in 'APTQ']
    print(j,len(bl),len(tf),[ (int(b['cx']/4),round(b['dist'])) for b in bl])
json.dump(blobs,open('work/blobs2.json','w'))
