# -*- coding: utf-8 -*-
"""Zbiera wszystkie zrodla przepisow w jeden zbior, deduplikuje po linku."""
import json, os, re, shutil, collections

SP = os.path.dirname(os.path.abspath(__file__))
DL = r"C:\Users\Sebastian\Downloads\ig_captions.json"
if os.path.exists(DL):
    shutil.copy(DL, SP + "/ig_captions.json")

ing_index = json.load(open(SP + "/ing_index.json", encoding="utf-8"))
caps_file = json.load(open(SP + "/captions.json", encoding="utf-8"))
caps_coll = json.load(open(SP + "/collection_tiktok.json", encoding="utf-8"))
caps_ig = json.load(open(SP + "/ig_captions.json", encoding="utf-8"))


def canon(url):
    """Klucz deduplikacji."""
    if not url:
        return None
    m = re.search(r"tiktok\.com/@[\w.\-]+/(?:video|photo)/(\d+)", url)
    if m:
        return "tt:" + m.group(1)
    m = re.search(r"instagram\.com/[\w.\-]+/(?:reel|p)/([\w\-]+)", url)
    if m:
        return "ig:" + m.group(1)
    m = re.search(r"(?:youtube\.com/watch\?v=|youtu\.be/)([\w\-]+)", url)
    if m:
        return "yt:" + m.group(1)
    return "url:" + url.split("?")[0].rstrip("/")


def clean_ig(txt):
    """Usuwa prefiks 'NNN likes, NNN comments - autor on DATE:' i cudzyslowy."""
    if not txt or txt.startswith("ERR:") or txt == "BRAK":
        return ""
    m = re.match(r'^[\d.,KMk ]+ likes?, [\d.,KMk ]+ comments? - ([\w.\-]+) on ([^:]+): "(.*)"\s*\.?\s*$',
                 txt, re.S)
    if m:
        return m.group(3).strip()
    return txt.strip()


recipes = collections.OrderedDict()


def add(key, **kw):
    r = recipes.setdefault(key, dict(name=None, link=None, platform=None, author=None,
                                     caption="", servings=None, cat=None, typ=None,
                                     file_ings=[], site_ings=[], steps=[], sources=[]))
    for k, v in kw.items():
        if v in (None, "", [], {}):
            continue
        if k in ("file_ings", "site_ings", "steps", "sources"):
            r[k] = r[k] + [x for x in v if x not in r[k]]
        elif not r[k]:
            r[k] = v
    return r


# 1) przepisy z pliku uzytkownika
for x in ing_index:
    k = canon(x["link"]) or ("name:" + x["recipe"])
    r = add(k, name=x["recipe"], link=x["link"], servings=x["serv"],
            cat=x["cat"], typ=x["typ"], sources=["plik"])
    if x["ing"]:
        r["file_ings"].append({"qty": x["qty"], "unit": x["unit"], "ing": x["ing"]})

# 2) opisy dociagniete dla przepisow z pliku
for name, v in caps_file.items():
    k = canon(v.get("url"))
    if k not in recipes:
        continue
    r = recipes[k]
    if v.get("caption"):
        r["caption"] = r["caption"] or v["caption"]
    if v.get("ingredients"):
        r["site_ings"] = r["site_ings"] or v["ingredients"]
    if v.get("steps"):
        r["steps"] = r["steps"] or v["steps"]
    r["platform"] = r["platform"] or v.get("kind")
    r["author"] = r["author"] or v.get("author")

# 3) kolekcja TikTok
for vid, v in caps_coll.items():
    if not v.get("ok"):
        continue
    add(canon(v["url"]), link=v["url"], platform="tiktok", author=v["author"],
        caption=v.get("caption", ""), sources=["kolekcja TikTok"])

# 4) zapisane rolki Instagram
for path, txt in caps_ig.items():
    url = "https://www.instagram.com" + path
    cap = clean_ig(txt)
    m = re.match(r"^/([\w.\-]+)/", path)
    add(canon(url), link=url, platform="instagram", author=m.group(1) if m else None,
        caption=cap, sources=["zapisane IG"])

json.dump(recipes, open(SP + "/all_recipes.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

# --- raport
tot = len(recipes)
with_file = sum(1 for r in recipes.values() if r["file_ings"])
with_site = sum(1 for r in recipes.values() if r["site_ings"])


def rich(r):
    c = r["caption"] or ""
    has_kw = re.search(r"(?i)(sk[łl]adnik|ingredient|ingrediente|potrzebujemy|zutaten)", c)
    return bool(r["file_ings"] or r["site_ings"] or (has_kw and len(c) > 200))


usable = [k for k, r in recipes.items() if rich(r)]
print("UNIKALNYCH PRZEPISOW:            %d" % tot)
print("  ze skladnikami z Twojego pliku: %d" % with_file)
print("  ze skladnikami ze strony www:   %d" % with_site)
print("  z lista skladnikow w opisie:    %d" % (len(usable) - with_file - with_site))
print("  RAZEM DO ROZPISANIA:            %d" % len(usable))
print("  bez tresci (sam link):          %d" % (tot - len(usable)))
print()
by_src = collections.Counter()
for r in recipes.values():
    by_src[", ".join(r["sources"]) or "?"] += 1
for s, n in by_src.most_common():
    print("  %-32s %d" % (s, n))
print()
print("BEZ UZYTECZNEJ TRESCI:")
for k, r in recipes.items():
    if not rich(r):
        print("  %-46s %s" % ((r["name"] or "(bez nazwy)")[:46], (r["link"] or "")[:58]))
