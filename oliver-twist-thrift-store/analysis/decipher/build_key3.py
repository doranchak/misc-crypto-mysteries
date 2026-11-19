# Re-trace the flagged letters as WHOLE glyphs (all strokes in the aligner's glyph box) and rebuild ING as wave+loop
import json, numpy as np, cv2
import boot, keyglyphs as kg, keyglyphs2 as k2
P=k2.P
MAN={'A':['b2R:4:642','b2L:4:388'],'C':['b2R:3:417','b2R:10:346'],'N':['b2R:10:1087','b3R:16:243'],
     'R':['b2R:4:358','b3R:9:1791'],'U':['b2R:7:888','b2R:9:681']}
ING=[('b2R',3,1,9),('b3R',16,16,24)]     # last two pieces of EXPECTING, SHIVERING (wave + loop)
G=json.load(open('key_glyphs_old.json'))
def find(key):
    pg,li,x=key.split(':'); li=int(li); x=int(x)
    for ln in P[pg]['lines']:
        if ln['i']==li:
            for g in ln['glyphs']:
                if int(g['x'])==x: return pg,li,g
    raise KeyError(key)
for L,keys in MAN.items():
    out=[]
    for k in keys:
        pg,li,g=find(k); r=k2.render_glyph(pg,li,(g['x'],g['y'],g['w'],g['h'])); r.pop('keep'); out.append(r)
    G['ex'][L]=out
ing=[]
for pg,li,i,j in ING:
    pcs=boot.lines_of(pg)[li][j-2:j]; keep,up=k2.trace_box(pg,pcs,box=None); r=kg.to_path(keep,up,eps=0.5); r['page']=pg; ing.append(r)
G['fx']['ING']=ing
json.dump(G,open('key_glyphs.json','w'))
print({k:len(v) for k,v in G['ex'].items()},{k:len(v) for k,v in G['fx'].items()})
