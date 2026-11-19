# -*- coding: utf-8 -*-
"""Makra: odczyt z opisu autora + wyliczenie ze skladnikow."""
import re

# 0: kcal,P,C,F  |  1: kcal,P,C,F  |  2: kcal,B,T,W  |  3: kcal,B,W,T  |  4: B,W,T,kcal
PATS = [
    (re.compile(r"(\d{2,4})\s*(?:calories|kcal)[^\d]{0,20}(\d{1,3}(?:[.,]\d)?)\s*g?\s*"
                r"(?:protein|bia[łl]k\w*)"
                r"[^\d]{0,20}(\d{1,3}(?:[.,]\d)?)\s*g?\s*(?:carbs?|w[ęe]glowodan\w*)"
                r"[^\d]{0,20}(\d{1,3}(?:[.,]\d)?)\s*g?\s*(?:fat|t[łl]uszcz\w*)", re.I), "kPCF"),
    # "512 Calories 43gC | 12gF | 79.5gP" - kolejnosc wegle, tluszcz, bialko
    (re.compile(r"(\d{2,4})\s*(?:calories|kcal)\W{0,4}(\d{1,3}(?:[.,]\d)?)\s*g?\s*C\s*\|\s*"
                r"(\d{1,3}(?:[.,]\d)?)\s*g?\s*F\s*\|\s*(\d{1,3}(?:[.,]\d)?)\s*g?\s*P",
                re.I), "kCFP"),
    (re.compile(r"(\d{2,4})\s*(?:calories|kcal)\W{0,4}(\d{1,3}(?:[.,]\d)?)\s*g?\s*P\s*\|\s*"
                r"(\d{1,3}(?:[.,]\d)?)\s*g?\s*C\s*\|\s*(\d{1,3}(?:[.,]\d)?)\s*g?\s*F",
                re.I), "kPCF"),
    (re.compile(r"(\d{2,4})\s*kcal\s*(\d{1,3})\s*B\W{0,3}(\d{1,3})\s*T\W{0,3}(\d{1,3})\s*W",
                re.I), "kBTW"),
    # "340 kcal | BTW: 31/5/43" - bialko, tluszcz, wegle po ukosnikach
    (re.compile(r"(\d{2,4})\s*kcal\W{0,6}BTW\W{0,3}(\d{1,3}(?:[.,]\d)?)\s*/\s*"
                r"(\d{1,3}(?:[.,]\d)?)\s*/\s*(\d{1,3}(?:[.,]\d)?)", re.I), "kBTW"),
    # "Kcal: 755 B: 41 g W: 102 g T: 20 g" - liczba PO slowie kcal, kolejnosc B, W, T
    (re.compile(r"kcal\W{1,3}(\d{2,4})\W{0,4}B\W{0,3}(\d{1,3})\s*g?\W{0,3}W\W{0,3}"
                r"(\d{1,3})\s*g?\W{0,3}T\W{0,3}(\d{1,3})", re.I), "kBWT"),
    (re.compile(r"(\d{2,4})\s*kcal[^\d]{0,12}(\d{1,3})\s*g\s*bia[łl]k\w*[^\d]{0,18}"
                r"(\d{1,3})\s*g\s*w[ęe]glowodan\w*[^\d]{0,18}(\d{1,3})\s*g\s*t[łl]uszcz\w*",
                re.I), "kBWT"),
    (re.compile(r"B[:\s]*(\d{1,3})\s*g?\s*/\s*W[:\s]*(\d{1,3})\s*g?\s*/\s*T[:\s]*(\d{1,3})"
                r"\s*g?\s*/\s*(\d{2,4})\s*kcal", re.I), "BWTk"),
    (re.compile(r"(\d{2,4})\s*kcal\W{0,4}(\d{1,3})\s*B\b", re.I), "kP"),
    (re.compile(r"(\d{2,4})\s*(?:calories|kcal)[^\d]{0,25}(\d{1,3}(?:[.,]\d)?)\s*g\s*"
                r"(?:protein|bia[łl]k\w*)", re.I), "kP"),
    (re.compile(r"(\d{2,4})\s*cals?\b\W{0,4}(\d{1,3})\s*g\s*protein", re.I), "kP"),
    (re.compile(r"(?:calories|kcal)\s+per\s+(?:wrap|serving|portion|burrito|pita)\W{1,3}(\d{2,4})\b",
                re.I), "k"),
    (re.compile(r"(\d{2,4})\s*(?:calories|kcal)\b", re.I), "k"),
]
# odrzuc liczby, ktore nie sa makrami jednej porcji
BAD_CTX = re.compile(r"(?i)(ca[łl]ego dnia|per day|dziennie|na dob)")
# autor podaje wartosc ZA CALOSC, nie za porcje - trzeba podzielic przez liczbe porcji
WHOLE = re.compile(r"(?i)(ca[łl]a miska|ca[łl]y przepis|za ca[łl]o[śs][ćc]|"
                   r"whole (?:bowl|recipe|batch))")
# to znaczy DOKLADNIE ODWROTNIE - liczba jest per porcja
PER_PORTION = re.compile(r"(?i)(makro 1 porcji|na porcj|per serving|per meal|per burrito|"
                         r"jedna porcja|1 porcja|z przepisu wychodz|per portion|"
                         r"macros per|porcja ma)")


def is_whole_dish(txt):
    """True tylko wtedy, gdy liczba jawnie dotyczy calego dania, a nie porcji."""
    if not txt:
        return False
    m = re.search(r"(?i)[\d]{2,4}\s*(?:kcal|calories)", txt)
    if not m:
        return False
    win = txt[max(0, m.start() - 120):m.start() + 60]
    if PER_PORTION.search(win):
        return False
    return bool(WHOLE.search(win))


def author_macros(txt):
    """Zwraca (kcal, bialko, tluszcz, wegle) albo None. Brakujace pola = None."""
    if not txt or BAD_CTX.search(txt):
        return None
    for pat, kind in PATS:
        m = pat.search(txt)
        if not m:
            continue
        # zwykle zaokraglenie w gore od polowy - round() w Pythonie robi 44.5 -> 44
        g = [int(float(x.replace(",", ".")) + 0.5) for x in m.groups()]
        if kind == "kPCF":
            return (g[0], g[1], g[3], g[2])
        if kind == "kCFP":
            return (g[0], g[3], g[2], g[1])
        if kind == "kBTW":
            return (g[0], g[1], g[2], g[3])
        if kind == "kBWT":
            return (g[0], g[1], g[3], g[2])
        if kind == "BWTk":
            return (g[3], g[0], g[2], g[1])
        if kind == "kP":
            return (g[0], g[1], None, None)
        return (g[0], None, None, None)
    return None
