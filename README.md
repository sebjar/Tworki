# Planer posiłków

Domowa aplikacja z 167 przepisami (TikTok, Instagram, blogi), planerem całego tygodnia i listą zakupów.
Działa w przeglądarce, bez serwera: otwórz `index.html` (zdjęcia leżą obok, w `zdj/`).

## Co umie

- **Przepisy**: wyszukiwanie po składnikach, filtry (kategoria, mięso, kalorie, czas przygotowania),
  losowanie dania, karta przepisu ze skalowaniem porcji i trybem gotowania.
- **Tydzień**: śniadania, obiady i kolacje na 3–7 dni. Losowanie całego tygodnia albo tylko jednego
  posiłku, „Inne” dla pojedynczego dania, blokowanie dań, ręczny wybór, cofanie. Dania, które to
  zniosą, gotuje się raz na dwa dni. Plan dobiera dania dzielące świeże składniki, żeby mniej się
  marnowało, i może pilnować limitu czasu gotowania w dni robocze.
- **Czas przygotowania**: przy każdym przepisie orientacyjny czas pracy i czas do podania
  (z uwagą, gdy coś marynuje się lub rośnie), suma pracy na dzień i na tydzień.
- **Zakupy**: lista z całego planu, w całych opakowaniach ze sklepu, z odhaczaniem i kopiowaniem.

Stan (plan, ulubione, odhaczone zakupy) zostaje w przeglądarce (`localStorage`).

## Struktura

| Ścieżka | Co to jest |
| --- | --- |
| `index.html` | gotowa aplikacja (generowana, nie edytuj ręcznie) |
| `zdj/` | zdjęcia i miniatury do aplikacji (generowane) |
| `app/szablon.html` | kod aplikacji: HTML, CSS i JS |
| `app/buduj.mjs` | składa `index.html` z szablonu i danych |
| `app/test_planu.js` | testy logiki planu bez przeglądarki |
| `dane/przepisy.json` | dane przepisów (z arkusza, przez `skrypty/app_eksport.py`) |
| `dane/czasy.json` | czasy przygotowania: `a` minuty pracy, `c` minuty do podania, `u` uwaga |
| `Przepisy-planer.xlsx` | główny arkusz z przepisami |
| `skrypty/` | potok w Pythonie: zbieranie, normalizacja, makro, zdjęcia, eksport |

## Praca

Zmiana wyglądu lub logiki (wymaga tylko Node):

```
node app/buduj.mjs
node app/test_planu.js
```

Zmiana czasów: popraw wpis w `dane/czasy.json`, potem `node app/buduj.mjs`.

Zmiana przepisów w arkuszu (Python z `openpyxl` i `Pillow`):

```
python skrypty/uruchom.py build_v2.py
python skrypty/uruchom.py przelicz.py
python skrypty/uruchom.py app_eksport.py   # zapisuje dane/ i zdj/, potem sam woła app/buduj.mjs
```
