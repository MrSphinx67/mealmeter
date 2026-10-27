# Korak 9: izbor proizvoda iz stvarnog testa (bolonjez, Osijek, 27.10.2026.)

Provjere na stvarnoj bazi (cjenik 20.10.2026.) rade na kopiji baze kojoj se ponovno izgrade samo namirnice
(`build_staples` + `build_staple_prices`, 14 s). Zlatni izlazi su zapisani s te kopije. Postojeći izlazi su s
istog datuma, pa razlika u njima pokazuje točno što je promjena utjecala.

## 1. Maslac i mliječne namirnice: zadano kravlje i obično

**Problem.** „maslac” je u Plodinama dao MASLAC KOZJI 125 G. Na istoj bazi drugi lanci su za „maslac” birali
Kfree maslac bez laktoze (Kaufland) i dmBio ghee (dm). Kozji, ovčji, bivolji, bez laktoze i biljni proizvodi bili
su obični članovi namirnica `maslac`, `jogurt`, sireva i vrhnja. Mlijeko i jogurt isključivali su samo „bez
laktoze”, a regex `bez laktoze` nije pogađao kraticu „BEZ LAKT” („MLIJEKO TR 1.5% BEZ LAKT 1L”).

**Promjena** (`src/mealmeter/staples.yaml`):
- Novi atribut `vrsta_mlijeka` s vrijednostima `kozje` (i Capra Domestica, Caprodur), `ovcje` (i paški sir) i
  `bivolje` (bufala). Za jogurt i vrhnja tu je i `biljno` (soja, zob, kokos, badem, Alpro, Hopla). Atribut se ne
  zove `vrsta` kao kod mljevenog mesa jer maslac (slani/neslani), mlijeko (trajno/svježe) i jogurt (grčki/tekući)
  već imaju `vrsta`. Regexi su zajednički (YAML sidra `&vrsta_mlijeka`, `&laktoza`).
- `laktoza=bez` je jedan regex za sve: „bez lakt”, LF, „lactose free”, Kfree, Free Zone, „free from”.
- `default_exclude_variants` (postojeći mehanizam, kao `laktoza=bez` kod mlijeka) za `maslac`, `mlijeko`,
  `jogurt`, `kiselo_vrhnje`, `vrhnje_za_kuhanje`, `slatko_vrhnje`, `svjezi_sir`, `tvrdi_sir` i `mozzarella`:
  kozje, ovčje, bivolje, bez laktoze; biljno kod jogurta i vrhnja; ghee (novo `vrsta=ghee`, i „pročišćeni”) kod
  maslaca. Varijanta se bira samo kad je tražena imenom ili atributom.
- Mlijeko: „kozje” više nije u `must_not_match`, nego je varijanta na zahtjev („kozje mlijeko”).
- Sinonimi: „kravlji maslac”, „ghee”, „pročišćeni maslac”.
- Uz istu provjeru: „SIR TOPLJ LIST GOUDA” (topljeni sir) i „Fruit King Pripravak od svj. sira” (voćni desert)
  više nisu članovi `tvrdi_sir` i `svjezi_sir`.
- Nepromijenjeno: biljni sirevi i maslac bili su i ostaju potpuno isključeni (`biljn`, `vegan` u
  `must_not_match`), a biljni napitci nisu `mlijeko`. Parmezan nema `laktoza`, jer je prirodno bez laktoze.

**Nazivi sastojaka** (`resolve_name`): dvije riječi kao vrijednost („bez laktoze”, „s jajima”, „sa
spinatom”) i veznici bez značenja (`od`, `di`, `iz`, `mlijeka`). Prije su „mlijeko bez laktoze”, „jogurt bez
laktoze” i „kozji maslac” bili nepoznata namirnica. Sada daju:
- „kozji maslac”, „maslac od kozjeg mlijeka” → `vrsta_mlijeka=kozje`;
- „mlijeko bez laktoze” → `laktoza=bez`;
- „sojin jogurt” → `biljno`;
- „mozzarella di bufala” → `bivolje`.

**Stvarna baza, Osijek, „maslac”:** svih 9 lanaca bira kravlji maslac. Plodine biraju MASLAC 250 WEIDEGLUCK
(1,99 €) umjesto kozjeg (1,79 €), a Kaufland Zdenka 250 g umjesto Kfree bez laktoze. dm više nije u popisu,
jer ima samo ghee. „kozji maslac” daje Plodine, Kaufland i Spar; „ghee” daje dm i Kaufland. Jogurt, mozzarella,
tvrdi i svježi sir, vrhnje i mlijeko nigdje ne biraju posebnu vrstu.

**Testovi** (`tests/test_step9.py`, fixture `con9`, gdje je posebna vrsta uvijek jeftinija od obične):
- nazivi sastojaka;
- atributi stvarnih naziva proizvoda;
- izbor u košarici: zadano obično, na zahtjev posebno.

Bez promjene u `staples.yaml` pada 55 testova.

**Zlatni scenarij** `basket_maslac_plodine_osijek` (stvarni slučaj): Plodine ne biraju kozji, ghee ni maslac bez
laktoze (`test_golden_maslac_plodine`, uz `MM_GOLDEN=1`). Ostala 23 zlatna izlaza su nepromijenjena.

## 2. Tjestenina: zadano obična

**Problem.** „tagliatelle” nije bio sinonim namirnice `tjestenina`, pa je asistent sastojak poslao kao
`free_text`. Slobodna pretraga po nazivu nema zadanih isključenja, pa su izabrane bilo kakve tagliatelle, i to ne
nužno najjeftinije: u Plodinama TAGLIATELLE VERDI (1,19 €), iako su obični široki rezanci 1,06 €. Na istoj bazi
Konzum je dao tagliatelle od pira, Eurospin i Kaufland s jajima, NTL svježe. Unutar namirnice su postojale samo
vrste `integralna`, `bez_glutena` i `s_jajima`, a isključene su bile samo prve dvije. `oblik=tagliatelle`
(`\brezanc`) obuhvaćao je i Kritharaki (orzo; to je Lidl izabrao za „tagliatelle”), jušne, sitne i japanske
rezance, pa čak i „STROJ ZA REZANCE”.

**Promjena** (`staples.yaml`, `tjestenina`):
- Sinonimi oblika: tagliatelle, rezanci, široki/uski rezanci, farfalle, leptirići, mašnice, linguine, bucatini,
  fusili, svrdlići, pužići. Naziv sada daje namirnicu i oblik („tagliatelle” → `oblik=tagliatelle`), i kad
  dođe s `free_text: true`, jer se namirnica traži prije slobodne pretrage.
- Novi oblici `jusni` (za juhu, jušni, sitni, fidelini, čipkasti, kritharaki, orzo) i `azijski` (japanski,
  soba, udon, ramen, wok, konjak) stoje prije `tagliatelle`, pa se biraju samo kad su traženi.
- `vrsta` (prva vrijednost koja pogodi):
  - `bez_glutena`: i BG, B.G., heljda, kukuruz, riža;
  - `od_mahunarki`: leća, slanutak, grah, proteinska;
  - `integralna`: i INTE., INT;
  - `od_pira`: pir, spelt, kamut;
  - `sa_spinatom`: špinat, ŠPIN., ZELE., verdi, tipfeler ŠIPNAT;
  - `obojena`: tricolore, cikla, crnilo sipe, crni, tartuf, rajčica, mrkva, chili, gljive, šparoge, chlorella,
    začinjene;
  - `s_jajima`: i S JAJ, s jaji., JAJ., JAJA, s.j., jajčani; „bez jaja” i „b.j.” to nisu;
  - `svjeza`: svježa bez jaja u nazivu.
- `default_exclude_variants`: sve navedene vrste. Zadano je obična suha tjestenina; ostale vrste biraju se samo
  kad su tražene imenom („zelene tagliatelle”, „tagliatelle s jajima”, „integralni špageti”, „pirovi špageti”,
  „bezglutenska tjestenina”, „svježe tagliatelle”, „rezanci za juhu”) ili atributom.
- „stroj” i „kadaif” više nisu tjestenina.
- `resolve_name`: sinonim koji je i vrijednost atributa vrijedi i uz druge riječi („zelene tagliatelle” →
  `oblik=tagliatelle`, `vrsta=sa_spinatom`), i preko `value_words` („rezanci” → `tagliatelle`).

**Stvarna baza, Osijek, „tagliatelle”:** 8 lanaca bira obične tagliatelle ili široke/uske rezance:
- Plodine: TJ.SIR.REZANCI PARADISO 1,06 €;
- Konzum: REZANCI ŠIROKI LAURA 2,15 € (prije pir 1,69 €);
- Eurospin: TAGLIATELLE DURUM 1,29 €.

**Lidl više nema tagliatelle** („nedostaje”), jer ima samo rezance s jajima, sa špinatom i Kritharaki. To je
posljedica pravila „s jajima samo na zahtjev”. „tagliatelle s jajima” daje 7 lanaca, a „zelene tagliatelle” 7.
Špageti i penne: nijedan lanac ne bira posebnu vrstu. Eurospin je za penne prije birao integralne
(„TJE.INTE.PENNE”).

**Testovi** (`tests/test_step9.py`):
- nazivi sastojaka;
- 20 stvarnih naziva posebnih vrsta i oblika;
- obični nazivi bez vrste („BEZ JAJA”, „b.j.”, „INTERSPAR”);
- izbor u košarici (VERDI, s jajima i pir jeftiniji od običnih);
- stvarni ulaz `free_text: true`.

Bez promjene pada 42 testa.

**Zlatni scenarij** `basket_tagliatelle_plodine_osijek` (stvarni ulaz, `free_text: true`): u Plodinama obične
tagliatelle, bez vrste (`test_golden_tagliatelle_plodine`). Ostala 24 zlatna izlaza su nepromijenjena.

## 3. Vino za kuhanje

**Zašto ga nije bilo.** Namirnice „vino” nije bilo, pa je „crno vino” išlo kao `free_text`. Slobodna pretraga
(i košarica) uzima samo `is_food` bez `food_group = 'alkohol'`, a vino je u kategorijama lanaca uglavnom
alkohol (6882 od 7669 naziva s riječi „vino” na 20.10.). Pronađeno je samo ono što je lanac krivo svrstao u hranu.
U Kauflandu je to bilo desertno „Matić Vino crno Muškat Ruža 0,5L” za 14,52 €, a u ostalim lancima „nedostaje”.
`is_food` nije uzrok: alkohol je `is_food = true`, a izbacuje ga filtar skupine.

**Promjena:**
- Novo polje namirnice `alcohol: true` (`staples.py`). Samo za takvu namirnicu alkohol ne dobiva
  `drop_reason` u `product_staples`, a `_food_filter(include_alcohol=...)` ga propušta u košarici
  (`_rows_for`) i u `find_products` za tu namirnicu. Slobodna pretraga i sve ostale namirnice i dalje su bez
  alkohola: „rakija” kao `free_text` i dalje nema rezultata.
- Namirnica `vino` (`staples.yaml`): mirno stolno vino.
  - Članovi su nazivi s „vino” ili s glavnom sortom (plavac, vranac, merlot, cabernet, frankovka, graševina,
    malvazija, chardonnay, sauvignon, rizling, traminac, žilavka…). Sorta je potrebna jer proizvod bez riječi
    „vino” („VERITAS VRANAC 1,0”) inače nema vlastitu boju i ispada kad je boja tražena. Babić i pošip su samo u
    regexu boje: Babić je i pekara (desetci kruhova), a pošip i posip za kolače.
  - `must_not_match`: pjenušci (pjenušavo, pj, brut, extra dry, secco, gazirano, frizzante), slatka, polusuha,
    desertna i likerska (muškat, prošek, izborna i ledena berba, Tokaji, auslese, marsala, porto), aromatizirana
    (vermut, Hugo), kuhano vino i začini, bezalkoholno, rakije i likeri od sorte (rakija loza malvazija,
    komovica, liker teran), grožđe, kvasina, jela i salame s vinom, čaše i pribor.
  - Atribut `boja`: rosé, crno, bijelo, iz boje u nazivu ili iz sorte. Rosé se provjerava prije crnog
    („FRANKOVKA ROSE”), a crno prije bijelog („CABERNET SAUVIGNON” nije sauvignon). Ostalo je `nepoznato`.
    Rosé i nepoznata boja samo na zahtjev (`default_exclude_variants`).
  - Ostalo: `min_pack` 187 ml, `plausible_per_unit` 1-40 €/l.
- Nazivi: „crno vino”, „crveno vino”, „bijelo vino”, „suho bijelo vino”, „crno vino za kuhanje” daju boju; „vino”
  i „vino za kuhanje” su bez boje, pa je to najjeftinije od crnog i bijelog.
- `docs/SCHEMA.md`: iznimka u filtru hrane.

**Stvarna baza, Osijek, „crno vino” (`free_text`, kao u testu):** 8 lanaca (dm ne prodaje vino), nijedan
nedostaje. Najjeftinije mirno crno vino za 200 ml:

| lanac | vino | cijena |
|---|---|---:|
| Kaufland | Uff Vranac 250 ml | 1,79 € |
| Plodine | Kadarita crno 1,5 L | 1,99 € |
| Spar | Il Barone Merlot | 2,29 € |
| Lidl | Vranac | 2,35 € |
| NTL | Kastelan crno 1 L | 2,49 € |
| Roto | Terra Vinea Vranac 1 L | 2,61 € |
| Eurospin | Vranac 1 L | 2,89 € |
| Konzum | Vupik Vranac 1 L | 2,95 € |

„bijelo vino” daje 8 lanaca od 1,33 € (Lidl, Chardonnay/Colombard) do 3,79 €. Na 20.10. među prihvaćenim članovima
nema pjenušaca, slatkih ni rakija (provjera po riječima brut, poluslatko, slatko, rakija, liker, izborna berba…).

**Testovi** (`tests/test_step9.py`, fixture s kategorijama „VINO” i „ZESTOKO”, gdje su desertno, pjenušac, rosé,
vino nepoznate boje i rakija jeftiniji od stolnog):
- nazivi;
- ostali alkohol nije namirnica;
- boja iz naziva i sorte;
- 17 stvarnih naziva koji nisu vino za kuhanje;
- homonimi sorti (Babić, posip);
- izbor u košarici;
- `free_text`;
- rakija ni u slobodnoj pretrazi ni u `find_products` za vino.

Bez promjene pada 42 testa.

**Zlatni scenarij** `basket_crno_vino_osijek` (stvarni ulaz, `free_text: true`, cijeli grad): Konzum, Lidl,
Kaufland, Plodine i Spar imaju crno vino, a nijedan izbor nije muškat, pjenušac ni slatko
(`test_golden_crno_vino_osijek`). Ostala 25 zlatna izlaza su nepromijenjena.

## 4. Upute: što nedostaje uz cijenu, `cheaper = false` nije ušteda

**Problem.** U stvarnom testu asistent je napisao „Lidl oko 26 €” bez napomene da nedostaje pancetta, pa je ta
cijena izgledala usporedivo s potpunim lancima. Pravilo 8 je tražilo „nedostaje” samo za popis na kraju, a ne
uz svaku cijenu takvog lanca. Pravilo 11 je reklo samo kad alternativu smiješ zvati jeftinijom, a nije reklo da
`cheaper = false` nikad nije ušteda. Alternative uključuju i jednu iste cijene i bolje kvalitete (`delta_eur`
0). Veće pakiranje s `cheaper = true` na blagajni je skuplje (`cost_pack`), a jeftinije samo po potrebnoj
količini.

**Promjena** (`src/mealmeter/server.py`):
- Pravilo 7 (poznata trgovina): ako joj nešto nedostaje, uz ukupnu cijenu navedi što.
- Pravilo 8: uz cijenu lanca kojem nešto nedostaje „nedostaje: …” se uvijek navodi, gdje god se cijena
  spomene („Lidl oko 26 €, nedostaje: pancetta”), i takav lanac nije najjeftiniji.
- Pravilo 11: „jeftinija” ili „ušteda” samo uz `cheaper = true`, a `cheaper = false` nikad nije ušteda. Uz
  `size_note` pakiranje je drukčije i na blagajni može biti skuplje.
- Opis parametra `alternatives`: do 2 jeftinije (`cheaper = true`) i iznimno jedna iste cijene i bolje kvalitete
  (`cheaper = false`).
- Ograničenje duljine uputa u `tests/test_step7.py` povećano je s 1,2 na 1,3 puta duljine prije Koraka 7
  (6043 → 6547 znakova; upute sada imaju 6322). Prije promjene bilo je 6027, pa za ova pravila nije bilo mjesta.
  Skraćivanje drugih pravila bilo bi mijenjanje ponašanja koje nije traženo.

Podaci nisu mijenjani: `incomplete` već nosi `total_to_buy` i `note` („nedostaje: …”), a `cheaper` se računa
na istu potrebnu količinu.

**Testovi** (`tests/test_step9.py`):
- formulacije pravila 7, 8 i 11 (hr i en);
- nepotpuni lanac ima cijenu i `note` s onim što nedostaje;
- alternativa 1 kg ima `cheaper = true` i `size_note`, a `cost_pack` je veći od odabranog 500 g: to je slučaj
  „na blagajni skuplje”.

## Završno

- `pytest`: 1230 prolazi (+6 preskočenih, zlatni bez stvarne baze), exit 0.
- Uz `MM_GOLDEN=1` i stvarnu bazu s novim namirnicama: 1236 prolazi, exit 0.
- Zlatnih izlaza je 26 (+3: maslac, tagliatelle, crno vino); postojeća 23 su nepromijenjena.
- Workflow ih pri sljedećem pokretanju ponovno zapisuje s punom bazom i uspoređuje sa sažetom.
- Ništa nije deployano ručno.
