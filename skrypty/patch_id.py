# -*- coding: utf-8 -*-
"""Wprowadza ID przepisu (P001) wszedzie tam, gdzie dotad byla sama nazwa."""
import io, sys

P = "build_v2.py"
s = io.open(P, encoding="utf-8").read()
n = 0


def rep(a, b, cnt=1):
    global s, n
    if s.count(a) != cnt:
        sys.exit("NIE ZNALAZLEM (%d/%d):\n%s" % (s.count(a), cnt, a[:200]))
    s = s.replace(a, b)
    n += 1


# --- 1. "Podobne do": zbieramy nazwy, etykiety zlozymy po nadaniu ID
rep('''for r in recipes:
    r["similar"] = ", ".join(sorted(set(SIM.get(r["name"], []))))''',
    '''for r in recipes:
    r["similar_names"] = sorted(set(SIM.get(r["name"], [])))
    r["similar"] = ""''')

# --- 2. nadanie ID zaraz po ustaleniu kolejnosci wierszy
rep('''ing_rows.sort(key=lambda x: order_r.get(x["recipe"], 9999))''',
    '''ing_rows.sort(key=lambda x: order_r.get(x["recipe"], 9999))

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
                                                    key=lambda m: RID.get(m, "")))''')

# --- 3. Ustawienia: kolumna z kluczem "P001: Nazwa" dla list rozwijanych
rep('''    ws.column_dimensions[get_column_letter(ci)].width = 22
ws.freeze_panes = "A2"''',
    '''    ws.column_dimensions[get_column_letter(ci)].width = 22
# klucz przepisu dla list rozwijanych - liczy sie sam, wiec obejmie tez recznie dopisane
c = ws.cell(row=1, column=5, value="Przepisy (ID: nazwa)")
c.font = HDR_FONT
c.fill = HDR_FILL
for ri in range(2, len(recipes) + 41):
    ws.cell(row=ri, column=5, value='=IF(Przepisy!$B{0}="","",Przepisy!$A{0}&": "&Przepisy!$B{0})'
            .format(ri)).font = CALC
ws.column_dimensions["E"].width = 54
ws.freeze_panes = "A2"''')

# --- 4. szerokosc kolumny "Podobne do" - miesci sie teraz ID + nazwa
rep('''     [7, 46, 14, 12, 20, 44, 9, 10, 13, 88, 42, 12, 11, 11, 10, 12, 12, 12, 11, 22])''',
    '''     [7, 46, 14, 12, 20, 44, 9, 10, 13, 88, 54, 12, 11, 11, 10, 12, 12, 12, 11, 22])''')

# --- 5. Skladniki: naglowek, szerokosc i wartosc kolumny A
rep('''head(ws, ["Przepis", "Składnik", "Ilość", "Jednostka", "Dział sklepu",
          "Oryginalny zapis", "Do sprawdzenia", "Ilość wg planu", "Gramy wg planu"],
     [46, 28, 8, 12, 22, 38, 14, 14, 13])''',
    '''head(ws, ["Przepis (ID: nazwa)", "Składnik", "Ilość", "Jednostka", "Dział sklepu",
          "Oryginalny zapis", "Do sprawdzenia", "Ilość wg planu", "Gramy wg planu"],
     [54, 28, 8, 12, 22, 38, 14, 14, 13])''')
rep('''    ws.cell(row=row, column=1, value=x["recipe"])
    ws.cell(row=row, column=2, value=x["ing"])''',
    '''    ws.cell(row=row, column=1, value=x["rkey"])
    ws.cell(row=row, column=2, value=x["ing"])''')

# --- 6. Skladniki: wyszukiwanie po ID, nie po nazwie (odporne na zmiane nazwy)
rep('''        '=IFERROR($C{0}*SUMIF(Plan!$C:$C,$A{0},Plan!$D:$D)'
        '/INDEX(Przepisy!$G:$G,MATCH($A{0},Przepisy!$B:$B,0)),0)').format(row))''',
    '''        '=IFERROR($C{0}*SUMIF(Plan!$C:$C,$A{0},Plan!$D:$D)'
        '/INDEX(Przepisy!$G:$G,MATCH(LEFT($A{0},4),Przepisy!$A:$A,0)),0)').format(row))''')
rep('''dv(ws, "A2:A%d" % MAXS, "=Przepisy!$B$2:$B$%d" % MAXP)''',
    '''dv(ws, "A2:A%d" % MAXS, "=Ustawienia!$E$2:$E$%d" % MAXP)''')

# --- 7. Plan: naglowek, lista rozwijana i makra po ID
rep('''head(ws, ["Dzień", "Posiłek", "Przepis", "Porcje", "kcal", "Białko (g)",
          "Tłuszcz (g)", "Węgle (g)"],
     [16, 14, 46, 9, 9, 11, 11, 10], 22)''',
    '''head(ws, ["Dzień", "Posiłek", "Przepis (ID: nazwa)", "Porcje", "kcal", "Białko (g)",
          "Tłuszcz (g)", "Węgle (g)"],
     [16, 14, 54, 9, 9, 11, 11, 10], 22)''')
rep('''                '=IFERROR($D{0}*INDEX(Przepisy!${1}:${1},'
                'MATCH($C{0},Przepisy!$B:$B,0)),"")').format(row, src_col))''',
    '''                '=IFERROR($D{0}*INDEX(Przepisy!${1}:${1},'
                'MATCH(LEFT($C{0},4),Przepisy!$A:$A,0)),"")').format(row, src_col))''')
rep('''dv(ws, "C2:C%d" % LASTPLAN, "=Przepisy!$B$2:$B$%d" % MAXP)''',
    '''dv(ws, "C2:C%d" % LASTPLAN, "=Ustawienia!$E$2:$E$%d" % MAXP)''')

# --- 8. Instrukcja: skad sie biora ID
rep('''    ("", ""),
    ("JAK TO DZIAŁA", ""),''',
    '''    ("", ""),
    ("ID PRZEPISU", ""),
    ("Kolumna A", "Każdy przepis ma numer P001, P002... Wszędzie, gdzie odwołuję się do "
                  "przepisu — w Planie, w Składnikach i w kolumnie „Podobne do” — piszę "
                  "„P012: Nazwa”, żebyś po numerze od razu trafił do właściwego wiersza."),
    ("Zmiana nazwy", "Plan i Składniki szukają przepisu po numerze, nie po nazwie, "
                     "więc możesz zmieniać nazwy bez psucia przeliczeń."),
    ("", ""),
    ("JAK TO DZIAŁA", ""),''')

io.open(P, "w", encoding="utf-8").write(s)
print("podmian:", n)
