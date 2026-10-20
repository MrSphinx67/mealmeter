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
| dodatak_jelima | 94 | 14 | 68 | 46 |
| endivija | 24 | 0 | 0 | 5 |
| gljive | 109 | 0 | 3 | 8 |
| grah | 399 | 2 | 19 | 177 |
| grasak | 152 | 2 | 8 | 100 |
| griz | 31 | 5 | 6 | 34 |
| jabuka | 385 | 4 | 0 | 46 |
| jaja | 354 | 0 | 31 | 1083 |
| jogurt | 383 | 47 | 90 | 319 |
| junetina | 283 | 4 | 2 | 38 |
| kakao | 46 | 0 | 6 | 67 |
| kecap | 170 | 5 | 8 | 34 |
| kiseli_kupus | 126 | 4 | 6 | 5 |
| kiselo_vrhnje | 122 | 7 | 5 | 16 |
| koncentrat_rajcice | 41 | 3 | 1 | 0 |
| krastavac | 66 | 5 | 13 | 73 |
| krumpir | 234 | 2 | 1 | 207 |
| krusne_mrvice | 126 | 0 | 2 | 18 |
| kukuruz | 165 | 4 | 10 | 132 |
| kupus | 116 | 0 | 0 | 23 |
| kvasac | 60 | 0 | 0 | 1 |
| leca | 132 | 0 | 1 | 148 |
| limun | 96 | 0 | 2 | 33 |
| luk | 204 | 0 | 7 | 29 |
| majoneza | 178 | 6 | 15 | 8 |
| margarin | 96 | 5 | 3 | 1 |
| maslac | 245 | 7 | 27 | 354 |
| maslinovo_ulje | 351 | 11 | 20 | 75 |
| matovilac | 21 | 0 | 0 | 6 |
| med | 401 | 27 | 58 | 364 |
| mlijeko | 274 | 8 | 50 | 709 |
| mljevena_paprika | 98 | 13 | 10 | 10 |
| mljeveno_meso | 102 | 3 | 4 | 0 |
| mozzarella | 219 | 4 | 8 | 45 |
| mrkva | 118 | 1 | 0 | 44 |
| naranca | 111 | 0 | 2 | 37 |
| ocat | 145 | 0 | 22 | 195 |
| palenta | 79 | 6 | 1 | 0 |
| papar | 267 | 2 | 15 | 165 |
| paprika | 241 | 0 | 12 | 134 |
| parmezan | 110 | 5 | 4 | 18 |
| pasirana_rajcica | 134 | 4 | 4 | 4 |
| persin | 60 | 0 | 1 | 6 |
| pileca_prsa | 240 | 4 | 17 | 121 |
| piletina | 579 | 12 | 13 | 284 |
| prasak_za_pecivo | 44 | 4 | 0 | 0 |
| radic | 44 | 0 | 0 | 7 |
| rajcica | 198 | 1 | 7 | 189 |
| rajcica_konzerva | 183 | 7 | 0 | 1 |
| riza | 478 | 6 | 51 | 276 |
| rukola | 17 | 0 | 0 | 4 |
| secer | 312 | 0 | 22 | 126 |
| senf | 134 | 1 | 7 | 9 |
| slanina | 672 | 4 | 8 | 73 |
| slanutak | 116 | 1 | 3 | 30 |
| slatko_vrhnje | 28 | 4 | 11 | 0 |
| sol | 227 | 0 | 38 | 399 |
| spinat | 110 | 0 | 0 | 14 |
| sunka | 880 | 11 | 7 | 194 |
| svinjetina | 447 | 3 | 0 | 87 |
| svjezi_sir | 153 | 11 | 25 | 52 |
| tikvica | 53 | 0 | 0 | 9 |
| tjestenina | 1276 | 162 | 81 | 324 |
| tuna | 474 | 0 | 55 | 196 |
| tvrdi_sir | 893 | 68 | 65 | 18 |
| ulje | 243 | 2 | 29 | 1330 |
| vanilin_secer | 63 | 3 | 7 | 18 |
| vrhnje_za_kuhanje | 69 | 5 | 5 | 0 |
| zelena_salata | 71 | 1 | 0 | 2 |
| zobene_pahuljice | 69 | 3 | 3 | 17 |

Napomena: među slabim članovima ima krivih pogodaka kad drugi lanci proizvod zovu samo markom, a jedan naziv prolazi `must_match` (npr. „ČOKOLADA RIKI PŠENICA I MED“ kao med, „MINI CROASANI S MASLACEM“ kao maslac). Rangirani su ispod snažnih i označeni; točka 4 (kratice, `must_not_match`) dio njih uklanja.

30 slučajnih slabih članova:

| namirnica | grupa | m % | nazivi po lancu |
|---|---|---|---|
| tjestenina | 3838700010480 | 25,00 | spar: TJE.ZL.POLJE VALJANI REZ.400 g; tommy: TJ.REZANCI VALJANI 400 G ZLATO; bure: TJ.REZANCI 400g VALJANI; konzum: TJEST. FETTUCCINE 8 JAJ 400g ZLATOPOLJE |
| jogurt | 3850354005391 | 50,00 | stridon: JOGURT B.AKTIV 150 g 3+1 GRATIS DUKAT; studenac: B.AKTIV LGG NATUR 3X150g SUPER CIJENA |
| krastavac | 8595241528878 | 50,00 | trgovina-krk: KRASTAVCI 6-9 cm 670/360 g GIANA; branka: KRASTAVCI 6-9cm 670g/360g |
| med | 3858881047372 | 50,00 | ribola: ČOK.HONEY RIKI 230g; stridon: ČOKOLADA RIKI PŠENICA I MED KANDIT 230 g (9) |
| jogurt | 3850108030495 | 50,00 | lorenco: FRESCA EUFORIJA KREM JOGURT 150g; stridon: \*\*\*\*FRESKA EUFORIJA ČOKO CRISPY 150 g VINDIJA |
| pasirana_rajcica | 8003496005308 | 50,00 | trgovina-krk: RAJČICA PASIRANA PETTI 500 gr BRIK DELICATO; tommy: RAJČICA PAS. IL DELIC. 500 g |
| tvrdi_sir | 8002710440048 | 33,00 | tommy: SIR GRAN SPICO 200 g; jadranka_trgovina: SIR TVRDI GRAN SPICCO 200G ZANETTI; ribola: SIR EX.TVRDI 200 g ZANETTI |
| tjestenina | 3838700016567 | 33,00 | plodine: TJESTENINA RIBANA KASA 500 G ZLATO POLJE; studenac: ZP RIBANA KAŠA 500 g; djelo_vodice: ZP RIBANA KAŠA 500G; bure: TJ.RIBANA KAŠA 500 GPODRAVKA; spar: TJES.ZL.POLJ.RIBANA KAŠA 500 g; ntl: TJEST. RIBANA KAŠA JAJ 500G ZP; trgocentar: ZP TJEST.RIBANA KAŠA 500G (16) PODRAVKA; ribola: TJ.RIBANA KAŠA 500 g PODRAVKA ZLATO POLJ; ktc: RIBANA KAŠICA JAJČANA 500g ZLATOPOLJE; tommy: TJ.RIBANA KAŠA 500 g ZLATO; konzum: TJESTO RIBANA KAŠA JAJ 500g ZLATO POLJE; branka: TJESTENINA RIBANA KAŠA 500g; roto: TJESTO RIBANA KAŠA JAJ 500g ZLATO POLJE (14); lorenco: DOMAĆA RIBANA KAŠA 500g; trgovina-krk: TJEST. GRANDE RIBANA KAŠA 500 g PODRA |
| tjestenina | 3859892804213 | 33,00 | djelo_vodice: RAPSKE ŠURLICE 400G ARBONI; gavranovic: TJ.ARBONI 400g RAPSKE ŠURLICE; jadranka_trgovina: TJESTENINA ŠURLICE RAPSKE 400G ARBONI |
| cokolada_za_kuhanje | 7613035898646 | 40,00 | plodine: COKOLADA ZA KUHANJE DESS.CORSE 200 G NESTLE; metro: NESTLE ČOK KUH.DES. 200G CORSE; konzum: ČOKOL ZA KUH DESSERT CORSE 200g; kaufland: Nestle čokolada za kuhanje Corse 200 g; spar: ČOKO.NESTLE ZA KUH.CORSE 200 g |
| majoneza | 8445291266292 | 33,00 | plodine: MAJONEZA SMOKY 220 G THOMY; spar: UMAK SMOKY BBQ DOY.THOMY 220 g; zabac: THOMY Smoky mayo Doypack 18x220g RS |
| tjestenina | 3859889154758 | 33,00 | kaufland: Ragusa mozaik spirale 400g; plodine: TJ.VIJAK MOZAIK 400G PARADISO; studenac: TJ RAGUSA VIJAK MOZAIK 400G; ktc: TJESTEN.VIJAK MOZAIK 400g RAGUSA; spar: TJEST.RAGUSA VIJ.MOZAIK 400 g; branka: TJESTENINA VIJAK MOZAIK 400g RAGUSA |
| tjestenina | 3831001818809 | 50,00 | lorenco: MLI. VITA KOREAN.ŠKOLJKE PERL. 250G; plodine: TJESTENINA VITA PERLINE S MRKVOM 250 G MLINOTEST VRECICA |
| tvrdi_sir | 5902431270395 | 50,00 | konzum: SIR POLUTV CHEDDAR RED 200g DUB DAI; kaufland: Dublin Dairy Sir Ched.Red polutv.48%200g; spar: SIR CHEDDAR CRVENI DUB.DA.200g; plodine: SIR CHEDDAR CRVENI 200 G DUBLIN DAIRY EUROSER |
| jogurt | 3870085030530 | 50,00 | ribola: JOG.2,8% 330g MEGGLE; kaufland: Meggle tekući jogurt 2,8% m.m. 330 g PET |
| tjestenina | 3859890765134 | 33,00 | kaufland: Ragusa valvice 400g; spar: TJEST.RAGUSA VALVICE 400 g; ktc: VALVICE 400g RAGUSA |
| parmezan | 8003518100622 | 50,00 | lorenco: GRANA PADANO GIRA i GRATTA 150g; konzum: SIR TVRDI GP TWIST&GRATE 150 g |
| tjestenina | 8008343200875 | 50,00 | tommy: TJ. ORECCHIETTE 500 g RUMMO; jadranka_trgovina: TJESTENINA ORECCHIETTE No.87 PŠENIČNE 500G RUMMO; plodine: TJESTENINA ORECCHIETTE N.87 500 G RUMMO; metro: 500G RUMMO ORECCHIETTE Nº 87 |
| svinjetina | 3850139523423 | 50,00 | studenac: SVJEŽA SVINJSKA REBRA PIK VRBOVEC; konzum: SV REBRA |
| jogurt | 3859893374012 | 50,00 | ktc: TEKUĆI JOGURT 1kg KŽ MLJEKARA; kaufland: Križ.mljekara tekući jog.2,8%m.m. 1 kg |
| tjestenina | 3859893308154 | 25,00 | konzum: TIJEST REZANCI MRK JAJ 400 G KLARA M; plodine: TJESTENINA FIDELINI S MRKVOM 400 G KLARA MARIC; kaufland: Klara M fidelini za juhu s mrkvom 400g; spar: TJ.KLARA MARIĆ FIDELINI 400 g |
| dodatak_jelima | 3856003939932 | 50,00 | trgovina-krk: DODATAK JELU S POVRĆEM TO JE TO 1000 g NTL; ntl: DODATAK JELIMA S POVRĆEM 1kg TOJETO; boso: DODATAK TOJETO 1 kg POVRĆE; gavranovic: DODATAK JELIMA 1kg TOJETO S POVRĆEM |
| maslac | 8001618991898 | 50,00 | ntl: MINI CROASANI S MASLACEM PUNJENI ČOKOLADOM 200 g GOLOSINI; konzum: PECIVO GOLOSINI S ČOKOLADOM 200G RUGGERI |
| pasirana_rajcica | 3858891562902 | 50,00 | bure: PASIR.RAJČICA 680 g ULTRA; ribola: ULTRA-PAS.RA.680g ST |
| tvrdi_sir | 3856003951194 | 50,00 | ntl: SIR MOZZARELLA POLUTVRDI REZANI 100 g TOJETO; trgovina-krk: SIR MOZZARELLA POLUTVRDI REZANI 100G TO JE TO ZDENKA; gavranovic: SIR TOJETO MOZZARELLA 100g REZANI; boso: SIR TOJETO 100 g MOZZARELLA |
| mozzarella | 8000430130164 | 46,00 | studenac: SIR MOZZARELLA BUFA.125 g; lorenco: GALBANI BUFALA 125g; plodine: MOZZARELLA BUFALA GALBANI 125 G DUKAT; trgovina-krk: GALBANI BUFALA 125g DUKAT; spar: SIR MOZZ. BUFFALA GALBAN.125 g; tommy: SIR MOZZARELLA BUFALA 125 g; ribola: MOZZARE.125 g GAL.BU; vrutak: N-SIR MOZZARELLA BUFALA 125G GALBANI; bure: SIR MOZZAREL.125 g BUF.GAL.LOT:26102026; roto: SIR MEKI MOZZAR BUFALA 125G DUKAT (6); konzum: SIR MEKI MOZZAR BUFALA 125G DUKAT; ktc: SIR MOZZARELLA BUFALA 125g; dukat: GALBANI BUFALA 125g |
| tjestenina | 3859894191120 | 50,00 | konzum: TIJESTO SPIRULITELLE 250 g MARODI; ktc: SPIRULITELLE-SPIRULINA 250g MARODI\*\*; plodine: TJEST.SPIRULITELLE 250 G MARODI; kaufland: Marodi Tjestenina Spirulitelle 250g; branka: \*NE\*TJESTENINA SPIRULITELLE 250g; spar: TJ.MARODI SPITULITELLE 250 g |
| ulje | 8007153008374 | 50,00 | ribola: ULJE MIX SJEMEN. 1 l FIOR DI VITA FARCH; studenac: MIX SEMI FIOR DI VITA FARCHIONI 1 |
| mlijeko | 3850108011838 | 50,00 | ribola: ML.SVJ.1,5% 1L 21 VINDIJA; plodine: SVJEZE MLIJEKO 21 DAN 1,5% 1 L PET VINDIJA |
| med | 5900658739503 | 33,00 | ntl: MEDENJACI MIX S MLIJEČNOM ČOKOLADOM 400 g LAMBERTZ; trgocentar: MED.LAMBERTZ POLONIA VOLLMILCH 400G(10); gavranovic: MEDENJACI MIX S MLIJEČNOM ČOKOLADOM 400g; ktc: MEDENJACI 400g LAMBERTS MLIJEČ.ČOKOLADA; ribola: MED.SRC.MLI.ČO.400 g ULTRA; djelo_vodice: LAMBERTZ SRCA ML.ČOK. 400G |

30 grupa koje prelaze iz člana (2D) u `ambiguous`:

| namirnica | grupa | m % | x % | nazivi po lancu |
|---|---|---|---|---|
| med | 5949040203482 | 63,00 | 25,00 | ribola: KREK.M.SOL&MED 160 g ELEPHANT; plodine: SNACK MORSKA SOL I MED 160 G ELEPHANT TWIST; gavranovic: PECIVO TWIST MORSKA SOL I MED 160g - ELEPHANT; kaufland: Elephant Twist sl.pecivo m.sol i med160g; tommy: SNACK SOL MED 160 g ELEPHANT; lorenco: ALKA ELEPHANT TWIST-SOL I MED 160g; ntl: TRAJNO PEC. ELEP.TWIST - MORSKA SOL I MED 160g; djelo_vodice: ELEPHANT TWIST - MORSKA SOL i MED 160g |
| piletina | 3850159142321 | 77,00 | 15,00 | jadranka_trgovina: KRILCA BUCKET CEKIN 500G VINDIJA; kaufland: Cekin Pečena pileća krilca 500 g; trgocentar: CEKIN KRILCA BUCKET 500G; spar: PILE.KRILCA BUCKET CEKIN 500 g; ktc: CEKIN KIDS BUCKET KRILCA 500g; ntl: KRILCA PILEĆA PEČENA SM 500 g CEKIN; boso: KRILCA CEKIN 500 g BUCKET; vrutak: N-VIN KRILCA BUCKET 500G -4/1-; stridon: CEKIN KRILCA BUCKET 500 g 14232 VINDIJA; ribola: PIL.KRIL.BUCK. 500 gVINDIJA; plodine: CEKIN KRILCA BUCKET 500 G; branka: KRILCA BUCKET CEKIN 500g; trgovina-krk: CEKIN KRILCA BUCKET 500G |
| med | 5900617037152 | 86,00 | 14,00 | tommy: MUESLI GRAN. NUT/MED 300 g SAN; spar: GRAN.SANTE ORAŠ.PLOD.MED 300 g; plodine: MUESLI GRANOLA MED I ORASASTI PLODOVI 300 G SANTE; jadranka_trgovina: ŽITARICE GRANOLA GOLD ORASI+MED 300G SANTE; kaufland: Sante Granola Gold med i oraš.plod.300g; ribola: GRANOLA 300 g ORAH/ MED SANTE; konzum: MUESLI GRANOLA ORAŠ PLOD MED 300g SANTE |
| jaja | 5200701000063 | 67,00 | 17,00 | studenac: BOM. JAJE PEPA PIG 10 g; trgovina-krk: SRCE JAJE PEPPA PIG 10G; vrutak: SRCE PL. PEPPA PIG 10G; ribola: PEPPA PIG JAJE 10 g; konzum: JAJE S BOMBONIMA PEPA PIG 10g; ntl: JAJE IZNENAĐENJA 10 g MIX LICENCA |
| sol | 3856020222314 | 80,00 | 20,00 | plodine: MORSKA SOL MLINAC 100 G VEGETA MAESTRO; ktc: MORSKA SOL GRUBO MLJEVENA 100g PODRAVKA; ribola: SOL MORSKA 100 g VE GETA MAESTRO; konzum: ZAČIN SOL MORSKA ML 100g VEGETA MAESTRO; lorenco: VEGETA MAESTRO MORSKA SOL 100G; stridon: VEGETA MAESTRO MORSKA SOL M.100 G (6) PODRAVKA; tommy: VEGETA MAESTRO MORSKA SOL GRUBO MLJEVENA 100G; spar: ZAČ.SOL MORSKA VEG.MAES.100 g; bure: SOL MORSKA 100 g KRUNA PODR.; djelo_vodice: MORSKA SOL GRUBO MLJEVENA VEGETA MAESTRO BOČICA 100G |
| papar | 9001414440834 | 86,00 | 14,00 | plodine: SPICES DRINKS PAPAR CRVENI ZRNO 25 G; ntl: ZAČIN ZA KOKTELE SPICES & DRINKS PAPAR CRVENI 25 g KOTANYI; spar: ZAČIN PAPAR CRVENI ZRNO 25 g; lorenco: PAPAR CRVENI ZRNO KOKTEL SND ST 100; gavranovic: KOTANYI PAPAR CRVENI ZRNO 25g SPICE DRINKS; vrutak: KOTANYI KOKTEL PAPAR CRVENI SPICE i DRINKS 25G ZRNO; konzum: PAPAR CRVENI ZRNO S&D 25g KONTAYI |
| kiseli_kupus | 3859891493098 | 56,00 | 11,00 | gavranovic: ZELJE KISELO MIX ZA SARMU 1KG MADIG; spar: KUPUS KIS.MIX ZA SARMU 1 kg; lorenco: MADIG MIX ZA SARMU 1000g; eurospin: KUPUS KISELI MIX ZA SARMU 1kg; studenac: KIS. ZELJE MIX ZA SARMU 1100 g; tommy: KUPUS KIS. MIX ZA SARMU 1000 g; trgovina-krk: KUPUS KISELI MIX MADIG ZA SARMU 1 kg NTL; konzum: KUPUS KISELI MIX ZA SARMU MADIG; plodine: SARMA MIX 1 KG KISELI KUPUS MADIG |
| senf | 5949040202058 | 59,00 | 24,00 | studenac: KREK. ELEPHANT SENFLUK 70 g; ntl: TRAJNO SLANO PECIVO ELEPHANT 70 g MED,SENF I LUK; kaufland: Elephant slano pecivo med senf i luk 70g; plodine: SNACK MED/SENF/LUK 70 G ELEPHANT; spar: KRE.ELEPHANT SENF&MED&LUK 70 g; konzum: KREKER MED I SENF 70 g ELEPHANT; ktc: ELEPHANT MED,SENF I LUK 70g; lorenco: ALKA ELEPH.TS PECIVO 70g; djelo_vodice: ELEPHANT TRAJNO SLANO PECIVO - MED, SENF i LUK 70g; trgovina-krk: ELEPHANT TRAJNO SLANO PECIVO - MED,SENF I LUK 70 g; vrutak: ELEPHANT 70G TRAJNO SLANO PECIVO ALKA MED, SENF, LUK; branka: PECIVO ALKA ELEPHANT MED-SENF-LUK 70g; ribola: KREK.MED SEN.LU.70 g ELEPHANT; metro: 70G ELEPHANT FLAT MED SENF LUK; boso: KREKE ELEPHANT 70 g MED SENF LUK; jadranka_trgovina: GRICKALICE ELEPHANT MED, SENF I LUK 70G; tommy: SNACK MED SENF LUK 70 g ELEPHA |
| sol | 3870009000144 | 80,00 | 20,00 | vrutak: SOL KAMENA 250G SOLJENKA -15/1- TUZLA; spar: SOL KUHINJ. TUZLA SITNA 250 g; kaufland: Tuzla kuhinjska sol jodirana 250g; ktc: SOL KAMENA DOZA 250g TUZLA; plodine: SOL KUHINJSKA JODIRANA 250 G TULJAK TUZLA |
| maslac | 3856015325419 | 86,00 | 14,00 | branka: MARGARIN MARGO MASLAC 225g; kaufland: Margo Namaz miješani s maslacem 225g; plodine: MARGO S MASLACEM 225 G ZVIJEZDA; konzum: MARGO S MASLACEM 225g; lorenco: MARGO S MASLACEM 225G ZVIJEZDA; boso: MARG. MARGO 225 g S MASLACEM; tommy: MARGO S MASLACEM 225 G; ktc: MARGO S MASLACEM 225g ZVIJEZDA; trgovina-krk: MARGO S MASLACEM 225 gr; stridon: MARGO S MASLACEM 225 g ZVIJEZDA (16); trgocentar: MARGO S MASLACEM 225G (16),ZVIJEZDA; vrutak: N-MARGO S MASLACEM 225G -16/1-; spar: NAMAZ MARGO S MASLACEM 225 g; jadranka_trgovina: MARGARIN MARGO S MASLACEM 225G ZVIJEZDA |
| majoneza | 3856015324689 | 81,00 | 14,00 | zabac: CHILI MAJONEZA 75% 85 G; stridon: MAJONEZA ČILI ZVIJEZDA 85 g (25); trgovina-krk: MAJONEZA ČILI 85G; konzum: MAJONEZA ČILI PVC 85g ZVIJEZDA; boso: MAJON ZVIJE 85 g DELIK.ČILI; jadranka_trgovina: MAJONEZA 85G ČILI VREĆICA ZVIJEZDA; studenac: MAJONEZA ČILI 85g ZVIJ.; branka: MAJONEZA ČILI 85g; djelo_vodice: ČILI MAJONEZA 85g; gavranovic: MAJONEZA CHILLI VREĆICA 85g ZVIJEZDA; vrutak: N-MAJONEZA ZVIJEZDA 85G -25/1 ČILI; roto: MAJONEZA ČILI PVC 85g ZVIJEZDA (25); lorenco: ZVIJEZDA MAJONEZA ČILI 85G; metro: 85G ZVIJEZDA MAJONEZA ČILI; trgocentar: MAJONEZA ČILI 85G ,ZVIJEZDA; ribola: MAJONEZA ČILI 85 g ZVIJEZDA; spar: MAJONEZA CHILI ZVIJEZDA 85 g; kaufland: Zvijezda majoneza čili 85 g; tommy: MAJONEZA ČILI 85 G ZVIJEZDA; ktc: MAJONEZA ČILI 85g ZVIJEZDA; lidl: Zvijezda Majoneza Čili |
| senf | 5949040204953 | 60,00 | 10,00 | ribola: PERECI ME.SE.LU.75 g ELEPHANT; ntl: TRAJNO SLANO PECIVO ELEPHANT PRETZEL 75 g MED, SENF I LUK; gavranovic: PECIVO KOMADIĆI MED,SENF I LUK 75g ELEPHANT; konzum: PER LOMLJ MED SENF LUK 75 g ELEPHANT; ktc: ELEPHANT KOMADIĆI MED,SENF I LUK 75g; kaufland: Elephant Komadići med,senf i luk75g; stridon: ALKA ELEPHANT TS PECIVO-KOMAD.S OKUS.MEDA 14\*75 g; plodine: PEREC KOMADICI S OKUSOM MEDA,SENFA I LUKA 75 G ELEPHANT; tommy: SNACK MED SENF LUK 75 g ELEPHA; boso: KREKE ELEPHANT 75 g MED SENF LUK |
| sol | 3856020267216 | 83,00 | 17,00 | plodine: VEGETA MAESTRO SITNA MORSKA SOL POSIPAC 110 G BOCICA; lorenco: VEGETA MAESTRO SITNA MORSKA SOL; bure: VEGETA MAESTRO 110g SITNA SOL; spar: ZAČ.V.MAEST.SITNA MOR.SOL 110g; tommy: VEGETA MAESTRO SITNA MORSKA SOL POSIPAČ 110 g; konzum: SOL SITNA MORSKA 110g VEGETA MAESTRO |
| majoneza | 3856015304339 | 86,00 | 14,00 | trgocentar: MAJONEZA CHILI 165G TUBA (12) ZVIJEZDA; stridon: MAJONEZA ČILI TUBA 165 g (12) ZVIJEZDA; konzum: MAJONEZA ČILI 165g ZVIJEZDA; lorenco: ZVIJEZDA ČILI MAJONEZA 165g; branka: MAJONEZA ČILI 165g; roto: MAJONEZA ČILI 165G ZVIJEZDA (12); studenac: MAJONEZA ZV. 165G ČILI TUBA; vrutak: N-MAJONEZA ZVIJEZDA 165G -12/1 ČILI TUBA; plodine: MAJONEZA CILI 165 G TUBA ZVIJEZDA; kaufland: Zvijezda čili majoneza tuba 165g; gavranovic: MAJONEZA CHILLI 165g ZVIJEZDA; trgovina-krk: MAJONEZA ČILI 165 g ZVIJ; ktc: MAJONEZA TUBA ČILI 165g ZVIJEZDA; jadranka_trgovina: MAJONEZA 165G ČILI TUBA ZVIJEZDA |
| kukuruz | 3859893512254 | 70,00 | 30,00 | studenac: KUKURUZ PEČ.SL. NATURA 60 g; lorenco: KUKURUZ PEČENI SALNI BBQ 60g S.SNAC; spar: KUKURUZ PEČ.SLANI NATURA 60 g; plodine: KUKURUZ PECENI SLANI BBQ 60 G SUPER SNACK NATURA; gavranovic: KUKURUZ PEČENI SLANI BBQ 60g NATURA; trgocentar: KUKURUZ PEČENI SLANI 60G BBQ SUPER SNACK; trgovina-krk: KUKURUZ PS BBQ NATURA 60 g; vrutak: N-KUKURUZ NATURA 60G PEČENI SLANI BBQ -20/1- SUPER SNACK; jadranka_trgovina: KUKURUZ PEČENI SLANI BBQ 60G; ribola: KUKURUZ PEČENI 60 g SLANI NATURA |
| papar | 9001414274057 | 80,00 | 20,00 | plodine: SPICES DRINKS PAPAR CRNI, ZRNO 50 G; spar: ZAČ. PAPAR S&D CRNI ZRNO 50 g; ntl: ZAČIN ZA KOKTELE SPICES & DRINKS PAPAR CRNI 50 g KOTANYI; lorenco: PAPAR CRNI ZRNO SiD STAKLO 100ML; kaufland: Kotany papar crni zrno, bočica 50 g |
| papar | 9001414050026 | 54,00 | 46,00 | tommy: ZAČIN PAPAR ZEL/SAL. 100 g KOT; trgocentar: KOTANY ZELENI PAPAR U ZRNU 100G; djelo_vodice: PAPAR ZEL.SALAMURA; spar: ZAČ.PAPAR ZELEN.KOTANYI 100 g; trgovina-krk: PAPAR ZELENI U SALAMURI 100 g KOTAN; ribola: PAPAR ZEL.SAL. 100 g KOTANYI; bure: PAPAR ZELENI 100 g SALAMURA UG.; vrutak: KOTANYI 100G PAPAR ZELENI USALAMURI -24/1-; roto: PAPAR ZELENI U SALAMURI 100g KOTANYI (24); lorenco: ZELENI PAPAR 100 g KOTANYI; metro: 100G KOTANYI PAPAR ZELENI U SA; studenac: ZAČIN PAPAR ZELENI U SALAMURI 100 g KO; gavranovic: KOTANYI PAPAR ZEL.U SALAMURI 100g |
| papar | 9001414040867 | 60,00 | 10,00 | vrutak: KOTANYI 40G PAPAR ŠARENAMJEŠAVINA STAKLO -4/1-; plodine: PAPAR MIX 40 G STAKLO KOTANYI; gavranovic: KOTANYI PAPAR MJEŠAVINA STAKLO 40g; trgovina-krk: ZAČIN MJEŠAVINA PAPRA STAKLO 40 g KOTANY; branka: \*NE\*PAPAR MJEŠAVINA 35G STAKLO KOTANYI; spar: ZAČ.PAPAR MJEŠ.KOTANYI 40 g; studenac: ZAČIN PAPAR ŠARENI 40 g KOT.; tommy: ZAČIN PAPAR MJEŠ.40 g KOTANY; lorenco: ZAČIN MJEŠ. PAPRA 35 g KOTANYI; bure: ZAČIN MJEŠ.PAPRA 100g |
| med | 5949040205158 | 73,00 | 18,00 | djelo_vodice: ELEPHANT TWIST - MORSKA SOL i MED 180G; ktc: ELEPHANT TWIST MORSKA SOL I MED 180g; kaufland: Elephant Pecivo sl.morska sol,med180 g; tommy: SNACK SOL MED 180 g ELEPHANT; gavranovic: PECIVO TWIST MORSKA SOL I MED 180g - ELEPHANT; spar: PECIV.ELEP.TWIST SOL-MED 180 g; ntl: TRAJNO PEC. ELEP.TWIST - MORSKA SOL I MED 180g; plodine: KREKER MORSKA SOL I MED 180 G ELEPHANT; konzum: KREKE TWIST SOL I MED 180 g ELEPHANT; metro: 180G ELEPHANT TWIST SOL I MED; ribola: KREK.M.SOL&MED 180 g ELEPHANT |
| piletina | 3850159113154 | 60,00 | 20,00 | ribola: GAVELINO VINDIJA; spar: PILE GAVELINO; konzum: PILE GAVELINO POD VINDIJA; studenac: PILE GAVELINO VINDIJA KOKA kg; plodine: GAVELINO PILE ZA PECENJE CEKIN (11315) |
| dodatak_jelima | 3856020228910 | 90,00 | 10,00 | plodine: VEGETA NATUR BURGER 30 G CLASSIC; tommy: VEGETA NATUR BURGER VR.30 g PO; stridon: VEGETA NATUR BURGER CLASSIC 30 g (18); kaufland: Vegeta Natur Grill Burger classic 30 g; trgocentar: VEGETA NATUR BURGER CLASSIC VR.30G (18) (PAL 252) PODRAVKA; bure: VEGETA VR.BURG. 30 gCLASSIC; konzum: ZAČIN BURGER CLASSIC VR 30g VEGETA NATUR; lorenco: VEGETA NATUR BURGER CLASSIC VR.30g; trgovina-krk: VEGETA NATUR BURGER CLASSIC 30 g VREĆICA POD; spar: ZAČIN VEGETA NATUR BURGER 30 g |
| pileca_prsa | 3856020257064 | 57,00 | 14,00 | ribola: ŠUNKA PILEĆA 60 g LINO PODRAVKA; ktc: PILEĆA PRSA 60g LINO; tommy: PILEĆA PRSA 60 G LINO NARESCI PODRAVKA; spar: PILEĆA PRSA LINO NJUPAL. 60 g; plodine: LINO PILECA PRSA 60 G PODRAVKA; stridon: LINO PILEĆA ŠUNKA 60 g (10) PODRAVKA; konzum: LINO PILEĆA PRSA 60 g |
| pileca_prsa | 3850159125034 | 78,00 | 17,00 | tommy: PILEĆA PRSA U OVIT.500 g VI; spar: PIL.PRSA U OVITKU VIN. 500 g; ntl: SALAMA PILEĆA PRSA U OVITKU 500 g KOKA; trgovina-krk: SALAMA PILEĆA PRSA U OVITKU 500 g VINDIJA; metro: 500GR CEKIN PIL PRSA U OVITKU; bure: PILEĆA PRSA OV.500 gCEKIN LOT:1726102801; stridon: PILEĆA PRSA U OVITKU 500 g VINDIJA 12503; kaufland: Cekin Pileća prsa u ovitku 500g; vrutak: N-VIN PIL.PRSA U OVITKU 500G-12/1- 12503; lorenco: PILEĆA PRSA 500g CEKIN; plodine: PILECA PRSA U OVITKU 500 G CEKIN (12503) VINDIJA; boso: PILEĆ KOKA 500 g PRSA U OVITKU; branka: SALAMA PILEĆA PRSA 500g; konzum: PRSA PILEĆA U OVITKU 500g VINDIJA; studenac: PILEĆA PRSA U OVITKU 500g; trgocentar: PILEĆA PRSA U OVITKU 500G; gavranovic: PILEĆA PRSA U OVITKU 500g CEKIN (12503); ktc: PILEĆA PRSA U OVITKU 500g KOKA |
| grah | 3083680001793 | 67,00 | 17,00 | vrutak: N-GRAH BIJELI BONDUELLE 400G S RAJČICOM; plodine: BRETONA BIJELI GRAH U UMAKU OD RAJCICE 430 G; konzum: GRAH BIJELI RAJČICA 430/200g BONDUELLE; spar: GRAH BONDUELLE BRETONA 430 g; lorenco: BONDUELLE BIJELI GRAH S RAJČ.400g; kaufland: Bonduelle Bretona 430g/200g |
| tuna | 8004030860025 | 57,00 | 29,00 | tommy: TUNA SALATA CUS CUS 2X160 G RIO MARE; lorenco: TUNA -COUS-COUS SAL.2\*160g BOWL.; kaufland: Rio Mare Insal.sal.tuna cous cous2x160g; konzum: TUNJ SALATA COUS COUS 2X160g RIO MARE; spar: TUNA SAL.RIO MARE COUS 2X160 g; metro: 160GX2 RIO MARE INSALA.CUS CUS; plodine: TUNA COUS-COUS SAL.2X160G BOWL |
| zobene_pahuljice | 8595054907761 | 67,00 | 25,00 | plodine: ZOBENE PAHULJICE SUMSKO VOCE 300 G BIOPLOD; ribola: PAHULJ.ZO.BO.300 g D OBRE PAHULJICE; vrutak: ZOBENE PAHULJICE 300G BERRIES; branka: PAHULJICE ZOBENE BERRIES 300g; tommy: ZOBENE PAH. ŠUM.VOĆE 300 g DOB; zabac: Dobre zobene pahuljice 300g BERRIES; kaufland: Dobre Pahuljice zobene bobič.voće 300g; spar: DOBRE ZOBENE PAH.BOB.VOĆ.300 g; konzum: PAHULJICE ZOBENE BERRIES 300g; lorenco: DOBRE ZOBENE PAHULJICE 300g BERRIES; ntl: PAHULJICE ZOBENE BERRIES 300 g DOBRE; gavranovic: ZOBENE PAHULJICE DOBRE BERRIES 300g |
| sol | 9001414040034 | 69,00 | 31,00 | djelo_vodice: HIMALAJSKA SOL 100ML; plodine: HIMALAJSKA SOL 120 G KOTANY BOCICA; ribola: SOL HIMALAJSKA 120 g STAKLO KOTANYI; bure: SOL HIMALAJSKA 100 ml STAKLO; spar: SOL HIMALAJ.SITNA KOTANY120 g; kaufland: Kotanyi himalajska sol 120 g bočica; studenac: ZAČIN HIMALAJSKA SOL 120 g KOT.; trgovina-krk: ZAČIN SOL HIMALAJSKA BOČICA KOTA; branka: SOL HIMALAJSKA BOČICA 120g; tommy: SOL HIMALAJSKA STAK. 120 g KOT; konzum: HIMALAJSKA SOL BOČ 120G KOTANYI; ktc: SOL HIMALAJSKA 100mL ST KOTANYI; lorenco: HIMALAJSKA SOL JODIRANA STAKLO 100 |
| tjestenina | 8008857300771 | 83,00 | 17,00 | jadranka_trgovina: TJESTENINA SPAGHETTI TAGLIATI 077 500G REGGIA; trgovina-krk: TJEST. TAGLIATI 500 g REGGIA NTL; ntl: TJESTENINA TAGLAITI 500g REGGIA; trgocentar: SPAGETTI TAGLIATI 77 (SITNI REZANCI) 500G PASTA REGGIA (24); ribola: TJ.SPAGHETTI 500 g TAGLIATI JUHA REGGIA; bure: TJ.FIDELINI 77 500 gREGGIA (SPAGET.TAGLI |
| sol | 9001414046241 | 75,00 | 25,00 | konzum: MORSKA SOL BOČ 120 g KOTANYI; bure: SOL SITNA 100ml STAKLO; spar: MORSKA SOL KOTANY 120g; plodine: MORSKA SOL 120 G BOCICA KOTANYI; kaufland: Kotanyi Sol morska sitna jodirana 120g; tommy: SOL MORSKA JODIRANA 120 g KOTAN; vrutak: KOTANYI 100ML MORSKA SOL SITNA STAKLO -4/1-; metro: 120G KOTANYI MORSKA SOL BOČICA |
| pileca_prsa | 3850159123306 | 59,00 | 35,00 | tommy: PILEĆA PRSA NARESCI 100 g; plodine: PILECA PRSA 100 G VINDIJA; trgocentar: PILEĆA PRSA 100G, VINDIJA; vrutak: VIN PILEĆA PRSA 100G; ribola: PIL.PRS.U OV.100 g VINDIJA; konzum: PRSA PILEĆA U OVITKU NAR 100g; lorenco: PILEĆA PRSA 100g; djelo_vodice: PILEĆA PRSA 100G VIN.; stridon: PILEĆA PRSA 100 g VINDIJA; jadranka_trgovina: SALAMA PILEĆA PRSA 100G CEKIN VINDIJA; kaufland: Cekin Pileća prsa 100 g; spar: PILEĆA PRSA 100 g; ktc: PILEĆA PRSA 100g VINDIJA; studenac: PIL. PRSA U OVIT. 10 0g VINDVAC; trgovina-krk: SALAMA PILEĆA PRSA 100 g VIND; ntl: SALAMA PRSA PILEĆA 100 g VINDIVAC; gavranovic: CEKIN PILEĆA PRSA NAREZAK 100g |
