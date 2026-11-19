# -*- coding: utf-8 -*-
"""Dopisuje 2 przepisy z TikToka, ktore doszly do kolekcji po pierwszym pobraniu."""
import io, json

CAP1 = ("Prosty chiński makaron. Chicken Lo Mein. #foxxgotuje #przepis #chińszczyzna #kurczak "
        "PRZEPIS: Sos: - 3 łyżki sosu sojowego ciemnego - 1 łyżka oleju sezamowego "
        "- 2-3 łyżeczki cukru - szczypta soli - 1/3 łyżeczki pieprzu białego lub czarnego "
        "- 1 łyżeczka skrobi ziemniaczanej - 3-4 łyżki wody Kurczak: - 200 g udek z kurczaka "
        "bez kości - 2 łyżki sosu sojowego ciemnego - odrobina soli - 1 łyżeczka skrobi "
        "ziemniaczanej - 1-2 łyżki oleju Warzywa: - pokrojona marchekwa - pokrojona cebula "
        "- pokrojona kapusta - czosnek i imbir drobno posiekane / przeciśnięte przez prasę "
        "Opcjonalnie: - odrobina białego wina - szczypiorek - płatki chili "
        "Najpierw usmaż warzywa - duży ogień i krótko - max 2 min. Następnie usmaż kurczaka. "
        "Krok 3 to podsmażenie czosnku i imbiru i dodanie wina, a następnie od razu dodanie "
        "kurczaka, ugotowanego chińskiego makaronu oraz sosu.")

CAP2 = ("High Protein Sticky Korean Fried Chicken! Only 452 Calories. This has to be one of the "
        "best chicken & rice recipes, so much flavor, the perfect balance of sweet, spicy & "
        "savoury! Macros per serve (4 total) 452 Calories | 40g Protein | 51g Carbs | 10g Fat "
        "Ingredients (4 servings) - 700-800g Cubed Chicken Breast - 2 tsp Garlic Powder "
        "- 1.5 tsp Black Pepper - 2 tsp Paprika - 1 tsp Salt - 30g Cornflour For the Glaze "
        "- 50ml Light Soy sauce mixed with 50ml Water (total 100ml) - 25g Honey - 40g Gochujang "
        "Paste Pickled Cucumbers - Thinly sliced Cucumber - 20ml Light Soy Sauce - 10ml Rice "
        "Vinegar - OPTIONAL Chilli Flakes - 1 tsp Garlic Powder - 1 tsp Sesame Seeds "
        "Important cooking notes - When coating the chicken with cornflour makes sure it's well "
        "coated. - When making the glaze, add the ingredients on low heat then keep stirring "
        "till it starts to bubble lightly then let it reduce for 3-4 mins. It should thicken "
        "- You can store the cucumbers separately and warm up the meal prep without them.")

NEW = [
    dict(key="tt:7524647990372486422", author="foxx.gotuje", cap=CAP1,
         link="https://www.tiktok.com/@foxx.gotuje/video/7524647990372486422",
         name="Chicken Lo Mein"),
    dict(key="tt:7324768515263679777", author="jalalsamfit", cap=CAP2,
         link="https://www.tiktok.com/@jalalsamfit/video/7324768515263679777",
         name="Sticky Korean Fried Chicken"),
]

parsed = json.load(io.open("parsed.json", encoding="utf-8"))
ci = json.load(io.open("curate_input.json", encoding="utf-8"))
have = {r["key"] for r in ci}

added = 0
for e in NEW:
    if e["key"] in parsed or e["key"] in have:
        print("juz jest:", e["key"])
        continue
    parsed[e["key"]] = dict(
        author=e["author"], caption=e["cap"], cat="", file_ings=[], link=e["link"],
        n_ing=0, name=e["name"], platform="TikTok", servings=None, site_ings=[],
        sources=["kolekcja fud (dopisane po ponownym sprawdzeniu)"], steps=[], typ="video",
        parsed=dict(ings=[], name=e["name"], review="", servings=None, steps=[]))
    ci.append(dict(author=e["author"], blog=None, cap=e["cap"], file_ings=[], key=e["key"],
                   link=e["link"], name=e["name"], platform="TikTok", score=0, tr=""))
    added += 1

json.dump(parsed, io.open("parsed.json", "w", encoding="utf-8"), ensure_ascii=False)
json.dump(ci, io.open("curate_input.json", "w", encoding="utf-8"), ensure_ascii=False)
print("dopisano:", added, "| parsed:", len(parsed), "| curate_input:", len(ci))
print("indeksy nowych:", [i for i, r in enumerate(ci) if r["key"] in {e["key"] for e in NEW}])
