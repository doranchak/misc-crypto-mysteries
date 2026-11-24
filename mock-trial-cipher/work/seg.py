import cv2, numpy as np, json, sys
im = cv2.imread('original.png', 0)
S=4
big = cv2.resize(im, None, fx=S, fy=S, interpolation=cv2.INTER_CUBIC)
blur = cv2.GaussianBlur(big,(0,0),3)
bw = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,61,12)
k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
cl = cv2.morphologyEx(bw,cv2.MORPH_CLOSE,k)
n,lab,stats,cent = cv2.connectedComponentsWithStats(cl,connectivity=8)
comps=[]
for i in range(1,n):
    x,y,w,h,a = stats[i]
    if a<400 or w<25 or h<25: continue
    comps.append(dict(id=i,x=int(x),y=int(y),w=int(w),h=int(h),a=int(a),cy=float(cent[i][1]),cx=float(cent[i][0])))
print(len(comps))
# cluster into lines by cy
comps.sort(key=lambda c:c['cy'])
lines=[]
for c in comps:
    if lines and abs(c['cy']-np.mean([d['cy'] for d in lines[-1]]))<45:
        lines[-1].append(c)
    else:
        lines.append([c])
for i,l in enumerate(lines):
    ys=[c['cy'] for c in l]
    print(i, int(np.mean(ys)/S), len(l), int(min(c['x'] for c in l)/S), int(max(c['x']+c['w'] for c in l)/S))
