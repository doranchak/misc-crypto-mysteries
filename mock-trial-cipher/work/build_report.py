import json, html, math
from collections import Counter
D='work/'
lines=[l.split() for l in open(D+'transcript_v2.txt')]
R=json.load(open(D+'results.json')); ST=json.load(open(D+'stats.json'))
UNI={'R':'⇒','r':'→','L':'⇐','l':'←','H':'↔','V':'↕','U':'↑','D':'↓','d':'↧','S':'↘','W':'↙','N':'↗','E':'⇆','b':'↳','u':'⊔↓','j':'↱',
     'A':'▲','Q':'◀','P':'▶','T':'▼','a':'△','q':'◁','p':'▷','t':'▽','X':'◯','-':'–','?':'█'}
DESC={'R':'double-line arrow pointing right (looks like an outlined block arrow)','r':'thin single-line arrow pointing right','L':'double-line arrow pointing left','l':'thin arrow pointing left',
'H':'double-headed horizontal arrow','V':'double-headed vertical arrow','U':'arrow pointing up','D':'arrow pointing down','d':'down arrow with a foot / underline (⊥)',
'S':'diagonal arrow pointing down-right','W':'diagonal arrow pointing down-left','N':'diagonal arrow pointing up-right','E':'two stacked opposite arrows (⇆)','b':'down stroke that hooks right (L-shaped)',
'u':'down arrow rising from a cup (⊔)','j':'7-shaped hook after a left arrow','A':'filled triangle, apex up (often drawn as a right-angle ◢)','Q':'filled triangle pointing left','P':'filled triangle pointing right','T':'filled triangle pointing down',
'a':'hollow triangle, apex up','q':'hollow triangle pointing left','p':'hollow triangle pointing right (drawn like a “D”)','t':'hollow triangle pointing down','X':'large hand-drawn oval/blob (only at the start of two lines)','-':'short horizontal dash','?':'hidden under a black redaction bar'}
# ---- machine-readable transcript
out=[]
for i,l in enumerate(lines,1):
    chunks=[];cur=[]
    for t in l:
        if t=='|':
            if cur: chunks.append(cur);cur=[]
        else: cur.append(t)
    if cur: chunks.append(cur)
    out.append(dict(line=i,chunks=[''.join(c) if all(len(x)==1 for x in c) else c for c in chunks],
                    code=' | '.join(' '.join(c) for c in chunks),
                    unicode=' '.join(''.join(UNI[x] for x in c) for c in chunks)))
json.dump(dict(source='https://www.reddit.com/r/ciphers/comments/1y3u3zu/need_assistance_with_cipher/',poster='u/Tinman886',
   note='Hand transcription of a halftone scan; one letter per glyph class (see alphabet); " | " / chunk boundaries = visible gaps; ? = hidden by a black bar; X = blob; - = dash. Accuracy not verified.',
   alphabet={k:dict(unicode=UNI[k],description=DESC[k]) for k in UNI},lines=out),open('transcript.json','w'),ensure_ascii=False,indent=1)
open('transcript.txt','w').write('# glyph codes; " | " = visible gap; see transcript.json for the alphabet\n'+'\n'.join(f"{o['line']:2d}: {o['code']}" for o in out)+'\n')
open('transcript_unicode.txt','w').write('\n'.join(f"{o['line']:2d}: {o['unicode']}" for o in out)+'\n')
# ---- tentative decode
mp=R['free']['mapping']
def dec(t): return mp.get(t,'?') if t not in ('X','-','?') else {'X':'·','-':'-','?':'█'}[t]
for o,l in zip(out,lines):
    chunks=[];cur=[]
    for t in l:
        if t=='|':
            if cur: chunks.append(cur);cur=[]
        else: cur.append(t)
    if cur: chunks.append(cur)
    o['decode']=' '.join(''.join(dec(x) for x in c) for c in chunks)
# ---- html
def esc(s): return html.escape(s)
cnt=Counter(t for l in lines for t in l if t!='|')
tot=sum(v for k,v in cnt.items() if k not in ('?','X','-'))
rows=''
for k,v in cnt.most_common():
    pct=100*v/tot if k not in ('?','X','-') else None
    bar=f'<span class="bar" style="width:{pct*3.2:.0f}px"></span>' if pct else ''
    rows+=f'<tr><td class="g">{esc(UNI[k])}</td><td><code>{k}</code></td><td>{esc(DESC[k])}</td><td class="n">{v}</td><td class="n">{"%.1f%%"%pct if pct else "–"}</td><td>{bar}</td></tr>'
def z(real,m,sd): return (real-m)/sd
f=R['free']; REAL=R['real_25restarts'][0]; ng=R['null_glyph_shuffle']; nc=R['null_chunk_shuffle']; nw=R['null_within_chunk_shuffle']; nr=R['null_reverse_each_chunk']
exp_rows=[
 ('Real transcript (25 restarts × 8 seeds, same effort as the nulls)',f"{R['real_25restarts'][0]:.0f} ± {R['real_25restarts'][1]:.0f}",'—','—'),
 ('Null: glyphs shuffled across the page',f"{ng[0]:.0f} ± {ng[1]:.0f}",f"{z(REAL,*ng):+.1f}σ",'destroys all order'),
 ('Null: gap-delimited chunks shuffled as units',f"{nc[0]:.0f} ± {nc[1]:.0f}",f"{z(REAL,*nc):+.1f}σ",'keeps repeated words, destroys word order'),
 ('Null: glyphs shuffled inside each chunk',f"{nw[0]:.0f} ± {nw[1]:.0f}",f"{z(REAL,*nw):+.1f}σ",'keeps chunk contents, destroys their order'),
 ('Control: every chunk reversed',f"{nr[0]:.0f} ± {nr[1]:.0f}",f"{z(REAL,*nr):+.1f}σ",'keeps repeats; tests reading direction'),
 ('Control: whole stream reversed',f"{R['reversed_stream']:.0f}",'—','reading direction matters (60 restarts: %d vs %d)'%(f['score'],R['reversed_stream'])),
]
exp=''.join(f'<tr><td>{a}</td><td class="n">{b}</td><td class="n">{c}</td><td>{d}</td></tr>' for a,b,c,d in exp_rows)
sub=''.join(f"<tr><td>{k}</td><td class='n'>{v['n']}</td><td class='n'>{v['score']:.0f}</td><td class='n'>{v['null_mean']:.0f} ± {v['null_sd']:.0f}</td><td class='n'>{(v['score']-v['null_mean'])/v['null_sd']:+.1f}σ</td><td class='n'>{100*v['coverage']:.0f}% (null {100*v['null_cov']:.0f}%)</td></tr>" for k,v in R['subsets'].items())
sim=R['sim']
lineblocks=''
for i,o in enumerate(out,1):
    flag=''
    if i in (4,14,20,23,26): flag='<span class="warn">partly hidden by a black bar</span>'
    if i in (18,19,20,21): flag=flag or '<span class="warn">lower confidence</span>'
    if i in (18,19,20): pass
    lineblocks+=f'''<div class="line"><div class="ln">line {i} {flag}</div><img src="img/line_{i:02d}.png" alt="line {i}">
<div class="uni">{esc(o['unicode'])}</div><div class="code">{esc(o['code'])}</div><div class="dec">{esc(o['decode'])}</div></div>'''
dec_all='\n'.join(f"{o['line']:2d}  {o['decode']}" for o in out)
mapping_tbl=' '.join(f"<span class='m'>{esc(UNI[k])}→{v}</span>" for k,v in sorted(mp.items(),key=lambda kv:-cnt.get(kv[0],0)))
wl=dict(ST['wordlen']); mx=max(wl.values())
wlbars=''.join(f"<div class='wl'><span>{k}</span><span class='bar' style='width:{wl[k]/mx*200:.0f}px'></span> {wl[k]}</div>" for k in sorted(wl))
page=f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Arrow &amp; triangle glyph cipher (r/ciphers 1y3u3zu) — transcription and decipherment attempt</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{{font-family:-apple-system,Segoe UI,Helvetica,Arial,sans-serif;max-width:1100px;margin:24px auto;padding:0 18px;color:#1d1d1f;line-height:1.5}}
h1{{font-size:26px;margin-bottom:4px}} h2{{margin-top:36px;border-bottom:2px solid #ddd;padding-bottom:4px}}
.sub{{color:#555;margin-top:0}} .status{{background:#fff4e5;border:1px solid #f0b866;border-radius:8px;padding:12px 16px;margin:16px 0}}
table{{border-collapse:collapse;font-size:14px;margin:10px 0}} td,th{{border:1px solid #ddd;padding:4px 8px;vertical-align:top}} th{{background:#f3f3f3;text-align:left}}
td.n{{text-align:right;font-variant-numeric:tabular-nums}} td.g{{font-size:22px;text-align:center;min-width:40px}}
.bar{{display:inline-block;height:10px;background:#4a7bd0;vertical-align:middle}}
.line{{margin:14px 0;padding:8px;border:1px solid #e3e3e3;border-radius:6px;background:#fafafa}} .line img{{width:100%;image-rendering:auto;border:1px solid #ddd;background:#fff}}
.ln{{font-size:12px;color:#666}} .warn{{background:#ffe8cc;color:#8a4b00;padding:1px 6px;border-radius:4px;margin-left:8px}}
.uni{{font-size:22px;letter-spacing:1px;margin-top:4px;word-break:break-word}} .code{{font-family:Menlo,monospace;font-size:13px;color:#444}} .dec{{font-family:Menlo,monospace;font-size:13px;color:#a33;display:none}}
body.showdec .dec{{display:block}}
.m{{display:inline-block;margin:2px 6px 2px 0;padding:1px 6px;background:#eef;border-radius:4px;font-size:14px}}
img.full{{max-width:100%;border:1px solid #ccc}} code{{background:#f2f2f2;padding:0 3px;border-radius:3px}}
.wl{{font-size:13px}} .wl span:first-child{{display:inline-block;width:22px;text-align:right;margin-right:6px}}
pre{{background:#f6f6f6;padding:10px;overflow:auto;font-size:13px}} details{{margin:8px 0}} summary{{cursor:pointer;font-weight:600}}
.cols{{display:grid;grid-template-columns:1fr 1fr;gap:20px}} @media(max-width:800px){{.cols{{grid-template-columns:1fr}}}}
button{{font-size:14px;padding:4px 10px}}
</style></head><body>
<h1>Arrow &amp; triangle glyph cipher — transcription and decipherment attempt</h1>
<p class="sub">Source: Reddit r/ciphers, <a href="https://www.reddit.com/r/ciphers/comments/1y3u3zu/need_assistance_with_cipher/">“Need assistance with cipher”</a>, posted by u/Tinman886. The image is the one attached to that post; Reddit blocks automated fetching, so the thread text and comments were <b>not</b> read and nothing here comes from them.</p>
<div class="status"><b>Status: not deciphered.</b>
<ul style="margin:6px 0 0 18px">
<li>The page is a note whose 26 lines of ciphertext are written in about 24 glyph types (arrows in several directions, double-headed arrows, filled and hollow triangles). Scribbled notes (“WHERE DID THIS $$ GO?!?”, “MORE MISSING $$$”, “DOES NOT ADD UP!!”, “SKIMMING?”, “CAN I EVER TRUST T?”) and black bars were added on top.</li>
<li>The glyph stream has real, direction-sensitive, English-like structure (substitution-solver score {z(REAL,*ng):.1f}σ above shuffled controls; the most common “word” ▲↑⇒ is read as <b>THE</b> by an unguided search), but <b>no readable plaintext came out</b>: only {100*f['coverage']:.0f}% of the best decode segments into common words, where a clean English substitution of this length gives ~{100*sim['0.0']:.0f}%.</li>
<li>The transcription below is my own visual reading of a low-resolution halftone scan. The statistics are consistent with roughly 30% symbol errors <i>or</i> with a cipher model I have not identified.</li></ul></div>
<h2>1. The image</h2>
<p><img class="full" src="original.png" alt="the cipher page"></p>
<p><b>Handwritten additions (not cipher text):</b> “WHERE DID THIS $$ GO?!?” (below line 5), “???” (right end of line 5), “MORE MISSING $$$” (right of lines 8–9), “!!!!” (right of lines 11–12), several single “?” marks beside lines 11, 15–16 and 23–25 (positions approximate), “DOES NOT ADD UP!!” and “SKIMMING?” (between lines 17 and 18), and “CAN I EVER TRUST T?” written across a black bar on line 23. Black bars also cover parts of lines 4, 14, 20, 23 and 26. The faint “MD” at the right edge of line 1 is show-through from the other side of the paper, not a glyph.</p>
<h2>2. Glyph alphabet (24 classes plus 3 marks)</h2>
<p>One code letter per visually distinct glyph class (these codes are my own labels, not plaintext). Counts exclude the blob, dash and hidden marks in the percentage. The thin/double-line variants (<code>r</code>/<code>R</code>, <code>l</code>/<code>L</code>) and the “foot” down-arrow <code>d</code> are kept separate here although they may be the same letter; the double-line right arrow <code>R</code> is a single homogeneous class (its shaft-line count is not bimodal).</p>
<table><tr><th>glyph</th><th>code</th><th>description</th><th>count</th><th>share</th><th></th></tr>{rows}</table>
<h2>3. Machine-readable transcription</h2>
<p>Downloads: <a href="transcript.json">transcript.json</a> (alphabet + per-line chunks), <a href="transcript.txt">transcript.txt</a> (codes), <a href="transcript_unicode.txt">transcript_unicode.txt</a> (Unicode arrows). Format: one line of the page per row, glyph codes separated by spaces, <code>|</code> = a visible gap (probable word boundary), <code>?</code> = hidden under a bar, <code>X</code> = blob. Each line below shows the straightened image strip, the Unicode rendering, and the codes.</p>
<p><button onclick="document.body.classList.toggle('showdec')">Show / hide tentative decode under every line (low confidence)</button></p>
{lineblocks}
<h2>4. Statistics</h2>
<div class="cols"><div>
<p><b>{ST['N']}</b> glyphs, <b>{ST['classes']}</b> classes, index of coincidence <b>{ST['IC']:.3f}</b> (English letters ≈ 0.067), entropy {ST['H']:.2f} bits. The double-line right arrow is {100*cnt['R']/tot:.0f}% of the text, far more than any single English letter.</p>
<p>Most repeated gap-delimited chunks: ▲↑⇒ (<code>AUR</code>) ×7, ▲↕▶ (<code>AVP</code>) ×5, <code>AV</code> ×3, <code>Hr</code> ×3, <code>uR</code> ×3. Most frequent bigrams: <code>AU</code> 17, <code>RR</code> 16, <code>UR</code> 15, <code>RA</code> 13, <code>aR</code> 10, <code>LR</code> 10, <code>RL</code> 10, <code>VP</code> 10. ▲ is followed by ↑ in 17 of its {cnt['A']} uses and ↑ is followed by ⇒ in 15 of {cnt['U']}: the shape of “TH-E”.</p>
<p>I checked by eye (zoomed crops) that the first glyph of every ▲↑⇒ and every ▲↕▶ is the same class (a filled right-angle triangle).</p></div>
<div><p>Chunk lengths (visible gaps; {ST['words']} chunks; typical of English words — peak at 3–4):</p>{wlbars}</div></div>
<h2>5. Decipherment attempts</h2>
<p><b>Method.</b> Monoalphabetic-substitution hill-climbing (simulated annealing over glyph→letter maps, 60 restarts) scored with a 5-gram English model (Wortschatz list), run on the glyph stream with gaps ignored. Every number below comes from <code>work/experiments.py</code>.</p>
<table><tr><th>test</th><th>score / 5-gram</th><th>real vs. test</th><th>what it checks</th></tr>{exp}</table>
<p>Reading: the real stream beats every null, including the chunk-shuffled one, and scores {R['reversed_stream']-f['score']:+.0f} when reversed, so there is order-dependent, left-to-right, language-like structure beyond the repeated words. Skipping hypotheses (suggested by the scribbled “SKIMMING?”) produce no better decode than their shuffled controls (word-coverage in the last column):</p>
<table><tr><th>subsequence</th><th>glyphs</th><th>score</th><th>shuffled null</th><th>z</th><th>decode in common words</th></tr>{sub}</table>
<p><b>Best tentative mapping</b> (unguided search; identical to the “THE” crib A=T, U=H, R=E): {mapping_tbl}. The competing crib ▲↑⇒=ARE, ▲↕▶=AND scores lower ({R['crib_are_and']['score']:.0f} vs {R['crib_the']['score']:.0f}).</p>
<details><summary>Tentative decode of the whole page (do not trust — see below)</summary><pre>{esc(dec_all)}</pre></details>
<p><b>Why this is not a solution.</b> Counting how much of the decode falls into common 4+ letter words: real {100*f['coverage']:.1f}% vs {100*R['null_coverage'][0]:.1f}% ± {100*R['null_coverage'][1]:.1f}% for shuffled controls, but a simulated clean English substitution of the same length decodes to {100*sim['0.0']:.0f}% with no noise, {100*sim['0.1']:.0f}% at 10% symbol errors, {100*sim['0.2']:.0f}% at 20%, {100*sim['0.3']:.0f}% at 30%. The fragments that look English (THE, TO THE, THROUGH, WOULD, WITH THE, THIS…) are what an n-gram hill-climb produces from almost any noisy input and should not be read as confirmation. In addition the English model does not explain the ⇒ glyph: it would have to be “E” at {100*cnt['R']/tot:.0f}% (English E is ≈12.7%), and it occurs in runs such as ⇒⇒⇒.</p>
<p><b>Tested and discarded:</b> ⇒ as a word space (gives 15–22-letter “words” and no solver signal); ▲↑⇒=ARE/▲↕▶=AND (lower score than THE); reading only arrows, only triangles, or every 2nd/3rd glyph; reversing the text; treating ⇒ as two glyphs by shaft-line count (not bimodal).</p>
<h2>6. What would help</h2>
<ul><li>A higher-resolution or original (non-halftone) scan: my class-level transcription is the weakest link, especially lines 18–21 and the lines crossed by bars.</li>
<li>The thread itself (title, body text, comments, any stated origin of the page — e.g. a game, book or ARG) which I could not read. If the glyph set matches a known script or puzzle, that would settle the model immediately.</li>
<li>Models I have <b>not</b> tested: a two-glyph-per-letter or numeric/ledger encoding, Morse-like binary coding by glyph property, a keyed or polyalphabetic variant, and a non-English plaintext.</li></ul>
<h2>7. Files</h2>
<ul><li><code>original.png</code> — the image; <code>img/line_NN.png</code> — straightened strips per line</li>
<li><code>transcript.json / .txt / _unicode.txt</code> — the machine-readable transcription</li>
<li><code>work/</code> — segmentation, tracking, solver (<code>hc.c</code>, <code>hc2.c</code>), <code>experiments.py</code>, <code>build_report.py</code>, <code>results.json</code>, <code>stats.json</code>. The 5-gram table <code>five.bin</code> is not kept (rebuild with <code>work/make_ngram.py</code> from the azdecrypt-lite Wortschatz list); <code>corpus_clean.txt</code> is the small English corpus used for the word-coverage test.</li></ul>
<p style="color:#777;font-size:13px;margin-top:30px">Puzzle credit: u/Tinman886 on r/ciphers (<a href="https://www.reddit.com/r/ciphers/comments/1y3u3zu/need_assistance_with_cipher/">thread</a>).</p>
</body></html>'''
open('index.html','w').write(page)
print('ok',len(page))
