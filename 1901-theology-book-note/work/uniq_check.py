"""How constrained is the reading of the thin-pen sentence?
Glyph streams (refined segmentation):
 W2: Zc g o d z e n i e  -> glyphs  ZC  G  O  D  Z  E  N  I  E   (ZC = capital/initial oval glyph, allowed to equal Z's letter)
 W3: s i ę               -> S I Eog
 W4: n a                 -> N A
 W5: w o l ę             -> W O L Eog
 W6: B o ż ą             -> BC O Zdot Aog
Diacritic pairing constraints: Eog = ogonek(E), Aog = ogonek(A), Zdot = dot(Z or ZC).
Search all Polish dictionary words (pattern-consistent) and count solutions."""
import sys,collections,math
D=sys.argv[1]; MINF=int(sys.argv[2])
ws=[(l.split()[0],int(l.split()[1])) for l in open(D+'/pl_combined.txt',encoding='utf-8') if len(l.split())==2 and l.split()[0].isalpha() and int(l.split()[1])>=MINF]
OG={'a':'ą','e':'ę'}; DOT={'z':'ż'}
specs=[['ZC','G','O','D','Z','E','N','I','E'],['S','I','Eog'],['N','A'],['W','O','L','Eog'],['BC','O','Zdot','Aog']]
free_eq={('ZC','Z')}  # capital may share letter with lowercase
def consistent(m):
    inv=collections.defaultdict(set)
    for g,c in m.items(): inv[c].add(g)
    for c,gs in inv.items():
        if len(gs)>1 and not (gs<= {'ZC','Z'} or gs<={'BC'} ): return False
    if 'E' in m and 'Eog' in m and OG.get(m['E'])!=m['Eog']: return False
    if 'A' in m and 'Aog' in m and OG.get(m['A'])!=m['Aog']: return False
    if 'Zdot' in m:
        zs=[m[k] for k in ('Z','ZC') if k in m]
        if zs and not any(DOT.get(z)==m['Zdot'] for z in zs): return False
    return True
bylen=collections.defaultdict(list)
for w,f in ws: bylen[len(w)].append((w,f))
sols=[]
def rec(i,m,chosen,score):
    if i==len(specs):
        sols.append((score,chosen)); return
    for w,f in bylen[len(specs[i])]:
        m2=dict(m); ok=True
        for g,c in zip(specs[i],w):
            if g in m2 and m2[g]!=c: ok=False;break
            m2[g]=c
        if ok and consistent(m2): rec(i+1,m2,chosen+[w],score+math.log(f))
rec(0,{},[],0)
sols.sort(reverse=True)
print(len(sols),'solutions')
for s,c in sols[:15]: print('  %.1f'%s,' '.join(c))
