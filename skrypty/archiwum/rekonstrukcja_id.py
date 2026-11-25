# -*- coding: utf-8 -*-
"""Odtwarza numery ID z wersji arkusza z 15.09.2026 (ostatnia wyslana przed przegladem
z pazdziernika). Wtedy ID = pozycja po sortowaniu (jakosc, -liczba skladnikow, nazwa)."""
import glob, importlib.util, io, json, os, re, sys
SP = os.path.dirname(os.path.abspath(__file__))
os.chdir(SP)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


norm = load("normalize_stary.py", "normalize_wrzesien").normalize
JEDNOSTKI = ["g", "kg", "ml", "l", "dag", "szt.", "łyżka", "łyżeczka", "szklanka", "ząbek",
             "puszka", "opak.", "garść", "szczypta", "plaster", "pęczek", "główka", "oz", "lbs"]
CUR = {}
for p in sorted(glob.glob("curated_*.py")):
    base = os.path.basename(p)
    if base == "curated_14.py":
        continue
    alt = os.path.join("kopie", base[:-3] + "_przed_weryf.py")
    CUR.update(load(alt if os.path.exists(alt) else p, base[:-3] + "_wrzesien").C)
rows_in = json.load(io.open("curate_input_przed_pazdziernik.json", encoding="utf-8"))
idx2key = {i: r["key"] for i, r in enumerate(rows_in)}
cur_by_key = {idx2key[i]: e for i, e in CUR.items() if i in idx2key}
data = json.load(io.open("parsed_przed_pazdziernik.json", encoding="utf-8"))

used, recs = {}, []
for key, r in data.items():
    p, cur = r["parsed"], cur_by_key.get(key)
    name = (cur["name"] if cur else (r["name"] or p["name"] or "")).strip()
    if not name:
        name = "Bez nazwy (@%s)" % (r["author"] or "?")
    name = re.sub(r"\s+", " ", name)[:70]
    n = used.get(name.lower(), 0) + 1
    used[name.lower()] = n
    if n > 1:
        name = "%s (%d)" % (name, n)
    if not cur:
        sys.exit("brak opracowania dla %s - rekonstrukcja niepewna" % key)
    merged = set()
    for qty, unit, ing in cur["ings"]:
        canon = norm(ing)[0]
        if canon:
            merged.add((canon, unit if unit in JEDNOSTKI else "szt."))
    recs.append((key, name, len(merged)))
recs.sort(key=lambda x: (-x[2], x[1].lower()))
ids = {key: "P%03d" % (i + 1) for i, (key, name, n) in enumerate(recs)}
json.dump({"_zrodlo": "wersja z 15.09.2026", "ids": ids,
           "nazwy": {key: name for key, name, n in recs}},
          io.open("ids_wrzesien.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("przepisow:", len(recs))
for key, name, n in recs:
    print(ids[key], n, name[:50])
