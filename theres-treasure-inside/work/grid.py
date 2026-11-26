GRID_ROWS = """
QVUCALILENINETEENBMA
CRETEHTREAOUCSIFEVLE
OROUNDHNIMIHSTOLIARO
UHTRONROEOCEHSRARDWO
NOUBTDELOELTLNTRETAW
TETATSEONYNEOAOLINEO
PMUEHTTSEWODAHREERET
EONSKAEPTOOOILPASIEC
LESDBNOORAOOEVLEWTSR
ENTUFIVETNTNCOIUJTSO
VRNIEMAKLAWESCODTRID
EADTTEYOSSQUAREEERHT
NMTOPLECEOHETQUARRYO
NSIOSMIXZFDQBCCASLIY
APSOREZNGQZPSAPPHIRE
""".split()
assert all(len(r)==20 for r in GRID_ROWS), [len(r) for r in GRID_ROWS]
R, C = len(GRID_ROWS), 20
DIRS = {(0,1):'E',(0,-1):'W',(1,0):'S',(-1,0):'N',(1,1):'SE',(-1,-1):'NW',(1,-1):'SW',(-1,1):'NE'}
def find_all(word):
    out=[]
    for r in range(R):
        for c in range(C):
            for (dr,dc),name in DIRS.items():
                ok=True
                for k,ch in enumerate(word):
                    rr,cc=r+dr*k,c+dc*k
                    if not(0<=rr<R and 0<=cc<C) or GRID_ROWS[rr][cc]!=ch: ok=False;break
                if ok: out.append((r,c,dr,dc,name))
    return out
