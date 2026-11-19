# -*- coding: utf-8 -*-
"""Recznie wybrane zdjecia tam, gdzie automat trafil na twarz, surowe mieso albo opakowanie.
kNN = klatka z zdjecia_zrodla/kand (k00 = okladka), zdjNN = zdjecie z posta w zdjecia_zrodla.
Liczba po @ = srodek kwadratu w pionie (0 gora, 1 dol), domyslnie 0.55 dla pionowych kadrow."""
import json, os
import cv2
from zdj_pobierz import OUT_DIR, SRC_DIR, kwadrat

WYBOR = {
    "P001": ["k00", "k08"], "P010": ["k01", "k12"], "P040": ["k00", "k09"], "P046": ["k00", "k08"],
    "P077": ["k00", "k12"], "P085": ["k00"], "P091": ["k00", "k09"], "P096": ["k00", "k01@0.8"],
    "P100": ["k09@0.5", "k11@0.5"], "P104": ["k10", "k11"], "P110": ["k10@0.85", "k12@0.85"],
    "P112": ["k11", "k10"], "P114": ["k09", "k10"], "P119": ["k12", "k09"], "P121": ["k10", "k09"],
    "P122": ["k09", "k12"], "P125": ["k00", "k01"], "P126": ["k00", "k11"], "P129": ["k00", "k02"],
    "P134": ["k00", "k10"], "P140": ["k12@0.85", "k07"],
    # druga runda (weryfikacja 2.11): zamiast krojenia, surowego miesa i rozmazanych klatek
    "P004": ["k00", "k02"], "P011": ["k00", "k01"], "P020": ["k00", "k12"], "P036": ["k00", "k12"],
    "P058": ["k00", "k01"], "P059": ["k00", "k11"], "P060": ["k00", "k07@0.8"], "P063": ["k00", "k01"],
    "P068": ["k00", "k01"], "P069": ["k00", "k12"], "P073": ["k00", "k01"], "P087": ["k02", "k11"],
    "P108": ["k09", "k05"], "P120": ["k00", "k09"],
    # film w poscie to 8-sekundowy zlepek z pierscieniem z kurczakiem BBQ, a opis (i przepis) to
    # brownie - zdjecia kurczaka przy brownie wprowadzalyby w blad
    "P100": [],
    # jeden post ze zdjeciami na trzy przepisy: zdjecie dania + karta z produktami
    "P139": ["P139:zdj04", "P139:zdj05"], "P142": ["P139:zdj02", "P139:zdj03"],
    "P143": ["P139:zdj06", "P139:zdj07"],
    # trzecia runda (2.11, na prosbe): drugie zdjecie ma pokazywac gotowe danie, nie etap
    # gotowania, surowe skladniki ani sam dodatek; nadpisuje wczesniejsze wybory
    "P003": ["k00", "k01"], "P005": ["k00", "k10"], "P006": ["k00", "k11"], "P007": ["k00", "k12"],
    "P013": ["k00", "k11"], "P014": ["k00", "k01"], "P016": ["k00", "k12"], "P018": ["k00", "k12"],
    "P023": ["k00", "k09"], "P025": ["k00", "k01"], "P028": ["k00", "k12"], "P030": ["k00", "k12"],
    "P036": ["k00", "k01@0.75"], "P037": ["k00", "k01"], "P038": ["k00", "k12"],
    "P041": ["k00", "k10"], "P042": ["k00", "k01@1.0"], "P046": ["k00", "k12@0.65"],
    "P051": ["k00", "k12"], "P057": ["k00", "k01"], "P059": ["k00", "k11@0.85"],
    "P061": ["k00", "k11"], "P067": ["k00", "k12"], "P075": ["k00", "k01"], "P080": ["k00", "k12"],
    "P082": ["k00", "k12"], "P083": ["k00", "k09"], "P086": ["k00", "k12"], "P089": ["k00", "k09"],
    "P090": ["k00", "k12"], "P091": ["k00@0.85", "k09"], "P092": ["k00", "k10"],
    "P105": ["k00", "k11"], "P115": ["k00", "k09"], "P128": ["k00", "k11"], "P135": ["k00", "k03"],
    "P140": ["k12@0.85", "k10@0.85"], "P144": ["k00", "k01"],
    # rolki z Instagrama (linki odswiezone przez Chrome'a 2.11)
    "P002": ["k00", "k02@0.7"], "P012": ["k00", "k09"], "P019": ["k00", "k11"], "P024": ["k00", "k12"],
    "P026": ["k00", "k12"], "P029": ["k00", "k11"], "P039": ["k00", "k12"], "P045": ["k00", "k12"],
    "P049": ["k00", "k12"], "P066": ["k00", "k12"], "P070": ["k00", "k12"], "P078": ["k00", "k11"],
    "P084": ["k00", "k10"], "P109": ["k00", "k11"], "P150": ["k00", "k12"], "P151": ["k00", "k12"],
    "P152": ["k00", "k03"], "P158": ["k00", "k11"],
    # posty ze zdjeciami i blogi
    "P101": ["P101:zdj01", "P101:zdj13"], "P137": ["P137:zdj01", "P137:zdj13"],
    "P146": ["P146:zdj09", "P146:zdj08"], "P164": ["P164:zdj01", "P164:zdj09"],
    "P166": ["P166:zdj01", "P166:zdj10"],
    # po przejsciu na pelna rozdzielczosc (2.11) automat wybral tu gorsze klatki niz wczesniej;
    # przy YouTube k01-k03 to klatki 1280x720 z 1/4, 1/2 i 3/4 filmu
    "P044": ["k00", "k06"], "P076": ["k00", "k01"], "P127": ["k00", "k11"],
}


def opis(kod):
    if kod.startswith("k00"):
        return "okładka filmu"
    if kod.startswith("k"):
        return "klatka z filmu (wybrana ręcznie)"
    if not kod.startswith("P139:"):
        return "zdjęcie z bloga" if kod.startswith(("P164:", "P166:")) else "zdjęcie z posta"
    return "zdjęcie dania z posta" if kod.endswith(("zdj04", "zdj02", "zdj06")) else "karta z produktami z posta"


ZDJ = json.load(open("zdjecia.json", encoding="utf-8"))
for pid, kody in WYBOR.items():
    ZDJ[pid] = {}
    for i in (1, 2):
        p = os.path.join(OUT_DIR, "%s_%d.jpg" % (pid, i))
        if i > len(kody):
            if os.path.exists(p):
                os.remove(p)
            continue
        kod, _, sy = kody[i - 1].partition("@")
        if ":" in kod:
            zr = os.path.join(SRC_DIR, "%s_%s.jpg" % tuple(kod.split(":")))
        else:
            zr = os.path.join(SRC_DIR, "kand", "%s_%s.jpg" % (pid, kod))
        im = cv2.imread(zr)
        portret = im.shape[0] > im.shape[1] * 1.2
        cv2.imwrite(p, kwadrat(im, float(sy) if sy else (0.55 if portret else 0.5)), [cv2.IMWRITE_JPEG_QUALITY, 80])
        ZDJ[pid][str(i)] = opis(kod)
json.dump(ZDJ, open("zdjecia.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("ustawione:", len(WYBOR))
