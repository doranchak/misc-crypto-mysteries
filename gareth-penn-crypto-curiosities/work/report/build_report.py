import json, re, datetime, os
R=os.path.dirname(os.path.abspath(__file__)); W=os.path.dirname(R); OUT=os.path.join(os.path.dirname(W),'index.html')
t=open(os.path.join(R,'template.html')).read()
mj=os.path.join(W,'methods.json')
data=json.load(open(mj)) if os.path.exists(mj) else {"categories":[],"methods":[],"glossary":[],"timeline":[]}

def _rows(path,a,b):
    out=[]
    for l in open(path).read().splitlines()[a-1:b]:
        t=l.strip().split()
        if t and (re.fullmatch(r'[A-Z0-9]+',t[0]) or re.fullmatch(r'[01.]+',t[0])): out.append(t[0])
    return ''.join(out)
D=os.path.join(W,'docx')
T408=_rows(os.path.join(D,'340_793.txt'),46,69); CONF=_rows(os.path.join(D,'_radian_.txt'),619,638)
LA=_rows(os.path.join(D,'_radian_.txt'),46,71); DRAGON=_rows(os.path.join(D,'gareth penn sample.txt'),174,194)
HOLE=_rows(os.path.join(D,'gareth penn sample.txt'),46,58)
BITS=''.join(l.split()[1] for l in open(os.path.join(W,'extract','mensa_cryptogram.md')).read().splitlines()[161:181] if len(l.split())==2)
assert len(T408)==408 and len(CONF)==340 and len(BITS)==340, (len(T408),len(CONF),len(BITS))
GRID={'#213':T408+'|THAE','408 rows 13-16':T408+'|THAE','#103..#305':CONF+'|','Dragon Card':DRAGON+'|ONE','rect 4x15':DRAGON+'|ONE',
      'rect 6x11':LA+'|RIVERSIDE','340 dots':BITS+'|0010010000111','340-digital':BITS+'|0010010000111','bits':BITS+'|10000010'}
def norm(dm):
    w=dm.get('widget') or 'none'; p=str(dm.get('preset') or '')
    if w in ('morse','wizard','anagram','hypotenuse','cubes','nines'): return w,p
    if w=='base': return ('morse',p) if p.startswith('.') else ('binary',p)
    if w=='radian': return ('morse',p) if p in ('JU.LY','RADIAN') else (('binary',p) if p.isdigit() and p!='1' else ('radian',''))
    if w=='calendar':
        if '..' in p: return 'dayofyear',p.replace('..','|')
        if p.startswith('OCT5'): return 'grid17',HOLE+'|PI|4|1970-10-05'
        return 'none',''
    if w=='dayofyear':
        if p=='7/31': return w,'1969-07-31'
        return (w,p) if re.fullmatch(r'\d{4}-\d\d-\d\d',p) else ('none','')
    if w=='gematria': return (w,p) if re.fullmatch(r'[A-Z]+',p.replace(' ','')) and p!='SOMEONELL FIND HER' else ('none','')
    if w=='grid17':
        if p.startswith('THECONFESSION'): return w,CONF+'|BEAUTIFUL'
        return (w,GRID[p]) if p in GRID else ('none','')
    if w=='squares': return ('cubes',p) if p.isdigit() else ('none','')
    if w=='rebus':
        m=re.fullmatch(r'(\d+) (before|over) (\d+)',p)
        return ('rebus',f'{m.group(1)}|{m.group(3)}') if m else ('none','')
    if w=='redivision':
        if p=='IAMNOTSICKIAMINSANE': return 'redivision',p+'|BERTA'
        if '|' in p: return w,p
        if p=='SUPERBOWL': return 'none',''
        return 'decode',p
    return 'none',''
for m in data['methods']:
    dm=m.get('demo') or {}
    w,p=norm(dm); m['demo']={'widget':w,'preset':p,'expect':dm.get('expect','') if w!='none' else ''}

OVR={'pun-homophone':('morse','1 UP'),'expressive-postmark-digits':('cubes','731'),'char-per-day-calendar':('grid17',HOLE+'|PI|4|1970-10-05'),
     'radian-supplement-birthdate':('none',''),'bm-number-range':('binary','1140')}
for m in data['methods']:
    if m['id'] in OVR: w,p=OVR[m['id']]; m['demo']['widget']=w; m['demo']['preset']=p
pz=open(os.path.join(R,'puzzles.html')).read()
pz=pz.replace('<h2>1. ','<h2>5. ').replace('<h2>2. ','<h2>6. ')
pz=re.sub(r'<h3 id="([^"]+)">2\.(\d)',r'<h3 id="\1">6.\2',pz).replace('(section 2.1)','(section 6.1)').replace('(section 2.2)','(section 6.2)').replace('(section 2.4)','(section 6.4)')
summ=open(os.path.join(R,'summary.html')).read().replace('{{NMETHODS}}',str(len(data['methods']))).replace('{{NCATS}}',str(len(data['categories'])))
src=open(os.path.join(R,'sources.html')).read() if os.path.exists(os.path.join(R,'sources.html')) else '<p>(pending)</p>'
rep={'{{DATE}}':datetime.date.today().strftime('%d %B %Y'),'{{SUMMARY}}':summ,'{{SOURCES}}':src,'{{PUZZLES}}':pz,
     '{{NOTES}}':open(os.path.join(R,'notes.html')).read(),'{{WORDS}}':open(os.path.join(R,'words.txt')).read(),
     '{{METHODS_JSON}}':json.dumps(data,ensure_ascii=False).replace('</','<\\/'),'{{WIDGETS_JS}}':open(os.path.join(R,'widgets.js')).read()}
for k,v in rep.items(): t=t.replace(k,v)
t=t.replace('<h2>7. Notes','<h2>7. Notes')
open(OUT,'w').write(t); print('wrote',OUT,len(t),'bytes;',len(data['methods']),'methods')
