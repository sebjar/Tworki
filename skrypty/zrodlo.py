# -*- coding: utf-8 -*-
"""Weryfikacja kazdego przepisu wzgledem zrodla.

Dla kazdego recznie opracowanego przepisu porownuje moja liste skladnikow z:
  * lista rozparsowana z opisu pod filmem (parsed.ings), z pliku jedzenie.xlsx (file_ings),
  * surowym tekstem opisu, napisow i bloga - zeby wykryc produkt, ktory jest w zrodle,
    a ktorego nie ma u mnie, i odwrotnie.
Wypisuje tylko podejrzane miejsca - reszte uznaje za zgodna."""
import collections, glob, importlib.util, io, json, os, re, sys, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from normalize import normalize, deacc
from nutrition import grams

CUR, SRC_FILE = {}, {}
for p in sorted(glob.glob("curated_*.py")):
    spec = importlib.util.spec_from_file_location(os.path.basename(p)[:-3], p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    for k in m.C:
        SRC_FILE[k] = os.path.basename(p)
    CUR.update(m.C)
ci = json.load(io.open("curate_input.json", encoding="utf-8"))
parsed = json.load(io.open("parsed.json", encoding="utf-8"))
tr_all = json.load(io.open("tt_transcripts.json", encoding="utf-8"))

# produkty, ktorych nie warto gonic - pojawiaja sie w zrodlach jako ozdobniki
POMIJAJ = {"sól", "pieprz", "woda", "olej roślinny", "oliwa z oliwek"}

wyniki = collections.OrderedDict()


def dodaj(idx, typ, opis):
    wyniki.setdefault(idx, []).append((typ, opis))


def tekst_zrodla(idx):
    r = ci[idx]
    t = " ".join(filter(None, [r.get("cap") or "", r.get("tr") or "", r.get("blog") or ""]))
    key = r["key"]
    if key.startswith("tt:"):
        tid = key[3:].split("#")[0]
        for k, v in (tr_all.items() if isinstance(tr_all, dict) else []):
            if tid in k:
                t += " " + (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False))
    return t


def kanon_z_tekstu(t):
    """Produkty kanoniczne, ktore pojawiaja sie w tekscie. Tniemy tekst na krotkie
    kawalki (po przecinkach, myslnikach, nowych liniach) i normalizujemy kazdy."""
    out = set()
    for frag in re.split(r"[\n,;•·\-–—\|/]+|\s{2,}|(?<=[a-ząćęłńóśżź])\.\s", t):
        frag = re.sub(r"^\s*[\d.,½¼¾/]+\s*(g|kg|ml|l|szt\.?|łyż\w*|tbsp|tsp|cups?|szklank\w*|ząb\w*)?\s*",
                      "", frag.strip(), flags=re.I)
        if 2 < len(frag) < 60:
            c, s, k = normalize(frag)
            if c and k:
                out.add(c)
    return out


for idx, e in sorted(CUR.items()):
    if idx >= len(ci) or not e.get("ings"):
        continue
    key = ci[idx]["key"]
    if key not in parsed:            # przepis usuniety przez uzytkownika
        continue
    moje = collections.defaultdict(float)
    moje_jedn = {}
    for q, u, ing in e["ings"]:
        c = normalize(ing)[0]
        if c:
            moje[c] += grams(c, u, q)
            moje_jedn[c] = (q, u)
    note = (e.get("note") or "").lower()

    # --- 1. rozparsowana lista zrodlowa (najpewniejsza)
    src = collections.defaultdict(float)
    r = parsed[key]
    lista = (r.get("file_ings") or []) + (r["parsed"].get("ings") or []) + (r.get("site_ings") or [])
    for it in lista:
        if not isinstance(it, dict):
            continue
        c, s, k = normalize(it.get("ing") or "")
        if not c or not k:
            continue
        q, u = it.get("qty"), it.get("unit")
        if isinstance(q, (int, float)) and u in ("g", "kg", "ml", "l", "dag"):
            src[c] = max(src[c], grams(c, u, q))
        else:
            src.setdefault(c, 0.0)

    # --- 2. produkty wspomniane gdziekolwiek w tekscie zrodla
    txt = tekst_zrodla(idx)
    w_tekscie = kanon_z_tekstu(txt) if txt.strip() else set()

    for c, g in src.items():
        if c in POMIJAJ:
            continue
        if c not in moje:
            # moze to ten sam produkt pod inna nazwa (np. "kurczak" vs "pierś z kurczaka")
            pokrewne = [m for m in moje if c.split()[0][:5] in m or m.split()[0][:5] in c]
            if not pokrewne:
                dodaj(idx, "BRAK", "%s (w źródle%s)" % (c, ", %.0f g" % g if g else ""))
        elif g and moje[c]:
            ratio = moje[c] / g
            if ratio < 0.6 or ratio > 1.7:
                dodaj(idx, "ILOSC", "%s: u mnie %.0f g, w źródle %.0f g" % (c, moje[c], g))

    if w_tekscie and len(txt) > 120:
        for c in moje:
            if c in POMIJAJ or c in src or c in w_tekscie:
                continue
            slowo = deacc(c.split()[0])[:5]
            if slowo and slowo in deacc(txt):
                continue
            if deacc(c)[:5] in deacc(note) or "oszacow" in note or "dopisa" in note:
                continue
            dodaj(idx, "SPOZA", c)

print("Sprawdzone przepisy: %d" % sum(1 for i, e in CUR.items()
                                     if i < len(ci) and e.get("ings") and ci[i]["key"] in parsed))
print("Z uwagami: %d\n" % len(wyniki))
for idx, lst in wyniki.items():
    e = CUR[idx]
    print("C[%d] %s (%s, %s porc.)" % (idx, e["name"][:58], SRC_FILE[idx], e["serv"]))
    for typ, op in lst:
        print("     %-6s %s" % (typ, op))
