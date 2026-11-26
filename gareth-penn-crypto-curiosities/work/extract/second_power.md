# Gareth Penn, *The Second Power* (1999) — method catalog

Source: "The Second Power: A mathematical analysis of the letters attributed to the Zodiac murderer and
supplement to TIMES 17", (c) 1999 Gareth Penn. 64-page PDF; OCR `ocr/sp.v2.txt`; page images
`scratchpad/raw2/sp/p-NNN.png`. Every page image was viewed.

**Page numbering.** PDF pp.1-5 are unnumbered front matter (title, abstract, 2-page Errata insert,
"Writing Digitally" chart). Printed p.1 = PDF p.6 (Foreword). Printed p.N = PDF p.(N+5) up to p.17
(PDF 22). **Printed p.18 is missing from the PDF**. It survives as the Drive scan
`.../Gareth Penn - The Second Power/66937d02998c22694539275e1202ed49.jpeg` (different typeface; same
uncorrected text). Below it is cited as "SP p.18 (Drive jpeg 66937d…)". From printed p.19 on,
printed p.N = PDF p.(N+4) (p.60 = PDF 64). Chapter-opening pages are unnumbered, but the count
includes them.

**Verification.** I recomputed almost every redivision below with the chart's Morse table. Arabic
numerals were converted to base two. I checked whether the target's bit string occurs inside the
host's. They match unless flagged **[did not reproduce]**.

---

## 10-line summary of the booklet

1. A 60-page self-published "pamphlet" supplementing TIMES 17 (1987). It restates Penn's thesis that Michael Henry O'Hare wrote the Zodiac letters.
2. Foreword: rebuts the Zodiac=Unabomber theory, separates "accidental" from "contrived" coincidence, and answers the "pyramidologist" objection.
3. History chapter ("Remembrance of things past"): the crimes, the letters, the "radian" clue that his father Hugh Penn noticed.
4. "Reading the Zodiac": the crossed circle sits on square character positions; the 408 cipher expresses 130π; there are 17-column grids. His core method is Morse to binary (dash=1, dot=0) read as base-two numbers, plus "redivision".
5. "Tutorials": the Zodiac supposedly embedded lessons (by analogy with the Arecibo message, 1679 = 23x73) showing that ONE=60, TWO=95, the 17-column format, ONE-rectangles, calendars, and "Mendelevian" same-column relatedness.
6. "Naming names": PEN+DRAGON leads to Arthur D. Little (O'Hare's employer); OHARE/MIKE/HENRY/NAME, EUGENE/BERTA (parents), BER=130, TIMES17=9745=9/7/45 (Berta's 38th birthday).
7. "Family values" and its sequels: a lurid psycho-sexual "autobiography" built from hidden FATHER/MOTHER/SON/EUGENE/BERTA/INCEST/sexual-word redivisions. Squares are "masculine" (father) and times-17s "feminine" (mother).
8. Throughout, he compares the same configurations in O'Hare's own texts (dissertation preface, class reports, Wolves letter, obituary of Berta Margoulies, 1987 press statement) as proof of common authorship.
9. "Boy Z 'n the hood": crime-scene objects (desk, lift, bloodstain, car door, hood, car keys, Timex) were chosen for their digital spellings.
10. "Aftermath": O'Hare's reactions to TIMES 17 (radio ambush, press, libel non-suit, lawyers). "Reading and writing": overlap, compression and "meta-writing" explain how so much is packed into ~4000 words.

---

## The "Writing Digitally" chart (PDF p.5) and Penn's digitizing conventions

**Chart text:** "Readers may find it convenient from time to time to refer to these tables, which show
the form of Roman letters in Morse Code and the equivalents of familiar base-ten numbers in the less
familiar base-two system of notation. Numbers larger than 100 can be analogized from the table."

**Roman alphabet to Morse (0 = dot/dit, 1 = dash/dah):**

| A 01 | B 1000 | C 1010 | D 100 | E 0 | F 0010 | G 110 | H 0000 | I 00 |
|---|---|---|---|---|---|---|---|---|
| **J 0111** | **K 101** | **L 0100** | **M 11** | **N 10** | **O 111** | **P 0110** | **Q 1101** | **R 010** |
| **S 000** | **T 1** | **U 001** | **V 0001** | **W 011** | **X 1001** | **Y 1011** | **Z 1100** | |

**Numerals (Morse, 5 digits):** 1 01111, 2 00111, 3 00011, 4 00001, 5 00000, 6 10000, 7 11000,
8 11100, 9 11110, 0 11111.

**Base-ten to base-two table:** 1 to 100 (1=1, 2=10, ... 17=10001, 60=111100, 95=1011111,
100=1100100).

**Conventions as he actually applies them (from the text, mainly SP p.9 / PDF 14, and the examples):**
- Roman letters are written in Morse with dot=0 and dash=1, and the concatenated bit string is read
  as a base-two number. Letter boundaries are dropped. Example: "MIKE ... 11 00 101 0. That sequence
  of digits spells the number 202" (p.8).
- **Arabic numerals in a text are not converted with the Morse numeral table.** They become their
  base-two equivalent: "translating base-ten numbers written in Arabic numerals into their base-two
  equivalents" (p.9). Verified examples: 2→10 (ITHIN2, 2NINE), 10→1010 (OUT10MI, 10MINIS),
  13→1101 (VES13S), 18→10010 (TWO18), 7→111 (NINE7), 22 = NG (10110), 21857→101010101100001
  (ARKABL). The Morse-numeral half of the chart is reference only.
- A group of Arabic digits separated from other digits by punctuation is one base-two number. Car-door
  example: 12, 20, 68, 7, 4, 69, 27, 69, 6, 30 (p.53).
- For the 17-column grids: "I have omitted spaces between words, punctuation, cipher symbols, and
  ampersands" (p.9). The crossed circle and other non-alphanumerics are dropped (p.21). Arabic numerals
  are kept as characters.
- Characters are numbered 1..N left to right, top to bottom. In a 17-column grid, char# = 17(row-1)+col.
- A "digital" character number is the position in the bit string. "Its digital character-number ...
  is divided by 2.58 (the average digital length of the Morse letter in English), providing the
  approximate character-number of the same redivision in the literal text" (p.9). Searching was done
  with Microsoft Word find and "find file".
- "x 'is' a redivision of y": y's bit string occurs inside x's letter boundaries, and extra leading or
  trailing digits are allowed. A **perfect** redivision uses every digit (p.10, OPLEIN example).
- Leading zeros are insignificant. **Trailing zeros are "indifferent"**: multiplying by 2^n "does not
  change the basic form of a name or word; it only adds zeros at the end" (pp.32, 43, 56).
- Morse numerals in the chart are standard. The chart has no special rules beyond the 0=dot, 1=dash
  assignment.

---

## Methods

### M1: Morse-to-binary "digital spelling" of words
- Category: Morse/binary
- Rules: Write each letter in Morse (dot=0, dash=1), concatenate, and read the result as a base-two
  integer. That integer is the word's "digital spelling".
- Examples (all verified): MIKE 11 00 101 0 = 202; GARETH 110 01 010 0 1 0000 = 12,944; DEATH 100 0
  01 1 0000 = 1072; ONE 111 10 0 = 60; TWO 1 011 111 = 95; THREE and BUS both = 520; NAME 10 01 11 0
  = 78; HENRY = 299; EUGENE = 228; GENE 110 0 10 0 = 100; BER = 130; BERTA 1000 0 010 1 01 = 1045;
  BERTA M = 4183; MOM 11 111 11 = 127; MAMA = 221; BM = 35; DEAD 100 0 01 100 = 268; LIFE 0100 00 0010 0
  = 516; TIME 1 00 11 0 = 38; TIMES17 1 00 11 0 000 10001 = 9745; TIMES 3 = 1219; ELEVEN 0 0100 0
  0001 0 10 = 1034; INCEST 00 10 1010 0 000 1 = 1345; TIMER = 306; TIMEX 1 00 11 0 1001 = 617;
  BATES 1000 01 1 0 000 = DEATH; WOMB = 2040 = 120x17; PENIS 0110 0 10 00 000 = 1600 = 40²; ME 11 0 =
  6; MIKE O 11 00 101 0 111 = 1623; SQUARE has 16 digits (000 1101 001 01 010 0).
- What he claims it proves: the Zodiac "writes in Morse Code". The numbers are the digital spellings
  that character numbers, intervals, areas and dates later match.
- Citation: SP p.8 (PDF 13); chart PDF 5; used throughout.

### M2: Redivision (digital), hidden and perfect
- Category: Morse/binary; word-play
- Rules: Take any run of literal text (spaces removed), convert it to Morse bits, and regroup the
  bits into other letters. A target word is "found" if its bit string lies inside the run, with
  extra digits allowed at either end. It is "perfect" if no digits are left over. Penn credits the idea to medieval Kabbalists
  (literal LEGEND / LEG END, WEEKNIGHT / WEE KNIGHT). He says "digital redivision is far more subtle
  than literal redivision, because it can create and destroy letters".
- Examples: THREE (1 0000 010 0 0) = BUS (1000 001 000), as redivisions of 520 (p.8). Cipher #4: CEL
  (1010 0 0100) = 2NINE (10 10 00 10 0), which matches the radian 57.29°; 57 Morse digits precede CEL
  (corrected in the Errata: CJIOKAMFORTGXFDVJH = 57 digits). OPLEIN = 11 + TWELVE (p.10). BLUE =
  BASE2 (1000 01 000 0 10), so "blue writing is base-two writing" (p.10). BASEMENT gives BASE, IT WONT
  gives TWO, BLU gives BASE (p.10). DEEP HEAT = SADISM (p.13). OKEDCU (CROOKED CUES) = TORTURE
  (p.13). NUCENCE = SQUARE (p.11). VCARB (6V CAR BAT) = SQUARE (p.17). CEIMPRI (NICE IMPRIEST) =
  TRIANGLE (p.18). ODSTAI (BLOODSTAINED) = OHARE (p.22). THECO = BERTA M (p.24). TSICK = BERTA,
  IAMN = SON, IAMINS = EUGENE (p.37). THEMUP = BEATING ("BEATING THEM UP is a digital tautology",
  p.28). DIOFF = BATTERER (perfect, p.29). KSTOMAS = BOOLE, OUT10MI = GEORGE (p.19). NTHERETHEREA =
  RIVERSIDE (p.15). OWNETTTH = MY NAMES (perfect, p.42). EMICHAEL = ANAL SEX (p.44). RED SUITS =
  REDIVIDE (p.51). WOLV = MORSE (p.51).
- Hundreds more, all verified: family names (LDGIVE/NRATHER/ERATHER/SRATHER/IRATHER = FATHER;
  OMTHEL/YONESL/YOTHER/YTOHEL/KTODEVE/TOMEISTH = MOTHER; BATTERE/HTMEL/SOFA/CEJUS/SOFF/SOFI/SOFH/
  SOFL/HOUS/SOUS/RIOUS/IAMFI/IAMID/LAGAI/DJUS/HOINS/SOFP/CIOUS/BEOFU = EUGENE; PIFYO/BURN/LIARD/
  NIFYO/WHENTA/GHTAL/BEENTR/BERK/BURC/BURB/BURY/GESCO/NEVENT/GEVENT/THEKEY/USEARO/YSEARC/GHTAW/BERY
  = BERTA; UTTON/OOK/OOT/OOC/TOO/OOD/OON/MTOB/UTOG/OOO/OMM = MOM; ODSTAI/OTHECA/MTHEKI/UTTHETAS/
  OSEAL/ODIECU/UTTHECA = OHARE; MUR/PAR/JUL/OUR/WEAR/OTINK/OTINTH/OFTH/OFTI/PEC/MIND/GAR/PENN/PAL =
  MIKE; BEVERY/FEVERY/HERARO/BSTERNO/SELKAN/SVERY = HENRY). Sex/crime words (INCEST: UALSO, EARTHEG,
  EARTHEB, IKETHA, CARTHEM, IKETHED, FECTIV, HTENTHR, EARTSIN, PECTIV, INKSIM, URBIN; PENIS: ADBES,
  PLEH, YITHEP, 10MINIS, EMIDIS, ETTERSH, YERSI, NGLIES, NGETHEW, PASS, EGREES, EMUSEU, PRESS, PRESE;
  QUEER: QUIR, MAININ, TCREEK, ANDDAU, ONTINUA, ACASK, ORRIB, OREDETA, MEDDL, ORRUP; SECRET: BECAU,
  SULTF, SULTIN, HECLO, LICEDO; and others).
- What he claims it proves: hidden identification of O'Hare and his family, plus a hidden
  autobiography. Rarity (hapax) gives "statistical robustness".
- Citation: SP p.8 (PDF 13); p.10 (PDF 15) definition of "is"/"perfect"; passim.

### M3: Arabic numerals inside a redivision (base-two splice)
- Category: Morse/binary; numerology
- Rules: Numerals embedded in the letter stream are written in base two and spliced into the bit
  string. A word followed by a number can then spell "WORD + number" (a date, a fraction, etc.).
- Examples: ITHIN2 = ELEVEN (p.14). VES13S = LITTLE, where the 13 is a box-score "crossed circle = 13"
  (p.21). OUT10MI = GEORGE (p.19). 10MINIS = PENIS (p.34). HE2TEEN(A) = SECRET (p.46; works only if the
  following A is included). CEL = 2NINE, i.e. 57.29° (p.8). TWO18 = 1 011 111 10010 (= Feb 18): GOOF,
  YONEB, ROOF, YONETH, NOTMIN (p.48). NINE7 = 9/7: FIXO (p.52). NG = 22, so NGWHICH = "22BIRTH"
  (p.51). ARKABL and RKEYSW contain base-two 21857 (= 2/18/57) (pp.48-49). BAT1FL = EUGENE (p.48).
  "Two to the base two is 10", so the numbered facts "2 ... 10" and "3 ... THEB" read as the equations
  2=10 and 3=THREE (p.12).
- What he claims it proves: tutorial proof that numerals are meant to be read in base two; encoded
  dates (Berta's birthday 9/7, O'Hare's 22 Jan, the abuse date 2/18/57).
- Citation: SP p.12 (PDF 17); p.14 (PDF 19); p.21 (PDF 25); p.48 (PDF 52); p.51 (PDF 55); p.52 (PDF 56).

### M4: Letter-containment substitution and "any prefix/suffix" tricks
- Category: Morse/binary
- Rules: Because some Morse letters contain others (I=00 ⊃ E=0; S=000 ⊃ I=00; G=110 ⊃ ME=11 0), a
  letter can stand in for a shorter one. A word can also be completed by "any letter ending in 0" or
  "any base-two number".
- Examples: IRECT = ERECT ("E = 0, I = 00") (p.34). SHADTO = I HAD TO ("S = 000, I = 00") (p.49).
  Lower-case g in O'Hare's handwritten MARgOULIES: "Morse G (110) is a redivision of ME (11 0)", so it
  reads "ME in MARGOULIES" (p.56). Any letter ending in 0 + ATHER (R = 010) gives FATHER (p.19).
  Any letter ending in 0 + MICHAEL gives ANAL SEX (p.44). INCH + any base-two number (which always
  begins with 1) gives INCEST, explaining the postscript "& # inches along the radians" (p.38).
  10 + EUGENE + 010 = BATTERER: "within every BATTERER there is a EUGENE" (p.28). VE + SOFF =
  BATTERER (VE is also part of WIVES) (p.29). ME + IAMFI(N) = BATTERER (p.32).
- What he claims it proves: EUGENE is a batterer, the son was "in" the mother, and the postscript
  encodes INCEST.
- Citation: SP p.19 (PDF 23); p.28 (PDF 32); p.34 (PDF 38); p.38 (PDF 42); p.44 (PDF 48); p.49 (PDF 53);
  p.56 (PDF 60).

### M5: Trailing-zero / power-of-two equivalence ("skeleton" numbers)
- Category: Morse/binary; numerology
- Rules: Appending zeros (multiplying by 2^n) does not change a word. Stripping leading and trailing
  zeros gives the "skeleton" or "root" shared by different words.
- Examples: BIRTH (1000 00 010 1 0000) = THE END (1 0000 0 0 10 100) x 2². The skeleton of both is
  1000000101 = 517 = DESK (100 0 000 101), which is why the poem was carved on a desktop. LIFT = 0100
  00 0010 1 = 517: the "lift" offered to Bates meant THE END. LIFE = 516, so "what follows it (517) is
  both THE END and BIRTH", which explains "reborn" in the 408 cipher. In the dissertation preface,
  "from the beginning of SON #1 to the end of SON #2 is 517 characters" (p.56). #200 = GENE x 2,
  #404 = MIKE x 2, #456 = EUGENE x 2 (pp.32, 43, 55). HESS = 0000 0 000 000 (eleven zeros), so his
  correspondent Kevin Hess renamed himself "Kevin x 2¹¹" (p.60).
- Citation: SP p.32 (PDF 36); p.43 (PDF 47); p.56 (PDF 60); p.60 (PDF 64).

### M6: 17-column reformatting (the "times-17" format)
- Category: grid/geometry
- Rules: Strip spaces, punctuation, cipher symbols and ampersands. Keep letters and numerals. Write the
  text in rows of 17. "If a cipher is something worth analyzing and it is presented in that format,
  then anything else that is worth analytical effort should be presented in the same format. When
  it is, then *meaning will be provided by the format itself*." Justified by the Arecibo message
  (1679 = 23x73 bits, read as 23x73) and by Mendeleyev's 1869 periodic table being "published in the
  17-column rectangular format".
- Examples: Cipher #1 = 24x17 (three parts of 8 rows); Cipher #2 = 20x17; Cipher #4 = 17 + 15. "The
  first cipher can be read as an expression of the operation 24 x 17, the second as 20 x 17. What
  the two have in common is the phrase 'times 17'." The Hole Card has 221 characters = 13x17, a perfect
  rectangle (p.15). The Desktop Poem has 510 Morse digits = 30x17 (p.20).
- What he claims it proves: the Zodiac literature has a 2-D design, and TIMES 17 is the key.
- Citation: SP p.8-9 (PDF 13-14); p.10 (PDF 15); p.15 (PDF 20); p.16 (PDF 21).

### M7: Digital-level grids (bit strings laid out in rows)
- Category: Morse/binary; grid/geometry
- Rules: Lay the whole Morse bit string of a text out in 17 columns or "an arbitrary 25-column
  rectangular format to facilitate counting". Find redivisions by their digital character number and
  intervals measured in Morse digits.
- Examples: The Desktop Poem's bit string forms a 30x17 rectangle; in it DEATH #1 and LIFE #1 begin in
  Column 17 (times-17 character numbers) (p.20). In the poem, ODIECU/OHARE starts at digital #64 (8²)
  (p.25). University Herald letter (25-col): two EUGENEs 361 = 19² apart; the GENE of digital EUGENE #1
  begins at digital #100 (p.26). Torture/June-1970 letter: GENIUS #1 at digital #225 (15²), interval
  625 (25²) (p.45). LA Times letter: TIMEX at digital #425 (25x17) and #627, interval 202 (MIKE)
  (p.54). Two TIMES17s in THE CONFESSION are 323 Morse digits apart, 19x17 (p.14). CIOUS and SOFP are
  4 characters apart, i.e. 9 Morse digits (p.28). Hole Card horizontal EUGENE begins at digital #196
  (14²) (p.32).
- Citation: SP p.14 (PDF 19); p.20 (PDF 24); p.25-26 (PDF 29-30); p.32 (PDF 36); p.45 (PDF 49); p.54 (PDF 58).

### M8: Character numbers read as digital spellings (position = word)
- Category: letter-number; grid
- Rules: The 1-based index of a letter in the stripped text is a "character number". If it equals a
  word's digital spelling, that cell "is" the word. Squares and times-17 character numbers are also
  significant.
- Examples: #268 (Row 16) = DEAD (p.13); #516 = LIFE (p.13); #314 = π (pp.13-14, 52-53); #1416 = π's
  fraction, where ILDUM, LETTERSH (DEGREES) and FWHATSE (RADIANS) start (pp.14, 51); #618 = φ (PHOMPH IT
  makes a 4x4 square with it, p.11); #202 = MIKE (IRISH/EELSEH starts there; I-pronoun #6 falls there;
  pp.23, 26); #299 = HENRY; #228 = EUGENE (SOFI begins at #228, "its character-number is its own digital
  spelling", p.32); #127 = MOM (BABY begins there, p.20; PIFYO, p.24); #1045 = BERTA (Row 62, p.38);
  #1345 = INCEST (Row 80, p.38); #100 = GENE; #1623 = MIKE O (p.36); #1734 = 102x17 = 6x17x17 (VAGINA,
  p.35); #357 = 21x17 (WOMB, p.35); #544 = 32x17 (BEATING, p.28); #634 ≈ 202π, "MIKE OHARE", since PI
  paraphrases OHARE (p.26); #1400 = GENE (100) x 14 (I HAD TO, p.49); #484 = 22², "father-nickname"
  square (p.46); #6 = ME (DITOR, giving "ME SON", p.41). Squares: HEAMERI #81, DIOFF #121 (p.29); ERO #1
  starts at #36 (p.23). The LA Times box-score numeral 17 begins at #425 = 25x17 (p.14). The crossed
  circle at Z408 #100, Z340 #49, Z13 #4 are squares, and Z32 #29 is a prime = "full stop" (p.7).
- What he claims it proves: the author placed words on purpose. A "misspelling ... involving extra or
  missing letters seem[s] to be motivated by the need to adjust character-numbers" (p.33).
- Citation: SP p.7 (PDF 12); p.11-14 (PDF 16-19); pp.20-41 passim.

### M9: Grid squares, rectangles and other n x m figures (area = number)
- Category: grid/geometry
- Rules: Two forms in the grid mark opposite corners of a rectangle (rows x columns, counted
  inclusively). The area or the dimensions "express" a number.
- Examples: HEVEN and HSC (two SEVEN-redivisions) define a 7x7 square: "The dimensions of this figure
  express the word whose redivisions define it" (p.11). "Aug 1 69" makes 169 = 13²; with ONE it forms a
  4x9 rectangle = 36 = 6² (p.12). Two RIVERSIDEs make 6x11 = 66, i.e. 1966 (p.15). BASE and TWO make
  4x8 = 32, and BLU and TWO 2x8 = 16, both powers of two (p.10). POWER and TWO (and POWER and the
  numeral 2) form squares, "Power #2" (p.17). Two LIVEDs make 8x11 = 88, Berta's age at death (p.33).
  BERTA and SNATCH make 5x26 = 130 = BER (p.40). OUCA and SALT make **6 x 17 → "617" = TIMEX**: the
  dimensions are read as digits (p.54). 1957 and #57 make 2x7 = 14, O'Hare's age in 1957 (p.44).
  INCEST and SECRET make 2x7 = 14 (p.46). ARKABL and HINKIMG make 2x7 = 14 (p.48-49). Square side =
  √(digital value): an OMTHEL/YOTHER square 10x10 with √GENE = 10; a press-statement square 15x15 ≈
  √228 = 15.0997 (EUGENE) (p.50).
- Citation: SP p.10-12 (PDF 15-17); p.15 (PDF 20); p.17 (PDF 22); passim.

### M10: "Two-way" (double-duty) squares
- Category: grid/geometry
- Rules: A square figure whose two defining elements are also separated by a square number of
  characters. Penn says there are "six types" inscribable in a 17-column grid.
- Examples: TWELVE (OPLEIN) and #144 form a 5x5 square with interval 64 (p.10). NAME #1 and OTHECA
  (OHARE): 5x5 and interval 64 (p.24). Vallejo letter: MTHEKI (OHARE) and NAME #1: 10x10 and interval 144
  (p.25). MOTHER #2 and EUGENE: 9x9 and interval 144 (p.38). EARTHEG and #127: 3x3 and interval 36;
  EARTHEB and #127: 5x5 and interval 64; IKETHA/UTOG: 10x10 and interval 144 (p.41). ORRIB and Feb 18
  (2x2, difference 16) (p.48). FWEDO and #66 (10x10, 144) (p.54). INPAR/#228 with FEVERY (5x5,
  difference 64) (p.45).
- Citation: SP p.10 (PDF 15); p.24-25 (PDF 28-29); p.38 (PDF 42); p.41 (PDF 45); p.48 (PDF 52); p.54 (PDF 58).

### M11: ONE-rectangle (area 60) as the verb "to be"; TWO-rectangle (area 95) as antithesis
- Category: grid/geometry; word-play
- Rules: Two forms that define a rectangle with area 60 (= ONE, e.g. 4x15, 5x12, 6x10, 2x30) mean
  "X and Y are ONE", i.e. X = Y. This can also mean union or marriage. Area 95 (= TWO, 5x19) means
  opposition. "The geometric relationship between the formative elements supplies the meaning of
  [is, and]."
- Examples: NIWI (DEAD) and #268 form 4x15, "NIWI/DEAD = 268" (p.13). ALIVE and #268 form 5x19 = 95:
  "ALIVE and DEAD are TWO" (p.13). BEING and #516 (LIFE) form 2x30 (p.13). PI and PI, and DRIVEN and
  FEDSAL (ELEVEN and ELEVEN), form 5x12 (p.13). PI and #314 form 5x12 (p.13). ONE or the numeral 1
  defines 4x15 and 6x10 in the Dragon Card (p.12). PI #1 and #1416 (p.14). NAME and FORM in Cipher #1:
  "NAME and FORM are ONE" (p.22). OHARE/ODSTAI with #202 and #299: MIKE = OHARE, HENRY = OHARE (p.22).
  ERO and OHARE (p.23). WOMAN = BERTA (p.29). BERTA and MOM (pp.25, 51). EUGENE/BERTA rectangles as
  "marital or sexual union" (p.30). SON and MOTHER (p.41). COCK and PECKER (synonyms) (p.34). KIN and
  CHAOS: "My family is dysfunctional" (p.56). BEING and DEATH (p.49). QUEER = SELF, NAME = QUEER,
  QUEER = MICHAEL (p.44).
- Citation: SP p.12-13 (PDF 17-18); p.22 (PDF 26); p.30 (PDF 34); passim; summary p.60 (PDF 64).

### M12: Right triangles whose hypotenuse² is a digital spelling (legs as digits)
- Category: grid/geometry
- Rules: Two forms define a right triangle with legs a and b (column and row offsets). The
  "speaking" number is a²+b² (hypotenuse √n). The legs themselves can also be read as digits
  (9,7 → 9/7).
- Examples: The two BEAUTIFULs in THE CONFESSION: 9, 7, √130 (130 = BER; 9/7 = Berta's birthday), and
  their interval is also 130 characters (p.14). NTOMYS (WOMAN) with LIARD/BERTA: 9, 7, √130; the two
  MOTHERs: 3, 11, √130 (p.24). POLISH (Row 130) and YSEARC (BERTA): 5, 14, √221 (MAMA) (p.23). JEWISH
  and SON: the same 5,14 figure (p.23). Character #7 and SEVEN: 10, 11, √221 (p.39). NDOVE (LOVE) and
  OMTHEL: 9, 11, √202 (MIKE) (p.39). Two CARs (CAROL, O'Hare's wife): √202 (p.39). HE2TEEN (SECRET)
  and NAME: 9, 11, √202 (p.46). BECAU/SECRET and BOMB #3: 9, 7, √130 (p.46). DAY and DATE: 7, 13, √218
  (2/18) (p.48). UTTHECA (OHARE) and ORRUP (QUEER): 7, 13, √218 (p.48). ERO and PRESE: 7, 13, √218
  (p.49). HEPESTUL (EIGHTEEN) and YO (TWO): 9, 11, √202 (p.49). TOMEISTH and MOTHER: 6, 22, √520 (BUS)
  (p.53). MOTHER #1 and LRATHER: 8, 19, √425 = 25x17 (p.53). Penn cites Gauss's proposed Siberian
  Pythagorean diagram as precedent (p.6).
- Citation: SP p.6 (PDF 11); p.14 (PDF 19); p.23-24 (PDF 27-28); p.39 (PDF 43); p.46 (PDF 50);
  p.48-49 (PDF 52-53); p.53 (PDF 57).

### M13: Intervals (1-D distances) as words or numbers ("expressive difference"; NAME-interval)
- Category: numerology/arithmetic; grid
- Rules: Count the characters (or rows, or Morse digits) between two forms. The count is read as a
  digital spelling, a square, or a times-17. In the same column, interval = rows x 17.
- Examples: Two ZODIACs are 156 rows apart = 2 x 78 = "two NAMEs" (p.17). MUR (MIKE) and OHARE: 78
  (NAME) characters (p.22). The first two I-pronouns in THE CONFESSION are 202 (MIKE) apart; I #2 to PAR
  (MIKE) = 78 (NAME): "I, MIKE, NAME" (p.24). PIFYO to BURN = 221 (MAMA = 13x17) (p.24). BURC to BURB
  = 35 (BM) (p.38). SON to BERTA #2 = 221 (p.38). Two MARGOULIESes: 78 (p.33). PUSSY to MOM #2 = 306 =
  TIMER (p.40). SEVEN to INCEST: 18 rows = 306 (p.39). MOTHER to the three SONs = 228 (EUGENE) and 202
  (MIKE) (p.41). GIRL #1 to SON #2 = 202; CHILD to DAUGHTER = 404 (MIKE x 2) (p.43). Dissertation
  preface: BER and GENE are 30 apart (= 130 − 100), with #1345 (INCEST) between them (p.39). BERTA #1 to
  WOMAN #1 = 78: "WOMAN, NAME, woman's name" (p.29). AMMOS (WOMB) to HOLE = 22x17; FACTS (FEMALE) to
  USEARO (BERTA) = 26x17 = 442 = MAMA x 2 (p.35). ERECTION to HOLE = 272 = 16x17 (p.36). DRINKING
  follows FATHER #2 by 169 (13²) (p.31).
- Citation: SP p.17 (PDF 22); p.22-24 (PDF 26-28); pp.29-43 passim.

### M14: Interval arithmetic ("one + 60 = two"; numbers as operands)
- Category: numerology/arithmetic
- Rules: Treat number-words and numerals as quantities, and the interval between them as the
  operation. Several "correct answers" exist, "as quadratic equations have two solutions".
- Examples (Dragon Card): The first numeral 1 is #96; "If 1 = 96, then the difference between one and
  95 [TWO] is one". ONE at #200 and TWO at #260 are 60 apart, so "one + 60 = two". ONE at #106 and
  numeral 2 at #141 are 35 apart, so "one + 35 = two" (since 60+35 = 95). Death Machine Letter: TR (TEN)
  and ITHIN2 (ELEVEN) are 60 (ONE) apart, so TEN + ONE = ELEVEN. Numeral 2 is 60 from 1 #2: "the
  difference between 2 and 1 is ONE". 1 #1 (Errata correction; the text says #2) is 95 (TWO) from
  numeral 3: "1 + TWO = 3. QED" (p.14).
- What he claims it proves: tutorials showing that Morse-to-binary is "the rule here".
- Citation: SP p.12 (PDF 17); p.14 (PDF 19); Errata (PDF 4).

### M15: Countdown along the text (number-word as start of a descending count)
- Category: letter-number; grid
- Rules: From a number-word redivision, assign descending integers to the following characters. Look
  for a redivision of the matching number-word at the predicted position.
- Example: THE CONFESSION, "...MIDDLE WIRE FROM THE DISTRIBUTOR THEN I WAITED...": DL = NINE (perfect,
  100 0100); then E=8, W=7, I=6, R=5, E=4, F=3, so "the place of 2 in the series is taken by ROM, a
  redivision of TWO". From TR (= TEN) [inferred: I=9, B=8, U=7, T=6, O=5, R=4], "the place of 3 in
  the series is taken by THENI, a perfect redivision of THREE". DL and TR begin in the same column of
  consecutive rows.
- Citation: SP p.11 (PDF 16).

### M16: Row,column coordinates read as numbers; Cartesian axes; intersections
- Category: grid/geometry
- Rules: (a) The (row, column) of a form is read as a number (PI at 31,4 = 3.14). (b) The XAXIS
  redivision's row is the x-axis and the column of a nearby letter Y is the y-axis, giving signed
  coordinates. (c) A row through one form and a column through another meet at a meaningful cell.
- Examples: PI has row/column coordinates 31, 4 (π = 3.14…) (p.11). XAXIS = OUWITHI; there is no
  YAXIS. SQUARE (NUCENCE) is at (7, 7), "it forms a square". PI #1 is at (−1, +1) and PI #2 at (+5, −12):
  1x1 = 1 (the number one) and 5x12 = 60 (ONE) (p.11). The column of PI #1 and the row of PI #2
  intersect at #314 (p.13). The HARDON row and the HOLE column meet at #1623 = MIKE O, i.e. "the
  author's conception" (p.36).
- Citation: SP p.11 (PDF 16); p.13 (PDF 18); p.36 (PDF 40).

### M17: The "squares column"
- Category: grid/geometry; numerology
- Rules: In a grid with an odd number of columns, consecutive squares fall in the same column of
  consecutive rows at one column only: Column 13 in the 17-column grid (Column 10 in a 13-column grid).
  Add √n to 17 to get the next pair.
- Examples: 64 (8²) and 81 (9²) in Rows 4-5. 8+17 = 25 and 9+17 = 26 give 625/676 in Rows 37 and 40.
  The SQUARE redivision NUCENCE begins in Column 13.
- Citation: SP p.11 (PDF 16).

### M18: Mendelevian alignment (same column = related); vertical vs horizontal relationships
- Category: grid/geometry
- Rules: Like elements in a periodic-table column, related terms (synonyms, antonyms, sequences,
  family, causes) "align vertically". Vertical stacking order (top/bottom) and horizontal side-by-side
  placement encode kinds of relationship ("dualism"). Unusual word order and misspellings are
  explained as producing these alignments.
- Examples: POSITIVL and NEMIGHTS begin in the same column (p.16-17). The two ZODIACs begin in Column 10
  (p.17). The three paragraph numerals 1, 2, 3 sit in one column (p.17). VCARB (SQUARE) is under POWER
  (p.17). NUCENCE and CEIMPRI (both from "nuisance", both polygons) (p.18). The only MORSE redivision
  is under CODE (p.19). KSTOMAS (BOOLE) is over OUT10MI (GEORGE) (p.19). LDGIVE (FATHER) and OMTHEL
  (MOTHER) begin in the same column; "WHEN WE WERE AWAY FROM THE LIBRARY WALKING" was written in
  abnormal order to get that alignment (p.27). DEATH #1 (DEADS) and LIFE #1 (ETHEL) (p.20). The initials
  of HURTING and SADISM are in the same column (p.20). Family pictures: FATHER over SON over BERTA
  (Column 15) (p.31). Two Zs in the same column (p.52). MATHEMATICS/STATISTICS, FORM/DESIGN,
  PAST/HISTORY, THE TRUTH/VERITAS (p.51). RELATIVES/FAMILY (p.43).
- Citation: SP p.16-19 (PDF 21-23); p.20 (PDF 24); p.27 (PDF 31); p.31 (PDF 35); p.51 (PDF 55); passim.

### M19: Crossword-style vertical redivisions and "crossed" names
- Category: grid/geometry
- Rules: Read redivisions down a column as well as across. A horizontal and a vertical redivision of
  the same name crossing = a person "at cross purposes with himself". The crossing cell's number is
  meaningful.
- Examples: FATHER #2 is crossed by vertical EUGENEs BWNETH (Death Machine) and SOITU (Mikado) (p.28).
  Vertical BSP (Morse 1000 000 0110) = base-two 1030 = 10/30, the Riverside date, starting at #66
  (p.54). Hole Card: horizontal SJUS crosses vertical SEOERP (EUGENE) (p.32). Cipher #1 solution:
  horizontal SOFF crosses vertical SOITEA at #200 = GENE x 2; "roughly one in 3.5 billion" (p.32).
  1987 press statement: IAMFA crosses EROHRTI (E.R. OHARE), and WITH (GENE) crosses HOID (EUGENE) (p.33).
  Obituary: SOFS crosses SOUS, next to #228 (p.33). Belli letter: IAMID crosses ME IAMF(IN) (BATTERER)
  and LAGAI at #218 (p.49).
- Citation: SP p.28 (PDF 32); p.32-33 (PDF 36-37); p.49 (PDF 53); p.54 (PDF 58).

### M20: Calendar reading (each character = one day from an anchor)
- Category: calendar/date
- Rules: Choose an anchor: (a) a date written in the text ("Mon. Oct. 5, 1970" → OCT5); (b) a month
  word or its redivision (JAN = EOP/RMYA; AUG; JUNE) = the 1st of that month; or (c) lay the text out
  as a wall calendar for a stated year (7 per row). Each subsequent character is the next day. Words
  falling on significant dates "date" them. Calendars "commemorate the past [and] predict the future".
- Examples: Hole Card: the O of OCT5 = 5 Oct 1970, and "the lone string spelling ... PI begins on the
  fourteenth of March of 1971. In other words, PI = 3/14". The LA Times letter was postmarked 15 March
  1971, "the day after PI" (p.15). On the same calendar H = 2/18; ORRIB (QUEER) makes a 2x2 square with
  it (p.48). Cipher #1 solution: the JAN redivisions EOP and RMYA are 365 characters apart. Laid out as
  1945 (common year, New Year's Day a Monday), DANGERTUE puts TUE on a Tuesday, and the misspelled
  letter of PARADICE falls on 9/7. With EOP and RMYA as two New Year's Days, the text ends on 1/30
  (= 130) and begins on 12/19 (= 1219 = TIMES 3 digitally) (p.16). Cabby letter: EOP (JAN) is one day
  off, APRIL = LYINSTEA, and SCHOOL starts the week after Labor Day (p.16). Z32 letter (June 1970): EOP
  = 1 Jan; SUMMER is three days early on the astronomical calendar but right on the school calendar
  (p.16). LA Times letter: RMYA = 1 Jan, so BECAU (SECRET) falls on 30 October (the Riverside murder)
  and GIVETH (BIRTH) on 22 January (O'Hare's birthday) (p.24). Torture letter: "If AUG is the first of
  August, then the next BURN/BERTA is 7 September" (p.24). O'Hare's Tenth Anniversary Report: the
  explicit JUNE is June 1, and NGWHICH = "22BIRTH" falls on 22 January. EOP as JAN puts FIXO (NINE7)
  on 7 September (pp.51-52).
- What he claims it proves: the Zodiac (and O'Hare) dates important information: π, mother's
  birthday, his own birthday, the Riverside date.
- Citation: SP p.15-16 (PDF 20-21); p.24 (PDF 28); p.48 (PDF 52); p.51-52 (PDF 55-56). Errata: "The
  author doesn't calendars" should read "The author doesn't make calendars" (p.48).

### M21: Life/age calendar (one row = one year of someone's age)
- Category: calendar/date; grid
- Rules: Format a text so that each row is an age-year of the author (or of his father). Words in row
  n describe age n.
- Examples: THE CONFESSION in rows of **nine** characters starting with BABY ("Year Zero"): age-year 7
  contains the explicit SEVEN; HIGH SCHOOL ends at age 17.33 (p.30). Torture letter: each row is a year
  of Eugene's age (b. 1906), so EUGENE #2 + PAIN + WOMAN in Row 44 = 1950, when Michael was seven
  (p.30). Wolves letter (17 columns), a row per age-year of the author: Row 7 has EUGENE (SOFL) and BER
  separated by I; Row 14 has EVIL EUGENE (SOFI) merging with SON (FIMMI); Rows 16-19 read "FAMILY
  STRUCTURE IS AN INSULT TO DECENT VALUES" (teen years); Rows 22-24 read "SINGLE MALES WANDER ALONE UP
  TO NO GOOD" (the Riverside period); Row 38 begins with TIME (= 38), the age at which O'Hare learned he
  was a suspect; THEDE (BUS) in Row 38 = Joan Webster's abduction (p.55-56). Tenth Anniversary Report
  in three "tableaux" (Rows 1-40, ...); SION/SON at #7 = his age in 1950 (p.55).
- Citation: SP p.30 (PDF 34); p.55-56 (PDF 59-60).

### M22: Dates and numbers read from digit strings (position/date numbers)
- Category: calendar/date; numerology
- Rules: Read numbers, character numbers or digital values as month/day/year (US order). Concatenate
  adjacent numbers into a year.
- Examples: TIMES17 = 9745 = 7 September 1945 (Berta's 38th birthday), and "the word TIME is base-two
  38" (p.14, 16, 22). Vertical BSP = 1030 = 10/30 ('66 from #66) (p.54). 1/30 = 130; 1219 = TIMES 3
  (p.16). TWO18 = 2/18; 21857 = 2/18/57 (p.48). NINE7 = 9/7 (p.52). The character numbers of the three
  SECRETs in Cipher #1 are 19, 81, 324: "the first two, taken in order, express the year [1981] in which
  Joan Webster was murdered". The third (Errata: "third", the text says "second") x 17 = 5508, the days
  from Riverside to Boston (p.47). The numeral 1957 in the Badlands letter = the year O'Hare was 14
  (p.44). "Aug 1 69" → 169 (p.12). The Riverside murder year 66 appears via 6x11, ZIP 94566, Phillips 66,
  and #66 (pp.15, 54).
- Citation: SP p.12 (PDF 17); p.14-16 (PDF 19-21); p.44 (PDF 48); p.47-48 (PDF 51-52); p.54 (PDF 58).

### M23: Day-count and year-day numerology (chronology, postmarks)
- Category: calendar/date; numerology
- Rules: Count the days between events, a person's age in days, or a date's year-day number, and test
  for squares and times-17s.
- Examples: Days between murders: 782, 196, 85, 14 (782 = 46x17; 85 = 5x17; 196 = 14², and 14 is its
  root; 46 + 5 = 51 = 3x17) (p.9). Riverside (30 Oct 1966) to Boston (28 Nov 1981) = 5508 days = 324x17,
  and 324 = 18² (p.9) [verified]. O'Hare's age in days on 27 Sep 1969 = 9745 = TIMES17 (p.35, 53)
  [verified]. The first letter was postmarked 29 Nov 1966 = year-day 333 (THREE theme, with three copies
  and three documents) (p.8). The Death Machine Letter was postmarked year-day 314 (π) (p.14). Eugene's
  birthday 16 October = year-day 289 = 17², "and the date itself is a square (16 = 4²)" (p.26). Badlands
  letter postmarked 8 May 1974; Penn speculates it was dropped on the 7th (p.44).
- Citation: SP p.8-9 (PDF 13-14); p.14 (PDF 19); p.26 (PDF 30); p.35 (PDF 39); p.44 (PDF 48); p.53 (PDF 57).

### M24: Clock-hand angles
- Category: numerology/arithmetic; geometry
- Rules: Read the time on a physical object as a number and as hand angles.
- Example: The Timex watch stopped at 12:24. 1224 = 72x17. The hour hand is at 12°, the minute hand at
  144° (12²), and "the two hands form a 228° angle (digital spelling of the name EUGENE)".
- Citation: SP p.9 (PDF 14).

### M25: Cipher-structure numerology (squares, primes, π proportion)
- Category: numerology/arithmetic
- Rules: Test character counts and the positions of special symbols for squares, primes, times-17s and
  π.
- Examples: The first crossed circle is at #100 (Z408), #49 (Z340), #4 (Z13), all squares. There are 20
  squares in 1-408, 18 in 1-340 and 3 in 1-13, so the chance is (20/408)(18/340)(3/13) = 1/1670, against
  1/1444 for two roulette wins. The counts of crossed circles (4, 9, 1) are squares. Z32's crossed
  circle at #29 is prime, "a full stop". The roots 10, 7, 2 "in order of appearance" give 1072 = DEATH
  (p.7-8). Z408: 390 English letters + 18 gibberish, and 390:18 = 3:0.14159, so 130π; 390 = 130x3,
  with 130 = BER (pp.6, 14, 22, 40). The ciphers total 793 characters (408, 340, 13, 32) (p.4). The
  crossed circle "stands for D", D = 100 = base-ten 4 (a square), and 100 → GENE. It is a circle in four
  parts, and the OUR of FOUR = MIKE (p.53).
- Citation: SP p.4 (PDF 9); p.6-8 (PDF 11-13); p.14 (PDF 19); p.53 (PDF 57).

### M26: Morse-digit count of a cipher (Z32 = radian)
- Category: Morse/binary
- Rules: Count the Morse digits of the Roman-letter symbols in a cipher before a landmark symbol.
- Example (corrected Errata wording): "the Roman-letter symbols CJIOKAMFORTGXFDVJH (Morse 1010 0111 00
  111 101 01 11 0010 111 010 1 110 1001 0010 100 0001 0111 0000, 57 digits) is followed by ... CEL
  (1010 0 0100), which redivide to spell 10 10 00 10 0, 2NINE. Immediately following that is the
  crossed circle, Character #29". 57.29° = 1 radian. [57-digit count verified.]
- What he claims it proves: the June 1970 postscript "concerns radians" is truthful.
- Citation: SP p.8 (PDF 13); Errata (PDF 4).

### M27: Keyboard shift-characters as digits
- Category: other (typography)
- Rules: Read non-alphanumeric typed symbols as the unshifted numerals on the same keys.
- Example: "& #" in "The Mt. Diablo code concerns radians & # inches along the radians" are shift-7
  and shift-3, giving 73. "73 radians has the degree-value of 4183 (73 x 57.295779…), the digital
  spelling of BERTA M (1000 0 010 1 01 11)" [73 x 57.2958 = 4182.6].
- Citation: SP p.37 (PDF 41).

### M28: Box-scores, numerals and whole-text counts as operations
- Category: numerology
- Rules: Read the Zodiac's "box-score" (crossed circle = n, SFPD = 0) and the total character counts
  as parts of "n times 17".
- Examples: LA Times letter: the box-score "17" plus the newspaper name TIMES give the second part of "n
  times 17"; the numeral 17 begins at #425 = 25x17 (p.14). Hole Card: 13 appears as a word
  (THIRTEENTH), a numeral and 13 punched holes, and the 221 characters = 13x17, "the balance of the
  operation (TIMES 17) is left implicit" (p.15). Torture letter box-score: crossed circle = 13, giving
  VES13S = LITTLE (p.21). Car-door inscription: 35 alphanumerics = BM; digitized (letters in Morse,
  numbers 12, 20, 68, 7, 4, 69, 27, 69, 6, 30 in base two) it is 100 digits = GENE; a GENE and a BER
  redivision are 51 (3x17) digits apart (p.53) [35 and 100 verified].
- Citation: SP p.14-15 (PDF 19-20); p.21 (PDF 25); p.53 (PDF 57).

### M29: Number-words as landmarks (squares and times-17 intervals)
- Category: numerology; grid
- Rules: Highlight every number-word (literal or redivided) and measure intervals and positions.
- Example: Bus Bomb Letter p.1: the first three ONEs are all in Column 17 (char# 102, 153, 204 = 6, 9, 12
  x 17) and spaced by times-17s. ONEs #3-4 = 49; TWO to ONE = 25; TEN to TWO = 16 (all squares) (p.14).
  Examiner letter: the only two literal number-words are ONEs, in the same column (p.52). EIGHTEEN
  redivisions (NIGHTIC, HEPESTUL, LEANIFR, FIGHTIN) paired with TWO redivisions (YO, GTO, GOO): "TWO,
  EIGHTEEN, square, MIKE" (p.49). The Desktop Poem uses column numbers: GTO/TWO in Column 4 (2²) and
  LEANIFR/EIGHTEEN in Column 14 (O'Hare's age in 1957) (p.49).
- Citation: SP p.14 (PDF 19); p.49 (PDF 53); p.52 (PDF 56).

### M30: Row and column numbers as meaningful values
- Category: grid
- Rules: The row (or column) index of a form is read as a number or a digital spelling.
- Examples: POLISH occurs in Row 130 (BER) (p.23). FATHER is in Row 49 (7², masculine) and MOTHER in
  Row 51 (3x17, feminine) (p.27). The literal BM is in Row 35 (= BM) (p.52). GHTAL starts in Column 17,
  so its char# = row x 17 (feminine) (p.29). EUGENE row 81 (a square) and BERTA row 85 (5x17) in
  ONE-rectangles (p.30). The VCARB/ERATHER interval is 25 rows; the two Mikado FATHERs are 17 rows apart,
  i.e. 17x17 characters (p.28).
- Citation: SP p.23 (PDF 27); p.27-30 (PDF 31-34); p.52 (PDF 56).

### M31: Gendered number classes (squares masculine, times-17s feminine)
- Category: numerology
- Rules: Squares mark the father (EUGENE, "Gene is a square": GENE = 100; born on year-day 289 = 17²
  and the 16th; the cultural slang "square" for a non-artist engineer). Times-17s mark the mother (TIMES17 =
  her 38th birthday; MAMA 221 = 13x17). Same-column intervals (rows x 17) are feminine.
- Examples: VAGINA (VEOILD) at #1734 = 6x17x17; WOMB = 2040 = 120x17; HOOTB at #357 = 21x17;
  YSLAVES (BREASTS) makes a 6x17 rectangle with MOTHER (p.35). PENIS = 1600 = 40²; a MAN at #121 (11²)
  only because WOMAN was misspelled (p.33). The Berryessa attack on the day O'Hare was 9745 (TIMES17)
  days old is a "ritual observance of the femaleness of the date" (p.35). SON-redivisions in one column
  (times-17 intervals) "favor MOTHER", while squares "take after FATHER" (p.41).
- Citation: SP p.26-27 (PDF 30-31); pp.33-36 (PDF 37-40); p.41 (PDF 45).

### M32: Reading redivision chains as sentences
- Category: word-play
- Rules: Consecutive hidden words (plus explicit text and character-number "words") are parsed as a
  sentence, with omitted verbs or prepositions supplied by geometry or parallelism.
- Examples: IAMNOTSICKIAMINSANE = SON (IAMN), BERTA (TSICK), EUGENE (IAMINS): "a family portrait"
  (p.37). OWNETTTH = MY NAMES (MY NAME IS), then ATSAID = GIRL, then #299 (HENRY), then OWHENIAS =
  MYSELF: "MY NAME'S GIRL; HENRY['S] MY SELF" (p.42). INPAR: the I is #228 (EUGENE) and PAR = MIKE, so
  "EUGENE in MIKE"; ONTOPOFEVERY = "ON TOP OF HENRY" (p.45). DITOR at #6 (ME) = "ME SON" (p.41).
  LLECTINGOFSLA = DRINKING + GENIUS, "a drinking genius" (p.45). PENN'S FANTASY = MIKE'S FEMALE (PENN
  and GAR are MIKE redivisions; FANTAS = FEMALE) (p.43). EUGENE #2 is EVIL (adjective preceding SOFI)
  (p.32). FATHER #2 is BRUTAL (BLANKS) (p.28). NRATHERANGRY = "FATHER ANGRY" (p.31). "I HAD TO" literal
  and redivided (SHADTO, RHEADTO) = the victim's "muffled outcry" (p.49).
- Citation: SP p.28 (PDF 32); p.31-32 (PDF 35-36); p.37 (PDF 41); p.41-43 (PDF 45-47); p.45 (PDF 49); p.49 (PDF 53).

### M33: Literal strings, monograms, initials and acrostics
- Category: acrostic/word-play
- Rules: Look for literal (not redivided) monograms and initials, including across word boundaries.
  Read the first letters of the rows of a 17-column grid.
- Examples: ERO (Eugene Robert O'Hare's monogram) twice in the cabby letter (p.22). BM (Berta
  Margoulies) in Row 35 (p.52). SOM = Skidmore, Owings & Merrill (O'Hare's first employer); SOM and JOB
  (UTTONS) are 9 apart; SOM/JOB 4x9; and a ONE-rectangle joins the end of SOM to the beginning of ARTHUR
  (INCHEC), i.e. SOM to Arthur D. Little (p.36). Acrostic: Feb 1974 (SLA) letter in 17 columns reads
  DUALG, and "G is Morse 110, a redivision of ME" = DUAL ME (p.40). The initials of HURTING and SADISM
  are in the same column (p.20). Literal PI strings (p.11).
- Citation: SP p.11 (PDF 16); p.20 (PDF 24); p.22 (PDF 26); p.36 (PDF 40); p.40 (PDF 44); p.52 (PDF 56).

### M34: Roman-numeral letters
- Category: letter-number
- Rules: Letters (or letter pairs) that are Roman numerals take their value.
- Examples: In the LA Times letter the highlighted C (Roman 100 = GENE) is also #228 (EUGENE) (p.31). IL
  (non-standard Roman 49 = 7²) begins at #7 (p.39).
- Citation: SP p.31 (PDF 35); p.39 (PDF 43).

### M35: Synonym, formula and paraphrase substitution ("implied" words)
- Category: word-play
- Rules: A word that is not present can be "implied" by a synonym, chemical formula, slang term or
  translation, whose Morse is then redivided. Semantic relatives are expected to align.
- Examples: SALT → NaCl → NACL (10 01 1010 0100) = TIMEX; OUCA (the only TIMEX) and SALT make 6x17 →
  617 = TIMEX (p.54). PI as a paraphrase for OHARE (because π's binary fraction spells OHARE backwards)
  (p.44). BOMB = "bombshell", i.e. secret disclosed (pp.15, 46). HOLE = female reproductive tract; ROCKS
  = testicles (#196 = 14²) (p.36). KIN = FAMILY (p.56). BUST = BREASTS (p.35). THE TRUTH = VERITAS (p.51).
  FIFTH (a bottle) and OSOMETH (BOTTLE) align with #228 (p.31). POP = FATHER (KNOWI, POWE, WAMP)
  (pp.27-28, 46).
- Citation: SP p.31 (PDF 35); p.35-36 (PDF 39-40); p.44 (PDF 48); p.46 (PDF 50); p.51 (PDF 55); p.54 (PDF 58).

### M36: The binary fraction of π spells names (reversed)
- Category: Morse/binary; numerology
- Rules: Write π's fraction in base two and redivide the bits as letters, read forward or reversed.
- Examples: "The name OHARE is spelled by the fraction of π (albeit in reverse, as ERAHO)". ERAHO =
  0010010000111, the first 13 binary places of .14159… [verified]. ILDUM is "the fraction of π written
  to the base two and carried out to thirteen places" (#1416) (p.14). "There are six passages
  expressing the fraction of π to at least thirteen places in the literature, no more than one per
  document." THREE = BER (am) I, "in which the verb 'am' is understood" (p.22).
- Citation: SP p.14 (PDF 19); p.22 (PDF 26).

### M37: Rebus/pun from pictures, logos, place names and ZIP codes
- Category: word-play/pun; map/geography
- Rules: Combine the themes or found text of greeting cards, or the logos and ZIPs on enclosures,
  into names and numbers.
- Examples: Pen Card + Dragon Card: PEN + DRAGON = PENDRAGON → King Arthur → Arthur D. Little, Inc.
  (O'Hare's employer). The Incline Village (Boise Cascade) postcard: UNIT6 = UBBERW (p.21-22). The
  June 1970 Contra Costa road map was published by Phillips 66, so 66 = 1966 (the "bomb" on the map is
  a "bombshell" revelation of Riverside) (p.15). Pleasanton mail drop: ZIP 94566 (p.15). The Hallowe'en
  card's printed "secret pal": PAL 0110 01 0100 contains MIKE, "found material" (p.46). "CLOUDY DAY
  DISCONECT" (Circuit B of the Bus Bomb): 7 September, Berta's birthday, "which Roman Catholics observe
  as the festal day of St. Cloud" (p.48). O'Hare's chosen city BERK(eley) = BERTA: "Being in BERK is
  the same thing as being in BERTA" (p.56). The SAC term "Reference Point" and the return address "R.P."
  (July 1974) (p.6).
- Citation: SP p.6 (PDF 11); p.15 (PDF 20); p.21-22 (PDF 25-26); p.46 (PDF 50); p.48 (PDF 52); p.56 (PDF 60).

### M38: Crime-scene and authentication objects chosen for their digital spellings
- Category: other (behavioral reading)
- Rules: Explain each physical choice (object, garment, demand) by the Morse redivision of its name.
- Examples: The bloodstained shirt-tail: BLOODSTAINED contains ODSTAI = OHARE, "The bloodstain itself
  conveys the name OHARE" (a driver's licence would not: LICENSE has no OHARE) (p.22). The desktop (DESK =
  517 = skeleton of BIRTH and THE END) (p.56). The "lift" (LIFT = 517 = THE END) (p.56). CAR DOOR (1010
  01 010 100 111 111 010) contains RECTUM (p.56). The hood: HOOD = 0000 111 111 100 contains MOM, "He was
  in MOM. The day was TIMES 17" (p.56). The car keys: THEKEY = BERTA, "a secret within a secret" (p.53).
  The Timex watch: TIMEX = 617; the only WATCH is crossed by RIWIS (BATES/DEATH) at #266, and BATES is a
  perfect redivision of DEATH (p.54). Battery/BATTERED in THE CONFESSION: BATTERE = EUGENE, BATTERY
  ("assault and battery") (p.29). KNIFE redivisions GGESTS, YWHENA (p.53).
- Citation: SP p.22 (PDF 26); p.29 (PDF 33); p.53-54 (PDF 57-58); p.56 (PDF 60).

### M39: Misspellings, solecisms and errors as deliberate devices
- Category: typography/handwriting; word-play
- Rules: Every anomaly ("disorder") exists "for the purpose of creating order on a less obvious
  level". Show that the correct form would destroy a redivision or shift a character number.
- Examples: NUCENCE (SQUARE) (p.11). PHOMPH IT (PHI) (p.11). CROOKED replacing Gilbert's "twisted" (else no
  TORTURE) (p.13). DANGERTUE (TUE) (p.16). PARADICE (lands on 9/7) (p.16). NICE IMPRIEST (CEIMPRI =
  TRIANGLE) (p.18). "Washington and Maple" instead of Cherry gives PLESTL = ELEVEN, an error made "because
  he wanted an ELEVEN" (p.18). "most delicious of pain" and "torture ... to" his slaves (else no SOFP
  EUGENE, no WOMAN) (p.28). The misspelled WOMAN moves MAN to #121 (p.33). PESTULENTUAL (HEPESTUL =
  EIGHTEEN at #169) (p.49). BROWNETT (gives OWNETTTH = MY NAMES) (p.42). CHRISTMASS (gives ASS with MISHAL)
  (p.43). Misspelled DARK (gives ARC) (p.52). Abnormal word order "AWAY FROM THE LIBRARY WALKING" (p.27).
  The strike-out: LOOSE, COMPLET (struck), ALL; the crossed-out word divides OHARE (LOOSE ALL contains
  OHARE) "in two", an expression of duality (p.25) [LOOSEALL→OHARE verified].
- Citation: SP p.11 (PDF 16); p.13 (PDF 18); p.16 (PDF 21); p.18 (Drive jpeg 66937d…); p.25 (PDF 29);
  p.27-28 (PDF 31-32); p.33 (PDF 37); p.42-43 (PDF 46-47); p.49 (PDF 53); p.52 (PDF 56).

### M40: Hapax and frequency arguments (control-text baselines, probabilities)
- Category: other (statistics)
- Rules: Rarity gives robustness. "Hapax" = the only occurrence in the corpus. Compare expected
  counts against a control text (the Gettysburg Address, ~5% of the corpus by volume). Compute
  chance as 1/2^(digits) x 1/17, etc. A deficit is evidence that spontaneous occurrences were
  "edited out ... to prevent meaningless and unintentional occurrences from diluting its value".
- Examples: SQUARE (16 digits): 1/65,536 x 1/17 = "one in just over a million" for the observed
  placement (p.11). TORTURE is "nineteen times more likely to have occurred anywhere else" (p.13).
  OHARE occurs 3 times in the Gettysburg Address, so ~60 would be expected in the corpus, but there are
  7: "the dog did nothing in the night time" (p.22). ROBERT: 3 in Gettysburg, ~60 expected, 1 found
  (p.23). An 11-digit spelling at a given location = 1/2048; converging EUGENEs ≈ 1 in 3.5 billion
  (p.32). Crossed circles on squares = 1/1670 (p.7).
- Citation: SP p.7 (PDF 12); p.10-11 (PDF 15-16); p.13 (PDF 18); p.22-23 (PDF 26-27); p.32 (PDF 36).

### M41: Comparative authorship (same figures in O'Hare's signed texts)
- Category: other
- Rules: Run the same analysis on texts published under O'Hare's name. Matching configurations
  (crossed EUGENEs, ONE-rectangles, #66-TIMEX, calendars, MOTHER squares, MIKE/NAME intervals) are offered
  as proof of the same author. Authorship by statistics is precedented (the mathematician who identified
  the author of *Primary Colors*).
- Examples: Dissertation preface (May 1973): HEAMERI #81 and DIOFF #121 (BATTERER) (p.29); DUNIV at #66
  (BATES/DEATH) with RANDG (TIMEX) in Row 39, 9x36 = 324 (p.54). Fifth Anniversary Report: ENGINEERING and
  MATHEMATICS form an 11x11 square with the "label" 196 (14²) (p.36); I-pronouns at #100/#202 (p.51).
  Tenth Anniversary Report: BURC/BURB, HOUS next to #1045 (p.38); FWHATSE (RADIANS) at #1416 (p.51); the
  three tableaux (p.55). 1987 press statement: crossed EUGENEs (p.33); the MOTHER square reversed (p.50).
  Wolves letter (Jan 1995): BEENTR/BERK and SOFI at #228 (p.32); ERICANO (IDENTITY); REDIVIDE = RED
  SUITS and WOLV = MORSE, "the reason he chose this subject" (p.51). University Herald (Apr 1996): SOFA/
  CEJUS (p.26); YONEB/#218 (p.48). "Reflections on trust and confidence" (1994): FWEDO/#66 (p.54);
  RKEYSW (21857) and PETENCEB (PECKER) (p.49); EROUR/FOUR (p.53). The Berta Margoulies obituary (SF
  Chronicle 1996, family-written): LIVED 8x11 = 88; EARTSIN/PECTIV 7x7; TEANDT/#66 (p.33, 39, 54).
- Citation: SP p.7 (PDF 12); p.26 (PDF 30); pp.29-55 passim; esp. p.50-51 (PDF 54-55).

### M42: Probabilistic "speaking" coincidences in personal names
- Category: word-play
- Rules: Show that names of the relevant people redivide into related names.
- Examples: GAR(eth) and PENN are both MIKE redivisions (GAR = 110 01 010 = MIKE; PENN = 0 + MIKE). Penn
  calls it "One of the more ironic coincidences" (p.43). Carol BURChard (O'Hare's wife): BURC = BERTA,
  "a digital continuation of the incest" (p.56). CAROL twice in the Tenth Anniversary Report gives a
  √202 (MIKE) right triangle (p.39). MARGOULIES vs the obituary misspelling MARGOLLIES (p.33).
- Citation: SP p.33 (PDF 37); p.39 (PDF 43); p.43 (PDF 47); p.56 (PDF 60).

### M43: Literal hidden words (redivision of literal letters across word breaks)
- Category: anagram/word-play (literal)
- Rules: Ordinary letter strings across word boundaries (no Morse).
- Examples: LEGEND/LEG END, WEEKNIGHT/WEE KNIGHT (as illustrations, p.8). Literal PI strings, ERO, BM,
  SOM, "IS EVEN" (literal S-EVEN across the word break, cited as a SEVEN-redivision, p.39), THE M OTHERS (two
  "literal redivisions" of MOTHER, p.24). SPACE/SPA/ACE/PA "occupy the same space" (p.60).
- Citation: SP p.8 (PDF 13); p.24 (PDF 28); p.60 (PDF 64).

### M44: Tutorials (the Zodiac teaches the reading method)
- Category: other (framework)
- Rules: The "author" must supply tutorials, like the first row of the Arecibo message (1-10 in
  binary). Their value "derive[s] from reference to things about which there is no disagreement":
  mathematics (1+1=2, Pythagoras), historical facts (Fourth of July), and family relationships.
- Examples: The ONE/TWO arithmetic (M14), 2=10/3=THEB (M3), ALIVE/DEAD (M11), PI/#314, POSITIVE/NEGATIVE,
  ZODIAC/NAME, the radian 2NINE, and the Hole Card calendar ("does not require anything as esoteric as
  Morse Code").
- Citation: SP p.9-10 (PDF 14-15); p.12-17 (PDF 17-22).

### M45: "Meta-writing": overlap and compression as the theory of the text
- Category: other (framework)
- Rules: There are four "general answers" for how so much fits in ~4000 words. (1) Forms overlap
  (SPACE/SPA/ACE/PA), especially in digital writing. (2) Connective words are supplied by geometry (the
  ONE-rectangle replaces "is"/"and"). (3) Intervals and character numbers carry meaning, and material can
  sit inside intervals or the empty centre of squares. (4) Elements are shared between configurations, as
  in a crossword. "If you want to put a name on it, call it 'meta-writing'": O'Hare's own 1964 term
  ("art made up of writing in which the graphic form is more interesting than the verbal content").
- Citation: SP p.22 (PDF 26); p.47 (PDF 51); p.60 (PDF 64).

### Methods on the brief's "already known" list, as found in this source
- 17-column grid (M6); row,column read as number, PI at 31,4 (M16); position numbers such as #1030
  (vertical BSP) = 10/30 (M19/M22); row-column intersections (M16); Morse to binary with ONE=60, TWO=95,
  MIKE=202, DEATH=1072, BUS=520, THE END=2068 [digital value not stated here, only the 517 skeleton]
  (M1, M5); redivision BUS↔THREE (M2); calendar reading (M20); perfect squares (passim);
  right-triangle hypotenuse (M12); "expressive difference" as intervals (M13); expressive postmarks
  (year-day 333, year-day 314; the LA Times postmark the day after PI) (M23, M20); π proportion 390:18 ::
  3:0.14159 (M25); keyboard shift &#=73 (M27); hapax (M40); acrostic DUALG (M33); Roman numerals C=100,
  IL=49 (M34). **Not found in this booklet:** taxicab numbers, the WIZARD/reverse-alphabet cipher,
  A=1..Z=26 alphanumeric values, anagrams, radian geometry on the Mt. Diablo map (the postscript is
  discussed only as Morse/INCEST/keyboard), and the EIGHT=193 / BIRTH=8272 / RADIAN=4870 values (BIRTH
  appears only as a Morse string).

---

## Puzzle-relevant remarks

- **Predictions and bets as proof.** "I am willing to bet a substantial sum of money that when the text
  [of the unpublished Examiner cover letter] is available, it will be found that there is an
  OHARE-redivision and that it forms a two-way square with NAME #1" (p.25, PDF 29). Calendars are
  "predictive tools", and the LA Times postmark the day after PI shows the Zodiac "knew his schedule in
  advance" (p.15). Note that he anticipates content in unseen text.
- **How hidden messages should be built (his model of the author).** You must hide something while
  remaining readable: use "some kind of universally accessible system of writing (e.g. Morse Code)" and
  supply tutorials. Value rests on rarity (hapax). Edit out spontaneous occurrences so they don't dilute
  the signal. Use misspellings, word-order disruption and solecisms to tune positions. Make "a secret
  within a secret" (THEKEY). Overlap, share elements and let geometry replace verbs (pp.10, 22, 53, 60).
  Publication should "hinder, defer, or even prevent entirely, comprehension. To make it a fair
  challenge, tutorials would be written in" (p.47).
- **Favourite keys and numbers.** 17 / times-17; squares; 130 (BER) and 130π; 202 (MIKE); 228 (EUGENE);
  100 (GENE); 299 (HENRY); 78 (NAME); 1045 (BERTA); 4183 (BERTA M); 127 (MOM); 221 (MAMA = 13x17); 35
  (BM); 60/95 (ONE/TWO); 520 (BUS = THREE); 1072 (DEATH = BATES); 1345 (INCEST); 306 (TIMER); 617
  (TIMEX); 38 (TIME); 516/517 (LIFE / BIRTH and THE END skeleton = DESK = LIFT); 9745 (TIMES17 =
  9/7/45); 9/7 (Berta's birthday); 22 Jan (O'Hare's birthday); 10/30/66 (1030, #66); 14 and 7 (ages);
  1957 and 2/18/57 (TWO18, 21857); 1981 and 5508 (= 324x17); π/314/1416; φ/618; 1623 (MIKE O); 12944
  (GARETH). ZIP 94566 (Pleasanton). Phillips 66.
- **Penn's own name in the system.** GARETH = 12,944, and GAR and PENN are both MIKE redivisions (p.43).
  "PENN'S FANTASY" = "MIKE'S FEMALE" (p.43).
- **Play with names.** His correspondent Kevin Hess styled himself "Kevin x 2¹¹" because HESS is eleven
  zeros (p.60). This is the kind of digital pun Penn enjoys.
- **What a "good" message is.** Formatting is meaning ("meaning will be provided by the format
  itself"). Mathematics "transcends culture" (Arecibo, Gauss). Coincidence must be "artful", not
  "accidental": "The more of these coincidences we find, the lower the probability that they are of the
  accidental variety" (p.2). He answers the pyramidologist objection: unlike the Egyptians, the Zodiac
  "explicitly claims to be revealing his identity in some kind of code" (p.2).
- **Penn's search tooling.** He digitized all texts and searched with Word find and "find file". He
  converted digital positions to literal ones with ÷2.58 (p.9). "Since the computer can find or rule out
  anything in a matter of seconds, I've indulged myself in a lot of searches" (p.42). Many results are
  therefore cherry-picked from large word lists.
- **Authorship-by-statistics framing.** "it was a mathematician who identified the author of the
  pseudonymous best-seller, *Primary Colors*, using mathematics as an analytical tool" (p.2). Readers
  are urged to write to the California Attorney General.
- **Insurance/lottery/haiku/anagram-priority.** Not mentioned in this booklet. The nearest are gambling
  odds (roulette 1/1444, p.7) and the bet above.
- **Errata insert (PDF 3-4).** Penn admits to working "between three and five o'clock in the morning"
  and lacking anyone "fluen[t] in Morse Code" to proofread. Corrections: p.8 CEL/57-digit wording; p.14
  "1 #2" should be "1 #1"; p.18 PLESTL wording; p.23 ATTENTH should be ATTHENTH (verified: ATTHENTH
  contains OHARE, ATTENTH does not); p.34 YELECTRIC should be YELECTR; p.35 HOOT should be HOOTB; p.41
  HOTA/HOTH also form a 10x10 square; p.43 MISHAL–ASS interval 68 (4x17) should be 51 (3x17); p.46 "Chronicle
  cover letter" should be "Vallejo Times-Herald cover letter"; p.47 "second" should be "third"; p.48 "MIKE-redivision
  MINA" should be "GENE-redivision MINA", and "doesn't calendars" should be "doesn't make calendars". Also
  historical corrections from Jake Wark (Unabomber-theory origin; Kathleen Johns publicity; the .38/9mm
  bullet; the Shepard knife injury, which he will "omit ... from future editions").

---

## Bibliography leads (Penn's own writings and appearances mentioned)

- *TIMES 17* (book, self-published, April 1987; "a 320-page book"; 3 pages refute Graysmith's astrology
  theory). Cited throughout. Contains the handwriting comparisons and the Joan Webster attribution.
- Article in *California* magazine, November 1981 (on the Zodiac; repeated the 9mm claim) (Errata).
- 90-minute presentation, International Association of Forensic Sciences conference, UCLA, August 1999
  (Foreword).
- Article based on the same material "accepted for publication by *Cryptologia*" (1999) (Foreword).
- *The Second Power* (1999) itself: "subsequent press runs will be corrected" per the Errata, so more
  than one printing is implied.
- Media: KCZN Ventura talk show with Anthony Hilder, 29 May 1987 (O'Hare ambushed on air); General
  Broadcasting System (Jerome Maltz) talk shows; WBZ and WNEV (Boston) satellite interviews, Oct 1987;
  Boston Herald two-page article, 29 Oct 1987 (Eric Fehrnstrom); Harvard Crimson, 30 Oct 1987 (called
  TIMES 17 an "astrology" book); Beverly Times, 16 June 1990 (Webster remains). Mentions *America's Most
  Wanted* (O'Hare not named after a lawyer's letter).
- Other works he relies on: Robert Graysmith, *Zodiac* (St. Martin's, 1986).

---

## Biographical facts about Michael O'Hare and targets (ingredients of Penn's readings)

- **Michael Henry O'Hare**: born 22 January 1943 (GIVETH/BIRTH on 22 Jan; 22BIRTH). Age 7 in 1950, 14 in
  1957 (the incest dates Penn alleges: 1950 with the mother, 2/18/57 with the father), and 23 at the
  Riverside murder (ODIECU at #23). 9745 days old on 27 Sep 1969. Harvard Class of 1964. As an
  undergraduate he edited *Cambridge 38*; in Feb 1964 he published "First term in the Carpenter Center"
  (introduces "meta-writing"). First post-college employer: Skidmore, Owings & Merrill (SOM). Then Arthur
  D. Little, Inc. (ADL), transferred from Cambridge to the San Francisco office for four months in 1967-68
  on the Boise Cascade project (Incline Village, Unit 6, Nevada; Reno/Sparks/Washoe Regional Planning
  Commission). Marriage-licence application April 1969 to Carol Burchard (all caps except a lower-case g in
  "MARgOULIES"). Ph.D. in applied mathematics, Harvard, dissertation filed May 1973. Contributions to
  the Harvard Class of 1964 Fifth (1969) and Tenth (1974) Anniversary Reports. In 1987: a 44-year-old
  Harvard lecturer (JFK School letterhead), estate in Vermont, three-story house in Brookline (p.58). [inferred from p.59: a
  trick-or-treater says kids gave "#12" on Abbottsford Road a wide berth.] Moved to California in fall 1990 to UC Berkeley and lives in Berkeley (BERK = BERTA).
  Writings: October 1987 press statement (~100 words); "Reflections on trust and confidence" (1994,
  Berkeley public policy school web page); Wolves letter, SF Chronicle editorial page, January 1995;
  letter in Harvard's *University Herald*, April 1996. Attorneys: Jeffrey Rudman (Hale & Dorr, Boston;
  Carol Burchard O'Hare also worked there) and later Jeffrey Nussbaum (Stein & Lubin, SF). Penn says
  O'Hare relayed a lawsuit threat via the FBI around his 38th birthday (1981).
- **Social Security number:** Penn claims (p.26, PDF 30) that OMENTTHECHI in the Belli letter
  (December 1969) encodes O'Hare's SSN. He drops the leading digits and splits the remaining bits into four
  base-two groups, giving a 3-2-4 digit number "aligned with I/ME/MIKE/SELF". **The digits are withheld here
  for privacy**; the method is the split-bit-string reading in M3/M22.
- **Father, Eugene Robert O'Hare**: born 16 October 1906 (year-day 289 = 17²). An engineer, the
  "square". Monogram ERO. Died about six years before the 1987 press statement (~1981). Penn casts him
  as a drunk and batterer (unsupported).
- **Mother, Berta Margoulies (O'Hare)**: nickname BER (= 130), monogram BM (= 35). Birthday 7 September
  (9/7; her 38th birthday was 9/7/45, so born 1907) (feast of St. Cloud). Born and raised in Poland, Jewish,
  "a prominent sculptor" trained "in the best art schools in Europe". Moved to the Bay Area from
  Massachusetts in 1990 at age 83. Died March 1996 aged 88. Obituary in the SF Chronicle (it misspelled
  her name MARGOLLIES).
- **Other targets**: Joan Webster, a Harvard graduate student abducted from Logan Airport, Boston, and
  murdered 28 Nov 1981. Her suitcase was left in a locker at the Greyhound terminal and her remains were
  found in Hamilton in April 1990. Penn attributes her murder to the Zodiac and O'Hare. Riverside victim
  Cheri Jo Bates (30 Oct 1966). Kathleen Johns (March 1970 kidnapping).
- **Penn's own background**: graduate student in a literature department, and German medieval poetry
  is mentioned. His father Hugh Penn was a statistician at the California Department of Justice and a
  "former military cryptographer"; Hugh noticed the word "radian" in a suppressed July 1970 letter and
  told Gareth in late 1980. Penn says he works two jobs, one at sea on a research vessel (Errata).

---

## Verification notes (examples I could not reproduce with the chart's Morse)
- UNIT6 = UBBERW (p.22) **[did not reproduce]**: neither base-two 110 nor Morse 10000 for "6" fits.
- NDERLI = CHILD (p.31) **[did not reproduce]**: CHILD needs 17 digits and NDERLI has 15.
- GTO = TWO (p.49) **[did not reproduce]**: GTO = 1101111 and TWO = 1011111.
- CEWEREW = ANGLE (p.52) **[did not reproduce]**: EMATERI = ANGLE does reproduce.
- HE2TEEN = SECRET (p.46) works only if the following A is included (HE2TEENA).
- ME IAMFI = BATTERER (p.32) works only with the following N (IAMFIN, from "I AM FINDING").
- MARGOULIES = NAME (p.33) is semantic ("her name"), not a redivision.
- 73 x 57.2958 = 4182.6; Penn rounds to 4183 (BERTA M).
- Everything else spot-checked (well over 150 forms) reproduces exactly, including all the family-name,
  calendar, TWO18/21857, π-fraction and car-door-count examples.
