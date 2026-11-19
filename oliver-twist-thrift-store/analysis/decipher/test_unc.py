import sys, numpy as np
import boot, rank as rk, align as al, cost as cs
def top(page,li,i,j,K=8,drop=()):
    lp=rk.prep(page,li)
    r=rk.rank(page,li,i,j,lp,K=K)
    print(page,li,i,j,[(round(c,1),w) for c,w in r])
    return lp
def cmp(page,li,i,j,words):
    lp=rk.prep(page,li)
    for w in words:
        items,c=al.align(boot.lines_of(page)[li][i:j],lp[i:j],w.upper())
        print(f'   {w:12s} cost {c:5.1f}  per-letter {c/len(w):.2f}')
if __name__=='__main__':
    # (page, line, i, j, [hypotheses])
    T=[('b3L',7,7,15,['PIPACO','PICACO','PIPASO','PIPAC','PUBLIC','PICASSO']),
       ('b3L',23,0,5,['GET','SET','BET','LET','WET']),
       ('b3R',1,15,21,['TOWN','DOWN','GOWN','TOWNS','OWN','LOWN']),
       ('b3R',6,16,18,['IS','IT','AS','IN']),
       ('b3R',14,3,6,['SHOT','SHOP','SHOE','SHUT','SHOW','SHIT','SHOT']),
       ('b3R',12,10,18,['ENTIRLY','ENTIRELY','ENTIRE'])]
    for page,li,i,j,hy in T:
        print('==',page,li,i,j); cmp(page,li,i,j,hy)
