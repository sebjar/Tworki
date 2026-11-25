# -*- coding: utf-8 -*-
"""Dopisuje przepisy znalezione przy przegladzie z pazdziernika 2026."""
import io, json

D = "https://www.tiktok.com/@anaboliczny.darek/photo/7678743478884404512"
NEW = [
    (140, "tt:7532103187541560598", "coocharz", "TikTok",
     "https://www.tiktok.com/@coocharz/video/7532103187541560598",
     "Skyrowe chlebki z Kurczakiem BBQ",
     "PROTEINOWY PONIEDZIAŁEK - Skyrowe chlebki z Kurczakiem BBQ i serem. Makrosy jednej "
     "sztuki 340 kcal | BTW: 31/5/43 Składniki (8 sztuk): Kurczak: 600 g mięsa z piersi "
     "kurczaka 1 łyżeczka soli 1 łyżeczka pieprzu 1 łyżeczka wędzonej papryki 1 łyżeczka "
     "czosnku granulowanego 1/2 łyżeczki kuminu 120 g sosu barbecue Olej do smażenia "
     "Ciasto: 400 g mąki pszennej 1 łyżeczka soli 1 łyżeczka proszku do pieczenia "
     "420-450 g skyra Dodatkowo: 160 g sera mozzarella light"),
    (141, "tt:7687606766204357921", "stry.ola", "TikTok",
     "https://www.tiktok.com/@stry.ola/video/7687606766204357921",
     "Qurwitto", "odcinek 3 - Qurwitto"),
    (142, "tt:7685385807770684705", "dejm_life", "TikTok",
     "https://www.tiktok.com/@dejm_life/video/7685385807770684705",
     "Makaron z nduja i gorgonzolą",
     "Prosty, konkretny i komfortowy. Oliwa → cebula → czosnek → nduja → kurczak → "
     "śmietanka → makaron. Na koniec gorgonzola i właściwie tyle."),
    (143, "tt:7685767803449789728", "amadeusz_braksator", "TikTok",
     "https://www.tiktok.com/@amadeusz_braksator/video/7685767803449789728",
     "Kurczak z Airfryera na zapas",
     "Składniki: 2 filety z kurczaka 2 łyżeczki papryki słodkiej Sól ¼ łyżeczki czosnku "
     "½ łyżeczki pietruszki Opcjonalnie ¼ łyżeczki curry Pieczenie: 35 minut – 190*C "
     "Kanapka: Włoskie pieczywo Rukola Pomidor Kurczak Cheddar Parmezan Ogórek kiszony "
     "Sos: 60 g majonezu light 30 g musztardy 10 g sosu BBQ 5 g miodu"),
    (144, "tt:7676896147763498272", "michal.gotuje", "TikTok",
     "https://www.tiktok.com/@michal.gotuje/video/7676896147763498272",
     "Nocne bagietki bez wyrabiania",
     "NOCNE BAGIETKI BEZ WYRABIANIA Składniki: 500 g mąki pszennej typ 450–650 lub typ 00 "
     "350 g wody 9 g soli 3 g świeżych drożdży lub 1 g suchych instant"),
    (145, "tt:7678743478884404512#burger", "anaboliczny.darek", "TikTok", D + "?image_index=3",
     "Podwójny cheeseburger z frytkami",
     "Szybkie i tanie Obiady z biedronki! PODWÓJNY CHEESEBURGER Z FRYTKAMI "
     "Kcal: 755 B: 41 g W: 102 g T: 20 g koszt: ~29 zł"),
    (146, "tt:7678743478884404512#caesar", "anaboliczny.darek", "TikTok", D + "?image_index=5",
     "Chrupiąca sałatka Caesar",
     "Szybkie i tanie Obiady z biedronki! CHRUPIĄCA SAŁATKA CAESAR "
     "Kcal: 747 B: 57 g W: 49 g T: 34 g koszt: ~25 zł"),
    (147, "tt:7678743478884404512#mcchicken", "anaboliczny.darek", "TikTok", D + "?image_index=7",
     "McChicken",
     "Szybkie i tanie Obiady z biedronki! MCCHICKEN Jedna porcja z 4 "
     "Kcal: 360 B: 30 g W: 46 g T: 8 g"),
    (148, "tt:7673470904789241121", "ugotujmi", "TikTok",
     "https://www.tiktok.com/@ugotujmi/photo/7673470904789241121",
     "Dirty fries po meksykańsku",
     "Spodobała wam się poprzednia wersja dirty fires to dodaje kolejne"),
    (149, "tt:7664704410211175702", "sarahsplates", "TikTok",
     "https://www.tiktok.com/@sarahsplates/photo/7664704410211175702",
     "Avocado carbonara",
     "One avocado + 2 egg yolks = the creamiest pasta you'll ever make."),
    (150, "ig:DdGjE07sxJ4", "foxx.gotuje", "Instagram",
     "https://www.instagram.com/foxx.gotuje/reel/DdGjE07sxJ4/",
     "Prosty azjatycki obiad",
     "Prosty azjatycki obiad w kilka minut. 400 g udek bez kości lub piersi z kurczaka, "
     "sól i pieprz, 2-3 łyżeczki papryki słodkiej lub wędzonej, 1 puszka mleka kokosowego, "
     "1 limonka, odrobina szalotki i czosnku, opcjonalnie odrobina imbiru, olej, ryż, "
     "szczypiorek. Pikle: 1 ogórek, 3-4 łyżki sosu sojowego, 2-3 łyżki octu ryżowego, "
     "1-2 łyżeczki miodu, sezam, płatki chili."),
]

parsed = json.load(io.open("parsed.json", encoding="utf-8"))
ci = json.load(io.open("curate_input.json", encoding="utf-8"))
have = {r["key"] for r in ci}
added = 0
for idx, key, author, plat, link, name, cap in NEW:
    if key in parsed or key in have:
        print("juz jest:", key)
        continue
    if len(ci) != idx:
        raise SystemExit("indeks %d, a lista ma %d" % (idx, len(ci)))
    parsed[key] = dict(author=author, caption=cap, cat="", file_ings=[], link=link, n_ing=0,
                       name=name, platform=plat, servings=None, site_ings=[],
                       sources=["przegląd 2026-10"], steps=[], typ="video",
                       parsed=dict(ings=[], name=name, review="", servings=None, steps=[]))
    ci.append(dict(author=author, blog=None, cap=cap, file_ings=[], key=key, link=link,
                   name=name, platform=plat, score=0, tr=""))
    added += 1
json.dump(parsed, io.open("parsed.json", "w", encoding="utf-8"), ensure_ascii=False)
json.dump(ci, io.open("curate_input.json", "w", encoding="utf-8"), ensure_ascii=False)
print("dopisano:", added, "| parsed:", len(parsed), "| curate_input:", len(ci))
