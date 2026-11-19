# -*- coding: utf-8 -*-
"""Recznie opracowane przepisy 70-76, 78-83."""
C = {}

C[70] = dict(
    name="Ziemniaczane talarki z sosem koperkowym", cat="Przekąska", serv=4,
    ings=[(500, "g", "ziemniaki"), (3, "łyżka", "oliwa z oliwek"), (100, "g", "parmezan"),
          (1, "łyżeczka", "papryka słodka"), (0.5, "łyżeczka", "papryka ostra"),
          (1, "łyżeczka", "czosnek granulowany"), (1, "łyżeczka", "pieprz"),
          (1, "łyżeczka", "sól"), (3, "łyżka", "jogurt naturalny"),
          (1, "łyżka", "majonez"), (1, "łyżeczka", "koperek")],
    steps=["Ziemniaki pokrój na plastry.",
           "Włóż je na ok. 20 min do lodowatej wody, a potem osusz na ręczniku papierowym.",
           "Wymieszaj z ulubionymi przyprawami (bez soli — dodasz ją po upieczeniu), oliwą i startym parmezanem.",
           "Wyłóż płasko na blaszce tak, żeby talarki się nie dotykały.",
           "Piecz ok. 20 min w 200°C (góra-dół z termoobiegiem).",
           "Sos: wymieszaj jogurt z majonezem, koperkiem, solą i pieprzem.",
           "Upieczone talarki posól i podawaj z sosem."])

C[71] = dict(
    name="Sałatka z chrupiącym gnocchi", cat="Sałatka", serv=3,
    note="Autor nie podał gramatur — ilości to moje oszacowanie na 3 porcje.",
    ings=[(500, "g", "gnocchi"), (1, "główka", "sałata"), (1, "szt.", "ogórek"),
          (1, "szt.", "czerwona cebula"), (3, "łyżka", "oliwa z oliwek"),
          (1, "łyżeczka", "czosnek granulowany"), (1, "łyżeczka", "papryka słodka"),
          (1, "łyżeczka", "sól"), (1, "łyżeczka", "pieprz"), (1, "łyżeczka", "oregano"),
          (150, "g", "jogurt naturalny"), (100, "g", "śmietana kwaśna"),
          (1, "łyżka", "sok z cytryny"), (1, "pęczek", "koperek")],
    steps=["Wymieszaj surowe gnocchi z oliwą i wszystkimi przyprawami.",
           "Piecz w airfryerze w 200°C przez ok. 22 min, aż będą chrupiące.",
           "Pokrój sałatę rzymską, ogórka i czerwoną cebulę, przełóż do miski.",
           "Dressing: wymieszaj jogurt, śmietanę kwaśną, sok z cytryny, czosnek granulowany, sól z chili, pieprz i świeży koperek.",
           "Wymieszaj sałatę z dressingiem.",
           "Na wierzch wyłóż gorące, chrupiące gnocchi i podawaj od razu — ciepłe kontra zimne."])

C[72] = dict(
    name="Gnocchi z kurczakiem w sosie szpinakowo-gorgonzolowym", cat="Obiad", serv=4,
    ings=[(500, "g", "gnocchi"), (500, "g", "pierś z kurczaka"), (3, "ząbek", "czosnek"),
          (1, "szt.", "cebula"), (50, "g", "suszone pomidory"),
          (225, "g", "szpinak mrożony"), (150, "g", "brokuł"), (60, "g", "gorgonzola"),
          (200, "ml", "śmietana 12%"), (1, "łyżka", "oliwa z oliwek"),
          (1, "łyżeczka", "sól"), (1, "łyżeczka", "pieprz")],
    steps=["Pokrój kurczaka w kostkę i obsmaż na oliwie na złoto. Dopraw solą i pieprzem.",
           "Dodaj posiekaną cebulę i czosnek, smaż do zeszklenia.",
           "Wrzuć mrożony szpinak i poczekaj, aż się rozmrozi i odparuje.",
           "Dodaj różyczki brokuła i pokrojone suszone pomidory.",
           "Wlej śmietanę 12% i wkrusz gorgonzolę. Mieszaj, aż ser się rozpuści i powstanie kremowy sos.",
           "Ugotuj gnocchi według opakowania, odcedź i wrzuć na patelnię.",
           "Wymieszaj i rozłóż na 4 porcje."])

C[73] = dict(
    name="Arayes z kurczakiem", cat="Obiad", serv=6,
    ings=[(1, "szt.", "cebula"), (2, "ząbek", "czosnek"), (1, "szt.", "papryczka chili"),
          (1, "pęczek", "natka pietruszki"), (600, "g", "mięso mielone z piersi kurczaka"),
          (30, "g", "harissa"), (1, "łyżeczka", "sól"), (1, "łyżeczka", "pieprz"),
          (1, "łyżeczka", "sumak"), (1, "łyżka", "papryka wędzona"),
          (1, "łyżeczka", "kumin"), (3, "szt.", "pita")],
    steps=["Do blendera wrzuć cebulę, czosnek, papryczkę chilli i natkę pietruszki. Zblenduj.",
           "Dodaj zmiksowane warzywa do mielonej piersi z kurczaka razem z pastą harissa i przyprawami.",
           "Wyrabiaj, aż składniki się połączą.",
           "Pity natnij i przekrój na pół, a potem nafaszeruj masą mięsną.",
           "Podsmaż pity na patelni mięsem do dołu.",
           "Przełóż do piekarnika i piecz 20 min w 200°C."])

C[74] = dict(
    name="Sałatka z chrupiącym ryżem i kurczakiem gochujang", cat="Sałatka", serv=4,
    ings=[(150, "g", "ryż"), (1, "łyżka", "olej chili"), (2, "łyżka", "sos sojowy"),
          (3, "szt.", "ogórek"), (1, "szt.", "awokado"), (200, "g", "edamame"),
          (3, "szt.", "dymka"), (400, "g", "pierś z kurczaka"),
          (1, "łyżka", "gochujang"), (2, "ząbek", "czosnek"),
          (1, "łyżeczka", "papryka wędzona"), (25, "g", "masło orzechowe"),
          (1, "łyżka", "syrop klonowy"), (1, "szt.", "limonka")],
    steps=["Do ugotowanego ryżu dodaj olej chilli i łyżkę sosu sojowego, wymieszaj.",
           "Rozłóż ryż na blasze i piecz 15 min w 200°C, aż będzie chrupiący.",
           "Kurczaka dopraw pastą gochujang, czosnkiem, papryką wędzoną i ciemnym sosem sojowym, a potem upiecz w airfryerze.",
           "W międzyczasie pokrój ogórki, awokado i dymkę.",
           "Dressing: wymieszaj masło orzechowe, sos sojowy, syrop klonowy, przeciśnięty czosnek, sok z limonki i wodę do rozrzedzenia.",
           "Połącz warzywa, edamame, kurczaka i chrupiący ryż, polej dressingiem."])

C[75] = dict(
    name="Tacos z mięsem mielonym i cheddarem", cat="Obiad", serv=4,
    ings=[(500, "g", "mięso mielone wołowe"), (12, "szt.", "tortilla mała"),
          (8, "szt.", "ogórki konserwowe"), (1, "główka", "sałata lodowa"),
          (12, "plaster", "cheddar"), (1, "łyżeczka", "sól"), (1, "łyżeczka", "pieprz"),
          (5, "łyżka", "ketchup"), (2, "łyżka", "majonez"), (1, "szt.", "cebula")],
    steps=["Na placek tortilli wyłóż cienką warstwę mięsa mielonego.",
           "Posól i podsmaż na patelni stroną z mięsem do dołu, na złoty kolor.",
           "Przewróć na drugą stronę i połóż plaster cheddara. Podsmaż 2-3 min.",
           "Sos: wymieszaj ketchup, majonez, posiekaną cebulę i 2 posiekane ogórki konserwowe.",
           "Na środek placka wyłóż odrobinę sosu, posiekaną sałatę i plastry ogórków konserwowych.",
           "Dodaj jeszcze trochę sosu i złóż tortillę na pół."])

C[76] = dict(
    name="Chrupiący kurczak w panko z piekarnika", cat="Obiad", serv=2,
    note="Autor podaje tylko 2 łyżki oleju i „ulubione przyprawy” — wpisałem paprykę i czosnek granulowany, a ilości panko, parmezanu i mąki oszacowałem.",
    ings=[(2, "szt.", "pierś z kurczaka"), (2, "łyżka", "olej roślinny"),
          (100, "g", "panierka panko"), (40, "g", "parmezan"),
          (1, "łyżeczka", "papryka słodka"), (1, "łyżeczka", "czosnek granulowany"),
          (1, "łyżeczka", "sól"), (1, "łyżeczka", "pieprz"),
          (50, "g", "mąka"), (1, "szt.", "jajko")],
    steps=["Na patelnię wlej 2 łyżki oleju i rozgrzej.",
           "Wrzuć panierkę panko, starty parmezan i ulubione przyprawy.",
           "Praż przez ok. 2 min, cały czas mieszając, aż panierka się zarumieni.",
           "Pierś z kurczaka rozkrój na pół i rozbij tłuczkiem tak, żeby była cieniutka.",
           "Filet maczaj kolejno w mące, jajku i uprażonej panierce. Obsyp dokładnie i dociśnij z góry, potem przewróć na drugą stronę.",
           "Rozgrzej piekarnik do 220°C i włóż blaszkę z kurczakiem. Nie dodawaj już oleju.",
           "Piecz 10 min, przewróć na drugą stronę i piecz kolejne 10 min."])

C[78] = dict(
    name="Kremowy makaron cajun z kurczakiem", cat="Obiad", serv=3,
    ings=[(170, "g", "makaron"), (400, "g", "pierś z kurczaka"),
          (2, "łyżeczka", "oliwa z oliwek"), (1, "szt.", "limonka"),
          (3, "łyżka", "przyprawa cajun"), (0.5, "łyżeczka", "sól"),
          (0.5, "łyżeczka", "pieprz"), (1, "łyżka", "czosnek"), (1, "szt.", "cebula"),
          (1, "szt.", "papryka czerwona"), (1, "szklanka", "mleko"),
          (2, "łyżka", "serek śmietankowy"), (2, "łyżka", "koncentrat pomidorowy"),
          (0.5, "szklanka", "mozzarella"), (1, "łyżeczka", "płatki chilli")],
    steps=["Ugotuj makaron w osolonej wodzie. Zachowaj 1/3 szklanki wody z gotowania.",
           "Pokrój kurczaka, dopraw przyprawą cajun, solą, pieprzem i czosnkiem, skrop oliwą i sokiem z limonki.",
           "Usmaż mięso na patelni i odłóż.",
           "Na tej samej patelni podsmaż cebulę i paprykę pokrojone w paski.",
           "Wlej mleko, dodaj serek śmietankowy, koncentrat pomidorowy i przyprawę cajun. Mieszaj do gładkości.",
           "Wsyp mozzarellę i mieszaj, aż się rozpuści. Rozrzedź wodą z gotowania makaronu.",
           "Dodaj makaron i kurczaka, wymieszaj. Posyp płatkami chilli."])

C[79] = dict(
    name="Grecki bowl z kurczakiem i tzatzikami", cat="Obiad", serv=4,
    ings=[(500, "g", "pierś z kurczaka"), (450, "g", "jogurt grecki"),
          (1, "szt.", "cytryna"), (5, "ząbek", "czosnek"), (1, "łyżeczka", "oregano"),
          (2, "łyżeczka", "papryka słodka"), (1, "łyżeczka", "papryka ostra"),
          (1.5, "łyżeczka", "pieprz"), (2, "łyżeczka", "sól"),
          (2, "łyżka", "oliwa z oliwek"), (1.5, "szt.", "ogórek"),
          (1, "pęczek", "koperek"), (500, "g", "ziemniaki"),
          (1, "łyżeczka", "rozmaryn")],
    steps=["Kurczaka wymieszaj z jogurtem greckim, sokiem z połowy cytryny, czosnkiem, oregano, papryką słodką, pieprzem, solą i oliwą.",
           "Odstaw na minimum 30 min, najlepiej na całą noc.",
           "Ziemniaki pokrój, wymieszaj z oliwą, obiema paprykami, oregano, rozmarynem, solą i pieprzem.",
           "Piecz ziemniaki w 210°C (góra-dół), aż będą miękkie i przypieczone.",
           "Tzatziki: ogórki zetrzyj na tarce i mocno odciśnij z wody.",
           "Wymieszaj je z jogurtem greckim, czosnkiem, sokiem z połowy cytryny, świeżym koperkiem, solą i pieprzem.",
           "Kurczaka upiecz lub usmaż, pokrój i złóż bowl z ziemniakami i tzatzikami."])

C[80] = dict(
    name="Sałatka z chrupiącą ciecierzycą", cat="Sałatka", serv=2,
    note="Autorka bierze ciecierzycę ze słoika 400 g — po odsączeniu zostaje ok. 240 g. Podaje ~920 kcal za całą miskę, czyli ok. 460 kcal na porcję.",
    ings=[(240, "g", "ciecierzyca"), (1, "łyżeczka", "papryka wędzona"),
          (1, "łyżeczka", "kumin"), (1, "łyżeczka", "czosnek granulowany"),
          (3, "szt.", "ogórek"), (0.5, "szt.", "czerwona cebula"), (1, "garść", "sałata"),
          (1, "garść", "suszone pomidory"), (100, "g", "ser feta"),
          (1, "pęczek", "koperek"), (200, "g", "skyr"), (1, "łyżeczka", "musztarda"),
          (2, "ząbek", "czosnek"), (1, "szt.", "limonka"), (1, "łyżeczka", "miód"),
          (1, "łyżeczka", "płatki chilli"), (1, "łyżeczka", "sól"),
          (1, "łyżeczka", "pieprz")],
    steps=["Ciecierzycę opłucz i dokładnie osusz.",
           "Przypraw papryką wędzoną, kminem rzymskim i czosnkiem, a potem piecz 20 min w 200°C, aż będzie chrupiąca.",
           "Ogórki pokrój, posól i odstaw na kilka minut, żeby puściły wodę.",
           "Pokrój czerwoną cebulę, sałatę i suszone pomidory.",
           "Dressing: wymieszaj skyr, musztardę, przeciśnięty czosnek, sok z limonki, miód, koperek, płatki chilli, sól i pieprz.",
           "Połącz warzywa z pokruszoną fetą i chrupiącą ciecierzycą, polej dressingiem."])

C[81] = dict(
    name="Beyti kebab — szaszłyki z wrapa", cat="Obiad", serv=4,
    ings=[(500, "g", "mięso mielone wołowe"), (1, "szt.", "cebula"),
          (2, "łyżeczka", "papryka słodka"), (1, "łyżeczka", "sól"),
          (1, "łyżeczka", "pieprz"), (1.5, "łyżeczka", "czosnek granulowany"),
          (1, "łyżka", "koncentrat pomidorowy"), (1, "pęczek", "natka pietruszki"),
          (4, "szt.", "tortilla"), (150, "g", "mozzarella"), (30, "g", "masło"),
          (0.5, "łyżeczka", "płatki chilli"), (3, "łyżka", "jogurt naturalny")],
    steps=["Wymieszaj mięso mielone z drobno posiekaną cebulą, papryką, solą, pieprzem, czosnkiem granulowanym, koncentratem pomidorowym i świeżymi ziołami.",
           "Rozsmaruj masę na tortillach.",
           "Posyp startą mozzarellą.",
           "Zwiń ciasno w rulon i potnij na kawałki.",
           "Nadziej kawałki na drewniane patyczki.",
           "Piecz w 200°C przez 30-35 min.",
           "Masło paprykowe: rozpuść masło z papryką, płatkami chilli, solą i ziołami. Polej upieczone szaszłyki.",
           "Dip czosnkowy: wymieszaj jogurt z czosnkiem granulowanym, solą, pieprzem i ziołami."])

C[82] = dict(
    name="Domowe nuggetsy", cat="Obiad", serv=3,
    ings=[(400, "g", "mięso mielone z kurczaka"), (1, "łyżeczka", "czosnek granulowany"),
          (1, "łyżeczka", "papryka słodka"), (1, "łyżeczka", "sól"),
          (0.5, "łyżeczka", "pieprz"), (0.5, "łyżeczka", "przyprawa do kurczaka"),
          (1, "szklanka", "mąka"), (4, "łyżka", "skrobia ziemniaczana"),
          (0.5, "łyżeczka", "papryka ostra"), (400, "ml", "olej roślinny"),
          (4, "łyżka", "majonez"), (4, "łyżka", "śmietana"), (1, "szczypta", "cukier")],
    steps=["Wymieszaj mielone mięso z kurczaka z czosnkiem, papryką słodką, solą, pieprzem i przyprawą do kurczaka — po ok. pół łyżeczki każdego.",
           "Uformuj nuggetsy. Mięso może wydawać się luźne, ale tak ma być.",
           "Panierka: wymieszaj mąkę ze skrobią ziemniaczaną, czosnkiem, ostrą papryką i solą.",
           "Obtocz nuggetsy w suchej mieszance i odłóż na bok.",
           "Do pozostałej mąki stopniowo dolewaj wodę, mieszając, aż powstanie ciasto o konsystencji bardzo gęstego ciasta naleśnikowego.",
           "Obtocz mięso w cieście i smażyj na rozgrzanym oleju po 2-3 min z każdej strony.",
           "Sos: wymieszaj majonez, śmietanę, szczyptę cukru, sól i pieprz."])

C[83] = dict(
    name="Sałatka sylwestrowa z kurczakiem i orzo", cat="Sałatka", serv=4,
    note="Autorka podaje 200 g UGOTOWANEGO orzo — to ok. 90 g suchego makaronu.",
    ings=[(400, "g", "pierś z kurczaka"), (1, "łyżka", "przyprawa do kurczaka"),
          (90, "g", "makaron orzo"), (30, "g", "olej roślinny"),
          (100, "g", "roszponka"), (1, "szt.", "czerwona cebula"),
          (1, "szt.", "marchewka"), (4, "łyżka", "kukurydza konserwowa"),
          (5, "łyżka", "majonez"), (5, "łyżka", "śmietana 18%"),
          (1, "łyżeczka", "pieprz czosnkowy"), (1, "łyżeczka", "pieprz cytrynowy"),
          (1, "łyżeczka", "lubczyk"), (1, "szczypta", "sól")],
    steps=["Podsmaż podwójny filet z kurczaka z przyprawą do kurczaka na rozgrzanym oleju. Ostudź i pokrój.",
           "Ugotuj makaron orzo i odcedź.",
           "Do miski wsyp roszponkę, dodaj makaron orzo i mięso.",
           "Dorzuć startą na grubych oczkach marchewkę, czerwoną cebulę w kostce i odsączoną kukurydzę.",
           "Sos: wymieszaj majonez, śmietanę 18%, pieprz czosnkowy, pieprz cytrynowy, lubczyk i sól.",
           "Połącz wszystko z sosem tuż przed podaniem."])
