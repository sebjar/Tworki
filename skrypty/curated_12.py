# -*- coding: utf-8 -*-
"""Przepisy, ktore doszly do kolekcji TikToka po pierwszym pobraniu."""
C = {}

C[127] = dict(
    name="Chicken Lo Mein (chiński makaron)", cat="Obiad", serv=2,
    note="Autor nie podał ilości warzyw ani makaronu — przyjąłem 1 marchewkę, 1 cebulę, "
         "200 g kapusty i 200 g makaronu na 2 porcje. Sos sojowy ciemny wchodzi dwa razy "
         "(3 łyżki do sosu + 2 łyżki do marynaty) i tak samo skrobia oraz sól.",
    ings=[
        (3, "łyżka", "ciemny sos sojowy"),
        (1, "łyżka", "olej sezamowy"),
        (2.5, "łyżeczka", "cukier"),
        (1, "szczypta", "sól"),
        (0.33, "łyżeczka", "biały pieprz"),
        (1, "łyżeczka", "skrobia ziemniaczana"),
        (3.5, "łyżka", "woda"),
        (200, "g", "udka z kurczaka bez kości"),
        (2, "łyżka", "ciemny sos sojowy"),
        (1, "szczypta", "sól"),
        (1, "łyżeczka", "skrobia ziemniaczana"),
        (1.5, "łyżka", "olej roślinny"),
        (1, "szt.", "marchewka"),
        (1, "szt.", "cebula"),
        (200, "g", "kapusta"),
        (2, "ząbek", "czosnek"),
        (1, "łyżeczka", "imbir"),
        (2, "łyżka", "białe wino"),
        (1, "łyżka", "szczypiorek"),
        (1, "szczypta", "płatki chili"),
        (200, "g", "makaron chiński"),
    ],
    steps=[
        "Sos: wymieszaj 3 łyżki ciemnego sosu sojowego, olej sezamowy, cukier, szczyptę soli, "
        "biały pieprz, łyżeczkę skrobi ziemniaczanej i 3-4 łyżki wody.",
        "Udka pokrój w kawałki i wymieszaj w drugiej misce z 2 łyżkami ciemnego sosu sojowego, "
        "solą, łyżeczką skrobi i odrobiną oleju.",
        "Rozgrzej patelnię z olejem na dużym ogniu. Smaż marchewkę, cebulę i kapustę krótko, "
        "maksymalnie 2 minuty, po czym zdejmij warzywa z patelni.",
        "Na tej samej patelni, dalej na dużym ogniu, usmaż kurczaka.",
        "Ściągnij ogień, dodaj czosnek i imbir, chwilę podsmaż i wlej odrobinę białego wina.",
        "Wrzuć z powrotem warzywa, ugotowany chiński makaron i przygotowany sos. "
        "Mieszaj, aż sos zgęstnieje i oblepi makaron.",
        "Posyp szczypiorkiem i płatkami chili.",
    ])

C[128] = dict(
    name="Sticky Korean Fried Chicken", cat="Obiad", serv=4,
    note="Autor nie wpisał ryżu ani oleju na listę składników, ale podaje 51 g węglowodanów "
         "na porcję i na filmie mówi „serve with hot rice” — dopisałem 200 g ryżu i łyżkę "
         "oleju do smażenia, bez nich przepisu nie da się odtworzyć. Zamiast gochujangu autor "
         "dopuszcza koncentrat pomidorowy wymieszany ze sriracha.",
    ings=[
        (750, "g", "pierś z kurczaka"),
        (2, "łyżeczka", "czosnek granulowany"),
        (1.5, "łyżeczka", "pieprz czarny"),
        (2, "łyżeczka", "papryka słodka"),
        (1, "łyżeczka", "sól"),
        (30, "g", "skrobia kukurydziana"),
        (1, "łyżka", "olej roślinny"),
        (50, "ml", "jasny sos sojowy"),
        (50, "ml", "woda"),
        (25, "g", "miód"),
        (40, "g", "gochujang"),
        (1, "szt.", "ogórek"),
        (20, "ml", "jasny sos sojowy"),
        (10, "ml", "ocet ryżowy"),
        (1, "szczypta", "płatki chili"),
        (1, "łyżeczka", "czosnek granulowany"),
        (1, "łyżeczka", "sezam"),
        (200, "g", "ryż"),
    ],
    steps=[
        "Pierś z kurczaka pokrój w kostkę.",
        "Dodaj czosnek granulowany, czarny pieprz, paprykę, sól i skrobię kukurydzianą. "
        "Wymieszaj tak, żeby każdy kawałek był dokładnie obtoczony.",
        "Smaż na średnim ogniu około 8 minut, aż kurczak będzie złocisty i chrupiący. "
        "Zdejmij go z patelni.",
        "Na tę samą patelnię wlej jasny sos sojowy z wodą, dodaj miód i gochujang. "
        "Trzymaj na małym ogniu i mieszaj, aż zacznie lekko bulgotać, potem redukuj "
        "3-4 minuty, aż sos zgęstnieje.",
        "Wrzuć chrupiącego kurczaka do glazury i dokładnie wymieszaj.",
        "Ogórek pokrój w cienkie plastry, zalej sosem sojowym i octem ryżowym, dodaj płatki "
        "chili, czosnek granulowany i sezam. Wymieszaj.",
        "Podawaj z gorącym ryżem. Ogórki możesz trzymać osobno i podawać zimne — "
        "danie odgrzewa się wtedy bez nich.",
    ])
