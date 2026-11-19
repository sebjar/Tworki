# -*- coding: utf-8 -*-
"""2.11.2026: zapisany film P080 (Salatka Big Mac, coocharz) zniknal z TikToka - przepis, link
i zdjecia z nowszej wersji autora. Klucz tt:7209232328965491974 zostaje, zeby ID sie nie zmienilo."""
import io, json

KLUCZ = "tt:7209232328965491974"
LINK = "https://www.tiktok.com/@coocharz/video/7457157431211183382"
OPIS = ("FIT Sałatka BIG MAC 🍔 Przepis: 200 g chudej wołowiny 1/2 główki sałaty lodowej "
        "1/2 czerwonej cebulki 2-3 ogórki konserwowe 30 g sera cheddar 1 łyżeczka sezamu Olej do "
        "smażenia Sos burgerowy: 120 g majonezu light 80 g ketchupu 25 g musztardy angielskiej "
        "20 ml wody z ogórków konserwowych 15 ml sosu worcestershire 1/4 łyżeczki cebuli w proszku "
        "1/4 łyżeczki czosnku granulowanego #coocharz")


def zmien_json(plik, fn):
    d = json.load(io.open(plik, encoding="utf-8"))
    fn(d)
    # parsed.json i curate_input.json sa zapisane w jednej linii, reszta z indent=0
    jedna = io.open(plik, encoding="utf-8").read().count("\n") <= 1
    json.dump(d, io.open(plik, "w", encoding="utf-8"), ensure_ascii=False, indent=None if jedna else 0)


def parsed(d):
    d[KLUCZ].update(link=LINK, caption=OPIS, author="coocharz")


def wejscie(d):
    r = next(x for x in d if x["key"] == KLUCZ)
    r.update(link=LINK, cap=OPIS, author="coocharz", tr="")


def wer(d):
    d["P080"].update(porcje="nie podano — przyjęte 2, jak w starszej wersji autora",
                     wynik="2.11.2026: zapisany film zniknął z TikToka — przepis z nowszej wersji "
                           "autora („FIT Sałatka BIG MAC”), składniki i ilości z jej opisu.")


zmien_json("parsed.json", parsed)
zmien_json("curate_input.json", wejscie)
zmien_json("weryfikacja.json", wer)
zmien_json("zdj_linki.json", lambda d: d.__setitem__("P080", LINK))


def podmien(plik, stare, nowe):
    t = io.open(plik, encoding="utf-8").read()
    assert t.count(stare) == 1, (plik, t.count(stare))
    io.open(plik, "w", encoding="utf-8").write(t.replace(stare, nowe))


# weryfikacja_dane.py czyta _stara.xlsx, ktorego tu nie ma - poprawiam go dla porzadku,
# a weryfikacja.json wyzej recznie
podmien("weryfikacja_dane.py", '"P080": "autor: 2 porcje"',
        '"P080": "nie podano — przyjęte 2, jak w starszej wersji autora"')
podmien("weryfikacja_dane.py", '    "P081": "Dopisane kcal autora (538 na wrapa).",',
        '    "P080": "2.11.2026: zapisany film zniknął z TikToka — przepis z nowszej wersji autora '
        '(„FIT Sałatka BIG MAC”), składniki i ilości z jej opisu.",\n'
        '    "P081": "Dopisane kcal autora (538 na wrapa).",')

t = io.open("curated_08.py", encoding="utf-8").read()
a = t.index('C[98] = dict(\n    name="Sałatka Big Mac"')
b = t.index("C[99] = dict(")
NOWY = '''C[98] = dict(
    name="Sałatka Big Mac", cat="Sałatka", serv=2,
    note="Zapisany przez Ciebie film z 2023 r. zniknął z TikToka — przepis i zdjęcia są z nowszej "
         "wersji tego samego autora („FIT Sałatka BIG MAC”, styczeń 2025). Autor nie podał porcji; "
         "przyjmuję 2, jak w starej wersji. Autor używa chudej wołowiny i majonezu light — w kcal "
         "liczę zwykłe, wersja light to dokładnie jego przepis. Sosu wychodzi ok. 260 g, a autor "
         "polewa „wedle uznania”; liczę cały — z połową sosu porcja ma ok. 240 kcal mniej. Wędzoną "
         "paprykę autor dodaje do sosu tylko na nagraniu, bez ilości. Stara wersja (2 porcje): "
         "150 g wołowiny, 60 g cheddara, po 3 łyżki majonezu i ketchupu, łyżka wody z ogórków, "
         "sól, pieprz, cayenne, suszony czosnek i cebula.",
    ings=[(200, "g", "mięso mielone wołowe"), (1, "łyżka", "olej"),
          (0.5, "łyżeczka", "sól"), (0.5, "łyżeczka", "pieprz"),
          (0.5, "główka", "sałata lodowa"), (0.5, "szt.", "czerwona cebula"),
          (3, "szt.", "ogórki konserwowe"), (30, "g", "cheddar"), (1, "łyżeczka", "sezam"),
          (120, "g", "majonez"), (80, "g", "ketchup"), (25, "g", "musztarda angielska"),
          (15, "ml", "sos worcestershire"), (0.25, "łyżeczka", "cebula granulowana"),
          (0.25, "łyżeczka", "czosnek granulowany"), (0.25, "łyżeczka", "papryka wędzona")],
    steps=["Na patelni z odrobiną oleju podsmaż mieloną wołowinę, dopraw solą i pieprzem.",
           "Sos burgerowy: wymieszaj majonez, ketchup, musztardę angielską, 20 ml wody z ogórków konserwowych, sos worcestershire, cebulę w proszku, czosnek granulowany i szczyptę wędzonej papryki.",
           "Posiekaj sałatę lodową, pokrój czerwoną cebulę i ogórki konserwowe, zetrzyj cheddar.",
           "Na sałatę wyłóż cebulę, ogórki, cheddar i wołowinę.",
           "Polej sosem według uznania i posyp sezamem."])

'''
io.open("curated_08.py", "w", encoding="utf-8").write(t[:a] + NOWY + t[b:])

podmien("build_v2.py", "(brak linku, film usunięty z \"\n                \"TikToka, a przy P100",
        "(brak linku, a przy \"\n                \"P100")
print("ok")
