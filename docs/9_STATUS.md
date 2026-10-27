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
