# -*- coding: utf-8 -*-
"""Wciaga do zbioru opisy pobrane ze stron TikToka (zalogowana sesja),
tam gdzie sa pelniejsze niz to, co zwrocilo oEmbed."""
import json, os

SP = os.path.dirname(os.path.abspath(__file__))
allr = json.load(open(SP + "/all_recipes.json", encoding="utf-8"))
page = json.load(open(SP + "/tt_page_captions.json", encoding="utf-8"))

bylink = {}
for k, v in allr.items():
    if v.get("link"):
        bylink[v["link"]] = k

n = 0
for url, x in page.items():
    desc = (x or {}).get("desc") or ""
    k = bylink.get(url)
    if not k or not desc:
        continue
    if len(desc) > len(allr[k].get("caption") or "") + 20:
        allr[k]["caption"] = desc
        allr[k].setdefault("sources", []).append("strona TikTok")
        n += 1
        print("  uzupelniono: %-30s %d znakow" % (url.split("@")[1].split("/")[0][:30], len(desc)))

json.dump(allr, open(SP + "/all_recipes.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("Podmieniono opisow: %d" % n)
