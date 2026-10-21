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
57. **Pileća prsa: stanje.** Atribut `stanje` (smrznuto: SMRZ, LEDO, FROZ, ZAMRZ, BRAZIL; inače svježe), zadano
    svježe. Novo polje `plausible_by` daje granice po vrijednosti atributa (`product_staples.ppu_min/ppu_max`):
    svježe 3–20 €/kg, smrznuto 2–12 €/kg. `clean.staple_rules` nosi najširi raspon (2–20). „Jeli“ ostaje isključeno.
58. **Luk: sorte.** Obični luk (zadano) je crveni, žuti, kapula ili bez oznake sorte (`vrsta=obicni`).
    - Srebrenac (`srebren\w*`), ljubičasti (`ljubic\w*`, i „LJUBIČ.“), mladi, slatki, borettan, perlice i
      ljutika su vrijednosti `vrsta` izvan zadanog izbora.
    - Sorte se provjeravaju prije boje („LUK CRVENI SLATKI“ je slatki), a žuti prije crvenog
      („KAPULA ŽUTA (CRV.LUK)“).
    - „bijeli luk“ / „luk bijeli“ je češnjak i isključen je iz luka.
    - Rukavac 4/1 i dalje dobiva pretpostavljenih 500 g uz `unit_confidence=low`.
59. **Jaja i veleprodaja.**
    - Granice po uzgoju (`plausible_by`): bio 0,30–1,00 €/kom, ostali 0,15–0,55 €/kom (vlasnik).
    - **Metro** je `clean.stores.store_type = 'cash_and_carry'` i isključen je iz `find_products`, `get_prices` i
      `plan_basket`, osim uz `include_wholesale=True` (CLI `--include-wholesale`).
    - Kod Metroa se „10/1“ i „30/1“ ne tumače kao broj jaja (to su kartoni), a „30 KOM“ da.
60. **Vrećice (kvasac, prašak za pecivo, vanilin šećer).** Mijenja odluku 51.
    - Jedinica usporedbe je proizvod kakav se prodaje. Broj vrećica čita se iz naziva („5+1“, „3 PAK“,
      „6x8g“, „12GX6“, „10kom“, „(5VRE.)“), inače je 1. Gramatura se više ne dijeli veličinom vrećice
      (`sachet_g` služi samo za pretvorbu grama iz recepta).
    - Granice po vrećici (vlasnik): kvasac 0,10–1,50, prašak 0,10–0,60, vanilin šećer 0,10–1,80 €. Vrijede
      i za višestruka pakiranja (cijena / broj vrećica), u oba smjera.
    - Rinfuza od 500 g sada je jedno „pakiranje“ i obično je izvan granica (samo rezerva u košarici).
61. **Peršin:** zadano `dio=list`, a naziv bez oznake dijela je list. Korijen ulazi samo kad recept kaže
    „peršin korijen“. Novo polje `assume_piece`: proizvod bez gramature koji se ne prodaje na vagu dobiva
    procijenjenu masu komada iz `data/units.yaml` (`pieces.persin`: vezica 50 g, procjena), uz
    `unit_confidence=low` i `pack_source=assumed`. Recept „1 vezica“ = 50 g.
62. **Mjere i težine komada (prijedlog, sve procjene).**
    - Nove gustoće u `data/units.yaml`: kakao, med, prašak za pecivo, griz, krušne mrvice, mljevena paprika,
      papar, ocat, Vegeta (`dodatak_jelima`), zobene pahuljice i sjeckani peršin.
    - Nova sekcija `pieces`: luk 150, češanj 5, mrkva 100, krumpir 200, rajčica 120, paprika 150, tikvica 250,
      jabuka 180, limun 120, naranča 200, banana 150 g. Uz njih krastavac, kupus, zelena salata, jaje i vezica peršina.
    - `piece_g` je maknut iz `staples.yaml`; mase komada su samo u `units.yaml`.
    - `units.convert()` prima i komade („kom“, „glavica“, „češanj“, „vezica“).
63. **Filtar hrane: neprehrana u kategoriji hrane** (`food.nonfood_in_food`).
    - Strogi popis (igrač, svijeć, baterij, sjeme, cvijet, salvet, ukrasn) vrijedi za svu hranu: pogođeni idu
      u `ostalo` ili `kucanstvo`, uz `category_source = 'words'`.
    - Širi popis (posuđe, krpe, kozmetika, higijena, ljubimci, cvijeće…) vrijedi samo za ručne iznimke u
      `data/category_map.yaml` (`_chain_verify`: Gavranović „Hrana“, Boso „ZELENI PROGRAM“, Studenac „HRANA“,
      Plodine `ean_inherited`).
    - Zaštita za jestivo (šećerni ukrasi, Dr. Oetker, čokolada, bomboni ili flips s igračkom, naresci).
    - „ČAŠA“ je neprehrana samo kao „ČAŠE“, „+ ČAŠ“ ili „ČAŠA ZA“ (moja dopuna); „KALUP“ samo kao „KALUP ZA“.
    - Promjene su u `docs/data/food_changes_2d10.csv` i STEP2D_REVIEW.md.
64. **Pokrivenost** (samo izvještaj, `scripts/step2d_review.py`, točka 11).
    - Po namirnici broj lanaca s proizvodom u zadanom izboru, i broj proizvoda za Plodine, Konzum, Spar, Lidl,
      Kaufland, Tommy, Studenac i Eurospin.
    - Procjena dobitka od strogo pozitivnog `food_unverified` (naziv počinje riječju namirnice, cijena u
      granicama, poznata gramatura). **Nije primijenjeno.**
65. **Mahunarke bez oblika se ne pogađaju.** Mijenja odluku 37: za grah, leću, slanutak, grašak, kukuruz i
    gljive (`ambiguous_form`) bez `form`, `plan_basket` više ne bira najjeftiniji oblik.
    - Sastojak ide u `ambiguous`: `{"name", "staple", "amount", "unit", "ambiguity": {"form": [...],
      "question": "suho ili konzerva?", "prices": {...}}}`. Oblici su oni dostupni u gradu, redom suho,
      konzerva, smrznuto, svježe.
    - Sastojak se ne računa i nije među `missing`; upozorenje kaže da treba zadati `form`.
    - Rajčica (`form_staples`) i dalje bira najjeftiniji oblik uz upozorenje.
    - Moja dopuna: poznata ocijeđena masa („GRAH CRVENI 400/240 g“) znači `oblik=konzerva` (`form_heuristic`).
      Na arhivi 2026-10-19 to je bilo 52 proizvoda s `nepoznato`.
66. **Dnevno ažuriranje.**
    - Najnovija arhiva i dalje dolazi iz `/v0/list` (najveći datum).
    - Nova tablica `clean.archive_info` pamti učitanu verziju (`updated`, `size`), pa je ponovljeno pokretanje
      prazno, a ponovno objavljena arhiva se učitava.
    - Raspored: dva pokretanja dnevno (15:30 i 23:30).
    - Ispis uključuje razlike po lancu (`compare_stats`).
    - **Arhiva 2026-10-20 (objavljena u 14:26) je nepotpuna:** nema Stanića (31 trgovina), Gavranović ima 24
      trgovine manje (−272 tis. cijena), Metro 6 manje. Ukupno 27 lanaca, 1.452 trgovine, 474.121 proizvod,
      16,94 mil. redaka cijena (−371.547). Provjera je prošla (pad < 20 %), uz upozorenja; zapis je u
      `docs/data/update_2026-10-20.txt`. Baza je sada na 20.10., a 19.10. je u `clean.price_history`.
67. **docs/REVIEW_FOR_CHAT.md** (`scripts/review_for_chat.py`, najviše 150 redaka, provjerava se pri izradi):
    - košarice za palačinke i bolonjez u Osijeku, po stavkama;
    - mjere, gustoće i težine komada iz `units.yaml`;
    - pokrivenost (točka 11);
    - rezultat ažuriranja na 2026-10-20.

    Generirano nad arhivom 2026-10-20. STEP2D_REVIEW.md je generiran nad 19.10., prije ažuriranja; usporedbe
    prije/poslije u njemu odnose se na taj dan.

## Korak 2E (2026-10-20)

Izvještaji: [STEP2E_REVIEW.md](STEP2E_REVIEW.md) (`scripts/step2e_review.py`) i [REVIEW_2E.md](REVIEW_2E.md).

68. **Pripadnost grupe: tri razine** (zamjenjuje odluku 54; `clean.staple_groups.match_quality`).
    - m = udio lanaca čiji naziv prolazi `must_match` bez `must_not_match`; x = udio lanaca čiji naziv pogađa
      `must_not_match`. Neprehrambeni član po kategoriji ne ulazi ni u m ni u x.
    - Snažni član: m > 50 % i x < 10 %.
    - Slabi član (`weak`): x = 0, m ≥ 25 %, jedinica spojiva (`unit_compatible_sql`), barem jedan proizvod
      unutar min/max pakiranja i medijan cijene po jedinici u granicama. U zadanom je izboru, ali ispod snažnih
      (`find_products`: `match_quality`; `plan_basket`: zastavica `weak_match`, dakle rezerva).
    - Inače `ambiguous` (m > 0) ili `excluded` (m = 0).
    - Granice cijena (`set_auto_ranges`) računaju se prije grupa, jer ih slabi član treba.
    - Arhiva 2026-10-20: 15.819 snažnih, 546 slabih, 1.020 dvosmislenih grupa. Promjene naspram 2D su u
      `docs/data/groups_changes_2e1.csv`.
69. **Tvrda neprehrana na razini grupe** (`clean.products.hard_nonfood`, `food.hard_nonfood`). Ako naziv bilo
    kojeg lanca u grupi pogađa sjeme, igračk-, sapun, šampon, motorn-, svijeć-, baterij-, stolic- ili glazben-,
    grupa je `excluded` za namirnicu.
    - „SJEME“ uz kategoriju voća ili povrća i težinu u g je hrana („BUČINO SJEME 150 g II KL“).
    - Sjeme u g bez takve kategorije je nesigurno: nije tvrda neprehrana, a popis riječi ga ostavlja `unknown`.
    - **Odstupanje od zahtjeva:** „GARDEN“ je tvrda neprehrana samo uz sjeme ili u vrtnom programu (Boso „ZELENI
      PROGRAM“: „GARDEN 100 g GRAH ŽUTI BER“ je vrećica sjemena). Doslovno pravilo isključilo bi hranu: Konzumov
      „GARDEN GOOD“ (19 grupa graha, ajvar, suho voće), bio „Garden“ rižu, leću i slanutak, „GARDEN GOURMET“
      i Garden pivo.
70. **Spojivost jedinice** (`staples.unit_compatible_sql`, `drop_reason = 'jedinica'`, i uvjet za slabog člana).
    - Namirnica u komadima (jaja) traži pakiranje u komadima ili broj komada iz naziva („JAJE PRINCESS
      SUPRISE 15g“ ispada, „JAJA M 10 KOM 600 g“ ostaje).
    - Nepoznata jedinica pakiranja i vrećice ne isključuju.
    - **Odstupanje:** kod namirnica u kg ili l g i ml su zamjenjivi. Doslovno „kg traži g, l traži ml“ izbacilo
      bi jogurt u bocama od 1 l, passatu, majonezu, kečap i senf u ml te vrhnje u g.
    - Komad je spojiv samo ako namirnica ima masu komada u `units.yaml` („SALATA PUTERICA 1KOM“; dodana
      endivija, 300 g). Na arhivi 2026-10-20 ispada 80 proizvoda, od toga 64 „jaja“ (čokoladna i igračke).
71. **Kratice i sinonimi.**
    - `data/abbrev.yaml` (regex na tekstu s točkama) daje `clean.products.match_norm`, na kojem se radi
      podudaranje s namirnicama. `name` i `name_norm` ostaju.
    - Proširuju se samo nedvosmislene kratice: „pec.“ sam je i „peč.“ (pečeni), a „sv.“ je i svinjski i
      svježe, pa se ne šire. „ŠIR VALJ/REZ“ je široki, jer bi inače „sir“ isključio tjesteninu.
    - Novi `must_match`:
      - tjestenina: oblici i marke iz zahtjeva; lazanje više nisu u `must_not_match`;
      - jogurt: `jog\b`;
      - pileća prsa: odresci, file od prsa, pileći file, „pileci prsa“; `odresc` više nije isključen;
      - svinjetina: rebra;
      - vrhnje za kuhanje: creme cuisine;
      - tvrdi sir: leerdammer, emmental, maasdam, `edam\b`, cheddar.
    - Novi `must_not_match`:
      - tuna: cous, bowl, sal, salat;
      - moja isključenja za krive pogotke novih uzoraka: tjestenina (mesni rezanci, školjke kao morski
        plodovi, pralines, čarape, nož, „za tj“ = za tijelo, gotove lazanje, ricotta), tvrdi sir (umak, sos,
        dip), mlijeko (set, ker, keram: posuđe).
    - Vraćeno grupa: tjestenina 450, tvrdi sir 206, jogurt 89, mlijeko 35, pileća prsa 27, svinjetina 24;
      `docs/data/groups_changes_2e4.csv`.
72. **„cvijet“ i dječji pjenušac.**
    - „cvijet“ je samo u širem popisu (ručne iznimke po lancu), uz zaštite: čaj, brokula, cvjetača, sol,
      kulen, kamilica, bazga, neven, lipa, ukrasni cvjetići. Na 20.10. 78 proizvoda s „cvijet“ vraćeno je u hranu.
    - Vrećica sjemena ostaje neprehrana i prije zaštite za jestivo („SJEME GARDEN CVJETAČA“).
    - Dječji pjenušac (dječj…, spužva bob, bez alkohola, 0,0) i kategorija „DJEČJI PJENUŠCI“ su `pice`.
      Ta kategorija je u mapi bila `djeca`, a sada je `pice`.
73. **plan_basket: odabir i iznosi.**
    - Među pakiranjima koja pokrivaju količinu bira se najjeftinije u apsolutnom iznosu (`cost_pack`), uz
      jednaku cijenu manje. Prije je bilo najmanje pakiranje.
    - `total_to_buy`: cijela pakiranja svega što nije u `already_have`.
    - `total_used`: razmjerni trošak svih stavki.
    - Uklonjeni su `total`, `total_pack` i `counted`. Pantry se više ne računa posebno, jer `already_have`
      pokriva začine koje korisnik ima.
    - Novi parametar `already_have` (lista namirnica, CLI `--have "sol,papar"`): stavke ostaju, uz `have=true`.
      Nepoznata namirnica daje upozorenje.
    - Trgovine se rangiraju po `total_to_buy`.
74. **Carry-forward po trgovini** (`update.carry_forward`).
    - Prije `build_clean` trgovine koje nedostaju ili imaju više od 10 % manje cijena dobivaju prethodne
      sirove retke (stores, products, prices) za proizvode kojih u novoj arhivi nema.
    - Redak zadržava svoj datum i prenosi se samo dok nije stariji od 3 dana.
    - Provjera (`validate`) gleda arhivu prije prenošenja.
    - `clean.prices` dobiva `price_date` i `stale_days`; `price_history` ne duplicira prenesene retke.
    - Testovi: nedostaje lanac, pad 18 % (2 od 11 cijena), pad 9 % (ne prenosi se), 4. dan (ne prenosi se).
    - Baza je već na nepotpunoj arhivi 20.10., a 19.10. nije u sirovim tablicama, pa se Stanić neće vratiti
      sam od sebe. To bi tražilo ponovno učitavanje 19.10. pa 20.10. (`update.py --date … --force`).
75. **Datum po stavci i trgovini.**
    - `get_prices`: svaki redak ima `date`/`date_hr` (datum cijene) i `stale_days`.
    - `find_products`: grupa nosi najstariju cijenu (`date`) i najveći `stale_days`.
    - `plan_basket`: stavka nosi datum i starost odabranog proizvoda, a trgovina najstariju stavku i najveći
      `stale_days`. CLI uz prenesenu cijenu piše „cijena od dd.mm.yyyy. (n d)“.
76. **Prethodna arhiva = učitana arhiva** (`update._previous`). Uzima se iz `clean.archive_info`, a ne kao
    najveći datum u `archive_stats`. Inače ponovno učitavanje starijeg dana (`--force`) pa novijeg ne bi
    prepoznalo prethodni dan, pa ne bi bilo ni carry-forwarda.
77. **Lijevak za svježe povrće** (samo izvještaj, STEP2E_REVIEW.md, točka 9).
    - Za rajčicu, mrkvu, krastavac, zelenu salatu, luk, papriku i tikvicu po lancu, kroz faze kandidati →
      kategorija → pripadnost → varijante → pakiranje → price_suspect → rasprodaja → konačno.
    - Najveći gubitak je u pripadnosti: većinom prerađeni proizvodi, ali i povrće na komad s globalnim EAN-om
      („KRASTAVAC SALATAR kom“), koje pravilo za svježe povrće odbija.
78. **Eurospin i barkod 9999999999994** (samo izvještaj, točka 10).
    - Eurospin isti „globalni“ EAN koristi za 83 različita proizvoda (biljke, voće, povrće), pa jedan naziv
      („MRKVA 1kg“, „KRUMPIR 4kg“) uvodi cijelu grupu u namirnicu. Mrkve i krumpira je zato 63 i 60 (na 20.10.),
      a stvarnih proizvoda 4 i 7.
    - **Prijedlog (nije primijenjen, utječe i na košaricu):** EAN koji jedan lanac koristi za ≥ 5 različitih
      `name_norm` tretirati kao neglobalan (ključ grupe lanac + `name_norm`). Na arhivi 20.10. to pogađa samo
      9999999999994.
79. **Plodine: skupina iz prefiksa šifre** (`food.learn_prefix_rules`, `clean.prefix_rules`, `category_source = 'prefix'`).
    - Učenje na Plodinama s poznatom skupinom (`ean_inherited`), prefiksi od 2, 3 i 4 znaka, podjela 80/20
      po hashu šifre.
    - Primjenjuju se prefiksi čistoće ≥ 95 % s ≥ 30 primjera učenja, najduži prvi. Na 20.10. to je 37 prefiksa,
      uz točnost na odloženom skupu 99,3 % (769 proizvoda).
    - 1.681 Plodina izlazi iz `unknown` (hrana 1.524, kućanstvo 119, pića 33, alkohol 5), među njima i svježe
      povrće („LUK ZUTI“, „ROTKVA CRNA“). Ono sada ulazi i u `find_products`.
80. **Izvještaji Koraka 2E:** `docs/STEP2E_REVIEW.md` (`scripts/step2e_review.py`, detalji po točkama) i
    `docs/REVIEW_2E.md` (`scripts/review_2e.py`, najviše 150 redaka). Oba su generirana nad arhivom 2026-10-20
    s carry-forwardom.

## Korak 2F (2026-10-20)

Sažetak: [REVIEW_2F.md](REVIEW_2F.md) (`scripts/review_2f.py`).

81. **Lažni EAN-ovi** (`build.flag_dummy_eans`, `clean.products.ean_note`). Postaju `ean_global = false`, pa se
    grupiraju po lancu + `name_norm`:
    - EAN-ovi s popisa `data/dummy_eans.yaml` i EAN od jedne ponavljajuće znamenke (u svim lancima);
    - EAN koji jedan lanac koristi za ≥ 5 različitih `name_norm` (samo u tom lancu).
    
    Provjera je prije nasljeđivanja gramature i skupine preko EAN-a. Na 20.10.: Eurospin 9999999999994 (83
    proizvoda) i jedan Plodinin proizvod s ponavljajućom znamenkom; pravilo „≥ 5 naziva“ ne pogađa ništa drugo.
82. **Obavezni atribut** (`search._required_attrs_sql`, parametar `required` u `_candidates`).
    - Izričito traženi atribut, iz naziva sastojka („špageti“ → oblik=spageti, „glatko brašno“ → tip=glatko),
      iz `attributes` ili iz `form`, proizvod mora imati u svom nazivu (`how` ≠ `default`). Inače ispada, i kad
      ga grupa (isti EAN) ima po nazivu drugog lanca.
    - Zadani atributi (`default_attributes`, `default_preference`) se ne traže od proizvoda.
    - Novi oblici tjestenine: bucatini i linguine (provjeravaju se prije špageta), a špageti uključuju
      spaghetti i spagetini. „TJESTENINA BUCATINI 500 G RISCOSSA“ (isti EAN kao „ŠPAGETI N6“ u trgovini Krk)
      više nije špageti.
83. **Svježe povrće na komad.**
    - `loose_produce` sada propušta i proizvod s globalnim EAN-om koji se prodaje na komad (`pack_unit='kom'`),
      uz dosadašnji uvjet prve ili druge riječi. Fiksno pakiranje u g ispod 500 g i dalje ne prolazi.
    - Riječi prerade (konzerv, kisel, smrzn, pire, umak, sok, ajvar, juha) su dodane u `LOOSE_REJECT_REGEX`.
    - Za krastavac: `salatar` je maknut iz `must_not_match`, a `salata` je sužena na `salata\b`, jer je
      „KRASTAVAC SALATAR“ svježi salatni krastavac (18 proizvoda).
    - Lijevak, konačno (zbroj 8 lanaca): krastavac 30 → 37, luk 43 → 48; rajčica, mrkva, paprika i tikvica
      bez promjene (`docs/data/funnel_*_2f3.json`).
84. **Slabi članovi.**
    - `plan_basket` bira slabog člana samo kad trgovina za taj sastojak nema nijednog snažnog. Stavka nosi
      `match_quality`; zastavica `weak_match` je maknuta jer bi i snažnom izboru kvarila rang trgovine.
    - U `find_products` slabi članovi ostaju, uz oznaku.
    - Isključenja: grašak `poli\b`, `salam`; med `cokolad`, `riki\b`, `medenjak`, `lambertz`, `keks`.
    - `scripts/weak_suspects.py`: slabi članovi kojima nijedan naziv nema riječ namirnice među prve tri riječi
      (na 20.10. 39 od 447). Popis je u REVIEW_2F.md.
85. **Kupnja na vagu.**
    - Ravnopravan izbor za `loose_produce` (voće, povrće) i svježe meso. Novo polje `fresh_meat`: pileća prsa,
      piletina, mljeveno meso, svinjetina, junetina. Tu ulazi i meso na vagu bez „cca“.
    - Za ostalo (sirevi, šunke…) kupnja na vagu je samo roba promjenjive težine i samo kad u trgovini nema
      pakiranog proizvoda (`by_weight_fallback = true` u stavci). Parmezan u pakiranju ima prednost pred
      „CCA 4 KG“.
    - Usput: maslinovo ulje isključuje taralli i focacciu („TARALLI DJEVIČANSKO MASL.ULJE 500g“ bio je izbor
      u košarici).
86. **Provjera jedinice za gramaturu iz stupca `unit`** (`staples.flag_unit_suspects`,
    `product_staples.unit_suspect`, `drop_reason = 'unit_suspect'`).
    - Proizvod s `pack_source = 'unit'` čiji je medijan cijene po jedinici izvan 0,6x–1,6x medijana namirnice
      ispada iz zadanog izbora.
    - **Upozorenje:** na 20.10. to izbacuje 267 Lidlovih proizvoda, među njima i ispravne jeftine („Trajno
      mlijeko 2,8% 1l“ 0,52 €/l, „Viro Kristalni šećer 1kg“). Granica 0,6x pogađa jeftine trgovačke marke, a
      greške jedinice su obično faktor 10 ili više. Prijedlog: 0,3x–3x (`UNIT_SUSPECT_RATIO`). Tablica je u
      REVIEW_2F.md.
87. **docs/REVIEW_2F.md** (`scripts/review_2f.py`, najviše 100 redaka): lažni EAN-ovi, testovi točaka 2 i 3 (pokreću
    se pri izradi), lijevak prije i poslije točke 3, 20 sumnjivih slabih članova, tablica Lidla za točku 6 i
    košarice u Osijeku. Medijan šećera je oko 3,8 €/kg, jer uključuje šećer u prahu, smeđi i mala pakiranja.
    Zato je i ispravni kristal šećer na omjeru 0,2–0,3, što dodatno govori protiv granice 0,6x.
88. **unit_suspect, novo pravilo (Korak 4, 0.1; zamjenjuje odluku 86).** Vrijedi samo za gramaturu iz stupca `unit`.
    - Proizvod se označava kad mu je cijena po jedinici izvan ručnih granica (`plausible_per_unit` ili
      `plausible_by` po stanju/uzgoju), ili kad je izvan 0,4x–2,5x medijana istog globalnog EAN-a u ≥ 2 druga lanca.
    - Označeni se ne izbacuju. `find_products` ih rangira ispod neoznačenih (`unit_suspect` u izlazu). U
      `plan_basket` zastavica `unit_suspect` znači da su samo rezerva.
    - Na 20.10.: 10 proizvoda, svi u Lidlu (prije 267). „Križevačka mljekara Trajno mlijeko 1l“ 0,52 €/l nije
      označen, „Milkland“ 0,39 €/l jest.
    - Isti EAN s drugom gramaturom već ispada kao `drop_reason = 'pakiranje'`. Omjer prema EAN-u zato hvata
      samo istu gramaturu s cijenom drugog pakiranja (Dolcela 6x12 g po cijeni jedne vrećice?).
89. **Slabi članovi, Korak 4 (0.2).**
    - `find_products` ih zadano ne vraća (`include_weak=False`).
    - `plan_basket` uzima slabog člana samo kad trgovina nema snažnog i kad grupa ima `early_name` (riječ
      namirnice među prve tri riječi barem jednog naziva, na `match_norm`; `staple_groups.early_name`).
    - Opća isključenja u `_defaults`: keks, galett, petit beu (i „PETIT BEU.“), golosin, croasan, kora/kore za,
      sisac, airwav, zardinjer, shaker, cjedil, wafer, mais riso, u octu.
    - Po namirnici: tjestenina `krupica durum`; papar `tuna` i `tunj\b` (Konzum piše „TUNJ“).
    - Na 20.10.: 433 slaba, 406 s `early_name`. U uzorku od 40 (REVIEW_4.md) i dalje ima krivih koje test riječi
      propušta: KIBLA kao jogurt, „MED.“ (mediteransko ulje) kao med, AGAPANTHUS kao tjestenina, EAN s
      mrkvom i jabukom kao kukuruz. Nije popravljeno, čeka pregled.
90. **MCP poslužitelj (`src/mealmeter/server.py`, Korak 4.1).**
    - Službeni SDK `mcp` 2.x: `MCPServer`, nekadašnji FastMCP, preimenovan u 2.0; ovisnost `mcp>=2.3,<3`.
    - Alati: find_products, get_prices, plan_basket, list_stores, convert_units, list_staples. Vraćaju sažeti
      JSON (`CallToolResult` s jednim tekstnim blokom, bez dvostrukog `structured_content`), najviše 20 KB:
      dulji popisi se skraćuju uz `truncated`.
    - Svaki izlaz nosi datum cjenika (`date`, `date_hr`); stavke i trgovine nose i `stale_days`.
    - plan_basket dobiva tri parametra:
      - `store` {chain, address_contains}: nacionalne cijene lanca popunjavaju ono što lokalna trgovina
        nema; bez pogotka upozorenje i adrese lanca.
      - `alternatives`: do 2 druga proizvoda u istoj trgovini, preko `choose_product` bez već odabranih.
      - `price_overrides` [{name, cost_pack}]: cijena jednog pakiranja, primjenjuje se samo na trgovinu iz
        `store`, inače na best_store; `user_provided`, zbrojevi se preračunavaju, poredak ne.
    - Server vraća najviše 3 trgovine; alternative nosi samo best_store.
