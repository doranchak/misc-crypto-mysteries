import cv2, sys, numpy as np
src, dst = sys.argv[1], sys.argv[2]
im = cv2.imread(src, cv2.IMREAD_GRAYSCALE)
im = cv2.resize(im, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
bg = cv2.morphologyEx(im, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(41,41)))
norm = cv2.divide(im, bg, scale=255)
norm = cv2.GaussianBlur(norm,(3,3),0)
_, th = cv2.threshold(norm, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
cv2.imwrite(dst, th)
