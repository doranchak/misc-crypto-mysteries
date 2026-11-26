"""Build posts/transcripts/caption-*.json for the typed captions in the Google Doc.

cipher       = text as typed in the doc (it uses Latin look-alikes for some anchors)
cipher_norm  = same text with those anchors replaced by the Cyrillic letter that decodes
computed     = straight decode of cipher_norm (slips show up as wrong letters / ?)
reading_ru   = my reading, with every slip corrected (each one listed in slips)

Input: posts/captions-normalized.json (the doc's captions grouped per post, with
"caption_norm" = Latin anchors replaced by hand-checked Cyrillic choices; the
doc's bare Latin "I" stands for И or Я and was resolved by grammar).

    /opt/homebrew/bin/python3.11 -I build_captions.py posts/captions-normalized.json
    /opt/homebrew/bin/python3.11 -I build_posts_section.py
"""
import json, re, sys
sys.path.insert(0, ".")
from decode import decode_text, decode_token, strict_decode

posts = json.load(open(sys.argv[1], encoding="utf-8"))  # posts_norm.json

C = {}
C[0] = dict(after="image3.png",
 reading_ru="Как же я терпеть не могу большинство людей на этой блядской планете, в этой блядской стране, в этом блядском посёлке. Все они блять какие-то надменные, строят из себя пиздец каких важных личностей или людей, хотя на деле всего лишь отбитые наглухо дикари с абсолютно поломанным нахуй компасом. Нет чтобы вежливо какие-то моменты прояснить, они всегда с таким тоном грубым, напыщенным говорят, будто на месте в рот ебали меня и всю мою семью во все дыры нахуй. Я-то тебе что блять сделал? Это особенно сильно касается всех мигрантов и людей советской закалки, в общем, тех, кто вообще не уважает чужие мнения, ценности, кто считает себя правым по факту возраста или превосходящей мою силы, иначе говоря, выбирая критерии правоты словно ёбаные звери, обезьяны. Если вы меня не уважаете, с хуяли я обязан вас? Аминь",
 english="God, how I can't stand most people on this fucking planet, in this fucking country, in this fucking village. They're all, fuck, somehow arrogant, acting like they're such damn important personalities or people, when really they're just completely unhinged savages with an absolutely fucking broken compass. Instead of politely clearing some things up, they always talk in such a rude, pompous tone, as if they'd fucked me and my whole family in every hole right there on the spot. What the fuck did I ever do to you? This goes especially for all the migrants and people of the Soviet mould, in short, those who don't respect other people's opinions or values at all, who think they're right by virtue of age or of strength greater than mine; in other words, choosing their criteria of who's right like fucking beasts, apes. If you don't respect me, why the fuck am I obliged to [respect] you? Amen",
 slips=[
  ("ТЕПРЕТЬ", "ТЕРПЕТЬ", "Р and П swapped: Е→Р→П is 2↓2→|←, the text has 2↓→|→ (Е→П→Р)", "misspelling in plaintext"),
  ("СТРОЮС", "СТРОЯТ", "О→Я is 3↓2→, written 3↓→ (lands on Ю); the next chunk 3↑2→ is measured from Я", "author slip"),
  ("КАКДР", "КАКИХ", "К→И is ↑3→, written 2↑3→ (lands on Д); same slip as ТАКДА below", "author slip"),
  ("И?И", "ИЛИ", "И↑2→⟳ walks off the grid; ИЛИ would be И↓2←⟳ (↑2→ is the move back from Л to И)", "author slip"),
  ("ОТГ???Ж", "ОТБИТЫЕ", "Т→Б is 3↑3←, written 3↑←; every later chunk fits Б", "author slip"),
  ("ВЕЖВ??Е", "ВЕЖЛИВО", "Ж→Л is ↓, written ↑", "author slip"),
  ("МОМЕНЧ?", "МОМЕНТЫ", "Н→Т is ↓, written 2↓", "author slip"),
  ("ОЙНИ", "ОНИ", "stray bar: О↑|4→|↑ should be О↑4→|↑", "transcription or author slip"),
  ("КАСА?БА?", "КАСАЕТСЯ", "after ⟳ (back to А) the next chunk 2↑3← was measured from С, the letter before ⟳; from А it would be ↓", "author slip"),
  ("ЦИННОСТИ", "ЦЕННОСТИ", "Ц→И encoded (3↑→); standard spelling has Е", "misspelling in plaintext"),
  ("К?П", "КТО", "К→Т is ↓3→, written ↓4→", "author slip"),
  ("ЗВЕРЗ", "ЗВЕРИ", "Р→И is 2↑2→, written 2↑→", "author slip"),
  ("ОБЯЗА?", "ОБЯЗАН", "А→Н is 2↓4→, written 2↓5→ (five steps right runs off the 5-wide grid)", "author slip"),
 ])
C[1] = dict(after="image9.png",
 reading_ru="Я ещё жив и даже здоров!\nИ, как вы могли заметить по первому слайду, я начал изучать иврит, и мне невероятно сильно нравится, как он звучит :Р\nיש לי טלפון, אבל [אין?] לי מחשב :(\nИзвиняюсь, что долго не было контента. Просто мне и рассказывать сейчас особо нечего. Всё как-то... идёт своим чередом, что ли. Но скоро обязательно что-нибудь да произойдёт! ;)",
 english="I'm still alive and even healthy!\nAnd, as you may have noticed from the first slide, I've started learning Hebrew, and I'm incredibly into how it sounds :P\n[Hebrew:] \"I have a phone, but [no?] computer :(\"\nSorry there hasn't been any content for a long time. It's just that I don't have much to tell right now. Everything is sort of... running its course, I guess. But something is bound to happen soon! ;)",
 slips=[
  ("טלפן", "טלפון", "decodes as טלפן (no ו); four letters encoded, so the vav was simply left out (defective spelling)", "misspelling in plaintext"),
  ("יס", "אין?", "י2↓2→ decodes as יס, not a word; the sad face suggests אין (\"don't have\"), which would need anchor א", "unresolved"),
  ("РАССКАЗЫВАТ", "РАССКАЗЫВАТЬ", "final Ь (Т→Ь = 2↓) missing", "author or transcription slip"),
 ])
C[2] = dict(after="image5.png",
 reading_ru="Я полетел в отпуск, к себе на малую родину в станицу Заплавскую. Не сказать, что я этому сильно рад, но разнообразить жизнь мне явно не помешало бы. В течение поездки (два самолёта и один поезд) сахар в крови очень сильно поднялся вплоть до следующего дня после съедения выданного в полёте сэндвича, что выбило из колеи и снизило настроение на последующие часы :( У родственников висит странное напряжение в воздухе, что не может не удручать. Ещё интернет паршивый...\nВ остальном всё более менее спокойно. Занимаюсь спортом, ем. Жаль у меня здесь друзей нет, а если б и были, то у нас бы слишком сильно различались мировоззрения, потому что деревня.\nУмоляю тебя, Боже, вылечи меня от диабета... Я слишком устал…",
 english="I flew off on vacation, to my little homeland, the stanitsa of Zaplavskaya. Can't say I'm thrilled about it, but some variety in my life clearly wouldn't hurt. During the trip (two planes and one train) my blood sugar rose very high, all the way into the next day, after I ate the sandwich they handed out on the flight, which threw me off and dragged my mood down for the following hours :( At my relatives' there's a strange tension hanging in the air, which can't help but get you down. And the internet is lousy...\nOtherwise everything is more or less calm. I do sports, I eat. Pity I have no friends here, and even if I did, our worldviews would differ too much, because it's a village.\nI beg you, God, cure me of diabetes... I'm too tired…",
 slips=[
  ("ПОЛАНАЖ", "ПОЛЕТЕЛ", "Л→Е is ↑2←, written 2↑2← (lands on А); the remaining chunks 2↓4→|2↑4←|↓2→ fit Е-Т-Е-Л exactly", "author slip"),
 ])
C[3] = dict(after="image15.png",
 reading_ru="Сколько же птиц обитает в моём районе! Я в изумлении",
 english="So many birds live in my area! I'm amazed",
 slips=[("МОЁН", "МОЁМ", "Ё→М is ↓2→, written ↓3→", "author slip")])
C[4] = dict(after="image1.png",
 reading_ru="Мы обсуждали всякое, они ели различные вкусняшки (я не ел, потому что мне нельзя, зато я выпил пять кружек чая), также мы ходили в магазин, причём я с полной кружкой чая, ещё мой друг купил мне фруктовое пюре без сахара... В общем, было довольно весело! Также мой другой друг заметил, что я какой-то невесёлый и спросил, в чём дело, но я как полный дурак просто отмахнулся, соврав, что всё в порядке. Эх, а ведь был такой шанс высказаться! О болезни, об одиночестве, о скуке... Но я прозевал момент! И Бог его знает, когда будет следующий... 🙁🙁",
 english="We talked about all sorts of things, they ate various treats (I didn't, because I'm not allowed, but I drank five mugs of tea), we also went to the shop, me carrying a full mug of tea, and my friend bought me fruit puree with no sugar... All in all, it was pretty fun! Also, my other friend noticed I was kind of down and asked what was wrong, but like a complete fool I just brushed it off, lying that everything was fine. Ah, and that was such a chance to open up! About the illness, about loneliness, about boredom... But I missed the moment! And God knows when the next one will come... 🙁🙁",
 slips=[
  ("М?", "МЫ", "М→Ы is 3↓, written 3→", "author or transcription slip"),
  ("ЗНАЕ?", "ЗНАЕТ", "Е→Т is 2↓4→, written 2↓4↓", "author or transcription slip"),
 ])
C[5] = dict(after="image11.png",
 reading_ru="Вчера у меня были очень печальные новости - я первый раз в жизни вколол инсулин по причине высокого сахара 😢😢 Сначала всё было нормально: я, как обычно, накупил себе сладостей, чтобы потом отработать на велотренажёре, и сперва всё было в порядке, ибо сахар упал, но ближе к ужину очень сильно поднялся - пришлось сознаться, что я ел запрещёнку. В итоге меня поставили перед фактом, что я больше не должен есть обычные сладости, а исключительно диабетические, но по сравнению с привычными они такие невкусные, к тому же их всегда мало... Я настаиваю на том, чтобы уже полностью перейти на инсулинотерапию, но родители, почему-то, не хотят этого. Я не знаю, как мне жить до полной смерти бета-клеток😭😭",
 english="Yesterday I had some very sad news: for the first time in my life I injected insulin, because of high sugar 😢😢 At first everything was normal: as usual I bought myself a pile of sweets, planning to work them off on the exercise bike afterwards, and at first everything was fine, since my sugar dropped, but closer to dinner it went up very high, and I had to confess that I'd eaten forbidden stuff. In the end I was told flat out that I must not eat ordinary sweets any more, only diabetic ones, but compared to the usual kind they're so tasteless, and on top of that there's never enough of them... I'm pushing to switch fully to insulin therapy already, but my parents, for some reason, don't want that. I don't know how I'm supposed to live until my beta cells are completely dead😭😭",
 slips=[
  ("ИНСУРНТ", "ИНСУЛИН", "У→Л is 2↑2→, written ↑2→ (lands on Р)", "author slip"),
  ("БЫЛОНОРМАЛЬНО", "БЫЛО НОРМАЛЬНО", "missing space between two words", "transcription slip"),
  ("ОЧЕНЧ", "ОЧЕНЬ", "Н→Ь is 3↓, written 2↓", "author slip"),
  ("ТАКДА", "ТАКИЕ", "К→И is ↑3→, written 2↑3→ (lands on Д)", "author slip"),
  ("КЛЕТЙЁ", "КЛЕТОК", "Т→О is 4←, written ↑4←", "author slip"),
 ])
C[6] = dict(after="image8.png", reading_ru="Вот такие дела!", english="That's how things are!", slips=[])
C[7] = dict(after="image6.png",
 reading_ru="О сегодняшнем дне🤠\nВсем привет! Сегодня я хочу рассказать о прошедшем дне.\nУтром было относительно спокойно, единственное что около дома напротив повязали каких-то пьяниц🥴🥴\nС отцом разговор был натянутым из-за вчерашнего... Полагаю, он во мне разочарован :(\nПосле того, как я съел незапланированную шоколадку и поездил целый час на велосипеде сахар был нормальным, но стоило мне съесть бутеры, как он сильно поднялся и долго не приходил в норму... Зато под вечер словил гипогликемию😛😛\nКогда гулял, записал звук ранее невиданной птицы. Как опознаю, то сразу покажу её.\nНа этом, вроде бы, все. Всем спокойной ночи! :)",
 english="About today🤠\nHi everyone! Today I want to tell you about the day that just ended.\nThe morning was relatively calm, except that some drunks got hauled off near the building across the street🥴🥴\nThe talk with my father was strained because of yesterday... I suppose he's disappointed in me :(\nAfter I ate an unplanned chocolate bar and rode the bike for a whole hour my sugar was normal, but as soon as I ate some sandwiches it shot up and took a long time to come back to normal... Then again, towards evening I got a hypo😛😛\nWhile out walking I recorded the call of a bird I'd never seen before. Once I identify it, I'll show it right away.\nThat's about it, I think. Good night, everyone! :)",
 slips=[
  ("ВОЕМ", "ВСЕМ", "В→С is 3↓→, written 3↓2← (lands on О)", "author or transcription slip"),
  ("БЫЛ?", "БЫЛО", "Л→О is ↓2←, written ↓3←", "author slip"),
  ("ПОВ?????", "ПОВЯЗАЛИ", "В→Я is 6↓, written 6→; the remaining chunks 5↑→|↑3←|2↓2→|↑2→ fit Я-З-А-Л-И exactly", "author slip"),
  ("СЯЙЦЧ?", "СЪЕСТЬ", "С→Ъ is 2↓←, written 3↓← (lands on Я)", "author slip"),
  ("ПРИХП??М", "ПРИХОДИЛ", "Х→О is ↑2←, written ↑←", "author slip"),
  ("З?С?", "ЗАТО", "З→А is ↑3←, written ↑4←", "author slip"),
  ("ВСАЗ", "ВСЕМ", "С→Е is 2↑3←, written 3↑3← (lands on А)", "author slip"),
 ])
C[8] = dict(after="image4.png",
 reading_ru="Он у меня довольно консервативный человек, явно советской закалки, оттого смотрел на меня с очень большим недовольством и презрением. Я с мамой пытались сгладить ситуацию, но он был непреклонен, назвав это \"уродством\". Предложил вместо губы проколоть ухо, либо же вообще набить татуировку, но я отказался. А я, вроде, не хочу портить отношения с отцом, но его конкретно устаревшее мировоззрение мне до жути не нравится :( А индивидуальным и в то же время красивым быть хочется. Именно поэтому я, кроме, буквально, пары человек, не расскажу о своей ориентации :( Потому что тогда все от меня отвернутся или того хуже съедят заживо и не подавятся.",
 english="He's a pretty conservative person, clearly of the Soviet mould, so he looked at me with very great displeasure and contempt. Mom and I tried to smooth things over, but he wouldn't budge, calling it \"disfigurement\". He suggested piercing my ear instead of my lip, or even getting a tattoo instead, but I refused. And I sort of don't want to spoil things with my father, but I really, terribly dislike his downright outdated worldview :( And I do want to be individual and good-looking at the same time. That's exactly why, apart from literally a couple of people, I won't tell anyone about my orientation :( Because then everyone will turn away from me, or worse, eat me alive without so much as choking.",
 slips=[
  ("М?МЮ", "МЕНЯ", "М→Е is ↑3←, written ↑4←", "author slip"),
  ("БОЛЬШЕМ", "БОЛЬШИМ", "Ш→И is 4↑4→, written 4↑ (lands on Е)", "author slip or misspelling"),
  ("СИТУАЦЮ", "СИТУАЦИЮ", "И skipped: 2↓2← is the correct move Ц→Ю", "letter skipped in plaintext"),
  ("НЕПРИКЛОНЕН", "НЕПРЕКЛОНЕН", "Р→И encoded; standard spelling has Е", "misspelling in plaintext"),
  ("АНД И,", "А Я,", "the doc has the English words \"And I\" here; read as А Я (the doc's Latin I stands for both И and Я elsewhere too)", "transcription"),
  ("ВОДЕ", "ВРОДЕ", "missing bar: 3↓2← should be 3↓|2← (В→Р→О), as in the other ВРОДЕ", "transcription or author slip"),
  ("КОНКРЕЧТУ", "КОНКРЕТНО", "Е→Т is 2↓4→, written 3↓4→; ↑ and ↓4← then fit Н and О", "author slip"),
  ("НРАЙРЪЩ?", "НРАВИТСЯ", "А→В is 2→, written 2↓", "author slip"),
  ("ПАРЕ", "ПАРЫ", "Р→Е encoded (2↑2←); grammar wants пары", "grammar slip in plaintext"),
  ("ОРИЕНАЦИИ", "ОРИЕНТАЦИИ", "Т skipped: 2↑4← is the correct move Н→А", "letter skipped in plaintext"),
  ("ВРЕ", "ВСЕ", "В→С is 3↓→, written 3↓ (lands on Р)", "author or transcription slip"),
  ("ЗАЖИВ", "ЗАЖИВО", "final О (В→О = 3↓2←) missing", "letter skipped in plaintext"),
 ])
C[9] = dict(after="image14.png",
 reading_ru="В это же время всяких кровососущих насекомых было невообразимое количество. Далее я направился по грунтовой дороге и обнаружил нечто деревянное, что на фото. Позднее я пришёл к старому корпусу, где не оказалось ничего интересного. Попытался взломать и проникнуть в вахтовый грузовик - не вышло, ибо двери оказались запертыми, а стёкла слишком прочными, и я, явно разочарованный, вернулся домой через лес. Жаль в ТТ нельзя вставить полную версию музыки, ведь она отлично передаёт настроение этого маленького путешествия в неизвестное :)",
 english="Meanwhile there was an unimaginable number of all kinds of bloodsucking insects. Next I set off down a dirt road and found something wooden, the thing in the photo. Later I came to an old building, where there turned out to be nothing interesting. I tried to break into a shift-crew truck and get inside, but it didn't work, because the doors turned out to be locked and the windows too strong, and I, clearly disappointed, went home through the forest. Pity you can't put the full version of the music on TT [TikTok], because it captures the mood of this little journey into the unknown perfectly :)",
 slips=[
  ("НЕВООБРАЗИМГ?", "НЕВООБРАЗИМОЕ", "М→О is ↓3←, written ↓3↑", "author or transcription slip"),
  ("ОБНАЛОВДЖ", "ОБНАРУЖИЛ", "А→Р is 3↓2→, written 2↓2→ (lands on Л); every later chunk fits Р", "author slip"),
  ("ЛЕЭ", "ЛЕС", "Е→С is 2↓3→, written 2↓3↓", "author or transcription slip"),
  ("ВСТАВИТ?", "ВСТАВИТЬ", "Т→Ь is 2↓, written 2→", "author or transcription slip"),
  ("ВЕШЩР?", "ВЕРСИЮ", "Е→Р is 2↓2→, written 2↓2↓", "author or transcription slip"),
 ])

def find_token(norm_text, computed):
    for tok in norm_text.split():
        best = strict_decode(tok)
        core = re.sub(r"[^\wА-ЯЁא-ת?⁇]", "", best)
        if core == re.sub(r"[^\wА-ЯЁא-ת?⁇]", "", computed):
            return tok
    for tok in norm_text.split():  # word glued to a neighbour (emoji, hyphen)
        if computed in strict_decode(tok):
            return tok
    return None

out_ix = 0
for pi, p in enumerate(posts):
    if pi not in C:
        continue
    c = C[pi]
    cipher = "\n".join(p["caption"])
    norm = "\n".join(p["caption_norm"])
    computed = "\n".join(strict_decode(l) for l in p["caption_norm"])
    slips = []
    for comp, intended, fix, kind in c["slips"]:
        tok = find_token(norm, comp)
        if tok is None and comp not in ("БЫЛОНОРМАЛЬНО", "АНД И,"):
            print("!! token not found for", comp, file=sys.stderr)
        slips.append(dict(token=tok or "", computed=comp, intended=intended, fix=fix, kind=kind))
    rec = dict(id=f"caption-after-{c['after'].split('.')[0]}", after_image=c["after"],
               source="typed in the Google Doc", cipher=cipher, cipher_norm=norm,
               computed=computed, reading_ru=c["reading_ru"], english=c["english"],
               slips=slips, uncertain=[])
    fn = f"posts/transcripts/{rec['id']}.json"
    json.dump(rec, open(fn, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote", fn, len(slips), "slips")
