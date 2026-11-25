# -*- coding: utf-8 -*-
"""Druga runda poprawek po weryfikacji (produkty, ktorych nie ma w zrodle)."""
from patch_weryf_lib import podmien

podmien("curated_01.py", [
    ('(20, "g", "sriracha"), (1, "ząbek", "czosnek")]',
     '(20, "g", "sriracha"), (0.5, "łyżeczka", "czosnek granulowany")]'),
    ('wymieszaj majonez, sriracha i przeciśnięty czosnek.',
     'wymieszaj majonez, sriracha i suszony czosnek.'),
], od="C[17] = dict(", do=None)

podmien("curated_09.py", [
    ('note="Autor pokazuje przepis wyłącznie na nagraniu — kroki odtworzyłem z listy składników.",',
     'note="Autor pokazuje przepis wyłącznie na nagraniu — kroki odtworzyłem z listy składników. '
     'Sól, pieprz i czosnek granulowany do kurczaka oraz koperek do sosu dodałem od siebie '
     '— w Twoim pliku ich nie ma.",'),
    ('(150, "g", "panierka panko"), (2, "szt.", "jajko")',
     '(150, "g", "panierka panko"), (1, "szt.", "jajko")'),
], od="C[36] = dict(", do="steps=")

podmien("curated_06.py", [
    ('name="Burrito z indykiem (fit)", cat="Obiad", serv=2,\n',
     'name="Burrito z indykiem (fit)", cat="Obiad", serv=2,\n'
     '    note="Przypraw nie ma ani w Twoim pliku, ani w opisie filmu — oregano, kumin i chili '
     'to typowa meksykańska mieszanka, którą dobrałem sam.",\n'),
], od="C[61] = dict(", do="steps=")

podmien("curated_07.py", [
    ('name="Chrupiący kurczak w panko z piekarnika", cat="Obiad", serv=2,\n',
     'name="Chrupiący kurczak w panko z piekarnika", cat="Obiad", serv=2,\n'
     '    note="Autor podaje tylko 2 łyżki oleju i „ulubione przyprawy” — wpisałem paprykę '
     'i czosnek granulowany, a ilości panko, parmezanu i mąki oszacowałem.",\n'),
], od="C[76] = dict(", do="steps=")

podmien("curated_10.py", [
    ('"i nie pokazuje sposobu przygotowania — kroków nie było w źródle.",',
     '"i nie pokazuje sposobu przygotowania — kroków nie było w źródle. Składniki sosu to '
     'klasyczny beurre blanc (masło, szalotka, białe wino, ocet), ilości oszacowałem.",'),
], od="C[116] = dict(", do="ings=")
