# 2026-11-19: repairs two key exemplars and adds the IS glyph in key_glyphs.json (no pickles needed: retrace.py traces
# straight from the flattened pages embedded in glyph-editor.html).
#   FF (left example, b2R OFFSPRING): the middle bar is thin and light, the old trace (threshold factor 0.92) lost it -> 3 bars again
#   CC (left example, b2R ACCIDENTAL): the old glyph box started at the 2nd hump; the glyph spans x 1286-1397 (two humps,
#       rising top stroke, long diagonal). The neighbouring I-ring touches the diagonal near x=1393 -> small exclusion.
#   IS : the word IS is ONE fused glyph (slashed ellipse + top bar/zig-zag): b3L "THIS IS ALL", b3R "MELANIE IS OCCUPYING"
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import retrace as R

HERE = os.path.dirname(os.path.abspath(__file__))
fn = os.path.join(HERE, 'key_glyphs.json')
G = json.load(open(fn))


def clean(r):
    r = dict(r)
    r.pop('keep', None)
    return r


ff = clean(R.trace_rect('b2R', (153, 1014, 72, 108), thrf=1.0))
cc = clean(R.trace_rect('b2R', (1284, 915, 113, 85), exclude=[(1394, 936, 12, 45)]))
G['fx']['FF'][0] = ff
G['fx']['CC'][0] = cc
G['fx']['IS'] = [clean(R.trace_rect('b3L', (143, 1662, 95, 120))),
                 clean(R.trace_rect('b3R', (1305, 848, 112, 122)))]
json.dump(G, open(fn, 'w'))
print('FF[0]', round(ff['w'], 1), round(ff['h'], 1), '| CC[0]', round(cc['w'], 1), round(cc['h'], 1),
      '| IS', [(r['page'], round(r['w'], 1), round(r['h'], 1)) for r in G['fx']['IS']])
