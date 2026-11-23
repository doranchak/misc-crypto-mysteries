#!/usr/bin/env python3
"""Build index.html (static report + live encode/decode tool). Run: /opt/homebrew/bin/python3.11 build.py"""
import base64, string, html, math
CT = open("/Users/doranchak/projects/github/misc-crypto-mysteries/friend-two-ciphers-base64-caesar/cipher.txt").read().strip()
U, L = string.ascii_uppercase, string.ascii_lowercase
def rot(x, n): return x.translate(str.maketrans(U+L, U[n%26:]+U[:n%26]+L[n%26:]+L[:n%26]))
B64 = rot(CT, 16); PT = base64.b64decode(B64).decode()
assert rot(base64.b64encode(PT.encode()).decode(), 10) == CT

# 4-char groups -> 3 bytes
groups = []
for i in range(0, len(CT), 4):
    c = CT[i:i+4]; b = B64[i:i+4]; raw = base64.b64decode(b)
    groups.append((c, b, raw.hex(" "), raw.decode()))
grow = "\n".join(
    f"<tr><td class=mono>{i+1}</td><td class='mono ct'>{c}</td><td class=mono>{b}</td>"
    f"<td class=mono>{h}</td><td class='mono pt'>{html.escape(t).replace(' ', '&nbsp;')}</td></tr>"
    for i, (c, b, h, t) in enumerate(groups))

# 26-shift table
srows = []
for n in range(26):
    t = rot(CT, n)
    try:
        d = base64.b64decode(t + "="*(-len(t) % 4), validate=True)
        ok = all(32 <= x < 127 for x in d)
        shown = d.decode() if ok else "<span class=bad>bytes not printable ASCII</span>"
    except Exception:
        ok = False; shown = "<span class=bad>invalid</span>"
    cls = " class=hit" if ok else ""
    srows.append(f"<tr{cls}><td class=mono>+{n}</td><td class='mono wrap'>{t}</td><td>{shown}</td></tr>")
srows = "\n".join(srows)

p_one = (95/256) ** len(PT)
page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Friend's two-cipher puzzle — solved: Base64 + Caesar</title>
<style>
  :root {{
    --bg:#fafaf8; --fg:#1d1d1b; --muted:#6b6b66; --line:#dcdcd4; --card:#fff;
    --accent:#0b6e4f; --accent-bg:#e3f3ec; --warn:#a4400f; --warn-bg:#fbeadf;
    --c0:#d6e4ff; --c1:#ffe3c4;
    --mono: ui-monospace,"SF Mono",Menlo,Consolas,monospace;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{ --bg:#17181a; --fg:#e8e8e3; --muted:#9a9a92; --line:#333537; --card:#1f2022;
      --accent:#5fd1a2; --accent-bg:#173326; --warn:#f0a070; --warn-bg:#3a2416; --c0:#24385e; --c1:#5a3b17; }}
  }}
  *{{box-sizing:border-box}}
  body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif}}
  main{{max-width:980px;margin:0 auto;padding:32px 20px 80px}}
  h1{{font-size:1.6rem;margin:0 0 4px}}
  h2{{font-size:1.15rem;margin:40px 0 8px;padding-top:8px;border-top:1px solid var(--line)}}
  p{{margin:8px 0}} .sub{{color:var(--muted);margin-bottom:20px}}
  code,.mono{{font-family:var(--mono);font-size:.9em}}
  .card{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin:12px 0}}
  .answer{{background:var(--accent-bg);border-color:var(--accent)}}
  .answer .pt{{font-size:1.3rem;font-weight:600;margin-top:4px}}
  .label{{font-size:.75rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-bottom:4px}}
  .ctline{{font-family:var(--mono);word-break:break-all;font-size:.95rem}}
  .note{{background:var(--warn-bg);border:1px solid var(--warn);border-radius:8px;padding:10px 14px;font-size:.92rem;margin:12px 0}}
  .flow{{display:flex;flex-wrap:wrap;align-items:stretch;gap:8px;margin:12px 0}}
  .box{{flex:1 1 180px;border:1px solid var(--line);border-radius:10px;padding:10px 12px;background:var(--card)}}
  .box.c0{{background:var(--c0)}} .box.c1{{background:var(--c1)}}
  .box b{{display:block;margin-bottom:2px}} .box .mono{{word-break:break-all;font-size:.8rem}}
  .arrow{{align-self:center;color:var(--muted);font-size:1.3rem}}
  table{{border-collapse:collapse;width:100%;font-size:.86rem}}
  th,td{{border-bottom:1px solid var(--line);padding:4px 8px;text-align:left;vertical-align:top}}
  th{{color:var(--muted);font-weight:600}}
  td.wrap{{word-break:break-all}} tr.hit td{{background:var(--accent-bg);font-weight:600}}
  .bad{{color:var(--warn)}} .pt{{color:var(--accent)}}
  label.field{{display:block;margin:10px 0 2px;font-size:.85rem;color:var(--muted)}}
  input[type=text],textarea{{width:100%;font-family:var(--mono);font-size:.9rem;padding:8px 10px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--fg)}}
  .row{{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0;align-items:center}}
  button{{font:inherit;font-size:.85rem;padding:6px 12px;border:1px solid var(--line);background:var(--card);color:var(--fg);border-radius:6px;cursor:pointer}}
  button:hover{{border-color:var(--accent)}}
  .out{{font-family:var(--mono);padding:10px 12px;background:var(--bg);border:1px dashed var(--line);border-radius:6px;word-break:break-all;white-space:pre-wrap;min-height:2.6em}}
  ul{{margin:6px 0 6px 20px;padding:0}}
  a{{color:var(--accent)}}
</style>
</head>
<body>
<main>
<h1>Friend's two-cipher puzzle &mdash; solved</h1>
<p class="sub">"Cipher a friend made. It's made of 2 different ciphers &hellip; I think one of them is base64." &mdash; the guess was right, and the other cipher is a Caesar shift.</p>

<p class="sub" style="margin-top:-8px">Source: <a href="https://www.reddit.com/r/Cipher/comments/1y3aq83/cipher_a_friend_made/">r/Cipher &ldquo;Cipher a friend made&rdquo;</a>, posted by u/Maleficent-Mango5262.</p>

<div class="card">
  <div class="label">Ciphertext ({len(CT)} characters)</div>
  <div class="ctline">{CT}</div>
</div>

<div class="card answer">
  <div class="label">Plaintext</div>
  <div class="pt">{html.escape(PT)}</div>
  <p class="sub" style="margin:6px 0 0">Recovered by <b>Caesar &minus;10</b> (written as +16) on the letters, then <b>Base64</b>. Re-encoding the plaintext reproduces the ciphertext exactly.</p>
</div>

<h2>How it was made (and undone)</h2>
<div class="flow">
  <div class="box"><b>Plaintext</b><span class="mono">{html.escape(PT)}</span></div>
  <div class="arrow">&rarr;</div>
  <div class="box c0"><b>1. Base64</b><span class="mono">{B64}</span></div>
  <div class="arrow">&rarr;</div>
  <div class="box c1"><b>2. Caesar +10 <small>(letters only)</small></b><span class="mono">{CT}</span></div>
</div>
<p>To decode, run it backwards: shift every letter back 10 places (A&ndash;Z and a&ndash;z each wrap within their own case; digits unchanged), then Base64-decode the result. Equivalently, shift forward 16, which is how the brute-force below lists it.</p>

<div class="note"><b>About "two halves".</b> The puzzle description suggested one half uses one cipher and the other half another. That isn't the structure: both ciphers apply to the <em>whole</em> string, stacked as layers (Base64 first, Caesar on top). I also tested every split point with a Caesar shift and Base64 on either side alone, and found nothing except the whole-string shift +16 (see <code>solve.py</code>). Half-and-half is how it looks when you don't yet know the layers are stacked: the first thing you see is a Base64-looking string that won't decode.</div>

<h2>Step by step, four characters at a time</h2>
<p>Base64 reads four characters as three bytes. After undoing the Caesar shift, each group of four turns into three readable letters:</p>
<table>
<tr><th>#</th><th>Ciphertext</th><th>Shift &minus;10 (Base64)</th><th>Bytes (hex)</th><th>Text</th></tr>
{grow}
</table>
<p>The last group ends cleanly with no <code>=</code> padding because the plaintext is 39 bytes, a multiple of 3.</p>

<h2>Why shift 16 and no other: the brute force</h2>
<p>All 26 Caesar shifts, applied to the whole string and then Base64-decoded:</p>
<table>
<tr><th>Shift</th><th>String after shift</th><th>Base64 decode</th></tr>
{srows}
</table>
<p>Only one shift gives printable ASCII. Chance of a random 39-byte decode being all printable ASCII is about (95/256)<sup>39</sup> &asymp; {p_one:.1e}, so this isn't a coincidence. The shifted text is also the textbook Base64 of English: <code>VGhl</code> = "The".</p>

<h2>A tell you could have spotted</h2>
<ul>
  <li>The ciphertext contains digits <code>9 0 3 5</code> but no <code>+</code>, <code>/</code> or <code>=</code>, and it's a multiple of 4 long ({len(CT)}). That fits Base64 with a letter-only substitution on top.</li>
  <li><code>SQ</code> occurs 3 times. In Base64, <code>IG</code> is what a space at the start of a 3-byte group looks like when followed by a letter from a&ndash;o. <code>I</code>&rarr;<code>S</code> and <code>G</code>&rarr;<code>Q</code> are both +10, so the shift can be read straight off that pair.</li>
  <li>Digits stay put, so the substitution isn't a rotation of the whole 64-symbol Base64 alphabet. I tried that first (all 64 rotations, all split points) and it failed. It's ROT-style on letters only.</li>
</ul>

<h2>Try it</h2>
<div class="card">
  <label class="field" for="inp">Input (ciphertext to decode, or plaintext to encode)</label>
  <textarea id="inp" rows="2">{CT}</textarea>
  <div class="row">
    <label class="field" for="shift" style="margin:0">Caesar shift</label>
    <input id="shift" type="text" value="10" style="width:70px">
    <button id="dec">Decode (shift back, then Base64)</button>
    <button id="enc">Encode (Base64, then shift)</button>
  </div>
  <div class="label">Result</div>
  <div class="out" id="out"></div>
</div>

<h2>Files</h2>
<ul>
  <li><code>cipher.txt</code> &mdash; the ciphertext</li>
  <li><code>solve.py</code> &mdash; brute force over all shifts and split points, plus re-encode check</li>
  <li><code>build.py</code> &mdash; generates this page</li>
</ul>
</main>
<script>
const U="ABCDEFGHIJKLMNOPQRSTUVWXYZ", Lw=U.toLowerCase();
function rot(s,n){{
  n=((n%26)+26)%26;
  return s.replace(/[A-Za-z]/g,ch=>{{
    const base=ch<'a'?U:Lw; return base[(base.indexOf(ch)+n)%26];
  }});
}}
function shiftVal(){{ const v=parseInt(document.getElementById('shift').value,10); return isNaN(v)?0:v; }}
function show(t,bad){{ const o=document.getElementById('out'); o.textContent=t; o.className='out'+(bad?' bad':''); }}
function decode(){{
  const s=document.getElementById('inp').value.trim();
  try{{
    let t=rot(s,-shiftVal()); t+= '='.repeat((4-t.length%4)%4);
    const bin=atob(t); const bytes=Uint8Array.from(bin,c=>c.charCodeAt(0));
    show(new TextDecoder('utf-8').decode(bytes),false);
  }}catch(e){{ show('Not valid Base64 after shifting back '+shiftVal()+'.',true); }}
}}
function encode(){{
  const s=document.getElementById('inp').value;
  const bytes=new TextEncoder().encode(s); let bin=''; bytes.forEach(b=>bin+=String.fromCharCode(b));
  show(rot(btoa(bin).replace(/=+$/,''),shiftVal()),false);
}}
document.getElementById('dec').onclick=decode;
document.getElementById('enc').onclick=encode;
decode();
</script>
</body>
</html>
"""
open("/Users/doranchak/projects/github/misc-crypto-mysteries/friend-two-ciphers-base64-caesar/index.html","w").write(page)
print("wrote", len(page))
