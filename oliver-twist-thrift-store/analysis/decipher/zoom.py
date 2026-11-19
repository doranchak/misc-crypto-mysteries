import sys; sys.path.insert(0,'..')
import cv2, numpy as np, pickle
import boot
def zoom(page,li,j0,j1,scale=2.6,out=None):
    pcs=boot.lines_of(page)[li]
    flat=boot.A[page]['flat'] if page!='b1' else pickle.load(open('b1_pieces.pkl','rb'))['flat']
    sel=pcs[j0:j1+1]
    x0=int(min(p['x'] for p in sel))-25; x1=int(max(p['x']+p['w'] for p in sel))+25
    y0=int(min(p['y'] for p in sel))-25; y1=int(max(p['y']+p['h'] for p in sel))+25
    img=cv2.cvtColor(flat[max(0,y0):y1,max(0,x0):x1],cv2.COLOR_GRAY2BGR)
    for j in range(j0,j1+1):
        p=pcs[j]; col=(0,0,255) if j%2==0 else (255,0,0)
        cv2.rectangle(img,(int(p['x']-x0),int(p['y']-y0)),(int(p['x']+p['w']-x0),int(p['y']+p['h']-y0)),col,1)
        cv2.putText(img,str(j),(int(p['x']-x0),max(12,int(p['y']-y0)-3)),cv2.FONT_HERSHEY_SIMPLEX,0.5,col,1)
    img=cv2.resize(img,None,fx=scale,fy=scale,interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(out or f'../lines/z_{page}_{li}_{j0}_{j1}.png',img); return img.shape
if __name__=='__main__':
    page=sys.argv[1]; li,j0,j1=[int(a) for a in sys.argv[2:5]]
    sc=float(sys.argv[5]) if len(sys.argv)>5 else 2.6
    print(zoom(page,li,j0,j1,sc))
