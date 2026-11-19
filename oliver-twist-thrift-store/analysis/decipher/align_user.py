import sys, json, numpy as np
import boot, align as al, rank as rk
from user_b3 import USER
try:
    from user_b3 import DROP, FORCE
except ImportError:
    DROP={}; FORCE={}
_LP={}
def get_lp(page,li):
    if (page,li) not in _LP: _LP[(page,li)]=rk.prep(page,li)
    return _LP[(page,li)]
def run(page,li,text,lp=None,drop=None):
    words=text.split(); letters=''.join(words); breaks=[]; k=0
    for w in words: breaks.append(k); k+=len(w)
    breaks=breaks[1:]
    pcs_all=boot.lines_of(page)[li]
    lp=get_lp(page,li) if lp is None else lp
    drop=set(DROP.get((page,li),[]) if drop is None else drop)
    keep=[j for j in range(len(pcs_all)) if j not in drop]
    pcs=[pcs_all[j] for j in keep]
    items,c=al.align(pcs,lp[keep],letters,breaks=tuple(breaks))
    items=[(tuple(keep[j] for j in it),t,k0) for it,t,k0 in items]
    used={j for it,_,_ in items for j in it}
    skipped=[j for j in keep if j not in used]
    return pcs_all,items,c,skipped,words,letters
if __name__=='__main__':
    sel=sys.argv[1:]
    for (page,li),text in USER.items():
        if sel and f'{page}:{li}' not in sel: continue
        pcs,items,c,sk,words,letters=run(page,li,text)
        print(f'== {page}:{li} pieces={len(pcs)} letters={len(letters)} cost={c:.1f} cost/let={c/len(letters):.2f} skipped={sk}')
        print('   ',' '.join(f"{'+'.join(map(str,it))}={t}" for it,t,_ in items))
