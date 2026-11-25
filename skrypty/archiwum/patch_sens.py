# -*- coding: utf-8 -*-
"""Poprawki po weryfikacji "czy wszystko ma sens"."""
import io, re, sys

P = "build_v2.py"
s = io.open(P, encoding="utf-8").read()
n = 0


def rep(a, b, cnt=1):
    global s, n
    if s.count(a) != cnt:
        sys.exit("NIE ZNALAZLEM (%d):\n%s" % (s.count(a), a[:200]))
    s = s.replace(a, b)
    n += 1


def rep_tuple(label, nowy):
    """Podmienia cala krotke ("etykieta", "tekst...") w liscie ROWS Instrukcji."""
    global s, n
    rx = re.compile(r'\n    \("%s", .*?"\),\n' % re.escape(label), re.S)
    m = list(rx.finditer(s))
    if len(m) != 1:
        sys.exit("krotka %r: %d trafien" % (label, len(m)))
    s = s[:m[0].start()] + "\n" + nowy.rstrip("\n") + "\n" + s[m[0].end():]
    n += 1


# ------------------------------------------------------------------ 1. waga po ugotowaniu
rep('''for x in ing_rows:
    x["g"] = _g(x["ing"], x["unit"], 1)      # ile gramow wazy 1 jednostka tego wiersza''',
    '''# przepisy, w ktorych makaron/ryz gotuje sie w wodzie z listy (one-pan) - tam woda
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
    x["wyd"] = wydajnosc(x["ing"], x["recipe"])''')

rep('''    if x["g"]:
        ws.cell(row=row, column=18, value="=$C{0}*{1:g}".format(row, x["g"]))''',
    '''    if x["g"]:
        if x["fry"]:
            # olej do glebokiego smazenia w wiekszosci zostaje w garnku
            ws.cell(row=row, column=18, value="=IF($C{0}*{1:g}>={2:g},$C{0}*{3:.6g},$C{0}*{1:g})"
                    .format(row, x["g"], FRY_MIN_G, x["g"] * FRY_ABSORB))
        else:
            ws.cell(row=row, column=18, value="=$C{0}*{1:.6g}".format(row, x["g"] * x["wyd"]))''')
rep('''          "kcal light", "Tłuszcz light", "Gramy (baza)"],''',
    '''          "kcal light", "Tłuszcz light", "Gramy po ugotowaniu ≈"],''')

# ------------------------------------------------------------------ 2. porcje: na dzien, bez sosow
rep('''          "Waga porcji bazowej (g)", "Wpisz w Planie", "Twoja porcja (g)",
          "Jej porcja (g)", "Twoja porcja (kcal)", "Jej porcja (kcal)",''',
    '''          "W Planie na dzień", "Ugotuj razem (2 dni)", "Twoja porcja ≈ g",
          "Jej porcja ≈ g", "Twoja porcja (kcal)", "Jej porcja (kcal)",''')

stary = s[s.index("    # Garnek dzieli sie na 4 pojemniki"):s.index("    for ci in range(1, 34):")]
nowy = '''    # Garnek dzieli sie na 4 pojemniki: 2 Twoje wieksze i 2 jej mniejsze.
    # Y = ile porcji bazowych wpisac w Planie na JEDEN dzien; danie na 2 dni wpisuje sie
    # w dwa kolejne dni i lista zakupow sumuje oba. Sosy i napoje to nie posilek - puste.
    ws.cell(row=row, column=25, value=sprawdz(
        '=IF(OR($B{0}="",$L{0}="",$L{0}=0,$C{0}="Sos / dodatek",$C{0}="Napój"),"",'
        'MAX(0.25,ROUND((Ustawienia!$N$8+Ustawienia!$O$8)'
        '*IFERROR(VLOOKUP($C{0},Ustawienia!$Q$2:$R$12,2,0),0.3)/$L{0}*4,0)/4))'
        .format(row)))
    ws.cell(row=row, column=26, value=sprawdz('=IF($Y{0}="","",2*$Y{0})'.format(row)))
    for ci, udzial in ((27, "$N$10"), (28, "$O$10")):
        ws.cell(row=row, column=ci, value=sprawdz(
            '=IF($Y{0}="","",IFERROR(ROUND({1}/$G{0}*$Y{0}*Ustawienia!{2}),""))'
            .format(row, sumif(row, "R"), udzial)))
    for ci, udzial in ((29, "$N$10"), (30, "$O$10")):
        ws.cell(row=row, column=ci, value=sprawdz(
            '=IF($Y{0}="","",ROUND($L{0}*$Y{0}*Ustawienia!{1}))'.format(row, udzial)))
    ws.cell(row=row, column=31, value=sprawdz(
        '=IF($Y{0}="","",'
        'IF($Y{0}<1,"bardzo kaloryczne — na dzień dla Was obojga starczy "&$Y{0}&" porcji",'
        'IF($Y{0}>5,"lekkie — na dzień aż "&$Y{0}&" porcji, lepiej jako dodatek","")))'
        .format(row)))
'''
if not stary:
    sys.exit("nie znalazlem bloku porcji")
s = s.replace(stary, nowy)
n += 1

# ------------------------------------------------------------------ 3. ryz - uwaga o bezpieczenstwie nie moze zginac
rep('''for r in recipes:
    r["odgrz"], r["odgrz_jak"] = odgrzewanie(
        r["name"], " ".join(_skl.get(r["name"], [])), " ".join(r["steps"]))''',
    '''for r in recipes:
    r["odgrz"], r["odgrz_jak"] = odgrzewanie(
        r["name"], " ".join(_skl.get(r["name"], [])), " ".join(r["steps"]))
    # przy ryzu uwaga o szybkim schlodzeniu jest wazniejsza niz smak - dopisujemy ja zawsze
    if (r["odgrz"].startswith("Tak") and "ryż" not in r["odgrz_jak"].lower()
            and any(i.startswith("ryż") for i in _skl.get(r["name"], []))):
        r["odgrz_jak"] += (" Ryż wstaw do lodówki w ciągu godziny i zjedz w 24 h, "
                           "odgrzewając do gorąca.")''')

# ------------------------------------------------------------------ 4. Plan: kto ile zjadl + instrukcja
rep('''for ci, t in ((10, "Dzień"), (11, "kcal"), (12, "Białko (g)"),
              (13, "Tłuszcz (g)"), (14, "Węgle (g)"), (15, "kcal — light")):''',
    '''for ci, t in ((10, "Dzień"), (11, "kcal razem"), (12, "Białko (g)"),
              (13, "Tłuszcz (g)"), (14, "Węgle (g)"), (15, "kcal — light"),
              (17, "Ty (kcal)"), (18, "Ona (kcal)"), (19, "Wobec zapotrzebowania")):''')
rep('''    for ci in range(10, 16):
        ws.cell(row=rr, column=ci).border = BORDER''',
    '''    # ile z tego zjada kazde z Was przy podziale z Ustawien i ile to procent celu
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
        ws.cell(row=rr, column=ci).border = BORDER''')
rep('''for i, t in enumerate(["Jak używać", "1. W kolumnie C wybierz przepis z listy.",
                       "2. W kolumnie D wpisz liczbę z kolumny",
                       "   „Ugotuj na 2 dni” w arkuszu Przepisy.",
                       "3. Lista zakupów i makra przeliczą się same.", "",''',
    '''for i, t in enumerate(["Jak używać", "1. W kolumnie C wybierz przepis z listy.",
                       "2. W kolumnie D wpisz liczbę z kolumny",
                       "   „W Planie na dzień” w arkuszu Przepisy.",
                       "3. Danie na dwa dni wpisz w dwa kolejne dni —",
                       "   lista zakupów zsumuje oba, kupisz na jeden garnek.",
                       "4. Kolumny Ty / Ona po prawej mówią, ile każde",
                       "   z Was zje danego dnia i ile to % zapotrzebowania.", "",''')
rep('''for col, w in (("I", 3), ("J", 18), ("K", 9), ("L", 11), ("M", 11), ("N", 10), ("O", 12)):
    ws.column_dimensions[col].width = w''',
    '''for col, w in (("I", 3), ("J", 18), ("K", 10), ("L", 11), ("M", 11), ("N", 10), ("O", 12),
               ("Q", 10), ("R", 10), ("S", 22)):
    ws.column_dimensions[col].width = w''')

# ------------------------------------------------------------------ 5. Instrukcja: liczby i opisy
rep_tuple("Kolekcja TikTok",
          '''    ("Kolekcja TikTok", "54 z 56 filmów, które kolekcja „fud” realnie pokazuje — dwa "
                        "(drugą wersję ceviche i tikka masalę od jalalsamfit) usunąłeś jako "
                        "duplikaty. Licznik TikToka mówi 60, ale 4 pozycje w ogóle się nie "
                        "ładują — autorzy je skasowali albo ukryli."),''')
rep_tuple("Zapisane na IG",
          '''    ("Zapisane na IG", "27 rolek z kolekcji „food” plus 9 przepisów zapisanych poza tą "
                       "kolekcją. Przejrzałem wszystkie 620 zapisanych postów; spaghetti "
                       "hot dogi i dżem z borówek potem usunąłeś."),''')
rep_tuple("Kolumna „Wpisz w Planie”",
          '''    ("Kolumna „W Planie na dzień”", "Ile porcji BAZOWYCH tego przepisu wpisać w Planie na "
                                    "JEDEN dzień dla Was obojga. Danie na dwa dni wpisujesz "
                                    "w dwa kolejne dni — lista zakupów zsumuje oba i wyjdzie "
                                    "dokładnie jeden garnek. Kolumna obok, „Ugotuj razem”, "
                                    "mówi, ile to jest łącznie."),''')
rep_tuple("Twoja / Jej porcja",
          '''    ("Twoja / Jej porcja", "Kalorie są dokładne. Gramy to szacunek wagi PO ugotowaniu: "
                           "makaron wciąga wodę (×2,25), ryż jeszcze więcej (×2,5), mięso "
                           "ją traci (×0,75), a olej do smażenia w głębokim tłuszczu zostaje "
                           "w garnku. Najdokładniej: zważ cały garnek po ugotowaniu i weź "
                           "30% dla siebie, 20% dla niej."),''')
rep_tuple("Kolumna „Uwaga do porcji”",
          '''    ("Kolumna „Uwaga do porcji”", "Odzywa się przy skrajnych daniach: bardzo kalorycznych "
                                  "(na dzień starcza mniej niż jedna porcja bazowa) i bardzo "
                                  "lekkich (lepiej jako dodatek). Przy sosach i napojach "
                                  "kolumny porcji są puste — to nie jest posiłek."),''')
rep('''około 7% kalorii''', '''około 8% kalorii''')

io.open(P, "w", encoding="utf-8").write(s)
print("podmian:", n)
