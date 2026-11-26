"""Build ../index.html: report on the cipher slip found in Tanquerey's Synopsis (r/codes 1y5g8r3)."""
import html

# ---- interlinear data: (glyph-crop id, plaintext letter, css class) ----
# class: 'ok' decoded, 'cap' decoded capital, 'hd' heading glyph decoded on the second pass,
#        'weak' decoded but irregular, 'punct'
TITLE = [('t0', 'K', 'cap'), ('t0b', 'o', 'ok'), ('t1', 'm', 'hd'), ('t2', 'u', 'hd'), ('t3', 'n', 'ok'),
         ('t4', 'i', 'ok'), ('t5', 'k', 'hd'), ('t6', 'a', 'ok'), ('t7', 'c', 'hd'), ('t8', 'j', 'hd'),
         ('t9', 'a ,', 'ok')]
LINE = [
    [('n1', '1.', 'punct')],
    [('w1_1', 'P', 'cap'), ('w1_2', 'r', 'hd'), ('w1_3', 'a', 'ok'), ('w1_4', 'k', 'hd'),
     ('w1_5', 't', 'hd'), ('w1_6', 'y', 'hd'), ('w1_7', 'k?', 'weak'), ('w1_8', 'a', 'ok'), ('colon', ':', 'punct')],
    [('w2_1', 'Z', 'cap'), ('w2_2', 'g', 'ok'), ('w2_3', 'o', 'ok'), ('w2_4', 'd', 'ok'), ('w2_5', 'z', 'ok'),
     ('w2_6', 'e', 'ok'), ('w2_7', 'n', 'ok'), ('w2_8', 'i', 'ok'), ('w2_9', 'e', 'ok')],
    [('w3_1', 's', 'ok'), ('w3_2', 'i', 'ok'), ('w3_3', 'ę', 'ok')],
    [('w4_1', 'n', 'ok'), ('w4_2', 'a', 'ok')],
    [('w5_1', 'w', 'ok'), ('w5_2', 'o', 'ok'), ('w5_3', 'l', 'ok'), ('w5_4', 'ę', 'ok')],
    [('w6_1', 'B', 'cap'), ('w6_2', 'o', 'ok'), ('w6_3', 'ż', 'ok'), ('w6_4', 'ą', 'ok'), ('stop', '.', 'punct')],
]

# ---- glyph classes for hover/click highlighting: crop id -> glyph-class id ----
# Same class = same glyph shape (as read). The letter highlight is separate, so a letter with two
# glyph forms (k = serifed I or the blob; z = almond or capital oval) still lights up in full.
GCLASS = {
    't0': 'serifI', 't0b': 'dot', 't1': 'Nlead', 't2': 'V', 't3': 'arch', 't4': 'S', 't5': 'serifI',
    't6': 'square', 't7': 'tilde', 't8': 'footed4',  't9': 'square',
    'w1_1': 'bshape', 'w1_2': 'r', 'w1_3': 'square', 'w1_4': 'serifI', 'w1_5': 'invT', 'w1_6': 'dotted4',
    'w1_7': 'blob', 'w1_8': 'square',
    'w2_1': 'zOval', 'w2_2': 'check', 'w2_3': 'dot', 'w2_4': 'bowlD', 'w2_5': 'zOval', 'w2_6': 'stroke',
    'w2_7': 'arch', 'w2_8': 'S', 'w2_9': 'stroke',
    'w3_1': 'triangle', 'w3_2': 'S', 'w3_3': 'strokeHook',
    'w4_1': 'arch', 'w4_2': 'square',
    'w5_1': 'staff', 'w5_2': 'dot', 'w5_3': 'flatL', 'w5_4': 'strokeHook',
    'w6_1': 'Lshape', 'w6_2': 'dot', 'w6_3': 'ovalDot', 'w6_4': 'squareHook',
}
GDESC = {
    'serifI': 'serifed Ɪ (big initial = capital)', 'dot': 'mid-height dot', 'Nlead': 'N with lead-in stroke',
    'V': 'V', 'arch': 'Λ arch (title form has a cross-stroke)', 'S': 'S', 'square': 'square (dotted / heavy / plain)',
    'tilde': 'tilde-like stroke', 'footed4': '"4"/ʎ with foot stroke', 'bshape': 'b-shape (flipped P)',
    'r': 'r', 'invT': 'inverted T ⊥', 'dotted4': 'ʎ with dot in loop', 'blob': 'dark blob (irregular)',
    'check': 'long-armed check √', 'bowlD': 'upright with up-turned bowl',
    'zOval': 'z oval (capital Z: larger, slashed, with x; lower-case z: almond with dots)', 'stroke': 'short slanted stroke', 'triangle': 'filled triangle ∆',
    'strokeHook': 'stroke + zigzag hook', 'staff': 'staff with two crossbars ‡', 'flatL': 'upright with flat foot ┘',
    'Lshape': 'L-shape └', 'ovalDot': 'oval-with-x + dot above', 'squareHook': 'square + zigzag hook',
}

# ---- key tables ----
KEY = [
    ('w2_3', 'small mid-height dot', 'o', 'Appears inside words wherever Polish needs <i>o</i> (zg<b>o</b>dzenie, w<b>o</b>lę, B<b>o</b>żą, and K<b>o</b>munikacja). My first pass took it for punctuation, and that one mistake hid the whole solution.'),
    ('w2_6', 'short slanted stroke (like a dotless ı)', 'e', 'Ends the 9-glyph word twice (…<b>e</b>ni<b>e</b>).'),
    ('w3_3', 'the same stroke + zigzag hook below', 'ę', 'The hook is a Polish <b>ogonek</b>. The cipher keeps diacritics: e&rarr;ę is drawn as cipher-e + hook.'),
    ('w4_2', 'small square (dotted in the bold lines)', 'a', '<i>na</i>; the same square with a hook ends the line as <i>ą</i>; dotted squares give the a&rsquo;s of Komunik<b>a</b>cj<b>a</b> and Pr<b>a</b>ktyk<b>a</b>.'),
    ('w6_4', 'square + zigzag hook below', 'ą', 'Second ogonek glyph. It pairs with the square = a, as the stroke pairs with e/ę.'),
    ('w2_7', 'Λ (pointed arch)', 'n', '…e<b>n</b>ie, <b>n</b>a; the bold title has the same arch with a cross-stroke (Komu<b>n</b>ikacja).'),
    ('w2_8', 'S', 'i', '…en<b>i</b>e, s<b>i</b>ę and Komun<b>i</b>kacja: same glyph, same letter.'),
    ('w3_1', 'filled triangle ∆', 's', '<b>s</b>ię.'),
    ('w5_1', 'staff with two crossbars ‡', 'w', '<b>w</b>olę.'),
    ('w5_3', 'upright with flat foot to the left ┘', 'l', 'wo<b>l</b>ę. Compare the next row: the <i>d</i> glyph has an up-turned, bowl-like foot.'),
    ('w2_4', 'upright with up-turned bowl (open cursive d)', 'd', 'zgo<b>d</b>zenie. At low zoom it looks like the <i>l</i> glyph; side by side the two differ.'),
    ('w2_2', 'long-armed check mark √', 'g', 'z<b>g</b>odzenie (w is already ‡, so <i>zwodzenie</i> is excluded).'),
    ('w2_5', 'almond/oval with dots', 'z', 'zgod<b>z</b>enie.'),
    ('w2_1', 'larger slashed oval with an "x" mark', 'Z (capital)', 'Sentence-initial <b>Z</b>. It is a bigger, decorated oval like the lower-case z.'),
    ('w6_3', 'oval-with-x + dot above', 'ż', 'Bo<b>ż</b>ą. The dot above is the Polish over-dot: z&rarr;ż, again written as cipher-z + diacritic.'),
    ('w6_1', 'L-shape └', 'B (capital)', '<b>B</b>ożą. Capitalised exactly where Polish religious writing capitalises <i>Boża</i>.'),
]
KEY2 = [
    ('t5', 'serifed Ɪ', 'k', 'Komuni<b>k</b>acja and Pra<b>k</b>tyka. The big decorated I that opens the title is the same glyph as a capital: <b>K</b>omunikacja.'),
    ('t1', 'N with a long lead-in stroke', 'm', 'Ko<b>m</b>unikacja.'),
    ('t2', 'V', 'u', 'Kom<b>u</b>nikacja. V for u is the Latin-capital habit. V and Λ (u and n) are drawn as rotations of each other, like the letters themselves.'),
    ('t7', 'short tilde-like stroke ~', 'c', 'Komunika<b>c</b>ja.'),
    ('t8', '"4"/ʎ with a foot stroke', 'j', 'Komunikac<b>j</b>a.'),
    ('w1_1', 'b-shape (a P flipped top-to-bottom)', 'P (capital)', '<b>P</b>raktyka, at the start of the heading word.'),
    ('w1_2', 'r', 'r', 'P<b>r</b>aktyka.'),
    ('w1_5', 'inverted T ⊥', 't', 'Prak<b>t</b>yka. It is an upside-down T.'),
    ('w1_6', 'ʎ with a dot in its loop', 'y', 'Prakt<b>y</b>ka. It is an upside-down y. It differs from the title&rsquo;s <i>j</i> glyph, which has a foot stroke and no dot.'),
    ('w1_7', 'dark blob with a light centre', 'k ?', 'Prakty<b>k</b>a. <b>This is the weak point:</b> the word needs a second <i>k</i> here, but the glyph does not look like the Ɪ used for k elsewhere. It may be a blotted or variant k.'),
]

TITLE_PLAIN = 'Komunikacja'
HEAD_PLAIN = 'Praktyka'


def glyph_cell(gid, letter, cls):
    g = GCLASS.get(gid)
    if g is None:  # punctuation: not interactive
        return (f'<div class="g {cls}"><img src="glyphs/{gid}.png" alt="glyph {gid}">'
                f'<span>{html.escape(letter)}</span></div>')
    base = letter.replace('?', '').replace(',', '').strip().lower()
    # no native title= tooltips: they sit under the cursor and hide highlighted glyphs;
    # the page script shows its own tooltip placed clear of every highlighted glyph.
    return (f'<div class="g {cls}" data-g="{g}" data-l="{html.escape(base)}" data-desc="{html.escape(GDESC[g])}">'
            f'<img src="glyphs/{gid}.png" alt="glyph: {html.escape(GDESC[g])}" tabindex="0">'
            f'<span tabindex="0" aria-label="letter {html.escape(base)}">{html.escape(letter)}</span></div>')


def words_html(words):
    out = []
    for w in words:
        out.append('<div class="word">' + ''.join(glyph_cell(*g) for g in w) + '</div>')
    return '\n'.join(out)


title_html = '<div class="word">' + ''.join(glyph_cell(*g) for g in TITLE) + '</div>'
line_html = words_html(LINE)


def rows(key):
    return '\n'.join(
        f'<tr><td><img class="kimg" src="glyphs/{gid}.png" alt=""></td><td>{html.escape(desc)}</td>'
        f'<td class="pl">{html.escape(val)}</td><td>{ev}</td></tr>'
        for gid, desc, val, ev in key)


key_rows = rows(KEY)
key2_rows = rows(KEY2)

PAGE = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cipher slip in Tanquerey's Synopsis (1901): decipherment</title>
<style>
  :root {{ --ink:#1d232b; --muted:#5c6670; --line:#d9dee3; --ok:#1f6f43; --cap:#7a3e9d; --hd:#1f5f9a; --weak:#b2561a; --bg:#fbfaf7; }}
  body {{ font: 16px/1.55 Georgia, 'Iowan Old Style', serif; color: var(--ink); background: var(--bg); margin: 0; }}
  main {{ max-width: 1060px; margin: 0 auto; padding: 28px 22px 60px; }}
  h1 {{ font-size: 1.7rem; margin: 0 0 4px; }}
  h2 {{ font-size: 1.25rem; margin: 34px 0 10px; border-bottom: 1px solid var(--line); padding-bottom: 4px; }}
  .sub {{ color: var(--muted); margin: 0 0 18px; font-size: .95rem; }}
  .verdict {{ background: #fff; border: 1px solid var(--line); border-left: 5px solid var(--ok); padding: 16px 20px; border-radius: 6px; }}
  .verdict .pl {{ font-size: 1.45rem; }}
  .verdict .en {{ font-size: 1.1rem; color: var(--muted); }}
  .pl {{ font-family: 'Helvetica Neue', Arial, sans-serif; }}
  .tag {{ display:inline-block; font: 12px/1.6 'Helvetica Neue', Arial, sans-serif; padding: 0 7px; border-radius: 10px; color:#fff; }}
  .tag.ok {{ background: var(--ok); }} .tag.hd {{ background: var(--hd); }} .tag.weak {{ background: var(--weak); }}
  .photos {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }}
  .photos figure {{ margin: 0; background:#fff; border:1px solid var(--line); border-radius:6px; padding:6px; }}
  .photos img {{ width: 100%; display:block; border-radius:4px; }}
  figcaption {{ font-size: .85rem; color: var(--muted); padding: 4px 2px 0; }}
  .strip {{ width:100%; border:1px solid var(--line); border-radius:6px; background:#fff; }}
  .inter {{ background:#fff; border:1px solid var(--line); border-radius:6px; padding: 14px; }}
  .row {{ display:flex; flex-wrap: wrap; gap: 18px 26px; align-items:flex-end; margin: 6px 0 16px; }}
  .word {{ display:flex; gap: 3px; align-items:flex-end; padding: 4px 6px; border-radius: 6px; background: #f4f2ec; }}
  .g {{ display:flex; flex-direction:column; align-items:center; }}
  .g img {{ height: 64px; width:auto; }}
  .g span {{ font: 600 18px/1.3 'Helvetica Neue', Arial, sans-serif; min-width: 14px; text-align:center; }}
  .g.ok span {{ color: var(--ok); }} .g.cap span {{ color: var(--cap); }} .g.hd span {{ color: var(--hd); }}
  .g.weak span {{ color: var(--weak); }} .g.punct span {{ color: var(--muted); }}
  .legend span {{ margin-right: 16px; font: 14px 'Helvetica Neue', Arial, sans-serif; }}
  .g[data-g] img, .g[data-g] span {{ cursor: pointer; border-radius: 4px; transition: background .08s, box-shadow .08s; }}
  .g[data-g] img:focus-visible, .g[data-g] span:focus-visible {{ outline: 2px solid var(--hd); outline-offset: 1px; }}
  .g.hl-g img {{ box-shadow: 0 0 0 3px #e0a100; background: #fff3c4; }}
  .g.hl-g span {{ background: #ffe9a8; }}
  .g.hl-l span {{ background: #cfe3ff; box-shadow: 0 0 0 2px #2f6fd0; }}
  .g.hl-l img {{ box-shadow: 0 0 0 3px #2f6fd0; }}
  .inter.dim .g:not(.hl-g):not(.hl-l) img {{ opacity: .35; }}
  .inter.dim .g:not(.hl-g):not(.hl-l) span {{ opacity: .45; }}
  #hlstatus {{ font: 14px/1.4 'Helvetica Neue', Arial, sans-serif; color: var(--muted); min-height: 1.4em; margin: 0 0 8px; }}
  #hlstatus b {{ color: var(--ink); }}
  #hltip {{ position: fixed; z-index: 50; max-width: 300px; padding: 6px 10px; border-radius: 6px;
           background: #1d232b; color: #fff; font: 13px/1.4 'Helvetica Neue', Arial, sans-serif;
           box-shadow: 0 4px 14px rgba(0,0,0,.25); pointer-events: none; opacity: 0; transition: opacity .1s; }}
  #hltip.on {{ opacity: .96; }}
  #hltip b {{ color: #ffd66b; }}
  table {{ border-collapse: collapse; width: 100%; background:#fff; font-size: .95rem; }}
  th, td {{ border: 1px solid var(--line); padding: 6px 8px; vertical-align: middle; text-align:left; }}
  th {{ background: #f1efe9; font-family: 'Helvetica Neue', Arial, sans-serif; font-size:.85rem; }}
  td.pl {{ font-size: 1.25rem; font-weight: 600; color: var(--ok); white-space: nowrap; }}
  .kimg {{ height: 52px; }}
  .mono {{ font-family: Menlo, Consolas, monospace; font-size: .9em; }}
  .note {{ background:#fff7ec; border:1px solid #f0d9b5; border-radius:6px; padding: 10px 14px; }}
  ul.tight li {{ margin: 3px 0; }}
  .small {{ font-size: .9rem; color: var(--muted); }}
  .funnel td, .funnel th {{ text-align: right; }} .funnel td:first-child, .funnel th:first-child {{ text-align: left; }}
</style>
</head>
<body><main>

<h1>The cipher slip in Tanquerey's <i>Synopsis theologiae dogmaticae</i> (1901)</h1>
<p class="sub">Source: <a href="https://www.reddit.com/r/codes/comments/1y5g8r3/unknown_cipher_on_a_slip_found_in_a_1901_theology/">r/codes: "Unknown cipher on a slip found in a 1901 theology book (Poland)"</a>, posted by u/ColdDivide4423. The slip was found at p. 325 (<i>De Angelis</i>) of A. Tanquerey, <i>Synopsis theologiae dogmaticae</i>, vol. 1, bought from an antiquarian bookshop in Poland.</p>

<div class="verdict">
  <p style="margin:0 0 6px"><span class="tag ok">solved</span> The slip is <b>Polish</b>, written in one home-made substitution alphabet that keeps Polish diacritics:</p>
  <p class="pl" style="margin:4px 0"><b>Komunikacja.</b><br><b>1. Praktyka: Zgodzenie się na wolę Bożą.</b></p>
  <p class="en" style="margin:0 0 10px">"Communication. 1. Practice: consent to God's will."</p>
  <p style="margin:0"><span class="tag ok">high confidence</span> the sentence after the colon. <span class="tag hd">good</span> the title <i>Komunikacja</i>: it is the only fit among 3.2 million Polish word forms. <span class="tag weak">probable</span> the heading <i>Praktyka</i>: it is the only fit, but one glyph is irregular (see <a href="#heads">below</a>).</p>
</div>

<p>Nothing demonic is going on. "Zgodzenie się na wolę Bożą" is a stock phrase of Catholic ascetical writing, about resignation to God's will. The Polish translation of Tanquerey's own ascetical manual uses the near-identical "zdanie się na wolę bożą". It also uses "Praktyka" as an outline heading in exactly this way ("4. Praktyka pokory", "Praktyka umartwienia"). The note has the shape of a seminary or catechesis outline: topic, numbered point, practical application. The reverse side ("1. Powołanie. 2. Katechizmy." = "1. Vocation. 2. Catechisms.") is a numbered list in the same layout. What "Komunikacja" means as a topic is not clear from one line. It could be prayer as communication with God, a catechetics lesson, or even the "communication with spirits" discussed on the very page where the slip sat. The slip itself contains nothing occult.</p>

<h2>The slip</h2>
<div class="photos">
  <figure><img src="note%201.webp" alt="slip in the book at page 325"><figcaption>In situ at p. 325, <i>De Angelis</i>, §115 (magnetism / hypnotism).</figcaption></figure>
  <figure><img src="note%202.webp" alt="cipher side, frontal"><figcaption>Cipher side, frontal photo (used for all glyph crops).</figcaption></figure>
  <figure><img src="note%203.webp" alt="reverse side"><figcaption>Reverse: "1. Powołanie. 2. Katechizmy."</figcaption></figure>
</div>
<p><img class="strip" src="glyphs/strip_note2.png" alt="contrast-enhanced cipher lines"></p>

<h2>Interlinear decipherment</h2>
<p class="legend"><span style="color:var(--ok)">■ sentence key</span><span style="color:var(--cap)">■ capital</span><span style="color:var(--hd)">■ new letters from the title/heading pass</span><span style="color:var(--weak)">■ irregular</span><span style="color:var(--muted)">■ punctuation</span></p>
<p class="small" style="margin:0 0 6px">Hover over or click a <b>glyph</b> to highlight every occurrence of that glyph (amber). Hover over or click a <b>letter</b> to highlight every occurrence of that letter (blue), including letters written with more than one glyph form. A click pins the selection; click it again, or anywhere outside, to clear it. Esc also clears.</p>
<div class="inter" id="inter">
  <p id="hlstatus" aria-live="polite"></p>
  <div class="row">{title_html}</div>
  <div class="row">{line_html}</div>
</div>
<script>
(function () {{
  const box = document.getElementById('inter');
  const cells = Array.from(box.querySelectorAll('.g[data-g]'));
  const status = document.getElementById('hlstatus');
  const tip = document.createElement('div');
  tip.id = 'hltip'; tip.setAttribute('aria-hidden', 'true');
  document.body.appendChild(tip);
  const IDLE = 'Hover or click a glyph or a letter.';
  let pinned = null;            // {{sel:{{mode,key}}, anchor:element}}
  let current = null;           // what is on screen now: {{sel, anchor}}
  function same(a, b) {{ return a && b && a.mode === b.mode && a.key === b.key; }}

  function describe(sel, hits) {{
    const n = hits.length, occ = n + (n === 1 ? ' occurrence' : ' occurrences');
    const pin = pinned && same(pinned.sel, sel) ? ' <i>(pinned)</i>' : '';
    if (sel.mode === 'g') {{
      const letters = Array.from(new Set(hits.map(c => c.dataset.l)));
      return 'Glyph <b>' + hits[0].dataset.desc + '</b> = <b>' + letters.join(' / ') + '</b>: ' + occ + pin;
    }}
    const forms = Array.from(new Set(hits.map(c => c.dataset.desc)));
    return 'Letter <b>' + sel.key + '</b>: ' + occ + ', written with ' + forms.length +
      (forms.length === 1 ? ' glyph form' : ' glyph forms') + ' (' + forms.join('; ') + ')' + pin;
  }}

  // Place the tooltip where it covers no highlighted glyph (and not the hovered one).
  function placeTip(anchor, hits) {{
    const tw = tip.offsetWidth, th = tip.offsetHeight, pad = 6, gap = 12;
    const vw = window.innerWidth, vh = window.innerHeight;
    const avoid = hits.map(c => c.getBoundingClientRect());
    const cell = anchor.closest('.g'), word = anchor.closest('.word'), row = anchor.closest('.row');
    const a = cell.getBoundingClientRect(), w = word.getBoundingClientRect();
    const r = row.getBoundingClientRect(), b = box.getBoundingClientRect();
    const rowEnd = Math.max(...Array.from(row.children).map(x => x.getBoundingClientRect().right));
    const midY = a.top + a.height / 2 - th / 2;
    const cands = [
      [w.right + gap, midY],                 // just right of the hovered word
      [w.left - gap - tw, midY],             // just left of it
      [rowEnd + gap, midY],                  // past the end of the row
      [a.left, r.bottom + 4],                // in the gap below the row
      [a.left, r.top - th - 4],              // in the gap above the row
      [a.left, b.top - th - 8],              // above the whole interlinear box
      [a.left, b.bottom + 8],                // below it
      [w.right + gap, w.bottom + 4],         // diagonal fallbacks
      [w.left - gap - tw, w.top - th - 4],
    ];
    const overlaps = (x, y) => avoid.concat([a]).some(q =>
      x < q.right + pad && x + tw > q.left - pad && y < q.bottom + pad && y + th > q.top - pad);
    const fits = (x, y) => x >= 4 && y >= 4 && x + tw <= vw - 4 && y + th <= vh - 4;
    let pos = null;
    for (const [x0, y0] of cands) {{
      const x = Math.min(Math.max(x0, 4), vw - tw - 4);   // slide horizontally into view
      if (fits(x, y0) && !overlaps(x, y0)) {{ pos = [x, y0]; break; }}
    }}
    if (!pos) pos = [vw - tw - 12, 12];                   // last resort: top-right corner
    tip.style.left = pos[0] + 'px'; tip.style.top = pos[1] + 'px';
  }}

  function show(state) {{
    current = state;
    cells.forEach(c => c.classList.remove('hl-g', 'hl-l'));
    if (!state) {{
      box.classList.remove('dim'); status.textContent = IDLE; tip.classList.remove('on'); return;
    }}
    const sel = state.sel, attr = sel.mode === 'g' ? 'g' : 'l';
    const hits = cells.filter(c => c.dataset[attr] === sel.key);
    hits.forEach(c => c.classList.add(sel.mode === 'g' ? 'hl-g' : 'hl-l'));
    box.classList.add('dim');
    const text = describe(sel, hits);
    status.innerHTML = text;
    tip.innerHTML = text;
    tip.classList.add('on');
    placeTip(state.anchor, hits);
  }}
  function selFor(el) {{
    const cell = el.closest('.g[data-g]');
    return el.tagName === 'IMG' ? {{mode: 'g', key: cell.dataset.g}} : {{mode: 'l', key: cell.dataset.l}};
  }}
  cells.forEach(cell => {{
    [cell.querySelector('img'), cell.querySelector('span')].forEach(el => {{
      el.addEventListener('mouseenter', () => show({{sel: selFor(el), anchor: el}}));
      el.addEventListener('mouseleave', () => show(pinned));
      el.addEventListener('focus', () => show({{sel: selFor(el), anchor: el}}));
      el.addEventListener('blur', () => show(pinned));
      const toggle = (ev) => {{
        ev.stopPropagation();
        const s = selFor(el);
        pinned = pinned && same(pinned.sel, s) ? null : {{sel: s, anchor: el}};
        show(pinned || {{sel: s, anchor: el}});
      }};
      el.addEventListener('click', toggle);
      el.addEventListener('keydown', ev => {{ if (ev.key === 'Enter' || ev.key === ' ') {{ ev.preventDefault(); toggle(ev); }} }});
    }});
  }});
  document.addEventListener('click', () => {{ if (pinned) {{ pinned = null; show(null); }} }});
  document.addEventListener('keydown', ev => {{ if (ev.key === 'Escape') {{ pinned = null; show(null); }} }});
  const reflow = () => {{ if (current) show(current); }};
  window.addEventListener('scroll', reflow, {{passive: true}});
  window.addEventListener('resize', reflow);
  show(null);
}})();
</script>

<h2>The key</h2>
<h3 style="font-size:1.05rem;margin:14px 0 6px">From the sentence (thin pen)</h3>
<p>Two features made the system crackable. Polish diacritics are added on top of the cipher letter: e&rarr;ę and a&rarr;ą get a zig-zag ogonek, and z&rarr;ż gets a dot above. Capitals appear where Polish orthography wants them: <i>Z</i>godzenie, <i>B</i>ożą, and the first letters of the title and heading.</p>
<table>
<tr><th>glyph</th><th>description</th><th>Polish</th><th>evidence</th></tr>
{key_rows}
</table>
<h3 style="font-size:1.05rem;margin:18px 0 6px">Added by the title and heading (bold pen)</h3>
<p>None of these letters occurs in the sentence (k, m, u, c, j, p, r, t, y). Nothing contradicts the sentence key, so this is one alphabet written with a heavier pen, not a second cipher. Several glyphs are visibly flipped Latin letters: ⊥ = t, ʎ = y, b = P, and V/Λ = u/n.</p>
<table>
<tr><th>glyph</th><th>description</th><th>Polish</th><th>evidence</th></tr>
{key2_rows}
</table>

<h2>How it was cracked</h2>
<ol>
  <li><b>Known scripts first.</b> I compared the glyphs against Glagolitic, Phoenician/Paleo-Hebrew, Old Italic, Old Hungarian, Coptic and Gothic, and against Greek, Cyrillic and Hebrew letter shapes. A few shapes overlap by chance (Λ, ∆, θ), but no script accounts for the set. It is an invented alphabet.</li>
  <li><b>A test that failed usefully.</b> My first transcription treated the mid-dots as punctuation, merged the two "foot" glyphs, and treated the two oval glyphs as unrelated. I then asked whether any one-glyph-one-letter reading turned every word into a dictionary word. I tried Polish, Tanquerey's Latin, German, French, Italian and English. <b>Zero</b> full-line solutions came back in every language. That pointed to a wrong transcription model, not a hopeless text.</li>
  <li><b>The diacritic clue.</b> Two glyphs have a zig-zag hook hanging below the line. One is the short stroke that ends a 9-glyph word twice. The other is the square that ends the line. A hook under a vowel is a Polish <i>ogonek</i>, so stroke/stroke+hook = e/ę and square/square+hook = a/ą. A 3-glyph word ends in the hooked stroke (ę), and its middle glyph S also appears in the 9-glyph word's ending. That makes it <b>się</b>, with S = i. The next 2-glyph word, sharing the Λ, becomes <b>na</b>. That gives the very common Polish frame <i>"…enie się na …"</i>.</li>
  <li><b>The dot is a letter.</b> Read as <i>o</i>, the dot completes <b>wolę</b> and the idiom <i>na wolę Bożą</i>. The last word is then <b>Bożą</b>: capital B, o, a z-oval <i>with a dot above</i> (ż), and the hooked square (ą).</li>
  <li><b>Separating d from l.</b> <i>Wolę</i> and the 9-glyph word seemed to need the same glyph for both <i>l</i> and <i>d</i>. At high zoom they differ: the <i>l</i> glyph has a flat foot, and the <i>d</i> glyph has an up-turned bowl. The 9-glyph word is then <b>Zgodzenie</b>. Its first and fifth glyphs are both z-ovals, the first larger as a capital. The √ glyph cannot be <i>w</i> (‡ already is), so it is <i>g</i>.</li>
  <li><b>Checking uniqueness of the sentence.</b> I took the final glyph model and searched a ~70,000-form Polish list. It gives 377 word-consistent readings of the five words. <i>"…enie się na wolę Bożą"</i> ranks in the top five by plain word frequency, and it is the only idiomatic one; the rest are word salad such as <i>"chodzenie się na mogę bożą"</i>.</li>
  <li><b>Title and heading (second pass).</b> See the next section.</li>
</ol>

<h2 id="heads">Second pass: the title and the heading word</h2>
<p>The first pass read the title as a roman numeral "I." followed by 9 unknown glyphs. That segmentation was wrong. The big decorated <b>I</b> is the same serifed Ɪ glyph that recurs at title position 7 and in the heading word, just enlarged as an initial. The dot after it is the <b>o</b>-dot from the sentence key. So the title is one 11-glyph word:</p>
<p class="mono" style="font-size:1rem">Ɪ · N* V Λ̶ S Ɪ ▫ ~ 4 ▫ &nbsp;&rarr;&nbsp; X o ? ? n i X a ? ? a</p>
<p>The positions pinned by the sentence key are o, i, a…a, and n (the title's arch is the sentence's Λ = n with a cross-stroke). Together with the repeat of Ɪ at positions 1 and 7, they leave a single Polish word. Funnel over the full SJP word list (3.2 million inflected forms):</p>
<table class="funnel" style="max-width:640px">
<tr><th>constraint (11-letter forms)</th><th>forms left</th></tr>
<tr><td>all 11-letter forms</td><td>448,640</td></tr>
<tr><td>repeat pattern (Ɪ at 1 &amp; 7, square at 8 &amp; 11, the rest distinct)</td><td>197</td></tr>
<tr><td>+ dot = o, S = i, square = a</td><td>3 (kodyfikacja, komplikacja, komunikacja)</td></tr>
<tr><td>+ arch = n</td><td><b>1: komunikacja</b></td></tr>
</table>
<p style="margin-top:12px">That fixes Ɪ = k, N* = m, V = u, ~ = c and the footed 4 = j. None of these letters occurs in the decoded sentence, so nothing conflicts. The heading word (8 glyphs) becomes:</p>
<p class="mono" style="font-size:1rem">b r ▫ Ɪ ⊥ 4· ■ ▫ &nbsp;&rarr;&nbsp; ? ? a k ? ? ? a</p>
<p>There are 216,448 eight-letter forms in the list; 44 have the shape <i>??ak???a</i>. Require the four still-unknown glyphs (b, r, ⊥, dotted 4) to be four different letters not already in the key. Exactly one form survives: <b>praktyka</b>. It reads P (a flipped P), r, a, k, t (an upside-down T), y (an upside-down y), and a final a. The cost is glyph 7, the dark blob. "Praktyka" needs a second <i>k</i> there, but the blob does not look like the Ɪ used for k. It may be a blotted or variant k. Without it there is no Polish word at all, and allowing the blob to be any letter already in the key still gives only <i>praktyka</i>.</p>

<div class="note">
  <b>Caveats.</b> All glyph crops come from one ~1080-px phone photo. The <i>g</i> (√) rests on elimination, not on a second occurrence. The capitals Z, B, K and P are each seen once. Title: <i>Komunikacja</i> needs the arch-with-cross-stroke to be the same letter as Λ. That is a shape argument, but without it the only candidates are the two technical terms <i>kodyfikacja</i> and <i>komplikacja</i>. Heading: <i>Praktyka</i> needs the irregular blob = k. The sentence is idiomatic and fits every glyph. The topical interpretation of "Komunikacja" is open.
</div>

<h2>Ruled out along the way</h2>
<ul class="tight">
  <li>Known historical scripts: Glagolitic, Phoenician/Paleo-Hebrew, Old Italic, Old Hungarian (rovás), Coptic, Gothic, and Greek/Cyrillic/Hebrew transliteration.</li>
  <li>Mirror writing, 180° rotation, and 90° rotation of the line.</li>
  <li>Latin-letter-literal readings, e.g. the title as "INVASIO(NE)…": they don't extend across words.</li>
  <li>Plain one-glyph-one-letter substitution with dots as punctuation, in Polish, Latin, German, French, Italian and English: zero consistent full-line solutions.</li>
  <li>Title as roman numeral "I." + 9-glyph word, or "I." + an o-word: no meaningful Polish or Latin fit.</li>
</ul>

<h2>Sources and tools</h2>
<ul class="tight small">
  <li>Reddit thread (images and OP's description): <a href="https://www.reddit.com/r/codes/comments/1y5g8r3/unknown_cipher_on_a_slip_found_in_a_1901_theology/">r/codes 1y5g8r3</a>, u/ColdDivide4423. The comments could not be fetched from here.</li>
  <li>A. Tanquerey, <i>Zarys teologji ascetycznej i mistycznej</i>, t. 2 (Polish tr., 1949), OCR text at <a href="https://archive.org/details/Tanquerey.Zarys2">archive.org/details/Tanquerey.Zarys2</a>: "zdanie się na wolę bożą", "zgodzeniu się na działanie Boga", "Praktyka pokory", "Praktyka umartwienia".</li>
  <li>Tanquerey's Latin <i>Synopsis</i> OCR texts used as a Latin test vocabulary: <a href="https://archive.org/details/synopsistheolog00tanqgoog">synopsistheolog00tanqgoog</a> (1896, incl. <i>De magia, magnetismo, spiritismo</i>), <a href="https://archive.org/details/synopsistheologi00tanq">synopsistheologi00tanq</a>, <a href="https://archive.org/details/synopsistheolog03tanq">synopsistheolog03tanq</a>.</li>
  <li>Polish word lists: <a href="https://sjp.pl/sl/growy/">SJP "słownik do gier"</a> (3.2M inflected forms, Nov 2026) and <a href="https://github.com/hermitdave/FrequencyWords">hermitdave/FrequencyWords</a> (2018, 50k, also used for the other languages).</li>
  <li>Scripts in <span class="mono">work/</span>: <span class="mono">linesearch.py</span>, <span class="mono">sub*.py</span> (pattern searches), <span class="mono">uniq_check.py</span> (sentence uniqueness), <span class="mono">title_search.py</span> and <span class="mono">title_counts.py</span> (title/heading funnel), <span class="mono">make_glyphs.py</span> (crops), <span class="mono">build_report.py</span> (this page). The word lists were downloaded to a temporary folder and are not stored here.</li>
</ul>
</main></body></html>
"""

with open('../index.html', 'w', encoding='utf-8') as f:
    f.write(PAGE)
print('wrote ../index.html')
