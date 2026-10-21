# Korak 5P: stanje

| točka | stanje |
|---|---|
| 0 alternative iste vrste, oblik količine u uputama | gotovo (druga ili nepoznata vrsta: napomena "nije dimljena (posebna)") |
| 1 zlatni izlazi (tests/golden/) | gotovo: 20 scenarija (scripts/golden.py); usput ispravljena nedeterminističnost (dva poziva na istoj bazi razlikovala su se u 13 od 20) |
| 2 sažeta baza (scripts/build_compact.py, MM_DB) | gotovo: data/compact.duckdb 170 MB (chain_prices 0,48 M, store_products 13,2 M, price_exceptions 3,4 M; view clean.prices); zlatni izlazi 20/20 jednaki |
| 3 profiliranje plan_basketa | - |
| 4 ubrzanje | - |
| 5 mjerenja prije i poslije | - |

Hosting: nije dirano.

**Točka 2, napomene:** trgovina nema svaki proizvod lanca (popunjenost matrice trgovina × proizvod je 46 %), pa
sažeta baza čuva dostupnost po trgovini (`store_products`). Zato ima 170 MB, a ne ~104 MB kao procjena u 5-0. Iznimke
uključuju i redke iste cijene, ali drugog datuma (preneseni cjenik), pa je view točno jednak punoj tablici
(16 616 090 redaka). Usput: `.gitignore` je skrivao `data/brands.yaml`, `synonyms.yaml`, `yields.yaml`,
`assumptions.yaml` i `data/eval/`; sada su u repozitoriju.
