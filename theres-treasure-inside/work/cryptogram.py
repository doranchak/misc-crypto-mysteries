import re
CT = ["This hiuz li trxaq this plhiyb li plhxvs,",
      "mvpl lhxx vyq miplp li tihxpl bhxxy,",
      "vhhrex nic yid doxhx jxvcln poxxyp.",
      "Rl’p cyqxh, iexh, ry jxldxxy."]
PT = ["From rock to field, from strong to stream,",
      "past tree and posts to forest green,",
      "arrive you now where beauty sheens.",
      "It’s under, over, in between."]
key = {}
cw = re.findall(r"[a-z]+", " ".join(CT).lower()); pw = re.findall(r"[a-z]+", " ".join(PT).lower())
assert len(cw) == len(pw), (len(cw), len(pw))
for a, b in zip(cw, pw):
    assert len(a) == len(b), (a, b)
    for c, p in zip(a, b):
        assert key.setdefault(c, p) == p, (c, p)
inv = {}
for c, p in key.items():
    assert inv.setdefault(p, c) == c, ('not injective', p)
if __name__ == "__main__":
    print(len(key), "cipher letters")
    print("cipher->plain", " ".join(f"{c}{key[c]}" for c in sorted(key)))
    print("plain->cipher", " ".join(f"{p}{inv[p]}" for p in sorted(inv)))
    print("self-maps:", [c for c in key if key[c] == c])
    seen = set(); cyc = []
    for s in sorted(key):
        if s in seen: continue
        cur = s; ch = [s]; seen.add(s)
        while cur in key and key[cur] not in seen:
            cur = key[cur]; ch.append(cur); seen.add(cur)
        closed = cur in key and key[cur] == s
        cyc.append(("(" if closed else "[") + "".join(ch) + (")" if closed else "...]"))
    print("cycles/chains:", " ".join(cyc))
    import collections
    print(collections.Counter(ch for ch in "".join(CT).lower() if ch.isalpha()).most_common())
    print("unused plain:", sorted(set("abcdefghijklmnopqrstuvwxyz") - set(inv)), "unused cipher:", sorted(set("abcdefghijklmnopqrstuvwxyz") - set(key)))
