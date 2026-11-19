import sys, subprocess, os
# usage: shot_viz.py <index.html> <out.png> <tabRegex> [zoomPct] [W] [H] [clipTop] 
src,out,tab=sys.argv[1:4]; out=os.path.abspath(out); zoom=sys.argv[4] if len(sys.argv)>4 else '100'; W=sys.argv[5] if len(sys.argv)>5 else '1400'; H=sys.argv[6] if len(sys.argv)>6 else '1500'
s=open(src).read()
inj="""<script>window.addEventListener('load',()=>{
 const tabs=[...document.querySelectorAll('#vtabs .tab')]; const t=tabs.find(b=>new RegExp('%s','i').test(b.textContent))||tabs[2]; 
 const keep=[document.getElementById('vtabs'),document.querySelector('.ctrl'),document.getElementById('vwrap')];
 const box=document.createElement('div'); keep.forEach(k=>box.appendChild(k)); document.body.innerHTML=''; document.body.appendChild(box);
 document.getElementById('vwrap').style.maxHeight='none'; const z=document.getElementById('c_zoom'); z.value=%s; z.oninput&&z.oninput(); t.click();
});</script></body>"""%(tab,zoom)
tmp=out+'.html'; open(tmp,'w').write(s.replace('</body>',inj))
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
subprocess.run([CH,'--headless=new','--disable-gpu','--user-data-dir='+out+'.prof','--window-size=%s,%s'%(W,H),'--virtual-time-budget=10000','--screenshot='+out,'file://'+tmp],capture_output=True,timeout=180)
print(os.path.getsize(out))
