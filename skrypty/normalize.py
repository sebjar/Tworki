# -*- coding: utf-8 -*-
"""Sprowadza nazwy skladnikow do jednej, polskiej formy mianownikowej + przypisuje dzial sklepu."""
import re, unicodedata

# --- linie, ktore w ogole nie sa skladnikiem (makra, kalorie, marketing)
DROP = re.compile(r"(?i)"
                  r"^\s*(protein|carbs?|fat|calories|kcal|cal|makro|macros?|"
                  r"per serving|serving|net carbs|fibre|fiber|sugar content|"
                  r"[\d.,]+\s*(?:kcal|cal)\b|[a-z]\s*)\s*[:.]?\s*$"
                  r"|^\s*\d+\s*(?:g|kg)?\s*(?:protein|carbs?|fat)\b"
                  r"|\b\d+\s*calories\b|^(?:makes|serves)\s*\d+$"
                  # polskie makra i czasy - nigdy nie sa skladnikiem
                  r"|^\s*[\d.,]*\s*g?\s*(?:bia[lł]k\w*|t[lł]uszcz\w*|w[eę]glowodan\w*|"
                  r"kalori\w*|kcal|minut\w*|godzin\w*|porcj\w*|makro\w*)\s*[:.]?\s*$")

DROP_LINE = re.compile(r"(?i)woda z gotowania|pasta water|wody z gotowania")

DROP_WORDS = re.compile(r"(?i)\b(brand:|@[\w.]+|instagram|tiktok|cookbook|dm me|comment)\b")

# krotkie smieci, ktore przeciekly z opisow jako "skladnik"
DROP_EXACT = {"yes", "notes", "note", "recipe", "przepis", "sos", "farsz", "dodatki",
              "sauce", "topping", "chrupiacy", "robisz wieczorem", "egzotyczny final dnia",
              "smacznego", "gotowe", "wykonanie", "przygotowanie", "sposob", "ok", "itd",
              "wody przyprawy", "mozna uzyc swiezego", "_______", "-", "--"}


def deacc(s):
    s = s.replace("ł", "l").replace("Ł", "L")
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


def base(s):
    """Zdejmuje opisy sposobu obrobki, nawiasy, przecinkowe dopiski."""
    s = s.lower().strip()
    s = re.sub(r"\(.*?\)", " ", s)
    # UWAGA: nie wycinamy "mielon\w+" — w "mięso mielone wołowe" to czesc nazwy
    # produktu, a nie sposob obrobki. Wczesniej ucinalo to nazwe do samego "mięso".
    s = re.sub(r"(?i)\b(pokrojon\w+|posiekan\w+|start[ayeą]\w*|do smaku|"
               r"w kostk[ęe]|w pi[óo]rka|w plastry|w s[lł]upki|na tarce\w*|drobno|grubo|"
               r"opcjonalnie|obran\w+|umyt\w+|ugotowan\w+|surow\w+|"
               r"chopped|minced|diced|grated|finely|freshly|to taste|optional|raw|cubed|"
               r"halved|sliced|shredded|peeled|room temperature|as needed|divided|"
               r"for (?:frying|cooking|topping|serving|garnish)|if using)\b.*$", " ", s)
    s = re.sub(r"[,;].*$", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip(" -,.:")


# --- slownik: fragment nazwy (bez ogonkow) -> (nazwa kanoniczna PL, dzial sklepu)
W = "Warzywa i owoce"; M = "Mięso i ryby"; N = "Nabiał i jaja"; P = "Pieczywo"
S = "Sypkie i makarony"; O = "Oleje i sosy"; K = "Konserwy i słoiki"
Z = "Przyprawy i zioła"; F = "Mrożonki"; D = "Napoje"; C = "Słodycze i przekąski"; I = "Inne"

CANON = [
    # --- POPRAWKI KOLIZJI: bez tych wpisow krotszy fragment wygrywal i podmienial
    # produkt na inny (ogorki konserwowe -> ogorek, skrobia -> kukurydza z puszki itd.)
    ("ogorki konserwow", "ogórki konserwowe", K),
    ("serek smietankow", "serek śmietankowy", N),
    ("skrobia kukurydzian", "skrobia kukurydziana", S),
    ("udka z kurczaka", "udka z kurczaka", M), ("udziec z kurczaka", "udka z kurczaka", M),
    ("passata pomidorow", "passata pomidorowa", K),
    ("pomidory z puszki", "pomidory z puszki", K),
    ("maka chlebowa", "mąka chlebowa", S), ("maka tortowa", "mąka tortowa", S),
    ("orzechy nerkowca", "orzechy nerkowca", C),
    ("makaron udon", "makaron udon", S), ("makaron orzo", "makaron orzo", S),
    ("smietana kwasna", "śmietana kwaśna", N),
    ("bulion w proszku", "bulion w proszku", K),
    ("ryz basmati", "ryż basmati", S), ("wino biale", "wino białe", D),
    ("pieprz ziolowy", "pieprz ziołowy", Z),
    # to sa osobne produkty na polce, nie warianty tego samego
    ("sos sojowy jasny", "sos sojowy jasny", O),
    ("sos sojowy ciemny", "sos sojowy ciemny", O),
    ("bialy pieprz", "biały pieprz", Z), ("cukier brazowy", "cukier brązowy", S),
    # --- mieso i ryby
    ("piers z kurczaka", "pierś z kurczaka", M), ("piersi z kurczaka", "pierś z kurczaka", M),
    ("piers kurczaka", "pierś z kurczaka", M), ("filet z kurczaka", "pierś z kurczaka", M),
    ("chicken breast", "pierś z kurczaka", M), ("chicken thigh", "udka z kurczaka", M),
    ("chicken", "kurczak", M), ("kurczak", "kurczak", M), ("kurczaka", "kurczak", M),
    ("poledwiczki", "polędwiczki z kurczaka", M),
    ("mieso mielone wolowe", "mięso mielone wołowe", M),
    ("mieso mielone z kurczaka", "mięso mielone z kurczaka", M),
    ("mieso mielone z indyka", "mięso mielone z indyka", M),
    ("mieso mielone wieprzowe", "mięso mielone wieprzowe", M),
    ("mielonej piersi z kurczaka", "mięso mielone z piersi kurczaka", M),
    ("mieso mielone z piersi kurczaka", "mięso mielone z piersi kurczaka", M),
    ("mielona piers z kurczaka", "mięso mielone z piersi kurczaka", M),
    ("minced chicken", "mięso mielone z kurczaka", M),
    ("mieso mielone", "mięso mielone", M),
    ("miesa mielonego", "mięso mielone", M), ("mielonej wolowiny", "mięso mielone wołowe", M),
    ("ground beef", "mięso mielone wołowe", M), ("mince", "mięso mielone", M),
    ("mieszanka warzyw", "mieszanka warzyw stir-fry", W),
    ("beef strips", "wołowina w paskach", M), ("beef", "wołowina", M), ("wolowin", "wołowina", M),
    ("indyk", "indyk", M), ("turkey", "indyk", M), ("chorizo", "chorizo", M),
    ("boczek", "boczek", M), ("bacon", "boczek", M), ("salmon", "łosoś", M), ("losos", "łosoś", M),
    ("shrimp", "krewetki", M), ("krewetk", "krewetki", M), ("white fish", "ryba biała", M),
    ("cod", "dorsz", M), ("pstrag", "pstrąg", M), ("trout", "pstrąg", M), ("surimi", "paluszki surimi", M), ("pork", "wieprzowina", M),
    ("sausage", "kiełbasa", M), ("kielbas", "kiełbasa", M), ("pepperoni", "pepperoni", M),
    # --- nabial i jaja
    ("jajk", "jajko", N), ("jaja", "jajko", N), ("egg", "jajko", N),
    ("heavy cream", "śmietana kremówka", N), ("smietana kremow", "śmietana kremówka", N),
    ("smietana 30", "śmietana kremówka", N), ("smietank", "śmietana", N),
    ("smietana 12", "śmietana 12%", N), ("smietana 18", "śmietana 18%", N),
    ("smietan", "śmietana", N), ("double cream", "śmietana kremówka", N),
    ("sour cream", "śmietana kwaśna", N), ("cream cheese", "serek śmietankowy", N),
    ("serek", "serek śmietankowy", N), ("greek yogurt", "jogurt grecki", N),
    ("jogurt greck", "jogurt grecki", N), ("jogurt naturaln", "jogurt naturalny", N),
    ("jogurt", "jogurt naturalny", N), ("yogurt", "jogurt naturalny", N),
    ("cottage cheese", "serek wiejski", N), ("serek wiejski", "serek wiejski", N),
    ("twarog", "twaróg", N), ("serek kanapkow", "serek śmietankowy", N),
    ("skyr", "skyr", N),
    ("parmezan", "parmezan", N), ("parmesan", "parmezan", N),
    ("parmigiano", "parmezan", N), ("grana padano", "grana padano", N),
    ("mozzarella", "mozzarella", N), ("mozarella", "mozzarella", N),
    ("cheddar", "cheddar", N), ("gouda", "gouda", N), ("gorgonzola", "gorgonzola", N),
    ("feta", "ser feta", N), ("halloumi", "halloumi", N), ("mascarpone", "mascarpone", N),
    ("ser salatkow", "ser sałatkowy", N), ("cheese", "ser żółty", N), ("ser", "ser żółty", N),
    ("maslo", "masło", N), ("butter", "masło", N), ("mleko", "mleko", N), ("milk", "mleko", N),
    ("kefir", "kefir", N),
    # --- warzywa i owoce
    ("czerwona cebula", "czerwona cebula", W), ("cebula czerwona", "czerwona cebula", W),
    ("red onion", "czerwona cebula", W), ("shallot", "szalotka", W), ("szalotk", "szalotka", W),
    ("spring onion", "dymka", W), ("green onion", "dymka", W), ("dymk", "dymka", W),
    ("szczypior", "szczypiorek", W), ("chives", "szczypiorek", W),
    ("cebul", "cebula", W), ("onion", "cebula", W),
    ("czosnek granulowan", "czosnek granulowany", Z), ("garlic powder", "czosnek granulowany", Z),
    ("suszony czosnek", "czosnek granulowany", Z),
    ("czosn", "czosnek", W), ("garlic", "czosnek", W),
    ("pomidorki koktajlow", "pomidorki koktajlowe", W), ("cherry tomato", "pomidorki koktajlowe", W),
    ("pomidor", "pomidor", W), ("tomato paste", "koncentrat pomidorowy", K),
    ("koncentrat", "koncentrat pomidorowy", K), ("pasta pomidorow", "koncentrat pomidorowy", K),
    ("passata", "passata pomidorowa", K), ("suszone pomidory", "suszone pomidory", K),
    ("tomato", "pomidor", W),
    ("papryka czerwona", "papryka czerwona", W), ("czerwona papryka", "papryka czerwona", W),
    ("papryka zielona", "papryka zielona", W), ("zielona papryka", "papryka zielona", W),
    ("bell pepper", "papryka", W), ("papryczk", "papryczka chili", W),
    ("ziemniak", "ziemniaki", W), ("potato", "ziemniaki", W),
    ("marchew", "marchewka", W), ("carrot", "marchewka", W),
    ("ogorek konserwow", "ogórki konserwowe", K), ("ogork", "ogórek", W), ("ogorek", "ogórek", W),
    ("gherkin", "ogórki konserwowe", K), ("pickle", "ogórki konserwowe", K),
    ("cucumber", "ogórek", W),
    ("salata lodow", "sałata lodowa", W), ("sallata", "sałata", W), ("salat", "sałata", W),
    ("lettuce", "sałata", W), ("roszponk", "roszponka", W), ("rukol", "rukola", W),
    ("szpinak mrozon", "szpinak mrożony", F), ("szpinak", "szpinak", W), ("spinach", "szpinak", W),
    ("brokul", "brokuł", W), ("broccoli", "brokuł", W),
    ("brukselk", "brukselka", W), ("brussels sprout", "brukselka", W),
    ("cukini", "cukinia", W), ("zucchini", "cukinia", W),
    ("pieczark", "pieczarki", W), ("mushroom", "pieczarki", W),
    ("seler", "seler naciowy", W), ("celery", "seler naciowy", W),
    ("awokado", "awokado", W), ("avocado", "awokado", W),
    ("imbir", "imbir", W), ("ginger", "imbir", W),
    ("cytryn", "cytryna", W), ("lemon", "cytryna", W), ("limonk", "limonka", W), ("lime", "limonka", W),
    ("borowk", "borówki", W), ("zurawin", "żurawina suszona", C),
    ("natka pietruszki", "natka pietruszki", W), ("pietruszk", "natka pietruszki", W),
    ("parsley", "natka pietruszki", W), ("bazyli", "bazylia", W), ("basil", "bazylia", W),
    ("koperek", "koperek", W), ("kopru", "koperek", W), ("dill", "koperek", W),
    ("kielki", "kiełki", W), ("bataty", "bataty", W), ("sweet potato", "bataty", W),
    ("kapust", "kapusta", W), ("cabbage", "kapusta", W), ("por ", "por", W),
    ("mix salat", "mix sałat", W), ("stir fry mix", "mieszanka warzyw stir-fry", W),
    # --- sypkie, makarony, pieczywo
    ("makaron penne", "makaron penne", S), ("makaron spagetti", "makaron spaghetti", S),
    ("spaghetti", "makaron spaghetti", S), ("fettuccine", "makaron fettuccine", S),
    ("rigatoni", "makaron rigatoni", S), ("orzo", "makaron orzo", S),
    ("udon", "makaron udon", S), ("noodle", "makaron", S), ("makaron", "makaron", S),
    ("pasta", "makaron", S),
    ("ryz jasminow", "ryż jaśminowy", S), ("ryz parboiled", "ryż parboiled", S),
    ("ryz", "ryż", S), ("rice", "ryż", S),
    ("gnocchi", "gnocchi", S), ("platki owsiane", "płatki owsiane", S), ("oats", "płatki owsiane", S),
    ("maki", "mąka", S), ("maka", "mąka", S), ("flour", "mąka", S),
    ("skrobia", "skrobia ziemniaczana", S), ("cornflour", "skrobia kukurydziana", S),
    ("cornstarch", "skrobia kukurydziana", S),
    ("bulka tarta", "bułka tarta", S), ("panko", "panierka panko", S), ("panierk", "panierka panko", S),
    ("baking powder", "proszek do pieczenia", S), ("proszek do pieczenia", "proszek do pieczenia", S),
    ("cukier", "cukier", S), ("sugar", "cukier", S), ("brown sugar", "cukier brązowy", S),
    ("sezam", "sezam", Z), ("sesame seed", "sezam", Z), ("nasiona chia", "nasiona chia", S),
    ("orzech", "orzechy włoskie", C), ("walnut", "orzechy włoskie", C),
    ("pestek slonecznika", "pestki słonecznika", C), ("slonecznik", "pestki słonecznika", C),
    ("wrap", "tortilla", P), ("tortill", "tortilla", P), ("tortilla", "tortilla", P),
    ("placki do tacos", "tortilla", P), ("taco", "tortilla", P), ("nori", "nori", K),
    ("bulk", "bułka", P), ("bun", "bułka", P), ("chleb", "chleb", P), ("bread", "chleb", P),
    ("ciasto francuskie", "ciasto francuskie", F), ("ciasto do pizzy", "ciasto do pizzy", F),
    ("ciasto na pizz", "ciasto do pizzy", F), ("nachos", "nachosy", C),
    # --- oleje, sosy, konserwy
    ("oliwa", "oliwa z oliwek", O), ("olive oil", "oliwa z oliwek", O),
    ("olej sezamow", "olej sezamowy", O), ("sesame oil", "olej sezamowy", O),
    ("avocado oil", "olej z awokado", O), ("olej", "olej roślinny", O),
    ("vegetable oil", "olej roślinny", O), ("oil", "olej roślinny", O),
    ("sos sojow", "sos sojowy", O), ("soy sauce", "sos sojowy", O), ("dark soy", "sos sojowy ciemny", O),
    ("light soy", "sos sojowy jasny", O), ("oyster sauce", "sos ostrygowy", O),
    ("teriyaki", "sos teriyaki", O), ("bbq sauce", "sos BBQ", O), ("ketchup", "ketchup", O),
    ("majonez", "majonez", O), ("mayo", "majonez", O), ("musztard", "musztarda", O),
    ("mustard", "musztarda", O), ("sriracha", "sriracha", O), ("hot sauce", "sos ostry", O),
    ("chipotle", "sos chipotle", O), ("pesto", "pesto", K), ("ocet", "ocet", O),
    ("vinegar", "ocet", O), ("wino ryzow", "wino ryżowe", O), ("miod", "miód", C),
    ("honey", "miód", C), ("platki kukurydziane", "płatki kukurydziane", S),
    ("corn flakes", "płatki kukurydziane", S), ("cornflakes", "płatki kukurydziane", S),
    ("kukurydz", "kukurydza konserwowa", K), ("corn", "kukurydza konserwowa", K),
    ("pedow bambusa", "pędy bambusa", K), ("capers", "kapary", K), ("kapar", "kapary", K),
    ("bulion", "bulion", K), ("stock", "bulion", K), ("broth", "bulion", K),
    ("chicken powder", "bulion w proszku", K), ("puszka pomidorow", "pomidory z puszki", K),
    # --- przyprawy
    ("sol", "sól", Z), ("salt", "sól", Z), ("pieprz cayenne", "pieprz cayenne", Z),
    ("cayenne", "pieprz cayenne", Z), ("pieprz cytrynow", "pieprz cytrynowy", Z),
    ("pieprz czosnkow", "pieprz czosnkowy", Z), ("white pepper", "biały pieprz", Z),
    ("black pepper", "pieprz", Z), ("pieprz", "pieprz", Z), ("pepper", "pieprz", Z),
    ("papryka wedzon", "papryka wędzona", Z), ("smoked paprika", "papryka wędzona", Z),
    ("papryka slodk", "papryka słodka", Z), ("papryka ostr", "papryka ostra", Z),
    ("paprika", "papryka słodka", Z), ("papryki mielonej", "papryka mielona", Z),
    ("platki chilli", "płatki chilli", Z), ("chilli flakes", "płatki chilli", Z),
    ("chili flakes", "płatki chilli", Z), ("gochugaru", "gochugaru", Z),
    ("chili", "chili", Z), ("chilli", "chili", Z),
    ("oregano", "oregano", Z), ("italian seasoning", "zioła włoskie", Z),
    ("italian herbs", "zioła włoskie", Z), ("kumin", "kumin", Z), ("cumin", "kumin", Z),
    ("garam masala", "garam masala", Z), ("kurkum", "kurkuma", Z), ("turmeric", "kurkuma", Z),
    ("curry", "curry", Z), ("cajun", "przyprawa cajun", Z),
    ("onion powder", "cebula granulowana", Z), ("cebula granulowan", "cebula granulowana", Z),
    ("przyprawa gyros", "przyprawa gyros", Z), ("przyprawy do kurczaka", "przyprawa do kurczaka", Z),
    ("przyprawa do kurczaka", "przyprawa do kurczaka", Z), ("zlocista skork", "przyprawa do kurczaka", Z),
    ("lubczyk", "lubczyk", Z), ("tymianek", "tymianek", Z), ("thyme", "tymianek", Z),
    ("rozmaryn", "rozmaryn", Z), ("cynamon", "cynamon", Z), ("cinnamon", "cynamon", Z),
    # --- napoje / inne
    ("woda", "woda", D), ("water", "woda", D), ("piwo", "piwo", D), ("beer", "piwo", D),
    ("wodka", "wódka", D), ("vodka", "wódka", D), ("wine", "wino", D),
    # --- niemiecki (jeden z przepisow jest po niemiecku)
    ("rote zwiebel", "czerwona cebula", W), ("zwiebel", "cebula", W), ("pfeffer", "pieprz", Z),
    ("salz", "sól", Z), ("joghurt", "jogurt naturalny", N), ("saure sahne", "śmietana kwaśna", N),
    ("sahne", "śmietana", N), ("knoblauch", "czosnek", W), ("hahnchen", "kurczak", M),
    ("kase", "ser żółty", N), ("ei", "jajko", N), ("mehl", "mąka", S), ("butter", "masło", N),
    # --- pozostale czeste
    ("cilantro", "kolendra", W), ("coriander", "kolendra", W), ("kolendr", "kolendra", W),
    ("fresh herbs", "świeże zioła", W), ("cooking spray", "spray do smażenia", O),
    ("protein powder", "odżywka białkowa", C), ("vanilla", "wanilia", S),
    ("baking soda", "soda oczyszczona", S), ("soda oczyszczona", "soda oczyszczona", S),
    ("cukinia", "cukinia", W), ("bambus", "pędy bambusa", K),
    ("papryka", "papryka", W), ("papryke", "papryka", W), ("mieso", "mięso", M),
    ("syrop klonow", "syrop klonowy", C), ("schab", "schab", M), ("edamame", "edamame", F),
    ("erytrytol", "erytrytol", S), ("frytk", "frytki", F), ("lamb", "jagnięcina", M),
    ("chickpea", "ciecierzyca", K), ("ciecierzyc", "ciecierzyca", K),
    ("koperk", "koperek", W), ("wanili", "wanilia", S),
    # niemieckie
    ("zitronensaft", "sok z cytryny", W), ("cherry-tomaten", "pomidorki koktajlowe", W),
    ("tomaten", "pomidor", W), ("frische krauter", "świeże zioła", W),
    ("krauter", "świeże zioła", W), ("olivenol", "oliwa z oliwek", O),
    ("senf", "musztarda", O), ("nudeln", "makaron", S), ("reis", "ryż", S),
    # --- domkniecie dzialu "Inne"
    ("sos ostry", "sos ostry", O), ("sos ostrygow", "sos ostrygowy", O),
    ("sos bbq", "sos BBQ", O), ("harissa", "harissa", O), ("gochujang", "gochujang", O),
    ("pasta chili", "pasta chili", O), ("pasta z papryki", "pasta z papryki", O),
    ("olej chili", "olej chili", O), ("maslo orzechow", "masło orzechowe", C),
    ("ziola wloskie", "zioła włoskie", Z), ("przyprawa kebab", "przyprawa kebab", Z),
    ("przyprawa taco", "przyprawa taco", Z), ("przyprawa cajun", "przyprawa cajun", Z),
    ("sumak", "sumak", Z), ("majeranek", "majeranek", Z),
    ("galka muszkatolowa", "gałka muszkatołowa", Z),
    ("odzywka bialkowa", "odżywka białkowa", C), ("czekolada", "czekolada gorzka", C),
    ("truskawk", "truskawki", W), ("jablk", "jabłko", W), ("kiwi", "kiwi", W),
    ("soczewic", "soczewica", K), ("pico de gallo", "pico de gallo", K),
    ("pita", "pita", P), ("chlebki pita", "pita", P),
    ("ryba biala", "ryba biała", M), ("zeberka", "żeberka wieprzowe", M),
    ("jagniecina", "jagnięcina", M), ("drozdze", "drożdże instant", S),
    ("papier ryzow", "papier ryżowy", K), ("paluszki surimi", "paluszki surimi", M),
    ("labneh", "labneh", N), ("skyr", "skyr", N), ("gouda", "gouda", N),
    ("chilli con carne", "chilli con carne", K), ("nachosy", "nachosy", C),
    ("olej kokosow", "olej kokosowy", O), ("syrop klonow", "syrop klonowy", C),
    ("erytrytol", "erytrytol", S), ("frytki", "frytki", F),
    ("tortilla mala", "tortilla mała", P), ("woda gazowana", "woda gazowana", D),
    ("relish", "relish ogórkowy", K), ("oliwki", "oliwki", K),
    ("sos teriyaki", "sos teriyaki", O), ("edamame", "edamame", F),
    ("przyprawa gyros", "przyprawa gyros", Z),
    # --- dopisane przy przepisach z Instagrama (poza kolekcja "food")
    # KOLIZJA: "ocet jablkowy" lapal sie w "jablk" i stawal sie jablkiem
    ("ocet jablkow", "ocet jabłkowy", O), ("apple cider vinegar", "ocet jabłkowy", O),
    ("ocet ryzow", "ocet ryżowy", O), ("rice vinegar", "ocet ryżowy", O),
    ("ocet winny", "ocet winny", O),
    ("mieta", "mięta", W), ("mint", "mięta", W),
    ("groszek zielon", "groszek zielony", F), ("groszek", "groszek zielony", F),
    ("green peas", "groszek zielony", F), ("frozen peas", "groszek zielony", F),
    ("parowk", "parówki", M), ("hot dog", "parówki", M),
    ("ricotta", "ricotta", N), ("pecorino", "pecorino", N),
    ("szynka parmensk", "szynka parmeńska", M), ("prosciutto", "szynka parmeńska", M),
    ("szynka", "szynka", M), ("ham", "szynka", M),
    ("ciabatta", "ciabatta", P),
    ("pepperoni", "pepperoni", M), ("salami", "salami", M),
    ("anyz", "anyż gwiazdkowy", Z), ("star anise", "anyż gwiazdkowy", Z),
    ("estragon", "estragon", Z), ("tarragon", "estragon", Z),
    ("kakao", "kakao", S), ("cocoa", "kakao", S),
    ("sos pomidorow", "sos pomidorowy", K), ("marinara", "sos pomidorowy", K),
    ("pizza sauce", "sos pomidorowy", K),
    # --- dopisane przy przegladzie pazdziernikowym
    # KOLIZJA: "mleko kokosowe" stawalo sie zwyklym mlekiem (61 kcal zamiast ~200)
    ("mleko kokosow", "mleko kokosowe", K), ("coconut milk", "mleko kokosowe", K),
    # KOLIZJA: swieze drozdze to inny produkt i inna waga niz instant (3 g swiezych = 1 g suchych)
    ("drozdze swiez", "drożdże świeże", N), ("swieze drozdz", "drożdże świeże", N),
    ("smietanka slodk", "śmietana kremówka", N),
    ("ogorki kiszon", "ogórki kiszone", K), ("ogorek kiszon", "ogórki kiszone", K),
    ("kolendra ziarn", "kolendra ziarna", Z), ("nasiona kolendr", "kolendra ziarna", Z),
    ("kolendra mielon", "kolendra ziarna", Z),
    ("fasola czerwon", "fasola czerwona", K), ("kidney", "fasola czerwona", K),
    ("zoltk", "żółtko", N), ("egg yolk", "żółtko", N),
    ("worcester", "sos worcestershire", O),
    ("pancett", "boczek", M), ("nduja", "nduja", M),
    ("tajin", "tajin", Z), ("przyprawa wlosk", "zioła włoskie", Z),
    ("octu ryz", "ocet ryżowy", O), ("octu winn", "ocet winny", O),
    ("octu jablk", "ocet jabłkowy", O),
    ("chicken stock", "bulion", K), ("chicken broth", "bulion", K), ("beef broth", "bulion", K),
    ("bone broth", "bulion", K), ("chicken bouillon", "bulion w proszku", K),
    ("chipotle w adob", "chipotle w adobo", O), ("papryczki chipotle", "chipotle w adobo", O),
    ("papryczka chipotle", "chipotle w adobo", O),
    ("kminek", "kminek", Z), ("kmin rzymsk", "kumin", Z),
    ("pasta chipotle", "pasta chipotle", K), ("mleko zageszczon", "mleko zagęszczone", N),
    ("salsa", "salsa", K), ("bialko jaj", "białko jaja", N), ("bialka jaj", "białko jaja", N),
    ("jalapeno", "jalapeño", W), ("tandoori", "przyprawa tandoori", Z),
    ("ziele angielsk", "ziele angielskie", Z), ("fasola czarn", "fasola czarna", K),
    ("czarna fasol", "fasola czarna", K), ("ser topion", "ser topiony", N),
    ("pasta curry", "pasta curry", K), ("maslank", "maślanka", N),
    ("sok pomaranczow", "sok pomarańczowy", D), ("sok z pomarancz", "sok pomarańczowy", D),
]
# najdluzsze wzorce najpierw - zeby "piers z kurczaka" wygralo z "kurczak"
CANON.sort(key=lambda t: -len(t[0]))


def _words(s):
    return re.findall(r"[a-z0-9]+", s)


def _stem(w):
    """Ucina koncowke fleksyjna: papryka/papryki -> papryk, mleko/mleka -> mlek."""
    return re.sub(r"[aeiouy]$", "", w) if len(w) > 3 else w


def _stem_match(frag_stems, cand_stems):
    """Kazdy rdzen wzorca musi byc przedrostkiem kolejnego rdzenia kandydata.
    Dzieki temu 'sos sojow' lapie 'sosu sojowego', a 'papryka' lapie 'papryki'."""
    ci = 0
    for fs in frag_stems:
        hit = False
        while ci < len(cand_stems):
            cs = cand_stems[ci]
            ci += 1
            # przedrostek + limit dlugosci: bez tego rdzen "mies" (mieso)
            # lapal sie w "mieszanka"
            if (len(fs) >= 3 and cs.startswith(fs) and len(cs) <= len(fs) + 3) or cs == fs:
                hit = True
                break
        if not hit:
            return False
    return True


def _stem_match_any(frag_stems, cand_stems):
    """To samo co _stem_match, ale bez trzymania sie kolejnosci slow.
    Dzieki temu "chlebowa maka" trafia w "maka chlebowa", a nie w sam "chleb"."""
    for fs in frag_stems:
        if not any((len(fs) >= 3 and cs.startswith(fs) and len(cs) <= len(fs) + 4) or cs == fs
                   for cs in cand_stems):
            return False
    return True


CANON_W = [(re.compile(r"(?<![a-z0-9])" + re.escape(frag)), [_stem(w) for w in _words(frag)], n, s)
           for frag, n, s in CANON]
# wzorce wielowyrazowe - tylko rdzenie od 3 znakow, przyimki ("z", "do") pomijamy
CANON_MULTI = [([x for x in fw if len(x) >= 3], n, s) for _rx, fw, n, s in CANON_W]
CANON_MULTI = [t for t in CANON_MULTI if len(t[0]) >= 2]


def normalize(name):
    """Zwraca (nazwa_kanoniczna, dzial, czy_rozpoznano)."""
    if not name:
        return None, None, False
    raw = name.strip()
    if DROP.search(raw) or DROP_WORDS.search(raw) or DROP_LINE.search(raw):
        return None, None, False
    b = base(raw)
    if not b or len(b) < 2:
        return None, None, False
    d = deacc(b)
    if deacc(b).strip() in DROP_EXACT or re.fullmatch(r"[\d\s.,/%_-]*", d):
        return None, None, False
    cw0 = _words(d)
    # 0) najpierw wzorce wielowyrazowe, w dowolnej kolejnosci slow.
    #    Musi byc PRZED dopasowaniem doslownym, bo inaczej krotszy wzorzec
    #    lapie sie w przedrostku dluzszego slowa: "chleb" w "chlebowa",
    #    "jablk" w "jablkowy", "kukurydz" w "kukurydziana".
    cs0 = [_stem(w) for w in cw0]
    for fw, canon_name, section in CANON_MULTI:
        if _stem_match_any(fw, cs0):
            return canon_name, section, True
    # 1) dopasowanie doslowne, ale tylko od granicy slowa
    #    (bez tego "woda" lapalo sie w "weglowodanow", a "ser" w "deser")
    for rx, _fw, canon_name, section in CANON_W:
        if rx.search(d):
            return canon_name, section, True
    # 2) dopasowanie po rdzeniach slow (odmiana przez przypadki)
    cw = _words(d)
    for _frag, fw, canon_name, section in CANON_W:
        if _stem_match(fw, cw):
            return canon_name, section, True
    pretty = b[:1].upper() + b[1:]
    return pretty, "Inne", False
