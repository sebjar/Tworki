# -*- coding: utf-8 -*-
"""Diagnostyka bloga: odleglosc dhash (kwadraty) miedzy glownym zdjeciem a zdjeciami z tresci."""
import html as H, re, sys
import numpy as np
from zdj_pobierz import LINKI, dekoduj, dhash, kwadrat, pobierz

for pid in sys.argv[1:]:
    t = pobierz(LINKI[pid]).decode("utf-8", "ignore")
    og = re.search(r'<meta[^>]+property="og:image"[^>]+content="([^"]+)"', t).group(1)
    wz = dhash(kwadrat(dekoduj(pobierz(H.unescape(og)))))
    print(pid, "og", og[-40:], flush=True)
    for tag in re.findall(r'<img[^>]+>', t):
        m = re.search(r'src="(https://cdn\.aniagotuje\.(?:pl|com)/pictures/articles/[^"]+)"', tag)
        if not m or "-360x360" in m.group(1):
            continue
        alt = (re.search(r'alt="([^"]*)"', tag) or [None, ""])[1][:70]
        im = dekoduj(pobierz(H.unescape(m.group(1))))
        print("  %2d %s %s | %s" % (np.count_nonzero(dhash(kwadrat(im, 0.55)) != wz), m.group(1)[-28:],
                                   im.shape[:2], alt), flush=True)
