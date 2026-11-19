import sys, pickle, json
import boot, rank as rk
page=sys.argv[1]; only=set(sys.argv[2:])
F=pickle.load(open('final_decode.pkl','rb'))
for key,o in F.items():
    pg,li=key.split(':'); li=int(li)
    if pg!=page or (only and str(li) not in only): continue
    spans=[(i,j,w,c) for i,j,w,f,c in o if f=='D']
    if not spans: continue
    lp=rk.prep(page,li)
    for i,j,w,c in spans:
        r=rk.rank(page,li,i,j,lp,K=10)
        print(f'{key} [{i}:{j}] cur={w} {c} ->',' '.join(f'{x}({c_:.1f})' for c_,x in r),flush=True)
