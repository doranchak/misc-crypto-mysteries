import json, collections, math, re
P=json.load(open('report_pages.json'))
EN={'E':12.70,'T':9.06,'A':8.17,'O':7.51,'I':6.97,'N':6.75,'S':6.33,'H':6.09,'R':5.99,'D':4.25,'L':4.03,'C':2.78,'U':2.76,'M':2.41,'W':2.36,'F':2.23,'G':2.02,'Y':1.97,'P':1.93,'B':1.49,'V':0.98,'K':0.77,'J':0.15,'X':0.15,'Q':0.10,'Z':0.07}
sets={'K':[], 'V':[], 'ALL':[]}
perpage={}
for pg,d in P.items():
    cnt=collections.Counter(); cv=collections.Counter(); 
    for ln in d['lines']:
        for w in ln['words']:
            t=re.sub(r"[^A-Z']",'',w['t'])
            if not t.replace("'",''): continue
            if w['f']=='K': sets['K'].append(t); sets['V'].append(t); sets['ALL'].append(t); cv['K']+=len(t.replace("'",''))
            elif w['f']=='V': sets['V'].append(t); sets['ALL'].append(t); cv['V']+=len(t.replace("'",''))
            else:
                sets['ALL'].append(t); cv['D']+=len(t.replace("'",''))
                if w['c']>=0.55: cv['Dhi']+=len(t.replace("'",''))
    perpage[pg]=dict(K=cv['K'],V=cv['V'],D=cv['D'],Dhi=cv['Dhi'],lines=len(d['lines']))
def stats(words):
    napos=sum(w.count("'") for w in words); wraw=words; words=[w.replace("'",'') for w in words]
    c=collections.Counter(''.join(words)); N=sum(c.values())
    ic=sum(v*(v-1) for v in c.values())/(N*(N-1))
    freq={L:100*c.get(L,0)/N for L in EN}
    # correlation with English
    xs=[freq[L] for L in EN]; ys=[EN[L] for L in EN]
    mx=sum(xs)/26; my=sum(ys)/26
    r=sum((a-mx)*(b-my) for a,b in zip(xs,ys))/math.sqrt(sum((a-mx)**2 for a in xs)*sum((b-my)**2 for b in ys))
    chi=sum((freq[L]-EN[L])**2/EN[L] for L in EN)
    bi=collections.Counter(); tri=collections.Counter()
    for w in words:
        for i in range(len(w)-1): bi[w[i:i+2]]+=1
        for i in range(len(w)-2): tri[w[i:i+3]]+=1
    wc=collections.Counter(wraw)
    wl=collections.Counter(len(w) for w in words)
    dbl=collections.Counter(w[i:i+2] for w in words for i in range(len(w)-1) if w[i]==w[i+1])
    first=collections.Counter(w[0] for w in words); last=collections.Counter(w[-1] for w in words)
    return dict(napos=napos,N=N,nwords=len(words),counts={L:c.get(L,0) for L in EN},freq=freq,ic=ic,r=r,chi=chi,
        bigrams=bi.most_common(20),trigrams=tri.most_common(10),words=wc.most_common(25),wordlen=sorted(wl.items()),
        doubles=dbl.most_common(8),first=first.most_common(8),last=last.most_common(8))
out=dict(EN=EN,perpage=perpage,K=stats(sets['K']),V=stats(sets['V']),ALL=stats(sets['ALL']))
json.dump(out,open('report_stats.json','w'))
for k in ['K','V','ALL']: print(k,out[k]['N'],round(out[k]['ic'],4),round(out[k]['r'],3),out[k]['words'][:8],out[k]['bigrams'][:8])
print(perpage)
