# -*- coding: utf-8 -*-
"""Plansze kontrolne: pary zdjec wszystkich przepisow z numerem ID, do szybkiego przegladu.
Uzycie: zdj_podglad.py [ID ...] - bez argumentow wszystkie przepisy."""
import glob, os, re, sys
import cv2
import numpy as np

MINI, NA_WIERSZ, WIERSZY = 120, 6, 8
pids = sys.argv[1:] or sorted({re.match(r"(P\d+)_", os.path.basename(p)).group(1)
                               for p in glob.glob("zdjecia/P*_*.jpg")})
pole_w, pole_h = 2 * MINI + 14, MINI + 22
na_plansze = NA_WIERSZ * WIERSZY
for n in range(0, len(pids), na_plansze):
    czesc = pids[n:n + na_plansze]
    wiersze = (len(czesc) + NA_WIERSZ - 1) // NA_WIERSZ
    plansza = np.full((wiersze * pole_h, NA_WIERSZ * pole_w, 3), 255, np.uint8)
    for i, pid in enumerate(czesc):
        x0, y0 = (i % NA_WIERSZ) * pole_w, (i // NA_WIERSZ) * pole_h
        cv2.putText(plansza, pid, (x0 + 4, y0 + 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 160), 1)
        for j in (1, 2):
            p = "zdjecia/%s_%d.jpg" % (pid, j)
            if os.path.exists(p):
                im = cv2.resize(cv2.imread(p), (MINI, MINI))
                xx = x0 + 4 + (j - 1) * (MINI + 4)
                plansza[y0 + 20:y0 + 20 + MINI, xx:xx + MINI] = im
    out = "podglad_%d.jpg" % (n // na_plansze + 1)
    cv2.imwrite(out, plansza, [cv2.IMWRITE_JPEG_QUALITY, 85])
    print(out, len(czesc))
