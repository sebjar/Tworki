# -*- coding: utf-8 -*-
"""Rozpiska przepisu do recznej weryfikacji: skladnik -> gramy -> kcal, sumy, porcje,
oraz zdania ze zrodla, w ktorych autor mowi o porcjach, sztukach albo kaloriach.
Uzycie: rozpisz.py P001 P002 ...  albo  rozpisz.py P001-P020"""
import io, json, re, sys
recs = {r["id"]: r for r in json.load(io.open("audit_kcal.json", encoding="utf-8"))}
ids = json.load(io.open("ids.json", encoding="utf-8"))
id2key = {v: k for k, v in ids.items()}
ci = {r["key"]: r for r in json.load(io.open("curate_input.json", encoding="utf-8"))}
parsed = json.load(io.open("parsed.json", encoding="utf-8"))
TY, ONA, UDZ = 2903, 1822, {"Śniadanie": .25, "Obiad": .35, "Kolacja": .30, "Zupa": .25,
                            "Sałatka": .30, "Przekąska": .12, "Deser": .12}
PAT = re.compile(r"(?i)[^.!\n]{0,80}(porcj|serv|makes|yield|sztuk|\bszt\b|pieces|portion|osob|"
                 r"kcal|calor|kalor|per (meal|serving|wrap|burrito|piece)|na \d+ |dla \d+)[^.!\n]{0,80}")


def wybierz(args):
    out = []
    for a in args:
        m = re.match(r"P(\d+)-P(\d+)$", a)
        if m:
            out += ["P%03d" % i for i in range(int(m.group(1)), int(m.group(2)) + 1)]
        else:
            out.append(a)
    return out


for pid in wybierz(sys.argv[1:]):
    r = recs.get(pid)
    if not r:
        continue
    key = id2key.get(pid, "?")
    src = ci.get(key, {})
    p = parsed.get(key, {})
    it = r["items"]
    tot = sum(x["kcal"] for x in it); g = sum(x["g"] for x in it); gc = sum(x["cooked"] for x in it)
    B = sum(x["B"] for x in it); T = sum(x["T"] for x in it); W = sum(x["W"] for x in it)
    s = r["serv"] or 0
    print("=" * 110)
    print("%s %s | %s | porcje %s | autor kcal/porcja: %s | %s" % (pid, r["name"], r["cat"], s,
                                                                  r["autor_kcal"], r["link"] or "plik"))
    if not it:
        print("   (bez skladnikow)")
        continue
    for x in sorted(it, key=lambda x: -x["kcal"]):
        if x["kcal"] < 1 and x["g"] < 30:
            continue
        print("   %-26s %7s %-9s = %6.0f g  %6.0f kcal (%2.0f%%)" % (
            x["ing"][:26], ("%g" % x["q"]), x["u"], x["g"], x["kcal"], 100 * x["kcal"] / tot if tot else 0))
    drob = [x["ing"] for x in it if x["kcal"] < 1 and x["g"] < 30]
    if drob:
        print("   + drobne:", ", ".join(drob))
    if s:
        udz = UDZ.get(r["cat"])
        y = ""
        if udz:
            y = " | dzień dla Was obojga: %.2f porcji (Ty %.0f, Ona %.0f kcal z garnka/dzień)" % (
                (TY + ONA) * udz / (tot / s), (TY + ONA) * udz * .6, (TY + ONA) * udz * .4)
        print("   RAZEM %.0f kcal (B %.0f T %.0f W %.0f) | surowe %.0f g, po ugotowaniu ~%.0f g | "
              "na porcję %.0f kcal, ~%.0f g%s" % (tot, B, T, W, g, gc, tot / s, gc / s, y))
    txt = " ".join(filter(None, [src.get("cap"), src.get("blog")]))
    zd = []
    for m in PAT.finditer(txt):
        z = re.sub(r"\s+", " ", m.group(0)).strip()
        if z not in zd:
            zd.append(z)
    for z in zd[:6]:
        print("   > ", z[:170])
    if p.get("servings") and p.get("sources") == ["plik"]:
        print("   > plik: porcje", p.get("servings"))
    if r["prep"].startswith("UWAGA"):
        print("   UWAGA:", r["prep"].split("\n")[0][7:260])
