# -*- coding: utf-8 -*-
"""Dopisuje przepisy z Instagrama zapisane poza kolekcja "food"."""
import io, json

NEW = [
    # (indeks w curated_13, kod posta, autor, nazwa robocza, opis)
    (129, "C-vD8K9IN9-", "johngs", "Healthy Chicken Meatballs with Orzo Salad",
     "Healthy Chicken Meatballs with Garlicy yogurt and Orzo Salad. Serves 4. "
     "For the meatballs 600g chicken breasts, 4 spring onions, mint, parsley, dill, "
     "4 cloves garlic, zest of 1/2 lemon, 1 small egg, 40g breadcrumbs, 2 tbsp olive oil, "
     "salt and pepper. For the salad 300g orzo, 100g frozen peas, 200g cherry tomatoes, "
     "1/2 cucumber, 1/2 red onion, herbs, juice of a lemon, 2 tbsp extra virgin olive oil. "
     "For the yogurt 300g Greek yogurt, 2 cloves garlic, herbs."),
    (130, "C-lKp9pS4Iz", "thejoshelkin", "Spaghetti Hot Dogs",
     "Spaghetti Hot Dogs are better than spaghetti, and hot dogs. INGREDIENTS + RECIPE "
     "2 jumbo hot dogs, 8oz spaghetti, 1/2 cup marinara, 1 cup grated mozzarella cheese, "
     "1/4 grated parm. RICOTTA SPREAD 1/2 cup ricotta cheese, 1/4 cup ground pecorino "
     "romano, 2 tbsp chopped parsley. GARLIC BUTTER SPREAD 1/2 cup melted garlic butter, "
     "1/4 cup ground parmesan cheese, 2 tbsp chopped parsley for garnish."),
    (131, "C5qj1mVC5QX", "thisisplanetfood", "Cheesy Tiger Garlic Bread",
     "CHEESY TIGER GARLIC BREAD! Recipe: Preheat your oven to 200C/180C fan. To make your "
     "garlic butter, mix together 250g softened butter, 2 tbsp olive oil, 8 finely chopped "
     "garlic cloves, 1 tsp parsley, 1/2 tsp salt and 1 tbsp parmesan. Cut slices into your "
     "tiger bread - around 2cm apart but do not cut all the way through to the bottom of "
     "the loaf. Smother the garlic butter into the bread slices and all over the top. Fill "
     "the bread slices with mozzarella slices as well as on top. Wrap the loaf in foil and "
     "bake in the oven for 15 minutes until the butter has melted and cheese is golden."),
    (132, "C0gFjp-SO_E", "marcus.costanzo", "Chopped sandwich",
     "RECIPE BELOW! In this video, I used: a handful of rocket leaves, a few slices of "
     "tomato, a few slices of red onion, pinch of salt and pepper, a few slices of fresh "
     "ham, a small bunch of basil leaves, 1 tablespoon of mayonnaise, 1 teaspoon of jarred "
     "chilli, half a roast capsicum, a few slices of prosciutto, a few slices of fresh "
     "sliced mozzarella, a small drizzle of honey, fresh ciabatta bread."),
    (133, "CzyLDMnPffG", "_aussiefitness", "High Protein Pepperoni Pizza Hot Pockets",
     "High Protein Pepperoni Pizza Hot Pockets. Easy Meal Prep! (Macros: Per Hot Pocket - "
     "Recipe Makes 8) 280 Calories 29gC | 6gF | 25gP. Ingredients: 410g Low Fat Greek "
     "Yoghurt, 400g Plain All Purpose Flour, 2 Tsp Baking Powder, Italian Herb Seasoning, "
     "Garlic Powder & Salt, 20g Low Fat Cheese per pizza pocket, 15g Pizza Sauce/Marinara, "
     "20g Sliced Mini Pepperoni. Reheat instructions: Microwave 3-5 Minutes, Air Fryer "
     "5-10 Minutes 180C, Oven 5-10 Minutes 200C."),
    (134, "Cz0t5Efv35n", "andyhearnden", "Blueberry Jam",
     "Blueberry Jam. Ingredients - 1kg blueberries, 200g sugar, 60ml apple cider vinegar, "
     "1 tsp fennel pollen (star anise also works great). Method 1. Wash the berries well "
     "and then drain. Place the berries into a bowl with the sugar and mix well. Cover with "
     "a tea towel and leave at room temperature for 3-4 hours. 2. Place the berries and any "
     "liquid into a large pot. Bring to a simmer, then cook on medium-low until it thickens, "
     "about 2 hours. 3. Sterilise your jam jars by boiling them for 5 to 10 minutes. Pour "
     "the hot jam into the jars. 4. The jam will last up to 6 months unopened."),
    (135, "Ctw7D9vMLh0", "dominikczeronek", "Tortilla po grecku",
     "Tortilla, ale po grecku. Składniki: (na ok 2 tortille) 400g kurczaka (ew tofu), "
     "4 łyżki oliwy, 1 łyżeczka papryki słodkiej, 0,5 łyżeczki estragonu, 0,5 łyżeczki "
     "oregano, sól, pieprz. Tzatziki: 200g jogurtu greckiego, 2 ząbki czosnku, "
     "2-3 ogórki gruntowe, 2 łyżki oliwy, 2 łyżki octu winnego, garść siekanego koperku, "
     "sól, pieprz. Dodatkowo: placki tortilli, pokrojone pomidorki, frytki."),
    (136, "CvetmKzL1yp", "_aussiefitness", "Honey Buffalo Chicken Mac & Cheese",
     "Honey Buffalo Chicken Mac & Cheese! Easy High Protein Meal Prep (Per Serve - 4 Total) "
     "512 Calories 43gC | 12gF | 79.5gP. Ingredients: 700g Diced Chicken Breast seasoned "
     "with salt, smoked paprika, garlic powder & onion powder, 350g Low Fat Cottage Cheese, "
     "65g Low Fat Cream Cheese, 35g Natural Cheddar, 80ml Low Fat Milk, 20ml Hot Sauce, "
     "320g Macaroni (dry weight), 1 Tbsp Honey & 1 Tbsp Buffalo Sauce. Steps: 1. Season "
     "diced chicken. 2. Add all of the ingredients for the mac & cheese sauce into a blender "
     "cup then blend for 2 minutes until smooth and creamy. 3. Prepare 320g of uncooked "
     "pasta. 4. Cook chicken on medium heat for 8-10 minutes then add 1 Tbsp of honey with "
     "1 Tbsp of buffalo sauce. 5. Mix cooked pasta with the sauce and divide into 4."),
    (137, "CvSWBb1s-OZ", "raziyyz", "Chicken Alfredo Mac & Cheese",
     "Chicken Alfredo Mac & Cheese. Pasta: 170g pasta. Chicken: 400g chicken breast chopped, "
     "2 tsp olive oil, 1 tsp salt, pepper, paprika, italian seasoning, onion powder, "
     "1 tsp minced garlic. Alfredo Cheese Sauce: 3/4 cup any milk, 1/4 cup pasta water, "
     "1/3 cup low fat cheese, 1/4 cup light parmesan, 2 tbsp light cream cheese, "
     "1 tsp italian seasoning, 1 tsp chili flakes. Servings: Approx. 3. Calories/Macros "
     "(Per Serving): Approx. 460 Calories 47g Protein 45g Carbs 10.5g Fat."),
    (138, "Cu4SPPyrnWM", "coocharz", "Inflacyjny Butter Chicken",
     "Inflacyjny Butter Chicken! Składniki: Kurczak: 600 g mięsa z udek z kurczaka, "
     "150 g jogurtu greckiego, 2 ząbki czosnku, 1 łyżeczka startego imbiru, 15 ml soku "
     "z cytryny, 1 łyżeczka soli, 1 łyżeczka garam masali, 1 łyżeczka słodkiej papryki, "
     "1/2 łyżeczki chilli. Sos: 1 cebula, 4 ząbki czosnku, 1 łyżka startego imbiru, "
     "2 łyżeczki garam masali, 2 łyżeczki słodkiej papryki, 1 łyżeczka kurkumy, 2 łyżki "
     "pasty pomidorowej, 1 puszka pomidorów, 150 ml wody, 200 ml śmietanki 18/30%, "
     "40 g masła."),
    (139, "C9P7s9KIbHQ", "veryfunny.123", "Classic brownie",
     "Here's a classic brownie recipe for you: Ingredients: 1 cup (225g) unsalted butter, "
     "2 cups (400g) granulated sugar, 4 large eggs, 1 teaspoon vanilla extract, 3/4 cup "
     "(90g) unsweetened cocoa powder, 1 cup (125g) all-purpose flour, 1/2 teaspoon salt, "
     "optional 1 cup (175g) chocolate chips. Instructions: 1. Preheat your oven to 350F "
     "(175C) and grease a 9x13 inch baking pan. 2. In a medium saucepan, melt the butter "
     "over low heat. Remove from heat and stir in sugar, eggs, and vanilla extract. "
     "3. Beat in cocoa, flour, and salt until just blended. 4. Spread the batter into the "
     "prepared pan. 5. Bake for 25 to 30 minutes. 6. Let the brownies cool before cutting."),
]

parsed = json.load(io.open("parsed.json", encoding="utf-8"))
ci = json.load(io.open("curate_input.json", encoding="utf-8"))
have = {r["key"] for r in ci}

added = 0
for idx, code, author, name, cap in NEW:
    key = "ig:" + code
    link = "https://www.instagram.com/%s/reel/%s/" % (author, code)
    if key in parsed or key in have:
        print("juz jest:", key)
        continue
    if len(ci) != idx:
        raise SystemExit("indeks sie nie zgadza: %s ma trafic na %d, a lista ma %d"
                         % (key, idx, len(ci)))
    parsed[key] = dict(
        author=author, caption=cap, cat="", file_ings=[], link=link, n_ing=0, name=name,
        platform="Instagram", servings=None, site_ings=[],
        sources=["zapisane na Instagramie, poza kolekcją food"], steps=[], typ="reel",
        parsed=dict(ings=[], name=name, review="", servings=None, steps=[]))
    ci.append(dict(author=author, blog=None, cap=cap, file_ings=[], key=key, link=link,
                   name=name, platform="Instagram", score=0, tr=""))
    added += 1

json.dump(parsed, io.open("parsed.json", "w", encoding="utf-8"), ensure_ascii=False)
json.dump(ci, io.open("curate_input.json", "w", encoding="utf-8"), ensure_ascii=False)
print("dopisano:", added, "| parsed:", len(parsed), "| curate_input:", len(ci))
