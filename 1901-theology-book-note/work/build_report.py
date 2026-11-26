"""Build ../index.html: report on the cipher slip found in Tanquerey's Synopsis (r/codes 1y5g8r3)."""
import html

# ---- interlinear data: (glyph-crop id, plaintext letter, css class) ----
# class: 'ok' decoded, 'cap' decoded capital, 'unk' unread (bold heading set), 'punct'
TITLE = [('t0', 'I.', 'punct'), ('t1', '?', 'unk'), ('t2', '?', 'unk'), ('t3', '?', 'unk'), ('t4', '?', 'unk'),
         ('t5', '?', 'unk'), ('t6', '?', 'unk'), ('t7', '?', 'unk'), ('t8', '?', 'unk'), ('t9', '? ,', 'unk')]
LINE = [
    [('n1', '1.', 'punct')],
    [('w1_1', '?', 'unk'), ('w1_2', '?', 'unk'), ('w1_3', '?', 'unk'), ('w1_4', '?', 'unk'),
     ('w1_5', '?', 'unk'), ('w1_6', '?', 'unk'), ('w1_7', '?', 'unk'), ('w1_8', '?', 'unk'), ('colon', ':', 'punct')],
    [('w2_1', 'Z', 'cap'), ('w2_2', 'g', 'ok'), ('w2_3', 'o', 'ok'), ('w2_4', 'd', 'ok'), ('w2_5', 'z', 'ok'),
     ('w2_6', 'e', 'ok'), ('w2_7', 'n', 'ok'), ('w2_8', 'i', 'ok'), ('w2_9', 'e', 'ok')],
    [('w3_1', 's', 'ok'), ('w3_2', 'i', 'ok'), ('w3_3', 'ę', 'ok')],
    [('w4_1', 'n', 'ok'), ('w4_2', 'a', 'ok')],
    [('w5_1', 'w', 'ok'), ('w5_2', 'o', 'ok'), ('w5_3', 'l', 'ok'), ('w5_4', 'ę', 'ok')],
    [('w6_1', 'B', 'cap'), ('w6_2', 'o', 'ok'), ('w6_3', 'ż', 'ok'), ('w6_4', 'ą', 'ok'), ('stop', '.', 'punct')],
]

# ---- key table ----
KEY = [
    ('w2_3', 'small mid-height dot', 'o', 'Appears 3&times; inside words, always where Polish needs <i>o</i> (zg<b>o</b>dzenie, w<b>o</b>lę, B<b>o</b>żą). My first pass took it for punctuation, and that one mistake hid the whole solution.'),
    ('w2_6', 'short slanted stroke (like a dotless ı)', 'e', 'Ends the 9-glyph word twice (…<b>e</b>ni<b>e</b>).'),
    ('w3_3', 'the same stroke + zigzag hook below', 'ę', 'The hook is a Polish <b>ogonek</b>. The cipher keeps diacritics: e&rarr;ę is drawn as cipher-e + hook.'),
    ('w4_2', 'small square (heavily inked here)', 'a', '<i>na</i>; the same square with a hook ends the line as <i>ą</i>.'),
    ('w6_4', 'square + zigzag hook below', 'ą', 'Second ogonek glyph. It pairs with the square = a, as the stroke pairs with e/ę.'),
    ('w2_7', 'Λ (pointed arch)', 'n', '…e<b>n</b>ie and <b>n</b>a.'),
    ('w2_8', 'S', 'i', '…en<b>i</b>e and s<b>i</b>ę: same glyph, same letter.'),
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

UNREAD_T = 'I. [N*] [V] [A] [S] [Ɪ] [▫] [~] [4] [▫] ,'
UNREAD_W = '1. [b] [r] [▫] [Ɪ] [⊥] [4] [■] [▫] :'


def glyph_cell(gid, letter, cls):
    return (f'<div class="g {cls}"><img src="glyphs/{gid}.png" alt="glyph {gid}">'
            f'<span>{html.escape(letter)}</span></div>')


def words_html(words):
    out = []
    for w in words:
        out.append('<div class="word">' + ''.join(glyph_cell(*g) for g in w) + '</div>')
    return '\n'.join(out)


title_html = '<div class="word">' + ''.join(glyph_cell(*g) for g in TITLE) + '</div>'
line_html = words_html(LINE)

key_rows = '\n'.join(
    f'<tr><td><img class="kimg" src="glyphs/{gid}.png" alt=""></td><td>{html.escape(desc)}</td>'
    f'<td class="pl">{html.escape(val)}</td><td>{ev}</td></tr>'
    for gid, desc, val, ev in KEY)

PAGE = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cipher slip in Tanquerey's Synopsis (1901): decipherment</title>
<style>
  :root {{ --ink:#1d232b; --muted:#5c6670; --line:#d9dee3; --ok:#1f6f43; --cap:#7a3e9d; --unk:#b2561a; --bg:#fbfaf7; }}
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
  .tag.ok {{ background: var(--ok); }} .tag.unk {{ background: var(--unk); }}
  .photos {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }}
  .photos figure {{ margin: 0; background:#fff; border:1px solid var(--line); border-radius:6px; padding:6px; }}
  .photos img {{ width: 100%; display:block; border-radius:4px; }}
  figcaption {{ font-size: .85rem; color: var(--muted); padding: 4px 2px 0; }}
  .strip {{ width:100%; border:1px solid var(--line); border-radius:6px; background:#fff; }}
  .inter {{ background:#fff; border:1px solid var(--line); border-radius:6px; padding: 14px; }}
  .row {{ display:flex; flex-wrap: wrap; gap: 18px 26px; align-items:flex-end; margin: 6px 0 16px; }}
  .word {{ display:flex; gap: 3px; align-items:flex-end; padding: 4px 6px; border-radius: 6px; background: #f4f2ec; }}
  .g {{ display:flex; flex-direction:column; align-items:center; }}
  .g img {{ height: 64px; width:auto; image-rendering: auto; }}
  .g span {{ font: 600 18px/1.3 'Helvetica Neue', Arial, sans-serif; min-width: 14px; text-align:center; }}
  .g.ok span {{ color: var(--ok); }} .g.cap span {{ color: var(--cap); }} .g.unk span {{ color: var(--unk); }} .g.punct span {{ color: var(--muted); }}
  .legend span {{ margin-right: 16px; font: 14px 'Helvetica Neue', Arial, sans-serif; }}
  table {{ border-collapse: collapse; width: 100%; background:#fff; font-size: .95rem; }}
  th, td {{ border: 1px solid var(--line); padding: 6px 8px; vertical-align: middle; text-align:left; }}
  th {{ background: #f1efe9; font-family: 'Helvetica Neue', Arial, sans-serif; font-size:.85rem; }}
  td.pl {{ font-size: 1.25rem; font-weight: 600; color: var(--ok); white-space: nowrap; }}
  .kimg {{ height: 52px; }}
  code, .mono {{ font-family: Menlo, Consolas, monospace; font-size: .9em; }}
  .note {{ background:#fff7ec; border:1px solid #f0d9b5; border-radius:6px; padding: 10px 14px; }}
  ul.tight li {{ margin: 3px 0; }}
  .small {{ font-size: .9rem; color: var(--muted); }}
</style>
</head>
<body><main>

<h1>The cipher slip in Tanquerey's <i>Synopsis theologiae dogmaticae</i> (1901)</h1>
<p class="sub">Source: <a href="https://www.reddit.com/r/codes/comments/1y5g8r3/unknown_cipher_on_a_slip_found_in_a_1901_theology/">r/codes: "Unknown cipher on a slip found in a 1901 theology book (Poland)"</a>, posted by u/ColdDivide4423. The slip was found at p. 325 (<i>De Angelis</i>) of A. Tanquerey, <i>Synopsis theologiae dogmaticae</i>, vol. 1, bought from an antiquarian bookshop in Poland.</p>

<div class="verdict">
  <p style="margin:0 0 6px"><span class="tag ok">solved</span> The sentence after the colon is <b>Polish</b>, written in a home-made substitution alphabet that keeps Polish diacritics:</p>
  <p class="pl" style="margin:4px 0">1. <span style="color:var(--unk)">[heading]</span>: <b>Zgodzenie się na wolę Bożą.</b></p>
  <p class="en" style="margin:0 0 10px">"1. [heading]: Consent to God's will." (literally "agreeing to the will of God")</p>
  <p style="margin:0"><span class="tag unk">unread</span> The title (<span class="mono">I. ………</span>) and the heading word before the colon are in a separate, heavier "capital" glyph set. That set shares no letters with the solved sentence, and 17 glyphs are too few to break it on their own. Both are still unread (see <a href="#unread">below</a>).</p>
</div>

<p>Nothing demonic is going on. "Zgodzenie się na wolę Bożą" is a stock phrase of Catholic ascetical writing, about resignation to God's will. The Polish translation of Tanquerey's own ascetical manual uses the near-identical "zdanie się na wolę bożą". The slip probably landed on the page about magnetism and spiritism by chance, as a bookmark. The reverse side ("1. Powołanie. 2. Katechizmy." = "1. Vocation. 2. Catechisms.") is a numbered list in the same layout. That fits a seminarian's or priest's study or sermon notes. Consenting to God's will is the classic "human side" of a vocation. That link is suggestive but unproven.</p>

<h2>The slip</h2>
<div class="photos">
  <figure><img src="note%201.webp" alt="slip in the book at page 325"><figcaption>In situ at p. 325, <i>De Angelis</i>, §115 (magnetism / hypnotism).</figcaption></figure>
  <figure><img src="note%202.webp" alt="cipher side, frontal"><figcaption>Cipher side, frontal photo (used for all glyph crops).</figcaption></figure>
  <figure><img src="note%203.webp" alt="reverse side"><figcaption>Reverse: "1. Powołanie. 2. Katechizmy."</figcaption></figure>
</div>
<p><img class="strip" src="glyphs/strip_note2.png" alt="contrast-enhanced cipher lines"></p>

<h2>Interlinear decipherment</h2>
<p class="legend"><span style="color:var(--ok)">■ decoded</span><span style="color:var(--cap)">■ decoded capital</span><span style="color:var(--unk)">■ unread (heading glyph set)</span><span style="color:var(--muted)">■ punctuation</span></p>
<div class="inter">
  <div class="row">{title_html}</div>
  <div class="row">{line_html}</div>
</div>

<h2>The key (thin-pen alphabet)</h2>
<p>Sixteen glyph types are read. Two features made the system crackable. Polish diacritics are added on top of the cipher letter: e&rarr;ę and a&rarr;ą get a zig-zag ogonek, and z&rarr;ż gets a dot above. Capitals appear exactly where Polish orthography wants them: the first word after the colon, and <i>Bożą</i>.</p>
<table>
<tr><th>glyph</th><th>description</th><th>Polish</th><th>evidence</th></tr>
{key_rows}
</table>

<h2>How it was cracked</h2>
<ol>
  <li><b>Known scripts first.</b> I compared the glyphs against Glagolitic, Phoenician/Paleo-Hebrew, Old Italic, Old Hungarian, Coptic and Gothic, and against Greek, Cyrillic and Hebrew letter shapes. A few shapes overlap by chance (Λ, ∆, θ), but no script accounts for the set. It is an invented alphabet.</li>
  <li><b>A test that failed usefully.</b> My first transcription treated the mid-dots as punctuation, merged the two "foot" glyphs into one, and treated the two oval glyphs as unrelated. I then asked whether any one-glyph-one-letter reading turned every word into a dictionary word. I tried Polish (a 50k-word frequency list plus the vocabulary of the Polish Tanquerey), Tanquerey's Latin, and German, French, Italian and English. <b>Zero</b> full-line solutions came back in every language. That pointed to a wrong transcription model, not to a hopeless text.</li>
  <li><b>The diacritic clue.</b> Two glyphs have a zig-zag hook hanging below the line. One is the short stroke that ends a 9-glyph word twice. The other is the square that ends the line. A hook under a vowel is a Polish <i>ogonek</i>, so stroke/stroke+hook = e/ę and square/square+hook = a/ą. A 3-glyph word ends in the hooked stroke (ę), and its middle glyph S also appears in the 9-glyph word's ending. That makes it <b>się</b>, with S = i. The next 2-glyph word, sharing the Λ, becomes <b>na</b>. That gives the very common Polish frame <i>"…enie się na …"</i>.</li>
  <li><b>The dot is a letter.</b> Read as <i>o</i>, the dot completes <b>wolę</b> (4 glyphs ending in the ę-glyph) and the familiar idiom <i>na wolę Bożą</i>. The last word then has to be <b>Bożą</b>: capital B, o, a z-oval <i>with a dot above</i> (ż), and the hooked square (ą).</li>
  <li><b>Separating d from l.</b> <i>Wolę</i> and the 9-glyph word seemed to need the same glyph for both <i>l</i> and <i>d</i>. At high zoom they differ: the <i>l</i> glyph has a flat foot, and the <i>d</i> glyph has an up-turned bowl. With that settled, the 9-glyph word is <b>Zgodzenie</b>. Its first and fifth glyphs are both z-ovals (the first one larger and decorated, as a capital). The √ glyph cannot be <i>w</i>, because ‡ already is, so it is <i>g</i>.</li>
  <li><b>Checking uniqueness.</b> I took the final glyph model (shared glyphs, e/ę, a/ą and z/ż pairings, capitals allowed to repeat a lower-case letter). A dictionary search over a ~70,000-form Polish list gives 377 word-consistent readings of the five words. Ranked by plain word frequency, <i>"…enie się na wolę Bożą"</i> is already in the top five, and it is the only one that is idiomatic. (The rest are word salad such as <i>"chodzenie się na mogę bożą"</i>.) The frequency list happens to lack "zgodzenie" itself. The Polish Tanquerey has "zgodzeniem się … na" and "zgodzeniu się na działanie Boga".</li>
</ol>

<h2 id="unread">What is still unread: the title and the heading word</h2>
<p>The title and the word before the colon are written larger, with a heavier pen. Their glyphs are a different set: they share three glyphs with each other (the dotted square, the serifed Ɪ, and the "4"-like glyph) but almost nothing with the solved sentence.</p>
<ul class="tight">
  <li><b>Title</b> (after "I."): <span class="mono">{html.escape(UNREAD_T)}</span>. Nine glyphs, or eight if the small tilde is a flourish or accent. The dotted square repeats in positions 6 and 9.</li>
  <li><b>Heading</b>: <span class="mono">{html.escape(UNREAD_W)}</span>. Eight glyphs, with the dotted square in positions 3 and 8.</li>
  <li>Reading them with the thin-pen key (S=i, square=a, …) gives nothing Polish. I also solved them as their own small substitution against Polish and Latin word lists, and no meaningful pair fits. The only pairs that survive are random, e.g. <i>trzymania / kłamliwa</i>. Single-word fits like <i>Medytacja</i> (title) or <i>Pierwsze</i>, <i>Probatio</i> (heading) are pattern coincidences. They do not survive the shared-glyph constraints.</li>
  <li>So the bold set is most likely a separate capital alphabet. Reading it needs more text in the same hand: other slips or margin notes from the same book, if the OP has any.</li>
</ul>

<div class="note">
  <b>Caveats.</b> All glyph crops come from one ~1080-px phone photo. The reading of glyph w2_2 as <i>g</i> rests on elimination, not on a second occurrence. The capital Z and capital B are each seen once. The Polish sentence itself is idiomatic and fits every glyph, so I'm confident in it. The "vocation" interpretation of the whole slip is a guess based on the reverse side.
</div>

<h2>Ruled out along the way</h2>
<ul class="tight">
  <li>Known historical scripts: Glagolitic, Phoenician/Paleo-Hebrew, Old Italic, Old Hungarian (rovás), Coptic, Gothic, and Greek/Cyrillic/Hebrew transliteration.</li>
  <li>Mirror writing, 180° rotation, and 90° rotation of the line.</li>
  <li>Latin-letter-literal readings, e.g. the title as "INVASIO(NE)…": they don't extend across words.</li>
  <li>Plain one-glyph-one-letter substitution with dots as punctuation, in Polish, Latin, German, French, Italian and English: zero consistent full-line solutions.</li>
  <li>Latin plaintext for the thin-pen sentence: <i>exorcismi</i> fits W2's pattern but nothing else follows from it.</li>
</ul>

<h2>Sources and tools</h2>
<ul class="tight small">
  <li>Reddit thread (images and OP's description): <a href="https://www.reddit.com/r/codes/comments/1y5g8r3/unknown_cipher_on_a_slip_found_in_a_1901_theology/">r/codes 1y5g8r3</a>, u/ColdDivide4423. The comments could not be fetched from here.</li>
  <li>A. Tanquerey, <i>Zarys teologji ascetycznej i mistycznej</i>, t. 2 (Polish tr., 1949), OCR text at <a href="https://archive.org/details/Tanquerey.Zarys2">archive.org/details/Tanquerey.Zarys2</a>: "zdania się na wolę bożą", "zdanie się na wolę bożą", "zgodzeniu się na działanie Boga".</li>
  <li>Tanquerey's Latin <i>Synopsis</i> OCR texts used as a Latin test vocabulary: <a href="https://archive.org/details/synopsistheolog00tanqgoog">synopsistheolog00tanqgoog</a> (1896, incl. <i>De magia, magnetismo, spiritismo</i>), <a href="https://archive.org/details/synopsistheologi00tanq">synopsistheologi00tanq</a>, <a href="https://archive.org/details/synopsistheolog03tanq">synopsistheolog03tanq</a>.</li>
  <li>Polish and other word-frequency lists: <a href="https://github.com/hermitdave/FrequencyWords">hermitdave/FrequencyWords</a> (2018, 50k).</li>
  <li>Scripts: <span class="mono">work/linesearch.py</span>, <span class="mono">work/sub*.py</span> (pattern searches), <span class="mono">work/uniq_check.py</span> (uniqueness count), <span class="mono">work/make_glyphs.py</span> (crops), <span class="mono">work/build_report.py</span> (this page).</li>
</ul>
</main></body></html>
"""

with open('../index.html', 'w', encoding='utf-8') as f:
    f.write(PAGE)
print('wrote ../index.html')
