import json, numpy as np, cv2
S=4
boxes=json.load(open('work/boxes.json'))
for b in boxes: b.append(b[1]+b[3]/2)   # cy idx5
centers=[24,58,103,134,172,248,278,310,343,374,405,447,478,511,550,588,620,680,715,743,773,802,826,872,902,934]
# assign each box to nearest line center (original px), with local adaptive: use tolerance
assign={}
cyo=[b[5]/S for b in boxes]
# Fit line y as function of x per line: iterative tracking
lines=[]
for li,c0 in enumerate(centers):
    cand=[i for i,b in enumerate(boxes) if abs(cyo[i]-c0)<20]
    lines.append(cand)
# resolve conflicts: box goes to the line whose center is closest, but allow slope by x: use local median
final={i:None for i in range(len(boxes))}
for i in range(len(boxes)):
    d=[abs(cyo[i]-c) for c in centers]
    j=int(np.argmin(d))
    if d[j]<17: final[i]=j
out=[[] for _ in centers]
for i,j in final.items():
    if j is not None: out[j].append(i)
for j in range(len(out)):
    out[j].sort(key=lambda i:boxes[i][0])
    print(j,centers[j],len(out[j]))
unassigned=[i for i,j in final.items() if j is None]
print('unassigned',len(unassigned))
json.dump(dict(boxes=boxes,lines=out,centers=centers),open('work/lines.json','w'))
