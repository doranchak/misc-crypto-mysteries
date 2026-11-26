"""Gareth Penn toolkit: Morse->binary (dah=1, dit=0); Arabic numbers -> base two."""
import re
MORSE = {'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.','F':'..-.','G':'--.','H':'....','I':'..','J':'.---',
'K':'-.-','L':'.-..','M':'--','N':'-.','O':'---','P':'.--.','Q':'--.-','R':'.-.','S':'...','T':'-','U':'..-',
'V':'...-','W':'.--','X':'-..-','Y':'-.--','Z':'--..'}
BITS = {k:v.replace('-','1').replace('.','0') for k,v in MORSE.items()}
def bits(s):
    out=[]
    for tok in re.findall(r'[A-Za-z]|\d+', s):
        out.append(BITS[tok.upper()] if tok.isalpha() else bin(int(tok))[2:])
    return ''.join(out)
def mval(s):
    b=bits(s); return int(b,2) if b else 0
def mval_point(s):
    a,_,f = s.partition('.')
    ia = int(bits(a),2) if bits(a) else 0
    fb = bits(f)
    return ia + sum(int(ch)*2.0**-(i+1) for i,ch in enumerate(fb))
def alpha(s, e3=False):
    return sum((3 if (e3 and c=='E') else ord(c)-64) for c in s.upper() if c.isalpha())
if __name__=='__main__':
    for w,v in {'3RD':212,'TIMES17':None,'JU.LY':57.29296875}.items(): print(w,bits(w),mval(w))
    print('JU.LY23', mval_point('JU.LY23'), 'JU.LY1',mval_point('JU.LY1'))
    print('1729 in YWHEN bits:', bin(1729)[2:] in bits('YWHEN'))
