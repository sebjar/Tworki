# -*- coding: utf-8 -*-
"""Porownanie wersji z 15.09.2026 (odtworzonej) z aktualna: co sie zmienilo, wiersz po wierszu."""
import collections, io, json, os, shutil, sys
import openpyxl
from przelicz import przelicz, SRC

S = os.path.dirname(os.path.abspath(__file__))
STARA_SRC = os.path.join(S, "wrzesien", "Przepisy-wrzesien.xlsx")
shutil.copy(przelicz(SRC), os.path.join(S, "_nowa.xlsx"))
shutil.copy(przelicz(STARA_SRC), os.path.join(S, "_stara.xlsx"))
nv = openpyxl.load_workbook(os.path.join(S, "_nowa.xlsx"), data_only=True)
sv = openpyxl.load_workbook(os.path.join(S, "_stara.xlsx"), data_only=True)
nf = openpyxl.load_workbook(SRC)
sf = openpyxl.load_workbook(STARA_SRC)
out = {}


def przepisy(wb):
    ws = wb["Przepisy"]
    hdr = [c.value for c in ws[1]]
    d = {}
    for r in ws.iter_rows(min_row=2, values_only=True):
        if r[0] and r[1]:
            d[r[0]] = dict(zip(hdr, r))
    return hdr, d


hdr, P_new = przepisy(nv)
_, P_old = przepisy(sv)
zm = collections.OrderedDict()
for pid in sorted(P_old):
    o, n = P_old[pid], P_new.get(pid)
    if n is None:
        zm[pid] = [("ZNIKNAL", o["Nazwa przepisu"], None)]
        continue
    for h in hdr:
        a, b = o.get(h), n.get(h)
        if isinstance(a, float) or isinstance(b, float):
            if isinstance(a, (int, float)) and isinstance(b, (int, float)) and abs(a - b) < 0.01:
                continue
        if a != b:
            zm.setdefault(pid, []).append((h, a, b))
out["przepisy_zmiany"] = {k: [(h, str(a)[:300], str(b)[:300]) for h, a, b in v] for k, v in zm.items()}
out["nowe_id"] = sorted(set(P_new) - set(P_old))


def skladniki(wb):
    ws = wb["Składniki"]
    hdr = [c.value for c in ws[1]]
    d = collections.defaultdict(list)
    for r in ws.iter_rows(min_row=2, values_only=True):
        if r[0]:
            d[str(r[0]).split(":")[0]].append(tuple(r[1:4]))
    return hdr, d


sh, S_new = skladniki(nv)
_, S_old = skladniki(sv)
out["skladniki_hdr"] = sh[:6]
sk = {}
for pid in sorted(S_old):
    a, b = collections.Counter(S_old[pid]), collections.Counter(S_new.get(pid, []))
    if a != b:
        sk[pid] = dict(usuniete=[list(x) for x in (a - b).elements()],
                       dodane=[list(x) for x in (b - a).elements()])
out["skladniki_zmiany"] = sk


def lista(wb):
    ws = wb["Lista zakupów"]
    return {r[1] for r in ws.iter_rows(min_row=2, values_only=True) if r[1]}


out["lista_dodane"] = sorted(lista(nv) - lista(sv))
out["lista_usuniete"] = sorted(lista(sv) - lista(nv))

ins = lambda wb: [tuple(str(x) for x in r if x) for r in wb["Instrukcja"].iter_rows(values_only=True) if any(r)]
a, b = ins(sv), ins(nv)
out["instrukcja_usuniete"] = [r for r in a if r not in b]
out["instrukcja_dodane"] = [r for r in b if r not in a]

for arkusz in ("Ustawienia", "Plan"):
    roz = []
    for ws_o, ws_n in ((sf[arkusz], nf[arkusz]),):
        mr = max(ws_o.max_row, ws_n.max_row); mc = max(ws_o.max_column, ws_n.max_column)
        for r in range(1, mr + 1):
            for c in range(1, mc + 1):
                x, y = ws_o.cell(row=r, column=c).value, ws_n.cell(row=r, column=c).value
                if x != y:
                    roz.append((ws_o.cell(row=r, column=c).coordinate, str(x)[:120], str(y)[:120]))
    out["formuly_" + arkusz] = roz[:40] + ([("...", len(roz), "")] if len(roz) > 40 else [])

# formuly w Przepisach (wiersz 2 jako wzor) i w Skladnikach
for arkusz, wiersz in (("Przepisy", 2), ("Składniki", 2)):
    roz = []
    for c in range(1, nf[arkusz].max_column + 1):
        x = sf[arkusz].cell(row=wiersz, column=c).value
        y = nf[arkusz].cell(row=wiersz, column=c).value
        if (isinstance(x, str) and x.startswith("=")) or (isinstance(y, str) and y.startswith("=")):
            if x != y:
                roz.append((nf[arkusz].cell(row=1, column=c).value, str(x)[:200], str(y)[:200]))
    out["formuly_" + arkusz] = roz

json.dump(out, io.open(os.path.join(S, "porownanie.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("przepisy ze zmianami:", len(zm), "| nowe ID:", out["nowe_id"])
print("przepisy ze zmienionymi skladnikami:", len(sk))
print("lista zakupow +", out["lista_dodane"], "-", out["lista_usuniete"])
for k in ("formuly_Ustawienia", "formuly_Plan", "formuly_Przepisy", "formuly_Składniki"):
    print(k, len(out[k]))
