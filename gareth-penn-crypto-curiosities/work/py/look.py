from puzzles import P
from collections import Counter
import re
for k,s in P.items():
    L=''.join(c for c in s.upper() if c.isalpha()); D=''.join(c for c in s if c.isdigit()); S=''.join(c for c in s if not c.isalnum())
    print(f'{k:22s} len={len(s):3d} L={len(L):2d} D={len(D):2d} S={len(S)}  letters={L}  digits={D} sym={S}')
