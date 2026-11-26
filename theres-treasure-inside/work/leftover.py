from grid import *
import sys
# words: NAME@r,c,DIR  or NAME (first placement)
specs=sys.argv[1].split(',')
used={}
DIRV={v:k for k,v in DIRS.items()}
for s in specs:
    if '@' in s:
        w,pos=s.split('@'); r,c,d=pos.split(':'); r=int(r);c=int(c);dr,dc=DIRV[d]
    else:
        w=s; f=find_all(w); assert f, w; r,c,dr,dc,_=f[0]
    for k,ch in enumerate(w):
        rr,cc=r+dr*k,c+dc*k
        assert GRID_ROWS[rr][cc]==ch,(w,rr,cc)
        used.setdefault((rr,cc),[]).append(w)
print('    '+' '.join(f'{c%10}' for c in range(C)))
for r in range(R):
    print(f'{r:2}  '+' '.join(GRID_ROWS[r][c].lower() if (r,c) in used else GRID_ROWS[r][c] for c in range(C)), '   ', ' | '.join(
        ''.join(GRID_ROWS[r][c] for c in rng) for rng in __import__('itertools').groupby(range(C), key=lambda c:(r,c) in used) and []) )
for r in range(R):
    runs=[];cur=''
    for c in range(C):
        if (r,c) in used:
            if cur: runs.append(cur);cur=''
        else: cur+=GRID_ROWS[r][c]
    if cur: runs.append(cur)
    print(r, ' '.join(runs))
