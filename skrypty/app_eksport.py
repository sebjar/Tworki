# -*- coding: utf-8 -*-
"""Dane do aplikacji (Przepisy-aplikacja.html): przepisy, skladniki w gramach, zdjecia i
typowe opakowania, z ktorych aplikacja liczy, co zostanie po tygodniu.
Czyta _wartosci.xlsx (po przelicz.py) i zdjecia/, sklada app/szablon.html w jeden plik.
Uzycie: build_v2.py -> przelicz.py -> app_eksport.py"""
import hashlib, io, json, os, re, sys
import openpyxl
from PIL import Image
from nutrition import grams

sys.stdout.reconfigure(encoding="utf-8")
SP = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(SP), "Przepisy-aplikacja.html")

# Typowe opakowanie w polskim sklepie: (gramy, jak sie kupuje, waga marnowania).
# Waga mowi, jak bardzo boli resztka: swieze ziola i szpinak 1, mieso 0.6 (da sie zamrozic),
# twarde sery i jajka 0.3 (postoja). Czego tu nie ma, kupuje sie na sztuki albo stoi w szafce.
PACZKI = {
    "śmietana kremówka": (200, "kubek 200 ml", 1), "śmietana kwaśna": (200, "kubek 200 g", 1),
    "śmietana 18%": (200, "kubek 200 g", 1), "śmietana 12%": (200, "kubek 200 g", 1),
    "śmietana": (200, "kubek 200 g", 1), "jogurt grecki": (400, "kubek 400 g", 0.8),
    "jogurt naturalny": (400, "kubek 400 g", 0.8), "skyr": (150, "kubek 150 g", 0.8),
    "kefir": (400, "butelka 400 g", 0.8), "mleko": (1000, "karton 1 l", 0.5),
    "mozzarella": (125, "kulka 125 g", 0.8), "ser feta": (200, "kostka 200 g", 0.6),
    "serek śmietankowy": (150, "opak. 150 g", 0.7), "serek wiejski": (200, "kubek 200 g", 0.8),
    "cheddar": (200, "opak. 200 g", 0.4), "ser żółty": (150, "plastry 150 g", 0.4),
    "gouda": (150, "plastry 150 g", 0.4), "gorgonzola": (150, "opak. 150 g", 0.6),
    "parmezan": (100, "kawałek 100 g", 0.2), "masło": (200, "kostka 200 g", 0.2),
    "jajko": (550, "10 jajek", 0.2), "żółtko": (550, "10 jajek", 0.2),
    "mleko zagęszczone": (410, "puszka 410 g", 0.8),
    "pierś z kurczaka": (500, "tacka 500 g", 0.6), "udka z kurczaka": (500, "tacka 500 g", 0.6),
    "mięso mielone wołowe": (500, "tacka 500 g", 0.6), "mięso mielone z kurczaka": (500, "tacka 500 g", 0.6),
    "mięso mielone z piersi kurczaka": (500, "tacka 500 g", 0.6),
    "mięso mielone wieprzowe": (500, "tacka 500 g", 0.6), "mięso mielone": (500, "tacka 500 g", 0.6),
    "boczek": (150, "opak. 150 g", 0.5), "łosoś": (250, "opak. 250 g", 0.7),
    "szynka": (100, "opak. 100 g", 0.6), "pepperoni": (100, "opak. 100 g", 0.4),
    "natka pietruszki": (30, "pęczek", 1), "kolendra": (30, "pęczek", 1), "koperek": (30, "pęczek", 1),
    "szczypiorek": (30, "pęczek", 1), "dymka": (60, "pęczek", 0.8), "bazylia": (25, "doniczka", 1),
    "mięta": (25, "doniczka", 1), "szpinak": (150, "opak. 150 g", 1), "rukola": (100, "opak. 100 g", 1),
    "roszponka": (100, "opak. 100 g", 1), "sałata": (150, "opak. 150 g", 1),
    "sałata lodowa": (400, "główka", 0.8), "sałata rzymska": (300, "główka", 0.8),
    "pomidorki koktajlowe": (250, "opak. 250 g", 0.7), "brokuł": (400, "sztuka", 0.7),
    "ogórek": (200, "sztuka", 0.6), "papryka czerwona": (150, "sztuka", 0.5),
    "papryka zielona": (150, "sztuka", 0.5), "papryka żółta": (150, "sztuka", 0.5),
    "papryka": (150, "sztuka", 0.5), "cukinia": (300, "sztuka", 0.6), "awokado": (150, "sztuka", 0.8),
    "cytryna": (100, "sztuka", 0.3), "limonka": (70, "sztuka", 0.3),
    "tortilla": (360, "opak. 6 szt.", 0.6), "tortilla mała": (240, "opak. 8 szt.", 0.6),
    "pita": (240, "opak. 4 szt.", 0.6), "chleb": (500, "bochenek", 0.6),
    "passata pomidorowa": (500, "butelka 500 ml", 0.7), "pomidory z puszki": (400, "puszka 400 g", 0.7),
    "kukurydza konserwowa": (285, "puszka", 0.5), "mleko kokosowe": (400, "puszka 400 ml", 0.8),
    "fasola czerwona": (240, "puszka", 0.5), "fasola czarna": (240, "puszka", 0.5),
    "ciecierzyca": (240, "puszka", 0.5),
}
SPIZARNIA = {"Sypkie i makarony", "Przyprawy i zioła", "Oleje i sosy", "Słodycze i przekąski",
             "Napoje", "Mrożonki"}


# Zdjecia ida obok strony jako osobne pliki (wklejone w strone przekroczylyby limit 16 MB):
# app/zdj/ dla wersji opublikowanej i zdj/ obok Przepisy-aplikacja.html dla wersji z dysku.
# Bok 720 px wystarcza na ekran telefonu (karta ~250 pkt x 3), a w nazwie jest skrot tresci,
# zeby przegladarka nie pokazywala starego zdjecia z pamieci po podmianie.
ZDJ_BOK, ZDJ_JAKOSC = 720, 82
ZDJ_DIRS = [os.path.join(SP, "app", "zdj"), os.path.join(os.path.dirname(SP), "zdj")]
for d in ZDJ_DIRS:
    os.makedirs(d, exist_ok=True)
    for f in os.listdir(d):
        os.remove(os.path.join(d, f))
ZAPISANE = []


# Miniatury do siatki, planu i listy wyboru: po 48 w jednym pliku (8 x 6), ladowane od razu przy
# otwarciu - kilka zapytan zamiast 327. Duze zdjecie 720 px dociaga sie w karcie przepisu.
MIN_BOK, MIN_KOL, MIN_WIER, MIN_JAKOSC = 360, 8, 6, 80
MINIATURY = []


def zdjecie(p):
    im = Image.open(p).convert("RGB")
    im.thumbnail((ZDJ_BOK, ZDJ_BOK), Image.LANCZOS)
    b = io.BytesIO()
    im.save(b, "JPEG", quality=ZDJ_JAKOSC, optimize=True, progressive=True)
    nazwa = "%s-%s.jpg" % (os.path.basename(p)[:-4], hashlib.md5(b.getvalue()).hexdigest()[:6])
    for d in ZDJ_DIRS:
        open(os.path.join(d, nazwa), "wb").write(b.getvalue())
    ZAPISANE.append((nazwa, im.size[0], len(b.getvalue())))
    MINIATURY.append(im.resize((MIN_BOK, MIN_BOK), Image.LANCZOS))
    i = len(MINIATURY) - 1
    return "zdj/" + nazwa, [i // (MIN_KOL * MIN_WIER), i % (MIN_KOL * MIN_WIER)]


def zapisz_miniatury():
    """Sklada miniatury w pliki zbiorcze; zwraca ich sciezki wzgledne."""
    na_plik, pliki = MIN_KOL * MIN_WIER, []
    for n in range(0, len(MINIATURY), na_plik):
        arkusz = Image.new("RGB", (MIN_KOL * MIN_BOK, MIN_WIER * MIN_BOK), (233, 237, 230))
        for j, im in enumerate(MINIATURY[n:n + na_plik]):
            arkusz.paste(im, ((j % MIN_KOL) * MIN_BOK, (j // MIN_KOL) * MIN_BOK))
        b = io.BytesIO()
        arkusz.save(b, "JPEG", quality=MIN_JAKOSC, optimize=True, progressive=True)
        nazwa = "miniatury-%d-%s.jpg" % (n // na_plik + 1, hashlib.md5(b.getvalue()).hexdigest()[:6])
        for d in ZDJ_DIRS:
            open(os.path.join(d, nazwa), "wb").write(b.getvalue())
        ZAPISANE.append((nazwa, MIN_KOL * MIN_BOK, len(b.getvalue())))
        pliki.append("zdj/" + nazwa)
    return pliki


def liczba(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


wb = openpyxl.load_workbook(os.path.join(SP, "_wartosci.xlsx"), read_only=True, data_only=True)
wiersze = list(wb["Przepisy"].iter_rows(values_only=True))
H = {h: i for i, h in enumerate(wiersze[0])}
skl = {}
for r in wb["Składniki"].iter_rows(min_row=2, values_only=True):
    if not r[0] or not r[1] or r[2] is None:
        continue
    pid = r[0].split(":")[0]
    q = liczba(r[2]) or 0
    skl.setdefault(pid, []).append(dict(
        n=r[1], q=q, u=r[3] or "", s=r[4] or "Inne",
        g=round(grams(r[1], r[3], q), 1), gp=round(liczba(r[17]) or 0, 1)))

# rodzaj linku: film, post ze zdjeciami (TikTok /photo/, rolka bez filmu na Instagramie) albo blog
IG = json.load(open(os.path.join(SP, "zdj_ig.json"), encoding="utf-8"))


def rodzaj_linku(l):
    if "tiktok.com" in l:
        return "post" if "/photo/" in l else "film"
    if "instagram.com" in l:
        m = re.search(r"/(?:reel|p|tv)/([\w-]+)", l)
        return "film" if "/reel/" in l or (m and (IG.get(m.group(1)) or [None, None])[1]) else "post"
    return "film" if "youtu" in l else "blog"


przepisy = []
for w in wiersze[1:]:
    pid, nazwa = w[H["ID"]], w[H["Nazwa przepisu"]]
    if not pid or not nazwa or not str(pid).startswith("P"):
        continue
    tekst = w[H["Przygotowanie"]] or ""
    uwaga = ""
    if tekst.startswith("UWAGA: "):
        uwaga, _, tekst = tekst[7:].partition("\n\n")
    kroki = [re.sub(r"^\d+\.\s*", "", k).strip() for k in tekst.split("\n") if k.strip()]
    zdj = [zdjecie(p) for p in (os.path.join(SP, "zdjecia", "%s_%d.jpg" % (pid, i)) for i in (1, 2))
           if os.path.exists(p)]   # [(sciezka 720 px, [plik zbiorczy, pozycja])]
    ings = skl.get(pid, [])
    przepisy.append(dict(
        id=pid, n=nazwa, k=w[H["Kategoria"]] or "Inne", zr=w[H["Źródło"]] or "", a=w[H["Autor"]] or "",
        l=w[H["Link"]] or "", lt=rodzaj_linku(w[H["Link"]] or ""), p=liczba(w[H["Porcje bazowe"]]) or 2,
        kcal=liczba(w[H["kcal / porcję"]]), b=liczba(w[H["Białko (g)"]]),
        t=liczba(w[H["Tłuszcz (g)"]]), w=liczba(w[H["Węgle (g)"]]),
        light=liczba(w[H["kcal — wersja light"]]), zam=w[H["Co zamienić na light"]] or "",
        dwa=str(w[H["Na drugi dzień"]] or ""), odg=w[H["Jak odgrzewać"]] or "",
        pod=w[H["Podobne do"]] or "", sug=str(w[H["Skąd"]] or "").startswith("Sugestia"),
        uw=uwaga.strip(), kr=kroki, z=[s for s, _ in zdj], m=[m for _, m in zdj],
        ing=[[x["n"], x["q"], x["u"], x["s"], x["g"]] for x in ings],
        gp=round(sum(x["gp"] for x in ings), 1)))

ust = {}
uw = list(wb["Ustawienia"].iter_rows(values_only=True))
ik, iu = uw[0].index("Kategoria"), uw[0].index("Udział posiłku w dniu")
for r in uw:
    if isinstance(r[ik], str) and isinstance(r[iu], (int, float)):
        ust[r[ik]] = r[iu]
    teksty = [str(v) for v in r]
    for etykieta, klucz in (("Zapotrzebowanie na dzień", "_kcal"), ("Podział jedzenia z garnka", "_podzial")):
        if etykieta in teksty:
            i = teksty.index(etykieta)
            ust[klucz] = [r[i + 1], r[i + 2]]

dane = dict(przepisy=przepisy, paczki={k: list(v) for k, v in PACZKI.items()},
            spizarnia=sorted(SPIZARNIA), udzial={k: v for k, v in ust.items() if not k.startswith("_")},
            kcal=[round(v) for v in ust.get("_kcal", [2900, 1820])],
            podzial=ust.get("_podzial", [0.6, 0.4])[0], wersja="3.11.2026",
            miniatury=dict(pliki=zapisz_miniatury(), kol=MIN_KOL, wier=MIN_WIER))
js = json.dumps(dane, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
szablon = io.open(os.path.join(SP, "app", "szablon.html"), encoding="utf-8").read()
strona = szablon.replace("/*__DANE__*/null", js)
# wersja do opublikowania (claude.ai dokleja sam naglowek z kodowaniem i viewportem)
io.open(os.path.join(SP, "app", "Przepisy-planer.html"), "w", encoding="utf-8").write(strona)
# wersja do otwierania z dysku: wlasny naglowek, inaczej polskie litery sie sypia
io.open(OUT, "w", encoding="utf-8").write(
    '<!doctype html>\n<html lang="pl">\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
    'body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n' + strona + "\n</html>\n")
# lista plikow do publikacji (Artifact przyjmuje do 255 plikow na raz - dziele na paczki)
json.dump(["zdj/" + n for n, _, _ in ZAPISANE], open(os.path.join(SP, "app", "zdj_lista.json"), "w"), indent=0)
boki = sorted(w for _, w, _ in ZAPISANE)
print("przepisow:", len(przepisy), "| ze zdjeciami:", sum(1 for p in przepisy if p["z"]),
      "| kcal:", dane["kcal"], "| strona: %.2f MB" % (os.path.getsize(OUT) / 1e6),
      "| zdjec: %d, razem %.1f MB, bok min/mediana/max: %d/%d/%d px" % (
          len(ZAPISANE), sum(s for _, _, s in ZAPISANE) / 1e6, boki[0], boki[len(boki) // 2], boki[-1]))
