# -*- coding: utf-8 -*-
"""Audyt jakosci gotowego skoroszytu: skladniki, ilosci, kategorie, spojnosc."""
import collections, re, sys
import openpyxl

P = r"C:\Users\Sebastian\Documents\Przepisy-planer\Przepisy-planer.xlsx"

# gorne granice zdrowego rozsadku dla jednego przepisu
MAXQ = {"g": 2000, "kg": 3, "ml": 2000, "l": 3, "szt.": 20, "łyżka": 15, "łyżeczka": 12,
        "szklanka": 6, "ząbek": 15, "puszka": 4, "opak.": 4, "garść": 5, "szczypta": 5,
        "plaster": 16, "pęczek": 3, "główka": 3, "dag": 100, "oz": 40, "lbs": 4}
VERBY = re.compile(r"(?i)\b(smaz|dodaj|wymieszaj|piecz|gotuj|podsmaz|pokroj|wlej|odstaw|"
                   r"cook|add|mix|heat|stir|bake|fry|serve|pour|simmer|combine)")

wb = openpyxl.load_workbook(P)
wp, ws, wl = wb["Przepisy"], wb["Składniki"], wb["Lista zakupów"]

recipes = {}
for r in range(2, wp.max_row + 1):
    n = wp.cell(row=r, column=2).value
    if not n:
        continue
    recipes[n] = dict(row=r, cat=wp.cell(row=r, column=3).value,
                      serv=wp.cell(row=r, column=7).value,
                      ning=wp.cell(row=r, column=8).value or 0,
                      qual=wp.cell(row=r, column=9).value,
                      steps=wp.cell(row=r, column=10).value or "",
                      sim=wp.cell(row=r, column=11).value or "")

rows = []
for r in range(2, ws.max_row + 1):
    a, b, c, d, e = (ws.cell(row=r, column=i).value for i in (1, 2, 3, 4, 5))
    if a and b:
        rows.append(dict(row=r, rec=a, ing=b, qty=c, unit=d, sec=e))

problems = collections.OrderedDict()


def add(k, v):
    problems.setdefault(k, []).append(v)


# 1) spojnosc: kazdy przepis w Skladnikach musi istniec w Przepisach
for x in rows:
    if x["rec"] not in recipes:
        add("Składnik wskazuje na nieistniejący przepis (formuły go nie policzą)",
            "w. %d: %s" % (x["row"], x["rec"][:50]))

# 2) brak kategorii
for n, v in recipes.items():
    if not v["cat"]:
        add("Przepis bez kategorii", n[:60])

# 3) nazwa skladnika wygladajaca na zdanie
for x in rows:
    if len(x["ing"]) > 34 or VERBY.search(x["ing"]):
        add("Nazwa składnika wygląda na zdanie, nie produkt",
            "w. %d: %s" % (x["row"], x["ing"][:60]))

# 4) ilosci poza zdrowym rozsadkiem
for x in rows:
    q, u = x["qty"], x["unit"]
    if not isinstance(q, (int, float)):
        add("Brak liczbowej ilości", "w. %d: %s" % (x["row"], x["ing"][:40]))
    elif q <= 0:
        add("Ilość zero lub ujemna", "w. %d: %s" % (x["row"], x["ing"][:40]))
    elif u in MAXQ and q > MAXQ[u]:
        add("Podejrzanie duża ilość",
            "w. %d: %s %s %s (%s)" % (x["row"], q, u, x["ing"][:34], x["rec"][:26]))

# 5) ten sam skladnik dwa razy w jednym przepisie
seen = collections.Counter()
for x in rows:
    seen[(x["rec"], x["ing"], x["unit"])] += 1
for k, c in seen.items():
    if c > 1:
        add("Ten sam składnik powtórzony w przepisie", "%s: %s" % (k[0][:34], k[1][:30]))

# 6) dzial "Inne"
for x in rows:
    if x["sec"] == "Inne":
        add("Składnik bez przypisanego działu sklepu", "%s" % x["ing"][:50])

# 7) przepis ze skladnikami, ale bez przygotowania (i odwrotnie)
for n, v in recipes.items():
    if v["ning"] and not v["steps"]:
        add("Ma składniki, brak przygotowania", n[:60])
    if v["steps"] and not v["ning"]:
        add("Ma przygotowanie, brak składników", n[:60])

# 8) porcje
for n, v in recipes.items():
    if not isinstance(v["serv"], (int, float)) or not (0 < v["serv"] <= 24):
        add("Nieprawidłowa liczba porcji", "%s -> %s" % (n[:50], v["serv"]))

# --- raport
print("Przepisow: %d | wierszy skladnikow: %d" % (len(recipes), len(rows)))
print("Kategorie:", dict(collections.Counter(v["cat"] for v in recipes.values())))
print("Opracowanie:", dict(collections.Counter(v["qual"] for v in recipes.values())))
print("Oznaczonych jako podobne: %d" % sum(1 for v in recipes.values() if v["sim"]))
print()
if not problems:
    print("BRAK PROBLEMOW.")
for k, v in problems.items():
    uniq = list(dict.fromkeys(v))
    print("### %s — %d" % (k, len(v)))
    for item in uniq[:12]:
        print("     ", item)
    if len(uniq) > 12:
        print("      ... i %d wiecej" % (len(uniq) - 12))
    print()
