# Korak 13: marka (proizvođač) uz svaki proizvod

## 13.1 Popunjenost stupca marke (stvarne arhive)

Izvor je `products.csv` po lancu, stupac `brand`. U `clean.products` pune baze i u sažetoj bazi (`compact.duckdb`,
također `clean.staple_items`) stupac je **zadržan i jednak sirovom**: 458 498 proizvoda, 348 859 s markom u obje
baze (cjenik 28.10.2026.). 5V2 i 12 ga nisu izbacili. U sažetoj bazi zauzima ~1,8 MiB u `products` i ~0,5 MiB u
`staple_items`.

Popunjenost (udio proizvoda s nepraznim `brand`), 28.10. / 19.10.:

| lanac | proizvoda | popunjeno | što je u stupcu |
|---|---:|---:|---|
| boso | 9 269 | 99,3 % / 99,2 % | mješavina: marke (LEDO, NIVEA) i dobavljači (NTL, EUROCOM, KB D.O.O.) |
| bure | 17 163 | 0 % / 0 % | prazno |
| djelo_vodice | 10 726 | 0 % / 0 % | prazno |
| dm | 22 135 | 100 % / 100 % | marke (Balea, dmBio, NIVEA) |
| dukat | 408 | 88,7 % / 88,7 % | marke; „Autres marques tarif”, „Société” su smeće |
| eurospin | 4 008 | 100 % / 100 % | marke, ali 2 065 (52 %) „NO BRAND” |
| gavranovic | 15 824 | 99,0 % / 99,1 % | uglavnom dobavljači s d.o.o. (NTL d.o.o., Orbico, AWT, Offertissima) |
| jadranka_trgovina | 12 284 | 0 % / 0 % | prazno |
| kaufland | 19 375 | 99,8 % / 99,8 % | marke (K-Classic, Podravka); 343 „#” |
| konzum | 22 138 | 97,4 % / 97,4 % | marke, VELIKA SLOVA (K PLUS, PODRAVKA) |
| ktc | 15 709 | 100 % / 100 % | uglavnom tvrtke s d.o.o./d.d. i gradom („PODRAVKA d.d. KOPRIVNICA”) |
| lidl | 7 012 | 64,9 % / 63,9 % | vlastite marke (Milbona, Deluxe, Pilos); 109 „-” |
| lorenco | 17 444 | 0 % / 0 % | prazno |
| metro | 13 524 | 86,5 % / 86,6 % | marke (METRO CHEF, ARO) |
| ntl | 18 340 | 99,6 % / 99,6 % | uglavnom dobavljači s d.o.o. (Koopman B.V., IRA Commerce, Orbico) |
| plodine | 76 957 | 93,4 % / 93,4 % | marke i „AMIGA NO BRAND”, „ITALIJA - UNOS”, „KINA - UVOZ” |
| ribola | 16 974 | 70,4 % / 70,2 % | marke |
| spar | 23 393 | 73,1 % / 73,1 % | marke (S-BUDGET, SPAR, DESPAR) |
| stanic | 2 599 | 100 % / 100 % | nisu marke nego skupine robe („SM. RIBLJI PROIZVODI NEP.”) |
| stridon | 31 646 | 46,2 % / 46,3 % | marke |
| studenac | 19 924 | 87,4 % / 87,7 % | marke i dobavljači („STUDENAC-ROBNA MARKA”, „ORBICO-P&G”, „DUKAT UKUPNO BEZ GAUDE”) |
| tommy | 19 893 | 99,8 % / 99,8 % | marke, dobavljači s d.o.o. i „SKLADIŠTE …” |
| trgocentar | 10 316 | 38,6 % / 38,8 % | proizvođač s gradom („PODRAVKA, KOPRIVNICA”, „VINDIJA - CEKIN”) |
| trgovina-krk | 33 858 | 96,4 % / 96,4 % | uglavnom dobavljači s d.o.o. (NTL D.O.O., KB D.O.O., TRGOVINA KRK D.D.) |
| vrutak | 14 312 | 99,9 % / 100 % | marke i dobavljači |
| zabac | 3 267 | 0 % / 0 % | prazno |
| branka, roto | — / 14 462, 9 201 | — / 0 %, 100 % | 28.10. nisu u arhivi |

Preko svih lanaca: 60 146 vrijednosti s „d.o.o.”, 7 168 s „d.d.”, 1 930 s B.V./GmbH/S.p.A./SRL/Ltd,
3 729 „… - UNOS/UVOZ”, 452 samo interpunkcija („#”, „-”), 5 512 „NO BRAND”, „OSTALO”, „ROBNA MARKA”, „NEPOZNAT”.

**Zaključak.** Stupac postoji i nije izbačen, ali „marka” je u njemu samo kod dijela lanaca. Pet lanaca ga nema
(bure, djelo_vodice, jadranka_trgovina, lorenco, zabac), a gavranovic, ktc, ntl i trgovina-krk u njega upisuju
dobavljača ili distributera (Orbico za Nutellu, Koopman), pa ga se ne smije prikazati kao marku bez čišćenja.
