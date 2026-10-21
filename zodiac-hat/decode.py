#!/usr/bin/env python3
"""Z408-key reading of the 24 hat symbols (row-major). Glyph names were matched by eye to the Z408 key (arXiv 2403.17350 Fig. 4)."""
Z408 = {'solid circle':'T','M':'H','circle dot':'E','circle bar':'H','X':'O','solid square':'L','open square':'Y','A':'W',
        'reversed D':'O','T':'O','crosshair':'D','triangle dot':'I','B':'L','solid triangle':'A','reversed C':'V','Z':'E','square dot':'S'}
HAT = ['solid circle','M','circle dot','circle bar','X','solid square',
       'solid square','open square','A','reversed D','T','crosshair',
       'circle bar','triangle dot','B','B','M','solid triangle',
       'reversed C','Z','Z','open square','Z','square dot']
print(''.join(Z408[g] for g in HAT))
