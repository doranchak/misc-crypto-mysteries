import pickle, numpy as np
A=pickle.load(open('allpieces_orig.pkl','rb'))
new=pickle.load(open('rescue_b2R_new.pkl','rb'))
sel1=[p for p in new if (p['x'],p['y'])==(650,632)]
sel2=sorted([p for p in new if (p['x'],p['y']) in [(700,803),(727,785),(785,791),(841,790)]],key=lambda p:p['cx'])
print(len(sel1),len(sel2))
L=A['b2R']['lines']
L[1]=L[1]+sel1; L[2]=L[2]+sel2
for li in (1,2): print(li,len(L[li]),[int(p['x']) for p in L[li]])
pickle.dump(A,open('allpieces.pkl','wb'))
