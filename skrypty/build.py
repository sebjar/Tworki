# -*- coding: utf-8 -*-
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule
from openpyxl.utils import get_column_letter

OUT = r"C:\Users\Sebastian\AppData\Roaming\Claude\scratch-workspaces\f6600729-d3a0-4174-95db-7e95c240059b\e71ad464-1f26-4802-846a-f6f5ff18c0ec\scratch-2026-09-09-4868ff\Planer-posilkow.xlsx"

F = "Arial"
HDR_FILL = PatternFill("solid", fgColor="2F5233")
HDR_FONT = Font(name=F, bold=True, color="FFFFFF", size=10)
TITLE_FONT = Font(name=F, bold=True, size=14, color="2F5233")
BASE = Font(name=F, size=10)
CALC = Font(name=F, size=10, color="808080", italic=True)
INPUT_FILL = PatternFill("solid", fgColor="FFFDE7")
EX_FILL = PatternFill("solid", fgColor="FFF3CD")
THIN = Side(style="thin", color="D0D0D0")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

wb = openpyxl.Workbook()

# ---------------------------------------------------------------- Ustawienia
KATEGORIE = ["\u015aniadanie", "Obiad", "Kolacja", "Przek\u0105ska", "Deser", "Zupa",
             "Sa\u0142atka", "Nap\u00f3j", "Sos / dodatek"]
ZRODLA = ["TikTok", "Instagram", "YouTube", "Blog", "W\u0142asny", "Ksi\u0105\u017cka"]
JEDNOSTKI = ["g", "kg", "ml", "l", "szt.", "\u0142y\u017cka", "\u0142y\u017ceczka", "szklanka",
             "opak.", "z\u0105bek", "gar\u015b\u0107", "szczypta", "plaster", "puszka", "p\u0119czek"]
DZIALY = ["Warzywa i owoce", "Mi\u0119so i ryby", "Nabia\u0142 i jaja", "Pieczywo",
          "Sypkie i makarony", "Oleje i sosy", "Konserwy i s\u0142oiki",
          "Przyprawy i zio\u0142a", "Mro\u017conki", "Napoje", "S\u0142odycze i przek\u0105ski", "Inne"]
POSILKI = ["\u015aniadanie", "Obiad", "Kolacja", "Przek\u0105ska"]
TRUDNOSC = ["\u0141atwe", "\u015arednie", "Trudne"]
DNI = ["Poniedzia\u0142ek", "Wtorek", "\u015aroda", "Czwartek", "Pi\u0105tek", "Sobota", "Niedziela"]

ws = wb.active
ws.title = "Ustawienia"
cols = [("Kategorie", KATEGORIE), ("\u0179r\u00f3d\u0142a", ZRODLA), ("Jednostki", JEDNOSTKI),
        ("Dzia\u0142y sklepu", DZIALY), ("Posi\u0142ki", POSILKI), ("Trudno\u015b\u0107", TRUDNOSC)]
for ci, (name, vals) in enumerate(cols, start=1):
    c = ws.cell(row=1, column=ci, value=name)
    c.font = HDR_FONT
    c.fill = HDR_FILL
    for ri, v in enumerate(vals, start=2):
        ws.cell(row=ri, column=ci, value=v).font = BASE
    ws.column_dimensions[get_column_letter(ci)].width = 22
ws.freeze_panes = "A2"
ws.cell(row=20, column=8, value="Te listy zasilaj\u0105 rozwijane menu w pozosta\u0142ych arkuszach. "
                                "Mo\u017cesz je dopisywa\u0107 \u2014 nowe pozycje pojawi\u0105 si\u0119 "
                                "w listach automatycznie (do 30 wierszy).").font = Font(
    name=F, size=9, italic=True, color="808080")

# ---------------------------------------------------------------- Przepisy
PRZ_HDR = ["ID", "Nazwa przepisu", "Kategoria", "\u0179r\u00f3d\u0142o", "Link", "Porcje bazowe",
           "Czas (min)", "Trudno\u015b\u0107", "Tagi", "Przygotowanie", "Notatki"]
PRZ_W = [8, 34, 15, 13, 42, 13, 11, 12, 24, 72, 26]

PRZEPISY = [
    ["Zapiekana feta z pomidorkami i makaronem", "Obiad", "TikTok", "(wklej link)", 4, 40,
     "\u0141atwe", "wegetaria\u0144skie, one-pot",
     "1. Piekarnik 200\u00b0C (g\u00f3ra-d\u00f3\u0142).\n"
     "2. W \u017caroodpornym naczyniu wymieszaj pomidorki koktajlowe z oliw\u0105, sol\u0105 i pieprzem.\n"
     "3. Po\u0142\u00f3\u017c blok fety po \u015brodku, skrop oliw\u0105.\n"
     "4. Piecz 30 min, a\u017c pomidorki p\u0119kn\u0105, a feta si\u0119 zarumieni.\n"
     "5. W tym czasie ugotuj makaron al dente, zachowaj 1 szklank\u0119 wody z gotowania.\n"
     "6. Do gor\u0105cego naczynia dodaj przeci\u015bni\u0119ty czosnek i rozgnie\u0107 wszystko widelcem na sos.\n"
     "7. Wymieszaj z makaronem, rozrzed\u017a wod\u0105 z gotowania, dorzu\u0107 \u015bwie\u017c\u0105 bazyli\u0119."],
    ["Owsianka nocna z bor\u00f3wkami", "\u015aniadanie", "Instagram", "(wklej link)", 2, 10,
     "\u0141atwe", "meal prep, bez gotowania",
     "1. W s\u0142oiku wymieszaj p\u0142atki owsiane, nasiona chia, mleko i jogurt.\n"
     "2. Dodaj mi\u00f3d, wymieszaj.\n"
     "3. Wstaw do lod\u00f3wki na noc (min. 6 h).\n"
     "4. Rano dodaj bor\u00f3wki i ewentualnie orzechy."],
    ["Kurczak teriyaki z ry\u017cem", "Obiad", "TikTok", "(wklej link)", 3, 30,
     "\u015arednie", "szybkie, patelnia",
     "1. Ugotuj ry\u017c wed\u0142ug opakowania.\n"
     "2. Pier\u015b z kurczaka pokr\u00f3j w kostk\u0119, podsma\u017c na oleju sezamowym na z\u0142oto.\n"
     "3. Wymieszaj sos sojowy, mi\u00f3d, starty imbir i czosnek.\n"
     "4. Wlej sos na patelni\u0119, sma\u017c 3-4 min, a\u017c zg\u0119stnieje i oblepi kurczaka.\n"
     "5. Podawaj na ry\u017cu, posyp sezamem i dymk\u0105."],
]

ws = wb.create_sheet("Przepisy")
for ci, h in enumerate(PRZ_HDR, start=1):
    c = ws.cell(row=1, column=ci, value=h)
    c.font = HDR_FONT
    c.fill = HDR_FILL
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.column_dimensions[get_column_letter(ci)].width = PRZ_W[ci - 1]
ws.row_dimensions[1].height = 28

for i, r in enumerate(PRZEPISY):
    row = 2 + i
    for off, ci in enumerate([2, 3, 4, 5, 6, 7, 8, 9, 10]):
        ws.cell(row=row, column=ci, value=r[off])
    ws.row_dimensions[row].height = 130

MAXP = 101
for row in range(2, MAXP + 1):
    ws.cell(row=row, column=1, value='=IF($B{0}="","","P"&TEXT(ROW()-1,"000"))'.format(row))
    for ci in range(1, 12):
        c = ws.cell(row=row, column=ci)
        c.font = CALC if ci == 1 else BASE
        c.border = BORDER
        c.alignment = Alignment(vertical="top", wrap_text=(ci in (9, 10, 11)))
        if ci in (6, 7):
            c.alignment = Alignment(vertical="top", horizontal="center")
        if row <= 1 + len(PRZEPISY):
            c.fill = EX_FILL
ws.freeze_panes = "C2"
ws.auto_filter.ref = "A1:K{0}".format(MAXP)


def dv(sheet, rng, src):
    d = DataValidation(type="list", formula1=src, allow_blank=True, showDropDown=False)
    sheet.add_data_validation(d)
    d.add(rng)


dv(ws, "C2:C{0}".format(MAXP), "=Ustawienia!$A$2:$A$30")
dv(ws, "D2:D{0}".format(MAXP), "=Ustawienia!$B$2:$B$30")
dv(ws, "H2:H{0}".format(MAXP), "=Ustawienia!$F$2:$F$30")

# ---------------------------------------------------------------- Skladniki
SKL_HDR = ["Przepis", "Sk\u0142adnik", "Ilo\u015b\u0107", "Jednostka", "Dzia\u0142 sklepu",
           "Ilo\u015b\u0107 wg planu"]
SKL_W = [36, 30, 10, 14, 24, 16]
P1, P2, P3 = PRZEPISY[0][0], PRZEPISY[1][0], PRZEPISY[2][0]
SKLADNIKI = [
    [P1, "Makaron penne", 400, "g", "Sypkie i makarony"],
    [P1, "Ser feta", 200, "g", "Nabia\u0142 i jaja"],
    [P1, "Pomidorki koktajlowe", 500, "g", "Warzywa i owoce"],
    [P1, "Oliwa z oliwek", 60, "ml", "Oleje i sosy"],
    [P1, "Czosnek", 3, "z\u0105bek", "Warzywa i owoce"],
    [P1, "Bazylia \u015bwie\u017ca", 1, "p\u0119czek", "Warzywa i owoce"],
    [P1, "S\u00f3l", 1, "\u0142y\u017ceczka", "Przyprawy i zio\u0142a"],
    [P1, "Pieprz czarny", 1, "szczypta", "Przyprawy i zio\u0142a"],
    [P2, "P\u0142atki owsiane", 100, "g", "Sypkie i makarony"],
    [P2, "Mleko", 250, "ml", "Nabia\u0142 i jaja"],
    [P2, "Jogurt naturalny", 150, "g", "Nabia\u0142 i jaja"],
    [P2, "Nasiona chia", 2, "\u0142y\u017cka", "Sypkie i makarony"],
    [P2, "Mi\u00f3d", 2, "\u0142y\u017cka", "S\u0142odycze i przek\u0105ski"],
    [P2, "Bor\u00f3wki", 100, "g", "Warzywa i owoce"],
    [P3, "Pier\u015b z kurczaka", 500, "g", "Mi\u0119so i ryby"],
    [P3, "Ry\u017c ja\u015bminowy", 240, "g", "Sypkie i makarony"],
    [P3, "Sos sojowy", 60, "ml", "Oleje i sosy"],
    [P3, "Mi\u00f3d", 2, "\u0142y\u017cka", "S\u0142odycze i przek\u0105ski"],
    [P3, "Imbir \u015bwie\u017cy", 20, "g", "Warzywa i owoce"],
    [P3, "Czosnek", 2, "z\u0105bek", "Warzywa i owoce"],
    [P3, "Olej sezamowy", 1, "\u0142y\u017cka", "Oleje i sosy"],
    [P3, "Cebula dymka", 1, "p\u0119czek", "Warzywa i owoce"],
    [P3, "Sezam", 1, "\u0142y\u017cka", "Przyprawy i zio\u0142a"],
]

ws = wb.create_sheet("Sk\u0142adniki")
for ci, h in enumerate(SKL_HDR, start=1):
    c = ws.cell(row=1, column=ci, value=h)
    c.font = HDR_FONT
    c.fill = HDR_FILL
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.column_dimensions[get_column_letter(ci)].width = SKL_W[ci - 1]
ws.row_dimensions[1].height = 28

for i, r in enumerate(SKLADNIKI):
    for ci, v in enumerate(r, start=1):
        ws.cell(row=2 + i, column=ci, value=v)

MAXS = 501
for row in range(2, MAXS + 1):
    ws.cell(row=row, column=6, value=(
        '=IFERROR($C{0}*SUMIF(Plan!$C:$C,$A{0},Plan!$D:$D)'
        '/INDEX(Przepisy!$F:$F,MATCH($A{0},Przepisy!$B:$B,0)),0)').format(row))
    for ci in range(1, 7):
        c = ws.cell(row=row, column=ci)
        c.font = CALC if ci == 6 else BASE
        c.border = BORDER
        if ci in (3, 6):
            c.number_format = "0.##"
        if row <= 1 + len(SKLADNIKI):
            c.fill = EX_FILL
ws.freeze_panes = "B2"
ws.auto_filter.ref = "A1:F{0}".format(MAXS)
dv(ws, "A2:A{0}".format(MAXS), "=Przepisy!$B$2:$B$101")
dv(ws, "D2:D{0}".format(MAXS), "=Ustawienia!$C$2:$C$30")
dv(ws, "E2:E{0}".format(MAXS), "=Ustawienia!$D$2:$D$30")

# ---------------------------------------------------------------- Plan
ws = wb.create_sheet("Plan")
for ci, h in enumerate(["Dzie\u0144", "Posi\u0142ek", "Przepis", "Porcje"], start=1):
    c = ws.cell(row=1, column=ci, value=h)
    c.font = HDR_FONT
    c.fill = HDR_FILL
    c.alignment = Alignment(horizontal="center", vertical="center")
for ci, w in enumerate([16, 14, 38, 10], start=1):
    ws.column_dimensions[get_column_letter(ci)].width = w
ws.row_dimensions[1].height = 22

PLAN_EX = {(0, 1): (P1, 4), (1, 0): (P2, 4), (2, 1): (P3, 6), (4, 1): (P1, 2)}
row = 2
for di, d in enumerate(DNI):
    for mi, m in enumerate(POSILKI):
        ws.cell(row=row, column=1, value=d if mi == 0 else "")
        ws.cell(row=row, column=2, value=m)
        if (di, mi) in PLAN_EX:
            ws.cell(row=row, column=3, value=PLAN_EX[(di, mi)][0])
            ws.cell(row=row, column=4, value=PLAN_EX[(di, mi)][1])
        for ci in range(1, 5):
            c = ws.cell(row=row, column=ci)
            c.font = Font(name=F, size=10, bold=True) if ci == 1 else BASE
            c.border = BORDER
            if ci == 4:
                c.alignment = Alignment(horizontal="center")
            if ci in (3, 4):
                c.fill = INPUT_FILL
            elif di % 2 == 1:
                c.fill = PatternFill("solid", fgColor="F2F2F2")
        row += 1
LASTPLAN = row - 1
ws.freeze_panes = "C2"
dv(ws, "C2:C{0}".format(LASTPLAN), "=Przepisy!$B$2:$B$101")

ws.cell(row=1, column=6, value="Jak u\u017cywa\u0107").font = Font(name=F, bold=True, size=11, color="2F5233")
for i, t in enumerate([
    "1. W kolumnie C wybierz przepis z listy rozwijanej.",
    "2. W kolumnie D wpisz, ile porcji chcesz zje\u015b\u0107.",
    "3. Lista zakup\u00f3w przeliczy si\u0119 sama.",
    "",
    "\u017b\u00f3\u0142te pola = do wype\u0142nienia przez Ciebie.",
    "Wype\u0142nione teraz wiersze to przyk\u0142ad \u2014 mo\u017cesz je wyczy\u015bci\u0107.",
]):
    ws.cell(row=2 + i, column=6, value=t).font = Font(name=F, size=9, color="595959")
ws.column_dimensions["F"].width = 52

# ---------------------------------------------------------------- Lista zakupow
uniq, seen = [], {}
for przep, skl, il, jed, dzial in SKLADNIKI:
    key = (skl, jed)
    if key not in seen:
        seen[key] = [dzial, []]
        uniq.append(key)
    seen[key][1].append(przep)
order = {d: i for i, d in enumerate(DZIALY)}
uniq.sort(key=lambda k: (order.get(seen[k][0], 99), k[0]))

ws = wb.create_sheet("Lista zakup\u00f3w")
for ci, h in enumerate(["Dzia\u0142 sklepu", "Sk\u0142adnik", "Jednostka", "Potrzeba", "Kupione",
                        "Wyst\u0119puje w przepisach"], start=1):
    c = ws.cell(row=1, column=ci, value=h)
    c.font = HDR_FONT
    c.fill = HDR_FILL
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
for ci, w in enumerate([24, 30, 13, 12, 11, 46], start=1):
    ws.column_dimensions[get_column_letter(ci)].width = w
ws.row_dimensions[1].height = 28

for i, key in enumerate(uniq):
    row = 2 + i
    ws.cell(row=row, column=1, value=seen[key][0])
    ws.cell(row=row, column=2, value=key[0])
    ws.cell(row=row, column=3, value=key[1])
    ws.cell(row=row, column=6, value=", ".join(sorted(set(seen[key][1]))))

MAXL = 1 + len(uniq) + 40
for row in range(2, MAXL + 1):
    ws.cell(row=row, column=4, value=(
        '=IF($B{0}="","",SUMIFS(Sk\u0142adniki!$F:$F,Sk\u0142adniki!$B:$B,$B{0},'
        'Sk\u0142adniki!$D:$D,$C{0}))').format(row))
    for ci in range(1, 7):
        c = ws.cell(row=row, column=ci)
        c.font = BASE
        c.border = BORDER
        c.alignment = Alignment(vertical="center", wrap_text=(ci == 6))
        if ci == 4:
            c.number_format = "0.##"
            c.font = Font(name=F, size=10, bold=True)
            c.alignment = Alignment(horizontal="center")
        if ci == 5:
            c.fill = INPUT_FILL
            c.alignment = Alignment(horizontal="center")
ws.freeze_panes = "B2"
ws.auto_filter.ref = "A1:F{0}".format(MAXL)
dv(ws, "A2:A{0}".format(MAXL), "=Ustawienia!$D$2:$D$30")
dv(ws, "C2:C{0}".format(MAXL), "=Ustawienia!$C$2:$C$30")
dv(ws, "E2:E{0}".format(MAXL), '"\u2713"')
ws.conditional_formatting.add("A2:F{0}".format(MAXL), FormulaRule(
    formula=['AND($B2<>"",$D2=0)'], font=Font(name=F, size=10, color="BFBFBF")))
ws.conditional_formatting.add("A2:F{0}".format(MAXL), FormulaRule(
    formula=['$E2="\u2713"'], fill=PatternFill("solid", fgColor="E8F5E9")))

# ---------------------------------------------------------------- Instrukcja
ws = wb.create_sheet("Instrukcja", 0)
ws.column_dimensions["A"].width = 3
ws.column_dimensions["B"].width = 26
ws.column_dimensions["C"].width = 92
ws.sheet_view.showGridLines = False
ws["B2"] = "Planer posi\u0142k\u00f3w i lista zakup\u00f3w"
ws["B2"].font = TITLE_FONT
ws["B3"] = "Wybierasz przepisy na tydzie\u0144 \u2014 lista zakup\u00f3w liczy si\u0119 sama."
ws["B3"].font = Font(name=F, size=10, italic=True, color="595959")

ROWS = [
    ("", ""),
    ("JAK TO DZIA\u0141A", ""),
    ("1. Przepisy", "Baza wszystkich przepis\u00f3w: nazwa, \u017ar\u00f3d\u0142o (TikTok / Instagram), "
                    "link, liczba porcji bazowych i pe\u0142ny spos\u00f3b przygotowania."),
    ("2. Sk\u0142adniki", "Jeden wiersz = jeden sk\u0142adnik jednego przepisu. Ilo\u015bci podajesz "
                          "dla liczby porcji bazowych z arkusza Przepisy."),
    ("3. Plan", "Siatka 7 dni \u00d7 4 posi\u0142ki. Wybierasz przepis z listy i wpisujesz liczb\u0119 porcji."),
    ("4. Lista zakup\u00f3w", "Przelicza si\u0119 automatycznie z Planu: sumuje ten sam sk\u0142adnik "
                              "ze wszystkich zaplanowanych przepis\u00f3w i skaluje do liczby porcji."),
    ("5. Ustawienia", "Listy zasilaj\u0105ce rozwijane menu (kategorie, jednostki, dzia\u0142y sklepu). "
                      "Mo\u017cesz je dopisywa\u0107."),
    ("", ""),
    ("CO WYPE\u0141NIASZ", ""),
    ("\u017b\u00f3\u0142te pola", "Kom\u00f3rki do wype\u0142nienia przez Ciebie \u2014 kolumny Przepis "
                                  "i Porcje w arkuszu Plan oraz Kupione na Li\u015bcie zakup\u00f3w."),
    ("Szare, kursyw\u0105", "Kolumny wyliczane formu\u0142\u0105 (ID przepisu, Ilo\u015b\u0107 wg planu, "
                            "Potrzeba). Nie nadpisuj ich."),
    ("Pomara\u0144czowe wiersze", "Przyk\u0142adowe dane pokazuj\u0105ce oczekiwany format. Usu\u0144 je, "
                                  "gdy wgramy Twoje w\u0142asne przepisy."),
    ("", ""),
    ("PRZYK\u0141AD PRZELICZENIA", ""),
    ("", "Kurczak teriyaki ma 3 porcje bazowe i 500 g piersi. Planujesz 6 porcji \u2192 lista zakup\u00f3w "
         "poka\u017ce 1000 g. Je\u015bli inny zaplanowany przepis te\u017c u\u017cywa piersi z kurczaka, "
         "ilo\u015bci si\u0119 zsumuj\u0105 w jednej pozycji."),
    ("", ""),
    ("WA\u017bNE", ""),
    ("Nazwy musz\u0105 pasowa\u0107", "Sk\u0142adniki \u0142\u0105cz\u0105 si\u0119 z przepisami po nazwie. "
                                      "Zawsze wybieraj przepis z listy rozwijanej, nie wpisuj r\u0119cznie."),
    ("Jedna jednostka na produkt", "\u201eMi\u00f3d 2 \u0142y\u017cki\u201d i \u201eMi\u00f3d 30 g\u201d to dla "
                                   "arkusza dwie r\u00f3\u017cne pozycje. Trzymaj jedn\u0105 jednostk\u0119 "
                                   "dla danego sk\u0142adnika."),
    ("Nowy sk\u0142adnik", "Je\u015bli w arkuszu Sk\u0142adniki dodasz produkt, kt\u00f3rego nie ma jeszcze na "
                           "Li\u015bcie zakup\u00f3w, dopisz go w pustym wierszu na dole listy (dzia\u0142, "
                           "nazwa, jednostka) \u2014 formu\u0142a w kolumnie Potrzeba jest tam ju\u017c gotowa."),
    ("Ukryj niepotrzebne", "Na Li\u015bcie zakup\u00f3w w\u0142\u0105cz filtr w kolumnie Potrzeba i odznacz 0, "
                           "\u017ceby zosta\u0142y tylko produkty na ten tydzie\u0144."),
]
r = 5
for label, text in ROWS:
    if label and not text:
        c = ws.cell(row=r, column=2, value=label)
        c.font = Font(name=F, bold=True, size=10, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="2F5233")
        ws.cell(row=r, column=3).fill = PatternFill("solid", fgColor="2F5233")
    else:
        ws.cell(row=r, column=2, value=label).font = Font(name=F, bold=True, size=10)
        c = ws.cell(row=r, column=3, value=text)
        c.font = BASE
        c.alignment = Alignment(wrap_text=True, vertical="top")
        if text:
            ws.row_dimensions[r].height = 32
    r += 1

wb.save(OUT)
print("saved")
