import cv2, numpy as np, json
im = cv2.imread('original.png', 0)
S=4
big = cv2.resize(im, None, fx=S, fy=S, interpolation=cv2.INTER_CUBIC)
blur = cv2.GaussianBlur(big,(0,0),3)
bw = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,61,12)
k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
cl = cv2.morphologyEx(bw,cv2.MORPH_CLOSE,k)
n,lab,stats,cent = cv2.connectedComponentsWithStats(cl,connectivity=8)
boxes=[]
for i in range(1,n):
    x,y,w,h,a = stats[i]
    if a<500 or w<30 or h<30: continue
    boxes.append([int(x),int(y),int(w),int(h),int(a)])
# remove boxes contained in others
def contains(a,b):
    return a[0]<=b[0]+5 and a[1]<=b[1]+5 and a[0]+a[2]>=b[0]+b[2]-5 and a[1]+a[3]>=b[1]+b[3]-5
keep=[]
for i,b in enumerate(boxes):
    if any(i!=j and contains(boxes[j],b) and boxes[j]!=b for j in range(len(boxes))): continue
    keep.append(b)
print(len(boxes),len(keep))
ws=np.array([b[2] for b in keep]); hs=np.array([b[3] for b in keep])
print('w pct',np.percentile(ws,[10,25,50,75,90,99]))
print('h pct',np.percentile(hs,[10,25,50,75,90,99]))
json.dump(keep,open('work/boxes.json','w'))
# histogram of cy
cy=np.array([b[1]+b[3]/2 for b in keep])/S
hist,edges=np.histogram(cy,bins=np.arange(0,965,3))
for h,e in zip(hist,edges):
    print(int(e),'#'*h)
