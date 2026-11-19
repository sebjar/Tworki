# -*- coding: utf-8 -*-
"""Dociaga przepisy z blogow, do ktorych autorzy odsylaja w opisach (schema.org/Recipe)."""
import gzip, json, re, sys, urllib.parse, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/126 Safari/537.36",
      "Accept-Language": "pl,en;q=0.9", "Accept-Encoding": "gzip"}


def get(url, timeout=30):
    r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout)
    d = r.read()
    if r.headers.get("Content-Encoding") == "gzip":
        d = gzip.decompress(d)
    return d.decode("utf-8", "replace")


def _flat(x):
    if isinstance(x, str):
        return [x]
    if isinstance(x, dict):
        if x.get("@type") == "HowToSection":
            out = []
            for s in x.get("itemListElement", []):
                out += _flat(s)
            return out
        return [x.get("text") or x.get("name") or ""]
    if isinstance(x, list):
        out = []
        for i in x:
            out += _flat(i)
        return out
    return []


def _nodes(data):
    """Rozwija @graph i listy na plaska liste wezlow."""
    out = []
    stack = [data]
    while stack:
        n = stack.pop()
        if isinstance(n, list):
            stack.extend(n)
        elif isinstance(n, dict):
            out.append(n)
            if "@graph" in n:
                stack.append(n["@graph"])
    return out


def recipe_from_html(html):
    """Wyciaga Recipe z JSON-LD; obsluguje @graph i listy."""
    for m in re.finditer(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
                         html, re.S | re.I):
        raw = m.group(1).strip()
        try:
            data = json.loads(raw)
        except Exception:
            try:
                data = json.loads(re.sub(r",\s*([}\]])", r"\1", raw))
            except Exception:
                continue
        for node in _nodes(data):
            t = node.get("@type")
            types = t if isinstance(t, list) else [t]
            if any("Recipe" == str(x) for x in types):
                ings = [i.strip() for i in _flat(node.get("recipeIngredient")) if i and i.strip()]
                steps = [s.strip() for s in _flat(node.get("recipeInstructions")) if s and s.strip()]
                if ings:
                    return {"name": node.get("name"), "yield": str(node.get("recipeYield")),
                            "ingredients": ings, "steps": steps}
    return None


def _text(h):
    import html as H
    h = re.sub(r"(?is)<(script|style|svg)[^>]*>.*?</\1>", " ", h)
    h = re.sub(r"<[^>]+>", " ", h)
    return re.sub(r"\s+", " ", H.unescape(h)).strip()


def recipe_from_microdata(html):
    """Schema.org w formie mikrodanych (itemprop) - tak robi m.in. aniagotuje.pl."""
    ings = [_text(m.group(1)) for m in re.finditer(
        r'itemprop=["\']recipeIngredient["\'][^>]*>(.*?)</(?:li|span|p|div)>', html, re.S | re.I)]
    ings = [i for i in ings if i and len(i) < 160]
    if not ings:
        return None
    steps = [_text(m.group(1)) for m in re.finditer(
        r'itemprop=["\']recipeInstructions["\'][^>]*>(.*?)</(?:li|div|p|section)>', html, re.S | re.I)]
    steps = [s for s in steps if s and 10 < len(s) < 800]
    if not steps:
        steps = [_text(m.group(1)) for m in re.finditer(
            r'<(?:h3|strong)[^>]*>\s*Krok\s*\d+[^<]*</(?:h3|strong)>\s*(.{0,700}?)(?=<(?:h3|strong)|</section)',
            html, re.S | re.I)]
        steps = [s for s in steps if s and 10 < len(s) < 800]
    nm = re.search(r'itemprop=["\']name["\'][^>]*>(.*?)</', html, re.S | re.I)
    y = re.search(r'itemprop=["\']recipeYield["\'][^>]*?(?:content=["\']([^"\']+)|>(.*?)</)',
                  html, re.S | re.I)
    return {"name": _text(nm.group(1)) if nm else None,
            "yield": (y.group(1) or y.group(2)) if y else None,
            "ingredients": ings, "steps": steps}


def search_site(domain, query, limit=3):
    """Szuka wpisu na blogu przez wbudowana wyszukiwarke WordPressa."""
    urls = []
    for tpl in ("https://%s/?s=%s", "https://%s/search/%s"):
        try:
            html = get(tpl % (domain, urllib.parse.quote(query)))
        except Exception:
            continue
        for m in re.finditer(r'href="(https?://%s/[^"#?]+/)"' % re.escape(domain), html):
            u = m.group(1)
            if any(x in u for x in ("/category/", "/tag/", "/author/", "/page/",
                                    "/wp-", "/feed", "/privacy", "/about", "/contact")):
                continue
            if u not in urls:
                urls.append(u)
            if len(urls) >= limit * 4:
                break
        if urls:
            break
    return urls[:limit * 4]


def fetch_recipe(url):
    try:
        html = get(url)
    except Exception:
        return None
    return recipe_from_html(html) or recipe_from_microdata(html)


if __name__ == "__main__":
    tests = [
        ("bezposredni URL z opisu", "https://iamneverfull.com/sweet-honey-chicken-recipe/"),
        ("bezposredni URL z opisu", "https://erinscozykitchen.com/recipe/"
                                    "copycat-mcdonalds-mcchicken-big-mac-chicken-nuggets-homemade-sesame-buns/"),
        ("blog PL", "https://aniagotuje.pl/przepis/kurczak-teriyaki"),
        ("blog PL", "https://aniagotuje.pl/przepis/zapiekanka-gnocchi"),
    ]
    for label, u in tests:
        r = fetch_recipe(u)
        print("%-24s %-70s -> %s" % (label, u[:70],
              ("%d skl., %d krokow" % (len(r["ingredients"]), len(r["steps"]))) if r else "BRAK"))
    print("\n--- wyszukiwarka bloga majasrecipes.com ---")
    for q in ["butter chicken", "creamy pesto pasta"]:
        found = search_site("majasrecipes.com", q)
        print("  %-22s -> %s" % (q, found[:3] if found else "nic"))
