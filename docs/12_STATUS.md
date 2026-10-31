# Korak 12: sažeta baza preko 95 MB (dijagnoza i prijedlog, nije implementirano)

Workflow je pao na `vercel_bundle_size.py` („paket > 220 MB ili datoteka > 95 MB; ne deployam”) na dan kad je NTL
pao s 1 574 949 na 759 889 redaka, a preneseno je 813 169 cijena. Log nisam pročitao (`gh` nije prijavljen).
Mjerenja su na punoj bazi s cjenikom 28.10.2026. (DuckDB 1.5.6), a izgrađene baze su izvan repozitorija, u
`~/.cache/mm_sim/`. Veličine su u MiB (2^20), kao u `vercel_bundle_size.py`; po tablici i stupcu su procijenjene
iz `pragma_storage_info` (pomaci segmenata u blokovima od 256 KiB), a zbroj se slaže s datotekom unutar 1 %.

## 1. Dijagnoza

| baza | veličina | iznimke (`price_exceptions_k`) | `store_products_k` |
|---|---:|---:|---:|
| sažeta, cjenik 28.10. (bez prenesenih) | **92,8** | 2 833 369 | 14 145 043 |
| ista + simulirani NTL pad (810 770 redaka u 187/343 trgovine s jučerašnjim datumom, `stale_days` 1) | **95,5** | 3 397 519 | 13 580 893 |

Raspodjela (bez pada): products 25,2 (name 8,9, name_norm 7,7, ean_norm 2,6), price_exceptions_k 23,5
(price_per_unit 6,0, anchor_price 4,4, price_eff 4,3, sk 2,7), staple_prices_k 15,8 (price_per_unit 4,3,
price_eff 3,5, sk 2,8), store_products_k 14,8 (pk 14,4), chain_prices_k 4,5, staple_items 3,8, ostalo ~4.

**Uzrok.** `date` i `stale_days` su među stupcima vrijednosti osnovnog retka para (lanac, proizvod). Preneseni
redak ima jučerašnji datum, pa se razlikuje od osnovnog retka čak i kad je cijena ista. Kad je prenesena oko
polovica lanca, polovica njegovih redaka postaje iznimka s punim retkom vrijednosti: +564 k iznimaka (+3,7 MiB),
a `store_products_k` je 0,8 MiB manji, dakle ukupno **+2,7 MiB**.

**Koliko otpada na što:**
- Prenesene cijene (iznimke): ~2,7 MiB na dan NTL-ova pada. Koliko točno, ovisi o tome koliko je lanac velik i
  koliki je njegov dio prenesen.
- Namirnice iz Koraka 9–10 (14 novih: brokula, celer, cimet, cvjetača, kocka_za_juhu, kukuruzni_skrob, mahune,
  orasi, patlidžan, poriluk, ružmarin, svinjska_mast, tekući_temeljac, vino): 14,5 % redaka `staple_prices_k`
  (~2,3 MiB) i 18 % `staple_items` (~0,7 MiB), ukupno **~3 MiB**.
- Pravi problem je zaliha: bez prenesenih cijena baza je već 92,8 MiB (2,2 MiB ispod granice). Nove namirnice
  pojele su veći dio zalihe, a carry-forward ju je samo prešao. Bez promjene pada svaki dan kad se prenese velik
  lanac (Plodine 6,1 M redaka, Konzum 1,8 M).

## 2. Cilj

Uz rast od ~6 mjeseci i dalje barem 30 MiB rezerve: **datoteka ≤ 65 MiB i paket ≤ 190 MiB** (granice provjere su
95 i 220). Paket bez baze ima 92,7 MiB (5V2). Rast je pretpostavka od **~15 %** (~13 MiB), jer imam samo tri dana
povijesti: proizvodi 458–477 k, cijene 16,0–17,0 M, a rastu i broj lanaca u izvoru i broj namirnica (~0,2 MiB po
namirnici). Dakle sada je cilj baza ≤ ~84 MiB ukupno i ≤ ~56 MiB po datoteci.

## 3. Opcije (izmjereno na simuliranom NTL padu, najgori slučaj)

Brzina: 24 scenarija find_products i plan_basket iz `golden.py`, medijan 3 topla poziva; sadašnja shema
**19,4 s** ukupno (`basket_nepoznato` 7,7 s, `basket_free_text_tahini` 1,0 s). Svaka varijanta je provjerena
otiskom (broj redaka i zbroj hash-eva) prema punoj bazi: `prices` 16 978 412 redaka, `staple_prices` 2 655 708,
oba jednaka.

### (a) Prenesene cijene kompaktno: datum po trgovini

`date` i `stale_days` izlaze iz stupaca vrijednosti i idu u `clean.stores` (datum trgovine, `stale_days` =
datum cjenika − datum trgovine), pa view ne treba dodatni join. Cijela prenesena trgovina je tada „ista kao dan X”:
njezini redci su jednaki osnovnom retku i ostaju u `store_products_k`, gdje koštaju ~1 bajt po retku.
Uz to `staple_prices_k` ne sprema `price_per_unit`, `per_unit`, `unit_confidence` i `price_per_kg_drained`
nego ih view računa iz `products` (za proizvode s pakiranjem g/ml/kom i `pack_amount > 0`;
izračun daje 0 razlika). U `prices` ostaju spremljeni (vidi odbačene varijante).

- Veličina: **88,0 MiB** (s 95,5). Iznimaka 2 833 369 i uz 811 k prenesenih, dakle **carry-forward više ne
  povećava bazu**. staple_prices_k 16,0 → 10,8.
- Brzina: **18,2 s** prema 19,4 (`basket_nepoznato` 6,8 s prema 7,7).
- Rizik: nizak do srednji. Trgovina s djelomičnim padom ima dva datuma: preneseni redci moraju u iznimke sa
  svojim datumom (stupac `date` u iznimkama, NULL = datum trgovine), a isto i u `staple_prices_k`. Provjera otiska
  u `build_compact.py` ostaje. Sama nije dovoljna: jedna datoteka od 88 MiB je iznad 65.

Odbačene varijante iste ideje:
- izvedeni stupci računati i u `prices` view-u: 80,7 MiB, ali free_text 2,5–3,5× sporiji (`basket_nepoznato`
  18,7 s, tahini 2,5 s), jer se izrazi računaju nad cijelim view-om;
- rijetke iznimke (maska, samo stupci koji se razlikuju): još −1 MiB, a `basket_nepoznato` 27,5 s;
- datum u zasebnoj tablici `store_dates_k` uz skalarni podupit `max(date)`: isti broj MiB, ali sporije.

### (b) Dvije datoteke ispod 95 MB (ATTACH)

S (a): **A** = products 24,8 + staple_prices_k 10,8 + staple_items 3,8 + male tablice ~4 ≈ **44 MiB**;
**B** = price_exceptions_k 23,8 + store_products_k 14,8 + chain_prices_k 4,5 ≈ **43 MiB**. Uz +15 % rasta to je
~51 MiB po datoteci, dakle 44 MiB rezerve. Bez (a) bi bilo ~50 + 45 MiB, ali paket 188 MiB.

- Brzina: join između baza priključenih u isti DuckDB proces trebao bi biti jednako brz. Nije izmjereno.
- Rizik: srednji. View u A mora imenovati B punim imenom (`mmp.clean.…`), pa svaka točka koja otvara bazu mora
  priključiti B pod istim aliasom: `server._open` (ATTACH kao `mm`), `search.connect`, `build_compact.py`
  (provjera), `golden.py`, testovi, `vercel.json` (`includeFiles`), workflow i `vercel_bundle_size.py`. Dvije
  datoteke se ne mogu zamijeniti atomarno, a `server._con` sada prati samo jednu. Neslaganje `pk`/`sk` između
  datoteka dalo bi tiho krive cijene, pa bi obje nosile isti `build_id` koji se provjerava pri otvaranju.

### (c) Parquet s jačom kompresijom

ZSTD-19 nad tablicama iz (a): products 11,9, store_products_k 14,5, price_exceptions_k 4,8, staple_prices_k 2,0,
chain_prices_k 1,9, staple_items 1,4, ukupno **~37 MiB** (ZSTD-3: ~53). Paket ~135 MiB.

- Brzina: izravni upiti nad Parquetom dekomprimiraju pri svakom upitu. Zato bi se pri hladnom startu gradila
  DuckDB datoteka u `/tmp` (Vercel: 500 MB): lokalno **5,1 s** u jednoj dretvi, na Vercelu vjerojatno 8–10 s za
  svaki hladni start, uz `maxDuration` 60 s.
- Rizik: srednji do visok (hladni start, `/tmp` i memorija, novi put pokretanja). Najveća rezerva, najgora latencija.

### (d) Ostalo

- DuckDB `force_compression = 'zstd'`: products 24,8 → 71,5 MiB, lošije. Odbačeno.
- Baza se preuzima pri hladnom startu (Vercel Blob ili GitHub Release): nema ograničenja paketa, ali uvodi vanjsku
  ovisnost, a svaki hladni start prenosi ~90 MB (kvote prijenosa na Hobby planu). Ne preporučujem.
- Bez neprehrambenih proizvoda (34 % proizvoda, 23 % cijena): mijenja `find_products(include_nonfood)`. Ne bez
  odluke.
- `staple_items` kao (staple, pk) uz join s products: procjena −3,5 MiB, brzina neizmjerena.
- `store_products_k` po (pk, sk): veći (16,8 MiB prema 14,8). Odbačeno.

## 4. Prijedlog

**(a) + (b)**, a po potrebi i `staple_items` po ključu:

| | sada | nakon ~6 mj. (+15 %) | rezerva |
|---|---:|---:|---:|
| datoteka A / B | ~44 / ~43 MiB | ~51 / ~50 | ~44 MiB do 95 ✓ |
| paket (92,7 + baza) | ~181 MiB | ~194 | ~26 MiB do 220 ✗ (malo ispod 30) |
| paket uz `staple_items` po ključu | ~177 MiB | ~190 | ~30 MiB ✓ (na rubu) |

Uz to bi workflow ispisivao `::warning::` kad je neka datoteka > 65 MiB ili paket > 190 MiB, prije nego što
provjera padne. Ako rast bude veći od pretpostavljenog, sljedeći korak je (c) samo za cjenovne tablice (B).

Redoslijed: (a) u `build_compact.py` (stores.date/stale_days, datum u iznimkama, izvedeni stupci u
`staple_prices`), zatim provjera otiska, zlatni izlazi i mjerenje brzine; onda (b) sa svim točkama otvaranja i
provjerom `build_id`; na kraju upozorenja u workflowu i `DEPLOY.md`.

## 5. Implementacija

Odluka: (a) + (b); `staple_items` po ključu ne sada; rezerva paketa se traži u ovisnostima.

### 12.1 Datum po trgovini (a)

`scripts/build_compact.py`:
- `clean.stores.sk_date` (najčešći datum cijena trgovine, pri jednakom broju noviji) i `sk_stale_days` (datum
  cjenika − `sk_date`; datum cjenika je `date + stale_days`, jednak za sve retke, inače izgradnja staje);
- `date` i `stale_days` više nisu stupci vrijednosti osnovnog retka. Redak je osnovni kad su mu vrijednosti jednake
  osnovnima i datum jednak datumu trgovine. U `price_exceptions_k` i `staple_prices_k` stupac `date` je NULL osim
  kad se razlikuje od datuma trgovine (trgovina s djelomičnim padom);
- `staple_prices_k` ne sprema `price_per_unit`, `per_unit`, `unit_confidence` (spremljeni kao `*_x` samo za
  proizvode bez pakiranja g/ml/kom) ni `price_per_kg_drained`; view `staple_prices` ih računa (`DERIVED`).
  U `prices` ostaju spremljeni.

Provjera otiska view-ova prema punoj bazi prolazi. Golden: 27/27 jednako (zapis s pune baze 28.10., provjera nad
novom sažetom). pytest: 1351 prošlo, 7 preskočeno. Novi `tests/test_step12.py`: trgovina cijela od jučer nema
nijednu iznimku više od iste trgovine od danas; trgovina pola-pola ima iznimke s datumom; view i izlazi alata
(plan_basket u gradu i u toj trgovini, list_stores, get_prices) jednaki su punoj bazi.

| | prije | 12.1 |
|---|---:|---:|
| cjenik 28.10. | 92,8 MB | **89,5 MB** |
| + simulirani NTL pad | 95,5 MB | **88,8 MB** (iznimaka 2 833 369, kao bez pada) |

### 12.2 Dvije datoteke (b)

- `build_compact.py` piše glavnu datoteku (izlaz) i datoteku cijena uz nju (`search.prices_part`:
  `compact.duckdb` → `compact_prices.duckdb`) s `chain_prices_k`, `store_products_k` i `price_exceptions_k`. View
  `clean.prices` ih čita kao `mm_prices.clean.*` (`search.PRICES_ALIAS`). Prvo se zamjenjuje datoteka cijena, pa
  glavna.
- **Oznaka izgradnje:** obje datoteke imaju `clean.compact_build` (`build_id` = vrijeme + slučajni dio; glavna i
  `prices_file`). `search.attach_prices` priključuje datoteku cijena i uspoređuje oznake. Kad se razlikuju ili
  datoteka cijena nedostaje, javlja `search.CompactMismatch`, a ne tuđe cijene. Pozivaju je oba mjesta koja otvaraju
  bazu: `search.connect` i `server._open` (stdio, lokalni HTTP i Vercel idu kroz `_open`; `golden.py` kroz
  poslužitelj). Puna baza nema `compact_build` i otvara se kao prije.
- `server._con` prati obje datoteke (inode, mtime, veličina), pa zamjena bilo koje otvara novu vezu.
- `vercel.json` `includeFiles`: `data/compact_prices.duckdb` (`*.tmp` je već u `excludeFiles`).
- Testovi (`tests/test_step12.py`): obje datoteke imaju istu oznaku, a cijene su samo u datoteci cijena. Datoteka
  cijena iz druge izgradnje daje `CompactMismatch` u `search.connect` i `server._open`, a kroz MCP odgovor je greška
  (`is_error`, bez cijena). Isto vrijedi bez datoteke cijena, a i kad se datoteka cijena zamijeni dok poslužitelj radi.

| | glavna | cijene |
|---|---:|---:|
| cjenik 28.10. | **45,5 MB** | **43,3 MB** |
| + simulirani NTL pad | 44,8 MB | 43,3 MB |

Golden 27/27 jednako punoj bazi. pytest: 1356 prošlo, 7 preskočeno.

**Brzina** (24 scenarija find_products i plan_basket iz `golden.py`, medijan 3 topla poziva, isti cjenik 28.10.,
dva ponavljanja):

| baza | ukupno |
|---|---:|
| stara shema (jedna datoteka) | 19,2 / 19,4 s |
| 12.1 (jedna datoteka) | 20,2 / 20,3 s |
| 12.2 (dvije datoteke) | 20,3 / 19,8 s |

Podjela ne usporava (12.1 ≈ 12.2). Nova shema je ~4 % sporija na putu namirnica: plan_basket +0,05 do 0,15 s po
pozivu (`basket_bolonjez_osijek_10` 1,50 → 1,65 s), zbog izračuna izvedenih stupaca i datuma u view-u
`staple_prices`. Free text i `basket_nepoznato` nisu sporiji (7,5 → 7,4 s). (U prijedlogu je 19,4 s izmjereno na
simuliranom padu, a ondje je stara shema imala 564 k iznimaka više.)
