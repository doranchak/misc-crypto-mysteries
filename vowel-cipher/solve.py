#!/usr/bin/env python3
"""Vowel cipher solver / verifier.

Ciphertext: E6O4W1E5V5W1E5V5V1V5L2E1L3O1W4V5V3W1E2O4O1E4V6   (typo L5 -> L3 fixed)

Model that decodes it:
  * The cipher letters are the keyword VOWEL standing in for the vowels A E I O U
        A->V  E->O  I->W  O->E  U->L
  * A plaintext letter is written as  <key letter of the nearest vowel at or before it> + <1-based distance>
        T = O,P,Q,R,S,T  -> vowel O (cipher E), 6th letter of the run -> E6
  * V5 (and V6, O5, O6) are never the canonical code of any letter, so they are "spare" codes.
        V5 behaves as a word space; V6 closes the message.

Run:  /opt/homebrew/bin/python3.11 solve.py
"""
import itertools
import re

CT_ORIG = "E6O4W1E5V5W1E5V5V1V5L2E1L5O1W4V5V3W1E2O4O1E4V6"   # as first posted (typo)
CT = "E6O4W1E5V5W1E5V5V1V5L2E1L3O1W4V5V3W1E2O4O1E4V6"        # corrected

A = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
VOWELS = "AEIOU"
KEY = dict(zip(VOWELS, "VOWEL"))        # plaintext vowel -> cipher letter
INV = {v: k for k, v in KEY.items()}    # cipher letter -> plaintext vowel


def code_of(ch):
    """Canonical code of plaintext letter: nearest vowel at/before it + 1-based offset."""
    i = A.index(ch)
    j = i
    while A[j] not in VOWELS:
        j -= 1
    return KEY[A[j]], i - j + 1


CODEBOOK = {ch: code_of(ch) for ch in A}
REVERSE = {v: k for k, v in CODEBOOK.items()}


def decode(ct):
    out = []
    for letter, d in re.findall(r"([A-Z])(\d)", ct):
        d = int(d)
        c = (letter, d)
        if c in REVERSE:
            out.append(REVERSE[c])
        elif c == ("V", 5):
            out.append(" ")
        else:
            out.append("<%s%d>" % c)
    return "".join(out)


if __name__ == "__main__":
    print("codebook (plaintext letter -> code):")
    for ch in A:
        print(" ", ch, "%s%d" % CODEBOOK[ch])
    spare = [(l, d) for l in "VOWEL" for d in range(1, 7) if (l, d) not in REVERSE]
    print("spare (non-canonical) codes with digits 1-6:", ["%s%d" % s for s in spare])
    print()
    print("original :", CT_ORIG, "->", decode(CT_ORIG))
    print("corrected:", CT, "->", decode(CT))

    # how many pairs are canonical?
    pairs = [(a, int(b)) for a, b in re.findall(r"([A-Z])(\d)", CT)]
    canon = [p for p in pairs if p in REVERSE]
    print(len(pairs), "pairs;", len(canon), "canonical;",
          "non-canonical:", ["%s%d" % p for p in pairs if p not in REVERSE])

    # sanity search: all 120 assignments of the 5 cipher letters to AEIOU,
    # reading the digit as offset forward (+) or backward (-) from that vowel
    letters = sorted({a for a, _ in pairs})
    words = {w.strip().upper() for w in open("/usr/share/dict/words")}

    def seg_score(s):
        n = len(s)
        best = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            best[i] = best[i + 1]
            for j in range(i + 2, min(n, i + 14) + 1):
                if s[i:j] in words:
                    best[i] = max(best[i], (j - i) ** 2 + best[j])
        return best[0]

    res = []
    for perm in itertools.permutations(VOWELS, 5):
        m = dict(zip(letters, perm))
        for sign in (1, -1):
            s = "".join(A[(A.index(m[l]) + sign * (d - 1)) % 26] for l, d in pairs)
            res.append((seg_score(s), s, "".join("%s>%s " % (k, v) for k, v in m.items()), sign))
    res.sort(reverse=True)
    print("\nbrute force over 240 (assignment, direction) models; top 3 by dictionary-segmentation score:")
    for r in res[:3]:
        print(" ", r)
