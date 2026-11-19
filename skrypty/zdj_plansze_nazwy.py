# -*- coding: utf-8 -*-
"""Plansze do weryfikacji: para zdjec + ID + nazwa przepisu (polskie litery przez PIL).
Uzycie: zdj_plansze_nazwy.py [ID ...]"""
import os, sys
import openpyxl
from PIL import Image, ImageDraw, ImageFont

# nazwy to zwykle wartosci, wiec wystarczy sam arkusz, bez przeliczania
ws = openpyxl.load_workbook(r"C:\Users\Sebastian\Documents\Przepisy-planer\Przepisy-planer.xlsx", read_only=True)["Przepisy"]
NAZWY = {r[0]: r[1] for r in ws.iter_rows(min_row=2, max_col=2, values_only=True) if r[0] and r[1]}
pids = sys.argv[1:] or sorted(NAZWY)
M, NA, WIER = 130, 4, 6
PW, PH = 2 * M + 16, M + 40
f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 13)
fb = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 13)
for n in range(0, len(pids), NA * WIER):
    cz = pids[n:n + NA * WIER]
    pl = Image.new("RGB", (NA * PW, ((len(cz) + NA - 1) // NA) * PH), "white")
    d = ImageDraw.Draw(pl)
    for i, pid in enumerate(cz):
        x0, y0 = (i % NA) * PW, (i // NA) * PH
        nazwa = NAZWY.get(pid, "?")
        d.text((x0 + 4, y0 + 2), pid, fill=(160, 0, 0), font=fb)
        d.text((x0 + 44, y0 + 2), nazwa[:34], fill=(0, 0, 0), font=f)
        if len(nazwa) > 34:
            d.text((x0 + 4, y0 + 18), nazwa[34:72], fill=(0, 0, 0), font=f)
        for j in (1, 2):
            p = "zdjecia/%s_%d.jpg" % (pid, j)
            if os.path.exists(p):
                pl.paste(Image.open(p).resize((M, M)), (x0 + 4 + (j - 1) * (M + 4), y0 + 36))
    out = "weryf_%d.jpg" % (n // (NA * WIER) + 1)
    pl.save(out, quality=85)
    print(out, cz[0], "-", cz[-1])
