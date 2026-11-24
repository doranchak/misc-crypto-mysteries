#!/usr/bin/env python3
"""Builds five.bin (26^5 float32 table) from the Wortschatz 5-gram list shipped with AZdecrypt Lite:
   ~/projects/github/azdecrypt-lite/5-grams_english_wortschatz.txt
   Most exploration scripts in this folder read ./five.bin (score = sum of 5-gram table values)."""
import re, array, sys
src = sys.argv[1] if len(sys.argv) > 1 else '/Users/doranchak/projects/github/azdecrypt-lite/5-grams_english_wortschatz.txt'
txt = open(src).read()
arr = array.array('f', [0.0]) * (26**5)
for g, v in re.findall(r'([A-Z]{5})(\d+)', txt):
    i = 0
    for ch in g: i = i*26 + ord(ch) - 65
    arr[i] = float(v)
open('five.bin', 'wb').write(arr.tobytes())
