# -*- coding: utf-8 -*-
"""Wynik recznej weryfikacji przepis po przepisie (19-22.10.2026) -> weryfikacja.json.
Skad liczba porcji i co poprawilem; kcal 'przed' to wersja arkusza z 15.09."""
import io, json

PORCJE = {
    "P001": "6 bułek z przepisu", "P002": "autor: 11 burrito", "P004": "4 wrapy z przepisu",
    "P005": "autor: 2 porcje", "P008": "autor: 2 porcje", "P012": "autor: 4 porcje",
    "P014": "autorka podaje kcal za całą miskę — dzielę na 2", "P015": "autor: 2 porcje",
    "P018": "autor: 5 porcji", "P019": "autor: 4 porcje", "P020": "autor: ok. 3 porcje",
    "P021": "autor: 4 szaszłyki", "P023": "autorka: 2 porcje", "P024": "autor: 2 burrito",
    "P026": "blog autorki: 10 porcji", "P027": "autor: 4 porcje", "P029": "autor: 2 pity",
    "P031": "Twój plik: 4 porcje", "P032": "autorzy: „lunch we dwoje”", "P033": "autor: 4 porcje",
    "P037": "autor: 3 porcje", "P039": "autor: ok. 3 porcje", "P040": "blog autorki: 4 porcje",
    "P041": "blog autorki: 4 porcje", "P042": "autor: 3 porcje", "P043": "autorka: 2 porcje",
    "P044": "z makr autora: 4 porcje (po połówce papryki)", "P045": "autor: ok. 2 porcje",
    "P048": "autor: 12 burrito", "P049": "autor: ok. 3 porcje", "P050": "autor: 2 porcje",
    "P053": "autor: 4 wrapy", "P054": "autor: 4 porcje", "P055": "autor: 4 porcje",
    "P058": "autorka: 4 porcje", "P060": "autor: 4 porcje", "P061": "2 kawałki łososia",
    "P065": "6 bułek z przepisu", "P067": "autor: 12 sajgonek, porcja = 1",
    "P070": "autor: 3 porcje", "P072": "autor: 6 sztuk", "P074": "autor: 2 porcje",
    "P075": "autor: 4 porcje", "P076": "blog autorki: 4 porcje", "P078": "autor: 4 porcje",
    "P080": "nie podano — przyjęte 2, jak w starszej wersji autora", "P081": "autor: 2 porcje", "P082": "autor: 4 wrapy",
    "P084": "1 słoik (autor robi 4 naraz)", "P085": "autor: 4 sztuki", "P089": "4 filety łososia",
    "P093": "autor: 2 porcje", "P094": "12 tacos, po 3 na porcję", "P096": "autorka: ciasto na 4 części",
    "P097": "autor: 8 sztuk", "P099": "blog autora: 2 porcje", "P100": "blacha 23×33 cm, 12 kawałków",
    "P103": "autor: 1 porcja", "P107": "blog autorki: 4 porcje", "P109": "autor: 3 porcje",
    "P112": "Twój plik: 2 porcje", "P115": "1 porcja", "P116": "przyjęte: 125 g makaronu na osobę",
    "P118": "12 rulonów, porcja = 1", "P139": "autor: 1 porcja", "P140": "autorka: 2 porcje",
    "P142": "autor: 1 porcja", "P143": "autor: 4 porcje", "P144": "autor: 8 sztuk",
    "P147": "2 bagietki, porcja = pół",
}

POPRAWKI = {
    "P001": "Dopisany olej do smażenia nuggetsów i kotletów (autorka go pominęła).",
    "P002": "3 cytryny zamiast 2; kolendra w mieszance przypraw to mielona.",
    "P003": "Chipotle w adobo zamiast świeżego chili; doliczone przyprawy i olej do warzyw.",
    "P004": "Ser: po 30 g każdego na wrapa, razem 120 g cheddara i 120 g mozzarelli (było o połowę mniej).",
    "P005": "Porcje 4 → 2, tak jak podaje autor.",
    "P006": "Dopisana cytryna do podania.",
    "P008": "Porcje 3 → 2, tak jak podaje autor.",
    "P013": "Ryż: autorka podaje 200 g UGOTOWANEGO, czyli 80 g suchego (było 200 g suchego).",
    "P014": "Ciecierzyca ze słoika: 240 g po odsączeniu (było 400 g).",
    "P015": "Dopisana uwaga, że przyprawy są dobrane przeze mnie.",
    "P017": "Dopisana uwaga: kalorie bez ryżu.",
    "P028": "Suszone pomidory: 170 g po odsączeniu ze słoika (było 200 g).",
    "P029": "Pita 38 g, jak u autora (było 60 g).",
    "P032": "Porcje 4 → 2 („lunch we dwoje”); ziemniaki 450 g zamiast ok. 1 kg.",
    "P040": "Porcje 3 → 4, tak jak na blogu autorki.",
    "P044": "Porcje 2 → 4 (wynika z makr autora); dopisane kcal autora.",
    "P043": "Boczek 60 g — polskie plastry ok. 15 g (było liczone po 25 g).",
    "P066": "Dopisane makra autora: podaje je za 1 stripsa z 12, porcja w arkuszu to 4.",
    "P045": "Ryż: 95 g suchego, tyle co 1,5 szklanki ugotowanego (było 150 g).",
    "P053": "1 jajko zamiast 2, jak w Twoim pliku.",
    "P056": "Orzo: autorka podaje 200 g UGOTOWANEGO, czyli 90 g suchego (było 200 g suchego).",
    "P059": "Kolendra w mieszance przypraw to mielona, nie świeża.",
    "P060": "Czosnek suszony zamiast świeżego, jak u autora.",
    "P065": "Mielona pierś z kurczaka zamiast zwykłego mielonego (tak w przepisie).",
    "P067": "Mięso mielone wieprzowe, jak u autora.",
    "P072": "Mielona pierś z kurczaka zamiast zwykłego mielonego (tak w przepisie).",
    "P073": "Ciasto do pizzy zamiast francuskiego, tak jak w przepisie.",
    "P080": "2.11.2026: zapisany film zniknął z TikToka — przepis z nowszej wersji autora („FIT Sałatka BIG MAC”), składniki i ilości z jej opisu.",
    "P081": "Dopisane kcal autora (538 na wrapa).",
    "P083": "Kminek zamiast kuminu i ziarna kolendry, jak u autora.",
    "P091": "Dopisana uwaga, które ilości są szacunkowe.",
    "P094": "Małe tortille do tacos zamiast dużych.",
    "P099": "Porcje 4 → 2, tak jak na blogu autora.",
    "P103": "Krok 1 wymienia składniki wprost.",
    "P104": "Masło do sosu 100 g zamiast 150 g; dopisana uwaga o szacunkach.",
    "P109": "Porcje 4 → 3, tak jak podaje autor.",
    "P112": "1 jajko + 2 żółtka, jak na nagraniu (były 3 całe jajka).",
    "P116": "Ilości jak w Twoim pliku (500 g makaronu), porcje 2 → 4.",
    "P117": "Olej 70 ml zamiast 100 ml (tyle mniej więcej wsiąka).",
    "P118": "Porcje 4 → 12 (porcja = 1 rulon); 12 plastrów bekonu to ok. 180 g; ciasto francuskie wg polskiej etykiety.",
}

import openpyxl
# punkt odniesienia: wersja z 15.09 (sprzed obu rund weryfikacji), odtworzona i przeliczona
wrz = {}
for r in openpyxl.load_workbook("_stara.xlsx", data_only=True)["Przepisy"].iter_rows(min_row=2, values_only=True):
    if r[0] and r[1]:
        wrz[r[0]] = r[11]
rows = json.load(io.open("porownanie_kcal.json", encoding="utf-8"))
out = {}
for pid, name, s_old, s_new, _k22, k_new, k_aut, z_old, z_new in rows:
    k_old = wrz.get(pid)
    if k_new is None:
        wynik = "Autor nie podał przepisu — nie ma czego liczyć."
        porcje = "brak przepisu w źródle"
    else:
        porcje = PORCJE.get(pid, "przyjęte przeze mnie — autor nie podał")
        if pid in POPRAWKI:
            wynik = POPRAWKI[pid]
        elif k_old and abs(k_new - k_old) / k_old > 0.05:
            wynik = "Składniki zgodne ze źródłem; kcal zmieniły się tylko przez poprawioną tabelę wartości."
        else:
            wynik = "Składniki, ilości i porcje zgodne ze źródłem."
    out[pid] = dict(porcje=porcje, wynik=wynik, kcal_przed=k_old)
json.dump(out, io.open("weryfikacja.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(len(out), "wpisow;", sum(1 for v in out.values() if not v["wynik"].startswith(("Składniki", "Autor nie"))), "z poprawkami")
