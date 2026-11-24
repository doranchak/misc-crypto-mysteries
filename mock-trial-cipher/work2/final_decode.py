import sys, os, json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from lib import *
J=json.load(open('r4_R3A2_-?Edj.json'))
best=J['best']; al=J['al']; drop=set(J['drop'])
lines=load_lines()
ix={c:i for i,c in enumerate(al)}
# stream mapping
recs=[]  # (line,chunk,pos,code)
for li,l in enumerate(lines):
    for ci,c in enumerate(l):
        for pi,ch in enumerate(c):
            recs.append((li+1,ci,pi,ch))
text=best['text'].replace(' ','')
lab=best['lab']
M=len(best['L'])
# token->letter table
Lmap=best['L']
# split info
split={ix[s[0]]:int(s[1:]) for s in J['split'].split(',')}
extra0={}; m=len(al)
for c in split: extra0[c]=m; m+=split[c]-1
k=0; out=[]
for (li,ci,pi,ch) in recs:
    if ch in drop:
        out.append(dict(line=li,chunk=ci,pos=pi,code=ch,letter=None,sub=None)); continue
    c=ix[ch]; sub=lab[k] if c in split else 0
    tok=c if sub==0 else extra0[c]+sub-1
    letter=Lmap[tok]
    assert letter==text[k],(k,letter,text[k])
    out.append(dict(line=li,chunk=ci,pos=pi,code=ch,letter=letter,sub=sub if c in split else None)); k+=1
assert k==len(text)
# glyph -> letters table
tab={}
for o in out:
    if o['letter'] is None: continue
    key=o['code']+(f"#{o['sub']}" if o['sub'] is not None else '')
    tab.setdefault(key,{}).setdefault(o['letter'],0); tab[key][o['letter']]+=1
json.dump(dict(model=J['split'],dropped=''.join(sorted(drop)),score=best['score'],glyphs=out,table=tab),open('../solver_decode.json','w'),indent=1)
# text view
with open('../solver_decode.txt','w') as f:
    f.write('# Solver decode (R split 3 ways, A split 2 ways). Dropped (shown as .): '+''.join(sorted(drop))+'\n')
    for li,l in enumerate(lines):
        words=[]
        for ci,c in enumerate(l):
            w=''.join((o['letter'] or '.') for o in out if o['line']==li+1 and o['chunk']==ci)
            words.append(w)
        f.write(f'{li+1:2d}: '+' '.join(words)+'\n')
print(open('../solver_decode.txt').read())
print(json.dumps(tab))
