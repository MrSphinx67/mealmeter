# Odluke

Zapisnik odluka o podacima i ponašanju pretrage. Novije odluke dodaju se na kraj.

## Korak 1 (2026-10-19)

### Odluke vlasnika projekta

1. **Datum cijena** je dan iz naziva arhive (`2026-10-19.zip` → `2026-10-19`). Pohranjuje se kao
   `DATE` (ISO, `YYYY-MM-DD`) u stupcu `date`. Svaki izlaz funkcija nosi `date` (ISO string) i
   `date_hr` za prikaz korisniku u obliku `19.10.2026.` (dan i mjesec s vodećom nulom: `05.03.2026.`).
2. **dm i Lorenco** imaju `scope = 'national'`: cijena vrijedi za sve gradove. U izlazu takvi retci
   nose napomenu „Nacionalna cijena (web/sve poslovnice); provjeri dostupnost u svom gradu.“ Sve
   ostale trgovine imaju `scope = 'local'`.
3. **Gradovi**: alias tablica (`clean.city_alias`, izvor `CITY_ALIASES` u `normalize.py`) i
   usporedba bez dijakritika i bez razlike u velikim/malim slovima. Aliasi:
   - Sesvete, Sesvete - Kraljevec, Sesvetski Kraljevec, Zagreb-Dubrava, Dubrava, Novi Zagreb,
     Lučko, Kašina → **Zagreb** (svi su u sastavu Grada Zagreba)
   - V.gorica → Velika Gorica, Hrv.kostajnica → Hrvatska Kostajnica, Umag-Umago → Umag,
     Laslovo (szentlaszlo) → Laslovo
   - Kaštel Gomilica/Kambelovac/Lukšić/Novi/Stari/Sućurac/Štafilić → **Kaštela**

   Pretraga po gradu pogađa i kanonski naziv i izvorni naziv, pa „Kaštel Stari“ vraća samo tu
   trgovinu, a „Kaštela“ sve. „Sesvete“ se svodi na Zagreb, dakle vraća sve zagrebačke trgovine.

### Provjera pravila `price_eff = coalesce(nullif(special_price, 0), price)`

Provjereno na sirovim podacima prije čišćenja (`scripts/build_clean.py` ispisuje provjeru pri
svakom pokretanju):

| lanac | artikl | price | special | best_30 | anchor | unit_price | price_eff |
|---|---|---|---|---|---|---|---|
| eurospin | MED CVJETNI 500g (Osijek 310017) | 3,15 | 2,69 | 3,15 | 3,98 | 6,30 | **2,69** |
| konzum | DATULJA DEGLET NOUR 200g (Zagreb 0001) | 0,90 | 0,90 | 1,35 | 1,15 | 4,50 | **0,90** |

- **Eurospin**: `price` je redovna cijena, a `special_price` akcijska. `best_price_30` (3,15) je
  najniža cijena u 30 dana prije akcije, a `unit_price` 6,30 = 3,15 / 0,5 kg računat je iz redovne
  cijene. Kupac plaća 2,69.
- **Konzum**: `price` je već snižena i jednaka `special_price`. `unit_price` 4,50 = 0,90 / 0,2 kg,
  a `best_price_30` 1,35 je cijena prije akcije. Kupac plaća 0,90.
- Na svim akcijskim recima u arhivi vrijedi isto: kod 19 lanaca `special_price = price` u 100 %
  slučajeva, a kod Eurospina `special_price < price` u 100 % slučajeva (13.879 redaka). Nijedan
  lanac nema `special_price > price`. Pravilo zato daje točnu cijenu za kupca u oba slučaja.
- Ograničenje: provjera je unutarnja (dosljednost stupaca i `unit_price`), a ne usporedba s
  cijenom na polici ili webu trgovine.

### Odluke donesene tijekom implementacije

4. **`0.00` → NULL** u svim cjenovnim stupcima (`price`, `unit_price`, `best_price_30`,
   `anchor_price`, `special_price`). Cijena od 0 € u ovim podacima nikad nije stvarna.
5. **Retci bez cijene se izbacuju** iz `clean.prices` (Roto 3.480, NTL 3.583, Gavranović 550,
   Tommy 212 i drugi; ukupno ~8.000).
6. **Duplikati** `(chain, store_id, product_id)`: zadržava se red s najnižom `price_eff`, a
   izjednačenja rješava redom `unit_price`, `anchor_price`, `best_price_30` (NULL na kraju).
   `price` je kod duplikata gotovo uvijek isti (iznimke su Studenac s 19 parova i Ribola s 3).
7. **`is_special`** = `special_price IS NOT NULL` (nakon 0 → NULL). Redovna cijena za akcijske
   artikle poznata je samo kod Eurospina. Kod ostalih lanaca `price` je već snižena, pa se
   „ušteda“ ne može pouzdano izračunati (`best_price_30` i `anchor_price` nisu redovna cijena).
8. **EAN**:
   - 11 znamenki + vodeća nula = valjani UPC-A → svodi se na EAN-13 (`11210000018` →
     `0011210000018`). Od 1.962 takva koda 1.935 postaje valjano.
   - Svi UPC-A (12) i GTIN-14 s vodećom nulom također se svode na EAN-13, da se isti proizvod
     podudara među lancima.
   - `ean_valid` = kontrolna znamenka je ispravna (EAN-8 ili EAN-13 nakon normalizacije).
   - Dodatni stupac **`ean_global`**: `false` za kodove ograničene upotrebe (EAN-13 s prefiksom
     `2`, `02`, `04`; EAN-8 s prefiksom `0` ili `2`; to su vaga i interni kodovi trgovine). Takvi
     kodovi su valjani, ali isti broj u dva lanca nije isti proizvod, pa se po njima **ne grupira**.
9. **Gramatura** (`pack_amount`, `pack_unit` ∈ {`g`, `ml`, `kom`}; izvor u `pack_source`):
   - `name`: parsirano iz naziva (`normalize.parse_pack`). Prioritet je višestruko pakiranje
     (`6x0,33 l`, `30G*20`), zatim ocijeđena masa (`185g ocijeđ.mase 130g`, `565g/340g` → drugi
     broj), zatim masa/volumen, pa komadi.
   - `unit`: **proširenje izvorne specifikacije.** Lidl ne piše gramaturu u naziv, nego u stupac
     `unit` (`80g`, `10x1kg`). Bez toga bi samo 8 % Lidlovih cijena imalo cijenu po kg, a s tim
     je 97 %, uz 92 % slaganja s Lidlovim `unit_price`. Miks varijanti (`123g,200g,77g`) se ne
     tumači.
   - `ean`: **proširenje.** Proizvod bez gramature u nazivu (`BRAŠNO GLATKO 1/1`) nasljeđuje je
     od drugih lanaca s istim globalnim EAN-om, ali samo ako se svi parsirani nazivi za taj EAN
     slažu (~19.700 proizvoda).
   - Ne tumači se: `5/1`, `10/1` (u hrvatskim nazivima to može biti 5 kg, 10 komada ili broj
     komada u kutiji), `(10)`, dimenzije (`110X140 CM`), oznaka dobi (`+1g`, `1g.+` je
     „od 1 godine“, a ne 1 gram) i nazivi s `cca` (promjenjiva težina, cijena je po kg).
10. **`price_per_unit`** (`per_unit` ∈ {`kg`, `l`, `kom`}, `unit_confidence`):
    - `high`: gramatura iz `pack_source` (naziv, a za Lidl i stupac `unit` te EAN):
      `price_eff / pack_amount × 1000` (ili `/ pack_amount` za komade).
    - `low`: lančev `unit_price × price_eff / price` (skaliranje ispravlja Eurospin, gdje je
      `unit_price` računat iz redovne cijene). Koristi se samo kad je jedinica poznata iz stupaca
      `quantity`/`unit` (kg ili l). Inače `price_per_unit` ostaje NULL.
    - Lančev `unit_price` nije pouzdan izvor: kod Branke, Stanića i Žabca slaže se s našim
      izračunom u samo 4–15 % slučajeva (tamo je to cijena pakiranja).
11. **`name_norm`** = mala slova, bez dijakritika, `đ` i `dj` → `d`, interpunkcija → razmak
    (`BRAŠ.PŠ.GLATKO T-550` → `bras ps glatko t 550`). Računa se za sve proizvode (ne samo svježe),
    jer se po njemu pretražuje. Ista funkcija normalizira upit.
12. **Trgovine**: Sparovim adresama uklonjen je sufiks `„<store_id> Spar|Interspar“`. Dvjema
    Kauflandovim trgovinama bez grada grad je upisan ručno iz adrese (Lučko → Zagreb, Krk).
13. **Pretraga** (`find_products`):
    - Upit se normalizira i dijeli na riječi, a proizvod odgovara ako `name_norm` sadrži sve riječi.
    - Grupira se po `ean_norm` kad je `ean_global`, a inače po `lanac + name_norm`.
    - Grupa ulazi u rezultat ako **barem jedan** njezin naziv odgovara upitu. Tada ulaze svi
      proizvodi s tim EAN-om, pa i Sparov „BRAŠ.PŠ.GLATKO“ uz Podravkino brašno.
    - Poredak: relevantnost (udio riječi naziva koje pokriva upit, u tri razine), zatim broj
      lanaca, broj trgovina i cijena po jedinici.
    - Raspon cijene po jedinici računa se samo iz najpouzdanijeg izvora u grupi (`high` > `low`)
      i najčešće jedinice. Raspon `cijena €` uključuje sve trgovine, pa se ta dva raspona mogu
      razlikovati.
    - Prikazni naziv je naziv koji odgovara upitu i sam nosi gramaturu; od takvih se uzima najduži.
14. **`get_prices`** prima EAN (i 11/12-znamenkasti, normalizira se) ili `lanac:product_id`.
    Interni EAN (`ean_global = false`) i neispravan EAN daju jasnu grešku.
15. **Python UDF-ovi u DuckDB-u traže numpy**, pa se izvedeni stupci (EAN, gramatura,
    `name_norm`, gradovi) računaju u Pythonu i učitavaju preko privremenog CSV-a. Tako izbjegavamo
    ovisnost o numpyju.

## Korak 2 (2026-10-19)

### Odluke vlasnika projekta

16. **Odstupanja iz Koraka 1 su prihvaćena**: `pack_source` `unit`/`ean` računa se kao `high`, uz
    `ean_global`, EAN-13 kanonizaciju, pretragu po EAN grupi, „Sesvete“ = Zagreb i `date_hr` s
    vodećom nulom.
17. **Izlaz uvijek nosi `unit_confidence` i `pack_source`**, i u `find_products` i u `get_prices`
    (CLI ih prikazuje u stupcu „pouzdanost“, npr. `high/name`).
    - `pack_source` ∈ {`name`, `unit`, `ean`} kad je `unit_confidence = 'high'`.
    - `pack_source = 'unit_price'` kad je `unit_confidence = 'low'` (cijena po jedinici je od lanca).
    - Oba su NULL kad cijena po jedinici nije poznata.
18. **Lorenco ima `data_quality = 'suspect'`** (`clean.chains`, izvor je `SUSPECT_CHAINS` u
    `build.py`). Ostaje u bazi i u pretrazi (`find_products` vraća `suspect_chains`, `get_prices`
    vraća `data_quality`), ali se **isključuje iz preporuka `plan_basket`**.

### Po čemu su Lorenco podaci sumnjivi

`scripts/build_clean.py` pri svakom buildu ispisuje tablicu kvalitete za sve lance. Za Lorenco
(arhiva 2026-10-19, u zagradi je najgori među ostalim lancima):

| pokazatelj | Lorenco | ostali lanci |
|---|---|---|
| `unit_price` prazan ili 0 | 42,8 % | ≤ 6,5 % (KTC) |
| `price_eff` > 3× ili < ⅓ sidrene cijene | 19,9 % | ≤ 8,7 % (dm), većina < 1 % |
| bez kategorije | 100 % | 100 % samo Plodine |
| bez marke | 100 % | 100 % i Branka, Bure, djelo_vodice, Jadranka, Žabac |
| trgovina | jedna `all`, bez adrese i grada | dm isto (nacionalni web-shop) |

Uz to, Lorenco ima neispravne jedinice (`055`, `056`, `K0M`, `KO6`, `kođ`, `hks`, `50`; malo redaka,
ali jasno ručni unos) i besmislene sidrene cijene: „ALU PILEĆA KRILCA 1kg KOTANYI“ 17,11 € uz sidrenu
0,59 €, „TAYLORS FINE TAWNY 0,75L“ 15,40 € uz sidrenu 0,36 €.

**Napomena:** same cijene (`price_eff`) Lorenca **nisu** sumnjive. Za isti globalni EAN medijan
omjera prema ostalim lancima je 1,05, a samo 1,9 % artikala odstupa više od 2× (Konzum 4,0 %,
Studenac 11,7 %, Žabac 21,2 %). Sumnjiva su pomoćna polja i to što ne znamo gdje Lorenco prodaje.
Ako se pokaže da je Lorenco stvarni nacionalni web-shop, ovu odluku vrijedi preispitati.

### Dio A: rječnik osnovnih namirnica (`src/mealmeter/staples.yaml`)

19. **72 namirnice** s poljima `name`, `synonyms`, `must_match`, `must_not_match`, `unit` (kg/l/kom),
    `attributes` i `loose_produce`. Zajednička isključenja (hrana za ljubimce, kozmetika,
    grickalice, dječja hrana, gotova jela) su u `_defaults` i vrijede za sve namirnice.
    **Rječnik je prvi prijedlog i čeka ručni pregled** (`docs/staples_review.md`).
20. **Kako je nastao prijedlog:** za svaku namirnicu izračunate su najčešće riječi koje se u
    stvarnim nazivima pojavljuju uz nju (npr. uz „mlijek“: čokoladno, sojino, kakao, nivea, sapun…).
    Iz njih su izvedeni `must_not_match` i atributi, a zatim dorađeni prema pregledu kandidata.
    Nisam odlučivao koji su proizvodi „točni“: `scripts/staples_review.py` za svaku namirnicu ispisuje
    top 20 kandidata i top 10 isključenih (s uzorkom koji ih je isključio).
21. **Pravila podudaranja** računaju se pri buildu u `clean.product_staples` (proizvod ↔ namirnica,
    `excluded`) i `clean.product_attrs` (proizvod, namirnica, atribut, vrijednost):
    - `must_match` i `must_not_match` su RE2 uzorci na **početku riječi** u `name_norm` (prefiks je
      dovoljan, `\b` za kraj riječi).
    - Atributi su Python regexi na tekstu sa zadržanom interpunkcijom (`2,8%MM` → `2.8%mm`), jer u
      `name_norm` „2,8 %“ i „2,8 l“ izgledaju isto. Zato „Mlijeko trajno 1,5 L“ nema atribut `mast`.
    - Grupa (isti EAN) pripada namirnici ako barem jedan njezin naziv prolazi pravila, a nijedan ne
      pogađa `must_not_match`.
    - **`loose_produce`** (svježe voće i povrće) ima dodatno pravilo:
      - riječ namirnice je prva ili druga riječ naziva,
      - proizvod je bez globalnog EAN-a (vaga/PLU), bez gramature ili ≥ 500 g,
      - i nije tekućina.

      Bez toga „banana“ i „limun“ vraćaju uglavnom bombone, sokove i deterdžente s okusom.
22. **`find_products(query=None, city=None, limit=10, ingredient=None, attributes=None)`**:
    - `ingredient` je ključ ili sinonim namirnice, a `attributes` je npr. `{"tip": "glatko"}`.
      Nepoznata namirnica ili atribut daju `ValueError` s popisom dostupnih vrijednosti.
    - **Slobodan upit koji je točno sinonim namirnice** („mlijeko“, „Brašno“, „jaje“) automatski
      koristi namirnicu, pa „mlijeko“ ne vraća čokoladno ni sojino mlijeko. „Čokoladno mlijeko“ nije
      sinonim i ide kao slobodan upit.
    - Uz `ingredient` slobodan upit dodatno sužava po nazivu („podravka“ + brašno).
    - Cijena po jedinici bira se prvo u jedinici namirnice (mlijeko po l, jaja po kom).
    - Rezultat nosi `ingredient` i `attributes` grupe (najčešća vrijednost među proizvodima grupe).
    - Poredak za namirnicu: najprije grupe u kojima je riječ namirnice među prve tri riječi u
      **većini** naziva grupe („KEKS NUTRI MRKVA“ ide iza „MRKVA 1kg“), zatim broj lanaca i trgovina.
