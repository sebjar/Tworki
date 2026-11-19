# -*- coding: utf-8 -*-
"""Sprawdza, czy opis przygotowania pasuje do przepisu i jego skladnikow."""
import collections, os, re, sys, unicodedata
import openpyxl

def bez_id(s):
    """Arkusz Skladniki trzyma "P001: Nazwa" - do porownan potrzebna sama nazwa."""
    return re.sub(r"^P\d{3}:\s*", "", s) if isinstance(s, str) else s


SP = os.path.dirname(os.path.abspath(__file__))
# Makra sa teraz formulami, a openpyxl ich nie liczy - czytamy kopie przeliczona
# przez LibreOffice. przelicz() odswieza ja przy kazdym uruchomieniu.
from przelicz import przelicz
P = przelicz()


def deacc(s):
    s = (s or "").replace("ł", "l").replace("Ł", "L")
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


def stem(w):
    return re.sub(r"[aeiouy]$", "", w) if len(w) > 4 else w


# przyprawy i drobiazgi, ktorych autor czesto nie wymienia w krokach
SKIP = {"sól", "pieprz", "woda", "olej roślinny", "oliwa z oliwek", "cukier",
        "sos ostry", "zioła włoskie", "papryka słodka", "papryka ostra",
        "pieprz cayenne", "płatki chilli", "chili", "oregano", "kumin", "kurkuma",
        "cynamon", "majeranek", "tymianek", "rozmaryn", "sumak", "lubczyk",
        "gałka muszkatołowa", "curry", "garam masala", "biały pieprz",
        "cebula granulowana", "czosnek granulowany", "papryka wędzona",
        "pieprz cytrynowy", "pieprz czosnkowy", "sezam", "bazylia", "kolendra",
        "natka pietruszki", "koperek", "szczypiorek", "wanilia", "soda oczyszczona",
        "proszek do pieczenia", "świeże zioła", "papryka mielona"}

NOISE = re.compile(r"(?i)(obserwuj|zapisz na p|link in bio|w bio|komentarz|follow|"
                   r"subscribe|zaobserwuj|moja aplikacj|apce|luncher|sklep|"
                   r"kod rabatow|wsp[oó][lł]praca|reklama|#\w+|zapraszam|"
                   r"daj znac|dajcie znac|smacznego!?$)")

wb = openpyxl.load_workbook(P, data_only=True)   # czytamy WARTOSCI, nie formuly
wp, ws = wb["Przepisy"], wb["Składniki"]

ing = collections.defaultdict(list)
for r in range(2, ws.max_row + 1):
    a, b = bez_id(ws.cell(row=r, column=1).value), ws.cell(row=r, column=2).value
    if a and b:
        ing[a].append(b)

problems = collections.OrderedDict()


def add(k, v):
    problems.setdefault(k, []).append(v)


rows = []
for r in range(2, wp.max_row + 1):
    n = wp.cell(row=r, column=2).value
    if not n:
        continue
    steps = wp.cell(row=r, column=10).value or ""
    qual = wp.cell(row=r, column=9).value
    rows.append((r, n, qual, steps))

for r, n, qual, steps in rows:
    body = re.sub(r"^UWAGA:.*?\n\n", "", steps, flags=re.S)
    if not body.strip():
        continue
    nsteps = len([l for l in body.split("\n") if l.strip()])
    d = deacc(body)
    words = {stem(w) for w in re.findall(r"[a-z0-9]+", d)}

    # ile skladnikow (poza przyprawami) pojawia sie w krokach
    core = [i for i in set(ing.get(n, [])) if i not in SKIP]
    hit = 0
    missing = []
    for i in core:
        toks = [stem(w) for w in re.findall(r"[a-z0-9]+", deacc(i)) if len(w) > 2]
        if toks and any(t in words or any(w.startswith(t) for w in words) for t in toks):
            hit += 1
        else:
            missing.append(i)
    cov = hit / len(core) if core else 1.0

    if core and cov < 0.34:
        add("Kroki prawie nie wspominają składników (możliwy inny przepis)",
            "%-46s pokrycie %.0f%% (%d/%d) [%s]" % (n[:46], cov * 100, hit, len(core), qual))
    elif core and cov < 0.6:
        add("Niskie pokrycie składników w krokach",
            "%-46s %.0f%% — brak: %s" % (n[:46], cov * 100, ", ".join(missing[:5])))

    if NOISE.search(body):
        m = NOISE.search(body)
        add("Marketing/hashtagi zamiast instrukcji",
            "%-40s ...%s..." % (n[:40], body[max(0, m.start() - 30):m.start() + 40]
                                .replace("\n", " ")))
    if nsteps <= 2 and len(core) >= 5:
        add("Bardzo mało kroków jak na liczbę składników",
            "%-46s %d kroków, %d składników" % (n[:46], nsteps, len(core)))
    if re.search(r"[a-ząćęłńóśźż,]\s*$", body.strip()) and nsteps > 1:
        add("Ostatni krok wygląda na urwany", "%-46s ...%s" % (n[:46], body.strip()[-60:]))

print("Przepisow z opisem przygotowania: %d\n" % sum(1 for _, _, _, s in rows if s.strip()))
for k, v in problems.items():
    print("### %s — %d" % (k, len(v)))
    for x in v[:14]:
        print("     ", x)
    if len(v) > 14:
        print("      ... i %d wiecej" % (len(v) - 14))
    print()
if not problems:
    print("Brak zastrzezen.")
