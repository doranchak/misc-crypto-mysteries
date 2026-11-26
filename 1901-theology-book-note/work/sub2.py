import sys
exec(open('linesearch.py').read().split("T_opts=")[0])
S={'T':'N V A S I B Y B','T9':'N V A S I B T Y B','W1':'b r B I U Y D B','W1_7':'b r B I Y D B',
'W2':'O G J H i L S i','W2d':'O G d J H i L S i','W3':'E S Z','W4':'L D','W5':'F J Z','W5d':'F d J Z'}
for combo in [('W2d','W5d'),('W2d','W3','W5d'),('W2d','W3','W4','W5d'),('W2','W3','W4','W5'),('W2d','W4','W5d'),('W1','W2d','W4','W5d'),('W1','W2','W4','W5'),('T','W2d','W3','W4','W5d'),('T9','W2d','W3','W4','W5d'),('T','W1','W4')]:
    n,b=solve([S[c].split() for c in combo],12)
    print(combo,n)
    for s,ws in b: print('    %.1f '%s+' | '.join(ws))
