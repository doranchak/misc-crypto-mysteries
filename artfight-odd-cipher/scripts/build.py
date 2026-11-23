"""Build ../index.html from data/*.json + the pasted texts. Run from the scripts/ dir with python3.11."""
import json, html, re, sys
sys.path.insert(0,'.')
import os
from PIL import Image
import rules_view
RCSS,RHTML,RJS,RM,RROWS=rules_view.section_html()
PROFILE_URL="https://artfight.net/~redacted_entity"

def thumb(src,dst,width):
    im=Image.open(src).convert("RGB")
    if im.width>width: im=im.resize((width,round(im.height*width/im.width)),Image.LANCZOS)
    im.save(dst,optimize=True)
thumb("../images/profile-original.png","../images/profile-thumb.png",300)
thumb("../images/rules-original.png","../images/rules-thumb.png",400)
HAVE_HL=os.path.exists("../images/profile-highlighted.png")
if HAVE_HL: thumb("../images/profile-highlighted.png","../images/profile-highlighted-thumb.png",300)
else: print("NOTE: images/profile-highlighted.png not found - Figure 2 omitted")
F=rules_view.fig
figs=[F("images/profile-original.png","images/profile-thumb.png",
        "<b>Figure 1.</b> The profile as it looks on the site (click to enlarge). The three transcribed lines are the black bars: <span class=\"mono\">ERROR:</span> before the first, a red “-” after it, a red “. . .” at the end of the second and after the third, and a lone red “[&nbsp;]” at lower left. The avatar is also a glitched, partly blacked-out image.",
        "Screenshot of the ArtFight profile redacted_entity: three black bars after a red ERROR label","w1")]
if HAVE_HL:
    figs.append(F("images/profile-highlighted.png","images/profile-highlighted-thumb.png",
        "<b>Figure 2.</b> The same lines with the text selected (click to enlarge): the black-on-black text is revealed. It reads <span class=\"mono\">ERROR: UFDAILD TOSER ATAAE&nbsp;&nbsp;LOD -</span>, <span class=\"mono\">YERSSTEMTO BTING CKSUBVP ASU . . .</span>, <span class=\"mono\">cesriPosng . . .</span> — the same letters in the same order as the transcription; only the double space in line 1 is new.",
        "Screenshot of the profile with the hidden text revealed by selecting it","w1"))
figs.append(F("images/rules-original.png","images/rules-thumb.png",
        "<b>Figure 3.</b> The “Character Permissions” rules text as it originally appeared on the Characters tab (click to enlarge). Note the purple, large red / blue and small red <i>error</i> fragments; their colours matter, see the rules section below.",
        "Screenshot of the Characters tab with the garbled rules text","w2"))
FIGS='<div class="figrow">'+"".join(figs)+'</div>'

from collections import Counter
tiling=json.load(open('../data/tiling.json'))
stats=json.load(open('../data/chunk_stats.json'))
orders=json.load(open('../data/orders.json'))
rk=json.load(open('../data/rank_by_chunks.json'))
sc=json.load(open('../data/space_chars.json'))
SC1,SC2,SCR=sc['line1'],sc['line2'],sc['line2_orders']
SC_MINE=[r for r in SCR if r['order']=="SUBVERTING SYSTEM BACKUPS TO"][0]
SC_HMIN,SC_HMAX=min(r['hits'] for r in SCR),max(r['hits'] for r in SCR)
SC_KMIN,SC_KMAX=min(r['K'] for r in SCR),max(r['K'] for r in SCR)
SC_BEST=[r['order'].capitalize() for r in SCR if r['K']==SC_KMIN]
LINES=[("line1","UFDAILD TOSER ATAAE LOD","FAILED TO LOAD USER DATA","exact"),
       ("line2","YERSSTEMTO BTING CKSUBVP ASU","SUBVERTING SYSTEM BACKUPS TO","partial"),
       ("line3","cesriPosng","Processing","exact")]
RULES=open('../rules/corrupted.txt').read().strip()
n_error=len(re.findall(r'error',RULES,flags=re.I))
n_lines=len(RULES.splitlines())

def tiles_html(name,cipher,plain):
    t=tiling[name]['tiles']
    cs=cipher.replace(" ","")
    ps=plain.replace(" ","")
    ccol={};pcol={}
    for i,(pos,s,L) in enumerate(t):
        for j in range(L): ccol[pos+j]=i; pcol[s+j]=i
    def render(text,col):
        out=[];k=0
        for ch in text:
            if ch==" ": out.append('<span class="sp"></span>'); continue
            out.append(f'<span class="t" style="--h:{(col[k]*47)%360}">{html.escape(ch)}</span>'); k+=1
        return "".join(out)
    return (f'<div class="row"><span class="lab">cipher</span><span class="seq">{render(cipher,ccol)}</span></div>'
            f'<div class="row"><span class="lab">plain</span><span class="seq">{render(plain,pcol)}</span></div>')

def inventory(cipher,plain):
    a=Counter(cipher.replace(" ","").upper()); b=Counter(plain.replace(" ","").upper())
    keys=sorted(set(a)|set(b))
    cells="".join(f'<td>{k}</td>' for k in keys)
    ra="".join(f'<td>{a[k]}</td>' for k in keys); rb="".join(f'<td>{b[k]}</td>' for k in keys)
    ok = a==b
    return (f'<table class="inv"><tr><th>letter</th>{cells}</tr><tr><th>in cipher</th>{ra}</tr><tr><th>in plaintext</th>{rb}</tr></table>'
            f'<p class="{"ok" if ok else "no"}">{"Identical letter counts: same letters, different order." if ok else "MISMATCH"} ({sum(a.values())} letters)</p>')

top_orders="".join(f'<tr><td class="mono">{html.escape(s)}</td><td>{h}</td></tr>' for h,s in orders[:6])
mine=[h for h,s in orders if s=="SUBVERTING SYSTEM BACKUPS TO"][0]
lo=min(h for h,_ in orders); hi=max(h for h,_ in orders)

sections=[]
for name,c,p,kind in LINES:
    st=stats[name]; K=tiling[name]['K']; n=st['n']
    sections.append(f'''
<div class="card">
<h3>{html.escape(c)} → {html.escape(p)}</h3>
{tiles_html(name,c,p)}
<p class="small">{n} letters; one minimum tiling needs <b>{K} chunks</b> (average {n/K:.1f} letters per chunk). Adjacent letter pairs of the plaintext that are still adjacent, in order, somewhere in the cipher: <b>{st['bigram_hits']}</b>; a uniformly random reshuffle of the same letters averages <b>{st['random_mean']}</b>
({'p&nbsp;&lt;&nbsp;0.0001' if st['p_ge']==0 else 'p&nbsp;=&nbsp;'+format(st['p_ge'],'.3f')} over 20,000 shuffles).</p>
</div>''')

HTML=f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Odd cipher on an ArtFight profile — scrambled "error log" text</title>
<style>
:root {{ color-scheme: light dark; --bg:#f9f9f7; --ink:#0b0b0b; --ink2:#52514e; --line:#dcdbd3; --card:#fcfcfb; --bad:#b3362f; --good:#1f7a3d; --warn:#8a5a00; --l:84%; --tc:#111; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#0d0d0d; --ink:#f0efec; --ink2:#b9b8b0; --line:#2c2c2a; --card:#1a1a19; --bad:#e66767; --good:#5cc885; --warn:#e0b24a; --l:30%; --tc:#f4f4f2; }} }}
body {{ margin:0; background:var(--bg); color:var(--ink); font:16px/1.55 system-ui,-apple-system,sans-serif; }}
main {{ max-width:880px; margin:0 auto; padding:28px 20px 70px; }}
h1 {{ font-size:1.55rem; margin:0 0 4px; }} h2 {{ font-size:1.15rem; margin:34px 0 8px; border-bottom:1px solid var(--line); padding-bottom:4px; }} h3 {{ font-size:1rem; margin:0 0 8px; font-family:ui-monospace,Menlo,monospace; }}
p.sub {{ color:var(--ink2); margin:0 0 14px; }} .small {{ font-size:.9rem; color:var(--ink2); }}
a {{ color:inherit; }}
code,.mono {{ font-family:ui-monospace,Menlo,monospace; }}
.card {{ background:var(--card); border:1px solid var(--line); border-radius:8px; padding:12px 16px; margin:12px 0; }}
.answer {{ font:600 1.05rem/1.9 ui-monospace,Menlo,monospace; }}
.answer .c {{ color:var(--ink2); }} .answer .p {{ letter-spacing:.03em; }}
.tag {{ font:600 .72rem system-ui; padding:1px 7px; border-radius:99px; border:1px solid currentColor; margin-left:8px; vertical-align:middle; }}
.ok {{ color:var(--good); font-weight:600; }} .no {{ color:var(--bad); font-weight:600; }} .meh {{ color:var(--warn); font-weight:600; }}
table {{ border-collapse:collapse; font-size:.9rem; }} th,td {{ text-align:left; padding:4px 8px; border-bottom:1px solid var(--line); vertical-align:top; }} th {{ color:var(--ink2); font-weight:600; }}
table.inv td,table.inv th {{ text-align:center; padding:3px 6px; font-family:ui-monospace,Menlo,monospace; }} table.inv th:first-child {{ text-align:left; }}
.row {{ display:flex; align-items:center; gap:10px; margin:5px 0; }} .lab {{ width:48px; color:var(--ink2); font-size:.8rem; flex:none; }}
.seq {{ font:600 1.15rem ui-monospace,Menlo,monospace; display:flex; flex-wrap:wrap; }}
.t {{ background:hsl(var(--h) 62% var(--l)); color:var(--tc); padding:1px 2px; margin:0 1px 0 0; border-radius:3px; min-width:.9ch; text-align:center; }}
.sp {{ display:inline-block; width:1.1ch; }}
pre.rules {{ background:var(--card); border:1px solid var(--line); border-radius:8px; padding:10px 14px; white-space:pre-wrap; word-break:break-word; font:13px/1.5 ui-monospace,Menlo,monospace; }}

{RCSS}
</style>
</head>
<body>
<main>
<h1>Odd cipher found on an ArtFight profile</h1>
<p class="sub">Source: Reddit <a href="https://www.reddit.com/r/ciphers/comments/1y30jen/odd_cipher_found_on_artfight_profile/">r/ciphers — “Odd cipher found on artfight profile”</a>, posted by <b>u/fuckinhballin</b>.<br>
Original profile: <a href="{PROFILE_URL}">{PROFILE_URL}</a> (ArtFight user <i>redacted_entity</i>).<br>
The ciphertext and the rules text below are the poster's own transcription; the screenshots in the next section show how the profile looks on the site. I could not open either page myself (Reddit returned HTTP 403 to my fetch; ArtFight is behind a Cloudflare challenge, which I did not try to get around), so I have not read any replies, and the screenshots below are my only direct view of the live profile.</p>

<h2>The profile as it appears on the site</h2>
{FIGS}
<p class="small">The three lines in the answer below are the text inside the black bars (black on black, so invisible until selected — Figure 2). On the page they read, in order: <span class="mono">ERROR: ▮▮▮ -</span>, <span class="mono">▮▮▮ . . .</span>, <span class="mono">▮▮▮ . . .</span>, then <span class="mono">[ ]</span> — it reads like a failed-load log: an error, a status line, a “Processing …” line, and an empty list.</p>

<h2>Answer</h2>
<div class="card answer">
<div><span class="c">UFDAILD TOSER ATAAE LOD</span><br>&nbsp;&nbsp;→ <span class="p">FAILED TO LOAD USER DATA</span> <span class="tag ok">exact anagram</span></div>
<div style="margin-top:8px"><span class="c">YERSSTEMTO BTING CKSUBVP ASU</span><br>&nbsp;&nbsp;→ <span class="p">SUBVERTING SYSTEM BACKUPS TO</span> <span class="tag meh">SUBVERTING firm; rest likely; order open</span></div>
<div style="margin-top:8px"><span class="c">cesriPosng</span><br>&nbsp;&nbsp;→ <span class="p">Processing</span> <span class="tag ok">exact anagram</span></div>
</div>
<p><b>It is not a substitution cipher, so no Caesar shift could ever have worked.</b> Each line is the letters of an ordinary English phrase <i>rearranged</i> — the letters themselves are untouched, including the capital “P” in <i>Processing</i>. The three lines read like a computer error/status log (“FAILED TO LOAD USER DATA … Processing”), which fits the profile's glitchy “error” theme: the rules text is full of the word “error” and is itself visibly corrupted (I restore as much of it as I can in the rules section below, using its colour coding as a key). This is most likely a deliberate <i>glitch-text</i> effect rather than a secret meant to resist solving.</p>
<p><b>Confidence.</b> Lines 1 and 3: very high — every one of the 20 and 10 letters is used exactly once, with nothing left over. Line 2: <i>SUBVERTING</i> is well supported (see below); the remaining 15 letters fit <i>SYSTEM BACKUPS TO</i> exactly, but the data do not fix the word order or <i>BACKUPS</i>/<i>SYSTEMS</i> plurals, and the trailing “. . .” (visible in Figure 1) suggests the line continues or is a status message. Treat line 2 as a good reading, not a certainty.</p>

<h2>Why shifts fail, and how this was spotted</h2>
<p>A Caesar shift replaces every letter with a different one, so a shifted text has different letters from its plaintext. Here the multiset of letters in each line is <b>identical</b> to a plausible plaintext (counts below), so the cipher type is a pure <b>transposition / anagram</b>. The OP tried 25 shifts, forward and reversed — a reversed string is still the same letters in a new order, but reading backwards doesn’t restore these lines, so the shuffle isn’t a simple reversal.</p>
<p>How I found them: <code>cesriPosng</code> has the same ten letters as “Processing” (and keeps “ces” and “ng” intact). Line 1 contains fragments <code>AIL</code>, <code>TO</code>, <code>SER</code>, <code>ATA</code>, <code>LO</code> that suggest <i>FAILED TO LOAD USER DATA</i>; the letter count then matched exactly. Line 2 holds <code>SUBV</code>, <code>ER</code>, <code>TING</code>, <code>STEM</code>, <code>CK</code>.</p>
{"".join(f'<div class="card"><h3>{html.escape(c)}</h3>{inventory(c,p)}</div>' for _,c,p,_ in LINES)}

<h2>How the scramble behaves</h2>
<p>It is not a uniform random permutation: short pieces of the plaintext survive intact (<code>AIL</code>, <code>SER</code>, <code>ATA</code>, <code>TING</code>, <code>SUBV</code>, <code>STEM</code>, <code>CES</code>, <code>NG</code> …). The pictures colour the plaintext cut into the fewest pieces that can be re-ordered to give the cipher (a “minimum common string partition”, found by exhaustive search; ties are possible so this is <i>one</i> minimum tiling). The tilings were computed on the letters only; the spaces are discussed separately below. A piece can straddle a word boundary (<code>DTO</code> in line 1 — see “Spaces”).</p>
{"".join(sections)}
<p class="small">What this supports: the cipher text looks like “cut the text into small pieces (mostly 1–3 letters, occasionally 4), shuffle the pieces (spaces included, see below)”, or an equivalent glitch effect. The line-2 figures are optimistic, because I chose that plaintext after searching many splits; lines 1 and 3 were fixed by the exact anagram first. It does not identify the exact generator, so it cannot by itself fix the word order in line 2. Line 3 is too short to be significant by itself (p ≈ 0.1); its solution rests on the exact 10-letter anagram.</p>

<h3 style="font-family:system-ui;margin-top:20px">Spaces</h3>
<p>Selecting the text (Figure 2) shows something the transcription lost: line 1 has a <b>double space</b> between <code>ATAAE</code> and <code>LOD</code> (that gap is 12&nbsp;px wide in the screenshot, against 7&nbsp;px for the other word gaps). With it, the space counts match the plaintexts exactly: line 1 has {SC1['n_spaces']} spaces (as does <i>FAILED TO LOAD USER DATA</i>), line 2 has {SC2['n_spaces']} (as does <i>SUBVERTING SYSTEM BACKUPS TO</i>), line 3 has none. The simplest reading is that the word spaces are ordinary characters that get shuffled along with the letters — so two can land side by side, and the cipher's word lengths (7·5·5·3 in line 1) differ from the plaintext's (6·2·4·4·4) — rather than being laid down afterwards, which is what I assumed in the first version of this page. I did not test how likely matching space counts would be by chance.</p>
<p>What the pair statistics say, counting the space as a character: neighbouring pairs of the plaintext that are still neighbours, in order, in the cipher — line 1: <b>{SC1['hits']} of {SC1['pairs']}</b> against {SC1['rand_mean']} expected for a random permutation (p = {SC1['p']:.4f}); line 2: <b>{SC2['hits']} of {SC2['pairs']}</b> against {SC2['rand_mean']} (p &lt; 0.0001). Pairs that include a space, taken alone, are preserved only about as often as chance (line 1: {SC1['space_hits']} of {SC1['space_pairs']} against {SC1['space_rand_mean']}, p ≈ {SC1['space_p']:.2f}; line 2: {SC2['space_hits']} of {SC2['space_pairs']} against {SC2['space_rand_mean']}, p ≈ {SC2['space_p']:.2f}). So the spaces move, but I cannot show that they move <i>stuck to</i> their neighbours. A few pieces with a space in them do survive intact — <code>D TO</code>, <code>SER␣</code> and <code>␣LO</code> in line 1 (<i>FAILE<b>D TO</b> LOAD</i> ↔ <i>UFDAIL<b>D TO</b>SER</i>), <code>TING␣</code> in line 2 — but that is about what the near-chance pair count allows. Counting the spaces as characters costs only one extra piece in the fewest-pieces tilings: {SC1['K']} for line 1 (11 without), {SC2['K']} for line 2 (13 without), {sc['line3']['K']} for line 3 (no spaces).</p>

<h2>Line 2 in more detail</h2>
<ul>
<li><b>SUBVERTING.</b> The contiguous strings <code>SUBV</code> (in <code>CK<b>SUBV</b>P</code>), <code>ER</code> and <code>TING</code> are exactly what <i>SUBVERTING</i> needs. I enumerated all {rk['n']} splits of the 25 letters into at most four dictionary words (a ~3,900-word Oxford-derived list) and scored each by how many neighbouring letter pairs of the split also appear, in order, in the cipher (median {rk['median']:.0f}, best {rk['max']}). Only {rk['all_sub']} of the {rk['n']} splits contain <i>subverting</i>, yet <b>all {rk['top_within1']}</b> of the top-scoring ones (within one pair of the best) do. The other words in those splits are noise (“bypass mute stock subverting”), which is why the rest of the line has to be judged separately. Each split was scored in the alphabetical order its words were listed, so cross-word pairs are incidental.</li>
<li><b>The remaining 15 letters</b> (A B C E K M O P S S S T T U Y) split into 55,267 word combinations of 2–4 words from the 30,000 most frequent words in a web word-frequency list. The two highest-scoring by word frequency are <code>backup systems to</code> and <code>backups system to</code> — the same words as my reading — followed by weaker, less natural ones such as <code>back systems to up</code>. That is a fit to common phrasing, not independent proof.</li>
<li><b>Word order is undetermined.</b> Scoring all 24 orderings of SUBVERTING / SYSTEM / BACKUPS / TO by how many neighbouring-letter pairs the cipher preserves gives {lo}–{hi} pairs for every ordering, with no meaningful separation (my reading scores {mine}). Cipher <code>…STEMTO…</code> mildly hints at “SYSTEM TO” being adjacent, but this is weak evidence. “Subverting system backups to …” is just the order I find most natural. <b>Spaces as characters (new):</b> the orders still do not separate. Across the 24 orders, {SC_HMIN}–{SC_HMAX} neighbouring pairs are kept and {SC_KMIN}–{SC_KMAX} pieces are needed; my reading keeps {SC_MINE['hits']} and needs {SC_MINE['K']}, in the middle of both ranges. The orders needing the fewest pieces ({SC_KMIN}) are {', '.join('<i>'+b.lower()+'</i>' for b in SC_BEST)} — a one-piece difference that singles out nothing.</li>
</ul>
<table><tr><th>Top orderings by neighbour-pair preservation</th><th>pairs kept</th></tr>{top_orders}</table>

{RHTML}

<h2>Caveats</h2>
<ul>
<li>The text comes from the poster's transcription, which I checked by eye against Figure 2: all three lines match letter for letter (only the double space in line 1 was lost). Lines 1 and 3 reproducing perfect anagrams also supports their transcription; line 2 has no such check, because any 25 letters can be re-split into some words, so for line 2 the screenshot is the only check, and it rests on my reading of a small image.</li>
<li>The screenshot shows <span class="mono">ERROR:</span> before line 1, a “-” after it, “. . .” after lines 2 and 3, and a lone “[ ]” at lower left. These are plain red text outside the anagrams (there is nothing in them to rearrange), so they are not part of my reading. The screenshot ends just below the “[ ]”, so I cannot say whether anything follows it.</li>
<li>The rules restoration is partial and interpretive (see its own confidence notes); about a quarter of its letters sit in fragments I could not read. Only the colour-matched words (“Additional notes:”, “Don't”, “Aye”) have an independent check, and “Aye” is the weakest (three letters, position unknown).</li>
<li>Selecting the text (Figure 2) shows no extra hidden text in the three bars beyond what was transcribed. I can’t rule out text elsewhere on the page, outside the screenshots.</li>
</ul>

<h2>Files</h2>
<p class="small">Scripts in <code>scripts/</code> (Python 3.11): <code>anagram_fast.py</code> (bit-packed anagram finder), <code>tiling.py</code> (minimum chunk tiling), <code>chunk_stats.py</code> (neighbour-pair statistic vs. random shuffles), <code>rank_by_chunks.py</code>, <code>rank2b.py</code> (frequency-ranked splits), <code>remainder.py</code>, <code>orders.py</code>, and <code>lettercmp.py</code> + <code>resid.py</code> (per-paragraph letter-balance checks for the rules text), <code>space_chars.py</code> (spaces counted as characters: pair statistics, fewest-pieces tilings, the 24 line-2 orders; writes <code>data/space_chars.json</code>), <code>style_analysis.py</code> (hue-clusters the rules screenshot, aligns the styled pieces with the text, tests whether same-style pieces reunite, 100,000-draw null model; writes <code>data/style_analysis.json</code> and the crops in <code>images/crops/</code>), <code>build.py</code> + <code>rules_view.py</code> (this page); <code>rules/corrupted.txt</code>, <code>rules/styles.py</code> (the style of every coloured piece) and <code>rules/restoration.py</code> hold the garbled text, its styles, and my segment-by-segment restoration with the fragments each phrase came from. Screenshots in <code>images/</code>. Outputs in <code>data/</code>. Word lists used: an Oxford-derived list and a web word-frequency list from other projects on this machine.</p>
</main>
<script>{RJS}</script>
</body>
</html>
'''
open('../index.html','w').write(HTML)
print("wrote ../index.html",len(HTML),"bytes; error count",n_error,"lines",n_lines)
