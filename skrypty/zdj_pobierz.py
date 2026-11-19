# -*- coding: utf-8 -*-
"""Dwa zdjecia dania do kazdego przepisu.

Zdjecie 1: okladka posta (TikTok, Instagram, YouTube) albo glowne zdjecie z bloga.
Zdjecie 2: klatka z drugiej polowy filmu, gdzie zwykle widac gotowe danie - z kilku klatek
wybieram najostrzejsza i najbardziej kolorowa, bez twarzy i niepodobna do okladki.
Przy postach ze zdjeciami (karuzela) i na blogu biore kolejne zdjecie z posta.

Wynik: zdjecia/P001_1.jpg, P001_2.jpg (kwadrat 280 px) + zdjecia.json (skad kazde zdjecie).
Surowe pliki laduja w zdjecia_zrodla/ i nie sa uruchamiane, tylko dekodowane jako obrazy."""
import concurrent.futures as cf, html as H, http.cookiejar, io, json, os, re, sys, threading
import time, urllib.request
import cv2
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
SRC_DIR, OUT_DIR = "zdjecia_zrodla", "zdjecia"
os.makedirs(os.path.join(SRC_DIR, "tmp"), exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/141.0.0.0 Safari/537.36")
BOK = 1080      # gorna granica boku; mniejszych zrodel nie powiekszam
LINKI = json.load(open("zdj_linki.json", encoding="utf-8"))
IG = json.load(open("zdj_ig.json", encoding="utf-8"))
_watek = threading.local()          # klasyfikator twarzy nie jest bezpieczny dla watkow
_lock = threading.Lock()
CJ = http.cookiejar.CookieJar()
OP = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(CJ))


def twarz():
    if not hasattr(_watek, "c"):
        _watek.c = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    return _watek.c


def pobierz(url, referer=None, tries=3, op=None):
    h = {"User-Agent": UA, "Accept-Language": "pl-PL,pl;q=0.9,en;q=0.8"}
    if referer:
        h["Referer"] = referer
    for i in range(tries):
        try:
            return (op or OP).open(urllib.request.Request(url, headers=h), timeout=60).read()
        except Exception as e:
            err = e
            time.sleep(2 + 3 * i)
    raise err


def dekoduj(b):
    im = cv2.imdecode(np.frombuffer(b, np.uint8), cv2.IMREAD_COLOR)
    if im is None:                      # webp/heic itp. - przez Pillow
        from PIL import Image
        im = cv2.cvtColor(np.array(Image.open(io.BytesIO(b)).convert("RGB")), cv2.COLOR_RGB2BGR)
    return im


def kwadrat(im, srodek_y=0.5):
    h, w = im.shape[:2]
    b = min(h, w)
    x0 = (w - b) // 2
    y0 = int(min(max(srodek_y * h - b / 2, 0), h - b))
    s = min(BOK, b)
    return cv2.resize(im[y0:y0 + b, x0:x0 + b], (s, s), interpolation=cv2.INTER_AREA)


def dhash(im):
    g = cv2.resize(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY), (9, 8), interpolation=cv2.INTER_AREA)
    return (g[:, 1:] > g[:, :-1]).flatten()


def ocena(im, wzor=None):
    """Im wyzej, tym lepsze zdjecie dania: ostre, kolorowe, jasne, bez twarzy, inne niz okladka."""
    m = cv2.resize(im, (360, int(360 * im.shape[0] / im.shape[1])))
    g = cv2.cvtColor(m, cv2.COLOR_BGR2GRAY)
    ostrosc = cv2.Laplacian(g, cv2.CV_64F).var()
    b, gr, r = [c.astype(float) for c in cv2.split(m)]
    rg, yb = r - gr, 0.5 * (r + gr) - b
    kolor = np.sqrt(rg.std() ** 2 + yb.std() ** 2) + 0.3 * np.sqrt(rg.mean() ** 2 + yb.mean() ** 2)
    jasnosc = g.mean()
    twarze = twarz().detectMultiScale(g, 1.15, 6, minSize=(40, 40))
    pole = max([w * h for (_x, _y, w, h) in twarze] or [0]) / float(g.size)
    s = kolor / 40.0 + np.log10(ostrosc + 1) / 3.0
    s -= 2.0 if pole > 0.025 else 0
    s -= 1.0 if jasnosc < 45 or jasnosc > 225 else 0
    if wzor is not None and np.count_nonzero(dhash(im) != wzor) < 12:
        s -= 1.5
    return s


def klatki(sciezka, ulamki=(0.4, 0.5, 0.6, 0.68, 0.76, 0.84, 0.9, 0.95)):
    cap = cv2.VideoCapture(sciezka)
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    out = []
    for u in ulamki:
        if n > 0:
            cap.set(cv2.CAP_PROP_POS_FRAMES, int(n * u))
        ok, fr = cap.read()
        if ok and fr is not None:
            out.append((u, fr))
    cap.release()
    return out


def najlepsza(kandydaci, wzor):
    """kandydaci: [(opis, obraz)] -> (opis, obraz) z najlepsza ocena; pozniejsze lekko premiowane."""
    best = max(enumerate(kandydaci), key=lambda t: ocena(t[1][1], wzor) + 0.01 * t[0])
    return best[1]


def okladka_z_filmu(okladka, sciezka, nazwa="", prog=20):
    """Okladka rolki z Instagrama ma najwyzej 480 px szerokosci, a film 720 px. Okladka to zwykle
    klatka filmu, czasem z dodanym tytulem - szukam jej w filmie i jesli to ta sama scena, oddaje
    klatke w pelnej rozdzielczosci. Prog: srednia roznica jasnosci na miniaturze 72x128 (0-255);
    ta sama klatka ~10, z dopisanym tytulem ~18, inna scena powyzej 30.
    Film czytam po kolei (co 3. klatka) - przeskakiwanie po klatkach jest wielokrotnie wolniejsze."""
    cap = cv2.VideoCapture(sciezka)
    maly = lambda im: cv2.resize(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY), (72, 128), interpolation=cv2.INTER_AREA).astype(np.int16)
    wz, proporcja, naj, i = maly(okladka), okladka.shape[0] / okladka.shape[1], (1e9, None, 0), 0
    while cap.grab():
        if i % 3 == 0:
            ok, fr = cap.retrieve()
            if ok and abs(fr.shape[0] / fr.shape[1] - proporcja) <= .06:
                d = float(np.abs(maly(fr) - wz).mean())
                if d < naj[0]:
                    naj = (d, fr, i)
        i += 1
    cap.release()
    print("   okladka %s: roznica %.1f (klatka %d z %d) -> %s" % (nazwa, naj[0], naj[2], i, "z filmu" if naj[0] <= prog else "zostaje 480 px"), flush=True)
    return naj[1] if naj[0] <= prog else None


def z_filmu(url_mp4, okladka, referer, nazwa, op=None, szukaj_okladki=False):
    tmp = os.path.join(SRC_DIR, "tmp", nazwa + ".mp4")
    with open(tmp, "wb") as f:
        f.write(pobierz(url_mp4, referer, op=op))
    try:
        kl = klatki(tmp)
        hd = okladka_z_filmu(okladka, tmp, nazwa) if szukaj_okladki else None
    finally:
        os.remove(tmp)
    if not kl:
        raise RuntimeError("brak klatek")
    wz = dhash(okladka) if okladka is not None else None
    u, fr = najlepsza([("%d%%" % (u * 100), fr) for u, fr in kl], wz)
    if szukaj_okladki:
        return fr, "klatka z filmu (%s długości)" % u, hd
    return fr, "klatka z filmu (%s długości)" % u


def strumien_tt(v):
    """Najlepsza jakosc filmu TikToka: domyslny playAddr to 540p, w bitrateInfo bywa 720p (h265)."""
    wersje = [b for b in v.get("bitrateInfo") or [] if (b.get("PlayAddr") or {}).get("UrlList")]
    if not wersje:
        return v["playAddr"]
    b = max(wersje, key=lambda b: (b["PlayAddr"].get("Width") or 0, "264" in (b.get("CodecType") or "")))
    return b["PlayAddr"]["UrlList"][0]


def tiktok(link, nazwa):
    # strona /photo/ nie ma danych posta, ta sama pod /video/ ma (razem z lista zdjec)
    link = link.replace("/photo/", "/video/")
    op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    html = pobierz(link, op=op).decode("utf-8", "ignore")
    m = re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>', html, re.S)
    zakres = json.loads(m.group(1))["__DEFAULT_SCOPE__"]
    # filmy maja "webapp.video-detail", posty ze zdjeciami inny klucz - szukam po zawartosci
    it = next(v["itemInfo"]["itemStruct"] for v in zakres.values()
              if isinstance(v, dict) and (v.get("itemInfo") or {}).get("itemStruct"))
    if it.get("imagePost"):
        urls = [i["imageURL"]["urlList"][0] for i in it["imagePost"]["images"]]
        ims = [dekoduj(pobierz(u, "https://www.tiktok.com/", op=op)) for u in urls]
        for i, im in enumerate(ims):        # wszystkie, gdyby jeden post mial kilka dan
            cv2.imwrite(os.path.join(SRC_DIR, "%s_zdj%02d.jpg" % (nazwa, i + 1)), im)
        drugi = najlepsza([("zdjęcie %d z posta" % (i + 1), im) for i, im in enumerate(ims[1:], 1)],
                          dhash(ims[0])) if len(ims) > 1 else None
        return (ims[0], "zdjęcie 1 z posta"), drugi and (drugi[1], drugi[0])
    v = it["video"]
    ok = dekoduj(pobierz(v.get("cover") or v["originCover"], "https://www.tiktok.com/", op=op))
    fr, opis = z_filmu(strumien_tt(v), ok, "https://www.tiktok.com/", nazwa, op=op)
    return (ok, "okładka filmu"), (fr, opis)


def instagram(link, nazwa):
    code = re.search(r"/(?:reel|p|tv)/([\w-]+)", link).group(1)
    img, vid, _dur = IG[code]
    ok = dekoduj(pobierz(img))
    fr, opis, hd = z_filmu(vid, ok, None, nazwa, szukaj_okladki=True)
    return (ok if hd is None else hd, "okładka rolki"), (fr, opis)


def youtube(link, nazwa):
    vid = re.search(r"(?:v=|youtu\.be/)([\w-]{11})", link).group(1)
    ok = None
    for q in ("maxresdefault", "sddefault", "hqdefault"):
        try:
            ok = dekoduj(pobierz("https://i.ytimg.com/vi/%s/%s.jpg" % (vid, q)))
            if ok is not None and ok.shape[1] > 200:
                break
        except Exception:
            pass
    kand = []
    # maxres1-3 to klatki z 1/4, 1/2 i 3/4 filmu w 1280x720 (nie kazdy film je ma)
    for q in ("maxres1", "maxres2", "maxres3", "sd1", "sd2", "sd3"):
        try:
            kand.append(("klatka YouTube %s" % q[-1], dekoduj(pobierz("https://i.ytimg.com/vi/%s/%s.jpg" % (vid, q)))))
        except Exception:
            pass
    opis, fr = najlepsza(kand, dhash(ok))
    # miniatury YouTube maja czarne pasy u gory i u dolu - kwadrat i tak je obcina
    return (ok, "miniatura filmu"), (fr, "klatka z filmu (miniatura YouTube)")


def blog(link, nazwa):
    t = pobierz(link).decode("utf-8", "ignore")
    og = re.search(r'<meta[^>]+property="og:image"[^>]+content="([^"]+)"', t).group(1)
    ok = dekoduj(pobierz(H.unescape(og)))
    zdj, podane = [], []
    for tag in re.findall(r'<img[^>]+>', t):
        m = re.search(r'src="(https://cdn\.aniagotuje\.(?:pl|com)/pictures/articles/[^"]+)"', tag)
        # miniatury 360x360 to polecane inne przepisy pod artykulem, nie to danie
        if not m or "-360x360" in m.group(1) or m.group(1) == og or m.group(1) in zdj:
            continue
        zdj.append(H.unescape(m.group(1)))
        # opisy sa dlugie, o podanym daniu mowi poczatek ("Porcja...", "W misce zostala podana...")
        alt = (re.search(r'alt="([^"]*)"', tag) or [None, ""])[1].lower()[:60]
        if ("podan" in alt or "porcj" in alt) and "surow" not in alt:
            podane.append(zdj[-1])
    # zdjecia podanego dania to kilka ujec tego samego talerza - biore najbardziej rozne
    # od glownego (porownuje przyciete kwadraty, bo tak beda wygladac w arkuszu)
    wz, kand = dhash(kwadrat(ok)), []
    for u in podane or zdj[-3:]:
        try:
            im = dekoduj(pobierz(u))
        except Exception:
            continue
        kand.append((np.count_nonzero(dhash(kwadrat(im, 0.55)) != wz), im))
    fr = max(kand, key=lambda t: t[0])[1]
    return (ok, "główne zdjęcie z bloga"), (fr, "zdjęcie z bloga (gotowe danie)")


def przetworz(pid, link):
    nazwa = pid
    if "tiktok.com" in link:
        a, b = tiktok(link, nazwa)
    elif "instagram.com" in link:
        a, b = instagram(link, nazwa)
    elif "youtu" in link:
        a, b = youtube(link, nazwa)
    else:
        a, b = blog(link, nazwa)
    wynik = {}
    for i, para in enumerate((a, b), 1):
        if not para or para[0] is None:
            continue
        im, opis = para
        portret = im.shape[0] > im.shape[1] * 1.2
        cv2.imwrite(os.path.join(OUT_DIR, "%s_%d.jpg" % (pid, i)), kwadrat(im, 0.55 if portret else 0.5),
                    [cv2.IMWRITE_JPEG_QUALITY, 80])
        wynik[i] = opis
    return wynik


if __name__ == "__main__":
    ZDJ = {}
    if os.path.exists("zdjecia.json"):
        ZDJ = json.load(open("zdjecia.json", encoding="utf-8"))
    tylko = set(sys.argv[1:])
    zadania = [(p, l) for p, l in LINKI.items() if l and (p in tylko if tylko else
                                                         not (p in ZDJ and len(ZDJ[p]) == 2))]
    print("do zrobienia:", len(zadania), flush=True)
    bledy = {}
    with cf.ThreadPoolExecutor(4) as ex:
        fut = {ex.submit(przetworz, p, l): p for p, l in zadania}
        for i, f in enumerate(cf.as_completed(fut), 1):
            p = fut[f]
            try:
                w = f.result()
                with _lock:
                    ZDJ[p] = {str(k): v for k, v in w.items()}
                print("%3d/%d %s %s" % (i, len(zadania), p, w), flush=True)
            except Exception as e:
                bledy[p] = repr(e)[:200]
                print("%3d/%d %s BLAD %s" % (i, len(zadania), p, repr(e)[:150]), flush=True)
            if i % 10 == 0:
                json.dump(ZDJ, open("zdjecia.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    json.dump(ZDJ, open("zdjecia.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print("gotowe:", sum(1 for v in ZDJ.values() if len(v) == 2), "z dwoma zdjęciami; błędy:", bledy, flush=True)
    os._exit(0)     # po OpenCV w watkach proces na Windowsie potrafi nie zakonczyc sie sam
