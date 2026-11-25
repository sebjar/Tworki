# -*- coding: utf-8 -*-
"""Dwa zdjecia dania pod nazwa przepisu (kolumna B) w Przepisach i w Sugestiach."""
import os, shutil
from patch_weryf_lib import podmien

kop = os.path.join("kopie", "build_v2_przed_zdjeciami.py")
if not os.path.exists(kop):
    shutil.copy("build_v2.py", kop)

podmien("build_v2.py", [
    ('from openpyxl.utils import get_column_letter\n',
     'from openpyxl.utils import get_column_letter\n'
     'from openpyxl.drawing.image import Image as XLImage\n'
     'from openpyxl.drawing.spreadsheet_drawing import TwoCellAnchor, AnchorMarker\n'),
    ('def dv(ws, rng, src):\n',
     '# zdjecia dania: kwadraty 150 px pod nazwa przepisu, w tej samej komorce\n'
     'ZDJ_DIR = SP + "/zdjecia"\n'
     'ZDJ_PX, ZDJ_GORA, ZDJ_LEWO, ZDJ_ODST, EMU = 150, 22, 4, 6, 9525\n'
     'ZDJ_WIERSZ = (ZDJ_GORA + ZDJ_PX + 6) * 0.75          # wysokosc wiersza w punktach\n'
     '\n'
     '\n'
     'def zdjecia_przepisu(pid):\n'
     '    return [p for p in ("%s/%s_%d.jpg" % (ZDJ_DIR, pid, i) for i in (1, 2)) if os.path.exists(p)]\n'
     '\n'
     '\n'
     'def wstaw_zdjecia(ws, row, col0, pid):\n'
     '    """Kotwica "twoCell": przy filtrowaniu zdjecia chowaja sie razem z wierszem,\n'
     '    a przy sortowaniu jada razem z nim."""\n'
     '    pliki = zdjecia_przepisu(pid)\n'
     '    for i, p in enumerate(pliki):\n'
     '        img = XLImage(p)\n'
     '        img.width = img.height = ZDJ_PX\n'
     '        x = ZDJ_LEWO + i * (ZDJ_PX + ZDJ_ODST)\n'
     '        img.anchor = TwoCellAnchor(\n'
     '            editAs="twoCell",\n'
     '            _from=AnchorMarker(col=col0, colOff=x * EMU, row=row - 1, rowOff=ZDJ_GORA * EMU),\n'
     '            to=AnchorMarker(col=col0, colOff=(x + ZDJ_PX) * EMU, row=row - 1,\n'
     '                            rowOff=(ZDJ_GORA + ZDJ_PX) * EMU))\n'
     '        ws.add_image(img)\n'
     '    return len(pliki)\n'
     '\n'
     '\n'
     'def dv(ws, rng, src):\n'),
    ('    ws.row_dimensions[row].height = 15 if not r["steps"] else min(210, 13.5 * len(r["steps"]) + 10)\n',
     '    ws.row_dimensions[row].height = 15 if not r["steps"] else min(210, 13.5 * len(r["steps"]) + 10)\n'
     '    if wstaw_zdjecia(ws, row, 1, r["id"]):\n'
     '        ws.row_dimensions[row].height = max(ws.row_dimensions[row].height, ZDJ_WIERSZ)\n'),
    ('    ("Weryfikacja", "19-28.10.2026 (dwie rundy)',
     '    ("Zdjęcia", "Pod nazwą przepisu są dwa zdjęcia dania: okładka posta i klatka z drugiej "\n'
     '                "połowy filmu, gdzie zwykle widać gotowe danie (przy blogu i postach ze "\n'
     '                "zdjęciami — kolejne zdjęcie z posta). Klatki wybierałem automatycznie, więc "\n'
     '                "czasem trafi się etap gotowania zamiast talerza. Bez zdjęć zostały tylko "\n'
     '                "przepisy bez linku: %s."\n'
     '                % ", ".join(r["id"] for r in recipes if not zdjecia_przepisu(r["id"]))),\n'
     '    ("Weryfikacja", "19-28.10.2026 (dwie rundy)'),
    ('         [7, 44, 11, 20, 42, 74, 9, 10, 10, 10, 22])\n',
     '         [7, 46, 11, 20, 42, 74, 9, 10, 10, 10, 22])\n'),
    ('        ws.row_dimensions[row].height = 54\n',
     '        ws.row_dimensions[row].height = ZDJ_WIERSZ if wstaw_zdjecia(ws, row, 1, r["id"]) else 54\n'),
])
print("gotowe")
