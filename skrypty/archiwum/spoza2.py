# -*- coding: utf-8 -*-
"""Druga runda dla flag SPOZA: szuka produktu w tekscie zrodla po wszystkich synonimach
ze slownika normalizacji (takze angielskich). Wypisuje tylko to, czego nadal nie widac."""
import collections, io, re, subprocess, sys
import normalize as N
from normalize import deacc

SYN = collections.defaultdict(set)
for frag, canon, _s in N.CANON:
    SYN[canon].add(deacc(frag.lower()))
EXTRA = {
    "pierś z kurczaka": "chicken breast|chicken|kurczak|piers|filet", "udka z kurczaka": "thigh|udk|udz|chicken",
    "makaron": "pasta|noodle|vermicelli|spaghetti|makaron|macaroni", "makaron penne": "penne",
    "makaron rigatoni": "rigatoni", "makaron udon": "udon", "czosnek": "garlic|czosn",
    "dymka": "green onion|scallion|spring onion|dymk|szczypior", "ocet": "vinegar|ocet|octu",
    "cukier": "sugar|cukr|cukier", "cukier brązowy": "brown sugar", "mąka": "flour|mak",
    "jajko": "egg|jaj", "papryka czerwona": "bell pepper|papryk|pepper", "papryka zielona": "bell pepper|papryk|pepper",
    "pomidory z puszki": "tomato|pomidor", "ryż basmati": "basmati|rice", "ryż": "rice|ryz",
    "ryż jaśminowy": "jasmine", "kolendra ziarna": "coriander|kolendr", "kolendra": "cilantro|coriander|kolendr",
    "masło": "butter|masl|masel", "szalotka": "shallot|szalot", "wino białe": "white wine|wino|wina",
    "łosoś": "salmon|loso|losos", "ogórek": "cucumber|ogor", "serek śmietankowy": "cream cheese|serek",
    "sezam": "sesame|sezam", "soczewica": "lentil|soczew", "mięso mielone wołowe": "beef|wolow|mielon",
    "mięso mielone wieprzowe": "pork|wieprz|mielon", "mięso mielone z kurczaka": "chicken|kurczak|mielon",
    "cebula": "onion|cebul", "czerwona cebula": "red onion|cebul", "passata pomidorowa": "passata|tomato|pomidor",
    "bazylia": "basil|bazyli", "koncentrat pomidorowy": "tomato paste|koncentrat|przecier",
    "oliwki": "olive|oliwk", "pomidorki koktajlowe": "cherry|tomato|pomidor", "sałata": "lettuce|salat",
    "sałata lodowa": "lettuce|iceberg|salat", "pomidor": "tomato|pomidor", "imbir": "ginger|imbir",
    "natka pietruszki": "parsley|pietrusz|herb", "gałka muszkatołowa": "nutmeg|galk|muszkat",
    "sos sojowy jasny": "soy|soj", "pasta z papryki": "pepper paste|papryk", "papryka słodka": "paprika|papryk",
    "kumin": "cumin|kumin|kmin", "chili": "chili|chilli", "oregano": "oregano", "tymianek": "thyme|tymian",
    "zioła włoskie": "italian|wloskie|ziol", "bulion": "broth|stock|bulion|rosol", "śmietana kremówka": "cream|smietan|kremow",
    "czosnek granulowany": "garlic powder|granulowan|czosn", "cebula granulowana": "onion powder|granulowan|cebul",
    "koperek": "dill|koper", "szczypiorek": "chive|szczypior", "nachosy": "tortilla chip|nachos|chips",
    "jogurt grecki": "yogurt|yoghurt|jogurt", "skrobia kukurydziana": "corn starch|cornstarch|skrobi",
    "truskawki": "strawberr|truskaw|owoc|fruit", "czekolada gorzka": "chocolate|czekolad", "olej kokosowy": "coconut oil|kokos",
    "syrop klonowy": "maple|klonow", "borówki": "blueberr|borowk", "piwo": "beer|piw", "ryba biała": "cod|fish|haddock|ryb",
    "ziemniaki": "potato|ziemniak", "orzechy nerkowca": "cashew|nerkowc", "mozzarella": "mozzarella|cheese",
    "bułka tarta": "breadcrumb|panko|tart", "płatki chilli": "chili flake|red pepper flake|chilli flake|platki",
    "przyprawa taco": "taco seasoning|taco", "mąka chlebowa": "bread flour|chlebow", "mąka tortowa": "cake flour|tortow",
    "drożdże instant": "yeast|drozdz", "woda gazowana": "sparkling|soda water|gazowan", "papryka wędzona": "smoked paprika|wedzon",
}
for k, v in EXTRA.items():
    SYN[k].update(v.split("|"))

wyn = subprocess.run([sys.executable, "-c", "import zrodlo"], capture_output=True, text=True,
                     encoding="utf-8").stdout  # zrodlo drukuje przy imporcie
import zrodlo as Z  # noqa: E402  (wyniki i tekst zrodla)
zostaje = 0
for idx, lst in Z.wyniki.items():
    txt = deacc(Z.tekst_zrodla(idx).lower()) + " " + deacc((Z.CUR[idx].get("note") or "").lower())
    brak = [op for typ, op in lst if typ == "SPOZA" and not any(s and s in txt for s in SYN.get(op, ()))]
    if brak:
        zostaje += len(brak)
        print("C[%d] %-45s | %s" % (idx, Z.CUR[idx]["name"][:45], ", ".join(brak)))
print("zostaje do recznego sprawdzenia:", zostaje)
