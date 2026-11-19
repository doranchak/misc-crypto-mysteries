from pipeline import *
pages = {
 'b1': ('book1.jpeg',(330,1250,2800,3600), None),
 'b2R': ('book2.jpeg',(2050,900,3950,2750), None),
 'b2L': ('book2.jpeg',(330,150,2050,1350), None),
 'b3L': ('book3.jpeg',(30,780,1950,2750), None),
 'b3R': ('book3.jpeg',(1900,230,3950,2750), None),
}
res={}
for tag,(name,box,rot) in pages.items():
    reg,th,lab,gl,rot = process(name,box,rot,tag)
    overlay(reg,gl,f'seg/{tag}_ov.png')
    res[tag]=(reg,lab,gl,rot,box)
    cv2.imwrite(f'seg/{tag}_reg.png', reg)
pickle.dump({k:(v[2],v[3],v[4]) for k,v in res.items()}, open('seg/all_gl.pkl','wb'))
for k,v in res.items(): np.save(f'seg/{k}_lab.npy', v[1])
