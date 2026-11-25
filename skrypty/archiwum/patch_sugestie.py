# -*- coding: utf-8 -*-
"""Dopina moje propozycje (sugestie.py) do planera: nowe produkty w tabelach, kolumna
"Skąd" i niebieskie wiersze w Przepisach, zakladka Sugestie, opis w Instrukcji."""
import io, os, re, shutil
from patch_weryf_lib import podmien

for f in ("nutrition.py", "normalize.py", "lightdata.py", "build_v2.py", "sugestie.py"):
    kop = os.path.join("kopie", f[:-3] + "_przed_sugestiami.py")
    if not os.path.exists(kop):
        shutil.copy(f, kop)

# linki z nazwa konta, tak jak reszta arkusza (z nich bierze sie kolumna Autor)
t = io.open("sugestie.py", encoding="utf-8").read()
t = re.sub(r'link="https://www\.instagram\.com/p/([\w-]+)/", author="([\w.]+)"',
           r'link="https://www.instagram.com/\2/p/\1/", author="\2"', t)
io.open("sugestie.py", "w", encoding="utf-8").write(t)

podmien("nutrition.py", [
    ("\n\ndef grams(name, unit, qty):",
     '\n# --- dopisane przy moich propozycjach (28.10.2026)\n'
     'NUTR.update({\n'
     '    "pasta chipotle": (160, 2, 10, 15), "mleko zagęszczone": (131, 6.6, 7.5, 9.5),\n'
     '    "salsa": (36, 1.5, 0.2, 7), "białko jaja": (48, 10.9, 0.2, 0.7),\n'
     '    "jalapeño": (29, 0.9, 0.4, 6.5), "przyprawa tandoori": (250, 10, 8, 40),\n'
     '    "ziele angielskie": (263, 6, 8.7, 72), "fasola czarna": (91, 6, 0.5, 12),\n'
     '    "ser topiony": (280, 13, 23, 5), "pasta curry": (300, 4, 25, 15),\n'
     '    "maślanka": (38, 3.4, 0.5, 4.8), "sok pomarańczowy": (45, 0.7, 0.2, 10.4),\n'
     '})\n'
     'GRAMS.update({\n'
     '    ("cynamon", "szt."): 3, ("jalapeño", "szt."): 20, ("ser topiony", "plaster"): 20,\n'
     '    ("białko jaja", "szt."): 33, ("fasola czarna", "puszka"): 250,\n'
     '})\n'
     'SPICE_TSP |= {"przyprawa tandoori", "ziele angielskie"}\n'
     '\n\ndef grams(name, unit, qty):'),
])

podmien("normalize.py", [
    ('    ("kminek", "kminek", Z), ("kmin rzymsk", "kumin", Z),\n]',
     '    ("kminek", "kminek", Z), ("kmin rzymsk", "kumin", Z),\n'
     '    ("pasta chipotle", "pasta chipotle", K), ("mleko zageszczon", "mleko zagęszczone", N),\n'
     '    ("salsa", "salsa", K), ("bialko jaj", "białko jaja", N), ("bialka jaj", "białko jaja", N),\n'
     '    ("jalapeno", "jalapeño", W), ("tandoori", "przyprawa tandoori", Z),\n'
     '    ("ziele angielsk", "ziele angielskie", Z), ("fasola czarn", "fasola czarna", K),\n'
     '    ("czarna fasol", "fasola czarna", K), ("ser topion", "ser topiony", N),\n'
     '    ("pasta curry", "pasta curry", K), ("maslank", "maślanka", N),\n'
     '    ("sok pomaranczow", "sok pomarańczowy", D), ("sok z pomarancz", "sok pomarańczowy", D),\n'
     ']'),
])

podmien("lightdata.py", [
    ('                             "do sosów bez różnicy."),\n}',
     '                             "do sosów bez różnicy."),\n'
     '    "mleko zagęszczone": ("mleko zagęszczone light 4%", 103, 7.0, 4.0, 10.0,\n'
     '                          "W kremowym sosie różnicy prawie nie czuć."),\n'
     '}'),
])

podmien("build_v2.py", [
    # niebieskie tlo dla moich propozycji
    ('OK_FILL = PatternFill("solid", fgColor="E8F5E9")\n',
     'OK_FILL = PatternFill("solid", fgColor="E8F5E9")\n'
     'SUG_FILL = PatternFill("solid", fgColor="DDEBF7")\n'),
    # wczytanie propozycji obok przepisow z Twoich zapisanych
    ('BAD_BLOG = {"Creamy Chicken & Brown Butter Pasta", "Butter chicken"}\n',
     'BAD_BLOG = {"Creamy Chicken & Brown Butter Pasta", "Butter chicken"}\n'
     '\n'
     '# --- moje propozycje (sugestie.py): przepisy spoza Twoich zapisanych, opracowane recznie\n'
     'from sugestie import SUGESTIE, DATA as SUG_DATA\n'
     'SUG = {}\n'
     'for s in SUGESTIE:\n'
     '    k = "sugestia:" + s["link"]\n'
     '    data[k] = dict(name=s["name"], author=s["author"], link=s["link"], parsed={}, file_ings=[])\n'
     '    cur_by_key[k] = s\n'
     '    SUG[k] = s\n'),
    ('                        n_ing=len(items), steps=steps, note=(cur or {}).get("note", "")))\n',
     '                        n_ing=len(items), steps=steps, note=(cur or {}).get("note", ""),\n'
     '                        sug=key in SUG, powod=(cur or {}).get("powod", "")))\n'),
    # propozycje dostaja numery w kolejnosci z listy, przed innymi nowymi
    ('for r in recipes:                      # nowe numerujemy w dotychczasowym porzadku sortowania\n',
     'for s in SUGESTIE:                     # propozycje numerujemy w kolejnosci z listy\n'
     '    if "sugestia:" + s["link"] not in IDS:\n'
     '        IDS["sugestia:" + s["link"]] = "P%03d" % nastepny\n'
     '        nastepny += 1\n'
     'for r in recipes:                      # nowe numerujemy w dotychczasowym porzadku sortowania\n'),
    ('n_sim = sum(1 for r in recipes if r["similar"])\n',
     'n_sim = sum(1 for r in recipes if r["similar"])\n'
     'sug_r = [r for r in recipes if r["sug"]]\n'
     'n_sug = len(sug_r)\n'
     'sug_zakres = "%s-%s" % (sug_r[0]["id"], sug_r[-1]["id"]) if sug_r else ""\n'
     'sug_autorzy = []\n'
     'for r in sug_r:\n'
     '    if r["platform"] == "Instagram" and r["author"] not in sug_autorzy:\n'
     '        sug_autorzy.append(r["author"])\n'
     'n_sug_ig = sum(1 for r in sug_r if r["platform"] == "Instagram")\n'),
    # kolumna AH: skad jest przepis
    ('          "Uwaga do porcji", "Na drugi dzień", "Jak odgrzewać"],\n'
     '     [7, 46, 14, 12, 20, 44, 9, 10, 13, 88, 54, 12, 11, 11, 10, 12, 12, 12, 11, 22,\n'
     '      13, 12, 11, 60, 12, 12, 12, 12, 12, 12, 40, 24, 74])\n',
     '          "Uwaga do porcji", "Na drugi dzień", "Jak odgrzewać", "Skąd"],\n'
     '     [7, 46, 14, 12, 20, 44, 9, 10, 13, 88, 54, 12, 11, 11, 10, 12, 12, 12, 11, 22,\n'
     '      13, 12, 11, 60, 12, 12, 12, 12, 12, 12, 40, 24, 74, 26])\n'),
    ('        ws.cell(row=row, column=33, value=r["odgrz_jak"])\n',
     '        ws.cell(row=row, column=33, value=r["odgrz_jak"])\n'
     '    ws.cell(row=row, column=34, value=("Sugestia Claude " + SUG_DATA) if r["sug"]\n'
     '            else "Twoje zapisane")\n'),
    ('    for ci in range(1, 34):\n        c = ws.cell(row=row, column=ci)\n        c.border = BORDER\n'
     '        c.alignment = Alignment(vertical="top", wrap_text=(ci in (10, 11, 24, 31, 33)))\n',
     '    for ci in range(1, 35):\n        c = ws.cell(row=row, column=ci)\n        c.border = BORDER\n'
     '        c.alignment = Alignment(vertical="top", wrap_text=(ci in (10, 11, 24, 31, 33)))\n'),
    ('        if ci in (21, 22, 23, 24) or ci >= 25:\n',
     '        if ci in (21, 22, 23, 24) or 25 <= ci <= 33:\n'),
    ('        ws.cell(row=row, column=7).font = WARN\nws.freeze_panes = "C2"\n'
     'ws.auto_filter.ref = "A1:AG%d" % MAXP\n',
     '        ws.cell(row=row, column=7).font = WARN\n'
     '    # moje propozycje: niebieskie ID, nazwa i "Skąd" - od razu widac, ze to nie Twoje zapisane\n'
     '    if row - 2 < len(recipes) and recipes[row - 2]["sug"]:\n'
     '        for ci in (1, 2, 34):\n'
     '            ws.cell(row=row, column=ci).fill = SUG_FILL\n'
     '        ws.cell(row=row, column=34).font = Font(name=F, size=10, bold=True, color="1F4E79")\n'
     'ws.freeze_panes = "C2"\n'
     'ws.auto_filter.ref = "A1:AH%d" % MAXP\n'),
    # Instrukcja
    ('ws["B3"] = "%d przepisów z TikToka, Instagrama, YouTube i blogów." % len(recipes)\n',
     'ws["B3"] = ("%d przepisów z TikToka, Instagrama, YouTube i blogów, w tym %d moich propozycji "\n'
     '            "(niebieskie)." % (len(recipes), n_sug))\n'),
    ('                          "z kolejnymi numerami — te z przeglądu 19.10.2026 to P137-P147."),\n',
     '                          "z kolejnymi numerami — te z przeglądu 19.10.2026 to P137-P147, "\n'
     '                          "a moje propozycje z %s to %s." % (SUG_DATA, sug_zakres)),\n'),
    ('    ("", ""),\n    ("KOLUMNA „OPRACOWANIE”", ""),\n',
     '    ("", ""),\n'
     '    ("MOJE PROPOZYCJE", ""),\n'
     '    ("Co to jest", "%d przepisów, których nie zapisałeś — dobrałem je %s do tego, co "\n'
     '                   "zapisujesz najczęściej: kurczak, meal prep na kilka dni, kremowe sosy, "\n'
     '                   "wrapy, kuchnia azjatycka i meksykańska. Numery %s. %d z Instagrama (%s) "\n'
     '                   "i %d z aniagotuje.pl."\n'
     '                   % (n_sug, SUG_DATA, sug_zakres, n_sug_ig, ", ".join(sug_autorzy),\n'
     '                      n_sug - n_sug_ig)),\n'
     '    ("Jak je znaleźć", "W Przepisach mają niebieskie ID i nazwę, a w ostatniej kolumnie "\n'
     '                       "„Skąd” wpis „Sugestia Claude”. Filtr na tej kolumnie pokaże tylko je. "\n'
     '                       "Wszystkie są też w zakładce Sugestie — razem z tym, dlaczego Ci je "\n'
     '                       "proponuję."),\n'
     '    ("Kalorie", "Liczone jak w reszcie arkusza, na zwykłych produktach. Autorzy z Instagrama "\n'
     '                "liczą na light (jogurt 0%, lekki ser i majonez, chuda wołowina 96%), więc "\n'
     '                "ich liczby w kolumnie „kcal — autor” są zwykle niższe."),\n'
     '    ("Nie smakuje?", "Skasuj wiersz w Przepisach i jego wiersze w Składnikach, jak przy "\n'
     '                     "każdym innym przepisie. Numer nie wróci do obiegu."),\n'
     '    ("", ""),\n'
     '    ("KOLUMNA „OPRACOWANIE”", ""),\n'),
    # Weryfikacja: skad porcje przy propozycjach, bez zoltego "poprawione"
    ('        w = WER.get(r["id"], {})\n',
     '        w = WER.get(r["id"], {})\n'
     '        if r["sug"]:\n'
     '            w = dict(porcje=SUG[r["src"]]["porcje_skad"],\n'
     '                     wynik="Moja propozycja z %s, spoza Twoich zapisanych. Składniki i ilości "\n'
     '                           "przepisane ze źródła; produkty light autora policzone jako "\n'
     '                           "zwykłe." % SUG_DATA)\n'),
    ('        poprawiony = bool(wynik) and not wynik.startswith(("Składniki", "Autor nie"))\n',
     '        poprawiony = (bool(wynik) and not wynik.startswith(("Składniki", "Autor nie"))\n'
     '                      and not r["sug"])\n'),
    ('            if poprawiony:\n                c.fill = POPR_FILL\n',
     '            if poprawiony:\n                c.fill = POPR_FILL\n'
     '            elif r["sug"] and col <= 2:\n                c.fill = SUG_FILL\n'),
    # zakladka Sugestie zaraz za Przepisami
    ('\nwb.save(OUT)\n',
     '\n# ------------------------------------------------ moje propozycje w jednym miejscu\n'
     'if sug_r:\n'
     '    ws = wb.create_sheet("Sugestie", wb.sheetnames.index("Przepisy") + 1)\n'
     '    head(ws, ["ID", "Nazwa przepisu", "Kategoria", "Autor", "Link", "Dlaczego Ci to proponuję",\n'
     '              "Porcje bazowe", "kcal / porcję", "Białko (g)", "kcal — autor", "Na drugi dzień"],\n'
     '         [7, 44, 11, 20, 42, 74, 9, 10, 10, 10, 22])\n'
     '    for i, r in enumerate(sug_r):\n'
     '        row = 2 + i\n'
     '        ws.cell(row=row, column=1, value=r["id"])\n'
     '        szukaj = \'MATCH($A{0},Przepisy!$A:$A,0)\'.format(row)\n'
     '        # nazwa, porcje i kcal ida z Przepisow, wiec zmiana tam od razu widac tutaj\n'
     '        for col, kol in ((2, "B"), (3, "C"), (7, "G"), (8, "L"), (9, "M"), (10, "P"),\n'
     '                         (11, "AF")):\n'
     '            idx = \'INDEX(Przepisy!${0}:${0},{1})\'.format(kol, szukaj)\n'
     '            ws.cell(row=row, column=col, value=sprawdz(\n'
     '                \'=IFERROR(IF({0}="","",{0}),"")\'.format(idx)))\n'
     '        ws.cell(row=row, column=4, value=r["author"])\n'
     '        c = ws.cell(row=row, column=5, value=r["link"])\n'
     '        c.hyperlink = r["link"]\n'
     '        ws.cell(row=row, column=6, value=r["powod"])\n'
     '        for col in range(1, 12):\n'
     '            c = ws.cell(row=row, column=col)\n'
     '            c.border = BORDER\n'
     '            c.alignment = Alignment(vertical="top", wrap_text=col in (2, 5, 6, 11),\n'
     '                                    horizontal="center" if col in (7, 8, 9, 10) else None)\n'
     '            c.font = (Font(name=F, size=9, color="0563C1", underline="single") if col == 5\n'
     '                      else CALC if col in (2, 3, 7, 8, 9, 10, 11) else BASE)\n'
     '            if col <= 2:\n'
     '                c.fill = SUG_FILL\n'
     '        ws.row_dimensions[row].height = 54\n'
     '    ws.freeze_panes = "C2"\n'
     '    ws.auto_filter.ref = "A1:K%d" % (len(sug_r) + 1)\n'
     '\nwb.save(OUT)\n'),
])
print("gotowe")
