# -*- coding: utf-8 -*-
"""Wypelnia Plan czterema przepisami, przelicza w LibreOffice i porownuje z reczna kalkulacja.
Sprawdza: bledy formul, liste zakupow i sumy dobowe wszystkich czterech makr."""
import collections, os, re, shutil, subprocess, sys
import openpyxl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nutrition import grams as _g

SRC = r"C:\Users\Sebastian\Documents\Przepisy-planer\Przepisy-planer.xlsx"
WORK = os.path.dirname(SRC)
TEST = os.path.join(WORK, "testplan.xlsx")
OUTDIR = os.path.join(WORK, "recalcout")
SOFFICE = r"C:\Program Files\LibreOffice\program\soffice.exe"

MACRO_COLS = (12, 13, 14, 15)   # Przepisy: kcal, B, T, W
ROW_COLS = (5, 6, 7, 8)         # Plan, wiersze
SUM_COLS = (11, 12, 13, 14)     # Plan, blok podsumowania

wb = openpyxl.load_workbook(SRC)                 # wersja z formulami - do niej wpisujemy Plan
wp, ws, plan = wb["Przepisy"], wb["Składniki"], wb["Plan"]
wl_src = wb["Lista zakupów"]
# makra to teraz formuly, wiec wartosci do porownania bierzemy z przeliczonej kopii
from przelicz import przelicz
wv = openpyxl.load_workbook(przelicz(), data_only=True)
wpv = wv["Przepisy"]

serv, mac, key, light = {}, {}, {}, {}
for r in range(2, wp.max_row + 1):
    n = wp.cell(row=r, column=2).value
    if not n:
        continue
    serv[n] = float(wp.cell(row=r, column=7).value or 0)
    light[n] = wpv.cell(row=r, column=21).value
    mac[n] = [wpv.cell(row=r, column=c).value for c in MACRO_COLS]
    # ten sam klucz co formula w kolumnie A: "P001: Nazwa"
    key[n] = "P%03d: %s" % (r - 1, n)

rows = []
for r in range(2, ws.max_row + 1):
    a, b, c, d = (ws.cell(row=r, column=i).value for i in (1, 2, 3, 4))
    if a and b and isinstance(c, (int, float)):
        rows.append((re.sub(r"^P\d{3}:\s*", "", a), b, float(c), d))

pick = []
for n in serv:
    if serv[n] >= 2 and all(isinstance(v, (int, float)) for v in mac[n]):
        pick.append((n, serv[n] * (2 if len(pick) % 2 == 0 else 1)))
    if len(pick) == 4:
        break

slots = [(r, plan.cell(row=r, column=1).value) for r in (2, 7, 12, 18)]
mult = {}
for (row, day), (n, porcje) in zip(slots, pick):
    plan.cell(row=row, column=3, value=key[n])
    plan.cell(row=row, column=4, value=porcje)
    mult[n] = porcje / serv[n]
wb.save(TEST)

# oczekiwana lista zakupow: sumujemy gramy i dzielimy przez wage jednostki podstawowej
prim = {}
for r in range(2, wl_src.max_row + 1):
    b, u = (wl_src.cell(row=r, column=i).value for i in (2, 3))
    if b:
        prim[b] = u
exp_g = collections.defaultdict(float)
for a, b, c, d in rows:
    if a in mult:
        exp_g[b] += _g(b, d, c) * mult[a]
exp_ing = {}
for b, g in exp_g.items():
    if b not in prim:
        continue
    one = _g(b, prim[b], 1) or 1
    exp_ing[(b, prim[b])] = round(g / one, 1)
exp_day = {}
for (row, day), (n, porcje) in zip(slots, pick):
    exp_day[day] = [porcje * v for v in mac[n]]

shutil.rmtree(OUTDIR, ignore_errors=True)
os.makedirs(OUTDIR)
subprocess.run([SOFFICE, "--headless", "--norestore", "--convert-to",
                "xlsx:Calc MS Excel 2007 XML", "--outdir", OUTDIR, TEST],
               capture_output=True, timeout=300)
got = openpyxl.load_workbook(os.path.join(OUTDIR, "testplan.xlsx"), data_only=True)

ERR = ("#REF!", "#NAME?", "#VALUE!", "#DIV/0!", "#N/A", "#NULL!", "#NUM!", "Err:")
bad = [(s.title, c.coordinate, c.value) for s in got.worksheets for rr in s.iter_rows()
       for c in rr if isinstance(c.value, str) and any(c.value.startswith(e) for e in ERR)]

print("Test na 4 przepisach:")
for (row, day), (n, p) in zip(slots, pick):
    print("   %-12s %-42s %g porcji (baza %g)" % (day, n[:42], p, serv[n]))
print("\nBLEDY FORMUL: %d" % len(bad))
for b in bad[:6]:
    print("   ", b)

gl = got["Lista zakupów"]
act = {}
for r in range(2, gl.max_row + 1):
    n, u, q = (gl.cell(row=r, column=i).value for i in (2, 3, 4))
    if n and isinstance(q, (int, float)) and q:
        act[(n, u)] = round(float(q), 1)
exp = {k: v for k, v in exp_ing.items() if v}
diff = [(k, exp.get(k), act.get(k)) for k in set(exp) | set(act)
        if abs((exp.get(k) or 0) - (act.get(k) or 0)) > 0.15]
print("\nLISTA ZAKUPOW: oczekiwano %d pozycji, jest %d, rozbieznosci: %d"
      % (len(exp), len(act), len(diff)))
for k, e, a in diff[:6]:
    print("   %-40s oczekiwano %s, jest %s" % (str(k)[:40], e, a))

gp = got["Plan"]
print("\nWIERSZE PLANU [kcal, bialko, tluszcz, wegle]:")
for r in range(2, 30):
    if gp.cell(row=r, column=3).value:
        print("   %-12s %-38s porcje=%-5s %s"
              % (gp.cell(row=r, column=1).value,
                 str(gp.cell(row=r, column=3).value)[:38],
                 gp.cell(row=r, column=4).value,
                 [gp.cell(row=r, column=c).value for c in ROW_COLS]))

print("\nSUMY DOBOWE [kcal, bialko, tluszcz, wegle]:")
nbad = 0
for r in range(2, 9):
    d = gp.cell(row=r, column=10).value
    g = [gp.cell(row=r, column=c).value or 0 for c in SUM_COLS]
    e = exp_day.get(d, [0, 0, 0, 0])
    flag = ""
    if any(abs(gv - ev) > 1 for gv, ev in zip(g, e)):
        flag = "  <-- ROZNICA, oczekiwano %s" % [round(x) for x in e]
        nbad += 1
    print("   %-14s %-28s%s" % (d, [round(x) for x in g], flag))
print("\nSumy dobowe niezgodne: %d" % nbad)

shutil.rmtree(OUTDIR, ignore_errors=True)
os.remove(TEST)
