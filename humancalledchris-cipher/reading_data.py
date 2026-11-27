"""Glyph-by-glyph transcription of the HumanCalledChris / partner cipher.

Coordinates are y-ranges in images/original.png (4080x1884).  Each column is a
single continuous vertical stem read top to bottom.  Kinds:
  L  = letter / digit glyph (value = decoded symbol)
  >  = letter separator (kink pointing right)
  <  = word separator   (kink pointing left)
  B  = framing bar (top start bar, "+" cross, or the bottom bar = period)
"""

# approximate stem x at the top and bottom of each column (stem drifts slightly)
COLUMN_X = {
    1: (2405, 2345),
    2: (2655, 2615),
    3: (2900, 2870),
    4: (3085, 3060),
}

COLUMNS = {
    1: [
        ("B", "+", 150, 215, "start bar (cross)"),
        ("L", "H", 215, 330, "small centred circle low on the stem (stem above it)"),
        (">", "", 330, 370, ""),
        ("L", "I", 370, 455, "centred circle right at the top"),
        (">", "", 455, 495, ""),
        ("L", "I", 495, 580, "centred circle right at the top"),
        (">", "", 580, 610, ""),
        ("L", "I", 610, 700, "centred circle right at the top"),
        ("<", "", 700, 750, ""),
        ("L", "I", 750, 850, "centred circle right at the top"),
        (">", "", 850, 895, ""),
        ("L", "M", 895, 1040, "three small circles on the right"),
        ("<", "", 1040, 1100, ""),
        ("L", "M", 1100, 1255, "three small circles on the right"),
        (">", "", 1255, 1300, ""),
        ("L", "O", 1300, 1400, "big centred circle"),
        (">", "", 1400, 1450, ""),
        ("L", "O", 1450, 1555, "big centred circle"),
        (">", "", 1555, 1600, ""),
        ("L", "N", 1600, 1725, "two circles on the left"),
        ("B", "+", 1725, 1800, "end bar (cross) = full stop"),
    ],
    2: [
        ("B", "⊤", 165, 200, "start bar"),
        ("L", "I", 195, 290, "centred circle right at the top"),
        (">", "", 290, 325, ""),
        ("L", "T", 325, 425, "two arches"),
        ("<", "", 425, 470, ""),
        ("L", "I", 470, 550, "centred circle right at the top"),
        (">", "", 550, 580, ""),
        ("L", "S", 580, 705, "hook up-right, then centred circle"),
        ("<", "", 705, 732, ""),
        ("L", "T", 732, 825, "two arches"),
        (">", "", 825, 860, ""),
        ("L", "H", 860, 960, "small centred circle low on the stem"),
        (">", "", 960, 995, ""),
        ("L", "E", 995, 1095, "small right circle above a centred circle"),
        ("<", "", 1095, 1140, ""),
        ("L", "Y", 1140, 1265, "two stacked circles (lower one drawn off-centre)"),
        (">", "", 1265, 1310, ""),
        ("L", "E", 1310, 1440, "small right circle above a centred circle"),
        (">", "", 1440, 1480, ""),
        ("L", "A", 1480, 1570, "one circle on the left"),
        (">", "", 1570, 1615, ""),
        ("L", "R", 1615, 1725, "left curl at top, right c-hook at bottom"),
        ("<", "", 1725, 1790, ""),
    ],
    3: [
        ("L", "2", 175, 295, "ticks L L R L = 0010"),
        (">", "", 295, 330, ""),
        ("L", "0", 330, 420, "ticks L L L L = 0000"),
        (">", "", 420, 450, ""),
        ("L", "2", 450, 560, "ticks L L R L = 0010"),
        (">", "", 560, 610, ""),
        ("L", "6", 610, 710, "ticks L R R L = 0110 (ink overwritten)"),
        ("<", "", 710, 750, ""),
        ("L", "R", 750, 850, "left curl at top, right c-hook at bottom"),
        (">", "", 850, 890, ""),
        ("L", "I", 890, 960, "centred circle right at the top"),
        (">", "", 960, 1030, ""),
        ("L", "G", 1030, 1145, "c-hook on the right, low"),
        (">", "", 1145, 1190, ""),
        ("L", "H", 1190, 1305, "small centred circle low on the stem"),
        (">", "", 1305, 1345, ""),
        ("L", "T", 1345, 1460, "two arches"),
        ("<", "", 1460, 1510, ""),
        ("L", "N", 1510, 1600, "two circles on the left"),
        (">", "", 1600, 1640, ""),
        ("L", "O", 1640, 1740, "big centred circle"),
        (">", "", 1740, 1800, "letter separator: word runs on into column 4"),
    ],
    4: [
        ("L", "N", 175, 290, "two circles on the left"),
        (">", "", 290, 330, ""),
        ("L", "O", 330, 420, "big centred circle"),
        (">", "", 420, 460, ""),
        ("L", "W", 460, 580, "three circles: left, right, left"),
        ("B", ".", 580, 625, "bottom bar = full stop"),
    ],
}

# where each key glyph sits on the left page (display coords of the 2576-wide
# preview; multiply by 1.5838 for original pixels)
KEY_CENTERS = {
    'A': (688, 100), 'B': (668, 195), 'C': (668, 270), 'D': (650, 360), 'E': (650, 455),
    'F': (640, 545), 'G': (630, 640), 'H': (625, 750), 'I': (620, 820), 'J': (610, 910),
    'K': (595, 1030), 'L': (960, 155), 'M': (950, 225), 'N': (940, 312), 'O': (935, 398),
    'P': (930, 480), 'Q': (925, 570), 'R': (900, 662), 'S': (905, 757), 'T': (900, 842),
    'U': (885, 928), 'V': (880, 1022), 'W': (1132, 195), 'X': (1135, 275), 'Y': (1135, 350),
    'Z': (1130, 425),
    '1': (1125, 510), '2': (1120, 590), '3': (1110, 675), '4': (1105, 760), '5': (1100, 845),
    '6': (1095, 925), '7': (1085, 1010), '8': (1362, 215), '9': (1360, 300), '0': (1345, 380),
    '.': (1350, 465),
}
