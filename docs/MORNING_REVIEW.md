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
| branka | CVJETIĆI UKRASNI | HRANA | hrana | chain |
| ktc | BOMBONI 4g +IGRAČKA PONY | HRANA | hrana | chain |
| studenac | IGRAČKA HUGI WUGI BLOW BUBBLE 12/1 | HRANA | hrana | chain |
| boso | CVIJE ORHID.POSUD.CIKL.47 cm | ZELENI PROGRAM | hrana | chain |
| ktc | ROLADA VANILIJA 300g DEKOR DOMA | HRANA | hrana | chain |
| lorenco | MAČJI JEZICI PRALINE OD ML.I BJ.ČOK |  | hrana | ean_inherited |
| gavranovic | TANJURIĆI STAKLO 15X15cm HO-rasprodaja | Hrana | hrana | chain |
| branka | SALVETE DAISY MI BOŽIĆNA ZVIJEZDA 20/1 | HRANA | hrana | chain |
| vrutak | *TEMPRANILLO CASA SOLAR 0.75L COSECHEROS ZOZP SUHO 2025 -6/1- | VINO INOZEMNO | alkohol | chain |
| plodine | CROISSANT COK. 300 G 6/1 CASALINI |  | hrana | ean_inherited |
| ribola | GORDONS PINK 0,7L+COPA ČAŠA | PIĆE | pice | chain |
| gavranovic | VREĆICA UKRASNA 26X32X12 cm-rasprodaja | Hrana | hrana | chain |
| plodine | KAVA 400 G MLJEVENA FOLIJA ANAMARIJA |  | hrana | ean_inherited |
| gavranovic | TETA VIOLETA OMEKŠIVAČ 900ml LAGOON | Hrana | hrana | chain |
| trgovina-krk | JIM BEAM 0,7L + 1 ČAŠE | Piće | alkohol | chain |
| gavranovic | ČESTITKA-rasprodaja | Hrana | hrana | chain |
| boso | WHISK JACK 0,7 l DANIELS+2 ČAŠE | VINO I JAP | alkohol | chain |
| ntl | IGRAČKA FINGER SLUG VELIKI | Ostalo | hrana | ean_inherited |
| konzum | DRAŽEI JAJA RUM KOKOS 175 g CASALI | HRANA | hrana | chain |
| plodine | NOODLES CURRY 65 G FINI MINI CASA |  | hrana | ean_inherited |
