import json, base64, cv2, numpy as np, pickle, sys
sys.path.insert(0,'..')
import boot, strips
BASE='/Users/doranchak/projects/github/misc-crypto-mysteries/oliver-twist-thrift-store/'
def b64(img,q=70):
    ok,buf=cv2.imencode('.jpg',img,[cv2.IMWRITE_JPEG_QUALITY,q]); return base64.b64encode(buf).decode()
out={}
# photo thumbnails
for i in range(1,6):
    im=cv2.imread(BASE+f'book{i}.jpeg'); h,w=im.shape[:2]; f=720/max(h,w)
    out[f'photo{i}']=b64(cv2.resize(im,None,fx=f,fy=f,interpolation=cv2.INTER_AREA),68)
k=cv2.imread(BASE+'key.jpg'); out['key']=b64(k,80)
# heading strips
for page,li,name in [('b3L',3,'head_b3L'),('b3R',0,'head_b3R')]:
    flat=boot.A[page]['flat']; pcs=boot.lines_of(page)[li]
    pc=[dict(cx=p['x']+p['w']/2,cy=p['y']+p['h']/2,h=p['h']) for p in pcs]
    hm=np.median([p['h'] for p in pc]); o,_=strips.straighten(flat,pc,up=int(0.9*hm),dn=int(0.8*hm))
    out[name]=b64(o,80)
g=cv2.imread(BASE+'book1.jpeg',0); out['year']=b64(g[2040:2250,2030:2800],80)
h5=cv2.imread(BASE+'book5.jpeg',0); out['b5row']=b64(h5[2150:2380,500:2000],80)
json.dump(out,open('report_extra.json','w')); print({k:len(v)//1000 for k,v in out.items()})
