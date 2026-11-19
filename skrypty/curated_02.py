# -*- coding: utf-8 -*-
"""Recznie opracowane przepisy 19-26."""
C = {}

C[19] = dict(
    name="Sajgonki z mięsem mielonym", cat="Przekąska", serv=12,
    note="Porcja to JEDNA sajgonka — tak liczy autor („jedna sajgonka posiada 103 kcal”). Dlatego kategoria to przekąska, a nie obiad: przy planowaniu wpisz sobie 3-4 porcje na osobę.",
    ings=[(500, "g", "mięso mielone wieprzowe"), (12, "szt.", "papier ryżowy"),
          (1, "szt.", "marchewka"), (1, "szt.", "cebula"), (5, "ząbek", "czosnek"),
          (25, "g", "natka pietruszki"), (20, "g", "szczypiorek"),
          (20, "ml", "sos sojowy"), (10, "g", "oliwa z oliwek"), (6, "g", "imbir"),
          (7, "g", "papryka słodka"), (3, "szczypta", "sól"), (3, "szczypta", "pieprz")],
    steps=["Cebulę i imbir pokrój w drobną kostkę, czosnek w plastry, marchew zetrzyj na tarce. Posiekaj szczypiorek i pietruszkę.",
           "Podsmaż cebulę na rozgrzanej patelni z połową oliwy przez 5-6 min.",
           "Dodaj marchew i smaż 2-3 min.",
           "Dodaj mięso mielone i smaż, aż się zarumieni.",
           "Wrzuć szczypiorek, pietruszkę, imbir, czosnek, sos sojowy i przyprawy.",
           "Smaż jeszcze 2-3 min, co jakiś czas mieszając. Odstaw farsz do przestudzenia.",
           "Namoczony płat papieru ryżowego połóż na desce, nałóż farsz i zawiń w rulonik.",
           "Podsmaż sajgonki na patelni na reszcie oliwy, aż będą chrupiące. Podawaj z sosem słodko-kwaśnym."])

C[20] = dict(
    name="Wrapy a'la cezar do lunchboxa", cat="Obiad", serv=4,
    note="Autor pisze „Składniki na 4 szt wrapów” i osobno „całość na 1 wrapa wynosi 598 kcal” — to jest makro ZA JEDNEGO wrapa, nie za cały przepis. Porcja = jeden wrap.",
    ings=[(4, "szt.", "tortilla"), (500, "g", "pierś z kurczaka"),
          (250, "g", "sałata"), (140, "g", "kukurydza konserwowa"),
          (7, "g", "papryka słodka"), (2, "szczypta", "pieprz"), (2, "szczypta", "sól"),
          (10, "g", "oliwa z oliwek"), (150, "g", "majonez"), (20, "g", "musztarda"),
          (80, "g", "parmezan"), (10, "ml", "sok z limonki")],
    steps=["Kurczaka pokrój w kostkę, dopraw papryką słodką, solą i pieprzem, wymieszaj.",
           "Podsmaż mięso na rozgrzanej patelni z oliwą przez 6-8 min, co jakiś czas mieszając.",
           "Sałatę rzymską obmyj, osusz i poszatkuj.",
           "Wymieszaj sos: majonez, musztarda, starty parmezan, sok z limonki, sól i pieprz.",
           "W dużej misce połącz kurczaka, sałatę, odsączoną kukurydzę i sos.",
           "Na każdą tortillę nałóż 1/4 farszu, zawiń i podpiecz na patelni z obu stron.",
           "Na wynos: najlepiej złożyć tuż przed jedzeniem, żeby tortilla nie zmiękła."])

C[21] = dict(
    name="Kremowy makaron z kurczakiem i brązowym masłem", cat="Obiad", serv=4,
    note="Autor nie podał gramatur — ilości to moje oszacowanie na 4 porcje na podstawie nagrania.",
    ings=[(2, "szt.", "pierś z kurczaka"), (3, "łyżka", "masło"),
          (1, "szt.", "papryka czerwona"), (4, "ząbek", "czosnek"),
          (1.5, "szklanka", "śmietana kremówka"), (1, "łyżeczka", "papryka wędzona"),
          (1, "łyżeczka", "czosnek granulowany"), (250, "g", "makaron"),
          (1, "łyżeczka", "sól"), (1, "łyżeczka", "pieprz")],
    steps=["Zamarynuj i usmaż filety z kurczaka, po czym odłóż je na bok.",
           "Na tej samej patelni rozpuść masło i pozwól mu się zrumienić na orzechowo.",
           "Podsmaż pokrojoną paprykę i posiekany czosnek.",
           "Wlej śmietanę kremówkę, dopraw papryką wędzoną i czosnkiem granulowanym.",
           "W czasie gdy sos gęstnieje, ugotuj makaron w osolonej wodzie al dente.",
           "Wymieszaj makaron z sosem i podawaj z pokrojonym kurczakiem na wierzchu."])

C[22] = dict(
    name="Grecka sałatka z kurczakiem i kremowym sosem", cat="Sałatka", serv=2,
    note="Autor: „Serving Size: 2” i 347 kcal na porcję, licząc jogurt grecki 0%.",
    ings=[(300, "g", "pierś z kurczaka"), (1, "łyżeczka", "oliwa z oliwek"),
          (1, "łyżeczka", "sól"), (1, "łyżeczka", "pieprz"),
          (1, "łyżeczka", "papryka słodka"), (1, "łyżeczka", "czosnek granulowany"),
          (1, "łyżeczka", "oregano"), (0.75, "szklanka", "jogurt grecki"),
          (2, "łyżka", "sos ostry"), (1, "łyżka", "czosnek"), (0.5, "szt.", "cytryna"),
          (0.5, "łyżeczka", "koperek"), (2, "łyżka", "woda"), (250, "g", "sałata"),
          (1, "szklanka", "pomidorki koktajlowe"), (1, "szklanka", "ogórek"),
          (1, "szt.", "czerwona cebula"), (0.25, "szklanka", "oliwki"),
          (2, "łyżka", "ser feta")],
    steps=["Dopraw piersi solą, pieprzem, papryką, czosnkiem granulowanym i oregano. Skrop oliwą.",
           "Usmaż lub upiecz kurczaka, odstaw na chwilę i pokrój.",
           "Sos: wymieszaj jogurt grecki, sos ostry, przeciśnięty czosnek, sok i skórkę z połowy cytryny, koperek, sól i pieprz. Rozrzedź wodą do konsystencji dressingu.",
           "Poszatkuj sałatę rzymską, pokrój pomidorki, ogórki i czerwoną cebulę.",
           "Wymieszaj warzywa z kurczakiem, dodaj oliwki i pokruszoną fetę.",
           "Polej sosem tuż przed podaniem. Do lunchboxa trzymaj sos osobno.",
           "Opcjonalnie posyp płatkami chilli dla ostrości."])

C[23] = dict(
    name="Lody twarogowe o smaku sernika z borówkami", cat="Deser", serv=3,
    note="Autor: „Serving Size: 3” i 225 kcal na porcję — liczy na syropie klonowym bez cukru.",
    ings=[(450, "g", "serek wiejski"), (3, "łyżka", "serek śmietankowy"),
          (0.25, "szklanka", "syrop klonowy"), (30, "g", "odżywka białkowa"),
          (0.25, "łyżeczka", "sól"), (1, "szklanka", "borówki"), (1, "łyżeczka", "miód")],
    steps=["Wrzuć do blendera serek wiejski, serek śmietankowy, syrop klonowy, odżywkę białkową i sól. Zblenduj na całkiem gładko.",
           "Borówki z miodem przełóż do rondelka i gotuj na średnim ogniu, aż zrobi się dżem.",
           "Do słoika lub pojemnika wlej połowę masy serowej, na to połowę dżemu. Powtórz, żeby wyszły dwie warstwy.",
           "Widelcem lub nożem zawiruj dżem w masie, żeby smak rozłożył się równo.",
           "Zamroź na 3 godziny i podawaj.",
           "Im tłustszy serek wiejski, tym mniej masa zmarznie na kamień."])

C[24] = dict(
    name="Kurczak teriyaki stir fry", cat="Obiad", serv=2,
    note="Autor pisze „Makes: 2 servings” i podaje 650 kcal na porcję — bez ryżu i bez orzechów nerkowca (u niego opcjonalnych); bez nich wychodzi u mnie 633 kcal, czyli tyle samo. Ryżu nie podał, dopisałem 200 g suchego, czyli 100 g na porcję.",
    ings=[(550, "g", "pierś z kurczaka"), (16, "g", "skrobia kukurydziana"),
          (1, "łyżeczka", "sól"), (1, "łyżeczka", "pieprz"),
          (15, "ml", "olej roślinny"), (120, "g", "papryka czerwona"),
          (100, "g", "brokuł"), (70, "g", "marchewka"), (60, "g", "cebula"),
          (2, "szt.", "dymka"), (70, "g", "orzechy nerkowca"),
          (60, "ml", "sos sojowy"), (45, "ml", "woda"), (30, "g", "miód"),
          (15, "ml", "ocet"), (15, "ml", "olej sezamowy"), (2, "ząbek", "czosnek"),
          (1, "łyżeczka", "imbir"), (200, "g", "ryż jaśminowy"), (1, "łyżka", "sezam")],
    steps=["Pokrój kurczaka w cienkie paski, dopraw solą i pieprzem, obtocz w łyżce skrobi.",
           "Wymieszaj sos: sos sojowy, zimna woda, miód, ocet ryżowy, olej sezamowy, przeciśnięty czosnek, starty imbir i druga łyżka skrobi.",
           "Rozgrzej olej na patelni lub w woku na dużym ogniu i usmaż kurczaka na złoto. Zdejmij z patelni.",
           "Na tej samej patelni podsmaż paprykę, brokuł, marchew i cebulę — mają zostać jędrne.",
           "Wróć z kurczakiem na patelnię, wlej sos i smaż, aż zgęstnieje i oblepi składniki.",
           "Dorzuć nerkowce i posiekaną dymkę.",
           "Podawaj na ryżu jaśminowym, posypane sezamem i dodatkową dymką."])

C[25] = dict(
    name="Burger bowl", cat="Obiad", serv=2,
    ings=[(400, "g", "mięso mielone wołowe"), (2, "plaster", "ser żółty"),
          (400, "g", "frytki"), (0.33, "główka", "sałata lodowa"), (1, "szt.", "pomidor"),
          (4, "szt.", "ogórki konserwowe"), (1, "łyżka", "sezam"),
          (0.5, "łyżeczka", "sól"), (0.5, "łyżeczka", "pieprz"),
          (0.5, "łyżeczka", "czosnek granulowany"), (0.5, "łyżeczka", "papryka słodka"),
          (2, "łyżka", "ketchup"), (1, "łyżeczka", "musztarda"), (2, "łyżka", "majonez"),
          (0.5, "łyżeczka", "miód"), (1, "szczypta", "papryka ostra")],
    steps=["Wstaw frytki do piekarnika i piecz według opakowania.",
           "Mięso mielone wrzuć na suchą, rozgrzaną patelnię razem z przyprawami.",
           "Wymieszaj sos: ketchup, musztarda, majonez, miód i szczypta ostrej papryki.",
           "Mięso na patelni rozdziel na dwie części, lekko dociśnij i połóż na każdej plaster sera. Zostaw na ok. 3 min, aż ser się rozpuści.",
           "W tym czasie poszatkuj sałatę, pokrój pomidora i ogórki konserwowe.",
           "Składaj bowl: sałata, frytki, mięso z serem, pomidor, ogórki.",
           "Polej sosem i posyp sezamem."])

C[26] = dict(
    name="Owsianka nocna czekoladowo-truskawkowa", cat="Śniadanie", serv=1,
    ings=[(0.5, "szklanka", "jogurt grecki"), (0.33, "szklanka", "płatki owsiane"),
          (0.25, "szklanka", "mleko"), (1, "łyżeczka", "miód"),
          (30, "g", "odżywka białkowa"), (0.5, "szklanka", "truskawki"),
          (1, "łyżka", "czekolada gorzka"), (1, "łyżeczka", "olej kokosowy")],
    steps=["Do słoika (min. 450 ml) wsyp jogurt grecki, płatki owsiane, mleko, miód, odżywkę białkową i pokrojone truskawki — wszystko poza czekoladą — i dokładnie wymieszaj.",
           "Czekoladę i olej kokosowy wrzuć do miseczki i podgrzej w mikrofali 30-45 sekund, mieszając do rozpuszczenia. Możesz też rozpuścić w kąpieli wodnej.",
           "Wylej cienką warstwę roztopionej czekolady na wierzch owsianki.",
           "Zakręć szczelnie i wstaw do lodówki na 3-4 godziny albo na całą noc."])
