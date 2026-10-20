# Jutarnji pregled: Korak 2C (arhiva 2026-10-19)

Izvještaj generira `scripts/morning_review.py`. Točke 4 i 5 čekaju potvrdu vlasnika.

## 4. Pileća prsa: „Jeli“ (ČEKA POTVRDU)

`plausible_per_unit: [5, 20]` €/kg je primijenjen: izvan granica je 528 od 10613 cijena po kg preostalih (neisključenih) proizvoda.

Sve grupe s „jeli“ ili „je li“ u nazivu. To je Gavrilovićeva linija **Jeli**: delikatesna pileća prsa (narezak od 350 g i štruca od 2,6 kg), a ne svježi file. **Privremeno su isključene** iz `pileca_prsa` (`must_not_match: jeli\b, je li\b`) dok ne potvrdiš. Ako ih treba vratiti, dovoljno je obrisati ta dva uzorka u `staples.yaml`.

| grupa | nazivi | lanci | min €/kg | medijan €/kg | max €/kg | cijena |
|---|---|---|---|---|---|---|
| stridon:jeli pileca prsa 2600 g gavrilovic | JELI PILEĆA PRSA 2600 g GAVRILOVIĆ | stridon | 2,30 | 2,81 | 4,00 | 9 |
| trgovina-krk:jeli pileca prsa 2600 gr | JELI PILEĆA PRSA 2600 gr | trgovina-krk | 4,23 | 4,23 | 4,38 | 11 |
| branka:salama prsa pileca jeli gavrilovic | SALAMA PRSA PILEĆA JELI GAVRILOVIĆ | branka | 9,49 | 9,74 | 9,99 | 2 |
| 3858892724316 | JELI PILEĆA PRSA 2600G,GAVRILOVIĆ; PILEĆA PRSA JELI GAV RILOVIĆ; PILEĆA PRSA JELI GAVRILOVIĆ; PRSA PILEĆA JELI 2600 g; PRSA PILEĆA JELI kg; Pileća prsa Jeli | konzum, ktc, ribola, spar, studenac, trgocentar | 3,84 | 10,29 | 11,69 | 205 |
| tommy:pileca prsa jeli gavrilovic | PILEĆA PRSA JELI GAVRILOVIĆ | tommy | 9,99 | 10,49 | 10,99 | 81 |
| ntl:prsa pileca jeli kg gavrilovic | PRSA PILEĆA JELI kg GAVRILOVIĆ | ntl | 10,49 | 10,49 | 10,49 | 2 |
| gavranovic:gav jeli pileca prsa delikates | GAV.JELI PILEĆA PRSA DELIKATES | gavranovic | 10,49 | 10,49 | 10,49 | 44 |
| 3858892722572 | ŠUNKA JELI PIL. PRSA; ŠUNKA PILEĆA PRSA JELI | djelo_vodice, studenac | 10,69 | 11,04 | 11,39 | 2 |
| 3858892724392 | GAV.JELI PILEĆA PRSA 350g; Gavrilović Jeli Pileća prsa 350 g; JELI PILECA PRSA 350 G GAVRILOVIC; PILEĆA PRSA 350 g JE LI GAVRILOVIĆ; PILEĆA PRSA 350G JELI; PILEĆA PRSA 350g JELI GAVRILOVIĆ; PILEĆA PRSA JELI 350 g; PRSA PILEĆA JELI 350 g; PRSA PILEĆA JELI 350g | djelo_vodice, gavranovic, kaufland, konzum, ktc, plodine, ribola, spar, studenac | 8,11 | 11,11 | 13,40 | 310 |

Napomena: štruca od 2,6 kg ima 2,30–4,38 €/kg, pa vjerojatno nosi cijenu po kg kao cijenu pakiranja (lanac je cijenu po kg upisao kao cijenu proizvoda).

**Upozorenje uz granicu od 5 €/kg:** ispod nje su i stvarna svježa prsa po akcijskoj ili diskontnoj cijeni (Konzum K Plus 4,69 €/kg u 184 trgovine, Eurospin 4,99 €/kg). Ona sada postaju `price_suspect` i u košarici su samo rezerva. Prijedlog: donja granica 2,5 ili 3 €/kg. Najčešće cijene izvan granica:

| lanac | naziv | min €/kg | max €/kg | cijena |
|---|---|---|---|---|
| konzum | PRSA PILEĆA K PLUS BEZ KOŽE | 4,69 | 4,69 | 184 |
| konzum | PILEĆI FILE OD PRSA VAKUUM | 2,99 | 4,99 | 95 |
| tommy | PILEĆI FILE BRAZILSKI SMRZNUTI | 4,25 | 4,99 | 83 |
| eurospin | DOMAĆI PIL. FILE OD PRSA OBIT.RFZ | 4,99 | 4,99 | 43 |
| eurospin | DOMAĆI PIL. FILE OD PRSA OBIT. PAK. | 4,99 | 4,99 | 43 |
| stanic | PILEĆI FILE SMRZNUTI | 2,75 | 2,75 | 29 |
| roto | PILEĆI FILE SVJEŽI sniženje (12) | 2,50 | 2,50 | 9 |
| metro | 2,5KG UKR. PILEĆI FILE SMRZ | 31,50 | 31,50 | 7 |
| metro | CCA5KG MC PILEĆI FILE MAP | 4,99 | 4,99 | 7 |
| studenac | PILECI FILE SMRZ.STANIC | 3,92 | 3,98 | 5 |
| trgovina-krk | PILEĆI FILE ZA GASTRO 1 kg | 1,95 | 4,08 | 4 |
| konzum | PILEĆI FILE SOLJENI 6X2 BRAZIL | 3,28 | 4,11 | 4 |
| branka | PRSA PILEĆA SVJEŽA | 4,79 | 4,99 | 2 |
| studenac | PILEĆI FILE BRAZIL 2KG LEDO | 4,91 | 4,91 | 2 |
| studenac | GASTRO PILEĆI FILE PEČENI | 209,90 | 209,90 | 2 |

## 0. Filtar hrane

Proizvodi bez korisne kategorije lanca (nema je, ili je „Ostalo“) po lancu: koliko ih je naslijedilo skupinu preko globalnog EAN-a (većinska skupina u lancima s kategorijom, > 50 %), koliko ih je razvrstano popisom riječi i koliko ostaje `unknown`.

| lanac | proizvoda | bez kategorije | EAN | udio EAN | riječi | unknown |
|---|---|---|---|---|---|---|
| plodine | 76495 | 76495 | 22769 | 29.8 % | 3835 | 49891 |
| lorenco | 17443 | 17443 | 12444 | 71.3 % | 262 | 4737 |
| trgovina-krk | 33795 | 14462 | 3468 | 24.0 % | 1137 | 9857 |
| ntl | 18315 | 8004 | 2487 | 31.1 % | 392 | 5125 |
| gavranovic | 15144 | 5504 | 2022 | 36.7 % | 170 | 3312 |
| stridon | 31596 | 3023 | 983 | 32.5 % | 202 | 1838 |
| zabac | 3333 | 547 | 363 | 66.4 % | 7 | 177 |
| vrutak | 14246 | 67 | 50 | 74.6 % | 0 | 17 |
| djelo_vodice | 10768 | 58 | 49 | 84.5 % | 0 | 9 |
| dm | 21712 | 38 | 0 | 0.0 % | 0 | 38 |
| roto | 9201 | 26 | 10 | 38.5 % | 0 | 16 |
| stanic | 2601 | 10 | 2 | 20.0 % | 1 | 7 |
| boso | 9257 | 3 | 0 | 0.0 % | 0 | 3 |

Proizvodi izvan zadanog izbora (`find_products`/`get_prices` bez `include_*`), po skupini. Nijedan nije obrisan iz baze.

| skupina | proizvoda | iz kategorije | preko EAN-a | iz riječi |
|---|---|---|---|---|
| kucanstvo | 86825 | 70829 | 14725 | 1271 |
| unknown | 75027 | 0 | 0 | 0 |
| kozmetika | 46158 | 39839 | 4948 | 1371 |
| alkohol | 30147 | 26628 | 2676 | 843 |
| ostalo | 15956 | 12791 | 931 | 2234 |
| higijena | 8233 | 7418 | 776 | 39 |
| djeca | 1977 | 1856 | 93 | 28 |
| kucni_ljubimci | 1541 | 1269 | 52 | 220 |

20 nasumičnih proizvoda s `is_food = true` čiji naziv izgleda neprehrambeno (od 2168 koje pogađa `food.SUSPECT_NONFOOD_REGEX`):

| lanac | naziv | kategorija lanca | skupina | izvor |
|---|---|---|---|---|
| ktc | JACK DANIEL S 0,7L + 1 ČAŠA | PIĆA | alkohol | chain |
| gavranovic | POSUDA S POKLOPCEM 3,6L-rasprodaja | Hrana | hrana | chain |
| plodine | WHISKEY JAMESON 0,7 L + 2 CASE |  | alkohol | ean_inherited |
| boso | SJEME GARDEN PAPR.ŠOROKŠARI | ZELENI PROGRAM | hrana | chain |
| konzum | MEDENJACI DEKORAT SET 480 G LAMBERTZ | HRANA | hrana | chain |
| gavranovic | SYOSS ŠAMPON FULL HAIR 5D 440ml | Hrana | hrana | chain |
| gavranovic | VREĆICA UKRASNA 31X42X12Cm-rasprodaja | Hrana | hrana | chain |
| ribola | ABC 100G SPUŽVA BOB | HRANA | hrana | chain |
| vrutak | N-KRUH PIROV KALUP 500 G | PEKARSRVO | hrana | chain |
| roto | WHISKEY JACK DANIELS HONEY 0,70 + 2 ČAŠE (6)\* | ŽESTOKO | alkohol | chain |
| ntl | IGRAČKA FINGER SLUG VELIKI | Ostalo | hrana | ean_inherited |
| ktc | ČOK BOMONI 80g SA GLAZB. IGRAČKOM | HRANA | hrana | chain |
| gavranovic | H&S ŠAMPON 250ml OCEAN | Hrana | hrana | chain |
| studenac | KING DESIRE ČAŠA 450 ml | HRANA | hrana | chain |
| tommy | DEKOR ŠARENO PISMO 76 g DR.OET | PAKIRANA HRANA I PIĆE | pice | chain |
| studenac | WHISKY BALLANTINES 2 ČAŠE 0,7 l | PIĆE | alkohol | chain |
| vrutak | N-LEDO MACHO ČAŠA BIJELA ČOKOLADA 255G | SMRZNUTO MESO, POVRĆE, RIBA | hrana | chain |
| gavranovic | VREĆE ZA SMEĆE 50x65 TRGOMIX | Hrana | hrana | chain |
| konzum | KRUH KALUP 600g MARYMAT | HRANA | hrana | chain |
| spar | Kruh craft Karla u kalup.400 g | Hrana | hrana | chain |

## 1. Jaja

Uzgoj iz naziva: BIO/EKO → bio (prvi, jer „EKO … SLOBODNI UZGOJ“ je ekološki), KAVEZNI → kavezni, PODNI → podni, SLOBODNI → slobodni, inače `nepoznato`. Grupe su `jaja:<veličina>:<uzgoj>` (`get_prices` prima i `jaja:m` za sve uzgoje), a `plan_basket` vraća `attributes` odabranog proizvoda (velicina, uzgoj).

Nazivi u `jaja:m` s krajnjim cijenama po jajetu (≥ 1,00 ili ≤ 0,16 €; 1,30 € je Metroov karton, a 0,10 € je bila donja granica starog raspona):

| lanac | naziv | komada | cijena € | €/kom | trgovina |
|---|---|---|---|---|---|
| metro | 10/1 PERFA JAJA M | 10,00 | 44,10 | 4,41 | 5 |
| metro | 10/1 ŽITO JAJA M | 10,00 | 44,04 | 4,40 | 5 |
| metro | 10/1 ARO JAJA A KL M | 10,00 | 44,04 | 4,40 | 7 |
| metro | 15/1 MC JAJA PODNI UZGOJ M | 15,00 | 45,36 | 3,02 | 7 |
| metro | 30/1 ARO JAJA A KL M | 30,00 | 39,00 | 1,30 | 7 |
| studenac | SVJEŽA JAJA 10/1, RAZRED M | 10,00 | 1,59 | 0,16 | 1 |
| lidl | Žito Jaja razred M | 18,00 | 2,75 | 0,15 | 116 |
| lidl | PERFA Jaja podni uzgoj razred M | 15,00 | 2,25 | 0,15 | 116 |
| lidl | Kones Bi Jaja, razred M | 10,00 | 1,45 | 0,14 | 116 |
| stridon | SVJEŽA JAJA A KLASE RAZRED M 10/1 PERFA | 10,00 | 0,16 | 0,02 | 1 |
| jadranka_trgovina | JAJA SVJEŽA 30/1 KLASA A, RAZRED M | 30,00 | 0,26 | 0,01 | 1 |

Distribucija cijene po jajetu (provjerena hrana, 491 različitih parova proizvod × cijena): 5. percentil **0,19**, medijan 0,31, 95. percentil **0,47** €. **Primijenjeno: `plausible_per_unit: [0.19, 0.47]`** (prije [0.1, 1.5]). Bio i dio slobodnog uzgoja su iznad 0,47 €; ako ih želiš u zadanom izboru, gornja granica bi trebala biti oko 0,55 €.

| uzgoj | proizvoda | p5 | medijan | p95 | izvan granica |
|---|---|---|---|---|---|
| nepoznato | 320 | 0,19 | 0,31 | 0,42 | 25 |
| podni | 118 | 0,19 | 0,33 | 0,48 | 11 |
| kavezni | 24 | 0,16 | 0,25 | 0,29 | 2 |
| slobodni | 18 | 0,30 | 0,37 | 1,20 | 1 |
| bio | 11 | 0,34 | 0,47 | 0,53 | 5 |

Klase (veličina:uzgoj) i broj različitih proizvoda: `-:bio` 10, `-:kavezni` 3, `-:nepoznato` 40, `-:podni` 13, `-:slobodni` 3, `l:kavezni` 6, `l:nepoznato` 102, `l:podni` 41, `l:slobodni` 5, `m:bio` 1, `m:kavezni` 15, `m:nepoznato` 165, `m:podni` 56, `m:slobodni` 10, `s:nepoznato` 5, `s:podni` 2, `xl:nepoznato` 8, `xl:podni` 6

## 2. Zadane varijante

Zadano isključene varijante (vraćaju se samo kad je atribut izričito zadan) i broj grupa (EAN ili lanac + naziv) s tom vrijednošću:

| namirnica | varijanta | grupa | primjer |
|---|---|---|---|
| brasno | tip=integralno | 34 | 1KG FARINA BRAŠ.PŠ.CRNO T-1100 |
| brasno | gluten=bez | 5 | BRASNO BEZ GLUTENA 1 KG NUTRIFREE |
| brasno | vrsta=kukuruzno | 13 | 1KG PODRAVKA BRAŠNO KUKURUZNO |
| brasno | vrsta=pirovo | 33 | BIO BRAŠNO PIR PUN.ZRNO 1 kg |
| brasno | vrsta=razeno | 11 | 900G FARINA RAŽENO BRAŠ T 1250 |
| brasno | vrsta=heljdino | 10 | BRASNO HELJDA 1 KG FARINA SPECIALE |
| secer | vrsta=smedi | 70 | \*\*UGO. ŠEĆER SMEĐI 200/1 LOGO VRIJEME ZA KAVU\*\* |
| secer | vrsta=u_prahu | 22 | \*NE\*ŠEĆER U PRAHU U PET BOČICI 250g |
| secer | vrsta=kocke | 13 | 1KG RIOBA ŠEĆER KOCKA BIJELI |
| ulje | vrsta=avokado | 0 |  |
| ulje | vrsta=sezam | 5 | 2,5L DIAMOND SEZAMOVO ULJE |
| ulje | vrsta=kokos | 6 | Encian ulje kokosa 1 l |
| ulje | vrsta=grozde | 1 | ULJE KOŠTICA GROŽĐA 1 L FARCHI |
| ulje | vrsta=specijalno | 3 | 500ML MC ORAHOVO ULJE |
| ulje | vrsta=omegol | 2 | 1L ZVIJEZDA ULJE OMEGOL |
| ulje | vrsta=mediteran | 2 | ULJE 1L MEDITERAN ZVIJEZDA |
| ulje | presanje=hladno | 5 | Sunce Vinkovaca Hl. preš. sunc.ulje |
| rajcica | vrsta=cherry | 58 | \*RAJČIC CHERRY RFS |
| rajcica | vrsta=datterino | 1 | RAJČICA CHERRY DATERINO 500g SG |
| rajcica | vrsta=harmony | 4 | 500G RAJČICA TREŠNJAR HARMONY |
| rajcica | vrsta=campari | 2 | RAJČICA CAMPARI 400G SNIŽENJE |

- brašno: `vrsta` bez oznake je `psenicno` (zadano); heljdino više nije u `must_not_match`, nego je varijanta.
- šećer: `vrsta` bez oznake je `bijeli`.
- ulje: Zvijezda Omegol i Mediteran su `vrsta=omegol|mediteran`, hladno prešano je `presanje=hladno`.
- rajčica: cherry (i koktel, cocktail, mini), datterino, harmony i campari su izvan zadanog izbora.

**Riža i „oro“:** nijedan proizvod ne dobiva `parboiled` bez riječi „parboiled“ u nazivu (test `test_riza_oro_alone_not_parboiled`). Grupa 8001860190520 prikazuje se kao „Riso Scotti riža oro dugog zrna“, ali isti EAN u 10 lanaca glasi „RIŽA ORO PARBOILED“, pa je skupni atribut `parboiled` s izvorom `name`. To nisam mijenjao: Scotti Oro jest parboiled riža.

Izvor atributa za 10 grupa riže (`find_products(ingredient="riza")`):

| id | naziv | atributi | izvor (how, naziv) |
|---|---|---|---|
| 8001860100017 | Riso Scotti riža originario okr.zrno 1kg | vrsta=originario | vrsta: name („RIŽA ORIGINARIO 1 kg SCOTTI“) |
| 3838700540291 | RIŽA ZA DOMAĆA JELA ZLATO POLJE PODRAVKA 1 kg (12) | vrsta=originario | vrsta: name („RIŽA ZL.POLJE 1 kg (OKRUGLO ZRNO)“) |
| 3838700540369 | RIŽA ZLATO POLJE BLAZINICA PODRAVKA 800 g (9) |  |  |
| 8001860201011 | Riso Scotti riža arborio dugo zrno 1kg | vrsta=arborio | vrsta: name („RIŽA ARBORIO 1 kg SCOTTI“) |
| 8001860190520 | Riso Scotti riža oro dugog zrna 1kg | vrsta=parboiled | vrsta: name („RIŽA SCOTTI ORO 1 kg PARBOILED“) |
| 3838700540314 | RIŽA BIJELA 800 g VREĆICA ZLATO POLJE | vrsta=dugo_zrno | vrsta: name („Zlato polje riža dugo zrno pvc 800 g“) |
| 3838700540482 | RIŽA ZL POLJE ST ANDREA 500G KUT (18) |  |  |
| 5410673007490 | RIZA PARABOILED DUGO ZRNO VRECICA 500 G BENS ORIGINAL | vrsta=dugo_zrno | vrsta: name („RIŽA DUGO ZRNO 500 g 4 VREĆICE BEN S“) |
| 3838700540406 | RIŽA ZL POLJE ST ANDREA 1KG KUT VAK (12) |  |  |
| 3838700540604 | RIŽA ARBORIO VAKUMIRANA 1000 g PODRA | vrsta=arborio | vrsta: name („RIZA ARBORIO 1 KG VP ZLATO POLJE“) |

## 3. Kakao

Pozitivno podudaranje: naziv počinje s „kakao“ ili sadrži „kakao prah“, „prah kakao“, „kakao u prahu“ (i „kakao u pr.“), „kakao za kolače“. Isključeno: tortela, tortin, muffin, krema, benquick, napitak, choco box, te (moja dopuna) desert, kolač, rolice, šnite, biskvit, krafne, tabla (čokolada), instant i vending napitci, Dolce Gusto, „XXL“ i Lumpi (instant napitak).

Grupa prije: **173**, poslije: **31**.

Top 10:

| id | naziv | pakiranje | lanaca | €/kg |
|---|---|---|---|---|
| 3858881044012 | KAKAO PRAH KANDIT 100G -12/1- SMANJENE MASTI 16-18% | 100 g | 21 | 16,60–30,80 |
| 3850102110292 | KAKAO PRAH 100G (21), KRAŠ (PAL-90) | 100 g | 20 | 17,90–30,90 |
| 5997381346917 | KAKAO DR OETKER ZA KOLAČE 70G-16/1- | 70 g | 14 | 19,00–38,71 |
| 3858881773608 | KAKAO U PRAHU ANAMARIJA 100 g | 100 g | 9 | 9,30–30,50 |
| 3858891566221 | ULTRA KAKAO U PRAHU 100G ,ANAMARIJA | 100 g | 5 | 8,30–23,90 |
| 3850334055149 | KAKAO PRAH SWEET CHEF 250G (12) | 250 g | 2 | 17,32–21,16 |
| 3858890134360 | EKO KAKAO U PR.200 g EKOZONA | 200 g | 2 | 26,25–38,45 |
| 3850102945085 | KAKAO PRAH 100 g KRAŠ (21) | 100 g | 2 | 14,90–24,30 |
| 9100000963976 | KAKAO PRAH S-BUDGET 250 g | 250 g | 1 | 19,92–19,92 |
| 4002309015217 | KAKAO SUCHARD BENSDORP 125 g | 125 g | 1 | 35,92–35,92 |
