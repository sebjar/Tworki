# -*- coding: utf-8 -*-
"""Przepisy, ktore po indywidualnym sprawdzeniu okazaly sie NIE calkiem puste,
oraz sensowne nazwy dla wpisow, ktore mialy tylko hashtagi."""
C = {}

# --- odzyskane: post zdjeciowy, ktorego oEmbed nie odczytal (HTTP 400)
C[126] = dict(
    name="Bruschetta z pesto", cat="Przekąska", serv=2,
    note="Post zdjęciowy — API TikToka go nie odczytywało, treść wzięta ze strony. "
         "Autor nie podał gramatur; ilości to moje oszacowanie na 2 porcje.",
    ings=[(4, "plaster", "chleb"), (3, "szt.", "pomidor"), (2, "ząbek", "czosnek"),
          (1, "garść", "bazylia"), (3, "łyżka", "pesto"), (2, "łyżka", "oliwa z oliwek"),
          (1, "łyżeczka", "sól"), (0.5, "łyżeczka", "pieprz")],
    steps=["Pokrój chleb na kromki — najlepiej zakwasowy, ale ciabatta albo bagietka też zadziałają.",
           "Opiecz kromki na patelni grillowej lub w piekarniku, aż się zarumienią.",
           "Ciepłe pieczywo natrzyj przekrojonym ząbkiem czosnku.",
           "Pomidory pokrój w kostkę, dopraw solą, pieprzem i oliwą.",
           "Na każdą kromkę nałóż pesto, a na to pomidory.",
           "Posyp świeżą bazylią i skrop oliwą."])

# --- opis zawiera realna metode, tylko bardzo krotka
C[111] = dict(
    name="Kurczak zapiekany z pomidorem i mozzarellą", cat="Obiad", serv=2,
    note="Autor podał metodę w jednym zdaniu i nie podał gramatur — ilości oszacowane.",
    ings=[(500, "g", "pierś z kurczaka"), (2, "szt.", "pomidor"),
          (125, "g", "mozzarella"), (1, "łyżka", "oliwa z oliwek"),
          (1, "łyżeczka", "sól"), (0.5, "łyżeczka", "pieprz"),
          (1, "łyżeczka", "oregano")],
    steps=["Piersi rozkrój wzdłuż lub rozbij na równą grubość.",
           "Dopraw solą, pieprzem i oregano, skrop oliwą.",
           "Ułóż na wierzchu plastry pomidora i mozzarelli.",
           "Piecz 20 minut w 180°C, aż ser się rozpuści i zarumieni."])

# --- nazwa dania jest w opisie, metody autor nie podaje
C[116] = dict(
    name="Pstrąg z sosem beurre blanc i brukselką", cat="Obiad", serv=2,
    note="Autor wymienia tylko składowe dania („Pstrąg / beurre blanc / brukselka”) "
         "i nie pokazuje sposobu przygotowania — kroków nie było w źródle. Składniki sosu to klasyczny beurre blanc (masło, szalotka, białe wino, ocet), ilości oszacowałem.",
    ings=[(2, "szt.", "pstrąg"), (100, "g", "masło"), (1, "szt.", "szalotka"),
          (100, "ml", "wino białe"), (2, "łyżka", "ocet"), (300, "g", "brukselka"),
          (1, "łyżeczka", "sól"), (0.5, "łyżeczka", "pieprz")],
    steps=[])

# --- same hashtagi zamiast nazwy: nadaje czytelne nazwy, bez wymyslania przepisu
C[112] = dict(
    name="Naleśnikowe sushi na słodko (deser)", cat="Deser", serv=2, ings=[], steps=[],
    note="Autor odsyła po przepis na swój profil — w opisie i w napisach nie ma "
         "ani składników, ani metody.")
C[119] = dict(
    name="Kurczak z ryżem z airfryera", cat="Obiad", serv=2, ings=[], steps=[],
    note="Opis to wyłącznie hashtagi (#airfryer #chicken #rice), film nie ma napisów. "
         "Nazwę odtworzyłem z hashtagów.")
C[108] = dict(
    name="Loaded Mexican Taco Bowl", cat="Obiad", serv=2, ings=[], steps=[],
    note="Opis wymienia składowe (chrupiące ziemniaki, wołowina w przyprawach, "
         "pico de gallo, guacamole), ale po przepis odsyła na Instagram. "
         "Gramatur ani metody nie ma w źródle.")
# C[110] - usuniete na prosbe uzytkownika
