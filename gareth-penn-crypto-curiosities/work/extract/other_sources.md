# Gareth Penn method catalog: other sources (blog posts, letters, FBI files, third-party articles)

Extractor notes:
- Base path for images: `.../Zodiac/Solutions/Gareth Penn/attachments/<folder>/`. Text sources: `work/htmltxt/<file>.txt`.
- "Verified" means I recomputed the example with International Morse (dah=1, dit=0) or by counting
  characters in the transcribed text (script in scratchpad `verify/v.py`, `verify/v2.py`). All of Penn's
  numbers that I checked came out exactly right.
- **Redivision, as Penn actually uses it** (worked out from his examples, see gp26–gp27): write a run of
  consecutive letters (spaces and punctuation removed) in Morse bits. The run is a "digital redivision"
  of a target word if the target's bit string appears inside it, **starting inside the first letter and
  ending inside the last letter**. Partial letters at both ends are allowed. Example: KNIFE
  `101100000100` sits inside GGESTS `11011000001000` from bit 2 to bit 13. Exact full-letter
  redivisions (MIKE REVNEC = GARETH PENN, BLUE = BASE 2) are the special case with no leftover bits.

---

## 1. GZ4216 blog post of 7 June 2010 (Penn's own Q&A), image-only: gp1.jpg–gp34.jpg

Folder `2010 06 07 Gareth Penn (responding to Zamantha, I think)/`. Header on gp1 reads
"MONDAY, JUNE 7, 2010 / GZ 4216". These are Penn's answers to questions forwarded by "Zam"
(about 42 questions by his own count, gp31). I read all 34 images. gp34 ends mid-answer (Donna Lass
question).

### M: Morse-binary read as a fixed-point number (binary point inside the word)
- Category: Morse/binary; numerology/arithmetic
- Rules: write the word in Morse bits, put a binary point at a chosen letter boundary, and read it as a
  base-2 real number. Optionally append a day number in binary. Compare with a constant.
- Examples: "JULY written in Morse Code and read in base two, with a decimal point between U and L
  (0111 001.0100 1011) is 57.29…, replicating the degree-value of the rad to eight decimal places."
  Verified: 0111001.01001011₂ = 57.29296875. The first 8 binary places match 57.2957795…° =
  .01001011101110…₂, so "decimal places" means binary places. "Every date in July expresses the same
  number accurately to at least nine decimal places. The closest possible match in July is JULY 23
  (0111 001.0100 1011 10111), which is accurate to thirteen decimal places." Verified: JULY+23 gives
  57.2957763671875, which matches 13 binary places. Every other July day matches 9 to 12.
- What he claims it proves: the Zodiac's July 1970 letter using "radian" is self-referential. JULY
  encodes one radian in degrees.
- Citation: GZ4216 2010-06-07, gp8.jpg (answer to "radian theory is bunk … closer to 60 degrees").

### M: Calendar-year numerology (Hebrew year = degrees per radian)
- Category: calendar/date; numerology
- Rules: read a calendar-year number as digits of a constant.
- Examples: "The degree-value of the radian is 57.29…, and the Bay Area chapter of the Zodiac's career
  began in Hebrew calendar year 5729 (December 1968)."
- Claims: the start date was chosen to express the radian.
- Citation: gp8.jpg. Same answer: "I used the 1970 Bay Area map sheets published by the U.S. Geological
  Survey."

### M: Postage-stamp, map-brand and ZIP-code numerals ("66" = 1966)
- Category: numerology; other (nonverbal)
- Rules: read the denominations of the stamps on an envelope, side by side, as a number. Treat brand
  numbers and ZIP codes the same way.
- Examples: "The prevailing pattern was two six-cent stamps. In a June 1970 mailing, he enclosed a
  Phillips 66 map … The two six-cent stamps express the number 66, as does the map." The LA Times letter
  "was postmarked in Pleasanton, whose ZIP Code is 94566. All of these 66-references are nonverbal
  expressions referring to the year 1966."
- Claims: the Zodiac kept referring to 1966, the year of the Riverside (Bates) murder.
- Citation: gp16.jpg.

### M: Repeated mailing pattern as a "nonverbal statement" (Riverside ↔ Bay Area)
- Category: other (pattern/sequence)
- Rules: compare the structure of event sequences in two settings. The same structure means the same
  author.
- Examples: Riverside: the murder (Oct 1966), then letters a month later (both postmarked the same day),
  then on 30 Apr 1967 "three letters, one to the newspaper, one to the police, and one to the victim's
  father … the author put two four-cent stamps on all three envelopes" (postage was 4¢). Bay Area: the
  Dec 1968 murders, the 4 Jul 1969 attack, then at the end of July three letters to three newspapers,
  "Postage had gone up to six cents. He put two six-cent stamps on two of these envelopes and four on the
  third." "In each setting, Riverside and the Bay Area, the third event in the series of events consists
  of mailing three letters on the same day with excess postage." Translation offered: "The same person
  who has been committing these crimes in the Bay Area also committed the murder of Cheri Jo Bates in
  Riverside."
- Citation: gp15.jpg.

### M: Thirds (2/3 vs 1/3 partitions; dates as fractions)
- Category: numerology/arithmetic; calendar/date
- Rules: split a set of mailings or crimes into 2/3 and 1/3 by some attribute. Read a month/day date as
  a fraction.
- Examples: "two thirds of the April 1967 letters use the victim's name ['Bates had to die'] … two
  thirds of the July 1969 letters are franked differently [two stamps on two, four on the third], and
  the dates of the knife murders are two thirds" (the knife murders fell on "30 October and 27 September
  (10/30 and 9/27 both = 1/3)"). "The firearm-murders are similarly divided into two thirds, one third:
  two committed with the 9mm weapon and one with the .22-caliber." In the Webster case: three finds, two
  certain to be discovered ("i.e. two thirds"), gp17.
- Claims: a consistent "two-thirds" signature runs from Riverside to the Bay Area to Webster (1981).
- Citation: gp16.jpg, gp17.jpg.

### M: Morse value equals the product of physical numbers (GUN = 22 × 9)
- Category: Morse/binary; numerology
- Examples: "the word GUN in Morse Code, 110 001 10, is base-two 198, and that the calibers of the
  Zodiac's two guns, multiplied together, spell GUN in Morse Code: 22 x 9 = 198, or 22 x 9 = GUN."
  Verified: GUN = 11000110₂ = 198.
- Citation: gp16.jpg.

### M: Thematic word echoed by a physical act ("bus"), and contrived anniversaries
- Category: word-play/pun (nonverbal); calendar/date
- Rules: (a) a key word from earlier messages is "said" without words by choosing a matching place or
  object. (b) A crime date is chosen to fall on an anniversary of an earlier event ("light the fuse and
  let the calendar do his talking").
- Examples: Webster's suitcase was left in a Greyhound storage locker. "That finding would link her
  murder with the bus-theme" (the Zodiac's 1969–70 bus threats kept "bus" prominent for eight months,
  gp16). "The murderer expresses 'bus' and 'two thirds' without saying them." Dates: THE CONFESSION was
  postmarked 29 Nov 1966, and "28 November 1981 was fifteen full years, as the IRS and Social Security
  Administration reckon time, but it wasn't the anniversary." Two kinds of coincidence: spontaneous
  (Jefferson and Adams both dying on 4 July 1826) versus contrived (Oklahoma City on the Waco
  anniversary).
- Citation: gp16–gp17.jpg.

### M: Morse redivision used to build a pseudonym (MIKE REVNEC = GARETH PENN). Penn's own construction
- Category: Morse/binary; anagram-like (digital redivision)
- Rules: write the real name in Morse bits and re-segment the identical bit string into different
  letters to get a new "name".
- Examples: "Mike Revnec is a pseudonym I used to sign a letter or postcard to O'Hare (I forget which) a
  quarter-century or more ago … MIKE REVNEC (Morse 11 00 101 0 010 0 0001 10 0 1010) is a digital
  redivision of GARETH PENN (110 01 010 0 1 0000 0110 0 10 10)." Verified: both are
  `11001010010000011001010` (23 bits; value 6,627,530). "By May 1981, O'Hare knew that I was the author
  … he wasn't fooled by the Mike Revnec pseudonym. He also knew that it was actually not a pseudonym at
  all but my real name."
- Claims: O'Hare could read his Morse/binary language, so he knew who had signed.
- Citation: gp19.jpg.
- Puzzle note: this is the clearest evidence that Penn himself writes hidden messages by Morse
  redivision. (I also checked GEORGE OAKES `11001110101100111011010000`. It is not a redivision of
  GARETH (S) PENN.)

### M: Authorship comparison by searching for digital redivisions (his stated procedure)
- Category: Morse/binary (method)
- Rules (quoted): "Take a sample of texts published under the name of your suspect and digitize those
  texts, writing all numbers in base-two and transcribing all Roman-letter text into Morse Code, using 1
  for dash and 0 for dot. Do the same with the Zodiac texts. Now, using an application such as Word, you
  can search all those texts for digital redivisions … it will take only a little longer for you to
  locate those redivisions in the literal text. Having located them, where do they stand in relation to
  one another? What kind of relationships do they express? And if there is a consistent
  relationship-pattern in the texts written by the suspect, does it match another consistent pattern
  found in the Zodiac texts?"
- Cites as precedent Thisted & Efron, "Did Shakespeare write a newly-discovered poem?" Biometrika
  74:3:445-455 (1987), the *Primary Colors* attribution, and Soviet-bloc intercept comparison.
- Citation: gp24.jpg.

### M: Calendar counting from a dated landmark (Hole Card: PI = 14 March = 3/14)
- Category: calendar/date
- Rules: "Zodiac documents contain calendars. A landmark or two is created using a date or some other
  information pinpointing a particular day. Other dates can be established by their relationship to a
  landmark, counting each alphanumeric character as one day."
- Examples: the Hole Card (postmarked 6 Oct 1970) is "dated by the author ('Oct. 5, 1970')". It calls
  the police "pig cops". "The PI of PIG is the only one of its kind in this text. If the O of OCT 5 =
  5 October, and if each subsequent character = one day, then PI = 14 March, a date written numerically
  as 3/14 (π = 3.14…)." [inferred: P lies 160 characters after the O, since 5 Oct 1970 → 14 Mar 1971 =
  160 days.]
- Citation: gp25.jpg.

### M: Redivisions plus calendar back-count in O'Hare's own 1994 text (FOUR, FATHER, KNIFE)
- Category: Morse/binary; calendar/date
- Source text (Penn's transcription, spaces/punctuation removed; O'Hare, "Reflections on trust and
  confidence", Goldman School website, 1994). Penn bolds the letters shown here in [brackets]:
  `WHATTHISLASTEXAMPLESU[GGESTS]TOMEISTHATTHEKEYIDEAUNDERLYINGTRUSTANDCONFIDENCEININSTITUTIONSISNOT`
  `SOMUCHTHEIRVALUESORGOALSNORTHEIRCOMPETENCEBUTTHEIRPREDICTABILIT[YWHENA]WILDEYEDCHARACTERWITHAP`
  `ISTOLSAYSHEWILLSHOOTUSIFWEDONTHANDOV[EROUR]CARKEYSWEKNOWTHATHISINTERESTSAREVERYPOORLYALIGNEDWIT`
  `HOUROWNWEMAYALSOTHINKHISAIMPOORANDHISSELFCONTRO[LRATHER]LABILENEVERTHELESSWEACTPRECISELYASWEW`
  `OULDI[FOUR]MOTHERSAIDLENDMEYOURCARDEARIWANTTOSHOPFORYOUR[BIRTHDAY]PRESENT` (439 characters)
- Rules/examples (quoted): "this passage contains two redivisions of FOUR (ER OUR, [I]F OUR; F = Morse
  0010, ER = 0 010) and one redivision of FATHER (LRATHER; F = 0010, LR = 0100 010). If the B of BIRTHDAY
  = the author's birthday (22 January), then the FOURs fall on the fourth of July and the fourth of
  December. FATHER begins on 16 October, the author's father's birthday." "This text contains two digital
  redivisions of KNIFE (101 10 00 0010 0): GGESTS (110 110 0 000 1 000) and YWHENA (1011 011 0000 0 10
  01). The difference between GGESTS and YWHENA is 136 characters, the product of the operation 8 x 17."
  The literal level supplies a matching reference: "When a wild-eyed character with a pistol says he will
  shoot us if we don't hand over our car keys" = Lake Berryessa (pistol, car keys).
- Verified: B of BIRTHDAY is at position 425. Counting backward one day per character from 22 Jan: E of
  EROUR (pos 223) = 4 July; F of IFOUR (pos 376) = 4 December; L of LRATHER (pos 327) = 16 October.
  An exhaustive search of the passage finds exactly these: FOUR = EROUR and the literal FOUR; FATHER =
  LRATHER (target starts at bit 4 of L); KNIFE = GGESTS (pos 22) and YWHENA (pos 158); 158−22 = 136.
  The letter used as the "date" is the first letter of the redivision window, even when the target
  starts partway through it (the L of LRATHER).
- Also stated: TIMES 17 = 1 00 11 0 000 10001 = 9745 = O'Hare's age in days on 27 Sep 1969 (verified).
- Claims: O'Hare's 1994 prose carries the same encodings as the Zodiac's (Independence Day, KNIFE,
  multiples of 17, father's birthday).
- Citation: gp26.jpg.

### M: Distance between redivisions as a multiple of 17
- Category: Morse/binary; numerology (17)
- Examples: THE CONFESSION (1966) passage
  `MAYBESHEWILLBETHEBEAUTIFULBLONDTHATBAB[YSITS]NEARTHELITTLESTOREANDWALKSDOWNTHEDARKALLEYEACHEVENINGABOUTSEVENORMAYBESHEWILLBETHESHAPELYBLUEEYEDBROWNETTTHATSAIDN[OWHENI]ASKEDHERFORADATEINHIGHSCHOOL`:
  "the only two KNIFE-redivisions in the text, YSITS (1011 000 00 1 000) and OWHENI (111 011 0000 0 10
  00). The difference between them is 119 characters, the product of 7 x 17." A 1961 text "published
  over Michael O'Hare's name — by his father" (Vin Fiz / Calbraith Perry Rodgers anniversary; contains
  "SPENT180000TOMAKE"): "three KNIFE-redivisions. The first two are YISB (1011 00 000 1000) and YHAV
  (1011 0000 01 0001). The difference between the two is 408 characters (24 x 17)."
- Verified: YSITS at 38 and OWHENI at 157 (0-based), difference 119. YISB to YHAV is 408 only if the
  digits "180000" count as 6 characters (one per digit). This is a counting rule: numerals count as one
  character per digit when measuring distances.
- "These are just a couple of hundreds of examples."
- Citation: gp27.jpg.

### M: Old Norse etymology (SLA letter)
- Category: word-play/linguistic
- Rules/examples: the Zodiac's SLA letter cites Old Norse *slá* as meaning "to kill". Penn says it means
  "to beat, to strike". Wrongly equating it with English "slay" shows the writer used an English-language
  dictionary that gives *slá* as a cognate of "slay" without defining it. Penn identified which
  dictionaries on public-library reference shelves could be the source.
- Claims: an educated writer who has not studied Old Norse, which contradicts Miron's "high school"
  profile.
- Citation: gp28–gp29.jpg.

### M: Formal ("nonverbal") properties of the four ciphers
- Category: grid/geometry; numerology
- Examples (gp30): n × 17 format: #1 and #2 are perfect rectangles. #4 (17 + 15 symbols) is "an imperfect
  rectangle conforming to the formula", so #3 is "another imperfect example". Symmetry: "The first cipher
  has four crossed circles and nine Zs, while the second has nine crossed circles and four Zs." #3: 13
  symbols (prime) with the crossed circle at #4 (power of two). #4: crossed circle at #29 (prime) with
  32 symbols (power of two). The first crossed circle falls at #100 in #1, #49 in #2 and #4 in #3:
  "Three in a row, all perfect squares." "The square roots of these numbers, 10, 7, and 2, respectively,
  replicate the word DEATH written in Morse Code and read as a base-two number (DEATH = 100 0 01 1 0000
  = 1072)." Verified: DEATH = 1072.
- Citation: gp30.jpg.

### M: Turning a number-word into a number ("three eights" = 579)
- Category: Morse/binary; grid positions
- Examples: in the 13-character cipher, the 8-in-a-circle symbol (unique to this cipher) "appears as
  symbols ##5, 7, 9". "What if I asked you not how much three eights are where 'eight' is a number but
  where 'eight' is a word? … If you write EIGHT in Morse Code, using 1 for dash and 0 for dot, you get
  this: 0 00 110 0000 1, base-two 193. Now, if EIGHT = 193, then how much are three eights? You would
  answer 579 (3 x 193 = 579). Note that this result matches the symbol-numbers of the three eight-ball
  symbols." Penn's reading: "If you want to read what I have written, make use of Morse Code written in
  the form of base-two number." Verified: EIGHT = 193.
- Citation: gp30.jpg.

### M: π proportion in the 408 (390 : 18)
- Category: numerology
- Examples: "the 390 letters of English and eighteen of gibberish in the first cipher express the
  proportions of the integer and fraction parts of the natural number π (390 = 3 x 130, 18 = 0.14159…
  x 130)."
- Citation: gp30.jpg (says it was first pointed out in T17).

### M: TIMES 17 = 9745 (from the n × 17 format)
- Category: Morse/binary
- Examples: "the general formula n x 17 expresses the phrase TIMES 17, which, when read digitally (1 00 11
  0 000 10001) is base-two 9745, the date of Michael O'Hare's mother's 38th birthday and his age in days
  on the day of the Lake Berryessa murder." Verified: 10011000010001₂ = 9745, and 22 Jan 1943 → 27 Sep
  1969 = 9745 days. [inferred: "date" = 9/7/45 read as M/D/YY, so Berta Margoulies was born 7 Sep 1907.
  Not stated explicitly.]
- Citation: gp31.jpg; also gp26.jpg.

### M: Fraction written in binary gives a monogram (13/17 → MHO)
- Category: Morse/binary; numerology
- Examples: "Let's assume … that the third cipher also conforms to the n x 17 formula. The smallest
  perfect rectangle … would be 1 x 17. This cipher is 13/17 of that. The fraction 13/17 written to the
  base two is 0.110000111…, which expresses the monogram M (11) H (0000) O (111)." Verified: 13/17 =
  0.11000011 11000011…₂ (period 8).
- Claims: Michael Henry O'Hare's initials.
- Citation: gp31.jpg.

### M: Colour as code: BLUE ink = BASE 2 (mixed Morse plus binary numeral)
- Category: Morse/binary (redivision)
- Examples: "all of the Zodiac's handwritten letters are executed in blue ink. The word BLUE in Morse Code
  (1000 0100 001 0) is a redivision of BASE 2 (1000 01 000 0 10). Blue writing is base-two writing. This
  information is conveyed by a color — i.e. nonverbally." Verified: BLUE = BASE·"10" =
  `100001000010` exactly. The numeral 2 is written in binary ("10") inside the Morse string.
- Citation: gp31.jpg.

### M: Biographical-document anomalies as "story" signals (non-cryptographic, but they feed his keys)
- Category: other
- Examples: the turning point was an entry by O'Hare's mother in a biographical directory. It named her
  son "with his full name, including the middle name" but described her husband only by marital status.
  O'Hare's employer's personnel records showed assignment to its San Francisco branch "to do planning work
  on a vacation home project that was subsequently depicted on a Zodiac postcard". A later
  biobibliography "omitted two years of his employment with that employer (1969-1970)", while his 1973
  dissertation and a 1969 journal article show it. Comparison "going all the way back to 1961".
- Citation: gp25.jpg.

### M (idea): Base-two "bouncing ball" sing-along
- Category: other (Penn's own imagined device)
- "I would envision a Zodiac movie as a drive-in movie sing-along with a bouncing ball spelling out
  base-two numbers while the viewers take turns squeezing plastic margarine bags." Context: Zodiac
  Associates screenplay; "more to do with semiotics than with homicide".
- Citation: gp18.jpg.

### Other statements in gp1–gp34 that bear on method
- "The only powers of numbers I believe in are squares and cubes. I am interested in the use of number as
  a medium of communication because there is voluminous evidence in the Zodiac letters that their author
  uses number to communicate (using Morse Code and base-two notation, which are interchangeable)." What
  others call "ambiguous puzzles" "is what I call nonverbal communication." (gp12)
- "I published a digital solution to the 340-character cipher in TIMES 17." (gp30) "After publishing it,
  I figured out how to use the computer as an analytical tool and now have what I think is far more
  interesting material; I am working on a second book whose working title is The third knife." (gp12)
- His source on "radian": "My father told me that the Zodiac had used the word 'radian' in an unpublished
  letter." Hugh Penn, a WWII Army cryptographer, "tried his hand at solving the three unsolved Zodiac
  ciphers — with no success." (gp7, gp10)
- Coincidence bragging: "You name a coincidence, and I can top it." (Webster Street; Dirty Harry and
  Eastwood as mayor of Carmel, "where I was born") (gp1)
- "Rhetorical lead": he defends a fictionalized dateline ("Tahiti, 23 August 1773") and says "'accurate'
  and 'true' are not necessarily the same thing." (gp5)

---

## 2. Letter to Zam, 16 Aug 2010 (Penn email posted on opordanalytical.com)

File `2010 08 16 Letter to Zam from Gareth Penn.txt`. Exhibit images in
`2010 08 16 Letter to Zam from Gareth Penn/290db05d3cdf0de722813380565776a4.jpeg` (Exhibit 1) and
`e2d5ca2c3de57b550707ece4696c67c0.jpeg` (Exhibits 2–4). All four exhibits are Zodiac texts with
non-alphanumerics removed, set in 17 columns, with column numbers 5/10/15 on top and row numbers every
5 rows on the right. Position = (row−1)·17 + column. Digits count as characters.

### M: Row-of-one-word × column-of-another = position number (victim × weapon = date)
- Category: grid/geometry
- Rules: highlight word A and draw a vertical line down the column of its first letter. Highlight word B
  and draw a horizontal line along its row. The intersection cell's position number "is" the message.
- Example (Exhibit 1, THE CONFESSION, postmarked 29 Nov 1966): BATES is in row 30, cols 10–14
  ("LLEYSMISS**BATES**WAS"). The first KNIFE is in row 61, cols 5–9 ("MALL**KNIFE**ATHERTHR"). "The column
  marked by BATES and the row marked by KNIFE intersect at position #1030 (the 1030th alphanumeric
  character of the text)." Verified: (61−1)·17 + 10 = 1030 (cell = the A after KNIFE).
- Claims: 1030 = 10/30 = 30 Oct 1966, the date Bates was killed with a knife.
- Citation: Letter to Zam, para "I am attaching four exhibits…"; Exhibit 1 image.

### M: Calendar + intersection (two consecutive Fourths of July define VALLEJO)
- Category: calendar/date; grid
- Example (Exhibit 2, letter to the SF Examiner, 1 Aug 1969): "4THOFJUL" is in row 15, cols 10–17, and the
  Y wraps to row 16 col 1. "If the Arabic 4 = the fourth of July, and if each subsequent character = one
  day, then the next fourth of July (i.e. 4TH OF JULY + 365) = the highlighted letter I in Row 37." The
  column of the "4" (col 10) and row 37 intersect in "IDEDINTHE**VALLEJO**P" at the V. Verified: "4" =
  14·17+10 = 248, 248+365 = 613 = row 37 col 1 (the I). Row 37 col 10 = V.
- Claims: "These two consecutive fourth of Julys intersect at the name of a community in which the author
  committed a murder on the fourth of July."
- Citation: Letter to Zam; Exhibit 2.

### M: The word PI intersecting itself at position 314
- Category: grid
- Example (Exhibit 3, letter to the Chronicle postmarked 26 Jul 1970, starts "THISISTHEZODIACSP…"): the
  first PI is in row 8 ("NTHINKU**PI**FYOUDONO", P at col 8). The second PI is in row 19 ("AVE**PI**NE**S**PLINTERSD").
  "PI and PI intersect at position #314." Verified: 18·17 + 8 = 314 (the S of PINES). The text has
  four PIs; he uses the first two.
- Citation: Letter to Zam; Exhibit 3.

### M: Surplus words intersecting at their own meaning (END at the end)
- Category: grid
- Example (Exhibit 4, rows 38–45 of the 31 Jul 1969 Chronicle cover letter): each of the other two cover
  letters has one END (in WEEKEND). This letter has three: WEEKEND (row 40), "UNTILLI**E**/ **ND**UP"
  (wraps from row 43 col 17 to row 44), and WEEKEND (row 45, cols 15–17). "The two surplus ENDs intersect
  at the end of the text": the column of the wrapped END (col 17) × row 45 = row 45 col 17, the final
  character [computed: position 765].
- Summary rule (quoted): "two things can define a third by intersection: victim and weapon define the
  date …, two iterations of a date define the place …, the verbal form of a number defines a position
  expressing the same number in numerical form, or two repetitions of a word denoting a thing can define
  the thing itself. These are examples of two-dimensional effects that are format-dependent."
- Citation: Letter to Zam; Exhibit 4.

### M: (row, column) coordinate read as a decimal (STUPID → 31,4 → π)
- Category: grid
- Example: "Row 31 of the first example, where we find the first instance in the Zodiac literature of PI
  (in STUPID). It is conventional to identify grid points by row and column number, in that order. In
  this manner, the position of PI is expressed as 31, 4 (π = 3.14…)." Verified: row 31 =
  "STU**PI**DSHEWENTTOTH", P at col 4.
- Citation: Letter to Zam, end of exhibits paragraph.

### M: Cipher symbol counts as "a cube plus five"
- Category: numerology
- Examples: "in both cases, the number of cipher symbols used is a cube plus five (13 = the cube of 2 + 5;
  32 = the cube of 3 + 5)". The "times-17 principle is still in effect" in #4 (17 + 15).
- Citation: Letter to Zam, Hooke paragraph.

### M: Morse as a hidden language; "two-dimensional" writing (Flatland)
- Category: Morse/binary; grid (meta)
- "the Zodiac is concealing meaning by writing in Morse Code. I have several other proofs of this to
  offer." "Another aspect … is that he writes two-dimensionally" (Abbott, *Flatland*). Analogy: reading a
  Lithuanian letter as misspelled English for forty years.
- Citation: Letter to Zam, para "I get the general impression…".

### Puzzle-relevant in this letter (see the Puzzle section)
- His own "Sunday and Wednesday puzzles and the codicil to the second". "Reginald Graham Wordsworth" was
  proposed by a solver for the Wednesday codicil. Penn: "a delightful solution … but I have no idea how
  the solver arrived at this result or who Reginald Graham Wordsworth is. In other words, I don't get
  it." He invokes Robert Hooke's anagram CEIIINOSSSTTVV and Trivial Pursuit (answer first, then guess the
  question).
- Translation wordplay: his spoof calling the poster "theforeigner" a translation of Camus' *L'étranger*,
  defended with dictionary detail (*Den fremmede*, *The outsider*).

---

## 3. "Ave atque vale", GZ4216 farewell post, 11 Jan 2011, plus image 2h7gabs.jpg

File `2011 01 11 Gareth Penn - Ave atque vale.txt`. Image `2011 01 11 Gareth Penn - Ave atque vale/2h7gabs.jpg`.

### M: The blog title GZ4216 (Hue and Cry): a meta-clue
- Category: other (allusion)
- "In 1947, Ealing Studios released … *Hue and cry*. The movie has to do with a gang of children who try
  to track down a master criminal by looking for coded clues published in comic books … the letter-
  combination GZ is not used in UK license plate numbers, and when one of the children sights a truck
  bearing the plate number GZ4216, the gang takes it as proof … Zodiac websites and the people who
  frequent them remind me of children who look for coded clues in comic books and chase after nonexistent
  license plate numbers." He is "disappointed that no one has asked why".
- Citation: Ave atque vale, para 3.

### M: n × 17 rectangles; 408 padded with 18 gibberish letters to make a perfect rectangle
- Category: grid
- "The first was formatted as a perfect rectangle having 24 rows and 17 columns; it was divided into
  thirds, each of them a perfect 8 x 17 rectangle … 390 letters of English and 18 of gibberish. If the
  author had not included the gibberish, it would have been an imperfect rectangle." #2 is 20 × 17. #4
  "has 17 symbols in the first row and 15 in the second … he chose to make it an imperfect exemplar of
  the n x 17 format."
- Citation: para 5.

### M: Position numbers of every crossed circle; the first in each cipher is a perfect square
- Category: numerology; grid
- Data (exact): "#1) 100, 239, 267, 347 / #2) 49, 73, 117, 132, 155, 205, 260, 295, 332 / #3) 4 / #4) 29".
  "In each of the first three ciphers, the position number of the first crossed circle is a perfect
  square … None of the other 12 crossed circles has this property … It seems inescapable that this
  effect is the product of design." He poses questions to readers: why two perfect n × 17 rectangles and
  then two imperfect ones? Why mark perfect squares? Why write in cipher symbols at all?
- Image 2h7gabs.jpg: all four ciphers typeset 17 wide. The first crossed circle in the 408 (row 6,
  col 15 = #100), the 340 (row 3, col 15 = #49) and the 13-character cipher (#4) is shown inverse/
  highlighted. The 32-character cipher is shown as 17 + 15.
- Citation: para 6–7 and image.

---

## 4. Appendix A of *Times 17*, retyped in Ray Grant's blog "The roots of fascism" (12 Dec 2013)

File `Appendix A from Gareth Penn's Times 17.txt`. Images in `Appendix A from Gareth Penn's Times 17/`
(T17 cover with the 17×17 number grid: 489494c8….png; Zodiac cards and letters). **Penn's own text** is
the Appendix A "WHAT WENT WRONG?" (T17 ≈ pp. 347–350; Martin says the "manifesto" is on p. 347, Grant
says FASCISM is "on page 350"). **The numerology applied to it is Ray Grant's**, not Penn's.

### M (Penn, T17): 17×17 magic square with line sums 9745 (cover art)
- Category: numerology; grid
- Grant: the chapter before Appendix A, "Times 17", "has mostly to do with Gareth Penn constructing a
  magic square, 17 by 17, where the numbers in each column and row add up to 9745. Gareth clearly thought
  enough of this exercise that he put the result on the cover of his book." [note: 9745 is not divisible
  by 17, so it is not the normal 1..289 square, whose constant is 2465.]
- Citation: Grant blog, para 7; cover image 489494c8b86e810b65e599a818afde86.png.

### M (Penn, T17): TIMES 17 = 9745 = O'Hare's age in days at Berryessa (17 stab wounds)
- Category: Morse/binary
- "T I M E S 17 / 1 00 11 0 000 10001 = 9745 (digital Morse/binary math)". O'Hare DOB 1-22-43, attack
  27 Sep 1969. Verified.
- Citation: Grant blog, para "How likely is it…".

### M (Penn, Appendix A): anniversary "hooks" and date arithmetic in press coverage
- Category: calendar/date (reasoning, not decoding)
- Penn attacks Konte's Chronicle story (*This World*, 21 Dec 1986): "Eighteen years ago yesterday [20
  December 1986], the Zodiac killer murdered his first victim." The Riverside murder (30 Oct 1966) had
  been the first since Avery's 16–17 Nov 1970 series. "One Sunday in December, the 21st, happened to
  follow the eighteenth anniversary of the Lake Herman Road murders by twenty-four hours. Editors like to
  have a 'hook' … anniversaries are very good hooks."
- Also coined: **ZIK** = "Zodiac Identification Kit, a mailing whose contents identified Michael O'Hare",
  verb "to zick". Final line: "I went looking for the Zodiac, but what I found was the roots of fascism."
- Citation: Grant blog, Appendix A text.

### M (Ray Grant, third-party): Morse/binary number, then prime factorization ("roots")
- Category: Morse/binary; numerology
- Grant: FASCISM = 0010 01 000 1010 00 000 11 = 148,739 = 2521 × 59. PUMPKIN = 408,402 = 2521 × 162.
  DRAGON = 35,294 = 14 × 2521. 2521 = 100111011001₂ = 10011 | 1011001 = 19 | 89. All verified.
  Grant's claim: "the roots of fascism" (Penn's last words) tells the reader to factor Morse numbers, so
  PUMPKIN ≡ DRAGON (Dragon Plaza near 739 Clay St; Donna Lass buried at Portsmouth Square). Grant's other
  devices: 17 Bay Area mailings; the LA Times letter has 17 words after TIMES ("Times 17"); the Lake Tahoe
  card's punched hole is at x = 97 mm, y = 45 mm → 9745. T17's original price was $17.
- Citation: Grant blog, second half.

---

## 5. Laube, "Cryptograms and mountain keys to author's hypothesis", Vallejo Times-Herald, ~1 Nov 1981

Image `1981 11 01 Cryptograms and mountain key to author's hypothesis (George Oakes  Gareth Penn)/e5f7b846….jpeg`.
Penn appears as "George Oakes (a pen name)", age 41, "a former librarian in Vallejo".

### M: "Binary Morse" with interchangeable polarity
- Category: Morse/binary
- "'One of the Zodiac's most ingenious devices is a code I call "binary Morse,"' says Oakes. 'It has only
  two types of characters, dots and dashes. Zodiac used it from time to time in conjunction with binary
  numbers, substituting dashes for ones, dots for zeros, **and vice versa**.' 'Numbers can become words,
  and words can be transformed into numbers under this system.'" Note that both polarities are allowed.
- Citation: Laube 1981, col. 4.

### M: Radian angles on Mt. Diablo matching murder sites
- Category: map/geography
- "The Zodiac had hinted that if a radian angle were placed on Mount Diablo, it would provide insight
  into the 'rhymes and reason' behind his trail … by measuring different angles derived from complex
  mathematical formulas, he noticed patterns emerging that lined up with the locations of the Bay Area
  murders … the Zodiac, by charting his murder sites, had set a deliberate pattern." Starting point: the
  map the Zodiac included in a Chronicle letter.
- Citation: Laube 1981, cols. 2–3.

### M: Misspellings as deliberate syntax concealment (form over content)
- Category: typography/word-play
- "'I think the obvious inconsistencies in his letters and spelling words two or three times differently
  were by design to conceal the syntax. It's in code.'" "'Discussion of the Zodiac literature has always
  been limited to the literal meaning of the English words … no serious study has ever been devoted to
  the form in which those words are expressed.'"
- Citation: Laube 1981, cols. 4–5.

### Other
- Start date: "Ten months after he began on Dec. 26, 1980". The postscript of his California article
  wonders whether the Zodiac set the Atlas Peak fire (June 22 [1981]), given the vow to kill by "gun,
  knife, fire and rope": "it could be Mr. X just reminding us he's still around." "Fearing for his life,
  Oakes wrote the article under a pen name."

---

## 6. FBI files 1981–1985 (rendered at 150 dpi in scratchpad `fbi/`)

### 6a. Airtel SF → Director, 29 May 1981 (FBIZodiac6 pp. 74–78), "ZODIAC KILLER; EXTORTION"
Methods described:
- A 21-page article proposed to *New West* under a pen name, with supporting documents. Penn later made
  "annotations … and revised them concerning the deciphering of the Zodiac killer's code" (Set #2,
  mailed 27 May 1981).
- Harassment mail as a reaction test: interviewed 22 May 1981, Penn "freely admitted sending material to
  [O'Hare] … His motive was to elicit some response from [O'Hare] if [O'Hare] was, in fact, the Zodiac …
  Some of the material he sent to [O'Hare] was in the Zodiac's own code system as he has deciphered it."
- Premise: Zodiac is "very well educated but diabolical … taunting law enforcement by revealing his
  identity in codes and symbols." Uses media plus non-public information. One element (redacted) is
  "derived from an illustration" (illustration and analysis attached). Penn separates repeated,
  consistent "solutions" from "tentative … combination of analysis and an 'educated guess'", and agreed
  to mark which parts are "solid".
- Supporters: a Napa psychiatrist, professors at USF and UT Austin; a UNM professor "'dazzled, but could
  not vouch for it'"; UCLA (redacted). New West's cryptanalyst "not convinced". Two private cryptanalysts
  "not convinced".
- CII (Cal DOJ) factual errors in the draft: Bates's time of death "about 6:15 p.m." (CII "not aware of
  the time indicated on the Timex watch found at the scene"); Shepard and Hartnell "not stabbed with
  [redacted] but some other kind of knife"; Stine "shot behind the ear"; "discrepancies in the number of
  times victims were shot". SF agents: "may have some merit although he appears, in some instances, to
  be fitting his solutions to the facts".
- Citation: 1981 05 29 FBI documents, pp. 2–5.

### 6b. FBI Laboratory report, 26 June 1981 (FBIZodiac6 pp. 83–86), "Cryptanalysis"
- Specimens: cover letter of 14 May 1981 from New West with the article and enclosure; cover letter of
  [16?] May 1981 enclosing "a revision of Zodiac analysis".
- Result (read from a degraded scan): "the 'solution' advanced by Mr. [Penn] does not lend itself to
  cryptanalytic validation in the same sense as traditional cryptographic systems. There are elements of
  his theory which include standard cryptographic techniques such as the **'Wizard' and 'Binary Morse'
  substitutions**. The bulk of the theory, however, is based on speculation and a multitude of
  assumptions … Many, if not most, appear to be forced with results being used selectively if they are in
  keeping with the overall theme of the solution. For example, the [Penn] decryption of the
  [13?]-character cipher is based upon a series of assumptions and ultimately does not represent a unique
  solution, but one that generally agrees with the thrust of the solution. (To Mr. [Penn]'s credit, he
  points out that he is making assumptions and gives his basis …) … It is still possible that the
  340-character cipher will yield a unique solution by cryptanalysis."
- So by May 1981 the method set already had the WIZARD (reverse-alphabet) substitution, binary Morse,
  and a decryption of the 13-character cipher.
- Citation: 1981 06 21 FBI documents pp. 84–85.

### 6c. Airtel SF → Director, 14 July 1981 (FBIZodiac5 pp. 44–48)
- Four more Penn letters with analyses: (1) "analysis of an article from the pen of [redacted]"
  [inferred: an O'Hare text, as in gp26]; (2) "**analysis of calendar regarding Zodiac murders**, dated
  6/24/81"; (3) "**analysis related to Zodiac's telephone number, i.e. telephone number of [redacted]**,
  dated 6/30/81"; (4) analysis titled [redacted]. Also a "detailed analysis to support his previously
  expose of his theories". On 8 July 1981 Penn was told the Lab was not convinced. He admitted sending
  "one more card" to O'Hare and promised to stop. 25 pages withheld.
- Methods named: calendar analysis; telephone-number decoding (both still undocumented in our sources).

### 6d. Handwritten letter to Boston FBI, "4/2?/[8]2" (FBIZodiac5 pp. 37–40; notebook title says 1972)
- Writer redacted. Encloses "the latest materials from [Penn] re the Zodiac-[O'Hare] scenario (2
  mailings)" and asks the FBI to have "the [Penn] binary theory, handwriting etc." checked. Plans: have
  the Middlesex DA's office check [O'Hare's] whereabouts during the Zodiac killings; have Harvard Police
  check airline manifests to see if [O'Hare] "can be placed on [Joan Webster's] flight from Newark to
  Logan (he could have used an alias)". [inferred: the date is 1982, not 1972, because Webster vanished
  after the 28 Nov 1981 Newark→Logan flight; the envelope postmark appears to read '82.]

### 6e. FBI Lab report, 24 Jan 1983, on Boston communication of 4 May 1982 (FBIZodiac2 p. 14)
- K1 = "two sets of photocopies of one hundred and nineteen pages of material relating to [O'Hare/Webster]
  and the ZODIAC". Result: "Most of [Penn's] theories are based on conjecture and numerous assumptions.
  Some assumptions are possibly correct. However, [Penn] selectively dissects the literature (often
  misquoting material) and presents results only if they corroborate the overall theme of his solution.
  Thus, on a cryptanalytic, mathematical, and technical basis, the Laboratory contends that the results
  are forced and inconsistent. Unless investigative techniques validate the hypotheses … no further
  [Penn] communications will be analyzed."

### 6f. FBI Lab, 28 May 1982 (FBIZodiac6 pp. 93–94)
- Same K1 (119 pp.). The handwriting [samples] in K1 "are not sufficiently [adequate?] to permit
  meaningful comparisons with the questioned writing in the Zodiac case". Cryptanalysis results to follow
  separately. (Penn's 119-page packet included handwriting comparisons.)

### 6g. Airtel, 11 Dec 1985 (FBIZodiac6 pp. 173–174)
- Penn sent a letter plus two enclosures to the FBIHQ Special Inquiry Unit and "a similar package" to the
  FBI Academy (Behavioral Science Unit). It refers to the Webster homicide and suggests Harvard University
  police "may have some interest" in O'Hare. The FBI restates the 1981 Lab view ("bulk of his theory is
  based upon speculation and a multitude of assumptions … forced … used selectively").

### 6h. Letters of 26 Nov, 23 Dec and 30 Dec 1983 from Albion, CA (FBIZodiac6 pp. 89–92). **Probably not Penn**
- The writer's name is redacted. The return address is Albion, CA 95410. The content is astrology and
  occult: "RIVERton, of course, reminds of RIVERside" (Green River Killer); moon phases ("dark of the
  moon"); signs; sabbats (Beltane, winter solstice); "numerological significance of the number four to
  Zodiac"; the Berryessa hood copied from Aleister Crowley; the Rosicrucian cross vs the crossed circle.
  The style and themes don't match Penn's. Listed only because the notebook files them under his name.

---

## 7. Michael J. Martin, "With Malice Aforethought" (Weekly Scientist blog, Oct 2009; parts 1–8)

File `2009 10 06 With Malice Aforethought (Gareth Penn vs Michael O'Hare).txt`, images in the same-named
folder (notably `050574895713b7e83e0c5d571beba9da.jpeg` = Penn's mailings to O'Hare, as reproduced in
O'Hare's 2009 Washington Monthly piece).

### M: Binary Morse code, "a mathematical medium he invented"
- "he was insisting that 'binary Morse code' — a mathematical medium he invented to decipher the Zodiac —
  had revealed the killer's identity." (part 2)

### M: Misspellings as mathematical code (PHOMPHIT, CID)
- D'Angelo's summary of Penn: "various odd misspellings in Zodiac letters — 'phomphit' in lieu of 'puff
  it'; 'cid' instead of 'kid' — were part of an elaborate mathematical code" that "revealed the name of a
  real person — Michael O'Hare." (part 2)

### M: Radian Theory (Mt. Diablo)
- "O'Hare the architect had targeted his victims according to a Da Vinci-esque geometric design centered
  on … Mt. Diablo." It answers "PS. The Mt. Diablo code concerns Radians & # inches along the radians."
  Penn on the word itself: "Radian is something you find in the vocabulary of someone trained as an
  engineer—or an architect." (parts 2, 8; image a1f5a634… shows red radian lines from a vertex on the
  map, next to the T17 cover.)

### M: "Private language" / "Book of Secrets" (The Second Power)
- Penn claims O'Hare "had invented his own 'private language'" across the ciphers, letters and phone calls
  to write a "Book of Secrets" about sexual abuse. "'Decoded' by Penn, words like penis, balls, erect,
  jizz, creaming, semen, prick, cock, pecker, vagina, womb, hole, hard on, pussy, snatch, and incest
  emerge." [inferred: probably found by digital redivision, as in gp24–gp27; the method is not stated
  here.] (part 2)

### M: Biographical allusion to O'Hare's grandmother (Kate Richards O'Hare)
- Penn: "Several things the Zodiac killer did echoed the life of his grandmother … Death in Benicia,
  claiming to be an escaped convict, referencing the color red — the color of her hair — in several of
  his letters. It was an oblique way for Mike O'Hare to identify himself." (part 3)

### M: Reaction-test mailings ("psychological war", Jan–May 1981)
- T17 quoted: O'Hare "received a number of what you might call weird postcards … sent anonymously from a
  number of locations. I expressed in these postcards what I felt were allusions to Zodiac formulations
  that the Zodiac and nobody else would recognize. If O'Hare were not the Zodiac, he would be baffled."
  (part 2)
- Image 050574895713….jpeg shows later mailings to "Michael O'Hare, Goldman School of Public P[olicy],
  2607 Hearst …". They include: a typed letter grid ("ENCOURAGEMENTEXPERIENCEANDANINTOLERANC…",
  "…ARCHITECTURE…") with highlighted words crossing each other (e.g. "SOFT" twice) and row numbers 60/65,
  captioned "**TO RENT** / Here's my translation into USA English of Galsworthy. **G.**" [wordplay:
  Galsworthy's *To Let* → American "To Rent"]; a letter grid with a straight line drawn between two cells
  (row label 125); small grids with column labels 5/10/15 and a highlighted run, captioned
  "**eighteen!**"; sheets of binary digits with marked points joined by a line; a Sierra Club calendar;
  an envelope from PRBO (Point Reyes Bird Observatory, Stinson Beach) stamped "first class CONFIDENTIAL";
  a clipping "The Eisenhower Era was … round from…". Resolution is too low to read the grids. (These
  look like the "three or four letters a year" O'Hare says he files unopened.)

### M: Symbolic parallel (surveyor's flower garden)
- Penn's anecdote: O'Hare "sited every plant with a surveyor's transit". He pairs it with his own Kafka
  *Castle* story (artillery surveyor ordered to lay out a flower garden). (parts 4, 5)

### Other method-adjacent items
- Screenplay title "12:22", "the presumptive time of Cheri Jo Bates' murder" (Zodiac Associates, Inc.)
  (part 4).
- Copyright "Papers relating to the impending suicide of Michael Henry O'Hare", TXu000354164. Martin's
  blog wording makes "17 May 1989" read like the registration date. His later list (§8) shows "on 17 May
  1989" is part of the title (a prediction) and the registration date was 15 Dec 1988.
- Timing quip: O'Hare's 2009 article came "around the same time as the latest from Osama bin Laden …
  there's something in the air." (part 8)
- Penn on the Zodiac's tool kit (California magazine 1981): Zodiac as conceptual artist using "time and
  human life" as materials.

### Martin's (and others') arguments about Penn's own wordplay or Zodiac echoes (third-party)
- Penn's "I have tons more of this stuff and would love to rub your nose in it" echoes the Zodiac's
  "rubbing their noses in their booboos". (part 4)
- Alan Cabal (1983 meeting): "a bizarre head game … all ambiguity and coded references"; Penn's account of
  his epiphany is "patently false". (part 5)
- Mary Ann Winterrowd (Penn's wife) taught *The Most Dangerous Game*. (part 8)
- Farmer: radian theory, binary math and Mensa articles as "hyper-intellectual narrative" by which Penn
  is "calling attention to his own crimes". (part 7)
- Penn's 1970 *New Republic* letter on "Revolution as Theatre"; his 1972 paper "Gottfried von Strassburg
  and the Invisible Art", on the medieval "memory theatre" mnemonic that uses architectural landmarks as
  memory aids. That is a spatial encoding idea, comparable to his grid/landmark readings. (part 4)

---

## 8. Mike Martin emails, timeline, and Strange de Jim material

Files `Mike Martin's email with details implicating Gareth Penn as Zodiac.txt`, `Mike Martin's Gareth Penn
timeline.txt` (+ Resp2–4.jpg = pages 3–4 of the 1983/84 divorce trial brief, residence history only),
`Strange de Jim and Gareth Penn (email from Mike Martin).txt`, `1976 09 …`, `1976 11 …`.

### M (Penn, Ecphorizer "Lima Riki"): limericks in Old Norse; near-rhyme as a deliberate device
- Penn "used to write limericks 'in Old Norse'". "While some purists insist on pure rhyme, a contrived or
  near rhyme, especially in the pointe, heightens the humorous effect, a technique well known to fans of
  Ogden Nash, Sir William S. Gilbert, and the shaggy-dog story." The title "Lima Riki" is itself a
  pseudo-Norse respelling of "limerick" [observation].
- Citation: Martin email, "Language skills" and "Interest in … Mikado".

### M (Martin's argument): the "Dripping Pen" card as a pun on PENN
- Penn's 1976 letter: "PS. Please spell my name right. I stopped contributing to Caen when he left out a
  letter once." Martin pairs this with the Zodiac card "Sorry I haven't written, but I just washed my pen"
  and "Tell herb caen I am here". "The missing letter 'n' jives with the reason Penn said he stopped
  writing to Caen." (Strange de Jim email, 1/6/16)

### M (Penn, 1976 letter to *San Francisco* magazine): stylistic wordplay
- "I am not now, nor have I ever been, Strange de Jim" (HUAC formula). "while I have from time to time
  been as Strange or even Stranger, I have never been as Often. In any case, I am not such a shameless
  anonymity-hound as he is." Signed "Gareth S. Penn, **San Francisco**" (Sept 1976 issue, p. 10, image
  rendered from `Strange de Jim copy.pdf`). Strange de Jim's reply (Nov 1976) plays on zodiac signs: "the
  world's first sign change operation (I was born a Cancer, but I've always known I am really a Leo)",
  signed "His Abandonment".

### Copyright registrations (Martin's list; these are Copyright Office TXu numbers, not trademarks)
Several titles are dated predictions registered in advance, which works the same way as a sealed
priority anagram:
- TXu-126-336 "A Secret kept from all the rest", 16 May 1983
- TXu-176-361 "Zodiac problems", 29 Oct 1984
- TXu-234-140 "The Red king's dream", 31 Mar 1986
- TXu-238-116 "New documents", 7 May 1986; TXu-240-019 "Three more documents", 23 May 1986
- TXu-254-364 "The 13-character cipher", 22 Sep 1986
- TXu-354-164 "Papers relating to the impending suicide of Michael Henry O'Hare on 17 May 1989",
  registered 15 Dec 1988
- TXu-383-923 "The Geometry of life and death", 5 Sep 1989 (application title: "Resolution of the Zodiac
  mystery on 19 September 1989")
- TXu-385-039 "Language as geometry", 10 Aug 1989
- TXu-406-808 "Zodiac calendars", 13 Feb 1990 (application title: "Papers relating to the resolution of
  the zodiac matter on or about 19 February 1990"; "Special Codes: 1/B/D//A")
- TXu-430-480 "**8790**", 1 Aug 1990
- TXu-927-707 "The second power: a mathematical analysis of the letters attributed to the Zodiac
  murderer", 13 Dec 1999
- TXu-937-814 "**The end: a prediction of the future in six pages**", 22 Feb 2000
- TXu-1-044-778 "Digital, two-dimensional, private language: The letters of the zodiac murderer", 18 Mar 2002
- [extractor's computation, not Penn's claim: O'Hare's age in days on 17 May 1989 = 16,917; on 19 Sep
  1989 = 17,042; on 19 Feb 1990 = 17,195.]

---

## 9. "Domebuilder's Blues" by George Oakes (Shelter Publications; the editor says it was sent in 1981)

File `1979 - 1982 (approx) - Domebuilder Blues by George Oakes (Gareth Penn).txt`.
- **Pseudonym**: George Oakes. Penn says it was "a name that I borrowed from a novel by Gerald Kersh",
  first used for a sea-level-rise piece and kept because it sold (GZ4216 gp6). Laube says he used it out of
  fear for his life. Its Morse bit string is not a redivision of GARETH (S) PENN (checked).
- No cipher or puzzle content found. Paragraph initials (BTATTSGITTDAD…) are not an acrostic. Wordplay
  and noteworthy items:
  - Word dissection: "Iso-cyan-urate. Look at the middle part of the word. When it burns, it gives off
    cyanide gas." (reading a hidden word inside a word)
  - Acronym coinage: "I'm just going to abbreviate 'It Goes Without Saying.' IGWS".
  - Anonymization by letter: "Company X" (6×).
  - **The only proper-name "O'Hare"**: "the cyanide that killed Mrs. Hunt in that crash at O'Hare right
    after the Watergate break-in". [observation: United 553 (Dorothy Hunt, Dec 1972) crashed approaching
    Chicago **Midway**, not O'Hare. So this is either an error or a planted O'HARE, in a piece sent in
    1981, the year of his O'Hare campaign.]
  - Numbers stated: 60 panels, 22-ft dome, 39-ft kit, 147-degree joints, R-19/R-38, 1500 vs 3000 ft of
    tape, "My 9-year-old boy" (Felix, b. 1971 → written ~1980), Green Valley Road (Napa).

---

## 10. Short letters (letters to editors, Economist, NPR, Time, Nature, Sci Am)

No ciphers in any of them. The wordplay and devices are noted below.
- **1968-08-26, SF Chronicle "The 'It'"** (penn1.png), signed Gareth S. Penn & Mary Ann Penn, Berkeley.
  Exegesis contrasting the Douay and King James wording of Ephesians 5:3 ("let it not be named among
  you"), then turning James 3:6 ("the tongue is a fire") on the opponent. Device: comparing translations
  and quoting against the quoter. (The 1968 08 16-31 PDF is the same letters column. Its note says it
  contains one Penn letter.)
- **1994-07-11, Time**: "Sullivan wrote the words, and Gilbert wrote the music. Holmes is the doctor, and
  Watson the detective. Harpo had the cigar, and Groucho tooted the auto horn." Device: deadpan
  pair-swapping (transposition joke) about *The Mikado*.
- **1995-01-19, Nature 373:185, "Penn's law"** (PDF): reports the editors to "the SPCFA (Society for the
  Prevention of Cruelty to Figurative Animals)" for misusing Sherlock Holmes's dog that did not bark
  (*Silver Blaze*). He proposes "a natural law according to which almost all rhetorical references to
  works of literature are made by people who have never read the works to which they refer". Address:
  13½ Linda Avenue, San Rafael, CA 94903.
- **1996-07, Scientific American p. 8, "Bright Lights, Big City"**: corrects the claim that Jules Verne
  "could not imagine a city with more than a million inhabitants" (London had over 2 million by 1850;
  greater NYC over 3 million in 1900). San Rafael.
- **1997-07-23 email** (journal-quality list; Pullum's criteria). Signature quote from Michael Flanders:
  "But people have always eaten people! What else is there to eat? If the Juju had meant us not to eat
  people, he wouldn't have made them of meat!" Address: NMFS Tiburon Laboratory, 3150 Paradise Drive,
  Tiburon CA 94920.
- **1997-11-23, SF Chronicle** ("skibby"): Latin *scibile*, Lewis & Short, Tertullian, Martianus Capella.
  Church-Latin pronunciation would give "shibby". Joke: "the fabulous motto of the Boston Latin School
  cafeteria, 'he knows the faith,' i.e. '**fidem scit**'". [observation: a macaronic sound-pun. In Church
  Latin it sounds like "feed 'em shit".] Corte Madera.
- **1997-12-07, SF Examiner Magazine "Mores Frogs and Peaches"**: Cook & Moore's "Good Evening"; menu of
  "frog stuffed with peach and peach stuffed with frog"; "I suspect that the Gallicization 'Frog a la
  Peche' is Klein's original contribution." Device: mock-French translation pun. Tiburon.
- **1999-01-09, Economist** (barbed wire; tumbleweed from Russia), Larkspur. **1999-08-21** (hippie with a
  Mercedes logo, "class loyalty is dubious"), Stinson Beach. **1999-10-16** (Sphinx's riddle): "Those who
  answer this riddle correctly not only destroy monsters; they go on to marry their own mothers … and then
  gouge out their own eyes. Too bad for you that you answered it correctly." The riddle-solver/incest
  theme parallels his *Second Power* allegation. Tiburon.
- **2000-01-29** (Wyoming suffrage 1869; New Zealand "waited 24 years"), Stinson Beach. **2000-08-26**
  (WASP predates Baltzell 1964 per OED). **2000-12-16** ("elector": OED 1467 vs *Kurfürst* 1529, "some 61
  years later"; "choose-prince"). Larkspur/Tiburon. Device throughout: OED-date arithmetic and
  pedantic correction.
- **2002-07-20, NPR**: in New York for both blackouts (1965, 1977): "nobility does not sell newspapers."

---

## Puzzle-relevant remarks

- **Hooke-style priority anagram as the model for his own puzzles** (Letter to Zam, 2010): "Before anybody
  expends any more effort on these paltry little puzzles of mine, I would like to invoke the spirit of
  Robert Hooke, who proposed … a law of elasticity, which he published as an anagram: CEIIINOSSSTTVV.
  The only person who can testify as to the content of an anagram is the one who made it. Hooke intended
  to establish a claim to the principle by publishing it but to withhold the solution until a time that
  suited him. The Sunday and Wednesday puzzles (plus codicil) have the same purpose; I believe that they
  are completely unsolvable without knowing the context in which they are set." Then Trivial Pursuit:
  "read the answer and try to guess the question … It is impossible to come up with the right question
  without a context."
  - Implication: the puzzles encode claims or predictions he wants to prove later. The plaintext is a
    statement whose truth he expects to be confirmed. The solver needs his context (his theory and his
    keys).
  - A solver's proposal for the Wednesday codicil was "Reginald Graham Wordsworth". Penn called it
    "delightful" but said "I don't get it", which implies it is wrong.
- **Sealed, dated predictions** registered with the Copyright Office are the same priority device:
  "Papers relating to the impending suicide of Michael Henry O'Hare on 17 May 1989" (reg. 15 Dec 1988);
  "Resolution of the Zodiac mystery on 19 September 1989"; "… resolution of the zodiac matter on or about
  19 February 1990"; "The end: a prediction of the future in six pages" (22 Feb 2000); "8790" (1 Aug
  1990). *The Third Knife* is to "finally tell all" on his death (Martin).
- **How he builds hidden messages himself**: the pseudonym MIKE REVNEC is an exact Morse redivision of
  GARETH PENN (gp19). Mailings to O'Hare were "in the Zodiac's own code system as he has deciphered it"
  (FBI 1981) and carried "allusions … that the Zodiac and nobody else would recognize" (T17 via Martin).
  The mailings shown in 2009 include grids with intersecting highlighted words, row/column labels, a line
  between two grid points, binary-digit sheets, "eighteen!", and a translation pun signed "G." (To Let →
  To Rent).
- **Toolkit he treats as legitimate** (so likely in his own puzzles):
  - International Morse with dah=1, dit=0 ("interchangeable" with base two). Polarity may be flipped
    ("and vice versa", Laube 1981).
  - Numerals written in binary inside a Morse string (BLUE = BASE·10).
  - Redivisions may cut letters at the ends.
  - Binary-point readings (JULY = 57.29…).
  - Fractions to binary (13/17 → MHO).
  - Calendar counting, one character = one day, from an anchor letter (B of BIRTHDAY = 22 Jan; O of
    OCT 5 = 5 Oct; "4" of 4TH OF JULY).
  - 17-column layout. Position = (row−1)·17 + col, digits count one each. Row × column intersections.
    (row, col) read as a decimal (31,4 = π). Distances that are multiples of 17.
  - Squares and cubes ("the only powers of numbers I believe in"); "cube plus five".
  - Proportions (π = 390:18; thirds).
  - Stamp denominations, brands and ZIP codes as numbers.
  - WIZARD substitution (FBI 1981).
- **His definition of a good hidden message**: it is "nonverbal" and "format-dependent", and works
  "two-dimensionally" (Flatland). "Ambiguous puzzles" = "nonverbal communication". Contrived coincidences
  ("light the fuse and let the calendar do his talking"). Literal surface text should carry a matching
  echo (the car-keys sentence ↔ Berryessa). "Two things can define a third by intersection."
- **Favourite numbers/keys in these sources**: 17; 9745 (TIMES 17; O'Hare's age in days at Berryessa;
  9/7/45); 22 Jan 1943 (O'Hare DOB); 16 Oct (Eugene O'Hare's birthday); 66/1966; 1/3 and 2/3; 198 (GUN =
  22 × 9); 193/579 (EIGHT); 1072 (DEATH) / 100, 49, 4; 57.29 / 5729 / JULY 23; 314 / 3/14; 1030; 136 =
  8×17, 119 = 7×17, 408 = 24×17; 13 = 2³+5, 32 = 3³+5; 13/17; 4216 (GZ4216); 12:22; 8790; 17 May 1989;
  19 Sep 1989; 19 Feb 1990. Words: KNIFE, FOUR, FATHER, BIRTHDAY, PI, END, BUS, GUN, BLUE/BASE 2, MHO,
  MIKE, DEATH, EIGHT, TIMES 17.
- **Other self-made challenges** posed to readers (Ave atque vale): explain why two perfect n × 17
  rectangles are followed by two imperfect ones, why the first crossed circles fall on perfect squares,
  and why the author wrote in cipher symbols at all. The blog title GZ4216 (from *Hue and Cry*, a fake
  licence-plate clue) is a riddle he complained nobody asked about.
- **Translation and sound puns** he enjoys: To Let → To Rent; "theforeigner" = *L'étranger*; *fidem scit*;
  "Frog a la Peche"; "Lima Riki"; near rhymes "in the pointe" as a deliberate device; "Iso-cyan-urate";
  IGWS; "as Strange or even Stranger … never been as Often".
- **Not found in these sources**: no mention of "lottery", "insurance" or "haiku".

## Bibliography leads (Penn writings mentioned in these sources)

- "Portrait of the Artist as a Mass Murderer", *California* magazine (ex-*New West*), Nov 1981, as George
  Oakes. The 21-page draft went to New West and the FBI in May 1981. "Three articles … published in New
  West under a pseudonym (George Oakes)", the first a sea-level-rise real-estate piece (gp6).
- "Domebuilder's Blues", George Oakes, Shelter Publications (sent 1981).
- *Times 17: The Amazing Story of the Zodiac Murders in California and Massachusetts, 1966-1981* (1987;
  $17). It includes the chapter "Times 17" (17×17 magic square), Appendix A "What Went Wrong?" (pp. ~347–350),
  a "digital solution to the 340-character cipher", and the Fort Sill/March AFB scenario.
- *The Second Power: A Mathematical Analysis of the Letters Attributed to the Zodiac Murderer* (1990;
  "supplement to TIMES 17"; reg. TXu-927-707 1999). It includes the chapter "Aftermath".
- *The Third Knife* (manuscript in progress 2009–2010; "finally tell all").
- Mensa *Ecphorizer* series 1983–84, including the Grant Mahony story (May 1982), "The savage breast"
  (Feb 1983), "Where Were You?" (People's Park/Pessis), "Lima Riki" (Old Norse limericks). *Mensa
  Bulletin* article (generated "hundreds of letters", Appendix A; per file names "The Calculus of Evil",
  Jul/Aug 1985).
- Contributions to Tom Burnam, *More Misinformation* (1980) (Edda, Snorri Sturluson).
- "The Constellation of Characters in the 'Tristan' of Gottfried von Strassburg", *Monatshefte* (1972,
  with/through F. Tubach). "Gottfried von Strassburg and the Invisible Art", *Colloquia Germanica* (~1972;
  memory theatre).
- Letter on "Revolution as Theatre", *New Republic*, 25 Apr 1970.
- *In vivo veritas* (unpublished 1970s book on biologist Ted Walker; Little, Brown interest).
- Screenplay "12:22" (Zodiac Associates, Inc., optioned ~1986–87).
- 7-page letter to *Washington Monthly* (2009) answering O'Hare's "Confessions of a Non-Serial Killer".
- GZ4216 blog (gz4216.blogspot.com), ~July 2010 – 11 Jan 2011, 50-question Q&A. "Sunday and Wednesday
  puzzles" plus codicil (2010).
- A "serious academic paper about cryptography … presented at a conference during the 1990s" (Martin;
  unverified).
- 1981 analyses sent to the FBI: calendar of the Zodiac murders (24 Jun 1981); Zodiac/O'Hare telephone
  number (30 Jun 1981); analysis of an article "from the pen of [O'Hare?]"; 119-page packet (May 1982);
  1985 package to the FBI Special Inquiry Unit and Academy.
- Copyright registrations listed in §8.
- Letters: SF Chronicle 26 Aug 1968 and 23 Nov 1997; *San Francisco* mag Sept 1976; Time 11 Jul 1994;
  Nature 19 Jan 1995; Sci Am Jul 1996; SF Examiner Mag 7 Dec 1997; Economist 9 Jan, 21 Aug, 16 Oct 1999,
  29 Jan, 26 Aug, 16 Dec 2000; NPR 20 Jul 2002 ("at least 15 letters" to NPR per Martin); contributions to
  Herb Caen's column (pre-1976).

## Biographical facts about Michael O'Hare / targets (likely key ingredients)

- **Michael Henry O'Hare**. Born 22 Jan 1943 (Grant "DOB 1-22-43"; Penn "the author's birthday (22
  January)"). Only child; raised in New York City; Bronx High School of Science, class of 1960. Harvard-
  educated architect, doctoral dissertation 1973, a journal article 1969. Worked for Arthur D. Little (SF
  branch) "sometime in 1969"; Penn says 1969–1970, on a vacation-home project "depicted on a Zodiac
  postcard". Later MIT, then the Harvard JFK School of Government, then Berkeley's Goldman School of
  Public Policy (2607 Hearst, Berkeley CA 94720 on the 2009 envelope). Home 2962 Russell Street,
  Berkeley (near the Claremont Hotel). Property in Vermont. Penn claims Harvard Rifle Team membership.
  1994 paper "Reflections on trust and confidence" (Goldman School website). May/June 2009 *Washington
  Monthly* "Confessions of a Non–Serial Killer". Age in days on 27 Sep 1969 = 9745.
- **Eugene O'Hare** (father): birthday 16 October (Penn, gp26). DIY woodworking author. Married Berta in
  1938, died 1961. Author of the 1961 Vin Fiz/Calbraith Perry Rodgers anniversary text Penn analyses.
- **Berta Margoulies O'Hare** (mother): sculptor, Polish-Jewish émigré via Belgium/Holland/England,
  Guggenheim Fellow in Berkeley 1946, died 1996 at Walnut Creek. Penn: her "38th birthday" = 9745
  [inferred 7 Sep 1907, i.e. 9/7/45].
- **Kate Richards O'Hare** ("Red Kate", grandmother): red hair; imprisoned under the 1917 Espionage Act,
  sentence commuted by Wilson and pardoned by Coolidge; later Kate Richards Cunningham, worked in
  California penology; died 1948 in Benicia. **Frank P. O'Hare** (grandfather, St. Louis).
- **Victims/dates Penn keys on**: Cheri Jo Bates, 30 Oct 1966 (10/30; THE CONFESSION postmarked 29 Nov
  1966; 30 Apr 1967 triple mailing; Penn's "12:22" time); Lake Herman Rd 20 Dec 1968 (Hebrew year 5729);
  Blue Rock Springs 4 Jul 1969; Berryessa 27 Sep 1969 (9/27 = 1/3; 17 stab wounds; car keys and pistol);
  Stine 11 Oct 1969; Hole Card 5–6 Oct 1970; LA Times letter (Pleasanton 94566) Mar 1971; Joan Webster
  ~28 Nov 1981 (Newark→Logan flight; suitcase in a Greyhound locker; purse in a marsh; father George
  Webster, CIA administrator; mother Eleanor).
- **Penn himself** (in case his own data appear in his puzzles): Gareth Sewell Penn, born ~1940/41 in
  Carmel, CA (age 41 in Nov 1981). Father Hugh Scott Penn (WWII Army Air Corps cryptographer, later Cal
  DOJ/CHP statistician, retired 1976). Mother Jean Sewell (Standish), poet. Stepfather Miles Archibald
  Standish. Addresses: 1710 Kingsbury Road, Lawton OK (1966); 2804 Webster St, Berkeley (fall 1968 – summer 1969,
  gp28); 1708 Lincoln St, Berkeley ("for three and a half years", with 1970–71 W-2s addressed there, gp1;
  Martin's timeline instead has them in Vallejo from Aug 1969, which is disputed); Vallejo, including 701 Capitol St (Jan–May 1973); Berry Lane, Napa;
  dome on Green Valley Road, Napa (1979–83); 13½ Linda Ave, San Rafael 94903 (1995); later Tiburon,
  Larkspur, Stinson Beach, Corte Madera, Seattle (2008). Army: Fort Dix BCT (Expert badge, 60 of 84),
  artillery surveyor at Fort Sill (1965–67). Wives: Sandra Scott; Mary Ann Winterrowd (m. 23 Dec 1966);
  Diane Merrill. Children: Christiane, Felix (b. 1971), Amanda (b. ~1978). Pseudonyms: George Oakes; Mike
  Revnec. Signs "G." on mailings and "Gareth S. Penn" in 1968 and 1976.
