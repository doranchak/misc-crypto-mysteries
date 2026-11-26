"""Inject part 5 ("More posts from the same account") into index.html.

Reads posts/transcripts/*.json (image texts transcribed from the post images,
captions typed in the Google Doc; see build_captions.py) and writes the section
between <!-- POSTS:BEGIN --> / <!-- POSTS:END --> markers, plus its CSS and JS.
Re-running replaces the previous output.

    /opt/homebrew/bin/python3.11 -I build_posts_section.py
"""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from decode import strict_decode  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(HERE, "posts", "transcripts")
DOC_URL = "https://docs.google.com/document/d/1Mga3g-7vtbdbXf687XU30GJYVBQ6X3bMquVsGO0zghg/edit?usp=sharing"

ALT = {
    "image17": "TikTok profile header: round anime-style avatar, display name written in the cipher, 18 following, 19 followers, 67 likes.",
    "image3": "White cipher text on a black background.",
    "image2": "Purple flowering bushes with pale-yellow cipher text; the first line is Hebrew.",
    "image18": "Forest path with a wooden walkway, red cipher text over the trees.",
    "image9": "Layered rock gorge with a thin waterfall, white cipher text.",
    "image5": "View through an airplane window, white cipher text.",
    "image10": "White cipher text on a black background.",
    "image15": "Blurred photo of a small finch, blue cipher text.",
    "image1": "Abandoned barn interior with metal pens, green cipher text.",
    "image11": "Dark empty corridor, white cipher text.",
    "image8": "Blurred photo of a small dark-headed bird, cyan cipher text.",
    "image6": "Northern landscape: sparse larches, low bushes and a field of grey boulders under cloud. No text.",
    "image4": "Forest undergrowth, blue cipher text.",
    "image16": "Long block of white cipher text on black.",
    "image12": "White cipher text on black.",
    "image14": "Teal cipher text on black above and below a photo of trees.",
    "image7": "White cipher text on a slate background.",
    "image13": "White cipher text on black.",
}

# Entries in the doc's order (newest first). Grouping into posts is inferred
# from content: the doc only lists images and captions one after another.
POSTS = [
    dict(title="Fed up with “this world”", items=[("img", "image3"), ("cap", "caption-after-image3")]),
    dict(title="Holiday in Adygea, and learning Hebrew", items=[("img", "image2"), ("img", "image18"), ("img", "image9"), ("cap", "caption-after-image9")]),
    dict(title="Back, after a flight home to Zaplavskaya", items=[("img", "image5"), ("cap", "caption-after-image5")]),
    dict(title="“New videos soon”", items=[("img", "image10")]),
    dict(title="A brambling, identified by its song", items=[("img", "image15"), ("cap", "caption-after-image15")]),
    dict(title="An evening with friends", items=[("img", "image1"), ("cap", "caption-after-image1")]),
    dict(title="First insulin injection", items=[("img", "image11"), ("cap", "caption-after-image11")]),
    dict(title="Yesterday’s bird was a Siberian stonechat", items=[("img", "image8"), ("cap", "caption-after-image8")]),
    dict(divider=True),
    dict(title="About today", items=[("photo", "image6"), ("cap", "caption-after-image6")]),
    dict(title="The lip piercing, and Dad", items=[("img", "image4"), ("cap", "caption-after-image4")]),
    dict(title="Bored: copying out Pushkin in the cipher", items=[("img", "image16")]),
    dict(title="A friend’s lost present", items=[("img", "image12")]),
    dict(title="A walk in the forest", items=[("img", "image14"), ("cap", "caption-after-image14")]),
    dict(title="“I’m a type 1 diabetic”", items=[("img", "image7")]),
    dict(title="The first TikTok", items=[("img", "image13")]),
]

KIND = {
    "author slip": ("cipher slip", "One chunk points to the wrong cell; changing just that chunk makes every later letter of the word right."),
    "author or transcription slip": ("cipher or typing slip", "As above, but the text was typed into the doc by someone else, so the error may be theirs."),
    "transcription or author slip": ("cipher or typing slip", ""),
    "author slip or misspelling": ("cipher slip", ""),
    "transcription slip": ("doc typing", ""),
    "transcription": ("doc typing", ""),
    "misspelling in plaintext": ("spelling", "Every chunk is valid; the word itself is misspelt or colloquial."),
    "letter skipped in plaintext": ("spelling", ""),
    "grammar slip in plaintext": ("spelling", ""),
    "unresolved": ("unresolved", ""),
    "my uncertain read": ("uncertain read", ""),
}

e = html.escape


def load(name):
    with open(os.path.join(T, name + ".json"), encoding="utf-8") as f:
        return json.load(f)


def para(text):
    return "".join(f"<p>{e(line)}</p>" for line in text.split("\n") if line.strip())


def slips_table(slips):
    if not slips:
        return '<p class="hint">No slips: every chunk lands on the intended letter.</p>'
    rows = []
    for s in slips:
        kind = KIND.get(s["kind"], (s["kind"], ""))[0]
        rows.append(
            f'<tr><td class="cw">{e(s["computed"])}</td><td class="iw">{e(s["intended"])}</td>'
            f'<td class="fx">{e(s["fix"])}</td><td><span class="kind k-{re.sub(r"[^a-z]+", "-", kind)}">{e(kind)}</span></td></tr>')
    return ('<div class="tablewrap"><table class="slips"><thead><tr><th>Computed</th><th>Reading</th>'
            '<th>What went wrong</th><th>Kind</th></tr></thead><tbody>' + "".join(rows) + "</tbody></table></div>")


def text_block(d, kind):
    is_cap = kind == "cap"
    label = "Caption (typed in the doc)" if is_cap else "Text in the image"
    cipher_for_decode = d.get("cipher_norm") or d["cipher"]
    slip_words = [s["computed"].split(" (")[0] for s in d["slips"]]
    out = [f'<div class="txt{" cap" if is_cap else ""}">',
           f'<div class="label">{label}</div>',
           f'<div class="ru-read" lang="ru">{para(d["reading_ru"])}</div>',
           f'<div class="en-read">{para(d["english"])}</div>',
           '<details><summary>Cipher, live decode and slips'
           f' <span class="hint">({len(d["slips"])} slip{"s" if len(d["slips"]) != 1 else ""})</span></summary>']
    if is_cap:
        out.append('<h4>As typed in the doc</h4>')
        out.append(f'<pre class="ciph">{e(d["cipher"])}</pre>')
        out.append('<h4>With Cyrillic anchors restored <span class="hint">(the doc uses Latin look-alikes such as B, H, P, C, I, Ch, Zh)</span></h4>')
        out.append(f'<pre class="ciph">{e(d["cipher_norm"])}</pre>')
    else:
        out.append('<h4>Transcription</h4>')
        out.append(f'<pre class="ciph">{e(d["cipher"])}</pre>')
    out.append('<h4>Straight decode <span class="hint">(computed live on this page; slips marked)</span></h4>')
    out.append(f'<pre class="computed" data-cipher="{e(cipher_for_decode)}" '
               f'data-slips="{e(json.dumps(slip_words, ensure_ascii=False))}">{e(strict_decode(cipher_for_decode))}</pre>')
    out.append('<h4>Slips</h4>')
    out.append(slips_table(d["slips"]))
    if d.get("uncertain"):
        out.append('<h4>Notes on the transcription</h4><ul class="notes">' +
                   "".join(f"<li>{e(u)}</li>" for u in d["uncertain"]) + "</ul>")
    out.append("</details></div>")
    return "\n".join(out)


def post_html(n, p):
    imgs, texts = [], []
    for kind, name in p["items"]:
        if kind in ("img", "photo"):
            imgs.append(
                f'<a href="posts/{name}.png" target="_blank" rel="noopener"><img loading="lazy" src="posts/{name}.png" alt="{e(ALT[name])}"></a>')
        if kind == "img":
            texts.append(text_block(load(name), "img"))
        if kind == "cap":
            texts.append(text_block(load(name), "cap"))
    return (f'<article class="post" id="post-{n}"><h3><span class="pn">{n}</span> {e(p["title"])}</h3>'
            f'<div class="post-body"><div class="post-imgs">{"".join(imgs)}</div>'
            f'<div class="post-texts">{"".join(texts)}</div></div></article>')


def stats():
    n_img = n_cap = words = 0
    kinds = {}
    for f in os.listdir(T):
        d = json.load(open(os.path.join(T, f), encoding="utf-8"))
        if f.startswith("caption"):
            n_cap += 1
        else:
            n_img += 1
        words += len(re.findall(r"[А-Яа-яЁёא-ת]+", d["reading_ru"]))
        for s in d["slips"]:
            k = KIND.get(s["kind"], (s["kind"],))[0]
            kinds[k] = kinds.get(k, 0) + 1
    return n_img, n_cap, words, kinds


def section():
    n_img, n_cap, words, kinds = stats()
    nslip = sum(kinds.values())
    posts = []
    n = 0
    for p in POSTS:
        if p.get("divider"):
            posts.append('<div class="divider"><span>the doc has a “---” divider here</span></div>')
            continue
        n += 1
        posts.append(post_html(n, p))
    kinds_txt = ", ".join(f"{v} {k}" for k, v in sorted(kinds.items(), key=lambda kv: -kv[1]))
    return f"""<!-- POSTS:BEGIN (generated by build_posts_section.py; edit the JSON in posts/transcripts and re-run) -->
<section aria-labelledby="h-posts">
  <h2 id="h-posts">5 · More posts from the same account</h2>
  <p>Someone collected the account’s other posts in a
    <a href="{DOC_URL}" rel="noopener noreferrer">shared Google Doc</a>: the cipher text in the post images, and the post captions typed out as text.
    Every one of them uses the same grid and the same rules, and every one decodes.
    That is <strong>{n_img} image texts</strong> (transcribed from the pictures) and <strong>{n_cap} captions</strong> (as typed in the doc),
    about <strong>{words} words</strong> in all. The first post settles who is writing:
    <i lang="ru">«Привет! Меня зовут Сюгюльгё, и это мой первый тикток! Я диабетик :(»</i>,
    “Hi! My name is Syugyulgyo, and this is my first TikTok! I’m diabetic :(”. So <b>syugyulgyo</b> is the transliterated
    <span lang="ru">Сюгюльгё</span>. The display name ПОТАТУЕВ is still unexplained; it looks like a mock surname built on “potato”.</p>
  <p class="callout"><strong>Content note.</strong> These are personal diary posts: profanity, type 1 diabetes, arguments with a parent, low mood.
    The translations keep the original tone.</p>

  <h3>New notation in the later posts</h3>
  <div class="tablewrap"><table class="ext">
    <thead><tr><th>Symbol</th><th>Meaning</th><th>Example</th></tr></thead>
    <tbody>
      <tr><td><span class="sym">0</span></td><td>Same letter again (a doubled letter). The first page’s encoder now uses this too.</td><td><span class="sym">Н2↑4←|4→|2↓←|↑3←|↓4→|0|3↓←|4↑3←</span> = НАДМЕННЫЕ</td></tr>
      <tr><td><span class="sym">⟳</span></td><td>Go back to the letter before (undo the last move). The next chunk starts from there; in 2 of 11 cases (ТУПОРЫЛЫХ, КАСАЕТСЯ) the author measured it from the letter before ⟳ instead, which I count as slips.</td><td><span class="sym">К2↑←⟳</span> = КАК; <span class="sym">К2↑←⟳|↑3→|4←</span> = КАКИЕ</td></tr>
      <tr><td><span class="sym">[x]²</span></td><td>Do chunk <i>x</i> twice (two letters).</td><td><span class="sym">В2←|[↓2→]²|3↓←|↑←</span> = ВАЖНЫХ</td></tr>
      <tr><td><span class="sym">-</span></td><td>Hyphen: a new anchor starts right after it.</td><td><span class="sym">И←-З↑3←</span> = ИЗ-ЗА; <span class="sym">Т|0</span> = ТТ (TikTok)</td></tr>
      <tr><td>Hebrew</td><td>Same rule on the Hebrew alphabet, final forms in their places (27 letters), laid out right to left. So <span class="sym">←</span> is “next letter” and <span class="sym">→</span> is “previous letter”.</td><td><span class="sym">ש3↑2←|↑2→|↓4←</span> = שלום; <span class="sym">מ↑→|4↓2→|5↑←</span> = מחשב</td></tr>
    </tbody>
  </table></div>
  <div class="rules" style="margin-top:1rem">
    <div>
      <p>The Hebrew turns up because the author started learning it: <i lang="ru">«как вы могли заметить по первому слайду, я начал изучать иврит»</i>
      (“as you may have noticed from the first slide, I’ve started learning Hebrew”). The first slide opens with שלום, and one caption line is all Hebrew:
      <i lang="he" dir="rtl">יש לי טלפון, אבל … לי מחשב</i> (“I have a phone, but … computer :(”). Its third word decodes to יס, which isn’t a word; אין (“don’t have”) fits the sad face but would need a different anchor, so that one stays open.</p>
    </div>
    <div>
      <div class="kgrid hgrid" id="hgrid" dir="rtl" role="img" aria-label="The Hebrew alphabet with final forms, in rows of five, right to left: אבגדה, וזחטי, כךלמם, נןסעפ, ףצץקר, שת."></div>
      <div class="kcap">The Hebrew key, read right to left. Each final form (ך ם ן ף ץ) sits right after its ordinary letter.</div>
    </div>
  </div>

  <h3>Slips, and why they are easy to fix</h3>
  <p>The author is not always careful: I count <strong>{nslip}</strong> places where the straight decode is wrong ({kinds_txt}).
    The relative moves make most of them easy to fix. If one chunk is wrong but the author worked out the <em>next</em> move from the letter they meant,
    then only one change is needed, and it makes the whole rest of the word right. Example:
    <span class="sym">П←|↑2→|2↑2←|2↓4→|2↑4←|↓2→</span> decodes as ПОЛАНАЖ. Change the third chunk from <span class="sym">2↑2←</span> to <span class="sym">↑2←</span>
    and every later chunk lands on ПОЛЕТЕЛ (“flew”). Each post below lists its slips with the one-chunk fix.
    The captions were typed into the doc by someone else (with Latin look-alikes such as <span class="sym">B</span> for Б/В,
    <span class="sym">H</span> for Н, <span class="sym">Ch</span> for Ч, and even the English words “And I”), so a few of their slips may be typing errors rather than the author’s.</p>
  <p class="hint">The entries follow the doc’s order, which looks newest first: the stonechat post refers back to the bird recorded in the post below it,
    and the first TikTok is last. Which images and captions belong to one post is my inference from the content.</p>

  <div class="posts">
{chr(10).join(posts)}
  </div>
  <p class="hint">Transcriptions, readings and slip lists are in <code>posts/transcripts/*.json</code>; <code>decode.py</code> is the Python decoder used to check them.</p>
</section>
<!-- POSTS:END -->"""


CSS = """/* POSTS-CSS:BEGIN */
.posts { display: grid; gap: 22px; margin-top: 1.2rem; }
.post { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 16px 18px; }
.post h3 { margin: 0 0 .7rem; display: flex; gap: .6rem; align-items: baseline; }
.post .pn { display: inline-grid; place-items: center; min-width: 1.8rem; height: 1.8rem; border-radius: 50%;
  background: var(--accent-tint); color: var(--accent); font-size: .85rem; font-weight: 700; }
.post-body { display: grid; grid-template-columns: minmax(180px, 300px) 1fr; gap: 20px; align-items: start; }
@media (max-width: 760px) { .post-body { grid-template-columns: 1fr; } }
.post-imgs { display: grid; gap: 8px; }
.post-imgs img { width: 100%; height: auto; display: block; border-radius: 10px; border: 1px solid var(--border); }
.post-texts { display: grid; gap: 14px; min-width: 0; }
.txt { border-left: 4px solid var(--accent); padding: .1rem 0 .1rem .9rem; }
.txt.cap { border-left-color: var(--anchor); }
.txt .label { font-size: .72rem; letter-spacing: .06em; text-transform: uppercase; color: var(--muted); }
.ru-read p { font-size: 1.08rem; font-weight: 600; margin: .3rem 0; }
.en-read p { color: var(--muted); margin: .3rem 0; }
.txt details { margin-top: .5rem; padding: .45rem .8rem; }
.txt details h4 { font-size: .78rem; text-transform: uppercase; letter-spacing: .05em; color: var(--muted); margin: .8rem 0 .25rem; }
pre.ciph, pre.computed { white-space: pre-wrap; overflow-wrap: anywhere; font-family: inherit; font-size: .9rem;
  background: var(--surface-2); border: 1px solid var(--border); border-radius: 8px; padding: .5rem .65rem; margin: 0; }
pre.computed { font-weight: 600; }
mark.slip { background: var(--anchor-tint); color: var(--anchor); border-radius: 4px; padding: 0 .15em; }
table.slips td { white-space: normal; vertical-align: top; }
table.slips td.cw { color: var(--bad); font-weight: 600; }
table.slips td.iw { color: var(--ok); font-weight: 700; }
table.slips td.fx { min-width: 16rem; }
.kind { font-size: .75rem; border: 1px solid var(--border); border-radius: 999px; padding: .05rem .5rem; white-space: nowrap; }
table.ext td { white-space: normal; vertical-align: top; }
ul.notes { margin: .2rem 0; padding-left: 1.2rem; font-size: .9rem; }
.divider { text-align: center; color: var(--muted); font-size: .82rem; border-top: 1px dashed var(--border); margin-top: 6px; }
.divider span { position: relative; top: -.75em; background: var(--bg); padding: 0 .6rem; }
.hgrid .k { font-size: 1.25rem; }
/* POSTS-CSS:END */"""

JS = r"""<script id="posts-js">
// POSTS-JS:BEGIN — extended decoder for the later posts (0, ⟳, [x]², hyphens, Hebrew)
const HEB = "אבגדהוזחטיכךלמםנןסעפףצץקרשת";
const RICH_RE = /([А-ЯЁа-яёא-ת])([0-9↑↓←→|⟳\[\]²³]*)/g;
function richChunks(moves) {
  const out = [];
  for (let part of moves.split("|")) {
    if (!part) continue;
    part = part.replace(/\[([^\]]*)\]([²³])/g, (_, x, p) => Array(p === "²" ? 2 : 3).fill(x).join("|"));
    for (const p of part.split("|")) for (const q of p.split(/(⟳)/)) if (q) out.push(q);
  }
  return out;
}
function richWalk(anchor, chunks, alpha, rtl) {
  const i = alpha.indexOf(anchor);
  let cur = { r: Math.floor(i / W), c: i % W };
  const hist = [cur];
  const at = p => (p.r < 0 || p.c < 0 || p.c >= W || p.r * W + p.c >= alpha.length) ? null : alpha[p.r * W + p.c];
  let text = anchor, bad = 0;
  for (const ch of chunks) {
    if (ch === "0") { text += text[text.length - 1]; hist.push(cur); continue; }
    if (ch === "⟳") { cur = hist.length >= 2 ? hist[hist.length - 2] : cur; hist.push(cur); const L = at(cur); text += L || "?"; if (!L) bad++; continue; }
    let dr = 0, dc = 0;
    const left = ch.replace(/(\d*)([↑↓←→])/g, (_, n, a) => {
      const k = n === "" ? 1 : parseInt(n, 10);
      const d = DIR[a];
      dr += d[0] * k; dc += d[1] * k * (rtl ? -1 : 1);
      return "";
    });
    if (left) { text += "⁇"; bad++; continue; }
    cur = { r: cur.r + dr, c: cur.c + dc };
    hist.push(cur);
    const L = at(cur);
    if (!L) bad++;
    text += L || "?";
  }
  return { text, bad };
}
function richDecode(s, mark) {
  // mark(word, bad) may wrap a decoded word; used to highlight slips
  let bad = 0;
  const text = s.replace(RICH_RE, (_, a, moves) => {
    const he = /[א-ת]/.test(a);
    const r = richWalk(he ? a : a.toUpperCase(), richChunks(moves), he ? HEB : ALPHA, he);
    bad += r.bad;
    return mark ? mark(r.text, r.bad) : r.text;
  });
  return { text, bad };
}
(function () {
  const esc = s => s.replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const A = "\uE000", B = "\uE001";
  document.querySelectorAll("pre.computed[data-cipher]").forEach(el => {
    const slips = new Set(JSON.parse(el.dataset.slips || "[]"));
    const out = richDecode(el.dataset.cipher, (w, bad) => (bad || slips.has(w)) ? A + w + B : w).text;
    el.innerHTML = esc(out).split(A).join('<mark class="slip">').split(B).join("</mark>");
  });
  const hg = document.getElementById("hgrid");
  if (hg) hg.innerHTML = [...HEB].map((ch, i) => `<div class="k"><i>${i + 1}</i>${ch}</div>`).join("");
  // the playground decoder understands the new notation too
  const decIn = document.getElementById("dec-in");
  if (decIn && typeof runDec === "function") {
    const oldRun = runDec;
    const richRun = function () {
      const r = richDecode(decIn.value);
      document.getElementById("dec-out").value = r.text;
      document.getElementById("dec-warn").textContent = r.bad ? `${r.bad} move${r.bad > 1 ? "s" : ""} landed off the grid (shown as ?).` : "";
    };
    decIn.removeEventListener("input", oldRun);
    decIn.addEventListener("input", richRun);
    richRun();
  }
})();
// POSTS-JS:END
</script>"""


def splice(s, begin, end, new, anchor_before):
    if begin in s:
        a = s.index(begin)
        b = s.index(end) + len(end)
        return s[:a] + new + s[b:]
    i = s.index(anchor_before)
    return s[:i] + new + "\n" + s[i:]


def main():
    p = os.path.join(HERE, "index.html")
    s = open(p, encoding="utf-8").read()
    s = splice(s, "<!-- POSTS:BEGIN", "<!-- POSTS:END -->", section(), "</main>")
    s = splice(s, "/* POSTS-CSS:BEGIN */", "/* POSTS-CSS:END */", CSS, "</style>")
    if '<script id="posts-js">' in s:
        a = s.index('<script id="posts-js">')
        b = s.index("</script>", a) + len("</script>")
        s = s[:a] + JS + s[b:]
    else:
        s = s.replace("</body>", JS + "\n</body>", 1)
    open(p, "w", encoding="utf-8").write(s)
    print("ok", len(s))


if __name__ == "__main__":
    main()
