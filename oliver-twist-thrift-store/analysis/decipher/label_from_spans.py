import sys, json
import boot, align as al, rank as rk
from decode import LI
page=sys.argv[1]; lines=sys.argv[2:]
FS=json.load(open('fixed_spans.json')); E=json.load(open('explicit_labels.json')); E.setdefault(page,{})
print('LI has',sorted(k for k in LI if len(k)>1))
for li in lines:
    lp=rk.prep(page,int(li)); pcs=boot.lines_of(page)[int(li)]; lab=E[page].setdefault(li,{})
    for i,j,w in FS[page][li]:
        items,c=al.align(pcs[i:j],lp[i:j],w)
        row=[]
        for it,t,_ in items:
            row.append(f"{[i+k for k in it]}={t}")
            if len(it)==1 and t in LI: lab.setdefault(str(i+it[0]),t)
        print(page,li,w,round(c,1),' '.join(row))
json.dump(E,open('explicit_labels.json','w'))
