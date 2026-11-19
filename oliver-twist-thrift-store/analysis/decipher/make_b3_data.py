import json, sys
import boot, align as al, align_user as au
import user_b3 as U
FS=json.load(open('fixed_spans.json')); FG=json.load(open('forced_suggest.json')); GM=json.load(open('glyph_map.json'))
EXJ={}
def norm(it):
    pcs,t,k0=it; return dict(p=list(pcs),t=t)
rep=[]
for (page,li),text in U.USER.items():
    pcs_all,items,c,sk,words,letters=au.run(page,li,text)
    its=[norm(i) for i in items]
    for (lo,hi),new in U.MANUAL.get((page,li),{}).items():
        its=[i for i in its if not (lo<=min(i['p'])<hi)]
        for n in new:
            its.append(dict(box=n['box'],t=n['t'],p=n['p']) if isinstance(n,dict) else dict(p=n[:-1],t=n[-1]))
    its.sort(key=lambda i:min(i['p']))
    assert ''.join(i['t'] for i in its)==letters,(page,li,''.join(i['t'] for i in its),letters)
    # assign items to words
    k=0; wi=0; wb=[]; pos=0
    for w in words: wb.append((pos,pos+len(w),w)); pos+=len(w)
    wspan={}
    k=0
    for i in its:
        a=k; k+=len(i['t'])
        for (s,e,w) in wb:
            if s<=a<e:
                assert a+len(i['t'])<=e,(page,li,'item crosses word',i,w)
                wspan.setdefault((s,e,w),[]).append(i)
    spans=[]; sug=[]
    for (s,e,w),ii in sorted(wspan.items()):
        lo=min(min(i['p']) for i in ii); hi=max(max(i['p']) for i in ii)+1
        (sug if w in U.UNCERTAIN.get((page,li),[]) else spans).append([lo,hi,w])
    used=set()
    for lo,hi,w in spans+sug: used|=set(range(lo,hi))
    n=len(boot.lines_of(page)[li]); runs=[]; j=0
    while j<n:
        if j in used: j+=1; continue
        k2=j
        while k2<n and k2 not in used: k2+=1
        runs.append([j,k2,'']); j=k2
    spans=sorted(spans+runs)
    FS.setdefault(page,{})[str(li)]=spans
    if sug: FG.setdefault(page,{})[str(li)]=sorted(sug)
    elif str(li) in FG.get(page,{}): del FG[page][str(li)]
    GM[f'{page}:{li}']=[(i['p']+[i['t']] if 'box' not in i else dict(box=i['box'],t=i['t'],p=i['p'])) for i in its]
    if (page,li) in U.EXTRA: EXJ[f'{page}:{li}']=U.EXTRA[(page,li)]
    rep.append((page,li,c/len(letters),[f'{w}[{lo}:{hi}]' for lo,hi,w in sorted(spans+sug,key=lambda x:x[0]) if w]))
json.dump(FS,open('fixed_spans.json','w')); json.dump(FG,open('forced_suggest.json','w')); json.dump(GM,open('glyph_map.json','w')); json.dump(EXJ,open('extra_glyphs.json','w'))
for page,li,c,sp in rep: print(f'{page}:{li} {c:.2f}',' '.join(sp))
