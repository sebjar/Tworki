# -*- coding: utf-8 -*-
"""Poprawki po recznej weryfikacji przepisow ze zrodlami (pazdziernik 2026)."""
import io


def podmien(plik, zmiany, od=None, do=None):
    t = io.open(plik, encoding="utf-8").read()
    a = t.index(od) if od else 0
    b = t.index(do, a) if do else len(t)
    blok = t[a:b]
    for stare, nowe in zmiany:
        n = blok.count(stare)
        if n != 1:
            raise SystemExit("%s: %r wystepuje %d razy" % (plik, stare, n))
        blok = blok.replace(stare, nowe)
    io.open(plik, "w", encoding="utf-8").write(t[:a] + blok + t[b:])
    print("OK", plik, od or "", len(zmiany))


