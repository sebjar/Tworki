# -*- coding: utf-8 -*-
"""Kategorie posilkow + wykrywanie przepisow podobnych/duplikatow."""
import re, unicodedata


def deacc(s):
    s = (s or "").replace("ł", "l").replace("Ł", "L")
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


# regula: (kategoria, wzorzec w nazwie)  - pierwsza pasujaca wygrywa
RULES = [
    ("Sos / dodatek", r"\bsos\b|tzatziki|\bdip\b|glazura|dressing|marynata|majonez\b|"
                      r"metoda smazenia"),
    ("Zupa", r"\bzupa\b|harira|rosol|krem z |chowder|\bsoup\b"),
    ("Sałatka", r"salatka|\bsalat\b|coleslaw|ceviche|\bsalad\b"),
    # Sniadanie przed Deserem: owsianka nocna to sniadanie, mimo ze bywa "o smaku szarlotki"
    ("Śniadanie", r"owsianka|oats|nalesnik|pancake|jajecznic|omlet|chaczapuri|\btost\b|"
                  r"kanapk|shakshuka|sniadan|granola|jogurt naturalny$"),
    ("Deser", r"\blody\b|pudding|deser|sernik|\bciasto\b(?!.*francusk)|szarlotk|"
              r"czekolad|mus \b"),
    ("Przekąska", r"nuggets|chipsy|talarki|hash brown|przekaska|rolgeski|"
                  r"cheeseburgery na gryza|popcorn chicken|snack|frytki$"),
    ("Obiad", r".*"),
]
# skladniki, ktore wystepuja prawie wszedzie - nie swiadcza o podobienstwie
COMMON = {"sól", "pieprz", "czosnek", "cebula", "oliwa z oliwek", "olej roślinny",
          "masło", "woda", "papryka słodka", "czosnek granulowany", "cebula granulowana",
          "oregano", "sok z cytryny", "cukier", "natka pietruszki", "papryka wędzona",
          "chili", "płatki chilli", "kumin", "zioła włoskie", "sezam", "pieprz cayenne"}
NAME_STOP = {"z", "i", "w", "na", "do", "the", "and", "with", "for", "a", "od", "po",
             "domowe", "domowy", "prosty", "szybki", "easy", "high", "protein", "best",
             "wersja", "przepis", "moje", "moja", "danie"}


def category_of(name, ings):
    n = deacc(name)
    ing = {i.lower() for i in ings}
    if "płatki owsiane" in ing and not (ing & {"pierś z kurczaka", "kurczak",
                                                "mięso mielone wołowe", "wołowina"}):
        return "Śniadanie"
    for cat, pat in RULES:
        if re.search(pat, n):
            return cat
    return "Obiad"


def _tokens(name):
    return {w for w in re.findall(r"[a-z0-9]+", deacc(name))
            if len(w) > 2 and w not in NAME_STOP}


def _jac(a, b):
    return len(a & b) / len(a | b) if (a or b) else 0.0


def find_similar(recipes, ings_by_recipe):
    """recipes: lista dictow z 'name'. Zwraca {nazwa: [podobne nazwy]}."""
    toks = {r["name"]: _tokens(r["name"]) for r in recipes}
    core = {r["name"]: {i.lower() for i in ings_by_recipe.get(r["name"], [])} - COMMON
            for r in recipes}
    out = {}
    names = [r["name"] for r in recipes]
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            nj = _jac(toks[a], toks[b])
            ij = _jac(core[a], core[b])
            # duplikat: bardzo podobna nazwa ALBO niemal identyczny zestaw skladnikow
            if nj >= 0.6 or ij >= 0.62 or (nj >= 0.34 and ij >= 0.42):
                out.setdefault(a, []).append(b)
                out.setdefault(b, []).append(a)
    return out
