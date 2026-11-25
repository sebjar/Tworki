# -*- coding: utf-8 -*-
"""Rozpisuje kazdy przepis skladnik po skladniku: ilosc -> gramy -> kcal, tak jak liczy arkusz.
Czyta wspolczynniki wprost z formul w Skladnikach (=$C*wspolczynnik)."""
import collections, io, json, os, re
import openpyxl
from przelicz import SRC

S = os.path.dirname(os.path.abspath(__file__))
wf = openpyxl.load_workbook(SRC)
sk, pr = wf["Składniki"], wf["Przepisy"]


def fac(v, q=None):
    """Wspolczynnik na jednostke (ilosc z kolumny C razy wspolczynnik). Formula oleju
    =IF($C*g>=150,$C*a,$C*b) (wchlanianie przy smazeniu w glebokim tluszczu) liczona wprost."""
    if v is None:
        return 0.0
    if isinstance(v, str):
        m = re.match(r"=\$[A-Z]\d+\*([\d.Ee+-]+)$", v)
        if m:
            return float(m.group(1))
        m = re.match(r"=IF\(\$C\d+\*([\d.]+)>=([\d.]+),\$C\d+\*([\d.]+),\$C\d+\*([\d.]+)\)$", v)
        if m and q is not None:
            g, prog, a, b = map(float, m.groups())
            return a if q * g >= prog else b
        raise ValueError("nieznana formula: %s" % v)
    return float(v)


rows = collections.defaultdict(list)
for r in range(2, sk.max_row + 1):
    key = sk.cell(row=r, column=1).value
    if not key:
        continue
    q, u = sk.cell(row=r, column=3).value, sk.cell(row=r, column=4).value
    g, k = fac(sk.cell(row=r, column=9).value), fac(sk.cell(row=r, column=12).value, q)
    b, t, w = (fac(sk.cell(row=r, column=c).value, q) for c in (13, 14, 15))
    cooked = fac(sk.cell(row=r, column=18).value, q)
    rows[key.split(":")[0]].append(dict(ing=sk.cell(row=r, column=2).value, q=q, u=u, gpu=g, kpu=k,
                                        g=(q or 0) * (g or 0), kcal=(q or 0) * (k or 0),
                                        B=(q or 0) * (b or 0), T=(q or 0) * (t or 0), W=(q or 0) * (w or 0),
                                        cooked=(q or 0) * (cooked or 0), raw=sk.cell(row=r, column=6).value))
hdr = [c.value for c in pr[1]]
recs = []
for r in range(2, pr.max_row + 1):
    pid, name = pr.cell(row=r, column=1).value, pr.cell(row=r, column=2).value
    if not name or not isinstance(pid, str) or not pid.startswith("P"):
        continue
    d = {h: pr.cell(row=r, column=i + 1).value for i, h in enumerate(hdr)}
    recs.append(dict(id=pid, name=name, cat=d["Kategoria"], serv=d["Porcje bazowe"], link=d["Link"],
                     autor_kcal=d["kcal — autor"], prep=d["Przygotowanie"] or "", items=rows.get(pid, [])))
json.dump(recs, io.open(os.path.join(S, "audit_kcal.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)

# kombinacje produkt/jednostka i kcal na 100 g
combo = collections.defaultdict(set)
k100 = {}
for rc in recs:
    for it in rc["items"]:
        combo[(it["ing"], it["u"])].add(round(it["gpu"] or 0, 2))
        if it["gpu"] and it["kpu"] is not None:
            k100.setdefault(it["ing"], set()).add(round(it["kpu"] / it["gpu"] * 100, 1))
with io.open(os.path.join(S, "audit_combo.txt"), "w", encoding="utf-8") as f:
    for (ing, u), gs in sorted(combo.items()):
        if u in ("g", "ml", "kg", "l"):
            continue
        f.write("%-28s %-10s %s\n" % (ing, u, sorted(gs)))
with io.open(os.path.join(S, "audit_k100.txt"), "w", encoding="utf-8") as f:
    for ing, ks in sorted(k100.items()):
        f.write("%-28s %s\n" % (ing, sorted(ks)))
print(len(recs), "przepisow,", sum(len(r["items"]) for r in recs), "wierszy,",
      len(combo), "kombinacji, produktow:", len(k100))
