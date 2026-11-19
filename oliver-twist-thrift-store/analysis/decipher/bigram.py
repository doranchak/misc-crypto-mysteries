import re, collections, math, pickle
SP='/private/tmp/claude-501/-Users-doranchak-projects-github-misc-crypto-mysteries/19d89b9d-5003-435e-9fdc-b7411d73b6b1/scratchpad/'
uni=collections.Counter(); bi=collections.Counter()
for f in ['lm/ot.txt','lm/en2.txt']:
    t=open(SP+f,errors='ignore').read().upper().replace('\u2019',"'").replace('\u2018',"'")
    # split on sentence-ish boundaries so bigrams don't cross periods
    for sent in re.split(r"[.!?;:]+",t):
        ws=re.findall(r"[A-Z]+(?:'[A-Z]+)*",sent)
        prev='<S>'
        for w in ws:
            uni[w]+=1; bi[(prev,w)]+=1; prev=w
        uni['<S>']+=1
# add modern-diary seed text
seed="""I HAVE LESS THAN NINE MONTHS TO GET MY LIFE TOGETHER AND START ACTING LIKE AN ADULT
I WOULD LIKE TO DEDICATE THIS BOOK TO MY LOVE MY PARTNER MY FUTURE WIFE
I WENT TO THE CEREMONY WITH MY FRIEND AND I FEEL LIKE A FAKER
MY WIFE AND I ARE EXPECTING OUR FIRST CHILD
IT IS A BOY IT IS A GIRL I DO NOT KNOW WHAT TO DO
I AM NOT READY TO BE A FATHER
MELANIE AND I ARE GOING TO HAVE A BABY
I DO NOT KNOW HOW TO BE A GOOD FATHER
WE ARE GOING TO THE DOCTOR TODAY
I THINK WE ARE GOING TO BE OKAY
I HOPE THAT I WILL BE A GOOD FATHER
I WAS AFRAID THAT I WOULD NOT BE ABLE TO DO IT
SHE IS THE BEST THING THAT EVER HAPPENED TO ME
THE BABY IS DUE IN THE SPRING
I AM GOING TO TRY TO BE BETTER
THIS IS GOING TO BE HARD BUT IT WILL BE WORTH IT""".split('\n')  # MODERNSEED
for s in seed:
    prev='<S>'
    for w in s.split():
        uni[w]+=3; bi[(prev,w)]+=3; prev=w
for s2 in open('seed_domain.txt').read().strip().split('\n'):
    prev='<S>'
    for w in s2.split():
        uni[w]+=4; bi[(prev,w)]+=4; prev=w
N=sum(uni.values())
def lp(prev,w,lam=0.6):
    pu=(uni.get(w,0)+0.1)/(N+1)
    cb=bi.get((prev,w),0); cp=uni.get(prev,0)
    pb=cb/cp if cp>0 else 0
    return math.log(lam*pb+(1-lam)*pu)
pickle.dump((uni,bi,N),open('bigram.pkl','wb'))
print(len(uni),len(bi),N)
