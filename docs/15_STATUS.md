# Korak 15: arhiva 17.11.2026. (NN 101/26, 110/26), pad workflowa #65

## Uzrok

Run #65 (17.11. 21:51) pao je u koraku **Sažeta baza (build_compact.py)**: DuckDB `OutOfMemoryException`
(1,3/1,3 GiB) u upitu cijena namirnica. update.py je prošao, deploy nije ni počeo; svih 9 pokretanja prije njega je
uspjelo. Arhiva 17.11. narasla je sa ~17 M na **30,2 M** redaka cijena (zip 133 → 237 MB): po novoj odluci lanci
objavljuju sve trgovine i sav asortiman.

## Što se promijenilo u arhivi (16.11. → 17.11., uspoređeno i s 13.11.)

- Isto: nazivi datoteka, zaglavlja sva tri CSV-a, kodiranje (UTF-8 bez BOM-a, CRLF), archive-info.txt. Novih lanaca
  nema (konzum, studenac, branka i lorenco 16.11. su izostali, pa ih log zove "novi lanac").
- Trgovine: studenac 20 → 1366, konzum 187 → 450 (tipovi mali/super/maxi), boso 14 → 283, trgocentar 6 → 95,
  ribola 61 → 104, jadranka 1 → 18, ktc 34 → 81.
- KTC: neprehrambene poslovnice (25 poljoljekarni, 18 benzinskih, autopraona, frizerski i kozmetički salon; tip
  "kozmeti^ki" oštećen u izvoru) i 161 nova neprehrambena kategorija (pravila bi neke svrstala u hranu).
- Prazna kategorija: konzum, lidl, dm, boso, branka, jadranka, trgocentar, nove šifre kauflanda (djelo_vodice i vrutak
  već od 16.11.). Prazan `quantity`/`unit`: boso, jadranka, trgocentar.
- Lidl: `unit` je jedinica cijene ("g (1kg)", "bez (1 kom.)", "ml (1 L)") umjesto veličine pakiranja ("500g");
  `quantity` je bruto masa (0.252 za 250 ml). Šifre su izgubile vodeće nule ("0083215" → "83215"), često uz drukčiji
  barkod.

## Popravci podataka

- **Memorija polja proizvoda** (`update.remember_fields`, tablica `clean.product_fields`, zapis ispada nakon 90 dana):
  prazna kategorija, `quantity` ili `unit` (i Lidlov oblik "g (1kg)") dobiva zadnju poznatu vrijednost za isti (lanac,
  šifra); kad ista šifra za to polje nema vrijednost, za isti barkod lanca, pa za šifru bez vodećih nula (obje samo
  kad su jednoznačne). Prvo punjenje: sirovi proizvodi prethodne baze i arhiva 13.11. (`--seed-date`, u CI-ju jednom
  preuzeta). 17.11.: kategorija popunjena za boso 9442, branka 14710, djelo_vodice 10785, dm 21784, jadranka 9156,
  konzum 21609, lidl 5840, trgocentar 10461, vrutak 14435; Lidlov `unit` za 5826 proizvoda.
- **Lidlovo pakiranje**: `normalize.parse_pack_unit_field` ne čita pakiranje iz jedinice cijene
  (`PRICE_REF_UNIT_RX`, isti izraz u update.py). Prije je 7104 Lidlova proizvoda dobilo pakiranje iz nje, 714 lažno
  1 kg / 1 L (cijena po kg kriva).
- **Neprehrambene poslovnice** (`build.NONFOOD_STORE_TYPES`, po tipu poslovnice): izvan clean.stores/clean.prices,
  pa i izvan alata; sirove tablice ih zadržavaju. Nov tip poslovnice koji nije na popisu ostaje u bazi.
- **KTC kategorije** u `data/category_map.yaml` kao neprehrambene.

## Sažeta baza

- `build_compact` pod 1500 MB: DISTINCT cijena namirnica najprije u privremenu tablicu (samo 11 stupaca koje čita
  upit kandidata), pa spajanje s ključevima i sortiranje; prije je i sa suženim stupcima pao (1,3 GiB). Sada ~1 min,
  RSS ~1,6 GB. `clean.product_fields` se ne kopira (13 MB, samo za update.py).
- **Bez proizvoda s `is_food = false`** i njihovih cijena (275 tis. proizvoda, 8,25 M cijena, 29 %); `is_food` NULL
  ostaje. Uvjet je `search.STORE_PRODUCTS_SQL`.
- **`anchor_price` se ne čuva**: view `clean.prices` vraća NULL (`build_compact.NO_ANCHOR_COLS`; Korak 16: `MM_COMPACT_ANCHOR=1` ga zadržava). Sidrena cijena
  (2.5.2025.) razlikuje se po trgovini u 24 % redaka hrane (studenac 2,46 M, konzum 0,94 M, plodine 0,44 M) i
  stvarala je iznimke. Puna baza je zadržava.
- Provjera view-ova prema punoj bazi uspoređuje iste proizvode i stupce bez `anchor_price` i traži da je on NULL.

### Što se time gubi

- `include_nonfood` nad sažetom bazom (`search.find_products/get_prices(include_nonfood=True)`) ne nalazi ništa
  neprehrambeno. MCP alati taj parametar ne prosljeđuju, pa se njihovi izlazi ne mijenjaju: neprehrambeni upit
  ("deterdžent") ni prije nije vraćao neprehrambene proizvode.
- `get_prices`: `anchor_price` je uvijek `null` (na Vercelu). Ostali alati ga ne koriste; upute ga ne spominju.
  Puna baza (lokalni server) ga i dalje vraća.
- `list_stores.n_prices` broji samo cijene proizvoda koji nisu sigurno neprehrambeni (i nad punom bazom, da puna i
  sažeta daju isto); trgovina samo s neprehrambenim cijenama više nije na popisu.

### Veličine (cjenik 17.11., 28,75 M čistih cijena)

| | 28.10. | 17.11. bez promjena | 17.11. (Korak 15) | upozorenje / granica |
|---|---|---|---|---|
| compact.duckdb | 44,8 MB | 67,5 | **53,0** | 65 / 95 |
| compact_prices.duckdb | 43,3 MB | 95,5 | **54,0** | 65 / 95 |
| paket (`vercel build --prod`, vercel_bundle_size.py) | 180,8 MB | ~256 | **199,9** | 190 / 220 |

Paket je iznad upozorenja (rezerva do 220 MB: 20 MB), datoteke ~41 MB ispod granice. Najveći rast prema 28.10.:
iznimke cijena po trgovini (studenac s 1366 trgovina ima više iznimaka nego osnovnih redaka; cijene se stvarno
razlikuju po trgovini) i dostupnost po trgovini (`store_products_k` 14,1 M → 15,9 M redaka).

## Brzina

Plan upita s 30 M cijena:
- `get_prices` po klasi (jaja:m): korelirani `EXISTS` nad atributima postao je delim join, pa se cijeli view cijena
  (sve trgovine) spajao prije filtra proizvoda (36 s u spoju). Sada `(chain, product_id) IN (podupit)`.
- Kandidati slobodnog teksta (`search._candidates` uz `clean.prices`): najprije šifre proizvoda pogođenih grupa, pa
  `c.product_id IN (...)` (do `PRICE_KEYS_MAX` = 20 000), koji DuckDB gura do skeniranja view-a. Uvjet je već
  sadržan u spoju, rezultati su isti.

Zbroj medijana 3 topla poziva, 27 zlatnih scenarija, lokalno, `MM_DUCKDB_MEMORY` 300 MB:

| | ukupno | plan_basket | jaja:m | basket_nepoznato |
|---|---|---|---|---|
| 28.10. (stara sažeta baza) | 32,5 s | 27,8 | 2,8 | 10,9 |
| 17.11. bez promjena | 95,3 s | 51,6 | 40,9 | 28,1 |
| 17.11. A + bez anchor_price | 53,1 s | 30,7 | 20,4 | 11,4 |
| **17.11. Korak 15** | **18,5 s** | 16,2 | **0,6** | 1,9 |

Limit memorije (sažeta baza, isti skup): 300 MB 17,8 s / RSS 558 MB, 600 MB 17,3 s / 584 MB, 900 MB 17,5 s /
597 MB. Viši limit ne pomaže, pa Vercel ostaje na 300 MB (zadano u server.py). `list_stores` (sada i spoj s
proizvodima): Zagreb 1,4 s, Osijek 0,4 s.

## Workflow

- `MM_COMPACT_MEMORY=6000MB` (runner ubuntu-24.04: 4 CPU, 16 GB); lokalno zadano ostaje 1500 MB.
- `MM_DUCKDB_MEMORY=6000MB` za zlatni `--write` na punoj bazi i za pytest; zlatni `--check` na sažetoj bazi ostaje
  na 300 MB kao funkcija na Vercelu.
- update.py lokalno: ~5,1-5,7 GB RSS, 5-20 min (ovisno o slobodnoj memoriji računala).

## Zlatni izlazi

Zapis s pune baze 17.11., provjera na sažetoj: **27/27 jednako**. `golden.py` iz `get_prices` izlaza uklanja
`anchor_price` (sažeta ga nema). Svih 27 JSON-ova se mijenja prema 28.10. jer je cjenik nov (datum, cijene, broj
trgovina; više trgovina po lancu nakon NN 101/26). Vrijedi istaknuti:
- `prices_*` (3): bez `anchor_price`; `prices_lidl_brasno` traži novu Lidlovu šifru `lidl:2225` (stara `0002225`
  ostaje samo u prenesenoj trgovini).
- `basket_lidl_varivo_zagreb` 12,31 → 14,71 €: Pik kobasica više nije u akciji, mrkva rinfuza 0,49 → 0,79 €
  (s memorijom polja za šifre bez nula; bez nje Lidl je gubio krumpir, papar i rinfuzu: 17,30 €).
- `basket_varivo_slavonski_brod` lidl → ntl, `basket_krumpir_rijeka` plodine → konzum, `basket_grah_suho_osijek`
  konzum → studenac, `basket_tagliatelle_osijek` kaufland → roto, bolonjez Zagreb i Osijek → eurospin: novi
  najjeftiniji lanci.
- find_*: isti prvi rezultat uglavnom, više trgovina (npr. mlijeko Zagreb 167 → 376).

## Dugoročni rizik: novi proizvodi bez povijesti

Memorija polja pomaže samo poznatim šiframa. Novi = šifra ni barkod lanca nisu bili 13.11. ni 16.11. (~211 tis.).
`is_food` NULL ne ulazi u alate (osim svježeg voća i povrća namirnice).

| lanac | novih | bez kategorije | hrana / neprehr. / nepoznato | bez quantity ili unit | od toga bez pakiranja |
|---|---|---|---|---|---|
| trgocentar | 69 547 | 69 547 | 659 / 9 201 / 59 687 | 61 386 | 53 280 |
| konzum | 28 248 | 28 212 | 356 / 6 087 / 21 769 | 2 | 2 |
| kaufland | 16 853 | 16 837 | 29 / 3 035 / 13 773 | 0 | 0 |
| jadranka_trgovina | 10 597 | 10 390 | 2 889 / 2 988 / 4 513 | 10 404 | 5 099 |
| lidl | 7 948 | 7 150 | 21 / 328 / 6 801 | 7 150 (unit "g (1kg)") | 6 322 |
| boso | 3 244 | 3 167 | 494 / 1 083 / 1 590 | 3 167 | 1 807 |
| branka | 1 914 | 1 914 | 530 / 595 / 789 | 1 030 | 829 |

Lidl: od 7961 proizvoda s jedinicom cijene u `unit` pakiranje ima 828 (naziv 766, EAN 62). Koliko je hrane među
"nepoznato" ne zna se; to su proizvodi koje sada nijedan izvor (kategorija lanca, EAN drugog lanca, riječi) ne
svrstava. Studenac i lorenco nikad nisu imali quantity odnosno kategoriju.

## Poznato, nije popravljeno

- Carry-forward prenosi stare Lidlove šifre ("0002225") još do 7 dana uz nove ("2225") u istoj trgovini.
- Cache u Actionsu ima bazu 17.11. iz runa #65 (stari kod, bez `clean.product_fields`). Sljedeće pokretanje s novom
  arhivom jednom puni memoriju iz te baze i arhive 13.11.; arhiva 17.11. se neće ponovno učitati bez `force`.

## Provjera

- `uv run pytest -q`: 1445 passed, 7 skipped
- `MM_GOLDEN=1 uv run pytest -q`: 1452 passed
- `golden.py --write` (puna) pa `--check` (sažeta): 27/27
- `vercel build --prod` lokalno + vercel_bundle_size.py: 199,9 MB (upozorenje > 190), izlazni kod 0
- ručni deploy nije rađen; sljedeće zakazano pokretanje workflowa ide s ovim promjenama
