# -*- coding: utf-8 -*-
"""Parsuje opisy z TikToka/Instagrama na: nazwe, porcje, skladniki (ilosc/jednostka/nazwa), kroki."""
import json, os, re, unicodedata

SP = os.path.dirname(os.path.abspath(__file__))

FRAC = {"½": .5, "¼": .25, "¾": .75, "⅓": 1/3, "⅔": 2/3, "⅛": .125, "⅜": .375, "⅝": .625}

UNITS = {
    "g": "g", "gram": "g", "grama": "g", "gramy": "g", "gramow": "g", "grams": "g", "gr": "g",
    "kg": "kg", "kilo": "kg", "kilogram": "kg",
    "ml": "ml", "l": "l", "litr": "l", "litry": "l", "litra": "l", "liter": "l", "litre": "l",
    "dag": "dag", "dkg": "dag",
    "szt": "szt.", "sztuka": "szt.", "sztuki": "szt.", "sztuk": "szt.", "sztuke": "szt.",
    "item": "szt.", "items": "szt.", "arkusz": "szt.", "galazka": "szt.", "galazki": "szt.",
    "lyzka": "lyzka", "lyzki": "lyzka", "lyzek": "lyzka", "lyzke": "lyzka", "lyzkami": "lyzka",
    "tbsp": "lyzka", "tablespoon": "lyzka", "tablespoons": "lyzka", "tbs": "lyzka", "spoon": "lyzka",
    "lyzeczka": "lyzeczka", "lyzeczki": "lyzeczka", "lyzeczek": "lyzeczka", "lyzeczke": "lyzeczka",
    "tsp": "lyzeczka", "teaspoon": "lyzeczka", "teaspoons": "lyzeczka", "tep": "lyzeczka",
    "szklanka": "szklanka", "szklanki": "szklanka", "szklanek": "szklanka", "szklance": "szklanka",
    "cup": "szklanka", "cups": "szklanka",
    "zabek": "zabek", "zabki": "zabek", "zabkow": "zabek", "clove": "zabek", "cloves": "zabek",
    "puszka": "puszka", "puszki": "puszka", "puszke": "puszka", "can": "puszka", "cans": "puszka",
    "opak": "opak.", "opakowanie": "opak.", "opakowania": "opak.", "packet": "opak.",
    "packets": "opak.", "pack": "opak.",
    "garsc": "garsc", "garscie": "garsc", "garsci": "garsc", "handful": "garsc", "handfuls": "garsc",
    "szczypta": "szczypta", "szczypte": "szczypta", "pinch": "szczypta",
    "plaster": "plaster", "plastry": "plaster", "plastrow": "plaster", "plasterki": "plaster",
    "slice": "plaster", "slices": "plaster",
    "peczek": "peczek", "peczka": "peczek", "bunch": "peczek",
    "glowka": "glowka", "glowki": "glowka", "head": "glowka",
    "oz": "oz", "lbs": "lbs", "lb": "lbs",
}
PRETTY = {"g": "g", "kg": "kg", "ml": "ml", "l": "l", "dag": "dag", "szt.": "szt.",
          "lyzka": "łyżka", "lyzeczka": "łyżeczka", "szklanka": "szklanka", "zabek": "ząbek",
          "puszka": "puszka", "opak.": "opak.", "garsc": "garść", "szczypta": "szczypta",
          "plaster": "plaster", "peczek": "pęczek", "glowka": "główka", "oz": "oz", "lbs": "lbs"}

BULLET = r"^[\s]*(?:[-–—*•·‣▪◾⬛✅✔☑🔸🔹📍🥄🧂🍽>»]+|\d+[\).])\s*"
HDR_ING = re.compile(r"(?i)^(sk[łl]adniki|ingredients?|zutaten|potrzebujesz|potrzebujemy|"
                     r"co potrzebujemy|co potrzebujesz|lista sk[łl]adnik[oó]w|shopping list|"
                     r"what you.{0,3}ll need|what you need|you.{0,3}ll need|przepis)\b.{0,30}$")
HDR_STEP = re.compile(r"(?i)^(przygotowanie|wykonanie|spos[oó]b (?:przygotowania|wykonania)|"
                      r"instructions?|method|directions?|steps?|jak zrobi[cć])\b.{0,20}$")
# naglowki sekcji wewnatrz listy skladnikow - pomijamy jako skladnik
HDR_SECTION = re.compile(r"(?i)^(sos|farsz|marynata|nadzienie|dodatki|polewa|krem|dressing|"
                         r"topping|sauce|glaze|seasoning|spices?|przyprawy|to serve|garnish|"
                         r"for the .{0,30}|sk[łl]adniki na .{0,40}|na .{0,30})\s*:?\s*$")
NOISE = re.compile(r"(?i)(zapisz|obserwuj|follow me|follow along|comment|koment|link in bio|"
                   r"w bio|full recipe|przepis w formie|subscribe|stay hungry|dm you|i'?ll dm|"
                   r"cookbook|makro|macros per|calories|kcal \||partner|reklama|wsp[oó][lł]praca|"
                   r"film ci si[eę]|[lł]apk[eę] w g[oó]r[eę]|smacznego|rozdzia[lł]y|"
                   r"google \"|zostaw komentarz|share|udost[eę]pnij)")
PROSE = re.compile(r"[.!?]\s+\w|⃣")
HASHTAG_LINE = re.compile(r"^\s*(#[\wÀ-ɏ]+[\s#\wÀ-ɏ]*)+$")


def deacc(s):
    s = s.replace("ł", "l").replace("Ł", "L")
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


def strip_emoji(s):
    return "".join(c for c in s if unicodedata.category(c) not in ("So", "Sk", "Cf")).strip()


def unit_of(word):
    return UNITS.get(deacc((word or "").strip().rstrip(".")))


UNIT_TOKEN = re.compile(r"\d+\s*(?:g|kg|ml|l|dag|szt|tbsp|tsp|cup|oz|lbs|"
                        r"[łl]y[żz]|z[ąa]b|puszk|opak|gar[śs]|szklan|pl[ai]st)", re.I)


HAS_ING_HDR = re.compile(r"(?i)(sk[łl]adniki|ingredients?|what you.{0,3}ll need|"
                         r"co potrzebujesz|co potrzebujemy|potrzebujesz)\s*:")


def emoji_bullets(cap):
    """Emoji uzyte jako punktor listy. Zwykle wymagamy >=3 powtorzen, ale gdy opis
    ma naglowek 'Skladniki:'/'What you'll need:', kazde emoji moze byc punktorem
    (autorzy czesto daja inne emoji do kazdej pozycji)."""
    cnt = {}
    for ch in cap:
        if unicodedata.category(ch) == "So":
            cnt[ch] = cnt.get(ch, 0) + 1
    thr = 1 if HAS_ING_HDR.search(cap) else 3
    return [ch for ch, n in cnt.items() if n >= thr]


def explode(line):
    """Rozbija jedna dluga linie zlepionych skladnikow na osobne pozycje.
    'Mix: 3 lbs ground beef 2 tsp salt 1 onion' -> trzy linie."""
    if len(line) < 90 or len(UNIT_TOKEN.findall(line)) < 3:
        # krotsza linia z kilkoma miarami i przecinkami: 'lyzeczka tymianku, 1/2 lyzeczki soli'
        if len(UNIT_TOKEN.findall(line)) >= 2 and line.count(",") >= 1 and len(line) < 120:
            return [p.strip(" ,;") for p in line.split(",") if p.strip(" ,;")]
        return [line]
    parts = re.split(r"(?<=[a-ząćęłńóśźż\)])[\s,]+(?=[½¼¾⅓⅔]|\d)", line)
    return [p.strip(" ,;") for p in parts if p.strip(" ,;")]


def norm_lines(cap):
    cap = cap.replace("\r", "")
    lines = [l.strip() for l in cap.split("\n")]
    if len([l for l in lines if l]) < 4:
        t = cap
        for e in emoji_bullets(cap):
            t = t.replace(e, "\n" + e + " ")
        # myslnik-punktor: lapie zarowno "- 3 jajka" jak i "-3 jajka" (bez spacji)
        t = re.sub(r"\s+([-–—*•·‣▪◾⬛✅✔☑🔸🔹])\s*(?=\S)", r"\n\1 ", t)
        t = re.sub(r"\s+(?=\d+[\.\)]\s+[A-ZĄĆĘŁŃÓŚŹŻ])", "\n", t)
        t = re.sub(r"(?i)\s+(?=(?:step|krok)\s*\d)", "\n", t)
        t = re.sub(r"(?i)\s*((?:sk[łl]adniki|ingredients?|przygotowanie|wykonanie|"
                   r"instructions?|method|sos|farsz)\s*:)", r"\n\1", t)
        lines = [l.strip() for l in t.split("\n")]
    out = []
    for l in lines:
        if l:
            out.extend(explode(l))
    return [l for l in out if l]


def pre_qty(t):
    """Normalizuje 'pol', 'ok.', '1 i 1/2' itp. na poczatku linii."""
    t = re.sub(r"^(?:ok\.?|oko[łl]o|approx\.?|about|~)\s+", "", t, flags=re.I)
    t = re.sub(r"^p[oó][łl]tora\s+", "1.5 ", t, flags=re.I)
    t = re.sub(r"^p[oó][łl]\s+", "0.5 ", t, flags=re.I)
    t = re.sub(r"^(\d+)\s+i\s+1/2\s+", lambda m: "%s " % (int(m.group(1)) + .5), t, flags=re.I)
    t = re.sub(r"^(\d+)\s+1/2\s+", lambda m: "%s " % (int(m.group(1)) + .5), t)
    for sym, val in FRAC.items():
        t = re.sub(r"^%s\s*" % re.escape(sym), "%s " % val, t)
    t = re.sub(r"^(\d+)\s*/\s*(\d+)\s+",
               lambda m: "%s " % (int(m.group(1)) / int(m.group(2))), t)
    return t.strip()


def parse_qty(txt):
    """(ilosc, jednostka, reszta) z poczatku linii."""
    t = pre_qty(txt.strip())
    m = re.match(r"^(\d+(?:[.,]\d+)?)\s*(?:[-–]\s*\d+(?:[.,]\d+)?)?\s*"
                 r"([a-zA-ZÀ-ɏ.]+)?\s*(.*)$", t)
    if m:
        qty = float(m.group(1).replace(",", "."))
        u = unit_of(m.group(2))
        rest = m.group(3).strip()
        if u:
            return qty, u, rest
        return qty, None, ((m.group(2) or "") + " " + rest).strip()
    m = re.match(r"^([a-zA-ZÀ-ɏ]+)\s+(.*)$", t)
    if m and unit_of(m.group(1)):
        return 1.0, unit_of(m.group(1)), m.group(2).strip()
    return None, None, t


def looks_like_ing(line):
    l = line.strip()
    if not (2 <= len(l) <= 115) or HASHTAG_LINE.match(l) or l.startswith("#"):
        return False
    if re.match(BULLET, l) and not re.match(r"^\s*\d+[\).]\s", l):
        return True
    if re.match(r"^\s*\d+(?:[.,]\d+)?\s*(g|kg|ml|l|dag|oz|lbs)\b", l, re.I):
        return True
    if re.match(r"^\s*[½¼¾⅓⅔⅛]|^\s*\d+(?:[.,]\d+)?\s+\w", l):
        return True
    if re.match(r"(?i)^\s*(p[oó][łl]|ok\.)\s+\w", l):
        return True
    return False


def parse(cap, known_name=None):
    lines = norm_lines(cap)
    ings, steps, mode, seen = [], [], None, set()
    name, servings, review = known_name, None, []

    m = re.search(r"(?i)(?:serves|makes|for)\s*(\d+)|\((\d+)\s*(?:porcj\w*|servings?|osob\w*)\)|"
                  r"(\d+)\s*porcj\w*|na\s*(\d+)\s*(?:osob\w*|porcj\w*)|"
                  r"per serving \((\d+) total\)|\((\d+) total\)", cap)
    if m:
        servings = next((float(g) for g in m.groups() if g), None)

    for raw in lines:
        l = raw.strip()
        clean = strip_emoji(l)
        if HDR_ING.match(clean):
            mode = "ing"
            continue
        if HDR_STEP.match(clean):
            mode = "step"
            continue
        if HASHTAG_LINE.match(l):
            continue
        body = re.sub(BULLET, "", l).strip()
        body = re.sub(r"\s*#[\wÀ-ɏ]+.*$", "", body).strip()
        body = strip_emoji(body)
        if not body:
            continue
        if HDR_SECTION.match(body):
            mode = "ing"
            continue
        numbered = re.match(r"^\s*\d+[\).]\s", l)
        if numbered or (mode == "step" and len(body) > 45):
            if not NOISE.search(body):
                steps.append(body)
            mode = "step" if numbered else mode
            continue
        if NOISE.search(body):
            continue
        # zdanie (kropka w srodku) to opis czynnosci, nie skladnik
        if (mode == "ing" or looks_like_ing(clean)) and PROSE.search(body):
            if len(body) > 45:
                steps.append(body)
            continue
        if mode == "ing" or looks_like_ing(clean):
            if len(body) <= 95:
                q, u, rest = parse_qty(body)
                rest = rest.strip(" ,;:-.")
                key = deacc(rest)[:40]
                if rest and key and key not in seen:
                    seen.add(key)
                    if q is None:
                        q, u = 1.0, "szt."
                        review.append(rest)
                    elif u is None:
                        u = "szt."
                        review.append(rest)
                    ings.append({"qty": round(q, 3), "unit": u, "ing": rest, "raw": body})
                continue
        if not name and len(body) > 3 and not NOISE.search(body):
            name = body[:70]
    return dict(name=name, servings=servings, ings=ings, steps=steps, review=review)


if __name__ == "__main__":
    all_r = json.load(open(SP + "/all_recipes.json", encoding="utf-8"))
    out = {}
    for k, r in all_r.items():
        p = parse(r["caption"] or "", r["name"])
        out[k] = dict(r, parsed=p, n_ing=max(len(r["file_ings"]), len(p["ings"])))
    json.dump(out, open(SP + "/parsed.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    good = [k for k, v in out.items() if v["n_ing"] >= 3]
    tot_rev = sum(len(v["parsed"]["review"]) for v in out.values())
    print("Przepisow z >=3 skladnikami: %d / %d" % (len(good), len(out)))
    print("Pozycji bez rozpoznanej ilosci (domyslnie 1 szt., do sprawdzenia): %d" % tot_rev)
    sel = [(k, v) for k, v in out.items() if not v["file_ings"] and len(v["parsed"]["ings"]) >= 3]
    print("\n--- PROBKA (tylko z opisu) ---")
    for k, v in sel[:5]:
        p = v["parsed"]
        print("\n### %s   porcje=%s" % (p["name"], p["servings"]))
        for i in p["ings"][:15]:
            print("    %-6s %-10s %s" % (i["qty"], PRETTY.get(i["unit"], i["unit"]), i["ing"][:58]))
        for s in p["steps"][:2]:
            print("    KROK:", s[:95])
