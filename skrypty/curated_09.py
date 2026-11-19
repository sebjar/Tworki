# -*- coding: utf-8 -*-
"""Recznie opracowane przepisy 101-103, 105, 122, 124, 125."""
C = {}

C[101] = dict(
    name="Kebabowe kręciołki z tortilli", cat="Obiad", serv=4,
    note="Autor nie podał żadnych gramatur („ile chcesz”) — ilości to moje oszacowanie na 4 porcje.",
    ings=[(500, "g", "mięso mielone wołowe"), (1, "szt.", "papryka czerwona"),
          (1, "szt.", "papryka zielona"), (1, "pęczek", "natka pietruszki"),
          (1, "szt.", "cebula"), (3, "ząbek", "czosnek"),
          (1, "łyżeczka", "papryka wędzona"), (1, "łyżka", "przyprawa kebab"),
          (1, "łyżeczka", "papryka słodka"), (1, "łyżeczka", "sól"),
          (1, "łyżeczka", "pieprz"), (4, "szt.", "tortilla"),
          (2, "łyżka", "sos sojowy"), (1, "łyżka", "oliwa z oliwek"),
          (1, "łyżka", "miód")],
    steps=["Wymieszaj mięso mielone z drobno posiekaną papryką czerwoną i zieloną, natką, cebulą i czosnkiem.",
           "Dopraw papryką wędzoną, przyprawą kebab, papryką słodką, solą i pieprzem.",
           "Rozsmaruj masę na tortillach i zwiń w ciasne rulony.",
           "Potnij rulony na kawałki („kręciołki”).",
           "Glazura: wymieszaj sos sojowy, oliwę, miód i paprykę wędzoną.",
           "Posmaruj kręciołki glazurą.",
           "Piecz w piekarniku albo usmaż na patelni, aż będą rumiane i chrupiące."])

C[102] = dict(
    name="Żeberka w glazurze BBQ", cat="Obiad", serv=4,
    note="Podobne do „Żeberka pieczone w folii”. Autor nie podał wagi mięsa — oszacowałem 1,5 kg.",
    ings=[(1500, "g", "żeberka wieprzowe"), (2, "łyżeczka", "czosnek granulowany"),
          (2, "łyżeczka", "papryka wędzona"), (2, "łyżeczka", "papryka ostra"),
          (1, "łyżeczka", "sól"), (1, "łyżeczka", "pieprz"), (50, "ml", "woda"),
          (2, "łyżka", "miód"), (100, "g", "sos BBQ"), (1, "łyżeczka", "sos ostry")],
    steps=["Natrzyj żeberka mieszanką czosnku granulowanego, papryki wędzonej i ostrej, soli oraz pieprzu.",
           "Piecz 3 godziny w 130°C.",
           "Glazura: wymieszaj wodę, miód, sos BBQ i odrobinę ostrego sosu.",
           "Podnieś temperaturę do 190°C.",
           "Posmaruj żeberka glazurą i zapiekaj, obracając i smarując dwa razy."])

C[103] = dict(
    name="Cheeseburgery na gryza", cat="Przekąska", serv=6,
    note="Autor pisze „1 arkusz ciasta do pizzy” (nie francuskiego) — gotowy arkusz ma ok. 400 g.",
    ings=[(1, "szt.", "cebula"), (400, "g", "mięso mielone wołowe"),
          (1, "łyżeczka", "sól"), (1, "łyżeczka", "pieprz"),
          (1, "łyżeczka", "papryka wędzona"), (1, "łyżeczka", "czosnek granulowany"),
          (60, "g", "ketchup"), (20, "g", "musztarda"),
          (1, "szt.", "ciasto do pizzy"), (180, "g", "ser żółty"),
          (1, "szt.", "jajko"), (1, "łyżka", "sezam")],
    steps=["Podsmaż drobno posiekaną cebulę, dodaj mieloną wołowinę i smaż, aż się zarumieni.",
           "Dopraw solą, pieprzem, papryką wędzoną i czosnkiem granulowanym.",
           "Wmieszaj ketchup i musztardę, odparuj nadmiar płynu i ostudź farsz.",
           "Rozwiń arkusz ciasta i potnij na kwadraty.",
           "Na każdy kwadrat nałóż farsz i starty ser, zwiń lub złóż.",
           "Posmaruj roztrzepanym jajkiem i posyp sezamem.",
           "Piecz w 200°C ok. 20 min, aż się zarumienią."])

C[105] = dict(
    name="Naleśnikowe spaghetti", cat="Śniadanie", serv=3,
    ings=[(3, "szt.", "jajko"), (200, "g", "mąka"), (300, "ml", "mleko"),
          (30, "g", "masło"), (200, "g", "truskawki"), (2, "łyżka", "miód")],
    steps=["Zmiksuj jajka, mąkę i mleko na gładkie ciasto naleśnikowe. Wmieszaj roztopione masło.",
           "Usmaż cienkie naleśniki na rozgrzanej patelni.",
           "Ostudzone naleśniki zwiń w ciasny rulon.",
           "Potnij rulony w cienkie paski — po rozwinięciu wyglądają jak spaghetti.",
           "Wyłóż na talerz i podawaj z ulubionymi owocami.",
           "Polej miodem lub roztopioną czekoladą."])

C[122] = dict(
    name="Makaron z pesto", cat="Obiad", serv=4,
    note="W Twoim pliku: 500 g makaronu, 1 pesto i 200 g sera, a liczba porcji 1 (to raczej wartość domyślna). Przyjąłem 4 porcje — 125 g suchego makaronu na osobę, pesto = 1 słoik 190 g.",
    ings=[(500, "g", "makaron penne"), (190, "g", "pesto"), (200, "g", "ser żółty"),
          (1, "łyżeczka", "sól")],
    steps=["Ugotuj makaron penne al dente w osolonej wodzie. Zachowaj trochę wody z gotowania.",
           "Odcedź makaron i wrzuć z powrotem do garnka.",
           "Dodaj pesto i wymieszaj, rozrzedzając wodą z gotowania, aż sos ładnie oblepi makaron.",
           "Wmieszaj starty ser i podawaj od razu."])

C[124] = dict(
    name="Sałatka gyros", cat="Sałatka", serv=4,
    ings=[(800, "g", "pierś z kurczaka"), (2, "łyżka", "olej roślinny"),
          (30, "g", "przyprawa gyros"), (2, "łyżka", "majonez"),
          (4, "łyżka", "jogurt naturalny"), (2, "ząbek", "czosnek"),
          (3, "łyżka", "sok z cytryny"), (1, "łyżka", "koperek"),
          (400, "g", "kukurydza konserwowa"), (150, "g", "ogórki konserwowe"),
          (100, "g", "czerwona cebula"), (150, "g", "sałata lodowa"),
          (150, "g", "pomidorki koktajlowe"), (150, "g", "ogórek"),
          (300, "g", "papryka czerwona"), (4, "łyżka", "ketchup")],
    steps=["Pokrój piersi w kostkę, obtocz w przyprawie gyros i usmaż na oleju, aż będą rumiane. Ostudź.",
           "Sos: wymieszaj majonez, jogurt naturalny, przeciśnięty czosnek, sok z cytryny i siekany koperek.",
           "W przezroczystym naczyniu układaj warstwami — zacznij od kurczaka.",
           "Wyłóż pokrojone ogórki konserwowe.",
           "Rozłóż odsączoną kukurydzę.",
           "Dodaj pomidorki koktajlowe z czerwoną cebulą.",
           "Rozsmaruj warstwę sosu (opcjonalnie skrop ketchupem).",
           "Wyłóż kawałki papryki.",
           "Zakończ poszatkowaną sałatą lodową. Wstaw do lodówki przed podaniem."])

C[125] = dict(
    name="Sałatka z brokułem i jajkiem", cat="Sałatka", serv=4,
    ings=[(600, "g", "brokuł"), (4, "szt.", "jajko"), (200, "g", "pomidorki koktajlowe"),
          (1, "łyżka", "majonez"), (3, "łyżka", "jogurt naturalny"),
          (1, "ząbek", "czosnek"), (1, "szczypta", "sól"), (1, "szczypta", "pieprz"),
          (1, "garść", "natka pietruszki")],
    steps=["Brokuła podziel na różyczki i ugotuj al dente w osolonej wodzie — ma zostać jędrny. Odcedź i przelej zimną wodą.",
           "Ugotuj jajka na twardo, ostudź i pokrój.",
           "Pomidorki koktajlowe przekrój na połówki.",
           "Sos: wymieszaj majonez, jogurt naturalny i przeciśnięty czosnek. Dopraw solą i pieprzem.",
           "Połącz brokuła, jajka i pomidorki, polej sosem i posyp siekaną natką pietruszki."])

C[36] = dict(
    name="McWrap Tzatziki", cat="Obiad", serv=4,
    note="Autor pokazuje przepis wyłącznie na nagraniu — kroki odtworzyłem z listy składników. Sól, pieprz i czosnek granulowany do kurczaka oraz koperek do sosu dodałem od siebie — w Twoim pliku ich nie ma.",
    ings=[(8, "szt.", "polędwiczki z kurczaka"), (150, "g", "ser feta"),
          (300, "g", "skyr"), (1, "szt.", "papryka czerwona"),
          (1, "szt.", "ogórek"), (1, "szt.", "czerwona cebula"),
          (1, "opak.", "mix sałat"), (4, "szt.", "tortilla"),
          (150, "g", "panierka panko"), (1, "szt.", "jajko"),
          (1, "łyżeczka", "sól"), (1, "łyżeczka", "pieprz"),
          (1, "łyżeczka", "czosnek granulowany"), (1, "pęczek", "koperek")],
    steps=["Polędwiczki dopraw solą, pieprzem i czosnkiem granulowanym.",
           "Obtocz je w roztrzepanym jajku, a potem dokładnie w panierce panko.",
           "Piecz w piekarniku lub airfryerze, aż będą złote i chrupiące.",
           "Tzatziki: zetrzyj ogórek na tarce i mocno odciśnij z wody.",
           "Wymieszaj go ze skyrem, pokruszoną fetą, czosnkiem, koperkiem, solą i pieprzem.",
           "Na tortillę wyłóż mix sałat, paprykę i czerwoną cebulę pokrojone w paski.",
           "Dodaj chrupiące polędwiczki i sos tzatziki.",
           "Zawiń wrapa i podpiecz go krótko na suchej patelni."])

# Osierocony wiersz z jedzenie.xlsx: ten sam przepis co indeks 75, ale zostal
# po nim tylko jeden skladnik i brak linku. Nie moze nosic krokow tamtego dania.
C[123] = dict(
    name="Tacos 1 — niepełny wpis z Twojego pliku", cat="Obiad", serv=2,
    note="To resztka po tym samym przepisie co „Tacos z mięsem mielonym i cheddarem” "
         "— w jedzenie.xlsx został z niego jeden składnik i żaden link. "
         "Pełna wersja jest w tamtym wierszu; ten możesz usunąć.",
    ings=[], steps=[])
