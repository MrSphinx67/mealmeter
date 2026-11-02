# Korak 13: marka (proizvođač) uz svaki proizvod

## 13.1 Popunjenost stupca marke (stvarne arhive)

Izvor je `products.csv` po lancu, stupac `brand`. U `clean.products` pune baze i u sažetoj bazi (`compact.duckdb`,
također `clean.staple_items`) stupac je **zadržan i jednak sirovom**: 458 498 proizvoda, 348 859 s markom u obje
baze (cjenik 28.10.2026.). 5V2 i 12 ga nisu izbacili. U sažetoj bazi zauzima ~1,8 MiB u `products` i ~0,5 MiB u
`staple_items`.

Popunjenost (udio proizvoda s nepraznim `brand`), 28.10. / 19.10.:

| lanac | proizvoda | popunjeno | što je u stupcu |
|---|---:|---:|---|
| boso | 9 269 | 99,3 % / 99,2 % | mješavina: marke (LEDO, NIVEA) i dobavljači (NTL, EUROCOM, KB D.O.O.) |
| bure | 17 163 | 0 % / 0 % | prazno |
| djelo_vodice | 10 726 | 0 % / 0 % | prazno |
| dm | 22 135 | 100 % / 100 % | marke (Balea, dmBio, NIVEA) |
| dukat | 408 | 88,7 % / 88,7 % | marke; „Autres marques tarif”, „Société” su smeće |
| eurospin | 4 008 | 100 % / 100 % | marke, ali 2 065 (52 %) „NO BRAND” |
| gavranovic | 15 824 | 99,0 % / 99,1 % | uglavnom dobavljači s d.o.o. (NTL d.o.o., Orbico, AWT, Offertissima) |
| jadranka_trgovina | 12 284 | 0 % / 0 % | prazno |
| kaufland | 19 375 | 99,8 % / 99,8 % | marke (K-Classic, Podravka); 343 „#” |
| konzum | 22 138 | 97,4 % / 97,4 % | marke, VELIKA SLOVA (K PLUS, PODRAVKA) |
| ktc | 15 709 | 100 % / 100 % | uglavnom tvrtke s d.o.o./d.d. i gradom („PODRAVKA d.d. KOPRIVNICA”) |
| lidl | 7 012 | 64,9 % / 63,9 % | vlastite marke (Milbona, Deluxe, Pilos); 109 „-” |
| lorenco | 17 444 | 0 % / 0 % | prazno |
| metro | 13 524 | 86,5 % / 86,6 % | marke (METRO CHEF, ARO) |
| ntl | 18 340 | 99,6 % / 99,6 % | uglavnom dobavljači s d.o.o. (Koopman B.V., IRA Commerce, Orbico) |
| plodine | 76 957 | 93,4 % / 93,4 % | marke i „AMIGA NO BRAND”, „ITALIJA - UNOS”, „KINA - UVOZ” |
| ribola | 16 974 | 70,4 % / 70,2 % | marke |
| spar | 23 393 | 73,1 % / 73,1 % | marke (S-BUDGET, SPAR, DESPAR) |
| stanic | 2 599 | 100 % / 100 % | nisu marke nego skupine robe („SM. RIBLJI PROIZVODI NEP.”) |
| stridon | 31 646 | 46,2 % / 46,3 % | marke |
| studenac | 19 924 | 87,4 % / 87,7 % | marke i dobavljači („STUDENAC-ROBNA MARKA”, „ORBICO-P&G”, „DUKAT UKUPNO BEZ GAUDE”) |
| tommy | 19 893 | 99,8 % / 99,8 % | marke, dobavljači s d.o.o. i „SKLADIŠTE …” |
| trgocentar | 10 316 | 38,6 % / 38,8 % | proizvođač s gradom („PODRAVKA, KOPRIVNICA”, „VINDIJA - CEKIN”) |
| trgovina-krk | 33 858 | 96,4 % / 96,4 % | uglavnom dobavljači s d.o.o. (NTL D.O.O., KB D.O.O., TRGOVINA KRK D.D.) |
| vrutak | 14 312 | 99,9 % / 100 % | marke i dobavljači |
| zabac | 3 267 | 0 % / 0 % | prazno |
| branka, roto | — / 14 462, 9 201 | — / 0 %, 100 % | 28.10. nisu u arhivi |

Preko svih lanaca: 60 146 vrijednosti s „d.o.o.”, 7 168 s „d.d.”, 1 930 s B.V./GmbH/S.p.A./SRL/Ltd,
3 729 „… - UNOS/UVOZ”, 452 samo interpunkcija („#”, „-”), 5 512 „NO BRAND”, „OSTALO”, „ROBNA MARKA”, „NEPOZNAT”.

**Zaključak.** Stupac postoji i nije izbačen, ali „marka” je u njemu samo kod dijela lanaca. Pet lanaca ga nema
(bure, djelo_vodice, jadranka_trgovina, lorenco, zabac), a gavranovic, ktc, ntl i trgovina-krk u njega upisuju
dobavljača ili distributera (Orbico za Nutellu, Koopman), pa ga se ne smije prikazati kao marku bez čišćenja.

## 13.2 Polje `brand` u izlazima alata

Novi modul `src/mealmeter/brands.py` (`load_brands` i `BRANDS_PATH` premješteni iz `basket.py`, koji ih i dalje
izvozi). Marka se računa pri odgovoru, iz stupca koji je već u sažetoj bazi, pa se baza ne mijenja.

**Redoslijed** (`display_brand(brand, name, chain)`):
1. stupac `brand` iz cjenika, očišćen (`clean_brand`):
   - vrijednost koja sadrži marku iz `data/brands.yaml` daje tu marku: „PODRAVKA d.d. KOPRIVNICA”, „PODRAVKA-FOOD”
     → Podravka, „VINDIJA D.O.O.” → Vindija, „DR.OETKER” → Dr. Oetker, „PIK VRBOVEC PLUS D.O.O.” → PIK;
   - **null**: prazno, samo interpunkcija („-”, „#”), „N/A”, „NO BRAND”, „OSTALO”, „ROBNA MARKA”, „NEPOZNAT”,
     „… - UNOS/UVOZ”, „SKLADIŠTE …”; pravni oblik tvrtke (d.o.o., d.d., B.V., GmbH, S.p.A., SRL, Ltd, obrt…), jer je
     to dobavljač ili distributer (Orbico za Nutellu, Koopman); poznati distributeri i bez pravnog oblika (Orbico,
     AWT, Atlantic Trade, IRA Commerce, Koopman, Eurocom, Nird, Ultra, VM2…); cijeli stupac Stanića (skupine robe);
     odjel ili vrsta robe („Crveno meso”, „Povrće svježe”); naziv lanca, osim kad je to vlastita marka toga lanca
     (SPAR u Sparu, Plodine u Plodinama, Metro Chef u Metrou; „NTL” u Bosu, „NTL - Voće i povrće”, „Boso voće” su
     null); vrijednost jednaka nazivu proizvoda („Krumpir”);
   - ostalo ostaje kako piše u cjeniku; vrijednost pisana samo velikim slovima dobiva velika početna slova
     („K PLUS” → K Plus, „S-BUDGET” → S-Budget, „METRO CHEF” → Metro Chef, „TRE MULINI” → Tre Mulini);
2. ako stupac nije marka iz `brands.yaml`, a naziv proizvoda njome počinje, vrijedi marka iz naziva
   („EUROCOM” uz „NUTELLA 400 g” → Nutella);
3. stupac prazan ili očišćen u null: marka iz naziva preko `brands.yaml` („BRAŠNO GLATKO T-550 1kg MLINETA” →
   Mlineta), osim kad je ispred nje „s”, „sa”, „i”, „okus”, „punjen…”, „za”, „od” („keksi s Nutellom” → null);
4. inače **null**. Marka se ne pogađa.

`data/brands.yaml`: 30 → 98 marki (Mlineta, Belje, Cekin, Z bregov, Président, Šafram, Perutnina Ptuj, Čakovečki
mlinovi, Giana, Jamnica, Solana Pag, Thomy, Heinz, De Cecco, Rummo, Nestlé…) i vlastite marke lanaca (K Plus,
K-Classic, K-Bio, S-Budget, Despar, Milbona, Pilos, Favorina, Italiamo, Belbake, Chef Select, Solevita, Freshona,
Vitasia, Metro Chef, ARO, dmBio). Isti popis i dalje daje marku iz naziva sastojka u `plan_basket` (Korak 4C:
„mlineta brašno” sada preferira Mlinetu); u zlatnim scenarijima nijedan sastojak ne sadrži novu marku.

**Gdje je polje:**
- `plan_basket`: svaka stavka (`best_store.items[].brand`, uvijek prisutno, null kad nije poznato), svaka
  alternativa (`alternatives[].brand`, uvijek prisutno; alternativa tražene marke iz druge trgovine i dalje nosi
  traženu marku), kandidati slobodne pretrage (`candidates[].brand`) i `unmatched[].candidates[].brand`;
  `detail=true` u svim trgovinama;
- `find_products`: `results[].brand` (prije sirova najčešća vrijednost stupca, npr. „ORBICO D.O.O.”, sada
  očišćena). Grupa s istim EAN-om: najčešća marka proizvoda u grupi. Klasa namirnice (`jaja:m:podni`), koja spaja
  proizvode više proizvođača, ima marku samo kad je svim proizvodima ista;
- `get_prices`: `stores[].brand` po proizvodu u trgovini.

**Pokrivenost** na proizvodima namirnica (`clean.staple_items`, 60 357 proizvoda, cjenik 28.10.): stupac
neprazan 75,4 %, marka u izlazu **70,1 %**, od toga 7,8 % iz naziva.

| lanac | proizvoda | stupac neprazan | marka u izlazu | od toga iz naziva |
|---|---:|---:|---:|---:|
| boso | 967 | 98.9 % | 84.8 % | 0.0 % |
| bure | 1 805 | 0.0 % | 22.7 % | 22.7 % |
| djelo_vodice | 2 196 | 0.0 % | 32.1 % | 32.1 % |
| dm | 240 | 100.0 % | 100.0 % | 0.0 % |
| dukat | 229 | 93.4 % | 93.9 % | 5.7 % |
| eurospin | 906 | 100.0 % | 39.4 % | 0.7 % |
| gavranovic | 1 656 | 99.3 % | 59.4 % | 3.9 % |
| jadranka_trgovina | 1 867 | 0.0 % | 47.7 % | 47.7 % |
| kaufland | 3 363 | 99.6 % | 96.8 % | 0.3 % |
| konzum | 3 719 | 97.8 % | 97.7 % | 0.0 % |
| ktc | 2 490 | 100.0 % | 77.7 % | 1.4 % |
| lidl | 1 321 | 58.1 % | 72.9 % | 15.6 % |
| lorenco | 2 843 | 0.0 % | 27.5 % | 27.5 % |
| metro | 2 974 | 86.8 % | 86.8 % | 0.0 % |
| ntl | 1 982 | 99.5 % | 60.8 % | 5.4 % |
| plodine | 5 606 | 94.3 % | 90.0 % | 0.4 % |
| ribola | 2 934 | 74.7 % | 74.7 % | 4.6 % |
| spar | 4 305 | 62.4 % | 66.2 % | 3.9 % |
| stanic | 632 | 100.0 % | 34.5 % | 34.5 % |
| stridon | 2 573 | 84.1 % | 86.8 % | 3.5 % |
| studenac | 3 060 | 90.0 % | 79.2 % | 2.4 % |
| tommy | 3 685 | 99.7 % | 72.3 % | 0.8 % |
| trgocentar | 2 026 | 45.9 % | 63.0 % | 21.0 % |
| trgovina-krk | 3 428 | 97.4 % | 51.5 % | 3.1 % |
| vrutak | 3 073 | 100.0 % | 83.2 % | 2.4 % |
| zabac | 477 | 0.0 % | 24.9 % | 24.9 % |

U zlatnim izlazima: 146 stavki/alternativa s markom i 27 bez (svježe povrće na vagu, mljeveno meso bez oznake,
Lidlovi proizvodi s „-”), find_products 57/8, get_prices 135/27.

**Veličina odgovora.** Zadani (sažeti) odgovori plan_basket i find_products su 1,4–16,4 kB, ispod granice
`MAX_RESPONSE_BYTES` (20 000), pa se ne skraćuju. Odgovori koji su već bili skraćeni (`truncated: true`) sada stanu
jedan element manje: get_prices s 50 trgovina (`prices_ean_osijek` 32 → 31 trgovina, `prices_class_jaja_m` 33 → 32)
i `detail=true` (`basket_store_konzum_osijek` 2 → 1 trgovina u `stores`, `basket_bolonjez_osijek_10`
`best_store.items` 13 → 12; taj je već prije bio iznad granice, nepostavljeni `detail` daje svih 15 sastojaka u 9,6 kB).
Granicu nisam mijenjao.

**Provjere.** Golden zapisan s pune baze (28.10.) prije i poslije promjene: osim polja `brand` jednak je u 23/27
scenarija, a u preostala 4 razlika je samo gore navedeno skraćivanje. Provjera nad sažetom bazom: **27/27 jednako**.
pytest: 1405 prošlo, 7 preskočeno (izlazni kod 0). Novi `tests/test_step13.py` (49 testova): smeće i dobavljači
su null, vlastite marke lanaca ostaju, marka iz naziva i nikad iz sastojka, grupe i klase, polje u stavkama,
alternativama, detail, find_products i get_prices.

## 13.3 Upute

Pravilo 9 (`server.INSTRUCTIONS`): „Stavke prikaži kao popis: proizvod, marka (brand) kad je poznata, veličina
pakiranja (pack_size), cijena pakiranja (cost_pack), npr. "Brašno glatko T-550, Mlineta, 1 kg"; kad je brand null,
marku izostavi i ne izmišljaj je.” (i engleski dio: „brand when known … brand null: omit it, never guess one”).
Opisi alata `find_products`, `get_prices` i `plan_basket` navode polje `brand` („marka ili null / brand or null”).

Upute su sada 6 702 znaka; granica u `tests/test_step7.py` je 1,3 → **1,35** × upute prije Koraka 7 (5 036, dakle
6 798), jer je pri 1,3 ostalo samo 33 znaka. Test fraza pravila 9 (`test_rule_list_not_table`) prati novu
formulaciju; novi `test_instructions_brand_rule`. pytest: 1406 prošlo, 7 preskočeno (izlazni kod 0). Golden puna →
sažeta 27/27.

## 13.4 Veličina: sažete datoteke i paket

Marka se računa pri odgovoru iz stupca `brand`, koji je u sažetoj bazi već bio (13.1), pa se `build_compact.py` i
sažeta baza ne mijenjaju. Izmjereno lokalno (`vercel build --prod`, Vercel CLI, i
`scripts/vercel_bundle_size.py`, MB = MiB kao u skripti), cjenik 28.10., bez deploya:

| | prije (afc1822) | poslije (13.3) | upozorenje | rezerva do upozorenja |
|---|---:|---:|---:|---:|
| `compact.duckdb` | 44,8 MB (46 936 064 B) | 44,8 MB (46 936 064 B) | 65 | 20,2 |
| `compact_prices.duckdb` | 43,3 MB (45 363 200 B) | 43,3 MB (45 363 200 B) | 65 | 21,7 |
| paket `python.func` | 180,8 MB | 180,8 MB (189 605 497 B) | 190 | 9,2 |

Paket je veći za ~27 KB: novi `brands.py` (9,2 KB) i njegov `.pyc` (14,6 KB), `brands.yaml` +1,7 KB, `search.py`
i `server.py` +1,2 KB. Rezerva ostaje kao nakon Koraka 12 (12.5: ~26 MB do 220 nakon pretpostavljenog rasta), nijedna
vrijednost nije iznad upozorenja (65 MB po datoteci, 190 MB paket), pa nije bilo razloga za zaustavljanje.

## 13.5 Zlatni izlazi s poljem `brand`

`tests/golden/*.json` ponovno zapisani s pune baze (`golden.py --write --db data/mealmeter.duckdb`, cjenik
28.10.2026.; prije su bili s 20.10.). Polje `brand` je u 26/27 datoteka; `basket_grasak_bez_oblika` samo pita za
oblik i nema proizvoda. Provjera: puna baza **27/27**, sažeta **27/27**. Granica odgovora `MAX_RESPONSE_BYTES`
(20 000) ostaje, pa zlatni izlazi bilježe i skraćivanje iz 13.2.

`tests/test_step6.py::test_golden_grah_suho_all_chains` (samo uz `MM_GOLDEN=1`) više ne traži Roto: u arhivi
28.10. ga nema (13.1). Lidl, Eurospin i NTL su i dalje obvezni, a `incomplete` je i dalje prazan. pytest:
1406 prošlo, 7 preskočeno; uz `MM_GOLDEN=1` 1413 prošlo (oba izlazni kod 0).
