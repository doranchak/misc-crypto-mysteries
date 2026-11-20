# Builds index.html for the "Cipher leads to a image" puzzle (run with python3.11: needs numpy + PIL).
#   /opt/homebrew/bin/python3.11 -I build_report.py
import html
import numpy as np
from PIL import Image

SRC = "https://www.reddit.com/r/ciphers/comments/1y0v8t5/cipher_leads_to_a_image/"
AUTHOR = "u/Anxious-Anything-894"
GROUPS = ("12112111 12112111 12212222 12211112 12211112 12221222 12222121 12112111 12122112 12122112 "
          "11211221 12122222 11212212 11212122 11212122 12221111 12221211 12212221 12211121 12222112 "
          "12212121 12221221 12221211 11112121 12212111 11112121 11112121 12221211 12121111 12121212 "
          "12111222 12121112 12122121 12221122 11112121 11112121 11221222").split()
SHIFT = 7


def rot(c, k):
    if c.isalpha():
        b = 65 if c.isupper() else 97
        return chr((ord(c) - b - k) % 26 + b)
    return c


def vis(c):
    return {"\n": "&#9166; (LF)", " ": "&#9251;"}.get(c, html.escape(c))


# layer 1: bits -> ASCII -> Caesar -7 (letters only)
bytes_ = [int("".join("0" if ch == "1" else "1" for ch in g), 2) for g in GROUPS]
ascii_ = [chr(b) for b in bytes_]
dec = [rot(c, SHIFT) for c in ascii_]
assert "".join(dec) == "AAhttpsARR&_-++imgurcom\na\n\nmINZJSl\n\n7"

# which decoded characters belong to the URL (inferred): https | imgur com | a | mINZJSl
url_idx = set(range(2, 7)) | set(range(15, 23)) | {24} | set(range(27, 34))
rows = []
for i, (g, b, a, d) in enumerate(zip(GROUPS, bytes_, ascii_, dec)):
    cls = "url" if i in url_idx else "noise"
    rows.append(f"<tr class='{cls}'><td>{i+1}</td><td class='mono'>{g}</td><td class='mono'>{b:07b}</td>"
                f"<td class='mono'>0x{b:02X}</td><td class='mono'>{vis(a)}</td><td class='mono'>{vis(d)}</td>"
                f"<td>{'URL' if cls=='url' else 'junk'}</td></tr>")

# layer 3: LSB stego in row 0
arr = np.array(Image.open("qkhHnIc.png").convert("RGB"))
bits = "".join(str(v & 1) for v in arr[0, :80].reshape(-1))
sb = [int(bits[i:i + 8], 2) for i in range(0, 240, 8)]
msg = "".join(chr(x) for x in sb if x)
assert msg == "\rNicEcoMplEte2"
srows = "".join(f"<tr><td>{i}</td><td class='mono'>{bits[i*8:i*8+8]}</td><td class='mono'>{x}</td>"
                f"<td class='mono'>{html.escape(chr(x)) if 32 <= x < 127 else ('CR' if x == 13 else 'NUL' if x == 0 else '')}</td></tr>"
                for i, x in enumerate(sb))
rest = arr[0, 80:].reshape(-1)
assert (rest == 255).all()  # everything after the 80 stego pixels is plain white

page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cipher leads to a image - decoding notes</title>
<style>
:root {{ color-scheme: light dark; --bg:#f9f9f7; --card:#fcfcfb; --ink:#0b0b0b; --ink2:#52514e; --line:#e1e0d9; --acc:#2a78d6; --noise:#898781; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#0d0d0d; --card:#1a1a19; --ink:#f0efec; --ink2:#c3c2b7; --line:#2c2c2a; --acc:#3987e5; --noise:#898781; }} }}
body {{ margin:0; background:var(--bg); color:var(--ink); font:15px/1.55 system-ui,-apple-system,sans-serif; }}
.wrap {{ max-width:980px; margin:0 auto; padding:24px 20px 56px; }}
h1 {{ font-size:22px; margin:0 0 4px; }} h2 {{ font-size:17px; margin:0 0 8px; }}
.card {{ background:var(--card); border:1px solid var(--line); border-radius:10px; padding:16px 20px; margin-top:16px; }}
.sub {{ color:var(--ink2); }} a {{ color:var(--acc); }}
.mono {{ font-family:ui-monospace,SFMono-Regular,Menlo,monospace; }}
pre {{ background:var(--bg); border:1px solid var(--line); border-radius:8px; padding:10px 12px; overflow:auto; margin:8px 0; }}
table {{ border-collapse:collapse; width:100%; font-size:13px; }}
th,td {{ border-bottom:1px solid var(--line); padding:3px 8px; text-align:left; }}
tr.noise td {{ color:var(--noise); }} tr.url td {{ font-weight:600; }}
img {{ max-width:100%; border:1px solid var(--line); border-radius:8px; }}
.ok {{ color:#0a7a0a; font-weight:600; }} .bad {{ color:#c0392b; font-weight:600; }}
</style></head><body><div class="wrap">
<h1>Cipher leads to a image</h1>
<div class="sub">Source: <a href="{SRC}">{SRC}</a> &middot; posted by {AUTHOR} on r/ciphers</div>

<div class="card"><h2>Result</h2>
<p><span class="ok">Solved to the image and its hidden string:</span> the 37 groups decode to
<span class="mono">https://imgur.com/a/mINZJSl</span> &rarr; a PNG whose top pixel row hides
<span class="mono">NicEcoMplEte2</span> ("Nice complete 2").</p>
<p><span class="bad">Not decoded:</span> the four lines of visible "nonsensical CODE" in the picture
(see below). They are probably filler, but that is an inference, not something I could confirm
(the Reddit thread could not be read from here, so I have not seen the poster's hints or any solution).</p>
<ol>
<li>Each group of 8 digits (only 1 and 2) is a byte with 1&rarr;0, 2&rarr;1. The first digit is always 1, so every byte has its top bit clear: 7-bit ASCII.</li>
<li>Shift the <em>letters</em> back by {SHIFT} (Caesar, case kept; non-letters untouched). <span class="mono">ptnbyjvt</span> becomes <span class="mono">imgurcom</span>, <span class="mono">oaawz</span> becomes <span class="mono">https</span>.</li>
<li>Junk characters sit where the URL's punctuation belongs (<span class="mono">://</span>, <span class="mono">.</span>, <span class="mono">/</span>, <span class="mono">/</span>) plus some at the ends. Reinserting the punctuation gives <span class="mono">https://imgur.com/a/mINZJSl</span>; the album (title "Whhat") exists and holds one image, <span class="mono">https://i.imgur.com/qkhHnIc.png</span> (2048&times;2048).</li>
<li>The lowest bit of each colour value in the first 80 pixels of row 0 spells <span class="mono">NicEcoMplEte2</span> (preceded by a carriage return, with a zero byte between characters). Every pixel after that is plain white 255.</li>
</ol></div>

<div class="card"><h2>Layer 1: groups &rarr; ASCII &rarr; Caesar &minus;{SHIFT}</h2>
<p class="sub">Bold = characters that form the URL; grey = junk. Which characters are "URL" is my reading; the junk positions line up with where <span class="mono">://</span>, <span class="mono">.</span> and <span class="mono">/</span> would go.</p>
<table><tr><th>#</th><th>group</th><th>7 bits</th><th>hex</th><th>ASCII</th><th>Caesar&minus;{SHIFT}</th><th></th></tr>
{''.join(rows)}</table>
<pre class="mono">ASCII  : HHoaawzHYY&amp;_-++ptnbyjvt&#9166;h&#9166;&#9166;tPUGQZs&#9166;&#9166;7
Caesar : AAhttpsARR&amp;_-++imgurcom&#9166;a&#9166;&#9166;mINZJSl&#9166;&#9166;7
URL    : https://imgur.com/a/mINZJSl</pre></div>

<div class="card"><h2>Layer 2: the PNG</h2>
<p><img src="qkhHnIc.png" alt="the PNG: 'this Png contains nonsEnsical CODE:' and four lines of code" width="480"></p>
<pre class="mono">this Png contains nonsEnsical CODE:
Gdky5e
7e5usjf(p=d)jrsrsutefr7
gigkyjtur;$$+$+$
+_+3($</pre>
<p>Only 559 distinct colours, no extra PNG chunks. The capital P and E in "Png" and "nonsEnsical" look deliberate, in the same style as the capital E's in the hidden string.</p>
<p><b>Tried on the four lines, no English result:</b> Caesar on letters (all 25 shifts, whole text and lowercase-only), shifts over the 94 printable ASCII characters, single-byte XOR, Vigenere with keys nicecomplete / nicecomplete2 / png / code / nonsensical / imgur / https, every-2nd/3rd character, reversal, Atbash.
The only curiosity: the letter pattern of <span class="mono">jrsrsutefr</span> matches "rededicate", but that does not extend to the rest, so I treat it as coincidence.</p></div>

<div class="card"><h2>Layer 3: LSB steganography in row 0</h2>
<p>Red, green, blue least-significant bits of pixels 0&ndash;79 in order give 240 bits = 30 bytes:</p>
<table><tr><th>byte</th><th>bits</th><th>value</th><th>char</th></tr>{srows}</table>
<p class="sub">Reads <span class="mono">&lt;CR&gt; N i c E c o M p l E t e 2</span> with zero bytes in between. The earlier r/codes puzzle by the same poster
(Base64 + Caesar, in <span class="mono">../base-64-and-caesar-cipher/</span>) hid the lowercase words "nicecomplete", so this looks like the poster's completion message.</p></div>

<div class="card"><h2>Reproduce</h2>
<pre class="mono">/opt/homebrew/bin/python3.11 -I decode.py        # prints the Caesar result and the stego string
/opt/homebrew/bin/python3.11 -I build_report.py  # rebuilds this page</pre>
<p class="sub">Files: <span class="mono">decode.py</span>, <span class="mono">build_report.py</span>, <span class="mono">qkhHnIc.png</span> (downloaded from imgur; untrusted third-party image, kept only as data).</p></div>
</div></body></html>
"""
open("index.html", "w").write(page)
print("wrote index.html", len(page))
