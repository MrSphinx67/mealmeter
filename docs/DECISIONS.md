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

## Korak 2A2: ispravci rječnika nakon ručnog pregleda (2026-10-20)

23. **Pogrešna isključenja uklonjena.**
    - `pse\b` → `za pse`: „BRAŠ.PŠE.“ je pšenično brašno, a ne hrana za pse.
    - Uklonjeni su i `kutija`, `kolac`, `gala`, `jela`, `ben`, `kras`, `natur`, `list`, `korijen` i `ribani`.
    - Novi atributi: peršin `dio=list|korijen`, tvrdi sir `oblik=ribani`.
    - **Luk „rukavac“ je običan svježi luk u mrežici od 4 komada** („LUK CRVENI RUKAVAC 4/1“). Isključenje
      `rukavac` je zato pogrešno, ali je ostavljeno dok vlasnik ne odluči.
24. **Neprehrambene kategorije.** `category_group` normalizira 1.357 kategorija lanaca u hrana, pice,
    kozmetika, higijena, kucanstvo, djeca, sunce, igracke, ljubimci i ostalo (97 tis. proizvoda nema
    kategoriju).
    - Kozmetika, higijena, kućanstvo, djeca, sunce, igračke i ljubimci nikad se ne vežu za namirnicu.
      Ljubimci nisu bili na popisu, ali su očito neprehrambeni.
    - Takav proizvod se **samo izbacuje iz grupe** (`drop_reason`) i ne ruši cijelu EAN grupu.
    - Dodani su `must_not_match` uzorci po namirnici iz pregleda, s dvije napomene:
      - **ulje: umjesto `sun` dodani su `sun\b` i `suncan`**, jer bi prefiks `sun` isključio suncokretovo ulje.
      - **`kos` isključuje i „ULJE KOŠTICA GROŽĐA“**, koje je jestivo.
25. **Sustavna pravila** (polja u `staples.yaml`, tablica `clean.staple_rules`):
    - `plausible_per_unit`: vrijednosti vlasnika za mlijeko, brašno, šećer, sol, ulje, maslinovo ulje
      i maslac; za jaja **prijedlog** 0,1–1,5 €/kom. Cijena izvan raspona je `price_suspect`: ne ulazi
      u raspon `price_per_unit_min/max` (ni u plan_basket), a broj takvih cijena vraća se kao
      `n_price_suspect`. Build ispisuje broj odbačenih po namirnici.
    - `clearance`: naziv sadrži „SNIŽEN…“ (SNIŽENJE/SNIŽENO/SNIŽENI/SNIŽENA). Takvi proizvodi se ne
      prikazuju u zadanom izboru, a `include_clearance=True` ih vraća.
    - `default_exclude_variants`:
      - brašno: integralno i bez glutena (novi atribut `gluten`)
      - tjestenina: integralna i bez glutena
      - mlijeko i jogurt: bez laktoze
      - sol: himalajska
      - šećer: smeđi
      - riža: integralna

      **„kokos“ nema atribut**, jer je kokosovo brašno, mlijeko i šećer već isključen kroz `must_not_match`.
    - `min_pack`/`max_pack`: **vrijednosti su moj prijedlog za pregled** (npr. brašno 500–5000 g,
      maslac 100–1000 g, mlijeko 500–2000 ml). Pakiranje izvan raspona dobiva `drop_reason='pakiranje'`.
    - **Promjenjiva težina** („CCA“, „1-1,5KG“): nema pakiranja ni iz stupca `unit` ni preko EAN-a, pa je
      `unit_confidence='low'` (cijena po kg od lanca).
    - **Konzerve:** `parse_pack` sada vraća **bruto**, a `parse_drained` ocijeđenu masu. To mijenja
      ponašanje iz Koraka 1, gdje je „565g/340g“ davalo 340. `clean.prices.price_per_kg_drained` se
      vraća uz bruto `price_per_unit`.
    - **Višestruka pakiranja:** „3*80G“, „7GX5“, „4+1 GRATIS“, „3/1“, „6 PAK“, a „2x80“ bez jedinice
      tumači se kao grami. Mala gramatura (≤ 30 g, i po komadu < 5 g) uz broj komada se množi
      („7 g 4+1“ = 35 g); veća se uzima kao ukupna („35G 4+1“, „5+1 48GR“). „-25/1-“ je broj u kartonu
      i ne tumači se.
    - **Vrećice:** `compare_by: pack` (kvasac 7 g, svježi 42 g; vanilin šećer 8 g; prašak za pecivo
      12 g), pa je cijena po vrećici (`per_unit='vrecica'`).
    - `pantry`: papar, sol, mljevena paprika, ocat i dodatak jelima. Polje se vraća u izlazu, a koristit
      će ga plan_basket (cost_used).
26. **Atributi.**
    - Riža ima točno 8 vrsta; originario nije arborio, a „oro“ nije parboiled.
    - Mlijeko dobiva `mast=0` za „0%“. **„LAGANO JUTRO“ je Dukatova linija bez laktoze**: od 72 takva
      naziva 5 izričito kaže „BEZ LAKTOZE“, a nijedan suprotno. Uzorak `laktoza=bez` zato uključuje
      „lagano jutro“. Ranije se oznaka dobivala samo preko EAN grupe, pa je bila nedosljedna.
    - **Jaja:** broj komada iz „10/1“ i „10 KOM“ (`compare_by: count`, cijena po jajetu). Grupiraju
      se po klasi („jaja:m“, `group_by: velicina`), a ne po EAN-u. „S“ je i prijedlog, pa se veličina
      S prepoznaje samo uz razred/vel./kl. ili u zagradi.
    - Krumpir dobiva `namjena=kuhanje|pecenje|salata`.
    - `find_products` vraća `attribute_sources`: za svaki atribut naziv proizvoda iz kojeg je izvučen.
27. **Sadržaj.**
    - Voda, kruh i kava su `disabled` (u YAML-u, ali se ne grade i ne mogu se tražiti).
    - Nova namirnica `rajcica_konzerva` (pelati, polpa, sjeckana); polpa je izašla iz pasirane rajčice.
    - Grah, leća, slanutak, grašak, kukuruz i gljive dobivaju `oblik=konzerva|suho|smrznuto|svjeze`.
      Zadana vrijednost ako ništa ne pogodi (`attributes._default`): mahunarke suho, kukuruz konzerva,
      gljive svježe, grašak bez zadane vrijednosti.
    - Junetina i svinjetina traže dio mesa (`require_any`). Prefiks `junec` sada hvata
      „JUNEĆI BUT/VRAT/FILEKI“, pa je junetina narasla s 74 na 288 grupa.
    - Mljeveno meso: zadani filtar `vrsta=mijesano` (`default_attributes`), a naziv bez vrste računa
      se kao miješano.
    - **Zelena salata = glavice.** U podacima postoje: iceberg/ledenka (oko 30 proizvoda u 20 lanaca),
      puterica (31), kristalka i lollo. „Ledena“ i „glavatica“ se ne pojavljuju. Rukola, matovilac,
      radič i endivija su nove zasebne namirnice.
    - `loose_produce` odbija staklenke („6-9 cm“, ocij/ocj, kis).

## Korak 2B, ispravci rječnika (2026-10-20)

28. **Luk „rukavac“ je uključen.** Polje `packaged: {pattern: rukavac, default_g: 500}`: pakirani
    luk bez gramature u nazivu dobiva pretpostavljenih 500 g (`product_staples.assumed_g`), uz
    `unit_confidence='low'` i `pack_source='assumed'`. Kad je gramatura u nazivu, koristi se ona.
29. **Ulje.** `kos` je zamijenjen s `za kos|kosu\b|kose\b`, pa je ulje od koštica grožđa dopušteno.
    - Atribut `vrsta`: suncokretovo, repičino, biljno, te specijalna avokado, sezam, kokos, grožđe i
      specijalno (pistacija, konoplja, orah, kikiriki, badem…). Specijalna su u
      `default_exclude_variants`, pa zadani izbor sadrži samo uobičajena jestiva ulja.
    - Ulja bez prepoznate vrste („ZVIJEZDA OMEGOL“) ostaju u zadanom izboru.
    - **Sukob u zahtjevu:** točka 5 traži `avokad` u `must_not_match`, a točka 2 avokado kao
      specijalnu varijantu. Provedena je točka 2, jer bi `must_not_match` ulje avokada učinio
      nedohvatljivim. Iz zadanog izbora ispada svejedno.
    - „ULJE EDM“ (ekstra djevičansko maslinovo) isključeno je iz ulja kroz `edm|masli|djev|devic`.
30. **Porijeklo atributa.** `product_attrs.how` i `attribute_sources[atribut].how`:
    - `name`: vrijednost izričito piše u nazivu
    - `inferred`: zaključena (`inferred_attributes`, npr. LAGANO JUTRO → laktoza=bez)
    - `default`: nijedan uzorak nije pogodio (`attributes._default`)

    U pregledu su označene kao „(zaključeno)“ i „(zadano)“.
31. **Odbačene cijene i automatske granice.** Namirnice bez ručnog `plausible_per_unit` dobivaju
    granice 0,25x–4x medijana cijene po jedinici namirnice (`clean.staple_rules.range_source='auto'`,
    65 namirnica). Pretraga i košarica čitaju granice iz `clean.staple_rules`.
    - `docs/price_outliers.md` pokazuje odbačene grupe za namirnice s > 5 % odbačenih cijena.
    - Na temelju izvještaja dodani su krivi pogoci:
      - maslac: tikva, salata, tost/toast, povrće, focaccia
      - mlijeko: lončić
      - sol: šol (komad govedine)
      - ocat: balsamico i začinski
      - krumpir: pekarski, curly fries, krumpiruša
      - kečap: grickalice
      - krušne mrvice: nuggetsi
    - Luk: mladi luk i ljutika su zadano isključene varijante.
    - Iznad 5 % ostaju kvasac (18 %; rinfuza od 100–500 g je stvarno jeftinija po vrećici, pa ju
      automatska granica penalizira), luk (5,6 %; ljutika i borettane su skupi, ali su zadano
      isključeni) i sol (5,1 %; himalajska i cvijet soli).
32. **`docs/ranges.md`** sadrži sve `min_pack`/`max_pack` i granice cijena.
33. **Konzerve.** `pack_amount` je neto masa **s tekućinom** (bruto sadržaj), a `drained_amount`
    ocijeđena masa. Vidi SCHEMA.md.
34. **`pack_confidence`** (`clean.products`) je `low` kad gramatura ovisi o heuristici višestrukog
    pakiranja: „4+1“, „3/1“ i „PAK“ uz jednu gramaturu, „2x80“ bez jedinice, ili višestruko
    pakiranje uz „gratis“. U košarici takvi proizvodi nisu zadani izbor. „4+1 GR.“ više se ne čita
    kao grami.
35. **Oblik bez oznake je `nepoznato`** (`attributes._default`) za grah, leću, slanutak, grašak,
    kukuruz, gljive i rajčicu u konzervi. Ništa se ne pogađa, pa ni suho. „Podložak“ i „bez korijena“
    kod gljiva znače svježe.
36. **Neprehrambeni proizvodi.** Uz kategorije, `_defaults` dobiva uzorke za proizvode pronađene
    među kandidatima lanaca bez kategorije: sjeme, igračke, stolica „jaje“, vrtni luk, motorno ulje
    (Valvoline, 10W), citronela, folija za jaja.

## Korak 2B, Dio B: plan_basket (2026-10-20)

37. **`plan_basket(ingredients, city, mode="single_store")`** (`src/mealmeter/basket.py`).
    - Sastojak je `{name, amount, unit, form?, attributes?}`.
    - **Naziv** se razrješava kao točan sinonim namirnice, ili sinonim + vrijednosti atributa
      („glatko brašno“ → brasno, tip=glatko). Sinonim koji je i vrijednost atributa postavlja taj
      atribut („špageti“ → tjestenina, oblik=spageti).
    - Nepoznata namirnica, jedinica ili atribut ide u `unmatched` s razlogom.
    - **Jedinice:** g, dag, kg, ml, cl, dl, l, kom (komad, režanj/češanj, glavica) i vrećica.
      Žlica (15), žličica (5) i prstohvat (0,5) pretvaraju se uz gustoću 1 i upozorenje. Komad se
      pretvara u grame preko `piece_g` (luk 150 g, češanj 5 g, jaje 60 g…). g↔ml uz upozorenje.
    - **Dvosmislen oblik** (`ambiguous_form`: grah, leća, slanutak, grašak, kukuruz, gljive;
      `form_staples`: rajčica → svježa/konzerva/pasirana/koncentrat). Bez `form` bira se oblik
      najjeftiniji za traženu količinu u gradu i vraća upozorenje s `assumed_form` i cijenama ostalih
      oblika. **Prinos se ne uzima u obzir** (suhi grah naraste otprilike 2,5x). Proizvodi s
      `oblik=nepoznato` ne ulaze kad je oblik zadan ili pretpostavljen.
    - **Odabir u trgovini** (`choose_product`):
      1. Kandidati bez zastavica (rasprodaja, `price_suspect`, `pack_confidence=low`, lanac
         `suspect`); samo ako takvih nema, uzimaju se označeni (`fallback=true`, `flags`).
      2. Najmanje pakiranje koje pokriva količinu; uz jednaku veličinu najjeftinije.
      3. Inače najjeftinije po jedinici, u potrebnom broju pakiranja.
      - Konzerve koriste `drained_amount`, a vrećice i jaja `n_units`.
      - **Kupnja na vagu** (cijena po kg bez pakiranja) dopuštena je samo za `loose_produce` i robu
        promjenjive težine, jer bi inače npr. „Šećer kristal 25/1 kg“ bez gramature izgledao kao
        0,01 € za žlicu.
    - **Iznosi:** `cost_pack` (cijela pakiranja) i `cost_used` (razmjerno). U `total` ulazi
      `cost_pack`, a za `pantry` namirnice `cost_used` (`counted`).
    - **Trgovine:** grad preko aliasa + `scope=national`. Nepoznat grad vraća `city_suggestions`
      (difflib nad nazivima gradova) i nijednu trgovinu.
    - **Poredak trgovina:** broj povezanih sastojaka, lanac nije `suspect`, broj označenih stavki,
      ukupno. `best_store` je prva trgovina koja nije `suspect` (Lorenco), osim ako drugih nema;
      tada ide upozorenje.
    - Izlaz: `ingredients` (s pretpostavkama), `unmatched`, `stores` (stavke, `total`,
      `n_matched`, `missing`, `unit_confidence`, `date`, `date_hr`), `best_store` i `warnings`.
    - Podržan je samo `mode="single_store"`.
38. **`get_prices` prima id klase** („jaja:m“) za namirnice s `group_by`.
39. **Isključenja otkrivena kroz košaricu** (Plodine nemaju kategorija): „DEKORACIJA ZA JAJA“ i
    „BOCA ZA ULJE“ idu u `_defaults`.
    - Šećer u prahu i u kockama, te sol sa smanjenim natrijem, zadano su isključene varijante
      (**moja odluka**: za generički „šećer“ i „sol“ to nije očekivani proizvod).
    - Rinfuza (RFS/RFZ) kod mahunarki znači suho na vagu, a ne svježe.
40. **Recepti** su u `data/recipes/test_*.json` (palačinke, grah, bolonjez), u gitu kroz iznimku u
    `.gitignore`. CLI: `python -m mealmeter.cli basket data/recipes/test_grah.json --city Osijek`.

## Korak 2C: filtar hrane i ispravci rječnika (2026-10-20)

Izvještaji za pregled su u [MORNING_REVIEW.md](MORNING_REVIEW.md) (`scripts/morning_review.py`).

41. **Filtar hrane** (`src/mealmeter/food.py`, stupci `clean.products.food_group`, `is_food`, `category_source`).
    - Skupine: hrana, pice, alkohol, kozmetika, higijena, kucanstvo, djeca, kucni_ljubimci, ostalo,
      te `unknown` kad se ne zna. `is_food` je `true` za hrana/pice/alkohol, `false` za ostale, a
      **`NULL` za `unknown`** (umjesto teksta 'unknown', da SQL ostane trovrijednosni).
    - **`data/category_map.yaml`** (1.334 normalizirane kategorije, u gitu kroz iznimku u `.gitignore`)
      izrađen je pravilima iz `normalize._CATEGORY_RULES` (`scripts/make_category_map.py`) i može se
      ručno ispravljati. Kategorije izvan mape idu kroz ista pravila.
    - Stare skupine `sunce` → kozmetika, `igracke` → ostalo, `ljubimci` → `kucni_ljubimci`;
      „NEPREHRANA“ (Tommy) → ostalo; „PAKIRANA HRANA I PIĆE“ → pice.
    - **„Ostalo“ je `unknown`, a ne neprehrambeno**: kod NTL-a, trgovine Krk, Gavranovića i Žabca
      (28.559 proizvoda) miješa svrdla i ručnike s gastro hranom („MIJEŠANO MLJEVENO MESO ZA GASTRO 1 kg“).
    - Alkohol: kategorije vina, piva i žestica, te u kategorijama pića naziv (vino, pivo, rakija, marke
      piva i žestica, postotak alkohola 3,5–80 % osim sokova, nektara i mliječne masti).
      „0,0 %“/„bezalkoholno“ je `pice`.
    - **Hrana za ljubimce u kategoriji hrane** („HRANA ZA PSE …“ u Hrana) je `kucni_ljubimci` (moja
      dopuna nakon uzorka; „Felix“ nije na popisu jer je i marka kečapa i kiselih krastavaca).
    - Nasljeđivanje: proizvod bez korisne kategorije dobiva skupinu istog globalnog EAN-a iz lanaca s
      kategorijom ako ju ima **više od 50 % glasova** (jedan glas po proizvodu u lancu); inače `unknown`.
    - Riječi (samo kad ni kategorija ni EAN ne pomažu): popis iz zahtjeva, uz tri ispravka:
      `pse` samo kao cijela riječ i ne iza „bras“ (prefiks bi pogodio „PŠENIČNO“), `sjeme` samo kao
      cijela riječ („KRUH SA SJEMENKAMA“). Dodano: čaše i pribor za piće (`casa`, `depozit`,
      `otvarac`…, osim jogurta „u čaši“) i opće alkoholne riječi (vino, pivo, rakija…), jer bi inače
      „ČAŠA ZA PIVO“ i vino iz Plodina ostali `unknown`.
    - **Zadano:** `find_products` i `get_prices` vraćaju samo `is_food = true` bez alkohola; parametri
      `include_nonfood`, `include_alcohol`, `include_unverified` (CLI `--include-*`). Grupa samo od
      `unknown` proizvoda nosi `food_unverified = true`.
    - **`plan_basket`:** `unknown` samo za `loose_produce` i samo proizvod koji je sam prošao pravilo
      namirnice (riječ je prva ili druga u nazivu); stavka nosi `food_unverified`, ali bez kazne u
      poretku trgovina. Alkohol i neprehrambeno nikad (`drop_reason = 'kategorija:<skupina>'`).
    - **Dječja hrana** (dm „bebe & djeca“, „DJEČJA HRANA“) ostaje u skupini `djeca`, dakle izvan zadanog
      izbora, kao i u Koraku 2A2.
    - Brojke (arhiva 2026-10-19): Plodine 29,8 % naslijeđeno preko EAN-a, 49.890 ostaje `unknown`
      (velik dio su neprehrambeni artikli kojih nema u drugim lancima); Lorenco 71,4 %, 4.735 `unknown`.
42. **Jaja.**
    - Isključeni su i obuća, folija, termoskupljajuće, stolica, glazbeno i igr*.
    - Novi atribut `uzgoj`: bio (BIO/EKO, provjerava se prvi), kavezni, podni, slobodni, inače `nepoznato`.
    - `group_by` je sada popis atributa (`[velicina, uzgoj]`), pa su klase `jaja:m:podni`.
      `get_prices` prima i kraći id (`jaja:m` = svi uzgoji). Proizvod bez veličine ostaje u svojoj EAN grupi.
    - `plan_basket` uz svaku stavku vraća `attributes` odabranog proizvoda (veličina i uzgoj; za mlijeko vrsta i mast).
    - **`plausible_per_unit: [0.19, 0.47]`**: 5.–95. percentil cijene po jajetu za različite proizvode
      (provjerena hrana), umjesto mog prijedloga [0.1, 1.5].
      - Ispadaju Metroovi kartoni (1,30–4,41 €/kom, „10/1“ je broj kutija) i greške (0,01 €/kom).
      - Ispada i 5 od 11 bio proizvoda (do 0,53 €); vidi MORNING_REVIEW.md.
43. **Zadane varijante** (`default_exclude_variants`, vraćaju se kad je atribut izričito zadan).
    - Brašno: `vrsta` bez oznake je `psenicno`; kukuruzno, pirovo, raženo i heljdino su varijante.
      `heljd` je maknut iz `must_not_match`, pa je heljdino brašno dohvatljivo s `vrsta=heljdino`.
    - Šećer: `vrsta` bez oznake je `bijeli`; u prahu, kocke i smeđi ostaju izvan zadanog.
    - Ulje: nove vrijednosti `vrsta=omegol|mediteran` (Zvijezdine mješavine) i atribut `presanje=hladno`,
      sve izvan zadanog. To mijenja odluku 29, gdje je Omegol ostajao u zadanom izboru.
    - Rajčica: cherry (i koktel, cocktail, mini), datterino (i „daterino“), harmony i campari su izvan zadanog.
    - Riža: „oro“ ne daje `parboiled`; parboiled dolazi samo iz riječi u nazivu (sada i „PARABOILED“).
      Grupa Scotti Oro (8001860190520) je parboiled jer tako glasi naziv u 10 lanaca.
44. **Kakao: pozitivno podudaranje.** `must_match` je sada `^kakao\b`, „kakao prah“, „prah kakao“, „kakao u
    prahu“, „kakao u pr.“ i „kakao za kolač…“. Uz isključenja iz zahtjeva dodao sam desert, kolač, rolice,
    šnite, biskvit, krafne, tablu (čokolada), instant/vending napitke, Dolce Gusto, „XXL“ i Lumpi.
    Lidl naziva takve proizvode „Kakao …“. Broj grupa: 173 prije, vidi MORNING_REVIEW.md za poslije.
45. **Pileća prsa:** `plausible_per_unit: [5, 20]` €/kg (vlasnik). Grupe s „jeli“/„je li“ (Gavrilović Jeli,
    delikatesna prsa) su **privremeno isključene** dok vlasnik ne potvrdi (MORNING_REVIEW.md, točka 4).
46. **Luk:** samo izvještaj (MORNING_REVIEW.md, točka 5), mapiranje boja nije mijenjano do potvrde vlasnika.
47. **Sol:** `soljenk` je maknut iz `must_not_match`. Novo polje `require_pack` (`clean.product_staples.drop_reason =
    'bez_gramature'`): proizvod koji pogađa uzorak ispada samo ako nema gramature. „SOL MORSKA SITNA 250G
    SOLJENKA“ je sol.
48. **Mlijeko.**
    - Zadano je `vrsta=trajno, mast=2.8` (`default_attributes`, i u `find_products`).
    - Novo polje `substitutes: {mast: [2.8, 3.2, 3.5, 3.8]}`: tražena ili zadana masnoća iz skupine prihvaća
      svaku masnoću iz skupine. Svježe i trajno ostaju zasebne vrste.
    - Mlijeko bez oznake vrste u nazivu ne ulazi u zadani izbor (nema pogađanja); vidi raspodjelu u MORNING_REVIEW.md.
    - `plan_basket` po sastojku vraća `applied_attributes` i `accepted_values`, a po stavci `attributes`
      odabranog proizvoda (vrsta, mast). Zamjena (npr. „mast=3.2 umjesto 2.8“) ide u `notes`.
    - Prepoznaje se i „TR“ (trajno) i „SV.“ (svježe).
    - Isključeni su acidofilno, kiselo („KIS.“), protein, „ČOKOL.“ i palačinke.
49. **Peršin:** `unit: kg` (bio je `kom`) i `pantry: true`. Vezice i komadi bez gramature nemaju cijenu po kg i
    ne pretvaraju se. „vezica“ je poznata jedinica recepta, ali bez `piece_g` daje `unmatched`. Drugog
    svježeg bilja u rječniku nema.
50. **Pretvorba mjera** (`data/units.yaml`, `src/mealmeter/units.py`, `convert(amount, unit, staple)`).
    - Žlica 15 ml, žličica 5, šalica 250, dcl 100, prstohvat 0,5, čaša 200.
    - Gustoće (g/ml): brašno 0,55, šećer 0,85, sol 1,2, ulje 0,92, mlijeko 1,03, maslac 0,95, riža 0,85.
    - **Sve su procjene** (`estimate: true`) i čekaju pregled. Ostale namirnice računaju se s 1 g/ml, uz upozorenje.
    - `plan_basket` koristi `units.convert` umjesto ugrađenih žlica (prije: gustoća 1 za sve), pa je
      1 žlica šećera sada 12,75 g, a ne 15 g. Gustoća vrijedi i za g ↔ ml (npr. 103 g mlijeka = 100 ml).
51. **Kvasac, prašak za pecivo, vanilin šećer: granice po vrećici.**
    - Novo polje `plausible_per_pack` (€ po vrećici, `range_source = 'pack'`) zamjenjuje automatske granice.
    - Prijedlog iz podataka je [p5, 1,25 × p95] cijene pojedinačnih vrećica, zaokruženo na 0,05 €:
      kvasac 0,30–1,25, prašak 0,10–0,40, vanilin šećer 0,10–0,85.
    - `price_suspect`: cijena po vrećici iznad gornje granice, ili pojedinačna vrećica (≤ 1,5 vrećice u
      pakiranju) ispod donje. Rinfuza i višestruka pakiranja nisu kažnjeni zbog niže cijene po vrećici.
52. **Oblik mahunarki, kukuruza i gljiva** (`staples.form_heuristic`, polje `dry_rule`, `product_attrs.how = 'heuristic'`).
    - Oznake konzerve: dodani NALJEV i OC.MASA. Oznake smrznutog: dodani FROZY, FRESCO i ZAMRZ. Obje se
      provjeravaju i u stupcu `unit`.
    - Suho: pakiranje 400–1000 g, bez oznaka konzerve i smrznutog, a `unit` je rinfuza ili naziv sadrži PVC,
      vrećicu, NATURA, VEDRINI, PRIMAVITA ili ADVENT. Vrećica i PVC izvan tog uvjeta više ne znače suho.
    - Gljive nemaju `dry_rule`.
    - U pretrazi heuristika ima manju prednost od naziva i zaključka, a veću od zadane vrijednosti.
53. **cijene.dev ne traži API ključ** za popis arhiva ni za preuzimanje (HTTP 200/206, vidi SCHEMA.md), pa
    `update.py` nije mijenjan.

## Korak 2D: razrješavanje grupa, zadani izbori, mjere (2026-10-20)

Izvještaji: [STEP2D_REVIEW.md](STEP2D_REVIEW.md) (`scripts/step2d_review.py`) i [REVIEW_FOR_CHAT.md](REVIEW_FOR_CHAT.md).

54. **Pripadnost grupe namirnici** (`clean.staple_groups`, `clean.staple_group_attrs`).
    - Grupa (globalni EAN, inače lanac + naziv) je `member` ako naziv prolazi pravila u > 50 % lanaca grupe i
      nijedan isključeni naziv nema udio ≥ 25 % lanaca.
    - Inače je `ambiguous` (izvan zadanog izbora, `find_products(include_ambiguous=True)`), a `excluded` ako
      nijedan naziv ne prolazi (moja dopuna: takva grupa nije dvosmislena).
    - Proizvod izbačen zbog pakiranja računa se kao pogodak naziva, a neprehrambeni (`kategorija:*`) ne.
    - **Atribut grupe** je jedna vrijednost: iz naziva ispred zaključene, heurističke i zadane, zatim po
      broju lanaca. Filtri atributa i zadano isključene varijante gledaju tu vrijednost, a ne „bilo koji
      proizvod grupe“. Zato pureće mljeveno meso (u jednom lancu bez vrste) više nije zadano miješano.
    - Cijena pravila: grupe sa skraćenim ili samo markom imenovanim nazivima ispadaju (najviše tjestenina,
      202 grupe). Vidi STEP2D_REVIEW.md.
55. **Isključenja (Korak 2D.2).**
    - maslinovo ulje: kupus, kis, salat (tuna i sardin već postoje).
    - parmezan, mozzarella, maslac, tvrdi i svježi sir: biljn, vegan, greenvie/green vie, zamjen.
    - grah, leća, slanutak, grašak: kob\b, sipa, brudet, orzo.
    - `felix` je maknut iz `_defaults` (Felix je i kečap). Hrana za ljubimce isključuje se kroz macke, za pse,
      psa\b i novi `hrana za`.
    - Gramatura: jedinica zalijepljena za iduću riječ čita se kad je jedinica malim, a iduće slovo velikim slovom
      („250 gVOĆARNA“, „500gPAGANI“). „5 LIMUNA“ i dalje nije 5 l.
56. **Mljeveno meso:** novo polje `default_preference: {vrsta: [mijesano, junece, svinjsko]}` (umjesto
    `default_attributes: vrsta=mijesano`). `find_products` zadano vraća te tri vrste. `plan_basket` u svakoj
    trgovini uzima prvu vrstu redom koja daje proizvod bez zastavica, i kad je skuplja od iduće. Ako je to
    juneće ili svinjsko, piše to u `notes`. Pureće i pileće samo kad se traže (`attributes: {vrsta: purece}`).
