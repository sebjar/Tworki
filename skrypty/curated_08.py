# -*- coding: utf-8 -*-
"""Recznie opracowane przepisy 84-88, 90-100."""
C = {}

C[84] = dict(
    name="Sos czosnkowy z jogurtem greckim", cat="Sos / dodatek", serv=4,
    ings=[(400, "g", "jogurt grecki"), (4, "ząbek", "czosnek"),
          (1, "łyżka", "sok z cytryny"), (1, "łyżeczka", "sól"),
          (0.5, "łyżeczka", "pieprz"), (1, "łyżka", "majonez")],
    steps=["Wybierz naczynie, które łatwo zamkniesz i schowasz do lodówki.",
           "Wyłóż do niego cały jogurt grecki.",
           "Przeciśnij 4 ząbki czosnku — jeśli lubisz ostrzej, daj więcej.",
           "Dodaj odrobinę soku z cytryny, sól i pieprz.",
           "Wmieszaj łyżkę majonezu (możesz pominąć).",
           "Wymieszaj i wstaw do lodówki na 10 min."])

C[85] = dict(
    name="Chrupiące tacos z wołowiną", cat="Obiad", serv=2,
    ings=[(250, "g", "mięso mielone wołowe"), (1.5, "szt.", "cebula"),
          (1, "łyżka", "koncentrat pomidorowy"), (0.5, "łyżeczka", "kumin"),
          (0.5, "łyżeczka", "papryka wędzona"), (0.5, "łyżeczka", "papryka słodka"),
          (0.5, "łyżeczka", "płatki chilli"), (1, "łyżeczka", "czosnek granulowany"),
          (1, "łyżeczka", "sól"), (1, "łyżeczka", "pieprz"), (160, "ml", "woda"),
          (2, "szt.", "pomidor"), (1, "pęczek", "kolendra"), (0.5, "szt.", "cytryna"),
          (0.5, "szklanka", "majonez"), (2, "łyżka", "ketchup"),
          (1, "łyżeczka", "musztarda"), (1, "łyżka", "ogórki konserwowe"),
          (4, "szt.", "tortilla")],
    steps=["Podsmaż drobno posiekaną cebulę, dodaj mięso mielone i smaż, aż się zarumieni.",
           "Dodaj koncentrat pomidorowy, kumin, obie papryki, płatki chilli, czosnek granulowany, sól i pieprz.",
           "Wlej wodę i duś, aż płyn odparuje, a farsz zgęstnieje.",
           "Salsa: wymieszaj pokrojoną cebulę, pomidory, posiekaną kolendrę, sok z połowy cytryny, sól i pieprz.",
           "Sos: połącz majonez, ketchup, musztardę, drobno posiekaną cebulę i ogórek konserwowy oraz paprykę wędzoną.",
           "Nałóż farsz na tortille i podsmaż je na patelni na chrupiąco.",
           "Podawaj z salsą i sosem."])

C[86] = dict(
    name="Szaszłyki kebabowe z tortilli", cat="Obiad", serv=8,
    note="Autor nie podał liczby porcji — 1,36 kg mięsa i 10 tortilli podzieliłem na 8. Wychodzi 361 g i ok. 900 kcal na osobę, bo w sosie siedzi 230 g masła. To danie na imprezę, nie na codzienny obiad.",
    ings=[(1360, "g", "mięso mielone wołowe"), (2.5, "szt.", "cebula"),
          (1, "szt.", "papryka czerwona"), (10, "ząbek", "czosnek"),
          (0.5, "szklanka", "natka pietruszki"), (1, "łyżka", "kumin"),
          (4, "łyżka", "papryka słodka"), (2, "łyżka", "kolendra mielona"),
          (1, "łyżka", "czosnek granulowany"), (2, "łyżeczka", "pieprz"),
          (1.5, "łyżka", "sól"), (10, "szt.", "tortilla"), (230, "g", "masło"),
          (0.5, "szklanka", "jogurt grecki")],
    steps=["Wymieszaj mieloną wołowinę z posiekaną cebulą, papryką, czosnkiem, pietruszką, kuminem, papryką słodką, kolendrą, czosnkiem granulowanym, pieprzem i solą.",
           "Rozsmaruj masę na 10 przyciętych na kwadrat dużych tortillach.",
           "Ułóż po 5 tortilli jedna na drugiej, przykrywając stos od góry i od dołu czystą tortillą (wychodzą 2 stosy).",
           "Potnij stosy na paski szerokości ok. 2,5 cm, obróć na bok i nadziej na szpadki.",
           "Potnij pomiędzy szpadkami.",
           "Grilluj na naoliwionej patelni żeliwnej po kilka minut na stronę, obracając 4 razy.",
           "Sos: podgrzej masło z jogurtem lub labneh, posiekaną cebulą, pietruszką, czosnkiem, papryką i solą.",
           "Podawaj szaszłyki polane sosem albo z sosem do maczania."])

C[87] = dict(
    name="Kremowy makaron z kurczakiem i parmezanem", cat="Obiad", serv=10,
    note="Dokopałem się do pełnego przepisu na stronie autorki "
         "(goldengracekitchen.com/chicken-garlic-parmesan-pasta) — gramatury i kroki są "
         "już jej, nie moje. Ten sam przepis wrzuciła na Instagram dwa razy: "
         "reel C90rG0NP0-y i reel C2QsND3Pp5B, oba prowadzą do tego samego wpisu. "
         "Ćwierć szklanki wody z gotowania makaronu nie jest na liście zakupów.",
    ings=[(2, "łyżka", "oliwa z oliwek"), (680, "g", "pierś z kurczaka"),
          (1.5, "łyżeczka", "papryka słodka"), (1.5, "łyżeczka", "oregano"),
          (2, "łyżeczka", "czosnek granulowany"), (0.5, "łyżeczka", "tymianek"),
          (0.5, "łyżeczka", "pieprz"), (1, "łyżeczka", "sól"),
          (340, "g", "makaron"), (4, "łyżka", "masło"),
          (2, "łyżeczka", "szalotka"), (2, "łyżeczka", "zioła włoskie"),
          (120, "ml", "bulion"), (2, "łyżka", "mąka"),
          (3, "szklanka", "śmietana kremówka"), (340, "g", "parmezan")],
    steps=["Ugotuj makaron al dente według instrukcji na opakowaniu.",
           "Wymieszaj przyprawy do kurczaka: paprykę, oregano, czosnek granulowany, "
           "tymianek, sól i pieprz.",
           "Rozbij pierś tłuczkiem, żeby była trochę cieńsza, i obtocz ją przyprawami "
           "z obu stron.",
           "Na dużej patelni rozgrzej oliwę na średnim ogniu i obsmaż kurczaka "
           "po 5 minut z każdej strony.",
           "Zmniejsz ogień, przykryj patelnię i duś jeszcze 10-12 minut, aż mięso "
           "osiągnie 74°C w środku. Wyjmij je na deskę.",
           "Na tę samą patelnię wrzuć masło. Gdy się rozpuści, dodaj szalotkę, czosnek "
           "granulowany i zioła włoskie i smaż minutę.",
           "Wsyp mąkę i wymieszaj, zeskrobując osad z dna patelni.",
           "Wlej bulion i śmietanę kremówkę i ubijaj trzepaczką na gładki sos.",
           "Wsyp parmezan i mieszaj, aż się rozpuści. Gotuj, aż sos zgęstnieje.",
           "Wrzuć makaron i wymieszaj. Jeśli sos jest za gęsty, rozrzedź go wodą "
           "z gotowania makaronu, dolewając po łyżce.",
           "Pokrój kurczaka w plastry, dodaj do makaronu, delikatnie wymieszaj i podawaj."])

C[88] = dict(
    name="Sałatka z kurczakiem i sosem miodowo-musztardowym", cat="Sałatka", serv=2,
    ings=[(150, "g", "sałata"), (1, "szt.", "papryka"), (9, "szt.", "suszone pomidory"),
          (150, "g", "ser feta"), (1, "garść", "żurawina suszona"),
          (140, "g", "kukurydza konserwowa"), (250, "g", "pierś z kurczaka"),
          (0.5, "szklanka", "pestki słonecznika"), (1.5, "łyżka", "miód"),
          (2, "łyżeczka", "musztarda"), (2, "łyżka", "sok z cytryny")],
    steps=["Upraż pestki słonecznika na suchej patelni.",
           "Usmaż pierś z kurczaka i pokrój ją w paski.",
           "Do miski wsyp mix sałat, dodaj paprykę pokrojoną w kostkę i pokrojone suszone pomidory.",
           "Dorzuć fetę w kostce, suszoną żurawinę i odsączoną kukurydzę.",
           "Sos: wymieszaj miód, musztardę i sok z cytryny. Możesz wlać trochę oliwy z suszonych pomidorów.",
           "Połóż kurczaka i pestki na wierzchu, polej sosem."])

C[90] = dict(
    name="Tikka masala z ryżem", cat="Obiad", serv=4,
    note="Autor podaje sam sos z kurczakiem i pisze „podawaj z ryżem lub naanem”. "
         "Dopisałem 240 g suchego ryżu, czyli 60 g na osobę — bez tego kalorie "
         "i węglowodany w kolumnach L-O pokazywałyby sam sos. Jeśli wolisz naan, "
         "podmień ten jeden wiersz w Składnikach.",
    ings=[(800, "g", "pierś z kurczaka"), (250, "g", "jogurt grecki"),
          (1.5, "łyżeczka", "sól"), (3, "łyżeczka", "garam masala"),
          (1, "łyżeczka", "papryka wędzona"), (0.5, "łyżeczka", "kurkuma"),
          (7, "ząbek", "czosnek"), (2, "łyżeczka", "imbir"),
          (2, "łyżka", "olej roślinny"), (30, "g", "masło"), (1, "szt.", "cebula"),
          (1, "łyżeczka", "papryka słodka"), (1, "łyżeczka", "kurkuma"),
          (1, "łyżeczka", "chili"), (400, "g", "pomidory z puszki"),
          (200, "ml", "śmietana kremówka"), (240, "g", "ryż")],
    steps=["Marynata: wymieszaj pokrojone mięso z jogurtem greckim, solą, garam masalą, papryką wędzoną, kurkumą, czosnkiem i startym imbirem. Odstaw.",
           "Obsmaż zamarynowane mięso na mocno rozgrzanej patelni, aż się przypiecze. Odłóż.",
           "Na oleju z masłem zeszklij posiekaną dużą cebulę.",
           "Dodaj czosnek i starty imbir, smaż chwilę.",
           "Wsyp garam masalę, słodką paprykę, kurkumę i chili, praż kilkanaście sekund.",
           "Wlej puszkę pomidorów i duś, aż sos zgęstnieje. Możesz go zblendować na gładko.",
           "Dodaj mięso i śmietanę kremówkę, zagotuj delikatnie.",
           "Ugotuj ryż i podawaj z nim sos. Zamiast ryżu może być naan."])

C[91] = dict(
    name="One-pan kremowy makaron z pesto", cat="Obiad", serv=2,
    note="Autor nie podał gramatur — ilości to moje oszacowanie na 2 porcje.",
    ings=[(200, "g", "makaron fettuccine"), (250, "g", "pomidorki koktajlowe"),
          (100, "g", "szpinak"), (1, "garść", "bazylia"), (3, "ząbek", "czosnek"),
          (200, "ml", "śmietanka"), (400, "ml", "bulion"), (3, "łyżka", "pesto"),
          (1, "łyżeczka", "zioła włoskie"), (1, "łyżeczka", "sól"),
          (1, "łyżeczka", "pieprz"), (0.5, "łyżeczka", "płatki chilli")],
    steps=["Ułóż wszystkie składniki warstwami na jednej patelni: makaron, pomidorki, szpinak, bazylię i czosnek.",
           "Dopraw ziołami włoskimi, solą, pieprzem i płatkami chilli.",
           "Wlej śmietankę owsianą i bulion warzywny.",
           "Gotuj pod przykryciem, aż makaron będzie miękki, a płyn się zredukuje.",
           "Wmieszaj zielone pesto, aż powstanie jedwabisty, kremowy sos.",
           "Wymieszaj i podawaj od razu."])

C[92] = dict(
    name="Pudding chia", cat="Deser", serv=1,
    ings=[(35, "g", "nasiona chia"), (125, "ml", "mleko"), (1, "łyżka", "erytrytol"),
          (0.5, "łyżeczka", "wanilia"), (1, "szt.", "kiwi")],
    steps=["Podgrzej mleko z erytrytolem i wanilią, aż cukier się rozpuści.",
           "Zalej nim nasiona chia i wymieszaj.",
           "Odczekaj 15 minut i wymieszaj jeszcze raz — inaczej nasiona się zbiją.",
           "Odstaw na noc do lodówki.",
           "Podawaj z kiwi albo innym owocem. Porcja ma ok. 14 g błonnika."])

C[93] = dict(
    name="Zupa ziemniaczana z boczkiem i cheddarem", cat="Zupa", serv=4,
    ings=[(4, "plaster", "boczek"), (2, "łyżka", "masło"), (1, "szt.", "cebula"),
          (2, "szt.", "seler naciowy"), (2, "łyżka", "mąka"), (1, "l", "bulion"),
          (250, "ml", "mleko"), (250, "ml", "śmietana kremówka"),
          (800, "g", "ziemniaki"), (1, "łyżeczka", "papryka słodka"),
          (1, "łyżeczka", "bulion w proszku"), (1, "łyżeczka", "sól"),
          (1, "łyżeczka", "pieprz"), (200, "g", "cheddar"), (2, "szt.", "dymka"),
          (100, "g", "śmietana kwaśna")],
    steps=["Pokrój boczek w kostkę i wysmaż na chrupiąco. Odłóż część na posypkę.",
           "Na tłuszczu rozpuść masło i podsmaż drobno posiekaną cebulę oraz seler naciowy.",
           "Wsyp mąkę i smaż minutę, cały czas mieszając.",
           "Stopniowo wlewaj bulion drobiowy, mleko i śmietanę kremówkę, mieszając do gładkości.",
           "Dodaj obrane ziemniaki pokrojone w kostkę 1 cm, paprykę i bulion w proszku.",
           "Gotuj, aż ziemniaki zmiękną. Dopraw solą i pieprzem.",
           "Wmieszaj startego cheddara, aż się rozpuści.",
           "Podawaj z dymką, śmietaną kwaśną, dodatkowym serem i chrupiącym boczkiem."])

C[94] = dict(
    name="Zapiekanka z gnocchi", cat="Obiad", serv=4,
    ings=[(800, "g", "gnocchi"), (400, "g", "pomidory z puszki"),
          (200, "g", "mozzarella"), (50, "g", "parmezan"),
          (0.33, "łyżeczka", "sól"), (0.33, "łyżeczka", "pieprz"),
          (1, "garść", "bazylia")],
    steps=["Rozgrzej piekarnik do 200°C.",
           "Wymieszaj gotowe gnocchi (lub kopytka) z pomidorami z puszki albo przecierem.",
           "Dopraw solą i pieprzem, dodaj świeżą bazylię.",
           "Przełóż do naczynia żaroodpornego.",
           "Rozłóż na wierzchu mozzarellę i posyp startym parmezanem lub pecorino.",
           "Zapiekaj, aż ser się rozpuści i zarumieni."])

C[95] = dict(
    name="Ceviche z krewetek", cat="Przekąska", serv=4,
    note="Autor nie podał gramatur — ilości to moje oszacowanie na 4 porcje.",
    ings=[(500, "g", "krewetki"), (1, "szt.", "czerwona cebula"),
          (1, "pęczek", "kolendra"), (2, "szt.", "dymka"),
          (1, "szt.", "papryczka chili"), (2, "szt.", "pomidor"), (1, "szt.", "ogórek"),
          (4, "szt.", "limonka"), (1, "łyżeczka", "sól"), (1, "łyżka", "sos ostry")],
    steps=["Krewetki krótko sparz we wrzątku, a potem zalej sokiem z limonki (możesz też zostawić surowe i pozwolić limonce zamarynować je do końca).",
           "Pokrój drobno czerwoną cebulę, kolendrę, białą część dymki, papryczkę serrano, pomidora i ogórka.",
           "Połącz warzywa z krewetkami.",
           "Dopraw sokiem z limonki, solą i sosem ostrym do smaku.",
           "Wstaw do lodówki na co najmniej 30 min przed podaniem."])

C[96] = dict(
    name="Kurczak teriyaki", cat="Obiad", serv=4,
    ings=[(1200, "g", "pierś z kurczaka"), (300, "g", "sos teriyaki"),
          (2, "łyżka", "oliwa z oliwek"), (2, "łyżka", "sezam"),
          (1, "garść", "szczypiorek"), (300, "g", "ryż jaśminowy"),
          (400, "g", "brokuł")],
    steps=["Przygotuj sos teriyaki albo użyj gotowego ze sklepu.",
           "Upraż sezam na suchej patelni, aż zacznie pachnieć.",
           "Pokrój mięso w paski lub kostkę.",
           "Rozgrzej oliwę i obsmaż kurczaka, aż się zarumieni i będzie gotowy.",
           "Wlej sos teriyaki i smaż, aż zgęstnieje i oblepi mięso.",
           "Dodaj siekany szczypiorek i uprażony sezam.",
           "Podawaj z ryżem jaśminowym lub brązowym i gotowanymi brokułami."])

# C[97] - usuniete na prosbe uzytkownika
C[98] = dict(
    name="Sałatka Big Mac", cat="Sałatka", serv=2,
    note="Zapisany przez Ciebie film z 2023 r. zniknął z TikToka — przepis i zdjęcia są z nowszej "
         "wersji tego samego autora („FIT Sałatka BIG MAC”, styczeń 2025). Autor nie podał porcji; "
         "przyjmuję 2, jak w starej wersji. Autor używa chudej wołowiny i majonezu light — w kcal "
         "liczę zwykłe; wersja light to jego przepis, tylko z cheddarem light. Sosu wychodzi ok. 260 g, a autor "
         "polewa „wedle uznania”; liczę cały — z połową sosu porcja ma ok. 240 kcal mniej. Wędzoną "
         "paprykę autor dodaje do sosu tylko na nagraniu, bez ilości. Stara wersja (2 porcje): "
         "150 g wołowiny, 60 g cheddara, po 3 łyżki majonezu i ketchupu, łyżka wody z ogórków, "
         "sól, pieprz, cayenne, suszony czosnek i cebula.",
    ings=[(200, "g", "mięso mielone wołowe"), (1, "łyżka", "olej"),
          (0.5, "łyżeczka", "sól"), (0.5, "łyżeczka", "pieprz"),
          (0.5, "główka", "sałata lodowa"), (0.5, "szt.", "czerwona cebula"),
          (3, "szt.", "ogórki konserwowe"), (30, "g", "cheddar"), (1, "łyżeczka", "sezam"),
          (120, "g", "majonez"), (80, "g", "ketchup"), (25, "g", "musztarda angielska"),
          (15, "ml", "sos worcestershire"), (0.25, "łyżeczka", "cebula granulowana"),
          (0.25, "łyżeczka", "czosnek granulowany"), (0.25, "łyżeczka", "papryka wędzona")],
    steps=["Na patelni z odrobiną oleju podsmaż mieloną wołowinę, dopraw solą i pieprzem.",
           "Sos burgerowy: wymieszaj majonez, ketchup, musztardę angielską, 20 ml wody z ogórków konserwowych, sos worcestershire, cebulę w proszku, czosnek granulowany i szczyptę wędzonej papryki.",
           "Posiekaj sałatę lodową, pokrój czerwoną cebulę i ogórki konserwowe, zetrzyj cheddar.",
           "Na sałatę wyłóż cebulę, ogórki, cheddar i wołowinę.",
           "Polej sosem według uznania i posyp sezamem."])

C[99] = dict(
    name="Grecki bowl z udkiem kurczaka", cat="Obiad", serv=3,
    note="Autor nie podał, na ile porcji to jest. Przy dwóch wychodziło 871 g i 1329 kcal na miskę — to nie jest jedna porcja. Przy trzech wychodzi 581 g i 886 kcal, czyli normalna miska. Ilość ryżu też jest moja — w opisie jest samo „ryż”, bez gramatury.",
    ings=[(500, "g", "udka z kurczaka"), (4, "ząbek", "czosnek"),
          (1, "łyżeczka", "papryka słodka"), (1, "łyżeczka", "oregano"),
          (1, "łyżeczka", "sól"), (1, "łyżeczka", "pieprz"),
          (30, "ml", "oliwa z oliwek"), (1, "szt.", "cytryna"),
          (150, "g", "jogurt grecki"), (1.25, "szt.", "ogórek"),
          (1, "pęczek", "koperek"), (200, "g", "pomidorki koktajlowe"),
          (1, "szt.", "cebula"), (50, "g", "oliwki"), (100, "g", "ser feta"),
          (200, "g", "ryż")],
    steps=["Zamarynuj mięso z udek lub filet z czosnkiem, papryką słodką, oregano, solą, pieprzem, oliwą i sokiem z połowy cytryny.",
           "Tzatziki: zetrzyj i odciśnij ćwiartkę ogórka, wymieszaj z jogurtem greckim, koperkiem, sokiem z ćwiartki cytryny, oliwą, czosnkiem, solą i pieprzem.",
           "Sałatka: pokrój pomidorki, ogórek i cebulę, wymieszaj z oliwkami, oliwą, solą i pieprzem. Dodaj pokruszoną fetę.",
           "Ugotuj ryż.",
           "Usmaż lub upiecz zamarynowane mięso.",
           "Złóż bowl: ryż, mięso, sałatka i tzatziki."])

C[100] = dict(
    name="Mac and cheese z kurczakiem", cat="Obiad", serv=2,
    note="Ten sam przepis autor wrzucił i na TikToka, i na Instagram (https://www.instagram.com/coocharz/reel/CsdWz7qI0og/) — składniki są identyczne, więc zostawiłem jeden wiersz.",
    ings=[(220, "g", "makaron"), (650, "ml", "mleko"), (130, "g", "gouda"),
          (20, "g", "ser żółty"), (250, "g", "pierś z kurczaka"),
          (60, "g", "suszone pomidory"), (1, "garść", "natka pietruszki"),
          (1, "łyżeczka", "sól"), (1, "łyżeczka", "pieprz"),
          (0.5, "łyżeczka", "pieprz cayenne"), (1, "łyżeczka", "papryka wędzona"),
          (1, "łyżeczka", "czosnek granulowany")],
    steps=["Pokrój pierś z kurczaka w kostkę i dopraw solą, pieprzem, cayenne, papryką wędzoną i czosnkiem granulowanym.",
           "Obsmaż mięso na patelni i odłóż.",
           "Na tę samą patelnię wlej mleko i zagotuj.",
           "Wsyp suchy makaron i gotuj w mleku, mieszając, aż zmięknie, a mleko zgęstnieje.",
           "Dodaj starte sery i mieszaj, aż powstanie gładki, serowy sos.",
           "Wrzuć pokrojone suszone pomidory i kurczaka.",
           "Posyp natką pietruszki i podawaj."])
