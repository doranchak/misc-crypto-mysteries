(function () {
  "use strict";
  const A = "ABCDEFGHIJKLMNOPQRSTUVWXYZ", VOW = "AEIOU", DEFAULT_KEY = "VOWEL";
  const $ = (id) => document.getElementById(id);
  const el = (tag, cls, text) => {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  };
  const KIND_CHAR = { space: " ", period: ".", comma: ",", question: "?", exclaim: "!" };
  const KIND_LABEL = { none: "unmapped", space: "word space", period: "period .", comma: "comma ,",
    question: "question ?", exclaim: "exclaim !", arith: "arithmetic letter" };

  let keyWord = DEFAULT_KEY, book = null, spareCfg = {}, last = "ct", cardsNow = [];

  // ---------- codebook ----------
  // key: plaintext vowel -> cipher letter.  A letter = key[nearest vowel at/before it] + 1-based offset.
  function makeBook(word) {
    const key = {}, inv = {}, enc = {}, dec = {}, spare = [];
    [...VOW].forEach((v, i) => { key[v] = word[i]; inv[word[i]] = v; });
    for (let i = 0; i < 26; i++) {
      let j = i;
      while (!VOW.includes(A[j])) j--;
      const code = key[A[j]] + (i - j + 1);
      enc[A[i]] = { code, vowel: A[j], off: i - j + 1, start: j };
      dec[code] = A[i];
    }
    for (const v of VOW) for (let d = 1; d <= 6; d++) {
      const code = key[v] + d;
      if (!(code in dec)) spare.push({ code, vowel: v, off: d, start: A.indexOf(v) });
    }
    return { key, inv, enc, dec, spare };
  }

  function resetSpare() {
    spareCfg = {};
    book.spare.forEach((s) => (spareCfg[s.code] = "none"));
    // puzzle convention: key[A] + 5 is the word space
    const sp = book.key.A + "5";
    if (sp in spareCfg) spareCfg[sp] = "space";
  }

  // ---------- cards ----------
  const runOf = (start, off) => A.slice(start, start + off).split("");

  function codeCard(code, kind, extra) {
    const v = book.inv[code[0]], d = +code.slice(1), start = A.indexOf(v);
    return Object.assign({ kind, ct: code, vowel: v, off: d, start, key: code[0], code }, extra);
  }

  function err(ct, note) { return { kind: "err", ct, pt: "⟨?⟩", tag: "error", note }; }

  function resolveCode(raw) {
    const L = raw[0].toUpperCase(), digits = raw.slice(1), shown = L + digits;
    const keyLetters = [...VOW].map((v) => book.key[v]).join(" ");
    if (!digits) return err(shown, "A cipher letter with no digit after it.");
    if (!(L in book.inv)) return err(shown, `"${L}" is not one of the key letters (${keyLetters}).`);
    if (!/^[1-6]$/.test(digits)) return err(shown, `The digit must be 1–6 (got "${digits}").`);
    const code = L + digits;
    if (code in book.dec) {
      const c = codeCard(code, "letter", { pt: book.dec[code] });
      c.note = `${L} = vowel ${c.vowel}; digit ${c.off} = ${c.off === 1 ? "the vowel itself" : "the letter " + (c.off - 1) + " after it"}.`;
      return c;
    }
    const kind = spareCfg[code] || "none";
    const base = codeCard(code, "spare", {});
    const arith = A[base.start + base.off - 1];
    if (kind === "arith")
      return Object.assign(base, { kind: "alt", pt: arith, tag: "spare",
        note: `Spare code read arithmetically: ${base.vowel}+${base.off - 1} = ${arith}.` });
    if (kind in KIND_CHAR)
      return Object.assign(base, { kind: kind === "space" ? "space" : "punct", pt: KIND_CHAR[kind],
        tag: KIND_LABEL[kind], note: `Spare code mapped to ${KIND_LABEL[kind]}.` });
    return Object.assign(base, { pt: "⟨" + code + "⟩", tag: "spare",
      note: `Spare code: no letter uses it (${base.vowel}+${base.off - 1} would be ${arith}, which already has its own code). Map it in the options to test a hypothesis.` });
  }

  // ---------- decode: any ciphertext string -> cards ----------
  function decodeCT(s) {
    const chars = Array.from(s), cards = [], wsBreak = $("vz-ws").checked;
    let i = 0;
    while (i < chars.length) {
      const c = chars[i];
      if (/[A-Za-z]/.test(c)) {
        let j = i + 1;
        while (j < chars.length && /[0-9]/.test(chars[j])) j++;
        cards.push(resolveCode(chars.slice(i, j).join("")));
        i = j;
      } else if (/\s/.test(c)) {
        let j = i;
        while (j < chars.length && /\s/.test(chars[j])) j++;
        if (wsBreak && cards.length && j < chars.length)
          cards.push({ kind: "space", ct: "␣", pt: " ", tag: "space", note: "Whitespace in the ciphertext, read as a word break." });
        i = j;
      } else if (/[0-9]/.test(c)) {
        let j = i;
        while (j < chars.length && /[0-9]/.test(chars[j])) j++;
        cards.push(err(chars.slice(i, j).join(""), "Digits with no cipher letter in front of them."));
        i = j;
      } else {
        cards.push({ kind: "lit", ct: c, pt: c, tag: "literal", note: "Not part of the cipher; passed through unchanged." });
        i++;
      }
    }
    return cards;
  }

  // ---------- encode: any plaintext string -> cards ----------
  function encodePT(s) {
    const cards = [], pass = $("vz-other").value === "pass", wsBreak = $("vz-ws").checked;
    const rev = {}; // character -> spare entry
    book.spare.forEach((sp) => {
      const k = spareCfg[sp.code];
      if (k in KIND_CHAR && !(KIND_CHAR[k] in rev)) rev[KIND_CHAR[k]] = sp;
    });
    let prevWs = false;
    for (const c of Array.from(s.trim())) {
      if (/\s/.test(c)) {
        if (prevWs) continue;
        prevWs = true;
        if (wsBreak) cards.push({ kind: "space", ct: " ", pt: " ", tag: "space", note: "Word break written as a literal space." });
        else if (" " in rev) cards.push(codeCard(rev[" "].code, "space", { pt: " ", tag: "space", note: "Word space." }));
        else cards.push({ kind: "skip", ct: "–", pt: "␣", tag: "skipped", note: "No spare code is mapped to word space, so the space was dropped." });
        continue;
      }
      // only characters that actually get encoded end a run of spaces; skipped ones don't
      if (/^[A-Za-z]$/.test(c) || c in rev || (pass && !/[0-9]/.test(c))) prevWs = false;
      if (/^[A-Za-z]$/.test(c)) {
        const u = c.toUpperCase(), e = book.enc[u];
        cards.push(codeCard(e.code, "letter", { pt: u, note: `${u} is in the run starting at vowel ${e.vowel}, position ${e.off}.` }));
      } else if (c in rev) {
        cards.push(codeCard(rev[c].code, "punct", { pt: c, tag: "mapped", note: `"${c}" uses the spare code you mapped.` }));
      } else if (pass && !/[0-9]/.test(c)) {
        cards.push({ kind: "lit", ct: c, pt: c, tag: "literal", note: "No code for this character; passed through unchanged." });
      } else {
        const digit = /[0-9]/.test(c);
        cards.push({ kind: "skip", ct: "–", pt: c, tag: "skipped",
          note: digit ? "Digits can't be encoded: they would merge with the cipher's own digits."
                      : "No code for this character; skipped." });
      }
    }
    // a word space with nothing encoded before or after it (e.g. next to skipped digits) is meaningless: drop it
    const kept = () => cards.map((c, i) => (c.kind !== "skip" ? i : -1)).filter((i) => i >= 0);
    let idx = kept();
    if (idx.length && cards[idx[0]].kind === "space") { cards.splice(idx[0], 1); idx = kept(); }
    if (idx.length && cards[idx[idx.length - 1]].kind === "space") cards.splice(idx[idx.length - 1], 1);
    return cards;
  }

  const ctString = (cards) => {
    const toks = cards.filter((c) => c.kind !== "skip").map((c) => c.ct);
    return $("vz-ws").checked || $("vz-layout").value === "compact" ? toks.join("") : toks.join(" ");
  };
  const ptString = (cards) => cards.map((c) => c.pt).join("");

  // ---------- rendering ----------
  function render(cards) {
    cardsNow = cards;
    const box = $("vz-cards");
    box.textContent = "";
    if (!cards.length) box.appendChild(el("div", "vz-empty", "Nothing to show yet."));
    cards.forEach((c) => {
      const d = el("div", "vz-card k-" + c.kind);
      d.title = c.note || "";
      if (c.code) d.dataset.code = c.code;
      d.appendChild(el("div", "ct", c.ct));
      if (c.vowel) {
        d.appendChild(el("div", "kk", `${c.key} → ${c.vowel}`));
        const run = el("div", "run");
        runOf(c.start, c.off).forEach((ch, i, a) => run.appendChild(el(i === a.length - 1 ? "b" : "span", null, ch)));
        d.appendChild(run);
      }
      d.appendChild(el("div", "pt", c.pt === " " ? "␣" : c.pt));
      if (c.tag) d.appendChild(el("div", "tag", c.tag));
      if (c.vowel) {
        d.addEventListener("mouseenter", () => ribbonHover(c.code, true));
        d.addEventListener("mouseleave", () => ribbonHover(c.code, false));
      }
      box.appendChild(d);
    });
    // mark codes used in the current message on the codebook
    const used = new Set(cards.filter((c) => c.code).map((c) => c.code));
    document.querySelectorAll("#vz-rib .vz-cell").forEach((b) => b.classList.toggle("used", used.has(b.dataset.code)));
  }

  function ribbonHover(code, on) {
    const v = book.inv[code[0]], d = +code.slice(1);
    document.querySelectorAll(`#vz-rib .vz-cell[data-v="${v}"]`).forEach((b) => {
      const o = +b.dataset.o;
      b.classList.toggle("run", on && o < d);
      b.classList.toggle("hit", on && o === d);
    });
  }

  function cardsHover(code, on) {
    document.querySelectorAll(`#vz-cards .vz-card[data-code="${code}"]`).forEach((c) => c.classList.toggle("hl", on));
  }

  function renderRibbon() {
    const rib = $("vz-rib");
    rib.textContent = "";
    rib.appendChild(el("div", "vz-rh", ""));
    for (let d = 1; d <= 6; d++) rib.appendChild(el("div", "vz-rh", String(d)));
    for (const v of VOW) {
      rib.appendChild(el("div", "vz-rl", `${v} → ${book.key[v]}`));
      for (let d = 1; d <= 6; d++) {
        const code = book.key[v] + d, letter = book.dec[code];
        const b = el("button", "vz-cell" + (letter ? "" : " spare"));
        b.type = "button";
        b.dataset.code = code; b.dataset.v = v; b.dataset.o = d;
        b.appendChild(el("span", "p", letter || "·"));
        b.appendChild(el("span", "c", code));
        b.title = letter ? `${code} = ${letter}` : `${code} is a spare code (${KIND_LABEL[spareCfg[code]]})`;
        b.addEventListener("mouseenter", () => cardsHover(code, true));
        b.addEventListener("mouseleave", () => cardsHover(code, false));
        b.addEventListener("click", () => {
          const ch = letter || KIND_CHAR[spareCfg[code]];
          if (ch == null) return;
          $("vz-pt").value += ch;
          run("pt");
        });
        rib.appendChild(b);
      }
    }
  }

  function renderSpare() {
    const box = $("vz-spare");
    box.textContent = "";
    book.spare.forEach((s) => {
      const w = el("label", null, "");
      w.appendChild(el("span", "c mono", s.code));
      const sel = el("select");
      Object.keys(KIND_LABEL).forEach((k) => {
        const o = el("option", null, k === "arith" ? `arithmetic letter (${A[s.start + s.off - 1]})` : KIND_LABEL[k]);
        o.value = k;
        sel.appendChild(o);
      });
      sel.value = spareCfg[s.code];
      sel.addEventListener("change", () => { spareCfg[s.code] = sel.value; renderRibbon(); run(last); });
      w.appendChild(sel);
      box.appendChild(w);
    });
  }

  function status(cards, dir) {
    const n = (k) => cards.filter((c) => c.kind === k).length;
    const parts = [`${cards.filter((c) => c.kind !== "skip" && c.kind !== "lit").length} cipher units`,
      `${n("letter")} letters`, `${n("space")} spaces`];
    if (n("punct") + n("alt")) parts.push(`${n("punct") + n("alt")} mapped spare`);
    if (n("spare")) parts.push(`${n("spare")} unmapped spare`);
    if (n("lit")) parts.push(`${n("lit")} literal`);
    if (n("skip")) parts.push(`${n("skip")} skipped`);
    const html = [parts.join(" · ")];
    if (n("err")) html.push(`<span class="bad">${n("err")} invalid</span>`);
    if (dir === "pt") {
      const back = ptString(decodeCT($("vz-ct").value));
      const want = ptString(cards.filter((c) => c.kind !== "skip"));
      html.push(back === want ? '<span class="ok">round trip ✓</span>'
                              : '<span class="bad">round trip ✗</span>');
    }
    $("vz-status").innerHTML = html.join(" · ");
  }

  // ---------- control flow ----------
  function run(dir) {
    last = dir;
    let cards;
    if (dir === "pt") {
      cards = encodePT($("vz-pt").value);
      $("vz-ct").value = ctString(cards);
    } else {
      cards = decodeCT($("vz-ct").value);
      $("vz-pt").value = ptString(cards);
    }
    render(cards);
    status(cards, dir);
  }

  function setKey(word) {
    keyWord = word;
    book = makeBook(word);
    resetSpare();
    renderSpare();
    renderRibbon();
  }

  function resetAll() {
    $("vz-key").value = DEFAULT_KEY;
    $("vz-ws").checked = false;
    $("vz-layout").value = "compact";
    $("vz-other").value = "skip";
    keyMsg("", false);
    setKey(DEFAULT_KEY);
  }

  function keyMsg(text, bad) {
    const m = $("vz-keymsg");
    m.textContent = text;
    m.classList.toggle("bad", !!bad);
  }

  $("vz-key").addEventListener("input", () => {
    const k = $("vz-key").value.toUpperCase().replace(/[^A-Z]/g, "");
    $("vz-key").value = k;
    if (k.length === 5 && new Set(k).size === 5) {
      keyMsg([...VOW].map((v, i) => `${v}→${k[i]}`).join(" "), false);
      setKey(k);
      run(last);
    } else {
      keyMsg("need 5 distinct letters (" + k.length + " so far)", true);
    }
  });
  $("vz-pt").addEventListener("input", () => run("pt"));
  $("vz-ct").addEventListener("input", () => run("ct"));
  ["vz-ws", "vz-layout", "vz-other"].forEach((id) => $(id).addEventListener("change", () => run(last)));

  document.querySelectorAll("#vz [data-ct],#vz [data-pt]").forEach((b) => {
    b.addEventListener("click", () => {
      resetAll();
      if (b.dataset.ct != null) { $("vz-ct").value = b.dataset.ct; if (b.dataset.pt != null) $("vz-pt").value = b.dataset.pt; run("ct"); }
      else { $("vz-pt").value = b.dataset.pt; run("pt"); }
    });
  });

  document.querySelectorAll("#vz [data-copy]").forEach((b) => {
    b.addEventListener("click", () => {
      const t = $(b.dataset.copy);
      t.select();
      const old = b.textContent;
      const done = () => { b.textContent = "Copied"; setTimeout(() => (b.textContent = old), 1200); };
      if (navigator.clipboard) navigator.clipboard.writeText(t.value).then(done, () => { document.execCommand("copy"); done(); });
      else { document.execCommand("copy"); done(); }
    });
  });

  // start with the puzzle ciphertext
  resetAll();
  $("vz-ct").value = "%%CT%%";
  run("ct");

  // exposed for testing from the console
  window.vowelCipher = { run, setKey, decodeCT, encodePT, get book() { return book; }, get cards() { return cardsNow; } };
})();
