#!/opt/homebrew/bin/python3.11
"""Builds ../index.html: the single report page (reading, key, line-by-line view, how it was found)."""
import json, os, html, sys, collections
HERE=os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE+'/..'); sys.path.insert(0,HERE)
from reading_data import R, KEY
T=json.load(open('transcript.json')); AL=T['alphabet']; EV=json.load(open('work2/evidence.json'))
SOL={int(l.split(':')[0]):l.split(':',1)[1].strip() for l in open('solver_decode.txt') if l[:2].strip().isdigit()}
esc=html.escape
conf={3:('high','#d8f0d8'),2:('medium','#fff2c2'),1:('low','#ffd9d2')}
nh,nm,nl=(sum(1 for r in R if r[2]==k) for k in (3,2,1))
# data files
open('reading.txt','w').write('# Close reading. [ ] = letters supplied by me, ? = unread, ███ = blacked out on the page\n'+'\n'.join(f'{li:2d}: {t}' for li,t,c,g,n in R)+'\n')
json.dump([dict(line=li,reading=t,confidence=conf[c][0],glyphs=g,note=n) for li,t,c,g,n in R],open('reading.json','w'),indent=1,ensure_ascii=False)
# line blocks
blocks=''
for li,txt,c,g,note in R:
    first=T['lines'][li-1]
    blocks+=(f'<div class="line"><div class="ln">line {li} — confidence: <span class="cf" style="background:{conf[c][1]}">{conf[c][0]}</span></div>'
      f'<img src="img/line_{li:02d}.png" alt="line {li}"><div class="uni">{esc(g)}</div><div class="rd">{esc(txt)}</div>'
      +(f'<div class="nt">{esc(note)}</div>' if note else '')
      +f'<details><summary>earlier stages of this line</summary><div class="old">first-pass transcription: <span class="u2">{esc(first["unicode"])}</span><br>codes: <code>{esc(first["code"])}</code><br>solver output before the close reading: <code>{esc(SOL.get(li,""))}</code></div></details></div>')
krows=''.join(f'<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td></tr>' for a,b,c in KEY)
# first-pass glyph classes
cnt=collections.Counter(ch for L in T['lines'] for c in L['chunks'] for ch in c)
tot=sum(v for k,v in cnt.items() if k in AL)
grows=''.join(f'<tr><td class="g">{AL[k]["unicode"]}</td><td><code>{k}</code></td><td>{esc(AL[k]["description"])}</td><td class="n">{cnt[k]}</td><td class="n">{100*cnt[k]/tot:.1f}%</td></tr>' for k in sorted(AL,key=lambda k:-cnt[k]))
def ev(s,label):
    e=EV[s]; return (f'<tr><td>{label}</td><td class="n">{e["real_score"]:.0f}</td><td class="n">{e["null_mean"]:.0f} ± {e["null_sd"]:.0f}</td><td class="n">{e["real_score"]-e["null_mean"]:.0f}</td>'
      f'<td class="n">{100*e["real_vocab"]:.1f}%</td><td class="n">{100*e["null_vocab_mean"]:.1f}% (max {100*e["null_vocab_max"]:.1f}%)</td></tr>')
evrows=ev('none','one letter per glyph class')+ev('R3','⇒ split 3 ways')+ev('R3,A2','⇒ split 3 ways, ▲ split 2 ways')+ev('R3,A2,L2','⇒ ×3, ▲ ×2, ⇐ ×2')
walk=[('6×4 torus, steps 2/2/1/2/2, ↔↕ two cells',9,'−1952','−1973','21'),('6×4 torus, 2/2/1/2/2, ↔↕ two cells (variant)',14,'−1964','−1999','35'),('2×13 torus, all 1, ↔↕ mirror',19,'−2007','−2017','11'),('2×13 torus, 1/1/2/1/1, ↔↕ mirror',20,'−2019','−2042','23'),('6×4 torus, 2/2/1/2/2, ↔↕ mirror',23,'−2032','−2118','86'),('2×13 torus, 1/2/2/2/2, ↔↕ two cells',17,'−2038','−2099','61'),('3×8 torus, 2/2/1/2/2, ↔↕ two cells',20,'−2052','−2101','50'),('6×4 torus, 1/2/1/2/2, ↔↕ two cells',22,'−2041','−2089','48'),('5×5 clamped, all 1, ↔↕ two cells',21,'−2109','−2154','45'),('4×6 clamped, 2/2/1/2/2, ↔↕ two cells',20,'−2072','−2117','45'),('5×5 torus, all 2, ↔↕ two cells',25,'−2163','−2164','2')]
walkrows=''.join(f'<tr><td>{a}</td><td class="n">{b}</td><td class="n">{c}</td><td class="n">{d}</td><td class="n">{e}</td></tr>' for a,b,c,d,e in walk)
THREAD='https://www.reddit.com/r/ciphers/comments/1y3u3zu/need_assistance_with_cipher/'
page=f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Arrow &amp; triangle glyph cipher (r/ciphers 1y3u3zu) — transcription and decipherment</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{{font-family:-apple-system,Segoe UI,Helvetica,Arial,sans-serif;max-width:1150px;margin:24px auto;padding:0 18px;color:#1d1d1f;line-height:1.5}}
h1{{font-size:26px;margin-bottom:4px}} h2{{margin-top:36px;border-bottom:2px solid #ddd;padding-bottom:4px}} h3{{margin-top:22px}}
.sub{{color:#555;margin-top:0}} .status{{background:#e8f5e9;border:1px solid #7cbf86;border-radius:8px;padding:12px 16px;margin:16px 0}}
.warnb{{background:#fff4e5;border:1px solid #f0b866;border-radius:8px;padding:10px 14px;margin:14px 0}}
table{{border-collapse:collapse;font-size:14px;margin:10px 0}} td,th{{border:1px solid #ddd;padding:4px 8px;vertical-align:top}} th{{background:#f3f3f3;text-align:left}}
td.n{{text-align:right;font-variant-numeric:tabular-nums}} td.g{{font-size:22px;text-align:center;min-width:40px}}
.line{{margin:14px 0;padding:8px;border:1px solid #e3e3e3;border-radius:6px;background:#fafafa}} .line img{{width:100%;border:1px solid #ddd;background:#fff}}
.ln{{font-size:12px;color:#666}} .cf{{padding:1px 6px;border-radius:4px;color:#222}}
.uni{{font-size:21px;letter-spacing:1px;margin-top:4px;word-break:break-word}} .rd{{font-family:Menlo,monospace;font-size:16px;font-weight:600;color:#7a1f1f;margin-top:2px}} .nt{{font-size:13px;color:#555;margin-top:2px}}
.old{{font-size:13px;color:#555;margin:4px 0 0 14px}} .u2{{font-size:17px}} details{{margin:6px 0}} summary{{cursor:pointer;font-size:13px;color:#555}} h2+details>summary,details.big>summary{{font-size:15px;font-weight:600;color:#1d1d1f}}
pre{{background:#f6f6f6;padding:12px;overflow:auto;font-size:14px;line-height:1.45}} code{{background:#f2f2f2;padding:0 3px;border-radius:3px}}
img.full{{max-width:100%;border:1px solid #ccc}}
</style></head><body>
<h1>Arrow &amp; triangle glyph cipher — transcription and decipherment</h1>
<p class="sub">Source: Reddit r/ciphers, <a href="{THREAD}">“Need assistance with cipher”</a>, posted by u/Tinman886. I could not open the thread (Reddit blocked every fetch), so everything here comes from the image alone.</p>
<div class="status"><b>Status: mostly read.</b> The cipher is a one-glyph-per-letter substitution with word gaps and punctuation. Lines 1–16 and 21–23 read as continuous English ({nh} lines high confidence, {nm} medium, {nl} low); lines 17–20 and 24–26 are still partly or wholly unread, and three stretches are blacked out on the page.
<p style="margin:8px 0 0">The message is a taunt from the people who write the Pennsylvania mock-trial case, addressed to whoever decodes it: breaking the code gives no insight into the case.</p></div>

<h2>1. Reading</h2>
<pre>{esc(chr(10).join(f"{li:2d}  {t}" for li,t,c,g,n in R))}</pre>
<p><code>[ ]</code> = letters I supplied where the drawn glyphs say something else or are missing, <code>?</code> = unread, <code>███</code> = blacked out on the page, <code>(?)</code> = doubtful word.</p>
<p>As running text, for the part I trust:</p>
<div class="warnb">Pennsylvania Mock Trial is amazing. It is great for students, the teachers, and, and, of course the law[,] lawyers involved. If you thought [written: through] by breaking this code, you would get insight into the case, you are wrong. But we really appreciate the effort in trying. Paul and [?] have been working on the case material[s] for going on two decades now. Do you really think we would give an advantage to a team because they got a … Wingding … with the… [unread] … we love that … we love ███ did this. … we obsess deeply about Mock Trial and … and months with this problem. I ███ … from the mountains(?) to the … [unread to the end].</div>
<p>Downloads: <a href="reading.txt">reading.txt</a>, <a href="reading.json">reading.json</a> (reading, glyphs as re-read, and a note per line).</p>

<h2>2. The image</h2>
<p><img class="full" src="original.png" alt="the cipher page"></p>
<p><b>Handwritten additions (not cipher text):</b> “WHERE DID THIS $$ GO?!?”, “???”, “MORE MISSING $$$”, “!!!!”, “DOES NOT ADD UP!!”, “SKIMMING?”, “CAN I EVER TRUST T?”, several single “?” marks, and black bars over parts of lines 4, 14, 20, 23 and 26. They have nothing to do with the decoded text as far as it is read.</p>

<h2>3. How far to trust the reading</h2>
<ul>
<li><b>It is a human reading guided by a solver.</b> A statistical solver produced a rough decode (section 6); I then went through every line at roughly 6–14× magnification and re-read each glyph where the solver text broke a word.</li>
<li><b>Inferred, not seen:</b> which double-line right arrow ⇒ is A, C or E, and which left arrow ⇐ is B or D. I compared the three ⇒ of TEACHERS with those of DECADES and found no consistent visible difference at this resolution; the words fix them by context only.</li>
<li><b>The writer made slips</b> (or the drawing is loose): “FOE” for FOR, “EF” for IF, THROUGH where THOUGHT is meant, “ADV ADVAGE”, “BECUWE”, “MOUAINS”. The reading shows the intended word in brackets; the glyph row in section 5 shows what is drawn. Because of this, a doubtful glyph cannot always be settled by spelling.</li>
<li>Filled triangles (T, P, U, Y, Z) differ mainly by orientation and shape, and I do not separate T from P reliably; context decides. “DEEPLY” (line 21) is my reading of an unclear word.</li>
<li>Low-confidence lines are guesses at word level. “SORKIN”, “WINGDING”, “WEST” and “MOUNTAINS” are what the glyphs appear to spell, not words I can vouch for.</li>
<li>I searched the web for several phrases and found no source text to check against.</li>
</ul>

<h2>4. Key</h2>
<table><tr><th>letter</th><th>glyph</th><th>remarks</th></tr>{krows}</table>
<p>The layout looks systematic: A–F double-line arrows alternating right/left, G–I thin arrows, K–M diagonals, N–O double-headed arrows, P–W triangles (filled and hollow in four directions), X–Z right-angled triangles. Direction, line style and fill act as modifiers that expand a few base shapes into a full alphabet.</p>

<h2>5. Line by line</h2>
<p>For each line: the straightened strip from the image, the glyphs as I now read them (Unicode approximations), the reading, and what changed. “Earlier stages” shows my first-pass transcription and the solver output it led to.</p>
{blocks}

<h2>6. How it was found</h2>
<h3>6.1 First pass: transcription and a failed attack</h3>
<p>I segmented the page (connected components at 4× upscale, line tracking, per-line straightening) and transcribed 543 glyphs in 24 classes by eye, with visible gaps as chunk breaks (139 chunks). A substitution solver that scored the text <i>without</i> word breaks (5-gram model) found ▲↑⇒ = THE but only 7% of its output fell into common words, against 54% for a clean English substitution of the same size. One class, the double-line right arrow ⇒, made up 22% of all glyphs — too many for any single English letter. At that stage I reported the cipher as not deciphered.</p>
<details class="big"><summary>First-pass glyph classes (24 classes; several are now known to merge or confuse letters)</summary>
<table><tr><th>glyph</th><th>code</th><th>description</th><th>count</th><th>share</th></tr>{grows}</table>
<p>Machine-readable first-pass transcription: <a href="transcript.json">transcript.json</a>, <a href="transcript.txt">transcript.txt</a>, <a href="transcript_unicode.txt">transcript_unicode.txt</a>. It contains the misreads listed in section 5; <a href="reading.json">reading.json</a> has the corrected glyphs.</p></details>

<h3>6.2 Word-aware scoring</h3>
<p>The chunk lengths follow English word lengths (1–2–3–4 glyphs = 6%, 20%, 22%, 20% of chunks), so I treated gaps as word breaks and scored with a word-aware character 4-gram model (spaces included, ~85,000 words of English, interpolated smoothing). With that change alone a plain glyph→letter substitution scores about 270 log-units above shuffled controls (26σ) and words such as MOCK, TRIAL, WOULD, THROUGH appear. A planted substitution of the same size is recovered 100% by this solver.</p>

<h3>6.3 Arrows as movements in a substitution grid — ruled out</h3>
<p>Model: each word starts at a home cell, every glyph moves a cursor, and the cell reached is the letter.</p>
<ul>
<li><b>Shape-derived moves, grid layout solved for (576 hypotheses):</b> direction from the glyph, step length 1 or 2 per glyph style (double-line / thin / foot / filled / hollow), ↔↕ = stay, mirror or two cells; grids 5×5 (torus and clamped), 6×4, 4×6 clamped, 3×8, 2×13. The 8 best raw scores and the best of each grid, each against 8 shuffled streams through the same walk (gap = real minus control mean, log-units):
<table><tr><th>hypothesis</th><th>cells used</th><th>real</th><th>control mean</th><th>gap</th></tr>{walkrows}</table>
The best gap is 86 (3.7σ before correcting for 576 tries) against ~270 for one letter per glyph. The models with the highest raw scores use only 9–14 cells and win by producing low-variety text.</li>
<li><b>Free displacements on a fixed standard layout</b> (Polybius 5×5 without J or without Q, 2×13 alphabet, 26-ring forward and reversed, QWERTY-like 3×9): unrestricted, the optimum is degenerate (“AAAAAAA AHHH”); with zero displacement forbidden the output is repetitive junk (“HAHAHO”, “PETIXIXM”), gaps 12–85.</li>
<li>Caveat: a planted grid-walk cipher is recovered ~86% when the layout is known and not at all when steps and layout are both free, so the fully free variant is only weakly tested.</li>
</ul>

<h3>6.4 Modifiers expanding a smaller alphabet — supported</h3>
<p>Model: a glyph class is a base shape, and each occurrence carries a modifier I did not transcribe that selects one of k letters. The solver picks a hidden sub-class for every occurrence of a chosen class, together with the letter table.</p>
<table><tr><th>model</th><th>score</th><th>shuffled controls</th><th>gap</th><th>dictionary letters, real</th><th>…controls</th></tr>{evrows}</table>
<ul>
<li><b>⇒ = three letters (A, E, C):</b> the gap grows by 69 beyond what controls gain from the extra freedom, dictionary coverage rises from 15% to 23%, and a fourth sub-class adds nothing. TEACHERS is ▲⇒⇒⇒↑⇒△▽, so its three ⇒ must be E, A, C.</li>
<li><b>▲ = two letters (T, Y):</b> gain 52 against 18 in controls; “TOU” (▲↕▶, five times) becomes YOU.</li>
<li><b>⇐ split in two:</b> no better than controls in this test. The close reading later showed why: ⇐ is B and D, and many of my “⇐” were the double-headed N.</li>
</ul>
<p>The solver output at this stage is in <a href="solver_decode.txt">solver_decode.txt</a> / <a href="solver_decode.json">solver_decode.json</a> (about a third of its letters were wrong). Montages of 92 wide arrow glyphs, made while looking for the visible difference between the ⇒ variants: <a href="img/arrows_montage_a.png">a</a>, <a href="img/arrows_montage_b.png">b</a>.</p>

<h3>6.5 Close reading</h3>
<p>With readable fragments in hand I re-read every line against the image. Most remaining errors were mine, not the cipher’s: ↔ read as ⇐ (which gave “OD” for ON), ↓ read as ↘, wrong triangle orientations, word gaps placed inside WORKING / WRONG / INSIGHT, and two punctuation marks (comma ↧, full stop long ↘) read as letters. The result is section 1.</p>

<h2>7. Still open</h2>
<ul>
<li>Lines 17–20: the repeated word ▽⇒↓⇐↴↓, the glyphs ↴ ↱ ⊔, and most of line 18.</li>
<li>Lines 24–26: the words after “TO THE” and the last line.</li>
<li>The visible difference between A, C and E (and between B and D).</li>
<li>A sharper scan would settle most of these; so would the original poster’s key or the thread text.</li>
</ul>

<h2>8. Files</h2>
<ul>
<li><a href="reading.txt">reading.txt</a>, <a href="reading.json">reading.json</a> — current reading per line with corrected glyphs and notes.</li>
<li><a href="transcript.json">transcript.json</a>, <a href="transcript.txt">transcript.txt</a>, <a href="transcript_unicode.txt">transcript_unicode.txt</a> — first-pass transcription (codes and Unicode), kept as the solver input.</li>
<li><a href="solver_decode.txt">solver_decode.txt</a>, <a href="solver_decode.json">solver_decode.json</a> — solver output with inferred sub-classes.</li>
<li><code>img/</code> — straightened line strips and arrow montages; <code>original.png</code> — the source image.</li>
<li><code>work/</code> — first-pass scripts (segmentation, line tracking, spaceless solver; <code>build_report.py</code> there built the first version of this page and is no longer used).</li>
<li><code>work2/</code> — <code>make_lm2.py</code> (word-aware 4-gram model), <code>wsolve.c</code> and <code>wsplit.c</code> (solvers), <code>enum_walk.py</code>, <code>null_walk.py</code>, <code>free_walk.py</code> (movement tests), <code>scan2.py</code>, <code>evidence.py</code>, <code>run4.py</code>, <code>final_decode.py</code> (modifier tests and solver decode), <code>synth.py</code>, <code>synth2.py</code> (planted-cipher checks), <code>reading_data.py</code> + <code>build_index.py</code> (this page). The language-model file and binaries are not kept: run <code>make_lm2.py</code> and <code>cc -O3 -o wsplit wsplit.c -lm</code> inside <code>work2/</code>.</li>
<li>Credit: cipher image and puzzle by u/Tinman886 on r/ciphers (<a href="{THREAD}">thread</a>).</li></ul>
</body></html>'''
open('index.html','w').write(page); print(len(page))
