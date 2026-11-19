# -*- coding: utf-8 -*-
"""Czy danie nadaje sie na drugi dzien.

Reguly ida po kolei, pierwsza pasujaca wygrywa. Najpierw wyjatki wpisane recznie,
potem wzorce na nazwie i skladnikach. Werdykt jest jednym z:
  "Tak", "Tak, jest nawet lepsze", "Tak, ale ...", "Nie", "Nie dotyczy".
"""
import re

# --- recznie, po nazwie przepisu; ma pierwszenstwo nad wszystkim
WYJATKI = {
    "Carbonara": ("Nie",
                  "Sos z żółtek zwarzy się przy odgrzewaniu i zrobi się jajecznica — "
                  "to danie robi się i zjada od razu."),
    "Carbonara na patelni (Instagram)": ("Nie", "Sos z żółtek zwarzy się przy odgrzewaniu."),
    "Ceviche z krewetek": ("Nie",
                           "Surowe krewetki marynowane w limonce — drugiego dnia to już "
                           "nie jest bezpieczne."),
    "Ceviche z krewetek (wersja 2)": ("Nie", "Surowe krewetki w marynacie — tylko świeże."),
    "Metoda smażenia mięsa mielonego „brick”": (
        "Tak", "To technika, nie danie — usmażone mięso leży w lodówce 3 dni."),
    "Ogórki konserwowe": ("Nie dotyczy", "Przetwór, leży tygodniami."),
    "Dżem z borówek": ("Nie dotyczy", "Zamknięty stoi w lodówce do 6 miesięcy."),
    # --- reguly zlapaly te dania za szeroko, poprawiam recznie
    "Sałatka ziemniaczana z pieczonymi ziemniakami": (
        "Tak, na zimno", "Ziemniaki i feta spokojnie wytrzymają dwa dni w lodówce. "
                         "Nie odgrzewaj — to sałatka, je się ją zimną."),
    "Sałatka sylwestrowa z kurczakiem i orzo": (
        "Tak, na zimno", "Sałatka na makaronie trzyma się 2-3 dni. Dopraw przed podaniem, "
                         "bo orzo wypija dressing."),
    "Sałatka z brokułem i jajkiem": (
        "Tak, na zimno", "Wytrzyma dwa dni. Sos wymieszaj dopiero przed jedzeniem."),
    "Burger bowl": (
        "Tak, ale osobno", "Mięso i ryż odgrzej, a sałatę, pomidora i sos dorzuć świeże. "
                           "Odgrzana sałata to nic dobrego."),
    "Big Mac Smashburger Tacos": (
        "Tak, ale nie w mikrofali", "Odgrzej na suchej patelni — tortilla ma zostać sucha."),
    "Meal prep z Lidla na 3 dni (4 przepisy)": (
        "Tak", "To jest przepis pomyślany na 3 dni w lodówce. Jedyne, czego nie kroj "
               "wcześniej, to awokado."),
    "Naleśnikowe sushi na słodko (deser)": (
        "Nie dotyczy", "Je się na zimno. W lodówce wytrzyma dobę, potem naleśnik rozmięka."),
    "Burrito z kurczakiem tikka masala": (
        "Tak", "Autor zawija je i mrozi. Odgrzewanie: 2 minuty w mikrofali zawinięte w ręcznik "
               "papierowy, potem 6-8 minut w airfryerze w 190°C, żeby tortilla znów była "
               "chrupiąca."),
    "Trzy sałatki z ogórka (łosoś, śródziemnomorska, edamame)": (
        "Nie", "Ogórek puszcza wodę, a awokado ciemnieje — po nocy sałatka pływa. Zrób ją tuż "
               "przed jedzeniem; łososia albo wołowinę możesz przygotować dzień wcześniej."),
    "Turecki makaron Anny Paul": (
        "Tak, ale osobno", "Makaron z mięsem odgrzej, a sos jogurtowy podawaj zimny — podgrzany "
                           "jogurt się zważy. Masło paprykowe roztop na świeżo."),
    "Popcorn chicken w ostro-miodowej glazurze": (
        "Tak", "Autor robi to jako meal prep na 5 dni: dodaj łyżeczkę wody i odgrzej w mikrofali "
               "3 minuty pod uchyloną pokrywką, potem wymieszaj. Chrupiej wyjdzie z airfryera: "
               "180°C, 5-6 minut."),
    "Składany wrap z chilli con carne i masłem czosnkowym": (
        "Tak, ale nie w mikrofali", "Złożony wrap odgrzej na suchej patelni albo w piekarniku — "
                                    "w mikrofali placek rozmięknie. Możesz też trzymać chilli "
                                    "osobno i składać wrapy na świeżo."),
    "Spaghetti all'assassina": (
        "Tak, ale na patelni", "Odsmaż na rozgrzanej patelni z odrobiną oliwy, aż makaron znów "
                               "się przypiecze — w mikrofali zrobi się miękki."),
    "Spaghetti all'assassina (hannahyoussef)": (
        "Tak, ale na patelni", "Odsmaż na rozgrzanej patelni z odrobiną oliwy, aż makaron znów "
                               "się przypiecze — w mikrofali zrobi się miękki."),
    "Dirty fries po meksykańsku": (
        "Tak, ale straci chrupkość", "Frytki z mięsem i serem odgrzej w airfryerze albo "
                                     "piekarniku, 200°C przez 5-8 minut — w mikrofali zmiękną. "
                                     "Majonez i świeże dodatki dodaj dopiero po odgrzaniu."),
    "Chrupiąca sałatka Caesar z kurczakiem w panko": (
        "Tak, ale osobno", "Sałatę, sos i parmezan trzymaj osobno i łącz tuż przed jedzeniem — "
                           "inaczej liście zwiędną. Kurczaka w panko odgrzej w airfryerze albo "
                           "piekarniku, 180°C przez 5-8 minut; w mikrofali panierka zmięknie."),
    "Kurczak z airfryera na zapas + kanapka": (
        "Tak", "Kurczak jest pomyślany na zapas — w lodówce postoi 3-4 dni. Jedz go na zimno "
               "w kanapce albo odgrzej 3-4 minuty w airfryerze. Kanapkę składaj tuż przed "
               "jedzeniem, bo pieczywo nasiąka."),
    "Nocne bagietki bez wyrabiania": (
        "Tak, ale odśwież", "Najlepsze w dniu pieczenia. Następnego dnia skrop bagietkę wodą "
                            "i wstaw na 5 minut do piekarnika nagrzanego do 200°C — skórka znów "
                            "będzie chrupiąca. Można je też zamrozić."),
    "Bez przepisu (@mat.suchecki)": ("", ""),
    "Tacos 1 — niepełny wpis z Twojego pliku": ("", ""),
}

# --- wzorce sprawdzane TYLKO na nazwie
NAZWA = [
    (r"(?i)^sałatk|^salad|^\w+ sałatka\b", "Nie",
     "Liście zwiędną pod dressingiem. Możesz przygotować składniki osobno i złożyć "
     "dopiero przed jedzeniem."),
    (r"(?i)sushi", "Nie", "Ryż po nocy w lodówce twardnieje, a ryby się nie odgrzewa."),
    (r"(?i)mcchicken", "Tak, ale osobno",
     "Kotlety (i nuggetsy) odgrzej w airfryerze albo piekarniku, 180°C przez 6-8 minut — "
     "w mikrofali panierka zmięknie. Bułki z sałatą i sosem składaj na świeżo."),
    (r"(?i)burger|kanapk|bruschett|tost\b", "Nie",
     "Pieczywo nasiąka i robi się gumowate. Wsad zrób wcześniej, złóż na miejscu."),
    (r"(?i)owsianka|pudding chia|\blody\b|smoothie|koktajl", "Nie dotyczy",
     "To i tak jesz na zimno prosto z lodówki."),
    (r"(?i)brownie|sernik|muffin|ciasteczk|cookies|\bciasto\b", "Nie dotyczy",
     "Deser jesz w temperaturze pokojowej — w szczelnym pojemniku wytrzyma kilka dni."),
    (r"(?i)^sos |^tzatziki|^dip|^salsa|^pesto|^hummus", "Nie dotyczy",
     "Sos stoi w lodówce kilka dni, nie odgrzewasz go."),
    (r"(?i)kremow\w* (makaron|sos)|w kremowym sosie|alfredo|mac and cheese",
     "Tak, ale rozrzedź",
     "Sos gęstnieje w lodówce. Odgrzewaj na patelni z 2-3 łyżkami mleka albo wody."),
    # bez slowa "ryz" w komentarzu - inaczej builder nie dopisze uwagi o szybkim schlodzeniu ryzu
    (r"(?i)\bbowl\b", "Tak, ale osobno",
     "Ciepłe składniki odgrzej, a sosy i świeże warzywa dodaj zimne, już po odgrzaniu."),
    (r"(?i)chaczapuri|chlebek|chlebki|pizza|focaccia|rolgeski|ciasta francuskiego|"
     r"hash brown|placek ziemniaczany", "Tak, ale nie w mikrofali",
     "Odgrzej w piekarniku albo airfryerze, 180°C przez 5-8 minut — w mikrofali zrobi się "
     "miękkie i gumowate."),
    (r"(?i)gulasz|curry|tikka|butter chicken|chilli con carne|leczo|harira|"
     r"^zupa|bolognese|ragu|klopsik|pulpet|żeberka|papryka faszerowana", "Tak, jest nawet lepsze",
     "Po nocy w lodówce ma więcej smaku. Odgrzej pod przykryciem, na małym ogniu."),
]

# --- wzorce sprawdzane na nazwie + skladnikach + krokach
TRESC = [
    # \b, zeby "sos tatarski" do ryby z frytkami nie robil z niej surowego tatara
    (r"(?i)ceviche|\btatar\b", "Nie", "Surowa ryba albo mięso — tylko tego samego dnia."),
    (r"(?i)carbonar", "Nie", "Sos na żółtkach zwarzy się przy podgrzaniu."),
    (r"(?i)\bawokado\b|guacamole", "Nie, chyba że osobno",
     "Awokado ciemnieje przez noc. Odgrzej resztę, awokado dokrój świeże."),
    (r"(?i)chrupiąc|crunch|panierk|panko|panierowan|nugget|fish and chips|frytk|talark|"
     r"w cieście|głębokim oleju|płatk\w* kukurydz",
     "Tak, ale straci chrupkość",
     "Piekarnik albo airfryer, 180°C przez 8-10 minut. W mikrofali to, co chrupiące, "
     "zrobi się miękkie i gąbczaste."),
    (r"(?i)naleśnik|omlet|jajeczni|jajko sadzon", "Tak, ale ostrożnie",
     "Odgrzewaj krótko na patelni. W mikrofali jajko gumowacieje."),
    (r"(?i)tortill|wrap\b|burrit|quesadill|taco|\bpit[ay]\b|arayes|kebab|hot pocket",
     "Tak, ale nie w mikrofali",
     "Piekarnik albo sucha patelnia. W mikrofali placek zrobi się wilgotny i będzie się rwał."),
    (r"(?i)śmietana kremówka|alfredo|kremowy sos|kremowym sosie|mac and cheese",
     "Tak, ale rozrzedź",
     "Sos gęstnieje w lodówce. Odgrzewaj na patelni z 2-3 łyżkami mleka albo wody."),
    (r"(?i)\błosoś|pstrąg|ryba biała|krewetk|surimi", "Tak, ale krótko",
     "Rybę odgrzewaj delikatnie. Od nadmiaru ciepła wysycha i zaczyna nieprzyjemnie pachnieć."),
    (r"(?i)\bryż\b|risotto", "Tak, ale schłódź szybko",
     "Ryż wstaw do lodówki w ciągu godziny od ugotowania i zjedz w 24 h — inaczej rozwija "
     "się w nim Bacillus cereus. Odgrzewaj do gorąca, nie letnio."),
    (r"(?i)zapiekank|lasagn|gnocchi|faszerowan|z blachy|meal prep|one.?pan|jednogarnkow",
     "Tak", "Odgrzewaj pod przykryciem albo w piekarniku."),
]

DOMYSLNIE = ("Tak", "Odgrzewaj pod przykryciem, na małym ogniu albo w mikrofali "
                    "z odrobiną wody.")


def odgrzewanie(nazwa, skladniki="", kroki=""):
    """Zwraca (werdykt, komentarz). Pusty werdykt = przepis bez treści."""
    if nazwa in WYJATKI:
        return WYJATKI[nazwa]
    for wzor, werdykt, kom in NAZWA:
        if re.search(wzor, nazwa):
            return werdykt, kom
    tekst = " ".join([nazwa, skladniki, kroki])
    for wzor, werdykt, kom in TRESC:
        if re.search(wzor, tekst):
            return werdykt, kom
    return DOMYSLNIE


# --- moje propozycje (28.10.2026): tam, gdzie autor sam mowi, jak przechowywac,
# albo gdzie reguly zlapaly danie za szeroko (chili trafialo do tortilli)
WYJATKI.update({
    "Miski z kebabem tandoori i żółtym ryżem": (
        "Tak, ale schłódź szybko", "Kurczaka z ryżem odgrzej w mikrofali pod przykryciem albo na "
        "patelni. Sos z kolendry i mięty trzymaj osobno i dodawaj na zimno. Ryż wstaw do lodówki w ciągu godziny i zjedz w 24 h, odgrzewając do gorąca."),
    "Chili con carne": (
        "Tak, jest nawet lepsze", "Po nocy w lodówce ma więcej smaku. Odgrzej w garnku pod "
        "przykryciem z łyżką wody albo w mikrofali. Nadaje się też do mrożenia."),
    "Tortilla z kurczakiem i sosem czosnkowym": (
        "Tak, na zimno", "Ania zawija gotowe tortille w papier albo folię i zabiera do pracy — je "
        "się je na zimno. Na dłużej niż dzień trzymaj kurczaka, warzywa i sos osobno i zawijaj "
        "na świeżo."),
    "Wrapy z kurczakiem po koreańsku z surówką z ogórka": (
        "Tak, ale osobno", "Kurczaka odgrzej na patelni albo w mikrofali, a surówkę i sos trzymaj "
        "osobno w lodówce i zawijaj na świeżo w podgrzaną tortillę."),
    "Ryż zapiekany jak pizza z pepperoni": (
        "Tak, można mrozić", "Autor mrozi porcje i odgrzewa je 5-7 minut w mikrofali, a na "
        "wierzch sypie trochę parmezanu. Ryż wstaw do lodówki w ciągu godziny i zjedz w 24 h, odgrzewając do gorąca."),
    "Miski z ryżem, chili i sosem serowym": (
        "Tak, można mrozić", "Autor mrozi porcje: z zamrażarki 5-6 minut w mikrofali pod "
        "przykryciem, potem 5-6 minut odstawić, nadal przykryte. Z lodówki wystarczą "
        "2-3 minuty. Ryż wstaw do lodówki w ciągu godziny i zjedz w 24 h, odgrzewając do gorąca."),
    "Miski z kurczakiem shawarma": (
        "Tak, można mrozić", "Autor mrozi miski i odgrzewa w mikrofali. Sos jogurtowy trzymaj "
        "osobno i dodaj na zimno. Ryż wstaw do lodówki w ciągu godziny i zjedz w 24 h, odgrzewając do gorąca."),
    "Miski z kurczakiem i sałatką z pieczonej kukurydzy": (
        "Tak, ale osobno", "Kurczaka z ryżem odgrzej, a sałatkę z kukurydzy (jogurt, majonez, "
        "feta) trzymaj w osobnym pojemniku i jedz na zimno. Ryż wstaw do lodówki w ciągu godziny i zjedz w 24 h, odgrzewając do gorąca."),
    "Quesadille z kurczakiem chipotle": (
        "Tak, można mrozić", "Po ostudzeniu owiń w folię. Z zamrażarki: bez folii, w wilgotnym "
        "ręczniku papierowym 3-4 minuty w mikrofali, potem frytkownica, żeby była chrupiąca. "
        "Z lodówki: 30 sekund w mikrofali i frytkownica."),
    "Rolki z tortilli z kurczakiem, jalapeño i serem": (
        "Tak, można mrozić", "Owinięte w folię wytrzymają w zamrażarce miesiące. Odgrzewanie: bez "
        "folii, w mokrym ręczniku papierowym 4-6 minut w mikrofali, potem chwilę we frytkownicy "
        "albo na patelni."),
    "Chrupiący kurczak popcorn po koreańsku z ryżem": (
        "Tak", "Autor trzyma go w lodówce do 5 dni. Odgrzewaj z łyżeczką wody w mikrofali, "
        "3 minuty pod uchyloną pokrywką, potem wymieszaj — glazura i tak go zmiękcza. Ryż wstaw do lodówki w ciągu godziny i zjedz w 24 h, odgrzewając do gorąca."),
})
