import sys, numpy as np, boot
lab=boot.build_train(boot.load_ver()); D=boot.D; meta=boot.meta; idx=boot.idx
ids=np.array(sorted(lab))
def nn(page,li,j,k=8):
    i=idx[(page,li,j)]; d=D[i,ids].copy(); d[ids==i]=1e9
    o=np.argsort(d)[:k]
    return ' '.join(f'{lab[ids[t]]}[{meta[ids[t]][0]}:{meta[ids[t]][1]}:{meta[ids[t]][2]}]{d[t]:.2f}' for t in o)
if __name__=='__main__':
    page=sys.argv[1]; li=int(sys.argv[2])
    for j in map(int,sys.argv[3:]): print(f'{page}:{li}:{j}', nn(page,li,j))
