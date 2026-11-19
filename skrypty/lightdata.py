# -*- coding: utf-8 -*-
"""Odchudzone odpowiedniki produktow: nazwa + wartosci na 100 g (kcal, B, T, W).

Bralem wersje, ktore realnie stoja na polce w polskim sklepie, a nie teoretyczne
"0% wszystkiego". Tam, gdzie odchudzona wersja psuje danie, jest o tym uwaga
w kolumnie "Uwaga" - te uwagi trafiaja do arkusza Ustawienia.
"""

# produkt kanoniczny -> (nazwa light, kcal, bialko, tluszcz, wegle, uwaga)
LIGHT = {
    "śmietana kremówka": ("śmietanka 12% do zup", 130, 3.0, 12, 3.5,
                          "Zwarzy się przy pomidorach, winie i cytrynie. Dosyp łyżkę mąki "
                          "albo hartuj: wlej kilka łyżek gorącego sosu do śmietany, dopiero "
                          "potem całość na patelnię."),
    "śmietana kwaśna": ("śmietana 12%", 130, 3.0, 12, 3.5,
                        "Do zimnych sosów bez różnicy. Na gorąco hartuj."),
    "śmietana 18%": ("śmietana 12%", 130, 3.0, 12, 3.5, ""),
    "serek śmietankowy": ("serek twarogowy light", 170, 8.0, 13, 4.5,
                          "Do sosów i nadzień bez różnicy. Do sernika na zimno gorzej trzyma."),
    "ser żółty": ("ser żółty light ~17% tł.", 270, 30.0, 17, 1.0,
                  "Gorzej się ciągnie i szybciej gumowacieje. Do zapiekania średnio, "
                  "do kanapek bez różnicy."),
    "cheddar": ("cheddar light", 280, 30.0, 18, 1.0,
                "Do mac and cheese odradzam — sos wychodzi ziarnisty."),
    "gouda": ("gouda light", 270, 30.0, 17, 1.5, ""),
    "mozzarella": ("mozzarella light", 200, 24.0, 11, 2.0,
                   "Puszcza więcej wody. Odsącz przed zapiekaniem."),
    "majonez": ("majonez light", 330, 1.0, 35, 4.0,
                "To majonez z wodą i skrobią. W sosie do sałatki ujdzie, na kanapce nie."),
    "mleko": ("mleko 0,5%", 35, 3.4, 0.5, 4.8,
              "W sosie nie poczujesz różnicy i kosztuje tyle samo."),
    "ser feta": ("feta light", 180, 16.0, 12, 3.0, ""),
    "masło": ("mix masła z olejem 60%", 540, 0.5, 60, 0.5,
              "Do smarowania i do sosów tak. Do ciasta i do smażenia na ostro nie — "
              "ma wodę, pryska i inaczej się rumieni."),
    "jogurt naturalny": ("jogurt naturalny 0%", 40, 4.5, 0.2, 4.7, ""),
    "śmietana": ("śmietana 12%", 130, 3.0, 12, 3.5, ""),
    "jogurt grecki": ("jogurt grecki 0%", 56, 10.0, 0.2, 3.6,
                      "Gęstszy i bardziej kwaśny. Na zimno bez różnicy, do gorącego sosu hartuj."),
    "syrop klonowy": ("syrop „zero” o smaku klonowym", 10, 0.0, 0.0, 2.5,
                      "To słodziki, nie cukier — do owsianki i lodów bez różnicy, do pieczenia średnio."),
    "mięso mielone wołowe": ("wołowina mielona chuda (do 5% tł.)", 134, 21.0, 5.5, 0.0,
                             "Mniej soczysta. Do burgerów dodaj łyżkę zimnej wody na 250 g mięsa, "
                             "do sosów bez różnicy."),
    "mleko zagęszczone": ("mleko zagęszczone light 4%", 103, 7.0, 4.0, 10.0,
                          "W kremowym sosie różnicy prawie nie czuć."),
}
