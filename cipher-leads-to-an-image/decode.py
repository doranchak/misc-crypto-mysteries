# Puzzle 2: 37 groups of 8 digits (1/2) -> 7-bit ASCII -> Caesar -7 on letters -> imgur URL;
# then LSB stego in row 0 of the downloaded PNG.
import numpy as np
from PIL import Image
s="12112111 12112111 12212222 12211112 12211112 12221222 12222121 12112111 12122112 12122112 11211221 12122222 11212212 11212122 11212122 12221111 12221211 12212221 12211121 12222112 12212121 12221221 12221211 11112121 12212111 11112121 11112121 12221211 12121111 12121212 12111222 12121112 12122121 12221122 11112121 11112121 11221222"
by=[int(''.join('0' if c=='1' else '1' for c in g),2) for g in s.split()]
txt=''.join(chr(b) for b in by)
def rot(c,k):
    if c.isalpha():
        b=65 if c.isupper() else 97
        return chr((ord(c)-b-k)%26+b)
    return c
print(repr(''.join(rot(c,7) for c in txt)))   # AAhttpsARR&_-++imgurcom\na\n\nmINZJSl\n\n7  -> https://imgur.com/a/mINZJSl (noise removed)
a=np.array(Image.open('qkhHnIc.png').convert('RGB'))
bits=''.join(str(v&1) for v in a[0,:80].reshape(-1))
print(''.join(chr(int(bits[i:i+8],2)) for i in range(0,240,8)).replace('\x00',''))  # NicEcoMplEte2
