import sys,re
from collections import Counter
def letters(s,drop_error=False):
    if drop_error: s=re.sub(r'error','',s,flags=re.I)
    return Counter(c.lower() for c in s if c.isalpha())
def cmp(a,b,drop_error=True):
    A=letters(a,drop_error);B=letters(b)
    return "".join(sorted((A-B).elements())),"".join(sorted((B-A).elements()))
if __name__=="__main__":
    C=open('../rules/corrupted.txt').read().splitlines()
    G3="Please don't draw my non-human characters (ex. werewolf) as human or vice versa. No explicit NSFW as"
    print(cmp(C[2],G3))
