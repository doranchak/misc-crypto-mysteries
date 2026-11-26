from grid import *
import sys
words=sys.argv[1].split(',')
used=set()
for w in words:
    f=find_all(w)
    print(w,f)
    if f:
        r,c,dr,dc,_=f[0]
        for k in range(len(w)): used.add((r+dr*k,c+dc*k))
for r in range(R):
    print(' '.join(GRID_ROWS[r][c] if (r,c) not in used else '.' for c in range(C)))
print(''.join(GRID_ROWS[r][c] for r in range(R) for c in range(C) if (r,c) not in used))
