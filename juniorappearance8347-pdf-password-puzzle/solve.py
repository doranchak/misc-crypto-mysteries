#!/usr/bin/env python3
"""Solver for the juniorappearance8347 PDF-password puzzle (hints: BACON, HEX, BIBLE).
Usage: python3 solve.py decode1.txt decode1.pdf
Decodes the puzzle text, then tests ONLY the password(s) the puzzle points to using qpdf.
"""
import subprocess, sys

txt, pdf = sys.argv[1], sys.argv[2]
lines = [l for l in open(txt, 'rb').read().decode('ascii').replace('\r', '').split('\n') if l.strip()]

# 1. HEX -> text. A 4-digit token "2013" is U+2013 (EN DASH), i.e. a verse range.
def hexline(l):
    out = ''
    for tk in l.split():
        out += chr(int(tk, 16)) if len(tk) == 2 else ('–' if tk == '2013' else '?')
    return out
refs = [hexline(l).replace('–', '-') for l in lines[:2]]
print('Bible references:', refs)

# 2. BACON (24-letter alphabet, I=J and U=V)
ALPHA = 'ABCDEFGHIKLMNOPQRSTUWXYZ'
bacon = ''.join(ALPHA[int(g.replace('a', '0').replace('b', '1'), 2)] for g in lines[2].split())
print('Bacon:', bacon)                     # FINDTHECOMMONTHING

# 3. Common thing = "seven" (3x in Gen 2:2-3, 5x in Lev 25:8-10 = 8x, matching the trailing "8x").
#    The password is therefore the digit 7 written 8 times.
password = '7' * 8
r = subprocess.run(['qpdf', '--check', f'--password={password}', pdf], capture_output=True, text=True)
print('password', repr(password), '->', 'OPENS' if r.returncode in (0, 3) else 'fails')
