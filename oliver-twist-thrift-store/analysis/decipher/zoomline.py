import sys, cv2, numpy as np, boot
from showline import show
page=sys.argv[1]; li=int(sys.argv[2]); j0=int(sys.argv[3]); j1=int(sys.argv[4]); out=sys.argv[5]; sc=float(sys.argv[6]) if len(sys.argv)>6 else 2.6
show(page,li,j0,j1,out,scale=sc,pad=10)
