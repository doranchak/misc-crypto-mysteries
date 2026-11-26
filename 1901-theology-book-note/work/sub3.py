import sys
exec(open('linesearch.py').read().split("T_opts=")[0])
S={'T9':'N V A S I B T Y B','T8':'N V A S I B Y B','W1':'b r B I U Y D B','W1sq':'b r Q I U Y D B','T9sq':'N V A S I Q T Y B',
'W2':'O G J H i L S i','W2d':'O G d J H i L S i','W3':'E S Z','W4':'L D','W5':'F J Z','W5d':'F d J Z'}
for combo in [('T9','W1'),('T9sq','W1sq'),('T9','W1','W4'),('T9sq','W1sq','W4'),('T9','W1sq')]:
    n,b=solve([S[c].split() for c in combo],15)
    print(combo,n)
    for s,ws in b: print('    %.1f '%s+' | '.join(ws))
