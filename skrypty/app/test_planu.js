// Test logiki aplikacji bez przegladarki: atrapa DOM, potem plany, blokady, zamiany, wstawianie,
// liczba dni, ulubione i wykluczone, wyszukiwanie, jednostki i lista zakupow.
// Uzycie: node app/test_planu.js (po app_eksport.py). Kod wyjscia 1 = cos nie przeszlo.
const fs = require("fs"), path = require("path");
const t = fs.readFileSync(path.join(__dirname, "..", "..", "Przepisy-aplikacja.html"), "utf8");
const kod = t.slice(t.lastIndexOf("<script>") + 8, t.lastIndexOf("</script>"));
const el = () => ({ innerHTML: "", textContent: "", hidden: false, value: "", style: {}, dataset: {}, scrollTop: 0,
  classList: { add() {}, remove() {}, toggle() {}, contains: () => false }, appendChild() {}, replaceWith() {}, focus() {},
  addEventListener() {}, setAttribute() {}, select() {}, querySelector: () => ({ hidden: false }) });
global.document = { querySelector: () => el(), querySelectorAll: () => [], createElement: el, addEventListener() {}, body: { style: {} }, activeElement: null };
global.window = { scrollTo() {}, addEventListener() {} }; global.Image = function () {}; global.location = { hash: "" }; global.history = { replaceState() {} };
global.localStorage = { getItem: () => null, setItem() {} }; global.navigator = {};
const A = new Function(kod + `;return { S, BY, R, F, ULUB, BAN, HIST, lista, nowyPlan, zmienSesje, wstaw, ustawDni, cofnij,
  pula, potrzeby, bilans, ileKupic, tekstListy, ilosc, porcje, frac, wolneDni, naDzien, przelaczUlub, przelaczBan, film };`)();
const { S, BY } = A;
let bledy = 0;
const ok = (warunek, co) => { console.log((warunek ? "  OK   " : "  BLAD ") + co); if (!warunek) bledy++; };
const opis = () => S.plan.map(s => `${s.dni.join("")}:${s.id}${s.lock ? "*" : ""}`).join(" ");
function spojny(co) {
  const d = S.plan.flatMap(s => s.dni).sort((a, b) => a - b), ids = S.plan.map(s => s.id);
  const pelny = d.length === S.ndni && d.every((x, i) => x === i);
  const bezPowtorek = new Set(ids).size === ids.length;
  const dwa = S.plan.every(s => s.dni.length === 1 || (s.dni[1] === s.dni[0] + 1 && (BY[s.id].dwa.startsWith("Tak"))));
  ok(pelny && bezPowtorek && dwa, `${co} [${opis()}]`);
}

console.log("Plany");
const czasy = [], zestawy = [];
for (let i = 0; i < 6; i++) { const t0 = Date.now(); A.nowyPlan(); czasy.push(Date.now() - t0); spojny("plan " + (i + 1)); zestawy.push(S.plan.map(s => s.id).sort().join()); }
ok(new Set(zestawy).size >= 5, `kolejne plany sa rozne (${new Set(zestawy).size}/6 roznych)`);
ok(Math.max(...czasy) < 400, `ukladanie szybkie: ${czasy.join(", ")} ms`);
const b = A.bilans(A.potrzeby(S.plan));
ok(b.proc > 0 && b.proc <= 1, `wykorzystanie w zakresie: ${Math.round(b.proc * 100)}%`);

console.log("Blokady i cofanie");
S.plan.forEach(s => s.lock = false); S.plan[1].lock = true; const zost = JSON.stringify(S.plan[1]);
A.nowyPlan(); ok(S.plan.some(s => JSON.stringify(s) === zost), "zablokowane danie zostaje na swoich dniach po nowym planie");
const przed = JSON.stringify(S.plan); A.zmienSesje(0); ok(JSON.stringify(S.plan) !== przed, "„Inne danie” zmienia plan"); spojny("po zamianie");
ok(S.plan.some(s => JSON.stringify(s) === zost), "zamiana nie rusza zablokowanego");
A.cofnij(); ok(JSON.stringify(S.plan) === przed, "Cofnij przywraca poprzedni plan");

console.log("Wstawianie");
S.plan.forEach(s => s.lock = false);
const sas = S.plan.find(s => s.dni[0] >= 2 && s.dni[0] <= 5); sas.lock = true;
const dwuD = A.pula().find(r => r.dwa.startsWith("Tak") && !S.plan.some(s => s.id === r.id));
A.wstaw(dwuD.id, sas.dni[0] - 1);
ok(S.plan.some(s => s.id === sas.id && s.dni.join() === sas.dni.join()), "danie na 2 dni nie zjada zablokowanego sąsiada");
ok(S.plan.find(s => s.id === dwuD.id).dni.length === 1, "w takim razie wstawione danie dostaje 1 dzień"); spojny("po wstawieniu obok blokady");
const jednoD = A.pula().find(r => !r.dwa.startsWith("Tak"));
A.wstaw(jednoD.id, 6); ok(S.plan.find(s => s.id === jednoD.id).dni.join() === "6", "danie 1-dniowe w ostatni dzień"); spojny("po wstawieniu na ostatni dzień");
const jest = S.plan[0].id; A.wstaw(jest, 4); ok(S.plan.filter(s => s.id === jest).length === 1, "wstawienie dania, które już jest w planie, przenosi je (bez dubla)"); spojny("po przeniesieniu");

console.log("Liczba dni");
A.ustawDni(4); spojny("4 dni"); ok(S.plan.every(s => s.dni.every(d => d < 4)), "nic poza 4. dniem");
A.ustawDni(7); spojny("z powrotem 7 dni");
A.ustawDni(3); A.nowyPlan(); spojny("nowy plan na 3 dni"); A.ustawDni(7);

console.log("Mała pula i tryb 1 dzień");
S.kat = ["Zupa"]; S.plan = null; A.nowyPlan();
ok(new Set(S.plan.map(s => s.id)).size === S.plan.length, `same zupy: bez powtórek (${A.pula().length} w puli, wolne dni: ${A.wolneDni(S.plan).length})`);
S.kat = ["Obiad"]; S.dwa = false; S.plan = null; A.nowyPlan(); spojny("tryb 1 danie = 1 dzień"); ok(S.plan.length === 7, "7 gotowań"); S.dwa = true;

console.log("Ulubione i wykluczone");
const ul = A.pula().slice(0, 15).map(r => r.id); ul.forEach(id => A.ULUB.add(id));
let trafien = 0; for (let i = 0; i < 8; i++) { A.nowyPlan(); trafien += S.plan.filter(s => A.ULUB.has(s.id)).length; }
ok(trafien >= 12, `ulubione częściej w planie: ${trafien} trafień w 8 planach (15 ulubionych z ${A.pula().length})`);
ul.forEach(id => A.ULUB.delete(id));
const ban = A.pula().slice(0, 60).map(r => r.id); ban.forEach(id => A.BAN.add(id));
let banW = 0; for (let i = 0; i < 6; i++) { A.nowyPlan(); banW += S.plan.filter(s => A.BAN.has(s.id)).length; }
ok(banW === 0, "wykluczone nie trafiają do planu"); ban.forEach(id => A.BAN.delete(id));

console.log("Odhaczone zakupy");
S.kupione = { "pierś z kurczaka": 1 }; A.nowyPlan(); ok(!Object.keys(S.kupione).length, "nowy plan czyści odhaczone zakupy");

console.log("Wyszukiwanie i filtry");
const ile = q => { A.F.q = q; const n = A.lista().length; A.F.q = ""; return n; };
ok(ile("salatka") === ile("sałatka") && ile("salatka") > 0, `bez polskich liter: salatka=${ile("salatka")}, sałatka=${ile("sałatka")}`);
ok(ile("kurczak szpinak") > 0 && ile("kurczak szpinak") < ile("kurczak"), `dwa słowa naraz: ${ile("kurczak szpinak")} (kurczak: ${ile("kurczak")})`);
ok(ile("raziyyz") > 0, `po autorze: raziyyz=${ile("raziyyz")}`);
ok(ile("P080") === 1, "po ID");
A.F.bialko = "Ryby i owoce morza"; const ryby = A.lista(); A.F.bialko = null;
ok(ryby.length > 0 && ryby.every(r => r.ing.some(x => /łosoś|ryba|pstrąg|krewet|surimi|tuńczyk|dorsz/.test(x[0]))), `filtr ryby: ${ryby.length}, każdy ma rybę`);
A.F.kcal = 600; const lekkie = A.lista(); A.F.kcal = 0; ok(lekkie.every(r => r.kcal <= 600), `do 600 kcal: ${lekkie.length}`);
A.F.sort = "bialko"; const sb = A.lista(); A.F.sort = "id"; ok(sb.every((r, i) => !i || (sb[i - 1].b ?? -1) >= (r.b ?? -1)), "sortowanie po białku");
A.F.zr = "sug"; ok(A.lista().length === 20, "tylko sugestie: 20"); A.F.zr = "moje"; ok(A.lista().length === 147, "tylko Twoje: 147"); A.F.zr = "all";

console.log("Jednostki i liczby");
const fm = [[A.porcje(1), "1 porcja"], [A.porcje(2), "2 porcje"], [A.porcje(5), "5 porcji"], [A.porcje(2.75), "2¾ porcji"], [A.porcje(1.5), "1½ porcji"],
  [A.ilosc(.5, "łyżka"), "½ łyżki"], [A.ilosc(3, "ząbek"), "3 ząbki"], [A.ilosc(5, "ząbek"), "5 ząbków"], [A.ilosc(22, "ząbek"), "22 ząbki"],
  [A.ilosc(12, "łyżka"), "12 łyżek"], [A.ilosc(1, "pęczek"), "1 pęczek"], [A.ilosc(1234, "g"), "1235 g"], [A.ilosc(7.25, "g"), "7,3 g"], [A.frac(1.97), "2"]];
fm.forEach(([a, e]) => ok(a === e, `${e} → ${a}`));
const papryka = { n: "papryka czerwona", units: new Set(["g", "szt."]), g: 235, q: 0, per: { "szt.": 150, g: 1 } };
ok(A.ileKupic(papryka) === "2 szt.", `papryka 235 g + sztuki → ${A.ileKupic(papryka)}`);

console.log("Lista zakupów");
A.nowyPlan(); const m = A.potrzeby(S.plan);
let zgodne = true;
for (const s of S.plan) for (const [n, , , , g] of BY[s.id].ing) if (!m.get(n) || m.get(n).g < g * 0.2) zgodne = false;
ok(zgodne, "każdy składnik planu jest na liście");
const tekst = A.tekstListy(); ok(tekst.startsWith("Zakupy na obiady") && tekst.includes("\n- "), "kopiowany tekst listy ma nagłówek i pozycje");
S.kupione[[...m.values()].find(e => !A.R.some(() => false)).n] = 1;
ok(A.tekstListy().split("\n").length < tekst.split("\n").length, "odhaczone znikają z kopiowanej listy");

console.log("Linki do filmów");
const zLinkiem = A.R.filter(r => r.l), rodzaje = {};
zLinkiem.forEach(r => { const f = A.film(r); rodzaje[f ? f.krotko : "brak"] = (rodzaje[f ? f.krotko : "brak"] || 0) + 1; });
ok(zLinkiem.every(r => A.film(r) && A.film(r).href === r.l), `każdy przepis z linkiem ma przycisk: ${JSON.stringify(rodzaje)}`);
ok(A.R.filter(r => !r.l).every(r => A.film(r) === null), `bez linku: ${A.R.filter(r => !r.l).map(r => r.id).join(", ")}`);
ok(A.film(BY.P101).krotko === "Post" && A.film(BY.P001).krotko === "Film" && A.film(BY.P009).krotko === "Przepis", "P101 post ze zdjęciami, P001 film, P009 blog");

console.log(bledy ? `\n${bledy} BLEDOW` : "\nWSZYSTKO OK");
process.exitCode = bledy ? 1 : 0;
