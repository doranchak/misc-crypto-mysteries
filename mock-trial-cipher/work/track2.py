import json, numpy as np
S=4
bs=json.load(open('work/gboxes.json'))
bs=[b for b in bs if b[2]*b[3]>1500]
starts=[24,58,103,134,172,248,278,310,343,374,405,447,478,511,550,588,620,680,715,743,773,802,826,872,902,934]
cy=lambda b:b[1]+b[3]/2
used=set()
lines=[]
for c0 in starts:
    cand=[(i,b) for i,b in enumerate(bs) if b[0]/S<80 and abs(cy(b)/S-c0)<15 and i not in used]
    if not cand: print('no start',c0); lines.append([]); continue
    i0,b0=min(cand,key=lambda t:(abs(cy(t[1])/S-c0)+ t[1][0]/S*0.1))
    chain=[i0]; used.add(i0)
    while True:
        last=bs[chain[-1]]
        pts=[bs[i] for i in chain[-5:]]
        if len(pts)>=3:
            xs=np.array([p[0]+p[2]/2 for p in pts]); ys=np.array([cy(p) for p in pts])
            slope=np.polyfit(xs,ys,1)[0]; slope=max(-0.12,min(0.12,slope))
        else: slope=0.03
        lastx=last[0]+last[2]
        best=None
        for i,b in enumerate(bs):
            if i in used: continue
            if b[0]<lastx-35: continue
            dx=b[0]+b[2]/2-(last[0]+last[2]/2)
            if dx<20 or dx>330: continue
            pred=cy(last)+slope*dx
            dy=abs(cy(b)-pred)
            tol=60+0.0*dx
            if dy<tol:
                score=dy*1.0+dx*0.5
                if best is None or score<best[0]: best=(score,i)
        if best is None: break
        chain.append(best[1]); used.add(best[1])
    lines.append(chain)
tr=[l.split() for l in open('work/transcript_v1.txt')]
for j,ch in enumerate(lines):
    n=sum(1 for t in tr[j] if t!='|') if j<len(tr) else -1
    print(j,starts[j],len(ch),n, int((bs[ch[-1]][0]+bs[ch[-1]][2])/S) if ch else None)
json.dump(dict(boxes=bs,lines=lines),open('work/tracked.json','w'))
