// Sklada aplikacje: dane/przepisy.json + dane/czasy.json + app/szablon.html -> index.html.
// Uzycie (z katalogu repo): node app/buduj.mjs
// Zdjecia leza w zdj/ obok index.html (zapisuje je skrypty/app_eksport.py).
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const KORZEN = path.join(path.dirname(fileURLToPath(import.meta.url)), "..");
const czytaj = p => fs.readFileSync(path.join(KORZEN, p), "utf8");

const dane = JSON.parse(czytaj("dane/przepisy.json"));
const czasy = JSON.parse(czytaj("dane/czasy.json"));

// czas przygotowania: [minuty pracy, minuty do podania, uwaga] - orientacyjnie;
// null w czasy.json = wpis bez przepisu, czasu nie da sie podac
const brak = [];
for (const r of dane.przepisy) {
  const c = czasy[r.id];
  if (c === null) continue;
  if (!c) { brak.push(r.id); continue; }
  r.cz = c.u ? [c.a, c.c, c.u] : [c.a, c.c];
}
if (brak.length) console.warn("Brak czasu w dane/czasy.json dla:", brak.join(", "));

const js = JSON.stringify(dane).replace(/<\//g, "<\\/");
const szablon = czytaj("app/szablon.html");
if (!szablon.includes("/*__DANE__*/null")) throw new Error("W szablonie brak znacznika /*__DANE__*/null");
const strona = szablon.replace("/*__DANE__*/null", () => js);

const html = '<!doctype html>\n<html lang="pl">\n<meta charset="utf-8">\n' +
  '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n' +
  '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}' +
  'body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n' + strona + "\n</html>\n";
fs.writeFileSync(path.join(KORZEN, "index.html"), html);
// node app/buduj.mjs <plik>: dodatkowo wersja do publikacji na claude.ai (bez doctype i <head>,
// claude.ai dokleja je sam); zdjecia publikuje sie obok jako zdj/*
if (process.argv[2]) fs.writeFileSync(process.argv[2], strona);

const zCzasem = dane.przepisy.filter(r => r.cz).length;
console.log(`index.html: ${dane.przepisy.length} przepisów, ${zCzasem} z czasem przygotowania, ${(html.length / 1e6).toFixed(2)} MB`);
