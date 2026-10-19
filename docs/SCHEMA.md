# Struktura podataka (cijene.dev dnevna arhiva)

Analizirana arhiva: `https://api.cijene.dev/v0/archive/2026-10-19.zip` (123 MB zip, ~250 MB DuckDB).
Skripte: `scripts/explore.py` (pregled CSV-ova), `scripts/load.py` (učitavanje u DuckDB),
`scripts/probe_queries.py` (probni upiti).

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
| datum | **nema stupca** | datum je samo u nazivu arhive; loader dodaje `price_date` |

## DuckDB (`data/mealmeter.duckdb`)

Učitano sirovo, bez normalizacije (`scripts/load.py`):

- `stores(chain, store_id, type, address, city, zipcode)`: 1.512 redaka
- `products(chain, product_id, barcode, name, brand, category, unit, quantity)`: 477.526 redaka
- `prices(chain, store_id, product_id, price, unit_price, best_price_30, anchor_price, special_price, price_date)`: 17.316.247 redaka

Svi identifikatori su `VARCHAR` (zbog vodećih nula). Cijene su `DECIMAL(10,2)`, a svaka neprazna
vrijednost se uspješno parsirala.

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

1. **Datum**: `prices` nema datum. Smijemo li pretpostaviti da su sve cijene iz arhive `D` važile na dan `D`?
   Mape u zipu imaju vremena 21:30–21:57, pa je moguće da je ovo stanje s kraja dana.
2. **Eurospin `price` vs. `special_price`**: drugačija semantika od ostalih lanaca. Je li to namjerno
   u cijene.dev ili greška u scraperu? Treba li to prijaviti uzvodno?
3. **Duplikati**: kad se `unit_price`/`anchor_price` razlikuju za isti (store, product), koji red je točan?
   Za sada uzimamo `min()`.
4. **Normalizacija EAN-a**: treba li 11-znamenkaste kodove nadopuniti nulom na 12 znamenki, a EAN-13
   koji počinju s `0` svesti na UPC? Na taj način se dodatno povezuju proizvodi među lancima.
5. **Gramatura**: treba li `quantity` parsirati po lancu, uzimati gramaturu iz naziva ili kombinirati
   oboje? Što kad se dva izvora ne slažu (Metro, Boso)?
6. **dm i Lorenco** nemaju trgovine. Treba li ih prikazivati za svaki grad (ima li Lorenco uopće
   nacionalnu prodaju?) ili ih isključiti iz pretrage po gradu?
7. **Gradovi**: trebaju li „Sesvete“ i „Zagreb-Dubrava“ ulaziti u „Zagreb“? Treba li nam mapiranje
   grad → županija ili poštanski broj za „u blizini“?
8. **Roto `price = 0.00`** (4 %): je li proizvod nedostupan ili je cijena nepoznata? Takve retke za sada isključujemo.
9. **Pretraga po nazivu**: kratice i nedostatak dijakritike (`BRAŠ.PŠ.`, `BRASNO`, `POD.` = Podravka)
   traže normalizaciju (strip_accents, rječnik kratica) ili fuzzy/FTS pretragu.
10. **Pokrivenost**: koliko dana povijesti vrijedi držati (trend, `best_price_30` sami izračunati)?
    Svaka arhiva ima oko 123 MB.
