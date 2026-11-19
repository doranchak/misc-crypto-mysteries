import re, collections, math, pickle
SP='/private/tmp/claude-501/-Users-doranchak-projects-github-misc-crypto-mysteries/19d89b9d-5003-435e-9fdc-b7411d73b6b1/scratchpad/'
cnt=collections.Counter()
for f in ['lm/ot.txt','lm/en2.txt']:
    t=open(SP+f,errors='ignore').read().upper().replace('\u2019',"'").replace('\u2018',"'")
    cnt.update(re.findall(r"[A-Z]+(?:'[A-Z]+)*",t))
N=sum(cnt.values())
web=set(w.strip().upper() for w in open('/usr/share/dict/web2',errors='ignore') if w.strip().isalpha())
words=set(w for w,c in cnt.items() if c>=2 and len(w)<=14)|set(w for w in web if len(w)<=14)
CONTR="I'M I'VE I'LL I'D IT'S ISN'T DON'T DIDN'T WASN'T WEREN'T HASN'T HAVEN'T WON'T WOULDN'T COULDN'T SHOULDN'T CAN'T DOESN'T THAT'S THERE'S HE'S SHE'S WHAT'S LET'S WE'RE YOU'RE THEY'RE WE'VE YOU'VE THEY'VE WE'LL YOU'LL SHE'LL HE'LL IT'LL HE'D SHE'D WHO'S HERE'S THAT'LL AIN'T MELANIE'S SEAN'S BABY'S MOM'S DAD'S NOBODY'S EVERYONE'S SOMEONE'S".split()
words|=set(CONTR)
# contractions fragments and common modern words
extra="""A I S T M D LL VE RE
BOTANICAL WEDDING CEREMONY MELANIE GARDENS CHRONICLE TRIBULATIONS DEDICATE
TODAY TONIGHT YESTERDAY TOMORROW DIARY JOURNAL FRIEND FRIENDS BIRTHDAY
""".split()
words|=set(extra)
modern=set(open('modern.txt').read().split())
words|=modern
vocab={}
for w in words:
    c=cnt.get(w,0)
    vocab[w]=math.log((c+0.5)/N) if c>=2 else math.log(0.02/N)
for w in extra: vocab[w]=max(vocab.get(w,-20),-9.0)
for w in CONTR: vocab[w]=max(vocab.get(w,-20),-8.5)
for w in modern: vocab[w]=max(vocab.get(w,-20),-8.0)
# boost very short function words
for w in "A I S T M D".split(): vocab[w]=min(vocab[w],-9.0) if w in ('S','T','M','D') else vocab[w]
print(len(vocab),N)
pickle.dump(vocab,open('vocab.pkl','wb'))
