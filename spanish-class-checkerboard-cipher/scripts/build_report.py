"""Generates index.html: the decipherment report, a clean HTML/CSS re-rendering of the board (cipher unit +
base-3 numeral + plaintext letter), the substitution tables and the encode/decode tool.
Run: /opt/homebrew/bin/python3.11 -I scripts/build_report.py"""
import os, json, html, collections
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
ver=json.load(open(os.path.join(ROOT,'figures','verify_alignment.json')))
BLACK_TOP=["IM BORED AND HAVE STUFF","TO DO"]
RED=["YEAH / READ THE TITLE / THIS MORNING I DECIDED TO LEARN A NEW",
     "CIPHER AND FOR SOME REASON I REALLY LIKED IT AND",
     "CAUGHT ONTO IT WITH INCREDIBLE SPEED / SINCE NOBODY WILL",
     "EVER READ THIS IM GONNA SHARE A SECRET WITH YOU /"]
BLACK_BOTTOM=["IM THE ONE WHO BROS THE","MIRROR"]
def trits(v): return (v%3,(v//3)%3,v//9)          # top, mid, bottom
def numeral(v):
    t,m,b=trits(v); return f"{b}{m}{t}"
def cell(x): return '<i class="c"></i>' if x==0 else '<i class="c st"></i>' if x==1 else '<i class="c sq"></i>'
def unit(v,letter,extra='',title=None,alt=None):
    t,m,b=trits(v)
    ttl=title or (f"{letter}: value {v}, base-3 {numeral(v)} (bottom→top), top/mid/bottom = {t}/{m}/{b}" if v else "space = empty column 000")
    cls='u'+(' sp' if v==0 else '')+(' '+extra if extra else '')
    altd=f'<div class="alt">{alt}</div>' if alt else ''
    return (f'<div class="{cls}" title="{html.escape(ttl)}"><div class="g">{cell(t)}{cell(m)}{cell(b)}</div>'
            f'<div class="n">{numeral(v)}</div><div class="l">{"␣" if v==0 else letter}</div>{altd}</div>')
def bar(): return '<div class="u bar" title="vertical bar (sentence mark)"><div class="g"><b></b></div><div class="n">&mdash;</div><div class="l">/</div></div>'
def excl(): return '<div class="u ex" title="literal exclamation mark (handwritten, not part of the code)"><div class="g"><span>!</span></div><div class="n">&mdash;</div><div class="l">!</div></div>'
def line_html(text,flags=None):
    """flags: dict {(word_index,letter_index): (extra_class,title,alt)}"""
    flags=flags or {}
    toks=text.split(' '); out=[]; wi=0; prev_bar=True
    i=0
    while i<len(toks):
        tk=toks[i]
        if tk=='/':
            out.append(('bar',bar())); prev_bar=True
        elif tk=='!!!':
            out.append(('w','<span class="word">'+excl()*3+'</span>'))
        else:
            if out and not prev_bar: out.append(('sp','<span class="word spw">'+unit(0,' ')+'</span>'))
            us=''
            for li,ch in enumerate(tk):
                f=flags.get((wi,li))
                us+=unit(ord(ch)-64,ch,*(f if f else ()))
            out.append(('w',f'<span class="word">{us}</span>')); wi+=1; prev_bar=False
        i+=1
    return ''.join(h for _,h in out)
ZIG='''<svg class="zig" viewBox="0 0 520 92" aria-label="sawtooth divider"><path d="M8,10 C140,6 300,6 508,22" stroke="#e0657a" stroke-width="1.2" fill="none" opacity=".55"/><path d="M8,62 L100,14 L116,48 L216,14 L236,54 L334,18 L356,58 L444,22 L466,54 L506,28" stroke="#222" stroke-width="3.2" fill="none" stroke-linejoin="round" stroke-linecap="round"/><path d="M8,84 C140,82 300,82 508,86" stroke="#e0657a" stroke-width="2" fill="none"/></svg>'''
flags_bottom={(4,3):('flag','Drawn as S (201: top stroke, bottom square). Swapping the two shapes gives K (102: top square, bottom stroke), probably intended: BROK(E).','K?')}
# top black: BORED drawn as two clusters (BOR | ED)
board=[]
board.append('<div class="blkblock"><div class="bl">black &middot; top block (double-scale cells)</div>')
board.append('<div class="line blk">'+line_html(BLACK_TOP[0])+'</div>')
board.append('<div class="line blk"><div class="grp">'+line_html(BLACK_TOP[1])+'</div>'+ZIG+'</div></div>')
board.append('<div class="redblock"><div class="bl">red &middot; body (single-scale cells)</div>')
glare={(0,0):None}
for n,t in enumerate(RED,1):
    extra={}
    html_line=line_html(t)
    if n==2:
        # mark 'IT' (word index 8) as hidden by glare in the photo
        fl={(8,0):('glare','Partly hidden by glare in the photo (read from context).',None),(8,1):('glare','Partly hidden by glare in the photo (read from context).',None)}
        html_line=line_html(t,fl)
    board.append(f'<div class="rl"><span class="ln">L{n}</span><div class="line">{html_line}</div></div>')
board.append('</div>')
board.append('<div class="blkblock"><div class="bl">black &middot; bottom block</div>')
board.append('<div class="line blk">'+line_html(BLACK_BOTTOM[0],flags_bottom)+'</div>')
board.append('<div class="line blk xl">'+line_html(BLACK_BOTTOM[1])+'<span class="word">'+excl()*3+'</span></div></div>')
BOARD='\n'.join(board)
# --- substitution tables
alltext=' '.join(BLACK_TOP+RED+BLACK_BOTTOM)
cnt=collections.Counter(ch for ch in alltext if 'A'<=ch<='Z')
def rows(vs):
    r=''
    sym=lambda x:'·╲□'[x]
    for v in vs:
        t,m,b=trits(v)
        let='␣' if v==0 else chr(64+v)
        red_cell='<div class="board mini"><div class="line">'+unit(v,let)+'</div></div>'
        blk_cell='<div class="board mini"><div class="line blk">'+unit(v,let)+'</div></div>'
        uses=str(cnt[chr(64+v)]) if v else ''
        r+=('<tr><td class="lt">'+let+' <span class="sm muted">'+str(v)+'</span></td><td class="mono">'+numeral(v)+'</td>'
            '<td class="mono">'+sym(t)+'&nbsp;'+sym(m)+'&nbsp;'+sym(b)+'</td>'
            '<td class="wb">'+red_cell+'</td><td class="wb">'+blk_cell+'</td><td class="n">'+uses+'</td></tr>')
    return r
head='<tr><th>Plain · value</th><th>Base-3<br><span class="sm">bottom→top</span></th><th>top · mid · bot</th><th>Red</th><th>Black</th><th class="n">Uses</th></tr>'
TABLES=''.join(f'<div class="tcol"><table class="sub">{head}{rows(vs)}</table></div>' for vs in (range(1,10),range(10,19),list(range(19,27))+[0]))
vr=ver['red']['P=47.0']['total']; vb=ver['black']['total']
subs={'EXACT_R':vr['exact'],'N_R':vr['expected'],'ONE_R':vr['exact']+vr['one_trit'],'EXACT_B':vb['exact'],'N_B':vb['expected'],'ONE_B':vb['exact']+vb['one_trit']}
tpl=open(os.path.join(HERE,'report_template.html')).read()
out=tpl.replace('@@BOARD@@',BOARD).replace('@@TABLES@@',TABLES)
for k,v in subs.items(): out=out.replace('@@'+k+'@@',str(v))
out=out.replace('@@PCT_R@@',str(round(100*vr['exact']/vr['expected']))).replace('@@PCT1_R@@',str(round(100*(vr['exact']+vr['one_trit'])/vr['expected'])))
out=out.replace('@@PCT_B@@',str(round(100*vb['exact']/vb['expected']))).replace('@@PCT1_B@@',str(round(100*(vb['exact']+vb['one_trit'])/vb['expected'])))
open(os.path.join(ROOT,'index.html'),'w').write(out)
print('wrote index.html',len(out))
