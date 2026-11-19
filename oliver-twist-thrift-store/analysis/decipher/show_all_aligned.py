import sys, json
import boot, align as al, rank as rk, align_user as au, render_assign as ra
from user_b3 import USER
page=sys.argv[1]; sel=[int(x) for x in sys.argv[2:]]
ims=[]
for (pg,li),text in USER.items():
    if pg!=page or (sel and li not in sel): continue
    pcs,items,c,sk,words,letters=au.run(pg,li,text)
    ims.append(ra.render(pg,li,items,title=f'{pg}:{li} {text}  cost/let={c/len(letters):.2f} skipped={sk}'))
    print(pg,li,'ok')
ra.stack(ims,f'../v/aligned_{page}_{"_".join(map(str,sel)) or "all"}.png')
