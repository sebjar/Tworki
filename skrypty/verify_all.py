# -*- coding: utf-8 -*-
"""Pelna weryfikacja gotowego skoroszytu - 10 niezaleznych testow."""
import collections, json, os, re, sys
import openpyxl

SP = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SP)
from nutrition import macros as ing_macros, NUTR
from normalize import normalize

# Makra sa teraz formulami, a openpyxl ich nie liczy - czytamy kopie przeliczona
# przez LibreOffice. przelicz() odswieza ja przy kazdym uruchomieniu.
from przelicz import przelicz
P = przelicz()

FAIL, WARN, OK = [], [], []

def bez_id(s):
    """Arkusz Skladniki trzyma "P001: Nazwa" - do porownan potrzebna sama nazwa."""
    return re.sub(r"^P\d{3}:\s*", "", s) if isinstance(s, str) else s



def fail(t, d=""):
    FAIL.append((t, d))


def warn(t, d=""):
    WARN.append((t, d))


def ok(t):
    OK.append(t)


wb = openpyxl.load_workbook(P, data_only=True)   # czytamy WARTOSCI, nie formuly
need = ["Instrukcja", "Ustawienia", "Przepisy", "Składniki", "Plan", "Lista zakupów"]
missing = [s for s in need if s not in wb.sheetnames]
if missing:
    fail("Brak arkuszy", str(missing))
else:
    ok("Wszystkie 6 arkuszy na miejscu")

wp, ws, wl, wpl = wb["Przepisy"], wb["Składniki"], wb["Lista zakupów"], wb["Plan"]

# ---------------------------------------------------------------- dane
rec = {}
for r in range(2, wp.max_row + 1):
    n = wp.cell(row=r, column=2).value
    if not n:
        continue
    rec[n] = dict(
        row=r, cat=wp.cell(row=r, column=3).value, src=wp.cell(row=r, column=4).value,
        link=wp.cell(row=r, column=6).value, serv=wp.cell(row=r, column=7).value,
        ning=wp.cell(row=r, column=8).value or 0, qual=wp.cell(row=r, column=9).value,
        steps=wp.cell(row=r, column=10).value or "", sim=wp.cell(row=r, column=11).value or "",
        kcal=wp.cell(row=r, column=12).value, B=wp.cell(row=r, column=13).value,
        T=wp.cell(row=r, column=14).value, W=wp.cell(row=r, column=15).value,
        msrc=wp.cell(row=r, column=20).value or "")

rows = []
for r in range(2, ws.max_row + 1):
    a, b, c, d, e = (ws.cell(row=r, column=i).value for i in (1, 2, 3, 4, 5))
    if a and b:
        rows.append(dict(row=r, rec=bez_id(a), ing=b, qty=c,
                         unit=d, sec=e, key=a))

shop = []
for r in range(2, wl.max_row + 1):
    a, b, c = (wl.cell(row=r, column=i).value for i in (1, 2, 3))
    if b:
        shop.append(dict(row=r, sec=a, ing=b, unit=c))

# ---------------------------------------------------------------- 1. integralnosc
bad = [x for x in rows if x["rec"] not in rec]
if bad:
    fail("Składnik wskazuje nieistniejący przepis", "%d wierszy" % len(bad))
else:
    ok("Każdy z %d wierszy Składników wskazuje istniejący przepis" % len(rows))

# lista zakupow ma JEDNA jednostke na produkt, skladniki maja jednostki kuchenne
# - porownujemy wiec same nazwy produktow
NIE_KUPUJEMY = {"woda"}
pairs_ing = {x["ing"] for x in rows} - NIE_KUPUJEMY
pairs_shop = {x["ing"] for x in shop}
orphan = pairs_shop - pairs_ing
lost = pairs_ing - pairs_shop
if orphan:
    fail("Pozycja listy zakupów bez pokrycia w Składnikach", "%d: %s" % (len(orphan), list(orphan)[:4]))
else:
    ok("Wszystkie %d pozycji listy zakupów ma pokrycie w Składnikach" % len(shop))
if lost:
    fail("Składnik nieobecny na liście zakupów (nie da się kupić)",
         "%d: %s" % (len(lost), list(lost)[:6]))
else:
    ok("Każdy kupowalny składnik ma dokładnie jeden wiersz na liście zakupów")

# ---------------------------------------------------------------- 2. kategorie
nocat = [n for n, v in rec.items() if not v["cat"]]
if nocat:
    fail("Przepisy bez kategorii", "%d" % len(nocat))
else:
    ok("Wszystkie %d przepisów ma kategorię" % len(rec))

# ---------------------------------------------------------------- 3. porcje
badserv = [(n, v["serv"]) for n, v in rec.items()
           if not isinstance(v["serv"], (int, float)) or not (0 < v["serv"] <= 24)]
if badserv:
    fail("Nieprawidłowa liczba porcji", str(badserv[:5]))
else:
    ok("Liczba porcji poprawna wszędzie (1-24)")

# ---------------------------------------------------------------- 4. ilosci
MAXQ = {"g": 2000, "kg": 3, "ml": 2000, "l": 3, "szt.": 20, "łyżka": 15, "łyżeczka": 12,
        "szklanka": 6, "ząbek": 15, "puszka": 4, "opak.": 4, "garść": 5, "szczypta": 5,
        "plaster": 16, "pęczek": 3, "główka": 3, "dag": 100, "oz": 40, "lbs": 4}
big = [x for x in rows if isinstance(x["qty"], (int, float))
       and x["unit"] in MAXQ and x["qty"] > MAXQ[x["unit"]]]
noqty = [x for x in rows if not isinstance(x["qty"], (int, float)) or x["qty"] <= 0]
if noqty:
    fail("Brak/zerowa ilość", "%d wierszy" % len(noqty))
else:
    ok("Każdy składnik ma dodatnią ilość liczbową")
if big:
    warn("Ilości powyżej progu zdrowego rozsądku", "%d: %s" %
         (len(big), ["%s %s %s (%s)" % (x["qty"], x["unit"], x["ing"][:20], x["rec"][:18])
                     for x in big[:5]]))
else:
    ok("Żadna ilość nie przekracza progu zdrowego rozsądku")

# ---------------------------------------------------------------- 5. dzialy
inne = collections.Counter(x["ing"] for x in rows if x["sec"] == "Inne")
if inne:
    warn("Składniki bez działu sklepu", "%d różnych" % len(inne))
else:
    ok("Każdy składnik ma przypisany dział sklepu")

# ---------------------------------------------------------------- 6. duplikaty w przepisie
dup = [k for k, c in collections.Counter((x["rec"], x["ing"], x["unit"]) for x in rows).items()
       if c > 1]
if dup:
    fail("Ten sam składnik dwa razy w jednym przepisie", "%d" % len(dup))
else:
    ok("Brak powtórzonych składników w obrębie przepisu")

# ---------------------------------------------------------------- 7. makra: Atwater
# kcal powinno sie zgadzac z 4*B + 9*T + 4*W
atw_bad = []
for n, v in rec.items():
    if not all(isinstance(v[k], (int, float)) for k in ("kcal", "B", "T", "W")):
        continue
    est = 4 * v["B"] + 9 * v["T"] + 4 * v["W"]
    if v["kcal"] and abs(est - v["kcal"]) / v["kcal"] > 0.25:
        atw_bad.append((n, v["kcal"], round(est), v["msrc"]))
n_full = sum(1 for v in rec.values()
             if all(isinstance(v[k], (int, float)) for k in ("kcal", "B", "T", "W")))
if atw_bad:
    warn("Makra niespójne ze wzorem Atwatera (>25%%)", "%d z %d" % (len(atw_bad), n_full))
    for x in atw_bad[:8]:
        WARN.append(("   %s: kcal=%s, z makr=%s [%s]" % (x[0][:40], x[1], x[2], x[3]), ""))
else:
    ok("Makra zgodne ze wzorem Atwatera we wszystkich %d przepisach" % n_full)

# ---------------------------------------------------------------- 8. makra: przeliczenie
mism = []
for n, v in rec.items():
    if not isinstance(v["kcal"], (int, float)):
        continue
    tot = 0.0
    for x in rows:
        if x["rec"] != n:
            continue
        m = ing_macros(x["ing"], x["unit"], x["qty"])
        if m:
            tot += m[0]
    mine = round(tot / v["serv"])
    if abs(mine - v["kcal"]) > 2:
        mism.append((n, v["kcal"], mine))
if mism:
    fail("kcal w arkuszu != przeliczenie ze składników", "%d: %s" % (len(mism), mism[:4]))
else:
    ok("Wyliczone kcal zgadzają się z sumą składników co do jednostki")

# ---------------------------------------------------------------- 9. pokrycie tabeli
nonutr = collections.Counter(x["ing"] for x in rows if x["ing"] not in NUTR)
if nonutr:
    warn("Składniki bez wartości odżywczych", "%d różnych: %s"
         % (len(nonutr), list(nonutr)[:6]))
else:
    ok("Wszystkie %d składników ma wartości odżywcze" % len({x["ing"] for x in rows}))

# ---------------------------------------------------------------- 10. zrodlo, kompletnosc
orig = json.load(open(SP + "/ing_index.json", encoding="utf-8"))
orig_links = {x["link"].split("?")[0] for x in orig if x.get("link")}
have_links = {(v["link"] or "").split("?")[0] for v in rec.values()}
# film usuniety przez autora - przepis jest, ale z linkiem do jego nowszej wersji (P080, 2.11.2026)
ZASTAPIONE = {"https://www.tiktok.com/@coocharz/video/7209232328965491974":
              "https://www.tiktok.com/@coocharz/video/7457157431211183382"}
have_links |= {stary for stary, nowy in ZASTAPIONE.items() if nowy in have_links}
miss = orig_links - have_links
if miss:
    fail("Przepisy z Twojego pliku, których nie ma w skoroszycie", "%d" % len(miss))
else:
    ok("Wszystkie %d linków z jedzenie.xlsx obecne" % len(orig_links))

nostep = [n for n, v in rec.items() if v["ning"] and not v["steps"]]
noing = [n for n, v in rec.items() if v["steps"] and not v["ning"]]
if nostep:
    warn("Ma składniki, brak przygotowania", "%d: %s" % (len(nostep), nostep[:3]))
if noing:
    warn("Ma przygotowanie, brak składników", "%d: %s" % (len(noing), noing[:3]))

# ---------------------------------------------------------------- raport
print("=" * 74)
print("PRZESZLO (%d):" % len(OK))
for t in OK:
    print("   OK   %s" % t)
print()
print("DO UWAGI (%d):" % len(WARN))
for t, d in WARN:
    print("   !    %s %s" % (t, d))
print()
print("BLEDY (%d):" % len(FAIL))
for t, d in FAIL:
    print("   XX   %s %s" % (t, d))
print("=" * 74)
print("Przepisow: %d | wierszy skladnikow: %d | pozycji zakupowych: %d"
      % (len(rec), len(rows), len(shop)))
print("Kategorie:", dict(collections.Counter(v["cat"] for v in rec.values())))
print("Opracowanie:", dict(collections.Counter(v["qual"] for v in rec.values())))
print("Zrodlo makr:", dict(collections.Counter(v["msrc"] or "brak" for v in rec.values())))
