import pickle, cv2, numpy as np, collections
S=4.725
d=pickle.load(open('b1_pieces.pkl','rb')); lines=d['lines']; flat=d['flat']
units=pickle.load(open('blue_units.pkl','rb'))
w,h=2470,2650
M=cv2.getRotationMatrix2D((w/2,h/2),-0.75,1.0)
def to_reg(xo,yo):
    x=xo-330; y=yo-1250
    return M[0,0]*x+M[0,1]*y+M[0,2], M[1,0]*x+M[1,1]*y+M[1,2]
LT=[]  # per line: letters with x positions
for ln in range(1,13):
    L=[]
    for u,c in units[ln]:
        k=len(u); x0=c['x']; x1=c['x']+c['w']
        for i,ch in enumerate(u):
            kx=x0+(i+0.5)*(x1-x0)/k
            xr,yr=to_reg(kx*S,(c['cy']+22)*S)
            L.append((ch,xr))
    LT.append(L)
LT.append([(ch,None) for ch in "BOOKTOCHRONICLEMYTRIALSAND"])  # line 13 no positions
def align(P,L,sx=28.0):
    m=len(P); n=len(L); INF=1e9
    dp=np.full((m+1,n+1),INF); bp={}
    dp[0][0]=0
    for j in range(m+1):
        for i in range(n+1):
            if dp[j][i]>=INF: continue
            c0=dp[j][i]
            if j<m:
                # skip piece
                if c0+3.0<dp[j+1][i]: dp[j+1][i]=c0+3.0; bp[(j+1,i)]=('sp',)
                for k in (1,2,3):
                    if i+k<=n:
                        xs=np.mean([L[i+t][1] for t in range(k)])
                        c=((P[j]['cx']-xs)/sx)**2+(1.5*(k-1))
                        if c0+c<dp[j+1][i+k]: dp[j+1][i+k]=c0+c; bp[(j+1,i+k)]=('m',k)
            if i<n:
                if c0+3.5<dp[j][i+1]: dp[j][i+1]=c0+3.5; bp[(j,i+1)]=('sl',)
    res=[];j,i=m,n
    while (j,i)!=(0,0):
        op=bp[(j,i)]
        if op[0]=='sp': res.append((j-1,None)); j-=1
        elif op[0]=='sl': i-=1
        else:
            k=op[1]; res.append((j-1,''.join(L[i-k+t][0] for t in range(k)))); j-=1; i-=k
    return res[::-1],dp[m][n]
out=[]
for ln in range(12):
    P=lines[ln]; L=LT[ln]
    res,c=align(P,L)
    lab=[None]*len(P)
    for j,s in res: lab[j]=s
    print(ln+1,round(c,1),len(P),len(L),''.join((s if s else '.')+' ' for s in lab))
    for j,p in enumerate(P): p['label']=lab[j]
pickle.dump(lines,open('b1_labeled.pkl','wb'))
