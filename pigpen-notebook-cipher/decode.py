"""Decode the notebook cipher from the stroke-token transcription.
Token alphabet: U=open-top box, N=Pi with bottom-right hook, b=Pi plain (no hook), C=[ bracket, E=[ bracket with inner dash,
L=L shape, O=square, o=round O, A=Lambda, V=V, <, >, T=inverted T, h=hook-stroke, 7=dash-over-slash ("7"),
c=small Pi-like arc ("C-with-hook" glyph used for V), plus marks | - \\ /"""
KEY = {   # unit (token string) -> letter
 'U':'E', 'U\\':'I', 'U/':'I',
 'A':'F', 'A\\':'L',
 'O':'O', 'o':'O', 'O/-':'Y',
 'L':'H', '<':'M', 'V':'G', 'T':'R',
 '>|':'A', '|':'D', '\\-':'N',
 'b':'B', 'N':'C', 'Q':'C',
 'C|':'T', '5|':'T', 'E':'U',
 '|<':'P', '|>':'P',
 'h':'W', 'h|':'W',
 '-/':'S', '7':'X',
 'c-':'V',
}
LINES = [
 ["U\\\\-", "U7>|NA\\O/-"],            # IN EXACLY
 ["O\\-U", "<U\\\\-EUC|U"],            # ONE MINUETE
 ["C|LU", "OAAU\\NU"],                 # THE OFFICE
 ["|>LO\\-U", "h|U\\A\\A\\"],          # PHONE WILL
 ["TU\\\\-V", ">|\\-|", "U\\A\\A\\"], # RING AND ILL
 ["bU", "-/U\\-C|", "C|o"],            # BE SENT TO
 ["C|LU", "OAAU\\NU"],                 # THE OFFICE
 ["hLUTU", "<O/-", ">||O|<C|U/c-U"],   # WHERE MY ADOPTIVE
 ["A>|<U\\A\\O/-", "h|U\\A\\A\\"],     # FAMILY WILL
 ["NO<U", "NOA\\A\\UNC|", "<U"],       # COME COLLECT ME
 ["U\\", ">|NNU|>C|", "h|U\\C|L"],     # I ACCEPT WITH
 ["VT>|5|C|U\\C|E|U"],                 # GRATTITUDE
]
UNITS = sorted(KEY, key=lambda u:-len(u))
def seg(w):
    def rec(i):
        if i==len(w): return []
        for u in UNITS:
            if w.startswith(u,i):
                r=rec(i+len(u))
                if r is not None: return [u]+r
        return None
    r=rec(0)
    if r is None: raise ValueError(f'cannot segment {w}')
    return r
if __name__=='__main__':
    # note: leading '|' before '>' / '<' is the pre-mark of P, so handle by pre-segmentation preference
    for li,l in enumerate(LINES,1):
        words=[]
        for w in l:
            try: words.append(''.join(KEY[u] for u in seg(w)))
            except ValueError as e: words.append('<<'+str(e)+'>>')
        print(li,' '.join(words))
