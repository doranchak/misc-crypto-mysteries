"""Glyph cells of the substitution key (letters, joined glyphs, doubles, digits) as HTML strings.

Shared by make_key_html.py (printable 16:9 substitution-key.html) and build_index.py (key section at the
end of index.html). Data: key_glyphs.json (traced whole glyphs, see build_key3.py / build_key4.py).
"""
import json, html, os
G=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'key_glyphs.json'))); EX=G['ex']; FX=G['fx']
MEDH={'b1':112.0,'b2L':72.0,'b2R':72.0,'b3L':80.0,'b3R':80.0}
DESC={'A':'ring + centre dot','B':'arch, hooked foot','C':'zig-zag, long tail','D':'slant, two bars','E':'hooked 7','F':'three-bar D','G':'figure-8 loop','H':'small hooked loop','I':'slashed ellipse','J':'big zig-zag + curl','K':'H-like, cross-stroke','L':'open “3”','M':'tall loop','N':'wave ω + S-curve','O':'zig-zag + bar','P':'7 + one bar','Q':'not seen in the text','R':'“(” + dot','S':'C / Z + dot','T':'cup','U':'plain V','V':'plain Z, hooked foot','W':'slash + dots','X':'“3” + tick','Y':'plus “+”','Z':'not seen in the text',"'":'small raised loop'}
def svg(r,maxw=58,maxh=108,base=0.95):
    maxw=r.get('maxw',maxw); maxh=r.get('maxh',maxh)
    sc=min(base*72.0/MEDH.get(r.get('page','b2R'),72.0),maxw/r['w'],maxh/r['h'])
    w,h=r['w']*sc,r['h']*sc
    return f'<svg width="{w:.1f}" height="{h:.1f}" viewBox="0 0 {r["w"]:.1f} {r["h"]:.1f}"><path d="{r["d"]}" fill-rule="evenodd"/></svg>'
def cell(label,gl,desc,cls='',big=True):
    body=''.join(svg(r) for r in gl) if gl else '<span class="none">—</span>'
    return f'<div class="c {cls}"><div class="l">{html.escape(label)}</div><div class="g">{body}</div><div class="d">{html.escape(desc)}</div></div>'
EX['N']=[dict(r,maxw=116,maxh=66) for r in EX['N'][:2]]   # wide glyph: two examples stacked
FX['ING']=[dict(r,maxw=124,maxh=94) for r in FX['ING'][:1]]
letters=''.join(cell(L,EX.get(L,[]),DESC[L],'blank' if not EX.get(L) else ('stack' if L=='N' else '')) for L in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
letters+=cell('’',EX.get("'",[]),DESC["'"],'ap')
JD=[('TH','TH','T-cup + H hook'),('THE','THE','the word “the”'),('AND','AND','the word “and”'),('WH','WH','W slash + H loop'),('SH','SH','S + H loop'),('ING','–ING','wave + loop, no I'),('CH','CH','C + H'),('GH','GH','G + H'),('ST','ST','S + T'),('OU','OU','O + U')]
joined=''.join(cell(lbl,FX.get(k,[]),d,'j') for k,lbl,d in JD)
DB=[('OO','OO','double O'),('EE','EE','double E'),('TT','TT','double T'),('LL','LL','double L'),('SS','SS','double S'),('FF','FF','double F'),('CC','CC','double C')]
doubles=''.join(cell(lbl,FX.get(k,[]),d,'j') for k,lbl,d in DB)
dots='<svg width="60" height="40" viewBox="0 0 60 40"><circle cx="30" cy="9" r="4.5"/><circle cx="18" cy="31" r="4.5"/><circle cx="42" cy="31" r="4.5"/></svg>'
tilde='<svg width="80" height="40" viewBox="0 0 80 40"><path d="M8 24 C 18 6, 30 6, 40 20 S 62 34, 72 14" fill="none" stroke="#000" stroke-width="5" stroke-linecap="round"/></svg>'
joined+=f'<div class="c j"><div class="l">∴</div><div class="g">{dots}</div><div class="d">end of sentence</div></div>'
doubles+=f'<div class="c j"><div class="l">~</div><div class="g">{tilde}</div><div class="d">flourish ≈ comma</div></div>'
DG=G['digits']
def dsvg(r,maxw=56,maxh=84):
    sc=min(maxw/r['w'],maxh/r['h']); w,h=r['w']*sc,r['h']*sc
    return f'<svg width="{w:.1f}" height="{h:.1f}" viewBox="0 0 {r["w"]:.1f} {r["h"]:.1f}"><path d="{r["d"]}" fill-rule="evenodd"/></svg>'
digits=''.join(f'<div class="c j"><div class="l">{d}</div><div class="g">{dsvg(DG[d])}</div><div class="d"></div></div>' for d in '1234567890')
