# -*- coding: utf-8 -*-
"""Przepuszcza skoroszyt przez LibreOffice, zeby formuly mialy policzone wartosci.
Reszta testow czyta ten plik, bo openpyxl sam formul nie liczy."""
import os, shutil, subprocess, sys

SRC = r"C:\Users\Sebastian\Documents\Przepisy-planer\Przepisy-planer.xlsx"
WORK = os.path.dirname(SRC)
OUT = os.path.join(WORK, "_wartosci")
DOCEL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_wartosci.xlsx")
SOFFICE = r"C:\Program Files\LibreOffice\program\soffice.exe"


def _ubij_soffice():
    """LibreOffice pilnuje jednej instancji - wiszacy proces po cichu blokuje konwersje."""
    for exe in ("soffice.exe", "soffice.bin"):
        subprocess.run(["taskkill", "/F", "/IM", exe], capture_output=True)


def przelicz(src=SRC):
    got = os.path.join(OUT, os.path.basename(src))
    for proba in (1, 2):
        shutil.rmtree(OUT, ignore_errors=True)
        os.makedirs(OUT)
        r = subprocess.run([SOFFICE, "--headless", "--norestore", "--convert-to",
                            "xlsx:Calc MS Excel 2007 XML", "--outdir", OUT, src],
                           capture_output=True, timeout=500)
        if os.path.exists(got):
            break
        _ubij_soffice()
    if not os.path.exists(got):
        sys.exit("LibreOffice nie przeliczyl: %s" % r.stderr.decode("utf-8", "ignore")[:300])
    shutil.copy(got, DOCEL)
    shutil.rmtree(OUT, ignore_errors=True)
    return DOCEL


if __name__ == "__main__":
    print("zapisano:", przelicz())
