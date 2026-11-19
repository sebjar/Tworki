# -*- coding: utf-8 -*-
"""Uruchamia skrypt z tego folderu z krotka (8.3) sciezka jako katalogiem roboczym -
pelna sciezka folderu jest za dluga dla Windows."""
import os, runpy, sys
D = os.path.dirname(os.path.abspath(__file__))
os.chdir(D)
sys.path.insert(0, D)
skrypt = sys.argv[1]
sys.argv = sys.argv[1:]
runpy.run_path(os.path.join(D, skrypt), run_name="__main__")
