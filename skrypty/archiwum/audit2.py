# -*- coding: utf-8 -*-
"""Drugi audyt - inne katy niz sanity.py. Szuka rzeczy, ktore przechodza testy,
ale czlowiek patrzac na nie powie 'to jakas glupota'."""
import collections, os, re, sys
import openpyxl

SP = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SP)
from nutrition import grams, macros, NUTR

# Makra sa teraz formulami, a openpyxl ich nie liczy - czytamy kopie przeliczona
# przez LibreOffice. przelicz() odswieza ja przy kazdym uruchomieniu.
from przelicz import przelicz
P = przelicz()


def bez_id(s):
    return re.sub(r"^P\d{3}:\s*", "", s) if isinstance(s, str) else s


def deacc(s):
    s = (s or "").replace("ł", "l").replace("Ł", "L")
    import unicodedata
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


wb = openpyxl.load_workbook(P, data_only=True)   # czytamy WARTOSCI, nie formuly
wp, ws, wl = wb["Przepisy"], wb["Składniki"], wb["Lista zakupów"]

rec = {}
for r in range(2, wp.max_row + 1):
    n = wp.cell(row=r, column=2).value
    if not n:
        continue
    rec[n] = dict(
        id="P%03d" % (r - 1), row=r, cat=wp.cell(row=r, column=3).value,
        plat=wp.cell(row=r, column=4).value, autor=wp.cell(row=r, column=5).value,
        link=wp.cell(row=r, column=6).value, serv=wp.cell(row=r, column=7).value,
        ning=wp.cell(row=r, column=8).value or 0,
        steps=wp.cell(row=r, column=10).value or "",
        sim=wp.cell(row=r, column=11).value or "",
        kcal=wp.cell(row=r, column=12).value, B=wp.cell(row=r, column=13).value,
        T=wp.cell(row=r, column=14).value, W=wp.cell(row=r, column=15).value,
        aK=wp.cell(row=r, column=16).value, msrc=wp.cell(row=r, column=20).value or "")

ing = collections.defaultdict(list)
for r in range(2, ws.max_row + 1):
    a, b, q, u, sek, orig = (ws.cell(row=r, column=i).value for i in (1, 2, 3, 4, 5, 6))
    if a and b:
        ing[bez_id(a)].append(dict(ing=b, qty=q, unit=u, sek=sek, orig=orig, row=r))

OUT = collections.OrderedDict()


def add(k, v):
    OUT.setdefault(k, []).append(v)


# ---------------------------------------------------------------- 1. nazwy
for n, v in rec.items():
    if re.search(r"#\w|@\w|\bhttp|👉|✅|\.{3}$|^\W|\s{2,}", n):
        add("Nazwa ze śmieciem (hashtag, link, emoji, urwanie)", "%s %s" % (v["id"], n))
    if len(n) < 6:
        add("Nazwa bardzo krótka", "%s %s" % (v["id"], n))

# duplikaty nazw po deakcentowaniu i bez liczby w nawiasie
byslug = collections.defaultdict(list)
for n, v in rec.items():
    byslug[re.sub(r"\s*\(\d+\)$", "", deacc(n))].append((v["id"], n))
for k, lst in byslug.items():
    if len(lst) > 1:
        add("Dwa przepisy o tej samej nazwie", " | ".join("%s %s" % x for x in lst))

# ---------------------------------------------------------------- 2. linki
links = collections.Counter((v["link"] or "").split("?")[0] for v in rec.values() if v["link"])
for l, c in links.items():
    if c > 1:
        who = [v["id"] for v in rec.values() if (v["link"] or "").split("?")[0] == l]
        add("Ten sam link w kilku przepisach", "%s -> %s" % (l[-46:], who))
for n, v in rec.items():
    if not v["link"]:
        add("Przepis bez linku", "%s %s" % (v["id"], n))
    elif not re.match(r"https?://", v["link"]):
        add("Link nie jest adresem", "%s %s" % (v["id"], v["link"][:50]))

# autor kontra link
for n, v in rec.items():
    m = re.search(r"(?:tiktok\.com/@|instagram\.com/)([\w.]+)", v["link"] or "")
    if m and v["autor"] and deacc(m.group(1)) != deacc(v["autor"]):
        add("Autor nie zgadza się z linkiem",
            "%s %-30s autor=%-18s link=%s" % (v["id"], n[:30], v["autor"], m.group(1)))

# ---------------------------------------------------------------- 3. ilosci na porcje
# ile jednego skladnika przypada na jedna porcje - szukamy absurdow
LIMIT_NA_PORCJE = {           # gramy na jedna porcje, powyzej ktorych to bez sensu
    "sól": 12, "cukier": 90, "pieprz": 6, "czosnek": 30, "masło": 90, "oliwa z oliwek": 45,
    "olej roślinny": 45, "ocet": 60, "sos sojowy": 60, "miód": 60, "chili": 8,
    "papryka słodka": 10, "imbir": 25, "koncentrat pomidorowy": 60, "sezam": 20,
    "parmezan": 80, "ser żółty": 120, "mozzarella": 150, "śmietana kremówka": 200,
    "makaron": 160, "ryż": 140, "mąka": 200, "jajko": 180,
}
for n, items in ing.items():
    s = rec[n]["serv"] or 1
    for it in items:
        if not isinstance(it["qty"], (int, float)):
            continue
        g = grams(it["ing"], it["unit"], it["qty"]) / s
        lim = LIMIT_NA_PORCJE.get(it["ing"])
        if lim and g > lim:
            add("Absurdalna ilość na porcję",
                "%s %-34s %g %s %s = %.0f g/porcję (próg %d)"
                % (rec[n]["id"], n[:34], it["qty"], it["unit"], it["ing"], g, lim))

# ---------------------------------------------------------------- 4. makra: skrajnosci
for n, v in rec.items():
    if not isinstance(v["kcal"], (int, float)) or not v["kcal"]:
        continue
    B, T, W = v["B"] or 0, v["T"] or 0, v["W"] or 0
    if T * 9 / v["kcal"] > 0.75 and v["cat"] not in ("Sos / dodatek",):
        add("Ponad 75% kalorii z tłuszczu", "%s %-40s %s kcal, T=%s" % (v["id"], n[:40], v["kcal"], T))
    if B * 4 / v["kcal"] > 0.65:
        add("Ponad 65% kalorii z białka", "%s %-40s %s kcal, B=%s" % (v["id"], n[:40], v["kcal"], B))
    if B < 3 and v["cat"] in ("Obiad", "Kolacja"):
        add("Danie główne prawie bez białka", "%s %-40s B=%s g" % (v["id"], n[:40], B))

# ---------------------------------------------------------------- 5. kroki
for n, v in rec.items():
    s = v["steps"]
    if not s:
        continue
    body = re.sub(r"^UWAGA:.*?\n\n", "", s, flags=re.S)
    kroki = [x for x in body.split("\n") if x.strip()]
    for k in kroki:
        t = re.sub(r"^\d+\.\s*", "", k)
        if len(t) < 12:
            add("Krok prawie pusty", "%s %-34s „%s”" % (v["id"], n[:34], t))
        if re.search(r"#\w{3,}|@[\w.]{3,}|link w bio|zapisz sobie|obserwuj", t, re.I):
            add("Krok to marketing, nie instrukcja", "%s %-30s „%s”" % (v["id"], n[:30], t[:60]))
        if re.search(r"[a-ząćęłńóśżź],$|\bi$|\bz$|\bna$", t.strip()):
            add("Krok urwany w pół zdania", "%s %-30s „…%s”" % (v["id"], n[:30], t[-45:]))
    if len(kroki) == 1 and v["ning"] > 5:
        add("Jeden krok na wiele składników", "%s %-40s %d składników" % (v["id"], n[:40], v["ning"]))

# ---------------------------------------------------------------- 6. dzialy sklepu
DZIAL_OK = {
    "Warzywa i owoce": r"warzyw|owoc|sałat|zioł|śwież",
    "Mięso i ryby": r"mięs|ryb|kurcz|woł|wieprz|łoso|krewet",
    "Nabiał i jaja": r"ser|mlek|jaj|jogurt|śmieta|masł",
}
podejrzane = {
    ("cukier", "Sypkie i makarony"), ("sól", "Przyprawy i zioła"),
}
sek = {}
for items in ing.values():
    for it in items:
        sek.setdefault(it["ing"], set()).add(it["sek"])
for k, v in sek.items():
    if len(v) > 1:
        add("Ten sam składnik w dwóch działach sklepu", "%-30s %s" % (k, sorted(v)))

# ---------------------------------------------------------------- 7. oryginalny zapis
for n, items in ing.items():
    for it in items:
        o = (it["orig"] or "").strip()
        if not o:
            continue
        if re.search(r"kcal|makro|protein|białk\w*\s*:|http|#\w", o, re.I):
            add("„Oryginalny zapis” to nie składnik",
                "%s %-26s %-18s ← „%s”" % (rec[n]["id"], n[:26], it["ing"][:18], o[:40]))

# ---------------------------------------------------------------- 8. podobienstwa
par = set()
for n, v in rec.items():
    for cel in [x.strip() for x in v["sim"].split(",") if x.strip()]:
        cid = cel[:4]
        par.add(tuple(sorted([v["id"], cid])))
brak_zwrotny = []
for a, b in par:
    ra = next((v for v in rec.values() if v["id"] == a), None)
    rb = next((v for v in rec.values() if v["id"] == b), None)
    if ra and rb and (b not in ra["sim"] or a not in rb["sim"]):
        brak_zwrotny.append((a, b))
if brak_zwrotny:
    add("Podobieństwo tylko w jedną stronę", str(brak_zwrotny[:6]))

# przepisy o niemal identycznym zestawie skladnikow, ktore NIE sa oznaczone
sets = {n: {i["ing"] for i in items} for n, items in ing.items() if len(items) >= 4}
POSPOLITE = {"sól", "pieprz", "czosnek", "oliwa z oliwek", "olej roślinny", "cebula",
             "masło", "woda", "cukier", "papryka słodka"}
names = list(sets)
for i in range(len(names)):
    for j in range(i + 1, len(names)):
        a, b = names[i], names[j]
        sa, sb = sets[a] - POSPOLITE, sets[b] - POSPOLITE
        if not sa or not sb:
            continue
        jac = len(sa & sb) / len(sa | sb)
        if jac >= 0.7 and rec[b]["id"] not in rec[a]["sim"]:
            add("Prawie te same składniki, a nie oznaczone jako podobne",
                "%s %-30s ~ %s %-30s (%.0f%%)" % (rec[a]["id"], a[:30], rec[b]["id"], b[:30], jac * 100))

# ---------------------------------------------------------------- raport
print("Przepisów: %d | wierszy składników: %d\n" % (len(rec), sum(len(v) for v in ing.values())))
if not OUT:
    print("Nic nie znalazłem.")
for k, v in OUT.items():
    print("### %s — %d" % (k, len(v)))
    for x in v[:12]:
        print("     ", x)
    if len(v) > 12:
        print("      ... i %d więcej" % (len(v) - 12))
    print()
