import pickle, numpy as np
lines=pickle.load(open('blue_lines.pkl','rb'))
def U(*idx):
    out=[]
    for i in idx: out+=lines[i]
    return sorted(out,key=lambda c:c['cx'])
PT={1:("I BOUGHT THIS BOOK ON THE DAY",U(0)),
 2:("OF SEAN FLECKENSTEINS WED",U(1)),
 3:("DING AT THE LEACH BOTANICAL",U(2)),
 4:("GARDENS",U(3)),
 5:("THE DATE IS JUNE NINTH",U(6)),
 6:("TODAY MY FRIEND SEAN MARIED",U(7)),
 7:("GWENETH LURID I WENT TO THE",U(8)),
 8:("CEREMONY WITH MELANIE BUD",U(9,10)),
 9:("AND NICK",U(11)),
 10:("ITS REALY RATHER FITING THAT I",U(12)),
 11:("PURCHASED THIS BOOK TODAY IVE",U(13)),
 12:("BEEN THINKING ABOUT GETTING A SPECIAL",U(14))}
MERGE={'TH','THE','OU','GH','ST','CK','CH','ING','ND','AND','EE','SP','TT','OO','NG','ETT','OUGH','NI','IN','ET','IS','ED'}
def align(text,comps):
    words=text.split(); letters=''.join(words); N=len(letters)
    # word boundaries
    wb=set(); p=0
    for w in words: p+=len(w); wb.add(p)
    M=len(comps); INF=1e9
    dp=np.full((M+1,N+1),INF); bp={}
    dp[0][0]=0
    for i in range(1,M+1):
        w=comps[i-1]['w']
        for j in range(1,N+1):
            for k in (1,2,3,4):
                if j-k<0: continue
                sub=letters[j-k:j]
                if k>1:
                    if sub not in MERGE: continue
                    # must not cross word boundary
                    if any((j-k)<b<j for b in wb): continue
                if dp[i-1][j-k]>=INF: continue
                exp=12+6*(k-1)
                c=((w-exp)/5.0)**2+(0.7*(k-1) if k>1 else 0)
                if dp[i-1][j-k]+c<dp[i][j]: dp[i][j]=dp[i-1][j-k]+c; bp[(i,j)]=k
    if dp[M][N]>=INF: return None,dp[M][N]
    res=[];i,j=M,N
    while i>0:
        k=bp[(i,j)]; res.append((letters[j-k:j],comps[i-1])); i-=1; j-=k
    return res[::-1],dp[M][N]
out={}
for ln,(t,cs) in PT.items():
    r,c=align(t,cs)
    if r is None: print(ln,'FAIL',len(cs),len(t.replace(' ','')));continue
    out[ln]=r
    print(ln,round(c,1),' '.join(u for u,_ in r))
pickle.dump(out,open('blue_units.pkl','wb'))
