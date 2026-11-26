import sys
exec(open('linesearch.py').read().split("T_opts=")[0])
S={'T9':'N V A S I B T Y B','W1':'b r B I U Y D B',
'W2':'O G J H i L S i','W2d':'O G d J H i L S i','W3':'E S Z','W4':'L D','W5':'F J Z','W5d':'F d J Z',
'W6':'P Q R X','W6d':'K d P Q R X','W6L':'P Q R X'}
def ok(ws,combo):
    # ogonek constraints: Z (zeta-like) and X (final box) must be nasal vowels
    m=dict(zip(combo,ws))
    if 'W3' in m and m['W3'][-1] not in 'ąę': return False
    for k in ('W6','W6d'):
        if k in m and m[k][-1] not in 'ąę': return False
    return True
for combo in [('W2','W3','W4','W5','W6'),('W2d','W3','W4','W5d','W6'),('W2d','W3','W4','W5d','W6d')]:
    n,b=solve([S[c].split() for c in combo],100000)
    b=[x for x in b if ok(x[1],combo)]
    print(combo,len(b))
    for s,ws in b[:25]: print('    %.1f '%s+' | '.join(ws))
