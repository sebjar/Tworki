# -*- coding: utf-8 -*-
"""Druga runda weryfikacji (28.10.2026): wartosci z niezaleznej tabeli kontrolnej,
makra autora podane za sztuke, polskie plastry boczku."""
import os, shutil
from patch_weryf_lib import podmien

for f in ("nutrition.py", "build_v2.py", "curated_04.py", "curated_05.py"):
    kop = os.path.join("kopie", f[:-3] + "_przed_runda2.py")
    if not os.path.exists(kop):
        shutil.copy(f, kop)

podmien("nutrition.py", [
    # polskie ciasto francuskie (np. Henglein): ok. 395 kcal; 558 to wartosc z tabel USA
    ('"ciasto francuskie": (558, 7, 38, 45),', '"ciasto francuskie": (395, 5.6, 24.5, 38),'),
    # musztarda stolowa / Dijon z polskich etykiet: 120-150 kcal
    ('"musztarda": (66, 4, 3.3, 5),', '"musztarda": (130, 6, 7, 10.5),'),
    # koncentrat 30%
    ('"koncentrat pomidorowy": (82, 4.3, 0.5, 19),', '"koncentrat pomidorowy": (100, 4.5, 0.5, 19),'),
    # krewetki surowe (99 to po ugotowaniu)
    ('"krewetki": (99, 24, 0.3, 0.2),', '"krewetki": (85, 20, 0.5, 0),'),
    ('("gochujang", "łyżka"): 20,', '("gochujang", "łyżka"): 20, ("chleb", "plaster"): 35,'),
])

podmien("curated_04.py", [
    ('(4, "plaster", "boczek")', '(60, "g", "boczek")'),
    ('name="Makaron w kremowym sosie z boczkiem", cat="Obiad", serv=2,\n',
     'name="Makaron w kremowym sosie z boczkiem", cat="Obiad", serv=2,\n'
     '    note="„4 plasterki boczku” — polski boczek w plastrach to ok. 15 g na plaster, razem ok. 60 g.",\n'),
], od='name="Makaron w kremowym sosie z boczkiem"', do="steps=")

podmien("curated_05.py", [
    ('name="Ostro-miodowe stripsy z kurczaka", cat="Obiad", serv=3,\n',
     'name="Ostro-miodowe stripsy z kurczaka", cat="Obiad", serv=3,\n'
     '    note="Autor podaje makra za jednego stripsa z 12 (72 kcal, 7 g białka, 8,5 g węgli, 1 g '
     'tłuszczu). Porcja w arkuszu to 4 stripsy, więc w kolumnach autora jest to razy 4.",\n'
     '    autor_makra=(288, 28, 4, 34),\n'),
], od='name="Ostro-miodowe stripsy z kurczaka"', do="steps=")

# makra autora wpisane recznie w opracowaniu (gdy autor podaje je za sztuke, nie za porcje)
podmien("build_v2.py", [
    ('    r["aK"], r["aB"], r["aT"], r["aW"] = auth if auth else (None,) * 4\n',
     '    r["aK"], r["aB"], r["aT"], r["aW"] = auth if auth else (None,) * 4\n'
     '    ov = (cur_by_key.get(r["src"]) or {}).get("autor_makra")\n'
     '    if ov:                     # juz przeliczone na porcje z arkusza\n'
     '        r["aK"], r["aB"], r["aT"], r["aW"] = ov\n'),
])
print("gotowe")
