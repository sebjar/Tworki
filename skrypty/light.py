# -*- coding: utf-8 -*-
"""Ile realnie daje zamiana produktow na wersje light - liczone na przepisach z arkusza."""
import collections, re, sys
import openpyxl
sys.path.insert(0, ".")
from nutrition import NUTR, grams

# Makra sa teraz formulami, a openpyxl ich nie liczy - czytamy kopie przeliczona
# przez LibreOffice. przelicz() odswieza ja przy kazdym uruchomieniu.
from przelicz import przelicz
P = przelicz()

# produkt -> (nazwa wersji light, kcal, bialko, tluszcz, wegle na 100 g)
LIGHT = {
    "śmietana kremówka":  ("śmietanka 12% do zup",      130, 3.0, 12, 3.5),
    "śmietana kwaśna":    ("śmietana 12%",              130, 3.0, 12, 3.5),
    "śmietana 18%":       ("śmietana 12%",              130, 3.0, 12, 3.5),
    "serek śmietankowy":  ("serek light (np. Philadelphia Light)", 170, 8.0, 13, 4.5),
    "ser żółty":          ("ser żółty light ~17% tł.",  270, 30.0, 17, 1.0),
    "cheddar":            ("cheddar light",             280, 30.0, 18, 1.0),
    "gouda":              ("gouda light",               270, 30.0, 17, 1.5),
    "mozzarella":         ("mozzarella light",          200, 24.0, 11, 2.0),
    "majonez":            ("majonez light",             330, 1.0, 35, 4.0),
    "mleko":              ("mleko 0,5%",                 35, 3.4, 0.5, 4.8),
    "ser feta":           ("feta light",                180, 16.0, 12, 3.0),
    "masło":              ("mix masła z olejem 60%",    540, 0.5, 60, 0.5),
}

wb = openpyxl.load_workbook(P, data_only=True)   # czytamy WARTOSCI, nie formuly
wp, ws = wb["Przepisy"], wb["Składniki"]

rec = {}
for r in range(2, wp.max_row + 1):
    n = wp.cell(row=r, column=2).value
    if n:
        rec["P%03d" % (r - 1)] = dict(
            nazwa=n, serv=wp.cell(row=r, column=7).value or 1,
            kcal=wp.cell(row=r, column=12).value,
            aK=wp.cell(row=r, column=16).value,
            msrc=wp.cell(row=r, column=20).value or "")
ing = collections.defaultdict(list)
for r in range(2, ws.max_row + 1):
    a, b, q, u = (ws.cell(row=r, column=i).value for i in (1, 2, 3, 4))
    if a and b and isinstance(q, (int, float)):
        ing[a[:4]].append((b, q, u))

# ile kcal w calym arkuszu siedzi w produktach, ktore maja wersje light
oszcz_prod = collections.Counter()
gramy_prod = collections.Counter()
wynik = []
for pid, v in rec.items():
    if not isinstance(v["kcal"], (int, float)):
        continue
    std = light = 0.0
    zmiany = []
    for b, q, u in ing[pid]:
        g = grams(b, u, q)
        n = NUTR.get(b)
        if not n:
            continue
        std += n[0] * g / 100
        if b in LIGHT:
            l = LIGHT[b]
            light += l[1] * g / 100
            d = (n[0] - l[1]) * g / 100
            if d > 0:
                zmiany.append((b, g, d))
                oszcz_prod[b] += d / v["serv"]
                gramy_prod[b] += g
        else:
            light += n[0] * g / 100
    if zmiany:
        wynik.append((pid, v, std / v["serv"], light / v["serv"], zmiany))

wynik.sort(key=lambda x: -(x[2] - x[3]))
print("PRZEPISY, KTORE NAJWIECEJ ZYSKUJA NA WERSJACH LIGHT (kcal na porcje)\n")
print("%-5s %-42s %7s %7s %7s   %s" % ("ID", "przepis", "zwykle", "light", "mniej", "autor podaje"))
for pid, v, s, l, z in wynik[:22]:
    aut = ("%s" % v["aK"]) if v["aK"] else "—"
    print("%-5s %-42s %7.0f %7.0f %6.0f%%   %s" % (pid, v["nazwa"][:42], s, l, (s - l) / s * 100, aut))

print("\n\nKTORE PRODUKTY DAJA TE OSZCZEDNOSC (suma po wszystkich przepisach)\n")
print("%-22s %-38s %9s %9s" % ("produkt", "wersja light", "łącznie g", "mniej kcal"))
for b, d in oszcz_prod.most_common():
    print("%-22s %-38s %9.0f %9.0f" % (b, LIGHT[b][0], gramy_prod[b], d))

print("\n\nGDZIE ROZBIEZNOSC Z AUTOREM ZNIKA PO ZAMIANIE\n")
ile_tlumaczy = 0
for pid, v, s, l, z in wynik:
    if not v["aK"] or not isinstance(v["kcal"], (int, float)):
        continue
    przed = abs(v["aK"] - s) / s * 100
    po = abs(v["aK"] - l) / l * 100 if l else 999
    if przed > 10 and po <= 15:
        ile_tlumaczy += 1
        print("   %-5s %-40s autor %4s | zwykłe %4.0f (%+.0f%%) | light %4.0f (%+.0f%%)"
              % (pid, v["nazwa"][:40], v["aK"], s, (v["aK"] - s) / s * 100, l, (v["aK"] - l) / l * 100))
print("\nPrzepisow, w ktorych sama zamiana na light tlumaczy roznice: %d" % ile_tlumaczy)
