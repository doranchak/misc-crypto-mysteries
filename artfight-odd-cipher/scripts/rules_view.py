"""Build the before/after view of the glitched rules paragraph from rules/corrupted.txt + rules/restoration.py."""
import re, sys, html, json
from collections import Counter
sys.path.insert(0, '../rules')
from restoration import PARAS

CORR = open('../rules/corrupted.txt').read().splitlines()
assert len(CORR) == len(PARAS)
TIER_NAME = {"k": "recovered", "r": "repaired", "i": "inferred", "g": "gap"}

def locate(par, pattern, claimed):
    """Return list of (start,end) char ranges to highlight for pattern with {..} marking the highlighted part."""
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

def build():
    left_html, right_html, rows = [], [], []
    tot_alpha = tot_claimed = 0
    sup = {"k": [0, 0], "r": [0, 0], "i": [0, 0]}      # [supported letters, letters in segment text]
    leftovers = []
    seg_counter = 0
    sid_tier = {}
    tot_decoded = tot_gap = 0
    tier_letters = Counter()
    for pi, (par, segs) in enumerate(zip(CORR, PARAS)):
        n = len(par)
        claimed = [None] * n          # seg id per character
        err = [False] * n
        for m in re.finditer(r'error', par, flags=re.I):
            for k in range(m.start(), m.end()): err[k] = True
        seg_ids = []
        for tier, text, srcs in segs:
            sid = f"s{seg_counter}"; seg_counter += 1
            seg_ids.append(sid); sid_tier[sid] = tier
            src_letters = Counter()
            for pat in srcs:
                a, b = locate(par, pat, claimed)
                for k in range(a, b):
                    assert not err[k], (pi, pat)
                    claimed[k] = sid
                src_letters.update(c.lower() for c in par[a:b] if c.isalpha())
            if tier in sup:
                seg_letters = Counter(c.lower() for c in text if c.isalpha())
                sup[tier][0] += sum((seg_letters & src_letters).values())
                sup[tier][1] += sum(seg_letters.values())
        # left rendering
        out = []; k = 0
        while k < n:
            e, c = err[k], claimed[k]
            j = k
            while j < n and err[j] == e and claimed[j] == c: j += 1
            chunk = html.escape(par[k:j])
            if e: out.append(f'<span class="err">{chunk}</span>')
            elif c: out.append(f'<span class="src" data-s="{c}">{chunk}</span>')
            else: out.append(chunk)
            k = j
        left_html.append("".join(out))
        # right rendering
        parts = []; plain = []; prev = ""
        for (tier, text, srcs), sid in zip(segs, seg_ids):
            glue = " "
            if prev and (prev[-1] in "(/" or text[0] in ",.;:!?)/"): glue = ""
            parts.append(glue + f'<span class="tk {tier}" data-s="{sid}" title="{TIER_NAME[tier]}">{html.escape(text)}</span>')
            plain.append(glue + text); prev = text
        right_html.append("".join(parts).lstrip())
        # accounting
        alpha_idx = [k for k in range(n) if par[k].isalpha() and not err[k]]
        tot_alpha += len(alpha_idx)
        tot_claimed += sum(1 for k in alpha_idx if claimed[k])
        tot_decoded += sum(1 for k in alpha_idx if claimed[k] and sid_tier[claimed[k]] != 'g')
        tot_gap += sum(1 for k in alpha_idx if claimed[k] and sid_tier[claimed[k]] == 'g')
        # leftover runs (unclaimed, non-error, non-space)
        runs = []; k = 0
        while k < n:
            if claimed[k] is None and not err[k] and not par[k].isspace():
                j = k
                while j < n and claimed[j] is None and not err[j] and not par[j].isspace(): j += 1
                if par[k:j].strip("[](){}.,;:-/!"): runs.append(par[k:j])
                k = j
            else: k += 1
        leftovers.append(runs)
        rows.append(("".join(plain)).strip())
        for tier, text, srcs in segs:
            tier_letters[tier] += sum(1 for c in text if c.isalpha())
    metrics = dict(
        total_letters=tot_alpha, claimed=tot_claimed, decoded=tot_decoded, gap=tot_gap, unplaced=tot_alpha-tot_claimed,
        support={t: (v[0], v[1]) for t, v in sup.items()},
        tier_letters=dict(tier_letters),
        n_segments=seg_counter,
    )
    return left_html, right_html, rows, leftovers, metrics

if __name__ == "__main__":
    l, r, rows, lo, m = build()
    print(json.dumps(m, indent=1))
    for i, t in enumerate(rows): print(f"P{i+1}:", t, "\n   leftovers:", lo[i], "\n")


# ----------------------------------------------------------------------------------------------------------------
RULES_CSS = """
.legend { display:flex; flex-wrap:wrap; gap:6px 14px; font-size:.85rem; margin:8px 0 14px; }
.legend .tk { padding:1px 8px; }
.ba { display:grid; grid-template-columns:1fr 1fr; gap:0; border:1px solid var(--line); border-radius:8px; overflow:hidden; margin:10px 0; }
.ba > div { padding:9px 13px; border-bottom:1px solid var(--line); }
.ba > div:nth-last-child(-n+2) { border-bottom:0; }
.ba .hd { background:var(--card); font-weight:600; font-size:.85rem; color:var(--ink2); position:sticky; top:0; }
.ba .L { font:12.5px/1.65 ui-monospace,Menlo,monospace; border-right:1px solid var(--line); word-break:break-word; background:color-mix(in srgb,var(--card) 70%,transparent); }
.ba .R { font-size:15.5px; line-height:1.7; }
.ba .pn { display:block; color:var(--ink2); font:600 .7rem system-ui; margin-bottom:2px; letter-spacing:.04em; }
.err { color:var(--bad); font-weight:700; background:color-mix(in srgb,var(--bad) 14%,transparent); border-radius:3px; }
.src { background:color-mix(in srgb,var(--warn) 22%,transparent); border-radius:3px; }
.tk { border-radius:4px; padding:0 3px; transition:outline-color .1s; outline:2px solid transparent; }
.tk.k { background:color-mix(in srgb,var(--good) 20%,transparent); }
.tk.r { background:color-mix(in srgb,var(--warn) 26%,transparent); }
.tk.i { background:color-mix(in srgb,#4a7fd1 24%,transparent); font-style:italic; text-decoration:underline dashed; text-underline-offset:3px; }
.tk.g { color:var(--ink2); background:color-mix(in srgb,var(--line) 70%,transparent); }
.tk.on,.src.on { outline-color:var(--ink); }
.metrics td:first-child { color:var(--ink2); }
.pl { white-space:pre-wrap; background:var(--card); border:1px solid var(--line); border-radius:8px; padding:10px 14px; font-size:.95rem; line-height:1.65; }
@media (max-width:720px) { .ba { grid-template-columns:1fr; } .ba .L { border-right:0; } }
"""
RULES_JS = """
document.querySelectorAll('[data-s]').forEach(function(el){
  var id=el.getAttribute('data-s');
  el.addEventListener('mouseenter',function(){document.querySelectorAll('[data-s="'+id+'"]').forEach(function(e){e.classList.add('on');});});
  el.addEventListener('mouseleave',function(){document.querySelectorAll('[data-s="'+id+'"]').forEach(function(e){e.classList.remove('on');});});
});
"""

def section_html():
    left, right, rows, leftovers, m = build()
    pct = lambda a, b: f"{100*a/b:.0f}%"
    s_k, s_r, s_i = m['support']['k'], m['support']['r'], m['support']['i']
    grid = ['<div class="hd">Before — as posted (garbled)</div><div class="hd">After — my restoration</div>']
    for i, (l, r) in enumerate(zip(left, right)):
        grid.append(f'<div class="L"><span class="pn">¶{i+1}</span>{l}</div><div class="R"><span class="pn">¶{i+1}</span>{r}</div>')
    plain = "\n".join(rows)
    dis = [
        ("explicit", "<code>exp</code> (end of ¶3, “expNSFW”)", "<code>licit</code> (¶2, “hgorms)licit”)"),
        ("ONLY", "<code>ON</code> (¶4, “whouONne”)", "<code>LY</code> (¶2, “licit LY if”) — both pieces are upper-case in the garble, as <i>ONLY</i> would be"),
        ("Additionally", "<code>Addi</code> (¶5, “biAddiin”) and <code>tional</code> (¶4, “ottional”)", "<code>ly</code> (start of ¶6)"),
    ]
    dis_rows = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td></tr>" for a, b, c in dis)
    ex = [
        ("dropped letters", "Do't · chrs · goingvered · eceptions · spller, e mindful", "Don't · chars · going covered · exceptions · spoiler, be mindful"),
        ("neighbouring letters swapped", "migth", "might"),
        ("letters replaced / mangled", "hakely · otherwit, · cuy · ehawise", "likely · otherwise, · guy · otherwise"),
        ("spaces lost, words fused", "interactionmy · hatebeAnPlease · witsyouwhe", "interaction my · hate. Be … Please · with … you … when"),
        ("stray fragments in the wrong place", "“Dev”, “amp.”, “nender”, lone “y”, “b”, “D” …", "(pieces of words whose other halves are elsewhere)"),
        ("the word <i>error</i> inserted", "oerror · errors-swful · error igher …", f"7 occurrences — deleted, not restored"),
    ]
    ex_rows = "".join(f"<tr><td>{a}</td><td class='mono'>{b}</td><td class='mono'>{c}</td></tr>" for a, b, c in ex)
    lo = "  ·  ".join(f"¶{i+1}: " + " ".join(f"<code>{html.escape(x)}</code>" for x in runs) for i, runs in enumerate(leftovers) if runs)
    gist = """
<ul>
<li><b>Have fun; no hate.</b> <span class="small">(“fun!!” and “No hate.” survive intact; the rest of that opening is lost.)</span></li>
<li><b>Don't draw my non-human characters as human, or the reverse.</b> <span class="small">(with a werewolf as the example — the clearest sentence in the paragraph.)</span></li>
<li><b>NSFW is restricted.</b> <span class="small">“No … explicit NSFW” and “ONLY if … been given …” are both present, but the exact condition is lost.</span></li>
<li><b>Romance/interaction between characters is welcome.</b> <span class="small">(“Romance is cool, I'd … authentic interaction”.)</span></li>
<li><b>The owner's characters are adults.</b> <span class="small">(“my guys are 20+”.)</span></li>
<li><b>Outfit suggestions are welcome.</b> <span class="small">There are also caveats about “presentation”, gender and “unless specified otherwise”, but their details are mostly lost.</span></li>
<li><b>Darker tone, with a spoiler warning:</b> “my characters going covered in blood / afraid and exhausted / fighting tooth and nail to survive &lt;- my spoiler, be mindful.”</li>
</ul>"""
    html_out = f"""
<h2>The “rules” paragraph: before and after</h2>
<p>The posted rules text looks like the same kind of fragment-shuffling as the cipher lines, but heavier, and it is not a clean anagram. Below is my attempt to undo it. <b>This is a partial, best-effort reading, not a recovered verbatim original.</b> Every phrase on the right is tied to the garbled fragments it came from: hover a phrase (or a highlighted fragment) to see the link. Where I couldn't read a fragment I left an ellipsis rather than invent text.</p>
<div class="legend">
<span><span class="tk k">recovered</span> words survive, ≤ 1 letter off</span>
<span><span class="tk r">repaired</span> recognisable, letters missing/swapped/displaced</span>
<span><span class="tk i">inferred</span> a guess from context</span>
<span><span class="tk g">…</span> fragment I could not read</span>
<span><span class="err">error</span> inserted word (removed)</span>
</div>
<div class="ba">{"".join(grid)}</div>

<h3 style="font-family:system-ui;margin-top:20px">Restored text, plain</h3>
<div class="pl">{html.escape(plain)}</div>

<h3 style="font-family:system-ui;margin-top:20px">What the rules appear to say (gist)</h3>
{gist}
<p class="small">The gist is my interpretation of the restored phrases above; anything marked <i>repaired</i> or <i>inferred</i> there carries the same uncertainty here.</p>

<h3 style="font-family:system-ui;margin-top:20px">What kind of damage this is</h3>
<table><tr><th>Type</th><th>Garbled</th><th>Restored</th></tr>{ex_rows}</table>
<p>Some fragments have travelled <b>between</b> paragraphs, which is why a letter-for-letter check per paragraph fails (unlike the three cipher lines):</p>
<table><tr><th>Word</th><th>Piece A</th><th>Piece B</th></tr>{dis_rows}</table>

<h3 style="font-family:system-ui;margin-top:20px">How much of it is restored</h3>
<table class="metrics">
<tr><td>Letters in the garbled text (excluding the 7 inserted “error”s)</td><td>{m['total_letters']}</td></tr>
<tr><td>Letters sitting in fragments I turned into words (recovered / repaired / inferred)</td><td>{m['decoded']} ({pct(m['decoded'], m['total_letters'])})</td></tr>
<tr><td>Letters in fragments I located but could not read (the ellipses)</td><td>{m['gap']} ({pct(m['gap'], m['total_letters'])})</td></tr>
<tr><td>Letters not placed anywhere</td><td>{m['unplaced']}</td></tr>
<tr><td>“Recovered” words: letters found in their source fragments</td><td>{s_k[0]} of {s_k[1]} ({pct(*s_k)})</td></tr>
<tr><td>“Repaired” words: letters found in their source fragments (the rest were dropped letters I restored)</td><td>{s_r[0]} of {s_r[1]} ({pct(*s_r)})</td></tr>
<tr><td>“Inferred” words: letters found in their source fragments</td><td>{s_i[0]} of {s_i[1]} ({pct(*s_i)})</td></tr>
</table>
<p class="small">“Located in fragments I turned into words” measures how much of the garble my reading accounts for, <i>not</i> how correct it is: a wrong reading would count too. The unplaced single letters: {lo}.</p>
<p class="small"><b>What I'm confident of:</b> the sentences about non-human characters (“Please don't draw my non-human chars (e.g. werewolf) as human or vice versa”), “No hate”, “so go ham”, “my characters going covered in blood/afraid and exhausted/fighting tooth and nail to survive &lt;- my spoiler, be mindful”, and “outfit ideas”. <b>Least certain:</b> the middle of ¶4 (e.g. “don't draw their prey”, “who … with might me”), ¶5's “character battle”, and every ellipsis. I searched once for a public copy of the original text and found none, so apart from the letter accounting above there is nothing to check this restoration against.</p>
"""
    return RULES_CSS, html_out, RULES_JS, m, rows
