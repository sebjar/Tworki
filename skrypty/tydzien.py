# -*- coding: utf-8 -*-
"""Wypelnia CALY tydzien (28 posilkow) i oglada wynikowa liste zakupow -
tak jak zrobi to czlowiek. Szuka pozycji, ktore po przeliczeniu wygladaja glupio."""
import collections, os, random, shutil, subprocess, sys
import openpyxl

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SRC = r"C:\Users\Sebastian\Documents\Przepisy-planer\Przepisy-planer.xlsx"
WORK = os.path.dirname(SRC)
TEST = os.path.join(WORK, "tydzien.xlsx")
OUT = os.path.join(WORK, "tydzienout")
SOFFICE = r"C:\Program Files\LibreOffice\program\soffice.exe"

wb = openpyxl.load_workbook(SRC)
wp, plan = wb["Przepisy"], wb["Plan"]

# przepisy pogrupowane po kategorii, tylko te z policzonymi makrami
poKat = collections.defaultdict(list)
for r in range(2, wp.max_row + 1):
    n = wp.cell(row=r, column=2).value
    if not n or not wp.cell(row=r, column=12).value:
        continue
    poKat[wp.cell(row=r, column=3).value].append(("P%03d: %s" % (r - 1, n), wp.cell(row=r, column=7).value))

DOPASUJ = {"Śniadanie": ["Śniadanie", "Deser", "Przekąska"],
           "Obiad": ["Obiad", "Zupa"],
           "Kolacja": ["Kolacja", "Obiad", "Sałatka"],
           "Przekąska": ["Przekąska", "Deser", "Sałatka"]}
random.seed(7)
wybrane = {}
for r in range(2, 30):
    posilek = plan.cell(row=r, column=2).value
    if not posilek:
        continue
    pula = [x for k in DOPASUJ.get(posilek, [posilek]) for x in poKat.get(k, [])]
    if not pula:
        continue
    klucz, baza = random.choice(pula)
    porcje = 2
    plan.cell(row=r, column=3, value=klucz)
    plan.cell(row=r, column=4, value=porcje)
    wybrane[r] = (klucz, porcje, baza)
wb.save(TEST)

shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT)
subprocess.run([SOFFICE, "--headless", "--norestore", "--convert-to",
                "xlsx:Calc MS Excel 2007 XML", "--outdir", OUT, TEST],
               capture_output=True, timeout=400)
got = openpyxl.load_workbook(os.path.join(OUT, "tydzien.xlsx"), data_only=True)
gl, gp = got["Lista zakupów"], got["Plan"]

print("Zaplanowano %d posiłków po 2 porcje.\n" % len(wybrane))
print("SUMY DOBOWE [kcal, B, T, W]")
for r in range(2, 9):
    d = gp.cell(row=r, column=10).value
    v = [gp.cell(row=r, column=c).value or 0 for c in (11, 12, 13, 14)]
    print("   %-14s %s" % (d, [round(x) for x in v]))

poz = []
for r in range(2, gl.max_row + 1):
    dz, nm, jed, il = (gl.cell(row=r, column=i).value for i in (1, 2, 3, 4))
    if nm and isinstance(il, (int, float)) and il:
        poz.append((dz, nm, jed, float(il)))
print("\nLISTA ZAKUPÓW: %d pozycji z zerem odfiltrowane, zostaje %d\n" % (224 - len(poz), len(poz)))

# co wyglada glupio na liscie zakupow
GLUPOTY = []
for dz, nm, jed, il in poz:
    if jed == "g" and il > 4000:
        GLUPOTY.append(("Ponad 4 kg jednego produktu", "%s %.0f g" % (nm, il)))
    if jed == "ml" and il > 4000:
        GLUPOTY.append(("Ponad 4 litry", "%s %.0f ml" % (nm, il)))
    if jed == "szt." and il > 40:
        GLUPOTY.append(("Ponad 40 sztuk", "%s %.0f szt." % (nm, il)))
    if jed in ("łyżeczka", "łyżka") and il > 30:
        GLUPOTY.append(("Absurdalna liczba łyżek", "%s %.0f %s" % (nm, il, jed)))
    if il < 0.2:
        GLUPOTY.append(("Ilość poniżej progu kupienia", "%s %.2f %s" % (nm, il, jed)))
    if jed == "ząbek" and il > 60:
        GLUPOTY.append(("Ponad 60 ząbków czosnku", "%s %.0f" % (nm, il)))

if GLUPOTY:
    grup = collections.OrderedDict()
    for k, v in GLUPOTY:
        grup.setdefault(k, []).append(v)
    for k, v in grup.items():
        print("### %s — %d" % (k, len(v)))
        for x in v[:12]:
            print("     ", x)
        print()
else:
    print("Nic na liście zakupów nie wygląda absurdalnie.")

print("\n--- pełna lista, dział po dziale ---")
akt = None
for dz, nm, jed, il in poz:
    if dz != akt:
        akt = dz
        print("\n[%s]" % dz)
    print("   %-32s %8.1f %s" % (nm, il, jed))
