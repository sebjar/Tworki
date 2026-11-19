# -*- coding: utf-8 -*-
"""Pelne przepisy z aniagotuje.pl (skladniki, kroki, wartosci na 100 g) dla sugestii."""
import html as H, io, json, re, sys, time, urllib.request

SLUGI = ["kurczak-curry", "zapiekanka-gyros", "tortilla-z-kurczakiem", "chili-con-carne",
         "kurczak-po-toskansku", "kurczak-po-koreansku"]


def clean(x):
    x = re.sub(r"<br\s*/?>", "\n", x or "")
    x = H.unescape(re.sub(r"<[^>]+>", " ", x))
    return "\n".join(re.sub(r"[ \t\xa0]+", " ", l).strip() for l in x.split("\n") if l.strip())


out = {}
for s in SLUGI:
    url = "https://aniagotuje.pl/przepis/" + s
    t = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}),
                               timeout=25).read().decode("utf-8", "ignore")
    io.open("www/sug_%s.html" % s, "w", encoding="utf-8").write(t)
    g = lambda p: (re.search(p, t, re.S) or [None, None])[1]
    # skladniki w grupach (naglowki sekcji typu "Sos:" tez sa przydatne)
    ings = [clean(m) for m in re.findall(r'class="ingredient ingredient-name">(.*?)</span>', t, re.S)]
    steps = []
    for name, txt in re.findall(r'class="step-name">.*?itemprop="name">(.*?)</span>.*?'
                                r'class="step-text" itemprop="text">(.*?)<div', t, re.S):
        steps.append(clean(name) + ": " + clean(txt).replace("\n", " "))
    out[s] = dict(url=url, name=clean(g(r"<h1[^>]*>(.*?)</h1>")),
                  yield_=g(r'itemprop="recipeYield" content="([^"]+)"'),
                  kcal_porcja=g(r"Około\s*(\d{2,4})\s*kcal w 1 porc"),
                  na100=[clean(g(r'itemprop="%s">([^<]+)' % k)) for k in
                         ("calories", "proteinContent", "fatContent", "carbohydrateContent")],
                  ocena=clean(g(r'itemprop="ratingValue"[^>]*>([^<]+)')),
                  glosy=clean(g(r'itemprop="ratingCount"[^>]*>([^<]+)')),
                  ings=ings, steps=steps)
    time.sleep(0.8)
json.dump(out, io.open("www/sug_ag.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for s, d in out.items():
    print("=" * 8, s, "|", d["name"], "| wyd:", d["yield_"], "| kcal/porcję:", d["kcal_porcja"],
          "| 100 g:", d["na100"], "| ocena", d["ocena"], d["glosy"])
    for i in d["ings"]:
        print("  -", i)
    for i, st in enumerate(d["steps"], 1):
        print("  %d. %s" % (i, st))
