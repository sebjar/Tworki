# -*- coding: utf-8 -*-
"""Dla przepisow bez skladnikow: probuje dociagnac tresc z blogow autorow."""
import json, os, re, sys, time, unicodedata

SP = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SP)
from blogs import fetch_recipe, search_site, get

# autor (z TikToka/IG) -> domena bloga
BLOGS = {
    "maja": "majasrecipes.com", "majasrecipes": "majasrecipes.com",
    "i.am.never.full": "iamneverfull.com", "iamneverfull": "iamneverfull.com",
    "erinscozykitchen": "erinscozykitchen.com", "erin.lim": "erinscozykitchen.com",
    "goldengracekitchen": "goldengracekitchen.com",
    "jalalsamfit": "jalalsamfit.com",
    "stealth_health_life": "stealthhealthlife.com",
    "overalleats": "overalleats.com",
    "recipeincaption": "recipeincaption.com",
    "owen.han": "owenhan.com",
    "cookwithcourt_": "cookwithcourt.com",
}
URL_RE = re.compile(r"https?://[^\s\"'<>)\]]+", re.I)
STOP = {"the", "and", "with", "for", "my", "a", "of", "day", "viral", "recipe", "recipes",
        "easy", "best", "high", "protein", "przepis", "na", "z", "w", "i"}


def deacc(s):
    s = (s or "").replace("ł", "l").replace("Ł", "L")
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


def slug_words(s):
    return [w for w in re.findall(r"[a-z0-9]+", deacc(s)) if w not in STOP and len(w) > 2]


def best_url(urls, query):
    qw = set(slug_words(query))
    best, score = None, 0
    for u in urls:
        slug = u.rstrip("/").split("/")[-1]
        s = len(qw & set(slug_words(slug)))
        if s > score:
            best, score = u, s
    return best if score >= 2 else None


def enrich(name, caption, author, link):
    """Zwraca (przepis, metoda) albo (None, powod)."""
    # 1) jawny link w opisie
    for u in URL_RE.findall(caption or ""):
        u = u.rstrip(".,)")
        if any(x in u for x in ("tiktok.com", "instagram.com", "youtu", "linktr.ee", "bit.ly")):
            continue
        r = fetch_recipe(u)
        if r and len(r["ingredients"]) >= 3:
            return r, "link podany w opisie"
    # 2) blog z adresu przepisu
    if link and not any(x in link for x in ("tiktok.com", "instagram.com", "youtu")):
        r = fetch_recipe(link)
        if r and len(r["ingredients"]) >= 3:
            return r, "strona przepisu"
    # 3) wyszukiwarka bloga autora
    dom = BLOGS.get(deacc(author).strip("✨ ").strip())
    if not dom:
        for k, v in BLOGS.items():
            if k in deacc(author):
                dom = v
                break
    if dom and name:
        q = " ".join(slug_words(name)[:6])
        if q:
            try:
                urls = search_site(dom, q)
            except Exception:
                urls = []
            u = best_url(urls, name)
            if u:
                r = fetch_recipe(u)
                if r and len(r["ingredients"]) >= 3:
                    r["source_url"] = u
                    return r, "wyszukiwarka bloga %s" % dom
    return None, "brak zrodla"


if __name__ == "__main__":
    data = json.load(open(SP + "/parsed.json", encoding="utf-8"))
    weak = [(k, v) for k, v in data.items()
            if (len(v["file_ings"]) or len(v["parsed"]["ings"])) < 3]
    print("Do proby: %d przepisow\n" % len(weak))
    out, stats = {}, {}
    for i, (k, v) in enumerate(weak, 1):
        nm = v["name"] or v["parsed"]["name"] or ""
        r, how = enrich(nm, v["caption"] or "", v["author"] or "", v["link"] or "")
        stats[how] = stats.get(how, 0) + 1
        if r:
            out[k] = {"recipe": r, "how": how}
            print("%2d. OK   %-42s %2d skl, %2d krokow  (%s)"
                  % (i, nm[:42], len(r["ingredients"]), len(r["steps"]), how))
        else:
            print("%2d. --   %-42s %s" % (i, nm[:42], how))
        time.sleep(0.4)
    json.dump(out, open(SP + "/enriched.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("\nODZYSKANE: %d / %d" % (len(out), len(weak)))
    for h, n in sorted(stats.items(), key=lambda x: -x[1]):
        print("   %-34s %d" % (h, n))
