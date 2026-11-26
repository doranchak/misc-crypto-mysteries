from fractions import Fraction
from decimal import Decimal
for s in ['204.9878045153','34.7657830759','4.62345604807','15.3587885416','57.295776']:
    a,f = s.split('.')
    ia=int(a); fr=Decimal('0.'+f)
    # binary expansion of fraction, 45 bits
    x=fr; b=''
    for i in range(45):
        x*=2
        if x>=1: b+='1'; x-=1
        else: b+='0'
    # find smallest k such that fr*2^k is near integer
    best=None
    for k in range(1,48):
        v=fr*(2**k); err=abs(v-round(v))
        if err < Decimal(2**k)*Decimal('0.6e-%d'%len(f)) : best=(k,int(round(v))); break
    print(s, 'int', bin(ia)[2:], 'frac', b, 'exact-k', best, (bin(best[1])[2:].zfill(best[0]) if best else ''))
