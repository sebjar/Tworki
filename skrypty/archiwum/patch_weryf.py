# -*- coding: utf-8 -*-
"""Poprawki po recznej weryfikacji przepisow ze zrodlami (pazdziernik 2026)."""
import io


def podmien(plik, zmiany, od=None, do=None):
    t = io.open(plik, encoding="utf-8").read()
    a = t.index(od) if od else 0
    b = t.index(do, a) if do else len(t)
    blok = t[a:b]
    for stare, nowe in zmiany:
        n = blok.count(stare)
        if n != 1:
            raise SystemExit("%s: %r wystepuje %d razy" % (plik, stare, n))
        blok = blok.replace(stare, nowe)
    io.open(plik, "w", encoding="utf-8").write(t[:a] + blok + t[b:])
    print("OK", plik, od or "", len(zmiany))


podmien("normalize.py", [(
    '("tajin", "tajin", Z), ("przyprawa wlosk", "zioła włoskie", Z),\n',
    '("tajin", "tajin", Z), ("przyprawa wlosk", "zioła włoskie", Z),\n'
    '    ("octu ryz", "ocet ryżowy", O), ("octu winn", "ocet winny", O),\n'
    '    ("octu jablk", "ocet jabłkowy", O),\n'
    '    ("chicken stock", "bulion", K), ("chicken broth", "bulion", K), ("beef broth", "bulion", K),\n'
    '    ("bone broth", "bulion", K), ("chicken bouillon", "bulion w proszku", K),\n'
    '    ("chipotle w adob", "chipotle w adobo", O), ("papryczki chipotle", "chipotle w adobo", O),\n'
    '    ("papryczka chipotle", "chipotle w adobo", O),\n'
    '    ("kminek", "kminek", Z), ("kmin rzymsk", "kumin", Z),\n')])

podmien("nutrition.py", [
    ('"tajin": (50, 0, 0, 10), "sos pomidorowy": (35, 1.6, 0.2, 7),\n',
     '"tajin": (50, 0, 0, 10), "sos pomidorowy": (35, 1.6, 0.2, 7),\n'
     '    "chipotle w adobo": (80, 1.5, 4, 10), "kminek": (333, 20, 15, 50),\n'),
    ('("fasola czerwona", "puszka"): 240, ("bułka", "szt."): 60,\n',
     '("fasola czerwona", "puszka"): 240, ("bułka", "szt."): 60,\n'
     '    ("chipotle w adobo", "szt."): 12,\n'),
    ('SPICE_TSP = {"pieprz",', 'SPICE_TSP = {"kminek", "pieprz",'),
])

podmien("curated_01.py", [
    ('name="Burrito z kurczakiem tikka masala", cat="Obiad", serv=11,\n',
     'name="Burrito z kurczakiem tikka masala", cat="Obiad", serv=11,\n'
     '    note="Jogurt grecki 800 g to 200 g do sosu masala + 600 g do ziołowego sosu do maczania '
     '— tak podaje autor. Cytryny: 2 do marynaty i 1 do sosu.",\n'),
    ('(2, "szt.", "cytryna")', '(3, "szt.", "cytryna")'),
    ('(1, "łyżka", "kolendra")', '(1, "łyżka", "kolendra mielona")'),
], od="C[13] = dict(", do="C[14] = dict(")

podmien("curated_01.py", [
    ('name="Fajitas z kurczakiem z blachy z sosem chipotle", cat="Obiad", serv=6,\n',
     'name="Fajitas z kurczakiem z blachy z sosem chipotle", cat="Obiad", serv=6,\n'
     '    note="Przyprawy policzone razem dla kurczaka i warzyw (autor podaje je osobno). '
     'Chipotle to wędzone papryczki w sosie adobo ze słoika/puszki — nie świeże chili.",\n'),
    ('(4, "łyżka", "olej roślinny")', '(5, "łyżka", "olej roślinny")'),
    ('(1, "łyżka", "chili")', '(4, "łyżeczka", "chili")'),
    ('(1, "łyżka", "kumin")', '(4, "łyżeczka", "kumin")'),
    ('(3, "łyżeczka", "sól")', '(4, "łyżeczka", "sól")'),
    ('(2, "szt.", "papryczka chili")]', '(2, "szt.", "papryczki chipotle w adobo"),\n'
     '          (0.5, "pęczek", "kolendra")]'),
], od="C[14] = dict(", do="C[15] = dict(")

podmien("curated_05.py", [
    ('(1, "łyżeczka", "sól"), (1, "łyżeczka", "pieprz")],',
     '(1, "łyżeczka", "sól"), (1, "łyżeczka", "pieprz"), (1, "szt.", "cytryna")],'),
    ('Dopraw solą i pieprzem."])', 'Dopraw solą i pieprzem i podawaj skropioną sokiem z cytryny."])'),
], od="C[48] = dict(", do="C[49] = dict(")

podmien("curated_05.py", [
    ('(0.5, "łyżeczka", "kumin")', '(0.5, "łyżeczka", "kminek mielony")'),
    ('(0.5, "łyżeczka", "kolendra")', '(0.5, "łyżeczka", "kolendra ziarna")'),
], od="C[54] = dict(", do="C[55] = dict(")

podmien("curated_06.py", [
    ('name="Crunch Wrap Supreme", cat="Obiad", serv=4,\n',
     'name="Crunch Wrap Supreme", cat="Obiad", serv=4,\n'
     '    note="Autor: „po 30 g każdego sera na sztukę” — przy 4 wrapach to 120 g cheddara '
     'i 120 g mozzarelli.",\n'),
    ('(60, "g", "cheddar"), (60, "g", "mozzarella")', '(120, "g", "cheddar"), (120, "g", "mozzarella")'),
], od="C[58] = dict(", do="C[59] = dict(")

podmien("curated_08.py", [
    ('(2, "łyżka", "kolendra")', '(2, "łyżka", "kolendra mielona")'),
], od="C[86] = dict(", do="steps=")

podmien("curated_09.py", [
    ('name="Makaron z pesto", cat="Obiad", serv=2,\n',
     'name="Makaron z pesto", cat="Obiad", serv=4,\n'
     '    note="W Twoim pliku: 500 g makaronu, 1 pesto i 200 g sera, a liczba porcji 1 '
     '(to raczej wartość domyślna). Przyjąłem 4 porcje — 125 g suchego makaronu na osobę, '
     'pesto = 1 słoik 190 g.",\n'),
    ('(250, "g", "makaron penne"), (100, "g", "pesto"), (100, "g", "ser żółty")',
     '(500, "g", "makaron penne"), (190, "g", "pesto"), (200, "g", "ser żółty")'),
], od="C[122] = dict(", do="C[124] = dict(")
