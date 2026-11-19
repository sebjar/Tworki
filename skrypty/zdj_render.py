# -*- coding: utf-8 -*-
"""Podglad: kilka pierwszych wierszy arkusza Przepisy ze zdjeciami, wyrenderowany przez LibreOffice do PNG."""
import os, subprocess
import openpyxl
from przelicz import SOFFICE
OUT = r"C:\Users\Sebastian\Documents\Przepisy-planer\Przepisy-planer.xlsx"

wb = openpyxl.load_workbook(OUT)
for n in wb.sheetnames:
    if n != "Przepisy":
        del wb[n]
ws = wb["Przepisy"]
ws.print_area = "A1:F5"
ws.page_setup.orientation = "landscape"
ws.page_setup.fitToWidth = 1
ws.sheet_properties.pageSetUpPr.fitToPage = True
wb.save("render_tmp.xlsx")
subprocess.run([SOFFICE, "--headless", "--norestore", "--convert-to", "png", "--outdir", ".", "render_tmp.xlsx"],
               check=True, timeout=180)
print(os.path.exists("render_tmp.png"))
