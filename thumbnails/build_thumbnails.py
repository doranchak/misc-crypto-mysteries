#!/usr/bin/env python3
"""Build the README thumbnails (360x240 JPEG, shown at 180x120).

Each entry crops a box from a source image in the repo, grows the box to
3:2 around its centre (padding with a background colour when the image
runs out), and downsizes it.  Text-only reports have no source image, so
their entries crop from a 2x headless-Chrome screenshot of the report
(see SHOTS below); those screenshots are not committed.

Run from the repo root:
    python3 thumbnails/build_thumbnails.py [screenshot_dir]
"""
import os
import subprocess
import sys
import tempfile

from PIL import Image

W, H = 360, 240
OUT = "thumbnails"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Reports with no picture of their own: render them at 2x and crop.
# name -> (report page, window height in CSS px)
SHOTS = {
    "caesar-shift-per-word": ("caesar-shift-per-word/index.html", 1800),
    "friend-two-ciphers-base64-caesar": ("friend-two-ciphers-base64-caesar/index.html", 1800),
    "giokku-sci-fi-story-cipher": ("giokku-sci-fi-story-cipher/index.html", 2300),
    "juniorappearance8347-pdf-password-puzzle": ("juniorappearance8347-pdf-password-puzzle/index.html", 1800),
    "solid-camp6739-code": ("solid-camp6739-code/index.html", 1800),
    "tbstewa-custom-cipher": ("tbstewa-custom-cipher/report.html", 1800),
    "vowel-cipher": ("vowel-cipher/index.html", 1800),
}

# name -> (source, box (x0, y0, x1, y1) in source px, pad colour or None)
# A source of "shot:" means the 2x screenshot; its box is given in CSS px.
SPEC = {
    "1901-theology-book-note": ("1901-theology-book-note/note 2.webp", (30, 150, 1000, 797), None),
    "artfight-odd-cipher": ("artfight-odd-cipher/images/profile-highlighted.png", (0, 0, 403, 150), "auto"),
    "base-64-and-caesar-cipher": ("base-64-and-caesar-cipher/cipher.jpg", (0, 0, 640, 427), None),
    "friend-two-ciphers-base64-caesar": ("shot:", (130, 280, 655, 630), None),
    "bulgarian-treasure-hunt-cipher": ("bulgarian-treasure-hunt-cipher/card.jpg", (125, 0, 1475, 900), None),
    "spanish-class-checkerboard-cipher": ("spanish-class-checkerboard-cipher/pic1.jpeg", (100, 150, 2900, 2017), None),
    "cipher-leads-to-an-image": ("cipher-leads-to-an-image/qkhHnIc.png", (180, 420, 1950, 1960), "auto"),
    "disturbed-student-enciphered-journal": ("disturbed-student-enciphered-journal/page 1.webp", (40, 60, 1040, 727), None),
    "oliver-twist-thrift-store": ("oliver-twist-thrift-store/book1.jpeg", (150, 250, 2900, 2083), None),
    "gareth-penn-crypto-curiosities": ("gareth-penn-crypto-curiosities/images/times17-cover.jpg", (6, 72, 794, 598), None),
    "giokku-sci-fi-story-cipher": ("shot:", (120, 1430, 760, 1857), None),
    "mock-trial-cipher": ("mock-trial-cipher/original.png", (0, 0, 600, 400), None),
    "juniorappearance8347-pdf-password-puzzle": ("shot:", (190, 150, 760, 530), None),
    "pigpen-notebook-cipher": ("pigpen-notebook-cipher/original.png", (450, 950, 2700, 2450), None),
    "caesar-shift-per-word": ("shot:", (120, 1000, 1080, 1640), None),
    "solid-camp6739-code": ("shot:", (135, 840, 615, 1160), None),
    "tbstewa-custom-cipher": ("shot:", (120, 225, 720, 625), None),
    "tech-tools-substitution-cipher": ("tech-tools-substitution-cipher/images/cipher.png", (0, 0, 1074, 716), None),
    "the-lost-spiral": ("the-lost-spiral/lost-spiral.png", (0, 0, 790, 863), "auto"),
    "tiktok-comment": ("tiktok-comment/code.jpeg", (0, 0, 1080, 423), "auto"),
    "vowel-cipher": ("shot:", (130, 360, 565, 650), None),
    "weird-message-from-a-strange-guy": ("weird-message-from-a-strange-guy/message.webp", (0, 0, 1080, 720), None),
    "xmr-monero-wallet": ("xmr-monero-wallet/cipher.png", (0, 0, 897, 598), None),
    "z340-inspired-art-codes": ("z340-inspired-art-codes/pic 1.webp", (0, 10, 1080, 730), None),
    "zodiac-hat": ("zodiac-hat/hat1.webp", (80, 60, 1060, 713), None),
}


def screenshot(name, shot_dir):
    path = os.path.join(shot_dir, name + ".png")
    if not os.path.exists(path):
        page, height = SHOTS[name]
        url = "file://" + os.path.abspath(page)
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
                        "--hide-scrollbars", "--force-device-scale-factor=2",
                        "--virtual-time-budget=6000", f"--window-size=1200,{height}",
                        f"--screenshot={path}", url],
                       check=True, stderr=subprocess.DEVNULL)
    return path


def fit_box(box, iw, ih):
    """Grow box to 3:2 about its centre; shift it to stay inside the image."""
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    if bw / bh < W / H:
        bw = bh * W / H
    else:
        bh = bw * H / W
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    x0, y0 = cx - bw / 2, cy - bh / 2
    # slide back inside where the image is big enough
    if bw <= iw:
        x0 = min(max(x0, 0), iw - bw)
    if bh <= ih:
        y0 = min(max(y0, 0), ih - bh)
    return x0, y0, x0 + bw, y0 + bh


def build(name, shot_dir):
    src, box, pad = SPEC[name]
    if src == "shot:":
        im = Image.open(screenshot(name, shot_dir)).convert("RGB")
        box = tuple(2 * v for v in box)
    else:
        im = Image.open(src).convert("RGB")
    x0, y0, x1, y1 = fit_box(box, *im.size)
    if pad == "auto":
        pad = im.getpixel((1, 1))
    canvas = Image.new("RGB", (round(x1 - x0), round(y1 - y0)), pad or (255, 255, 255))
    # paste the part of the image that falls inside the box
    cx0, cy0 = max(0, round(x0)), max(0, round(y0))
    cx1, cy1 = min(im.width, round(x1)), min(im.height, round(y1))
    canvas.paste(im.crop((cx0, cy0, cx1, cy1)), (cx0 - round(x0), cy0 - round(y0)))
    thumb = canvas.resize((W, H), Image.LANCZOS)
    out = os.path.join(OUT, name + ".jpg")
    thumb.save(out, "JPEG", quality=85, optimize=True, progressive=True)
    return out


def main():
    if len(sys.argv) > 1:
        shot_dir = sys.argv[1]
        os.makedirs(shot_dir, exist_ok=True)
    else:
        shot_dir = tempfile.mkdtemp(prefix="readme-shots-")
    for name in SPEC:
        out = build(name, shot_dir)
        print(f"{out}  {os.path.getsize(out) // 1024} KB")


if __name__ == "__main__":
    main()
