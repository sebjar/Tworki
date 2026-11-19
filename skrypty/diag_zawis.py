# -*- coding: utf-8 -*-
"""Diagnostyka: gdzie wisi zdj_pobierz.py - po 40 s zrzut stosu wszystkich watkow i wyjscie."""
import faulthandler, runpy, sys
faulthandler.dump_traceback_later(40, exit=True, file=open("diag_zawis.txt", "w"))
sys.argv = ["zdj_pobierz.py"] + sys.argv[1:]
runpy.run_path("zdj_pobierz.py", run_name="__main__")
