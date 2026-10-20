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
| tjestenina | 3859892804077 | 33,00 | lorenco: ARBONI RAPSKI FIDELINI 400g; jadranka_trgovina: TJESTENINA FIDELINI RAPSKI 400G ARBONI; djelo_vodice: RAPSKI FIDELINI 400G ARBONI |
| jogurt | 3850354018377 | 48,00 | gavranovic: JOGURT DUKATOS DIVINE 150g KARAMELA DUKAT; ktc: DUKATOS DIVINE 150g KARAMELA; ntl: JOGURT DUKATOS DIVINE SLANA KARAMELA 150 g DUKAT; plodine: DUKATOS SLANA KARAMELA 150 G; branka: JOGURT DUKATOS DIVINE SLANA KARAMELA 150g; djelo_vodice: DUKATOS DIVINE SLANA KARAMELA 150G; kaufland: Dukatos Jogurt grčki sl.ka.6%mm 150g; vrutak: N-DUKAT JOGURT DUKATOS DIVINE150G SLANA KARAMELA -6/1- 13000; stanic: DUKATOS DIVINE SLANA KARAMELA 150 g DUKAT; studenac: DUKATOS DIVINE SLANA KARAMELA 150g; tommy: JOGURT SLANA KARAMELA 150 g DUKATOS; trgocentar: DUKATOS DIVINE SLANA KARAMELA 150G (X); ribola: DUKATOS 150 g SL.KA. DIVINE; stridon: DUKATOS DIVINE SLANA KARAMELA 150 g DUKAT; lorenco: DUKATOS DIVINE SLANA KARAMELA 150G; jadranka_trgovina: JOGURT DUKATOS DIVINE SLANA KARAMELA150G; spar: JOG.DUKAT.DIVINE KARAMEL.150 g; konzum: JOGURT DUKATOS DIVINE SLAN KAR 150g; trgovina-krk: JOGURT DUKATOS DIVINE SLANA KARAMELA 150 gr; dukat: DUKATOS DIVINE SLANA KARAMELA 150g; boso: JOGUR DUKAT 150 g DUK.DIV.SL.KAR |
| tjestenina | 8004350141156 | 50,00 | trgovina-krk: CANELONI PASTA 250 g; ribola: TJ.CANNELLONI 250 g BR.115 ULTRA; lorenco: TJEST.115 CANNELLONI 250g; konzum: TIJESTO CANNELLONI 115 250g ZARA |
| tjestenina | 3859888231023 | 50,00 | kaufland: Clarum fidelini sitni 400 g; ntl: TJEST.FIDELINI SITNI 400 g CLARUM |
| grasak | 3838977044508 | 25,00 | tommy: POLI GREEN MINI 220 g; ribola: POLI GREEN 220 g PER UTNINA; studenac: POLI GREEN MINI 220 g; kaufland: Poli Salama od graška Green 220g |
| tjestenina | 5060194790120 | 50,00 | konzum: SOBA NOODLES 300g SAITAKU; tommy: TJ.JAPANSKA SOBA NOOD. 300 g; plodine: SOBA NOODLES 300 G SAITAKU; ribola: REZANCI JAPAN 300 g SAITAKU SOBA |
| grasak | 8000627306938 | 33,00 | trgovina-krk: SJEME GRAH MAHUNAR BERGOLD 250 g MARCON; ntl: GRAŠAK M.BERGGOLLD 250G; plodine: SJEME GRAH MAHUNAR BERGGOLD |
| sunka | 3850159128929 | 45,00 | ktc: PUREĆA DELUXE ISTRANKA 100g VINDIJA; trgovina-krk: DELUX ISTRANKA 100 gr; boso: DELUXE 100 g ISTRANKA; djelo_vodice: DELUXE ISTRANKA 100g; branka: SALAMA ISTRANKA DELUXE 100g; jadranka_trgovina: ŠUNKA PUREĆA DELUXE ISTRANKA 100G; ribola: SAL.DEL.ISTR.100 g V INDIJA; vrutak: N-VIN PUREĆA DE LUX ŠUNKA ISTRANKA 100G -12/1-; konzum: ŠUNKA PUREĆA ISTRANKA NAR 100g; plodine: PURECA SUNKA ISTRANKA 100 G VINDON VINDIJA; tommy: ŠUNKA PUREĆA ISTRANKA 100 G |
| kecap | 3856020275730 | 30,00 | konzum: UMAK ZIK ZAK LJUTI 310 g PODRAVKA; lidl: ZIK ZAK paprika ljuti umak; plodine: KETCHUP LJUTI 310 G ZIK ZAK PODRAVKA; tommy: KETCHUP LJUTI PAPRIKA 310 g PODR; spar: KETC.ZIK ZAK PODR.LJUTI 310 g; jadranka_trgovina: UMAK ZIK ZAK LJUTI 310G PODRAVKA; roto: ZIK ZAK LJUTI 310G PODRAVKA (6); ktc: ZIK ZAK LJUTI 310g PODRAVKA; kaufland: Zik Zak Umak od paprike ljuti 310g vg.; studenac: KETCHUP ZIK ZAK LJUTI 310g |
| jogurt | 3850108032666 | 25,00 | lorenco: FORTIA VIŠNJA 300g TTOP; trgocentar: FORTIA VIŠNJA 330G TTOP; stridon: FORTIA VIŠNJA 330 gr TTOP VINDIJA; ribola: JOG.330 g VIŠ.TT FOR TIA |
| cokolada_za_kuhanje | 3877000595778 | 50,00 | trgovina-krk: ČOKOLADA ZA KUHANJE 300 g LA BOMBA; gavranovic: ČOKOLADA ZA KUHANJE 300g LA BOMBA; boso: ČOKOL LA BOMBA 300 g JELO I KUH.; stridon: ČOKOLADA ZA JELO I KUHANJE 300 g LA BOMBA (10); ntl: ČOKOLADA ZA JELO I KUHANJE 300 g LA BOMBA; tommy: ČOKOLADA ZA KUH.XXL 300 g LA BOMBA |
| mlijeko | 3850108021202 | 50,00 | ribola: ML.TR.1,6% 1L KAL.VINDIJA; stridon: MLIJEKO CA+ 1.6%MM 1 L VINDIJA |
| krumpir | 3859893072031 | 50,00 | lorenco: LIČKI KRUMPIR 5/1; metro: 10KG LIČKI KRUMPIR CRVENI |
| jogurt | 3831051018563 | 50,00 | spar: JOG.GRČKI TIP 0% MYTHOS 400 g; ktc: MYTHOS GRČKI TIP 0%mm 400g |
| sunka | 3838885333022 | 50,00 | trgovina-krk: PRŠUT KMEČKI NAREZAK 100 g KRAS; jadranka_trgovina: ŠUNKA SUHA KMEČKA 100G KRAS |
| tjestenina | 3858894412037 | 50,00 | trgovina-krk: LILIUM MIX FI 13; eurospin: BILJKA LJILJAN |
| maslac | 8719200265127 | 25,00 | jadranka_trgovina: MARGARIN RAMA NAMAZ BUTTERY 400G; lorenco: RAMA CLASSIC S MASLACEM 400G; kaufland: Rama Margarin buttery 400 g; stanic: RAMA NAMAZ BUTTERY 400 g; ktc: RAMA NAMAZ BUTTERY 400g; spar: RAMA NAMAZ BUTTERY 400 g; plodine: RAMA CLASSIC S MASLACEM 400 G; lidl: Rama Margarin SK1 |
| tvrdi_sir | 3859889426459 | 33,00 | konzum: SIR TVRDI MEDITERANO VAC PAŠKA SIRAN; lorenco: SIR MEDITERANO PAŠKA SIRANA VP.1/4; plodine: SIR MEDITERANO 1/4 PASKA SIRANA |
| jabuka | 3859893211324 | 50,00 | metro: 6/1 JABUKA CRVENI DELIŠES KOM PD; plodine: BIO JABUKA CRVENA PODLOZAK |
| cokolada_za_kuhanje | 8606015718415 | 40,00 | branka: \*NE\*ČOKOLADA MLIJEČNA 150g DR. OETKER; tommy: ČOKOLADA ZA KUH. MLIJ. 150 g DR.OET; kaufland: Dr.Oekter Čokolada mliječna 33% 150 g; ribola: ČOKO.MLIJEČNA 150 g DR.OETKER; plodine: COKOLADA ZA KUHANJE MLIJECNA 150 G DR.OETKER; vrutak: N-ČOKOLADA ZA KUHANJE 150G MLIJEČNA -15/1-; bure: ČOKOLADA 150 g MLIJEČNA; konzum: ČOKO ZA KUH MILK 33% 150 g DR OETKER; trgovina-krk: ČOKOLADA ZA KUHANJE MLIJEČNA 150 g; spar: ČOKO.ZA KUHANJE MLIJEČNA 150 g |
| tjestenina | 3859888931053 | 38,00 | trgovina-krk: PLJUKANCI 500 gr SMRZNUTO; konzum: PLJUKANCI 500 g MARIJA TJESTENINE; spar: TJES.MARIJA PLJUKANCI 500 g; plodine: ISTARSKI PLJUKANCI 500 G MARIJA; lorenco: TJESTENINA PLJUKANCI "MARIJA"; jadranka_trgovina: TJESTENINA PLJUKANCI ISTARSKI DS 500G MARIJA; metro: 500G MARIJA ISTARSKI PLJUK SM; stanic: PLJUKANCI 500 g SMRZNUTI |
| tjestenina | 3859888666047 | 50,00 | ntl: TJESTENINA MAFALDINE CORTE 400g MARODI; branka: TJESTENINA KRPICE SREDNJE/MAFALDINE CORTE 400g; konzum: TIJESTO KRPICE SREDNJE 400g MARODI; metro: 400G MARODI MAFAL COR BEZ JAJA; gavranovic: TJ.MARODI 400g KRPICE SREDNJE; trgovina-krk: TJES.MARODI KRPICE SREDNJE 400 g; vrutak: TJEST MARODI MAFALDINE CORTE/KRPICE SREDNJE 400G -10/1-; roto: TIJESTO KRPICE SREDNJE 400g MARODI (10); ktc: MAFALDINE CORTE 400g MARODI; kaufland: Marodi srednje krpice 400 g; jadranka_trgovina: TJESTENINA MAFALDINE CORTE 400G MARODI; ribola: TJ.MAFALD.CORT.400 g MARODI; bure: TJ.SREDNJE KRPICE 400 g MAFALDINE; stridon: MAFALDINE CORTE (SREDNJE KRPICE) MARODI 400 g (10) |
| tvrdi_sir | 8003518100622 | 50,00 | lorenco: GRANA PADANO GIRA i GRATTA 150g; konzum: SIR TVRDI GP TWIST&GRATE 150 g |
| tvrdi_sir | 3858891770208 | 25,00 | spar: SIR S MASLINAMA GLIGORA 125 g; lorenco: SIR S MASLINAMA 125g GLIGORA; plodine: SIR S MASLINAMA 125 G SIRANA GLIGORA; vrutak: SIR S MASLINAMA 125G GLIGORA POLUTVRDI KRAVLJI -12/1 |
| tvrdi_sir | 3858891773889 | 25,00 | jadranka_trgovina: SIR TVRDI LIBURJAN VAC. 190G SIRANA GLIGORA; trgovina-krk: SIR LIBURJAN 190 gr; tommy: SIR LIBURJAN 190 g GLIGORA; vrutak: SIR LIBURJAN GLIGORA 190G -8/1- |
| tjestenina | 3858887101856 | 50,00 | kaufland: Farina Speciale Krupica durum 1 kg; konzum: KRUPICA DURUM ZA TJEST 1 kg FARINA |
| svjezi_sir | 3859893220067 | 33,00 | tommy: SIR SVJ.SKUTA KRAVLJA 250 g; spar: SKUTA KRAVLJA MILS 250 g; lorenco: SKUTA KRAVLJA 250g MILS; studenac: SKUTA KRAVLJA DALMAT.SIREVI 250 g; konzum: SIR SVJ KRAVLJA SKUTA 250g DALMAT SIR; ribola: SKUTA KRAV.250g DALM |
| med | 8594071650308 | 50,00 | konzum: MEDENE KUGLICE KAKAO 235g MARLENKA; spar: KUGLICE OD MEDA S KAKAOM 235g |
| mrkva | 3859893211331 | 33,00 | metro: 6/1 JABUKA CRIPS PINK KOM PD; plodine: MRKVA 500 G; spar: KUKURUZ ŠEĆERAC 3/1 |
| tvrdi_sir | 3858881190757 | 33,00 | plodine: SIR ISTARSKI KRAVLJI CCA 1,7 KG AGROLAGUNA; spar: Sir kravlji Špin; konzum: SIR TVRDI KRAVLJI ŠPIN |

30 grupa koje prelaze iz člana (2D) u `ambiguous`:

| namirnica | grupa | m % | x % | nazivi po lancu |
|---|---|---|---|---|
| majoneza | 3856015304339 | 86,00 | 14,00 | roto: MAJONEZA ČILI 165G ZVIJEZDA (12); studenac: MAJONEZA ZV. 165G ČILI TUBA; vrutak: N-MAJONEZA ZVIJEZDA 165G -12/1 ČILI TUBA; kaufland: Zvijezda čili majoneza tuba 165g; plodine: MAJONEZA CILI 165 G TUBA ZVIJEZDA; branka: MAJONEZA ČILI 165g; lorenco: ZVIJEZDA ČILI MAJONEZA 165g; gavranovic: MAJONEZA CHILLI 165g ZVIJEZDA; jadranka_trgovina: MAJONEZA 165G ČILI TUBA ZVIJEZDA; ktc: MAJONEZA TUBA ČILI 165g ZVIJEZDA; trgovina-krk: MAJONEZA ČILI 165 g ZVIJ; trgocentar: MAJONEZA CHILI 165G TUBA (12) ZVIJEZDA; stridon: MAJONEZA ČILI TUBA 165 g (12) ZVIJEZDA; konzum: MAJONEZA ČILI 165g ZVIJEZDA |
| zobene_pahuljice | 8595054907761 | 67,00 | 25,00 | vrutak: ZOBENE PAHULJICE 300G BERRIES; branka: PAHULJICE ZOBENE BERRIES 300g; gavranovic: ZOBENE PAHULJICE DOBRE BERRIES 300g; ntl: PAHULJICE ZOBENE BERRIES 300 g DOBRE; tommy: ZOBENE PAH. ŠUM.VOĆE 300 g DOB; zabac: Dobre zobene pahuljice 300g BERRIES; kaufland: Dobre Pahuljice zobene bobič.voće 300g; plodine: ZOBENE PAHULJICE SUMSKO VOCE 300 G BIOPLOD; ribola: PAHULJ.ZO.BO.300 g D OBRE PAHULJICE; spar: DOBRE ZOBENE PAH.BOB.VOĆ.300 g; konzum: PAHULJICE ZOBENE BERRIES 300g; lorenco: DOBRE ZOBENE PAHULJICE 300g BERRIES |
| sol | 3870009000144 | 80,00 | 20,00 | plodine: SOL KUHINJSKA JODIRANA 250 G TULJAK TUZLA; kaufland: Tuzla kuhinjska sol jodirana 250g; spar: SOL KUHINJ. TUZLA SITNA 250 g; ktc: SOL KAMENA DOZA 250g TUZLA; vrutak: SOL KAMENA 250G SOLJENKA -15/1- TUZLA |
| tjestenina | 8710605028430 | 71,00 | 29,00 | ntl: TJESTENINA OD PŠ. BRAŠNA S JAJIMA 250G NIKAS; vrutak: TJESTENINA GO-TAN 250G EGG WOK NOODLES -8/1-; plodine: TJESTENINA S JAJIMA GNIJEZDA 250 G NOODLES GO TAN; spar: TJESTENINA GOTAN NEST 250 g; kaufland: Go Tan tjest.s jajima za Wok 250 g; ribola: TJEST.GO TAN 250g; konzum: TJESTENINA S JAJIMA GNIJEZDA GO TAN 250g |
| sol | 3856020222314 | 80,00 | 20,00 | tommy: VEGETA MAESTRO MORSKA SOL GRUBO MLJEVENA 100G; spar: ZAČ.SOL MORSKA VEG.MAES.100 g; ribola: SOL MORSKA 100 g VE GETA MAESTRO; ktc: MORSKA SOL GRUBO MLJEVENA 100g PODRAVKA; konzum: ZAČIN SOL MORSKA ML 100g VEGETA MAESTRO; lorenco: VEGETA MAESTRO MORSKA SOL 100G; bure: SOL MORSKA 100 g KRUNA PODR.; djelo_vodice: MORSKA SOL GRUBO MLJEVENA VEGETA MAESTRO BOČICA 100G; stridon: VEGETA MAESTRO MORSKA SOL M.100 G (6) PODRAVKA; plodine: MORSKA SOL MLINAC 100 G VEGETA MAESTRO |
| piletina | 3850159142321 | 77,00 | 15,00 | vrutak: N-VIN KRILCA BUCKET 500G -4/1-; branka: KRILCA BUCKET CEKIN 500g; plodine: CEKIN KRILCA BUCKET 500 G; stridon: CEKIN KRILCA BUCKET 500 g 14232 VINDIJA; trgocentar: CEKIN KRILCA BUCKET 500G; boso: KRILCA CEKIN 500 g BUCKET; spar: PILE.KRILCA BUCKET CEKIN 500 g; ktc: CEKIN KIDS BUCKET KRILCA 500g; ntl: KRILCA PILEĆA PEČENA SM 500 g CEKIN; trgovina-krk: CEKIN KRILCA BUCKET 500G; ribola: PIL.KRIL.BUCK. 500 gVINDIJA; jadranka_trgovina: KRILCA BUCKET CEKIN 500G VINDIJA; kaufland: Cekin Pečena pileća krilca 500 g |
| pileca_prsa | 3850159125034 | 78,00 | 17,00 | trgovina-krk: SALAMA PILEĆA PRSA U OVITKU 500 g VINDIJA; bure: PILEĆA PRSA OV.500 gCEKIN LOT:1726102801; metro: 500GR CEKIN PIL PRSA U OVITKU; studenac: PILEĆA PRSA U OVITKU 500g; trgocentar: PILEĆA PRSA U OVITKU 500G; gavranovic: PILEĆA PRSA U OVITKU 500g CEKIN (12503); kaufland: Cekin Pileća prsa u ovitku 500g; stridon: PILEĆA PRSA U OVITKU 500 g VINDIJA 12503; tommy: PILEĆA PRSA U OVIT.500 g VI; spar: PIL.PRSA U OVITKU VIN. 500 g; ntl: SALAMA PILEĆA PRSA U OVITKU 500 g KOKA; ktc: PILEĆA PRSA U OVITKU 500g KOKA; vrutak: N-VIN PIL.PRSA U OVITKU 500G-12/1- 12503; boso: PILEĆ KOKA 500 g PRSA U OVITKU; branka: SALAMA PILEĆA PRSA 500g; konzum: PRSA PILEĆA U OVITKU 500g VINDIJA; lorenco: PILEĆA PRSA 500g CEKIN; plodine: PILECA PRSA U OVITKU 500 G CEKIN (12503) VINDIJA |
| senf | 5949040202058 | 61,00 | 22,00 | djelo_vodice: ELEPHANT TRAJNO SLANO PECIVO - MED, SENF i LUK 70g; plodine: SNACK MED/SENF/LUK 70 G ELEPHANT; spar: KRE.ELEPHANT SENF&MED&LUK 70 g; konzum: KREKER MED I SENF 70 g ELEPHANT; ktc: ELEPHANT MED,SENF I LUK 70g; lorenco: ALKA ELEPH.TS PECIVO 70g; boso: KREKE ELEPHANT 70 g MED SENF LUK; jadranka_trgovina: GRICKALICE ELEPHANT MED, SENF I LUK 70G; kaufland: Elephant slano pecivo med senf i luk 70g; ntl: TRAJNO SLANO PECIVO ELEPHANT 70 g MED,SENF I LUK; trgovina-krk: ELEPHANT TRAJNO SLANO PECIVO - MED,SENF I LUK 70 g; vrutak: ELEPHANT 70G TRAJNO SLANO PECIVO ALKA MED, SENF, LUK; branka: PECIVO ALKA ELEPHANT MED-SENF-LUK 70g; tommy: SNACK MED SENF LUK 70 g ELEPHA; ribola: KREK.MED SEN.LU.70 g ELEPHANT; metro: 70G ELEPHANT FLAT MED SENF LUK; studenac: KREK. ELEPHANT SENFLUK 70 g; stanic: ELEPHANT PECIVO MED, SENF, LUK 70 g |
| med | 5949040205158 | 75,00 | 17,00 | tommy: SNACK SOL MED 180 g ELEPHANT; gavranovic: PECIVO TWIST MORSKA SOL I MED 180g - ELEPHANT; konzum: KREKE TWIST SOL I MED 180 g ELEPHANT; metro: 180G ELEPHANT TWIST SOL I MED; kaufland: Elephant Pecivo sl.morska sol,med180 g; ktc: ELEPHANT TWIST MORSKA SOL I MED 180g; stanic: ELEPHANT TWIST - MORSKA SOL I MED 180 g; spar: PECIV.ELEP.TWIST SOL-MED 180 g; ntl: TRAJNO PEC. ELEP.TWIST - MORSKA SOL I MED 180g; plodine: KREKER MORSKA SOL I MED 180 G ELEPHANT; ribola: KREK.M.SOL&MED 180 g ELEPHANT; djelo_vodice: ELEPHANT TWIST - MORSKA SOL i MED 180G |
| med | 5900617037152 | 86,00 | 14,00 | ribola: GRANOLA 300 g ORAH/ MED SANTE; konzum: MUESLI GRANOLA ORAŠ PLOD MED 300g SANTE; kaufland: Sante Granola Gold med i oraš.plod.300g; jadranka_trgovina: ŽITARICE GRANOLA GOLD ORASI+MED 300G SANTE; tommy: MUESLI GRAN. NUT/MED 300 g SAN; spar: GRAN.SANTE ORAŠ.PLOD.MED 300 g; plodine: MUESLI GRANOLA MED I ORASASTI PLODOVI 300 G SANTE |
| med | 4000521010294 | 63,00 | 31,00 | jadranka_trgovina: MUESLI CRUNCHY PLUS MED BADEM 300G VITALIS; studenac: MUESLI MED BADEM VITALIS 300 g; plodine: MUSLI PLUS MED BADEM 300 G CRUNCHY DR OETKER; kaufland: Dr.Oetker vitalis crunchy med badem 300g; metro: 300G VITALIS CRUN PLUS MED/BAD; tommy: MUESLI CRUN.PL. MED 300 g DR.O; trgocentar: VITALIS CRUNCHY PLUS MED BADEM 300G, DR.OETKER; bure: MUESLI VITALIS 300 gHONEY-ALMOND; ribola: MUESLI CHR.MED 300 g VITALIS DR OETKER; trgovina-krk: MUSLI CRUNCHY PLUS MED BADEM 300 g DR OETKER; roto: MUESLI KNUSPER MED BADEM 300G VITALI (8); vrutak: MUSLI DR OETKER 300G MED I BADEM CRUNCHY PLUS -8/1-; djelo_vodice: MUSLI CRUNCHY MED BADEM 300g; spar: MUSLI VITALIS MED,BADEM 300 g; konzum: MUESLI KNUSPER MED BADEM 300g VITALI; lorenco: DR.OETKER CRUNCHY PLUS MED BADEM |
| papar | 9001414274057 | 80,00 | 20,00 | plodine: SPICES DRINKS PAPAR CRNI, ZRNO 50 G; ntl: ZAČIN ZA KOKTELE SPICES & DRINKS PAPAR CRNI 50 g KOTANYI; spar: ZAČ. PAPAR S&D CRNI ZRNO 50 g; kaufland: Kotany papar crni zrno, bočica 50 g; lorenco: PAPAR CRNI ZRNO SiD STAKLO 100ML |
| kukuruz | 3859893512254 | 70,00 | 30,00 | spar: KUKURUZ PEČ.SLANI NATURA 60 g; jadranka_trgovina: KUKURUZ PEČENI SLANI BBQ 60G; gavranovic: KUKURUZ PEČENI SLANI BBQ 60g NATURA; plodine: KUKURUZ PECENI SLANI BBQ 60 G SUPER SNACK NATURA; studenac: KUKURUZ PEČ.SL. NATURA 60 g; lorenco: KUKURUZ PEČENI SALNI BBQ 60g S.SNAC; ribola: KUKURUZ PEČENI 60 g SLANI NATURA; trgocentar: KUKURUZ PEČENI SLANI 60G BBQ SUPER SNACK; trgovina-krk: KUKURUZ PS BBQ NATURA 60 g; vrutak: N-KUKURUZ NATURA 60G PEČENI SLANI BBQ -20/1- SUPER SNACK |
| papar | 9001414440834 | 86,00 | 14,00 | plodine: SPICES DRINKS PAPAR CRVENI ZRNO 25 G; ntl: ZAČIN ZA KOKTELE SPICES & DRINKS PAPAR CRVENI 25 g KOTANYI; gavranovic: KOTANYI PAPAR CRVENI ZRNO 25g SPICE DRINKS; spar: ZAČIN PAPAR CRVENI ZRNO 25 g; lorenco: PAPAR CRVENI ZRNO KOKTEL SND ST 100; vrutak: KOTANYI KOKTEL PAPAR CRVENI SPICE i DRINKS 25G ZRNO; konzum: PAPAR CRVENI ZRNO S&D 25g KONTAYI |
| tuna | 8004030860025 | 0,00 | 86,00 | lorenco: TUNA -COUS-COUS SAL.2\*160g BOWL.; spar: TUNA SAL.RIO MARE COUS 2X160 g; kaufland: Rio Mare Insal.sal.tuna cous cous2x160g; konzum: TUNJ SALATA COUS COUS 2X160g RIO MARE; tommy: TUNA SALATA CUS CUS 2X160 G RIO MARE; metro: 160GX2 RIO MARE INSALA.CUS CUS; plodine: TUNA COUS-COUS SAL.2X160G BOWL |
| piletina | 3850159113154 | 60,00 | 20,00 | ribola: GAVELINO VINDIJA; plodine: GAVELINO PILE ZA PECENJE CEKIN (11315); konzum: PILE GAVELINO POD VINDIJA; spar: PILE GAVELINO; studenac: PILE GAVELINO VINDIJA KOKA kg |
| senf | 5949040204953 | 60,00 | 10,00 | kaufland: Elephant Komadići med,senf i luk75g; konzum: PER LOMLJ MED SENF LUK 75 g ELEPHANT; ktc: ELEPHANT KOMADIĆI MED,SENF I LUK 75g; stridon: ALKA ELEPHANT TS PECIVO-KOMAD.S OKUS.MEDA 14\*75 g; gavranovic: PECIVO KOMADIĆI MED,SENF I LUK 75g ELEPHANT; ntl: TRAJNO SLANO PECIVO ELEPHANT PRETZEL 75 g MED, SENF I LUK; plodine: PEREC KOMADICI S OKUSOM MEDA,SENFA I LUKA 75 G ELEPHANT; tommy: SNACK MED SENF LUK 75 g ELEPHA; boso: KREKE ELEPHANT 75 g MED SENF LUK; ribola: PERECI ME.SE.LU.75 g ELEPHANT |
| pileca_prsa | 3856020257064 | 57,00 | 14,00 | ktc: PILEĆA PRSA 60g LINO; plodine: LINO PILECA PRSA 60 G PODRAVKA; tommy: PILEĆA PRSA 60 G LINO NARESCI PODRAVKA; spar: PILEĆA PRSA LINO NJUPAL. 60 g; ribola: ŠUNKA PILEĆA 60 g LINO PODRAVKA; stridon: LINO PILEĆA ŠUNKA 60 g (10) PODRAVKA; konzum: LINO PILEĆA PRSA 60 g |
| majoneza | 3856015324689 | 81,00 | 14,00 | trgocentar: MAJONEZA ČILI 85G ,ZVIJEZDA; kaufland: Zvijezda majoneza čili 85 g; ribola: MAJONEZA ČILI 85 g ZVIJEZDA; spar: MAJONEZA CHILI ZVIJEZDA 85 g; studenac: MAJONEZA ČILI 85g ZVIJ.; branka: MAJONEZA ČILI 85g; djelo_vodice: ČILI MAJONEZA 85g; gavranovic: MAJONEZA CHILLI VREĆICA 85g ZVIJEZDA; trgovina-krk: MAJONEZA ČILI 85G; boso: MAJON ZVIJE 85 g DELIK.ČILI; jadranka_trgovina: MAJONEZA 85G ČILI VREĆICA ZVIJEZDA; konzum: MAJONEZA ČILI PVC 85g ZVIJEZDA; vrutak: N-MAJONEZA ZVIJEZDA 85G -25/1 ČILI; tommy: MAJONEZA ČILI 85 G ZVIJEZDA; ktc: MAJONEZA ČILI 85g ZVIJEZDA; lidl: Zvijezda Majoneza Čili; roto: MAJONEZA ČILI PVC 85g ZVIJEZDA (25); lorenco: ZVIJEZDA MAJONEZA ČILI 85G; metro: 85G ZVIJEZDA MAJONEZA ČILI; zabac: CHILI MAJONEZA 75% 85 G; stridon: MAJONEZA ČILI ZVIJEZDA 85 g (25) |
| papar | 9001414050026 | 54,00 | 46,00 | spar: ZAČ.PAPAR ZELEN.KOTANYI 100 g; trgovina-krk: PAPAR ZELENI U SALAMURI 100 g KOTAN; ribola: PAPAR ZEL.SAL. 100 g KOTANYI; trgocentar: KOTANY ZELENI PAPAR U ZRNU 100G; djelo_vodice: PAPAR ZEL.SALAMURA; bure: PAPAR ZELENI 100 g SALAMURA UG.; studenac: ZAČIN PAPAR ZELENI U SALAMURI 100 g KO; gavranovic: KOTANYI PAPAR ZEL.U SALAMURI 100g; vrutak: KOTANYI 100G PAPAR ZELENI USALAMURI -24/1-; roto: PAPAR ZELENI U SALAMURI 100g KOTANYI (24); lorenco: ZELENI PAPAR 100 g KOTANYI; metro: 100G KOTANYI PAPAR ZELENI U SA; tommy: ZAČIN PAPAR ZEL/SAL. 100 g KOT |
| dodatak_jelima | 3856020228910 | 90,00 | 10,00 | kaufland: Vegeta Natur Grill Burger classic 30 g; konzum: ZAČIN BURGER CLASSIC VR 30g VEGETA NATUR; lorenco: VEGETA NATUR BURGER CLASSIC VR.30g; tommy: VEGETA NATUR BURGER VR.30 g PO; stridon: VEGETA NATUR BURGER CLASSIC 30 g (18); trgocentar: VEGETA NATUR BURGER CLASSIC VR.30G (18) (PAL 252) PODRAVKA; trgovina-krk: VEGETA NATUR BURGER CLASSIC 30 g VREĆICA POD; spar: ZAČIN VEGETA NATUR BURGER 30 g; bure: VEGETA VR.BURG. 30 gCLASSIC; plodine: VEGETA NATUR BURGER 30 G CLASSIC |
| sol | 3856020267216 | 83,00 | 17,00 | bure: VEGETA MAESTRO 110g SITNA SOL; tommy: VEGETA MAESTRO SITNA MORSKA SOL POSIPAČ 110 g; spar: ZAČ.V.MAEST.SITNA MOR.SOL 110g; lorenco: VEGETA MAESTRO SITNA MORSKA SOL; konzum: SOL SITNA MORSKA 110g VEGETA MAESTRO; plodine: VEGETA MAESTRO SITNA MORSKA SOL POSIPAC 110 G BOCICA |
| tjestenina | 8008857300771 | 83,00 | 17,00 | trgovina-krk: TJEST. TAGLIATI 500 g REGGIA NTL; ntl: TJESTENINA TAGLAITI 500g REGGIA; bure: TJ.FIDELINI 77 500 gREGGIA (SPAGET.TAGLI; ribola: TJ.SPAGHETTI 500 g TAGLIATI JUHA REGGIA; trgocentar: SPAGETTI TAGLIATI 77 (SITNI REZANCI) 500G PASTA REGGIA (24); jadranka_trgovina: TJESTENINA SPAGHETTI TAGLIATI 077 500G REGGIA |
| med | 5949040203482 | 70,00 | 20,00 | tommy: SNACK SOL MED 160 g ELEPHANT; plodine: SNACK MORSKA SOL I MED 160 G ELEPHANT TWIST; ribola: KREK.M.SOL&MED 160 g ELEPHANT; gavranovic: PECIVO TWIST MORSKA SOL I MED 160g - ELEPHANT; kaufland: Elephant Twist sl.pecivo m.sol i med160g; metro: 160G ELEPHANT TWIST SOL I MED; djelo_vodice: ELEPHANT TWIST - MORSKA SOL i MED 160g; lorenco: ALKA ELEPHANT TWIST-SOL I MED 160g; ntl: TRAJNO PEC. ELEP.TWIST - MORSKA SOL I MED 160g; stanic: ELEPHANT TWIST - MORSKA SOL I MED 160 g |
| papar | 9001414040867 | 60,00 | 10,00 | trgovina-krk: ZAČIN MJEŠAVINA PAPRA STAKLO 40 g KOTANY; branka: \*NE\*PAPAR MJEŠAVINA 35G STAKLO KOTANYI; gavranovic: KOTANYI PAPAR MJEŠAVINA STAKLO 40g; plodine: PAPAR MIX 40 G STAKLO KOTANYI; spar: ZAČ.PAPAR MJEŠ.KOTANYI 40 g; studenac: ZAČIN PAPAR ŠARENI 40 g KOT.; tommy: ZAČIN PAPAR MJEŠ.40 g KOTANY; bure: ZAČIN MJEŠ.PAPRA 100g; lorenco: ZAČIN MJEŠ. PAPRA 35 g KOTANYI; vrutak: KOTANYI 40G PAPAR ŠARENAMJEŠAVINA STAKLO -4/1- |
| sol | 9001414040034 | 69,00 | 31,00 | kaufland: Kotanyi himalajska sol 120 g bočica; spar: SOL HIMALAJ.SITNA KOTANY120 g; bure: SOL HIMALAJSKA 100 ml STAKLO; plodine: HIMALAJSKA SOL 120 G KOTANY BOCICA; ribola: SOL HIMALAJSKA 120 g STAKLO KOTANYI; studenac: ZAČIN HIMALAJSKA SOL 120 g KOT.; tommy: SOL HIMALAJSKA STAK. 120 g KOT; konzum: HIMALAJSKA SOL BOČ 120G KOTANYI; ktc: SOL HIMALAJSKA 100mL ST KOTANYI; lorenco: HIMALAJSKA SOL JODIRANA STAKLO 100; trgovina-krk: ZAČIN SOL HIMALAJSKA BOČICA KOTA; branka: SOL HIMALAJSKA BOČICA 120g; djelo_vodice: HIMALAJSKA SOL 100ML |
| jaja | 5200701000063 | 67,00 | 17,00 | trgovina-krk: SRCE JAJE PEPPA PIG 10G; studenac: BOM. JAJE PEPA PIG 10 g; vrutak: SRCE PL. PEPPA PIG 10G; konzum: JAJE S BOMBONIMA PEPA PIG 10g; ntl: JAJE IZNENAĐENJA 10 g MIX LICENCA; ribola: PEPPA PIG JAJE 10 g |
| kiseli_kupus | 3859891493098 | 56,00 | 11,00 | studenac: KIS. ZELJE MIX ZA SARMU 1100 g; konzum: KUPUS KISELI MIX ZA SARMU MADIG; eurospin: KUPUS KISELI MIX ZA SARMU 1kg; spar: KUPUS KIS.MIX ZA SARMU 1 kg; lorenco: MADIG MIX ZA SARMU 1000g; plodine: SARMA MIX 1 KG KISELI KUPUS MADIG; tommy: KUPUS KIS. MIX ZA SARMU 1000 g; trgovina-krk: KUPUS KISELI MIX MADIG ZA SARMU 1 kg NTL; gavranovic: ZELJE KISELO MIX ZA SARMU 1KG MADIG |
| sol | 9001414046241 | 75,00 | 25,00 | spar: MORSKA SOL KOTANY 120g; kaufland: Kotanyi Sol morska sitna jodirana 120g; plodine: MORSKA SOL 120 G BOCICA KOTANYI; metro: 120G KOTANYI MORSKA SOL BOČICA; tommy: SOL MORSKA JODIRANA 120 g KOTAN; vrutak: KOTANYI 100ML MORSKA SOL SITNA STAKLO -4/1-; bure: SOL SITNA 100ml STAKLO; konzum: MORSKA SOL BOČ 120 g KOTANYI |
| pileca_prsa | 3850159123306 | 59,00 | 35,00 | spar: PILEĆA PRSA 100 g; ktc: PILEĆA PRSA 100g VINDIJA; vrutak: VIN PILEĆA PRSA 100G; djelo_vodice: PILEĆA PRSA 100G VIN.; ribola: PIL.PRS.U OV.100 g VINDIJA; konzum: PRSA PILEĆA U OVITKU NAR 100g; lorenco: PILEĆA PRSA 100g; trgocentar: PILEĆA PRSA 100G, VINDIJA; studenac: PIL. PRSA U OVIT. 10 0g VINDVAC; trgovina-krk: SALAMA PILEĆA PRSA 100 g VIND; gavranovic: CEKIN PILEĆA PRSA NAREZAK 100g; ntl: SALAMA PRSA PILEĆA 100 g VINDIVAC; jadranka_trgovina: SALAMA PILEĆA PRSA 100G CEKIN VINDIJA; kaufland: Cekin Pileća prsa 100 g; stridon: PILEĆA PRSA 100 g VINDIJA; tommy: PILEĆA PRSA NARESCI 100 g; plodine: PILECA PRSA 100 G VINDIJA |

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
| tjestenina | strong | bure: TJ.LAZANJE 500 g PALLANTE; djelo_vodice: LASAGNE REGGIA 500G; ntl: TJESTENINA LASAGNE 500g REGGIA; ribola: TJ.LASAGNE 500 g REGGIA; vrutak: TJEST REGGIA 500G LASAGNE U-21132 12/1; trgocentar: LASAGNE 105 (LAZANJE) 500G PASTA REGGIA (12); trgovina-krk: TJEST. LASAGNE 500 g REGGIA NTL; jadranka_trgovina: TJESTENINA LASAGNE 205 500G REGGIA |
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
| tjestenina | strong | gavranovic: LJILJAN 37 cm - BIJELA/ROZA; ntl: LJILJAN 37 CM BIJELA/ROZA; trgovina-krk: LJILJAN 37CM |
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
| kozmetika → hrana | 1 |
| unknown → pice | 1 |
| ostalo → unknown | 1 |
| unknown → ostalo | 1 |

Vraćeno u `hrana` s „cvijet“ u nazivu: **78**. 20 primjera:

| lanac | naziv | kategorija | prije |
|---|---|---|---|
| konzum | SOL SOLNI CVIJET 150g SOLANA PAG | HRANA | ostalo |
| zabac | Cvijetni med Varžak 450g | Umaci i namazi | ostalo |
| trgocentar | ČAJ KAMILICA CVIJET 50G | Hrana | ostalo |
| trgocentar | MED CVIJETNI LIVADA 900G, APIMEL (12) | Hrana | ostalo |
| metro | BEGONIJA CVIJET - KOM | hrana | ostalo |
| metro | 1L TE VODA OD CVIJETA RUŽE | hrana | ostalo |
| branka | ČAJ NEVEN CVIJET S/C 30g | HRANA | ostalo |
| trgovina-krk | KLINČIĆ CVIJET 50 g | Hrana | ostalo |
| metro | 100G TIKVICA CVIJET | hrana | ostalo |
| ktc | ČAJ BAZGA CVIJET 40g AGRISTAR | HRANA | ostalo |
| jadranka_trgovina | MED CVIJETNI 450G | HRANA | ostalo |
| bure | MED CVIJETNI 900 g PIP LOT:17.08.28 | HRANA | ostalo |
| metro | 60G TIKVICA CVIJET | hrana | ostalo |
| metro | TIKVICA CVIJET - KOM | hrana | ostalo |
| ktc | ČAJ KAMILICA CVIJET 50g AGRISTAR | HRANA | ostalo |
| branka | ČAJ KAMILICA CVIJET 80g | HRANA | ostalo |
| ntl | BROKULA CVIJET 2,5kg ZMH | Hrana | ostalo |
| lorenco | MED CVJETNI 459 GRAMA |  | ostalo |
| metro | BORAŽINA CVIJET - KOM | hrana | ostalo |
| roto | MED CVIJETNI 900g MJEŠAVINA VARŽ (12) | MED | ostalo |

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
| konzum | RAJČICA BUMBOLINO 200 grama |
| lidl | Podravka Koncentrat rajčice 2x |
| studenac | RAJČICA PASIRANA VERDEAMO 500 g |
| plodine | RAJCICA TERNETTO 250 G |
| plodine | PASIRANA RAJCICA 500 G PLODINE (M) |
| konzum | RAJČICA PASIRANA 700g STAR |
| plodine | UMAK CHERRY RAJCICA S GLJIVAMA 400 G GUSTIBUS |
| spar | PESTO SPAR RAJČICA,BOS.190 g |
| studenac | KONC. RAJČICA PODRAVKA 260 g |
| plodine | UMAK RICOTTA I CHERRY RAJCICE 260 G, AGROMONTE |

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
| spar | POKE BOWL MRKVA I MANGO 350 g |
| plodine | KASICA JABUKA BANANA MRKVA 150 G GERBER |
| studenac | SOK VINDI A+C+E NARANČA MRKVA 0,5 l |
| konzum | BISKVIT ČOK MRKVA 8/1 200 g MR BROWN |
| eurospin | GRAŠAK I MRKVA 3X450g/390g |
| konzum | MJEŠ TORTA OD MRKVE 230 g DOLCELA |
| kaufland | Rio Mare Namaz od tune i mrkve 100g |
| konzum | SOK BIOTTA MRKVA 500ML PRETTI |
| tommy | FRUTEK SOK MRKVA 125 ml |
| konzum | NEG PIĆE TOCO NARANČA MRKVA 1.5L |

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
| studenac | SOK LIMUN KRASTAVAC TOCO 0,5 l |
| kaufland | Imbiss KLC.Krastavci 1550g/850g |
| konzum | KRASTAVAC EXCLUSIVE 290g DOORA |
| kaufland | KFav.Krastavci u medu premium 330g |
| plodine | SOK TOCO LIMUN- KRASTAVAC 0,5 L |
| tommy | KRASTAVCI 6-9 cm 680 g T! |
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
| lidl | Salata Iceberg |
| kaufland | Salata zelena rucola 125g |
| plodine | SALATA ZELENA BIO 100G |
| spar | Salata zelena sa sirom |
| plodine | SALATA ZELENA 100 G |
| eurospin | ZELENA SALATA 250g |

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
| konzum | LUK PRAH 70g SOTINAC |
| plodine | PECENI KIKIRIKI PAPIKA LUK MIX 400 G YUMMY |
| konzum | ČIPS CRUNCHIPS SIR LUK 130g |
| plodine | SNACK KARAMELIZIRANI LUK 160 G ELEPHANT TWIST |
| konzum | KVIKI GRIC VRHNJE I LUK 50G PODRAVKA |
| eurospin | KIKIRIKI U OMOTAČU VRHNJE/LUK 150G |
| plodine | CVARCI LUK I PAPRIKA VRECICA PRESANI 100 G PIVAC |
| plodine | PASTA LUK TUBA 190 G PODRAVKA |

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
| plodine | SIR ABC PAPRIKA100 G BELJE ZVIJEZDA |
| eurospin | PAPRIKA CRVENA FILETI 670g/320g |
| studenac | PAPRIKA FIL. ZUTI NATURETA 530g/290g |
| konzum | PAPRIKA SLATKA 500g ŠAFRAM |
| plodine | MASLINE ZELENE S PAPRIKOM 700 G ZVIJEZDA |
| kaufland | KLC.Paprika slatka mljevena 100g |
| plodine | MARINIRANA CRVENA PAPRIKA 720 G CAMPO |
| plodine | MASLINE ZELENE PUNJENE PAPRIKOM 350 G SELECTION |
| plodine | PUNJENE PAPRIKE I PIRE KRUMPIR PORCIJA |

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
| 8001553801269 | eurospin:014300201 | MRKVA | 44 |
| 8001553801207 | eurospin:014300101 | MRKVA | 44 |
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
| 177285 | SIR EMMENTALER ALPEN CCA 2,9 KG BERGLANDMILCH | hrana |
| 178488 | ROLANA PANCETA NAREZAK 80 G CORTE BUONA | hrana |
| 111823 | BIO CESNJAK 250G | hrana |
| 179537 | SUHA KOBASICA S PAPROM 200 G BELL FRANCE | hrana |
| 176206 | SUHA PECENICA 1/2 VP GUSTI PIVAC | hrana |
| 177373 | SIR GRAN SPICCO CCA 1 KG ZANETTI | hrana |
| 175704 | SIR TRAPIST KOLAN VP 1/4 CCA 550 G SIRANA GLIGORA | hrana |
| 181201 | SMRZNUTI PILECI BATAK 1 KG AIA | hrana |
| 177284 | SIR EMMENTALER CCA 3 KG MEGGLE | hrana |
| 179701 | SUSENI PRESANI ATLANTSKI BAKALAR 200-400G | hrana |
| 185402 | SV.KARE BK ODREZAK MAP E400 G | hrana |
| 185007 | SV.VRAT S.K. III KAT | hrana |
| 111758 | BIO MANDARINA 1 KG | hrana |
| 179101 | JAMON BODEGA 100 G ESPANA | hrana |
| 034514 | KAPULICA U ACETO BALSAMICU 350 G PONTI | hrana |
| 111826 | BIO RAJCICA 500G | hrana |
| 179489 | WUBERINI PILECE HRENOVKE 100 G BERETTA | hrana |
| 177176 | ZAMJENA ZA SIR PRIPR. OD OBR. MLIJEKA I PALM. ULJA 16 KG | hrana |
| 265781 | MAPED GUMICA SOFTY BLISTER 2/1 MAP021792 | kucanstvo |
| 179503 | WUBER HRENOVKE 250 G BERETTA | hrana |
| 617083 | CEKER 59X50X24CM GAMA SIR | kucanstvo |
| 178262 | PECENI BUT CCA 1000 G GUSTI PPK | hrana |
| 178918 | KUHANA SUNKA PRAGA COATI | hrana |
| 185048 | SVJEZA KOBASICA ZA PECENJE I SUSENJE | hrana |
| 179343 | MINI KOBASICA OD SVINJSKOG MESA 75 G AUVERNOU | hrana |
| 185735 | ROSTILJ KOBASICA E400 G | hrana |
| 175695 | SIR ABC DISNEY 100G BELJE ZVIJEZDA | hrana |
| 185804 | PILECA PRSA S KOZOM RINFUZO | hrana |
| 185117 | JUN.VRAT S.K. III KAT | hrana |
| 178782 | BRESAOLA DELLA VALTELLINA 100 G NAREZAK BERETTA | hrana |
