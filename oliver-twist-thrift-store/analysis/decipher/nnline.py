import sys, numpy as np, boot
lab=boot.build_train(boot.load_ver()); D=boot.D; meta=boot.meta; idx=boot.idx
ids=np.array(sorted(lab)); P1=np.array([meta[i][0]=='b1' for i in ids])
def line(page,li,k=3):
    pcs=boot.lines_of(page)[li]; out=[]
    for j in range(len(pcs)):
        i=idx[(page,li,j)]; d=D[i,ids].copy(); d[ids==i]=1e9
        o=np.argsort(d); seen={}; 
        for t in o:
            L=lab[ids[t]]
            if L not in seen: seen[L]=d[t]
            if len(seen)>=k: break
        out.append(' '.join(f'{L}{v:.1f}' for L,v in seen.items()))
    return out
if __name__=='__main__':
    page=sys.argv[1]
    for li in map(int,sys.argv[2:]):
        pcs=boot.lines_of(page)[li]; o=line(page,li)
        print(f'--- {page}:{li}')
        print('  '.join(f'{j}:{s}' for j,s in enumerate(o)))
