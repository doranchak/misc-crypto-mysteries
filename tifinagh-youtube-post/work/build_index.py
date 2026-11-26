"""Build ../index.html for the Tifinagh YouTube community post (r/codes 1xm43zd).

Run:  /opt/homebrew/bin/python3.11 -I work/build_index.py   (from the folder above)
Input: work/post_text.txt  (raw Unicode text of the post, fetched from YouTube)
"""
import html, unicodedata, collections, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
TEXT = (HERE / "post_text.txt").read_text(encoding="utf-8").strip()

# Standard Kabyle Latin value of each Neo-Tifinagh letter that occurs in the post.
LAT = {
    "ⴰ": "a", "ⴱ": "b", "ⴳ": "g", "ⴵ": "ǧ", "ⴷ": "d", "ⴹ": "ḍ", "ⴻ": "e", "ⴼ": "f",
    "ⴽ": "k", "ⵃ": "ḥ", "ⵅ": "x", "ⵉ": "i", "ⵍ": "l", "ⵎ": "m", "ⵏ": "n", "ⵓ": "u",
    "ⵔ": "r", "ⵖ": "ɣ", "ⵙ": "s", "ⵛ": "c", "ⵜ": "t", "ⵟ": "ṭ", "ⵡ": "w", "ⵢ": "y",
}
SOUND = {
    "ǧ": "j as in <i>jam</i>", "ḍ": "emphatic d", "e": "schwa (short ‘uh’)", "ḥ": "pharyngeal h",
    "x": "kh as in <i>Bach</i>", "ɣ": "gh (French r)", "c": "sh", "ṭ": "emphatic t",
}

def translit(s):
    return "".join(LAT.get(ch, ch) for ch in s)

# Word-by-word gloss: (Tifinagh, gloss, grammar note)
WORDS = [
    ("ⵃⴱⴻⵙ,", "stop!", "imperative of <i>ḥbes</i> ‘stop, halt’"),
    ("ⵓⵔ", "not", "<i>ur</i>: first half of the negation <i>ur … ara</i>"),
    ("ⵉⵢⵉⴷ-ⵜⴻⵙⵙⴻⴽⵛⴻⵎ", "bring me in", "<i>iyi</i> ‘me’ + <i>d</i> ‘toward here’ + <i>tessekcem</i>, from <i>sekcem</i> ‘make enter’ (causative of <i>kcem</i> ‘enter’)"),
    ("ⴰⵔⴰ;", "(not)", "<i>ara</i>: second half of the negation"),
    ("ⴻⴵⴵ", "leave, let", "imperative of <i>eǧǧ</i> ‘leave, let be’"),
    ("ⵉⵎⴷⴰⵏⴻⵏ", "people", "plural of <i>amdan</i> ‘human being’"),
    ("ⵢⴻⵎⵎⵓⵜⴻⵏ", "who died", "participle of <i>mmet</i> ‘die’ (cf. <i>yemmut</i> ‘he died’)"),
    ("ⴰⴷ", "(will / so that)", "particle before the aorist"),
    ("ⵙⴳⵓⵏⴼⵓⵏ", "they rest", "<i>sgunfu</i> ‘rest’, 3rd person plural"),
    ("ⴷⵉ", "in", "preposition"),
    ("ⵜⴰⵍⵡⵉⵜ", "peace", "<i>talwit</i>"),
    ("—", "", ""),
    ("ⴰⵅⴰⵟⴻⵔ", "because", "<i>axaṭer</i>"),
    ("ⵓⵔ", "not", "<i>ur … ara</i> again"),
    ("ⵜⴻⴱⵖⵉⴹ", "you want", "<i>bɣu</i> ‘want’, 2nd person singular <i>t-…-ḍ</i>"),
    ("ⴰⵔⴰ", "(not)", ""),
    ("ⵜⵉⵔⴳⴰ", "dreams", "plural of <i>targit</i> ‘dream’"),
    ("ⵏ", "of", "genitive particle"),
    ("ⵢⵉⴹ,", "night", "<i>iḍ</i> ‘night’ (form <i>yiḍ</i> after <i>n</i>)"),
    ("ⵢⴻⵔⵏⴰ", "and also", "<i>yerna</i> ‘moreover, and besides’"),
    ("ⵜⴻⴱⵖⵉⴹ", "you want", ""),
    ("ⴰⴷ", "to", ""),
    ("ⵜⴻⵟⵟⵙⴻⴹ", "you sleep", "<i>eṭṭes</i> ‘sleep’, 2nd person singular aorist"),
]
assert " ".join(w for w, _, _ in WORDS) == TEXT, "gloss words do not reproduce the post text"

letters = [ch for ch in TEXT if "ⴰ" <= ch <= "⵿"]
counts = collections.Counter(letters)
assert set(counts) == set(LAT), set(counts) ^ set(LAT)
N = len(letters)
_top = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
assert _top[0][0] == "ⴻ"
RUNNERS = ", ".join(f"{c} <i>{LAT[c]}</i> ({n})" for c, n in _top[1:6])
TR = translit(TEXT)
TR = TR[0].upper() + TR[1:]

def esc(s):
    return html.escape(s, quote=False)

# ---------- HTML pieces ----------
word_cards = []
for w, gloss, note in WORDS:
    if w == "—":
        word_cards.append('<div class="wc dash"><div class="tf">—</div></div>')
        continue
    word_cards.append(
        f'<div class="wc"><div class="tf">{esc(w)}</div>'
        f'<div class="lt">{esc(translit(w))}</div>'
        f'<div class="gl">{esc(gloss)}</div></div>')

gloss_rows = []
for i, (w, gloss, note) in enumerate(WORDS, 1):
    if w == "—":
        continue
    gloss_rows.append(
        f"<tr><td class='tf'>{esc(w.strip(',;'))}</td><td class='lt'>{esc(translit(w.strip(',;')))}</td>"
        f"<td>{esc(gloss)}</td><td class='nt'>{note}</td></tr>")

key_rows = []
for ch, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
    name = unicodedata.name(ch).replace("TIFINAGH LETTER ", "")
    lat = LAT[ch]
    snd = SOUND.get(lat, "")
    key_rows.append(
        f"<tr><td class='tf big'>{ch}</td><td><code>U+{ord(ch):04X}</code></td><td class='sm'>{name}</td>"
        f"<td class='lt'>{lat}</td><td class='sm'>{snd}</td><td class='num'>{n}</td>"
        f"<td><span class='bar' style='width:{n / counts.most_common(1)[0][1] * 90:.0f}px'></span></td></tr>")

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tifinagh YouTube post (@Soul09-t4e): Kabyle, not a cipher</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Tifinagh&display=swap" rel="stylesheet">
<style>
  :root {{ --ink:#1d232b; --muted:#5c6670; --line:#d9dee3; --ok:#1f6f43; --hd:#1f5f9a; --weak:#b2561a; --bg:#fbfaf7; }}
  body {{ font: 16px/1.55 Georgia, 'Iowan Old Style', serif; color: var(--ink); background: var(--bg); margin: 0; }}
  main {{ max-width: 1060px; margin: 0 auto; padding: 28px 22px 60px; }}
  h1 {{ font-size: 1.7rem; margin: 0 0 4px; }}
  h2 {{ font-size: 1.25rem; margin: 34px 0 10px; border-bottom: 1px solid var(--line); padding-bottom: 4px; }}
  .sub {{ color: var(--muted); margin: 0 0 18px; font-size: .95rem; }}
  .tf {{ font-family: 'Noto Sans Tifinagh', 'Ebrima', sans-serif; }}
  .lt {{ font-family: 'Helvetica Neue', Arial, sans-serif; }}
  .verdict {{ background: #fff; border: 1px solid var(--line); border-left: 5px solid var(--ok); padding: 16px 20px; border-radius: 6px; }}
  .verdict p {{ margin: 6px 0; }}
  .verdict .en {{ font-size: 1.2rem; }}
  .tag {{ display:inline-block; font: 12px/1.7 'Helvetica Neue', Arial, sans-serif; padding: 0 8px; border-radius: 10px; color:#fff; background: var(--ok); vertical-align: 2px; }}
  .claim {{ font-style: italic; color: var(--muted); border-left: 3px solid var(--line); padding-left: 12px; margin: 10px 0; }}
  .shots {{ display:grid; grid-template-columns: 2fr 1fr; gap: 14px; align-items:start; }}
  figure {{ margin: 0; background:#fff; border:1px solid var(--line); border-radius:6px; padding:6px; }}
  figure img {{ width:100%; display:block; border-radius:4px; }}
  figcaption {{ font-size: .85rem; color: var(--muted); padding: 4px 2px 0; }}
  .raw {{ background:#111; color:#eee; border-radius:6px; padding:14px 18px; font-size: 1.5rem; line-height:1.6; }}
  .tl {{ background:#fff; border:1px solid var(--line); border-radius:6px; padding:12px 18px; font-size:1.12rem; }}
  .cards {{ display:flex; flex-wrap:wrap; gap:10px 10px; background:#fff; border:1px solid var(--line); border-radius:6px; padding:14px; }}
  .wc {{ background:#f4f2ec; border-radius:6px; padding:6px 10px; text-align:center; }}
  .wc .tf {{ font-size: 1.55rem; line-height:1.3; }}
  .wc .lt {{ font-size: 1.0rem; color: var(--hd); font-weight:600; }}
  .wc .gl {{ font: .85rem/1.3 'Helvetica Neue', Arial, sans-serif; color: var(--muted); }}
  .wc.dash {{ background:none; align-self:center; }}
  table {{ border-collapse: collapse; width:100%; background:#fff; border:1px solid var(--line); }}
  th, td {{ border-bottom: 1px solid var(--line); padding: 5px 9px; text-align:left; vertical-align: middle; }}
  th {{ font: 600 .85rem 'Helvetica Neue', Arial, sans-serif; color: var(--muted); background:#f4f2ec; }}
  td.tf {{ font-size: 1.3rem; }} td.big {{ font-size: 1.6rem; text-align:center; }}
  td.lt {{ font-weight:600; color: var(--hd); }}
  td.nt, td.sm {{ font-size: .9rem; color: var(--muted); }}
  td.num {{ text-align:right; font-family: 'Helvetica Neue', Arial, sans-serif; }}
  .bar {{ display:inline-block; height: 10px; background: var(--hd); border-radius: 2px; }}
  ol li, ul li {{ margin: 6px 0; }}
  .note {{ background:#fff8ec; border:1px solid #f0dfbf; border-radius:6px; padding: 10px 16px; font-size:.95rem; }}
  code {{ font-size: .88em; }}
  @media (max-width: 760px) {{ .shots {{ grid-template-columns: 1fr; }} }}
</style>
</head>
<body>
<main>
<h1>A Tifinagh post on a blank-titled YouTube channel</h1>
<p class="sub">Source: <a href="https://www.reddit.com/r/codes/comments/1xm43zd/hello_everyone_i_found_an_account_with_this_kind/">“Hello everyone, I found an account with this kind…”</a>, r/codes, posted by u/Emotional-Point-4093. The post is on the YouTube channel <a href="https://www.youtube.com/@Soul09-t4e/posts">@Soul09-t4e</a> (Posts tab).</p>

<div class="verdict">
  <p><span class="tag">CLAIM CONFIRMED</span> &nbsp;It is a language, not a code. The script is <b>Tifinagh</b> (the modern Neo-Tifinagh alphabet), and the language is <b>Kabyle</b> (<i>Taqbaylit</i>), a Tamazight (Berber) language of northern Algeria.</p>
  <p class="en">“Stop, don’t bring me in; let the dead rest in peace, because you don’t want nightmares, and you want to be able to sleep.”</p>
  <p class="lt" style="color:var(--muted)">Ḥbes, ur iyi-d-tessekcem ara; eǧǧ imdanen yemmuten ad sgunfun di talwit — axaṭer ur tebɣiḍ ara tirga n yiḍ, yerna tebɣiḍ ad teṭṭseḍ.</p>
</div>

<p class="claim">The claim being checked (a reply in the thread): “This is no code, this is the Tifinagh alphabet, the messages are probably in a Tamazight language.”</p>
<p>Every part of the claim holds. The one thing to add is <i>which</i> Tamazight language: the text is Kabyle. It uses Kabyle’s two-part negation <i>ur … ara</i> and Kabyle words such as <i>axaṭer</i> ‘because’ and <i>yerna</i> ‘and also’. It is spelled letter for letter in standard Kabyle Latin spelling, written with Tifinagh letters (see <a href="#kabyle">why Kabyle</a>).</p>

<h2>The post</h2>
<div class="shots">
  <figure><img src="images/post.png" alt="Screenshot of the YouTube community post in Tifinagh"><figcaption>Screenshot from the Reddit thread. YouTube showed the post with 3.1k likes and 798 comments.</figcaption></figure>
  <figure><img src="images/channel.png" alt="Screenshot of the @Soul09-t4e channel page"><figcaption>The channel @Soul09-t4e (98.7k subscribers, 10 videos at screenshot time).</figcaption></figure>
</div>

<h3>Raw text, as stored by YouTube</h3>
<div class="raw tf">{esc(TEXT)}</div>
<p style="font-size:.92rem;color:var(--muted)">This text was fetched from the channel’s Posts tab on 2026-11-26 (post id <code>UgkxTeSd9kcxxBFQjfeyy4TpR7akBGtbUPyZ</code>, listed as “3 months ago”). It is real Unicode text, not an image. It uses 24 different letters, all from the Unicode Tifinagh block (U+2D30–U+2D7F), plus ordinary punctuation: a comma, a hyphen, a semicolon and an em dash. My transcription from the screenshot alone, made before the fetch, matched it character for character.</p>

<h2>Reading, word by word</h2>
<div class="cards">
{''.join(word_cards)}
</div>

<h3>Transliteration (standard Kabyle Latin spelling)</h3>
<div class="tl lt">{esc(TR)}.</div>
<p style="font-size:.92rem;color:var(--muted)">This is a direct letter-for-letter conversion. The only differences from textbook spelling are the missing hyphen in <i>iyid-</i> (normally <i>iyi-d-</i>) and the missing final full stop. I added the full stop here.</p>

<h3>Translation</h3>
<div class="tl">
  <p><b>Literal:</b> “Stop, do not bring me in; leave the people who have died to rest in peace, because you do not want dreams of the night, and besides, you want to sleep.”</p>
  <p><b>Natural:</b> “Stop. Don’t bring me into this. Let the dead rest in peace, because you don’t want nightmares, and you’d like to be able to sleep.”</p>
</div>

<h3>Gloss</h3>
<table>
<tr><th>Tifinagh</th><th>Latin</th><th>Meaning</th><th>Notes</th></tr>
{''.join(gloss_rows)}
</table>

<div class="note" style="margin-top:14px">
<b>Uncertain points.</b> These glosses come from Kabyle dictionary forms. A native speaker has not checked them.
<ul>
  <li><i>ur iyi-d-tessekcem ara</i> is clearly “not … bring/let me in (toward here)”. But the verb form is a little odd for a command. A native prohibition would normally be built on the bare intensive form (as in <i>ur ttru ara</i> ‘don’t cry’). As written, <i>tessekcem</i> looks like “she brought in”, or a “you” form missing its final <i>-ḍ</i>. That may point to a learner or a machine translation, but the intended sense is clear: “don’t drag me in / don’t let me in”.</li>
  <li><i>tirga n yiḍ</i> is literally “dreams of the night”. In context (“you don’t want …, and you want to sleep”) it means bad dreams, i.e. nightmares.</li>
</ul>
</div>

<h2>Letter key</h2>
<p>These are the 24 Tifinagh letters in the post, with their Unicode names and the Kabyle Latin letter each one stands for. Each Tifinagh letter maps to exactly one Latin letter. There are {N} letters in total.</p>
<table>
<tr><th>Glyph</th><th>Code point</th><th>Unicode name</th><th>Latin</th><th>Sound</th><th>Count</th><th></th></tr>
{''.join(key_rows)}
</table>

<h2 id="not-cipher">Why this is not a cipher</h2>
<ol>
  <li><b>The characters are real script, not invented symbols.</b> The text is stored as standard Unicode Tifinagh code points. That is what a Tifinagh keyboard layout produces.</li>
  <li><b>No key is needed.</b> Read with each letter’s standard sound value, all 22 words are ordinary Kabyle words. They form a grammatical sentence, and the punctuation (comma, semicolon, dash, comma) falls exactly at the clause breaks. A cipher would not turn into fluent text under the script’s own published sound values.</li>
  <li><b>The letter counts look like Kabyle.</b> The most common letter is ⴻ <i>e</i> (schwa, {counts['ⴻ']}/{N}). Next come {RUNNERS}. Kabyle writing is full of schwas and of <i>t</i> from feminine and verb prefixes.</li>
</ol>

<h2 id="kabyle">Why Kabyle in particular</h2>
<ul>
  <li><b>The negation <i>ur … ara</i></b> wraps the verb twice (<i>ur iyid-tessekcem ara</i>, <i>ur tebɣiḍ ara tirga</i>). This two-part negation is the standard Kabyle pattern, e.g. <i>Ur urareɣ ara</i> ‘I did not play’ (<a href="https://en.wikipedia.org/wiki/Kabyle_grammar">Kabyle grammar</a>). The pre-verbal <i>ur</i> is common to Berber, but the word after the verb varies by language, and <i>ara</i> is the Kabyle one. Other varieties use <i>ur</i> alone or a different second word such as <i>ša</i> (<a href="https://sites.uwm.edu/ouali/files/2021/09/15.-Ouali-2003.pdf">Ouali 2003</a>).</li>
  <li><b>The vocabulary is Kabyle:</b> <i>axaṭer</i> ‘because’, <i>yerna</i> ‘and also’, <i>ḥbes</i> ‘stop’, <i>eǧǧ</i> ‘leave’ (compare <i>Eǧǧ-iyi!</i> ‘Leave me alone!’ in Kabyle phrasebooks), <i>sgunfu</i> ‘rest’, <i>imdanen</i> ‘people’, <i>eṭṭes</i> ‘sleep’.</li>
  <li><b>The spelling is Kabyle Latin spelling, carried over letter for letter.</b> The schwa is written (ⴻ for <i>e</i>), doubled consonants are written double (ⵙⵙ, ⵎⵎ, ⵟⵟ, ⴵⴵ), and clitics are joined to the verb with a hyphen (ⵉⵢⵉⴷ-ⵜⴻⵙⵙⴻⴽⵛⴻⵎ <i>iyid-tessekcem</i>; standard spelling hyphenates once more, <i>iyi-d-tessekcem</i>). This is how Kabyle is usually written in Latin letters. Here it has simply been typed with a Tifinagh keyboard.</li>
  <li><b>ⴵ for <i>ǧ</i>.</b> Unicode names this letter <code>TIFINAGH LETTER BERBER ACADEMY YAJ</code> (U+2D35). It comes from the Berber Academy (Agraw Imazighen), the Kabyle-led group that popularised Neo-Tifinagh from the late 1960s.</li>
</ul>

<h2>Context on the channel</h2>
<ul>
  <li>The channel’s name, its description and all 11 video titles fetched on 2026-11-26 consist only of invisible filler characters (U+3164 HANGUL FILLER and U+2800 BRAILLE PATTERN BLANK). So the Tifinagh post is the only readable text on the channel page.</li>
  <li>The message fits the channel’s eerie found-footage style. It is a warning, apparently in the voice of the dead, to stop digging and leave them alone.</li>
  <li>Only this one post appeared in the first page of the Posts tab, so any older posts on the channel were not checked. If other posts are also in Tifinagh, the same letter key above should read them.</li>
</ul>

<p class="sub" style="margin-top:36px">Files: <code>images/post.png</code>, <code>images/channel.png</code> (screenshots from the thread); <code>work/post_text.txt</code> (raw post text); <code>work/build_index.py</code> (builds this page and checks that the gloss reproduces the raw text exactly).</p>
</main>
</body>
</html>
"""
(ROOT / "index.html").write_text(page, encoding="utf-8")
print("wrote", ROOT / "index.html", "| letters:", N, "| distinct:", len(counts))
print(TR)
