import re
from penn import bits
from fractions import Fraction
LINES = """Ida eats|ocarina vines|stairs starve|one sock civets|Ed Wood zoo exhibit|bit off Ali G
egrets indeed|satyr hanky panky|schwa tune|nemean wags
moist eponyms|cad task|abhor mines|ghost steam|trade steal|esp psychic|also old
DONUT JAM|almond oil pipette|op ed necks|reap aces|corvette ginger|arenas ashore|oh boy Malawi
bipolar|abets|blunts|aversion vet|Illini omitted|Alameda actual|rifts IOUs|ALer silent treatment|atop Gruyere
pending scree|I say moi|bluish ales|Mao alien|airy true|she's abdominal|Balzac enamel|deceit smog
Aunt Andie|synods damn|grieve skunk|Steffi onset|jampacked sank|axel grease zone|ohm coat hanger|hermit crab Orion
gets into trouble anoint|untold animists|at last rail|abdicator pizza|energetic asp|stinko hiss
free gas|on stage adjective|in love Lolita|tilt set|yes yes in error|inanity curious|inanity curios|red smears|argue rail|Amos makes do
elbows beaten eased|moth shoes seem|notes Peoria steer|ship Peoria elbow|wrap zit|wiser Toyota|Jupiter sense|scams a bit
Laverne greets|frost free rain|cited how|frat crew|overdo Mel Gibson|code name ovolo|free Qbert|gunning Lady Gaga|soap opera da capo|deviled ague
over angle|Oscar areas|vice amigos|Tapper asks to""".replace('\n','|').split('|')
for L in LINES:
    b=bits(L)
    v=int(b,2)
    f=float(Fraction(v,2**len(b)))
    print(f'{L:26s} {len(b):3d} bits  int={v:<16d} frac=0.{str(f)[2:14]:12s}  {b}')
