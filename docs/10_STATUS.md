# Korak 10: nalazi iz testa bolonjeza (Osijek, 28.10.2026.)

Provjere na stvarnoj bazi (cjenik 20.10.2026.) rade na kopiji baze kojoj se ponovno izgrade samo namirnice
(`build_staples` + `build_staple_prices`, 24 s), kao u Koraku 9. Zlatni izlazi su zapisani s te kopije.

## 1. Neprepoznati sastojci: pancetta, celer, kocka za juhu

### Pancetta

**Zašto nije prepoznata.** Namirnica `slanina` (od 4B) imala je sinonim „panceta”, ali ne „pancetta”.
`resolve_name` traži točan sinonim ili sinonim s vrijednostima atributa, bez sličnih naziva, pa je
„pancetta” bila nepoznata namirnica (`unmatched`). Podudaranje proizvoda nije bilo problem: `pancet` pogađa i
PANCETA i PANCETTA. Nije bilo ni `needs_confirmation`, jer sastojak nije stigao do namirnice. Kao `free_text`
pretraga po nazivu „pancetta” ne nalazi PANCETA, pa je Lidl ostao bez nje („Lidl oko 26 €, nedostaje: pancetta”).

**Promjena:**
- Sinonim „pancetta”.
- `resolve_name`: kad naziv nije prepoznat, riječi s udvojenim slovom zamjenjuju se riječju sinonima koja je ista
  bez udvajanja („pancetta” → panceta, „mozzarela” → mozzarella, „špagetti” → špageti).
- Atribut `vrsta` (`panceta`, `pureca`): „panceta” i „pancetta” traže pancetu, i kad je obična slanina
  jeftinija. „slanina” je bilo koja slanina, ali bez pureće (`default_exclude_variants`, osim na zahtjev).
- `must_not_match`: kikiriki, štangice, pecivo i sl. „s okusom” ili „sa slaninom”. Na istoj bazi je za
  „pancetta” (preko `slanina`) Eurospin birao HRSKAVI KIKIRIKI OKUS SLANINE, Lidl BO Štangicu sa slaninom, a Konzum
  PUREĆU SLANINU.

Stvarna baza, Osijek: svih 10 lanaca s pancetom bira pancetu (Konzum PANCETA DIMLJ KOCKICE 2,59 €, Plodine
PANCETA NAREZAK 1,59 €, Lidl Dalmatinska panceta 1,99 €, Kaufland KFav.Panceta 1,99 €…). U Zagrebu je isto.

### Celer

Nova namirnica `celer` (kg, svježe povrće), atribut `vrsta`:
- `korijen`: korijen, korjen, KOR., glava, gomolj. Provjerava se prvi, pa je „Celer korijen list” korijen.
- `stabljika`: stabljika, štapići, rebraš i **list**. „Celer list” u trgovinama (Lidl, Kaufland, Plodine 500 g,
  Konzum KOM, Spar) je svežanj stabljika s lišćem, 450-500 g. Pravi stabljični celer pod tim imenom je samo kod
  Metroa („200G CELER STABLJIKA”).
- `nepoznato` („Celer”, „CELER 500g”): samo na zahtjev.

Ne ulaze sjeme, sok, salata, ribani i rezani, granule ni začini.

**Vrsta se ne pogađa** (novo polje namirnice `ask_attribute`):
- Recept ima luk i mrkvu (soffritto, bolonjez): `vrsta=stabljika`, uz zapis u `assumptions` („stabljika, jer
  recept ima i luk i mrkva; za drugo zadaj attributes.vrsta”).
- Inače `ask_user` s cijenom stabljike i korijena (najjeftinije u gradu, za traženu količinu), kao kod oblika
  mahunarki. Sastojak nije uračunat dok korisnik ne odgovori. Odgovor ide kao `attributes.vrsta` ili kao naziv
  („celer korijen”).
- Samo jedna vrsta dostupna u gradu: ta, uz zapis u `assumptions`.

**Količine** (`data/units.yaml`):
- Komad u receptu je stabljika od 50 g. Za korijen je komad 400 g: novi ključ `celer.korijen`, a `piece_weight`
  prima atribute.
- Proizvod na komad bez težine („CELER LIST KOM”) je svežanj od 450 g (novo `pack_g`, `assume_piece`). Lidlov
  „Celer list” ima `pack_unit = kom` (1komad), pa sada i takav komad dobiva procjenu mase. Prije je bio bez količine
  i Lidl je ostao bez celera.

Stvarna baza, „celer” uz luk i mrkvu, 1 kom:
- Osijek: stabljiku ima 7 lanaca (Konzum, Plodine, Spar, Roto, Kaufland ≈ 450 g 1,29 €, Lidl ≈ 450 g 1,29 €).
- Zagreb: isto, plus Stridon.
- Eurospin, NTL, Tommy i Gavranović imaju samo korijen ili celer bez oznake, pa im stabljika nedostaje.

„celer” sam daje pitanje: Osijek stabljika 0,12 € (50 g) ili korijen 0,32 € (400 g).

**Poznato ograničenje:** Konzumov „CELER LIST KOM” ima u cjeniku cijenu po kg (3,98 €/kg), pa se kupuje „na vagu”
(0,20 € za 50 g), a ne cijeli svežanj za 1,99 €. Isto vrijedi za ostale takve proizvode Konzuma. Nije mijenjano.

### Kocka za juhu i temeljac

Dvije nove namirnice:
- `kocka_za_juhu` (kg): kocke i temeljac u prahu. Uključuje „JUHA-KOCKA” (Spar): `keep_defaults: [juha]` je novo
  polje koje za ovu namirnicu isključuje zajednički uzorak „juha”.
  - Atribut `okus`: povrtni, kokošji (i pileći), goveđi, mesni, nepoznato.
  - Atribut `vrsta`: kocka, prah, gel.
  - Gel je Podravkin „temeljac za jela” 4 × 28 g za 0,5 l, a treba skoro 3 puta više grama od kocke. Zato je samo na
    zahtjev, kao i vrsta nepoznato.
  - Ne ulaze riblji i temeljac od škampa, začinske mješavine („TEMELJAC SPAR ZA GULAŠ”, Kotanyi) ni tekući.
- `tekuci_temeljac` (l): „TEKUĆI” ili volumen u nazivu, najmanje 250 ml (Kauflandov tekući koncentrat od 140 ml
  ispada). Ne ulazi „TEMELJ ZA ŽELJEZO”.

Kako se biraju:
- Okus: zadano povrtni. Kad ga trgovina nema, redom kokošji, goveđi, mesni, nepoznati (`default_preference`).
  Povrtni je izabran i kad je goveđa kocka jeftinija (Kaufland: Maggi povrtna 1,89 € umjesto Benita goveđe
  0,75 €).
- „kocka za juhu”, „temeljac” i „bujon” su `kocka_za_juhu` s `form_staples` {koncentrat, tekuci}. Oblik iz naziva
  zadaje novo polje `form_words`: „kocka”, „prah” → koncentrat, a „tekući” → tekuci („tekući goveđi temeljac”).
  „temeljac” bez oblika bira najjeftiniji za traženu količinu, uz upozorenje („pretpostavljen 'koncentrat' …;
  ostali: tekuci 0.65 €”). To je praktički uvijek koncentrat.
- Količina: kocka je 10 g. Recept u ml preračunava se preko `densities.kocka_za_juhu = 0.02`, što su grami
  koncentrata po ml temeljca (kocka 10 g za 0,5 l), pa je „500 ml temeljca” 10 g kocke. Žlica praha zato nije
  točna; to piše u `data/units.yaml`.
- Bez količine: 1 kocka (`data/assumptions.yaml`).

Stvarna baza, Osijek, „kocka za juhu”: 9 lanaca (Spar S-Budget 0,68 €, Konzum 0,79 €, dm 0,95 €, NTL kokošja
0,99 €, Eurospin 1,19 €…). U Zagrebu 12 lanaca. „tekući temeljac” u Osijeku daje Eurospin (od mesa, 1,29 €),
Spar, Plodine i Kaufland. „pileća kocka” prije ispravka je u Eurospinu bila KOKOS KOCKE XXL (kokos, ne kokošja),
pa je uzorak sada `kokosj`.

### Ostalo u kodu

- `staples.py`: polja `keep_defaults`, `form_words` i `ask_attribute`. YAML sidro atributa se kopira, jer ga
  dijele `kocka_za_juhu` i `tekuci_temeljac`, a učitavanje je vadilo `_default` iz zajedničkog rječnika.
- `basket.py`: `form_of`, `_ask_attribute`, a pitanje s atributom ide u `ask_user` (`options[].attributes`
  umjesto `form`). Tekst upozorenja za oblik je isti kao prije.

### Testovi i zlatni scenarij

`tests/test_step10.py` (fixture `con10`; ono što ne smije biti izabrano jeftinije je od onoga što mora):
- nazivi i udvojena slova;
- atributi stvarnih naziva;
- 13 stvarnih naziva koji nisu članovi;
- pancetta (i kao `free_text`);
- celer uz luk i mrkvu, sam (pitanje), korijen 400 g, Lidlov svežanj bez težine;
- kocka (povrtna, drugi okus kad nema povrtne, gel na zahtjev), količine, tekući temeljac.

Bez promjene pada 63 od 64 testa.

**Zlatni scenarij** `basket_bolonjez_osijek_10`: bolonjez iz testa (tagliatelle i crno vino kao `free_text`, pancetta,
celer, kocka za juhu, maslac…), cijeli Osijek. Nema `unmatched` ni pitanja.
- Potpuni lanci: Konzum 23,73 €, Plodine 25,44 €, Spar 26,16 €, Roto 26,60 €, Lidl 27,37 € i Kaufland 29,31 €.
  Lidl je prije bio „nedostaje: pancetta”.
- Eurospinu i NTL-u nedostaje celer.
- Svaka pancetta je panceta, celer stabljika, kocka povrtna, vino crno, a maslac kravlji (`test_golden_bolonjez_osijek_10`).

Ostalih 26 zlatnih izlaza je nepromijenjeno.

## 2. Upute za neprepoznate sastojke i česti sastojci koji nisu bili namirnice

### Upute: unmatched nije uračunat, bez procjene

**Problem.** U testu je asistent za neprepoznate sastojke sam dodao „otprilike X €”. Pravilo 3 je zabranjivalo
procjenu cijena općenito, a pravilo 6 je tražilo da se proizvod ne proglasi nepostojećim nakon jedne pretrage.
Nijedno nije reklo što s cijenom sastojka iz `unmatched`.

**Promjena** (`src/mealmeter/server.py`):
- Pravilo 6: sastojak iz `unmatched` nije uračunat. Asistent to kaže i nikad mu ne procjenjuje cijenu (ni
  „otprilike X €”). Odmah pokušava `find_products` ili `free_text` (i drugi naziv) i nudi `candidates`. Ostaje i
  „ne zaključuj da proizvoda nema nakon jedne pretrage”. Engleski: „An unmatched ingredient is not counted: say so,
  never estimate its price; at once try find_products or free_text and offer candidates.”
- Opis `plan_basket`:
  - `unmatched (nije uračunato, bez cijene; s prijedlozima / not counted, no price; with suggestions)`;
  - `ask_user` je i za atribut (celer: stabljika ili korijen);
  - `assumptions` su i pretpostavljene vrijednosti.

Upute imaju 6514 znakova, a ograničenje iz Koraka 9 je 6547 (1,3 × 5036), pa ga nije trebalo dizati.

### Česti sastojci

Provjereni su sastojci iz tipičnih hrvatskih recepata. Svi koje je zadatak naveo već su bili namirnice:
- lovor (`lovorov_list`) i peršin (`persin`);
- vrhnje za kuhanje i kiselo vrhnje;
- krušne mrvice, kvasac i prašak za pecivo;
- šunka, paprika, tikvica i kupus.

Iznimka su **mahune**: bile su samo u `must_not_match` graha.

Popis od još ~60 čestih naziva (`resolve_name`) dao je ove nepoznate: mahune, poriluk, cvjetača/karfiol, brokula,
patlidžan, svinjska mast, orasi, gustin/kukuruzni škrob, cimet, ružmarin, kopar, vlasac, timijan, muškatni
oraščić, kurkuma, kumin, čili, đumbir, kus kus, jabučni ocat, puretina, teletina, hrenovke, losos, oslić, kruh
(namirnica postoji, ali je `disabled`), tortilja, lisnato tijesto, kore za pitu, želatina, bademi, lješnjaci,
grožđice, batat, cikla, rotkvica, limeta, soda bikarbona i „vrhnje” bez vrste.

**Dodano** (deset najčešćih u kuhanju, svaka provjerena na stvarnim nazivima u Osijeku i Zagrebu):

| namirnica | sinonimi | zadano / napomena |
|---|---|---|
| `mahune` | mahune, mahuna, grah mahune, grah mahunar, boranija | svježe ili smrznute; konzerva i staklenka (ml) samo na zahtjev; boja zelena/žuta iz naziva |
| `poriluk` | poriluk, praziluk, prasa | svježe povrće (na vagu); komad 250 g |
| `cvjetaca` | cvjetača, karfiol | i smrznuta; romanesco na zahtjev; glavica bez težine 800 g |
| `brokula` | brokula | i smrznuta; glavica bez težine 500 g |
| `patlidzan` | patlidžan, melancana | svježe povrće; komad 300 g |
| `svinjska_mast` | svinjska mast, mast, domaća mast | bez biljne i kokosove masti, tekućih pripravaka i kanti za mast |
| `orasi` | orasi, orah, jezgra oraha | jezgra ili mljeveni (i „ribani”); bez indijskog, brazilskog, pekana, muškatnog oraščića, lokuma, likera, juneće „orah” |
| `kukuruzni_skrob` | gustin, kukuruzni škrob, škrob, gussnel | gustin „za umake” i „brzi” na zahtjev |
| `cimet` | cimet, mljeveni cimet, cimet u kori, štapić cimeta | zadano mljeveni; kora na zahtjev (štapić 3 g); bez čajeva, šećera s cimetom, deserta |
| `ruzmarin` | ružmarin | začin (do 200 g); bez grisina, kobasica, namaza, svijeća, paste za zube |

`data/units.yaml`: gustoće (cimet 0,5; škrob 0,6; mast 0,9; orasi 0,45 g/ml) i komadi. `data/assumptions.yaml`:
cimet i ružmarin 2 g kad recept ne kaže količinu.

Primjeri, stvarna baza, Osijek:
- mahune 500 g: Kaufland KLC narezane 1 kg 1,64 €, Konzum 1 kg 1,99 €, Lidl 600 g 2,19 €;
- cvjetača 1 kom: Kaufland i Lidl ≈ 800 g 1,39 €;
- orasi 100 g: Eurospin jezgra 1,59 €, Konzum mljeveni 200 g 1,99 € (prije ispravka su četiri lanca, a u Zagrebu šest, birala rahat lokum s orasima);
- svinjska mast 50 g: Spar 500 g 1,55 € (u Zagrebu je prije ispravka Spar birao biljni pripravak „PRIP.TEK.BILJ.MAST”).

**Nije dodano:** začini koje recepti rijetko kupuju posebno (kopar, vlasac, timijan, muškatni oraščić, kurkuma,
kumin, čili, đumbir), meso i riba (puretina, teletina, losos, oslić, hrenovke: traže dijelove i oblike kao `junetina`),
tijesta (lisnato, kore za pitu, tortilja), orašasti plodovi osim oraha, ostalo povrće i voće s popisa, soda
bikarbona i želatina. „vrhnje” bez vrste nije spojeno ni s kiselim vrhnjem ni s vrhnjem za kuhanje, jer je to
pitanje za korisnika. Sve to i dalje radi kao `free_text`.

### Testovi

`tests/test_step10.py`:
- formulacija pravila 6 (hr i en) i opis `plan_basket`;
- nazivi novih namirnica;
- 22 stvarna naziva koji nisu članovi;
- izbor u košarici: mahune bez konzerve, ali konzerva na zahtjev; orasi jezgra, ne lokum ni indijski; svinjska, ne
  biljna mast; cimet mljeveni, a štapić na zahtjev.

Bez promjene pada 42 testa. Zlatnih izlaza je 27 i svi su nepromijenjeni.

## Završno

- `pytest`: 1349 prolazi (+7 preskočenih, zlatni bez stvarne baze), exit 0.
- Uz `MM_GOLDEN=1` i stvarnu bazu s novim namirnicama: 1356 prolazi, exit 0.
- Zlatnih izlaza je 27 (+1: `basket_bolonjez_osijek_10`); postojećih 26 je nepromijenjeno.
- Workflow ih pri sljedećem pokretanju ponovno zapisuje s punom bazom i uspoređuje sa sažetom.
- Ništa nije deployano ručno.
