"""Transcription data for the two journal pages.

Each word: (x0, x1, text, kind, note)
  text  = the letters as WRITTEN (cipher glyphs decoded one-for-one), plus punctuation
          '.' = long dash used as full stop, ',' comma, '"' quote, "'" apostrophe, '(' ')' parens
  kind  = 'w' normal | 's' struck-through but legible | 'x' scribbled out, illegible
          'i' inserted above the line | 'a' annotation in ordinary Latin letters | 'u' uncertain reading
Line = (cell index between ruled lines, [words], optional custom y-range override)
x coordinates are page pixels in the 1080-px-wide photos.
"""

PAGE1_RULES = [45, 101, 156, 213, 269, 327, 384, 441, 498, 552, 608, 667, 722, 776, 832,
               887, 942, 997, 1052, 1106, 1159, 1213, 1268, 1318]
PAGE2_RULES = [103, 158, 215, 272, 330, 388, 446, 506, 564, 623, 682, 741, 802, 861, 920,
               979, 1038, 1096]

PAGE1 = [
    (0, [(175, 205, 'i', 'w', ''), (240, 360, 'said', 'w', ''), (405, 495, 'brr', 'w', ''),
         (518, 582, 'is', 'w', 'written "is" for "it\'s"'), (598, 628, '', 'x', 'one glyph scribbled out'),
         (638, 760, 'cold', 'w', ''), (800, 866, 'in', 'w', ''), (900, 1042, 'here.', 'w', '')]),
    (1, [(155, 332, 'shing', 'u', 'reads s-h-i-n-g; probably a slip for "shining" (see the struck word below)')]),
    (2, [(158, 392, 'sining', 's', 'struck through with two lines; glyphs read s-i-n-i-n-g (an h may be hidden under the strike)'),
         (452, 680, 'angels', 'w', ''), (732, 902, 'stick', 'w', ''), (912, 1022, 'on.', 'w', '')]),
    (3, [(862, 992, 'send', 'i', 'inserted above the line with a caret ^, replacing the struck "shine" below')],
     (238, 294)),
    (4, [(158, 262, 'moon', 'w', ''), (262, 424, 'tell', 'w', 'the writer left the space after the t of "tell"'),
         (452, 540, 'me', 'w', ''), (558, 622, 'if', 'w', ''), (672, 702, 'i', 'w', ''),
         (732, 826, 'can', 'w', ''), (852, 1008, 'shine', 's', 'struck through with an arrowed line; "send" is inserted above'),
         (1008, 1040, '', 'x', 'scribbled-out glyph')]),
    (5, [(156, 202, '', 'x', 'scribbled-out glyph'), (205, 392, 'down', 'w', ''), (436, 526, 'my', 'w', ''),
         (543, 742, 'heart', 'w', ''), (752, 818, 'to', 'w', ''), (852, 990, 'you.', 'w', '')]),
    (7, [(162, 352, 'cheer', 'w', ''), (372, 615, 'pratice', 'w', 'sic: "practice" with the c before t missing'),
         (662, 874, 'sucks.', 'w', '')]),
    (9, [(150, 292, 'dont', 'w', ''), (355, 597, 'listen', 'w', ''), (630, 694, 'to', 'w', ''),
         (730, 1040, 'negativi', 'w', 'word continues on the next line ("negativi-ty"); a stray ")" sits at the margin')]),
    (10, [(152, 262, 'ty.', 'w', 'end of "negativity"')]),
    (12, [(148, 326, 'when', 'w', ''), (365, 472, 'the', 'w', ''), (522, 692, 'birds', 'w', ''),
          (728, 870, 'come', 'w', ''), (885, 942, 'to', 'w', '')]),
    (13, [(148, 222, 'dry', 'w', ''), (260, 357, 'off', 'w', ''), (380, 572, 'their', 'w', ''),
          (598, 768, 'wings,', 'w', ''), (770, 868, 'you', 'w', ''), (884, 972, 'can', 'w', '')]),
    (14, [(156, 190, '', 'x', 'struck glyph (looks like k)'), (200, 252, 'go', 'w', ''),
          (285, 374, '', 'x', 'scribbled-out word'), (400, 494, 'fly', 'w', ''), (533, 666, 'with', 'w', ''),
          (692, 872, 'them.', 'w', '')]),
    (16, [(145, 253, 'the', 'w', ''), (288, 463, 'world', 'w', ''), (488, 661, 'knows', 'w', ''),
          (690, 798, 'your', 'w', ''), (828, 946, 'name', 'w', '')]),
    (17, [(155, 238, 'but', 'w', ''), (262, 360, 'not', 'w', ''), (423, 531, 'your', 'w', ''),
          (560, 770, 'story.', 'w', '')]),
    (19, [(146, 266, 'the', 'w', ''), (322, 625, 'previous', 'w', ''), (662, 792, 'pen', 'w', ''),
          (818, 922, 'was', 'w', '')]),
    (20, [(158, 354, 'better', 'w', 'the ink colour changes at "the previous pen was better" (lighter pen)')]),
    (22, [(146, 184, '', 'x', 'scribbled-out glyph'), (184, 292, 'mas,', 'u', 'reads m-a-s; meaning unclear (a name? "Ma\'s"?)'),
          (316, 411, 'you', 'w', ''), (437, 559, 'cant', 'w', ''), (592, 752, 'rush', 'w', ''),
          (778, 978, 'pens.', 'w', '')]),
]

PAGE2 = [
    (0, [(145, 232, 'im,', 'w', 'I\'m'), (285, 476, 'gonna', 'w', ''), (535, 716, 'shoot', 'w', ''),
         (757, 830, 'up', 'w', ''), (865, 1025, 'this', 'w', '')]),
    (1, [(138, 345, 'whole', 'w', ''), (350, 606, 'shool.', 'w', 'sic: "school" without the c')]),
    (2, [(138, 192, 'my', 'w', ''), (233, 552, '"friends"', 'w', 'in quotation marks'),
         (582, 722, 'suck,', 'w', ''), (758, 820, 'my', 'w', ''), (843, 1030, 'house', 'w', 'continues as "house-hold" on the next line')]),
    (3, [(125, 268, 'hold', 'w', ''), (305, 425, 'also', 'w', ''), (462, 530, 'is', 'w', ''),
         (568, 862, 'miserable.', 'w', ''), (885, 972, '', 'x', 'scribbled-out glyph(s)')]),
    (4, [(130, 262, 'with', 'w', ''), (305, 352, 'my', 'w', ''), (356, 525, 'biggest', 'w', ''),
         (538, 922, 'problem', 'w', '')]),
    (5, [(130, 232, 'was', 'w', ''), (262, 522, 'someone', 'w', ''), (540, 652, 'not', 'w', ''),
         (665, 945, 'telling', 'w', 'written t-e-l-l-i-n-g (texting?)'), (958, 1030, 'me', 'w', '')]),
    (6, [(125, 280, 'back.', 'w', ''), (290, 410, 'ive', 'w', "I've"), (455, 622, 'been', 'w', ''),
         (645, 690, 'a', 'w', ''), (715, 887, 'third', 'w', ''), (887, 922, '', 'x', 'scribbled-out glyph')]),
    (7, [(128, 380, 'wheel', 'w', ''), (395, 436, 'my', 'w', ''), (448, 695, 'whole', 'w', ''),
         (720, 860, 'life', 'w', ''), (880, 1010, 'and', 'w', '')]),
    (8, [(128, 232, 'its', 'w', ''), (255, 385, 'just', 'w', 'only occurrence of j'), (400, 645, 'gotten', 'w', ''),
         (665, 915, 'worse.', 'w', '')]),
    (9, [(122, 235, 'not', 'w', ''), (258, 285, 'a', 'w', ''), (315, 560, 'single', 'w', ''),
         (572, 690, 'one', 'w', ''), (725, 790, 'of', 'w', ''), (812, 1005, 'these', 'w', '')]),
    (10, [(122, 235, 'mfs', 'w', 'slang abbreviation'), (270, 295, 'i', 'w', ''), (318, 630, 'actually', 'w', ''),
          (641, 840, 'like.', 'w', ''), (865, 910, '', 'x', 'scribbled-out glyph'), (918, 955, 'i', 'w', '')]),
    (11, [(120, 168, '', 'x', 'scribble with an arrow running back to the "I" above'), (168, 322, 'wish', 'w', ''),
          (378, 410, 'i', 'w', ''), (435, 560, 'had', 'w', ''), (578, 722, 'real', 'w', ''),
          (722, 1015, 'friend(s)', 'w', 'written with no space after "real"; the final s is in parentheses')]),
    (12, [(122, 185, 'but', 'w', ''), (185, 205, '', 'x', 'struck glyph'), (207, 235, 'i', 'w', ''),
          (258, 460, 'guess', 'w', ''), (505, 582, 'im', 'w', ''),
          (595, 725, 'used', 'w', 'circled in pen'),
          (725, 785, 'on', 'a', 'the word "on" is written in ordinary Latin letters above a squiggle next to the circle'),
          (798, 842, 'to', 'w', ''), (875, 1028, 'being', 'w', '')]),
    (13, [(122, 368, 'alone.', 'w', ''), (388, 455, 'i', 'w', ''), (465, 622, 'hate', 'w', ''),
          (640, 855, 'being', 'w', ''), (857, 1025, 'third', 'w', '')]),
    (14, [(122, 318, 'wheel', 'w', ''), (348, 612, "they're", 'w', 'with an apostrophe'), (620, 695, 'all', 'w', ''),
          (715, 982, 'getting', 'w', '')]),
    (15, [(115, 435, 'blocked.', 'w', ''), (475, 552, 'im', 'w', ''), (572, 772, 'gonna', 'w', ''),
          (795, 882, 'cut', 'w', ''), (905, 1040, 'every', 'w', 'the y is squeezed into the margin above the r')]),
    (16, [(115, 255, 'fake', 'w', ''), (278, 409, 'cunt', 'w', ''), (441, 525, 'off', 'w', ''),
          (555, 612, 'fo', 'w', 'sic: probably "of" with the letters swapped'), (641, 702, 'my', 'w', ''),
          (718, 955, 'life.', 'w', '')]),
]

READING1 = [
    ('I said brr, is [it\'s] cold in here.', 'A cheerleading chant ("I said brr, it\'s cold in here").'),
    ('Shing [shining?] — <s>sining</s> — angels stick on.', 'The first word reads "shing"; the struck word on the next line looks like a second try at "shining".'),
    ('Moon, tell me if I can <s>shine</s> ^send^ down my heart to you.', '"send" is inserted above the line with a caret.'),
    ('Cheer pratice [practice] sucks.', ''),
    ('Don\'t listen to negativity.', ''),
    ('When the birds come to dry off their wings, you can go fly with them.', ''),
    ('The world knows your name but not your story.', ''),
    ('The previous pen was better.', 'The ink does change here: the last lines are in a lighter pen.'),
    ('[?]mas, you can\'t rush pens.', 'The first word reads m-a-s after a scribbled-out glyph.'),
]

READING2 = [
    'I\'m gonna shoot up this whole shool [school].',
    'My "friends" suck, my household also is miserable.',
    'With my biggest problem was someone not telling me back.',
    'I\'ve been a third wheel my whole life and it\'s just gotten worse.',
    'Not a single one of these mfs I actually like.',
    'I wish I had real friend(s), but I guess I\'m used to being alone.',
    'I hate being third wheel. They\'re all getting blocked.',
    'I\'m gonna cut every fake c*nt off fo [of] my life.',
]
