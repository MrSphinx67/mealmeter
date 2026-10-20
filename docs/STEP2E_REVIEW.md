# Pregled Koraka 2E (arhiva 2026-10-20)

Generira `scripts/step2e_review.py` nad izgrađenom bazom; sažetak je u REVIEW_2E.md.

## 1. Pripadnost grupe: tri razine

m = udio lanaca čiji naziv prolazi `must_match` bez `must_not_match`, x = udio lanaca čiji naziv pogađa `must_not_match`. **Snažni** član: m > 50 % i x < 10 %. **Slabi** (`match_quality = 'weak'`): x = 0, m ≥ 25 %, jedinica spojiva, barem jedan proizvod unutar min/max pakiranja i medijan cijene po jedinici u granicama; u zadanom je izboru, ali ispod snažnih i označen (`find_products.match_quality`, u košarici zastavica `weak_match`). Inače `ambiguous` (m > 0) ili `excluded` (m = 0).

Prema pravilu iz 2D: 33 grupa prelazi iz člana u `ambiguous`, 0 u `excluded`, a 550 postaje član.

| namirnica | snažnih | slabih | dvosmislenih | isključenih |
|---|---|---|---|---|
| banana | 60 | 0 | 3 | 47 |
| brasno | 434 | 2 | 15 | 102 |
| cesnjak | 57 | 0 | 3 | 19 |
| cokolada_za_kuhanje | 35 | 21 | 1 | 0 |
| dodatak_jelima | 94 | 14 | 68 | 46 |
| endivija | 24 | 0 | 0 | 5 |
| gljive | 111 | 0 | 3 | 8 |
| grah | 406 | 2 | 19 | 180 |
| grasak | 154 | 2 | 8 | 102 |
| griz | 31 | 6 | 5 | 34 |
| jabuka | 389 | 4 | 0 | 47 |
| jaja | 353 | 0 | 26 | 1092 |
| jogurt | 481 | 42 | 120 | 327 |
| junetina | 283 | 4 | 2 | 38 |
| kakao | 46 | 0 | 6 | 67 |
| kecap | 171 | 5 | 8 | 34 |
| kiseli_kupus | 127 | 4 | 6 | 5 |
| kiselo_vrhnje | 131 | 3 | 5 | 16 |
| koncentrat_rajcice | 45 | 4 | 0 | 0 |
| krastavac | 67 | 5 | 13 | 74 |
| krumpir | 236 | 2 | 1 | 208 |
| krusne_mrvice | 127 | 0 | 2 | 18 |
| kukuruz | 167 | 4 | 10 | 132 |
| kupus | 117 | 0 | 0 | 23 |
| kvasac | 60 | 0 | 0 | 1 |
| leca | 133 | 0 | 1 | 148 |
| limun | 96 | 0 | 2 | 33 |
| luk | 206 | 0 | 7 | 33 |
| majoneza | 180 | 6 | 14 | 8 |
| margarin | 96 | 8 | 1 | 1 |
| maslac | 249 | 7 | 26 | 354 |
| maslinovo_ulje | 355 | 11 | 20 | 75 |
| matovilac | 21 | 0 | 0 | 6 |
| med | 406 | 27 | 55 | 364 |
| mlijeko | 305 | 5 | 100 | 900 |
| mljevena_paprika | 100 | 13 | 10 | 10 |
| mljeveno_meso | 102 | 3 | 4 | 0 |
| mozzarella | 225 | 4 | 8 | 46 |
| mrkva | 120 | 1 | 0 | 46 |
| naranca | 111 | 0 | 2 | 37 |
| ocat | 145 | 3 | 20 | 195 |
| palenta | 80 | 6 | 1 | 0 |
| papar | 270 | 2 | 15 | 166 |
| paprika | 241 | 0 | 13 | 140 |
| parmezan | 111 | 5 | 4 | 18 |
| pasirana_rajcica | 137 | 5 | 2 | 4 |
| persin | 61 | 0 | 1 | 6 |
| pileca_prsa | 269 | 6 | 18 | 125 |
| piletina | 593 | 12 | 13 | 285 |
| prasak_za_pecivo | 45 | 4 | 1 | 0 |
| radic | 45 | 0 | 0 | 7 |
| rajcica | 201 | 1 | 7 | 198 |
| rajcica_konzerva | 186 | 7 | 0 | 1 |
| riza | 476 | 5 | 44 | 290 |
| rukola | 17 | 0 | 0 | 4 |
| secer | 313 | 0 | 22 | 126 |
| senf | 135 | 1 | 7 | 9 |
| slanina | 704 | 4 | 8 | 73 |
| slanutak | 119 | 1 | 3 | 30 |
| slatko_vrhnje | 34 | 5 | 8 | 0 |
| sol | 226 | 0 | 40 | 398 |
| spinat | 112 | 0 | 0 | 14 |
| sunka | 907 | 13 | 7 | 196 |
| svinjetina | 474 | 4 | 1 | 90 |
| svjezi_sir | 149 | 12 | 24 | 57 |
| tikvica | 53 | 0 | 0 | 9 |
| tjestenina | 1821 | 68 | 68 | 560 |
| tuna | 470 | 0 | 43 | 219 |
| tvrdi_sir | 1129 | 70 | 64 | 33 |
| ulje | 251 | 2 | 29 | 1335 |
| vanilin_secer | 63 | 3 | 7 | 18 |
| vrhnje_za_kuhanje | 73 | 4 | 5 | 0 |
| zelena_salata | 71 | 1 | 0 | 2 |
| zobene_pahuljice | 69 | 3 | 3 | 17 |

Napomena: među slabim članovima ima krivih pogodaka kad drugi lanci proizvod zovu samo markom, a jedan naziv prolazi `must_match` (npr. „ČOKOLADA RIKI PŠENICA I MED“ kao med, „MINI CROASANI S MASLACEM“ kao maslac). Rangirani su ispod snažnih i označeni; točka 4 (kratice, `must_not_match`) dio njih uklanja.

30 slučajnih slabih članova:

| namirnica | grupa | m % | nazivi po lancu |
|---|---|---|---|
| tjestenina | 3859892804077 | 33,00 | jadranka_trgovina: TJESTENINA FIDELINI RAPSKI 400G ARBONI; lorenco: ARBONI RAPSKI FIDELINI 400g; djelo_vodice: RAPSKI FIDELINI 400G ARBONI |
| jogurt | 3850354018377 | 48,00 | jadranka_trgovina: JOGURT DUKATOS DIVINE SLANA KARAMELA150G; lorenco: DUKATOS DIVINE SLANA KARAMELA 150G; spar: JOG.DUKAT.DIVINE KARAMEL.150 g; boso: JOGUR DUKAT 150 g DUK.DIV.SL.KAR; dukat: DUKATOS DIVINE SLANA KARAMELA 150g; trgovina-krk: JOGURT DUKATOS DIVINE SLANA KARAMELA 150 gr; konzum: JOGURT DUKATOS DIVINE SLAN KAR 150g; studenac: DUKATOS DIVINE SLANA KARAMELA 150g; tommy: JOGURT SLANA KARAMELA 150 g DUKATOS; trgocentar: DUKATOS DIVINE SLANA KARAMELA 150G (X); ribola: DUKATOS 150 g SL.KA. DIVINE; stridon: DUKATOS DIVINE SLANA KARAMELA 150 g DUKAT; vrutak: N-DUKAT JOGURT DUKATOS DIVINE150G SLANA KARAMELA -6/1- 13000; stanic: DUKATOS DIVINE SLANA KARAMELA 150 g DUKAT; branka: JOGURT DUKATOS DIVINE SLANA KARAMELA 150g; djelo_vodice: DUKATOS DIVINE SLANA KARAMELA 150G; kaufland: Dukatos Jogurt grčki sl.ka.6%mm 150g; ktc: DUKATOS DIVINE 150g KARAMELA; ntl: JOGURT DUKATOS DIVINE SLANA KARAMELA 150 g DUKAT; plodine: DUKATOS SLANA KARAMELA 150 G; gavranovic: JOGURT DUKATOS DIVINE 150g KARAMELA DUKAT |
| tjestenina | 8004350141156 | 50,00 | lorenco: TJEST.115 CANNELLONI 250g; konzum: TIJESTO CANNELLONI 115 250g ZARA; trgovina-krk: CANELONI PASTA 250 g; ribola: TJ.CANNELLONI 250 g BR.115 ULTRA |
| tjestenina | 3859888231023 | 50,00 | ntl: TJEST.FIDELINI SITNI 400 g CLARUM; kaufland: Clarum fidelini sitni 400 g |
| grasak | 3838977044508 | 25,00 | studenac: POLI GREEN MINI 220 g; kaufland: Poli Salama od graška Green 220g; ribola: POLI GREEN 220 g PER UTNINA; tommy: POLI GREEN MINI 220 g |
| tjestenina | 5060194790120 | 50,00 | plodine: SOBA NOODLES 300 G SAITAKU; ribola: REZANCI JAPAN 300 g SAITAKU SOBA; tommy: TJ.JAPANSKA SOBA NOOD. 300 g; konzum: SOBA NOODLES 300g SAITAKU |
| grasak | 8000627306938 | 33,00 | ntl: GRAŠAK M.BERGGOLLD 250G; plodine: SJEME GRAH MAHUNAR BERGGOLD; trgovina-krk: SJEME GRAH MAHUNAR BERGOLD 250 g MARCON |
| sunka | 3850159128929 | 45,00 | boso: DELUXE 100 g ISTRANKA; djelo_vodice: DELUXE ISTRANKA 100g; branka: SALAMA ISTRANKA DELUXE 100g; jadranka_trgovina: ŠUNKA PUREĆA DELUXE ISTRANKA 100G; ribola: SAL.DEL.ISTR.100 g V INDIJA; tommy: ŠUNKA PUREĆA ISTRANKA 100 G; konzum: ŠUNKA PUREĆA ISTRANKA NAR 100g; plodine: PURECA SUNKA ISTRANKA 100 G VINDON VINDIJA; vrutak: N-VIN PUREĆA DE LUX ŠUNKA ISTRANKA 100G -12/1-; trgovina-krk: DELUX ISTRANKA 100 gr; ktc: PUREĆA DELUXE ISTRANKA 100g VINDIJA |
| kecap | 3856020275730 | 30,00 | tommy: KETCHUP LJUTI PAPRIKA 310 g PODR; plodine: KETCHUP LJUTI 310 G ZIK ZAK PODRAVKA; spar: KETC.ZIK ZAK PODR.LJUTI 310 g; jadranka_trgovina: UMAK ZIK ZAK LJUTI 310G PODRAVKA; roto: ZIK ZAK LJUTI 310G PODRAVKA (6); studenac: KETCHUP ZIK ZAK LJUTI 310g; kaufland: Zik Zak Umak od paprike ljuti 310g vg.; ktc: ZIK ZAK LJUTI 310g PODRAVKA; lidl: ZIK ZAK paprika ljuti umak; konzum: UMAK ZIK ZAK LJUTI 310 g PODRAVKA |
| jogurt | 3850108032666 | 25,00 | trgocentar: FORTIA VIŠNJA 330G TTOP; lorenco: FORTIA VIŠNJA 300g TTOP; ribola: JOG.330 g VIŠ.TT FOR TIA; stridon: FORTIA VIŠNJA 330 gr TTOP VINDIJA |
| cokolada_za_kuhanje | 3877000595778 | 50,00 | tommy: ČOKOLADA ZA KUH.XXL 300 g LA BOMBA; ntl: ČOKOLADA ZA JELO I KUHANJE 300 g LA BOMBA; stridon: ČOKOLADA ZA JELO I KUHANJE 300 g LA BOMBA (10); boso: ČOKOL LA BOMBA 300 g JELO I KUH.; gavranovic: ČOKOLADA ZA KUHANJE 300g LA BOMBA; trgovina-krk: ČOKOLADA ZA KUHANJE 300 g LA BOMBA |
| mlijeko | 3850108021202 | 50,00 | stridon: MLIJEKO CA+ 1.6%MM 1 L VINDIJA; ribola: ML.TR.1,6% 1L KAL.VINDIJA |
| krumpir | 3859893072031 | 50,00 | metro: 10KG LIČKI KRUMPIR CRVENI; lorenco: LIČKI KRUMPIR 5/1 |
| jogurt | 3831051018563 | 50,00 | spar: JOG.GRČKI TIP 0% MYTHOS 400 g; ktc: MYTHOS GRČKI TIP 0%mm 400g |
| sunka | 3838885333022 | 50,00 | jadranka_trgovina: ŠUNKA SUHA KMEČKA 100G KRAS; trgovina-krk: PRŠUT KMEČKI NAREZAK 100 g KRAS |
| tjestenina | 3858894412037 | 50,00 | eurospin: BILJKA LJILJAN; trgovina-krk: LILIUM MIX FI 13 |
| maslac | 8719200265127 | 25,00 | stanic: RAMA NAMAZ BUTTERY 400 g; lidl: Rama Margarin SK1; plodine: RAMA CLASSIC S MASLACEM 400 G; ktc: RAMA NAMAZ BUTTERY 400g; spar: RAMA NAMAZ BUTTERY 400 g; kaufland: Rama Margarin buttery 400 g; lorenco: RAMA CLASSIC S MASLACEM 400G; jadranka_trgovina: MARGARIN RAMA NAMAZ BUTTERY 400G |
| tvrdi_sir | 3859889426459 | 33,00 | lorenco: SIR MEDITERANO PAŠKA SIRANA VP.1/4; plodine: SIR MEDITERANO 1/4 PASKA SIRANA; konzum: SIR TVRDI MEDITERANO VAC PAŠKA SIRAN |
| jabuka | 3859893211324 | 50,00 | metro: 6/1 JABUKA CRVENI DELIŠES KOM PD; plodine: BIO JABUKA CRVENA PODLOZAK |
| cokolada_za_kuhanje | 8606015718415 | 40,00 | kaufland: Dr.Oekter Čokolada mliječna 33% 150 g; ribola: ČOKO.MLIJEČNA 150 g DR.OETKER; trgovina-krk: ČOKOLADA ZA KUHANJE MLIJEČNA 150 g; konzum: ČOKO ZA KUH MILK 33% 150 g DR OETKER; spar: ČOKO.ZA KUHANJE MLIJEČNA 150 g; bure: ČOKOLADA 150 g MLIJEČNA; vrutak: N-ČOKOLADA ZA KUHANJE 150G MLIJEČNA -15/1-; plodine: COKOLADA ZA KUHANJE MLIJECNA 150 G DR.OETKER; tommy: ČOKOLADA ZA KUH. MLIJ. 150 g DR.OET; branka: \*NE\*ČOKOLADA MLIJEČNA 150g DR. OETKER |
| tjestenina | 3859888931053 | 38,00 | plodine: ISTARSKI PLJUKANCI 500 G MARIJA; lorenco: TJESTENINA PLJUKANCI "MARIJA"; stanic: PLJUKANCI 500 g SMRZNUTI; metro: 500G MARIJA ISTARSKI PLJUK SM; jadranka_trgovina: TJESTENINA PLJUKANCI ISTARSKI DS 500G MARIJA; konzum: PLJUKANCI 500 g MARIJA TJESTENINE; spar: TJES.MARIJA PLJUKANCI 500 g; trgovina-krk: PLJUKANCI 500 gr SMRZNUTO |
| tjestenina | 3859888666047 | 50,00 | trgovina-krk: TJES.MARODI KRPICE SREDNJE 400 g; gavranovic: TJ.MARODI 400g KRPICE SREDNJE; konzum: TIJESTO KRPICE SREDNJE 400g MARODI; metro: 400G MARODI MAFAL COR BEZ JAJA; vrutak: TJEST MARODI MAFALDINE CORTE/KRPICE SREDNJE 400G -10/1-; roto: TIJESTO KRPICE SREDNJE 400g MARODI (10); bure: TJ.SREDNJE KRPICE 400 g MAFALDINE; stridon: MAFALDINE CORTE (SREDNJE KRPICE) MARODI 400 g (10); jadranka_trgovina: TJESTENINA MAFALDINE CORTE 400G MARODI; ribola: TJ.MAFALD.CORT.400 g MARODI; kaufland: Marodi srednje krpice 400 g; ktc: MAFALDINE CORTE 400g MARODI; branka: TJESTENINA KRPICE SREDNJE/MAFALDINE CORTE 400g; ntl: TJESTENINA MAFALDINE CORTE 400g MARODI |
| tvrdi_sir | 8003518100622 | 50,00 | konzum: SIR TVRDI GP TWIST&GRATE 150 g; lorenco: GRANA PADANO GIRA i GRATTA 150g |
| tvrdi_sir | 3858891770208 | 25,00 | plodine: SIR S MASLINAMA 125 G SIRANA GLIGORA; vrutak: SIR S MASLINAMA 125G GLIGORA POLUTVRDI KRAVLJI -12/1; lorenco: SIR S MASLINAMA 125g GLIGORA; spar: SIR S MASLINAMA GLIGORA 125 g |
| tvrdi_sir | 3858891773889 | 25,00 | trgovina-krk: SIR LIBURJAN 190 gr; tommy: SIR LIBURJAN 190 g GLIGORA; vrutak: SIR LIBURJAN GLIGORA 190G -8/1-; jadranka_trgovina: SIR TVRDI LIBURJAN VAC. 190G SIRANA GLIGORA |
| tjestenina | 3858887101856 | 50,00 | konzum: KRUPICA DURUM ZA TJEST 1 kg FARINA; kaufland: Farina Speciale Krupica durum 1 kg |
| svjezi_sir | 3859893220067 | 33,00 | lorenco: SKUTA KRAVLJA 250g MILS; konzum: SIR SVJ KRAVLJA SKUTA 250g DALMAT SIR; ribola: SKUTA KRAV.250g DALM; studenac: SKUTA KRAVLJA DALMAT.SIREVI 250 g; tommy: SIR SVJ.SKUTA KRAVLJA 250 g; spar: SKUTA KRAVLJA MILS 250 g |
| med | 8594071650308 | 50,00 | konzum: MEDENE KUGLICE KAKAO 235g MARLENKA; spar: KUGLICE OD MEDA S KAKAOM 235g |
| mrkva | 3859893211331 | 33,00 | metro: 6/1 JABUKA CRIPS PINK KOM PD; plodine: MRKVA 500 G; spar: KUKURUZ ŠEĆERAC 3/1 |
| tvrdi_sir | 3858881190757 | 33,00 | plodine: SIR ISTARSKI KRAVLJI CCA 1,7 KG AGROLAGUNA; spar: Sir kravlji Špin; konzum: SIR TVRDI KRAVLJI ŠPIN |

30 grupa koje prelaze iz člana (2D) u `ambiguous`:

| namirnica | grupa | m % | x % | nazivi po lancu |
|---|---|---|---|---|
| majoneza | 3856015304339 | 86,00 | 14,00 | konzum: MAJONEZA ČILI 165g ZVIJEZDA; trgocentar: MAJONEZA CHILI 165G TUBA (12) ZVIJEZDA; stridon: MAJONEZA ČILI TUBA 165 g (12) ZVIJEZDA; branka: MAJONEZA ČILI 165g; lorenco: ZVIJEZDA ČILI MAJONEZA 165g; roto: MAJONEZA ČILI 165G ZVIJEZDA (12); trgovina-krk: MAJONEZA ČILI 165 g ZVIJ; jadranka_trgovina: MAJONEZA 165G ČILI TUBA ZVIJEZDA; ktc: MAJONEZA TUBA ČILI 165g ZVIJEZDA; gavranovic: MAJONEZA CHILLI 165g ZVIJEZDA; kaufland: Zvijezda čili majoneza tuba 165g; studenac: MAJONEZA ZV. 165G ČILI TUBA; vrutak: N-MAJONEZA ZVIJEZDA 165G -12/1 ČILI TUBA; plodine: MAJONEZA CILI 165 G TUBA ZVIJEZDA |
| zobene_pahuljice | 8595054907761 | 67,00 | 25,00 | gavranovic: ZOBENE PAHULJICE DOBRE BERRIES 300g; ntl: PAHULJICE ZOBENE BERRIES 300 g DOBRE; plodine: ZOBENE PAHULJICE SUMSKO VOCE 300 G BIOPLOD; ribola: PAHULJ.ZO.BO.300 g D OBRE PAHULJICE; branka: PAHULJICE ZOBENE BERRIES 300g; vrutak: ZOBENE PAHULJICE 300G BERRIES; lorenco: DOBRE ZOBENE PAHULJICE 300g BERRIES; konzum: PAHULJICE ZOBENE BERRIES 300g; spar: DOBRE ZOBENE PAH.BOB.VOĆ.300 g; kaufland: Dobre Pahuljice zobene bobič.voće 300g; tommy: ZOBENE PAH. ŠUM.VOĆE 300 g DOB; zabac: Dobre zobene pahuljice 300g BERRIES |
| sol | 3870009000144 | 80,00 | 20,00 | plodine: SOL KUHINJSKA JODIRANA 250 G TULJAK TUZLA; vrutak: SOL KAMENA 250G SOLJENKA -15/1- TUZLA; kaufland: Tuzla kuhinjska sol jodirana 250g; spar: SOL KUHINJ. TUZLA SITNA 250 g; ktc: SOL KAMENA DOZA 250g TUZLA |
| tjestenina | 8710605028430 | 71,00 | 29,00 | vrutak: TJESTENINA GO-TAN 250G EGG WOK NOODLES -8/1-; kaufland: Go Tan tjest.s jajima za Wok 250 g; konzum: TJESTENINA S JAJIMA GNIJEZDA GO TAN 250g; ribola: TJEST.GO TAN 250g; plodine: TJESTENINA S JAJIMA GNIJEZDA 250 G NOODLES GO TAN; ntl: TJESTENINA OD PŠ. BRAŠNA S JAJIMA 250G NIKAS; spar: TJESTENINA GOTAN NEST 250 g |
| sol | 3856020222314 | 80,00 | 20,00 | tommy: VEGETA MAESTRO MORSKA SOL GRUBO MLJEVENA 100G; spar: ZAČ.SOL MORSKA VEG.MAES.100 g; plodine: MORSKA SOL MLINAC 100 G VEGETA MAESTRO; ktc: MORSKA SOL GRUBO MLJEVENA 100g PODRAVKA; stridon: VEGETA MAESTRO MORSKA SOL M.100 G (6) PODRAVKA; bure: SOL MORSKA 100 g KRUNA PODR.; djelo_vodice: MORSKA SOL GRUBO MLJEVENA VEGETA MAESTRO BOČICA 100G; konzum: ZAČIN SOL MORSKA ML 100g VEGETA MAESTRO; lorenco: VEGETA MAESTRO MORSKA SOL 100G; ribola: SOL MORSKA 100 g VE GETA MAESTRO |
| piletina | 3850159142321 | 77,00 | 15,00 | branka: KRILCA BUCKET CEKIN 500g; plodine: CEKIN KRILCA BUCKET 500 G; jadranka_trgovina: KRILCA BUCKET CEKIN 500G VINDIJA; kaufland: Cekin Pečena pileća krilca 500 g; boso: KRILCA CEKIN 500 g BUCKET; ktc: CEKIN KIDS BUCKET KRILCA 500g; ntl: KRILCA PILEĆA PEČENA SM 500 g CEKIN; trgocentar: CEKIN KRILCA BUCKET 500G; spar: PILE.KRILCA BUCKET CEKIN 500 g; vrutak: N-VIN KRILCA BUCKET 500G -4/1-; ribola: PIL.KRIL.BUCK. 500 gVINDIJA; trgovina-krk: CEKIN KRILCA BUCKET 500G; stridon: CEKIN KRILCA BUCKET 500 g 14232 VINDIJA |
| pileca_prsa | 3850159125034 | 78,00 | 17,00 | gavranovic: PILEĆA PRSA U OVITKU 500g CEKIN (12503); studenac: PILEĆA PRSA U OVITKU 500g; trgocentar: PILEĆA PRSA U OVITKU 500G; ntl: SALAMA PILEĆA PRSA U OVITKU 500 g KOKA; tommy: PILEĆA PRSA U OVIT.500 g VI; spar: PIL.PRSA U OVITKU VIN. 500 g; bure: PILEĆA PRSA OV.500 gCEKIN LOT:1726102801; metro: 500GR CEKIN PIL PRSA U OVITKU; trgovina-krk: SALAMA PILEĆA PRSA U OVITKU 500 g VINDIJA; boso: PILEĆ KOKA 500 g PRSA U OVITKU; branka: SALAMA PILEĆA PRSA 500g; konzum: PRSA PILEĆA U OVITKU 500g VINDIJA; lorenco: PILEĆA PRSA 500g CEKIN; plodine: PILECA PRSA U OVITKU 500 G CEKIN (12503) VINDIJA; vrutak: N-VIN PIL.PRSA U OVITKU 500G-12/1- 12503; ktc: PILEĆA PRSA U OVITKU 500g KOKA; kaufland: Cekin Pileća prsa u ovitku 500g; stridon: PILEĆA PRSA U OVITKU 500 g VINDIJA 12503 |
| senf | 5949040202058 | 61,00 | 22,00 | boso: KREKE ELEPHANT 70 g MED SENF LUK; jadranka_trgovina: GRICKALICE ELEPHANT MED, SENF I LUK 70G; studenac: KREK. ELEPHANT SENFLUK 70 g; stanic: ELEPHANT PECIVO MED, SENF, LUK 70 g; kaufland: Elephant slano pecivo med senf i luk 70g; ntl: TRAJNO SLANO PECIVO ELEPHANT 70 g MED,SENF I LUK; djelo_vodice: ELEPHANT TRAJNO SLANO PECIVO - MED, SENF i LUK 70g; konzum: KREKER MED I SENF 70 g ELEPHANT; ktc: ELEPHANT MED,SENF I LUK 70g; lorenco: ALKA ELEPH.TS PECIVO 70g; plodine: SNACK MED/SENF/LUK 70 G ELEPHANT; spar: KRE.ELEPHANT SENF&MED&LUK 70 g; metro: 70G ELEPHANT FLAT MED SENF LUK; ribola: KREK.MED SEN.LU.70 g ELEPHANT; tommy: SNACK MED SENF LUK 70 g ELEPHA; branka: PECIVO ALKA ELEPHANT MED-SENF-LUK 70g; trgovina-krk: ELEPHANT TRAJNO SLANO PECIVO - MED,SENF I LUK 70 g; vrutak: ELEPHANT 70G TRAJNO SLANO PECIVO ALKA MED, SENF, LUK |
| med | 5949040205158 | 75,00 | 17,00 | konzum: KREKE TWIST SOL I MED 180 g ELEPHANT; metro: 180G ELEPHANT TWIST SOL I MED; djelo_vodice: ELEPHANT TWIST - MORSKA SOL i MED 180G; kaufland: Elephant Pecivo sl.morska sol,med180 g; ktc: ELEPHANT TWIST MORSKA SOL I MED 180g; gavranovic: PECIVO TWIST MORSKA SOL I MED 180g - ELEPHANT; tommy: SNACK SOL MED 180 g ELEPHANT; ribola: KREK.M.SOL&MED 180 g ELEPHANT; ntl: TRAJNO PEC. ELEP.TWIST - MORSKA SOL I MED 180g; plodine: KREKER MORSKA SOL I MED 180 G ELEPHANT; stanic: ELEPHANT TWIST - MORSKA SOL I MED 180 g; spar: PECIV.ELEP.TWIST SOL-MED 180 g |
| med | 5900617037152 | 86,00 | 14,00 | konzum: MUESLI GRANOLA ORAŠ PLOD MED 300g SANTE; ribola: GRANOLA 300 g ORAH/ MED SANTE; plodine: MUESLI GRANOLA MED I ORASASTI PLODOVI 300 G SANTE; tommy: MUESLI GRAN. NUT/MED 300 g SAN; spar: GRAN.SANTE ORAŠ.PLOD.MED 300 g; jadranka_trgovina: ŽITARICE GRANOLA GOLD ORASI+MED 300G SANTE; kaufland: Sante Granola Gold med i oraš.plod.300g |
| med | 4000521010294 | 63,00 | 31,00 | studenac: MUESLI MED BADEM VITALIS 300 g; plodine: MUSLI PLUS MED BADEM 300 G CRUNCHY DR OETKER; djelo_vodice: MUSLI CRUNCHY MED BADEM 300g; konzum: MUESLI KNUSPER MED BADEM 300g VITALI; lorenco: DR.OETKER CRUNCHY PLUS MED BADEM; vrutak: MUSLI DR OETKER 300G MED I BADEM CRUNCHY PLUS -8/1-; spar: MUSLI VITALIS MED,BADEM 300 g; tommy: MUESLI CRUN.PL. MED 300 g DR.O; jadranka_trgovina: MUESLI CRUNCHY PLUS MED BADEM 300G VITALIS; roto: MUESLI KNUSPER MED BADEM 300G VITALI (8); trgovina-krk: MUSLI CRUNCHY PLUS MED BADEM 300 g DR OETKER; bure: MUESLI VITALIS 300 gHONEY-ALMOND; trgocentar: VITALIS CRUNCHY PLUS MED BADEM 300G, DR.OETKER; ribola: MUESLI CHR.MED 300 g VITALIS DR OETKER; kaufland: Dr.Oetker vitalis crunchy med badem 300g; metro: 300G VITALIS CRUN PLUS MED/BAD |
| papar | 9001414274057 | 80,00 | 20,00 | ntl: ZAČIN ZA KOKTELE SPICES & DRINKS PAPAR CRNI 50 g KOTANYI; plodine: SPICES DRINKS PAPAR CRNI, ZRNO 50 G; kaufland: Kotany papar crni zrno, bočica 50 g; lorenco: PAPAR CRNI ZRNO SiD STAKLO 100ML; spar: ZAČ. PAPAR S&D CRNI ZRNO 50 g |
| kukuruz | 3859893512254 | 70,00 | 30,00 | jadranka_trgovina: KUKURUZ PEČENI SLANI BBQ 60G; lorenco: KUKURUZ PEČENI SALNI BBQ 60g S.SNAC; studenac: KUKURUZ PEČ.SL. NATURA 60 g; spar: KUKURUZ PEČ.SLANI NATURA 60 g; trgocentar: KUKURUZ PEČENI SLANI 60G BBQ SUPER SNACK; trgovina-krk: KUKURUZ PS BBQ NATURA 60 g; vrutak: N-KUKURUZ NATURA 60G PEČENI SLANI BBQ -20/1- SUPER SNACK; ribola: KUKURUZ PEČENI 60 g SLANI NATURA; gavranovic: KUKURUZ PEČENI SLANI BBQ 60g NATURA; plodine: KUKURUZ PECENI SLANI BBQ 60 G SUPER SNACK NATURA |
| papar | 9001414440834 | 86,00 | 14,00 | ntl: ZAČIN ZA KOKTELE SPICES & DRINKS PAPAR CRVENI 25 g KOTANYI; plodine: SPICES DRINKS PAPAR CRVENI ZRNO 25 G; konzum: PAPAR CRVENI ZRNO S&D 25g KONTAYI; vrutak: KOTANYI KOKTEL PAPAR CRVENI SPICE i DRINKS 25G ZRNO; gavranovic: KOTANYI PAPAR CRVENI ZRNO 25g SPICE DRINKS; lorenco: PAPAR CRVENI ZRNO KOKTEL SND ST 100; spar: ZAČIN PAPAR CRVENI ZRNO 25 g |
| tuna | 8004030860025 | 0,00 | 86,00 | spar: TUNA SAL.RIO MARE COUS 2X160 g; tommy: TUNA SALATA CUS CUS 2X160 G RIO MARE; lorenco: TUNA -COUS-COUS SAL.2\*160g BOWL.; metro: 160GX2 RIO MARE INSALA.CUS CUS; plodine: TUNA COUS-COUS SAL.2X160G BOWL; kaufland: Rio Mare Insal.sal.tuna cous cous2x160g; konzum: TUNJ SALATA COUS COUS 2X160g RIO MARE |
| piletina | 3850159113154 | 60,00 | 20,00 | plodine: GAVELINO PILE ZA PECENJE CEKIN (11315); ribola: GAVELINO VINDIJA; studenac: PILE GAVELINO VINDIJA KOKA kg; konzum: PILE GAVELINO POD VINDIJA; spar: PILE GAVELINO |
| senf | 5949040204953 | 60,00 | 10,00 | ribola: PERECI ME.SE.LU.75 g ELEPHANT; gavranovic: PECIVO KOMADIĆI MED,SENF I LUK 75g ELEPHANT; ntl: TRAJNO SLANO PECIVO ELEPHANT PRETZEL 75 g MED, SENF I LUK; kaufland: Elephant Komadići med,senf i luk75g; konzum: PER LOMLJ MED SENF LUK 75 g ELEPHANT; ktc: ELEPHANT KOMADIĆI MED,SENF I LUK 75g; boso: KREKE ELEPHANT 75 g MED SENF LUK; tommy: SNACK MED SENF LUK 75 g ELEPHA; plodine: PEREC KOMADICI S OKUSOM MEDA,SENFA I LUKA 75 G ELEPHANT; stridon: ALKA ELEPHANT TS PECIVO-KOMAD.S OKUS.MEDA 14\*75 g |
| pileca_prsa | 3856020257064 | 57,00 | 14,00 | plodine: LINO PILECA PRSA 60 G PODRAVKA; ribola: ŠUNKA PILEĆA 60 g LINO PODRAVKA; ktc: PILEĆA PRSA 60g LINO; konzum: LINO PILEĆA PRSA 60 g; stridon: LINO PILEĆA ŠUNKA 60 g (10) PODRAVKA; tommy: PILEĆA PRSA 60 G LINO NARESCI PODRAVKA; spar: PILEĆA PRSA LINO NJUPAL. 60 g |
| majoneza | 3856015324689 | 81,00 | 14,00 | kaufland: Zvijezda majoneza čili 85 g; trgocentar: MAJONEZA ČILI 85G ,ZVIJEZDA; ribola: MAJONEZA ČILI 85 g ZVIJEZDA; spar: MAJONEZA CHILI ZVIJEZDA 85 g; zabac: CHILI MAJONEZA 75% 85 G; stridon: MAJONEZA ČILI ZVIJEZDA 85 g (25); boso: MAJON ZVIJE 85 g DELIK.ČILI; jadranka_trgovina: MAJONEZA 85G ČILI VREĆICA ZVIJEZDA; konzum: MAJONEZA ČILI PVC 85g ZVIJEZDA; trgovina-krk: MAJONEZA ČILI 85G; lorenco: ZVIJEZDA MAJONEZA ČILI 85G; metro: 85G ZVIJEZDA MAJONEZA ČILI; roto: MAJONEZA ČILI PVC 85g ZVIJEZDA (25); ktc: MAJONEZA ČILI 85g ZVIJEZDA; lidl: Zvijezda Majoneza Čili; tommy: MAJONEZA ČILI 85 G ZVIJEZDA; vrutak: N-MAJONEZA ZVIJEZDA 85G -25/1 ČILI; branka: MAJONEZA ČILI 85g; djelo_vodice: ČILI MAJONEZA 85g; gavranovic: MAJONEZA CHILLI VREĆICA 85g ZVIJEZDA; studenac: MAJONEZA ČILI 85g ZVIJ. |
| papar | 9001414050026 | 54,00 | 46,00 | tommy: ZAČIN PAPAR ZEL/SAL. 100 g KOT; djelo_vodice: PAPAR ZEL.SALAMURA; trgocentar: KOTANY ZELENI PAPAR U ZRNU 100G; spar: ZAČ.PAPAR ZELEN.KOTANYI 100 g; lorenco: ZELENI PAPAR 100 g KOTANYI; metro: 100G KOTANYI PAPAR ZELENI U SA; vrutak: KOTANYI 100G PAPAR ZELENI USALAMURI -24/1-; roto: PAPAR ZELENI U SALAMURI 100g KOTANYI (24); gavranovic: KOTANYI PAPAR ZEL.U SALAMURI 100g; studenac: ZAČIN PAPAR ZELENI U SALAMURI 100 g KO; bure: PAPAR ZELENI 100 g SALAMURA UG.; trgovina-krk: PAPAR ZELENI U SALAMURI 100 g KOTAN; ribola: PAPAR ZEL.SAL. 100 g KOTANYI |
| dodatak_jelima | 3856020228910 | 90,00 | 10,00 | konzum: ZAČIN BURGER CLASSIC VR 30g VEGETA NATUR; lorenco: VEGETA NATUR BURGER CLASSIC VR.30g; plodine: VEGETA NATUR BURGER 30 G CLASSIC; tommy: VEGETA NATUR BURGER VR.30 g PO; stridon: VEGETA NATUR BURGER CLASSIC 30 g (18); kaufland: Vegeta Natur Grill Burger classic 30 g; bure: VEGETA VR.BURG. 30 gCLASSIC; trgovina-krk: VEGETA NATUR BURGER CLASSIC 30 g VREĆICA POD; spar: ZAČIN VEGETA NATUR BURGER 30 g; trgocentar: VEGETA NATUR BURGER CLASSIC VR.30G (18) (PAL 252) PODRAVKA |
| sol | 3856020267216 | 83,00 | 17,00 | tommy: VEGETA MAESTRO SITNA MORSKA SOL POSIPAČ 110 g; plodine: VEGETA MAESTRO SITNA MORSKA SOL POSIPAC 110 G BOCICA; lorenco: VEGETA MAESTRO SITNA MORSKA SOL; bure: VEGETA MAESTRO 110g SITNA SOL; konzum: SOL SITNA MORSKA 110g VEGETA MAESTRO; spar: ZAČ.V.MAEST.SITNA MOR.SOL 110g |
| tjestenina | 8008857300771 | 83,00 | 17,00 | jadranka_trgovina: TJESTENINA SPAGHETTI TAGLIATI 077 500G REGGIA; trgocentar: SPAGETTI TAGLIATI 77 (SITNI REZANCI) 500G PASTA REGGIA (24); bure: TJ.FIDELINI 77 500 gREGGIA (SPAGET.TAGLI; ribola: TJ.SPAGHETTI 500 g TAGLIATI JUHA REGGIA; ntl: TJESTENINA TAGLAITI 500g REGGIA; trgovina-krk: TJEST. TAGLIATI 500 g REGGIA NTL |
| med | 5949040203482 | 70,00 | 20,00 | tommy: SNACK SOL MED 160 g ELEPHANT; ribola: KREK.M.SOL&MED 160 g ELEPHANT; stanic: ELEPHANT TWIST - MORSKA SOL I MED 160 g; djelo_vodice: ELEPHANT TWIST - MORSKA SOL i MED 160g; lorenco: ALKA ELEPHANT TWIST-SOL I MED 160g; ntl: TRAJNO PEC. ELEP.TWIST - MORSKA SOL I MED 160g; metro: 160G ELEPHANT TWIST SOL I MED; gavranovic: PECIVO TWIST MORSKA SOL I MED 160g - ELEPHANT; kaufland: Elephant Twist sl.pecivo m.sol i med160g; plodine: SNACK MORSKA SOL I MED 160 G ELEPHANT TWIST |
| papar | 9001414040867 | 60,00 | 10,00 | vrutak: KOTANYI 40G PAPAR ŠARENAMJEŠAVINA STAKLO -4/1-; gavranovic: KOTANYI PAPAR MJEŠAVINA STAKLO 40g; plodine: PAPAR MIX 40 G STAKLO KOTANYI; trgovina-krk: ZAČIN MJEŠAVINA PAPRA STAKLO 40 g KOTANY; bure: ZAČIN MJEŠ.PAPRA 100g; lorenco: ZAČIN MJEŠ. PAPRA 35 g KOTANYI; studenac: ZAČIN PAPAR ŠARENI 40 g KOT.; tommy: ZAČIN PAPAR MJEŠ.40 g KOTANY; spar: ZAČ.PAPAR MJEŠ.KOTANYI 40 g; branka: \*NE\*PAPAR MJEŠAVINA 35G STAKLO KOTANYI |
| sol | 9001414040034 | 69,00 | 31,00 | djelo_vodice: HIMALAJSKA SOL 100ML; bure: SOL HIMALAJSKA 100 ml STAKLO; plodine: HIMALAJSKA SOL 120 G KOTANY BOCICA; ribola: SOL HIMALAJSKA 120 g STAKLO KOTANYI; branka: SOL HIMALAJSKA BOČICA 120g; trgovina-krk: ZAČIN SOL HIMALAJSKA BOČICA KOTA; konzum: HIMALAJSKA SOL BOČ 120G KOTANYI; ktc: SOL HIMALAJSKA 100mL ST KOTANYI; lorenco: HIMALAJSKA SOL JODIRANA STAKLO 100; tommy: SOL HIMALAJSKA STAK. 120 g KOT; studenac: ZAČIN HIMALAJSKA SOL 120 g KOT.; kaufland: Kotanyi himalajska sol 120 g bočica; spar: SOL HIMALAJ.SITNA KOTANY120 g |
| jaja | 5200701000063 | 67,00 | 17,00 | studenac: BOM. JAJE PEPA PIG 10 g; ribola: PEPPA PIG JAJE 10 g; konzum: JAJE S BOMBONIMA PEPA PIG 10g; ntl: JAJE IZNENAĐENJA 10 g MIX LICENCA; vrutak: SRCE PL. PEPPA PIG 10G; trgovina-krk: SRCE JAJE PEPPA PIG 10G |
| kiseli_kupus | 3859891493098 | 56,00 | 11,00 | konzum: KUPUS KISELI MIX ZA SARMU MADIG; gavranovic: ZELJE KISELO MIX ZA SARMU 1KG MADIG; eurospin: KUPUS KISELI MIX ZA SARMU 1kg; lorenco: MADIG MIX ZA SARMU 1000g; spar: KUPUS KIS.MIX ZA SARMU 1 kg; studenac: KIS. ZELJE MIX ZA SARMU 1100 g; tommy: KUPUS KIS. MIX ZA SARMU 1000 g; trgovina-krk: KUPUS KISELI MIX MADIG ZA SARMU 1 kg NTL; plodine: SARMA MIX 1 KG KISELI KUPUS MADIG |
| sol | 9001414046241 | 75,00 | 25,00 | bure: SOL SITNA 100ml STAKLO; konzum: MORSKA SOL BOČ 120 g KOTANYI; spar: MORSKA SOL KOTANY 120g; tommy: SOL MORSKA JODIRANA 120 g KOTAN; vrutak: KOTANYI 100ML MORSKA SOL SITNA STAKLO -4/1-; metro: 120G KOTANYI MORSKA SOL BOČICA; kaufland: Kotanyi Sol morska sitna jodirana 120g; plodine: MORSKA SOL 120 G BOCICA KOTANYI |
| pileca_prsa | 3850159123306 | 59,00 | 35,00 | ktc: PILEĆA PRSA 100g VINDIJA; spar: PILEĆA PRSA 100 g; plodine: PILECA PRSA 100 G VINDIJA; tommy: PILEĆA PRSA NARESCI 100 g; trgocentar: PILEĆA PRSA 100G, VINDIJA; jadranka_trgovina: SALAMA PILEĆA PRSA 100G CEKIN VINDIJA; kaufland: Cekin Pileća prsa 100 g; stridon: PILEĆA PRSA 100 g VINDIJA; gavranovic: CEKIN PILEĆA PRSA NAREZAK 100g; ntl: SALAMA PRSA PILEĆA 100 g VINDIVAC; studenac: PIL. PRSA U OVIT. 10 0g VINDVAC; trgovina-krk: SALAMA PILEĆA PRSA 100 g VIND; djelo_vodice: PILEĆA PRSA 100G VIN.; konzum: PRSA PILEĆA U OVITKU NAR 100g; lorenco: PILEĆA PRSA 100g; vrutak: VIN PILEĆA PRSA 100G; ribola: PIL.PRS.U OV.100 g VINDIJA |

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
| tjestenina | strong | tommy: TJ.FUSILI TROB.37 500 g ARRIGH |
| tjestenina | strong | trgovina-krk: LAZANJE 1 KOM TK |
| tjestenina | strong | konzum: RIŽINI REZANCI 225g MAMA |
| tvrdi_sir | strong | metro: CCA15KG HOLLAND EDAM |
| tvrdi_sir | strong | tommy: SIR CHEDDAR FRIENDSHIP |
| tvrdi_sir | strong | kaufland: KLC.Emmentaler rezani 150 g |
| jogurt | strong | plodine: JOG.JOGO MARELICA 1 KG PET DUKAT |
| slatko_vrhnje | strong | ribola: VRH.ZA ŠLAG ČOK.500gDUKAT |
| tjestenina | strong | plodine: TJESTENINA LASAGNA 500 G RISCOSSA |
| jogurt | strong | spar: JOG.GRČKI FF 0%M.M 150 g |
| tjestenina | strong | eurospin: REZANCI ZA JUHU S MRKV/JAJIMA 400g |
| tjestenina | strong | trgovina-krk: LAZANJE GASTRO TS |
| tjestenina | strong | tommy: TJ. RAJČICA MOZZARELLA U ČAŠI 70 g BERRUTO |
| jogurt | strong | spar: JOG.GRČ.TIP VIŠ./NAR. SB150 g |
| tjestenina | strong | bure: TJ.LAZANJE 500 g PALLANTE; vrutak: TJEST REGGIA 500G LASAGNE U-21132 12/1; trgovina-krk: TJEST. LASAGNE 500 g REGGIA NTL; jadranka_trgovina: TJESTENINA LASAGNE 205 500G REGGIA; trgocentar: LASAGNE 105 (LAZANJE) 500G PASTA REGGIA (12); ntl: TJESTENINA LASAGNE 500g REGGIA; ribola: TJ.LASAGNE 500 g REGGIA; djelo_vodice: LASAGNE REGGIA 500G |
| tvrdi_sir | strong | metro: 1KG MC RED CHEDDAR RIBANI |
| jogurt | strong | plodine: JOG. VOC. MIX 140 G DOLCE DUKAT |
| tjestenina | strong | plodine: FANTASY GUMICA I SILJILO SKOLJKA |
| tvrdi_sir | strong | kaufland: KLC.Sir Emmentaler ribani XXL 500 g |
| tvrdi_sir | strong | spar: Sir Emmentaler Illertaler |
| tvrdi_sir | strong | metro: 500G ARO EMMENTAL REZANI |
| tvrdi_sir | strong | kaufland: KLC.Sir Maasdam rezani 45% 300g |
| tjestenina | strong | kaufland: KFav.Tijesto za lasagne 250 g |
| tjestenina | strong | kaufland: Cetina Rezanci uski s jajima premium400g; tommy: TJ.USKI REZAN.S JAJ. 400 g CET |
| jogurt | weak | ktc: MYTHOS GRČKI TIP 0%mm 400g; spar: JOG.GRČKI TIP 0% MYTHOS 400 g |
| tjestenina | strong | tommy: TJ.B.G. KUK/ RIŽA 400 g COOP |
| tjestenina | strong | trgovina-krk: LJILJAN 37CM; ntl: LJILJAN 37 CM BIJELA/ROZA; gavranovic: LJILJAN 37 cm - BIJELA/ROZA |
| mlijeko | strong | metro: 30GX24 BARNI BISKVIT MLIJ.PUNJ |
| tvrdi_sir | strong | trgovina-krk: SIR EMMENTALER PUNOMASNI 300 g TO JE TO ZDENK |
| svinjetina | strong | metro: CCA2,5KG SV.REBRA ZA ROŠT ULMA |

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
| unknown → pice | 1 |
| unknown → ostalo | 1 |
| kozmetika → hrana | 1 |

Vraćeno u `hrana` s „cvijet“ u nazivu: **78**. 20 primjera:

| lanac | naziv | kategorija | prije |
|---|---|---|---|
| plodine | SOL CVIJETNA 125 G SOLANA PAG |  | unknown |
| bure | MED CVIJETNI 900 g PIP LOT:17.08.28 | HRANA | ostalo |
| branka | ČAJ LIPA CVIJET 100g | HRANA | ostalo |
| metro | 5KG MELBI MED CVIJETNI | hrana | ostalo |
| branka | ČAJ GLOG CVIJET I LIST 100g | HRANA | ostalo |
| branka | ČAJ BAZGA CVIJET 40g | HRANA | ostalo |
| jadranka_trgovina | ČAJ ŠIPAK S CVIJETOM HIBISKUSA 40X2,5G NATURAVITA | HRANA | ostalo |
| djelo_vodice | API MEL MED CVIJET 450G | MED CVJETNI | ostalo |
| konzum | SOL SOLNI CVIJET 150g SOLANA PAG | HRANA | ostalo |
| branka | ČAJ LAVANDA CVIJET 100g | HRANA | ostalo |
| spar | CVIJET SOL.ZELEN.PAP.BIO 125 g | Hrana | ostalo |
| metro | 1L TE VODA CVIJETA NARANČE | hrana | ostalo |
| lorenco | SOLNI CVIJET 150g |  | unknown |
| metro | NEVEN CVIJET - KOM | hrana | ostalo |
| bure | MED CVIJETNI 450 g PIP LOT:24.06.28 | HRANA | ostalo |
| djelo_vodice | SOLNI CVIJET 150G | SOL KRUPNA | ostalo |
| dm | dmBio čaj cvijet lipe 20x1,5 g 30 g | prehrana | ostalo |
| konzum | ČAJ BAZGA CVIJET 40G | HRANA | ostalo |
| trgovina-krk | UKRASNI CVJETIĆI | Hrana | kucanstvo |
| branka | DESERT KAMILA MINI CVIJET 120g | HRANA | ostalo |

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

## 9. Lijevak za svježe povrće

Broj proizvoda po fazi (svaka faza je podskup prethodne): kandidati (`must_match` na nazivu) → nakon kategorije (bez neprehrane i alkohola) → nakon pripadnosti (pravilo svježeg povrća i `must_not_match` po proizvodu, grupa `member`) → nakon zadano isključenih varijanti → nakon pakiranja (min/max, jedinica) → nakon `price_suspect` (barem jedna cijena u granicama) → nakon rasprodaje → konačno (filtar hrane kao u `plan_basket`: provjerena hrana ili nepoznata skupina za svježe povrće; bez veleprodaje). Ćelija je „kandidati → … → konačno“.

Zapažanje: „pripadnost“ su većinom prerađeni proizvodi (krekeri, sokovi, konzerve, tjestenina s mrkvom), ali pravilo za svježe povrće izbacuje i stvarno povrće koje se prodaje na komad uz globalni EAN („KRASTAVAC SALATAR kom“, Lidl „Salata Iceberg“), jer traži bez gramature ili ≥ 500 g.

### rajcica

| lanac | kandidati → kategorija → pripadnost → varijante → pakiranje → price_suspect → rasprodaja → konačno |
|---|---|
| konzum | 124 → 122 → 4 → 3 → 3 → 3 → 3 → 3 |
| spar | 102 → 102 → 11 → 7 → 7 → 7 → 7 → 7 |
| plodine | 264 → 261 → 17 → 13 → 13 → 13 → 13 → 13 |
| lidl | 55 → 55 → 10 → 4 → 4 → 4 → 4 → 4 |
| kaufland | 122 → 122 → 9 → 5 → 5 → 5 → 5 → 5 |
| tommy | 147 → 147 → 19 → 12 → 12 → 11 → 9 → 9 |
| studenac | 80 → 79 → 15 → 12 → 12 → 11 → 9 → 9 |
| eurospin | 37 → 37 → 5 → 4 → 4 → 4 → 4 → 4 |

Najčešći razlog gubitka: **pripadnost** (835 proizvoda; svi razlozi: pripadnost 835, varijante 30, kategorija 6, rasprodaja 4, price_suspect 2). Primjeri:

| lanac | naziv |
|---|---|
| tommy | UMAK RAJČICA SA SIROM ST. 400 g MUTTI |
| plodine | BOLSIUS CITRONELA 18/1 RAJCICA |
| konzum | RAJČICA POLPA BOSILJAK 400g MUTTI |
| spar | BIO RAJČICA SJECK.PODRAV.400 g |
| konzum | RAJČICA PASIRANA 500g PODRAVKA |
| tommy | RAJČICA OGULJ. SJEC.400 g PET |
| kaufland | Podravka Ćufte u umaku od rajčice 400g |
| kaufland | Cirio Rajčica sjeckana luk i češnj.390g |
| konzum | UMAK RAJČICA BOSILJ 330 g AGROMONTE |
| plodine | RAJCICA SJECKANA 690 G MUTTI |

### mrkva

| lanac | kandidati → kategorija → pripadnost → varijante → pakiranje → price_suspect → rasprodaja → konačno |
|---|---|
| konzum | 49 → 35 → 5 → 5 → 5 → 5 → 5 → 5 |
| spar | 37 → 34 → 4 → 4 → 4 → 4 → 4 → 4 |
| plodine | 89 → 61 → 5 → 5 → 5 → 5 → 5 → 5 |
| lidl | 15 → 12 → 5 → 5 → 5 → 4 → 4 → 4 |
| kaufland | 71 → 54 → 6 → 6 → 6 → 6 → 6 → 6 |
| tommy | 46 → 37 → 9 → 9 → 9 → 9 → 8 → 8 |
| studenac | 44 → 38 → 7 → 7 → 7 → 7 → 5 → 5 |
| eurospin | 11 → 11 → 4 → 4 → 4 → 4 → 4 → 4 |

Najčešći razlog gubitka: **pripadnost** (237 proizvoda; svi razlozi: pripadnost 237, kategorija 80, rasprodaja 3, price_suspect 1). Primjeri:

| lanac | naziv |
|---|---|
| plodine | KEKS LAN MRKVA BEZ SECERA 120 G FRANCK OLI |
| kaufland | KBio.Snack kukur.sa prosom i mrkvom30g |
| studenac | SOK VINDI A+C+E NARANČA MRKVA 0,5 l |
| kaufland | B.aktiv LGG jog jab.dinja mrkva 330g PET |
| plodine | BEBIVITA SOK MRKVA VOCE 500 ML |
| kaufland | KLC. Grašak-mrkva 1 kg |
| spar | FLIPS LINO MRKVA 35 g |
| plodine | RIBANA KASA S JAJIMA I MRKVOM 400 G |
| tommy | FRUTEK SOK MRKVA 125 ml |
| kaufland | Biotta bio sok od mrkve 500 ml |

### krastavac

| lanac | kandidati → kategorija → pripadnost → varijante → pakiranje → price_suspect → rasprodaja → konačno |
|---|---|
| konzum | 20 → 20 → 2 → 2 → 2 → 2 → 2 → 2 |
| spar | 36 → 36 → 7 → 7 → 7 → 7 → 7 → 7 |
| plodine | 66 → 59 → 6 → 6 → 6 → 6 → 6 → 6 |
| lidl | 15 → 15 → 4 → 4 → 4 → 4 → 4 → 4 |
| kaufland | 30 → 30 → 3 → 3 → 3 → 3 → 3 → 3 |
| tommy | 34 → 34 → 4 → 4 → 4 → 4 → 3 → 3 |
| studenac | 13 → 13 → 3 → 3 → 3 → 3 → 2 → 2 |
| eurospin | 7 → 7 → 3 → 3 → 3 → 3 → 3 → 3 |

Najčešći razlog gubitka: **pripadnost** (182 proizvoda; svi razlozi: pripadnost 182, kategorija 7, rasprodaja 2). Primjeri:

| lanac | naziv |
|---|---|
| lidl | Kiseli krastavci, ATG: 450g |
| spar | NAMAZ VITAL KRASTAVAC 135 g |
| kaufland | KLC.Krastavci kiseli 670g/360g_OC |
| studenac | SOK LIMUN KRASTAVAC TOCO 1,5 l |
| konzum | KRASTAVAC EXCLUSIVE 290g DOORA |
| tommy | KRASTAVCI KIS. 6-9cm 670 g T! |
| plodine | SOK TOCO LIMUN- KRASTAVAC 0,5 L |
| konzum | KRASTAVAC K PLUS I KL 350g |
| lidl | Zvijezda Krastavci del. (OM 350g) |
| lidl | Kiseli krastavci narezani |

### zelena_salata

| lanac | kandidati → kategorija → pripadnost → varijante → pakiranje → price_suspect → rasprodaja → konačno |
|---|---|
| konzum | 1 → 1 → 1 → 1 → 1 → 1 → 1 → 1 |
| spar | 2 → 2 → 1 → 1 → 1 → 1 → 1 → 1 |
| plodine | 5 → 4 → 2 → 2 → 2 → 2 → 2 → 2 |
| lidl | 2 → 2 → 1 → 1 → 1 → 1 → 1 → 1 |
| kaufland | 7 → 7 → 6 → 6 → 6 → 6 → 6 → 6 |
| tommy | 6 → 6 → 6 → 6 → 6 → 6 → 6 → 6 |
| studenac | 4 → 4 → 4 → 4 → 4 → 4 → 4 → 4 |
| eurospin | 7 → 7 → 6 → 6 → 6 → 6 → 6 → 6 |

Najčešći razlog gubitka: **pripadnost** (6 proizvoda; svi razlozi: pripadnost 6, kategorija 1). Primjeri:

| lanac | naziv |
|---|---|
| kaufland | Salata zelena rucola 125g |
| spar | Salata zelena sa sirom |
| plodine | SALATA ZELENA 100 G |
| eurospin | ZELENA SALATA 250g |
| lidl | Salata Iceberg |
| plodine | SALATA ZELENA BIO 100G |

### luk

| lanac | kandidati → kategorija → pripadnost → varijante → pakiranje → price_suspect → rasprodaja → konačno |
|---|---|
| konzum | 45 → 45 → 6 → 3 → 3 → 3 → 3 → 3 |
| spar | 45 → 44 → 12 → 4 → 4 → 4 → 4 → 4 |
| plodine | 66 → 63 → 15 → 9 → 9 → 9 → 9 → 9 |
| lidl | 17 → 17 → 12 → 7 → 7 → 7 → 7 → 7 |
| kaufland | 46 → 45 → 12 → 7 → 7 → 7 → 7 → 7 |
| tommy | 55 → 54 → 10 → 5 → 5 → 5 → 4 → 4 |
| studenac | 31 → 29 → 13 → 6 → 6 → 6 → 5 → 5 |
| eurospin | 17 → 17 → 9 → 2 → 2 → 2 → 2 → 2 |

Najčešći razlog gubitka: **pripadnost** (225 proizvoda; svi razlozi: pripadnost 225, varijante 46, kategorija 8, rasprodaja 2). Primjeri:

| lanac | naziv |
|---|---|
| studenac | ČIPS LETS PARTY TUBA VRHNJE I LUK 100 g |
| tommy | KIKIRIKI LUK/ VRHNJE 60 g MOGY |
| plodine | KREKER LUK 100 G TUC |
| spar | FLIPS BOBI RINGS VRH.-LUK 70 g |
| kaufland | Polleosport Protein chips vrhnje luk 50g |
| plodine | GO-TAN PRZENI LUK 100 G |
| plodine | KIKIRIKI U HRSKAVOM OMOTACU LUK I VRHNJE 150 G BITS BYTES |
| konzum | LUK KANDIRANI ROUGIE STAKL 115g MIVA |
| spar | PAŠ.S LUK. I BUČ.SJ.150 g |
| plodine | HEREVIN POSUDA ZA KRUMPIR I LUK ZELENA |

### paprika

| lanac | kandidati → kategorija → pripadnost → varijante → pakiranje → price_suspect → rasprodaja → konačno |
|---|---|
| konzum | 138 → 138 → 8 → 8 → 8 → 8 → 8 → 8 |
| spar | 125 → 125 → 11 → 11 → 11 → 11 → 11 → 11 |
| plodine | 227 → 225 → 18 → 18 → 18 → 17 → 17 → 17 |
| lidl | 48 → 48 → 9 → 9 → 9 → 9 → 9 → 9 |
| kaufland | 147 → 147 → 8 → 8 → 8 → 8 → 8 → 8 |
| tommy | 137 → 137 → 16 → 16 → 16 → 16 → 11 → 11 |
| studenac | 87 → 87 → 14 → 14 → 14 → 14 → 8 → 8 |
| eurospin | 34 → 34 → 5 → 5 → 5 → 5 → 5 → 5 |

Najčešći razlog gubitka: **pripadnost** (852 proizvoda; svi razlozi: pripadnost 852, rasprodaja 11, kategorija 2, price_suspect 1). Primjeri:

| lanac | naziv |
|---|---|
| konzum | ČIPS LAY'S SPICY PAPRIKA 130g |
| kaufland | Podravka Masline zel.paprika 680g/390g |
| tommy | KETCHUP LJUTI PAPRIKA 310 g PODR |
| spar | NAMAZ NATURETA PAPRIKA 290 g |
| konzum | PAPRIKA SLATKA 500g ŠAFRAM |
| plodine | MASLINE ZELENE S PAPRIKOM 700 G ZVIJEZDA |
| studenac | ČIPS CHIO CHIPS RED PAPRIKA 200 g |
| plodine | MARINIRANA CRVENA PAPRIKA 720 G CAMPO |
| kaufland | KBio.Paprika 400g |
| konzum | DELKO S PAPRIKOM NAR 250g VAC VINDIJA |

### tikvica

| lanac | kandidati → kategorija → pripadnost → varijante → pakiranje → price_suspect → rasprodaja → konačno |
|---|---|
| konzum | 3 → 3 → 2 → 2 → 2 → 2 → 2 → 2 |
| spar | 3 → 3 → 2 → 2 → 2 → 2 → 2 → 2 |
| plodine | 15 → 9 → 4 → 4 → 4 → 4 → 4 → 4 |
| lidl | 3 → 3 → 3 → 3 → 3 → 3 → 3 → 3 |
| kaufland | 2 → 2 → 2 → 2 → 2 → 2 → 2 → 2 |
| tommy | 8 → 8 → 5 → 5 → 5 → 5 → 4 → 4 |
| studenac | 7 → 7 → 4 → 4 → 4 → 3 → 2 → 2 |
| eurospin | 4 → 4 → 4 → 4 → 4 → 4 → 4 → 4 |

Najčešći razlog gubitka: **pripadnost** (13 proizvoda; svi razlozi: pripadnost 13, kategorija 6, rasprodaja 2, price_suspect 1). Primjeri:

| lanac | naziv |
|---|---|
| studenac | RIŽOTO S PILETINOM I TIKVICAMA 2,5 kg |
| tommy | MJEŠAVINA BULGUR/TIKVICA 350 g LEDO |
| plodine | PASTA S KOZICAMA I TIKVICAMA |
| plodine | RIZOTO S PILETINOM I TIKVICAMA 2,5 KG AMERICAN DONUT |
| spar | OROZOTTO TIKVICE BOS.300 g |
| studenac | RIŽOTO PILETINA I TIKVICE kg |
| tommy | TIKVICE PEČENE PORCIJA |
| plodine | RIZOTO S PILETINOM I TIKVICAMA PLODINE |
| tommy | TIKVICE PEČENE |
| plodine | RIZOTO S PILETINOM I TIKVICAMA PORCIJA |


## 10. Eurospin: zašto 62 mrkve i 59 krumpira

### mrkva: 63 proizvoda, od toga 60 iz grupe 9999999999994

| grupa (bkey) | id | naziv | trgovina |
|---|---|---|---|
| 8001553801207 | eurospin:014300101 | MRKVA | 44 |
| 8001553801269 | eurospin:014300201 | MRKVA | 44 |
| eurospin:mrkva rfz | eurospin:080054401 | MRKVA rfz | 44 |
| 9999999999994 | eurospin:080138802 | AVOKADO kom | 44 |
| 9999999999994 | eurospin:080100601 | BILJKA ALOE VERA | 44 |
| 9999999999994 | eurospin:080001101 | BILJKA BEGONIJA | 44 |
| 9999999999994 | eurospin:080001201 | BILJKA BONSAI | 44 |
| 9999999999994 | eurospin:080118301 | BILJKA BROMELIA | 44 |
| 9999999999994 | eurospin:080151701 | BILJKA CALLUNA MIX | 44 |
| 9999999999994 | eurospin:080172101 | BILJKA CELOZIJA | 44 |
| 9999999999994 | eurospin:080107501 | BILJKA CVIJET ASTRA | 44 |
| 9999999999994 | eurospin:080106801 | BILJKA DRACENA | 44 |
| 9999999999994 | eurospin:080111001 | BILJKA ECHEVERIA MIX BOJE | 44 |
| 9999999999994 | eurospin:080093501 | BILJKA ERIKA MIX | 44 |
| 9999999999994 | eurospin:080098701 | BILJKA FUKSIJA | 44 |
| 9999999999994 | eurospin:080099201 | BILJKA GAZANIJA | 44 |
| 9999999999994 | eurospin:080171501 | BILJKA HEBE MIX | 44 |
| 9999999999994 | eurospin:080171601 | BILJKA HEBE VARIEGATA | 44 |
| 9999999999994 | eurospin:080003001 | BILJKA HIBISKUS | 44 |
| 9999999999994 | eurospin:080003601 | BILJKA HORTENZIJA | 44 |
| 9999999999994 | eurospin:080004001 | BILJKA JAGLAC | 44 |
| 9999999999994 | eurospin:080001301 | BILJKA KALA | 44 |
| 9999999999994 | eurospin:080165901 | BILJKA KANA | 44 |
| 9999999999994 | eurospin:080078502 | BILJKA KAVE | 44 |
| 9999999999994 | eurospin:080095001 | BILJKA LAVANDA FI14 | 44 |
| 9999999999994 | eurospin:080154201 | BILJKA LJUBIČICA | 44 |
| 9999999999994 | eurospin:080116301 | BILJKA LOVOR FI14 | 44 |
| 9999999999994 | eurospin:080197701 | BILJKA MINI CIKLAMA FI10 | 44 |
| 9999999999994 | eurospin:080093401 | BILJKA MINI KAKTUS | 44 |
| 9999999999994 | eurospin:080002101 | BILJKA NEPHROLEPIS | 44 |

### krumpir: 60 proizvoda, od toga 56 iz grupe 9999999999994

| grupa (bkey) | id | naziv | trgovina |
|---|---|---|---|
| 3859891443208 | eurospin:080220301 | KRUMPIR 5kg | 44 |
| 8017596042378 | eurospin:011395501 | KRUMPIR REZANI PREDPRŽENI 1kg | 44 |
| eurospin:krumpir rfs | eurospin:080059201 | KRUMPIR RFS | 44 |
| 3859891088997 | eurospin:080464701 | KRUMPIR ZA PEČENJE 3kg | 44 |
| 9999999999994 | eurospin:080100601 | BILJKA ALOE VERA | 44 |
| 9999999999994 | eurospin:080001101 | BILJKA BEGONIJA | 44 |
| 9999999999994 | eurospin:080001201 | BILJKA BONSAI | 44 |
| 9999999999994 | eurospin:080118301 | BILJKA BROMELIA | 44 |
| 9999999999994 | eurospin:080151701 | BILJKA CALLUNA MIX | 44 |
| 9999999999994 | eurospin:080172101 | BILJKA CELOZIJA | 44 |
| 9999999999994 | eurospin:080107501 | BILJKA CVIJET ASTRA | 44 |
| 9999999999994 | eurospin:080106801 | BILJKA DRACENA | 44 |
| 9999999999994 | eurospin:080111001 | BILJKA ECHEVERIA MIX BOJE | 44 |
| 9999999999994 | eurospin:080093501 | BILJKA ERIKA MIX | 44 |
| 9999999999994 | eurospin:080098701 | BILJKA FUKSIJA | 44 |
| 9999999999994 | eurospin:080099201 | BILJKA GAZANIJA | 44 |
| 9999999999994 | eurospin:080171501 | BILJKA HEBE MIX | 44 |
| 9999999999994 | eurospin:080171601 | BILJKA HEBE VARIEGATA | 44 |
| 9999999999994 | eurospin:080003001 | BILJKA HIBISKUS | 44 |
| 9999999999994 | eurospin:080003601 | BILJKA HORTENZIJA | 44 |
| 9999999999994 | eurospin:080004001 | BILJKA JAGLAC | 44 |
| 9999999999994 | eurospin:080001301 | BILJKA KALA | 44 |
| 9999999999994 | eurospin:080165901 | BILJKA KANA | 44 |
| 9999999999994 | eurospin:080078502 | BILJKA KAVE | 44 |
| 9999999999994 | eurospin:080095001 | BILJKA LAVANDA FI14 | 44 |
| 9999999999994 | eurospin:080154201 | BILJKA LJUBIČICA | 44 |
| 9999999999994 | eurospin:080116301 | BILJKA LOVOR FI14 | 44 |
| 9999999999994 | eurospin:080197701 | BILJKA MINI CIKLAMA FI10 | 44 |
| 9999999999994 | eurospin:080093401 | BILJKA MINI KAKTUS | 44 |
| 9999999999994 | eurospin:080002101 | BILJKA NEPHROLEPIS | 44 |

**Objašnjenje:** Eurospin za 83 različita proizvoda (biljke, naranče, jagode, mrkva, krumpir…) koristi isti barkod **9999999999994**. Kontrolna znamenka je ispravna, pa je to „globalni“ EAN i svi ti proizvodi čine jednu grupu. Jedan naziv u njoj („MRKVA 1kg“, „KRUMPIR 4kg“) čini grupu snažnim članom mrkve ili krumpira, pa u izbor ulaze i begonije, jagode i naranče. Stvarnih Eurospinovih mrkvi i krumpira je 4 odnosno 7.

**Prijedlog (nije primijenjen):** EAN koji jedan lanac koristi za barem 5 različitih `name_norm` tretirati kao neglobalan, pa se grupira po lanac + `name_norm` (kao proizvodi bez EAN-a). EAN-ovi koji bi to pogodili:

| EAN | lanac | proizvoda | različitih naziva |
|---|---|---|---|
| 9999999999994 | eurospin | 83 | 83 |

## 11. Plodine: skupina iz prefiksa šifre

Učenje na Plodinama sa skupinom iz EAN-a (`category_source = 'ean_inherited'`; Plodine nemaju kategorija), prefiksi od 2, 3 i 4 znaka, 80 % učenje i 20 % odloženo (po hashu šifre). Primjenjuju se samo prefiksi čistoće ≥ 95 % s ≥ 30 primjera, najduži ima prednost (`category_source = 'prefix'`, `clean.prefix_rules`).

Primijenjeno 37 prefiksa; točnost na odloženom skupu 99,3 % (769 proizvoda). Iz `unknown` izlazi **1681** Plodina (hrana 1524, kucanstvo 119, pice 33, alkohol 5); `unknown` ostaje 48398.

| prefiks | primjera (učenje) | skupina | čistoća | odloženo | točnost |
|---|---|---|---|---|---|
| 02 | 280 | hrana | 0,99 | 65 | 1,00 |
| 04 | 111 | hrana | 0,98 | 27 | 0,96 |
| 05 | 86 | hrana | 1,00 | 20 | 1,00 |
| 11 | 32 | hrana | 1,00 | 11 | 1,00 |
| 17 | 648 | hrana | 1,00 | 157 | 1,00 |
| 18 | 138 | hrana | 1,00 | 37 | 1,00 |
| 26 | 38 | kucanstvo | 0,97 | 3 | 1,00 |
| 010 | 53 | pice | 0,96 | 14 | 1,00 |
| 011 | 41 | pice | 0,95 | 9 | 1,00 |
| 012 | 90 | alkohol | 0,99 | 29 | 0,97 |
| 013 | 43 | alkohol | 0,98 | 12 | 0,83 |
| 021 | 86 | hrana | 1,00 | 24 | 1,00 |
| 022 | 73 | hrana | 0,99 | 9 | 1,00 |
| 023 | 104 | hrana | 0,98 | 24 | 1,00 |
| 030 | 54 | hrana | 1,00 | 10 | 1,00 |
| 031 | 74 | hrana | 1,00 | 8 | 1,00 |
| 032 | 39 | hrana | 1,00 | 5 | 1,00 |
| 034 | 66 | hrana | 1,00 | 15 | 1,00 |
| 035 | 63 | hrana | 1,00 | 15 | 1,00 |
| 036 | 73 | hrana | 1,00 | 14 | 1,00 |
| 042 | 53 | hrana | 1,00 | 15 | 1,00 |
| 052 | 38 | hrana | 1,00 | 2 | 1,00 |
| 175 | 52 | hrana | 1,00 | 11 | 1,00 |
| 176 | 64 | hrana | 1,00 | 18 | 1,00 |
| 177 | 88 | hrana | 1,00 | 22 | 1,00 |
| 178 | 161 | hrana | 1,00 | 38 | 1,00 |
| 179 | 213 | hrana | 1,00 | 50 | 1,00 |
| 181 | 53 | hrana | 1,00 | 13 | 1,00 |
| 185 | 62 | hrana | 1,00 | 17 | 1,00 |
| 0235 | 43 | hrana | 0,98 | 11 | 1,00 |
| 0236 | 37 | hrana | 0,97 | 10 | 1,00 |
| 0354 | 35 | hrana | 1,00 | 8 | 1,00 |
| 1792 | 31 | hrana | 1,00 | 15 | 1,00 |
| 1793 | 35 | hrana | 1,00 | 9 | 1,00 |
| 6170 | 47 | kucanstvo | 1,00 | 3 | 1,00 |
| 8823 | 31 | kucanstvo | 1,00 | 11 | 1,00 |
| 8998 | 42 | hrana | 0,95 | 8 | 0,88 |

30 primjera:

| šifra | naziv | skupina |
|---|---|---|
| 185550 | RAZNJICI OD SV.LOPATICE E530 G | hrana |
| 185238 | SV.LOPATICA. S.K I SPEKOM-NEOBRADJENA | hrana |
| 178984 | MORTADELA 150 G GUSTI | hrana |
| 260127 | BIOKILL 1/2 INSEKTICID REFIL | kucanstvo |
| 176606 | GRANA PADANO 90GGRANAROLO MAGROS | hrana |
| 177424 | SIR LANDANA ZELENI PESTO CCA 4 KG VANDERSTERRE | hrana |
| 185130 | TEL.LEDA S.K I KAT | hrana |
| 178787 | SUHA DOMACA SALAMA VP Z DEZELE | hrana |
| 176071 | SIR TARTUFI CCA 600 G ZDENKA | hrana |
| 178477 | FARMER SUNKA 150 G RADATZ | hrana |
| 179145 | MORTADELLA PISTACCHIO FELSINEO | hrana |
| 185692 | MARINIRANI SVINJSKI FILE | hrana |
| 177158 | SIR REZANI TILZIT 150 G DOLINE | hrana |
| 185084 | JUN.REBRA III KAT VP | hrana |
| 177488 | SIR PECORINO RIBANI 100 G BIRAGHI | hrana |
| 177373 | SIR GRAN SPICCO CCA 1 KG ZANETTI | hrana |
| 178876 | ZIMSKA SALAMA 80 G GUSTI PPK | hrana |
| 266816 | SONAX MARAMICE ZA NJEGU PLASTIKE 10/1 | kucanstvo |
| 178899 | EXTRA KOBASICA 1000 G+100 G GRATIS PERUTNINA | hrana |
| 023609 | GUSTI JETRENA PASTETA 100 G GAVRILOVIC | hrana |
| 178118 | SUHE NOGICE RFZ PLODINE PPK | hrana |
| 178049 | SLANINSKA KOBASICA RFZ KUDELIC | hrana |
| 113540 | BUKOVACE 250GR | hrana |
| 185187 | JUN.BIFTEK - S | hrana |
| 177113 | RAJCICA SUSENA RINFUZO(NETTO 0,9 KG) IVOX | hrana |
| 113309 | ROTKVA CRNA | hrana |
| 110703 | LUK ZUTI | hrana |
| 179374 | FINA KOBASICA 300 G PIVAC | hrana |
| 185138 | TEL.LOPATICA B.K. II KAT MP | hrana |
| 185860 | DOMACA JANJETINA | hrana |
