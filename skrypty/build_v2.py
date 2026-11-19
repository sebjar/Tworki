# -*- coding: utf-8 -*-
"""Buduje planer: recznie opracowane przepisy + reszta z automatu."""
import collections, glob, importlib.util, json, os, re, sys
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image as XLImage
from openpyxl.drawing.spreadsheet_drawing import TwoCellAnchor, AnchorMarker

SP = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SP)
from normalize import normalize
from parse import parse_qty, PRETTY
from classify import category_of, find_similar
from nutrition import macros as ing_macros, NUTR
from macros_calc import author_macros, is_whole_dish
from lightdata import LIGHT
from odgrzewanie import odgrzewanie

OUT = r"C:\Users\Sebastian\Documents\Przepisy-planer\Przepisy-planer.xlsx"

F = "Arial"
HDR_FILL = PatternFill("solid", fgColor="2F5233")
HDR_FONT = Font(name=F, bold=True, color="FFFFFF", size=10)
BASE = Font(name=F, size=10)
CALC = Font(name=F, size=10, color="808080", italic=True)
WARN = Font(name=F, size=10, color="9C5700")
INPUT_FILL = PatternFill("solid", fgColor="FFFDE7")
WARN_FILL = PatternFill("solid", fgColor="FFF3CD")
OK_FILL = PatternFill("solid", fgColor="E8F5E9")
SUG_FILL = PatternFill("solid", fgColor="DDEBF7")
THIN = Side(style="thin", color="D9D9D9")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

DZIALY = ["Warzywa i owoce", "Mięso i ryby", "Nabiał i jaja", "Pieczywo", "Sypkie i makarony",
          "Oleje i sosy", "Konserwy i słoiki", "Przyprawy i zioła", "Mrożonki", "Napoje",
          "Słodycze i przekąski", "Inne"]
JEDNOSTKI = ["g", "kg", "ml", "l", "dag", "szt.", "łyżka", "łyżeczka", "szklanka", "ząbek",
             "puszka", "opak.", "garść", "szczypta", "plaster", "pęczek", "główka", "oz", "lbs"]
KATEGORIE = ["Śniadanie", "Obiad", "Kolacja", "Przekąska", "Deser", "Zupa", "Sałatka",
             "Napój", "Sos / dodatek"]
POSILKI = ["Śniadanie", "Obiad", "Kolacja", "Przekąska"]
DNI = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"]

STEPS_FROM_FILE = {
    "Ziemniaczane talarki": [
        "Ziemniaki kroimy na plastry.",
        "Wkładamy na około 20 min do lodowatej wody, następnie osuszamy na ręczniku papierowym.",
        "Dodajemy ulubione przyprawy (oprócz soli, którą dodamy po upieczeniu), oliwę i parmezan. Mieszamy.",
        "Wykładamy płasko na blaszce tak, aby talarki się nie dotykały, i pieczemy ok. 20 min w 200°C."],
    "Kurczak ze szpinakiem": [
        "Przesmażyć kurczaka na oliwie.", "Doprawić solą, pieprzem, papryką i oregano.",
        "Usmażony przerzucić do innej miski.", "Podsmażyć cebulę w kostkę i dodać soli.",
        "Dodać czosnek, pastę pomidorową i płatki chilli.",
        "Wlać wodę, śmietankę i trochę soli.", "Ugotować na tym makaron.",
        "Dodać pokrojone suszone pomidory, szpinak i kurczaka."],
    "Tacos 1": [
        "Na placek tortilli wyłóż mięso mielone. Posól i podsmaż stroną z mięsem na złoty kolor.",
        "Przewróć na drugą stronę i dodaj ser cheddar. Podsmaż 2-3 min.",
        "Na środek wyłóż sos, posiekaną sałatę i plastry ogórków konserwowych. Złóż na pół."],
}


YT_KANAL = {"I4OHJX2EdT0": "Policzona Szama", "RFwsegemstE": "Policzona Szama",
            "iK4ab0eXFJY": "Policzona Szama", "wBJL1edWlQI": "Top Gar"}
SMIECI_AUTOR = {"", "@", "-", "?", "none", "null"}


def author_of(autor, link):
    """Kolumna Autor ma mowic, czyj to przepis. Puste i smieciowe wpisy uzupelniam
    z linku; gdy podany autor to co innego niz konto, z ktorego wisi film, pokazuje oba."""
    a = (autor or "").strip()
    link = link or ""
    m = re.search(r"tiktok\.com/@([\w.]+)", link) or         re.search(r"instagram\.com/([\w.]+)/(?:reel|p)/", link)
    konto = m.group(1) if m else ""
    if not konto:
        m = re.search(r"youtu(?:\.be/|be\.com/watch\?v=)([\w-]{11})", link)
        if m:
            konto = YT_KANAL.get(m.group(1), "")
        else:
            m = re.search(r"https?://(?:www\.)?([\w-]+\.[\w.-]+)/", link)
            konto = m.group(1) if m else ""
    if a.lower() in SMIECI_AUTOR:
        return konto
    if not konto or a.lower() == konto.lower():
        return a
    # nazwa wyswietlana (spacje, emoji) obok uchwytu - to normalne, nie dopisuje
    if " " in a or any(ord(c) > 127 for c in a):
        return a
    return "%s (@%s)" % (a, konto)


def platform_of(link):
    if "tiktok.com" in (link or ""):
        return "TikTok"
    if "instagram.com" in (link or ""):
        return "Instagram"
    if "youtu" in (link or ""):
        return "YouTube"
    return "Blog" if link else "Inne"


# ------------------------------------------------ wczytaj recznie opracowane
CUR = {}
for path in sorted(glob.glob(SP + "/curated_*.py")):
    spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    CUR.update(mod.C)

rows_in = json.load(open(SP + "/curate_input.json", encoding="utf-8"))
idx2key = {i: r["key"] for i, r in enumerate(rows_in)}
cur_by_key = {idx2key[i]: e for i, e in CUR.items() if i in idx2key}

data = json.load(open(SP + "/parsed.json", encoding="utf-8"))
enr = json.load(open(SP + "/enriched.json", encoding="utf-8"))
BAD_BLOG = {"Creamy Chicken & Brown Butter Pasta", "Butter chicken"}

# --- moje propozycje (sugestie.py): przepisy spoza Twoich zapisanych, opracowane recznie
from sugestie import SUGESTIE, DATA as SUG_DATA
SUG = {}
for s in SUGESTIE:
    k = "sugestia:" + s["link"]
    data[k] = dict(name=s["name"], author=s["author"], link=s["link"], parsed={}, file_ings=[])
    cur_by_key[k] = s
    SUG[k] = s

recipes, ing_rows, used = [], [], {}

for key, r in data.items():
    p = r["parsed"]
    cur = cur_by_key.get(key)

    name = (cur["name"] if cur else (r["name"] or p["name"] or "")).strip()
    if not name:
        name = "Bez nazwy (@%s)" % (r["author"] or "?")
    name = re.sub(r"\s+", " ", name)[:70]
    n = used.get(name.lower(), 0) + 1
    used[name.lower()] = n
    if n > 1:
        name = "%s (%d)" % (name, n)

    items, quality = [], "auto"
    if cur:
        quality = "ręcznie"
        for qty, unit, ing in cur["ings"]:
            canon, section, known = normalize(ing)
            if not canon:
                continue
            items.append(dict(ing=canon, qty=round(float(qty), 3),
                              unit=unit if unit in JEDNOSTKI else "szt.",
                              section=section, raw=ing[:60], ok=True))
        steps = cur.get("steps") or []
        serv = float(cur.get("serv") or 2)
        serv_guess = False
        cat = cur.get("cat") or ""
    else:
        src = r["file_ings"] or p["ings"]
        blog = enr.get(key)
        if blog and (r["name"] or "") not in BAD_BLOG and len(src) < 3:
            quality = "blog"
            src = []
            for line in blog["recipe"]["ingredients"]:
                q, u, rest = parse_qty(line)
                src.append({"qty": q, "unit": u, "ing": rest or line})
        for i in src:
            raw_name = i.get("ing") or ""
            qty, unit = i.get("qty"), i.get("unit")
            if not isinstance(qty, (int, float)) or unit is None:
                q2, u2, rest2 = parse_qty(raw_name)
                if q2 is not None:
                    qty, unit, raw_name = q2, (u2 or unit), (rest2 or raw_name)
            canon, section, known = normalize(raw_name)
            if not canon:
                continue
            if not isinstance(qty, (int, float)):
                qty, known = 1.0, False
            unit = PRETTY.get(unit, unit) if unit else None
            if unit not in JEDNOSTKI:
                unit, known = "szt.", False
            items.append(dict(ing=canon, qty=round(float(qty), 3), unit=unit,
                              section=section, raw=raw_name.strip()[:60], ok=known))
        steps = STEPS_FROM_FILE.get(name) or (
            blog["recipe"]["steps"] if (blog and quality == "blog") else None) or \
            r.get("steps") or p.get("steps") or []
        serv = r.get("servings") or p.get("servings")
        serv_guess = False
        try:
            serv = float(serv)
            if not (0 < serv <= 24):
                raise ValueError
        except (TypeError, ValueError):
            serv, serv_guess = 2.0, True
        cat = r.get("cat") if r.get("cat") in KATEGORIE else ""

    merged = {}
    for it in items:
        k2 = (it["ing"], it["unit"])
        if k2 in merged:
            merged[k2]["qty"] = round(merged[k2]["qty"] + it["qty"], 3)
        else:
            merged[k2] = it
    items = list(merged.values())

    steps = [re.sub(r"\s+", " ", s).strip() for s in steps if s and len(s.strip()) > 8][:16]

    recipes.append(dict(src=key, name=name, platform=platform_of(r.get("link")),
                        author=author_of(r.get("author"), r.get("link")),
                        link=r.get("link") or "",
                        serv=serv, serv_guess=serv_guess, cat=cat, quality=quality,
                        n_ing=len(items), steps=steps, note=(cur or {}).get("note", ""),
                        sug=key in SUG, powod=(cur or {}).get("powod", "")))
    for it in items:
        ing_rows.append(dict(recipe=name, **it))

# --- makra: z opisu autora, w razie braku wyliczone ze skladnikow
src_txt = {}
for i, rr in enumerate(rows_in):
    if rr.get("link"):
        src_txt[rr["link"]] = " ".join(filter(None, [rr.get("cap"), rr.get("blog") or ""]))
tot_m = {}
for x in ing_rows:
    m = ing_macros(x["ing"], x["unit"], x["qty"])
    if m is None:
        continue
    t = tot_m.setdefault(x["recipe"], [0.0, 0.0, 0.0, 0.0])
    for i in range(4):
        t[i] += m[i]
for r in recipes:
    calc = tot_m.get(r["name"])
    per = tuple(round(v / r["serv"]) for v in calc) if (calc and r["serv"]) else None
    auth = author_macros(src_txt.get(r["link"], "")) if r["link"] else None
    # straznik: wartosc autora rzadu <35%% wyliczonej to prawie na pewno zly odczyt
    if auth and per and auth[0] and per[0] and auth[0] < 0.35 * per[0]:
        auth = None
    # Makra licze ZAWSZE sam, ta sama metoda dla kazdego przepisu.
    # Wartosci autora ida obok, jako niezalezna kontrola.
    r["kcal"], r["mB"], r["mT"], r["mW"] = per if per else (None,) * 4
    if auth and is_whole_dish(src_txt.get(r["link"], "")) and r["serv"]:
        # autor podal makra za cale danie - sprowadzamy do jednej porcji
        auth = tuple(round(v / r["serv"]) if v is not None else None for v in auth)
    r["aK"], r["aB"], r["aT"], r["aW"] = auth if auth else (None,) * 4
    ov = (cur_by_key.get(r["src"]) or {}).get("autor_makra")
    if ov:                     # juz przeliczone na porcje z arkusza
        r["aK"], r["aB"], r["aT"], r["aW"] = ov

    if r["aK"] and r["kcal"]:
        d = (r["aK"] - r["kcal"]) / r["kcal"] * 100
        if abs(d) <= 10:
            r["msrc"] = "zgodne (%+.0f%%)" % d
        elif d < 0:
            r["msrc"] = "autor zaniża o %.0f%%" % -d
        else:
            r["msrc"] = "autor zawyża o %.0f%%" % d
    elif r["aK"]:
        r["msrc"] = "tylko dane autora"
    elif r["kcal"]:
        r["msrc"] = "autor nie podał"
    else:
        r["msrc"] = ""

# kategorie: reczna wygrywa, reszta z regul
ings_by = {}
for x in ing_rows:
    ings_by.setdefault(x["recipe"], []).append(x["ing"])
for r in recipes:
    if not r["cat"]:
        r["cat"] = category_of(r["name"], ings_by.get(r["name"], []))
SIM = find_similar(recipes, ings_by)
# recznie dopisane pary, ktorych heurystyka nie zlapie (rozne nazwy, urwane dane)
for a, b in [("Tacos 1 — niepełny wpis z Twojego pliku",
              "Tacos z mięsem mielonym i cheddarem"),
             ("Arayes (bliskowschodnie pity z mięsem)", "Arayes z kurczakiem"),
             ("Carbonara na patelni (Instagram)", "Carbonara"),
             ("Spaghetti all'assassina (hannahyoussef)", "Spaghetti all'assassina"),
             ("Chicken Tikka Masala (jalalsamfit)", "Tikka masala")]:
    names = {r["name"] for r in recipes}
    if a in names and b in names:
        SIM.setdefault(a, []).append(b)
        SIM.setdefault(b, []).append(a)
for r in recipes:
    r["similar_names"] = sorted(set(SIM.get(r["name"], [])))
    r["similar"] = ""

# --- ujednolicenie jednostek: bez tego "sól" ma na liscie zakupow 4 osobne wiersze
from nutrition import grams as _g
_units = {}
for x in ing_rows:
    _units.setdefault(x["ing"], collections.Counter())[x["unit"]] += 1

SMALL = {"szczypta", "łyżeczka", "łyżka"}
# szklanki nie ma na etykiecie w sklepie - na liscie zakupow pokazuje wage albo objetosc
PLYNY = {"piwo", "wódka", "woda gazowana", "woda", "mleko", "kefir", "sok jabłkowy",
         "śmietana kremówka", "śmietana 12%", "śmietana 18%", "wino białe", "bulion"}


def primary_unit(name, cnt):
    u = set(cnt)
    if u == {"szklanka"}:
        return "ml" if name in PLYNY else "g"
    if len(u) == 1:
        return next(iter(u))
    if u <= SMALL:
        return "łyżeczka"
    if u & {"g", "kg", "dag"}:
        return "g"
    if "szt." in u:            # sztuki przed objetoscia: limonke kupuje sie na sztuki
        return "szt."
    if u & {"ml", "l"}:
        return "ml"
    return cnt.most_common(1)[0][0]


# W arkuszu Skladniki ZOSTAWIAMY jednostki kuchenne (szczypta, lyzka) - tak sie gotuje.
# Scalanie do jednej jednostki robimy dopiero na liscie zakupow.
PRIMARY = {n: primary_unit(n, c) for n, c in _units.items()}
from nutrition import FRYING, FRY_MIN_G, FRY_ABSORB
# przepisy, w ktorych makaron/ryz gotuje sie w wodzie z listy (one-pan) - tam woda
# juz siedzi w wadze, wiec nie doliczamy drugi raz tego, co ziarno wciagnie
_WODA = {x["recipe"] for x in ing_rows
         if x["ing"] == "woda" and _g(x["ing"], x["unit"], x["qty"]) >= 100}
MIESO = {"pierś z kurczaka", "udka z kurczaka", "kurczak", "polędwiczki z kurczaka",
         "mięso mielone", "mięso mielone wołowe", "mięso mielone wieprzowe",
         "mięso mielone z kurczaka", "mięso mielone z indyka", "wołowina",
         "wołowina w paskach", "schab", "indyk", "żeberka wieprzowe", "jagnięcina", "mięso"}
RYBY = {"łosoś", "pstrąg", "ryba biała"}


def wydajnosc(nazwa, przepis):
    """Ile razy zmienia sie waga skladnika po ugotowaniu. To szacunek - liczymy tylko
    te zmiany, ktore naprawde przestawiaja wage porcji."""
    kcal = (NUTR.get(nazwa) or (0,))[0]
    if kcal >= 300 and przepis not in _WODA:          # suchy produkt, nie z puszki
        if nazwa.startswith("makaron"):
            return 2.25
        if nazwa.startswith(("ryż", "kasza", "soczewica")):
            return 2.5
    if nazwa in MIESO:
        return 0.75
    if nazwa in RYBY:
        return 0.8
    if nazwa == "boczek":
        return 0.5
    return 1.0


for x in ing_rows:
    x["g"] = _g(x["ing"], x["unit"], 1)      # ile gramow wazy 1 jednostka tego wiersza
    x["wyd"] = wydajnosc(x["ing"], x["recipe"])
    n = NUTR.get(x["ing"])
    l = LIGHT.get(x["ing"])
    # wspolczynniki "na jedna jednostke" - arkusz mnozy je przez kolumne Ilosc,
    # dzieki czemu zmiana ilosci od razu przelicza makra
    x["f"] = tuple(x["g"] * v / 100.0 for v in n[:4]) if n else None
    x["fl"] = tuple(x["g"] * v / 100.0 for v in (l[1:5] if l else (n[:4] if n else (0,) * 4)))
    # olej do glebokiego smazenia: powyzej progu do jedzenia wchodzi tylko czesc
    x["fry"] = x["ing"] in FRYING and x["unit"] in ("g", "ml", "l")

# --- wersja light: to samo danie na odchudzonych produktach
tot_l = {}
for x in ing_rows:
    g = _g(x["ing"], x["unit"], x["qty"])
    n = NUTR.get(x["ing"])
    l = LIGHT.get(x["ing"])
    x["light"] = l[0] if l else ""
    x["dkcal"] = 0
    if n and l:
        x["dkcal"] = round((n[0] - l[1]) * g / 100)
    t = tot_l.setdefault(x["recipe"], [0.0, 0.0, 0.0, 0.0])
    src = l[1:5] if l else (n[:4] if n else None)
    if src:
        for i in range(4):
            t[i] += src[i] * g / 100
_skl = {}
for x in ing_rows:
    _skl.setdefault(x["recipe"], []).append(x["ing"])
for r in recipes:
    r["odgrz"], r["odgrz_jak"] = odgrzewanie(
        r["name"], " ".join(_skl.get(r["name"], [])), " ".join(r["steps"]))
    # przy ryzu uwaga o szybkim schlodzeniu jest wazniejsza niz smak - dopisujemy ja zawsze
    if (r["odgrz"].startswith("Tak") and "ryż" not in r["odgrz_jak"].lower()
            and any(i.startswith("ryż") for i in _skl.get(r["name"], []))):
        r["odgrz_jak"] += (" Ryż wstaw do lodówki w ciągu godziny i zjedz w 24 h, "
                           "odgrzewając do gorąca.")
for r in recipes:
    calc = tot_l.get(r["name"])
    if calc and r["serv"] and r["kcal"]:
        r["kcalL"], r["mBL"], r["mTL"], r["mWL"] = (round(v / r["serv"]) for v in calc)
        r["oszcz"] = r["kcal"] - r["kcalL"]
        # wypisujemy tylko te zamiany, ktore realnie cos daja
        sw = [(x["ing"], x["dkcal"]) for x in ing_rows
              if x["recipe"] == r["name"] and x["dkcal"] >= 15]
        sw.sort(key=lambda t: -t[1])
        r["swap"] = ", ".join("%s → %s" % (n, LIGHT[n][0]) for n, _d in sw)
    else:
        r["kcalL"] = r["mBL"] = r["mTL"] = r["mWL"] = None
        r["oszcz"], r["swap"] = None, ""

QORD = {"ręcznie": 0, "blog": 1, "auto": 2}
recipes.sort(key=lambda x: (QORD[x["quality"]], -x["n_ing"], x["name"].lower()))
order_r = {r["name"]: i for i, r in enumerate(recipes)}
ing_rows.sort(key=lambda x: order_r.get(x["recipe"], 9999))

# ID przepisu jest staly miedzy wersjami arkusza: ids.json pamieta numer kazdego przepisu.
# Nowe przepisy dostaja kolejne wolne numery, a numery usunietych nie wracaja do obiegu,
# zeby "P046" zawsze znaczylo to samo danie. Pierwsze numery pochodza z wersji z 15.09.2026.
IDS_PATH = SP + "/ids.json"
if os.path.exists(IDS_PATH):
    IDS = json.load(open(IDS_PATH, encoding="utf-8"))
else:
    IDS = json.load(open(SP + "/ids_wrzesien.json", encoding="utf-8"))["ids"]
nastepny = max([int(v[1:]) for v in IDS.values()] or [0]) + 1
for s in SUGESTIE:                     # propozycje numerujemy w kolejnosci z listy
    if "sugestia:" + s["link"] not in IDS:
        IDS["sugestia:" + s["link"]] = "P%03d" % nastepny
        nastepny += 1
for r in recipes:                      # nowe numerujemy w dotychczasowym porzadku sortowania
    if r["src"] not in IDS:
        IDS[r["src"]] = "P%03d" % nastepny
        nastepny += 1
    r["id"] = IDS[r["src"]]
    r["key"] = "%s: %s" % (r["id"], r["name"])
json.dump(IDS, open(IDS_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
recipes.sort(key=lambda x: int(x["id"][1:]))
order_r = {r["name"]: i for i, r in enumerate(recipes)}
ing_rows.sort(key=lambda x: order_r.get(x["recipe"], 9999))
# wiersze dopisane recznie pod lista dostaja numery od pierwszego wolnego
ID_OFFSET = max(int(r["id"][1:]) for r in recipes) - len(recipes)
KEY = {r["name"]: r["key"] for r in recipes}
RID = {r["name"]: r["id"] for r in recipes}
for x in ing_rows:
    x["rkey"] = KEY.get(x["recipe"], x["recipe"])
# w "Podobne do" ma byc ID i nazwa - po ID trafiasz do wiersza bez szukania
for r in recipes:
    r["similar"] = ", ".join(KEY[m] for m in sorted(r["similar_names"],
                                                    key=lambda m: RID.get(m, "")))

n_man = sum(1 for r in recipes if r["quality"] == "ręcznie")
n_ing = sum(1 for r in recipes if r["n_ing"] > 0)
n_steps = sum(1 for r in recipes if r["steps"])
n_check = sum(1 for x in ing_rows if not x["ok"])
n_sim = sum(1 for r in recipes if r["similar"])
sug_r = [r for r in recipes if r["sug"]]
n_sug = len(sug_r)
sug_zakres = "%s-%s" % (sug_r[0]["id"], sug_r[-1]["id"]) if sug_r else ""
sug_autorzy = []
for r in sug_r:
    if r["platform"] == "Instagram" and r["author"] not in sug_autorzy:
        sug_autorzy.append(r["author"])
n_sug_ig = sum(1 for r in sug_r if r["platform"] == "Instagram")
print("Przepisow: %d | opracowanych recznie: %d | ze skladnikami: %d | z przygotowaniem: %d"
      % (len(recipes), n_man, n_ing, n_steps))
print("Wierszy skladnikow: %d | do sprawdzenia: %d | oznaczonych jako podobne: %d"
      % (len(ing_rows), n_check, n_sim))

# ------------------------------------------------ skoroszyt
wb = openpyxl.Workbook()


def sprawdz(f):
    """Pilnuje, zeby formula miala zbilansowane nawiasy. Nawiasy w cudzyslowach
    sie nie licza - "zgodne (" to zwykly tekst, a nie otwarcie funkcji."""
    if not isinstance(f, str) or not f.startswith("="):
        return f
    głęb, w_tekscie = 0, False
    for ch in f:
        if ch == '"':
            w_tekscie = not w_tekscie
        elif not w_tekscie:
            if ch == "(":
                głęb += 1
            elif ch == ")":
                głęb -= 1
                if głęb < 0:
                    raise ValueError("nawias zamykajacy bez otwierajacego: " + f)
    if głęb:
        raise ValueError("niezbilansowane nawiasy (%+d): %s" % (głęb, f))
    if w_tekscie:
        raise ValueError("niedomkniety cudzyslow: " + f)
    return f


def head(ws, headers, widths, height=30):
    for ci, h in enumerate(headers, start=1):
        c = ws.cell(row=1, column=ci, value=h)
        c.font = HDR_FONT
        c.fill = HDR_FILL
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws.column_dimensions[get_column_letter(ci)].width = widths[ci - 1]
    ws.row_dimensions[1].height = height


# zdjecia dania: kwadraty 150 px pod nazwa przepisu, w tej samej komorce
ZDJ_DIR = SP + "/zdjecia"
ZDJ_PX, ZDJ_GORA, ZDJ_LEWO, ZDJ_ODST, EMU = 150, 22, 4, 6, 9525
ZDJ_WIERSZ = (ZDJ_GORA + ZDJ_PX + 6) * 0.75          # wysokosc wiersza w punktach


def zdjecia_przepisu(pid):
    return [p for p in ("%s/%s_%d.jpg" % (ZDJ_DIR, pid, i) for i in (1, 2)) if os.path.exists(p)]


def zdjecie_xl(p, bok=300):
    """Pliki maja do 1080 px, w arkuszu wyswietlam 150 px - 300 px jest ostre tez na ekranach
    HiDPI (x2), a arkusz nie puchnie."""
    import io
    from PIL import Image as PILImage
    b = io.BytesIO()
    PILImage.open(p).convert("RGB").resize((bok, bok), PILImage.LANCZOS).save(b, "JPEG", quality=85)
    b.seek(0)
    return XLImage(b)


def wstaw_zdjecia(ws, row, col0, pid):
    """Kotwica "twoCell": przy filtrowaniu zdjecia chowaja sie razem z wierszem,
    a przy sortowaniu jada razem z nim."""
    pliki = zdjecia_przepisu(pid)
    for i, p in enumerate(pliki):
        img = zdjecie_xl(p)
        img.width = img.height = ZDJ_PX
        x = ZDJ_LEWO + i * (ZDJ_PX + ZDJ_ODST)
        img.anchor = TwoCellAnchor(
            editAs="twoCell",
            _from=AnchorMarker(col=col0, colOff=x * EMU, row=row - 1, rowOff=ZDJ_GORA * EMU),
            to=AnchorMarker(col=col0, colOff=(x + ZDJ_PX) * EMU, row=row - 1,
                            rowOff=(ZDJ_GORA + ZDJ_PX) * EMU))
        ws.add_image(img)
    return len(pliki)


def dv(ws, rng, src):
    d = DataValidation(type="list", formula1=src, allow_blank=True, showDropDown=False)
    ws.add_data_validation(d)
    d.add(rng)


ws = wb.active
ws.title = "Ustawienia"
for ci, (nm, vals) in enumerate([("Kategorie", KATEGORIE), ("Jednostki", JEDNOSTKI),
                                 ("Działy sklepu", DZIALY), ("Posiłki", POSILKI)], start=1):
    c = ws.cell(row=1, column=ci, value=nm)
    c.font = HDR_FONT
    c.fill = HDR_FILL
    for ri, v in enumerate(vals, start=2):
        ws.cell(row=ri, column=ci, value=v).font = BASE
    ws.column_dimensions[get_column_letter(ci)].width = 22
# klucz przepisu dla list rozwijanych - liczy sie sam, wiec obejmie tez recznie dopisane
c = ws.cell(row=1, column=5, value="Przepisy (ID: nazwa)")
c.font = HDR_FONT
c.fill = HDR_FILL
for ri in range(2, len(recipes) + 41):
    ws.cell(row=ri, column=5, value='=IF(Przepisy!$B{0}="","",Przepisy!$A{0}&": "&Przepisy!$B{0})'
            .format(ri)).font = CALC
ws.column_dimensions["E"].width = 54

# --- kto to je: z tego licza sie porcje na posilek w arkuszu Przepisy
OSOBY = [("Płeć (M albo K)", "M", "K"), ("Wiek (lat)", 30, 30), ("Wzrost (cm)", 195, 170),
         ("Waga (kg)", 100, 55), ("Aktywność (1,2-1,9)", 1.4, 1.4)]
for ci, nm in ((13, "Wasze dane"), (14, "Ty"), (15, "Ona")):
    c = ws.cell(row=1, column=ci, value=nm)
    c.font = HDR_FONT
    c.fill = HDR_FILL
    c.alignment = Alignment(horizontal="center", vertical="center")
for ri, (etykieta, a, b) in enumerate(OSOBY, start=2):
    ws.cell(row=ri, column=13, value=etykieta).font = BASE
    for ci, v in ((14, a), (15, b)):
        c = ws.cell(row=ri, column=ci, value=v)
        c.font = BASE
        c.fill = INPUT_FILL
        c.alignment = Alignment(horizontal="center")
# wiersze: 2 plec, 3 wiek, 4 wzrost, 5 waga, 6 aktywnosc
for ri, etykieta, wzor in (
        (7, "Przemiana spoczynkowa (BMR)",
         '=10*{0}5+6.25*{0}4-5*{0}3+IF(UPPER({0}2)="M",5,-161)'),
        (8, "Zapotrzebowanie na dzień", "={0}7*{0}6")):
    ws.cell(row=ri, column=13, value=etykieta).font = Font(name=F, size=10, bold=True)
    for ci in (14, 15):
        kol = get_column_letter(ci)
        c = ws.cell(row=ri, column=ci, value=sprawdz(wzor.format(kol)))
        c.font = CALC
        c.number_format = "0"
        c.alignment = Alignment(horizontal="center")
ws.cell(row=10, column=13, value="Podział jedzenia z garnka").font = Font(
    name=F, size=10, bold=True)
for ci, v in ((14, 0.6), (15, 0.4)):
    c = ws.cell(row=10, column=ci, value=v)
    c.font = BASE
    c.fill = INPUT_FILL
    c.number_format = "0%"
    c.alignment = Alignment(horizontal="center")
ws.cell(row=9, column=13, value="Liczby liczą się same wzorem Mifflina-St Jeora. "
                                "Zmień wiek albo aktywność i porcje, gramy i kalorie "
                                "w Przepisach przeliczą się na nowo.").font = CALC

# --- ile procent dziennego zapotrzebowania to jeden posilek danej kategorii
UDZIALY = [("Śniadanie", 0.25), ("Obiad", 0.35), ("Kolacja", 0.30), ("Zupa", 0.25),
           ("Sałatka", 0.30), ("Przekąska", 0.12), ("Deser", 0.12), ("Napój", 0.05),
           ("Sos / dodatek", 0.05)]
for ci, nm in ((17, "Kategoria"), (18, "Udział posiłku w dniu")):
    c = ws.cell(row=1, column=ci, value=nm)
    c.font = HDR_FONT
    c.fill = HDR_FILL
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
for ri, (kat, u) in enumerate(UDZIALY, start=2):
    ws.cell(row=ri, column=17, value=kat).font = BASE
    c = ws.cell(row=ri, column=18, value=u)
    c.font = BASE
    c.fill = INPUT_FILL
    c.number_format = "0%"
    c.alignment = Alignment(horizontal="center")
for col, w in (("M", 30), ("N", 12), ("O", 12), ("Q", 18), ("R", 14)):
    ws.column_dimensions[col].width = w
# na czym licze wersje light - widoczne i do poprawienia, jesli kupujesz co innego
for ci, nm in ((7, "Produkt"), (8, "Wersja light"), (9, "kcal/100 g zwykły"),
               (10, "kcal/100 g light"), (11, "Kiedy uważać")):
    c = ws.cell(row=1, column=ci, value=nm)
    c.font = HDR_FONT
    c.fill = HDR_FILL
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
for ri, (prod, l) in enumerate(sorted(LIGHT.items(),
                                      key=lambda t: -(NUTR.get(t[0], (0,))[0] - t[1][1])), start=2):
    ws.cell(row=ri, column=7, value=prod).font = BASE
    ws.cell(row=ri, column=8, value=l[0]).font = BASE
    ws.cell(row=ri, column=9, value=NUTR.get(prod, (None,))[0]).font = BASE
    ws.cell(row=ri, column=10, value=l[1]).font = BASE
    c = ws.cell(row=ri, column=11, value=l[5])
    c.font = BASE
    c.alignment = Alignment(wrap_text=True, vertical="top")
    if l[5]:
        ws.row_dimensions[ri].height = 30
for col, w in (("G", 24), ("H", 30), ("I", 16), ("J", 15), ("K", 74)):
    ws.column_dimensions[col].width = w
ws.freeze_panes = "A2"

ws = wb.create_sheet("Przepisy")
head(ws, ["ID", "Nazwa przepisu", "Kategoria", "Źródło", "Autor", "Link", "Porcje bazowe",
          "Składników", "Opracowanie", "Przygotowanie", "Podobne do",
          "kcal / porcję", "Białko (g)", "Tłuszcz (g)", "Węgle (g)",
          "kcal — autor", "Białko — autor", "Tłuszcz — autor", "Węgle — autor",
          "Zgodność z autorem",
          "kcal — wersja light", "Tłuszcz light (g)", "Mniej kcal", "Co zamienić na light",
          "W Planie na dzień", "Ugotuj razem (2 dni)", "Twoja porcja ≈ g",
          "Jej porcja ≈ g", "Twoja porcja (kcal)", "Jej porcja (kcal)",
          "Uwaga do porcji", "Na drugi dzień", "Jak odgrzewać", "Skąd"],
     [7, 46, 14, 12, 20, 44, 9, 10, 13, 88, 54, 12, 11, 11, 10, 12, 12, 12, 11, 22,
      13, 12, 11, 60, 12, 12, 12, 12, 12, 12, 40, 24, 74, 26])
MAXP = len(recipes) + 40
for i, r in enumerate(recipes):
    row = 2 + i
    ws.cell(row=row, column=2, value=r["name"])
    ws.cell(row=row, column=3, value=r["cat"])
    ws.cell(row=row, column=4, value=r["platform"])
    ws.cell(row=row, column=5, value=r["author"])
    if r["link"]:
        c = ws.cell(row=row, column=6, value=r["link"])
        c.hyperlink = r["link"]
        c.font = Font(name=F, size=9, color="0563C1", underline="single")
    ws.cell(row=row, column=7, value=r["serv"])
    ws.cell(row=row, column=9, value=r["quality"])
    txt = "\n".join("%d. %s" % (n, s) for n, s in enumerate(r["steps"], 1))
    if r["note"]:
        txt = ("UWAGA: %s\n\n" % r["note"]) + txt
    if txt:
        ws.cell(row=row, column=10, value=txt)
    if r["similar"]:
        c = ws.cell(row=row, column=11, value=r["similar"])
        c.font = WARN
    for off, key in enumerate(("aK", "aB", "aT", "aW")):
        if r[key] is not None:
            c = ws.cell(row=row, column=16 + off, value=r[key])
            c.font = CALC
    if r["swap"]:
        ws.cell(row=row, column=24, value=r["swap"])
    if r["odgrz"]:
        ws.cell(row=row, column=32, value=r["odgrz"])
        ws.cell(row=row, column=33, value=r["odgrz_jak"])
    ws.cell(row=row, column=34, value=("Sugestia Claude " + SUG_DATA) if r["sug"]
            else "Twoje zapisane")
    ws.row_dimensions[row].height = 15 if not r["steps"] else min(210, 13.5 * len(r["steps"]) + 10)
    if wstaw_zdjecia(ws, row, 1, r["id"]):
        ws.row_dimensions[row].height = max(ws.row_dimensions[row].height, ZDJ_WIERSZ)

KLUCZ = '$A{0}&": "&$B{0}'          # tym kluczem wiersze Skladnikow wskazuja przepis


def sumif(row, kol):
    return 'SUMIF(Składniki!$A:$A,%s,Składniki!$%s:$%s)' % (KLUCZ.format(row), kol, kol)


for row in range(2, MAXP + 1):
    # ID wpisane na stale, a nie liczone z numeru wiersza. Gdyby liczylo sie z wiersza,
    # skasowanie jednego przepisu przesunelo by numery wszystkich ponizej, a wiersze
    # w Skladnikach i w Planie wskazywalyby wtedy na cudze dania.
    if row - 2 < len(recipes):
        ws.cell(row=row, column=1, value=recipes[row - 2]["id"])
    else:
        ws.cell(row=row, column=1, value='=IF($B%d="","","P"&TEXT(ROW()-1+%d,"000"))'
                % (row, ID_OFFSET))
    # liczba skladnikow, makra i wersja light licza sie same z arkusza Skladniki
    ws.cell(row=row, column=8, value='=IF($B{0}="","",COUNTIF(Składniki!$A:$A,{1}))'
            .format(row, KLUCZ.format(row)))
    for off, kol in enumerate("LMNO"):
        ws.cell(row=row, column=12 + off, value=(
            '=IF(OR($B{0}="",$H{0}=0),"",IFERROR(ROUND({1}/$G{0}),""))'
            .format(row, sumif(row, kol))))
    ws.cell(row=row, column=20, value=sprawdz(
        '=IF($B{0}="","",IF($P{0}="",IF($L{0}="","","autor nie podał"),'
        'IF($L{0}="","tylko dane autora",'
        'IF(ABS($P{0}-$L{0})<=0.1*$L{0},"zgodne ("&TEXT(($P{0}-$L{0})/$L{0},"+0%;-0%")&")",'
        'IF($P{0}<$L{0},"autor zaniża o "&TEXT(($L{0}-$P{0})/$L{0},"0%"),'
        '"autor zawyża o "&TEXT(($P{0}-$L{0})/$L{0},"0%"))))))'.format(row)))
    ws.cell(row=row, column=21, value=(
        '=IF(OR($B{0}="",$H{0}=0),"",IFERROR(ROUND({1}/$G{0}),""))'
        .format(row, sumif(row, "P"))))
    ws.cell(row=row, column=22, value=(
        '=IF(OR($B{0}="",$H{0}=0),"",IFERROR(ROUND({1}/$G{0}),""))'
        .format(row, sumif(row, "Q"))))
    ws.cell(row=row, column=23, value=(
        '=IF(OR($L{0}="",$U{0}=""),"",$L{0}-$U{0})'.format(row)))
    # Garnek dzieli sie na 4 pojemniki: 2 Twoje wieksze i 2 jej mniejsze.
    # Y = ile porcji bazowych wpisac w Planie na JEDEN dzien; danie na 2 dni wpisuje sie
    # w dwa kolejne dni i lista zakupow sumuje oba. Sosy i napoje to nie posilek - puste.
    ws.cell(row=row, column=25, value=sprawdz(
        '=IF(OR($B{0}="",$L{0}="",$L{0}=0,$C{0}="Sos / dodatek",$C{0}="Napój"),"",'
        'MAX(0.25,ROUND((Ustawienia!$N$8+Ustawienia!$O$8)'
        '*IFERROR(VLOOKUP($C{0},Ustawienia!$Q$2:$R$12,2,0),0.3)/$L{0}*4,0)/4))'
        .format(row)))
    # danie, ktore sie nie odgrzewa (kolumna AF = "Nie"), gotuje sie tylko na jeden dzien
    ws.cell(row=row, column=26, value=sprawdz(
        '=IF($Y{0}="","",IF($AF{0}="Nie","— jedz od razu",2*$Y{0}))'.format(row)))
    for ci, udzial in ((27, "$N$10"), (28, "$O$10")):
        ws.cell(row=row, column=ci, value=sprawdz(
            '=IF($Y{0}="","",IFERROR(ROUND({1}/$G{0}*$Y{0}*Ustawienia!{2}),""))'
            .format(row, sumif(row, "R"), udzial)))
    for ci, udzial in ((29, "$N$10"), (30, "$O$10")):
        ws.cell(row=row, column=ci, value=sprawdz(
            '=IF($Y{0}="","",ROUND($L{0}*$Y{0}*Ustawienia!{1}))'.format(row, udzial)))
    ws.cell(row=row, column=31, value=sprawdz(
        '=IF($Y{0}="","",'
        'IF($AF{0}="Nie","nie na drugi dzień — zrób "&$Y{0}&" porcji tylko na jeden dzień",'
        'IF($Y{0}<1,"bardzo kaloryczne — na dzień dla Was obojga starczy "&$Y{0}&" porcji",'
        'IF($Y{0}>5,"lekkie — na dzień aż "&$Y{0}&" porcji, lepiej jako dodatek",""))))'
        .format(row)))
    for ci in range(1, 35):
        c = ws.cell(row=row, column=ci)
        c.border = BORDER
        c.alignment = Alignment(vertical="top", wrap_text=(ci in (10, 11, 24, 31, 33)))
        if ci == 1:
            c.font = CALC
        elif ci != 6 or not ws.cell(row=row, column=6).hyperlink:
            c.font = BASE
        if ci in (7, 8, 9, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23):
            c.alignment = Alignment(vertical="top", horizontal="center")
        if ci in (21, 22, 23, 24) or 25 <= ci <= 33:
            c.font = CALC
        if 25 <= ci <= 30:
            c.alignment = Alignment(vertical="top", horizontal="center")
    if row - 2 < len(recipes) and recipes[row - 2]["serv_guess"]:
        ws.cell(row=row, column=7).fill = WARN_FILL
        ws.cell(row=row, column=7).font = WARN
    # moje propozycje: niebieskie ID, nazwa i "Skąd" - od razu widac, ze to nie Twoje zapisane
    if row - 2 < len(recipes) and recipes[row - 2]["sug"]:
        for ci in (1, 2, 34):
            ws.cell(row=row, column=ci).fill = SUG_FILL
        ws.cell(row=row, column=34).font = Font(name=F, size=10, bold=True, color="1F4E79")
ws.freeze_panes = "C2"
ws.auto_filter.ref = "A1:AH%d" % MAXP
dv(ws, "C2:C%d" % MAXP, "=Ustawienia!$A$2:$A$30")
ws.conditional_formatting.add("I2:I%d" % MAXP, FormulaRule(formula=['$I2="ręcznie"'], fill=OK_FILL))
ws.conditional_formatting.add("T2:T%d" % MAXP, FormulaRule(
    formula=['ISNUMBER(SEARCH("zgodne",$T2))'], fill=OK_FILL))
ws.conditional_formatting.add("T2:T%d" % MAXP, FormulaRule(
    formula=['OR(ISNUMBER(SEARCH("zaniża",$T2)),ISNUMBER(SEARCH("zawyża",$T2)))'],
    fill=WARN_FILL, font=WARN))
ws.conditional_formatting.add("A2:AG%d" % MAXP, FormulaRule(
    formula=['AND($B2<>"",$H2="")'], fill=WARN_FILL))
# czerwono tam, gdzie dania nie da sie odgrzac
ws.conditional_formatting.add("AF2:AG%d" % MAXP, FormulaRule(
    formula=['AND(LEFT($AF2,3)="Nie",$AF2<>"Nie dotyczy")'],
    fill=PatternFill("solid", fgColor="FCE4E4"),
    font=Font(name=F, size=10, color="9C2828")))
ws.conditional_formatting.add("AF2:AG%d" % MAXP, FormulaRule(
    formula=['LEFT($AF2,3)="Tak"'], fill=OK_FILL))
# zielono tam, gdzie zamiana na light naprawde cos daje
ws.conditional_formatting.add("U2:X%d" % MAXP, FormulaRule(
    formula=['AND($L2<>"",$W2>=0.15*$L2)'], fill=OK_FILL))

def fmt_skl(row, wsp, fry, g):
    """Formula na jeden skladnik. Dla oleju do glebokiego smazenia powyzej progu
    liczy sie tylko ta czesc, ktora realnie zostaje w jedzeniu."""
    if not wsp:
        return None
    if fry:
        return ('=IF($C{0}*{1:g}>={2:g},$C{0}*{3:.8g},$C{0}*{4:.8g})'
                .format(row, g, FRY_MIN_G, wsp * FRY_ABSORB, wsp))
    return '=$C{0}*{1:.8g}'.format(row, wsp)


ws = wb.create_sheet("Składniki")
head(ws, ["Przepis (ID: nazwa)", "Składnik", "Ilość", "Jednostka", "Dział sklepu",
          "Oryginalny zapis", "Do sprawdzenia", "Ilość wg planu", "Gramy wg planu",
          "Zamiennik light", "Mniej kcal",
          "kcal", "Białko (g)", "Tłuszcz (g)", "Węgle (g)",
          "kcal light", "Tłuszcz light", "Gramy po ugotowaniu ≈"],
     [54, 28, 8, 12, 22, 38, 14, 14, 13, 30, 11, 9, 10, 10, 9, 10, 11, 11])
MAXS = len(ing_rows) + 150
for i, x in enumerate(ing_rows):
    row = 2 + i
    ws.cell(row=row, column=1, value=x["rkey"])
    ws.cell(row=row, column=2, value=x["ing"])
    ws.cell(row=row, column=3, value=x["qty"])
    ws.cell(row=row, column=4, value=x["unit"])
    ws.cell(row=row, column=5, value=x["section"])
    ws.cell(row=row, column=6, value=x["raw"])
    if not x["ok"]:
        ws.cell(row=row, column=7, value="✔")
    if x["light"]:
        ws.cell(row=row, column=10, value=x["light"])
    # L-Q: mnozymy kolumne Ilosc przez wspolczynnik na jedna jednostke
    if x["f"]:
        for off, (fn, fl) in enumerate(zip(x["f"], x["fl"])):
            ws.cell(row=row, column=12 + off, value=fmt_skl(row, fn, x["fry"], x["g"]))
        ws.cell(row=row, column=16, value=fmt_skl(row, x["fl"][0], x["fry"], x["g"]))
        ws.cell(row=row, column=17, value=fmt_skl(row, x["fl"][2], x["fry"], x["g"]))
    ws.cell(row=row, column=11, value=(
        '=IF(OR($L{0}="",$P{0}=""),"",ROUND($L{0}-$P{0}))'.format(row)))
    if x["g"]:
        if x["fry"]:
            # olej do glebokiego smazenia w wiekszosci zostaje w garnku
            ws.cell(row=row, column=18, value="=IF($C{0}*{1:g}>={2:g},$C{0}*{3:.6g},$C{0}*{1:g})"
                    .format(row, x["g"], FRY_MIN_G, x["g"] * FRY_ABSORB))
        else:
            ws.cell(row=row, column=18, value="=$C{0}*{1:.6g}".format(row, x["g"] * x["wyd"]))
for row in range(2, MAXS + 1):
    ws.cell(row=row, column=8, value=(
        '=IFERROR($C{0}*SUMIF(Plan!$C:$C,$A{0},Plan!$D:$D)'
        '/INDEX(Przepisy!$G:$G,MATCH(LEFT($A{0},4),Przepisy!$A:$A,0)),0)').format(row))
    if row - 2 < len(ing_rows):
        ws.cell(row=row, column=9,
                value="=$H%d*%g" % (row, ing_rows[row - 2]["g"] or 0))
    for ci in range(1, 19):
        c = ws.cell(row=row, column=ci)
        c.border = BORDER
        c.font = CALC if ci in (6, 8, 9, 10, 11) or ci >= 12 else BASE
        c.alignment = Alignment(vertical="center")
        if ci in (3, 8, 9, 11) or ci >= 12:
            c.number_format = "0.##"
        if ci >= 11:
            c.alignment = Alignment(horizontal="center")
        if ci == 7:
            c.alignment = Alignment(horizontal="center")
            c.font = WARN
ws.freeze_panes = "B2"
ws.auto_filter.ref = "A1:R%d" % MAXS
dv(ws, "A2:A%d" % MAXS, "=Ustawienia!$E$2:$E$%d" % MAXP)
dv(ws, "D2:D%d" % MAXS, "=Ustawienia!$B$2:$B$30")
dv(ws, "E2:E%d" % MAXS, "=Ustawienia!$C$2:$C$30")
ws.conditional_formatting.add("A2:R%d" % MAXS, FormulaRule(formula=['$G2="✔"'], fill=WARN_FILL))
ws.conditional_formatting.add("J2:K%d" % MAXS, FormulaRule(formula=['$K2>=30'], fill=OK_FILL))

ws = wb.create_sheet("Plan")
head(ws, ["Dzień", "Posiłek", "Przepis (ID: nazwa)", "Porcje", "kcal", "Białko (g)",
          "Tłuszcz (g)", "Węgle (g)"],
     [16, 14, 54, 9, 9, 11, 11, 10], 22)
row = 2
for di, d in enumerate(DNI):
    for mi, m in enumerate(POSILKI):
        ws.cell(row=row, column=1, value=d)
        ws.cell(row=row, column=2, value=m)
        # kcal / bialko / tluszcz / wegle - kolumny L, M, N, O w arkuszu Przepisy
        for off, src_col in enumerate(("L", "M", "N", "O")):
            ws.cell(row=row, column=5 + off, value=(
                '=IFERROR($D{0}*INDEX(Przepisy!${1}:${1},'
                'MATCH(LEFT($C{0},4),Przepisy!$A:$A,0)),"")').format(row, src_col))
        # kolumna P (ukryta): kcal tego posilku w wersji light - zasila podsumowanie
        ws.cell(row=row, column=16, value=(
            '=IFERROR($D{0}*INDEX(Przepisy!$U:$U,'
            'MATCH(LEFT($C{0},4),Przepisy!$A:$A,0)),"")').format(row))
        for ci in range(1, 9):
            c = ws.cell(row=row, column=ci)
            c.font = Font(name=F, size=10, bold=True) if ci == 1 else BASE
            if ci in (5, 6, 7, 8):
                c.font = CALC
                c.number_format = "0"
                c.alignment = Alignment(horizontal="center")
            c.border = BORDER
            if ci in (3, 4):
                c.fill = INPUT_FILL
            elif di % 2:
                c.fill = PatternFill("solid", fgColor="F2F2F2")
            if ci == 4:
                c.alignment = Alignment(horizontal="center")
        row += 1
LASTPLAN = row - 1
ws.freeze_panes = "C2"
dv(ws, "C2:C%d" % LASTPLAN, "=Ustawienia!$E$2:$E$%d" % MAXP)
# podsumowanie dobowe
for ci, t in ((10, "Dzień"), (11, "kcal razem"), (12, "Białko (g)"),
              (13, "Tłuszcz (g)"), (14, "Węgle (g)"), (15, "kcal — light"),
              (17, "Ty (kcal)"), (18, "Ona (kcal)"), (19, "Wobec zapotrzebowania")):
    c = ws.cell(row=1, column=ci, value=t)
    c.font = HDR_FONT
    c.fill = HDR_FILL
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
for i, d in enumerate(DNI):
    rr = 2 + i
    ws.cell(row=rr, column=10, value=d).font = Font(name=F, size=10, bold=True)
    # sumy dobowe: kolumny E-H planu, po nazwie dnia z kolumny A
    for off, src in enumerate(("E", "F", "G", "H")):
        c = ws.cell(row=rr, column=11 + off,
                    value='=SUMIF($A:$A,$J%d,$%s:$%s)' % (rr, src, src))
        c.number_format = "0"
        c.alignment = Alignment(horizontal="center")
    c = ws.cell(row=rr, column=15, value='=SUMIF($A:$A,$J%d,$P:$P)' % rr)
    c.number_format = "0"
    c.alignment = Alignment(horizontal="center")
    c.font = CALC
    # ile z tego zjada kazde z Was przy podziale z Ustawien i ile to procent celu
    for ci, udz in ((17, "$N$10"), (18, "$O$10")):
        c = ws.cell(row=rr, column=ci, value="=ROUND($K%d*Ustawienia!%s)" % (rr, udz))
        c.number_format = "0"
        c.alignment = Alignment(horizontal="center")
    c = ws.cell(row=rr, column=19, value=sprawdz(
        '=IF($K{0}=0,"","Ty "&ROUND($Q{0}/Ustawienia!$N$8*100,0)&"% · Ona "'
        '&ROUND($R{0}/Ustawienia!$O$8*100,0)&"%")'.format(rr)))
    c.alignment = Alignment(horizontal="center")
    c.font = CALC
    for ci in (10, 11, 12, 13, 14, 15, 17, 18, 19):
        ws.cell(row=rr, column=ci).border = BORDER
for i, t in enumerate(["Jak używać", "1. W kolumnie C wybierz przepis z listy.",
                       "2. W kolumnie D wpisz liczbę z kolumny",
                       "   „W Planie na dzień” w arkuszu Przepisy.",
                       "3. Danie na dwa dni wpisz w dwa kolejne dni —",
                       "   lista zakupów zsumuje oba, kupisz na jeden garnek.",
                       "4. Kolumny Ty / Ona po prawej mówią, ile każde",
                       "   z Was zje danego dnia i ile to % zapotrzebowania.", "",
                       "Kolumna „kcal — light” pokazuje to samo menu",
                       "na odchudzonych produktach (arkusz Ustawienia).", "",
                       "Żółte pola wypełniasz Ty.",
                       "Szare kolumny liczą się z arkusza Przepisy."]):
    c = ws.cell(row=11 + i, column=10, value=t)
    c.font = Font(name=F, size=(11 if i == 0 else 9), bold=(i == 0),
                  color=("2F5233" if i == 0 else "595959"))
for col, w in (("I", 3), ("J", 18), ("K", 10), ("L", 11), ("M", 11), ("N", 10), ("O", 12),
               ("Q", 10), ("R", 10), ("S", 22)):
    ws.column_dimensions[col].width = w
ws.column_dimensions["P"].hidden = True

NIE_KUPUJEMY = {"woda"}          # kranówki nikt nie kupuje
uniq, seen = [], {}
for x in ing_rows:
    if x["ing"] in NIE_KUPUJEMY:
        continue
    k2 = (x["ing"], PRIMARY[x["ing"]])
    if k2 not in seen:
        seen[k2] = x["section"]
        uniq.append(k2)
uniq.sort(key=lambda k: (DZIALY.index(seen[k]) if seen[k] in DZIALY else 99, k[0].lower()))

ws = wb.create_sheet("Lista zakupów")
head(ws, ["Dział sklepu", "Składnik", "Jednostka", "Potrzeba", "Kupione"], [24, 30, 13, 12, 11])
MAXL = len(uniq) + 60
for i, k2 in enumerate(uniq):
    row = 2 + i
    ws.cell(row=row, column=1, value=seen[k2])
    ws.cell(row=row, column=2, value=k2[0])
    ws.cell(row=row, column=3, value=k2[1])
for row in range(2, MAXL + 1):
    # sumujemy GRAMY z arkusza Skladniki i dzielimy przez wage jednej jednostki
    per = _g(uniq[row - 2][0], uniq[row - 2][1], 1) if row - 2 < len(uniq) else 0
    ws.cell(row=row, column=4, value=(
        '=IF($B{0}="","",ROUND(SUMIF(Składniki!$B:$B,$B{0},Składniki!$I:$I)/{1},1))'
        ).format(row, per or 1))
    for ci in range(1, 6):
        c = ws.cell(row=row, column=ci)
        c.border = BORDER
        c.font = BASE
        if ci == 4:
            c.number_format = "0.##"
            c.font = Font(name=F, size=10, bold=True)
            c.alignment = Alignment(horizontal="center")
        if ci == 5:
            c.fill = INPUT_FILL
            c.alignment = Alignment(horizontal="center")
ws.freeze_panes = "B2"
ws.auto_filter.ref = "A1:E%d" % MAXL
dv(ws, "A2:A%d" % MAXL, "=Ustawienia!$C$2:$C$30")
dv(ws, "C2:C%d" % MAXL, "=Ustawienia!$B$2:$B$30")
dv(ws, "E2:E%d" % MAXL, '"✔"')
ws.conditional_formatting.add("A2:E%d" % MAXL, FormulaRule(
    formula=['AND($B2<>"",$D2=0)'], font=Font(name=F, size=10, color="BFBFBF")))
ws.conditional_formatting.add("A2:E%d" % MAXL, FormulaRule(formula=['$E2="✔"'], fill=OK_FILL))

ws = wb.create_sheet("Instrukcja", 0)
ws.sheet_view.showGridLines = False
ws.column_dimensions["A"].width = 3
ws.column_dimensions["B"].width = 26
ws.column_dimensions["C"].width = 96
ws["B2"] = "Planer posiłków i lista zakupów"
ws["B2"].font = Font(name=F, bold=True, size=14, color="2F5233")
ws["B3"] = ("%d przepisów z TikToka, Instagrama, YouTube i blogów, w tym %d moich propozycji "
            "(niebieskie)." % (len(recipes), n_sug))
ws["B3"].font = Font(name=F, size=10, italic=True, color="595959")
ROWS = [
    ("", ""),
    ("SKĄD SĄ DANE", ""),
    ("Twój plik", "Wszystkie przepisy z jedzenie.xlsx wraz z ilościami, które już miałeś."),
    ("Kolekcja TikTok", "64 dania z 62 filmów i postów z kolekcji „fud” (w jednym poście @anaboliczny.darek są trzy przepisy). Ostatni przegląd 19.10.2026 dodał 10 dań; 5 pozostałych nowych pozycji to nie przepisy, więc je pominąłem. Dwa filmy (drugą wersję ceviche i tikka masalę od jalalsamfit) usunąłeś wcześniej jako duplikaty, a kilka pozycji z licznika kolekcji w ogóle się nie ładuje — autorzy je skasowali albo ukryli."),
    ("Zapisane na IG", "37 przepisów z kolekcji „food” i spoza niej. Przy przeglądzie 19.10.2026 przejrzałem wszystkie 625 zapisanych postów: doszedł 1 przepis (@foxx.gotuje), a jeden nowy zapis (@matyjasikmichal) to film bez przepisu. Spaghetti hot dogi i dżem z borówek usunąłeś wcześniej."),
    ("Opisy pod filmami", "Pełne opisy pobrane przez API TikToka i z zalogowanej sesji."),
    ("Napisy z filmów", "Automatyczna transkrypcja ścieżki dźwiękowej — stąd sposób przygotowania tam, gdzie autor nie napisał go w opisie. Instagram takich napisów nie udostępnia, więc przy rolkach szukałem tego samego przepisu na TikToku twórcy i brałem napisy stamtąd."),
    ("Blogi autorów", "majasrecipes.com, iamneverfull.com, erinscozykitchen.com, aniagotuje.pl, goldengracekitchen.com."),
    ("Czego nie ma", "Trzy posty odpuściłem świadomie: dwa to ten sam przepis wrzucony drugi raz (napisałem o tym w uwadze przy oryginale), trzeci to wpis o meal prepie bez żadnego przepisu."),
    ("Zdjęcia", "Pod nazwą przepisu są dwa zdjęcia dania: okładka posta i klatka z drugiej "
                "połowy filmu, gdzie zwykle widać gotowe danie (przy blogu i postach ze "
                "zdjęciami — kolejne zdjęcie z posta). Klatki wybierał automat, a tam, gdzie "
                "trafił na twarz albo surowe mięso, wybrałem ręcznie; czasem i tak zostanie etap "
                "gotowania zamiast talerza. Przy P139, P142 i P143 (jeden post z Biedronki) drugie "
                "zdjęcie to karta z produktami. Bez zdjęć: %s (brak linku, a przy "
                "P100 film pokazuje inne danie niż przepis); z jednym zdjęciem: %s."
                % (", ".join(r["id"] for r in recipes if not zdjecia_przepisu(r["id"])),
                   ", ".join(r["id"] for r in recipes if len(zdjecia_przepisu(r["id"])) == 1) or "—")),
    ("Weryfikacja", "19-28.10.2026 (dwie rundy) każdy przepis sprawdziłem osobno ze źródłem (opis, napisy z filmu, "
                    "blog, Twój plik): składniki, ilości, liczbę porcji i kalorie. Wynik dla każdego "
                    "przepisu — skąd liczba porcji i co poprawiłem — jest w zakładce Weryfikacja "
                    "(żółte wiersze to poprawione). Wszystkie linki do źródeł działają."),
    ("Waga surowa", "Mięso, ryby, makaron i ryż liczę w wadze PRZED gotowaniem, z wartościami dla "
                    "produktu surowego — np. pierś z kurczaka ok. 110 kcal/100 g, makaron suchy "
                    "371 kcal/100 g. Żeberka liczę razem z kością, a ciecierzycę i suszone pomidory "
                    "ze słoika po odsączeniu."),
    ("", ""),
    ("MOJE PROPOZYCJE", ""),
    ("Co to jest", "%d przepisów, których nie zapisałeś — dobrałem je %s do tego, co "
                   "zapisujesz najczęściej: kurczak, meal prep na kilka dni, kremowe sosy, "
                   "wrapy, kuchnia azjatycka i meksykańska. Numery %s. %d z Instagrama (%s) "
                   "i %d z aniagotuje.pl."
                   % (n_sug, SUG_DATA, sug_zakres, n_sug_ig, ", ".join(sug_autorzy),
                      n_sug - n_sug_ig)),
    ("Jak je znaleźć", "W Przepisach mają niebieskie ID i nazwę, a w ostatniej kolumnie "
                       "„Skąd” wpis „Sugestia Claude”. Filtr na tej kolumnie pokaże tylko je. "
                       "Wszystkie są też w zakładce Sugestie — razem z tym, dlaczego Ci je "
                       "proponuję."),
    ("Kalorie", "Liczone jak w reszcie arkusza, na zwykłych produktach. Autorzy z Instagrama "
                "liczą na light (jogurt 0%, lekki ser i majonez, chuda wołowina 96%), więc "
                "ich liczby w kolumnie „kcal — autor” są zwykle niższe."),
    ("Nie smakuje?", "Skasuj wiersz w Przepisach i jego wiersze w Składnikach, jak przy "
                     "każdym innym przepisie. Numer nie wróci do obiegu."),
    ("", ""),
    ("KOLUMNA „OPRACOWANIE”", ""),
    ("ręcznie", "Przepis przeczytany i rozpisany przeze mnie: składniki w jednej formie "
                "i kroki odtworzone z opisu oraz z tego, co autor mówi na nagraniu. "
                "Zielone tło — najwyższa jakość."),
    ("blog", "Składniki i kroki pobrane wprost ze strony autora."),
    ("auto", "Wyciągnięte automatycznie z opisu. Warto zerknąć przed gotowaniem."),
    ("", ""),
    ("ID PRZEPISU", ""),
    ("Kolumna A", "Każdy przepis ma numer P001, P002... Wszędzie, gdzie odwołuję się do "
                  "przepisu — w Planie, w Składnikach i w kolumnie „Podobne do” — piszę "
                  "„P012: Nazwa”, żebyś po numerze od razu trafił do właściwego wiersza."),
    ("Nowe wersje pliku", "Numery są stałe także między wersjami arkusza: przepis, który "
                          "był P046, zostaje P046. Nowe przepisy dopisuję na końcu listy "
                          "z kolejnymi numerami — te z przeglądu 19.10.2026 to P137-P147, "
                          "a moje propozycje z %s to %s." % (SUG_DATA, sug_zakres)),
    ("Zmiana nazwy", "Plan i Składniki szukają przepisu po numerze, nie po nazwie, "
                     "więc możesz zmieniać nazwy bez psucia przeliczeń."),
    ("Kasowanie przepisu", "ID są wpisane na stałe, więc skasowanie wiersza nie przesuwa "
                           "numerów pozostałych przepisów i nic się nie rozjeżdża. "
                           "Zostaje tylko dziura w numeracji — to normalne. Skasuj też "
                           "wiersze tego przepisu w Składnikach, inaczej będą wisiały "
                           "bez właściciela i zostaną na liście zakupów."),
    ("", ""),
    ("ILE UGOTOWAĆ NA WAS DWOJE", ""),
    ("Jak to działa", "Z jednego gotowania wychodzą 4 porcje: DWIE TWOJE, większe, "
                      "i DWIE JEJ, mniejsze. Pierwszego dnia bierzecie po jednej, "
                      "drugiego dnia po drugiej. Twoja porcja to 30% garnka, jej 20% "
                      "— razem 100%."),
    ("Skąd te liczby", "W Ustawieniach (kolumny M-O) są Wasze dane: płeć, wiek, wzrost, "
                       "waga i współczynnik aktywności. Z nich liczy się przemiana "
                       "spoczynkowa wzorem Mifflina-St Jeora i zapotrzebowanie na dzień. "
                       "Zmień wiek albo aktywność i cały arkusz przeliczy się na nowo."),
    ("Ile wyszło", "Przy 30 latach i aktywności 1,4: Ty 2903 kcal na dzień, Ona 1822. "
                   "Jesz o 59% więcej od niej — dlatego porcje nie mogą być równe."),
    ("Podział 60/40", "Z tych 59% zrobiłem równy podział 60/40 — w praktyce wychodzi Ci około 2% mniej niż zapotrzebowanie, a jej około 4% więcej. Proporcję zmienisz w Ustawieniach, wiersz „Podział jedzenia z garnka”."),
    ("Kolumna „W Planie na dzień”", "Ile porcji BAZOWYCH tego przepisu wpisać w Planie na "
                                    "JEDEN dzień dla Was obojga. Danie na dwa dni wpisujesz "
                                    "w dwa kolejne dni — lista zakupów zsumuje oba i wyjdzie "
                                    "dokładnie jeden garnek. Kolumna obok, „Ugotuj razem”, "
                                    "mówi, ile to jest łącznie. Przy daniach, które się nie "
                                    "odgrzewają (carbonara, sushi, ceviche), pokazuje "
                                    "„— jedz od razu”: te wpisujesz tylko na jeden dzień."),
    ("Twoja / Jej porcja", "Kalorie są dokładne. Gramy to szacunek wagi PO ugotowaniu: "
                           "makaron wciąga wodę (×2,25), ryż jeszcze więcej (×2,5), mięso "
                           "ją traci (×0,75), a olej do smażenia w głębokim tłuszczu zostaje "
                           "w garnku. Najdokładniej: zważ cały garnek po ugotowaniu i weź "
                           "30% dla siebie, 20% dla niej."),
    ("Kolumna „Uwaga do porcji”", "Odzywa się przy skrajnych daniach: bardzo kalorycznych "
                                  "(na dzień starcza mniej niż jedna porcja bazowa) i bardzo "
                                  "lekkich (lepiej jako dodatek). Przy sosach i napojach "
                                  "kolumny porcji są puste — to nie jest posiłek."),
    ("", ""),
    ("CZY TO SIĘ ODGRZEJE", ""),
    ("Kolumna „Na drugi dzień”", "Zielone = odgrzejesz bez straty. Czerwone „Nie” = to "
                                 "danie robi się i zjada od razu, drugiego dnia będzie "
                                 "gorsze albo niebezpieczne."),
    ("Kolumna „Jak odgrzewać”", "Konkretna instrukcja przy każdym daniu — co zrobić, "
                                "żeby drugiego dnia nadal było dobre."),
    ("Czego nie odgrzewać", "Carbonary (żółtka się zwarzą), ceviche (surowe krewetki), "
                            "sushi, sałatek z liśćmi i wszystkiego w bułce. Panierowane "
                            "i chrupiące odżyją w piekarniku, ale nie w mikrofali."),
    ("", ""),
    ("WSZYSTKO SIĘ LICZY SAMO", ""),
    ("Co możesz zmieniać", "Kolumnę „Ilość” w Składnikach i „Porcje bazowe” w Przepisach. "
                           "Po każdej zmianie kcal, białko, tłuszcz, węgle, wersja light, "
                           "zgodność z autorem, Plan i lista zakupów przeliczają się same."),
    ("Przykład", "Chlebek czosnkowy ma 250 g masła i 499 kcal na porcję. Wpisz 150 g "
                 "i w tej samej sekundzie robi się 409 kcal, a lista zakupów prosi "
                 "o mniej masła."),
    ("Skąd te liczby", "Kolumny L-Q w Składnikach to kcal i makra tego jednego wiersza — "
                       "mnożę Twoją ilość przez wartość odżywczą produktu. Przepisy sumują "
                       "te wiersze i dzielą przez porcje. Nic nie jest wklepane na sztywno."),
    ("Czego nie ruszać", "Kolumny w szarym kursywnym druku to formuły. Jak którąś "
                         "nadpiszesz, w tym wierszu przestanie się liczyć — ale reszta "
                         "arkusza działa dalej."),
    ("Nowy przepis", "Dopisz wiersz w Przepisach (ID zrobi się samo) i jego składniki "
                     "w Składnikach, wybierając przepis z listy w kolumnie A. Makra "
                     "policzą się, jeśli składnik jest w mojej tabeli wartości odżywczych; "
                     "przy nieznanym produkcie zostaną puste."),
    ("", ""),
    ("JAK TO DZIAŁA", ""),
    ("Plan", "7 dni × 4 posiłki. Wybierasz przepis z listy i wpisujesz liczbę porcji."),
    ("Lista zakupów", "Przelicza się sama: skaluje do porcji, sumuje ten sam produkt "
                      "z różnych przepisów i grupuje po działach sklepu."),
    ("", ""),
    ("CO WYMAGA UWAGI", ""),
    ("Pomarańczowe wiersze", "%d przepisów, przy których w źródle nie było listy składników "
                            "— zostaje sam link i uwaga, co dokładnie autor pominął."
                            % sum(1 for r in recipes if not r["n_ing"])),
    ("Żółte porcje", "Pojawiają się tylko przy przepisie dopisanym bez liczby porcji — arkusz przyjmuje wtedy 2. Skąd wzięła się liczba porcji przy każdym z moich przepisów, pisze w zakładce Weryfikacja."),
    ("Puste „Przygotowanie”", "Przepisy ze składnikami, ale bez opisanej kolejności łączenia: %d. Autor jej nie podał, a film nie ma napisów — uwaga przy każdym z nich mówi, czego brakuje." % sum(1 for r in recipes if r["n_ing"] and not r["steps"])),
    ("Makra (kolumny L-O)", "kcal, białko, tłuszcz i węgle na jedną porcję — ZAWSZE liczone "
                            "przeze mnie ze składników, tą samą metodą dla każdego przepisu. "
                            "To one zasilają Plan."),
    ("Makra autora (P-S)", "To, co autor podał w opisie. Puste, jeśli nic nie podał."),
    ("Wersja light (U-X)", "To samo danie policzone na odchudzonych produktach: kcal, "
                           "tłuszcz, ile mniej wychodzi i co konkretnie zamienić. Zielone "
                           "wiersze to te, gdzie zamiana ścina co najmniej 15% kalorii. "
                           "Wykaz zamienników i wartości, na których to liczę, siedzi "
                           "w arkuszu Ustawienia (kolumny G-K) — możesz je podmienić na "
                           "produkty, które faktycznie kupujesz."),
    ("Ile to daje", "W połowie przepisów zamiana na light ścina około 8% kalorii (jakieś 50 kcal "
                    "na porcję) — mniej niż łyżka oliwy. Najwięcej dają trzy zamiany: chuda "
                    "wołowina zamiast zwykłej mielonej (16 przepisów, mediana 145 kcal na porcję), "
                    "śmietana 12% zamiast 30% (16 przepisów, 109 kcal) i majonez light (26 przepisów, "
                    "49 kcal). Jogurt grecki 0% zamiast 10% to 21 przepisów, ale tylko ok. 34 kcal "
                    "na porcję."),
    ("Uwaga o light", "Odchudzona wersja to zwykle mniej tłuszczu i więcej wody, skrobi "
                      "i gum. Śmietana 12% zwarzy się przy pomidorach i winie, a ser "
                      "light się nie ciągnie. Kolumna „Kiedy uważać” w Ustawieniach "
                      "mówi, gdzie to boli."),
    ("Zgodność (T)", "Porównanie obu kolumn. Zielone „zgodne” = różnica do 10%. "
                     "Pomarańczowe = autor podaje wyraźnie mniej lub więcej niż wychodzi "
                     "ze składników."),
    ("Skąd różnice", "Moja tabela wycenia produkty STANDARDOWE, pełnotłuste. Twórcy fitness "
                     "często używają wersji light, 0% i bez cukru i liczą po nich — dlatego "
                     "ich liczby bywają niższe. Rozbieżność nie musi znaczyć, że ktoś kłamie; "
                     "znaczy, że liczycie inny koszyk."),
    ("Kolumna „Podobne do”", "%d przepisów ma bliźniaka o zbliżonej nazwie lub prawie identycznym "
                             "zestawie składników. Nie usunąłem ich — sam zdecyduj, który zostaje."
                             % n_sim),
]
r = 5
for label, text in ROWS:
    if label and not text:
        c = ws.cell(row=r, column=2, value=label)
        c.font = Font(name=F, bold=True, size=10, color="FFFFFF")
        c.fill = HDR_FILL
        ws.cell(row=r, column=3).fill = HDR_FILL
    else:
        ws.cell(row=r, column=2, value=label).font = Font(name=F, bold=True, size=10)
        c = ws.cell(row=r, column=3, value=text)
        c.font = BASE
        c.alignment = Alignment(wrap_text=True, vertical="top")
        if text:
            ws.row_dimensions[r].height = 34
    r += 1

# ------------------------------------------------ weryfikacja przepis po przepisie
WER_PATH = SP + "/weryfikacja.json"
if os.path.exists(WER_PATH):
    WER = json.load(open(WER_PATH, encoding="utf-8"))
    ws = wb.create_sheet("Weryfikacja")
    head(ws, ["ID", "Nazwa przepisu", "Porcje", "Skąd liczba porcji", "kcal / porcję teraz",
              "kcal / porcję 15.09", "kcal — autor", "Co sprawdziłem / poprawiłem"],
         [7, 46, 9, 40, 12, 12, 11, 92])
    POPR_FILL = PatternFill("solid", fgColor="FFF3CD")
    for i, r in enumerate(recipes):
        row = 2 + i
        w = WER.get(r["id"], {})
        if r["sug"]:
            w = dict(porcje=SUG[r["src"]]["porcje_skad"],
                     wynik="Moja propozycja z %s, spoza Twoich zapisanych. Składniki i ilości "
                           "przepisane ze źródła; produkty light autora policzone jako "
                           "zwykłe." % SUG_DATA)
        ws.cell(row=row, column=1, value=r["id"]).font = CALC
        szukaj = 'MATCH($A{0},Przepisy!$A:$A,0)'.format(row)
        for col, kol in ((2, "B"), (3, "G"), (5, "L"), (7, "P")):
            idx = 'INDEX(Przepisy!${0}:${0},{1})'.format(kol, szukaj)
            ws.cell(row=row, column=col, value=sprawdz(
                '=IFERROR(IF({0}="","",{0}),"")'.format(idx)))
        ws.cell(row=row, column=4, value=w.get("porcje", ""))
        ws.cell(row=row, column=6, value=w.get("kcal_przed") if w.get("kcal_przed") else
                ("nowy" if r["id"] >= "P137" else ""))
        wynik = w.get("wynik", "")
        ws.cell(row=row, column=8, value=wynik)
        poprawiony = (bool(wynik) and not wynik.startswith(("Składniki", "Autor nie"))
                      and not r["sug"])
        for col in range(1, 9):
            c = ws.cell(row=row, column=col)
            c.border = BORDER
            c.alignment = Alignment(vertical="top", wrap_text=col in (2, 4, 8),
                                    horizontal="center" if col in (3, 5, 6, 7) else None)
            if col != 1:
                c.font = CALC if col in (2, 3, 5, 7) else BASE
            if poprawiony:
                c.fill = POPR_FILL
            elif r["sug"] and col <= 2:
                c.fill = SUG_FILL
    ws.freeze_panes = "C2"
    ws.auto_filter.ref = "A1:H%d" % (len(recipes) + 1)

# ------------------------------------------------ moje propozycje w jednym miejscu
if sug_r:
    ws = wb.create_sheet("Sugestie", wb.sheetnames.index("Przepisy") + 1)
    head(ws, ["ID", "Nazwa przepisu", "Kategoria", "Autor", "Link", "Dlaczego Ci to proponuję",
              "Porcje bazowe", "kcal / porcję", "Białko (g)", "kcal — autor", "Na drugi dzień"],
         [7, 46, 11, 20, 42, 74, 9, 10, 10, 10, 22])
    for i, r in enumerate(sug_r):
        row = 2 + i
        ws.cell(row=row, column=1, value=r["id"])
        szukaj = 'MATCH($A{0},Przepisy!$A:$A,0)'.format(row)
        # nazwa, porcje i kcal ida z Przepisow, wiec zmiana tam od razu widac tutaj
        for col, kol in ((2, "B"), (3, "C"), (7, "G"), (8, "L"), (9, "M"), (10, "P"),
                         (11, "AF")):
            idx = 'INDEX(Przepisy!${0}:${0},{1})'.format(kol, szukaj)
            ws.cell(row=row, column=col, value=sprawdz(
                '=IFERROR(IF({0}="","",{0}),"")'.format(idx)))
        ws.cell(row=row, column=4, value=r["author"])
        c = ws.cell(row=row, column=5, value=r["link"])
        c.hyperlink = r["link"]
        ws.cell(row=row, column=6, value=r["powod"])
        for col in range(1, 12):
            c = ws.cell(row=row, column=col)
            c.border = BORDER
            c.alignment = Alignment(vertical="top", wrap_text=col in (2, 5, 6, 11),
                                    horizontal="center" if col in (7, 8, 9, 10) else None)
            c.font = (Font(name=F, size=9, color="0563C1", underline="single") if col == 5
                      else CALC if col in (2, 3, 7, 8, 9, 10, 11) else BASE)
            if col <= 2:
                c.fill = SUG_FILL
        ws.row_dimensions[row].height = ZDJ_WIERSZ if wstaw_zdjecia(ws, row, 1, r["id"]) else 54
    ws.freeze_panes = "C2"
    ws.auto_filter.ref = "A1:K%d" % (len(sug_r) + 1)

wb.save(OUT)
print("Zapisano:", OUT)
print("Pozycji na liscie zakupow: %d" % len(uniq))
