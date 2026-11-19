# user's reading of spread 3 (2026-11-18) keyed by (page, my line index)
USER={
 ('b3L',5):"SITTING AT HOME PREPARING TO LEAVE",
 ('b3L',6):"FOR FINAL MANAGING SHIFT AT OLD",
 ('b3L',7):"TOWN PIPACO",
 ('b3L',9):"THE DAY HAS STARTED OFF BADLY FOR",
 ('b3L',11):"MELANIE AND I I JUST CAN'T SEEM",
 ('b3L',13):"TO KEEP MYSELF FROM BEING SELFISH",
 ('b3L',14):"IN THE FACE OF WHAT MUST BE A",
 ('b3L',15):"NEARLY OVERWHELMING FEAR FOR HER",
 ('b3L',16):"BUT I AM SCARED TOO SO I",
 ('b3L',18):"HELP IT IF I WANT A CERTAIN AMOUNT",
 ('b3L',19):"OF AFFIRMATION TO MAKE ME FEEL THAT",
 ('b3L',21):"THIS IS ALL WORTHWHILE",
 ('b3L',20):"AM READY TO",
 ('b3L',22):"GIVE HER EVERYTHING BUT ONLY IF I",
 ('b3L',23):"GET WHAT LITTLE I NEED",
 ('b3R',1):"NOW I'M AT OLD TOWN ONE",
 ('b3R',2):"WOULD THINK I WOULD BE EXPER",
 ('b3R',3):"IENCING SOME DEPTH OF EMOTION",
 ('b3R',4):"THIS BEING MY LAST BAR SHIFT I DON'T",
 ('b3R',5):"REALLY FEEL ANYTHING",
 ('b3R',6):"NATURALLY MELANIE IS OCCUPYING",
 ('b3R',8):"HER NORMAL PLACE AT THE BAR",
 ('b3R',9):"WOULD THINK SHE WOULD BE GOOD AND TIRED",
 ('b3R',10):"OF THAT BY NOW BUT I KNOW HER",
 ('b3R',11):"BETTER THAN THAT I GET THE FEELING THAT",
 ('b3R',12):"SHE WOULD BE ENTIRLY COMFORTABLE",
 ('b3R',13):"SITTING IN THAT SAME SPOT EIGHT HOURS",
 ('b3R',14):"AT A SHOT IF I STAYED HERE",
 ('b3R',15):"AT THIS TIME I AM ON MY BREAK",
 ('b3R',16):"MELANIE IS A PALE WHIMPERING MESS",
 ('b3R',17):"CONTINUOUSLY HALF TEARFUL AND NON",
 ('b3R',18):"RESPONSIVE SHE MADE HER NORMAL",
 ('b3R',19):"I'M HUNGRY STATEMENT WHICH REALLY",
 ('b3R',20):"MEANS PAMPER ME SO I DON'T HAVE TO",
}
# pieces that are gutter shadow / page-edge blotches (not glyphs) -> removed before aligning
DROP={('b3L',7):[0,1,2,15,16,17],('b3L',11):[0,1],('b3L',6):[0],('b3L',13):[0,1],('b3L',15):[0,24],('b3L',16):[0],('b3L',18):[26],('b3R',9):[0],('b3R',20):[30]}
FORCE={}

# ---- hand-specified glyph partitions that replace the aligner's choice for the given piece range [lo,hi) of a line
# item = [piece,...,'TEXT']   or   {'box':[x,y,w,h],'t':'TEXT','p':[pieces it occupies]}   (box in flat-page pixel coordinates)
MANUAL={
 ('b3L',21):{(0,14):[[0,'TH'],[1,'I'],[2,'S'],[3,'IS'],[4,'A'],[5,'LL'],[6,'W'],[7,'O'],[8,'R'],[9,'TH'],[10,'WH'],[11,'I'],[12,'L'],[13,'E']]},
 ('b3L',20):{(0,9):[[0,'A'],[1,'M'],[2,'R'],[3,'E'],[4,'A'],[5,'D'],[6,'Y'],[7,'T'],[8,'O']]},
 ('b3R',9):{(24,27):[{'box':[1669,1094,70,100],'t':'T','p':[24,25]},[26,'I']]},
 ('b3L',22):{(15,25):[[15,'B'],[16,'U'],{'box':[1090,1851,71,85],'t':'T','p':[16]},[17,'O'],[18,19,'N'],[20,'L'],[21,'Y'],[22,'I'],[23,'F'],[24,'I']]},
 ('b3L',18):{(5,8):[[5,'IT'],[6,'I'],{'box':[429,1403,58,100],'t':'F','p':[6]},[7,'I']]},
}
# glyphs whose piece was lost (merged into another line / filtered out): word is added to the line with explicit boxes
EXTRA={
 ('b3L',20):[{'word':'I','x':1133,'glyphs':[{'box':[1133,1673,94,157],'t':'I'}]}],
 ('b3L',16):[{'word':"CAN'T",'x':1547,'glyphs':[{'box':[1547,1263,70,117],'t':'C'},{'box':[1628,1286,55,50],'t':'A'},{'box':[1675,1291,81,50],'t':'N'},{'box':[1756,1274,50,62],'t':'T'}]}],
 ('b3R',8):[{'word':'ONE','x':1674,'glyphs':[{'box':[1674,962,113,100],'t':'O'},{'box':[1783,975,90,86],'t':'N'},{'box':[1874,977,68,79],'t':'E'}]}],
}
# words the user (or I) is not sure about -> shown with '?' (forced suggestion), everything else = verified reading
UNCERTAIN={('b3R',6):['IS'],('b3L',7):['PIPACO'],('b3L',23):['GET']}
