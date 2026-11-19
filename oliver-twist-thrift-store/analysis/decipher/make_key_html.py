import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from keycells import letters, joined, doubles, digits
page=f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>Oliver Twist thrift-store cipher — substitution key (16:9, printable)</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{{box-sizing:border-box}}
html,body{{margin:0;background:#e9ebee;font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue",Arial,sans-serif;color:#000;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.stage{{position:relative;margin:0 auto;overflow:hidden}}
.slide{{position:absolute;left:0;top:0;width:1600px;height:900px;background:#fff;transform-origin:0 0;padding:22px 30px 0 30px}}
.top{{display:flex;justify-content:space-between;align-items:flex-end;height:50px;border-bottom:3px solid #000}}
.top h1{{margin:0;font-size:31px;letter-spacing:.2px;line-height:1.1}}
.top .sub{{font-size:14.5px;text-align:right;line-height:1.35;padding-bottom:3px}}
.grid{{display:grid;grid-template-columns:repeat(9,1fr);margin-top:10px;border-top:1px solid #777;border-left:1px solid #777}}
.c{{position:relative;height:190px;border-right:1px solid #777;border-bottom:1px solid #777}}
.c .l{{position:absolute;left:8px;top:2px;font-size:42px;font-weight:800;line-height:1}}
.c .g{{position:absolute;left:46px;right:3px;top:8px;height:140px;display:flex;align-items:center;justify-content:center;gap:6px}}
.c .g svg{{fill:#000;display:block;flex:none}}
.c .d{{position:absolute;left:0;right:0;bottom:6px;text-align:center;font-size:13.5px;color:#222}}
.c.stack .g{{flex-direction:column;gap:2px}}
.c.blank{{background:repeating-linear-gradient(135deg,#fff 0 9px,#f1f1f1 9px 10px)}}
.c .none{{color:#888;font-size:13px}}
.c.ap .l{{font-size:42px}}
.band{{margin-top:8px;font-size:15px;font-weight:700;letter-spacing:.3px;text-transform:uppercase}}
.grid2{{display:grid;grid-template-columns:repeat(11,1fr);margin-top:4px;border-top:1px solid #777;border-left:1px solid #777}}
.grid2 .c{{height:150px}}
.grid2 .c .l{{font-size:27px;left:6px;top:4px}}
.grid2 .c .g{{left:6px;right:6px;top:30px;height:94px}}
.grid2 .c .d{{font-size:12.5px;bottom:5px}}
.foot{{margin-top:7px;font-size:12.5px;line-height:1.38;color:#222;display:flex;gap:28px;justify-content:space-between}}
.foot div{{flex:1}}
.pg{{font-size:16px;font-weight:600;color:#666;margin-left:10px}}
.notes{{margin-top:12px;font-size:14.5px;line-height:1.45;color:#111}}
.notes div{{margin-bottom:9px}}
.m{{font-family:ui-monospace,Menlo,monospace;font-weight:700}}
@media print{{
  @page{{size:13.333in 7.5in;margin:0}}
  html,body{{background:#fff;width:13.333in}}
  .stage{{width:13.333in!important;height:7.5in!important;margin:0!important;page-break-after:always;break-after:page}}
  .slide{{transform:scale(.8)!important}}
}}
</style></head><body>
<div class="stage" data-s="1"><div class="slide">
 <div class="top"><h1>Oliver Twist thrift-store cipher &nbsp;·&nbsp; substitution key <span class="pg">1 / 2</span></h1>
  <div class="sub">one handwritten glyph per letter, joined in cursive · read left to right<br>find the glyph, read the letter in its box</div></div>
 <div class="grid">{letters}</div>
 <div class="band">Single glyphs that stand for two or three letters (and the end-of-sentence mark)</div>
 <div class="grid2">{joined}</div>
 <div class="foot">
  <div><b>Source of the key.</b> Page 1 of the book comes with a partial key (blue letters over the glyphs); every other letter was checked glyph by glyph in words on pages 2–3 and on the cover pages. Two examples are shown per letter; the hand varies a little.</div>
  <div><b>Cautions.</b> J, V and X are rare; Q and Z have not been seen. N and E are sometimes cut in two by the joins. Touching neighbours (IN, IS, AN …) are <i>not</i> special glyphs. Doubles and digits: slide 2.</div>
  <div><b>Puzzle.</b> r/codes “Found at a thrift store. How do I decode this?”, u/jar_of_spiders_. Plaintext: an expectant father's diary, June 1996.</div>
 </div>
</div></div>
<div class="stage" data-s="2"><div class="slide">
 <div class="top"><h1>Doubled letters, marks and block-hand digits <span class="pg">2 / 2</span></h1>
  <div class="sub">same hand · a repeated letter is written as one glyph<br>numbers use a separate upright “block” hand</div></div>
 <div class="band">Doubled letters: one glyph for the repeated letter</div>
 <div class="grid2">{doubles}</div>
 <div class="band">Block-hand digits (the row on the back cover, left to right = 1 2 3 4 5 6 7 8 9 0)</div>
 <div class="grid2">{digits}</div>
 <div class="notes">
  <div><b>Where the digits come from.</b> The back cover carries a row of ten block glyphs. The page-1 key reads the year as “1&nbsp;9&nbsp;9&nbsp;?”: the first glyph matches the first glyph of the row, and the two repeated glyphs match the ninth, so the row runs 1…9, 0. The fourth year glyph is then the sixth in the row, <b>6</b>. This is confirmed by the two headings on spread 3, which read <span class="m">960611.18:31</span> and <span class="m">960611.18:11</span> (YYMMDD.HH:MM): year 96, month 06 = June (page 1 says “June ninth”), day 11, and times 18:11 and 18:31. The title page repeats “1996”. Digits 2, 3, 4, 5, 7 and 8 rest on the row order only (3 and 8 occur in the time stamps).</div>
  <div><b>Doubled letters.</b> EE, TT, LL, SS, FF, CC and OO are each drawn as one glyph that looks like the letter with an extra stroke (SEEM, KEEP, FEEL · LITTLE, SITTING · STILL, REALLY · MESS, PASSING · OFFSPRING · ACCIDENTAL · GOOD, TOO). PP in APPARENTLY is written as two separate P's, and a few other doubles are ambiguous, so this list is only the pairs seen at least three times with a consistent shape.</div>
  <div><b>Not listed.</b> CK looks fused in one BACK but separate in the other, so it is left out. ION and similar endings are two touching glyphs, not a special one.</div>
 </div>
</div></div>
<script>
function fit(){{document.querySelectorAll('.stage').forEach(function(st){{var sl=st.firstElementChild,s=Math.min(innerWidth/1600,innerHeight/900);
 sl.style.transform='scale('+s+')';st.style.width=(1600*s)+'px';st.style.height=(900*s)+'px';st.style.marginTop=Math.max(0,(innerHeight-900*s)/2)+'px';}});}}
addEventListener('resize',fit);fit();
</script>
</body></html>'''
out='/Users/doranchak/projects/github/misc-crypto-mysteries/oliver-twist-thrift-store/substitution-key.html'
open(out,'w').write(page); print(len(page)//1000,'KB')
