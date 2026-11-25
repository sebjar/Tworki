# -*- coding: utf-8 -*-
"""Makra autora: liczby ulamkowe (44.5 g) i kolejnosc kcal / C / F / P."""
import io, sys
P = "macros_calc.py"
s = io.open(P, encoding="utf-8").read()


def rep(a, b):
    global s
    if s.count(a) != 1:
        sys.exit("NIE ZNALAZLEM:\n" + a[:160])
    s = s.replace(a, b)


# liczba moze byc ulamkowa: "44.5g protein", "79,5 g bialka"
rep(r'''    (re.compile(r"(\d{2,4})\s*(?:calories|kcal)[^\d]{0,20}(\d{1,3})\s*g?\s*(?:protein|bia[łl]k\w*)"
                r"[^\d]{0,20}(\d{1,3})\s*g?\s*(?:carbs?|w[ęe]glowodan\w*)"
                r"[^\d]{0,20}(\d{1,3})\s*g?\s*(?:fat|t[łl]uszcz\w*)", re.I), "kPCF"),''',
    r'''    (re.compile(r"(\d{2,4})\s*(?:calories|kcal)[^\d]{0,20}(\d{1,3}(?:[.,]\d)?)\s*g?\s*"
                r"(?:protein|bia[łl]k\w*)"
                r"[^\d]{0,20}(\d{1,3}(?:[.,]\d)?)\s*g?\s*(?:carbs?|w[ęe]glowodan\w*)"
                r"[^\d]{0,20}(\d{1,3}(?:[.,]\d)?)\s*g?\s*(?:fat|t[łl]uszcz\w*)", re.I), "kPCF"),
    # "512 Calories 43gC | 12gF | 79.5gP" - kolejnosc wegle, tluszcz, bialko
    (re.compile(r"(\d{2,4})\s*(?:calories|kcal)\W{0,4}(\d{1,3}(?:[.,]\d)?)\s*g?\s*C\s*\|\s*"
                r"(\d{1,3}(?:[.,]\d)?)\s*g?\s*F\s*\|\s*(\d{1,3}(?:[.,]\d)?)\s*g?\s*P",
                re.I), "kCFP"),''')

# ulamki takze w pozostalych wzorcach
rep(r'''    (re.compile(r"(\d{2,4})\s*(?:calories|kcal)\s*(\d{1,3})\s*g?\s*P\s*\|\s*(\d{1,3})\s*g?\s*C"
                r"\s*\|\s*(\d{1,3})\s*g?\s*F", re.I), "kPCF"),''',
    r'''    (re.compile(r"(\d{2,4})\s*(?:calories|kcal)\W{0,4}(\d{1,3}(?:[.,]\d)?)\s*g?\s*P\s*\|\s*"
                r"(\d{1,3}(?:[.,]\d)?)\s*g?\s*C\s*\|\s*(\d{1,3}(?:[.,]\d)?)\s*g?\s*F",
                re.I), "kPCF"),''')
rep(r'''    (re.compile(r"(\d{2,4})\s*(?:calories|kcal)[^\d]{0,25}(\d{1,3})\s*g\s*(?:protein|bia[łl]k\w*)",
                re.I), "kP"),''',
    r'''    (re.compile(r"(\d{2,4})\s*(?:calories|kcal)[^\d]{0,25}(\d{1,3}(?:[.,]\d)?)\s*g\s*"
                r"(?:protein|bia[łl]k\w*)", re.I), "kP"),''')

# odczyt liczb: przecinek jak kropka, wynik zaokraglony do grama
rep('''        g = [int(x) for x in m.groups()]''',
    '''        g = [int(round(float(x.replace(",", ".")))) for x in m.groups()]''')
rep('''        if kind == "kBTW":''',
    '''        if kind == "kCFP":
            return (g[0], g[3], g[2], g[1])
        if kind == "kBTW":''')

io.open(P, "w", encoding="utf-8").write(s)
print("ok")
