"""Builds ../../solved-puzzles.html: only the fully solved Gareth Penn puzzles, every value computed here."""
import math, os, html
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','solved-puzzles.html')
T='https://twitter.com/gareth_penn/status/'
def grid(s,w=7):
    rows=[s[i:i+w] for i in range(0,len(s),w)]
    cols=''.join(r[c] for c in range(w) for r in rows)
    h='<table class="g">'+''.join('<tr>'+''.join(f'<td class="c{c%2}">{html.escape(ch)}</td>' for c,ch in enumerate(r))+'</tr>' for r in rows)+'</table>'
    words=' '.join(cols[i:i+7] for i in range(0,len(cols),7))
    return h,cols,words
A='TPTD@EIWRHTPYFEIOWOEONLUEISRTTSNNCNYWATTAIAONYRLA'
B='DIYTTEIALTWPYFTTWEOEOEWENISRAENTNCNPNTYTAIRTYARLA'
gA,cA,wA=grid(A); gB,cB,wB=grid(B)
assert cA=='TWENTYAPRILTWOTHOUSANDTWENTY@POINTREYESCALIFORNIA' and cB=='DATEAPRILTWENTYTWENTYTWENTYATPOINTREYESCALIFORNIA'
n=42020
def fmt(x,ref):  # format like the tweet (same number of decimals)
    d=len(ref.split('.')[1]) if '.' in ref else 0
    return f'{x:.{d}f}' if d else str(x)
nums=[('22 Mar','1241692158295326721','A424',format(n,'X'),'42020 written in hexadecimal (A=10: 10·16³+4·16²+2·16+4)'),
      ('23 Mar','1242046870106411009','1765680400',str(n**2),'42020² ("the second power", the title of Penn\'s 1999 booklet)'),
      ('24 Mar','1242409841806589953','204.9878045153',fmt(math.sqrt(n),'204.9878045153'),'√42020'),
      ('25 Mar','1242770406135566338','74193890408000',str(n**3),'42020³'),
      ('26 Mar','1243134617395138562','34.7657830759',fmt(n**(1/3),'34.7657830759'),'∛42020'),
      ('27 Mar','1243522308691480577','4.62345604807',fmt(math.log10(n),'4.62345604807'),'log₁₀ 42020'),
      ('28 Mar','1243909420154679296','15.3587885416',fmt(math.log2(n),'15.3587885416'),'log₂ 42020')]
for _,_,tw,calc,_ in nums: assert tw==calc,(tw,calc)
numrows=''.join(f'<tr><td>{d}</td><td><a href="{T}{i}" class="mono">{tw}</a></td><td class="mono">{c}</td><td>{e}</td></tr>' for d,i,tw,c,e in nums)
def tob(x,b):
    s=''
    while x: s=str(x%b)+s; x//=b
    return s
reps=[tob(9320,b) for b in (6,7,8,9)]
assert reps==['111052','36113','22150','13705']
basrows=''.join(f'<tr><td class="mono">{r}</td><td>base {b}</td><td class="mono">{" + ".join(f"{dg}·{b}<sup>{len(r)-1-k}</sup>" for k,dg in enumerate(r) if dg!="0")} = 9320</td></tr>' for r,b in zip(reps,(6,7,8,9)))
P=sum(ord(c)-64 for c in 'PLYMOUTH'); assert P==130
page=f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Gareth Penn's puzzles: the solved ones</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{{margin:0;font:16px/1.55 Georgia,serif;color:#1d2430;background:#fbfaf7}} header{{background:#1d2430;color:#f3efe6;padding:24px 6vw}} header h1{{margin:0 0 6px;font-weight:normal}} header p{{margin:4px 0;color:#c9c3b6;max-width:900px}}
main{{padding:8px 6vw 50px;max-width:1100px}} h2{{font-weight:normal;color:#8a2f2f;border-bottom:2px solid #8a2f2f;padding-bottom:3px;margin-top:34px}} h3{{color:#24507a;margin:20px 0 6px}}
.mono{{font-family:ui-monospace,Menlo,monospace;font-size:14px}} a{{color:#24507a}} .muted{{color:#6a7280}} .ans{{background:#fff7e8;border-left:5px solid #9a6a00;padding:8px 14px;margin:10px 0}}
table.t{{border-collapse:collapse;margin:8px 0}} table.t td,table.t th{{border:1px solid #d9dde3;padding:4px 9px;text-align:left;vertical-align:top;font-size:15px}} table.t th{{background:#efece5}}
table.g{{border-collapse:collapse;display:inline-table;margin:6px 24px 6px 0}} table.g td{{width:26px;height:26px;text-align:center;font:15px ui-monospace,Menlo,monospace;border:1px solid #ddd}} td.c0{{background:#fff}} td.c1{{background:#f1ede3}}
.pair{{display:flex;flex-wrap:wrap;gap:20px;align-items:flex-start}} .pair div{{min-width:300px}}
</style></head><body>
<header><h1>Gareth Penn's puzzles: the solved ones</h1>
<p>Penn's 2020 tweet series that can be decoded completely. Each series is a "ticket": a date plus a place, stated many times in different disguises. Values on this page are recomputed, and every number matches Penn's tweet digit for digit. The full analysis, including the unsolved and partly read puzzles, is in <a href="index.html">index.html</a>.</p></header>
<main>

<h2>1. 20 April 2020, Point Reyes, California (21 Mar – 1 Apr 2020)</h2>
<div class="ans"><b>Answer:</b> eleven daily tweets all say <b>4/20/20 (42020)</b>; the first and last add the place, <b>Point Reyes, California</b>.</div>

<h3>1a. The two 49-letter tweets: 7×7 column transposition</h3>
<p>Write the 49 characters into a 7×7 square row by row, then read down the columns, left to right. The "@" means "at".</p>
<div class="pair">
<div><a href="{T}1241341034694467584">21 Mar 2020</a><br><span class="mono">{A}</span><br>{gA}<br>columns → <b>{wA}</b><br>= <b>TWENTY APRIL TWO THOUSAND TWENTY @ POINT REYES CALIFORNIA</b></div>
<div><a href="{T}1245310760856588290">1 Apr 2020</a><br><span class="mono">{B}</span><br>{gB}<br>columns → <b>{wB}</b><br>= <b>DATE APRIL TWENTY TWENTY TWENTY AT POINT REYES CALIFORNIA</b></div>
</div>

<h3>1b. The seven number tweets: one number, seven disguises</h3>
<p>Each number is a function of <b>42020</b>, the date 4/20/20 with the slashes removed.</p>
<table class="t"><tr><th>Tweet</th><th>As tweeted</th><th>Recomputed</th><th>How</th></tr>{numrows}</table>

<h3>1c. The three word tweets: things tied to 20 April</h3>
<table class="t"><tr><th>Tweet</th><th>As tweeted</th><th>How it points to 20 April</th></tr>
<tr><td>29 Mar</td><td><a href="{T}1244266363268395008">Aquilegia</a></td><td><i>Aquilegia</i> is the botanical genus of the columbine. That points to the Columbine High School massacre, <b>20 April</b> 1999.</td></tr>
<tr><td>30 Mar</td><td><a href="{T}1244585756015783936">Sulu, Moses Pray, Smeagol</a></td><td>Three characters whose actors were born on <b>20 April</b>: Sulu (George Takei, 1937), Moses "Moze" Pray in <i>Paper Moon</i> (Ryan O'Neal, 1941), Sméagol (Andy Serkis, 1964).</td></tr>
<tr><td>31 Mar</td><td><a href="{T}1244959018595962880">The ten commandments, Spartacus, An American in Paris, Cash McCall, Executive suite</a></td><td>The one actor in all five films is Nina Foch, born <b>20 April</b> 1924.</td></tr></table>
<p class="muted">Why 20 April: in <i>Times 17</i> (1987) Penn reads the Zodiac's "KFV" figure plus 26 as binary 42042 = "4-20-42", which he takes to be his suspect's conception date. 20 April 2020 is its anniversary. Point Reyes is where Penn's former employer, Point Reyes Bird Observatory, had its field station. This series was also reported solved on the YouTube channel "Zodiac Killer Insights" (video now unavailable).</p>

<h2>2. 3 September 2020, Plymouth, New York (27 Aug – 2 Sep 2020)</h2>
<div class="ans"><b>Answer:</b> the place is stated in plain text and the date is hidden in a number series: <b>9320 = 9/3/20</b>, the day after the last tweet.</div>
<table class="t"><tr><th>Tweet</th><th>Text</th></tr>
<tr><td><a href="{T}1299103211987451911">27 Aug 2020</a></td><td>All the factors add up to one place: Plymouth, New York.</td></tr>
<tr><td><a href="{T}1299354141458722822">28 Aug 2020</a></td><td>The exciting story of Plymouth, New York, is hitherto unknown to the public and has yet to be told. The truth will out.</td></tr>
<tr><td><a href="{T}1301127439238668288">2 Sep 2020</a></td><td class="mono">111052, 36113, 22150, 13705…</td></tr></table>
<h3>2a. The number series: one number in bases 6, 7, 8, 9</h3>
<table class="t"><tr><th>Term</th><th>Base</th><th>Value</th></tr>{basrows}</table>
<p>The "…" asks for the next term, base 10: <b>9320</b>, read as a date <b>9/3/20</b> (3 September 2020). This is how Penn writes dates as numbers elsewhere: TIMES 17 → 9745 → 9-7-45 in <i>Times 17</i>; a Copyright Office registration titled "8790".</p>
<h3>2b. "All the factors add up": why Plymouth</h3>
<p>With Penn's letter values (A=1 … Z=26), <b>PLYMOUTH</b> = 16+12+25+13+15+21+20+8 = <b>{P}</b>. Throughout his books, 130 is his number for the suspect's mother ("BER", for Berta). That makes the place itself part of his number vocabulary. <span class="muted">This reading of "add up" is ours; the date and place are not in doubt.</span></p>

<p class="muted" style="margin-top:40px">Tweet texts are from the collection's "Gareth Penn's puzzles – reddit post (updated) (and tweets)". The base-6–9 identification of 9320 was first noted there. Generated by <span class="mono">work/report/build_solved.py</span>.</p>
</main></body></html>'''
open(OUT,'w').write(page); print('wrote',os.path.abspath(OUT),len(page))
