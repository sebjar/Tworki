# -*- coding: utf-8 -*-
"""Kontrola po dodaniu propozycji: (1) stare przepisy bez zmian, (2) kazdy skladnik propozycji
ma wartosci odzywcze, (3) przeglad liczb dla P148+ (kcal, makra, autor, odgrzewanie, porcje)."""
import sys
import openpyxl
from nutrition import NUTR

sys.stdout.reconfigure(encoding="utf-8")
stary = openpyxl.load_workbook("_przed_sugestiami.xlsx", data_only=True, read_only=True)
nowy = openpyxl.load_workbook("_wartosci.xlsx", data_only=True, read_only=True)


def przepisy(wb):
    ws = wb["Przepisy"]
    hdr = [c for c in next(ws.iter_rows(min_row=1, max_row=1, values_only=True))]
    out = {}
    for r in ws.iter_rows(min_row=2, values_only=True):
        if r[0] and r[1]:
            out[r[0]] = dict(zip(hdr, r))
    return out, hdr


S, _ = przepisy(stary)
N, hdr = przepisy(nowy)
zmiany = 0
for pid, a in S.items():
    b = N.get(pid)
    if not b:
        print("ZNIKNAL", pid)
        zmiany += 1
        continue
    for h in hdr[:33]:
        if h in ("Podobne do",):
            continue
        if a.get(h) != b.get(h):
            print("ZMIANA", pid, h, repr(a.get(h))[:60], "->", repr(b.get(h))[:60])
            zmiany += 1
print("Stare przepisy: %d, zmian: %d" % (len(S), zmiany))

# skladniki propozycji bez wartosci odzywczych
sk = nowy["Składniki"]
braki = 0
for r in sk.iter_rows(min_row=2, max_col=12, values_only=True):
    if r[0] and r[0][:4] >= "P148" and r[0][0] == "P":
        if r[1] not in NUTR or r[11] in (None, ""):
            print("BRAK WARTOSCI", r[0][:30], r[1], r[2], r[3], r[11])
            braki += 1
print("Skladniki bez wartosci:", braki)

kol = ["ID", "Porcje bazowe", "Składników", "kcal / porcję", "Białko (g)", "Tłuszcz (g)",
       "Węgle (g)", "kcal — autor", "Białko — autor", "Zgodność z autorem", "kcal — wersja light",
       "W Planie na dzień", "Ugotuj razem (2 dni)", "Twoja porcja (kcal)", "Jej porcja (kcal)",
       "Na drugi dzień", "Skąd"]
for pid in sorted(N):
    if pid >= "P148":
        r = N[pid]
        print("%s %-52s %s" % (pid, r["Nazwa przepisu"][:52], r["Kategoria"]))
        print("     " + " | ".join("%s=%s" % (k.split(" (")[0][:14], r.get(k)) for k in kol[1:]))
        print("     odgrz:", (r.get("Jak odgrzewać") or "")[:150])
        if r.get("Podobne do"):
            print("     podobne:", r["Podobne do"][:150])
