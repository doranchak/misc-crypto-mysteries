import cv2, numpy as np, pickle, sys
from glyphlib import *
def process(name, box, rot=None, tag=None, block=101, C=22, minh=45):
    reg0 = load_region(name, box, 0)
    if rot is None:
        th0 = binarize(reg0, block, C)
        rot = best_angle(th0)
    reg = load_region(name, box, rot)
    th = binarize(reg, block, C)
    comps, lab = components(th)
    gl = merge_contained(comps, lab)
    print(tag, 'rot',rot,'glyph units',sum(1 for g in gl if g['kind']=='glyph'),'dots',sum(1 for g in gl if g['kind']=='dot'))
    return reg, th, lab, gl, rot
def overlay(reg, gl, path):
    vis = cv2.cvtColor(reg, cv2.COLOR_GRAY2BGR)
    for k,g in enumerate(gl):
        col=(0,0,255) if g['kind']=='glyph' else (255,0,0)
        cv2.rectangle(vis,(g['x'],g['y']),(g['x']+g['w'],g['y']+g['h']),col,2)
    cv2.imwrite(path, vis)
