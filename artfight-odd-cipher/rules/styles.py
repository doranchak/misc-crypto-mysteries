"""Style annotations for the glitched ArtFight rules text, read off the original screenshot (images/rules-original.png).

Measured by hue-clustering the screenshot (scripts/style_inventory.py): exactly 16 coloured spans in the rules area.

  style  look in the screenshot                      pieces
  -----  ------------------------------------------  --------------------------------------------------
  E      small red   (155,56,50)  ~12px tall "error"    7 x "error"
  P      purple      (165,66,192) normal size           4 pieces:  tes:   no   tional   Addi
  R      LARGE red   (203,65,56)  ~1.9x size            2 pieces:  n   Do't
  B      LARGE blue  (85,182,224) ~1.9x size            2 pieces:  A   ye
  Y      emoji (its own colours)                        1 piece

Everything else is plain grey (221,221,221-ish) normal-size text.

Each entry: (paragraph index 0-based, pattern, style).  The part of the pattern in {braces} is the styled piece; the rest
is context that makes the match unique.  'error' is not listed here - build code styles every "error" automatically.
"""

STYLES = [
    # purple, normal size
    (1, "g{tes:}No hate", "P"),          # P2
    (3, "ot{tional}", "P"),              # P4 (end of visual line 2)
    (3, "{no}g ther", "P"),              # P4 (start of visual line 3)
    (4, "bi{Addi}in", "P"),              # P5
    # LARGE red
    (1, "beA{n}Please", "R"),            # P2
    (3, "{Do't}", "R"),                  # P4
    # LARGE blue
    (2, "ch{ye} werewolf", "B"),         # P3
    (3, "-{A}rsa", "B"),                 # P4
    # emoji
    (4, "{😎}", "Y"),                    # P5
]

STYLE_NAME = {
    "E": "small red (inserted “error”)",
    "P": "purple, normal size",
    "R": "LARGE red",
    "B": "LARGE blue",
    "Y": "emoji",
}
