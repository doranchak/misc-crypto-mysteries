import sys,itertools
exec(open('linesearch.py').read().split("T_opts=")[0])
words_spec={
 'T':'N V A S I B Y B'.split(),
 'T9':'N V A S I B T Y B'.split(),
 'W1':'b r B I U Y D B'.split(),
 'W1_7':'b r B I Y D B'.split(),
 'W2':'O G J H i L S i'.split(),
 'W2d':'O G d J H i L S i'.split(),
 'W3':'E S Z'.split(),'W4':'L D'.split(),
 'W5':'F J Z'.split(),'W5d':'F d J Z'.split()}
groups=[('T','T9'),('W1','W1_7'),('W2','W2d'),('W3',),('W4',),('W5','W5d')]
for drop in range(len(groups)):
    for combo in itertools.product(*[g for i,g in enumerate(groups) if i!=drop]):
        if ('W2d' in combo)!=('W5d' in combo): continue
        n,b=solve([words_spec[c] for c in combo],5)
        if n: 
            print('drop',groups[drop],combo,n)
            for s,ws in b: print('    %.1f '%s+' | '.join(ws))
