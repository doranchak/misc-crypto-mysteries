import json
P=json.load(open('report_pages.json')); P.update(json.load(open('report_pages_covers.json')))
NAMES={'b1':'Page 1 (photo 1)','b2L':'Spread 2, left page (photo 2)','b2R':'Spread 2, right page (photo 2)','b3L':'Spread 3, left page (photo 3)','b3R':'Spread 3, right page (photo 3)',
       'b4L':'Inside cover, left page (photo 4)','b4R':'Title page, right page (photo 4)','b5':'Back cover digit row (photo 5)'}
out=["Oliver Twist thrift-store cipher — plaintext transcription",
"Legend: plain word = from key (page 1) or verified glyph-by-glyph; word? = uncertain reading.",
"The apostrophe is a small raised loop glyph (I'M, IT'S, DON'T); the key leaves a gap there and the apostrophes are restored on page 1.",
"Single glyphs that stand for several letters: THE, AND, TH, WH, SH, CH, GH, ST, OU, -ING and the doubled letters EE, TT, LL, SS, FF, CC, OO.",
"Block-hand numbers are digits (the row on the back cover reads 1 2 3 4 5 6 7 8 9 0): the year is 1996 and the two spread-3 headings are YYMMDD.HH:MM time stamps (960611.18:11 and 960611.18:31 = 11 June 1996, 18:11 and 18:31).",
"Spread 3 follows the requester's reading, aligned to the glyphs; three omissions in it were restored from the glyphs (MELANIE AND I . I JUST / SO I CAN'T / HELP IT IF). The cover lettering (photo 4) is the requester's reading; only JAMES ANDERSEN and the digits have glyph-level boxes.",
""]
for pg in ['b1','b2L','b2R','b3L','b3R','b4L','b4R','b5']:
    out.append(f"== {NAMES[pg]} ==")
    lines=list(P[pg]['lines'])
    if pg=='b3L':    # the two halves (21, 20) of one physical line are printed as one line
        k=[x for x,l in enumerate(lines) if l['i']==21]
        if k and k[0]+1<len(lines) and lines[k[0]+1]['i']==20:
            m=dict(lines[k[0]]); m['words']=lines[k[0]]['words']+lines[k[0]+1]['words']; lines[k[0]:k[0]+2]=[m]
    for q,ln in enumerate(lines):
        ln=dict(ln); ln['n']=q+1
        ws=[]
        for w in sorted(ln['words'],key=lambda w:w['x']):
            t=w['t']
            if w['f']=='D': t+= '*' if w['c']>=0.55 else '?'
            ws.append(t)
        out.append(f"L{ln['n']:02d}: "+' '.join(ws))
    out.append("")
open('/Users/doranchak/projects/github/misc-crypto-mysteries/oliver-twist-thrift-store/transcription.txt','w').write('\n'.join(out))
print('\n'.join(out))
