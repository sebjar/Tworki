# -*- coding: utf-8 -*-
"""Weryfikacja liczby porcji: co napisal autor kontra co mam w arkuszu."""
import collections, io, json, re, sys
import openpyxl
sys.path.insert(0, ".")
from nutrition import grams

# Makra sa teraz formulami, a openpyxl ich nie liczy - czytamy kopie przeliczona
# przez LibreOffice. przelicz() odswieza ja przy kazdym uruchomieniu.
from przelicz import przelicz
P = przelicz()

# wzorce, w ktorych autor deklaruje wydajnosc przepisu
WZORCE = [
    (re.compile(r"(?i)\bserves?\s*(\d{1,2})\b"), "serves N"),
    (re.compile(r"(?i)\bmakes?\s*(\d{1,2})\b"), "makes N"),
    (re.compile(r"(?i)\(\s*makes\s*(\d{1,2})\s*\)"), "(makes N)"),
    (re.compile(r"(?i)\b(\d{1,2})\s*servings?\b"), "N servings"),
    (re.compile(r"(?i)servings?\s*:?\s*(?:approx\.?\s*)?(\d{1,2})"), "servings: N"),
    (re.compile(r"(?i)per\s+serve\s*\(\s*(\d{1,2})\s*total\s*\)"), "per serve (N total)"),
    (re.compile(r"(?i)\byields?\s*:?\s*(\d{1,2})"), "yields N"),
    (re.compile(r"(?i)recipe\s+makes\s*(\d{1,2})"), "recipe makes N"),
    (re.compile(r"(?i)\bna\s+(\d{1,2})\s+porcj"), "na N porcji"),
    (re.compile(r"(?i)wychodz\w*\s+(\d{1,2})\s+porcj"), "wychodzi N porcji"),
    (re.compile(r"(?i)(\d{1,2})\s+porcj\w*\b"), "N porcji"),
    (re.compile(r"(?i)\bna\s+(?:ok\.?\s*)?(\d{1,2})\s+(?:tortill|wrap|burrit|kanapk|plack|sztuk)"),
     "na N sztuk"),
    (re.compile(r"(?i)\bna\s+(\d{1,2})\s+(?:osob|dni)"), "na N osób/dni"),
    (re.compile(r"(?i)this\s+recipe\s+serves\s*(\d{1,2})"), "recipe serves N"),
]
# konteksty, w ktorych liczba NIE jest liczba porcji
PULAPKI = re.compile(r"(?i)(minut|min\b|godzin|stopni|°C|kcal|gram|\bg\b|ml\b|%|"
                     r"dni w lodówce|days|hours|minutes)")

wb = openpyxl.load_workbook(P, data_only=True)   # czytamy WARTOSCI, nie formuly
wp, ws = wb["Przepisy"], wb["Składniki"]

rec = {}
for r in range(2, wp.max_row + 1):
    n = wp.cell(row=r, column=2).value
    if n:
        rec["P%03d" % (r - 1)] = dict(
            n=n, link=(wp.cell(row=r, column=6).value or "").split("?")[0],
            serv=wp.cell(row=r, column=7).value, kcal=wp.cell(row=r, column=12).value,
            aK=wp.cell(row=r, column=16).value, cat=wp.cell(row=r, column=3).value,
            note=wp.cell(row=r, column=10).value or "")
ing = collections.defaultdict(list)
for r in range(2, ws.max_row + 1):
    a, b, q, u = (ws.cell(row=r, column=i).value for i in (1, 2, 3, 4))
    if a and b and isinstance(q, (int, float)):
        ing[a[:4]].append((b, q, u))

rows = json.load(io.open("curate_input.json", encoding="utf-8"))
cap_po_linku = {}
for r in rows:
    if r.get("link"):
        cap_po_linku[r["link"].split("?")[0]] = " ".join(
            filter(None, [r.get("cap"), r.get("tr") or "", r.get("blog") or ""]))

OUT = collections.OrderedDict()


def add(k, v):
    OUT.setdefault(k, []).append(v)


zgodne = niezgodne = brak = 0
for pid, v in sorted(rec.items()):
    cap = cap_po_linku.get(v["link"], "")
    kandydaci = []
    for rx, opis in WZORCE:
        for m in rx.finditer(cap):
            win = cap[max(0, m.start() - 40):m.end() + 40]
            if PULAPKI.search(cap[m.end():m.end() + 12]):
                continue
            n = int(m.group(1))
            if 1 <= n <= 24:
                kandydaci.append((n, opis, win.strip()[:80]))
    if not kandydaci:
        brak += 1
        continue
    licz = collections.Counter(n for n, _o, _w in kandydaci)
    naj, ile = licz.most_common(1)[0]
    if abs((v["serv"] or 0) - naj) < 0.01:
        zgodne += 1
    else:
        niezgodne += 1
        opis = [k for k in kandydaci if k[0] == naj][0]
        add("Autor deklaruje inną liczbę porcji niż mam w arkuszu",
            "%s %-40s arkusz=%-4s autor=%-3s [%s] „%s”"
            % (pid, v["n"][:40], v["serv"], naj, opis[1], opis[2]))

# --- masa porcji: sprawdzenie od drugiej strony
for pid, v in rec.items():
    items = ing.get(pid)
    if not items or not v["serv"]:
        continue
    tot = sum(grams(b, u, q) for b, q, u in items)
    per = tot / v["serv"]
    if v["cat"] in ("Sos / dodatek", "Napój", "Deser", "Przekąska"):
        lo, hi = 30, 500
    elif v["cat"] == "Sałatka":
        lo, hi = 150, 900
    else:
        lo, hi = 200, 900
    if per < lo:
        add("Porcja za lekka jak na tę kategorię",
            "%s %-42s %.0f g/porcję (%d porcji) [%s]" % (pid, v["n"][:42], per, v["serv"], v["cat"]))
    elif per > hi:
        add("Porcja za ciężka jak na tę kategorię",
            "%s %-42s %.0f g/porcję (%d porcji) [%s]" % (pid, v["n"][:42], per, v["serv"], v["cat"]))

# --- porcje = 2 (moja wartosc domyslna) przy duzej ilosci jedzenia
for pid, v in rec.items():
    items = ing.get(pid)
    if not items or v["serv"] != 2:
        continue
    tot = sum(grams(b, u, q) for b, q, u in items)
    if tot > 1600:
        add("Ustawione 2 porcje, a jedzenia na więcej",
            "%s %-42s %.0f g łącznie = %.0f g/porcję" % (pid, v["n"][:42], tot, tot / 2))

# --- makra autora vs moje: rozjazd bliski wielokrotnosci liczby porcji
for pid, v in rec.items():
    if not v["aK"] or not v["kcal"] or not v["serv"]:
        continue
    il = v["kcal"] / v["aK"]
    for k in (v["serv"], 2, 3, 4):
        if k > 1 and abs(il - k) / k < 0.12:
            add("Rozjazd z autorem prawie dokładnie ×N — podejrzenie złej liczby porcji",
                "%s %-40s moje %s / autor %s = %.2f (×%g?) porcji=%s"
                % (pid, v["n"][:40], v["kcal"], v["aK"], il, k, v["serv"]))
            break

print("PORCJE KONTRA DEKLARACJA AUTORA")
print("   zgodnych: %d | niezgodnych: %d | autor nic nie podał: %d\n" % (zgodne, niezgodne, brak))
for k, val in OUT.items():
    print("### %s — %d" % (k, len(val)))
    for x in val[:16]:
        print("     ", x)
    if len(val) > 16:
        print("      ... i %d więcej" % (len(val) - 16))
    print()
