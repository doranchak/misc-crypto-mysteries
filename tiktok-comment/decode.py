"""Decoder for the @syugyulgyo grid-walk cipher (TikTok).

System (see index.html): letters sit in a 5-wide grid in alphabet order.
Each word = plain anchor letter + '|'-separated chunks; each chunk is a move
relative to the previous letter ("n" before an arrow multiplies it).

Extensions seen in the later posts:
  0        repeat the previous letter (doubled letter, e.g. НН)
  ⟳        go back to the letter before the previous one (КА⟳ = КАК)
  [x]²     do chunk x twice (two letters)
  -        hyphen inside a token starts a new anchor (ИЗ-ЗА, КАКИЕ-ТО)
  Hebrew   same rule on the 27-letter Hebrew alphabet (finals in place),
           laid out right-to-left, so → means "one letter back".
  Latin    some anchors are typed with Latin letters (B = Б or В, H = Н,
           P = П or Р, C = С, Ch = Ч, Zh = Ж ...); every candidate is tried.
"""
import re
import sys

RU = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
HE = "אבגדהוזחטיכךלמםנןסעפףצץקרשת"
W = 5

LATIN = {
    "A": "А", "B": "БВ", "C": "СЦЧ", "D": "Д", "E": "ЕЭ", "F": "Ф", "G": "Г",
    "H": "НХ", "I": "ИЙ", "J": "Й", "K": "К", "L": "Л", "M": "М", "N": "Н",
    "O": "О", "P": "ПР", "R": "Р", "S": "С", "T": "Т", "U": "У", "V": "В",
    "W": "ЖЗШВЩ", "X": "Х", "Y": "УЫЙ", "Z": "З", "Ë": "Ё",
}
DIGRAPH = {"Ch": "Ч", "CH": "Ч", "Zh": "Ж", "ZH": "Ж", "Sh": "Ш", "SH": "Ш"}

ARROWS = {"↑": (-1, 0), "↓": (1, 0), "←": (0, -1), "→": (0, 1)}
LETTER_RE = r"(?:Ch|CH|Zh|ZH|Sh|SH|[А-ЯЁа-яёA-Za-zËא-ת])"
MOVE_CHARS = "0123456789↑↓←→|⟳[]²³"
SEG_RE = re.compile(r"(" + LETTER_RE + r")([" + re.escape(MOVE_CHARS) + r"]*)")


def script_of(ch):
    if re.match(r"[א-ת]", ch):
        return "he"
    return "ru"


def anchor_candidates(a):
    if a in DIGRAPH:
        return DIGRAPH[a]
    if re.match(r"[А-ЯЁа-яё]", a):
        return a.upper()
    if re.match(r"[א-ת]", a):
        return a
    return LATIN.get(a.upper(), "")


def split_chunks(moves):
    """'3↑←⟳|[2←]²|0' -> ['3↑←', '⟳', '2←', '2←', '0']"""
    out = []
    for part in moves.split("|"):
        if part == "":
            continue
        # expand [x]² / [x]³
        def rep(m):
            k = 2 if m.group(2) == "²" else 3
            return "|".join([m.group(1)] * k)
        part = re.sub(r"\[([^\]]*)\]([²³])", rep, part)
        for p in part.split("|"):
            # a trailing/leading ⟳ is its own chunk
            pieces = re.split(r"(⟳)", p)
            out += [x for x in pieces if x]
    return out


def chunk_delta(ch, rtl=False):
    dr = dc = 0
    for m in re.finditer(r"(\d*)([↑↓←→])", ch):
        n = int(m.group(1)) if m.group(1) else 1
        r, c = ARROWS[m.group(2)]
        if rtl:
            c = -c
        dr += r * n
        dc += c * n
    leftover = re.sub(r"(\d*)([↑↓←→])", "", ch)
    return dr, dc, leftover


def letter_at(alpha, r, c):
    if r < 0 or c < 0 or c >= W:
        return None
    i = r * W + c
    return alpha[i] if i < len(alpha) else None


def walk(anchor, chunks, alpha, rtl=False, loop_stays=False):
    """Return (text, bad_steps, notes). '?' marks a move off the grid."""
    i = alpha.index(anchor)
    pos = [(i // W, i % W)]  # history of positions (virtual, may be off-grid)
    text = anchor
    bad = 0
    cur = pos[0]
    for ch in chunks:
        if ch == "0":
            text += text[-1]
            pos.append(cur)
            continue
        if ch == "⟳":
            back = pos[-2] if len(pos) >= 2 else pos[-1]
            L = letter_at(alpha, *back)
            text += L or "?"
            if not loop_stays:
                cur = back
            pos.append(cur if loop_stays else back)
            continue
        dr, dc, left = chunk_delta(ch, rtl)
        if left.strip():
            text += "⁇"
            bad += 1
            continue
        cur = (cur[0] + dr, cur[1] + dc)
        L = letter_at(alpha, *cur)
        if L is None:
            bad += 1
        text += L or "?"
        pos.append(cur)
    return text, bad


def decode_segment(anchor_raw, moves):
    cands = anchor_candidates(anchor_raw)
    if not cands:
        return [(anchor_raw + moves, 0, anchor_raw)]
    sc = script_of(cands[0])
    alpha = HE if sc == "he" else RU
    chunks = split_chunks(moves)
    res = []
    for a in cands:
        if a not in alpha:
            continue
        for stays in (False, True):
            if stays and "⟳" not in chunks:
                continue
            t, bad = walk(a, chunks, alpha, rtl=(sc == "he"), loop_stays=stays)
            res.append((t, bad, a + (" ⟳stay" if stays else "")))
    # dedupe keep order
    seen, out = set(), []
    for r in res:
        if r[0] not in seen:
            seen.add(r[0])
            out.append(r)
    out.sort(key=lambda r: r[1])
    return out


def strict_decode(s):
    """Decode with the plain rules only (first anchor candidate, ⟳ always
    returns to the earlier letter). Same output as the page's live decoder."""
    def seg(m):
        cands = anchor_candidates(m.group(1))
        if not cands:
            return m.group(0)
        a = cands[0]
        he = script_of(a) == "he"
        return walk(a, split_chunks(m.group(2)), HE if he else RU, rtl=he)[0]
    return STRICT_RE.sub(seg, s)


STRICT_RE = re.compile(r"([А-ЯЁа-яёא-ת])([" + re.escape(MOVE_CHARS) + r"]*)")


EMOTICONS = [">:3", ":3", ":D", ":Ρ", ":P", ":(", ":)", ";)", "xD", "XD"]


def decode_token(tok):
    """Return list of alternatives for a whitespace token: [(text, bad)]"""
    # protect emoticons
    prot = {}
    for k, e in enumerate(EMOTICONS):
        if e in tok:
            key = "\x00%d\x00" % k
            tok = tok.replace(e, key)
            prot[key] = e
    pieces = []  # list of lists of alternatives
    pos = 0
    for m in SEG_RE.finditer(tok):
        if m.start() > pos:
            pieces.append([(tok[pos:m.start()], 0, "")])
        pieces.append(decode_segment(m.group(1), m.group(2)))
        pos = m.end()
    if pos < len(tok):
        pieces.append([(tok[pos:], 0, "")])
    # combine: best alternative per piece, plus list of alternates
    best = "".join(p[0][0] for p in pieces)
    bad = sum(p[0][1] for p in pieces)
    alts = [p for p in pieces if len(p) > 1]
    for key, e in prot.items():
        best = best.replace(key, e)
    return best, bad, alts


def decode_text(s):
    out = []
    notes = []
    for tok in re.split(r"(\s+)", s):
        if tok == "" or tok.isspace():
            out.append(tok)
            continue
        best, bad, alts = decode_token(tok)
        out.append(best)
        if bad or alts:
            notes.append((tok, best, bad, alts))
    return "".join(out), notes


if __name__ == "__main__":
    src = open(sys.argv[1], encoding="utf-8").read() if len(sys.argv) > 1 else sys.stdin.read()
    for line in src.splitlines():
        if not line.strip():
            continue
        text, notes = decode_text(line)
        print(text)
        for tok, best, bad, alts in notes:
            a = " | ".join(",".join(f"{t}({b})" for t, b, _ in p) for p in alts)
            print(f"    !! {tok} -> {best} bad={bad} alts: {a}")
        print()
