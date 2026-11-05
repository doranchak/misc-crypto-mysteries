#!/usr/bin/env python3
"""Decode the Bulgarian treasure-hunt business-card grid (18 x 10 moon glyphs).

Source thread: https://www.reddit.com/r/codes/comments/1xg9me4/unsolved_grid_cypher/

Rules (from the solving comment):
  1. Read the grid as a snake ("boustrophedon"): row 1 left->right, row 2
     right->left, row 3 left->right, ... down to the bottom-right.
  2. In that order:   ○        = dot
                      ● ● ●    = dash
                      ◐◐◐ / ◑◑◑ (any three half-moons) = gap between letters
  3. Read the dots/dashes as International Morse code.

Usage:  python3 decode.py [grid.txt]
No third-party packages needed.
"""
import sys
from pathlib import Path

MORSE = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F',
    '--.': 'G', '....': 'H', '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L',
    '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P', '--.-': 'Q', '.-.': 'R',
    '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X',
    '-.--': 'Y', '--..': 'Z',
    '-----': '0', '.----': '1', '..---': '2', '...--': '3', '....-': '4',
    '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9',
    '.--.-.': '@', '.-.-.-': '.',
}


def load(path):
    rows = [line.split() for line in Path(path).read_text(encoding='utf-8').splitlines() if line.strip()]
    assert len({len(r) for r in rows}) == 1, 'rows must all have the same length'
    return rows


def reading_order(rows, snake=True):
    seq = []
    for i, row in enumerate(rows):
        seq += row[::-1] if (snake and i % 2) else row
    return seq


def to_morse(seq):
    """Tolerant tokeniser: '?' marks a run of glyphs that is not a multiple of 3."""
    out, i = [], 0
    while i < len(seq):
        c, j = seq[i], i
        same = (lambda x: x == c) if c in '○●' else (lambda x: x in '◐◑')
        while j < len(seq) and same(seq[j]):
            j += 1
        n = j - i
        if c == '○':
            out += ['.'] * n
        elif c == '●':
            out += ['-'] * (n // 3) + ['?'] * (n % 3)
        else:
            out += [' '] * (n // 3) + ['?'] * (n % 3)
        i = j
    return ''.join(out)


def to_text(morse):
    return ''.join(MORSE.get(code, '?') for code in morse.split(' '))


if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else Path(__file__).with_name('grid.txt')
    rows = load(path)
    print(f'grid: {len(rows)} rows x {len(rows[0])} columns = {sum(map(len, rows))} glyphs\n')

    for name, snake in (('snake (zig-zag)', True), ('every row left->right', False)):
        morse = to_morse(reading_order(rows, snake))
        print(f'[{name}]')
        print('  morse :', morse)
        print('  text  :', to_text(morse))
        print('  unreadable glyphs:', morse.count('?'), '\n')

    # The half-moon orientation is fully determined by the row's reading direction.
    for i, row in enumerate(rows, 1):
        halves = {c for c in row if c in '◐◑'}
        print(f'row {i:2d} read {"left->right" if i % 2 else "right->left"}: half-moons used = {"".join(sorted(halves))}')
