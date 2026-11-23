"""Build the colour analysis + before/after view of the glitched rules text from
rules/corrupted.txt + rules/styles.py + rules/restoration.py + data/style_analysis.json."""
import re, sys, html, json
from collections import Counter
sys.path.insert(0, '../rules')
from restoration import PARAS
from styles import STYLES

CORR = open('../rules/corrupted.txt').read().splitlines()
assert len(CORR) == len(PARAS)
SA = json.load(open('../data/style_analysis.json'))
TIER_NAME = {"c": "colour-matched", "k": "recovered", "r": "repaired", "i": "inferred", "g": "gap"}


def fig(href, thumb, caption, alt, cls=""):
    return (f'<figure class="fig {cls}"><a href="{href}" target="_blank" rel="noopener"><img src="{thumb}" alt="{html.escape(alt)}" loading="lazy"></a>'
            f'<figcaption>{caption}</figcaption></figure>')


def locate(par, pattern, claimed):
    """(start,end) of the {braced} core of pattern inside par, choosing an occurrence whose core is not yet claimed."""
    m = re.fullmatch(r'(.*?)\{(.*?)\}(.*)', pattern, flags=re.S)
    assert m, pattern
    pre, core, post = m.groups()
    full = pre + core + post
    start = 0
    while True:
        i = par.find(full, start)
        assert i >= 0, f"pattern not found: {pattern!r}"
        a, b = i + len(pre), i + len(pre) + len(core)
        if not any(claimed[k] for k in range(a, b)):
            return a, b
        start = i + 1


def parse_pattern(pat, default_par):
    m = re.match(r'§(\d+)\|(.*)', pat, flags=re.S)
    return (int(m.group(1)) - 1, m.group(2)) if m else (default_par, pat)


def build():
    NP = len(CORR)
    err = [[False] * len(p) for p in CORR]
    claimed = [[None] * len(p) for p in CORR]
    style = [[None] * len(p) for p in CORR]
    for pi, p in enumerate(CORR):
        for m in re.finditer(r'error', p, flags=re.I):
            for k in range(m.start(), m.end()): err[pi][k] = True
    for pi, pat, st in STYLES:
        a, b = locate(CORR[pi], pat, [None] * len(CORR[pi]))
        for k in range(a, b): style[pi][k] = st

    # ---- claim source fragments for every segment (patterns may point into other paragraphs)
    sup = {t: [0, 0] for t in "ckri"}      # [supported letters, letters in segment text]
    sid_tier, seg_ids, seg_counter = {}, [], 0
    for pi, segs in enumerate(PARAS):
        ids = []
        for tier, text, srcs in segs:
            sid = f"s{seg_counter}"; seg_counter += 1
            ids.append(sid); sid_tier[sid] = tier
            src_letters = Counter()
            for pat in srcs:
                tp, pt = parse_pattern(pat, pi)
                a, b = locate(CORR[tp], pt, claimed[tp])
                for k in range(a, b):
                    assert not err[tp][k], (pi, pat)
                    claimed[tp][k] = sid
                src_letters.update(c.lower() for c in CORR[tp][a:b] if c.isalpha())
            if tier in sup:
                seg_letters = Counter(c.lower() for c in text if c.isalpha())
                sup[tier][0] += sum((seg_letters & src_letters).values())
                sup[tier][1] += sum(seg_letters.values())
        seg_ids.append(ids)

    # ---- render
    left_html, right_html, rows, leftovers = [], [], [], []
    tot_alpha = tot_claimed = tot_decoded = tot_gap = 0
    tier_letters = Counter()
    for pi, (par, segs) in enumerate(zip(CORR, PARAS)):
        n = len(par)
        out = []; k = 0
        key = lambda j: (err[pi][j], style[pi][j], claimed[pi][j])
        while k < n:
            e, st, c = key(k)
            j = k
            while j < n and key(j) == (e, st, c): j += 1
            chunk = html.escape(par[k:j])
            if e: out.append(f'<span class="err">{chunk}</span>')
            else:
                cls = ("src " if c else "") + (f"s{st}" if st else "")
                if cls: out.append(f'<span class="{cls.strip()}"' + (f' data-s="{c}"' if c else '') + f'>{chunk}</span>')
                else: out.append(chunk)
            k = j
        left_html.append("".join(out))
        parts = []; plain = []; prev = ""
        for (tier, text, srcs), sid in zip(segs, seg_ids[pi]):
            glue = " "
            if prev and (prev[-1] in "(/" or text[0] in ",.;:!?)/"): glue = ""
            parts.append(glue + f'<span class="tk {tier}" data-s="{sid}" title="{TIER_NAME[tier]}">{html.escape(text)}</span>')
            plain.append(glue + text); prev = text
        right_html.append("".join(parts).lstrip())
        rows.append(("".join(plain)).strip())
        alpha_idx = [j for j in range(n) if par[j].isalpha() and not err[pi][j]]
        tot_alpha += len(alpha_idx)
        tot_claimed += sum(1 for j in alpha_idx if claimed[pi][j])
        tot_decoded += sum(1 for j in alpha_idx if claimed[pi][j] and sid_tier[claimed[pi][j]] != 'g')
        tot_gap += sum(1 for j in alpha_idx if claimed[pi][j] and sid_tier[claimed[pi][j]] == 'g')
        runs = []; k = 0
        while k < n:
            if claimed[pi][k] is None and not err[pi][k] and not par[k].isspace():
                j = k
                while j < n and claimed[pi][j] is None and not err[pi][j] and not par[j].isspace(): j += 1
                if par[k:j].strip("[](){}.,;:-/!"): runs.append(par[k:j])
                k = j
            else: k += 1
        leftovers.append(runs)
        for tier, text, srcs in segs:
            tier_letters[tier] += sum(1 for c in text if c.isalpha())
    metrics = dict(total_letters=tot_alpha, claimed=tot_claimed, decoded=tot_decoded, gap=tot_gap, unplaced=tot_alpha - tot_claimed,
                   support={t: tuple(v) for t, v in sup.items()}, tier_letters=dict(tier_letters), n_segments=seg_counter)
    return left_html, right_html, rows, leftovers, metrics


if __name__ == "__main__":
    l, r, rows, lo, m = build()
    print(json.dumps(m, indent=1))
    for i, t in enumerate(rows): print(f"P{i+1}:", t, "\n   leftovers:", lo[i], "\n")


# ----------------------------------------------------------------------------------------------------------------
RULES_CSS = """
:root { --purple:#9a3bb4; --red2:#c8352b; --blue:#1d8bbd; }
@media (prefers-color-scheme: dark) { :root { --purple:#c46be0; --red2:#f0584c; --blue:#55b6e0; } }
.legend { display:flex; flex-wrap:wrap; gap:6px 14px; font-size:.85rem; margin:8px 0 14px; }
.legend .tk { padding:1px 8px; }
.ba { display:grid; grid-template-columns:1fr 1fr; gap:0; border:1px solid var(--line); border-radius:8px; overflow:hidden; margin:10px 0; }
.ba > div { padding:9px 13px; border-bottom:1px solid var(--line); }
.ba > div:nth-last-child(-n+2) { border-bottom:0; }
.ba .hd { background:var(--card); font-weight:600; font-size:.85rem; color:var(--ink2); position:sticky; top:0; }
.ba .L { font:12.5px/1.65 ui-monospace,Menlo,monospace; border-right:1px solid var(--line); word-break:break-word; background:color-mix(in srgb,var(--card) 70%,transparent); }
.ba .R { font-size:15.5px; line-height:1.7; }
.ba .pn { display:block; color:var(--ink2); font:600 .7rem system-ui; margin-bottom:2px; letter-spacing:.04em; }
.err { color:var(--bad); font-weight:700; font-size:.82em; background:color-mix(in srgb,var(--bad) 14%,transparent); border-radius:3px; }
.src { background:color-mix(in srgb,var(--warn) 22%,transparent); border-radius:3px; }
.sP { color:var(--purple); font-weight:700; }
.sR { color:var(--red2); font-size:1.55em; line-height:1; font-family:system-ui,sans-serif; }
.sB { color:var(--blue); font-size:1.55em; line-height:1; font-family:system-ui,sans-serif; }
.sw { display:inline-block; min-width:1.2em; text-align:center; }
.tk { border-radius:4px; padding:0 3px; transition:outline-color .1s; outline:2px solid transparent; }
.tk.c { background:color-mix(in srgb,var(--purple) 20%,transparent); box-shadow:inset 0 -2px 0 var(--purple); font-weight:600; }
.tk.k { background:color-mix(in srgb,var(--good) 20%,transparent); }
.tk.r { background:color-mix(in srgb,var(--warn) 26%,transparent); }
.tk.i { background:color-mix(in srgb,#4a7fd1 24%,transparent); font-style:italic; text-decoration:underline dashed; text-underline-offset:3px; }
.tk.g { color:var(--ink2); background:color-mix(in srgb,var(--line) 70%,transparent); }
.tk.on,.src.on { outline-color:var(--ink); }
.metrics td:first-child { color:var(--ink2); }
.pl { white-space:pre-wrap; background:var(--card); border:1px solid var(--line); border-radius:8px; padding:10px 14px; font-size:.95rem; line-height:1.65; }
.figrow { display:flex; flex-wrap:wrap; gap:14px; align-items:flex-start; margin:10px 0; }
.fig { margin:0; background:var(--card); border:1px solid var(--line); border-radius:8px; padding:8px; }
.fig img { display:block; border-radius:4px; max-width:100%; height:auto; }
.fig figcaption { font-size:.82rem; color:var(--ink2); margin-top:6px; line-height:1.4; }
.fig { box-sizing:border-box; } .fig.w1 { width:240px; } .fig.w2 { width:330px; } .fig.full { width:100%; }
.crops { display:flex; flex-wrap:wrap; gap:8px; margin:8px 0 14px; }
.crops .fig { width:196px; padding:5px; } .crops .fig figcaption { font-size:.76rem; margin-top:3px; }
.sty td, .sty th { padding:6px 9px; }
.kbd { font-family:ui-monospace,Menlo,monospace; font-size:.9em; }
@media (max-width:720px) { .ba { grid-template-columns:1fr; } .ba .L { border-right:0; } .fig.w1,.fig.w2 { width:100%; box-sizing:border-box; } }
"""
RULES_JS = """
document.querySelectorAll('[data-s]').forEach(function(el){
  var id=el.getAttribute('data-s');
  el.addEventListener('mouseenter',function(){document.querySelectorAll('[data-s="'+id+'"]').forEach(function(e){e.classList.add('on');});});
  el.addEventListener('mouseleave',function(){document.querySelectorAll('[data-s="'+id+'"]').forEach(function(e){e.classList.remove('on');});});
});
"""

PRIOR = dict(total=852, decoded=637, gap=198, unplaced=17)      # metrics of the previous version (before the colour analysis)


def section_html():
    left, right, rows, leftovers, m = build()
    pct = lambda a, b: f"{100*a/b:.0f}%"
    s_c, s_k, s_r, s_i = (m['support'][t] for t in "ckri")
    mc = SA['mc_purple']
    crops = {(c['kind'], c['text']): c['file'] for c in SA['crops']}
    pieces = {st: [p for p in SA['pieces'] if p['style'] == st] for st in 'PRB'}
    tot_len = sum(len(p) for p in CORR) + len(CORR) - 1
    n_err = SA['n_errors']
    ec = Counter(e['par'] for e in SA['error_positions'])
    err_where = ", ".join(f"¶{k}" + (f" ×{v}" if v > 1 else "") for k, v in sorted(ec.items()))
    n_styled_chars = sum(len(p['text']) for p in SA['pieces'] if p['style'] in 'PRB')

    def crop(kind, text, label):
        f = crops[(kind, text)]
        return fig('images/rules-original.png', f, label, f"crop of the screenshot showing the {STYLE_LABEL[kind]} piece {text}")
    STYLE_LABEL = {'P': 'purple', 'R': 'large red', 'B': 'large blue'}
    gallery = "".join([
        crop('P', 'Addi', '<span class="sw sP">Addi</span> — ¶5'),
        crop('P', 'tional', '<span class="sw sP">tional</span> — ¶4, end of a visual line'),
        crop('P', 'no', '<span class="sw sP">no</span> — ¶4, start of the next line'),
        crop('P', 'tes:', '<span class="sw sP">tes:</span> — ¶2'),
        crop('R', "Do't", '<span class="sw sR">Do\'t</span> — ¶4'),
        crop('R', 'n', '<span class="sw sR">n</span> — ¶2'),
        crop('B', 'A', '<span class="sw sB">A</span> — ¶4'),
        crop('B', 'ye', '<span class="sw sB">ye</span> — ¶3'),
    ])

    grid = ['<div class="hd">Before — as posted (garbled; colours and sizes as in the screenshot)</div><div class="hd">After — my restoration</div>']
    for i, (l, r) in enumerate(zip(left, right)):
        grid.append(f'<div class="L"><span class="pn">¶{i+1}</span>{l}</div><div class="R"><span class="pn">¶{i+1}</span>{r}</div>')
    plain = "\n".join(rows)

    dis = [
        ("Additional notes:", '<span class="sP">Addi</span> (¶5), <span class="sP">tional</span> + <span class="sP">no</span> (¶4, still neighbours), <span class="sP">tes:</span> (¶2)', "all four purple — colour evidence"),
        ("Don't", '<span class="sR">Do\'t</span> (¶4)', '<span class="sR">n</span> (¶2, “hatebeA<span class="sR">n</span>Please”) — large red, colour evidence'),
        ("Aye <span class='small'>(tentative)</span>", '<span class="sB">A</span> (¶4, “-<span class="sB">A</span>rsa;d”)', '<span class="sB">ye</span> (¶3, “ch<span class="sB">ye</span> werewolf)”) — large blue, colour evidence'),
        ("explicit", "<code>exp</code> (end of ¶3, “expNSFW”)", "<code>licit</code> (¶2, “hgorms)licit”)"),
        ("ONLY", "<code>ON</code> (¶4, “whouONne”)", "<code>LY</code> (¶2, “licit LY if”) — both pieces are upper-case in the garble, as <i>ONLY</i> would be"),
    ]
    dis_rows = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td></tr>" for a, b, c in dis)
    ex = [
        ("letters missing (dropped, or moved elsewhere)", "Do't · chrs · goingvered · eceptions · spller, e mindful", "Don't · chars · going covered · exceptions · spoiler, be mindful — for <i>Don't</i> the missing letter is shown to have <i>moved</i> (the large red n in ¶2)"),
        ("neighbouring letters swapped", "migth", "might"),
        ("letters replaced / mangled", "hakely · otherwit, · cuy · ehawise", "likely · otherwise, · guy · otherwise"),
        ("spaces lost, words fused", "interactionmy · hatebeAnPlease · witsyouwhe", "interaction my · hate. Be … Please · with … you … when"),
        ("stray fragments in the wrong place", "“Dev”, “amp.”, “nender”, lone “y”, “b”, “D” …", "(pieces of words whose other halves are elsewhere)"),
        ("the word <i>error</i> inserted", "oerror · errors-swful · error igher …", "7 occurrences, all in the same small red — deleted, not restored"),
    ]
    ex_rows = "".join(f"<tr><td>{a}</td><td class='mono'>{b}</td><td class='mono'>{c}</td></tr>" for a, b, c in ex)
    lo = "  ·  ".join(f"¶{i+1}: " + " ".join(f"<code>{html.escape(x)}</code>" for x in runs) for i, runs in enumerate(leftovers) if runs)

    gist = """
<ul>
<li><b>Have fun; no hate.</b> <span class="small">(“fun!!” and “No hate.” survive intact; the rest of that opening is lost.)</span></li>
<li><b>Don't draw my non-human characters as human, or the reverse.</b> <span class="small">(with a werewolf as the example — the clearest sentence in the paragraph.)</span></li>
<li><b>NSFW is restricted.</b> <span class="small">“No … explicit NSFW” and “ONLY if … been given …” are both present, but the exact condition is lost.</span></li>
<li><b>Romance/interaction between characters is welcome.</b> <span class="small">(“Romance is cool, I'd … authentic interaction”.)</span></li>
<li><b>A large red “Don't”</b> emphasises a prohibition (“… /cigs involving my chars – cos …”; the details are mostly lost). <span class="small">The large blue “Aye” (yes) may be its counterpart, but I cannot say where it stood.</span></li>
<li><b>Outfit suggestions are welcome.</b> <span class="small">There are also caveats about “presentation”, gender and “unless specified otherwise”, but their details are mostly lost.</span></li>
<li><b>A purple “Additional notes:” heading</b> <span class="small">sits at the ¶4/¶5 boundary, so ¶5–¶6 are most likely that section:</span> <b>the owner's characters are adults (“my guys are 20+”), character battles are fine (“so go ham”), with a darker tone and a spoiler warning:</b> “my characters going covered in blood / afraid and exhausted / fighting tooth and nail to survive &lt;- my spoiler, be mindful.”</li>
</ul>"""

    html_out = f"""
<h2>The “rules” section: does the colour coding matter?</h2>
<p>The “Characters (0) — redacted_entity's Character Permissions” panel of the profile is where the garbled rules text sits. The poster's text transcription carries no formatting, but the screenshot does: most of the text is plain grey, while some fragments are <b>purple</b>, some are <b>large red or large blue</b>, and seven are the small red word <span class="err">error</span>. My earlier reading ignored all that. The question is whether the colours say anything about how to put the text back together.</p>
{fig('images/rules-original.png', 'images/rules-original.png', '<b>Figure 3</b> (repeated at a larger size) — the rules section as it originally appeared on the site; click for the full-size screenshot. The six garbled paragraphs are right-aligned; the blank band at the top is part of the page.', 'Screenshot of the Characters tab showing the garbled rules text with purple, red, blue and small red error fragments', 'full')}

<h3 style="font-family:system-ui;margin-top:20px">1. Style inventory (measured from the screenshot)</h3>
<p>I hue-clustered the screenshot (<code>scripts/style_analysis.py</code>) and aligned every coloured span with the transcription. There are exactly 16 styled spans — four colour styles plus one emoji; everything else is plain grey. The counts agree with the transcription (7 <i>error</i>s, and the four purple / two red / two blue pieces all appear in it).</p>
<table class="sty">
<tr><th>Style</th><th>Pieces, as they sit in the garble</th><th>What they could be</th></tr>
<tr><td><span class="err">error</span> small red</td><td>{n_err} × the word “error” ({err_where})</td><td>Always the identical 5-letter word. Most likely a glitch insertion, not part of the original text.</td></tr>
<tr><td><span class="sP">purple</span> normal size</td><td><span class="sP">tes:</span> (¶2) · <span class="sP">tional</span> (¶4) · <span class="sP">no</span> (¶4) · <span class="sP">Addi</span> (¶5)</td><td>A single styled heading, chopped into 4 pieces: <b>“Additional notes:”</b></td></tr>
<tr><td><span class="sR">LARGE red</span></td><td><span class="sR">n</span> (¶2) · <span class="sR">Do't</span> (¶4)</td><td>A single styled word, <b>“Don't”</b>, with its <i>n</i> moved away from the middle</td></tr>
<tr><td><span class="sB">LARGE blue</span></td><td><span class="sB">A</span> (¶4) · <span class="sB">ye</span> (¶3)</td><td>The word <b>“Aye”</b> (capital A first). Only three letters, so weaker evidence.</td></tr>
<tr><td>😎 emoji</td><td>1, end of ¶5</td><td>Nothing to reunite.</td></tr>
</table>
<p class="small">Crops of the eight non-<i>error</i> pieces, enlarged 3× from the screenshot (click for the full screenshot):</p>
<div class="crops">{gallery}</div>

<h3 style="font-family:system-ui;margin-top:20px">2. Do pieces that share a style belong together?</h3>
<p>If the glitch effect chops the text into pieces and moves them around <i>without</i> stripping their formatting, then each styled word of the original would show up as a few same-coloured pieces, and putting them back together would give English. That is exactly what happens:</p>
<ul>
<li><b>Purple → “Additional notes:”.</b> Of the 24 possible orderings of the four purple pieces, the ones that read as English are <i>additional notes</i> and <i>notes additional</i>. The ordering the garble itself suggests is the first: <span class="sP">tional</span> and <span class="sP">no</span> are still next to each other, with only a line wrap (a space) between them, and the colon sits on the last piece. As a null model I drew 4 random chunks of the same sizes ({', '.join(str(s) for s in mc['sizes'])} characters) from the garbled text itself, {mc['trials']:,} times: only <b>{mc['hits']}</b> draws ({100*mc['hits']/mc['trials']:.2f}%) could be arranged into one or two common English words of 3+ letters (30,000-word frequency list), so this is not a fluke.</li>
<li><b>Large red → “Don't”.</b> Putting the lone <span class="sR">n</span> back into <span class="sR">Do't</span> gives <i>Don't</i> at once; of the five places the <i>n</i> could go, only one makes a contraction. This also explains why <i>Do't</i> looked like a “dropped letter”: the letter was not dropped, it was moved.</li>
<li><b>Large blue → “Aye”.</b> <span class="sB">A</span> + <span class="sB">ye</span> gives <i>Aye</i> (the capital A stays word-initial); the other order would be “yeA”. Real, but three letters prove little — I treat it as a probable reading, and I cannot say where it stood in the text.</li>
<li><b>Small red “error”.</b> Seven identical, tiny tokens: always the same word, size and colour, so there is nothing to reunite. I read them as pure insertions, although I cannot tell whether each one replaced anything. (The previous version already removed them.)</li>
</ul>
<p><b>So yes: the colours are a reliable key for reassembling the styled words</b>, because each piece keeps its style when it is moved. Two further things follow from the positions of the pieces:</p>
<ul>
<li>The pieces <i>moved</i> a long way — a distance of up to {max(p['g'] for p in pieces['P']) - min(p['g'] for p in pieces['P'])} characters in a {tot_len}-character text — but <span class="sP">tional</span> and <span class="sP">no</span> did not move relative to each other, and <span class="sP">Addi</span> sits only {pieces['P'][3]['g'] - pieces['P'][2]['g']} characters after them. Three of four pieces within one ~60-character window has roughly a 1% chance if the pieces landed at random (an after-the-fact estimate), so the heading probably stood close to the ¶4/¶5 boundary, i.e. <b>“Additional notes:” introduces ¶5–¶6</b>, which are indeed the “my guys are 20+ / go ham / gore” paragraphs.</li>
<li>This fits a simple damage model: <i>pieces of 1–6 characters are cut out and pasted elsewhere</i> (<i>Do't</i> and <i>tional no</i> show the neighbours rejoining after the cut). That is the same kind of damage as the three cipher lines, only heavier and with styles attached.</li>
</ul>
<p class="small"><b>Limit.</b> Colour only helps for the 8 styled pieces ({n_styled_chars} characters out of about {tot_len}). All of the plain grey text has no such key, which is why the rest of the restoration stays partial.</p>

<h3 style="font-family:system-ui;margin-top:20px">3. What this changed in my restoration</h3>
<ul>
<li><b>“Additionally,” was wrong.</b> I had joined <i>Addi</i> (¶5), <i>tional</i> (¶4) and <i>ly</i> (the start of ¶6). But <i>ly</i> is plain grey while <i>Addi</i> and <i>tional</i> are purple, so they cannot be one word. The purple pieces make <b>“Additional notes:”</b> instead, which also explains the formerly unexplained leftover <i>gtes:</i> in ¶2. The loose <i>ly</i> is now an unread fragment.</li>
<li><b>“Do't” → “Don't”</b> now rests on evidence rather than a guess, and the large red <i>n</i> (previously an unplaced “An” in ¶2) is accounted for.</li>
<li><b>“Aye”</b> is new (colour-matched), displayed where its <i>A</i> sits, but its true position is unknown.</li>
<li><b>“chars (e.g. werewolf)” lost some support.</b> I had counted the blue <i>ye</i> as part of “chars (e.g.”. It belongs to <i>Aye</i> instead; the sentence still reads, but the letters <i>ars (e.g.</i> are not visibly present in ¶3 any more. They moved elsewhere, as pieces do.</li>
<li>The gist below now notes the “Additional notes” section and the red/blue emphasis.</li>
</ul>

<h2>The “rules” paragraph: before and after</h2>
<p>The posted rules text looks like the same kind of fragment-shuffling as the cipher lines, but heavier, and it is not a clean anagram per paragraph. Below is my attempt to undo it. <b>This is a partial, best-effort reading, not a recovered verbatim original.</b> Every phrase on the right is tied to the garbled fragments it came from: hover a phrase (or a highlighted fragment) to see the link — for the colour-matched words, all of their pieces light up, even in other paragraphs. Where I couldn't read a fragment I left an ellipsis rather than invent text. The left column now shows the original colours and sizes.</p>
<div class="legend">
<span><span class="tk c">colour-matched</span> same-style pieces reunited (new)</span>
<span><span class="tk k">recovered</span> words survive, ≤ 1 letter off</span>
<span><span class="tk r">repaired</span> recognisable, letters missing/swapped/displaced</span>
<span><span class="tk i">inferred</span> a guess from context</span>
<span><span class="tk g">…</span> fragment I could not read</span>
<span><span class="err">error</span> inserted word (removed)</span>
</div>
<div class="ba">{"".join(grid)}</div>
<p class="small">A colour-matched word is shown where its main piece sits in the garble, not necessarily where it stood in the original: <i>Additional notes:</i> at the start of ¶5 (where <i>Addi</i> is), <i>Don't</i> at the start of ¶4, <i>Aye</i> beside its <i>A</i>.</p>

<h3 style="font-family:system-ui;margin-top:20px">Restored text, plain</h3>
<div class="pl">{html.escape(plain)}</div>

<h3 style="font-family:system-ui;margin-top:20px">What the rules appear to say (gist)</h3>
{gist}
<p class="small">The gist is my interpretation of the restored phrases above; anything marked <i>repaired</i> or <i>inferred</i> there carries the same uncertainty here.</p>

<h3 style="font-family:system-ui;margin-top:20px">What kind of damage this is</h3>
<table><tr><th>Type</th><th>Garbled</th><th>Restored</th></tr>{ex_rows}</table>
<p>Some fragments have travelled <b>between</b> paragraphs, which is why a letter-for-letter check per paragraph fails (unlike the three cipher lines). The first three words are the ones the colours reunite:</p>
<table><tr><th>Word</th><th>Piece A</th><th>Piece B</th></tr>{dis_rows}</table>

<h3 style="font-family:system-ui;margin-top:20px">How much of it is restored</h3>
<table class="metrics">
<tr><td>Letters in the garbled text (excluding the 7 inserted “error”s)</td><td>{m['total_letters']}</td></tr>
<tr><td>Letters sitting in fragments I turned into words (colour-matched / recovered / repaired / inferred)</td><td>{m['decoded']} ({pct(m['decoded'], m['total_letters'])}) <span class="small">— before the colour analysis: {PRIOR['decoded']} ({pct(PRIOR['decoded'], PRIOR['total'])})</span></td></tr>
<tr><td>Letters in fragments I located but could not read (the ellipses)</td><td>{m['gap']} ({pct(m['gap'], m['total_letters'])}) <span class="small">— before: {PRIOR['gap']} ({pct(PRIOR['gap'], PRIOR['total'])})</span></td></tr>
<tr><td>Letters not placed anywhere</td><td>{m['unplaced']} <span class="small">— before: {PRIOR['unplaced']}</span></td></tr>
<tr><td>“Colour-matched” words: letters found in their source pieces</td><td>{s_c[0]} of {s_c[1]} ({pct(*s_c)})</td></tr>
<tr><td>“Recovered” words: letters found in their source fragments</td><td>{s_k[0]} of {s_k[1]} ({pct(*s_k)})</td></tr>
<tr><td>“Repaired” words: letters found in their source fragments (the rest were dropped letters I restored)</td><td>{s_r[0]} of {s_r[1]} ({pct(*s_r)})</td></tr>
<tr><td>“Inferred” words: letters found in their source fragments</td><td>{s_i[0]} of {s_i[1]} ({pct(*s_i)})</td></tr>
</table>
<p class="small">“Located in fragments I turned into words” measures how much of the garble my reading accounts for, <i>not</i> how correct it is: a wrong reading would count too, and the colour-matched words are the only ones that are checked by something independent of my reading. The unplaced single letters: {lo}.</p>
<p class="small"><b>What I'm confident of:</b> “Additional notes:” and “Don't” (colour-matched), the sentences about non-human characters (“Please don't draw my non-human chars (e.g. werewolf) as human or vice versa”), “No hate”, “so go ham”, “my characters going covered in blood/afraid and exhausted/fighting tooth and nail to survive &lt;- my spoiler, be mindful”, and “outfit ideas”. <b>Least certain:</b> “Aye” (placement), the middle of ¶4 (e.g. “don't draw their prey”, “who … with might me”), ¶5's “character battle”, and every ellipsis. I searched once for a public copy of the original text and found none, and the live profile is behind a Cloudflare challenge that I did not try to get around, so apart from the colour evidence and the letter accounting above there is nothing to check this restoration against.</p>
"""
    return RULES_CSS, html_out, RULES_JS, m, rows
