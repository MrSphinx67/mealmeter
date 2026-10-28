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
