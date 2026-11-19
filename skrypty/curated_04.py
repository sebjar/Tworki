# -*- coding: utf-8 -*-
"""Recznie opracowane przepisy 34-35, 37-44, 89."""
C = {}

C[34] = dict(
    name="Popcorn chicken w ostro-miodowej glazurze", cat="Obiad", serv=4,
    ings=[(800, "g", "pierś z kurczaka"), (2, "łyżeczka", "czosnek granulowany"),
          (1, "łyżeczka", "cebula granulowana"), (2, "łyżeczka", "papryka słodka"),
          (1, "łyżeczka", "pieprz cayenne"), (2, "łyżeczka", "sól"),
          (2, "łyżeczka", "pieprz"), (1, "szt.", "jajko"),
          (60, "g", "skrobia kukurydziana"), (900, "g", "ziemniaki"),
          (1, "łyżeczka", "oregano"), (60, "g", "sriracha"), (60, "g", "miód"),
          (1, "łyżka", "szczypiorek")],
    steps=["Pokrój pierś w niewielkie kawałki. Dopraw czosnkiem i cebulą granulowaną, papryką, cayenne, solą i pieprzem.",
           "Wbij jajko, wymieszaj, a potem obtocz kawałki w skrobi kukurydzianej.",
           "Spryskaj olejem. Airfryer 200°C przez 10-12 min lub piekarnik 220°C przez 15-18 min.",
           "Ziemniaki pokrój w kostkę i wymieszaj z czosnkiem granulowanym, oregano, papryką, cayenne, solą i pieprzem. Spryskaj olejem.",
           "Airfryer 190°C przez 25-30 min lub piekarnik 200°C przez 30-35 min.",
           "Wymieszaj sriracha z miodem na ostro-miodowy sos.",
           "Polej gotowego kurczaka sosem, posyp szczypiorkiem i podawaj z ziemniakami."])

C[35] = dict(
    name="Owsianka nocna o smaku szarlotki", cat="Śniadanie", serv=1,
    note="Ilości podane na 1 słoik. Autor pisze „Yields: 4 servings”, bo nadzienie jabłkowe robi od razu na 4 słoiki — tutaj jest przeliczone na jeden, żeby makra zgadzały się z porcją. Autor podaje 327 kcal, u mnie wychodzi więcej, bo używa syropu klonowego zero kcal („low calorie maple syrup”), a ja liczę zwykły.",
    ings=[(0.33, "szklanka", "płatki owsiane"), (0.25, "szklanka", "mleko"),
          (0.5, "szklanka", "jogurt grecki"), (1, "łyżka", "syrop klonowy"),
          (30, "g", "odżywka białkowa"), (0.5, "łyżeczka", "cynamon"),
          (0.5, "szt.", "jabłko"), (0.125, "szklanka", "woda"),
          (1, "łyżka", "syrop klonowy"), (0.25, "łyżka", "cynamon"),
          (0.25, "łyżka", "sok z cytryny"), (0.25, "łyżeczka", "skrobia kukurydziana")],
    steps=["Do słoika wsyp płatki owsiane, wlej mleko i jogurt grecki, dodaj słodzik, odżywkę białkową i cynamon. Wymieszaj.",
           "Nadzienie: pokrój jabłka w kostkę i wrzuć do rondelka z wodą, syropem, cynamonem i sokiem z cytryny.",
           "Gotuj na średnim ogniu, aż jabłka zmiękną, a płyn zgęstnieje. Skrobia przyspieszy gęstnienie.",
           "Ostudź nadzienie i nałóż na owsiankę.",
           "Wstaw do lodówki na noc."])

C[37] = dict(
    name="Łosoś w ostro-miodowym sosie (meal prep)", cat="Obiad", serv=3,
    ings=[(500, "g", "łosoś"), (1, "łyżeczka", "oliwa z oliwek"),
          (1, "łyżeczka", "sól"), (1, "łyżeczka", "pieprz"),
          (1, "łyżeczka", "papryka słodka"), (1, "łyżeczka", "chili"),
          (2, "łyżka", "sos sojowy jasny"), (1, "łyżka", "miód"),
          (1, "łyżka", "sos ostry"), (1, "szt.", "cytryna"),
          (2, "łyżeczka", "czosnek"), (1, "łyżka", "ocet"),
          (0.5, "łyżeczka", "płatki chilli")],
    steps=["Osusz łososia ze skórą, skrop oliwą i obsyp solą, pieprzem, papryką i chili z każdej strony.",
           "Sos: wymieszaj jasny sos sojowy, miód, sos ostry, sok z całej cytryny, przeciśnięty czosnek i ocet. Opcjonalnie dodaj płatki chilli.",
           "Upiecz łososia w piekarniku (ok. 200°C, 12-15 min) albo usmaż na patelni.",
           "Podgrzej sos, aż lekko zgęstnieje. Dla szybszego efektu dodaj szczyptę mąki lub skrobi przed gotowaniem.",
           "Polej rybę sosem.",
           "Podawaj z ryżem i groszkiem albo z ziemniakami i szparagami. Posyp sezamem i dymką."])

C[38] = dict(
    name="Carbonara", cat="Obiad", serv=2,
    ings=[(1, "szt.", "jajko"), (2, "szt.", "żółtko"), (100, "g", "boczek"), (300, "g", "makaron spaghetti"),
          (100, "g", "grana padano"), (1, "łyżeczka", "pieprz"), (1, "szczypta", "sól")],
    steps=["Pokrój boczek w drobną kostkę — tak jak na jajecznicę.",
           "Smaż go na średnim ogniu, aż zrobią się z niego skwarki.",
           "Do miski wbij 1 całe jajko i 2 żółtka. Zetrzyj do tego grana padano (oryginalnie powinno być pecorino).",
           "Wsyp dużo świeżo mielonego pieprzu i dokładnie wymieszaj masę.",
           "Ugotuj spaghetti al dente — świeży makaron ok. 5 min, suchy według opakowania.",
           "Zdejmij patelnię z ognia, wrzuć odcedzony makaron do skwarek i wymieszaj.",
           "Dodaj masę jajeczną poza ogniem, energicznie mieszając i podlewając wodą z gotowania, aż zrobi się kremowy sos. Nie dopuść do ścięcia jajka.",
           "Podawaj od razu z dodatkowym serem i pieprzem."])

C[39] = dict(
    name="Sushi burger z surimi", cat="Obiad", serv=2,
    note="Autor nie podał gramatur — ilości to moje oszacowanie na 2 porcje. Ryż liczony jako suchy (do kupienia), po ugotowaniu wyjdzie go ok. 2,5 raza więcej.",
    ings=[(3, "szt.", "nori"), (120, "g", "ryż"), (8, "szt.", "paluszki surimi"),
          (1, "szt.", "ogórek"), (1, "szt.", "marchewka"), (1, "szt.", "awokado"),
          (1, "garść", "kiełki"), (100, "g", "serek śmietankowy"),
          (1, "szt.", "jajko"), (100, "g", "panierka panko"),
          (400, "ml", "olej roślinny")],
    steps=["Na płacie nori ułóż warstwę ryżu, na to serek kanapkowy, ogórek i marchewkę w słupkach oraz paluszki surimi.",
           "Na wierzch daj pastę z awokado, kiełki i jeszcze jedną warstwę ryżu.",
           "Zawiń całość, przykryj drugim płatem nori i zawiń w folię spożywczą.",
           "Odłóż do lodówki na minimum pół godziny, żeby burger się zestalił.",
           "Obtocz w rozbitym jajku, a potem w panko.",
           "Smaż na dobrze rozgrzanym oleju, aż panierka będzie złota i chrupiąca."])

C[40] = dict(
    name="Makaron w kremowym sosie z boczkiem", cat="Obiad", serv=2,
    note="„4 plasterki boczku” — polski boczek w plastrach to ok. 15 g na plaster, razem ok. 60 g.",
    ings=[(180, "g", "makaron"), (60, "g", "boczek"), (2, "łyżka", "oliwa z oliwek"),
          (1, "szt.", "czerwona cebula"), (3, "ząbek", "czosnek"),
          (50, "g", "suszone pomidory"), (2, "łyżka", "koncentrat pomidorowy"),
          (1, "łyżeczka", "oregano"), (1, "łyżeczka", "papryka słodka"),
          (150, "ml", "śmietana kremówka"), (1, "łyżeczka", "cukier"),
          (1, "łyżeczka", "sól"), (1, "łyżeczka", "pieprz"),
          (1, "garść", "bazylia"), (60, "g", "parmezan")],
    steps=["Usmaż boczek na chrupiący i odłóż go na bok.",
           "Na tej samej patelni na oliwie zeszklij czerwoną cebulę, dodaj czosnek i suszone pomidory, chwilę podsmaż.",
           "Dodaj koncentrat pomidorowy i przyprawy, smaż ok. minutę.",
           "Zalej śmietanką 30%, dopraw solą, pieprzem i cukrem, zagotuj. Podlej wodą z gotowania makaronu.",
           "Wrzuć do sosu chrupiący boczek, świeżo starty parmezan i bazylię.",
           "Dodaj ugotowany makaron, wymieszaj i podawaj."])

C[41] = dict(
    name="Łosoś w sosie teriyaki", cat="Obiad", serv=2,
    ings=[(250, "g", "łosoś"), (2, "łyżka", "olej roślinny"),
          (3, "łyżka", "sos sojowy jasny"), (1, "łyżka", "sos sojowy ciemny"),
          (4, "łyżka", "miód"), (3, "łyżka", "sok z cytryny"), (15, "g", "imbir"),
          (2, "ząbek", "czosnek"), (1, "łyżeczka", "sezam"),
          (0.5, "łyżeczka", "płatki chilli"), (1, "łyżeczka", "olej sezamowy"),
          (1, "łyżeczka", "sól"), (1, "łyżeczka", "pieprz")],
    steps=["Łososia ze skórą pokrój na mniejsze kawałki i dopraw solą oraz pieprzem z obu stron.",
           "Na rozgrzany olej ułóż rybę skórą do dołu, lekko dociśnij i chwilę przytrzymaj. Smaż maksymalnie 2 min na stronę.",
           "Zdejmij rybę z patelni i zmniejsz moc palnika.",
           "Wlej jasny i ciemny sos sojowy, miód, sok z cytryny, opcjonalnie płatki chilli i zetrzyj imbir.",
           "Podgrzewaj na średnim ogniu do zagotowania, potem redukuj 2-3 min, aż sos zgęstnieje.",
           "Dodaj przeciśnięty czosnek, sezam i opcjonalnie olej sezamowy, mieszaj minutę.",
           "Zmniejsz ogień, włóż rybę, polej i obróć, żeby cała pokryła się glazurą.",
           "Podawaj na ryżu, skropione sosem, z sezamem i kolendrą."])

C[42] = dict(
    name="Popcorn chicken w sosie słodko-ostrym", cat="Przekąska", serv=2,
    note="Autor nie podał ilości kurczaka — przyjąłem 400 g na 2 porcje.",
    ings=[(400, "g", "pierś z kurczaka"), (1, "szt.", "jajko"),
          (0.33, "szklanka", "mąka"), (0.5, "łyżeczka", "sól"),
          (0.5, "łyżeczka", "pieprz"), (0.5, "łyżeczka", "oliwa z oliwek"),
          (2, "łyżka", "pasta z papryki"), (1, "łyżka", "miód"),
          (1, "łyżka", "sos sojowy jasny"), (1, "łyżka", "ocet")],
    steps=["Pokrój kurczaka na małe kawałki, dopraw solą i pieprzem.",
           "Obtocz w rozbitym jajku, a potem w mące.",
           "Skrop odrobiną oliwy — dzięki temu będzie chrupiący.",
           "Airfryer 200°C przez 12 min lub piekarnik 230°C przez 15 min, w połowie przewróć. Rozłóż kawałki luźno, żeby się nie sparzyły.",
           "Sos: wymieszaj pastę z czerwonej papryki, miód, jasny sos sojowy i ocet.",
           "Wymieszaj gorącego kurczaka z sosem i podawaj od razu."])

C[43] = dict(
    name="Sos czosnkowy jak z pizzerii", cat="Sos / dodatek", serv=4,
    ings=[(1, "łyżeczka", "bazylia"), (1, "łyżeczka", "oregano"),
          (2.5, "łyżka", "majonez"), (2, "łyżka", "jogurt naturalny"),
          (1, "ząbek", "czosnek"), (1, "szczypta", "sól"), (1, "szczypta", "cukier")],
    steps=["Do miseczki wsyp po płaskiej łyżeczce suszonej bazylii i oregano.",
           "Zalej je wrzątkiem — tylko tyle, żeby przykryło zioła. To jest cały sekret: zioła uwalniają wtedy aromat.",
           "Przykryj talerzykiem i zostaw na ok. 10 min, aż przestygnie.",
           "Dodaj majonez i jogurt naturalny, wymieszaj.",
           "Przeciśnij duży ząbek czosnku przez praskę i wmieszaj.",
           "Dopraw solą i cukrem do smaku. Proporcje możesz dowolnie zmieniać pod siebie."])

C[44] = dict(
    name="Burrito z kurczakiem chili-limonka", cat="Obiad", serv=2,
    note="Ten sam przepis masz zapisany dwa razy: u autora (@raziyyz) i jako repost @gymratrecipes — https://www.instagram.com/gymratrecipes/reel/CvXqNuyoO2d/ . Zostawiłem jeden wiersz. Repost podaje makra: 420 kcal, 44,5 g białka, 31,5 g węgli, 12,5 g tłuszczu na burrito.",
    ings=[(300, "g", "pierś z kurczaka"), (1, "łyżeczka", "oliwa z oliwek"),
          (0.5, "łyżeczka", "sól"), (0.5, "łyżeczka", "pieprz"),
          (0.75, "łyżeczka", "chili"), (0.5, "łyżeczka", "kumin"),
          (1, "łyżeczka", "papryka słodka"), (1.25, "łyżeczka", "czosnek granulowany"),
          (1, "szt.", "limonka"), (3, "łyżka", "majonez"), (1, "łyżka", "sos ostry"),
          (2, "szt.", "tortilla"), (0.25, "szklanka", "mozzarella"),
          (0.5, "szklanka", "sałata"), (1, "szt.", "pomidor"),
          (1, "szt.", "czerwona cebula")],
    steps=["Dopraw piersi solą, pieprzem, chili, kuminem, papryką i czosnkiem granulowanym. Skrop oliwą i sokiem z połowy limonki.",
           "Usmaż kurczaka i pokrój w paski.",
           "Sos: wymieszaj majonez, sos ostry, chili i czosnek granulowany oraz sok z drugiej połowy limonki.",
           "Na tortillę wyłóż ser, poszatkowaną sałatę, plastry pomidora i cebuli oraz kurczaka.",
           "Polej sosem i zawiń burrito.",
           "Podpiecz na suchej patelni z obu stron, aż tortilla będzie chrupiąca.",
           "Jeśli masz czas, zetrzyj skórkę z limonki do mięsa i do sosu — smak jest wtedy dużo lepszy."])

C[89] = dict(
    name="Rolgeski z ciasta francuskiego z bekonem i serem", cat="Przekąska", serv=12,
    note="Wychodzi 12 rulonów i porcja to jeden rulon — przy planowaniu wpisz 2-3 na osobę. 12 plastrów bekonu to typowe opakowanie ok. 180 g.",
    ings=[(1, "szt.", "ciasto francuskie"), (180, "g", "boczek"),
          (12, "plaster", "ser żółty")],
    steps=["Z ciasta francuskiego wytnij paski wielkości plastra bekonu.",
           "Na blacie ułóż plaster bekonu i przykryj go paskiem ciasta francuskiego.",
           "Na wierzch połóż przekrojony na pół plaster sera.",
           "Zwiń z tego rulony i nabij je na patyczki do szaszłyków.",
           "Ułóż na blaszce i piecz w 200°C przez ok. 20 min, aż się ładnie przypieką.",
           "Podawaj z ulubionym sosem."])
