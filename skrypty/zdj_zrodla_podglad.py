# -*- coding: utf-8 -*-
"""Plansza wszystkich zdjec z posta (zdjecia_zrodla/<ID>_zdjNN.jpg), zeby recznie wybrac pare.
Uzycie: zdj_zrodla_podglad.py ID"""
import glob, os, sys
import cv2
import numpy as np

pid = sys.argv[1]
pliki = sorted(glob.glob("zdjecia_zrodla/%s_zdj*.jpg" % pid))
W, H, NA_WIERSZ = 200, 266, 4
wiersze = (len(pliki) + NA_WIERSZ - 1) // NA_WIERSZ
plansza = np.full((wiersze * (H + 24), NA_WIERSZ * (W + 6), 3), 255, np.uint8)
for i, p in enumerate(pliki):
    x0, y0 = (i % NA_WIERSZ) * (W + 6), (i // NA_WIERSZ) * (H + 24)
    im = cv2.imread(p)
    s = min(W / im.shape[1], H / im.shape[0])
    im = cv2.resize(im, (int(im.shape[1] * s), int(im.shape[0] * s)))
    plansza[y0 + 22:y0 + 22 + im.shape[0], x0:x0 + im.shape[1]] = im
    cv2.putText(plansza, os.path.basename(p)[5:-4], (x0 + 4, y0 + 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 160), 1)
out = "zrodla_%s.jpg" % pid
cv2.imwrite(out, plansza, [cv2.IMWRITE_JPEG_QUALITY, 85])
print(out, len(pliki))
