# -*- coding: utf-8 -*-
"""Do recznego wyboru: 12 klatek z calego filmu (plus okladka) dla wskazanych przepisow.
Klatki laduja w zdjecia_zrodla/kand/<ID>_kNN.jpg (k00 = okladka), plansze w kandydaci_N.jpg.
Uzycie: zdj_kandydaci.py ID [ID ...]"""
import concurrent.futures as cf, http.cookiejar, json, os, re, sys, urllib.request
import cv2
import numpy as np
from zdj_pobierz import IG, LINKI, SRC_DIR, dekoduj, klatki, okladka_z_filmu, pobierz, strumien_tt

KAND = os.path.join(SRC_DIR, "kand")
os.makedirs(KAND, exist_ok=True)
ULAMKI = (0.12, 0.2, 0.28, 0.36, 0.44, 0.52, 0.6, 0.68, 0.76, 0.84, 0.91, 0.97)


def zrodlo(link):
    """-> (okladka, url mp4, referer, opener) albo dla YouTube (okladka, [klatki], None, None)"""
    if "tiktok.com" in link:
        op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        html = pobierz(link.replace("/photo/", "/video/"), op=op).decode("utf-8", "ignore")
        m = re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>', html, re.S)
        it = next(v["itemInfo"]["itemStruct"] for v in json.loads(m.group(1))["__DEFAULT_SCOPE__"].values()
                  if isinstance(v, dict) and (v.get("itemInfo") or {}).get("itemStruct"))
        v = it["video"]
        ok = dekoduj(pobierz(v.get("cover") or v["originCover"], "https://www.tiktok.com/", op=op))
        return ok, strumien_tt(v), "https://www.tiktok.com/", op
    if "instagram.com" in link:
        img, vid, _ = IG[re.search(r"/(?:reel|p|tv)/([\w-]+)", link).group(1)]
        return dekoduj(pobierz(img)), vid, None, None
    vid = re.search(r"(?:v=|youtu\.be/)([\w-]{11})", link).group(1)
    ims = []
    for q in ("maxresdefault", "maxres1", "maxres2", "maxres3", "sd1", "sd2", "sd3", "hq1", "hq2", "hq3", "sddefault", "hqdefault"):
        try:
            ims.append(dekoduj(pobierz("https://i.ytimg.com/vi/%s/%s.jpg" % (vid, q), tries=1)))
        except Exception:
            pass
    return ims[0], ims[1:], None, None


def przygotuj(pid):
    ok, film, ref, op = zrodlo(LINKI[pid])
    if isinstance(film, list):
        kl = film
    else:
        tmp = os.path.join(SRC_DIR, "tmp", pid + "_k.mp4")
        with open(tmp, "wb") as f:
            f.write(pobierz(film, ref, op=op))
        try:
            kl = [fr for _u, fr in klatki(tmp, ULAMKI)]
            if "instagram.com" in LINKI[pid]:      # okladka rolki ma 480 px - ta sama klatka z filmu ma 720
                hd = okladka_z_filmu(ok, tmp, pid)
                ok = ok if hd is None else hd
        finally:
            os.remove(tmp)
    for i, im in enumerate([ok] + kl):
        cv2.imwrite(os.path.join(KAND, "%s_k%02d.jpg" % (pid, i)), im, [cv2.IMWRITE_JPEG_QUALITY, 88])
    return [ok] + kl


pids = sys.argv[1:]
gotowe = {}
with cf.ThreadPoolExecutor(4) as ex:
    fut = {ex.submit(przygotuj, p): p for p in pids}
    for f in cf.as_completed(fut):
        try:
            gotowe[fut[f]] = f.result()
            print(fut[f], len(gotowe[fut[f]]), flush=True)
        except Exception as e:
            print(fut[f], "BLAD", repr(e)[:150], flush=True)

# plansze: 4 przepisy na plansze, wiersz = okladka + 12 klatek, miniatury 96x170 (proporcje 9:16)
MW, MH, NA = 96, 170, 4
kolejka = [p for p in pids if p in gotowe]
for n in range(0, len(kolejka), NA):
    czesc = kolejka[n:n + NA]
    pl = np.full((len(czesc) * (MH + 22), 13 * (MW + 4) + 4, 3), 255, np.uint8)
    for r, pid in enumerate(czesc):
        y0 = r * (MH + 22)
        for i, im in enumerate(gotowe[pid][:13]):
            s = min(MW / im.shape[1], MH / im.shape[0])
            m = cv2.resize(im, (max(1, int(im.shape[1] * s)), max(1, int(im.shape[0] * s))))
            x0 = 4 + i * (MW + 4)
            pl[y0 + 20:y0 + 20 + m.shape[0], x0:x0 + m.shape[1]] = m
            cv2.putText(pl, ("%s k%02d" % (pid, i)) if i == 0 else "k%02d" % i, (x0, y0 + 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 160), 1)
    out = "kandydaci_%d.jpg" % (n // NA + 1)
    cv2.imwrite(out, pl, [cv2.IMWRITE_JPEG_QUALITY, 85])
    print(out, czesc)
sys.stdout.flush()
os._exit(0)     # po OpenCV w watkach proces na Windowsie potrafi nie zakonczyc sie sam
