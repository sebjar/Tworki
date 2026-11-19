# -*- coding: utf-8 -*-
"""Poprawki po weryfikacji kalorii i porcji przepis po przepisie (pazdziernik 2026)."""
import io, os, shutil
from patch_weryf_lib import podmien

# (tabela, slownik i wzorce makr zostaly juz nalozone w pierwszym przebiegu)

# ---------------------------------------------------------------- przepisy
podmien("curated_00.py", [
    ('name="McDonald\'s w domu: bułki, nuggetsy, McChicken i Big Mac", cat="Obiad", serv=6,\n',
     'name="McDonald\'s w domu: bułki, nuggetsy, McChicken i Big Mac", cat="Obiad", serv=6,\n'
     '    note="Nuggetsy i kotlety McChicken smaży się w głębokim oleju, a autorka nie wpisała go '
     'na listę. Przyjąłem 700 ml w garnku; do kalorii liczy się z tego tylko to, co wsiąka '
     'w panierkę (ok. 15%).",\n'),
    ('(2, "łyżeczka", "biały pieprz")]', '(2, "łyżeczka", "biały pieprz"), (700, "ml", "olej roślinny")]'),
], od='name="McDonald', do="steps=")

podmien("curated_02.py", [
    ('name="Kurczak teriyaki stir fry", cat="Obiad", serv=4,\n',
     'name="Kurczak teriyaki stir fry", cat="Obiad", serv=2,\n'
     '    note="Autor pisze „Makes: 2 servings” i podaje 650 kcal na porcję — bez ryżu. Ryżu nie podał, '
     'dopisałem 200 g suchego, czyli 100 g na porcję, stąd u mnie więcej kalorii.",\n'),
], od='name="Kurczak teriyaki stir fry"', do="steps=")

podmien("curated_02.py", [
    ('name="Grecka sałatka z kurczakiem i kremowym sosem", cat="Sałatka", serv=3,\n',
     'name="Grecka sałatka z kurczakiem i kremowym sosem", cat="Sałatka", serv=2,\n'
     '    note="Autor: „Serving Size: 2” i 347 kcal na porcję, licząc jogurt grecki 0%.",\n'),
], od='name="Grecka sałatka z kurczakiem', do="steps=")

podmien("curated_03.py", [
    ('name="Sałatka z chrupiącym ryżem i kurczakiem", cat="Sałatka", serv=4,\n',
     'name="Sałatka z chrupiącym ryżem i kurczakiem", cat="Sałatka", serv=4,\n'
     '    note="Autorka podaje 200 g UGOTOWANEGO ryżu — to ok. 80 g suchego, i tyle jest na liście '
     'zakupów.",\n'),
    ('(200, "g", "ryż parboiled")', '(80, "g", "ryż parboiled")'),
], od='name="Sałatka z chrupiącym ryżem i kurczakiem"', do="steps=")

podmien("curated_07.py", [
    ('name="Sałatka z chrupiącą ciecierzycą", cat="Sałatka", serv=2,\n',
     'name="Sałatka z chrupiącą ciecierzycą", cat="Sałatka", serv=2,\n'
     '    note="Autorka bierze ciecierzycę ze słoika 400 g — po odsączeniu zostaje ok. 240 g. '
     'Podaje ~920 kcal za całą miskę, czyli ok. 460 kcal na porcję.",\n'),
    ('(400, "g", "ciecierzyca")', '(240, "g", "ciecierzyca")'),
], od='name="Sałatka z chrupiącą ciecierzycą"', do="steps=")

podmien("curated_13.py", [
    ('note="Czosnek wchodzi dwa razy', 'note="Kalorie to sam kurczak w sosie — autor nie wlicza '
     'ryżu ani naanu. Czosnek wchodzi dwa razy'),
], od='name="Inflacyjny butter chicken"', do="steps=")

podmien("curated_06.py", [
    ('name="Kurczak ze szpinakiem z jednej patelni", cat="Obiad", serv=4,\n',
     'name="Kurczak ze szpinakiem z jednej patelni", cat="Obiad", serv=4,\n'
     '    note="„1 słoik suszonych pomidorów” — słoik ma ok. 280 g, po odsączeniu z oleju zostaje '
     'ok. 170 g.",\n'),
    ('(1, "opak.", "suszone pomidory")', '(170, "g", "suszone pomidory")'),
], od='name="Kurczak ze szpinakiem z jednej', do="steps=")

podmien("curated_06.py", [
    ('(1, "szt.", "pita")', '(38, "g", "pita")'),
    ('name="Pita z kurczakiem miodowo-czosnkowym", cat="Obiad", serv=2,\n',
     'name="Pita z kurczakiem miodowo-czosnkowym", cat="Obiad", serv=2,\n'
     '    note="Autor używa jednej małej pity pełnoziarnistej (38 g) przekrojonej na pół — '
     'stąd „2 pity” po 298 kcal.",\n'),
], od='name="Pita z kurczakiem miodowo', do="steps=")

podmien("curated_00.py", [
    ('name="Sałatka ziemniaczana z pieczonymi ziemniakami", cat="Sałatka", serv=4,\n',
     'name="Sałatka ziemniaczana z pieczonymi ziemniakami", cat="Sałatka", serv=2,\n'
     '    note="Autorzy piszą o „lunchu we dwoje”, stąd 2 porcje. 6-7 młodych ziemniaków to ok. '
     '450 g. Najwięcej kalorii daje oliwa — 7 łyżek (3 do pieczenia, 4 do sosu).",\n'),
    ('(7, "szt.", "ziemniaki")', '(450, "g", "ziemniaki")'),
], od='name="Sałatka ziemniaczana z pieczonymi', do="steps=")

podmien("curated_00.py", [
    ('name="Kremowy makaron z kurczakiem, czosnkiem i parmezanem", cat="Obiad", serv=3,\n',
     'name="Kremowy makaron z kurczakiem, czosnkiem i parmezanem", cat="Obiad", serv=4,\n'
     '    note="Na blogu autorki (majasrecipes.com) przepis jest na 4 porcje.",\n'),
], od='name="Kremowy makaron z kurczakiem, czosnkiem', do="steps=")

podmien("curated_05.py", [
    ('cat="Obiad", serv=2,\n    note="Dwie papryki przekrojone na pół to cztery połówki, czyli po dwie '
     'na osobę — stąd 2 porcje. Autor nie podał ani liczby porcji, ani makr.",',
     'cat="Obiad", serv=4,\n    note="Autor podaje 540 kcal i 41 g białka na porcję (na chudej '
     'wołowinie 3%) — to się zgadza przy 4 porcjach, czyli po połówce papryki z ryżem. Ilość ryżu '
     'jest moja, w opisie jest samo „long grain rice”.",'),
], od='name="Papryka faszerowana wołowiną', do="steps=")

podmien("curated_05.py", [
    ('name="Ryż z kurczakiem fajita", cat="Obiad", serv=2,\n',
     'name="Ryż z kurczakiem fajita", cat="Obiad", serv=2,\n'
     '    note="Autor: 1,5 szklanki ugotowanego ryżu, „approx. 0.5 uncooked” — czyli ok. 95 g '
     'suchego.",\n'),
    ('(150, "g", "ryż")', '(95, "g", "ryż")'),
], od='name="Ryż z kurczakiem fajita"', do="steps=")

podmien("curated_07.py", [
    ('name="Sałatka sylwestrowa z kurczakiem i orzo", cat="Sałatka", serv=4,\n',
     'name="Sałatka sylwestrowa z kurczakiem i orzo", cat="Sałatka", serv=4,\n'
     '    note="Autorka podaje 200 g UGOTOWANEGO orzo — to ok. 90 g suchego makaronu.",\n'),
    ('(200, "g", "makaron orzo")', '(90, "g", "makaron orzo")'),
], od='name="Sałatka sylwestrowa', do="steps=")

podmien("curated_03.py", [
    ('(900, "g", "mięso mielone z kurczaka")', '(900, "g", "mięso mielone z piersi kurczaka")'),
], od='name="McChicken domowy"', do="steps=")

podmien("curated_02.py", [
    ('(500, "g", "mięso mielone")', '(500, "g", "mięso mielone wieprzowe")'),
], od='name="Sajgonki z mięsem mielonym"', do="steps=")

podmien("curated_07.py", [
    ('(600, "g", "mięso mielone z kurczaka")', '(600, "g", "mięso mielone z piersi kurczaka")'),
], od='name="Arayes z kurczakiem"', do="steps=")

podmien("curated_09.py", [
    ('name="Cheeseburgery na gryza", cat="Przekąska", serv=6,\n',
     'name="Cheeseburgery na gryza", cat="Przekąska", serv=6,\n'
     '    note="Autor pisze „1 arkusz ciasta do pizzy” (nie francuskiego) — gotowy arkusz ma ok. 400 g.",\n'),
    ('(1, "szt.", "ciasto francuskie")', '(1, "szt.", "ciasto do pizzy")'),
], od='name="Cheeseburgery na gryza"', do="steps=")

podmien("curated_07.py", [
    ('(12, "szt.", "tortilla")', '(12, "szt.", "tortilla mała")'),
], od='name="Tacos z mięsem mielonym', do="steps=")

podmien("curated_06.py", [
    ('name="Sweet honey chicken", cat="Obiad", serv=4,\n',
     'name="Sweet honey chicken", cat="Obiad", serv=2,\n'
     '    note="Na blogu autora (iamneverfull.com) przepis jest na 2 porcje. Ryżu nie podał — '
     'dopisałem 100 g suchego na porcję.",\n'),
], od='name="Sweet honey chicken"', do="steps=")

podmien("curated_10.py", [
    ('(150, "g", "masło")', '(100, "g", "masło")'),
], od='name="Pstrąg z sosem', do="steps=")

podmien("curated_02.py", [
    ('name="Lody twarogowe o smaku sernika z borówkami", cat="Deser", serv=4,\n',
     'name="Lody twarogowe o smaku sernika z borówkami", cat="Deser", serv=3,\n'
     '    note="Autor: „Serving Size: 3” i 225 kcal na porcję — liczy na syropie klonowym bez cukru.",\n'),
], od='name="Lody twarogowe', do="steps=")

podmien("curated_04.py", [
    ('(3, "szt.", "jajko")', '(1, "szt.", "jajko"), (2, "szt.", "żółtko")'),
], od='name="Carbonara"', do="steps=")

podmien("curated_01.py", [
    ('name="Placek ziemniaczany hash brown", cat="Śniadanie", serv=4,\n',
     'name="Placek ziemniaczany hash brown", cat="Śniadanie", serv=4,\n'
     '    note="Autor smaży na „hojnej” warstwie oleju bez podania ilości — liczę 70 ml, mniej '
     'więcej tyle wsiąka w placek.",\n'),
    ('(100, "ml", "olej roślinny")', '(70, "ml", "olej roślinny")'),
], od='name="Placek ziemniaczany', do="steps=")

podmien("curated_04.py", [
    ('name="Rolgeski z ciasta francuskiego z bekonem i serem", cat="Przekąska", serv=4,\n',
     'name="Rolgeski z ciasta francuskiego z bekonem i serem", cat="Przekąska", serv=12,\n'
     '    note="Wychodzi 12 rulonów i porcja to jeden rulon — przy planowaniu wpisz 2-3 na osobę. '
     '12 plastrów bekonu to typowe opakowanie ok. 180 g.",\n'),
    ('(12, "plaster", "boczek")', '(180, "g", "boczek")'),
], od='name="Rolgeski', do="steps=")
print("gotowe")
