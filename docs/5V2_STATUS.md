# Korak 5V2: manji paket za Vercel

| točka | stanje |
|---|---|
| 0 kako Vercel puni paket; Python 3.12; paket bez baze | gotovo |
| 1 veličina sažete baze po tablici i stupcu | gotovo |
| 2 smanjena baza (isti view-ovi, isti rezultat) | gotovo: **100,0 MB** (bilo 212,5; najmanje izmjereno 85,0 MB, ali sporije) |
| 3 zlatni izlazi i mjerenja na novoj bazi | gotovo: zlatni 20/20; brzina jednaka bazi iz 5P |
| 4 `vercel build --prod` s bazom | gotovo: 192,7 MB; zatim smanjeno, vidi 5 |
| 5 nijedna datoteka > 95 MB (Hobby upload) | gotovo: baza **92,3 MB** u jednoj datoteci, paket **184,9 MB** |

Ništa nije deployano.

## 0. Što ide u paket

**Ispravak 5V_STATUS:** dokumentacija kaže 500 MB za Python, ali alat za build (Vercel CLI 65.0.0, `@vercel/python`,
`dependency-externalizer`) radi drukčije:
- Prag je **225 MB** (`LAMBDA_SIZE_THRESHOLD_BYTES`). Paket do 225 MB ide cijeli (kod, datoteke iz `includeFiles`,
  ovisnosti u `_vendor/`).
- Iznad 225 MB, uz `uv.lock`, javni paketi s kompatibilnim wheelom **ne ulaze u paket**: instaliraju se pri hladnom
  startu u `/tmp/_vc_deps` (efemerni disk 500 MB), a u paket ulazi binarni `uv` (`_uv/`, ~50 MB). Ostatak
  (naše datoteke, privatni paketi, paketi bez kompatibilnog wheela i `uv`) mora stati u 225 MB. Inače:
  "exceeds the maximum function size (225 MB) even after optimizing dependencies".
- Kompatibilnost wheela: lokalno (bez `VERCEL_BUILD_IMAGE`) builder pretpostavlja **manylinux 2.17**. duckdb ima samo
  wheelove manylinux_2_26/2_28, pa je lokalno "bez kompatibilnog wheela" i uvijek u paketu (58 MB).
- "Large functions" (do 5 GB, beta) zaobilaze ovo uz `VERCEL_SUPPORT_LARGE_FUNCTIONS=1`; nisam ih koristio.
- Izvori: [Python runtime, controlling what gets bundled](https://vercel.com/docs/functions/runtimes/python#controlling-what-gets-bundled),
  [Python version](https://vercel.com/docs/functions/runtimes/python/python-version), kod
  `node_modules/vercel/node_modules/@vercel/python/dist/index.js`.

**Python 3.12:** Vercel uzima `.python-version` (3.14) čak i kad je u `.vercelignore`. Bez te datoteke uzima 3.14 iz
`requires-python = ">=3.12"` (najviša podržana). 3.12 bi tražio `requires-python` ograničen na 3.12, a to bi vezalo i
lokalni razvoj; ne može se odvojiti, a ne bi ni pomoglo, jer duckdb ostaje u paketu (manylinux 2.17 iznad).
`.python-version` je ostao 3.14.

**Paket bez baze** (`vercel build --prod`, zbroj datoteka iz `.vc-config.json` → `filePathMap`): **92,7 MB**; duckdb
57,7, cryptography 14,3, pydantic_core 4,9, pyyaml 2,7, pydantic 1,9, vercel_runtime 1,7, mcp 1,2 MB. Ispod 225 MB
nema vanjske instalacije, pa za paket ≤ 200 MB sažeta baza mora biti ≤ ~105 MB (sada 212,5 MB).

**Sigurnost:** u paketu je bio `.env.local` (i `.pytest_cache`). `.vercelignore` na `vercel build` ne djeluje, pa
`vercel.json` → `excludeFiles` sada izričito isključuje `.env*`, `.pytest_cache/**`, `__pycache__` i `_uv/**`;
provjereno: `.env*` više nije u paketu.

## 1. Sažeta baza iz 5P (212,5 MB), po tablici i stupcu

Metoda: `pragma_storage_info`, veličina segmenta = razmak do idućeg segmenta u istom bloku od 256 KiB (+ dodatni blokovi).

| tablica | MB | redaka | najveći stupci |
|---|---|---|---|
| price_exceptions | 59,2 | 3 396 054 | product_id 11,4 (FSST); price_per_unit 7,4, unit_price 7,0, price 6,4, price_eff 6,4, anchor_price 6,3 (BitPacking); store_id 2,5 |
| **store_products** | **55,2** | 13 220 036 | **product_id 44,1** (Dictionary/FSST), store_id 7,9, chain 3,2 |
| products | 39,5 | 478 181 | name 9,3, name_norm 8,0, match_norm 8,0, barcode 2,9, ean_norm 2,6 |
| staple_prices | 32,2 | 2 239 329 | ista struktura kao cijene, product_id 4,4 |
| chain_prices | 11,0 | 477 819 | product_id 1,9, cijene ~1 MB po stupcu |
| staple_items | 4,5 | 53 734 | name, match_norm, name_norm ~1 MB |
| ostalo | ~3,5 | | |

Zaključci: najviše prostora zauzimaju tekstualni ključevi (`product_id` i `store_id` u 13,2 M + 3,4 M redaka) i stupci
koje alati ne čitaju. Dodatne provjere:
- trgovine s istim asortimanom: 1 380 različitih od 1 535, pa grupiranje ne pomaže;
- "lanac minus nedostajući": samo 31 % manje redaka, a view bi morao graditi komplement pri upitu;
- datum je gotovo uvijek svojstvo trgovine (16 trgovina ima više datuma); iznimki samo zbog datuma ima 481 089.

## 2. Nova sažeta baza: 85,0 MB (`scripts/build_compact.py`)

Što je promijenjeno (izbor prema mjerenju iz točke 1):
1. **Cjelobrojni ključevi.** `clean.products.pk` (INTEGER) i `clean.stores.sk` (SMALLINT). Dostupnost, osnovne
   cijene i iznimke čuvaju ključeve umjesto teksta. Iznimke su složene po (proizvod, trgovina), jer su cijene istog
   proizvoda slične i bolje se sažimaju.
2. **Izostavljeni stupci koje alati ne čitaju** (provjereno pretragom koda search/basket/server):
   - cijene: `price`, `unit_price`, `price_date`;
   - proizvodi: `barcode`, `ean_valid`, `match_norm`, `category`, `unit`, `quantity`, `unit_hint`, `ean_note`,
     `ean_incoherent`, `hard_nonfood`.
3. **Cijene namirnica** kao i glavne: ključevi za retke jednake osnovnom (`staple_base_k`) i puni redci samo za
   iznimke (`staple_exceptions_k`). Proizvodi namirnice su samo ključevi (`staple_items_k`).
4. **View-ovi** `clean.prices`, `clean.staple_prices` i `clean.staple_items` imaju ista imena i iste stupce koje
   alati čitaju. `search.has_staple_prices` prepoznaje i view.
5. **Provjera pri svakom buildu:** svaki view mora vratiti točno iste retke kao puna baza (broj redaka i zbroj
   hash-eva redaka po svim preostalim stupcima), inače build pada.

| tablica | MB | redaka |
|---|---|---|
| price_exceptions_k (pk, sk, vrijednosti) | 26,5 | 3 395 582 |
| products (bez nekorištenih stupaca, + pk) | 26,0 | 478 181 |
| store_products_k (sk, pk) | 14,0 | 13 220 508 |
| staple_base_k (staple, sk, pk) | 5,0 | 1 775 283 |
| chain_prices_k (pk, vrijednosti) | 4,5 | 477 819 |
| staple_exceptions_k | 4,5 | 464 046 |
| ostalo (grupe, pravila, trgovine...) | 3,8 | |
| **ukupno (datoteka)** | **85,0** | |

Build traje ~2 min. DuckDB ima memory_limit 1,5 GB i 2 dretve, a RSS procesa je do 1,86 GB. Testovi: 971 prolazi.

### 2b. Konačni izbor: 100,0 MB (nakon mjerenja brzine)

Verzija od 85 MB je cijene namirnica držala kao ključeve (osnovni redak + iznimke), a proizvode namirnice kao view.
Svaki upit kandidata ih je spajao natrag s `products` i `chain_prices_k`. To je bilo **~20 % sporije** od baze iz 5P
(palačinke 1,08 s naspram 0,89 s, bolonjez 1,50 naspram 1,25 s, mjereno zajedno). Zato su `clean.staple_prices` i
`clean.staple_items` opet tablice, ali samo sa stupcima koje čita upit kandidata (`STAPLE_PRICE_COLS`: lanac,
trgovina, proizvod, date, stale_days, price_eff, is_special, price_per_unit, per_unit, unit_confidence,
price_per_kg_drained). To dodaje 15 MB, a brzina je ista kao prije.

| tablica | MB | redaka |
|---|---|---|
| products (bez nekorištenih stupaca, + pk) | 27,5 | 478 181 |
| price_exceptions_k (pk, sk, vrijednosti) | 26,5 | 3 395 582 |
| staple_prices (samo potrebni stupci) | 20,0 | 2 239 329 |
| store_products_k (sk, pk) | 14,0 | 13 220 508 |
| chain_prices_k (pk, vrijednosti) | 4,5 | 477 819 |
| staple_items | 3,0 | 53 734 |
| ostalo | 3,7 | |
| **datoteka** | **100,0** | |

## 3. Zlatni izlazi i mjerenja (nova baza)

Zlatni izlazi: **20/20 jednaki punoj bazi** (`MM_GOLDEN=1`, `scripts/golden.py --check --db data/compact.duckdb`).
Testovi: 971 prolazi.

Mjerenje kao u 5P (medijan 20 ponavljanja, jedan proces, funkcije alata). Stroj je sada sporiji nego u 5P (Firefox i
ostalo; sam import traje 1,2-1,5 s umjesto 0,8 s), pa je baza iz 5P izmjerena ponovno, u istim uvjetima:

| mjerenje | baza iz 5P (212,5 MB), sada | nova baza (100 MB), sada | baza iz 5P, mjereno u 5P |
|---|---|---|---|
| find_products brašno, Osijek | 0,19 s | 0,19 s | 0,13 s |
| plan_basket palačinke (7), Osijek | 0,89 s | **0,90 s** | 0,61 s |
| plan_basket bolonjez (7), Zagreb | 1,25 s | **1,25 s** | 0,86 s |
| najveći RSS | 368 MB | **330 MB** | 371 MB |

Nova baza je jednako brza kao stara, uz manji RSS. Cilj ≤ 1 s za bolonjez u ovim uvjetima nije ostvaren ni sa starom
bazom; u uvjetima iz 5P stara baza je imala 0,86 s, a nova bi trebala jednako. Usko grlo su upiti kandidata
(~0,1-0,14 s po sastojku) i atributi (~0,03 s po sastojku). Na Vercelu funkcija ima 1 vCPU, pa treba izmjeriti
tamo.

## 4. `vercel build --prod` (stvarno, s bazom od 100 MB)

Build prolazi (`Using Python 3.14 from .python-version`), bez "optimizing dependencies" i bez `_uv/`.
Veličina iz `.vc-config.json` → `filePathMap` (`scripts/vercel_bundle_size.py`):

| dio | MB |
|---|---|
| data/compact.duckdb | 100,0 |
| duckdb (.so) | 57,7 |
| cryptography | 14,2 |
| pydantic_core, pyyaml, pydantic, vercel_runtime, mcp, ostalo | 20,8 |
| **ukupno** | **192,7** (cilj ≤ 200, granica 225) |

Provjereno: u paketu nema `.env*`; od `data/` su samo `compact.duckdb` i `*.yaml`. `_uv/` nije nastao, a već je
u `.gitignore` i `.vercelignore`.

**Ispravci:**
- `docs/5V_STATUS.md` i `docs/DEPLOY.md`: granica je 225 MB, a ne 500 MB.
- GitHub workflow je veličinu mjerio s `du` na `.vercel/output`, što pokazuje ~1 MB, jer se datoteke funkcije samo
  navode u `filePathMap`. Sada koristi `scripts/vercel_bundle_size.py --max-mb 220`.

**Rezerva:** paket ima ~32 MB do granice od 225 MB. Sažeta baza raste s cjenicima, pa će CI javiti kad se približi.
Ako granica postane problem, mogućnosti su: verzija baze od 85 MB (~20 % sporiji plan_basket), izbaciti
`cryptography` (14 MB; povlači ga mcp, a mi ga ne koristimo) ili "Large functions" (`VERCEL_SUPPORT_LARGE_FUNCTIONS=1`).

## 5. Najviše 95 MB po datoteci (Hobby: `vercel deploy` odbija datoteke > 100 MB)

`vercel deploy --prebuilt --prod` je odbio bazu od 100 MB ("File size limit exceeded (100 MB)").

**Izbor: jedna datoteka od 92,3 MB, bez dijeljenja na više datoteka (ATTACH).** `clean.staple_prices` sada ima
cjelobrojne ključeve (`staple_prices_k`: staple, pk, sk i potrebni stupci, po (staple, pk, sk)), a view s istim imenom
spaja samo male `stores` i `products` po ključu. Za razliku od verzije od 85 MB, ne spaja osnovne cijene
(`chain_prices_k`, 478 tisuća redaka).

Usporedba u istim uvjetima (medijan 20 ponavljanja, dva uzastopna mjerenja):

| | verzija 100 MB | nova 92,3 MB |
|---|---|---|
| plan_basket palačinke (7), Osijek | 0,62 s / 0,91 s | 0,63 s / 0,92 s |
| plan_basket bolonjez (7), Zagreb | 0,86 s / 1,29 s | 0,92 s / 1,05 s |
| find_products brašno | 0,13 s / 0,19 s | 0,13 s / 0,19 s |
| najveći RSS | 332 MB | 369-378 MB |

(Prvi broj je mjeren u brzim uvjetima, kao u 5P, a drugi u sporijim.) Nova verzija je najviše ~7 % sporija, a ponekad
brža. Cilj ≤ 1 s i RSS ≤ 400 MB vrijede u uvjetima iz 5P. Dijeljenje na dvije datoteke (glavna ~77 MB i namirnice
~23 MB) zadržalo bi brzinu verzije od 100 MB, ali bi svako mjesto koje otvara bazu (poslužitelj, `search.connect`,
zlatni testovi, testovi) moralo priključiti i drugu datoteku, a view-ovi bi pokazivali u drugi katalog. To je više
posla i krhko, za razliku od ~0-7 % brzine.

**Provjere:**
- zlatni izlazi 20/20 (`MM_GOLDEN=1`, skripta i pytest);
- testovi: 972 prolazi;
- `vercel build --prod` prolazi: **184,9 MB** (baza 92,3, duckdb 57,7, cryptography 14,2 MB), najveća datoteka
  92,3 MB.

**`scripts/vercel_bundle_size.py --max-file-mb 95`** (zadano 95) pada ako je ijedna datoteka u paketu veća od 95 MB, a
workflow ga zove s `--max-mb 220 --max-file-mb 95`, pa ne deploya. Rezerva po datoteci je samo ~2,7 MB. Baza
raste s cjenicima, pa će CI javiti prije nego Vercel odbije upload. Sljedeći korak tada je dijeljenje baze ili
izbacivanje dodatnih stupaca.
