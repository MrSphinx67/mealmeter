# Jutarnji pregled: Korak 2C (arhiva 2026-10-19)

Izvještaj generira `scripts/morning_review.py`. Točke 4 i 5 čekaju potvrdu vlasnika.

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
| ribola | DUKAT ČOK.MLI 0,2l ČAŠA | HRANA | hrana | chain |
| gavranovic | KRPA KUH.40X60cm 100%PAMUK HT-8902 | Hrana | hrana | chain |
| boso | POSUD DALAS ARANŽ. MALA | ZELENI PROGRAM | hrana | chain |
| studenac | IGRAČKA HUGI WUGI BLOW BUBBLE 12/1 | HRANA | hrana | chain |
| gavranovic | VREĆICA UKRASNA 26x32x12cm TOČKICE ROZA/BIJELA -rasprodaja | Hrana | hrana | chain |
| plodine | SVIJECE ZA TORTU UKRASNE 12/1 52506 |  | hrana | ean_inherited |
| branka | DEKOR ROZA KRISTALIĆI 10g | HRANA | hrana | chain |
| djelo_vodice | SENF ČAŠA 250ML | SENF ČAŠICA | hrana | chain |
| gavranovic | NOŽ 3/1 23360/335-rasprodaja | Hrana | hrana | chain |
| spar | Kruh craft Karla u kalup.400 g | Hrana | hrana | chain |
| ribola | PLAZMA ČAŠA 450ml LEDO | HRANA | hrana | chain |
| vrutak | \*TEMPRANILLO CASA SOLAR 0.75L COSECHEROS ZOZP SUHO 2025 -6/1- | VINO INOZEMNO | alkohol | chain |
| ktc | NUTELLA 200g ČAŠA | HRANA | hrana | chain |
| ktc | MUFFINS CLASIC 250g U POSUDI | HRANA | hrana | chain |
| konzum | ČAJ CVIJET BAZGE EKO 40g DARVITALIS | HRANA | hrana | chain |
| plodine | UKRAS DRAZESNA SRCA 7 G DR OETKER |  | hrana | ean_inherited |
| trgovina-krk | JIM BEAM 0,7L + 1 ČAŠE | Piće | alkohol | chain |
| plodine | PALOMA SALVETE STYLE 33X33/20 RUZA |  | hrana | ean_inherited |
| gavranovic | TANJURIĆI STAKLO 15X15cm HO-rasprodaja | Hrana | hrana | chain |
| boso | SJEME GARDEN MJEŠ.CVIJEĆA LUN.ST | ZELENI PROGRAM | hrana | chain |

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
| 8001860100017 | Riso Scotti riža originario okr.zrno 1kg | vrsta=originario | vrsta: name („RIŽA SCOTTI NIKAS ORIGINARIO 1 kg“) |
| 3838700540291 | RIŽA ZA DOMAĆA JELA ZLATO POLJE PODRAVKA 1 kg (12) | vrsta=originario | vrsta: name („RIŽA ZL.POLJE 1 kg (OKRUGLO ZRNO)“) |
| 3838700540369 | RIŽA ZLATO POLJE BLAZINICA PODRAVKA 800 g (9) |  |  |
| 8001860201011 | Riso Scotti riža arborio dugo zrno 1kg | vrsta=arborio | vrsta: name („RIŽA ARBORIO 1 kg RISO SCOT“) |
| 8001860190520 | Riso Scotti riža oro dugog zrna 1kg | vrsta=parboiled | vrsta: name („RIŽA ORO PARBOILED 1 kg SCO“) |
| 3838700540314 | RIŽA BIJELA 800 g VREĆICA ZLATO POLJE | vrsta=dugo_zrno | vrsta: name („Zlato polje riža dugo zrno pvc 800 g“) |
| 3838700540482 | RIŽA ZL POLJE ST ANDREA 500G KUT (18) |  |  |
| 5410673007490 | RIZA PARABOILED DUGO ZRNO VRECICA 500 G BENS ORIGINAL | vrsta=dugo_zrno | vrsta: name („RIŽA BENS DUGO ZRNO 500 g“) |
| 3838700540406 | RIŽA ZL POLJE ST ANDREA 1KG KUT VAK (12) |  |  |
| 3838700540604 | RIŽA ARBORIO VAKUMIRANA 1000 g PODRA | vrsta=arborio | vrsta: name („RIŽA ZLATO POLJE ARBORIO VP 1 kg“) |

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
