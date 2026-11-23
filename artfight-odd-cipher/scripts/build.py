"""Build ../index.html from data/*.json + the pasted texts. Run from the scripts/ dir with python3.11."""
import json, html, re, sys
sys.path.insert(0,'.')
import rules_view
RCSS,RHTML,RJS,RM,RROWS=rules_view.section_html()
from collections import Counter
tiling=json.load(open('../data/tiling.json'))
stats=json.load(open('../data/chunk_stats.json'))
orders=json.load(open('../data/orders.json'))
rk=json.load(open('../data/rank_by_chunks.json'))
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
<p class="sub">Source: Reddit <a href="https://www.reddit.com/r/ciphers/comments/1y30jen/odd_cipher_found_on_artfight_profile/">r/ciphers — “Odd cipher found on artfight profile”</a>, posted by <b>u/fuckinhballin</b>. The ciphertext and the rules paragraph below are the poster's own transcription. I could not open the thread itself (Reddit returned HTTP 403 to my fetch), so I have not read any replies, and I have not seen the profile image.</p>

<h2>Answer</h2>
<div class="card answer">
<div><span class="c">UFDAILD TOSER ATAAE LOD</span><br>&nbsp;&nbsp;→ <span class="p">FAILED TO LOAD USER DATA</span> <span class="tag ok">exact anagram</span></div>
<div style="margin-top:8px"><span class="c">YERSSTEMTO BTING CKSUBVP ASU</span><br>&nbsp;&nbsp;→ <span class="p">SUBVERTING SYSTEM BACKUPS TO</span> <span class="tag meh">SUBVERTING firm; rest likely; order open</span></div>
<div style="margin-top:8px"><span class="c">cesriPosng</span><br>&nbsp;&nbsp;→ <span class="p">Processing</span> <span class="tag ok">exact anagram</span></div>
</div>
<p><b>It is not a substitution cipher, so no Caesar shift could ever have worked.</b> Each line is the letters of an ordinary English phrase <i>rearranged</i> — the letters themselves are untouched, including the capital “P” in <i>Processing</i>. The three lines read like a computer error/status log (“FAILED TO LOAD USER DATA … Processing”), which fits the profile's glitchy “error” theme: the rules paragraph is full of the word “error” and is itself visibly corrupted (I restore as much of it as I can in the before/after view below). This is most likely a deliberate <i>glitch-text</i> effect rather than a secret meant to resist solving.</p>
<p><b>Confidence.</b> Lines 1 and 3: very high — every one of the 20 and 10 letters is used exactly once, with nothing left over. Line 2: <i>SUBVERTING</i> is well supported (see below); the remaining 15 letters fit <i>SYSTEM BACKUPS TO</i> exactly, but the data do not fix the word order or <i>BACKUPS</i>/<i>SYSTEMS</i> plurals, and the trailing “. . .” suggests the original line continues. Treat line 2 as a good reading, not a certainty.</p>

<h2>Why shifts fail, and how this was spotted</h2>
<p>A Caesar shift replaces every letter with a different one, so a shifted text has different letters from its plaintext. Here the multiset of letters in each line is <b>identical</b> to a plausible plaintext (counts below), so the cipher type is a pure <b>transposition / anagram</b>. The OP tried 25 shifts, forward and reversed — a reversed string is still the same letters in a new order, but reading backwards doesn’t restore these lines, so the shuffle isn’t a simple reversal.</p>
<p>How I found them: <code>cesriPosng</code> has the same ten letters as “Processing” (and keeps “ces” and “ng” intact). Line 1 contains fragments <code>AIL</code>, <code>TO</code>, <code>SER</code>, <code>ATA</code>, <code>LO</code> that suggest <i>FAILED TO LOAD USER DATA</i>; the letter count then matched exactly. Line 2 holds <code>SUBV</code>, <code>ER</code>, <code>TING</code>, <code>STEM</code>, <code>CK</code>.</p>
{"".join(f'<div class="card"><h3>{html.escape(c)}</h3>{inventory(c,p)}</div>' for _,c,p,_ in LINES)}

<h2>How the scramble behaves</h2>
<p>It is not a uniform random permutation: short pieces of the plaintext survive intact (<code>AIL</code>, <code>SER</code>, <code>ATA</code>, <code>TING</code>, <code>SUBV</code>, <code>STEM</code>, <code>CES</code>, <code>NG</code> …). The pictures colour the plaintext cut into the fewest pieces that can be re-ordered to give the cipher (a “minimum common string partition”, found by exhaustive search; ties are possible so this is <i>one</i> minimum tiling). The word spaces were laid down separately — the cipher's word lengths (7·5·5·3) do not match the plaintext's (6·2·4·4·4), and a piece can straddle a word boundary (<code>DTO</code> in line 1).</p>
{"".join(sections)}
<p class="small">What this supports: the cipher text looks like “cut the text into small pieces (mostly 1–3 letters, occasionally 4), shuffle the pieces, re-insert spaces”, or an equivalent glitch effect. The line-2 figures are optimistic, because I chose that plaintext after searching many splits; lines 1 and 3 were fixed by the exact anagram first. It does not identify the exact generator, so it cannot by itself fix the word order in line 2. Line 3 is too short to be significant by itself (p ≈ 0.1); its solution rests on the exact 10-letter anagram.</p>

<h2>Line 2 in more detail</h2>
<ul>
<li><b>SUBVERTING.</b> The contiguous strings <code>SUBV</code> (in <code>CK<b>SUBV</b>P</code>), <code>ER</code> and <code>TING</code> are exactly what <i>SUBVERTING</i> needs. I enumerated all {rk['n']} splits of the 25 letters into at most four dictionary words (a ~3,900-word Oxford-derived list) and scored each by how many neighbouring letter pairs of the split also appear, in order, in the cipher (median {rk['median']:.0f}, best {rk['max']}). Only {rk['all_sub']} of the {rk['n']} splits contain <i>subverting</i>, yet <b>all {rk['top_within1']}</b> of the top-scoring ones (within one pair of the best) do. The other words in those splits are noise (“bypass mute stock subverting”), which is why the rest of the line has to be judged separately. Each split was scored in the alphabetical order its words were listed, so cross-word pairs are incidental.</li>
<li><b>The remaining 15 letters</b> (A B C E K M O P S S S T T U Y) split into 55,267 word combinations of 2–4 words from the 30,000 most frequent words in a web word-frequency list. The two highest-scoring by word frequency are <code>backup systems to</code> and <code>backups system to</code> — the same words as my reading — followed by weaker, less natural ones such as <code>back systems to up</code>. That is a fit to common phrasing, not independent proof.</li>
<li><b>Word order is undetermined.</b> Scoring all 24 orderings of SUBVERTING / SYSTEM / BACKUPS / TO by how many neighbouring-letter pairs the cipher preserves gives {lo}–{hi} pairs for every ordering, with no meaningful separation (my reading scores {mine}). Cipher <code>…STEMTO…</code> mildly hints at “SYSTEM TO” being adjacent, but this is weak evidence. “Subverting system backups to …” is just the order I find most natural.</li>
</ul>
<table><tr><th>Top orderings by neighbour-pair preservation</th><th>pairs kept</th></tr>{top_orders}</table>

{RHTML}

<h2>Caveats</h2>
<ul>
<li>Everything is from the poster's transcription. Lines 1 and 3 reproducing perfect anagrams strongly suggests the transcription of those two is accurate; line 2 has no such check, because any 25 letters can be re-split into some words, so a typo there would go unnoticed.</li>
<li>The “-” after line 1 and the “. . .” after line 2 are not part of my reading. If the profile shows more text after them, it may complete the phrase.</li>
<li>The rules restoration is partial and interpretive (see its own confidence notes); about a quarter of its letters sit in fragments I could not read.</li>
<li>I can’t rule out that the profile owner intended a longer hidden message in the blacked-out area; I only decoded what was transcribed.</li>
</ul>

<h2>Files</h2>
<p class="small">Scripts in <code>scripts/</code> (Python 3.11): <code>anagram_fast.py</code> (bit-packed anagram finder), <code>tiling.py</code> (minimum chunk tiling), <code>chunk_stats.py</code> (neighbour-pair statistic vs. random shuffles), <code>rank_by_chunks.py</code>, <code>rank2b.py</code> (frequency-ranked splits), <code>remainder.py</code>, <code>orders.py</code>, and <code>lettercmp.py</code> + <code>resid.py</code> (per-paragraph letter-balance checks for the rules text), <code>build.py</code> + <code>rules_view.py</code> (this page); <code>rules/corrupted.txt</code> and <code>rules/restoration.py</code> hold the garbled text and my segment-by-segment restoration with the fragments each phrase came from. Outputs in <code>data/</code>. Word lists used: an Oxford-derived list and a web word-frequency list from other projects on this machine.</p>
</main>
<script>{RJS}</script>
</body>
</html>
'''
open('../index.html','w').write(HTML)
print("wrote ../index.html",len(HTML),"bytes; error count",n_error,"lines",n_lines)
