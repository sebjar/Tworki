# -*- coding: utf-8 -*-
"""Wypelnia Plan testowo, przelicza w LibreOffice i porownuje z reczna kalkulacja."""
import os, shutil, subprocess, collections, sys
import openpyxl

SP = os.path.dirname(os.path.abspath(__file__))
SRC = r"C:\Users\Sebastian\Documents\Przepisy-planer\Przepisy-planer.xlsx"
WORK = os.path.dirname(SRC)
TEST = os.path.join(WORK, "testplan.xlsx")
OUTDIR = os.path.join(WORK, "recalcout")
SOFFICE = r"C:\Program Files\LibreOffice\program\soffice.exe"

# 1) znajdz dwa przepisy dzielace skladnik
wb = openpyxl.load_workbook(SRC)
ws = wb["Składniki"]
rows = []
for r in range(2, ws.max_row + 1):
    a, b, c, d = (ws.cell(row=r, column=i).value for i in (1, 2, 3, 4))
    if a and b:
        rows.append((a, b, float(c or 0), d))
by_ing = collections.defaultdict(set)
for a, b, c, d in rows:
    by_ing[(b, d)].add(a)
shared = [(k, v) for k, v in by_ing.items() if len(v) >= 2]
shared.sort(key=lambda kv: -len(kv[1]))
(ing, unit), recs = shared[0]
r1, r2 = sorted(recs)[:2]

serv = {}
wp = wb["Przepisy"]
for r in range(2, wp.max_row + 1):
    n = wp.cell(row=r, column=2).value
    if n:
        serv[n] = float(wp.cell(row=r, column=7).value or 0)

# 2) wpisz plan: r1 na podwojnych porcjach, r2 na porcjach bazowych
plan = wb["Plan"]
plan.cell(row=2, column=3, value=r1)
plan.cell(row=2, column=4, value=serv[r1] * 2)
plan.cell(row=6, column=3, value=r2)
plan.cell(row=6, column=4, value=serv[r2])
wb.save(TEST)

# 3) oczekiwane ilosci
mult = {r1: 2.0, r2: 1.0}
expected = collections.defaultdict(float)
for a, b, c, d in rows:
    if a in mult:
        expected[(b, d)] += c * mult[a]

# 4) przelicz
shutil.rmtree(OUTDIR, ignore_errors=True)
os.makedirs(OUTDIR)
p = subprocess.run([SOFFICE, "--headless", "--norestore", "--convert-to",
                    "xlsx:Calc MS Excel 2007 XML", "--outdir", OUTDIR, TEST],
                   capture_output=True, timeout=300)
print("rc=%s out=%r err=%r" % (p.returncode, p.stdout[-300:], p.stderr[-300:]))
print("outdir ->", os.listdir(OUTDIR))
got = openpyxl.load_workbook(os.path.join(OUTDIR, os.path.basename(TEST)), data_only=True)

ERR = ("#REF!", "#NAME?", "#VALUE!", "#DIV/0!", "#N/A", "#NULL!", "#NUM!", "Err:")
bad = [(s.title, c.coordinate, c.value) for s in got.worksheets for row in s.iter_rows()
       for c in row if isinstance(c.value, str) and any(c.value.startswith(e) for e in ERR)]
print("BLEDY FORMUL: %d" % len(bad))
for b in bad[:10]:
    print("   ", b)

gl = got["Lista zakupów"]
actual = {}
for r in range(2, gl.max_row + 1):
    n, u, q = gl.cell(row=r, column=2).value, gl.cell(row=r, column=3).value, gl.cell(row=r, column=4).value
    if n and isinstance(q, (int, float)) and q:
        actual[(n, u)] = round(float(q), 3)

exp = {k: round(v, 3) for k, v in expected.items() if v}
print("\nTEST: %s x2 porcje + %s x1 porcja" % (r1[:34], r2[:34]))
print("Wspolny skladnik: %s (%s), wystepuje w %d przepisach" % (ing, unit, len(recs)))
print("Oczekiwanych pozycji: %d, na liscie: %d" % (len(exp), len(actual)))
diff = [(k, exp.get(k), actual.get(k)) for k in set(exp) | set(actual)
        if abs((exp.get(k) or 0) - (actual.get(k) or 0)) > 0.01]
print("ROZBIEZNOSCI: %d" % len(diff))
for k, e, a in diff[:10]:
    print("   %-34s oczekiwano %s, jest %s" % (str(k)[:34], e, a))
print("\nPROBKA (oczekiwane vs arkusz):")
for k in sorted(exp, key=lambda k: -exp[k])[:8]:
    print("   %-30s %-10s %8s | %s" % (k[0][:30], k[1], exp[k], actual.get(k)))
print("\nWspolny skladnik '%s': oczekiwano %s, arkusz: %s"
      % (ing, exp.get((ing, unit)), actual.get((ing, unit))))
