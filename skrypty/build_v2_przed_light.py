# -*- coding: utf-8 -*-
"""Buduje planer: recznie opracowane przepisy + reszta z automatu."""
import collections, glob, importlib.util, json, os, re, sys
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule
from openpyxl.utils import get_column_letter

SP = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SP)
from normalize import normalize
from parse import parse_qty, PRETTY
from classify import category_of, find_similar
from nutrition import macros as ing_macros
from macros_calc import author_macros, is_whole_dish

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

    recipes.append(dict(name=name, platform=platform_of(r.get("link")),
                        author=author_of(r.get("author"), r.get("link")),
                        link=r.get("link") or "",
                        serv=serv, serv_guess=serv_guess, cat=cat, quality=quality,
                        n_ing=len(items), steps=steps, note=(cur or {}).get("note", "")))
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
for x in ing_rows:
    x["g"] = _g(x["ing"], x["unit"], 1)      # ile gramow wazy 1 jednostka tego wiersza

QORD = {"ręcznie": 0, "blog": 1, "auto": 2}
recipes.sort(key=lambda x: (QORD[x["quality"]], -x["n_ing"], x["name"].lower()))
order_r = {r["name"]: i for i, r in enumerate(recipes)}
ing_rows.sort(key=lambda x: order_r.get(x["recipe"], 9999))

# ID przepisu = jego pozycja w arkuszu; dokladnie to samo liczy formula w kolumnie A
for i, r in enumerate(recipes):
    r["id"] = "P%03d" % (i + 1)
    r["key"] = "%s: %s" % (r["id"], r["name"])
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
print("Przepisow: %d | opracowanych recznie: %d | ze skladnikami: %d | z przygotowaniem: %d"
      % (len(recipes), n_man, n_ing, n_steps))
print("Wierszy skladnikow: %d | do sprawdzenia: %d | oznaczonych jako podobne: %d"
      % (len(ing_rows), n_check, n_sim))

# ------------------------------------------------ skoroszyt
wb = openpyxl.Workbook()


def head(ws, headers, widths, height=30):
    for ci, h in enumerate(headers, start=1):
        c = ws.cell(row=1, column=ci, value=h)
        c.font = HDR_FONT
        c.fill = HDR_FILL
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws.column_dimensions[get_column_letter(ci)].width = widths[ci - 1]
    ws.row_dimensions[1].height = height


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
ws.freeze_panes = "A2"

ws = wb.create_sheet("Przepisy")
head(ws, ["ID", "Nazwa przepisu", "Kategoria", "Źródło", "Autor", "Link", "Porcje bazowe",
          "Składników", "Opracowanie", "Przygotowanie", "Podobne do",
          "kcal / porcję", "Białko (g)", "Tłuszcz (g)", "Węgle (g)",
          "kcal — autor", "Białko — autor", "Tłuszcz — autor", "Węgle — autor",
          "Zgodność z autorem"],
     [7, 46, 14, 12, 20, 44, 9, 10, 13, 88, 54, 12, 11, 11, 10, 12, 12, 12, 11, 22])
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
    if r["n_ing"]:
        ws.cell(row=row, column=8, value=r["n_ing"])
    ws.cell(row=row, column=9, value=r["quality"])
    txt = "\n".join("%d. %s" % (n, s) for n, s in enumerate(r["steps"], 1))
    if r["note"]:
        txt = ("UWAGA: %s\n\n" % r["note"]) + txt
    if txt:
        ws.cell(row=row, column=10, value=txt)
    if r["similar"]:
        c = ws.cell(row=row, column=11, value=r["similar"])
        c.font = WARN
    for off, key in enumerate(("kcal", "mB", "mT", "mW")):
        if r[key] is not None:
            ws.cell(row=row, column=12 + off, value=r[key])
    for off, key in enumerate(("aK", "aB", "aT", "aW")):
        if r[key] is not None:
            c = ws.cell(row=row, column=16 + off, value=r[key])
            c.font = CALC
    if r["msrc"]:
        ws.cell(row=row, column=20, value=r["msrc"]).font = CALC
    ws.row_dimensions[row].height = 15 if not r["steps"] else min(210, 13.5 * len(r["steps"]) + 10)

for row in range(2, MAXP + 1):
    ws.cell(row=row, column=1, value='=IF($B%d="","","P"&TEXT(ROW()-1,"000"))' % row)
    for ci in range(1, 21):
        c = ws.cell(row=row, column=ci)
        c.border = BORDER
        c.alignment = Alignment(vertical="top", wrap_text=(ci in (10, 11)))
        if ci == 1:
            c.font = CALC
        elif ci != 6 or not ws.cell(row=row, column=6).hyperlink:
            c.font = BASE
        if ci in (7, 8, 9, 12, 13, 14, 15, 16, 17, 18, 19):
            c.alignment = Alignment(vertical="top", horizontal="center")
    if row - 2 < len(recipes) and recipes[row - 2]["serv_guess"]:
        ws.cell(row=row, column=7).fill = WARN_FILL
        ws.cell(row=row, column=7).font = WARN
ws.freeze_panes = "C2"
ws.auto_filter.ref = "A1:T%d" % MAXP
dv(ws, "C2:C%d" % MAXP, "=Ustawienia!$A$2:$A$30")
ws.conditional_formatting.add("I2:I%d" % MAXP, FormulaRule(formula=['$I2="ręcznie"'], fill=OK_FILL))
ws.conditional_formatting.add("T2:T%d" % MAXP, FormulaRule(
    formula=['ISNUMBER(SEARCH("zgodne",$T2))'], fill=OK_FILL))
ws.conditional_formatting.add("T2:T%d" % MAXP, FormulaRule(
    formula=['OR(ISNUMBER(SEARCH("zaniża",$T2)),ISNUMBER(SEARCH("zawyża",$T2)))'],
    fill=WARN_FILL, font=WARN))
ws.conditional_formatting.add("A2:T%d" % MAXP, FormulaRule(
    formula=['AND($B2<>"",$H2="")'], fill=WARN_FILL))

ws = wb.create_sheet("Składniki")
head(ws, ["Przepis (ID: nazwa)", "Składnik", "Ilość", "Jednostka", "Dział sklepu",
          "Oryginalny zapis", "Do sprawdzenia", "Ilość wg planu", "Gramy wg planu"],
     [54, 28, 8, 12, 22, 38, 14, 14, 13])
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
for row in range(2, MAXS + 1):
    ws.cell(row=row, column=8, value=(
        '=IFERROR($C{0}*SUMIF(Plan!$C:$C,$A{0},Plan!$D:$D)'
        '/INDEX(Przepisy!$G:$G,MATCH(LEFT($A{0},4),Przepisy!$A:$A,0)),0)').format(row))
    if row - 2 < len(ing_rows):
        ws.cell(row=row, column=9,
                value="=$H%d*%g" % (row, ing_rows[row - 2]["g"] or 0))
    for ci in range(1, 10):
        c = ws.cell(row=row, column=ci)
        c.border = BORDER
        c.font = CALC if ci in (6, 8, 9) else BASE
        c.alignment = Alignment(vertical="center")
        if ci in (3, 8, 9):
            c.number_format = "0.##"
        if ci == 7:
            c.alignment = Alignment(horizontal="center")
            c.font = WARN
ws.freeze_panes = "B2"
ws.auto_filter.ref = "A1:I%d" % MAXS
dv(ws, "A2:A%d" % MAXS, "=Ustawienia!$E$2:$E$%d" % MAXP)
dv(ws, "D2:D%d" % MAXS, "=Ustawienia!$B$2:$B$30")
dv(ws, "E2:E%d" % MAXS, "=Ustawienia!$C$2:$C$30")
ws.conditional_formatting.add("A2:I%d" % MAXS, FormulaRule(formula=['$G2="✔"'], fill=WARN_FILL))

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
for ci, t in ((10, "Dzień"), (11, "kcal"), (12, "Białko (g)"),
              (13, "Tłuszcz (g)"), (14, "Węgle (g)")):
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
    for ci in range(10, 15):
        ws.cell(row=rr, column=ci).border = BORDER
for i, t in enumerate(["Jak używać", "1. W kolumnie C wybierz przepis z listy.",
                       "2. W kolumnie D wpisz liczbę porcji.",
                       "3. Lista zakupów i makra przeliczą się same.", "",
                       "Żółte pola wypełniasz Ty.",
                       "Szare kolumny liczą się z arkusza Przepisy."]):
    c = ws.cell(row=11 + i, column=10, value=t)
    c.font = Font(name=F, size=(11 if i == 0 else 9), bold=(i == 0),
                  color=("2F5233" if i == 0 else "595959"))
for col, w in (("I", 3), ("J", 18), ("K", 9), ("L", 11), ("M", 11), ("N", 10)):
    ws.column_dimensions[col].width = w

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
ws["B3"] = "%d przepisów z TikToka, Instagrama, YouTube i blogów." % len(recipes)
ws["B3"].font = Font(name=F, size=10, italic=True, color="595959")
ROWS = [
    ("", ""),
    ("SKĄD SĄ DANE", ""),
    ("Twój plik", "Wszystkie przepisy z jedzenie.xlsx wraz z ilościami, które już miałeś."),
    ("Kolekcja TikTok", "Wszystkie 56 filmów, które kolekcja „fud” realnie pokazuje. Licznik TikToka mówi 60, ale 4 pozycje w ogóle się nie ładują — autorzy je skasowali albo ukryli, nie da się ich otworzyć."),
    ("Zapisane na IG", "27 rolek z kolekcji „food” plus 11 przepisów, które miałeś zapisane poza tą kolekcją. Przejrzałem wszystkie 620 zapisanych postów."),
    ("Opisy pod filmami", "Pełne opisy pobrane przez API TikToka i z zalogowanej sesji."),
    ("Napisy z filmów", "Automatyczna transkrypcja ścieżki dźwiękowej — stąd sposób przygotowania tam, gdzie autor nie napisał go w opisie. Instagram takich napisów nie udostępnia, więc przy rolkach szukałem tego samego przepisu na TikToku twórcy i brałem napisy stamtąd."),
    ("Blogi autorów", "majasrecipes.com, iamneverfull.com, erinscozykitchen.com, aniagotuje.pl, goldengracekitchen.com."),
    ("Czego nie ma", "Trzy posty odpuściłem świadomie: dwa to ten sam przepis wrzucony drugi raz (napisałem o tym w uwadze przy oryginale), trzeci to wpis o meal prepie bez żadnego przepisu."),
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
    ("Zmiana nazwy", "Plan i Składniki szukają przepisu po numerze, nie po nazwie, "
                     "więc możesz zmieniać nazwy bez psucia przeliczeń."),
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
    ("Żółte porcje", "Liczba porcji, której nie było w źródle — przyjąłem 2."),
    ("Puste „Przygotowanie”", "%d przepisów ma składniki, ale autor nie napisał, w jakiej kolejności je łączyć, a film nie ma napisów. Uwaga przy każdym z nich mówi, czego brakuje." % sum(1 for r in recipes if r["n_ing"] and not r["steps"])),
    ("Makra (kolumny L-O)", "kcal, białko, tłuszcz i węgle na jedną porcję — ZAWSZE liczone "
                            "przeze mnie ze składników, tą samą metodą dla każdego przepisu. "
                            "To one zasilają Plan."),
    ("Makra autora (P-S)", "To, co autor podał w opisie. Puste, jeśli nic nie podał."),
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

wb.save(OUT)
print("Zapisano:", OUT)
print("Pozycji na liscie zakupow: %d" % len(uniq))
