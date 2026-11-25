# -*- coding: utf-8 -*-
import glob, importlib.util, io, json, os, re, sys
sys.path.insert(0, ".")
CUR = {}
for p in sorted(glob.glob("curated_*.py")):
    spec = importlib.util.spec_from_file_location(os.path.basename(p)[:-3], p)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    CUR.update(m.C)
ci = json.load(io.open("curate_input.json", encoding="utf-8"))
parsed = json.load(io.open("parsed.json", encoding="utf-8"))
for a in sys.argv[1:]:
    idx, slowa = a.split(":")[0], a.split(":")[1:] if ":" in a else []
    idx = int(idx)
    e, r = CUR[idx], ci[idx]
    pr = parsed.get(r["key"], {})
    print("=" * 100)
    print("C[%d] %s | porcje %s | %s" % (idx, e["name"], e["serv"], r.get("link")))
    print("MOJE: " + "; ".join("%g %s %s" % t for t in e["ings"]))
    lista = (pr.get("file_ings") or []) + (pr.get("parsed", {}).get("ings") or [])
    if lista:
        print("ZRODLO-LISTA: " + "; ".join((i.get("raw") or "%s %s %s" % (i.get("qty"), i.get("unit"), i.get("ing")))
                                         for i in lista if isinstance(i, dict))[:900])
    tekst = " ".join(filter(None, [r.get("cap") or "", r.get("tr") or ""]))
    for w in slowa:
        for m in list(re.finditer(w, tekst, re.I))[:2]:
            print("   [%s] ...%s..." % (w, tekst[max(0, m.start() - 90):m.end() + 90].replace("\n", " ")))
    if e.get("note"):
        print("UWAGA: " + e["note"][:300])
