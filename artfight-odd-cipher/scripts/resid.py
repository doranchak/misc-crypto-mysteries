import sys
from collections import Counter
sys.path.insert(0,'.')
from lettercmp import letters
C=open('../rules/corrupted.txt').read().splitlines()
def resid(par, cand, drop_error=True):
    A=letters(C[par],drop_error); B=letters(cand)
    return "".join(sorted((A-B).elements())),"".join(sorted((B-A).elements()))
if __name__=="__main__":
    tests={
     5:"encourage drawing jam. more like this: my characters going covered in blood/afraid and exhausted/fighting tooth and nail to survive <- my spoiler, be mindful",
     2:"Please don't draw my non-human chars (eg. werewolf) as human or vice versa. No explicit NSFW as",
    }
    for k,v in tests.items():
        print(k, resid(k,v))
