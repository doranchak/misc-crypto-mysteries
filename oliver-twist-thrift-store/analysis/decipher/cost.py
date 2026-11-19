import sys, numpy as np
import boot, align as al, rank as rk
def cost(page,li,i,j,words,lp=None,show=False):
    lp=rk.prep(page,li) if lp is None else lp
    pcs=boot.lines_of(page)[li][i:j]; sl=lp[i:j]
    for w in words:
        items,c=al.align(pcs,sl,w.upper())
        print(f'{page}:{li}:{i}-{j} {w:14s} cost {c:5.1f}  ',' '.join(f"{[i+k for k in it]}={t}" for it,t,_ in items) if show else '')
if __name__=='__main__':
    page=sys.argv[1]; li=int(sys.argv[2]); i,j=map(int,sys.argv[3].split(':')); cost(page,li,i,j,sys.argv[4:],show=True)
