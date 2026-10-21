# Korak 5P: stanje

| točka | stanje |
|---|---|
| 0 alternative iste vrste, oblik količine u uputama | gotovo (druga ili nepoznata vrsta: napomena "nije dimljena (posebna)") |
| 1 zlatni izlazi (tests/golden/) | gotovo: 20 scenarija (scripts/golden.py); usput ispravljena nedeterminističnost (dva poziva na istoj bazi razlikovala su se u 13 od 20) |
| 2 sažeta baza (scripts/build_compact.py, MM_DB) | gotovo: data/compact.duckdb 170 MB (chain_prices 0,48 M, store_products 13,2 M, price_exceptions 3,4 M; view clean.prices); zlatni izlazi 20/20 jednaki |
| 3 profiliranje plan_basketa | gotovo (vidi niže) |
| 4 ubrzanje | gotovo: clean.staple_prices i clean.staple_items (po namirnici, složeno); palačinke 0,58 s, bolonjez 0,85 s, RSS 291 MB; zlatni 20/20 na obje baze |
| 5 mjerenja prije i poslije | gotovo (vidi niže); cilj ostvaren |

Hosting: nije dirano.

**Točka 2, napomene:** trgovina nema svaki proizvod lanca (popunjenost matrice trgovina × proizvod je 46 %), pa
sažeta baza čuva dostupnost po trgovini (`store_products`). Zato ima 170 MB, a ne ~104 MB kao procjena u 5-0. Iznimke
uključuju i redke iste cijene, ali drugog datuma (preneseni cjenik), pa je view točno jednak punoj tablici
(16 616 090 redaka). Usput: `.gitignore` je skrivao `data/brands.yaml`, `synonyms.yaml`, `yields.yaml`,
`assumptions.yaml` i `data/eval/`; sada su u repozitoriju.

**Točka 3, profil (sažeta baza, 3. ponavljanje, `prof.py` s omotačima oko funkcija):** import 0,76 s, otvaranje 0,02 s.

| faza | palačinke (7, Osijek) | bolonjez (7, Zagreb) |
|---|---|---|
| razrješavanje sastojaka (naziv, količina, oblik) | < 0,001 s | < 0,001 s |
| kandidati: SQL (`_rows_for`) | **4,36 s** (2 710 redaka) | **5,35 s** (12 160 redaka) |
| kandidati: atributi proizvoda | 0,14 s | 0,15 s |
| odabir pakiranja po trgovini | 0,011 s | 0,035 s |
| alternative | 0,001 s | < 0,001 s |
| spajanje i usporedba trgovina | < 0,001 s | 0,001 s |
| serijalizacija (sažet JSON) | 0,001 s | 0,001 s |
| **ukupno** | **4,55 s** | **5,63 s** |

Najveći RSS je 492 MB. Usko grlo je jedan SQL po sastojku (oko 0,6-0,8 s): spoj kandidata sa svih 16,6 M redaka
cijena (view nad 13,2 M + 3,4 M), iako sastojak ima samo nekoliko tisuća redaka.

**Točka 4, što je ubrzalo:**
1. `clean.staple_prices` i `clean.staple_items` (build i build_compact): cijene i proizvodi grupa svake namirnice,
   složeni po namirnici. Kandidati za sastojak čitaju ~1-10 tisuća redaka umjesto 16,6 M. Bez tih tablica (starija
   baza) kod radi kao prije.
2. Datum cjenika (`max(date)`) pamti se po vezi baze: na view-u sažete baze trajao je 0,3 s po pozivu alata.
3. DuckDB veza poslužitelja ima 2 dretve i memory_limit 300 MB (`MM_DUCKDB_THREADS`, `MM_DUCKDB_MEMORY`):
   RSS 431 → 371 MB, bez gubitka brzine.
4. Usput (točka 1): izbor pri jednakoj cijeni i nazivi grupa bili su nedeterministički (paralelni DuckDB);
   sada su zadani redoslijedom (product_id, naziv), pa su zlatni izlazi stabilni.

## Točka 5: prije i poslije (isti kod; funkcije alata kao u MCP pozivu; medijan 20 ponavljanja, jedan proces)

| mjerenje | prije: puna baza (1,14 GB) | poslije: sažeta baza (212 MB) |
|---|---|---|
| hladan start (import + otvaranje baze) | 0,77 + 0,03 s | 0,80 + 0,03 s |
| find_products brašno, Osijek | 0,39 s | **0,13 s** |
| plan_basket palačinke (7), Osijek | 3,92 s | **0,61 s** |
| plan_basket bolonjez (7), Zagreb | 4,27 s | **0,86 s** |
| najveći RSS (find ×21, plan_basket ×42) | 591 MB | **371 MB** |

Cilj (≤ 1,0 s za 7 sastojaka i RSS ≤ 400 MB na sažetoj bazi) je ostvaren; zlatni izlazi 20/20 jednaki na obje baze.
Preostalo vrijeme plan_basketa je 7 SQL upita kandidata (~0,06 s svaki) i 7 upita atributa (~0,02 s svaki).
Sam import (duckdb, mcp, pydantic) je ~100 MB RSS. Sažeta baza: `uv run python scripts/build_compact.py`, zatim
poslužitelj s `MM_DB=data/compact.duckdb`.
