"""Best-effort restoration of the glitched ArtFight "rules" paragraph.

Each paragraph (same order as corrupted.txt) is a list of segments:  (tier, text, [source patterns])
  tier  c = colour-matched (pieces that share a colour/size in the original screenshot, reunited; see styles.py)
        k = recovered   (words survive in the garbled text, at most ~1 letter off)
        r = repaired    (recognisable word(s) with several letters missing, swapped or displaced)
        i = inferred    (a guess assembled from context and displaced fragments; NOT verifiable)
        g = gap         (a fragment I could not read; shown as an ellipsis)
  source patterns: strings from the garbled paragraph; the part in {braces} is what gets highlighted, the rest is
  context used to find the right occurrence. A pattern may start with "§N|" to point into paragraph N instead of the
  paragraph the segment is listed in (colour-matched words are made of pieces from several paragraphs).
  rules_view.py asserts every pattern exists.
"""

PARAS = [
# ---- P1 ---------------------------------------------------------------------------------------------------
[("k", "fun!!", ["{fun!!}y"]),
 ("g", "…", ["{y} error", "error{s-swful} o", "{o}error"])],

# ---- P2 ---------------------------------------------------------------------------------------------------
[("g", "…", ["{Gesitputt}No"]),
 ("k", "No hate.", ["tes:{No hate}be"]),
 ("r", "Be", ["hate{be}An"]),
 ("g", "…", ["be{A}nPlease"]),
 ("r", "Please be", ["n{Please b}"]),
 ("g", "…", ["{I} hgorms", "{hgorms)}"]),
 ("r", "ONLY if", ["{LY if}"]),
 ("g", "…", []),
 ("r", "been given", ["{een giv}"]),
 ("g", "…", []),
 ("k", "fine", ["giv {fine} haven"]),
 ("g", "…", []),
 ("r", "haven't specified before", ["{haven specifer preore}"]),
 ("g", "…", []),
 ("r", "presentation", ["preore i{ssentation}you"]),
 ("r", "you", ["issentation{you}hakely"]),
 ("g", "…", []),
 ("r", "likely to", ["you{hakely to} reven"]),
 ("g", "…", ["to {reven}ecified"]),
 ("r", "specified otherwise,", ["reven{ecified otherwit,}"]),
 ("k", "psycho", ["{psycho} kigee"]),
 ("g", "…", ["psycho {kigee} rules"]),
 ("k", "rules, but", ["{rules, but}"]),
 ("r", "suggest outfit", ["{suggesutfit}"]),
 ("g", "…", [])],

# ---- P3 ---------------------------------------------------------------------------------------------------
[("r", "Please don't draw", ["{lease don't draw}"]),
 ("r", "my non-human chars (e.g. werewolf)", ["Dev{my non-human ch}ye", "ye {werewolf)}"]),
 ("r", "as human or vice versa.", ["werewolf) {or vicevearaers.}", "expNSFW {as}"]),
 ("g", "…", ["amp. {Dev}my", "{amp.}", "vicevearaers.{nender}No"]),
 ("k", "No", ["nender{No} exp"]),
 ("r", "explicit", ["No {exp}NSFW"]),
 ("k", "NSFW", ["exp{NSFW}"]),
 ("g", "…", [])],

# ---- P4 ---------------------------------------------------------------------------------------------------
[("g", "…", ["{igher}"]),
 ("c", "Don't", ["{Do't}", "§2|beA{n}Please"]),
 ("g", "…", ["{ing} thnds", "{thnds}/cigs"]),
 ("k", "…/cigs", ["thnds{/cigs}lving"]),
 ("r", "involving my chars", ["cigs{lving my char}"]),
 ("k", "– cos", ["char {- cos} pleaChaners"]),
 ("g", "…", ["cos {pleaChaners}"]),
 ("k", "as", ["Chaners {as} have"]),
 ("g", "…", ["as {have b}"]),
 ("k", "or etc.", ["b {or etc.}"]),
 ("r", "Romance is cool,", ["{Romaacts cool,}"]),
 ("k", "I'd", ["{I'd} umin"]),
 ("g", "…", ["I'd {umintingh}"]),
 ("r", "authentic interaction", ["{enentic interaction}my"]),
 ("g", "…", ["interaction{my caneraction}"]),
 ("r", "with you when", ["{witsyouwhe}"]),
 ("r", "(unless specified otherwise)", ["{(unle else}", "error {ictie)}"]),
 ("r", "chars are fine as animals,", ["{chrs is fineas anim,}", "(human{als}"]),
 ("r", "may have special characters otherwise.", ["{aray have specs cters ehawise.}"]),
 ("g", "…", ["ehawise. {y} (human"]),
 ("r", "(humans", ["{(human}als"]),
 ("r", "(either friendly", ["{(eshther friendly}"]),
 ("g", "…", ["friendly {ins}"]),
 ("r", "don't draw their", ["ins {thon't draw meir}"]),
 ("i", "prey", ["{orey} unless"]),
 ("k", "unless", ["{unless} theexen"]),
 ("g", "…", ["unless {theexen -}A"]),
 ("c", "Aye", ["-{A}rsa", "§3|ch{ye} werewolf"]),
 ("g", "…", ["-A{rsa;d}"]),
 ("k", "human", ["d {human} f-ap"]),
 ("g", "…", ["human {f-ap} aphbe", "{aph}be happy"]),
 ("r", "be happy to see", ["aph{be happy to see}"]),
 ("r", "who", ["{who}uONne"]),
 ("g", "…", ["who{uONne}"]),
 ("r", "with", ["{wi h} migth"]),
 ("r", "might", ["{migth}"]),
 ("k", "me", ["migth {me}"]),
 ("g", "…", ["{er oat ot}tional", "no{g ther}"]),
 ("k", "and", ["ther {and} havetive"]),
 ("r", "have", ["and {have}tive"]),
 ("g", "…", ["have{tive} is"]),
 ("r", "outfit ideas", ["{fiteraoemhttfit ideas}"]),
 ("r", "you", ["ideas {yu}"])],

# ---- P5 ---------------------------------------------------------------------------------------------------
[("c", "Additional notes:", ["bi{Addi}in", "§4|ot{tional}", "§4|{no}g ther", "§2|g{tes:}No hate"]),
 ("g", "…", ["{D} biAddi", "Addi{in} smrc", "{smrc okatction or bsc isy}"]),
 ("i", "character battle", ["isy {alacter haraattle} so"]),
 ("k", "so go ham,", ["{so go ham,}"]),
 ("r", "my guys are 20+.", ["{my cuy f are 20+.}"]),
 ("g", "…", ["20+.{oted dssue.}"]),
 ("r", "Exceptions involve all the guys", ["{eceptions invome all t guys}"]),
 ("r", "their gender,", ["{eir gend.i}"]),
 ("r", "unless my", ["{unlesemy}"]),
 ("r", "single characters", ["{crarhae singlacters}"]),
 ("k", "are", ["singlacters {are} bof"]),
 ("r", "both of them", ["{bof thsrren}"]),
 ("k", "😎", ["{😎}"])],

# ---- P6 ---------------------------------------------------------------------------------------------------
[("g", "…", ["{ly} enco"]),
 ("r", "encourage", ["{enco}ified", "f{urage}"]),
 ("g", "…ified/", ["enco{ified/}visor"]),
 ("r", "visual", ["/{visormual} f"]),
 ("k", "drawing", ["{drawing} pCrickin"]),
 ("g", "…", ["{pCrickin}"]),
 ("k", "jam.", ["{jam.}"]),
 ("k", "More", ["{more} lie"]),
 ("i", "like this: my", ["{liethiemy}"]),
 ("k", "characters", ["{characters} goingvered"]),
 ("r", "going covered in", ["{goingvered in}"]),
 ("k", "blood/afraid and exhausted/fighting tooth and nail to survive",
       ["{blood/afraid and exhausted/fighting tooth and nail to survive}"]),
 ("k", "<-", ["{<-} m"]),
 ("r", "my spoiler, be mindful", ["{m spller, e mindful}"])],
]
