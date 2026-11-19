# -*- coding: utf-8 -*-
"""Szuka rzeczy formalnie poprawnych, ale bez sensu dla czlowieka."""
import collections, os, re, sys
import openpyxl

SP = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SP)
from nutrition import grams

# Makra sa teraz formulami, a openpyxl ich nie liczy - czytamy kopie przeliczona
# przez LibreOffice. przelicz() odswieza ja przy kazdym uruchomieniu.
from przelicz import przelicz
P = przelicz()

wb = openpyxl.load_workbook(P, data_only=True)   # czytamy WARTOSCI, nie formuly
wp, ws, wl = wb["Przepisy"], wb["Składniki"], wb["Lista zakupów"]

def bez_id(s):
    """Arkusz Skladniki trzyma "P001: Nazwa" - do porownan potrzebna sama nazwa."""
    return re.sub(r"^P\d{3}:\s*", "", s) if isinstance(s, str) else s


rec = {}
for r in range(2, wp.max_row + 1):
    n = wp.cell(row=r, column=2).value
    if n:
        rec[n] = dict(row=r, cat=wp.cell(row=r, column=3).value,
                      serv=wp.cell(row=r, column=7).value or 0,
                      ning=wp.cell(row=r, column=8).value or 0,
                      kcal=wp.cell(row=r, column=12).value,
                      sim=wp.cell(row=r, column=11).value or "")
ing = collections.defaultdict(list)
for r in range(2, ws.max_row + 1):
    a, b, q, u = (ws.cell(row=r, column=i).value for i in (1, 2, 3, 4))
    if a and b:
        ing[bez_id(a)].append((b, q, u))

P_ = collections.OrderedDict()


def add(k, v):
    P_.setdefault(k, []).append(v)


# 1) nazwy przepisow, ktore nie sa nazwami dania
BAD_NAME = re.compile(r"(?i)(^bez |^delish|^\?|zapisz|obserwuj|^przepis[:\s]*$|"
                      r"^\W|^[a-z]{1,3}$|\.\.\.$|^(?:tu nie ma|najlepszy czas|też jecie))")
for n, v in rec.items():
    if BAD_NAME.search(n) or len(n) > 60:
        add("Nazwa nie brzmi jak nazwa dania", "%-60s" % n[:60])

# 2) skladniki, ktore nie wygladaja na produkt
BAD_ING = re.compile(r"(?i)(\d|^\W|^[a-z]{1,2}$|kcal|porcj|makro|minut)")
seen_ing = collections.Counter()
for n, items in ing.items():
    for b, q, u in items:
        seen_ing[b] += 1
for b, c in seen_ing.items():
    if BAD_ING.search(b) and not re.match(r"(?i)^(śmietana \d|mąka|tortilla)", b):
        add("Podejrzana nazwa składnika", "%-40s (%dx)" % (b[:40], c))

# 3) kcal na porcje poza rozsadkiem
for n, v in rec.items():
    k = v["kcal"]
    if not isinstance(k, (int, float)):
        continue
    cat = v["cat"]
    if cat in ("Sos / dodatek", "Napój"):
        lo, hi = 10, 400
    elif cat in ("Przekąska", "Deser"):
        lo, hi = 60, 700
    else:
        lo, hi = 150, 1100
    if k < lo:
        add("Bardzo mało kcal na porcję", "%-46s %s kcal [%s]" % (n[:46], k, cat))
    elif k > hi:
        add("Bardzo dużo kcal na porcję", "%-46s %s kcal [%s]" % (n[:46], k, cat))

# 4) masa porcji poza rozsadkiem
for n, items in ing.items():
    v = rec.get(n)
    if not v or not v["serv"]:
        continue
    tot = sum(grams(b, u, q) for b, q, u in items if isinstance(q, (int, float)))
    per = tot / v["serv"]
    # porcja deseru, sosu czy przekaski z zalozenia jest mala
    lekkie = v["cat"] in ("Deser", "Sos / dodatek", "Napój", "Przekąska")
    if per < (40 if lekkie else 120):
        add("Porcja waży podejrzanie mało", "%-46s %.0f g/porcję" % (n[:46], per))
    elif per > 1300:
        add("Porcja waży podejrzanie dużo", "%-46s %.0f g/porcję" % (n[:46], per))

# 5) przepis z 1-2 skladnikami, ale nie sos
for n, v in rec.items():
    if 0 < v["ning"] <= 2 and v["cat"] not in ("Sos / dodatek", "Napój"):
        add("Bardzo mało składników", "%-46s %d [%s]" % (n[:46], v["ning"], v["cat"]))

# 6) rzeczy, ktorych sie nie kupuje, na liscie zakupow
# wode gazowana i lod kupuje sie normalnie - zostaje sama kranowka
NOBUY = {"woda"}
for r in range(2, wl.max_row + 1):
    b = wl.cell(row=r, column=2).value
    if b and b.lower() in NOBUY:
        add("Na liście zakupów rzecz, której się nie kupuje", b)

# 7) kategoria kloci sie z nazwa
CAT_HINT = [("Sałatka", r"(?i)^sałatk|^salad"), ("Zupa", r"(?i)\bzupa\b|harira"),
            ("Deser", r"(?i)\blody\b|deser|sernik"), ("Śniadanie", r"(?i)owsianka|naleśnik")]
for n, v in rec.items():
    for cat, pat in CAT_HINT:
        if re.search(pat, n) and v["cat"] != cat:
            add("Kategoria kłóci się z nazwą", "%-46s ma [%s], nazwa sugeruje [%s]"
                % (n[:46], v["cat"], cat))

# 8) ten sam skladnik w bardzo roznych jednostkach miedzy przepisami
byname = collections.defaultdict(set)
for n, items in ing.items():
    for b, q, u in items:
        byname[b].add(u)
for b, us in byname.items():
    if len(us) >= 4:
        add("Składnik w wielu różnych jednostkach", "%-34s %s" % (b[:34], sorted(us)))

print("Przepisow: %d | roznych skladnikow: %d\n" % (len(rec), len(seen_ing)))
if not P_:
    print("Nic podejrzanego.")
for k, v in P_.items():
    print("### %s — %d" % (k, len(v)))
    for x in v[:14]:
        print("     ", x)
    if len(v) > 14:
        print("      ... i %d wiecej" % (len(v) - 14))
    print()
