# Pregled Koraka 2E (arhiva 2026-10-20)

Generira `scripts/step2e_review.py` nad izgrađenom bazom; sažetak je u REVIEW_2E.md.

## 1. Pripadnost grupe: tri razine

m = udio lanaca čiji naziv prolazi `must_match` bez `must_not_match`, x = udio lanaca čiji naziv pogađa `must_not_match`. **Snažni** član: m > 50 % i x < 10 %. **Slabi** (`match_quality = 'weak'`): x = 0, m ≥ 25 %, jedinica spojiva, barem jedan proizvod unutar min/max pakiranja i medijan cijene po jedinici u granicama; u zadanom je izboru, ali ispod snažnih i označen (`find_products.match_quality`, u košarici zastavica `weak_match`). Inače `ambiguous` (m > 0) ili `excluded` (m = 0).

Prema pravilu iz 2D: 33 grupa prelazi iz člana u `ambiguous`, 0 u `excluded`, a 550 postaje član.

| namirnica | snažnih | slabih | dvosmislenih | isključenih |
|---|---|---|---|---|
| banana | 60 | 0 | 3 | 47 |
| brasno | 426 | 2 | 14 | 102 |
| cesnjak | 57 | 0 | 3 | 19 |
| cokolada_za_kuhanje | 35 | 21 | 1 | 0 |
| dodatak_jelima | 94 | 15 | 67 | 46 |
| endivija | 24 | 0 | 0 | 5 |
| gljive | 109 | 0 | 3 | 8 |
| grah | 399 | 2 | 19 | 177 |
| grasak | 152 | 2 | 8 | 100 |
| griz | 31 | 5 | 6 | 34 |
| jabuka | 385 | 4 | 0 | 46 |
| jaja | 354 | 0 | 26 | 1088 |
| jogurt | 477 | 43 | 119 | 327 |
| junetina | 283 | 4 | 2 | 38 |
| kakao | 46 | 0 | 6 | 67 |
| kecap | 170 | 5 | 8 | 34 |
| kiseli_kupus | 126 | 4 | 6 | 5 |
| kiselo_vrhnje | 131 | 3 | 5 | 16 |
| koncentrat_rajcice | 41 | 4 | 0 | 0 |
| krastavac | 66 | 5 | 13 | 73 |
| krumpir | 234 | 2 | 1 | 207 |
| krusne_mrvice | 126 | 0 | 2 | 18 |
| kukuruz | 165 | 4 | 10 | 132 |
| kupus | 116 | 0 | 0 | 23 |
| kvasac | 60 | 0 | 0 | 1 |
| leca | 132 | 0 | 1 | 148 |
| limun | 96 | 0 | 2 | 33 |
| luk | 204 | 0 | 7 | 29 |
| majoneza | 178 | 7 | 14 | 8 |
| margarin | 96 | 7 | 1 | 1 |
| maslac | 245 | 8 | 26 | 354 |
| maslinovo_ulje | 351 | 11 | 20 | 75 |
| matovilac | 21 | 0 | 0 | 6 |
| med | 404 | 27 | 55 | 364 |
| mlijeko | 304 | 5 | 100 | 899 |
| mljevena_paprika | 98 | 13 | 10 | 10 |
| mljeveno_meso | 102 | 3 | 4 | 0 |
| mozzarella | 219 | 4 | 8 | 45 |
| mrkva | 118 | 1 | 0 | 44 |
| naranca | 111 | 0 | 2 | 37 |
| ocat | 145 | 2 | 20 | 195 |
| palenta | 79 | 6 | 1 | 0 |
| papar | 267 | 2 | 15 | 165 |
| paprika | 241 | 0 | 12 | 134 |
| parmezan | 110 | 5 | 4 | 18 |
| pasirana_rajcica | 134 | 6 | 2 | 4 |
| persin | 60 | 0 | 1 | 6 |
| pileca_prsa | 265 | 6 | 18 | 125 |
| piletina | 579 | 12 | 13 | 284 |
| prasak_za_pecivo | 45 | 4 | 1 | 0 |
| radic | 44 | 0 | 0 | 7 |
| rajcica | 198 | 1 | 7 | 189 |
| rajcica_konzerva | 183 | 7 | 0 | 1 |
| riza | 472 | 5 | 44 | 290 |
| rukola | 17 | 0 | 0 | 4 |
| secer | 312 | 0 | 22 | 126 |
| senf | 134 | 1 | 7 | 9 |
| slanina | 672 | 4 | 8 | 73 |
| slanutak | 116 | 1 | 3 | 30 |
| slatko_vrhnje | 33 | 5 | 8 | 0 |
| sol | 226 | 0 | 40 | 398 |
| spinat | 110 | 0 | 0 | 14 |
| sunka | 880 | 11 | 7 | 194 |
| svinjetina | 470 | 4 | 1 | 90 |
| svjezi_sir | 149 | 11 | 24 | 57 |
| tikvica | 53 | 0 | 0 | 9 |
| tjestenina | 1812 | 69 | 65 | 558 |
| tuna | 465 | 0 | 43 | 217 |
| tvrdi_sir | 1097 | 70 | 64 | 32 |
| ulje | 243 | 2 | 29 | 1330 |
| vanilin_secer | 63 | 3 | 7 | 18 |
| vrhnje_za_kuhanje | 72 | 4 | 5 | 0 |
| zelena_salata | 71 | 1 | 0 | 2 |
| zobene_pahuljice | 69 | 3 | 3 | 17 |

Napomena: među slabim članovima ima krivih pogodaka kad drugi lanci proizvod zovu samo markom, a jedan naziv prolazi `must_match` (npr. „ČOKOLADA RIKI PŠENICA I MED“ kao med, „MINI CROASANI S MASLACEM“ kao maslac). Rangirani su ispod snažnih i označeni; točka 4 (kratice, `must_not_match`) dio njih uklanja.

30 slučajnih slabih članova:

| namirnica | grupa | m % | nazivi po lancu |
|---|---|---|---|
| maslac | 8002734000594 | 33,00 | konzum: PANETTONE RUČNO MOT 1000 g GRAN DUCA; spar: PANETTONE VECCHIO FORNO 1000 g; tommy: PANETTONE MASLAC 1 KG GRANDUCA |
| dodatak_jelima | 3859892109790 | 33,00 | trgovina-krk: ZAČIN MOJ ZAČIN 200 g ŠAFRA; vrutak: N-MOJ ZAČIN ŠAFRAM 200G DODAT.JELIMA S POVRĆEM -20/1-; stridon: MOJ ZAČIN 200 g ŠAFRAM (20); trgocentar: MOJ ZAČIN 200G DODATAK JELIMA S POVRĆEM, ŠAFRAM (20); ktc: MOJ ZAČIN 200g; boso: ZAČIN ŠAFRA 200 g MOJ ZAČIN; branka: MOJ ZAČIN DODATAK JELIMA S POVRĆEM 200g; plodine: DODATAK JELIMA MOJ ZACIN 200 G VRECICA SAFRAM; spar: DODAT.JEL.S POVRĆEM 200 g |
| tjestenina | 8001250121707 | 40,00 | ribola: TJ.VERMICELLI 500 g DE CECCO; konzum: TIJESTO VERMICELLI 500 g DE CECCO; vrutak: TJEST VERMICELLI br.170 500G DE CECCO -24/1-; plodine: VERMICELLI 500 G DE CECCO; spar: TJES.DE CECCO VERMICELLI 500 g |
| tjestenina | 3858881509139 | 40,00 | ktc: ŠURLICE 350g KARLA; kaufland: Karla Tjestenina šurlice 350 g; konzum: ŠURLICE 350g KARLA; plodine: SURLICE 350 G KARLA; spar: TJESTENINA ŠURLICE KARLA 350 g |
| svinjetina | 3850139443530 | 33,00 | ribola: SV.REBRA MARIN.VP PIK; studenac: SVINJSKA MARINIRANA REBRA VP PIK kg; metro: CCA0,4KG SV.MARINIRANA REBRA V |
| rajcica_konzerva | 8001440133602 | 50,00 | kaufland: Cirio Rajčica sjeckana sa bosiljkom 390g; plodine: RAJCICA S BOSILJKOM 390 G CIRIO |
| svjezi_sir | 3850355007561 | 50,00 | lidl: President Zag.svj. sir bez laktoze; stridon: PRESIDENT ZAGREBAČKI SIR BEZ LAKTOZE 220 g DUKAT; plodine: SIR SVJEZI ZAGREBACKI 220 G PRESIDENT; ribola: SIR SV.ZAG.B.LA.220gPRESIDENT |
| tvrdi_sir | 3859889426459 | 33,00 | lorenco: SIR MEDITERANO PAŠKA SIRANA VP.1/4; plodine: SIR MEDITERANO 1/4 PASKA SIRANA; konzum: SIR TVRDI MEDITERANO VAC PAŠKA SIRAN |
| majoneza | 7613036679725 | 50,00 | boso: MAJON THOMY 80 g VREĆICA; stridon: MAJONEZA THOMY 80 g (24) |
| tjestenina | 3859888931053 | 50,00 | trgovina-krk: PLJUKANCI 500 gr SMRZNUTO; plodine: ISTARSKI PLJUKANCI 500 G MARIJA; konzum: PLJUKANCI 500 g MARIJA TJESTENINE; spar: TJES.MARIJA PLJUKANCI 500 g; lorenco: TJESTENINA PLJUKANCI "MARIJA"; jadranka_trgovina: TJESTENINA PLJUKANCI ISTARSKI DS 500G MARIJA |
| mljevena_paprika | 3859890104117 | 40,00 | studenac: PAPRIKA ZAC. MLJ.SL.500 g SAFRAM; trgocentar: PAPRIKA SLATKA ZAČINSKA 500G, ŠAFRAM; plodine: PAPRIKA SLA. MLJ. 500 G VR. SAFRAM; spar: ZAČ.PAPRIKA SLATK.ŠAFRAM 500 g; stridon: PAPRIKA ZAČ.MLJ.SL.500 g ŠAFRAM (8); trgovina-krk: PAPRIKA ZAČ.MLJ.SLATKA 500g; konzum: PAPRIKA SLATKA 500g ŠAFRAM; metro: 500G ŠAFRAM PAPRIKA MLJEV.SLAT; kaufland: Šafram paprika zač. mljev. slatka 500 g; ktc: PAPRIKA SLATKA 500g ŠAFRAM |
| med | 3859888851689 | 50,00 | tommy: MED ĐUMBIR PREM. 270 g APIMEL; lorenco: PREMIUM ĐUMBIR 270g |
| med | 3850220428491 | 50,00 | spar: PILEĆI FILE MIX 600 g; konzum: MEĐ PILEĆI MIX FILE 600g PERUTNINA |
| kiselo_vrhnje | 3870085020432 | 50,00 | plodine: KISELO VRHNJE 20,5% 850 G MEGGLE; studenac: VRHNJE ZA SV. SIR 850 g 22,5% mm ME |
| dodatak_jelima | 8600947042105 | 25,00 | konzum: ZAČIN ZA ČOBANAC 50g ALEVA; plodine: ZACIN ZA COBANAC 50 G ALEVA; kaufland: Aleva dod. jelima za čobanac 50 g; ntl: DODATAK JELIMA SA ZAČINIMA ZA ČOBANAC 50g ALEVA |
| jogurt | 3850108036695 | 50,00 | ktc: FORTIA JAG.-GRO.C.RIB.200g; branka: JOGURT FORTIA JAG GROŽĐE RIBIZ 200g |
| maslinovo_ulje | 3858882924023 | 25,00 | branka: ULJE KOKOS EX. DJEV. 300ml; tommy: BIO ULJE KOKOS. EX.DJ.300 ml A; lorenco: EKSTRA DJEVI.KOKOS.ULJE BIO 300ML; bure: ULJE KOKOSOVO 300 ml EXTRA DJEVIČANSKO |
| margarin | 8719200266582 | 25,00 | ktc: BECEL NAMAZ CLASSIC 225g; spar: NAMAZ BECEL CLASSIC 225 g; kaufland: Becel Namaz masni 225g vg.; zabac: BECEL margarina 225G |
| zobene_pahuljice | 3858882921077 | 33,00 | tommy: BIO ZOBENE PAHULJICE 500 g ADV; ribola: EKO PAH.ZOB.500 g BI ORGANIC ADVENT; studenac: ZOB. PAH. SITNE BIORGANIC 500 g |
| mozzarella | 8001665724814 | 50,00 | plodine: RAVIOLI RAJCICA/MOZZARELLA 250 G RANA; spar: RAVIOL.RAJČ.MOZZARE.RANA 250 g |
| griz | 3858881327290 | 25,00 | trgocentar: ULTRA KRUPICA PŠENIČNA 1KG, KLARA (20)(GRIS); bure: PŠEN.KRUPICA 1 kg ULTRA; ribola: GRIS PŠ.KRUP 1 kg ULTRA; djelo_vodice: PŠENIČNI GRIZ 1KG ULTRA |
| zobene_pahuljice | 3858882921084 | 50,00 | jadranka_trgovina: ZOBENE PAHULJICE KRUPNE 500G PRIMAVITA; bure: PAHULJ.ZOB.500 g KRUPNE ADVENT; branka: PAHULJICE ZOBENE KRUPNE 500g; ribola: PAH.KR.ZOB.500 g PRI MAVITA ADVENT; studenac: ZOB. PAH. KRUPNE ADVENT 500 g; tommy: PAHULJICE ZOBENE KRUP.500 g AD |
| tjestenina | 5201193218530 | 50,00 | konzum: TJESTENINA MINIONS 400 g MELISSA; spar: TJESTEN.MINIONS MELISSA 400 g |
| tjestenina | 8005121000900 | 50,00 | branka: TJESTENINA DIVELLA FETTUCCINE 90 500g; stridon: FETUCCINE A NIDI 90 500 G(12) DIVELLA (IT) |
| tvrdi_sir | 3228023910039 | 25,00 | kaufland: President sir Ementaler 250g; konzum: SIR TVRDI EMENTAL PRES 250g DUKAT; ribola: SIR EMEN.250 g PRESI; trgovina-krk: SIR PRESIDENT EMENTALER 250 g DUKAT; ntl: SIR EMENTALER PRESIDENT 250 g DUKAT; trgocentar: PRESIDENT EMENTALER 250G, DUKAT; ktc: SIR PRESIDENT EMENTALER 250g; spar: SIR EMMENTAL PRESIDENT 250 g; tommy: SIR EMENTAL 250 g PRESIDENT; plodine: EMENTALER PRESIDENT 250 G DUKAT; studenac: SIR EMMENTAL PRESID. 250 g; vrutak: SIR PRESIDENT EMENTALER 250G -12/1- |
| med | 3858881047372 | 50,00 | ribola: ČOK.HONEY RIKI 230g; stridon: ČOKOLADA RIKI PŠENICA I MED KANDIT 230 g (9) |
| piletina | 3850220428514 | 25,00 | spar: PILEĆI MIX ZA JUHU 400 g; ktc: PILEĆI MIX ZA JUHU 400g PIPO; trgovina-krk: PILEĆI MIX ZA JUHU 400G PERUTNINA; plodine: MEDJIMURSKO PILE PILECI MIX ZA JUHU 400 G PERUTNINA |
| rajcica | 8437007225402 | 50,00 | ribola: \*RAJC CRNA 500 g; studenac: RAJČICA CRNA 500 g |
| maslinovo_ulje | 3858888737931 | 33,00 | tommy: BIO ULJE KOKOS. EX.DJ.300 ml E; vrutak: ULJE KOKOSOVO 300ML EKOZONA EKSTRA DJEVIČANSKO; ribola: ULJE KOKOS EX. 300ml; plodine: ULJE KOKOS EKSTRA DJEVICANSKO 300 ML EKOZONA; studenac: ULJE KOKOSOVO EXTRA DJEV. EKOZONA 300 ml; ktc: ULJE KOKOSOVO EKST.DJEVIČ.300mL EKOZONA |
| jogurt | 3850354014829 | 50,00 | trgovina-krk: JOGURT B.ACTIV MULTIV. BERI BOOM 330 g DUKA; plodine: B.AKTIV LGG MULTIVITAMIN BERRY BOOM 330 G DUKAT |

30 grupa koje prelaze iz člana (2D) u `ambiguous`:

| namirnica | grupa | m % | x % | nazivi po lancu |
|---|---|---|---|---|
| med | 5949040205158 | 73,00 | 18,00 | spar: PECIV.ELEP.TWIST SOL-MED 180 g; ntl: TRAJNO PEC. ELEP.TWIST - MORSKA SOL I MED 180g; plodine: KREKER MORSKA SOL I MED 180 G ELEPHANT; tommy: SNACK SOL MED 180 g ELEPHANT; gavranovic: PECIVO TWIST MORSKA SOL I MED 180g - ELEPHANT; kaufland: Elephant Pecivo sl.morska sol,med180 g; ktc: ELEPHANT TWIST MORSKA SOL I MED 180g; konzum: KREKE TWIST SOL I MED 180 g ELEPHANT; metro: 180G ELEPHANT TWIST SOL I MED; djelo_vodice: ELEPHANT TWIST - MORSKA SOL i MED 180G; ribola: KREK.M.SOL&MED 180 g ELEPHANT |
| senf | 5949040204953 | 60,00 | 10,00 | stridon: ALKA ELEPHANT TS PECIVO-KOMAD.S OKUS.MEDA 14\*75 g; tommy: SNACK MED SENF LUK 75 g ELEPHA; boso: KREKE ELEPHANT 75 g MED SENF LUK; plodine: PEREC KOMADICI S OKUSOM MEDA,SENFA I LUKA 75 G ELEPHANT; kaufland: Elephant Komadići med,senf i luk75g; konzum: PER LOMLJ MED SENF LUK 75 g ELEPHANT; ktc: ELEPHANT KOMADIĆI MED,SENF I LUK 75g; gavranovic: PECIVO KOMADIĆI MED,SENF I LUK 75g ELEPHANT; ntl: TRAJNO SLANO PECIVO ELEPHANT PRETZEL 75 g MED, SENF I LUK; ribola: PERECI ME.SE.LU.75 g ELEPHANT |
| papar | 9001414274057 | 80,00 | 20,00 | spar: ZAČ. PAPAR S&D CRNI ZRNO 50 g; plodine: SPICES DRINKS PAPAR CRNI, ZRNO 50 G; ntl: ZAČIN ZA KOKTELE SPICES & DRINKS PAPAR CRNI 50 g KOTANYI; kaufland: Kotany papar crni zrno, bočica 50 g; lorenco: PAPAR CRNI ZRNO SiD STAKLO 100ML |
| tjestenina | 8008857300771 | 83,00 | 17,00 | trgocentar: SPAGETTI TAGLIATI 77 (SITNI REZANCI) 500G PASTA REGGIA (24); trgovina-krk: TJEST. TAGLIATI 500 g REGGIA NTL; ntl: TJESTENINA TAGLAITI 500g REGGIA; jadranka_trgovina: TJESTENINA SPAGHETTI TAGLIATI 077 500G REGGIA; bure: TJ.FIDELINI 77 500 gREGGIA (SPAGET.TAGLI; ribola: TJ.SPAGHETTI 500 g TAGLIATI JUHA REGGIA |
| sol | 3856020222314 | 80,00 | 20,00 | ribola: SOL MORSKA 100 g VE GETA MAESTRO; stridon: VEGETA MAESTRO MORSKA SOL M.100 G (6) PODRAVKA; konzum: ZAČIN SOL MORSKA ML 100g VEGETA MAESTRO; lorenco: VEGETA MAESTRO MORSKA SOL 100G; ktc: MORSKA SOL GRUBO MLJEVENA 100g PODRAVKA; tommy: VEGETA MAESTRO MORSKA SOL GRUBO MLJEVENA 100G; spar: ZAČ.SOL MORSKA VEG.MAES.100 g; plodine: MORSKA SOL MLINAC 100 G VEGETA MAESTRO; bure: SOL MORSKA 100 g KRUNA PODR.; djelo_vodice: MORSKA SOL GRUBO MLJEVENA VEGETA MAESTRO BOČICA 100G |
| majoneza | 3856015304339 | 86,00 | 14,00 | studenac: MAJONEZA ZV. 165G ČILI TUBA; vrutak: N-MAJONEZA ZVIJEZDA 165G -12/1 ČILI TUBA; kaufland: Zvijezda čili majoneza tuba 165g; plodine: MAJONEZA CILI 165 G TUBA ZVIJEZDA; trgovina-krk: MAJONEZA ČILI 165 g ZVIJ; gavranovic: MAJONEZA CHILLI 165g ZVIJEZDA; roto: MAJONEZA ČILI 165G ZVIJEZDA (12); branka: MAJONEZA ČILI 165g; lorenco: ZVIJEZDA ČILI MAJONEZA 165g; trgocentar: MAJONEZA CHILI 165G TUBA (12) ZVIJEZDA; stridon: MAJONEZA ČILI TUBA 165 g (12) ZVIJEZDA; konzum: MAJONEZA ČILI 165g ZVIJEZDA; jadranka_trgovina: MAJONEZA 165G ČILI TUBA ZVIJEZDA; ktc: MAJONEZA TUBA ČILI 165g ZVIJEZDA |
| maslac | 3856015325419 | 86,00 | 14,00 | tommy: MARGO S MASLACEM 225 G; ktc: MARGO S MASLACEM 225g ZVIJEZDA; trgocentar: MARGO S MASLACEM 225G (16),ZVIJEZDA; vrutak: N-MARGO S MASLACEM 225G -16/1-; spar: NAMAZ MARGO S MASLACEM 225 g; trgovina-krk: MARGO S MASLACEM 225 gr; stridon: MARGO S MASLACEM 225 g ZVIJEZDA (16); boso: MARG. MARGO 225 g S MASLACEM; lorenco: MARGO S MASLACEM 225G ZVIJEZDA; plodine: MARGO S MASLACEM 225 G ZVIJEZDA; konzum: MARGO S MASLACEM 225g; jadranka_trgovina: MARGARIN MARGO S MASLACEM 225G ZVIJEZDA; branka: MARGARIN MARGO MASLAC 225g; kaufland: Margo Namaz miješani s maslacem 225g |
| papar | 9001414040867 | 60,00 | 10,00 | branka: \*NE\*PAPAR MJEŠAVINA 35G STAKLO KOTANYI; spar: ZAČ.PAPAR MJEŠ.KOTANYI 40 g; trgovina-krk: ZAČIN MJEŠAVINA PAPRA STAKLO 40 g KOTANY; gavranovic: KOTANYI PAPAR MJEŠAVINA STAKLO 40g; plodine: PAPAR MIX 40 G STAKLO KOTANYI; vrutak: KOTANYI 40G PAPAR ŠARENAMJEŠAVINA STAKLO -4/1-; studenac: ZAČIN PAPAR ŠARENI 40 g KOT.; tommy: ZAČIN PAPAR MJEŠ.40 g KOTANY; bure: ZAČIN MJEŠ.PAPRA 100g; lorenco: ZAČIN MJEŠ. PAPRA 35 g KOTANYI |
| sol | 3870009000144 | 80,00 | 20,00 | ktc: SOL KAMENA DOZA 250g TUZLA; kaufland: Tuzla kuhinjska sol jodirana 250g; spar: SOL KUHINJ. TUZLA SITNA 250 g; plodine: SOL KUHINJSKA JODIRANA 250 G TULJAK TUZLA; vrutak: SOL KAMENA 250G SOLJENKA -15/1- TUZLA |
| grah | 3083680001793 | 67,00 | 17,00 | konzum: GRAH BIJELI RAJČICA 430/200g BONDUELLE; plodine: BRETONA BIJELI GRAH U UMAKU OD RAJCICE 430 G; spar: GRAH BONDUELLE BRETONA 430 g; lorenco: BONDUELLE BIJELI GRAH S RAJČ.400g; vrutak: N-GRAH BIJELI BONDUELLE 400G S RAJČICOM; kaufland: Bonduelle Bretona 430g/200g |
| kiseli_kupus | 3859891493098 | 56,00 | 11,00 | tommy: KUPUS KIS. MIX ZA SARMU 1000 g; trgovina-krk: KUPUS KISELI MIX MADIG ZA SARMU 1 kg NTL; studenac: KIS. ZELJE MIX ZA SARMU 1100 g; eurospin: KUPUS KISELI MIX ZA SARMU 1kg; spar: KUPUS KIS.MIX ZA SARMU 1 kg; lorenco: MADIG MIX ZA SARMU 1000g; konzum: KUPUS KISELI MIX ZA SARMU MADIG; gavranovic: ZELJE KISELO MIX ZA SARMU 1KG MADIG; plodine: SARMA MIX 1 KG KISELI KUPUS MADIG |
| papar | 9001414440834 | 86,00 | 14,00 | vrutak: KOTANYI KOKTEL PAPAR CRVENI SPICE i DRINKS 25G ZRNO; konzum: PAPAR CRVENI ZRNO S&D 25g KONTAYI; gavranovic: KOTANYI PAPAR CRVENI ZRNO 25g SPICE DRINKS; spar: ZAČIN PAPAR CRVENI ZRNO 25 g; lorenco: PAPAR CRVENI ZRNO KOKTEL SND ST 100; plodine: SPICES DRINKS PAPAR CRVENI ZRNO 25 G; ntl: ZAČIN ZA KOKTELE SPICES & DRINKS PAPAR CRVENI 25 g KOTANYI |
| kukuruz | 3859893512254 | 70,00 | 30,00 | gavranovic: KUKURUZ PEČENI SLANI BBQ 60g NATURA; plodine: KUKURUZ PECENI SLANI BBQ 60 G SUPER SNACK NATURA; trgocentar: KUKURUZ PEČENI SLANI 60G BBQ SUPER SNACK; trgovina-krk: KUKURUZ PS BBQ NATURA 60 g; vrutak: N-KUKURUZ NATURA 60G PEČENI SLANI BBQ -20/1- SUPER SNACK; spar: KUKURUZ PEČ.SLANI NATURA 60 g; studenac: KUKURUZ PEČ.SL. NATURA 60 g; lorenco: KUKURUZ PEČENI SALNI BBQ 60g S.SNAC; jadranka_trgovina: KUKURUZ PEČENI SLANI BBQ 60G; ribola: KUKURUZ PEČENI 60 g SLANI NATURA |
| majoneza | 3856015324689 | 81,00 | 14,00 | studenac: MAJONEZA ČILI 85g ZVIJ.; branka: MAJONEZA ČILI 85g; djelo_vodice: ČILI MAJONEZA 85g; gavranovic: MAJONEZA CHILLI VREĆICA 85g ZVIJEZDA; roto: MAJONEZA ČILI PVC 85g ZVIJEZDA (25); lorenco: ZVIJEZDA MAJONEZA ČILI 85G; metro: 85G ZVIJEZDA MAJONEZA ČILI; vrutak: N-MAJONEZA ZVIJEZDA 85G -25/1 ČILI; trgovina-krk: MAJONEZA ČILI 85G; boso: MAJON ZVIJE 85 g DELIK.ČILI; jadranka_trgovina: MAJONEZA 85G ČILI VREĆICA ZVIJEZDA; konzum: MAJONEZA ČILI PVC 85g ZVIJEZDA; trgocentar: MAJONEZA ČILI 85G ,ZVIJEZDA; kaufland: Zvijezda majoneza čili 85 g; ribola: MAJONEZA ČILI 85 g ZVIJEZDA; spar: MAJONEZA CHILI ZVIJEZDA 85 g; zabac: CHILI MAJONEZA 75% 85 G; stridon: MAJONEZA ČILI ZVIJEZDA 85 g (25); tommy: MAJONEZA ČILI 85 G ZVIJEZDA; ktc: MAJONEZA ČILI 85g ZVIJEZDA; lidl: Zvijezda Majoneza Čili |
| tuna | 8004030860025 | 0,00 | 86,00 | kaufland: Rio Mare Insal.sal.tuna cous cous2x160g; konzum: TUNJ SALATA COUS COUS 2X160g RIO MARE; lorenco: TUNA -COUS-COUS SAL.2\*160g BOWL.; tommy: TUNA SALATA CUS CUS 2X160 G RIO MARE; spar: TUNA SAL.RIO MARE COUS 2X160 g; metro: 160GX2 RIO MARE INSALA.CUS CUS; plodine: TUNA COUS-COUS SAL.2X160G BOWL |
| med | 5949040203482 | 63,00 | 25,00 | plodine: SNACK MORSKA SOL I MED 160 G ELEPHANT TWIST; gavranovic: PECIVO TWIST MORSKA SOL I MED 160g - ELEPHANT; kaufland: Elephant Twist sl.pecivo m.sol i med160g; ribola: KREK.M.SOL&MED 160 g ELEPHANT; tommy: SNACK SOL MED 160 g ELEPHANT; djelo_vodice: ELEPHANT TWIST - MORSKA SOL i MED 160g; lorenco: ALKA ELEPHANT TWIST-SOL I MED 160g; ntl: TRAJNO PEC. ELEP.TWIST - MORSKA SOL I MED 160g |
| papar | 9001414050026 | 54,00 | 46,00 | trgovina-krk: PAPAR ZELENI U SALAMURI 100 g KOTAN; ribola: PAPAR ZEL.SAL. 100 g KOTANYI; vrutak: KOTANYI 100G PAPAR ZELENI USALAMURI -24/1-; roto: PAPAR ZELENI U SALAMURI 100g KOTANYI (24); lorenco: ZELENI PAPAR 100 g KOTANYI; metro: 100G KOTANYI PAPAR ZELENI U SA; bure: PAPAR ZELENI 100 g SALAMURA UG.; spar: ZAČ.PAPAR ZELEN.KOTANYI 100 g; trgocentar: KOTANY ZELENI PAPAR U ZRNU 100G; djelo_vodice: PAPAR ZEL.SALAMURA; tommy: ZAČIN PAPAR ZEL/SAL. 100 g KOT; studenac: ZAČIN PAPAR ZELENI U SALAMURI 100 g KO; gavranovic: KOTANYI PAPAR ZEL.U SALAMURI 100g |
| pileca_prsa | 3856020257064 | 57,00 | 14,00 | tommy: PILEĆA PRSA 60 G LINO NARESCI PODRAVKA; spar: PILEĆA PRSA LINO NJUPAL. 60 g; ktc: PILEĆA PRSA 60g LINO; ribola: ŠUNKA PILEĆA 60 g LINO PODRAVKA; plodine: LINO PILECA PRSA 60 G PODRAVKA; stridon: LINO PILEĆA ŠUNKA 60 g (10) PODRAVKA; konzum: LINO PILEĆA PRSA 60 g |
| sol | 9001414040034 | 69,00 | 31,00 | kaufland: Kotanyi himalajska sol 120 g bočica; spar: SOL HIMALAJ.SITNA KOTANY120 g; trgovina-krk: ZAČIN SOL HIMALAJSKA BOČICA KOTA; branka: SOL HIMALAJSKA BOČICA 120g; studenac: ZAČIN HIMALAJSKA SOL 120 g KOT.; bure: SOL HIMALAJSKA 100 ml STAKLO; plodine: HIMALAJSKA SOL 120 G KOTANY BOCICA; ribola: SOL HIMALAJSKA 120 g STAKLO KOTANYI; djelo_vodice: HIMALAJSKA SOL 100ML; tommy: SOL HIMALAJSKA STAK. 120 g KOT; konzum: HIMALAJSKA SOL BOČ 120G KOTANYI; ktc: SOL HIMALAJSKA 100mL ST KOTANYI; lorenco: HIMALAJSKA SOL JODIRANA STAKLO 100 |
| piletina | 3850159142321 | 77,00 | 15,00 | stridon: CEKIN KRILCA BUCKET 500 g 14232 VINDIJA; ribola: PIL.KRIL.BUCK. 500 gVINDIJA; vrutak: N-VIN KRILCA BUCKET 500G -4/1-; trgocentar: CEKIN KRILCA BUCKET 500G; boso: KRILCA CEKIN 500 g BUCKET; spar: PILE.KRILCA BUCKET CEKIN 500 g; ktc: CEKIN KIDS BUCKET KRILCA 500g; ntl: KRILCA PILEĆA PEČENA SM 500 g CEKIN; branka: KRILCA BUCKET CEKIN 500g; plodine: CEKIN KRILCA BUCKET 500 G; jadranka_trgovina: KRILCA BUCKET CEKIN 500G VINDIJA; kaufland: Cekin Pečena pileća krilca 500 g; trgovina-krk: CEKIN KRILCA BUCKET 500G |
| dodatak_jelima | 3856020228910 | 90,00 | 10,00 | bure: VEGETA VR.BURG. 30 gCLASSIC; trgocentar: VEGETA NATUR BURGER CLASSIC VR.30G (18) (PAL 252) PODRAVKA; kaufland: Vegeta Natur Grill Burger classic 30 g; tommy: VEGETA NATUR BURGER VR.30 g PO; stridon: VEGETA NATUR BURGER CLASSIC 30 g (18); konzum: ZAČIN BURGER CLASSIC VR 30g VEGETA NATUR; lorenco: VEGETA NATUR BURGER CLASSIC VR.30g; plodine: VEGETA NATUR BURGER 30 G CLASSIC; trgovina-krk: VEGETA NATUR BURGER CLASSIC 30 g VREĆICA POD; spar: ZAČIN VEGETA NATUR BURGER 30 g |
| sol | 3856020267216 | 83,00 | 17,00 | spar: ZAČ.V.MAEST.SITNA MOR.SOL 110g; bure: VEGETA MAESTRO 110g SITNA SOL; lorenco: VEGETA MAESTRO SITNA MORSKA SOL; tommy: VEGETA MAESTRO SITNA MORSKA SOL POSIPAČ 110 g; plodine: VEGETA MAESTRO SITNA MORSKA SOL POSIPAC 110 G BOCICA; konzum: SOL SITNA MORSKA 110g VEGETA MAESTRO |
| piletina | 3850159113154 | 60,00 | 20,00 | konzum: PILE GAVELINO POD VINDIJA; spar: PILE GAVELINO; studenac: PILE GAVELINO VINDIJA KOKA kg; ribola: GAVELINO VINDIJA; plodine: GAVELINO PILE ZA PECENJE CEKIN (11315) |
| pileca_prsa | 3850159125034 | 78,00 | 17,00 | kaufland: Cekin Pileća prsa u ovitku 500g; stridon: PILEĆA PRSA U OVITKU 500 g VINDIJA 12503; vrutak: N-VIN PIL.PRSA U OVITKU 500G-12/1- 12503; boso: PILEĆ KOKA 500 g PRSA U OVITKU; branka: SALAMA PILEĆA PRSA 500g; konzum: PRSA PILEĆA U OVITKU 500g VINDIJA; lorenco: PILEĆA PRSA 500g CEKIN; plodine: PILECA PRSA U OVITKU 500 G CEKIN (12503) VINDIJA; trgovina-krk: SALAMA PILEĆA PRSA U OVITKU 500 g VINDIJA; bure: PILEĆA PRSA OV.500 gCEKIN LOT:1726102801; metro: 500GR CEKIN PIL PRSA U OVITKU; tommy: PILEĆA PRSA U OVIT.500 g VI; spar: PIL.PRSA U OVITKU VIN. 500 g; ntl: SALAMA PILEĆA PRSA U OVITKU 500 g KOKA; studenac: PILEĆA PRSA U OVITKU 500g; trgocentar: PILEĆA PRSA U OVITKU 500G; gavranovic: PILEĆA PRSA U OVITKU 500g CEKIN (12503); ktc: PILEĆA PRSA U OVITKU 500g KOKA |
| tjestenina | 8710605028430 | 71,00 | 29,00 | ntl: TJESTENINA OD PŠ. BRAŠNA S JAJIMA 250G NIKAS; plodine: TJESTENINA S JAJIMA GNIJEZDA 250 G NOODLES GO TAN; vrutak: TJESTENINA GO-TAN 250G EGG WOK NOODLES -8/1-; kaufland: Go Tan tjest.s jajima za Wok 250 g; ribola: TJEST.GO TAN 250g; konzum: TJESTENINA S JAJIMA GNIJEZDA GO TAN 250g; spar: TJESTENINA GOTAN NEST 250 g |
| zobene_pahuljice | 8595054907761 | 67,00 | 25,00 | tommy: ZOBENE PAH. ŠUM.VOĆE 300 g DOB; zabac: Dobre zobene pahuljice 300g BERRIES; kaufland: Dobre Pahuljice zobene bobič.voće 300g; lorenco: DOBRE ZOBENE PAHULJICE 300g BERRIES; spar: DOBRE ZOBENE PAH.BOB.VOĆ.300 g; konzum: PAHULJICE ZOBENE BERRIES 300g; vrutak: ZOBENE PAHULJICE 300G BERRIES; branka: PAHULJICE ZOBENE BERRIES 300g; plodine: ZOBENE PAHULJICE SUMSKO VOCE 300 G BIOPLOD; ribola: PAHULJ.ZO.BO.300 g D OBRE PAHULJICE; gavranovic: ZOBENE PAHULJICE DOBRE BERRIES 300g; ntl: PAHULJICE ZOBENE BERRIES 300 g DOBRE |
| jaja | 5200701000063 | 67,00 | 17,00 | trgovina-krk: SRCE JAJE PEPPA PIG 10G; ribola: PEPPA PIG JAJE 10 g; vrutak: SRCE PL. PEPPA PIG 10G; studenac: BOM. JAJE PEPA PIG 10 g; konzum: JAJE S BOMBONIMA PEPA PIG 10g; ntl: JAJE IZNENAĐENJA 10 g MIX LICENCA |
| med | 5900617037152 | 86,00 | 14,00 | kaufland: Sante Granola Gold med i oraš.plod.300g; jadranka_trgovina: ŽITARICE GRANOLA GOLD ORASI+MED 300G SANTE; ribola: GRANOLA 300 g ORAH/ MED SANTE; konzum: MUESLI GRANOLA ORAŠ PLOD MED 300g SANTE; tommy: MUESLI GRAN. NUT/MED 300 g SAN; spar: GRAN.SANTE ORAŠ.PLOD.MED 300 g; plodine: MUESLI GRANOLA MED I ORASASTI PLODOVI 300 G SANTE |
| sol | 9001414046241 | 75,00 | 25,00 | tommy: SOL MORSKA JODIRANA 120 g KOTAN; vrutak: KOTANYI 100ML MORSKA SOL SITNA STAKLO -4/1-; kaufland: Kotanyi Sol morska sitna jodirana 120g; plodine: MORSKA SOL 120 G BOCICA KOTANYI; spar: MORSKA SOL KOTANY 120g; bure: SOL SITNA 100ml STAKLO; konzum: MORSKA SOL BOČ 120 g KOTANYI; metro: 120G KOTANYI MORSKA SOL BOČICA |
| pileca_prsa | 3850159123306 | 59,00 | 35,00 | vrutak: VIN PILEĆA PRSA 100G; djelo_vodice: PILEĆA PRSA 100G VIN.; ribola: PIL.PRS.U OV.100 g VINDIJA; konzum: PRSA PILEĆA U OVITKU NAR 100g; lorenco: PILEĆA PRSA 100g; jadranka_trgovina: SALAMA PILEĆA PRSA 100G CEKIN VINDIJA; kaufland: Cekin Pileća prsa 100 g; stridon: PILEĆA PRSA 100 g VINDIJA; trgocentar: PILEĆA PRSA 100G, VINDIJA; spar: PILEĆA PRSA 100 g; ktc: PILEĆA PRSA 100g VINDIJA; tommy: PILEĆA PRSA NARESCI 100 g; plodine: PILECA PRSA 100 G VINDIJA; studenac: PIL. PRSA U OVIT. 10 0g VINDVAC; trgovina-krk: SALAMA PILEĆA PRSA 100 g VIND; gavranovic: CEKIN PILEĆA PRSA NAREZAK 100g; ntl: SALAMA PRSA PILEĆA 100 g VINDIVAC |

## 4. Sinonimi i kratice

`data/abbrev.yaml` proširuje kratice prije podudaranja (`clean.products.match_norm`; izvorni naziv i `name_norm` ostaju): praš. pec. → prašak za pecivo, braš. → brašno, mlij. → mlijeko, jog. → jogurt, tj./tje./tjest. → tjestenina, vrh. → vrhnje, pil. → pileći, kuh. → kuhanje, „ŠIR VALJ“ → široki. „pec.“ i „sv.“ sami se ne šire (peč./pečeni, svinjski/svježe).

Novi `must_match`: tjestenina (oblici i marke iz zahtjeva), jogurt `jog\b`, pileća prsa (odresci, file od prsa, pileći file; `odresc` više nije isključen), svinjetina (rebra), vrhnje za kuhanje (creme cuisine), tvrdi sir (leerdammer, emmental, maasdam, edam\b, cheddar). Tuna isključuje cous, bowl, sal, salat. Uz „školjke“ i „tj“ dodana su isključenja (morski plodovi, pralines, čarape, „za tj“ = za tijelo, gotove lazanje).

Grupe vraćene u namirnicu (i izgubljene) po namirnici:

| namirnica | vraćeno | izgubljeno |
|---|---|---|
| tjestenina | 450 | 7 |
| tvrdi_sir | 206 | 0 |
| jogurt | 89 | 3 |
| mlijeko | 35 | 9 |
| pileca_prsa | 27 | 0 |
| svinjetina | 24 | 0 |
| kiselo_vrhnje | 5 | 0 |
| slatko_vrhnje | 3 | 0 |
| vrhnje_za_kuhanje | 2 | 0 |
| prasak_za_pecivo | 1 | 0 |
| tuna | 0 | 9 |
| riza | 0 | 7 |
| svjezi_sir | 0 | 4 |
| sol | 0 | 1 |
| med | 0 | 1 |

30 nasumičnih vraćenih grupa:

| namirnica | razina | nazivi po lancu |
|---|---|---|
| tjestenina | strong | metro: 750G KARLA ŠKOLJKICE |
| jogurt | strong | kaufland: KLC.Muesli pločica marelica+jog.30g |
| jogurt | strong | spar: JOG.FANTASIA ČOK.KUGLICE 100g; jadranka_trgovina: JOGURT FANTASIA ČOK.KUGLICE 100G DANONE; plodine: JOG.FANTASIA COK.KUG.100G DANONE MAGROS |
| tjestenina | strong | tommy: TJ. FUŽI 250 g KLARA MARIĆ; spar: TJ.KLARA MARIĆ FUŽI. 250 g; konzum: TIJESTO FUŽI 250g KLARA M; djelo_vodice: ISTARSKI FUŽI 250G |
| tjestenina | strong | trgovina-krk: REZANCI ZELENI ZA GASTRO 1 kg |
| tvrdi_sir | strong | konzum: SIR WHITE CHEDDAR NAR DELISO 200 g |
| jogurt | strong | lorenco: JOG.ACTIVIA PRIRODNA 330g |
| tvrdi_sir | strong | lorenco: SIR BAYERNTALER EMMENTALER |
| tjestenina | strong | spar: LASAGNE DESPAR 250 g |
| tvrdi_sir | strong | kaufland: KLC.Sir Emmentaler ribani XXL 500 g |
| jogurt | weak | ribola: JOG.250g BORO.+Ž.SEN; stridon: SENSIA BOROVNICA ŽITARICE 250 g TT DUKAT |
| tjestenina | strong | metro: 1KG MC LASAGNE BEZ JAJA |
| tjestenina | strong | tommy: TJ. RAJČICA MOZZARELLA U ČAŠI 70 g BERRUTO |
| tjestenina | strong | studenac: TJ. CETINA 400g br.20 LAZANJA SAVI.; lorenco: LAZANJA SAVIJENA br.20 400g; ribola: TJ.LAZANJA 400 g BR. 20 SAVIJEN TJ.CETIN; tommy: TJ.LAZANJA SAV.20 400 g CETI; djelo_vodice: TJE.CETINA LAZANJE SAVIJENA BR.200 400G |
| tvrdi_sir | strong | dukat: PRESIDENT CHEDDAR ZRELI 200g; studenac: SIR CHEDDAR MATURE PRESIDENT 200 g; konzum: SIR POLU CHEDDAR MATURE 200g; plodine: SIR CHEDDAR MATURE 200 G PRESIDENT DUKAT; tommy: SIR CHEDDAR MATUR 200 g PRESID; vrutak: N-SIR PRESIDENT CHEDDAR MATURE 200G; spar: SIR CHEDD.MATURE PRESID.200 g |
| tvrdi_sir | strong | metro: CCA3KG OLDENBURGER EDAM |
| jogurt | strong | plodine: JOG. VOC. MIX 140 G DOLCE DUKAT |
| tjestenina | strong | tommy: TJ.DITALI BR.66 500 g ARRIGHI |
| tvrdi_sir | strong | metro: 500G MC EDAM REZANI 40% |
| tjestenina | strong | konzum: TIJESTO CONCHIGLIE 54 500g PASTA ZA; roto: TIJESTO CONCHIGLIE 54 500g PASTA ZA (10) |
| jogurt | weak | plodine: FRESKA JAGODA VAN. 330 G VINDIJA; bure: JOG.VOĆ. 330 g JAG-VAN. LOT:1426082768 |
| tvrdi_sir | strong | lidl: Sir Cheddar Mature XXL |
| tjestenina | strong | plodine: ZENSKI SESIR 042992 SA SKOLJKICAMA |
| tjestenina | strong | eurospin: REZANCI S JAJIMA PAPPARDELLE 250g |
| tjestenina | strong | plodine: LEGO BOTANICALS MINI LJILJAN |
| pileca_prsa | strong | ktc: FILE OD PRSA SVJ.RFS PIPO |
| tvrdi_sir | strong | zabac: SPECIAL MOMENTS Mature Colored Cheddar Cheese 48+, 10x200g; konzum: SIR CHEDDAR MATURE RED 200 g SPEC MOM |
| jogurt | strong | metro: 150GR DUKATOS NATUR JOG. |
| tjestenina | strong | eurospin: REZANCI ŠIROKI S JAJIMA 400g |
| jogurt | strong | spar: JOG.NATUR SPAR HIGH PROT.500 g |

## 5. „cvijet“ i dječji pjenušac

„cvijet“ više nije u strogom popisu neprehrane (vrijedi za sve proizvode), nego samo u širem popisu za ručne iznimke po lancu, uz zaštite: čaj, brokula, cvjetača, sol, kulen, kamilica, bazga, neven, lipa, ukrasni cvjetići. Dječji pjenušac (dječj…, spužva bob, bez alkohola, 0,0, i kategorija „DJEČJI PJENUŠCI“) je `pice`, ne `alkohol`.

| promjena | proizvoda |
|---|---|
| ostalo → hrana | 71 |
| alkohol → pice | 38 |
| ostalo → pice | 13 |
| djeca → pice | 11 |
| unknown → hrana | 5 |
| alkohol → unknown | 3 |
| kucanstvo → hrana | 2 |
| hrana → ostalo | 2 |
| ostalo → unknown | 1 |
| kozmetika → hrana | 1 |
| unknown → pice | 1 |
| unknown → ostalo | 1 |

Vraćeno u `hrana` s „cvijet“ u nazivu: **78**. 20 primjera:

| lanac | naziv | kategorija | prije |
|---|---|---|---|
| branka | ČAJ NEVEN CVIJET S/C 30g | HRANA | ostalo |
| metro | BEGONIJA CVIJET KOM | hrana | ostalo |
| lorenco | SOLNI CVIJET 150g |  | unknown |
| plodine | CAJ KAMILICA CVIJET 50 G AGRISTAR |  | ostalo |
| ktc | ČAJ KAMILICA CVIJET 50g AGRISTAR | HRANA | ostalo |
| konzum | ČAJ KAMILICA CVIJET 50g AGRISTAR | HRANA | ostalo |
| konzum | SOL SOLNI CVIJET 125g | HRANA | ostalo |
| metro | 100G TIKVICA CVIJET | hrana | ostalo |
| kaufland | KBio.Šećer od kokosovog cvijeta 250g | HRANA | ostalo |
| ntl | CVIJETAČA SM 2,5KG ZMH | Hrana | ostalo |
| lorenco | MED CVIJETNI -LIVADA 20g |  | unknown |
| plodine | SOL CVIJETNA 125 G SOLANA PAG |  | unknown |
| ktc | ČAJ BAZGA CVIJET 40g AGRISTAR | HRANA | ostalo |
| dm | dmBio čaj cvijet lipe 20x1,5 g 30 g | prehrana | ostalo |
| branka | ČAJ LAVANDA CVIJET 100g | HRANA | ostalo |
| kaufland | Solana Pag Sol paška solni cvijet 150g | HRANA | ostalo |
| lorenco | MED CVJETNI CHN/HR 900G |  | unknown |
| lorenco | MED CVJETNI 459 GRAMA |  | ostalo |
| branka | ČAJ LIPA CVIJET 100g | HRANA | ostalo |
| metro | 100G TIKVICA CVIJET | hrana | ostalo |

Napomena: Metro „BEGONIJA CVIJET KOM“ (biljka u kategoriji hrane) se vraća u hranu, jer Metro nije među ručnim iznimkama po lancu; vrećice sjemena („SJEME GARDEN CVJETAČA“) ostaju neprehrana.

Primjeri novog `pice`:

| lanac | naziv | prije | poslije |
|---|---|---|---|
| branka | ČAJ HIBISKUS CVIJET 30g | ostalo | pice |
| djelo_vodice | PJENUŠAC BATMAN 0,75L | djeca | pice |
| djelo_vodice | PJENUŠAC CARS 0,75L | djeca | pice |
| djelo_vodice | PJENUŠAC DJ.FROZEN 0,75L | djeca | pice |
| djelo_vodice | PJENUŠAC DJ.MICKEY MOUSE 0,75L | djeca | pice |
| djelo_vodice | PJENUŠAC DJEČJI HELLO KITTY JAGODA 0,75L | djeca | pice |
| djelo_vodice | PJENUŠAC DJEČJI JURASSIC W. GROŽĐE 0,75l | djeca | pice |
| djelo_vodice | PJENUŠAC DJEČJI MADAGASKAR JABUKA 0,75L | djeca | pice |
| djelo_vodice | PJENUŠAC DJEČJI SPUŽVA BOB BANANA 0,75L | djeca | pice |
| djelo_vodice | PJENUŠAC DJEČJI ŠTRUMPFOVI 0,75L ŠUMSKO VOĆE | djeca | pice |
| djelo_vodice | ŠAMPANJAC VIŠNJA 0,75L YIPPY | djeca | pice |
| djelo_vodice | ŠAMPANJAC ŠUMSKO VOĆE 0,75L YIPPY | djeca | pice |
