# -*- coding: utf-8 -*-
"""Poprawki po pierwszej probie zdj_pobierz.py: TikTok w osobnej sesji na film, posty ze
zdjeciami, klasyfikator twarzy na watek, og:image z dowolna kolejnoscia atrybutow."""
from patch_weryf_lib import podmien

podmien("zdj_pobierz.py", [
    ('TWARZ = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")\n',
     '_watek = threading.local()          # klasyfikator twarzy nie jest bezpieczny dla watkow\n'),
    ('def pobierz(url, referer=None, tries=3):\n',
     'def twarz():\n'
     '    if not hasattr(_watek, "c"):\n'
     '        _watek.c = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")\n'
     '    return _watek.c\n\n\n'
     'def pobierz(url, referer=None, tries=3, op=None):\n'),
    ('            return OP.open(urllib.request.Request(url, headers=h), timeout=60).read()\n',
     '            return (op or OP).open(urllib.request.Request(url, headers=h), timeout=60).read()\n'),
    ('    twarze = TWARZ.detectMultiScale(g, 1.15, 6, minSize=(40, 40))\n',
     '    twarze = twarz().detectMultiScale(g, 1.15, 6, minSize=(40, 40))\n'),
    ('def z_filmu(url_mp4, okladka, referer, nazwa):\n',
     'def z_filmu(url_mp4, okladka, referer, nazwa, op=None):\n'),
    ('        f.write(pobierz(url_mp4, referer))\n',
     '        f.write(pobierz(url_mp4, referer, op=op))\n'),
    # TikTok: kazdy film we wlasnej sesji - token z ciasteczka musi pasowac do adresu mp4
    ('    html = pobierz(link).decode("utf-8", "ignore")\n'
     '    m = re.search(r\'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>\', html, re.S)\n'
     '    it = json.loads(m.group(1))["__DEFAULT_SCOPE__"]["webapp.video-detail"]["itemInfo"]["itemStruct"]\n',
     '    op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))\n'
     '    html = pobierz(link, op=op).decode("utf-8", "ignore")\n'
     '    m = re.search(r\'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>\', html, re.S)\n'
     '    zakres = json.loads(m.group(1))["__DEFAULT_SCOPE__"]\n'
     '    # filmy maja "webapp.video-detail", posty ze zdjeciami inny klucz - szukam po zawartosci\n'
     '    it = next(v["itemInfo"]["itemStruct"] for v in zakres.values()\n'
     '              if isinstance(v, dict) and (v.get("itemInfo") or {}).get("itemStruct"))\n'),
    ('        ims = [dekoduj(pobierz(u, "https://www.tiktok.com/")) for u in urls]\n',
     '        ims = [dekoduj(pobierz(u, "https://www.tiktok.com/", op=op)) for u in urls]\n'),
    ('    ok = dekoduj(pobierz(v.get("cover") or v["originCover"], "https://www.tiktok.com/"))\n'
     '    fr, opis = z_filmu(v["playAddr"], ok, "https://www.tiktok.com/", nazwa)\n',
     '    ok = dekoduj(pobierz(v.get("cover") or v["originCover"], "https://www.tiktok.com/", op=op))\n'
     '    fr, opis = z_filmu(v["playAddr"], ok, "https://www.tiktok.com/", nazwa, op=op)\n'),
    ('    og = re.search(r\'<meta property="og:image" content="([^"]+)"\', t).group(1)\n',
     '    og = re.search(r\'<meta[^>]+property="og:image"[^>]+content="([^"]+)"\', t).group(1)\n'),
])
