# -*- coding: utf-8 -*-
"""Buduje finalny planer posilkow ze wszystkich zebranych przepisow."""
import json, os, re, sys
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule
from openpyxl.utils import get_column_letter

SP = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SP)
from normalize import normalize
from parse import parse_qty, PRETTY

OUT = r"C:\Users\Sebastian\Documents\Przepisy-planer\Przepisy-planer.xlsx"

F = "Arial"
HDR_FILL = PatternFill("solid", fgColor="2F5233")
HDR_FONT = Font(name=F, bold=True, color="FFFFFF", size=10)
BASE = Font(name=F, size=10)
CALC = Font(name=F, size=10, color="808080", italic=True)
WARN = Font(name=F, size=10, color="9C5700")
INPUT_FILL = PatternFill("solid", fgColor="FFFDE7")
WARN_FILL = PatternFill("solid", fgColor="FFF3CD")
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

# przygotowanie przepisane z arkusza "Przepisy" w Twoim pliku
STEPS_FROM_FILE = {
    "Ziemniaczane talarki": [
        "Ziemniaki kroimy na plastry.",
        "Wkładamy na około 20 min do lodowatej wody, następnie osuszamy na ręczniku papierowym.",
        "Dodajemy ulubione przyprawy (oprócz soli, którą dodamy po upieczeniu), oliwę i parmezan. Mieszamy.",
        "Wykładamy płasko na blaszce tak, aby talarki się nie dotykały, i pieczemy ok. 20 min "
        "w nagrzanym do 200 stopni piekarniku (góra-dół z termoobiegiem).",
    ],
    "Kurczak ze szpinakiem": [
        "Przesmażyć kurczaka na oliwie.",
        "Doprawić go solą, pieprzem, papryką i oregano.",
        "Usmażony przerzucić do innej miski.",
        "Podsmażyć cebulę w kostkę i dodać soli.",
        "Dodać czosnek, pastę pomidorową i płatki chilli.",
        "Wlać wodę, śmietankę i trochę soli.",
        "Ugotować na tym makaron.",
        "Dodać pokrojone suszone pomidory, szpinak i kurczaka.",
    ],
    "Tacos 1": [
        "Na placek tortilli wyłóż mięso mielone. Posól i podsmaż stroną z mięsem na złoty kolor.",
        "Przewróć na drugą stronę i dodaj ser cheddar. Podsmaż 2-3 min.",
        "Na środek wyłóż odrobinę sosu, posiekaną sałatę i kilka plastrów ogórków konserwowych. "
        "Dodaj jeszcze odrobinę sosu i złóż na pół.",
    ],
}

PLATFORM = {"tiktok": "TikTok", "instagram": "Instagram", "youtube": "YouTube",
            "aniagotuje": "Blog", "other": "Inne"}


def platform_of(r):
    link = r.get("link") or ""
    if "tiktok.com" in link:
        return "TikTok"
    if "instagram.com" in link:
        return "Instagram"
    if "youtu" in link:
        return "YouTube"
    if link:
        return "Blog"
    return "Inne"


# ---------------------------------------------------------------- dane
data = json.load(open(SP + "/parsed.json", encoding="utf-8"))
recipes, ing_rows = [], []
used_names = {}

for key, r in data.items():
    p = r["parsed"]
    name = (r["name"] or p["name"] or "").strip()
    if not name:
        name = "Bez nazwy (@%s)" % (r["author"] or "?")
    name = re.sub(r"\s+", " ", name)[:70]
    n = used_names.get(name.lower(), 0) + 1
    used_names[name.lower()] = n
    if n > 1:
        name = "%s (%d)" % (name, n)

    src = r["file_ings"] or p["ings"]
    items = []
    for i in src:
        raw_name = i.get("ing") or ""
        qty, unit = i.get("qty"), i.get("unit")
        # ilosc zapisana w tresci skladnika (np. "1 lyzeczka papryki wedzonej")
        # albo zepsuta przez Excela na date
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

    # scal duplikaty tego samego skladnika w jednym przepisie
    merged = {}
    for it in items:
        k = (it["ing"], it["unit"])
        if k in merged:
            merged[k]["qty"] = round(merged[k]["qty"] + it["qty"], 3)
        else:
            merged[k] = it
    items = list(merged.values())

    serv = r.get("servings") or p.get("servings")
    serv_guess = False
    try:
        serv = float(serv)
        if not (0 < serv <= 24):
            raise ValueError
    except (TypeError, ValueError):
        serv, serv_guess = 2.0, True

    steps = STEPS_FROM_FILE.get(name) or r.get("steps") or p.get("steps") or []
    steps = [re.sub(r"\s+", " ", s).strip() for s in steps if s and len(s.strip()) > 8][:14]

    recipes.append(dict(name=name, platform=platform_of(r), author=r.get("author") or "",
                        link=r.get("link") or "", serv=serv, serv_guess=serv_guess,
                        cat=r.get("cat") or "", typ=r.get("typ") or "",
                        n_ing=len(items), steps=steps,
                        complete=bool(items) and bool(steps)))
    for it in items:
        ing_rows.append(dict(recipe=name, **it))

recipes.sort(key=lambda x: (-x["n_ing"], x["name"].lower()))
order_r = {r["name"]: i for i, r in enumerate(recipes)}
ing_rows.sort(key=lambda x: order_r.get(x["recipe"], 999))

print("Przepisow: %d   (z rozpisanymi skladnikami: %d)"
      % (len(recipes), sum(1 for r in recipes if r["n_ing"] > 0)))
print("Wierszy skladnikow: %d" % len(ing_rows))
print("Przepisow z opisem przygotowania: %d" % sum(1 for r in recipes if r["steps"]))

# ---------------------------------------------------------------- skoroszyt
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


# --- Ustawienia
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
ws.freeze_panes = "A2"

# --- Przepisy
ws = wb.create_sheet("Przepisy")
head(ws, ["ID", "Nazwa przepisu", "Kategoria", "Źródło", "Autor", "Link", "Porcje bazowe",
          "Składników", "Status", "Przygotowanie"],
     [7, 44, 14, 12, 20, 46, 9, 10, 18, 84])
MAXP = len(recipes) + 40
for i, r in enumerate(recipes):
    row = 2 + i
    ws.cell(row=row, column=2, value=r["name"])
    ws.cell(row=row, column=3, value=r["cat"] if r["cat"] in KATEGORIE else "")
    ws.cell(row=row, column=4, value=r["platform"])
    ws.cell(row=row, column=5, value=r["author"])
    if r["link"]:
        c = ws.cell(row=row, column=6, value=r["link"])
        c.hyperlink = r["link"]
        c.font = Font(name=F, size=9, color="0563C1", underline="single")
    ws.cell(row=row, column=7, value=r["serv"])
    if r["n_ing"]:
        ws.cell(row=row, column=8, value=r["n_ing"])
    status = ("Kompletny" if r["complete"] else
              ("Brak przygotowania" if r["n_ing"] else "Do uzupełnienia"))
    ws.cell(row=row, column=9, value=status)
    if r["steps"]:
        ws.cell(row=row, column=10,
                value="\n".join("%d. %s" % (n, s) for n, s in enumerate(r["steps"], 1)))
    ws.row_dimensions[row].height = 15 if not r["steps"] else min(150, 14 * len(r["steps"]) + 8)

for row in range(2, MAXP + 1):
    ws.cell(row=row, column=1, value='=IF($B%d="","","P"&TEXT(ROW()-1,"000"))' % row)
    for ci in range(1, 11):
        c = ws.cell(row=row, column=ci)
        c.border = BORDER
        c.alignment = Alignment(vertical="top", wrap_text=(ci == 10))
        if ci == 1:
            c.font = CALC
        elif ci != 6 or not ws.cell(row=row, column=6).hyperlink:
            c.font = BASE
        if ci in (7, 8):
            c.alignment = Alignment(vertical="top", horizontal="center")
    if row - 2 < len(recipes) and recipes[row - 2]["serv_guess"]:
        ws.cell(row=row, column=7).fill = WARN_FILL
        ws.cell(row=row, column=7).font = WARN
ws.freeze_panes = "C2"
ws.auto_filter.ref = "A1:J%d" % MAXP
dv(ws, "C2:C%d" % MAXP, "=Ustawienia!$A$2:$A$30")
ws.conditional_formatting.add("I2:I%d" % MAXP, FormulaRule(
    formula=['$I2="Do uzupełnienia"'], fill=WARN_FILL, font=WARN))

# --- Składniki
ws = wb.create_sheet("Składniki")
head(ws, ["Przepis", "Składnik", "Ilość", "Jednostka", "Dział sklepu",
          "Oryginalny zapis", "Do sprawdzenia", "Ilość wg planu"],
     [44, 28, 8, 12, 22, 40, 14, 14])
MAXS = len(ing_rows) + 120
for i, x in enumerate(ing_rows):
    row = 2 + i
    ws.cell(row=row, column=1, value=x["recipe"])
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
        '/INDEX(Przepisy!$G:$G,MATCH($A{0},Przepisy!$B:$B,0)),0)').format(row))
    for ci in range(1, 9):
        c = ws.cell(row=row, column=ci)
        c.border = BORDER
        c.font = CALC if ci in (6, 8) else BASE
        c.alignment = Alignment(vertical="center")
        if ci in (3, 8):
            c.number_format = "0.##"
        if ci == 7:
            c.alignment = Alignment(horizontal="center")
            c.font = WARN
ws.freeze_panes = "B2"
ws.auto_filter.ref = "A1:H%d" % MAXS
dv(ws, "A2:A%d" % MAXS, "=Przepisy!$B$2:$B$%d" % MAXP)
dv(ws, "D2:D%d" % MAXS, "=Ustawienia!$B$2:$B$30")
dv(ws, "E2:E%d" % MAXS, "=Ustawienia!$C$2:$C$30")
ws.conditional_formatting.add("A2:H%d" % MAXS, FormulaRule(
    formula=['$G2="✔"'], fill=WARN_FILL))

# --- Plan
ws = wb.create_sheet("Plan")
head(ws, ["Dzień", "Posiłek", "Przepis", "Porcje"], [16, 14, 46, 10], 22)
row = 2
for di, d in enumerate(DNI):
    for mi, m in enumerate(POSILKI):
        ws.cell(row=row, column=1, value=d if mi == 0 else "")
        ws.cell(row=row, column=2, value=m)
        for ci in range(1, 5):
            c = ws.cell(row=row, column=ci)
            c.font = Font(name=F, size=10, bold=True) if ci == 1 else BASE
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
dv(ws, "C2:C%d" % LASTPLAN, "=Przepisy!$B$2:$B$%d" % MAXP)
for i, t in enumerate(["Jak używać", "1. W kolumnie C wybierz przepis z listy.",
                       "2. W kolumnie D wpisz liczbę porcji.",
                       "3. Lista zakupów przeliczy się sama.", "",
                       "Żółte pola wypełniasz Ty."]):
    c = ws.cell(row=1 + i, column=6, value=t)
    c.font = Font(name=F, size=(11 if i == 0 else 9), bold=(i == 0),
                  color=("2F5233" if i == 0 else "595959"))
ws.column_dimensions["F"].width = 46

# --- Lista zakupów
uniq, seen = [], {}
for x in ing_rows:
    k = (x["ing"], x["unit"])
    if k not in seen:
        seen[k] = x["section"]
        uniq.append(k)
uniq.sort(key=lambda k: (DZIALY.index(seen[k]) if seen[k] in DZIALY else 99, k[0].lower()))

ws = wb.create_sheet("Lista zakupów")
head(ws, ["Dział sklepu", "Składnik", "Jednostka", "Potrzeba", "Kupione"],
     [24, 30, 13, 12, 11])
MAXL = len(uniq) + 60
for i, k in enumerate(uniq):
    row = 2 + i
    ws.cell(row=row, column=1, value=seen[k])
    ws.cell(row=row, column=2, value=k[0])
    ws.cell(row=row, column=3, value=k[1])
for row in range(2, MAXL + 1):
    ws.cell(row=row, column=4, value=(
        '=IF($B{0}="","",SUMIFS(Składniki!$H:$H,Składniki!$B:$B,$B{0},'
        'Składniki!$D:$D,$C{0}))').format(row))
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
ws.conditional_formatting.add("A2:E%d" % MAXL, FormulaRule(
    formula=['$E2="✔"'], fill=PatternFill("solid", fgColor="E8F5E9")))

# --- Instrukcja
ws = wb.create_sheet("Instrukcja", 0)
ws.sheet_view.showGridLines = False
ws.column_dimensions["A"].width = 3
ws.column_dimensions["B"].width = 26
ws.column_dimensions["C"].width = 96
ws["B2"] = "Planer posiłków i lista zakupów"
ws["B2"].font = Font(name=F, bold=True, size=14, color="2F5233")
ws["B3"] = "%d przepisów z TikToka, Instagrama, YouTube i blogów." % len(recipes)
ws["B3"].font = Font(name=F, size=10, italic=True, color="595959")

n_done = sum(1 for r in recipes if r["n_ing"] > 0)
n_steps = sum(1 for r in recipes if r["steps"])
n_check = sum(1 for x in ing_rows if not x["ok"])
ROWS = [
    ("", ""),
    ("SKĄD SĄ DANE", ""),
    ("Twój plik", "Wszystkie przepisy z arkusza jedzenie.xlsx, razem z ilościami, "
                  "które już miałeś wpisane."),
    ("Kolekcja TikTok", "54 filmy z kolekcji „fud” — składniki odczytane z opisów pod filmami."),
    ("Zapisane na IG", "27 rolek z kolekcji „food” — składniki odczytane z opisów."),
    ("Strony przepisów", "aniagotuje.pl i opisy z YouTube."),
    ("", ""),
    ("JAK TO DZIAŁA", ""),
    ("1. Przepisy", "Baza %d przepisów: źródło, autor, klikalny link, porcje bazowe "
                    "i przygotowanie krok po kroku." % len(recipes)),
    ("2. Składniki", "Jeden wiersz = jeden składnik przepisu, w ilości na porcje bazowe."),
    ("3. Plan", "7 dni × 4 posiłki. Wybierasz przepis z listy i wpisujesz liczbę porcji."),
    ("4. Lista zakupów", "Przelicza się sama: skaluje do porcji, sumuje ten sam produkt "
                         "z różnych przepisów i grupuje po działach sklepu."),
    ("", ""),
    ("CO WYMAGA TWOJEJ UWAGI", ""),
    ("Kolumna Status", "%d przepisów ma rozpisane składniki, %d ma też opis przygotowania. "
                       "Reszta ma sam link — opis pod filmem nie zawierał przepisu "
                       "(autor odsyła do bio albo przepis jest tylko w nagraniu)."
                       % (n_done, n_steps)),
    ("Kolumna „Do sprawdzenia”", "%d pozycji, gdzie w opisie nie było jednoznacznej ilości — "
                                 "wpisałem 1 szt. Kolumna „Oryginalny zapis” pokazuje, "
                                 "co było w źródle." % n_check),
    ("Żółte porcje", "Liczba porcji, której nie było w źródle — przyjąłem 2. "
                     "Popraw, jeśli gotujesz inaczej, bo od tego zależy skalowanie."),
    ("", ""),
    ("WAŻNE", ""),
    ("Wybieraj z listy", "W arkuszu Plan zawsze wybieraj przepis z listy rozwijanej. "
                         "Wpisany ręcznie nie połączy się ze składnikami."),
    ("Jedna jednostka", "„Miód 2 łyżki” i „Miód 30 g” to dla arkusza dwie osobne pozycje "
                        "na liście zakupów."),
    ("Nowy składnik", "Jeśli dopiszesz w Składnikach produkt, którego nie ma na Liście zakupów, "
                      "dodaj go w pustym wierszu na dole listy — formuła jest tam gotowa."),
    ("Ukryj zbędne", "Na Liście zakupów włącz filtr w kolumnie Potrzeba i odznacz 0."),
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
print("Pozycji do sprawdzenia: %d" % n_check)
