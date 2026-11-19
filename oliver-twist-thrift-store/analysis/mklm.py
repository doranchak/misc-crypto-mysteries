import re, sys, unicodedata, numpy as np, pickle
A='abcdefghijklmnopqrstuvwxyz'; idx={c:i+1 for i,c in enumerate(A)}
for lang,start in (('en','lm/ot.txt'),('es','lm/es.txt'),('fr','lm/fr.txt'),('it','lm/it.txt'),('de','lm/de.txt'),('pt','lm/pt.txt'),('nl','lm/nl.txt'),('en2','lm/en2.txt')):
    txt=open(start,encoding='utf-8',errors='ignore').read()
    txt=unicodedata.normalize('NFKD',txt).encode('ascii','ignore').decode().lower()
    toks=re.findall(r'[a-z]+',txt)
    tri=np.ones((27,27,27))*0.1
    for w in toks:
        s=[0,0]+[idx[c] for c in w]+[0]
        for a,b,c in zip(s,s[1:],s[2:]): tri[a,b,c]+=1
    tri=tri/tri.sum(axis=2,keepdims=True)
    pickle.dump(np.log(tri),open(f'lm/logtri_{lang}.pkl','wb'))
    print(lang,len(toks))
