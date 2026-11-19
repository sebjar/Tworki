# -*- coding: utf-8 -*-
"""Wartosci odzywcze na 100 g + przeliczniki jednostek na gramy.
Wartosci typowe (USDA / tabele PL). Sluza do oszacowania makr przepisu."""

# nazwa kanoniczna -> (kcal, bialko, tluszcz, wegle) na 100 g
# Wartosci dla produktu SUROWEGO, w takiej postaci, w jakiej wazy sie go do przepisu
# (mieso surowe, makaron i ryz suche; zeberka razem z koscia).
NUTR = {
    # --- mieso i ryby
    "pierś z kurczaka": (110, 23, 1.8, 0), "kurczak": (110, 23, 1.8, 0),
    "udka z kurczaka": (130, 19, 6, 0), "polędwiczki z kurczaka": (110, 23, 1.8, 0),
    "mięso mielone wołowe": (250, 26, 17, 0), "mięso mielone z kurczaka": (143, 22, 6, 0),
    "mięso mielone wieprzowe": (263, 17, 21, 0), "mięso mielone z indyka": (150, 21, 7, 0),
    "mięso mielone": (250, 26, 17, 0), "mięso": (200, 20, 12, 0),
    "wołowina": (160, 21, 8.5, 0), "wołowina w paskach": (160, 21, 8.5, 0),
    "indyk": (110, 24, 1.5, 0), "schab": (143, 21, 6, 0), "chorizo": (455, 24, 38, 2),
    "boczek": (400, 13, 38.5, 0.5), "żeberka wieprzowe": (200, 11.2, 17.2, 0),
    "jagnięcina": (282, 25, 20, 0), "kiełbasa": (300, 14, 27, 2),
    "łosoś": (208, 20, 13, 0), "ryba biała": (82, 18, 0.7, 0),
    "dorsz": (82, 18, 0.7, 0), "pstrąg": (148, 21, 7, 0), "krewetki": (85, 20, 0.5, 0),
    "paluszki surimi": (95, 8, 1, 12),
    # --- nabial i jaja
    "jajko": (143, 13, 10, 0.7), "mleko": (61, 3.4, 3.3, 4.8), "kefir": (55, 3.5, 2, 4.5),
    "masło": (717, 0.9, 81, 0.1), "śmietana kremówka": (292, 2.4, 30, 3.1),
    "śmietanka": (195, 2.5, 20, 3), "śmietana": (195, 2.5, 20, 3),
    "śmietana 12%": (130, 3, 12, 3.5), "śmietana 18%": (184, 2.8, 18, 3.4),
    "śmietana kwaśna": (198, 2.4, 20, 2.9), "serek śmietankowy": (247, 6, 23, 4),
    "skyr": (63, 11, 0.2, 4), "jogurt grecki": (122, 3.8, 10, 4.2), "jogurt grecki 0%": (56, 10, 0.2, 3.6),
    "jogurt naturalny": (61, 3.5, 3.3, 4.7), "serek wiejski": (98, 11, 4.3, 3.4),
    "labneh": (174, 8, 14, 4), "twaróg": (98, 18, 1, 3.5),
    "parmezan": (431, 38, 29, 4.1), "grana padano": (384, 33, 28, 0),
    "mozzarella": (280, 22, 22, 2.2), "cheddar": (403, 25, 33, 1.3),
    "gouda": (356, 25, 27, 2.2), "ser żółty": (371, 25, 29, 1.3),
    "ser feta": (264, 14, 21, 4.1), "ser sałatkowy": (264, 14, 21, 4.1),
    "gorgonzola": (350, 19, 29, 2.3), "halloumi": (321, 22, 25, 2.2),
    "mascarpone": (429, 4.5, 44, 4.8),
    # --- warzywa i owoce
    "cebula": (40, 1.1, 0.1, 9.3), "czerwona cebula": (40, 1.1, 0.1, 9.3),
    "szalotka": (72, 2.5, 0.1, 17), "dymka": (32, 1.8, 0.2, 7.3),
    "szczypiorek": (30, 3.3, 0.7, 4.4), "czosnek": (149, 6.4, 0.5, 33),
    "pomidor": (18, 0.9, 0.2, 3.9), "pomidorki koktajlowe": (18, 0.9, 0.2, 3.9),
    "papryka": (26, 1, 0.3, 6), "papryka czerwona": (31, 1, 0.3, 6),
    "papryka zielona": (20, 0.9, 0.2, 4.6), "papryczka chili": (40, 1.9, 0.4, 9),
    "ziemniaki": (77, 2, 0.1, 17), "bataty": (86, 1.6, 0.1, 20),
    "marchewka": (41, 0.9, 0.2, 9.6), "ogórek": (15, 0.7, 0.1, 3.6),
    "sałata": (15, 1.4, 0.2, 2.9), "sałata lodowa": (14, 0.9, 0.1, 3),
    "roszponka": (21, 2, 0.4, 3.6), "rukola": (25, 2.6, 0.7, 3.7),
    "mix sałat": (17, 1.5, 0.2, 3), "szpinak": (23, 2.9, 0.4, 3.6),
    "szpinak mrożony": (23, 2.9, 0.4, 3.6), "brokuł": (34, 2.8, 0.4, 7), "brukselka": (43, 3.4, 0.3, 9),
    "cukinia": (17, 1.2, 0.3, 3.1), "seler naciowy": (16, 0.7, 0.2, 3),
    "pieczarki": (22, 3.1, 0.3, 3.3), "kapusta": (25, 1.3, 0.1, 6),
    "awokado": (160, 2, 15, 9), "kiełki": (30, 3, 0.5, 4),
    "natka pietruszki": (36, 3, 0.8, 6.3), "kolendra": (23, 2.1, 0.5, 3.7),
    "koperek": (43, 3.5, 1.1, 7), "bazylia": (23, 3.2, 0.6, 2.7),
    "świeże zioła": (30, 3, 0.7, 5), "imbir": (80, 1.8, 0.8, 18),
    "cytryna": (29, 1.1, 0.3, 9), "limonka": (30, 0.7, 0.2, 11),
    "sok z cytryny": (22, 0.4, 0.2, 7), "truskawki": (32, 0.7, 0.3, 7.7),
    "borówki": (57, 0.7, 0.3, 14), "jabłko": (52, 0.3, 0.2, 14),
    "kiwi": (61, 1.1, 0.5, 15), "mieszanka warzyw stir-fry": (35, 2, 0.3, 6),
    "por": (61, 1.5, 0.3, 14),
    # --- sypkie, makarony, pieczywo
    "makaron": (371, 13, 1.5, 75), "makaron penne": (371, 13, 1.5, 75),
    "makaron spaghetti": (371, 13, 1.5, 75), "makaron rigatoni": (371, 13, 1.5, 75),
    "makaron fettuccine": (371, 13, 1.5, 75), "makaron orzo": (371, 13, 1.5, 75),
    "makaron udon": (130, 4, 0.5, 27), "ryż": (360, 7, 0.7, 79),
    "ryż jaśminowy": (360, 7, 0.7, 79), "ryż parboiled": (360, 7, 0.7, 79),
    "gnocchi": (170, 4, 1, 35), "płatki owsiane": (379, 13, 7, 67),
    "mąka": (364, 10, 1, 76), "mąka chlebowa": (364, 12, 1, 72),
    "mąka tortowa": (364, 8, 1, 78), "ryż basmati": (360, 7, 0.7, 79), "skrobia ziemniaczana": (330, 0.1, 0.1, 83),
    "skrobia kukurydziana": (381, 0.3, 0.1, 91), "panierka panko": (395, 13, 2.5, 78),
    "bułka tarta": (395, 13, 2.5, 78), "płatki kukurydziane": (357, 7, 0.4, 84),
    "chleb": (265, 9, 3.2, 49), "bułka": (280, 9, 3.5, 50), "pita": (275, 9, 1.2, 55),
    "tortilla": (310, 8, 8, 50), "tortilla mała": (310, 8, 8, 50),
    "ciasto francuskie": (395, 5.6, 24.5, 38), "ciasto do pizzy": (257, 7, 4.5, 47),
    "mięso mielone z piersi kurczaka": (110, 23, 1.8, 0), "nachosy": (490, 7, 25, 60),
    "frytki": (150, 2.4, 5.0, 24), "proszek do pieczenia": (53, 0, 0, 28),
    "drożdże instant": (325, 40, 7.6, 41), "soda oczyszczona": (0, 0, 0, 0),
    "nasiona chia": (486, 17, 31, 42), "soczewica": (353, 25, 1.1, 60),
    "ciecierzyca": (115, 7, 2.5, 16), "edamame": (121, 12, 5, 9),
    "pędy bambusa": (27, 2.6, 0.3, 5.2), "papier ryżowy": (330, 0.5, 0.1, 82),
    "nori": (306, 36, 2, 36), "cukier": (400, 0, 0, 100),
    "cukier brązowy": (380, 0, 0, 98), "erytrytol": (20, 0, 0, 5),
    "wanilia": (288, 0.1, 0.1, 13),
    # --- oleje, sosy, konserwy, slodycze
    "oliwa z oliwek": (884, 0, 100, 0), "olej roślinny": (884, 0, 100, 0),
    "olej sezamowy": (884, 0, 100, 0), "olej kokosowy": (862, 0, 100, 0),
    "olej chili": (884, 0, 100, 0), "olej z awokado": (884, 0, 100, 0),
    "spray do smażenia": (884, 0, 100, 0),
    "majonez": (680, 1, 75, 1.5), "ketchup": (112, 1.3, 0.2, 26),
    "musztarda": (130, 6, 7, 10.5), "sos sojowy": (53, 8, 0.1, 4.9),
    "sos sojowy jasny": (53, 8, 0.1, 4.9), "sos sojowy ciemny": (60, 6, 0.1, 9),
    "sos ostrygowy": (51, 2, 0.2, 11), "sos teriyaki": (89, 1.5, 0, 18),
    "sos BBQ": (172, 0.8, 0.5, 41), "sos ostry": (30, 1, 0.5, 5),
    "sriracha": (93, 1.9, 0.9, 19), "sos chipotle": (100, 1, 6, 10),
    "harissa": (130, 3, 9, 9), "gochujang": (220, 5, 1, 45),
    "pasta chili": (90, 2, 3, 13), "pasta z papryki": (90, 2, 3, 13),
    "pesto": (450, 5, 45, 6), "masło orzechowe": (588, 25, 50, 20),
    "ocet": (20, 0, 0, 0.9), "wino ryżowe": (130, 0.3, 0, 5),
    "oliwki": (145, 1, 15, 4), "kapary": (23, 2.4, 0.9, 4.9),
    "koncentrat pomidorowy": (100, 4.5, 0.5, 19), "passata pomidorowa": (35, 1.6, 0.2, 7),
    "pomidory z puszki": (32, 1.6, 0.3, 7), "suszone pomidory": (213, 5, 14, 17),
    "kukurydza konserwowa": (86, 3.2, 1.2, 19), "ogórki konserwowe": (12, 0.6, 0.2, 2.3),
    "relish ogórkowy": (130, 0.5, 0.5, 32), "pico de gallo": (25, 1, 0.2, 5),
    "chilli con carne": (130, 9, 6, 10), "bulion": (5, 0.6, 0.2, 0.4),
    "bulion w proszku": (200, 10, 5, 30), "miód": (304, 0.3, 0, 82),
    "syrop klonowy": (260, 0, 0, 67), "czekolada gorzka": (546, 8, 31, 61),
    "orzechy włoskie": (654, 15, 65, 14), "pestki słonecznika": (584, 21, 51, 20),
    "żurawina suszona": (308, 0.1, 1.4, 82), "odżywka białkowa": (380, 75, 5, 8),
    "sezam": (573, 18, 50, 23), "orzechy nerkowca": (553, 18, 44, 30),
    # --- przyprawy (male gramatury, ale liczymy uczciwie)
    "sól": (0, 0, 0, 0), "pieprz": (251, 10, 3.3, 64), "biały pieprz": (296, 10, 2.1, 69), "pieprz ziołowy": (270, 10, 4, 60),
    "papryka słodka": (282, 14, 13, 54), "papryka wędzona": (282, 14, 13, 54),
    "papryka ostra": (282, 14, 13, 54), "papryka mielona": (282, 14, 13, 54),
    "chili": (282, 14, 13, 54), "płatki chilli": (318, 12, 14, 57),
    "gochugaru": (318, 12, 14, 57), "pieprz cayenne": (318, 12, 17, 57),
    "czosnek granulowany": (331, 17, 0.7, 73), "cebula granulowana": (341, 10, 1, 79),
    "oregano": (265, 9, 4.3, 69), "zioła włoskie": (265, 9, 4.3, 69),
    "kumin": (375, 18, 22, 44), "kurkuma": (354, 8, 10, 65),
    "garam masala": (379, 15, 15, 45), "curry": (325, 14, 14, 56),
    "cynamon": (247, 4, 1.2, 81), "gałka muszkatołowa": (525, 6, 36, 49),
    "majeranek": (271, 13, 7, 60), "tymianek": (276, 9, 7, 64),
    "rozmaryn": (331, 5, 15, 64), "lubczyk": (275, 12, 7, 55),
    "sumak": (300, 4, 15, 60), "pieprz cytrynowy": (300, 10, 5, 55),
    "pieprz czosnkowy": (300, 10, 5, 55), "przyprawa cajun": (250, 10, 8, 40),
    "przyprawa kebab": (250, 10, 8, 40), "przyprawa taco": (250, 10, 8, 40),
    "przyprawa gyros": (250, 10, 8, 40), "przyprawa do kurczaka": (250, 10, 8, 40),
    # --- napoje
    "woda": (0, 0, 0, 0), "woda gazowana": (0, 0, 0, 0), "wino": (83, 0.1, 0, 2.6), "wino białe": (82, 0.1, 0, 2.6),
    "piwo": (43, 0.5, 0, 3.6), "wódka": (231, 0, 0, 0),
}

# domyslna masa jednostki w gramach
# --- dopisane przy przepisach z Instagrama (poza kolekcja "food")
NUTR.update({
    "mięta": (44, 3.3, 0.7, 8.4), "groszek zielony": (81, 5.4, 0.4, 14),
    "parówki": (290, 11, 26, 2), "ricotta": (174, 11, 13, 3),
    "pecorino": (387, 26, 32, 0), "szynka": (145, 18, 8, 1),
    "szynka parmeńska": (250, 26, 16, 0), "ciabatta": (271, 9, 3, 51),
    "salami": (378, 21, 31, 2), "pepperoni": (494, 20, 44, 5),
    "anyż gwiazdkowy": (337, 18, 16, 50), "estragon": (295, 23, 7, 50),
    "kakao": (228, 20, 14, 58), "ocet jabłkowy": (22, 0, 0, 0.9),
    "ocet winny": (19, 0, 0, 0.6), "ocet ryżowy": (18, 0, 0, 0.5),
    "mleko kokosowe": (197, 2, 21, 3), "drożdże świeże": (105, 12, 2, 11),
    "ogórki kiszone": (12, 0.6, 0.2, 1.6), "kolendra ziarna": (298, 12, 18, 55),
    "fasola czerwona": (100, 7, 0.5, 14), "żółtko": (322, 16, 27, 3.6),
    "sos worcestershire": (78, 0, 0, 19), "nduja": (513, 14, 50, 2),
    "tajin": (50, 0, 0, 10), "sos pomidorowy": (35, 1.6, 0.2, 7),
    "chipotle w adobo": (80, 1.5, 4, 10), "kminek": (333, 20, 15, 50),
})

UNIT_G = {"g": 1, "kg": 1000, "dag": 10, "ml": 1, "l": 1000, "szt.": 100,
          "łyżka": 15, "łyżeczka": 5, "szklanka": 240, "ząbek": 5, "szczypta": 0.5,
          "plaster": 20, "główka": 400, "pęczek": 30, "garść": 25, "opak.": 200,
          "puszka": 400, "oz": 28, "lbs": 454}

# nadpisania dla konkretnych produktow (produkt, jednostka) -> gramy
GRAMS = {
    ("pierś z kurczaka", "szt."): 220, ("pstrąg", "szt."): 150, ("awokado", "szt."): 150, ("polędwiczki z kurczaka", "szt."): 60,
    ("łosoś", "szt."): 150, ("paluszki surimi", "szt."): 17,
    ("jajko", "szt."): 55, ("boczek", "plaster"): 25,
    ("ser żółty", "plaster"): 20, ("cheddar", "plaster"): 22,
    ("masło", "łyżka"): 14, ("masło", "plaster"): 10, ("masło", "szklanka"): 227,
    ("czosnek", "główka"): 40,
    ("cebula", "szt."): 100, ("czerwona cebula", "szt."): 100, ("szalotka", "szt."): 30,
    ("dymka", "szt."): 15, ("pomidor", "szt."): 120, ("papryka", "szt."): 150,
    ("papryka czerwona", "szt."): 150, ("papryka zielona", "szt."): 150,
    ("papryczka chili", "szt."): 15, ("ziemniaki", "szt."): 150,
    ("marchewka", "szt."): 70, ("ogórek", "szt."): 200, ("brokuł", "szt."): 400,
    ("cukinia", "szt."): 300, ("seler naciowy", "szt."): 40, ("awokado", "szt."): 150,
    ("cytryna", "szt."): 100, ("limonka", "szt."): 70, ("jabłko", "szt."): 180,
    ("kiwi", "szt."): 75, ("sałata", "główka"): 400, ("sałata lodowa", "główka"): 400,
    ("tortilla", "szt."): 60, ("tortilla mała", "szt."): 30, ("pita", "szt."): 60,
    ("bułka", "szt."): 60, ("nori", "szt."): 3, ("papier ryżowy", "szt."): 10,
    ("ciasto francuskie", "szt."): 275, ("ciasto do pizzy", "szt."): 400,
    ("mąka", "szklanka"): 120, ("mąka", "łyżka"): 8,
    ("płatki owsiane", "szklanka"): 90, ("panierka panko", "szklanka"): 60,
    ("płatki kukurydziane", "szklanka"): 30,
    ("ryż", "szklanka"): 185, ("soczewica", "szklanka"): 200,
    ("ciecierzyca", "szklanka"): 165, ("kukurydza konserwowa", "szklanka"): 165,
    ("parmezan", "szklanka"): 90, ("parmezan", "łyżka"): 6,
    ("mozzarella", "szklanka"): 110, ("cheddar", "szklanka"): 110,
    ("oliwki", "szklanka"): 135, ("pestki słonecznika", "szklanka"): 140,
    ("pomidorki koktajlowe", "szklanka"): 150, ("szpinak", "szklanka"): 30,
    ("truskawki", "szklanka"): 150, ("borówki", "szklanka"): 150,
    ("cukier", "łyżka"): 12, ("cukier", "łyżeczka"): 4, ("erytrytol", "łyżka"): 12,
    ("miód", "łyżka"): 21, ("miód", "łyżeczka"): 7, ("syrop klonowy", "łyżka"): 20,
    ("oliwa z oliwek", "łyżka"): 13, ("oliwa z oliwek", "łyżeczka"): 4.5,
    ("olej roślinny", "łyżka"): 13, ("olej sezamowy", "łyżka"): 13,
    ("olej chili", "łyżka"): 13, ("olej kokosowy", "łyżeczka"): 4.5,
    ("majonez", "łyżka"): 14, ("majonez", "szklanka"): 220,
    ("ketchup", "łyżka"): 17, ("sos sojowy", "łyżka"): 16,
    ("sos ostrygowy", "łyżka"): 18, ("sriracha", "łyżka"): 17,
    ("gochujang", "łyżka"): 20, ("chleb", "plaster"): 35, ("koncentrat pomidorowy", "łyżka"): 16,
    ("sezam", "łyżka"): 9, ("skrobia ziemniaczana", "łyżka"): 10,
    ("czekolada gorzka", "łyżka"): 15, ("nasiona chia", "łyżka"): 12,
    ("sól", "łyżeczka"): 6, ("proszek do pieczenia", "łyżeczka"): 4,
    ("natka pietruszki", "pęczek"): 30, ("kolendra", "pęczek"): 30,
    ("koperek", "pęczek"): 30, ("bazylia", "garść"): 15,
    ("orzechy włoskie", "garść"): 30, ("żurawina suszona", "garść"): 40,
    ("suszone pomidory", "garść"): 25, ("mix sałat", "opak."): 150,
    ("suszone pomidory", "opak."): 200, ("przyprawa taco", "opak."): 30,
    # male sztuki - bez tego "9 szt. suszonych pomidorow" liczylo sie jako 900 g
    ("suszone pomidory", "szt."): 5, ("oliwki", "szt."): 4,
    ("pomidorki koktajlowe", "szt."): 15, ("ogórki konserwowe", "szt."): 30,
    ("czosnek", "szt."): 40, ("dymka", "pęczek"): 60, ("szczypiorek", "pęczek"): 30,
}

# tluszcz do glebokiego smazenia - do jedzenia trafia tylko ulamek
GRAMS.update({
    ("parówki", "szt."): 50, ("ciabatta", "szt."): 250, ("chleb", "szt."): 500,
    ("mięta", "garść"): 8, ("bazylia", "garść"): 8, ("koperek", "garść"): 8,
    ("szynka", "plaster"): 15, ("szynka parmeńska", "plaster"): 12,
    ("pepperoni", "plaster"): 3, ("salami", "plaster"): 5,
    ("borówki", "szklanka"): 150, ("kakao", "łyżka"): 7,
    ("żółtko", "szt."): 17, ("ogórki kiszone", "szt."): 80, ("mleko kokosowe", "puszka"): 400,
    ("fasola czerwona", "puszka"): 240, ("bułka", "szt."): 60,
    ("chipotle w adobo", "szt."): 12,
    # szklanka to 240 ml, a nie 240 g - dla lekkich i gestych rzeczy trzeba osobno
    ("ricotta", "szklanka"): 250, ("pecorino", "szklanka"): 90,
    ("ser żółty", "szklanka"): 110, ("serek śmietankowy", "szklanka"): 230,
    ("sos pomidorowy", "szklanka"): 245, ("jogurt grecki", "szklanka"): 245,
    ("śmietana kwaśna", "szklanka"): 230, ("mleko", "szklanka"): 245,
    ("miód", "szklanka"): 340, ("syrop klonowy", "szklanka"): 320,
    ("olej roślinny", "szklanka"): 218, ("oliwa z oliwek", "szklanka"): 216,
    ("sałata", "szklanka"): 50, ("sałata lodowa", "szklanka"): 50,
    ("natka pietruszki", "szklanka"): 60, ("kolendra", "szklanka"): 60,
    ("ogórek", "szklanka"): 130, ("czerwona cebula", "szklanka"): 160,
    ("cebula", "szklanka"): 160, ("papryka czerwona", "szklanka"): 150,
    ("papryka zielona", "szklanka"): 150, ("makaron", "szklanka"): 100,
    ("skrobia kukurydziana", "szklanka"): 128, ("bułka tarta", "szklanka"): 108,
})

FRYING = {"olej roślinny", "olej z awokado", "oliwa z oliwek"}
FRY_MIN_G = 150      # powyzej tylu gramow to kapiel olejowa, nie dodatek do potrawy
FRY_ABSORB = 0.15    # tyle realnie zostaje w jedzeniu
# przyprawy sypkie: lyzeczka ~2.3 g, nie 5 g
SPICE_TSP = {"kminek", "pieprz", "papryka słodka", "papryka wędzona", "papryka ostra", "chili",
             "płatki chilli", "pieprz cayenne", "czosnek granulowany", "cebula granulowana",
             "oregano", "zioła włoskie", "kumin", "kurkuma", "garam masala", "curry",
             "cynamon", "gałka muszkatołowa", "majeranek", "tymianek", "rozmaryn",
             "lubczyk", "sumak", "pieprz cytrynowy", "pieprz czosnkowy", "biały pieprz",
             "przyprawa cajun", "przyprawa kebab", "przyprawa taco", "przyprawa gyros",
             "przyprawa do kurczaka", "papryka mielona", "gochugaru", "wanilia",
             "estragon", "anyż gwiazdkowy", "proszek do pieczenia", "kolendra ziarna", "tajin"}

# --- dopisane przy moich propozycjach (28.10.2026)
NUTR.update({
    "pasta chipotle": (160, 2, 10, 15), "mleko zagęszczone": (131, 6.6, 7.5, 9.5),
    "salsa": (36, 1.5, 0.2, 7), "białko jaja": (48, 10.9, 0.2, 0.7),
    "jalapeño": (29, 0.9, 0.4, 6.5), "przyprawa tandoori": (250, 10, 8, 40),
    "ziele angielskie": (263, 6, 8.7, 72), "fasola czarna": (91, 6, 0.5, 12),
    "ser topiony": (280, 13, 23, 5), "pasta curry": (300, 4, 25, 15),
    "maślanka": (38, 3.4, 0.5, 4.8), "sok pomarańczowy": (45, 0.7, 0.2, 10.4),
})
GRAMS.update({
    ("cynamon", "szt."): 3, ("jalapeño", "szt."): 20, ("ser topiony", "plaster"): 20,
    ("białko jaja", "szt."): 33, ("fasola czarna", "puszka"): 250,
})
SPICE_TSP |= {"przyprawa tandoori", "ziele angielskie"}


def grams(name, unit, qty):
    """Masa skladnika w gramach."""
    if (name, unit) in GRAMS:
        return GRAMS[(name, unit)] * qty
    if unit == "łyżeczka" and name in SPICE_TSP:
        return 2.3 * qty
    if unit == "łyżka" and name in SPICE_TSP:
        return 7 * qty
    return UNIT_G.get(unit, 100) * qty


def macros(name, unit, qty):
    """(kcal, bialko, tluszcz, wegle) dla podanej ilosci. None gdy brak w tabeli."""
    n = NUTR.get(name)
    if not n:
        return None
    g_abs = grams(name, unit, qty)
    if name in FRYING and unit in ("g", "ml", "l") and g_abs >= FRY_MIN_G:
        g_abs *= FRY_ABSORB
    g = g_abs / 100.0
    return (n[0] * g, n[1] * g, n[2] * g, n[3] * g)
