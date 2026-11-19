# -*- coding: utf-8 -*-
"""Pobiera dane przepisow z aniagotuje.pl (mikrodane schema.org/Recipe) dla listy kandydatow."""
import html as H, io, json, re, sys, time, urllib.request
out = {}
for s in sys.argv[1:]:
    url = "https://aniagotuje.pl/przepis/" + s
    try:
        t = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=25).read().decode("utf-8", "ignore")
    except Exception as e:
        out[s] = {"err": str(e)}; continue
    g = lambda p: (re.search(p, t, re.S) or [None, None])[1]
    clean = lambda x: re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", x or ""))).strip()
    ings = [clean(m) for m in re.findall(r'itemprop="recipeIngredient"[^>]*>(.*?)</span>\s*</', t, re.S)]
    kc = g(r"Około\s*(\d{2,4})\s*kcal w 1 porc")
    out[s] = dict(name=clean(g(r'<h1[^>]*>(.*?)</h1>')), yield_=g(r'itemprop="recipeYield" content="([^"]+)"'),
                  time=g(r'itemprop="totalTime" content="([^"]+)"'), kcal_porcja=kc,
                  bialko_100g=clean(g(r'itemprop="proteinContent"[^>]*>([^<]+)')),
                  ocena=clean(g(r'itemprop="ratingValue"[^>]*>([^<]+)')), glosy=clean(g(r'itemprop="ratingCount"[^>]*>([^<]+)')),
                  ings=ings, url=url)
    time.sleep(0.8)
json.dump(out, io.open("www/ag_kandydaci.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for s, d in out.items():
    print("%-40s | %s | %s | %s kcal/porcję | ocena %s (%s) | %d skł." % (s[:40], (d.get("name") or d.get("err") or "")[:40], d.get("yield_"), d.get("kcal_porcja"), d.get("ocena"), d.get("glosy"), len(d.get("ings") or [])))
