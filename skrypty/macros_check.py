# -*- coding: utf-8 -*-
"""Liczy makra ze skladnikow i porownuje z tym, co podal autor."""
import collections, json, os, re, sys
import openpyxl

SP = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SP)
from nutrition import macros, NUTR

P = r"C:\Users\Sebastian\Documents\Przepisy-planer\Przepisy-planer.xlsx"

# --- 1) policz ze skladnikow
wb = openpyxl.load_workbook(P)
wp, ws = wb["Przepisy"], wb["Składniki"]
serv, link = {}, {}
for r in range(2, wp.max_row + 1):
    n = wp.cell(row=r, column=2).value
    if n:
        serv[n] = wp.cell(row=r, column=7).value or 2
        link[n] = wp.cell(row=r, column=6).value or ""

tot = collections.defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])
missing = collections.Counter()
nrows = collections.Counter()
for r in range(2, ws.max_row + 1):
    rec, ing, qty, unit = (ws.cell(row=r, column=i).value for i in (1, 2, 3, 4))
    if not (rec and ing) or not isinstance(qty, (int, float)):
        continue
    nrows[rec] += 1
    m = macros(ing, unit, qty)
    if m is None:
        missing[ing] += 1
        continue
    for i in range(4):
        tot[rec][i] += m[i]

calc = {}
for rec, v in tot.items():
    s = float(serv.get(rec) or 2)
    if s > 0 and nrows[rec]:
        calc[rec] = tuple(round(x / s) for x in v)

# --- 2) makra podane przez autora
rows = json.load(open(SP + "/curate_input.json", encoding="utf-8"))
by_link = {}
for x in rows:
    if x["link"]:
        by_link[x["link"]] = " ".join(filter(None, [x["cap"], x["blog"] or ""]))

PATS = [
    # "597 Calories | 59g Protein | 52g Carbs | 16g Fat"
    re.compile(r"(\d{2,4})\s*(?:calories|kcal)[^\d]{0,20}(\d{1,3})\s*g?\s*(?:protein|p\b)"
               r"[^\d]{0,20}(\d{1,3})\s*g?\s*(?:carbs?|c\b)[^\d]{0,20}(\d{1,3})\s*g?\s*(?:fat|f\b)",
               re.I),
    # "Per Meal: 493 calories 52g P | 64g C | 3g F"
    re.compile(r"(\d{2,4})\s*(?:calories|kcal)\s*(\d{1,3})\s*g?\s*P\s*\|\s*(\d{1,3})\s*g?\s*C"
               r"\s*\|\s*(\d{1,3})\s*g?\s*F", re.I),
    # "379 kcal 21B 22T 32W"  (PL: bialko/tluszcz/wegle)
    re.compile(r"(\d{2,4})\s*kcal\s*(\d{1,3})\s*B\W{0,3}(\d{1,3})\s*T\W{0,3}(\d{1,3})\s*W", re.I),
    # "610 kcal 40 g bialka 68 g wegli 22 g tluszczow"
    re.compile(r"(\d{2,4})\s*kcal[^\d]{0,12}(\d{1,3})\s*g\s*bia[łl]k\w*[^\d]{0,18}"
               r"(\d{1,3})\s*g\s*w[ęe]glowodan\w*[^\d]{0,18}(\d{1,3})\s*g\s*t[łl]uszcz\w*", re.I),
]
KCAL_ONLY = re.compile(r"(\d{2,4})\s*(?:kcal|calories)", re.I)


def author_macros(txt):
    for i, pat in enumerate(PATS):
        m = pat.search(txt)
        if m:
            k, a, b, c = (int(x) for x in m.groups())
            if i == 3:      # kcal, bialko, wegle, tluszcz
                return k, a, c, b
            if i == 2:      # kcal, B, T, W
                return k, a, b, c
            return k, a, c, b   # kcal, protein, fat, carbs  (wzorce 0 i 1: P, C, F)
    return None


# --- 3) porownanie
print("Skladnikow bez wartosci odzywczych w tabeli: %d roznych, %d wierszy"
      % (len(missing), sum(missing.values())))
for n, c in missing.most_common(12):
    print("    %2d  %s" % (c, n))

cmp_rows = []
for rec, txt in by_link.items():
    pass
name_by_link = {link[n]: n for n in link if link[n]}
for lk, txt in by_link.items():
    rec = name_by_link.get(lk)
    if not rec or rec not in calc:
        continue
    a = author_macros(txt)
    if not a:
        continue
    c = calc[rec]
    cmp_rows.append((rec, a, c))

print("\nPOROWNANIE: %d przepisow ma makra od autora i policzone przeze mnie\n" % len(cmp_rows))
print("%-42s %-22s %-22s %s" % ("przepis", "autor (kcal/B/T/W)", "moje (kcal/B/T/W)", "roznica kcal"))
diffs = []
for rec, a, c in sorted(cmp_rows, key=lambda x: -abs(x[2][0] - x[1][0])):
    d = (c[0] - a[0]) / a[0] * 100 if a[0] else 0
    diffs.append(abs(d))
    print("%-42s %-22s %-22s %+6.0f%%"
          % (rec[:42], "%s/%s/%s/%s" % a, "%s/%s/%s/%s" % c, d))
if diffs:
    diffs.sort()
    print("\nMediana odchylenia kcal: %.0f%%   |  w granicach 20%%: %d/%d  |  >40%%: %d"
          % (diffs[len(diffs) // 2],
             sum(1 for d in diffs if d <= 20), len(diffs),
             sum(1 for d in diffs if d > 40)))
