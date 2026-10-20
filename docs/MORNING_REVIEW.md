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
| gavranovic | SLADOLED KING DESIRE 450ml ČAŠA LEDO | Hrana | hrana | chain |
| ribola | DUKAT ČOK.MLI 0,2l ČAŠA | HRANA | hrana | chain |
| ktc | BOMBONI 4g +IGRAČKA PONY | HRANA | hrana | chain |
| studenac | IGRAČKA HUGI WUGI BLOW BUBBLE 12/1 | HRANA | hrana | chain |
| plodine | SVIJECE ZA TORTU UKRASNE 12/1 52506 |  | hrana | ean_inherited |
| ktc | ROLADA VANILIJA 300g DEKOR DOMA | HRANA | hrana | chain |
| gavranovic | SVIJEĆA ROĐENDANSKA 10kom-rasprodaja | Hrana | hrana | chain |
| lorenco | MAČJI JEZICI PRALINE OD ML.I BJ.ČOK |  | hrana | ean_inherited |
| spar | Kruh craft Karla u kalup.400 g | Hrana | hrana | chain |
| ribola | PLAZMA ČAŠA 450ml LEDO | HRANA | hrana | chain |
| vrutak | *TEMPRANILLO CASA SOLAR 0.75L COSECHEROS ZOZP SUHO 2025 -6/1- | VINO INOZEMNO | alkohol | chain |
| boso | SJEME GARDEN KRAST.DUGI ZELENI | ZELENI PROGRAM | hrana | chain |
| branka | ČAJ LIPA CVIJET 50g | HRANA | hrana | chain |
| jadranka_trgovina | LIKER PELINKOVAC 0,7L VERSUS + 2 ČAŠE PROMO | PIĆE | alkohol | chain |
| boso | SJEME GARDEN PRKOS FIORI DOPPI | ZELENI PROGRAM | hrana | chain |
| gavranovic | VREĆICA UKRASNA ZA BOCU 12x36x9cm BIJELA/SIVA - rasprodaja | Hrana | hrana | chain |
| gavranovic | BATERIJE PHILIPS 6F22 9V 1/1-rasprodaja | Hrana | hrana | chain |
| trgovina-krk | JIM BEAM 0,7L + 1 ČAŠE | Piće | alkohol | chain |
| gavranovic | SCABIOSA CVIJET - rasprodaja | Hrana | hrana | chain |
| plodine | PALOMA SALVETE STYLE 33X33/20 RUZA |  | hrana | ean_inherited |

## 1. Jaja

Uzgoj iz naziva: BIO/EKO → bio (prvi, jer „EKO … SLOBODNI UZGOJ“ je ekološki), KAVEZNI → kavezni, PODNI → podni, SLOBODNI → slobodni, inače `nepoznato`. Grupe su `jaja:<veličina>:<uzgoj>` (`get_prices` prima i `jaja:m` za sve uzgoje), a `plan_basket` vraća `attributes` odabranog proizvoda (velicina, uzgoj).

Nazivi u `jaja:m` s krajnjim cijenama po jajetu (≥ 1,00 ili ≤ 0,16 €; 1,30 € je Metroov karton, a 0,10 € je bila donja granica starog raspona):

| lanac | naziv | komada | cijena € | €/kom | trgovina |
|---|---|---|---|---|---|
| metro | 10/1 PERFA JAJA M | 10,00 | 44,10 | 4,41 | 5 |
| metro | 10/1 ARO JAJA A KL M | 10,00 | 44,04 | 4,40 | 7 |
| metro | 10/1 ŽITO JAJA M | 10,00 | 44,04 | 4,40 | 5 |
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
