const fs = require('fs'), crypto = require('crypto');
const src = fs.readFileSync(process.argv[2], 'utf8');
const code = src.split('/* ==LAB-ENGINE-START== */')[1].split('/* ==LAB-ENGINE-END== */')[0];
const E = new Function(code + '; return {sha512, pySbox, runCipher, pyKeyWords};')();
let bad = 0;
// 1) SHA-512 vs node crypto on varied lengths (incl. padding edge cases)
for (const n of [0, 1, 55, 56, 111, 112, 113, 127, 128, 129, 300]) {
  const b = crypto.randomBytes(n);
  const a = Buffer.from(E.sha512(new Uint8Array(b))).toString('hex'), r = crypto.createHash('sha512').update(b).digest('hex');
  if (a !== r) { bad++; console.log('SHA512 MISMATCH len', n); }
}
console.log('sha512 checked');
// 2) S-box + encrypt vs python reference values
const ref = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
for (const r of ref) {
  const k = E.pySbox(r.key);
  if (JSON.stringify(k.forward) !== JSON.stringify(r.forward)) { bad++; console.log('SBOX MISMATCH', JSON.stringify(r.key)); continue; }
  const e = E.runCipher(r.msg, k.forward, k.inverse, r.init, 'enc').out;
  const d = E.runCipher(r.enc, k.forward, k.inverse, r.init, 'dec').out;
  if (e !== r.enc || d !== r.msg) { bad++; console.log('CIPHER MISMATCH', JSON.stringify(r.key)); }
}
console.log(ref.length, 'python reference cases checked; failures:', bad);
process.exit(bad ? 1 : 0);
