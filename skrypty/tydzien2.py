# -*- coding: utf-8 -*-
"""Tydzien tak, jak go realnie zaplanujecie: obiad gotowany raz i jedzony dwa dni,
sniadanie codziennie. Sprawdza, czy Plan, lista zakupow i podzial 60/40 sie zgadzaja."""
import os, shutil, subprocess, sys
import openpyxl

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from przelicz import przelicz

SRC = r"C:\Users\Sebastian\Documents\Przepisy-planer\Przepisy-planer.xlsx"
WORK = os.path.dirname(SRC)
TEST = os.path.join(WORK, "tydzien2.xlsx")
OUT = os.path.join(WORK, "tydzien2out")
SOFFICE = r"C:\Program Files\LibreOffice\program\soffice.exe"
POSILKI = ["Śniadanie", "Obiad", "Kolacja", "Przekąska"]

wv = openpyxl.load_workbook(przelicz(), data_only=True)
pv, uv = wv["Przepisy"], wv["Ustawienia"]
TY, ONA = uv["N8"].value, uv["O8"].value
SPLIT_T, SPLIT_O = uv["N10"].value, uv["O10"].value

obiady, sniadania = [], []
for r in range(2, pv.max_row + 1):
    nm, kat, y, odg = (pv.cell(row=r, column=c).value for c in (2, 3, 25, 32))
    if not nm or not isinstance(y, (int, float)):
        continue
    wpis = dict(id=pv.cell(row=r, column=1).value, nazwa=nm, y=y, g=pv.cell(row=r, column=7).value,
                kcal=pv.cell(row=r, column=12).value)
    if kat == "Obiad" and (odg or "").startswith("Tak") and len(obiady) < 3:
        obiady.append(wpis)
    if kat == "Śniadanie" and len(sniadania) < 2:
        sniadania.append(wpis)

wb = openpyxl.load_workbook(SRC)
plan = wb["Plan"]


def wpisz(dzien, posilek, w):
    row = 2 + dzien * 4 + POSILKI.index(posilek)
    plan.cell(row=row, column=3, value="%s: %s" % (w["id"], w["nazwa"]))
    plan.cell(row=row, column=4, value=w["y"])


for d in range(6):                              # pon-sob: obiad dwa dni z jednego garnka
    wpisz(d, "Obiad", obiady[d // 2])
    wpisz(d, "Śniadanie", sniadania[d % 2])
wb.save(TEST)

shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT)
subprocess.run([SOFFICE, "--headless", "--norestore", "--convert-to",
                "xlsx:Calc MS Excel 2007 XML", "--outdir", OUT, TEST],
               capture_output=True, timeout=500)
g = openpyxl.load_workbook(os.path.join(OUT, "tydzien2.xlsx"), data_only=True)

ERR = ("#REF!", "#NAME?", "#VALUE!", "#DIV/0!", "#N/A", "#NULL!", "#NUM!", "Err:")
bledy = [(s.title, c.coordinate) for s in g.worksheets for rr in s.iter_rows() for c in rr
         if isinstance(c.value, str) and any(c.value.startswith(e) for e in ERR)]
print("BLEDY FORMUL:", len(bledy), bledy[:4])

print("\nOBIADY Z JEDNEGO GARNKA (każdy wpisany w 2 kolejne dni):")
gs = g["Składniki"]
zle_garnki = 0
for w in obiady:
    klucz = "%s: %s" % (w["id"], w["nazwa"])
    wiersze = [r for r in range(2, gs.max_row + 1) if gs.cell(row=r, column=1).value == klucz]
    r0 = wiersze[0]
    qty, plan_qty = gs.cell(row=r0, column=3).value, gs.cell(row=r0, column=8).value
    ocz = qty * 2 * w["y"] / w["g"]
    ok = abs((plan_qty or 0) - ocz) < 0.01
    zle_garnki += 0 if ok else 1
    print("   %-40s dziennie %-4s -> garnek %-4s porcji | %s: %.3g (oczekiwane %.3g) %s"
          % (w["nazwa"][:40], w["y"], 2 * w["y"], gs.cell(row=r0, column=2).value,
             plan_qty or 0, ocz, "OK" if ok else "<<< ZLE"))

gp = g["Plan"]
print("\nDZIEŃ PO DNIU (śniadanie 25% + obiad 35% = cel ok. 60% dnia):")
zle_podzial = 0
for r in range(2, 9):
    dz, raz, ty, ona, opis = (gp.cell(row=r, column=c).value for c in (10, 11, 17, 18, 19))
    if not raz:
        print("   %-13s (nic nie zaplanowane)" % dz)
        continue
    if abs(ty - raz * SPLIT_T) > 1 or abs(ona - raz * SPLIT_O) > 1:
        zle_podzial += 1
    print("   %-13s razem %5.0f | Ty %5.0f | Ona %5.0f | %s" % (dz, raz, ty, ona, opis))
print("\nGarnków policzonych źle: %d | dni z podziałem innym niż 60/40: %d"
      % (zle_garnki, zle_podzial))
shutil.rmtree(OUT, ignore_errors=True)
os.remove(TEST)
