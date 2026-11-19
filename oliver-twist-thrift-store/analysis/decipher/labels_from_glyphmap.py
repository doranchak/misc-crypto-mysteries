# turn hand-specified glyph partitions (glyph_map.json) into per-piece training labels (explicit_labels.json); single-piece glyphs with a classifier class only
import json
from decode import LI
G=json.load(open('glyph_map.json')); E=json.load(open('explicit_labels.json')); n=0
for k,g in G.items():
    page,li=k.split(':'); d=E.setdefault(page,{}).setdefault(li,{})
    for x in g:
        if len(x)==2 and x[1] in LI: d[str(x[0])]=x[1]; n+=1
json.dump(E,open('explicit_labels.json','w')); print('labels written',n)
