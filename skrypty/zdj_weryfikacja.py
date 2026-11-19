# -*- coding: utf-8 -*-
"""Weryfikacja zdjec i calego skoroszytu po ich dodaniu.
A. kazde zdjecie w arkuszu siedzi w wierszu swojego przepisu, w dobrej kolejnosci i to jest ten plik
B. poza zdjeciami nic sie nie zmienilo wzgledem kopii sprzed zdjec (wartosci i formuly, wszystkie arkusze)
C. zdjecia pochodza z linku przepisu (zdj_linki.json == kolumna Link)
D. pliki: kwadratowe, co najmniej 280 px, niepuste, zgodne z zdjecia.json, bez powtorek miedzy roznymi przepisami"""
import glob, io, json, os, re, sys
import cv2
import numpy as np
import openpyxl
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
OUT = r"C:\Users\Sebastian\Documents\Przepisy-planer\Przepisy-planer.xlsx"
EMU = 9525
BLEDY = []


def blad(*a):
    BLEDY.append(" ".join(str(x) for x in a))
    print("  BŁĄD", *a)


def dh(im):
    g = cv2.resize(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY), (17, 16), interpolation=cv2.INTER_AREA)
    return (g[:, 1:] > g[:, :-1]).flatten()


def z_pliku(p):
    return cv2.imread(p)


def z_bajtow(b):
    return cv2.cvtColor(np.array(Image.open(io.BytesIO(b)).convert("RGB")), cv2.COLOR_RGB2BGR)


wb = openpyxl.load_workbook(OUT)
stary = openpyxl.load_workbook(sys.argv[1] if len(sys.argv) > 1 else "_przed_zdjeciami.xlsx")
pliki = {os.path.basename(p)[:-4]: p for p in glob.glob("zdjecia/P*_*.jpg")}

# ---- A
print("A. Zdjęcia w arkuszu")
for nazwa in ("Przepisy", "Sugestie"):
    ws = wb[nazwa]
    wiersz_pid = {r: ws.cell(r, 1).value for r in range(2, ws.max_row + 1)}
    w_arkuszu = {}
    for img in ws._images:
        a = img.anchor
        r = a._from.row + 1
        pid = wiersz_pid.get(r)
        if a.to.row != a._from.row or a._from.col != 1 or a.to.col != 1:
            blad(nazwa, pid, "zdjęcie wychodzi poza komórkę B%d" % r)
        if a._from.rowOff / EMU < 18:
            blad(nazwa, pid, "zdjęcie zasłania nazwę przepisu")
        w_arkuszu.setdefault(pid, []).append((a._from.colOff, z_bajtow(img._data())))
    oczekiwane = {r[1]: sorted(k for k in pliki if k.startswith(r[1] + "_")) for r in wiersz_pid.items() if r[1]}
    for pid, klucze in oczekiwane.items():
        jest = sorted(w_arkuszu.get(pid, []), key=lambda t: t[0])
        if len(jest) != len(klucze):
            blad(nazwa, pid, "w arkuszu %d zdjęć, plików %d" % (len(jest), len(klucze)))
            continue
        for (_x, im), k in zip(jest, klucze):
            d = np.count_nonzero(dh(im) != dh(z_pliku(pliki[k])))
            if d > 20:
                blad(nazwa, pid, "zdjęcie na miejscu %s nie zgadza się z plikiem (odległość %d)" % (k[-1], d))
    obce = set(w_arkuszu) - set(oczekiwane)
    if obce:
        blad(nazwa, "zdjęcia w wierszach bez przepisu:", obce)
    h_zle = [ws.cell(r, 1).value for r in wiersz_pid if wiersz_pid[r] and oczekiwane.get(wiersz_pid[r])
             and (ws.row_dimensions[r].height or 15) < 133]
    if h_zle:
        blad(nazwa, "za niskie wiersze (zdjęcia ucięte):", h_zle)
    print("  %s: %d przepisów, %d zdjęć, z dwoma: %d, z jednym: %s, bez: %s" % (
        nazwa, len(oczekiwane), sum(len(v) for v in w_arkuszu.values()),
        sum(1 for v in w_arkuszu.values() if len(v) == 2),
        [p for p, v in w_arkuszu.items() if len(v) == 1],
        [p for p in oczekiwane if p not in w_arkuszu]))

# Sugestie maja te same zdjecia co Przepisy dla P148-P167
sug_ids = [wb["Sugestie"].cell(r, 1).value for r in range(2, wb["Sugestie"].max_row + 1)]
print("  Sugestie:", [i for i in sug_ids if i][:1], "...", [i for i in sug_ids if i][-1:], len([i for i in sug_ids if i]))

# ---- B
print("B. Zmiany poza zdjęciami (formuły i wartości, wszystkie arkusze)")
for ws in wb:
    if ws.title not in stary.sheetnames:
        blad("nowy arkusz", ws.title)
        continue
    so = stary[ws.title]
    if ws.title == "Instrukcja":
        nowe = [tuple(c.value for c in r) for r in ws.iter_rows()]
        stare = [tuple(c.value for c in r) for r in so.iter_rows()]
        dodane = [r for r in nowe if r not in stare]
        usuniete = [r for r in stare if r not in nowe]
        print("  Instrukcja: dodane wiersze:", [next((x for x in r if x), None) for r in dodane],
              "| usunięte:", [next((x for x in r if x), None) for r in usuniete])
        continue
    roznice = []
    for r in range(1, max(ws.max_row, so.max_row) + 1):
        for c in range(1, max(ws.max_column, so.max_column) + 1):
            a, b = ws.cell(r, c).value, so.cell(r, c).value
            if a != b:
                roznice.append((ws.cell(r, c).coordinate, b, a))
    szer = [(k, so.column_dimensions[k].width, ws.column_dimensions[k].width)
            for k in set(ws.column_dimensions) | set(so.column_dimensions)
            if so.column_dimensions[k].width != ws.column_dimensions[k].width]
    print("  %-14s komórek zmienionych: %d | szerokości kolumn: %s | walidacje %d/%d | formatowanie warunkowe %d/%d" % (
        ws.title, len(roznice), szer, len(ws.data_validations.dataValidation),
        len(so.data_validations.dataValidation), len(ws.conditional_formatting), len(so.conditional_formatting)))
    for x in roznice[:5]:
        blad(ws.title, "komórka", *x)
    if ws.freeze_panes != so.freeze_panes or ws.auto_filter.ref != so.auto_filter.ref:
        blad(ws.title, "zmienione zamrożenie/filtr", ws.freeze_panes, so.freeze_panes, ws.auto_filter.ref, so.auto_filter.ref)

# ---- C
print("C. Źródło zdjęć = link przepisu")
LINKI = json.load(open("zdj_linki.json", encoding="utf-8"))
ws = wb["Przepisy"]
nag = [c.value for c in ws[1]]
kl = nag.index("Link") + 1
for r in range(2, ws.max_row + 1):
    pid = ws.cell(r, 1).value
    if not pid:
        continue
    link = ws.cell(r, kl).value or None
    if (LINKI.get(pid) or None) != link:
        blad("link", pid, "zdjęcia z", LINKI.get(pid), "a w arkuszu", link)
print("  sprawdzone linki:", sum(1 for r in range(2, ws.max_row + 1) if ws.cell(r, 1).value))

# ---- D
print("D. Pliki zdjęć")
ZDJ = json.load(open("zdjecia.json", encoding="utf-8"))
hashe = {}
for k, p in sorted(pliki.items()):
    im = z_pliku(p)
    if im.shape[0] != im.shape[1] or im.shape[0] < 280:
        blad(k, "rozmiar", im.shape)
    if im.std() < 12:
        blad(k, "prawie jednolite zdjęcie (std %.1f)" % im.std())
    pid, nr = k.split("_")
    if nr not in ZDJ.get(pid, {}):
        blad(k, "brak opisu w zdjecia.json")
    hashe[k] = dh(im)
for pid, v in ZDJ.items():
    for nr in v:
        if "%s_%s" % (pid, nr) not in pliki:
            blad(pid, nr, "opis w zdjecia.json bez pliku")
klucze = sorted(hashe)
pary = []
for i, a in enumerate(klucze):
    for b in klucze[i + 1:]:
        d = np.count_nonzero(hashe[a] != hashe[b])
        if d < 40:
            pary.append((d, a, b))
for d, a, b in sorted(pary):
    print("  podobne (%d/256): %s %s%s" % (d, a, b, "" if a[:4] != b[:4] else "  <- ten sam przepis"))
print("  plików:", len(pliki))

print("\nWYNIK:", "BEZ BŁĘDÓW" if not BLEDY else "%d błędów" % len(BLEDY))
