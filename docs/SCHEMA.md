# Struktura podataka (cijene.dev dnevna arhiva)

Analizirana arhiva: `https://api.cijene.dev/v0/archive/2026-10-19.zip` (123 MB zip, ~250 MB DuckDB).
Skripte: `scripts/explore.py` (pregled CSV-ova), `scripts/load.py` (učitavanje u DuckDB),
`scripts/build_clean.py` (čiste tablice), `scripts/probe_queries.py` (probni upiti iz Koraka 0),
`scripts/make_fixture.py` (fixture za testove). Odluke o čišćenju: [DECISIONS.md](DECISIONS.md).

## Struktura arhive

```
archive-info.txt            # službeni opis formata (hrvatski)
<lanac>/stores.csv          # poslovnice
<lanac>/products.csv        # proizvodi (jedinstveni unutar lanca)
<lanac>/prices.csv          # cijena proizvoda po poslovnici
```

28 lanaca: boso, branka, bure, djelo_vodice, dm, dukat, eurospin, gavranovic, jadranka_trgovina,
kaufland, konzum, ktc, lidl, lorenco, metro, ntl, plodine, ribola, roto, spar, stanic, stridon,
studenac, tommy, trgocentar, trgovina-krk, vrutak, zabac. (`archive-info.txt` nabraja samo njih 17,
pa je zastario.) Svi CSV-ovi su UTF-8, separator je zarez, a prvi redak sadrži zaglavlje. Stupci
su identični u svim lancima.

| datoteka | stupci |
|---|---|
| stores.csv | `store_id, type, address, city, zipcode` |
| products.csv | `product_id, barcode, name, brand, category, unit, quantity` |
| prices.csv | `store_id, product_id, price, unit_price, best_price_30, anchor_price, special_price` |

Ključevi: `(lanac, store_id)` i `(lanac, product_id)`. Šifre **nisu** jedinstvene između lanaca.
Svaki redak u `prices` ima odgovarajući proizvod i trgovinu (provjereno: 0 siročadi).

## Gdje je što

| pojam | stupac | napomena |
|---|---|---|
| lanac | naziv mape | u CSV-ovima ne postoji, loader ga dodaje kao `chain` |
| trgovina | `stores.store_id`, `address`, `city`, `zipcode`, `type` | `zipcode` postoji samo kod 10 lanaca |
| proizvod (EAN) | `products.barcode` | EAN ili `<lanac>:<product_id>`, vidi dolje |
| šifra proizvoda | `products.product_id` | interna šifra lanca, s vodećim nulama |
| naziv | `products.name` (+ `brand`, `category`) | slobodan tekst, kratice, ponekad bez dijakritike (Plodine: `BRASNO`) |
| cijena | `prices.price` | **ono što kupac plaća danas** (već uključuje akciju, osim kod Eurospina) |
| jedinična cijena | `prices.unit_price` | nepouzdana, vidi dolje |
| akcijska cijena | `prices.special_price` | prazno ili `0.00` znači da akcije nema |
| sidrena cijena | `prices.anchor_price` | cijena na dan 2.5.2025. (NN 75/2025) |
| najniža cijena u 30 dana | `prices.best_price_30` | većina lanaca je ne popunjava |
| datum | **nema stupca** | datum je samo u nazivu arhive; loader dodaje `date` (DATE) |

## DuckDB (`data/mealmeter.duckdb`)

```
uv run python scripts/load.py data/raw/extracted 2026-10-19 data/mealmeter.duckdb   # sirove tablice
uv run python scripts/build_clean.py                                                 # schema clean
```

### Sirove tablice (schema `main`, bez normalizacije)

- `stores(chain, store_id, type, address, city, zipcode)`: 1.512 redaka
- `products(chain, product_id, barcode, name, brand, category, unit, quantity)`: 477.526 redaka
- `prices(chain, store_id, product_id, price, unit_price, best_price_30, anchor_price, special_price, date)`: 17.316.247 redaka

Svi identifikatori su `VARCHAR` (zbog vodećih nula). Cijene su `DECIMAL(10,2)`, a svaka neprazna
vrijednost se uspješno parsirala.

### Čiste tablice (schema `clean`, nad njima radi pretraga)

**`clean.stores`** (1.512 redaka)

| stupac | opis |
|---|---|
| chain, store_id, type, zipcode | kao u sirovim podacima |
| address | Spar: bez sufiksa „87001 Spar“ |
| city | izvorni grad; 2 Kauflandove trgovine popunjene iz adrese |
| scope | `national` (dm, Lorenco: `store_id = 'all'`) ili `local` |
| city_norm | `norm_text(city)`: mala slova, bez dijakritika |
| city_canonical | grad nakon aliasa (Sesvete → Zagreb, Kaštel Stari → Kaštela) |
| city_key | `norm_text(city_canonical)`, ključ za pretragu |
| store_type | `cash_and_carry` (veleprodaja: Metro, `build.WHOLESALE_CHAINS`) ili `retail`; veleprodaja je izvan zadanog izbora (`include_wholesale`) |

**`clean.city_alias`** `(alias_norm, city)`: 19 aliasa, izvor je `CITY_ALIASES` u `normalize.py`.

**`clean.products`** (477.526 redaka)

| stupac | opis |
|---|---|
| chain, product_id, barcode, name, brand, category, unit, quantity | kao u sirovim podacima |
| ean_norm | normalizirani EAN-13/EAN-8 (11/12/14 znamenki → EAN-13), NULL ako kod nije valjan |
| ean_valid | kontrolna znamenka ispravna (446.394 + 7.189 = 453.583 proizvoda) |
| ean_global | valjan i nije kod ograničene upotrebe (vaga/in-store: 7.189 nije globalno); grupira se samo po njima. 219.343 različitih globalnih EAN-ova |
| name_norm | naziv: mala slova, bez dijakritika, `đ`/`dj` → `d`, interpunkcija → razmak |
| pack_amount, pack_unit | gramatura: količina u `g`, `ml` ili `kom` |
| pack_amount, pack_unit | gramatura pakiranja; kod konzervi **neto masa s tekućinom** (sadržaj limenke, npr. 400 g u „GRAH 400g/240g“) |
| pack_confidence | `high`, ili `low` kad gramatura ovisi o heuristici višestrukog pakiranja („7 g 4+1“, „10 g 3/1“, „2x80“, „5x35 g 1gratis“); NULL bez gramature |
| pack_source | `name`, `unit` (Lidl), `ean` (naslijeđeno od istog EAN-a), NULL (uglavnom neprehrambeno i roba na vagu) |
| drained_amount | **ocijeđena masa** konzerve u g, bez tekućine („OC. MASA 280 g“, „185/140g“, „NETO 800G“); košarica je koristi za konzerve |
| variable_weight | „CCA“ ili raspon težine („1-1,5KG“): nema pakiranja, cijena po kg je od lanca |
| clearance | naziv sadrži „SNIŽEN…“ (rasprodaja) |
| food_group | skupina (`food.py`): hrana, pice, alkohol, kozmetika, higijena, kucanstvo, djeca, kucni_ljubimci, ostalo ili `unknown` |
| is_food | `true` (hrana, pice, alkohol), `false` (ostale skupine), NULL (`unknown`) |
| category_source | `chain` (kategorija lanca, `data/category_map.yaml`), `ean_inherited` (većinska skupina istog globalnog EAN-a), `words` (popis riječi), `none` |
| unit_hint | `kg`/`l`: na što se (vjerojatno) odnosi lančev `unit_price` (iz `quantity`/`unit`) |

**`clean.prices`** (16.401.076 redaka; iz 17.316.247 uklonjeno 907.165 duplikata i 8.006 redaka bez cijene)

| stupac | opis |
|---|---|
| chain, store_id, product_id | jedinstveno (bez duplikata) |
| date | DATE, dan iz naziva arhive |
| price, special_price, unit_price, best_price_30, anchor_price | kao u sirovim podacima, ali `0.00` → NULL |
| price_eff | cijena koju kupac plaća: `coalesce(special_price, price)` |
| price_date | datum cijene: dan arhive, ili raniji dan kod prenesene cijene (carry-forward, `update.py`) |
| stale_days | starost cijene u danima (dan arhive − `price_date`); 0 za cijene iz same arhive |
| is_special | `special_price IS NOT NULL` |
| price_per_unit, per_unit | cijena po `kg` / `l` / `kom` |
| unit_confidence | `high` (iz gramature), `low` (iz lančevog `unit_price`), NULL. Ukupno 73,1 % high, 3,0 % low, 23,9 % bez cijene po jedinici |
| price_per_kg_drained | cijena po kg ocijeđene mase (konzerve) |

Kontrola gramature: naša cijena po kg/l (`high`) slaže se s lančevim `unit_price` (unutar 5 %) u
84–97 % slučajeva kod većine lanaca (Konzum 95,8 %, Tommy 96,6 %, Lidl 92,2 %). Niske vrijednosti
kod Branke (7,5 %), Stanića (14,7 %) i Žabca (4,4 %) potvrđuju da je njihov `unit_price` zapravo
cijena pakiranja. Metro (66 %) prodaje kutije porcija („20G PODRAVKA DŽEM“ za 15,81 €).

**`clean.chains`** `(chain, n_stores, scope, data_quality)`: `data_quality` je `ok` ili `suspect`
(Lorenco). Razlozi su u DECISIONS.md, a pokazatelje za sve lance ispisuje `build_clean.py`.

**`clean.staple_rules`** `(staple, name, unit, compare_by, compare_unit, ppu_min, ppu_max, range_source,
min_pack, max_pack, pantry, loose_produce)`: pravila aktivnih namirnica iz `staples.yaml`;
`range_source` je `manual` (`plausible_per_unit`) ili `auto` (0,25x–4x medijana). Vidi docs/ranges.md.

**`clean.product_staples`** `(chain, product_id, staple, excluded, drop_reason, n_units)`: proizvodi čiji
naziv pogađa `must_match` (i `require_any`) namirnice.
- `excluded = true` kad pogađa i `must_not_match`; tada cijela grupa ispada.
- `drop_reason` (`kategorija:*`, `pakiranje`) izbacuje samo taj proizvod.
- `n_units` je broj vrećica ili komada kad je `compare_by` pack ili count.
- `assumed_g` je pretpostavljena masa pakiranja bez gramature (`packaged`, luk rukavac 500 g).

**`clean.product_attrs`** `(chain, product_id, staple, attr, value, how)`: atributi iz naziva (npr.
brasno/tip/glatko, mlijeko/mast/2.8), samo za neisključene proizvode. `how` je `name`, `inferred`
ili `default`.

## Funkcije pretrage (`src/mealmeter/search.py`)

- Filtar hrane: obje funkcije zadano vraćaju samo `is_food = true` bez alkohola; `include_nonfood`,
  `include_alcohol` i `include_unverified` to proširuju, a izlaz nosi `food_group` i `food_unverified`.
- `find_products(query=None, city=None, limit=10, ingredient=None, attributes=None)`: grupe proizvoda
  (po EAN-u ili po lancu i nazivu) s poljima `id, ean, name, brand, pack, n_chains, n_stores, chains,
  price_min/max, price_per_unit_min/max, per_unit, unit_confidence, pack_source, suspect_chains,
  any_special, has_national, ingredient, date, date_hr`, uz `attributes` kad je zadana namirnica i
  `note` kad grupa uključuje nacionalnu cijenu.
- `get_prices(identifier, city=None, limit=50)`: identifier je EAN ili `lanac:product_id`. Po
  trgovini vraća `chain, store_id, address, city, scope, product_id, ean, name, price_eff,
  is_special, special_price, anchor_price, best_price_30, price_per_unit, per_unit,
  unit_confidence, pack_source, data_quality, date, date_hr` i `note` za nacionalne cijene.
- `plan_basket(ingredients, city, mode="single_store", already_have=None)` (`src/mealmeter/basket.py`):
  cijena recepta po trgovini (`total_to_buy`: cijela pakiranja bez `already_have`; `total_used`: razmjerno),
  najbolja trgovina, nepovezani i dvosmisleni sastojci i pretpostavke (DECISIONS.md, točke 37 i 73).
- `units.convert(amount, unit, staple)` (`src/mealmeter/units.py`, vrijednosti u `data/units.yaml`): žlica,
  žličica, šalica, dcl, prstohvat i čaša u ml, pa u grame preko gustoće namirnice; sve su procjene.
- CLI: `uv run python -m mealmeter.cli find "brašno glatko" --city Osijek`,
  `uv run python -m mealmeter.cli basket data/recipes/test_grah.json --city Osijek`,
  `uv run python -m mealmeter.cli find --ingredient brasno --attr tip=glatko --city Osijek` i
  `uv run python -m mealmeter.cli prices 3850104223624 --city Osijek` (`--json` za strojni izlaz).

## Zaključci

### Gradovi: postoje
- `city` je popunjen za sve trgovine osim dvije Kauflandove (grad je zapisan u adresi: „… Lucko“, „… Krk“)
  i dvije nacionalne pseudo-trgovine.
- **dm i Lorenco** imaju samo jednu „trgovinu“ `store_id='all'` bez adrese, dakle nacionalnu cijenu.
- Osijek: 58 trgovina iz 10 lanaca (NTL 34, Konzum 7, Spar 5, Lidl 3, …). Nema varijanti zapisa.
- Varijante su rijetke: `Plaski`/`Plaški`, `Zagreb-Dubrava` uz `Zagreb`, `Sesvete` kao zaseban grad.
  Ukupno 385 različitih gradova.
- Adrese su neuredne: Spar dodaje šifru i naziv trgovine („Optujska 171 87001 Spar“), Vrutak piše
  bez razmaka („Vodovodna20A“), Stanić nema adresu.

### Cijene
- `price` je gotovo uvijek popunjen (0 % NULL). Roto ima 4,2 % redaka s cijenom `0.00`, NTL 0,2 %.
- Kad akcija postoji (`special_price > 0`), kod svih lanaca osim Eurospina vrijedi `price == special_price`.
  **Kod Eurospina je `price` redovna cijena, a `special_price` niža cijena.** Cijena za kupca je zato
  `coalesce(nullif(special_price, 0), price)`.
- `0.00` se koristi umjesto praznog polja: Eurospin (`special_price`, `best_price_30`), KTC (oba stupca
  uvijek `0.00`), Dukat (`best_price_30`).
- `anchor_price` nedostaje u potpunosti kod KTC-a i Vrutka, a djelomično kod Lidla (20 %), Stanića (22 %),
  Metroa (18 %) i Tommyja (17 %). Lorenco ima besmislene sidrene cijene (torta 49 € → sidro 5,10 €).
- **Duplikati u `prices.csv`**: isti par (store, product) se ponavlja kod 10 lanaca. Kod Lidla je to
  ~2× (1,63 mil. redaka, 0,80 mil. jedinstvenih), a slijede Eurospin, djelo_vodice i Dukat. `price` je
  pritom isti; razlikuju se samo `unit_price`/`anchor_price` (Lidl 20 tis. parova). Kod Studenca
  (19 parova) i Ribole (3 para) se razlikuje i `price`.
- Cijene su po trgovini. Primjer: Podravka glatko brašno 1 kg (EAN 3850104223624) postoji u 18 lanaca
  i stoji 0,62–0,80 €. Gotovo svi lanci imaju istu cijenu u svim poslovnicama, a samo Stridon i Branka
  variraju po trgovini.

### Jedinična cijena (`unit_price`) nije pouzdana
- Kod nekih lanaca je jednaka cijeni pakiranja, a ne cijeni po kg/L (Stanić: brašno 25 kg → `unit_price` 17,99;
  Branka i Jadranka isto).
- Ima vrijednosti `0.00` (Lorenco 46 %, KTC 6,5 %, Bure 5 %) i besmislenih vrijednosti (KTC 15,49 € → 0,26).
- Za usporedbu po kg treba vlastiti izračun iz `quantity`/`unit`/naziva, što je posao za sljedeći korak.

### `unit` i `quantity` su potpuno neujednačeni
- `unit`: `KG/kg/ko/KILOGRAM/kilogram`, `KOM/kom/KOMAD/ea/PZ/K0M/kođ`, `L/LT/LITRA`, `-1`, `055`, …
- Lidl u `unit` stavlja veličinu pakiranja (`80g`, `10x1kg`, `123g,200g,77g`).
- `quantity`: `100 G`, `0.150 L`, `,165`, `0,15`, `1.000 L`, `500.000 GR`, `16,0000`. Žabac i nekoliko
  drugih lanaca ga uopće nemaju.
- Ima i grešaka: Metro „1KG VEGETA“ → `10000 G`, Boso „GRAH 800 g“ → `480 G`, Branka „FRISKIES 85g“ → `0.850 KG`.
- Najpouzdaniji izvor gramature je često sam naziv („… 1 kg“, „5/1“, „25KG“).

### EAN i proizvodi bez EAN-a (upit d)
- Prema dokumentaciji, kad EAN nedostaje, `barcode` ima oblik `<lanac>:<product_id>`
  (Ribola koristi i razmak: `ribola: 070703`). Najviše takvih ima Eurospin (22,5 %), slijede Studenac (13,9 %)
  i Ribola (7,2 %).
- **Mnogi lanci ne koriste taj prefiks**, nego u `barcode` stavljaju internu PLU šifru (`1`, `290318`, `5561`).
  Tommy, Gavranović, NTL, trgovina-krk i Lorenco imaju 0 % prefiksa, a 5–14 % kodova im nije valjan GTIN.
  Zato provjeravam kontrolnu znamenku GTIN-a (EAN-8/UPC-12/EAN-13/GTIN-14), a ne samo prefiks.
- **11-znamenkasti kodovi su UPC-A bez vodeće nule** (npr. Tabasco `11210000018`): od 1.962 takva koda,
  njih 1.935 postaje valjano kad im se doda `0`. Negdje u lancu obrade barkod je tretiran kao broj.
- Interni „in-store“ EAN-13 s prefiksom `2` (vaga, vlastita pekara): Metro i Trgocentar ~9 %, Bure 6 %.
  Valjani su, ali nisu globalno jedinstveni i ne smiju se spajati među lancima.
- Ukupno 225.480 različitih valjanih GTIN-ova.

### Svježi proizvodi
- Voće, povrće i meso na vagu uglavnom imaju `unit = kg`, `quantity = 1` i **nemaju EAN**
  (PLU kod ili `<lanac>:<id>`): „BANANA II KAT“ (Tommy, `290493`), „JABUKA IDARED“ (Stridon, `stridon:106458`).
  Takve proizvode možemo povezati samo po nazivu.
- Pakirani svježi proizvodi (mljeveno meso 500 g, krumpir 2,5 kg) obično imaju pravi EAN.
- Nazivi sadrže šum: „SNIŽENJE“, kalibar („70-75 CAL.“), klasu („II KL“), dobavljača.

### Brojke (upit e)
28 lanaca, 1.512 trgovina (uključujući 2 nacionalne pseudo-trgovine), 385 gradova, 477.526 proizvoda
(po lancu) i 17,3 mil. redaka cijena.

## Otvorena pitanja

Riješeno u Koraku 1 (vidi [DECISIONS.md](DECISIONS.md)): datum (1), duplikati (3), normalizacija
EAN-a (4), dm/Lorenco (6), gradovi i aliasi (7), Roto 0.00 (8: izbačeno), dijakritika u pretrazi (9).
Ostaje:

2. **Eurospin `price` vs. `special_price`**: drugačija semantika od ostalih lanaca. Je li to namjerno
   u cijene.dev ili greška u scraperu? Treba li to prijaviti uzvodno?
5. **Gramatura**: naziv je primarni izvor. Treba li dodati `quantity` kao treći izvor (srednja
   pouzdanost)? Treba li tumačiti `10/1` kod jaja (10 komada) i Metroove kutije porcija
   („40/1 24G“)? Danas se oboje preskače.
7. **„U blizini“**: treba li mapiranje grad → županija ili poštanski broj, da manji grad bez
   trgovina dobije rezultate iz susjednog?
9. **Kratice u nazivima**: `BRAŠ.PŠ.` se sada pronalazi preko istog EAN-a kao „brašno“, ali proizvodi
   bez EAN-a s kraticama se ne pronalaze. Treba li rječnik kratica ili fuzzy/FTS pretraga?
11. **Relevantnost**: „mlijeko“ vraća i čokoladno i sojino mlijeko na istoj razini. Treba li
    rječnik kategorija ili sinonima?
12. **Lorenco** ima besmislene sidrene cijene i 46 % `unit_price = 0`. Je li to uopće maloprodajni
    lanac s nacionalnom cijenom ili ga treba isključiti?
10. **Pokrivenost**: koliko dana povijesti vrijedi držati (trend, `best_price_30` sami izračunati)?
    Svaka arhiva ima oko 123 MB.

## Dnevno ažuriranje (`scripts/update.py`)

- Popis arhiva: `https://api.cijene.dev/v0/list` → `{"archives": [{"date", "url", "size", "updated"}]}`.
- **API ključ nije potreban** (provjereno 2026-10-20, bez zaglavlja `Authorization`): `GET /v0/list` vraća
  HTTP 200 (JSON, ~70 kB), `HEAD /v0/archive/2026-10-19.zip` HTTP 200 (`content-length` 128.905.233), a
  `GET` s `Range: bytes=0-1023` HTTP 206 (`application/zip`). `update.py` zato ostaje na istim URL-ovima.
  Arhiva 2026-10-20 bila je objavljena već u 14:26 (`updated` u popisu), dakle ne uvijek tek oko 22 h.
  Obrazac URL-a je stabilan: `https://api.cijene.dev/v0/archive/YYYY-MM-DD.zip`, a arhiva za dan D
  objavljuje se oko 22 h (20.10. u 13 h još nije postojala, 404). Ako popis nije dostupan, skripta
  ispituje obrazac URL-a za zadnjih 7 dana.
- Tijek: preuzimanje (`data/raw/<datum>.zip`, provjera veličine) → raspakiravanje u svježu mapu →
  izgradnja u privremenu bazu → provjera prema prethodnoj arhivi (pad ukupnih sirovih redaka cijena
  > 20 % prekida, izlaz 2) → carry-forward → čiste tablice (pad `clean.prices` > 20 % naspram prethodne baze
  prekida, izlaz 2) → povijest → `os.replace` (atomarno).
- Nove tablice: `clean.archive_stats (date, chain, n_stores, n_products, n_prices)` i
  `clean.price_history (date, chain, store_id, product_id, price, special_price, price_eff,
  price_per_unit, per_unit)`, za zadnjih 30 dana (`--keep-days`).
- Izlazni kodovi: 0 uspjeh ili već učitano, 1 greška, 2 provjera nije prošla.
- `clean.archive_info (date, updated, size, url, loaded_at)`: učitana verzija arhive. Isti datum s istim
  `updated` se ne učitava ponovno, a ponovno objavljena arhiva (novi `updated`) se učitava. Zato su dva
  dnevna pokretanja (15:30 i 23:30, `--print-schedule`) sigurna.
- Ispis nakon učitavanja uključuje razlike po lancu (trgovine, proizvodi, cijene) naspram prethodne arhive.
- **Carry-forward:** trgovina koja nedostaje u novoj arhivi ili ima više od 10 % manje cijena nego u prethodnoj
  zadržava prethodne cijene (sirovi retci stores/products/prices s izvornim datumom), najviše 7 dana (`CARRY_DAYS`). U
  `clean.prices` takvi retci imaju `stale_days` > 0. U `price_history` ulaze samo cijene dana arhive.
- `uv run python scripts/update.py --print-schedule` ispisuje cron (`30 15,23 * * *`) i systemd timer s dva
  `OnCalendar`; ništa se ne instalira.
