#!/usr/bin/env python3
"""
r/codes "Base 64 and Ceasar ciper" (u/Anxious-Anything-894)
https://www.reddit.com/r/codes/comments/1xwccu7/base_64_and_ceasar_ciper/

Pipeline recovered:
  1. Base64 (RFC 4648)  -> the OP's "RFC 1111011111101111011111111" hint is unary run-lengths
     (1111=4, 111111=6, 1111=4, 11111111=8, 0 = separator) => "RFC 4648".
  2. Caesar, shift 6    -> header "(6 SAYS)".  Decoding every LETTER by -6 turns the 12
     lowercase letters (t o i k i u s v r k z k) into  "nicecomplete".
  3. The uppercase letters / digits / '^' '"' '-' are filler (not decodable as English).

Usage: python3 solve.py
"""
import base64
import collections
import math
import string

CT = ("ICg2IFNBWVMpICBKMU9PSHRNSk5EXlhYVFE1MFJWQm8xOCI1XlNTVVJXSEZQTEpBaUsKayIiMFpaUVlZLVRUQ0NN"
      "UVlOUExIaUxKWFR1TU1NTkNDUFdXVk1Zc0xNTFZWdlZHTEleXl5eXl5eXl5BVExNTk8wMTNya3prRk9TTkpQWlo=")

# What the cipher.jpg shows, read by eye (sans font: I/l and O/0 are ambiguous).
IMAGE_READING = ("lCg2lFNBWVMplCBKMU9PSHRNSk5EXlhYVFE1MFJWQm8x0Cl1XlNTVVJXSEZQTEpBaUsKayli"
                 "MFpaUVlZLVRUQ0NNUVlOUExIaUxKWFR1TU1NTkNDUFdXVk1Zc0xNTFZWdlZHTEleXl5eXl5eXl5"
                 "BVExNTk8wMTNya3prRk9TTkpQWlo=")

RFC_BITS = "1111011111101111011111111"

ENGLISH = dict(zip(string.ascii_lowercase, [
    8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153, 0.772, 4.025, 2.406,
    6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074]))


def shift_letters(text, k):
    """Caesar-shift letters by k (case preserved); everything else is left alone."""
    out = []
    for c in text:
        if "a" <= c <= "z":
            out.append(chr((ord(c) - 97 + k) % 26 + 97))
        elif "A" <= c <= "Z":
            out.append(chr((ord(c) - 65 + k) % 26 + 65))
        else:
            out.append(c)
    return "".join(out)


def loglik(s):
    return sum(math.log(ENGLISH[c] / 100) for c in s)


def main():
    # --- transcription sanity check: paste vs image reading, modulo I/l and O/0 glyph ambiguity
    norm = lambda s: s.replace("l", "I").replace("0", "O")
    assert len(CT) == len(IMAGE_READING)
    diffs = [(i, a, b) for i, (a, b) in enumerate(zip(CT, IMAGE_READING)) if a != b]
    assert all(norm(a) == norm(b) for _, a, b in diffs), "transcriptions disagree beyond I/l, O/0"
    print(f"paste vs image: {len(diffs)} glyph-ambiguity differences only (I/l, O/0)")

    # --- step 1: the RFC hint
    runs = [len(r) for r in RFC_BITS.split("0")]
    print("RFC hint run-lengths:", runs, "-> RFC", "".join(map(str, runs)))

    # --- step 1: Base64
    raw = base64.b64decode(CT)
    t = raw.decode("latin1")
    print(f"\nBase64 -> {len(raw)} bytes")
    print(repr(t))
    header, body = t[:11], t[11:]
    print("header:", repr(header), "| body:", len(body), "chars (incl. 1 newline)")

    # --- step 2: Caesar on the body
    low = "".join(c for c in body if c.islower())
    print("\nlowercase letters in body:", low)
    print("shift  decoded lowercase   English log-likelihood")
    rows = []
    for k in range(26):
        d = shift_letters(low, -k)
        rows.append((loglik(d), k, d))
    for ll, k, d in sorted(rows, reverse=True)[:5]:
        print(f"  {k:2d}   {d:14s}  {ll:7.1f}")
    best = max(rows)
    print(f"\nbest shift = {best[1]}  ->  {best[2]!r}")

    print("\nfull body decoded with letters shifted by -6 (case kept):")
    print(shift_letters(body, -6))

    # --- filler statistics
    up = [c for c in body if c.isupper()]
    dig = [c for c in body if c.isdigit()]
    sym = [c for c in body if not c.isalnum() and c != "\n"]
    print(f"\nfiller: {len(up)} uppercase, {len(dig)} digits ({''.join(dig)}), "
          f"{len(sym)} symbols ({''.join(sym)})")
    letters = [c for c in body if c.isalpha()]
    dbl = sum(1 for a, b in zip(body, body[1:]) if a == b and a.isalpha())
    print(f"adjacent doubled letters: {dbl}/{len(letters) - 1} = {dbl / (len(letters) - 1):.1%} (English ~3%)")
    cnt = collections.Counter(up)
    ic = sum(v * (v - 1) for v in cnt.values()) / (len(up) * (len(up) - 1))
    print(f"uppercase-only index of coincidence: {ic:.4f} (English 0.066, random 0.038)")


if __name__ == "__main__":
    main()
