import sys, subprocess, os
src,out=sys.argv[1:3]; out=os.path.abspath(out); idx=sys.argv[3] if len(sys.argv)>3 else '0'; W=sys.argv[4] if len(sys.argv)>4 else '1300'; H=sys.argv[5] if len(sys.argv)>5 else '1100'
s=open(src).read()
inj="""<script>window.addEventListener('load',()=>{
 const tabs=[...document.querySelectorAll('table.ltab')]; const t=tabs[%s];
 const box=document.createElement('main'); box.appendChild(t); document.body.innerHTML=''; document.body.appendChild(box);
});</script></body>"""%idx
tmp=out+'.html'; open(tmp,'w').write(s.replace('</body>',inj))
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
subprocess.run([CH,'--headless=new','--disable-gpu','--user-data-dir='+out+'.prof','--window-size=%s,%s'%(W,H),'--virtual-time-budget=10000','--screenshot='+out,'file://'+tmp],capture_output=True,timeout=180)
print(os.path.getsize(out))
