import pickle, json, collections, html
d=pickle.load(open('seg/report_data.pkl','rb')); media=pickle.load(open('seg/media.pkl','rb'))
FCH={f:v['ch'] for f,v in d['fam'].items()}; FCH['junk']='~'
TITLES={'b1':'Page 1 — first handwritten page after the title (book1.jpeg)',
        'b2L':'Spread 2, left page (book2.jpeg)','b2R':'Spread 2, right page (book2.jpeg)',
        'b3L':'Spread 3, left page (book3.jpeg)','b3R':'Spread 3, right page (book3.jpeg)'}
# compact viewer data (no images)
V={'fam':{f:dict(ch=v['ch'],desc=v['desc'],n=v['n'],pos=v['pos'],clusters=v['clusters']) for f,v in d['fam'].items()},'pages':{}}
V['fam']['junk']=dict(ch='~',desc='flourish "~" at line ends and stroke fragments (not letters)',n=0,pos={},clusters=[0,2,6,15,19,7])
transcript=[]; txt_lines=[]
for tag,pg in d['pages'].items():
    lines=[]
    for li,items in enumerate(pg['lines']):
        li_out=[]
        s=[]
        for it in items:
            if it['type']=='w':
                li_out.append({'t':'w','g':[[g['x'],g['y'],g['w'],g['h'],g['c'],g['f']] for g in it['glyphs']]})
                s.append(''.join(FCH.get(g['f'],'?') for g in it['glyphs']))
            else:
                li_out.append({'t':'p','x':it['cx'],'y':it['cy']}); s.append('∴')
        lines.append(li_out); txt_lines.append(f'{tag} L{li+1:02d}: '+' '.join(s))
    V['pages'][tag]=dict(title=TITLES[tag],scale=pg['scale'],w=pg['w'],h=pg['h'],lines=lines)
    txt_lines.append('')
open('transcription.txt','w').write('\n'.join(txt_lines))
# stats
tot_glyph=sum(v['n'] for v in d['fam'].values())
rows=[]
for f,v in sorted(d['fam'].items(),key=lambda t:-t[1]['n']):
    p=v['pos']; n=max(1,v['n'])
    rows.append(dict(f=f,ch=v['ch'],desc=v['desc'],n=v['n'],single=p.get('single',0),first=p.get('first',0),mid=p.get('mid',0),last=p.get('last',0),cl=v['clusters']))
thumbs={}
for f,v in d['fam'].items():
    ts=[]
    for c in v['clusters']:
        ts+=d['cl'].get(str(c),{}).get('thumbs',[])[:2]
    thumbs[f]=ts[:4]
tpl=open('template.html').read()
out=tpl.replace('/*VIEWDATA*/',json.dumps(V,ensure_ascii=False,default=int)).replace('/*ROWS*/',json.dumps(rows,ensure_ascii=False,default=int)).replace('/*THUMBS*/',json.dumps(thumbs,default=int))
imgs=''.join(f'<img id="pg-{t}" src="data:image/jpeg;base64,{pg["img"]}" alt="">' for t,pg in d['pages'].items())
out=out.replace('<!--PAGEIMGS-->',imgs)
for k,v in media.items(): out=out.replace('{{'+k+'}}','data:image/jpeg;base64,'+v)
out=out.replace('{{TOTG}}',str(tot_glyph))
open('index.html','w').write(out)
print(len(out)//1024,'KB')
