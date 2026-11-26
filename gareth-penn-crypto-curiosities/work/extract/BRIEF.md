# Shared brief for extraction agents (Gareth Penn crypto-method catalog)

Gareth Penn (b. ~1941; librarian, Germanist, Mensa member) wrote for decades that Harvard/Berkeley
professor Michael O'Hare was the Zodiac killer. His "evidence" is almost entirely cryptographic or
pseudo-cryptographic: hidden messages he claims to find in the Zodiac's letters, ciphers, crime-scene
geography, dates, postmarks, etc. We are building a COMPREHENSIVE CATALOG of EVERY DISTINCT METHOD he
describes for extracting hidden meaning, with exact worked examples (so we can build interactive demos
that reproduce them) and precise citations.

Already known methods (from his 2022 essays) -- still record them if your source describes them, with
your source's citation and examples, but especially look for ones NOT on this list:
 17-column grid reformatting; row,column coordinates read as numbers (PI at 31,4 = 3.14); position
 numbers (#1030 = 10/30); intersections of a word's row with another word's column; Morse code to
 binary (dah=1, dit=0) read as base-2 number (ONE=60, TWO=95, EIGHT=193, MIKE=202, THE END=2068,
 DEATH=1072, BIRTH=8272, RADIAN=4870, BUS=520); "redivision" (same Morse bit-string split differently
 into other letters, BUS<->THREE); calendar reading (each character = one day from a dated anchor);
 taxicab numbers / sums of two cubes; perfect squares; right-triangle hypotenuse sqrt(a^2+b^2) between
 two grid points; "expressive difference" between two positions; expressive postmarks (7/31 -> 731=43x17);
 angles mod 360; pi proportion 390:18 :: 3:0.14159; WIZARD cipher (reverse alphabet A<->Z; matching
 pairs like GT, PK cancel and "drop out"); alphanumeric values A=1..Z=26 with E=3 and Roman-numeral
 values (V=5, C=100); acrostics; anagrams; radian geometry on the Mt. Diablo map; keyboard shift
 (&#=73 because shift-7 and shift-3); hapax legomenon rarity.

## Output format (write Markdown to the file path given in your task)
For EACH distinct method found in your source:

### M: <short method name>
- Category: (e.g. anagram, letter-number, Morse/binary, grid/geometry, map/geography, calendar/date,
  numerology/arithmetic, typography/handwriting, word-play/pun, cipher (classical), other)
- Rules: precise, reproducible description of the procedure as Penn applies it.
- Examples: Penn's worked examples with EXACT inputs and outputs (letters, numbers, positions, dates),
  copied carefully. Mark anything you had to infer as [inferred]. Short verbatim quotes are welcome.
- What he claims it proves: (e.g., "spells O'HARE", "O'Hare's birthday", "Harvard address").
- Citation(s): exact. For Times 17 use "T17 p.<printed page number> (Part N, PDF p.K)"; for The Second
  Power "SP p.<printed page> (PDF p.K)"; for other sources use the file name + page/paragraph.

Then a section **## Puzzle-relevant remarks** collecting anything that could help decode Penn's OWN
later puzzles: mentions of anagrams as proof of priority/prediction (e.g., Galileo/Hooke/Huygens-style
anagrams), "lottery", "insurance", "haiku", how he thinks hidden messages should be built, favourite
keys/words/numbers (17, 38, O'HARE, MIKE, birthdays, addresses, ZIP codes, phone numbers), his views on
what a "good" cipher/message is, any self-made puzzles or challenges he poses to readers.

Then **## Bibliography leads**: every other writing by Penn that your source mentions (title, venue, date).

Then **## Biographical facts about Michael O'Hare / targets** that Penn encodes (birthdate, middle name,
addresses, schools, phone numbers, etc.) -- these are likely ingredients of his messages.

Be exhaustive about METHODS; be concise in prose. OCR text may contain errors: when an example looks
garbled and matters, LOOK AT THE PAGE IMAGE (paths given in your task) to read it correctly.
Do not invent details. If a figure/diagram carries the method, describe it from the image.
