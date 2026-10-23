# Korak 7: ponašanje u stvarnim razgovorima

| točka | stanje |
|---|---|
| 0 mljeveno meso (juneće, svinjsko, miješano) | gotovo: nazivi sastojaka, nazivi proizvoda, vrsta; zlatni scenarij |
| 1 pravilo: svaka promjena -> ponovno plan_basket | gotovo |
| 2 kad pitati: samo recept / pitanje o cijeni | gotovo |
| 3 poznata trgovina: točan popis, drugi lanac samo ako je bitno jeftiniji | gotovo, uz novo polje `cheaper_elsewhere` |
| 4 bez trgovine: "Sve možeš kupiti u:" | gotovo; usporedba sad sadrži samo potpune lance, novo polje `price_spread` |
| 5 popis umjesto tablice | gotovo |
| 6 usklađivanje uputa | gotovo: 13 pravila, 6031 znak (+19,8 %) |

Ništa nije deployano.

## 0. Mljeveno meso

**Nazivi sastojaka.** Prije: "mljeveno meso junetina", "mljevena junetina" i "faširano" bili su `nepoznata namirnica`
(zato je Claude morao koristiti free_text i find_products); "juneće mljeveno meso" i "mljeveno juneće" već su radili,
ali "mljeveno juneće meso" nije. Popravak:
- `staples.yaml`, `mljeveno_meso`: sinonimi `mljevena`, `mljeveno mijesano meso`, `faširano`, `faširano meso`,
  `samljeveno meso`, i novo polje `value_words` (riječ u nazivu sastojka -> vrijednost atributa): junetina, juneće,
  govedina, goveđe... -> `vrsta=junece`; svinjetina, svinjski... -> `svinjsko`; mješano, miješana... -> `mijesano`;
  puretina, piletina, teletina.
- `basket.resolve_name`: uz vrijednosti atributa prepoznaje i `value_words`, a riječi iz sinonima iste namirnice
  ("meso" u "mljeveno juneće meso") ne smetaju.
- Vrsta nije navedena: kao i prije zadano miješano (`default_preference: miješano, juneće, svinjsko`, prva dostupna).

**Nazivi proizvoda.** Na stvarnim podacima (20.10.2026.) mnogi proizvodi mljevenog mesa uopće nisu bili namirnica
`mljeveno_meso`, a neki su imali krivu vrstu:
- nisu bili namirnica: Konzum "JUNETINA MLJEVENA", "JUN MLJEVENA 540G (MA)", "MLJEVENO MJEŠANO MESO", "MLJEVENA
  TELETINA"; Roto "JUN MLJEVENA 540G (MA) (8)"; Tommy "MLJEVENA JUN. 450 g", "MLJEVENO MIJEŠ. 450g", "MLJEVENO
  MIJ.MESO GASTRO"; Spar "Svinjetina mljevena", "Svinjska lopatica mljevena", "Juneći but mljeveni"; Kaufland "K-Pur
  mije. mlj. meso"; Studenac "MESO MLJ. MIJ. (SVI+JUN)"; Boso, Bure, Ribola, Djelo... Dodani `must_match` uzorci
  (`jun\w* mljev`, `mljeven\w* (jun|svinj|tele|mij|mjes|pur|pil)`, `mij\w* mlj`, `meso (mij|mjes)\w*( \w+){0,2} mlj`,
  `sv mlj`...). Ne pogađaju začine ("MJEŠ. KURK. MLJ."), keks, želatinu, pite i tjesteninu s mljevenim mesom (test).
- kriva vrsta: Konzum "JUN MLJEV MESO 850g" bio je zadano miješano (uzorak je tražio "jun."), Roto "SV MLJEV MESO
  850G" miješano umjesto svinjsko, Studenac "MLJEVENO JUNEĆE I SVINJSKO MESO" juneće umjesto miješano. Popravljeni
  uzorci vrste (`\bjun\b`, `\bsv\.?\s*mlj`, "X i/+/ Y" je miješano).

**Koji lanci imaju koju vrstu** (`plan_basket` 500 g sa `store`, puna baza od 20.10.2026., nakon popravka):

| lanac | Osijek: juneće | Zagreb: juneće | svinjsko (oba grada) | miješano (oba grada) |
|---|---|---|---|---|
| Konzum | JUN MLJEVENA 540G (MA), 6,59 € (prije: nema) | isto | SV MLJEVENA 540G (MA), 2,22 € (prije: nema) | da |
| Lidl | Mljeveno meso junetina 450 g, 10,78 € | isto | da | da |
| Kaufland | KPur. Juneće mljeveno meso 450 g, 10,78 € | isto | da | da |
| Spar | JUNEĆE MLJEVENO MESO 540 g, 6,59 € | isto | da | da |
| Plodine | JUNECE MLJEVENO MESO E500 G, 5,99 € | na vagu, 5,50 € | da | da |
| Eurospin | juneće obiteljsko pak., na vagu, 5,75 € | isto | da | da |
| Roto | JUN MLJEVENA 540G (MA) (8), 6,30 € (prije: nema) | isto | SV MLJEV MESO 850G | da |
| Tommy | nema trgovine u gradu | GOVEĐE MLJEVENO MESO, na vagu, 2,65 € | Zagreb | Zagreb |
| NTL | nema | nema | nema | da |
| Studenac | nema trgovine u gradu | nema trgovine u gradu | - | - |

Tommyjevo goveđe mljeveno meso je u cjeniku 5,31 €/kg (jedna trgovina, Ulica 144. brigade HV 5), što je neobično
jeftino za junetinu, ali je tako u službenom cjeniku; nije mijenjano.

**Zlatni scenarij** `basket_bolonjez_junece_osijek` (bolonjez iz zlatnih scenarija, "juneće mljeveno meso" 500 g,
Osijek): najjeftiniji Konzum 16,53 € (JUN MLJEVENA 540G), pa Eurospin 17,40, Roto 17,82, Plodine 18,00, Spar 19,40,
Lidl 20,68, Kaufland 21,46 €. Test provjerava da nema `unmatched`, da su Konzum, Lidl, Kaufland, Plodine i Spar u
usporedbi i da je odabrano meso `vrsta=junece`. (NTL je u `more_chains` sa 6 od 7 sastojaka, bez mesa: vidi točku 4.)

**Promjena ostalih zlatnih izlaza.** Od 22 postojeća scenarija promijenila su se samo dva bolonjeza u Zagrebu
(`basket_bolonjez_zagreb`, `basket_already_have_zagreb`): Tommy sad ima mljeveno meso ("MLJEVENO MIJ.MESO GASTRO",
na vagu 3,98 €/kg), pa je najjeftiniji Tommy 10,92 € umjesto Stridona 12,52 €; Kaufland 16,07 -> 15,47 €. Ostalih 20
je nepromijenjeno. Zlatni izlazi ponovno zapisani (23 scenarija).

**Provjera:**
- `tests/test_step7.py`: 14 naziva sastojaka (vrsta ili zadano miješano), nepromijenjeni "junetina", "mljevena
  paprika", "mljeveni papar"; 14 naziva proizvoda s vrstom; 6 naziva koji nisu mljeveno meso.
- Puna baza ponovno izgrađena (`build_clean`, uz memory_limit 2 GB: bez toga je proces ubijen zbog memorije), sažeta
  baza (`scripts/build_compact.py`, 92,3 MB) također.
- pytest: izlazni kod 0 (1031 prolazi, 3 preskočena); uz `MM_GOLDEN=1` (puna baza) izlazni kod 0; sažeta baza:
  `golden.py --check` 23/23 jednako.

## 1. Novo pravilo: ponovni poziv plan_basket

Pravilo 11 u uputama (`server.INSTRUCTIONS`), hr i en: za svako novo jelo, promjenu broja osoba, sastojaka, grada ili
trgovine ponovno pozovi plan_basket; nikad ne procjenjuj cijene niti ih prenosi iz ranijeg odgovora. Staro pravilo 11
(stvarna cijena -> price_overrides) je u istom pravilu, jer je to isti slučaj ponovnog poziva. Mjesto i brojevi
pravila se usklađuju u točki 6.

**Provjera:** `tests/test_step7.py::test_rule_call_again`; pytest izlazni kod 0 (1032 prolazi, 3 preskočena).

## 2. Kad pitati

Staro pravilo 1 ("prije plan_basket u JEDNOJ poruci pitaj...") zamijenjeno je s dva pravila (hr i en):
- **1.** Samo recept, bez pitanja o cijeni ili kupnji: recept i na kraju jedna kratka rečenica s ponudom da izračuna
  koliko košta i gdje to može kupiti u svom gradu; plan_basket tek kad korisnik pristane.
- **2.** Pitanje koliko košta ili gdje kupiti: u JEDNOJ poruci samo ono što još ne zna (grad; što već ima doma;
  "U koju trgovinu ideš (može i adresa ili kvart), ili da usporedim sve u gradu?"; nadjev ili dodatke kad je
  relevantno). Ne pretpostavlja što korisnik ima doma; samo na izričit zahtjev za brz odgovor smije pretpostaviti, uz
  jasno navedene pretpostavke i ponudu ponovnog izračuna.

"Ne pitaj ponovno ono što je već rekao" je sad "samo ono što još ne znaš". Ostala pravila su pomaknuta za jedno mjesto.

**Provjera:** `tests/test_step7.py::test_rule_when_to_ask`; pytest izlazni kod 0 (1033 prolazi, 3 preskočena).

## 3. Odgovor kad je trgovina poznata

Novo pravilo 6 (hr i en): plan_basket sa `store`, odgovor je točan popis za tu trgovinu; ostali lanci se ne nabrajaju,
osim jedne rečenice ako je neki drugi lanac u gradu jeftiniji za više od ~2 € ili 15 %.

**Zašto i promjena alata.** Sa `store` plan_basket vraća samo tu trgovinu (`comparison` ima jedan redak), pa Claude
ne bi mogao znati je li drugi lanac jeftiniji bez drugog poziva, a pravilo 12 zabranjuje procjenu cijena. plan_basket
ionako računa sve trgovine u gradu prije filtriranja, pa sad uz `store` vraća i **`cheaper_elsewhere`**:
najjeftiniji drugi lanac s trgovinom u gradu koji ima sve sastojke (lokalne trgovine, bez lanaca s nepouzdanim
podacima), `{chain, address, n_stores_city, total_to_buy, difference_eur}`, samo kad je razlika veća od 2 € ili od
15 % (`basket.CHEAPER_EUR`, `CHEAPER_SHARE`). Zbroj je isti kao total_to_buy (cijela pakiranja, bez already_have);
uspoređuje se nakon price_overrides. Polje je i u sažetom odgovoru i u opisu alata. Bez `store` ga nema.

Primjer (puna baza, palačinke bez dodataka: brašno, mlijeko, jaja; Osijek): Spar 4,53 € -> `cheaper_elsewhere`
Kaufland 2,99 € (razlika 1,54 €, 34 %); Konzum 3,23 € -> nema (0,24 €, 7 %); Kaufland 2,99 € -> nema.

**Provjera:** `tests/test_step7.py`: pragovi (više od 2 €, više od 15 %, ni jedno ni drugo, točno 2 € i 10 %,
already_have), polje samo uz `store`, pravilo u uputama. Zlatni izlazi nepromijenjeni (23/23: u oba zlatna
scenarija sa `store` nijedan drugi lanac nije jeftiniji iznad praga). pytest izlazni kod 0 (1036 prolazi, 3
preskočena).

## 4. Odgovor kad trgovina nije zadana ili je "svejedno"

Pravilo o preporuci po total_to_buy (staro 5) zamijenjeno je novim pravilom 7 (hr i en): odgovor počinje s "Sve možeš
kupiti u:" i popisom lanaca koji imaju sve sastojke, s cijenom za kupiti, po cijeni (po lancu najviše 2 adrese i broj
trgovina); jedna rečenica o najjeftinijem i razlici do najskupljeg (male razlike: neka ide gdje mu je
najpraktičnije); lanci kojima nešto nedostaje na kraj, s "nedostaje: ..."; ponuda točnog popisa za odabranu trgovinu.

**Promjena alata: u usporedbi samo potpuni lanci.** Do sada su u `comparison` i `more_chains` ulazili lanci s barem
80 % sastojaka, a `more_chains` nije imao oznaku potpunosti ni adrese. Popis "Sve možeš kupiti u:" bi time bio
pogrešan. Primjeri iz zlatnih izlaza (puna baza od 20.10.2026.):
- Slavonski Brod, varivo: Eurospin 11,17 € i Boso 13,83 € bili su u `more_chains`, Eurospin jeftiniji od
  "najjeftinijeg" Lidla (12,61 €), a obama nedostaje jedan od 10 sastojaka;
- Osijek, bolonjez s junećim: NTL 15,07 € u `more_chains`, bez mesa (točka 0);
- Zagreb, bolonjez: Vrutak 15,79 € u `more_chains` sa 6 od 7 sastojaka.

Sada (`basket.compare_chains`): `comparison` je najviše 6 potpunih lanaca po total_to_buy, `more_chains` ostali
potpuni lanci, i oni s `addresses` (najviše 2) i `n_stores_city`; lanci kojima išta nedostaje su u `incomplete` (sa
`total_to_buy` za ono što imaju), od najviše sastojaka. `COMPARE_MIN_SHARE` (80 %) je uklonjen. best_store se ne
mijenja (rangiranje je i prije bilo po broju sastojaka, pa po cijeni).

**Novo polje `price_spread`** (samo bez `store`, uz barem 2 potpuna lanca), da Claude ne mora sam računati razliku:
`cheapest` (popis lanaca, i kad ih je više iste cijene), `cheapest_total`, `most_expensive`, `most_expensive_total`,
`difference_eur`, `difference_pct` (u odnosu na najjeftiniji) i `small`. **Tumačenje praga:** `small` je true kad je
razlika manja od 1,5 € **ili** manja od 15 % najjeftinijeg (dovoljan je jedan uvjet, doslovno prema tekstu točke 4;
`SMALL_SPREAD_EUR`, `SMALL_SPREAD_SHARE`). Npr. krumpir u Rijeci 0,89 / 1,48 € (0,59 €, 66 %) je malo; palačinke s
Nutellom u Osijeku 7,98 / 9,52 € (1,54 €, 19 %) nije. Ako treba "oba uvjeta", to je jedna promjena u
`basket.price_spread`.

**Zlatni izlazi:** promijenjeno 10 košarica, samo `comparison`/`more_chains`/`incomplete` (gore) i novo
`price_spread`; best_store, stavke i iznosi su isti. Ponovno zapisani.

**Provjera:** `tests/test_step7.py`: compare_chains (nepotpuni lanac ide u incomplete), price_spread (izjednačeni
najjeftiniji, oba praga, jedan lanac), polje samo bez `store`, pravilo u uputama i nema stare preporuke;
`test_step5b` (more_chains s adresama) i `test_server` (popis riječi) prilagođeni. pytest izlazni kod 0 (1040
prolazi, 3 preskočena); `MM_GOLDEN=1` izlazni kod 0; sažeta baza `golden.py --check` 23/23 jednako.

## 5. Popis umjesto tablice

Staro pravilo 7 ("Tablica stavki ima stupce: proizvod, veličina pakiranja, cijena pakiranja, utrošak") zamijenjeno je
(hr i en): stavke kao popis (proizvod, veličina pakiranja, cijena pakiranja), tablica samo ako je korisnik traži;
usporedba lanaca također kao popis, jedan lanac po retku. Utrošak (cost_used) više nije stupac stavke, jer ga točka 5
ne navodi; ostaje u odgovoru alata.

**Provjera:** `tests/test_step7.py::test_rule_list_not_table` (novo pravilo, nema "Tablica stavki ima stupce" ni
"Item table columns"); pytest izlazni kod 0 (1041 prolazi, 3 preskočena).

## 6. Usklađivanje uputa

Upute sad imaju 13 pravila, redom: (1) samo recept, (2) pitanja prije izračuna, (3) ponovni poziv za svaku promjenu,
(4) potvrđeni sastojci i free_text, (5) količine i oblik, (6) ne izmišljaj, (7) poznata trgovina, (8) bez trgovine,
(9) popis umjesto tablice, (10) prirodan jezik i datum, (11) "jeftinija" alternativa, (12) nesiguran izbor,
(13) napomena o cjeniku.

Uklonjeno ili spojeno:
- staro pravilo 1 (pitanja) -> pravila 1 i 2 (točka 2); "ne pitaj ponovno" je "samo ono što još ne znaš";
- staro 5 (preporuka po total_to_buy) -> pravilo 8; "total_used i from_stock_value su informativni" premješteno u
  pravilo 10;
- staro 6: "Odgovor počni sa summary_hr" uklonjeno, jer proturječi početku "Sve možeš kupiti u:" (pravilo 8) i
  popisu za trgovinu (pravilo 7); summary_hr ostaje u odgovoru alata;
- staro 7 (tablica) -> pravilo 9;
- staro 8 (usporedba svih većih lanaca, nepotpuni, more_chains, 2 adrese, zasebni redci) uklonjeno: 2 SVOJE adrese,
  broj trgovina i "lance iste cijene ne spajaj" su u pravilu 8, jedan lanac po retku u pravilu 9, nepotpuni lanci
  na kraju u pravilu 8. Popis većih lanaca (Konzum ... Eurospin) nije potreban u uputama: plan_basket ih sam stavlja
  u incomplete kad u gradu nemaju sastojke (`basket.MAJOR_CHAINS`);
- staro 2 "Nikad ne zbrajaj cijene sam" premješteno u pravilo 3 (uz ponovni poziv i price_overrides), staro 11
  (price_overrides) također;
- engleski dijelovi pravila 5, 6 i 10 skraćeni.

Opis alata plan_basket usklađen: "samo recept: ne zovi dok korisnik ne pristane", "svaka promjena: novi poziv",
summary_hr više nije "počni njime", best_store je opisan (najviše sastojaka, pa najmanji total_to_buy) umjesto
"preporuka je", comparison/more_chains/incomplete/price_spread/cheaper_elsewhere prema točkama 3 i 4.

**Duljina:** 6031 znak prema 5036 prije Koraka 7 (+19,8 %, granica ~20 %).

**Provjera:** testovi uputa u `tests/test_step7.py` uspoređuju tekst bez prijeloma redaka; `test_server` popis riječi
prilagođen (uklonjeno: summary_hr, "Studenac, Eurospin", "Svaki lanac ide u svoj redak sa SVOJIM adresama";
dodano: "najviše 2 SVOJE adrese", "lance iste cijene ne spajaj", "jedan lanac po retku"). pytest izlazni kod 0 (1041
prolazi, 3 preskočena).
