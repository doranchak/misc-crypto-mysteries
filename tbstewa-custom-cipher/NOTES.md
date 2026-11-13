# tbstewa custom cipher — SOLVED

Source: https://www.reddit.com/r/codes/comments/1xi8s97/challenge_can_you_crack_my_custom_cipher_5000/

Plaintext: opening of the **Bee Movie script** ("According to all known laws of aviation, ...").
All 3,792 posted ciphertext chars decoded; author's own `encrypt()` with the recovered S-box reproduces
the ciphertext exactly. Visual report: `report.html`.

## Cipher (crypt-test/crypt.py)
`S[c_i] = S[p_i] + S[p_{i-1}] (mod 95)`, `S[p_-1] = init`, S = random.Random(passphrase).shuffle(range(95)).
Underneath the S-box this is a plain autokey sum over Z_95; the S-box only relabels symbols.

## Attack (ciphertext only, ~1 s, no key search, sample key/init NOT used)
1. With x=S[p], y=S[c], A_i = sum_{t<=i} (-1)^t y_t:  x_i = (-1)^i (A_i - init).
2. A repeated ciphertext substring c[i..]==c[j..] implies x_i - x_j = ±d; for English d=0 (plaintext repeats too).
   (a+b = b+a also means "ab" and "ba" collide.)
3. x_i = x_j is a homogeneous LINEAR equation in the 95 labels + init, coefficients read off the ciphertext.
4. Repeats >=5 chars -> 438 equations; solve over F_5 and F_19 (95 = 5*19): rank 94 of 96, nullity 2.
   Nullspace = {true key} + {constant vector: all labels equal} -> 5*19 = 95 shifted candidate keys.
5. Score 95 decodes with a char-trigram LM: best -2.32, next -4.73. Winner is the Bee Movie text.
6. Repeats >=4 (764 eq.) keep nullity at exactly 2, so no spurious equations. Works with ~2,000 chars (>=4) / ~3,000 (>=5).

## Notes
- Key recovered only up to scaling: (k*S, k*init), k coprime to 95 -> 72 equivalent keys, all decrypt identically.
  The passphrase string itself is not recoverable (and not needed).
- Ciphertext as pasted = 3,792 chars (not ~5,000); plaintext ends mid-sentence. 10 literal double-backslashes were correct.
- "ourjob" (no space) is in the source text fed to the cipher (re-encryption matches).
- The 15-char ciphertext period `|nu5\R$98>C:1f6` x4 = "Yellow, black. " x4.

## Interactive lab (in report.html)
Encrypt/decrypt tool + per-character pipeline (S-box -> add/sub prev -> inverse S-box), S-box table, step table.
Key = recovered challenge key, or any passphrase: JS re-implements Python's random.Random(str).shuffle
(SHA-512 seeding + MT19937) and matches crypt.py on 40 cases: `python3 -I tests/make_ref_cases.py ref.json && node tests/test_lab_engine.js report.html ref.json`.
Encrypting the first sentence with the recovered key reproduces the start of the posted ciphertext.

## Files
cipher.txt, algebraic_attack.py (equations + F_p nullspace), solve.py (candidates + scoring -> result.json),
build_data.py / build_report.py / report_template.html (-> report.html), tests/ (lab engine vs crypt.py), crypt-test/ (author's repo clone).
solve.py / build_data.py need an English corpus dir of .txt files (used Project Gutenberg books).
