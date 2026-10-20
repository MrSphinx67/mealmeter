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
| med | 400 | 27 | 55 | 368 |
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
| sol | 226 | 0 | 38 | 400 |
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
| parmezan | 8004225018828 | 50,00 | plodine: COPPA BUSTA 80 G FRATELLI PARMIGIANI CHIFFONADE; zabac: COPPA BUSTA GR.80 FP CHIFFONADE |
| tvrdi_sir | 3858888597962 | 25,00 | ribola: SIR TRA.BIL.400g ZDE NKA; konzum: SIR POLUT BILOGORSKI ZDENKA 400g; tommy: SIR TRAPIST BILOGOR. 400 g 1/5; vrutak: N-SIR ZDK BILOGORSKI 400G; studenac: SIR BILOGORSKI TRAP. ZDENKA 400 g; spar: SIR BILOGSKI TRAPIST ZDE.400 g; ktc: SIR BILOGORSKI 400g ZDENKA; plodine: SIR BILOGORSKI 400 G ZDENKA |
| piletina | 3850159150227 | 43,00 | ntl: PILEĆA KRILA U PIKANTNOJ MARINADI 450 g; tommy: PIL.KRILA U PIKA.MARIN. 450 g; trgovina-krk: PILEĆA KRILA U PIK. MARINADI 450 g VIND; spar: PILEĆA KRILA PIKANTNA 450 g; studenac: PIL.KRILA U PIKANTNOJ MAR.450g; konzum: PIL KRILA U PIKANTNOJ MARINADI 450g VINDIJA; lorenco: PIL.KRILA U PIKAN.MARINADI 450g |
| jogurt | 3850354017684 | 25,00 | tommy: SENSIA FIBERS SMOKVA JABUKA AKACIJA 500 g; ribola: JOG.500g SM/JAB/AK SENSIA FIBERS; stridon: SENSIA FIBERS SMOKVA JABUKA AKACIJA 500g 13792; lorenco: SENSIA FIBERS SMOKVA JABUKA |
| mljevena_paprika | 3858881731783 | 50,00 | gavranovic: PAPRIKA SLATKA DERMA 80g DOZA LIM.; ntl: PAPRIKA ZAČINSKA 80 g POSIPAČ DERMA |
| jogurt | 3850354000181 | 33,00 | trgocentar: B.AKTIV JOGURT 150G 1,5%MM (20) DUKAT; roto: JOGURT B AKTIV LGG NATUR 150g DUKAT (20); boso: JOGUR DUKAT 150 g B\*AKTIV NATUR; lidl: b.Aktiv s LGG natur, 150g; lorenco: BIOAKTIV LGg 150 g; dukat: B.AKTIV LGG NATUR 150 g |
| rajcica_konzerva | 8005110170300 | 50,00 | metro: 400GX3 MUTTI RAJČICA SITNO SJE; spar: RAJČICA SJEC.SIT.MUTTI 3X400 g |
| mljevena_paprika | 8001060008403 | 40,00 | plodine: UMAK RAJC/LJUTA PAPRIKA 350 G SACLA; lorenco: SCALA UMAK CHERRY RAJ.I LJUT.PAPRIK; vrutak: UMAK CHERRY RAJČICA I LJUTA PAPRIKA 350G SACLA -6/1-; spar: UMAK SACLA ARRABBIATA 350 g; kaufland: Sacla Umak cher.rajčice i lj.papri.350g |
| tjestenina | 3859889154512 | 40,00 | kaufland: Ragusa Fidelini domaći s jajima 400 g; plodine: TJESTENINA DOMACI FIDELINI 400 G RAGUSA VRECICA; branka: TJESTENINA DOMAĆI FIDELINI 400g RAGUSA; lorenco: FIDELINI DOMAĆI 400g; ktc: DOMAĆI FIDELINI 400g RAGUSA SITNI |
| riza | 3858893691716 | 33,00 | boso: RIŽINI LISTIĆI 500g ŠAFRAM; ktc: POHA RIŽINI LISTIĆI 500g; spar: LISTIĆI RIŽE POHA ŠAFRAM 500 g |
| tvrdi_sir | 8717545620236 | 50,00 | plodine: SIR NAREZAK 150 G OLD AMSTERDAM; konzum: SIR TVRDI OLD AMST REZ 150g VELDZUYZEN |
| tjestenina | 5948935000236 | 50,00 | lorenco: KUKURUZNA TJESTENINA BG-COR.RIg 500; trgocentar: PASTA D'ORO CORNETTI RIGATI 500G (12) BEZ GLUTENA |
| tvrdi_sir | 4770299390583 | 25,00 | ribola: SIR DZIUGAS 100g 12 MJ.; studenac: SIR DŽIUGAS 40% M.M. KOCKICE 100 g; konzum: SIR TVRDI KOCKICE 12mj100g DŽIUGAS; tommy: SIR SNACK DŽIUGAS 100 g |
| med | 5027324001860 | 40,00 | spar: SLA.MOCHI PIST. LITTLE M.192 g; kaufland: Little Moons Sladoled Mochi pistac.6x32g; konzum: SLAD MOCHI PISTAC LITTLE MOONS 6x32g; tommy: SLADOLED MED/PISTACIO MOCHI 6X32 g; plodine: MOCHI SLADOLED MED/PRZENA PISTACIJA 6 X 32G LITTLE MOONS |
| tvrdi_sir | 8002710412007 | 43,00 | konzum: SIR TVRDI GRANA PADANO 200g ZANETTI; trgovina-krk: SIR GRANA PADANO 200g ZANETTI; roto: SIR TVRDI GRANA PADANO 200g ZANETTI (25); djelo_vodice: SIR GRANA PADANO 200G; plodine: SIR GRANA PAD.200 G ZANETTI; jadranka_trgovina: SIR TVRDI GRANA PADANO 15M 200G ZANETTI; ntl: SIR GRANA PADANO 200 g ZANETTI |
| tvrdi_sir | 3228023910039 | 25,00 | tommy: SIR EMENTAL 250 g PRESIDENT; plodine: EMENTALER PRESIDENT 250 G DUKAT; trgocentar: PRESIDENT EMENTALER 250G, DUKAT; spar: SIR EMMENTAL PRESIDENT 250 g; ktc: SIR PRESIDENT EMENTALER 250g; studenac: SIR EMMENTAL PRESID. 250 g; vrutak: SIR PRESIDENT EMENTALER 250G -12/1-; ribola: SIR EMEN.250 g PRESI; konzum: SIR TVRDI EMENTAL PRES 250g DUKAT; trgovina-krk: SIR PRESIDENT EMENTALER 250 g DUKAT; ntl: SIR EMENTALER PRESIDENT 250 g DUKAT; kaufland: President sir Ementaler 250g |
| jogurt | 3850108036695 | 50,00 | branka: JOGURT FORTIA JAG GROŽĐE RIBIZ 200g; ktc: FORTIA JAG.-GRO.C.RIB.200g |
| dodatak_jelima | 3859892109783 | 50,00 | trgovina-krk: ZAČIN MOJ ZAČIN 400 g ŠAFRAM; trgocentar: MOJ ZAČIN 400G DODATAK JELIMA S POVRĆEM, ŠAFRAM (12); ktc: MOJ ZAČIN 400g; spar: DODAT.JELIMA S POVRĆEM 400 g; plodine: DODATAK JELIMA MOJ ZACIN 400 G VRECICA SAFRAM; branka: MOJ ZAČIN DODATAK JELIMA S POVRĆEM 400g |
| palenta | 3856003914595 | 50,00 | boso: KRUP. TOJETO 750 g KUKURUZNA; trgovina-krk: KRUPICA KUKURUZNA 0,75 NTL; ntl: KUKURUZNA KRUPICA 750 g TOJETO; gavranovic: KUKURUZNA KRUPICA 750g TO JE TO |
| kiselo_vrhnje | 3870085020432 | 50,00 | studenac: VRHNJE ZA SV. SIR 850 g 22,5% mm ME; plodine: KISELO VRHNJE 20,5% 850 G MEGGLE |
| tvrdi_sir | 3856003927151 | 25,00 | trgovina-krk: SIR EMENTALER TO JE TO 100 g NTL ZDEN; ntl: SIR EMENTALER REZANI 100 g TOJETO; gavranovic: SIR TOJETO EMENTALER 100g LISTIĆI; boso: SIR TOJETO 100 g EMMENTALER |
| grasak | 3838977044508 | 25,00 | kaufland: Poli Salama od graška Green 220g; studenac: POLI GREEN MINI 220 g; ribola: POLI GREEN 220 g PER UTNINA; tommy: POLI GREEN MINI 220 g |
| cokolada_za_kuhanje | 8445290908087 | 40,00 | plodine: COKOLADA ZA KUHANJE BLANC 180 G DESSERT; spar: ČOKO.NESTLE ZA KUH.BLANC 170 g; metro: 170G NESTLE DESSERT BLAC; zabac: NESTLE DESSERT White 170g; konzum: ČOKOLADA ZA KUH DESSERT BIJELA 170 g |
| vrhnje_za_kuhanje | 8600005011159 | 50,00 | branka: KREMA ZA KUHANJE 1L; trgocentar: VRHNJE ZA KUHANJE 1L |
| tjestenina | 8009452222499 | 50,00 | metro: 500G RUSTICHELLA T.AL NERO SEPPIA; bure: TJ.TONNARELLI 500 g NERO DI SEPPIA |
| med | 3870545000080 | 50,00 | kaufland: Vitaminka Krastavac med i paprika 540g; stridon: KRASTA. S MEDOM I PAP. OC.MASA 290G 540G VITA. (6); djelo_vodice: KRASTAVAC S MEDOM I PAPRIKOM 540g; spar: KRAST.VITAMIN. MED PAPR.540 g |
| vrhnje_za_kuhanje | 8000005048405 | 25,00 | trgocentar: VRHNJE ZA KUHANJE 1L ,EURO ALFA; branka: -VEGETALCREM ZA KUHANJE 1L; lorenco: VEGETALCREAM FOR COOKINg 1L; ntl: PRIPRAVAK ZA KUHANJE S BILJNOM MASTI 23 %1000 ml VEGETALCREM |
| ocat | 80127314 | 33,00 | stridon: CITRES LUK SREDNJI U OCTU 1550 g; metro: 1550G CITRES LUK SREDNJI OCAT; bure: LUK 1550 g SREDNJI CITRES |
| pileca_prsa | 3850159113383 | 40,00 | trgovina-krk: PILEĆI ODRESCI OD FILEA PRSIJU 400 g VIND; vrutak: N-VIN.PIL.ODRESCI 400G OD FILEA PRSIJU; konzum: ODRESCI PILEĆEG FILE OD PRSA 400g; ntl: PILEĆI ODRESCI OD FILE-A PRSIJU 400 g VINDIJA; ribola: PIL.ODRE.FIL.400 g VNDIJA; gavranovic: CEKIN PILEĆI ODRESCI OD FILEA PRSIJU 400g; djelo_vodice: VIN.ODRESCI FILE PRSIJU 400G; lorenco: ODRESCI PILEĆEg FILEA OD PRSA 400g; metro: 400GR ODRESCI PILEĆEG FILEA; tommy: PILEĆI ODR./FILE PRSIJU 400 g; plodine: PILECI ODRESCI FILEA 400 G VINDIJA; studenac: ODRES. PIL.FILEA OD PRSA 400g; spar: PILEĆI ODRESCI OD FILEA 400 g; trgocentar: PILEĆI FILE OD PRSA 400G,VINDIJA; kaufland: Cekin odresci pilećeg filea od prsa 400g |
| majoneza | 8715700034614 | 50,00 | bure: MAJON. HEINZ 2,15 l; metro: 2,15L HEINZ MAJONEZA |

30 grupa koje prelaze iz člana (2D) u `ambiguous`:

| namirnica | grupa | m % | x % | nazivi po lancu |
|---|---|---|---|---|
| zobene_pahuljice | 8595054907761 | 67,00 | 25,00 | lorenco: DOBRE ZOBENE PAHULJICE 300g BERRIES; kaufland: Dobre Pahuljice zobene bobič.voće 300g; tommy: ZOBENE PAH. ŠUM.VOĆE 300 g DOB; zabac: Dobre zobene pahuljice 300g BERRIES; plodine: ZOBENE PAHULJICE SUMSKO VOCE 300 G BIOPLOD; ribola: PAHULJ.ZO.BO.300 g D OBRE PAHULJICE; spar: DOBRE ZOBENE PAH.BOB.VOĆ.300 g; konzum: PAHULJICE ZOBENE BERRIES 300g; gavranovic: ZOBENE PAHULJICE DOBRE BERRIES 300g; ntl: PAHULJICE ZOBENE BERRIES 300 g DOBRE; branka: PAHULJICE ZOBENE BERRIES 300g; vrutak: ZOBENE PAHULJICE 300G BERRIES |
| med | 5949040205158 | 73,00 | 18,00 | kaufland: Elephant Pecivo sl.morska sol,med180 g; ktc: ELEPHANT TWIST MORSKA SOL I MED 180g; ribola: KREK.M.SOL&MED 180 g ELEPHANT; spar: PECIV.ELEP.TWIST SOL-MED 180 g; ntl: TRAJNO PEC. ELEP.TWIST - MORSKA SOL I MED 180g; plodine: KREKER MORSKA SOL I MED 180 G ELEPHANT; djelo_vodice: ELEPHANT TWIST - MORSKA SOL i MED 180G; konzum: KREKE TWIST SOL I MED 180 g ELEPHANT; metro: 180G ELEPHANT TWIST SOL I MED; gavranovic: PECIVO TWIST MORSKA SOL I MED 180g - ELEPHANT; tommy: SNACK SOL MED 180 g ELEPHANT |
| majoneza | 3856015304339 | 86,00 | 14,00 | trgovina-krk: MAJONEZA ČILI 165 g ZVIJ; kaufland: Zvijezda čili majoneza tuba 165g; plodine: MAJONEZA CILI 165 G TUBA ZVIJEZDA; studenac: MAJONEZA ZV. 165G ČILI TUBA; vrutak: N-MAJONEZA ZVIJEZDA 165G -12/1 ČILI TUBA; branka: MAJONEZA ČILI 165g; lorenco: ZVIJEZDA ČILI MAJONEZA 165g; jadranka_trgovina: MAJONEZA 165G ČILI TUBA ZVIJEZDA; ktc: MAJONEZA TUBA ČILI 165g ZVIJEZDA; gavranovic: MAJONEZA CHILLI 165g ZVIJEZDA; stridon: MAJONEZA ČILI TUBA 165 g (12) ZVIJEZDA; trgocentar: MAJONEZA CHILI 165G TUBA (12) ZVIJEZDA; konzum: MAJONEZA ČILI 165g ZVIJEZDA; roto: MAJONEZA ČILI 165G ZVIJEZDA (12) |
| piletina | 3850159142321 | 77,00 | 15,00 | ribola: PIL.KRIL.BUCK. 500 gVINDIJA; stridon: CEKIN KRILCA BUCKET 500 g 14232 VINDIJA; boso: KRILCA CEKIN 500 g BUCKET; spar: PILE.KRILCA BUCKET CEKIN 500 g; trgocentar: CEKIN KRILCA BUCKET 500G; ktc: CEKIN KIDS BUCKET KRILCA 500g; ntl: KRILCA PILEĆA PEČENA SM 500 g CEKIN; trgovina-krk: CEKIN KRILCA BUCKET 500G; jadranka_trgovina: KRILCA BUCKET CEKIN 500G VINDIJA; kaufland: Cekin Pečena pileća krilca 500 g; branka: KRILCA BUCKET CEKIN 500g; plodine: CEKIN KRILCA BUCKET 500 G; vrutak: N-VIN KRILCA BUCKET 500G -4/1- |
| sol | 3856020222314 | 80,00 | 20,00 | stridon: VEGETA MAESTRO MORSKA SOL M.100 G (6) PODRAVKA; ribola: SOL MORSKA 100 g VE GETA MAESTRO; ktc: MORSKA SOL GRUBO MLJEVENA 100g PODRAVKA; bure: SOL MORSKA 100 g KRUNA PODR.; djelo_vodice: MORSKA SOL GRUBO MLJEVENA VEGETA MAESTRO BOČICA 100G; konzum: ZAČIN SOL MORSKA ML 100g VEGETA MAESTRO; lorenco: VEGETA MAESTRO MORSKA SOL 100G; plodine: MORSKA SOL MLINAC 100 G VEGETA MAESTRO; spar: ZAČ.SOL MORSKA VEG.MAES.100 g; tommy: VEGETA MAESTRO MORSKA SOL GRUBO MLJEVENA 100G |
| papar | 9001414274057 | 80,00 | 20,00 | kaufland: Kotany papar crni zrno, bočica 50 g; lorenco: PAPAR CRNI ZRNO SiD STAKLO 100ML; spar: ZAČ. PAPAR S&D CRNI ZRNO 50 g; ntl: ZAČIN ZA KOKTELE SPICES & DRINKS PAPAR CRNI 50 g KOTANYI; plodine: SPICES DRINKS PAPAR CRNI, ZRNO 50 G |
| sol | 3870009000144 | 80,00 | 20,00 | ktc: SOL KAMENA DOZA 250g TUZLA; kaufland: Tuzla kuhinjska sol jodirana 250g; spar: SOL KUHINJ. TUZLA SITNA 250 g; vrutak: SOL KAMENA 250G SOLJENKA -15/1- TUZLA; plodine: SOL KUHINJSKA JODIRANA 250 G TULJAK TUZLA |
| maslac | 3856015325419 | 86,00 | 14,00 | spar: NAMAZ MARGO S MASLACEM 225 g; trgocentar: MARGO S MASLACEM 225G (16),ZVIJEZDA; vrutak: N-MARGO S MASLACEM 225G -16/1-; tommy: MARGO S MASLACEM 225 G; ktc: MARGO S MASLACEM 225g ZVIJEZDA; plodine: MARGO S MASLACEM 225 G ZVIJEZDA; konzum: MARGO S MASLACEM 225g; stridon: MARGO S MASLACEM 225 g ZVIJEZDA (16); trgovina-krk: MARGO S MASLACEM 225 gr; branka: MARGARIN MARGO MASLAC 225g; kaufland: Margo Namaz miješani s maslacem 225g; jadranka_trgovina: MARGARIN MARGO S MASLACEM 225G ZVIJEZDA; boso: MARG. MARGO 225 g S MASLACEM; lorenco: MARGO S MASLACEM 225G ZVIJEZDA |
| tjestenina | 8008857300771 | 83,00 | 17,00 | trgocentar: SPAGETTI TAGLIATI 77 (SITNI REZANCI) 500G PASTA REGGIA (24); bure: TJ.FIDELINI 77 500 gREGGIA (SPAGET.TAGLI; ribola: TJ.SPAGHETTI 500 g TAGLIATI JUHA REGGIA; trgovina-krk: TJEST. TAGLIATI 500 g REGGIA NTL; ntl: TJESTENINA TAGLAITI 500g REGGIA; jadranka_trgovina: TJESTENINA SPAGHETTI TAGLIATI 077 500G REGGIA |
| papar | 9001414040867 | 60,00 | 10,00 | branka: \*NE\*PAPAR MJEŠAVINA 35G STAKLO KOTANYI; gavranovic: KOTANYI PAPAR MJEŠAVINA STAKLO 40g; plodine: PAPAR MIX 40 G STAKLO KOTANYI; bure: ZAČIN MJEŠ.PAPRA 100g; studenac: ZAČIN PAPAR ŠARENI 40 g KOT.; tommy: ZAČIN PAPAR MJEŠ.40 g KOTANY; lorenco: ZAČIN MJEŠ. PAPRA 35 g KOTANYI; spar: ZAČ.PAPAR MJEŠ.KOTANYI 40 g; vrutak: KOTANYI 40G PAPAR ŠARENAMJEŠAVINA STAKLO -4/1-; trgovina-krk: ZAČIN MJEŠAVINA PAPRA STAKLO 40 g KOTANY |
| med | 4000521010294 | 63,00 | 31,00 | roto: MUESLI KNUSPER MED BADEM 300G VITALI (8); kaufland: Dr.Oetker vitalis crunchy med badem 300g; metro: 300G VITALIS CRUN PLUS MED/BAD; tommy: MUESLI CRUN.PL. MED 300 g DR.O; trgovina-krk: MUSLI CRUNCHY PLUS MED BADEM 300 g DR OETKER; bure: MUESLI VITALIS 300 gHONEY-ALMOND; ribola: MUESLI CHR.MED 300 g VITALIS DR OETKER; trgocentar: VITALIS CRUNCHY PLUS MED BADEM 300G, DR.OETKER; djelo_vodice: MUSLI CRUNCHY MED BADEM 300g; spar: MUSLI VITALIS MED,BADEM 300 g; vrutak: MUSLI DR OETKER 300G MED I BADEM CRUNCHY PLUS -8/1-; konzum: MUESLI KNUSPER MED BADEM 300g VITALI; lorenco: DR.OETKER CRUNCHY PLUS MED BADEM; plodine: MUSLI PLUS MED BADEM 300 G CRUNCHY DR OETKER; studenac: MUESLI MED BADEM VITALIS 300 g; jadranka_trgovina: MUESLI CRUNCHY PLUS MED BADEM 300G VITALIS |
| med | 5949040203482 | 63,00 | 25,00 | plodine: SNACK MORSKA SOL I MED 160 G ELEPHANT TWIST; ribola: KREK.M.SOL&MED 160 g ELEPHANT; djelo_vodice: ELEPHANT TWIST - MORSKA SOL i MED 160g; lorenco: ALKA ELEPHANT TWIST-SOL I MED 160g; ntl: TRAJNO PEC. ELEP.TWIST - MORSKA SOL I MED 160g; gavranovic: PECIVO TWIST MORSKA SOL I MED 160g - ELEPHANT; kaufland: Elephant Twist sl.pecivo m.sol i med160g; tommy: SNACK SOL MED 160 g ELEPHANT |
| kukuruz | 3859893512254 | 70,00 | 30,00 | trgocentar: KUKURUZ PEČENI SLANI 60G BBQ SUPER SNACK; trgovina-krk: KUKURUZ PS BBQ NATURA 60 g; vrutak: N-KUKURUZ NATURA 60G PEČENI SLANI BBQ -20/1- SUPER SNACK; gavranovic: KUKURUZ PEČENI SLANI BBQ 60g NATURA; plodine: KUKURUZ PECENI SLANI BBQ 60 G SUPER SNACK NATURA; studenac: KUKURUZ PEČ.SL. NATURA 60 g; lorenco: KUKURUZ PEČENI SALNI BBQ 60g S.SNAC; ribola: KUKURUZ PEČENI 60 g SLANI NATURA; jadranka_trgovina: KUKURUZ PEČENI SLANI BBQ 60G; spar: KUKURUZ PEČ.SLANI NATURA 60 g |
| grah | 3083680001793 | 67,00 | 17,00 | plodine: BRETONA BIJELI GRAH U UMAKU OD RAJCICE 430 G; kaufland: Bonduelle Bretona 430g/200g; vrutak: N-GRAH BIJELI BONDUELLE 400G S RAJČICOM; spar: GRAH BONDUELLE BRETONA 430 g; lorenco: BONDUELLE BIJELI GRAH S RAJČ.400g; konzum: GRAH BIJELI RAJČICA 430/200g BONDUELLE |
| tuna | 8004030860025 | 0,00 | 86,00 | kaufland: Rio Mare Insal.sal.tuna cous cous2x160g; konzum: TUNJ SALATA COUS COUS 2X160g RIO MARE; tommy: TUNA SALATA CUS CUS 2X160 G RIO MARE; metro: 160GX2 RIO MARE INSALA.CUS CUS; plodine: TUNA COUS-COUS SAL.2X160G BOWL; spar: TUNA SAL.RIO MARE COUS 2X160 g; lorenco: TUNA -COUS-COUS SAL.2\*160g BOWL. |
| senf | 5949040204953 | 60,00 | 10,00 | boso: KREKE ELEPHANT 75 g MED SENF LUK; tommy: SNACK MED SENF LUK 75 g ELEPHA; stridon: ALKA ELEPHANT TS PECIVO-KOMAD.S OKUS.MEDA 14\*75 g; gavranovic: PECIVO KOMADIĆI MED,SENF I LUK 75g ELEPHANT; ntl: TRAJNO SLANO PECIVO ELEPHANT PRETZEL 75 g MED, SENF I LUK; plodine: PEREC KOMADICI S OKUSOM MEDA,SENFA I LUKA 75 G ELEPHANT; ribola: PERECI ME.SE.LU.75 g ELEPHANT; kaufland: Elephant Komadići med,senf i luk75g; konzum: PER LOMLJ MED SENF LUK 75 g ELEPHANT; ktc: ELEPHANT KOMADIĆI MED,SENF I LUK 75g |
| tjestenina | 8710605028430 | 71,00 | 29,00 | plodine: TJESTENINA S JAJIMA GNIJEZDA 250 G NOODLES GO TAN; spar: TJESTENINA GOTAN NEST 250 g; kaufland: Go Tan tjest.s jajima za Wok 250 g; ribola: TJEST.GO TAN 250g; konzum: TJESTENINA S JAJIMA GNIJEZDA GO TAN 250g; vrutak: TJESTENINA GO-TAN 250G EGG WOK NOODLES -8/1-; ntl: TJESTENINA OD PŠ. BRAŠNA S JAJIMA 250G NIKAS |
| jaja | 5200701000063 | 67,00 | 17,00 | ribola: PEPPA PIG JAJE 10 g; trgovina-krk: SRCE JAJE PEPPA PIG 10G; studenac: BOM. JAJE PEPA PIG 10 g; konzum: JAJE S BOMBONIMA PEPA PIG 10g; ntl: JAJE IZNENAĐENJA 10 g MIX LICENCA; vrutak: SRCE PL. PEPPA PIG 10G |
| kiseli_kupus | 3859891493098 | 56,00 | 11,00 | tommy: KUPUS KIS. MIX ZA SARMU 1000 g; trgovina-krk: KUPUS KISELI MIX MADIG ZA SARMU 1 kg NTL; eurospin: KUPUS KISELI MIX ZA SARMU 1kg; spar: KUPUS KIS.MIX ZA SARMU 1 kg; lorenco: MADIG MIX ZA SARMU 1000g; plodine: SARMA MIX 1 KG KISELI KUPUS MADIG; gavranovic: ZELJE KISELO MIX ZA SARMU 1KG MADIG; konzum: KUPUS KISELI MIX ZA SARMU MADIG; studenac: KIS. ZELJE MIX ZA SARMU 1100 g |
| papar | 9001414050026 | 54,00 | 46,00 | roto: PAPAR ZELENI U SALAMURI 100g KOTANYI (24); vrutak: KOTANYI 100G PAPAR ZELENI USALAMURI -24/1-; lorenco: ZELENI PAPAR 100 g KOTANYI; metro: 100G KOTANYI PAPAR ZELENI U SA; ribola: PAPAR ZEL.SAL. 100 g KOTANYI; trgovina-krk: PAPAR ZELENI U SALAMURI 100 g KOTAN; djelo_vodice: PAPAR ZEL.SALAMURA; trgocentar: KOTANY ZELENI PAPAR U ZRNU 100G; gavranovic: KOTANYI PAPAR ZEL.U SALAMURI 100g; studenac: ZAČIN PAPAR ZELENI U SALAMURI 100 g KO; bure: PAPAR ZELENI 100 g SALAMURA UG.; tommy: ZAČIN PAPAR ZEL/SAL. 100 g KOT; spar: ZAČ.PAPAR ZELEN.KOTANYI 100 g |
| dodatak_jelima | 3856020228910 | 90,00 | 10,00 | bure: VEGETA VR.BURG. 30 gCLASSIC; stridon: VEGETA NATUR BURGER CLASSIC 30 g (18); tommy: VEGETA NATUR BURGER VR.30 g PO; spar: ZAČIN VEGETA NATUR BURGER 30 g; trgovina-krk: VEGETA NATUR BURGER CLASSIC 30 g VREĆICA POD; trgocentar: VEGETA NATUR BURGER CLASSIC VR.30G (18) (PAL 252) PODRAVKA; plodine: VEGETA NATUR BURGER 30 G CLASSIC; konzum: ZAČIN BURGER CLASSIC VR 30g VEGETA NATUR; lorenco: VEGETA NATUR BURGER CLASSIC VR.30g; kaufland: Vegeta Natur Grill Burger classic 30 g |
| sol | 3856020267216 | 83,00 | 17,00 | spar: ZAČ.V.MAEST.SITNA MOR.SOL 110g; lorenco: VEGETA MAESTRO SITNA MORSKA SOL; konzum: SOL SITNA MORSKA 110g VEGETA MAESTRO; plodine: VEGETA MAESTRO SITNA MORSKA SOL POSIPAC 110 G BOCICA; tommy: VEGETA MAESTRO SITNA MORSKA SOL POSIPAČ 110 g; bure: VEGETA MAESTRO 110g SITNA SOL |
| papar | 9001414440834 | 86,00 | 14,00 | vrutak: KOTANYI KOKTEL PAPAR CRVENI SPICE i DRINKS 25G ZRNO; konzum: PAPAR CRVENI ZRNO S&D 25g KONTAYI; plodine: SPICES DRINKS PAPAR CRVENI ZRNO 25 G; ntl: ZAČIN ZA KOKTELE SPICES & DRINKS PAPAR CRVENI 25 g KOTANYI; gavranovic: KOTANYI PAPAR CRVENI ZRNO 25g SPICE DRINKS; spar: ZAČIN PAPAR CRVENI ZRNO 25 g; lorenco: PAPAR CRVENI ZRNO KOKTEL SND ST 100 |
| majoneza | 3856015324689 | 81,00 | 14,00 | roto: MAJONEZA ČILI PVC 85g ZVIJEZDA (25); lorenco: ZVIJEZDA MAJONEZA ČILI 85G; metro: 85G ZVIJEZDA MAJONEZA ČILI; branka: MAJONEZA ČILI 85g; djelo_vodice: ČILI MAJONEZA 85g; gavranovic: MAJONEZA CHILLI VREĆICA 85g ZVIJEZDA; studenac: MAJONEZA ČILI 85g ZVIJ.; boso: MAJON ZVIJE 85 g DELIK.ČILI; jadranka_trgovina: MAJONEZA 85G ČILI VREĆICA ZVIJEZDA; trgovina-krk: MAJONEZA ČILI 85G; konzum: MAJONEZA ČILI PVC 85g ZVIJEZDA; tommy: MAJONEZA ČILI 85 G ZVIJEZDA; ktc: MAJONEZA ČILI 85g ZVIJEZDA; lidl: Zvijezda Majoneza Čili; vrutak: N-MAJONEZA ZVIJEZDA 85G -25/1 ČILI; stridon: MAJONEZA ČILI ZVIJEZDA 85 g (25); zabac: CHILI MAJONEZA 75% 85 G; kaufland: Zvijezda majoneza čili 85 g; ribola: MAJONEZA ČILI 85 g ZVIJEZDA; spar: MAJONEZA CHILI ZVIJEZDA 85 g; trgocentar: MAJONEZA ČILI 85G ,ZVIJEZDA |
| senf | 5949040202058 | 59,00 | 24,00 | ribola: KREK.MED SEN.LU.70 g ELEPHANT; metro: 70G ELEPHANT FLAT MED SENF LUK; kaufland: Elephant slano pecivo med senf i luk 70g; ntl: TRAJNO SLANO PECIVO ELEPHANT 70 g MED,SENF I LUK; tommy: SNACK MED SENF LUK 70 g ELEPHA; branka: PECIVO ALKA ELEPHANT MED-SENF-LUK 70g; trgovina-krk: ELEPHANT TRAJNO SLANO PECIVO - MED,SENF I LUK 70 g; vrutak: ELEPHANT 70G TRAJNO SLANO PECIVO ALKA MED, SENF, LUK; studenac: KREK. ELEPHANT SENFLUK 70 g; boso: KREKE ELEPHANT 70 g MED SENF LUK; jadranka_trgovina: GRICKALICE ELEPHANT MED, SENF I LUK 70G; djelo_vodice: ELEPHANT TRAJNO SLANO PECIVO - MED, SENF i LUK 70g; plodine: SNACK MED/SENF/LUK 70 G ELEPHANT; spar: KRE.ELEPHANT SENF&MED&LUK 70 g; konzum: KREKER MED I SENF 70 g ELEPHANT; ktc: ELEPHANT MED,SENF I LUK 70g; lorenco: ALKA ELEPH.TS PECIVO 70g |
| piletina | 3850159113154 | 60,00 | 20,00 | studenac: PILE GAVELINO VINDIJA KOKA kg; konzum: PILE GAVELINO POD VINDIJA; spar: PILE GAVELINO; plodine: GAVELINO PILE ZA PECENJE CEKIN (11315); ribola: GAVELINO VINDIJA |
| pileca_prsa | 3856020257064 | 57,00 | 14,00 | spar: PILEĆA PRSA LINO NJUPAL. 60 g; tommy: PILEĆA PRSA 60 G LINO NARESCI PODRAVKA; ribola: ŠUNKA PILEĆA 60 g LINO PODRAVKA; stridon: LINO PILEĆA ŠUNKA 60 g (10) PODRAVKA; konzum: LINO PILEĆA PRSA 60 g; plodine: LINO PILECA PRSA 60 G PODRAVKA; ktc: PILEĆA PRSA 60g LINO |
| med | 5900617037152 | 86,00 | 14,00 | kaufland: Sante Granola Gold med i oraš.plod.300g; jadranka_trgovina: ŽITARICE GRANOLA GOLD ORASI+MED 300G SANTE; spar: GRAN.SANTE ORAŠ.PLOD.MED 300 g; tommy: MUESLI GRAN. NUT/MED 300 g SAN; plodine: MUESLI GRANOLA MED I ORASASTI PLODOVI 300 G SANTE; ribola: GRANOLA 300 g ORAH/ MED SANTE; konzum: MUESLI GRANOLA ORAŠ PLOD MED 300g SANTE |
| sol | 9001414046241 | 75,00 | 25,00 | tommy: SOL MORSKA JODIRANA 120 g KOTAN; vrutak: KOTANYI 100ML MORSKA SOL SITNA STAKLO -4/1-; spar: MORSKA SOL KOTANY 120g; metro: 120G KOTANYI MORSKA SOL BOČICA; kaufland: Kotanyi Sol morska sitna jodirana 120g; plodine: MORSKA SOL 120 G BOCICA KOTANYI; bure: SOL SITNA 100ml STAKLO; konzum: MORSKA SOL BOČ 120 g KOTANYI |
| pileca_prsa | 3850159123306 | 59,00 | 35,00 | jadranka_trgovina: SALAMA PILEĆA PRSA 100G CEKIN VINDIJA; kaufland: Cekin Pileća prsa 100 g; stridon: PILEĆA PRSA 100 g VINDIJA; djelo_vodice: PILEĆA PRSA 100G VIN.; ribola: PIL.PRS.U OV.100 g VINDIJA; vrutak: VIN PILEĆA PRSA 100G; konzum: PRSA PILEĆA U OVITKU NAR 100g; lorenco: PILEĆA PRSA 100g; trgocentar: PILEĆA PRSA 100G, VINDIJA; gavranovic: CEKIN PILEĆA PRSA NAREZAK 100g; studenac: PIL. PRSA U OVIT. 10 0g VINDVAC; trgovina-krk: SALAMA PILEĆA PRSA 100 g VIND; ntl: SALAMA PRSA PILEĆA 100 g VINDIVAC; tommy: PILEĆA PRSA NARESCI 100 g; plodine: PILECA PRSA 100 G VINDIJA; spar: PILEĆA PRSA 100 g; ktc: PILEĆA PRSA 100g VINDIJA |

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
| med | 0 | 1 |
| sol | 0 | 1 |

30 nasumičnih vraćenih grupa:

| namirnica | razina | nazivi po lancu |
|---|---|---|
| tjestenina | strong | plodine: TJ.ELICOIDALI OPERA PRIMA 500 G VRECICA |
| tjestenina | strong | trgovina-krk: LAZANJE 1 KOM TK |
| tjestenina | strong | kaufland: OPG IK Rezanci s narančast.batatom 200g; spar: TJ.REZ.USKI NARANČ.BATAT 200 g |
| tvrdi_sir | strong | eurospin: SIR EMMENTAL JULIENNE 200g |
| tjestenina | strong | tommy: TJ.PENN. RIGATE 30 500 g ARRI |
| tjestenina | strong | spar: TJE.PREMIUM CRNI REZANCI 400 g |
| tjestenina | strong | ribola: TJ.ALBADORO 39 CONCH |
| tjestenina | strong | metro: 1KG MC LASAGNE S JAJIMA |
| tjestenina | strong | djelo_vodice: FUŽI KARLA; metro: 750G KARLA FUŽI |
| tjestenina | strong | trgovina-krk: REZANCI ZELENI ZA GASTRO 1 kg |
| tvrdi_sir | strong | konzum: SIR MAASDAM 300 g DELISO |
| tvrdi_sir | strong | dukat: PRESIDENT CHEDDAR MILD 200g; jadranka_trgovina: SIR CHEDDAR 200G MILD PRESIDENT DUKAT; lorenco: PRESIDENT CHEDDAR MILD 200g; plodine: SIR CHEDDAR MILD 200 G PRESIDENT DUKAT; spar: SIR CHEDDAR MILD PRESID.200 g; ktc: SIR CHEDDAR MILD 200g DUKAT; tommy: SIR CHEDDAR MILD 200 g PRESID; vrutak: N-SIR PRESIDENT CHEDDAR MILD 200G -8/1-; konzum: SIR POLU CHEDDAR MILD 200g; ribola: SIR CHED.MIL.200 g P RESIDENT |
| tjestenina | strong | plodine: DUCK MULTI ACT.38 G OSVJ.CITRUS ZA WC SKOLJKU |
| tjestenina | strong | kaufland: Farina brašno T-400 namj. za diz.tj.1kg |
| tjestenina | strong | branka: TJESTENINA REZANCI ŠIROKI JAJA 400g; tommy: TJ.ŠIROKI REZ. 400 g MARODI; stridon: ŠIROKI REZANCI S JAJIMA 400 g MARODI (8); vrutak: N-TJEST MARODI ŠIROKI REZANCI S JAJIMA 400G -8/1; plodine: SIROKI REZANCI 400 G MARODI; metro: 400G MARODI ŠIROKI REZ S JAJIM; studenac: TJ. MARODI Š.REZ.JAJA 400 g; trgovina-krk: TJEST. ŠIROKI REZANCI S JAJIMA 400 g MAROD; ribola: TJ.ŠIR REZANCI 400 g MARODI; bure: TJ.REZ. ŠIROKI 400 gG S JAJIMA MARODI; kaufland: Marodi široki rezanci s jajima 400 g; spar: TJES.MARODI REZAN.ŠIROKI 400 g; boso: TJEST MARODI 400 g ŠIR.REZ.S JAJ; jadranka_trgovina: TJESTENINA REZANCI ŠIROKI SA JAJIMA 400G MARODI; ktc: REZANCI ŠIROKI DOM.S JAJIMA 400g MARODI; lorenco: ŠIROKI REZANCI S JAJIMA MARODI 400G; trgocentar: MARODI ŠIROKI REZANCI S JAJIMA 400G (8) (PAL 24); roto: TIJESTO REZANCI ŠIR JAJ 400g MARODI (8); konzum: TIJESTO REZANCI ŠIR JAJ 400g MARODI; ntl: TJ.REZANCI ŠIROKI 400 g MARODI; gavranovic: TJ.MARODI 400g REZANCI ŠIROKI SA JAJIMA |
| tjestenina | strong | lorenco: GASTRO LASAGNE LEDO |
| jogurt | strong | kaufland: KLC.Muesli pločica marelica+jog.30g |
| svinjetina | strong | vrutak: N-SV. REBRA ZA ROŠTILJ MARINIRANA SVJEŽE |
| vrhnje_za_kuhanje | strong | plodine: VRH.KUH.2X500G BOCA DUKAT |
| pileca_prsa | strong | eurospin: FILE PIL.BAT.I ZAB. |
| jogurt | weak | lorenco: FORTIA JAG-GROŽ.-C.RIBIZ 1 kg TTOP; ribola: JOG.1kg J/G/C TT FORTIA; trgocentar: FORTIA JAGODA-GROŽĐE-CRNI RIBIZ 1KG |
| tjestenina | strong | konzum: TIJEST REZANCI JAJ MAXX 600 g KOLEDA |
| tjestenina | strong | lidl: Široki rezanci s jajima XXL |
| pileca_prsa | strong | kaufland: KPur. Pileći odresci file od prsa 400 g |
| tjestenina | strong | djelo_vodice: TJE.CETINA BR.67 FIDELINI GNIJEZDA |
| tjestenina | strong | spar: TJ.N.P.SPAGH.CRVENA LEĆA 250 g |
| tjestenina | strong | eurospin: REZANCI ZA JUHU S MRKV/JAJIMA 400g |
| tvrdi_sir | strong | bure: SIR CHEDDAR DUKAT LOT:18122026 |
| tjestenina | strong | lorenco: REZANCI USKI KLARA 500 g; plodine: TJ.REZANCI USKI 500 G KLARA VRECICA; trgocentar: REZANAC USKI 0,500KG (7), KLARA; vrutak: N-TJEST.KLARA ZP REZANCI USKI 500G -7/1- A60002; gavranovic: TJ.KLARA 500g REZANCI USKI; trgovina-krk: TIJ.REZANCI USKI 500G KLARA; tommy: TJ.REZANCI USKI 500 g KLARA |
| tvrdi_sir | strong | boso: SIR VINDI 150 g CHEDDAR; djelo_vodice: SIR CHEDDAR 150G VINDIJA; ktc: SIR CHEDDAR 150g VINDIJA MAP; vrutak: N-SIR VIN CHEDDAR 150G MAP -10/1-; jadranka_trgovina: SIR CHEDDAR SLICE MAP 150g VINDIJA; studenac: SIR CHEDDAR 150g MAP VINDIJA; kaufland: Vindija Sir Cheddar tvrdi45%mm150g; ntl: SIR CHEDDAR MAP 150 g VINDIJA; plodine: SIR NAREZAK CHEDDAR MAP 150 G VINDIJA; ribola: SIR CHEDDAR 150 g VI NDIJA; branka: SIR CHEDDAR 150g; konzum: SIR POLUTV CHEDDAR 150 g VINDIJA; lorenco: CHEDDAR 150g VINDIJA; trgovina-krk: SIR CHEDDAR 150G MAP; tommy: SIR CHEDDAR MAP 150 g VINDIJA; spar: SIR CHEDDAR VINDIJA MAP 150 g; trgocentar: SIR CHEDDAR 150G,VINDIJA; stridon: SIR CHEDDAR MAP 150G VINDIJA 5791 |
