"""Build ../index.html: There's Treasure Inside, Past and Future box (chapter XXVI) report.

Run:  /opt/homebrew/bin/python3.11 build_report.py   (from this work/ directory)
"""
import json, math, html
from grid import GRID_ROWS, R, C, DIRS
from classify import WORDS, MSG, AMBIG_O, STATES, classify, cells_of
from cryptogram import CT, PT, key

wc, mc, cls = classify()

# ---------------------------------------------------------------- grid data
word_list = []
for i, (w, r, c, d, cat) in enumerate(WORDS):
    cells = cells_of(w, r, c, d)
    word_list.append(dict(id=i, w=w, cat=cat, d=d, cells=cells,
                          back=d in ("W",), r=r + 1, c=c + 1))
msg_list = []
for i, (txt, cells) in enumerate(sorted(MSG, key=lambda m: min(m[1]))):
    cells_sorted = sorted(cells)
    raw = "".join(GRID_ROWS[r][c] for r, c in cells_sorted)
    msg_list.append(dict(id=i, txt=txt, cells=cells_sorted, raw=raw,
                         row=min(r for r, _ in cells) + 1))
cell_info = []
for r in range(R):
    row = []
    for c in range(C):
        row.append(dict(ch=GRID_ROWS[r][c], k=cls[(r, c)],
                        words=[i for i, wd in enumerate(word_list) if (r, c) in wd["cells"]],
                        msg=next((m["id"] for m in msg_list if (r, c) in m["cells"]), None),
                        st=STATES.get((r, c))))
    cell_info.append(row)

DATA = dict(cells=cell_info, words=word_list, msgs=msg_list)

# ---------------------------------------------------------------- cryptogram interlinear
def interlinear():
    out = []
    for ct, pt in zip(CT, PT):
        cws, pws = ct.split(" "), pt.split(" ")
        line = []
        for cw, pw in zip(cws, pws):
            cl = "".join(f"<span>{html.escape(ch)}</span>" for ch in cw)
            pl = "".join(f"<span>{html.escape(ch)}</span>" for ch in pw)
            line.append(f'<div class="iw"><div class="ic">{cl}</div><div class="ip">{pl}</div></div>')
        out.append('<div class="il">' + "".join(line) + "</div>")
    return "\n".join(out)

def keytable():
    cs = sorted(key)
    head = "".join(f"<th>{c}</th>" for c in cs)
    body = "".join(f"<td>{key[c].upper()}</td>" for c in cs)
    inv = {p: c for c, p in key.items()}
    ps = sorted(inv)
    head2 = "".join(f"<th>{p.upper()}</th>" for p in ps)
    body2 = "".join(f"<td>{inv[p]}</td>" for p in ps)
    return (f'<table class="key"><tr><th class="rl">cipher</th>{head}</tr><tr><th class="rl">plain</th>{body}</tr></table>'
            f'<table class="key" style="margin-top:8px"><tr><th class="rl">plain</th>{head2}</tr><tr><th class="rl">cipher</th>{body2}</tr></table>')

# ---------------------------------------------------------------- Tahoe geometry SVG
LAT0, LON0 = 39.0, -120.0
def brg(lat1, lon1, lat2, lon2):
    p1, p2 = map(math.radians, (lat1, lat2)); dl = math.radians(lon2 - lon1)
    y = math.sin(dl) * math.cos(p2); x = math.cos(p1) * math.sin(p2) - math.sin(p1) * math.cos(p2) * math.cos(dl)
    return math.degrees(math.atan2(y, x)) % 360
OBLIQUE = brg(39.0, -120.0, 35.0017, -114.6333)      # CA-NV oblique boundary, initial bearing at Tahoe
COIN_UP, COIN_LO = 20.0, 154.9                        # measured (coin_angle2.py, RANSAC; PCA in coin_angle.py gave 20.1/154.7)
COIN_ANG = COIN_LO - COIN_UP

# schematic shoreline (approximate; from known shore towns/landmarks, +-1 km)
SHORE = [(39.237, -120.027), (39.226, -120.000), (39.243, -119.950), (39.197, -119.931), (39.140, -119.935),
         (39.088, -119.940), (39.044, -119.948), (39.004, -119.947), (38.967, -119.951), (38.943, -119.977),
         (38.937, -120.010), (38.940, -120.060), (38.955, -120.085), (38.980, -120.100), (39.036, -120.120),
         (39.085, -120.160), (39.140, -120.152), (39.168, -120.140), (39.190, -120.090), (39.227, -120.080),
         (39.240, -120.050)]
K, CL = 1150.0, math.cos(math.radians(39.0))
LONMIN, LATMAX = -120.26, 39.31
def px(lat, lon): return ((lon - LONMIN) * CL * K + 20, (LATMAX - lat) * K + 20)
def tahoe_svg():
    W, H = px(38.86, -119.80)[0] + 20, px(38.86, -119.80)[1] + 10
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in (px(*p) for p in SHORE))
    vx, vy = px(LAT0, LON0)
    nx, ny = px(LATMAX, LON0)
    L = 380
    def ray(b, length=L):
        return vx + length * math.sin(math.radians(b)), vy - length * math.cos(math.radians(b))
    ox, oy = ray(OBLIQUE); cx_, cy_ = ray(COIN_ANG, 300)
    sx, sy = px(38.967, -119.951)
    g = []
    g.append(f'<svg viewBox="0 0 {W:.0f} {H:.0f}" class="map" role="img" aria-label="Schematic of Lake Tahoe with the California-Nevada border angle point at 39N 120W">')
    g.append(f'<rect x="0" y="0" width="{W:.0f}" height="{H:.0f}" fill="#f6f4ee"/>')
    # graticule
    for lat in (38.9, 39.0, 39.1, 39.2, 39.3):
        x1, y1 = px(lat, LONMIN); x2, _ = px(lat, -119.80)
        g.append(f'<line x1="{x1:.0f}" y1="{y1:.1f}" x2="{x2:.0f}" y2="{y1:.1f}" class="grat"/>'
                 f'<text x="{x2-4:.0f}" y="{y1-3:.1f}" class="gl" text-anchor="end">{lat:.1f}°N</text>')
    for lon in (-120.2, -120.1, -120.0, -119.9):
        x1, y1 = px(LATMAX, lon); _, y2 = px(38.86, lon)
        g.append(f'<line x1="{x1:.1f}" y1="{y1:.0f}" x2="{x1:.1f}" y2="{y2:.0f}" class="grat"/>'
                 f'<text x="{x1+3:.1f}" y="{y2-4:.0f}" class="gl">{-lon:.1f}°W</text>')
    g.append(f'<polygon points="{pts}" class="lake"/>')
    g.append(f'<text x="{px(39.17,-120.125)[0]:.0f}" y="{px(39.17,-120.125)[1]:.0f}" class="lk">Lake Tahoe</text>')
    g.append(f'<text x="{px(39.17,-120.125)[0]:.0f}" y="{px(39.17,-120.125)[1]+15:.0f}" class="gl">(outline schematic)</text>')
    # border
    g.append(f'<line x1="{nx:.1f}" y1="{ny:.1f}" x2="{vx:.1f}" y2="{vy:.1f}" class="border"/>')
    g.append(f'<line x1="{vx:.1f}" y1="{vy:.1f}" x2="{ox:.1f}" y2="{oy:.1f}" class="border"/>')
    g.append(f'<line x1="{vx:.1f}" y1="{vy:.1f}" x2="{cx_:.1f}" y2="{cy_:.1f}" class="coinray"/>')
    g.append(f'<circle cx="{vx:.1f}" cy="{vy:.1f}" r="13" class="hub"/>')
    g.append(f'<circle cx="{vx:.1f}" cy="{vy:.1f}" r="4" class="vtx"/>')
    g.append(f'<text x="{vx-12:.0f}" y="{vy-20:.0f}" class="lab" text-anchor="end">39°00′N 120°00′W</text>')
    g.append(f'<text x="{vx-12:.0f}" y="{vy-6:.0f}" class="gl" text-anchor="end">CA–NV border angle point</text>')
    g.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="4" class="town"/>'
             f'<text x="{sx+8:.0f}" y="{sy+4:.0f}" class="lab">Stateline, NV (approx.)</text>')
    g.append(f'<text x="{px(39.27,-120.24)[0]:.0f}" y="{px(39.27,-120.24)[1]:.0f}" class="st">CALIFORNIA</text>')
    g.append(f'<text x="{px(39.27,-119.975)[0]:.0f}" y="{px(39.27,-119.975)[1]:.0f}" class="st">NEVADA</text>')
    # angle annotations
    g.append(f'<text x="{ox-110:.0f}" y="{oy-8:.0f}" class="lab">border: {OBLIQUE:.1f}° from N</text>')
    g.append(f'<text x="{cx_-30:.0f}" y="{cy_+18:.0f}" class="lab coin">coin lines: {COIN_ANG:.1f}° apart</text>')
    g.append('</svg>')
    return "\n".join(g)

# coin with measured lines (RANSAC fit in coin_angle2.py, crop coords of assets/coin_front.jpg)
import numpy as np
_L = np.load("coin_lines.npy")
VX, VY = _L[2][0], _L[2][1]
_tips = {round(_L[i][4], 1): (_L[i][2], _L[i][3]) for i in range(2)}
def coin_svg(rotate=0.0, draw_border=False, size=420):
    def rot(x, y):
        a = math.radians(rotate); dx, dy = x - VX, y - VY
        return VX + dx * math.cos(a) - dy * math.sin(a), VY + dx * math.sin(a) + dy * math.cos(a)
    cid = f"cc{int(abs(rotate)*10)}{int(draw_border)}"
    s = [f'<svg viewBox="0 0 420 420" width="{size}" class="coin" role="img" aria-label="Commemorative coin with fitted line overlay">',
         f'<defs><clipPath id="{cid}"><circle cx="210" cy="205" r="200"/></clipPath></defs>',
         f'<g clip-path="url(#{cid})"><image href="assets/coin_front.jpg" x="0" y="0" width="420" height="420" '
         f'transform="rotate({rotate:.2f} {VX:.1f} {VY:.1f})"/></g>']
    for b, (tx, ty) in _tips.items():
        x2, y2 = rot(tx, ty)
        s.append(f'<line x1="{VX:.1f}" y1="{VY:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="fit"/>')
    if draw_border:
        n = (VX, VY - 185)
        ob = (VX + 200 * math.sin(math.radians(OBLIQUE)), VY - 200 * math.cos(math.radians(OBLIQUE)))
        s.append(f'<line x1="{VX:.1f}" y1="{VY:.1f}" x2="{n[0]:.1f}" y2="{n[1]:.1f}" class="border thin"/>')
        s.append(f'<line x1="{VX:.1f}" y1="{VY:.1f}" x2="{ob[0]:.1f}" y2="{ob[1]:.1f}" class="border thin"/>')
    s.append(f'<circle cx="{VX:.1f}" cy="{VY:.1f}" r="3.5" fill="#e0a100"/>')
    s.append('</svg>')
    return "\n".join(s)

# ---------------------------------------------------------------- TN/NC/SC schematic
def states_svg():
    # left: grid excerpt rows 6-11 (0-based 5..10) cols 6..15 ; right: real state centroids
    r0, r1, c0, c1, S = 5, 11, 5, 15, 34
    g = [f'<svg viewBox="0 0 {(c1-c0+1)*S+330} {(r1-r0+1)*S+40}" class="stsvg" role="img" aria-label="TN, NC, SC letters in the grid compared with real state positions">']
    for r in range(r0, r1 + 1):
        for c in range(c0, c1 + 1):
            x, y = (c - c0) * S + 10, (r - r0) * S + 10
            k = cls[(r, c)]
            fill = {"state": "#eb6834", "word": "#d7e6f8", "msg": "#d2f0e4", "spareO": "#fff", "ambig": "#fff"}.get(k, "#eee")
            stroke = "#c9ced3"
            g.append(f'<rect x="{x}" y="{y}" width="{S-2}" height="{S-2}" rx="3" fill="{fill}" stroke="{stroke}"/>')
            col = "#fff" if k == "state" else "#1d232b"
            g.append(f'<text x="{x+S/2-1}" y="{y+S/2+5}" text-anchor="middle" class="gc" fill="{col}">{GRID_ROWS[r][c]}</text>')
    # STATE diagonal
    sx0, sy0 = (7 - c0) * S + 10 + S / 2 - 1, (6 - r0) * S + 10 + S / 2 - 1
    sx1, sy1 = (11 - c0) * S + 10 + S / 2 - 1, (10 - r0) * S + 10 + S / 2 - 1
    g.append(f'<line x1="{sx0}" y1="{sy0}" x2="{sx1}" y2="{sy1}" stroke="#2a78d6" stroke-width="3" stroke-linecap="round" opacity=".55"/>')
    g.append(f'<text x="10" y="{(r1-r0+1)*S+30}" class="gl">grid rows {r0+1}–{r1+1}, cols {c0+1}–{c1+1}; blue line = STATE (diagonal)</text>')
    # real centroids (approx.)
    ox = (c1 - c0 + 1) * S + 40
    cent = {"TN": (35.86, -86.35), "NC": (35.56, -79.39), "SC": (33.92, -80.90), "GA": (32.68, -83.22), "KY": (37.53, -85.30), "VA": (37.52, -78.85)}
    def pp(lat, lon): return ox + (lon + 90.5) * 19, 20 + (38.5 - lat) * 30
    g.append(f'<rect x="{ox-10}" y="5" width="300" height="{(r1-r0+1)*S+10}" fill="#f6f4ee" rx="6"/>')
    for st, (la, lo) in cent.items():
        x, y = pp(la, lo)
        main = st in ("TN", "NC", "SC")
        g.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{6 if main else 4}" fill="{"#eb6834" if main else "#9aa3ab"}"/>'
                 f'<text x="{x+9:.0f}" y="{y+5:.0f}" class="{"lab" if main else "gl"}">{st}</text>')
    g.append(f'<text x="{ox}" y="{(r1-r0+1)*S+30}" class="gl">real state centroids (approx.), same orientation</text>')
    g.append('</svg>')
    return "\n".join(g)

# ---------------------------------------------------------------- tables
def words_table():
    rows = []
    catname = {"number": "number", "direction": "direction", "colour": "colour / gem", "place": "terrain / place", "other": "other"}
    dirname = {"E": "→ left-to-right", "W": "← backward", "S": "↓ down", "NE": "↗ diagonal up", "SE": "↘ diagonal down"}
    notes = {
        "NINE": "read backward from R1C12; its final E (R1C9) is the only non-random cell in row 1 not otherwise used",
        "NINETEEN": "= number of spare O's in the message zone (see COUNT)",
        "COUNT": "Holy Grail echo with THREE / FIVE (“Five is right out”); also “count the O's” → NINETEEN",
        "ESTATE": "row 6 backward; may be intended as STATE (R6C6→R6C2) with E shared with THREE",
        "DIVIDE": "could be DIVIDER (R13C18 R shared with QUARRY)",
        "LEMON": "the alternative OMELET (same diagonal) collides with message letters, so LEMON is the placed word",
        "STATE": "diagonal; its T (R10C11) sits exactly between the TN and NC letters",
        "THREE": "",
    }
    for wd in word_list:
        n = notes.get(wd["w"], "")
        if wd["w"] == "THREE":
            n = "column 7, down" if wd["d"] == "S" else "row 12, backward"
        rows.append(f'<tr data-w="{wd["id"]}"><td class="wd">{wd["w"]}</td><td>{catname[wd["cat"]]}</td>'
                    f'<td class="mono">R{wd["r"]}C{wd["c"]}</td><td>{dirname[wd["d"]]}</td><td class="small">{html.escape(n)}</td></tr>')
    return "\n".join(rows)

def msg_table():
    rows = []
    for m in msg_list:
        cells = m["cells"]
        loc = ", ".join(f"R{r+1}C{c+1}" for r, c in (cells[0], cells[-1]))
        rows.append(f'<tr data-m="{m["id"]}"><td class="mono">{m["raw"]}</td><td class="pt">{m["txt"]}</td><td class="mono small">{loc}</td></tr>')
    return "\n".join(rows)

counts = {}
for v in cls.values(): counts[v] = counts.get(v, 0) + 1

HTML = open("template.html", encoding="utf-8").read()
for k, v in {
    "%%DATA%%": json.dumps(DATA, separators=(",", ":")),
    "%%INTERLINEAR%%": interlinear(),
    "%%KEYTABLE%%": keytable(),
    "%%TAHOE%%": tahoe_svg(),
    "%%COIN_RAW%%": coin_svg(0.0, size=300),
    "%%COIN_ROT%%": coin_svg(-COIN_UP, draw_border=True, size=300),
    "%%STATES%%": states_svg(),
    "%%WORDS_TABLE%%": words_table(),
    "%%MSG_TABLE%%": msg_table(),
    "%%N_MSG%%": str(counts["msg"]), "%%N_WORD%%": str(counts["word"]), "%%N_RAND%%": str(counts["random"]),
    "%%N_SPARE%%": str(counts["spareO"]), "%%N_AMBIG%%": str(counts["ambig"]), "%%N_STATE%%": str(counts["state"]),
    "%%OBLIQUE%%": f"{OBLIQUE:.1f}", "%%COIN_ANG%%": f"{COIN_ANG:.1f}", "%%COIN_UP%%": f"{COIN_UP:.1f}", "%%COIN_LO%%": f"{COIN_LO:.1f}",
}.items():
    HTML = HTML.replace(k, v)
assert "%%" not in HTML, HTML[HTML.index("%%") - 50: HTML.index("%%") + 50]
open("../index.html", "w", encoding="utf-8").write(HTML)
print("wrote ../index.html", len(HTML), "bytes;", counts)
