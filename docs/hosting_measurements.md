# Mjerenja za hosting (Korak 5-0; baza 19. i 20.10.2026., samo read_only; 8 jezgri, 7 GB RAM)

## 1. Veličina baze (1 137,7 MB) i tablica (MB = blokovi iz `pragma_storage_info` × 256 KiB)

| tablica | redaka | MB |
|---|---|---|
| clean.price_history (povijest, sada 2 dana) | 32 428 371 | 437,5 |
| clean.prices | 16 616 090 | 338,2 |
| main.prices / main.products (sirovo, samo build) | 17 533 737 / 478 181 | 206,0 / 17,8 |
| clean.products | 478 181 | 39,5 |
| ostalih 14 tablica (staples, grupe, trgovine...) | < 60 000 svaka | 3,8 |

## 2. Ujednačenost cijena (osnovna = najčešća price_eff para lanac-proizvod; svi lanci, 3 s, 210 MB RSS)

| lanac | trgovina | redaka | parova | ista cijena svuda | iznimki | sažeto |
|---|---|---|---|---|---|---|
| plodine | 155 | 6 124 402 | 76 515 | 43,6 % | 803 672 | 880 187 |
| konzum | 188 | 1 817 662 | 22 252 | 41,4 % | 489 741 | 511 993 |
| ntl | 343 | 1 561 810 | 18 263 | 72,1 % | 192 971 | 211 234 |
| tommy | 87 | 990 813 | 19 941 | 36,2 % | 322 649 | 342 590 |
| ribola | 61 | 535 241 | 16 981 | 18,9 % | 301 463 | 318 444 |
| spar / gavranovic / kaufland / ktc | 378 | 3 657 411 | 73 923 | 89,7-96,9 % | 68 320 | 142 243 |
| lidl | 116 | 801 413 | 6 922 | 99,0 % | 1 038 | 7 960 |
| ostalih 18 lanaca | 205 | 1 127 338 | 243 022 | 78,5 % | 154 052 | 397 074 |
| **ukupno** | 1 533 | 16 616 090 | 477 819 | **69,6 %** | 2 333 906 | **2 811 725 (17 %)** |

## 3. Sažeta baza bez povijesti (izgrađena u /tmp, izmjerena i obrisana)
`clean.*` bez prices/price_history i sirovih tablica, uz `prices_base` + `prices_exc` (iste cijene, drugog datuma → osnovni).
- **DuckDB: 103,6 MB** (prices_exc 45,8, products 39,2, prices_base 9,5 MB); izgradnja 14 s, 0,9 GB RSS.
- SQLite s istim podacima (2 indeksa, VACUUM): 483,1 MB, oko 4,7 puta veći; izgradnja 87 s.

## 4. Vrijeme i memorija (današnja baza od 1,1 GB, funkcije alata, sažet odgovor; najveći RSS **590 MB**)
Hladan start: import 1,16 s i otvaranje baze 0,04 s = **1,2 s** (+ ~0,5 s `uv run`); baza je bila u page cacheu.
plan_basket po sastojku ponovno skenira cijene svih trgovina u gradu (treba optimizirati).

| upit | prvi | medijan idućih 20 | najsporiji |
|---|---|---|---|
| find_products brašno, Osijek | 1,05 s | 0,59 s | 0,72 s |
| plan_basket palačinke (7), Osijek | 3,92 s | **3,89 s** | 4,18 s |
| plan_basket bolonjez (7), Zagreb | 6,83 s | **6,71 s** | 6,95 s |

## 5. Ovisnosti
duckdb 1.5.6 **58 MB** (jedan `.so`; wheel manylinux x86_64 **20,6 MB**), mcp 2.3.0 4 MB (+12 paketa, npr. cryptography
15 MB), pyyaml 4 MB. site-packages ima 112 MB, od čega ~10 MB samo za razvoj, pa je za rad potrebno **~100 MB**.

## 6. Stateless HTTP i ASGI
**Da.** `streamable_http_app(stateless_http=True, json_response=True)` je Starlette (ASGI) bez sesija; naš `http_app()`
dodaje RequestLog, HostGuard i RateLimit, a endpoint je `/mcp`. Vercel (Python) traži ASGI varijablu `app`, npr.
`api/index.py`: `app = http_app(create_server(db_path=...), host="0.0.0.0")`; lokalno
`MM_ALLOWED_HOSTS='*.vercel.app' uv run uvicorn api.index:app` (nije napravljeno ni deployano).
Proba u procesu (Host `mealmeter.vercel.app`): **bez ASGI lifespana pada** (`Task group is not initialized`; i stateless
traži pokrenut session manager). Uz omotač koji lifespan pokrene pri prvom zahtjevu, `initialize` i `tools/list` vraćaju
200 i 6 alata. Šalje li Vercel lifespan, treba provjeriti; omotač tu ovisnost uklanja.

## Preporuka
1. Sažeta DuckDB (≈ 104 MB) i ovisnosti (≈ 100 MB) zajedno su **≈ 205 MB, ispod 400 MB**; današnja baza (1,14 GB) ne stane.
2. Hladan start (import i baza) je **≈ 1,2 s, ispod 5 s**, plus prijenos ~100 MB baze ako se ne pakira uz kod.
3. Usko grlo je plan_basket (3,9-6,7 s po pozivu, 590 MB RSS): prije serverlessa ga treba ubrzati na sažetoj shemi.
4. Za Vercel u kodu trebaju sažeta shema (`prices_base` + `prices_exc`) i lifespan omotač iz točke 6.
5. SQLite se ne isplati: 4,7 puta veći od DuckDB-a za iste podatke.
