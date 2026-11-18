# Korak 17: točnost košarice nakon nove odluke o cjenicima (NN 101/26, 110/26)

Cjenik 17.11.2026., puna baza ponovno izgrađena iz istih sirovih tablica (`build_clean`, 5,6 min, RSS 4,7 GB).
Načelo (vlasnik): lažni pogodak u košarici je gori od propuštenog proizvoda.

## Dijagnoza (prije izmjena)

- **A, proizvodi bez kategorije:** 197.281 proizvoda s `is_food` NULL (trgocentar 59,7 tis., Plodine 45,8 tis.,
  Konzum 21,8 tis., Spar 14,8 tis., Kaufland 13,8 tis.). Pravila namirnice (osim svježeg voća i povrća, koje je već
  ulazilo) prolazi 5.005, s cijenom u granicama 2.444; najviše Plodine (984), koje kategoriju nikad nisu imale.
  Probno uključivanje svih (13 gradova x 5 jela): mijenja se 62/65 scenarija, najjeftiniji lanac u 24 (najčešće prema
  Plodinama), nijedan lanac s "nedostaje" ne postaje potpun. U košaricama i lažni pogoci: Boso "KUTIJA ZA JAJA PVC" kao
  jaja, Plodine "ŠTAPIĆI ... S KIKIRKI MASLACEM" i Konzum "TROKUT S MASLACEM" kao maslac; u pravilima još motorna ulja
  kao ulje, "SVRDLO SDS" kao tjestenina, stočna i mirisna sol, maziva mast.
- **B, komad s cijenom po kg:** Konzum "CELER LIST KOM" (unit `ko`, quantity `0.50 kg`, cijena 1,99 €, unit_price
  3,98 €/kg) nema gramaturu u nazivu, pa ga je košarica računala na vagu: 50 g x 3,98 €/kg = 0,20 €. Kod namirnica na
  vagu 78 takvih proizvoda; 55 pouzdano po komadu (cijena / unit_price = quantity: Konzum 25, Plodine 18, Metro 5, NTL 4,
  Boso 2, Ribola 1; npr. SALATA ICEBERG KOMAD, RADIČ KOM, KRUMPIR 2.5/1, BANANA KARTON 18 kg kao 1,60 €/kg), meso
  "KOMAD" (Eurospin, Kaufland) stvarno po kg, a nekoliko nesigurnih (cijena = unit_price, bez mase komada).
  Obrnuto: Lidlova "Mrkva rinfuza" (unit `1kg`) bila je pakiranje od 1 kg (0,79 €) umjesto robe na vagu.

## A) Proizvodi bez kategorije

1. **EAN drugih lanaca, jedna strana** (`food.build_food`, `inherit.one_side`): kad se skupine istog globalnog EAN-a
   razilaze (udio <= 50 %), ali su svi glasovi hrana ili svi neprehrana, proizvod preuzima većinsku skupinu
   (`category_source = 'ean_inherited'`). `ean_inherited` 90.106 -> 99.788 (+9.682).
2. **Puni neprehrambeni izrazi** (`food.NONFOOD_PHRASES`, samo za proizvode bez kategorije, kao `NONFOOD_WORDS`):
   motorno ulje, ulje za motor/lance/mjenjače/svjetiljke/drvo/tijelo..., parafinsko i vazelinsko ulje, SAE oznaka
   (`10W-40`), sol za perilicu/posuđe/kupanje/ceste, stočna i mirisna sol, mlijeko za tijelo/lice/sunčanje, hrana za
   pse/mačke/ptice/ribe..., vinski kvasac, kutija za jaja, plastična jaja, svrdlo (jednina), maziva mast, kanta za
   mlijeko, boca za ocat/ulje. Bez samih riječi ("ulje", "sol", "mlijeko", "kvasac", "lopatica", "svrdla", "krema za",
   "sol za" su i hrana: Klara "TJESTENINA SVRDLA", "Začinska sol za piletinu", "JUNEĆA LOPATICA").
   **Provjera nad punom bazom:** 0 pogodaka na stvarnoj hrani; 10 pogodaka s `is_food = true` su neprehrana s krivom
   kategorijom lanca (sol za ceste, sol za perilice, hrana za pse i ribe, plastična uskrsna jaja) i ostaju kakve jesu
   (izraz ne nadjačava kategoriju lanca). `words` 10.318 -> 11.051.
   Ukupno: `is_food` NULL 197.281 -> 186.905, false 275.228 -> 285.290, true 258.947 -> 259.261 (EAN).
3. **Hrana samo za namirnicu, strogo** (`search._food_filter(unverified="staple_strict")`, `basket._rows_for` za sve
   namirnice osim svježeg voća i povrća, koje zadržava dosadašnje pravilo): proizvod bez kategorije ulazi u košaricu za
   tu namirnicu samo ako je jak član grupe (`staple_groups.match_quality = 'strong'`), nije isključen ni odbačen
   (pakiranje), riječ namirnice je prva ili druga riječ naziva (`product_staples.two_words`, `Staple.loose_regex`) i
   cijena po jedinici je u granicama namirnice (bez cijene po jedinici ne ulazi). Inače ga nema ni kao rezervu.
   Slobodni tekst, `find_products` i `get_prices` ga i dalje ne vide. Kandidata (prije provjere cijene po trgovini):
   2.771 proizvoda.
4. **must_not_match:** maslac (`s maslacem`, `sa maslacem`, `kikirki`, `maslacem`), jaja (`kutij`, `pvc`, `plastic`),
   tjestenina (`svrdlo\b`, `sds\b`, `hss\b`).

## B) Komad, svežanj, rinfuza

1. **Pakiranje iz quantity** (`build.quantity_packs`, `pack_source = 'quantity'`): proizvod bez gramature čija
   quantity ima jedinicu mase ili volumena (ili je jedinica cijene kg/l), različitu od 1 kg/l, i kod kojeg je u većini
   cijena cijena / unit_price = quantity (±5 %): cijena je za komad te mase. Broj komada ("JAJA 10/1", quantity
   `10.00`) i boce bez jedinice (`0,7500`) se ne čitaju. 3.916 proizvoda (Metro 1.159, trgocentar 564, Stridon 485,
   Konzum 333, trgovina-krk 299, Plodine 294...). Stavka dobiva napomenu "cijena za komad (≈ 500 g prema lancu,
   procjena)". Konzum "CELER LIST KOM": 1 kom = 1,99 €.
2. **Nesigurna jedinica** (`staples.flag_unit_uncertain`, `product_staples.unit_uncertain`, zastavica
   `unit_uncertain`): svježe voće i povrće s KOM/KOMAD/VEZICA u nazivu, bez gramature, a cijena po kg je lančev
   unit_price jednak cijeni. Uzima se samo kad trgovina nema drugog proizvoda, nije alternativa, a stavka ima napomenu
   "jedinica nesigurna: 0,88 € može biti cijena komada ili kg, provjeri cijenu na polici"; upute (pravilo 12) kažu
   Claudeu da to prenese. Sada 3: roto "LUK MLADI VEZICA KOM", trgocentar "SALATA PUTERICA KOMAD (PT)", Konzum
   "KUPUS KINESKI KOM". Svježe meso ("SVINJSKI VRAT KOMAD", cijena po kg) se ne označava.
3. **Najmanje jedan svežanj na vagu** (`data/units.yaml` `bunches`, procjene; `units.bunch_rule`,
   `basket.choose_product`): celer list 450 g, peršin (list) 50 g, mladi luk 150 g, blitva (svježa, u namirnici
   špinat) 500 g. Kupnja na vagu je najmanje jedan svežanj (cost_pack), utrošak ostaje količina iz recepta (cost_used);
   napomena "na vagu, najmanje jedan svežanj (≈ 450 g, procjena)". Spar "Celer list" 3,49 €/kg: 0,17 € -> 1,57 €.
   **Kopar** nije namirnica (staples.yaml), ide kao free_text i pravilo na njega ne djeluje.
4. **Rinfuza na vagu** (`build.LOOSE_NAME_RX`): pakiranje od točno 1 kg iz stupca unit uz "rinfuza" u nazivu (Lidl, 23
   proizvoda) više nije pakiranje: roba promjenjive težine, cijena po kg. Lidl "Mrkva rinfuza" za 150 g: 0,79 -> 0,12 €.

## Zlatni izlazi

Novi scenarij **`basket_bolonjez_celer_zagreb`** (Zagreb, already_have sol/papar/ulje; juneće mljeveno meso 500 g, luk
1 kom, mrkva 1 kom, celer 1 kom, pasirana rajčica 700 g, špageti 400 g, pancetta 100 g, parmezan 40 g):

| | prije | Korak 17 |
|---|---|---|
| Konzum | **13,55 €** (najjeftiniji; celer 0,20 € na vagu) | 15,34 € (celer 1 kom 1,99 €) |
| Plodine | 13,97 € | **12,43 €** (najjeftinije; uz to špageti Oho 0,66 € bez kategorije) |

Drugi predloženi scenarij (bolonjez + mrkva + celer bez already_have) ne pokriva ništa novo, pa nije dodan.

Zapis s pune baze, provjera na sažetoj: **28/28 jednako**. Od 27 postojećih mijenja se **15** (svi `basket_*`;
`find_*` i `prices_*` su isti). Promjene najjeftinijeg lanca / najbolje trgovine:
- `basket_bolonjez_zagreb` eurospin 11,21 -> **plodine 10,49**; `basket_already_have_zagreb` eurospin 10,62 ->
  **plodine 9,94** (Plodine: špageti Napoli 0,46 €, maslinovo ulje 0,25 l, Grana Padano 80 g, sol Plodine)
- `basket_bolonjez_osijek_10` konzum 22,71 -> **plodine 20,07** (kocka za juhu Plodine 0,75 €, maslac Burro delle Alpi
  10x10 g, pappardelle Prai)
- `basket_grah_suho_osijek` studenac 0,99 -> **plodine i studenac 0,99** (grah pinto Oho)
- `basket_lidl_varivo_zagreb` 14,71 -> 13,41 € (rinfuza na vagu); `basket_store_konzum_osijek` 6,44 -> 6,05 € (Gastro
  šećer i ulje); `basket_maslac_plodine_osijek` 1,99 -> 1,59 €
- ostalo: drugi redovi usporedbe (Konzum i Plodine jeftiniji), cijene oblika graška

Svi proizvodi bez kategorije u zlatnim košaricama su stvarna hrana (Plodinine marke, Gastro pakiranja Konzuma).

## Veličine (cjenik 17.11.)

| | Korak 16 | Korak 17 | upozorenje / granica |
|---|---|---|---|
| compact.duckdb | 53,8 MB | **51,5** | 65 / 95 |
| compact_prices.duckdb | 54,5 MB | **53,8** | 65 / 95 |
| paket (`vercel build --prod`, CLI 65.11.0) | 201,1 MB | **198,1** | 200 / 220 |

Manje jer je ~10 tis. proizvoda sada sigurno neprehrambeno i ispada iz sažete baze. Lokalno: `vercel build` pakira i
`data/*.backup.duckdb` (nisu u `.vercelignore` ni `excludeFiles`; 4 GB, "LAMBDA_SIZE_EXCEEDED"), pa su za mjerenje
privremeno maknute iz `data/`. U CI-ju ih nema.

## Provjera

- `uv run pytest -q`: 1494 passed, 7 skipped (novo: `tests/test_step17.py`, 47 testova)
- `MM_GOLDEN=1 uv run pytest -q`: 1501 passed
- `golden.py --write` (puna) pa `--check` (sažeta, 300 MB): 28/28
- upute: 6776 znakova (granica 6798, test_step7)
- ručni deploy nije rađen; sljedeće zakazano pokretanje workflowa ide s ovim promjenama
