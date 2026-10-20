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
| jabuka | 390 | 4 | 0 | 46 |
| jaja | 354 | 0 | 26 | 1091 |
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
| tuna | 472 | 0 | 43 | 217 |
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
| maslac | 3023470001015 | 33,00 | lorenco: LA GALETTE ALL BUTTER ST MICHEL 130; plodine: KEKS GALETTES 130 G BONNE MAMAN; studenac: KEKS GALETTES 130 g |
| svjezi_sir | 3850355007561 | 50,00 | stridon: PRESIDENT ZAGREBAČKI SIR BEZ LAKTOZE 220 g DUKAT; lidl: President Zag.svj. sir bez laktoze; ribola: SIR SV.ZAG.B.LA.220gPRESIDENT; plodine: SIR SVJEZI ZAGREBACKI 220 G PRESIDENT |
| tvrdi_sir | 3859892884413 | 33,00 | konzum: SIR TVRDI MEDITERANO 200 g PAŠKA SIR; lorenco: MEDITENO 200GR PAŠKA SIRANA; studenac: SIR MEDITERANO 200 g; tommy: SIR MEDITERANO 200 g PAŠKA SIRANA; jadranka_trgovina: SIR TVRDI MEDITERANO 200G PAŠKA SIRANA; ribola: SIR MEDITER.200 g PAŠKA |
| tvrdi_sir | 3859891700622 | 43,00 | jadranka_trgovina: SIR TVRDI OTOČAN 300G MIH; roto: SIR TVRDI OTOČAN 300g MIH (16); konzum: SIR TVRDI OTOČAN 300g MIH; plodine: SIR OTOCAN 1/8 300 G; studenac: SIR OTOČAN 300 g; ribola: SIR OTOČAN 300 g MIH; tommy: SIR OTOČAN 300 g MIH |
| slatko_vrhnje | 4034900027733 | 38,00 | lorenco: VRHNJE ZA ŠLAg 1000ML MEGGLE; spar: PRIP.ZA ŠLAG CREME PA.25% 1 L; kaufland: Creme Patisserie slatko vrhnje 25 % 1 l; roto: ŠLAG BRIK MEGGLE 1,0 (12); bure: VRHNJE ZA ŠLAG 1 kg MEGGL.LOT:270128; trgovina-krk: VRHNJE BILJNO PATISSERIE 25% B.M. 1L MEGGL; metro: 1L CREME PATISSERIE 25%; plodine: CREME PATISSERIE 1 L MEGGLE |
| tvrdi_sir | 8410285102733 | 50,00 | spar: SIR S TARTUFIMA PRESID.200 g; konzum: SIR POLUTV S TARTUFIMA 200 g PRESIDE |
| tjestenina | 3859888231023 | 50,00 | kaufland: Clarum fidelini sitni 400 g; ntl: TJEST.FIDELINI SITNI 400 g CLARUM |
| tjestenina | 8005121030969 | 50,00 | branka: \*NE\*TJESTENINA DIVELLA TAGLIOLINI 500g; stridon: TAGLIOLINI UOVO ((96) 500G DIVELLA (12) (IT) |
| med | 42212218 | 50,00 | ribola: AIRW.LIQ.DROP.33,5 g LIM/MED; plodine: AIRWAV.HONEY LEM.DR. 33,5 G |
| vanilin_secer | 9001414502389 | 50,00 | trgocentar: KOTANYI BURBON,VANILIN ŠEĆER 10G VREĆICA; studenac: ZAČIN BOURBON VANILI N ŠEĆER 10 g KOT.; gavranovic: KOTANYI BOURBON VANILIN ŠEĆER 10g; plodine: VANILIJIN SECER BOURBON 10 G KOTANYI; tommy: VANILIN ŠEĆER BOURBON 10 g KOT; lorenco: BOURBON VANILIN ŠEĆER 10g |
| kiseli_kupus | 3859891496921 | 33,00 | gavranovic: ZELJE KISELO MIX ZA SARMU 1,6 KG MADIG; ntl: KUPUS KISELI MIX ZA SARMU 1,6 kg; kaufland: Madig Mix za sarmu 1,6 kg |
| junetina | 3850139411164 | 50,00 | studenac: JUNEĆA LOPATICA B.K. PIK; konzum: JUN LOPATICA BK |
| tvrdi_sir | 3228023910039 | 25,00 | konzum: SIR TVRDI EMENTAL PRES 250g DUKAT; ribola: SIR EMEN.250 g PRESI; trgocentar: PRESIDENT EMENTALER 250G, DUKAT; spar: SIR EMMENTAL PRESIDENT 250 g; ktc: SIR PRESIDENT EMENTALER 250g; tommy: SIR EMENTAL 250 g PRESIDENT; plodine: EMENTALER PRESIDENT 250 G DUKAT; studenac: SIR EMMENTAL PRESID. 250 g; vrutak: SIR PRESIDENT EMENTALER 250G -12/1-; kaufland: President sir Ementaler 250g; trgovina-krk: SIR PRESIDENT EMENTALER 250 g DUKAT; ntl: SIR EMENTALER PRESIDENT 250 g DUKAT |
| margarin | 8719200266582 | 25,00 | ktc: BECEL NAMAZ CLASSIC 225g; kaufland: Becel Namaz masni 225g vg.; zabac: BECEL margarina 225G; spar: NAMAZ BECEL CLASSIC 225 g |
| griz | 3858881081598 | 27,00 | djelo_vodice: GRIS 400G FRANCK; spar: GRIS INSTANT FRANCK 400 g; lorenco: INST.GRIS 400 g FRANK; trgocentar: GRIS PŠENIČNI 400G, FRANCK; stridon: GRIS INSTANT 400 g FRANCK (14); bure: GRIS 400 g FRANCK; gavranovic: PŠ.GRIZ FRANCK 400g; metro: 400G FRANCK GRIS INSTANT VREĆI; kaufland: Franck instant gris 400 g; ktc: GRIS PŠENIČNI 400g FRANCK; plodine: PSENICNA KRUPICA INSTANT 400 G GRIS FRANCK; tommy: GRIZ INSTANT 400 g FRANCK; branka: GRIS INSTANT PŠENIČNI 400G FRANCK; jadranka_trgovina: PŠENIČNI GRIZ INSTANT 400G FRANCK; roto: KRUPICA PŠENIČNA 400G FRANCK (14); konzum: KRUPICA PŠENIČNA 400g FRANCK; trgovina-krk: GRIZ INSTANT 400 g KUT. FRAN; vrutak: GRIS FRANCK INST 400G -14/1-; stanic: GRIZ INSTANT 400 g FRANCK; ntl: GRIS PŠENIČNI 400 g FRANCK; studenac: GRIS INSTANT FRANCK 400 g; ribola: GRIS PŠ.KRUP. 400 g FRANCK |
| dodatak_jelima | 3856020263416 | 29,00 | lorenco: POVRTNA PASTA 190g TUBA; djelo_vodice: PASTA POVRTNA 190 G TUBA; trgovina-krk: PASTA POVRTNA VEGETA NATUR 190 gr TUBA; vrutak: N-VEGETA PODR 190G POVRTNA PASTA -12/1- TUBA; tommy: POVRTNA PASTA 190G TUBA PODRAVKA; bure: PASTA POVRTNA 190 g; trgocentar: POVRTNA PASTA 190G TUBA,PODRAVKA (12); plodine: PASTA POVRTNA TUBA 190 G PODRAVKA; ktc: PASTA POVRTNA 190g PODRAVKA; ntl: PASTA POVRTNA 190 g PODRAVKA; branka: PASTA POVRTNA 190g TUBA; kaufland: Vegeta Natur Pasta povrtna 190g; spar: VEGETA NAT.PASTA POVRTNA 190 g; konzum: PASTA POVRĆE TUBA 190g PODRAVKA |
| maslinovo_ulje | 3859890446538 | 50,00 | jadranka_trgovina: MASLINOVO ULJE 0,5L EXTRA DJEVIČANSKO ZLATNO ORGULA; ribola: ULJE EDM 500 ml ZLATNO ORGULA |
| krumpir | 3859893072031 | 50,00 | metro: 10KG LIČKI KRUMPIR CRVENI; lorenco: LIČKI KRUMPIR 5/1 |
| mrkva | 3859893211331 | 33,00 | spar: KUKURUZ ŠEĆERAC 3/1; metro: 6/1 JABUKA CRIPS PINK KOM PD; plodine: MRKVA 500 G |
| tvrdi_sir | 3858881194885 | 33,00 | metro: 230G ŠPIN KRAVLJI SIR; djelo_vodice: SIR KRAVLJI 230G ŠPIN; kaufland: Špin Sir tvrdi istarski kravlji45%mm230g; vrutak: SIR KRAVLJI ŠPIN 230G -16/1; bure: SIR KRAVLJI 230G LOT:24157; studenac: SIR KRAVLJI ŠPIN 230 g; jadranka_trgovina: SIR TVRDI KRAVLJI 230G ŠPIN AGROLAGUNA; plodine: SIR KRAVLJI 230 G AGROLAGUNA; konzum: SIR TVRDI KRAVLJI 230G ŠPIN |
| med | 5900658716801 | 25,00 | plodine: MEDENJACI PUNJENI JABUKOM I TRESNJOM 200 G LAMBERTZ; djelo_vodice: MEDENJACI 200G LAMBERTZ MULTIFRUIT; trgovina-krk: MEDENJACI S VOĆ. PUNJ. 200 gr PRE. ČOKOL. LAMBERTZ; ribola: MED.MIX VOĆE 200 g ULTRA |
| svjezi_sir | 3850355002498 | 50,00 | bure: SIR SV.ZAGREB.375 g LOT:25102026; dukat: PRESIDENT ZAGREBAČKI SIR 375g; vrutak: N-SIR DUKAT ZAGREBAČKI 375G25%MM PRESIDENT -9/1-; boso: SIR SVJEŽ 375 g PRES.ZAGREBAČ; lidl: Dukat President Zagrebački sir; plodine: SIR SVJEZI ZAGREBACKI 375 G DUKAT; branka: SIR PRESIDENT ZAGREBAČKI 375g; djelo_vodice: ZAGREBAČKI SVJEŽI SIR 375G PRESIDENT; kaufland: President Zagrebački svj. sir 25%mm 375g; roto: SIR SVJEŽI ZAGREB PRESIDENT 375g (9); lorenco: DUKAT ZAGREBAČKI SIR 375g; spar: SIR SVJ.ZAGREBAČKI DUKAT 375 g; trgocentar: SIR ZAGREBAČKI 375G 25% (8) DUKAT; gavranovic: SIR ZAGREBAČKI PRESIDENT SVJEŽI 375g 25%MM; konzum: SIR SVJ ZAGREB PRESIDENT 375g; stridon: PRESIDENT ZAGREBAČKI SVJEŽI SIR 375 g DUKAT; ktc: SIR SVJ.ZAGREBAČKI 375g DUKAT PRESIDENT; ribola: SIR SVJ.ZAGR.375 g P; metro: 375GR PRESIDENT ZAG.SV.SIR 25%; ntl: SIR PRESIDENT ZAGREBAČKI 375 g DUKAT; studenac: SIR ZAGREBAČKI DUKAT375 g; tommy: SIR SVJEŽI ZAGREBAČKI 375 g; trgovina-krk: SIR SVJEŽI ZAGREBAČKI 375 g DUKAT; stanic: PRESIDENT ZAGREBAČKI SIR 375 g, DUKAT |
| svjezi_sir | 4002174015008 | 50,00 | trgovina-krk: SIR SVIJEŽI KERNINGER FRISCH ZRNATI STANIĆ; kaufland: Kerniger svježi zrnati sir 20% mm 200 g |
| tvrdi_sir | 3859893066795 | 50,00 | vrutak: SIR 3\*1/8(675G) POKLON KUTIJKOLAN/ML.TRAPIST/DINARSKI 5/1; lorenco: KOMPLET OSMINA KMD 675g |
| tjestenina | 8005121031010 | 50,00 | stridon: PAPPARDELLE UOVO (101) 500 GR (12) DIVELLA (IT); branka: TJESTENINA DIVELLA PAPPARDELLE 500g |
| kecap | 50157655 | 50,00 | bure: HEINZ KETCH. 342 g BLAGI; kaufland: Heinz ketchup blagi 342 g |
| tjestenina | 3859889154598 | 50,00 | branka: TJESTENINA REZANCI SITNI S JAJIMA 400g; ktc: FIDELINI JUŠNI KRATKI 400g |
| tjestenina | 8076809523776 | 45,00 | spar: TJES.BARILLA FETTUCCINE 500 g; trgovina-krk: TJEST. FETTUCCINE 500 g AWT; jadranka_trgovina: TJESTENINA FETUCCINE 500G BARILLA; ribola: TJ.BARILLA PAPPARDEL LE 500G; plodine: TJESENINA FETTUCCINE 500 G BARILLA KUTIJA; lorenco: TJEST.PAPPARDELLE 500 g; ktc: BARILLA FETTUCCINE 500g; tommy: TJ.BARILLA FETTUCCINE 500 g; roto: TIJESTO FETTUCCINE LC 500G BARILLA (12); konzum: TIJESTO FETTUCCINE LC 500g BARILLA; metro: 500G BARILLA FETTUCCIN BEZ JAJ |
| dodatak_jelima | 8600947030317 | 25,00 | ntl: DODATAK JELIMA SA ZAČINIMA ZA RIBLJU JUHU 90g ALEVA; kaufland: Aleva dod. jelima za riblju juhu 90 g; boso: DODAT ALEVA 90 g ZA RIB.JUHU; stanic: ZAČIN ZA RIBLJU JUHU 90 g |
| tjestenina | 8004350130556 | 45,00 | studenac: TJ. PASTA ZARA CHIFF RIGATI BR. 55 500 g; branka: TJESTENINA PASTA ZARA CHIFFERI RIGATI 500g; kaufland: Pasta Zara 055 chifferi rigati b.j.500g; ribola: TJ.CHIFFERI 55 500 g RIGATI PASTA ZARA; konzum: TIJESTO CHIFFERI RIGATI 55 500g ZARA; ntl: TJEST. PASTA ZARA CHIFFERI RIGATI 500G; roto: TIJESTO CHIFFERI RIGATI 55 500g ZARA (10); lorenco: TJEST. 55 CHIFF RIg 500 g; zabac: PASTA ZARA CHIFFERI RIGATI 500 G; trgovina-krk: PASTA ZARA 055 CHIFFERI RIGATI 500G; djelo_vodice: PASTA ZARA CHIFFERI 500G |

30 grupa koje prelaze iz člana (2D) u `ambiguous`:

| namirnica | grupa | m % | x % | nazivi po lancu |
|---|---|---|---|---|
| med | 4000521010294 | 63,00 | 31,00 | tommy: MUESLI CRUN.PL. MED 300 g DR.O; roto: MUESLI KNUSPER MED BADEM 300G VITALI (8); metro: 300G VITALIS CRUN PLUS MED/BAD; kaufland: Dr.Oetker vitalis crunchy med badem 300g; konzum: MUESLI KNUSPER MED BADEM 300g VITALI; lorenco: DR.OETKER CRUNCHY PLUS MED BADEM; vrutak: MUSLI DR OETKER 300G MED I BADEM CRUNCHY PLUS -8/1-; spar: MUSLI VITALIS MED,BADEM 300 g; djelo_vodice: MUSLI CRUNCHY MED BADEM 300g; trgocentar: VITALIS CRUNCHY PLUS MED BADEM 300G, DR.OETKER; ribola: MUESLI CHR.MED 300 g VITALIS DR OETKER; bure: MUESLI VITALIS 300 gHONEY-ALMOND; studenac: MUESLI MED BADEM VITALIS 300 g; plodine: MUSLI PLUS MED BADEM 300 G CRUNCHY DR OETKER; jadranka_trgovina: MUESLI CRUNCHY PLUS MED BADEM 300G VITALIS; trgovina-krk: MUSLI CRUNCHY PLUS MED BADEM 300 g DR OETKER |
| med | 5949040205158 | 75,00 | 17,00 | ktc: ELEPHANT TWIST MORSKA SOL I MED 180g; kaufland: Elephant Pecivo sl.morska sol,med180 g; djelo_vodice: ELEPHANT TWIST - MORSKA SOL i MED 180G; ntl: TRAJNO PEC. ELEP.TWIST - MORSKA SOL I MED 180g; plodine: KREKER MORSKA SOL I MED 180 G ELEPHANT; stanic: ELEPHANT TWIST - MORSKA SOL I MED 180 g; spar: PECIV.ELEP.TWIST SOL-MED 180 g; konzum: KREKE TWIST SOL I MED 180 g ELEPHANT; metro: 180G ELEPHANT TWIST SOL I MED; tommy: SNACK SOL MED 180 g ELEPHANT; gavranovic: PECIVO TWIST MORSKA SOL I MED 180g - ELEPHANT; ribola: KREK.M.SOL&MED 180 g ELEPHANT |
| sol | 9001414040034 | 69,00 | 31,00 | plodine: HIMALAJSKA SOL 120 G KOTANY BOCICA; ribola: SOL HIMALAJSKA 120 g STAKLO KOTANYI; bure: SOL HIMALAJSKA 100 ml STAKLO; trgovina-krk: ZAČIN SOL HIMALAJSKA BOČICA KOTA; branka: SOL HIMALAJSKA BOČICA 120g; spar: SOL HIMALAJ.SITNA KOTANY120 g; kaufland: Kotanyi himalajska sol 120 g bočica; djelo_vodice: HIMALAJSKA SOL 100ML; studenac: ZAČIN HIMALAJSKA SOL 120 g KOT.; konzum: HIMALAJSKA SOL BOČ 120G KOTANYI; ktc: SOL HIMALAJSKA 100mL ST KOTANYI; lorenco: HIMALAJSKA SOL JODIRANA STAKLO 100; tommy: SOL HIMALAJSKA STAK. 120 g KOT |
| zobene_pahuljice | 8595054907761 | 67,00 | 25,00 | plodine: ZOBENE PAHULJICE SUMSKO VOCE 300 G BIOPLOD; ribola: PAHULJ.ZO.BO.300 g D OBRE PAHULJICE; lorenco: DOBRE ZOBENE PAHULJICE 300g BERRIES; tommy: ZOBENE PAH. ŠUM.VOĆE 300 g DOB; zabac: Dobre zobene pahuljice 300g BERRIES; kaufland: Dobre Pahuljice zobene bobič.voće 300g; konzum: PAHULJICE ZOBENE BERRIES 300g; spar: DOBRE ZOBENE PAH.BOB.VOĆ.300 g; ntl: PAHULJICE ZOBENE BERRIES 300 g DOBRE; gavranovic: ZOBENE PAHULJICE DOBRE BERRIES 300g; vrutak: ZOBENE PAHULJICE 300G BERRIES; branka: PAHULJICE ZOBENE BERRIES 300g |
| sol | 3856020222314 | 80,00 | 20,00 | ktc: MORSKA SOL GRUBO MLJEVENA 100g PODRAVKA; stridon: VEGETA MAESTRO MORSKA SOL M.100 G (6) PODRAVKA; ribola: SOL MORSKA 100 g VE GETA MAESTRO; plodine: MORSKA SOL MLINAC 100 G VEGETA MAESTRO; konzum: ZAČIN SOL MORSKA ML 100g VEGETA MAESTRO; lorenco: VEGETA MAESTRO MORSKA SOL 100G; tommy: VEGETA MAESTRO MORSKA SOL GRUBO MLJEVENA 100G; spar: ZAČ.SOL MORSKA VEG.MAES.100 g; bure: SOL MORSKA 100 g KRUNA PODR.; djelo_vodice: MORSKA SOL GRUBO MLJEVENA VEGETA MAESTRO BOČICA 100G |
| papar | 9001414274057 | 80,00 | 20,00 | spar: ZAČ. PAPAR S&D CRNI ZRNO 50 g; ntl: ZAČIN ZA KOKTELE SPICES & DRINKS PAPAR CRNI 50 g KOTANYI; plodine: SPICES DRINKS PAPAR CRNI, ZRNO 50 G; lorenco: PAPAR CRNI ZRNO SiD STAKLO 100ML; kaufland: Kotany papar crni zrno, bočica 50 g |
| papar | 9001414050026 | 54,00 | 46,00 | trgocentar: KOTANY ZELENI PAPAR U ZRNU 100G; djelo_vodice: PAPAR ZEL.SALAMURA; lorenco: ZELENI PAPAR 100 g KOTANYI; metro: 100G KOTANYI PAPAR ZELENI U SA; vrutak: KOTANYI 100G PAPAR ZELENI USALAMURI -24/1-; roto: PAPAR ZELENI U SALAMURI 100g KOTANYI (24); trgovina-krk: PAPAR ZELENI U SALAMURI 100 g KOTAN; ribola: PAPAR ZEL.SAL. 100 g KOTANYI; tommy: ZAČIN PAPAR ZEL/SAL. 100 g KOT; bure: PAPAR ZELENI 100 g SALAMURA UG.; spar: ZAČ.PAPAR ZELEN.KOTANYI 100 g; studenac: ZAČIN PAPAR ZELENI U SALAMURI 100 g KO; gavranovic: KOTANYI PAPAR ZEL.U SALAMURI 100g |
| tjestenina | 8008857300771 | 83,00 | 17,00 | trgocentar: SPAGETTI TAGLIATI 77 (SITNI REZANCI) 500G PASTA REGGIA (24); jadranka_trgovina: TJESTENINA SPAGHETTI TAGLIATI 077 500G REGGIA; ntl: TJESTENINA TAGLAITI 500g REGGIA; trgovina-krk: TJEST. TAGLIATI 500 g REGGIA NTL; ribola: TJ.SPAGHETTI 500 g TAGLIATI JUHA REGGIA; bure: TJ.FIDELINI 77 500 gREGGIA (SPAGET.TAGLI |
| kiseli_kupus | 3859891493098 | 56,00 | 11,00 | lorenco: MADIG MIX ZA SARMU 1000g; spar: KUPUS KIS.MIX ZA SARMU 1 kg; eurospin: KUPUS KISELI MIX ZA SARMU 1kg; tommy: KUPUS KIS. MIX ZA SARMU 1000 g; trgovina-krk: KUPUS KISELI MIX MADIG ZA SARMU 1 kg NTL; gavranovic: ZELJE KISELO MIX ZA SARMU 1KG MADIG; konzum: KUPUS KISELI MIX ZA SARMU MADIG; studenac: KIS. ZELJE MIX ZA SARMU 1100 g; plodine: SARMA MIX 1 KG KISELI KUPUS MADIG |
| sol | 3870009000144 | 80,00 | 20,00 | spar: SOL KUHINJ. TUZLA SITNA 250 g; kaufland: Tuzla kuhinjska sol jodirana 250g; ktc: SOL KAMENA DOZA 250g TUZLA; vrutak: SOL KAMENA 250G SOLJENKA -15/1- TUZLA; plodine: SOL KUHINJSKA JODIRANA 250 G TULJAK TUZLA |
| med | 5900617037152 | 86,00 | 14,00 | jadranka_trgovina: ŽITARICE GRANOLA GOLD ORASI+MED 300G SANTE; kaufland: Sante Granola Gold med i oraš.plod.300g; plodine: MUESLI GRANOLA MED I ORASASTI PLODOVI 300 G SANTE; tommy: MUESLI GRAN. NUT/MED 300 g SAN; spar: GRAN.SANTE ORAŠ.PLOD.MED 300 g; konzum: MUESLI GRANOLA ORAŠ PLOD MED 300g SANTE; ribola: GRANOLA 300 g ORAH/ MED SANTE |
| majoneza | 3856015304339 | 86,00 | 14,00 | lorenco: ZVIJEZDA ČILI MAJONEZA 165g; branka: MAJONEZA ČILI 165g; trgovina-krk: MAJONEZA ČILI 165 g ZVIJ; studenac: MAJONEZA ZV. 165G ČILI TUBA; vrutak: N-MAJONEZA ZVIJEZDA 165G -12/1 ČILI TUBA; plodine: MAJONEZA CILI 165 G TUBA ZVIJEZDA; kaufland: Zvijezda čili majoneza tuba 165g; konzum: MAJONEZA ČILI 165g ZVIJEZDA; trgocentar: MAJONEZA CHILI 165G TUBA (12) ZVIJEZDA; stridon: MAJONEZA ČILI TUBA 165 g (12) ZVIJEZDA; gavranovic: MAJONEZA CHILLI 165g ZVIJEZDA; roto: MAJONEZA ČILI 165G ZVIJEZDA (12); ktc: MAJONEZA TUBA ČILI 165g ZVIJEZDA; jadranka_trgovina: MAJONEZA 165G ČILI TUBA ZVIJEZDA |
| kukuruz | 3859893512254 | 70,00 | 30,00 | lorenco: KUKURUZ PEČENI SALNI BBQ 60g S.SNAC; studenac: KUKURUZ PEČ.SL. NATURA 60 g; trgocentar: KUKURUZ PEČENI SLANI 60G BBQ SUPER SNACK; trgovina-krk: KUKURUZ PS BBQ NATURA 60 g; vrutak: N-KUKURUZ NATURA 60G PEČENI SLANI BBQ -20/1- SUPER SNACK; plodine: KUKURUZ PECENI SLANI BBQ 60 G SUPER SNACK NATURA; gavranovic: KUKURUZ PEČENI SLANI BBQ 60g NATURA; jadranka_trgovina: KUKURUZ PEČENI SLANI BBQ 60G; spar: KUKURUZ PEČ.SLANI NATURA 60 g; ribola: KUKURUZ PEČENI 60 g SLANI NATURA |
| papar | 9001414040867 | 60,00 | 10,00 | plodine: PAPAR MIX 40 G STAKLO KOTANYI; gavranovic: KOTANYI PAPAR MJEŠAVINA STAKLO 40g; branka: \*NE\*PAPAR MJEŠAVINA 35G STAKLO KOTANYI; vrutak: KOTANYI 40G PAPAR ŠARENAMJEŠAVINA STAKLO -4/1-; spar: ZAČ.PAPAR MJEŠ.KOTANYI 40 g; trgovina-krk: ZAČIN MJEŠAVINA PAPRA STAKLO 40 g KOTANY; lorenco: ZAČIN MJEŠ. PAPRA 35 g KOTANYI; studenac: ZAČIN PAPAR ŠARENI 40 g KOT.; tommy: ZAČIN PAPAR MJEŠ.40 g KOTANY; bure: ZAČIN MJEŠ.PAPRA 100g |
| tuna | 8004030860025 | 0,00 | 86,00 | tommy: TUNA SALATA CUS CUS 2X160 G RIO MARE; kaufland: Rio Mare Insal.sal.tuna cous cous2x160g; konzum: TUNJ SALATA COUS COUS 2X160g RIO MARE; spar: TUNA SAL.RIO MARE COUS 2X160 g; lorenco: TUNA -COUS-COUS SAL.2\*160g BOWL.; metro: 160GX2 RIO MARE INSALA.CUS CUS; plodine: TUNA COUS-COUS SAL.2X160G BOWL |
| grah | 3083680001793 | 67,00 | 17,00 | plodine: BRETONA BIJELI GRAH U UMAKU OD RAJCICE 430 G; vrutak: N-GRAH BIJELI BONDUELLE 400G S RAJČICOM; lorenco: BONDUELLE BIJELI GRAH S RAJČ.400g; spar: GRAH BONDUELLE BRETONA 430 g; konzum: GRAH BIJELI RAJČICA 430/200g BONDUELLE; kaufland: Bonduelle Bretona 430g/200g |
| piletina | 3850159113154 | 60,00 | 20,00 | studenac: PILE GAVELINO VINDIJA KOKA kg; spar: PILE GAVELINO; konzum: PILE GAVELINO POD VINDIJA; plodine: GAVELINO PILE ZA PECENJE CEKIN (11315); ribola: GAVELINO VINDIJA |
| jaja | 5200701000063 | 67,00 | 17,00 | studenac: BOM. JAJE PEPA PIG 10 g; ribola: PEPPA PIG JAJE 10 g; trgovina-krk: SRCE JAJE PEPPA PIG 10G; vrutak: SRCE PL. PEPPA PIG 10G; konzum: JAJE S BOMBONIMA PEPA PIG 10g; ntl: JAJE IZNENAĐENJA 10 g MIX LICENCA |
| papar | 9001414440834 | 86,00 | 14,00 | ntl: ZAČIN ZA KOKTELE SPICES & DRINKS PAPAR CRVENI 25 g KOTANYI; plodine: SPICES DRINKS PAPAR CRVENI ZRNO 25 G; konzum: PAPAR CRVENI ZRNO S&D 25g KONTAYI; vrutak: KOTANYI KOKTEL PAPAR CRVENI SPICE i DRINKS 25G ZRNO; lorenco: PAPAR CRVENI ZRNO KOKTEL SND ST 100; spar: ZAČIN PAPAR CRVENI ZRNO 25 g; gavranovic: KOTANYI PAPAR CRVENI ZRNO 25g SPICE DRINKS |
| tjestenina | 8710605028430 | 71,00 | 29,00 | plodine: TJESTENINA S JAJIMA GNIJEZDA 250 G NOODLES GO TAN; konzum: TJESTENINA S JAJIMA GNIJEZDA GO TAN 250g; ribola: TJEST.GO TAN 250g; kaufland: Go Tan tjest.s jajima za Wok 250 g; vrutak: TJESTENINA GO-TAN 250G EGG WOK NOODLES -8/1-; ntl: TJESTENINA OD PŠ. BRAŠNA S JAJIMA 250G NIKAS; spar: TJESTENINA GOTAN NEST 250 g |
| dodatak_jelima | 3856020228910 | 90,00 | 10,00 | tommy: VEGETA NATUR BURGER VR.30 g PO; stridon: VEGETA NATUR BURGER CLASSIC 30 g (18); bure: VEGETA VR.BURG. 30 gCLASSIC; plodine: VEGETA NATUR BURGER 30 G CLASSIC; trgocentar: VEGETA NATUR BURGER CLASSIC VR.30G (18) (PAL 252) PODRAVKA; konzum: ZAČIN BURGER CLASSIC VR 30g VEGETA NATUR; lorenco: VEGETA NATUR BURGER CLASSIC VR.30g; kaufland: Vegeta Natur Grill Burger classic 30 g; trgovina-krk: VEGETA NATUR BURGER CLASSIC 30 g VREĆICA POD; spar: ZAČIN VEGETA NATUR BURGER 30 g |
| sol | 3856020267216 | 83,00 | 17,00 | lorenco: VEGETA MAESTRO SITNA MORSKA SOL; spar: ZAČ.V.MAEST.SITNA MOR.SOL 110g; plodine: VEGETA MAESTRO SITNA MORSKA SOL POSIPAC 110 G BOCICA; tommy: VEGETA MAESTRO SITNA MORSKA SOL POSIPAČ 110 g; bure: VEGETA MAESTRO 110g SITNA SOL; konzum: SOL SITNA MORSKA 110g VEGETA MAESTRO |
| piletina | 3850159142321 | 77,00 | 15,00 | ktc: CEKIN KIDS BUCKET KRILCA 500g; ntl: KRILCA PILEĆA PEČENA SM 500 g CEKIN; trgocentar: CEKIN KRILCA BUCKET 500G; spar: PILE.KRILCA BUCKET CEKIN 500 g; boso: KRILCA CEKIN 500 g BUCKET; ribola: PIL.KRIL.BUCK. 500 gVINDIJA; stridon: CEKIN KRILCA BUCKET 500 g 14232 VINDIJA; jadranka_trgovina: KRILCA BUCKET CEKIN 500G VINDIJA; kaufland: Cekin Pečena pileća krilca 500 g; plodine: CEKIN KRILCA BUCKET 500 G; branka: KRILCA BUCKET CEKIN 500g; vrutak: N-VIN KRILCA BUCKET 500G -4/1-; trgovina-krk: CEKIN KRILCA BUCKET 500G |
| maslac | 3856015325419 | 86,00 | 14,00 | konzum: MARGO S MASLACEM 225g; plodine: MARGO S MASLACEM 225 G ZVIJEZDA; trgocentar: MARGO S MASLACEM 225G (16),ZVIJEZDA; vrutak: N-MARGO S MASLACEM 225G -16/1-; spar: NAMAZ MARGO S MASLACEM 225 g; ktc: MARGO S MASLACEM 225g ZVIJEZDA; tommy: MARGO S MASLACEM 225 G; branka: MARGARIN MARGO MASLAC 225g; kaufland: Margo Namaz miješani s maslacem 225g; trgovina-krk: MARGO S MASLACEM 225 gr; stridon: MARGO S MASLACEM 225 g ZVIJEZDA (16); jadranka_trgovina: MARGARIN MARGO S MASLACEM 225G ZVIJEZDA; lorenco: MARGO S MASLACEM 225G ZVIJEZDA; boso: MARG. MARGO 225 g S MASLACEM |
| senf | 5949040202058 | 61,00 | 22,00 | ntl: TRAJNO SLANO PECIVO ELEPHANT 70 g MED,SENF I LUK; kaufland: Elephant slano pecivo med senf i luk 70g; metro: 70G ELEPHANT FLAT MED SENF LUK; ribola: KREK.MED SEN.LU.70 g ELEPHANT; studenac: KREK. ELEPHANT SENFLUK 70 g; stanic: ELEPHANT PECIVO MED, SENF, LUK 70 g; trgovina-krk: ELEPHANT TRAJNO SLANO PECIVO - MED,SENF I LUK 70 g; vrutak: ELEPHANT 70G TRAJNO SLANO PECIVO ALKA MED, SENF, LUK; branka: PECIVO ALKA ELEPHANT MED-SENF-LUK 70g; boso: KREKE ELEPHANT 70 g MED SENF LUK; jadranka_trgovina: GRICKALICE ELEPHANT MED, SENF I LUK 70G; konzum: KREKER MED I SENF 70 g ELEPHANT; ktc: ELEPHANT MED,SENF I LUK 70g; lorenco: ALKA ELEPH.TS PECIVO 70g; plodine: SNACK MED/SENF/LUK 70 G ELEPHANT; spar: KRE.ELEPHANT SENF&MED&LUK 70 g; djelo_vodice: ELEPHANT TRAJNO SLANO PECIVO - MED, SENF i LUK 70g; tommy: SNACK MED SENF LUK 70 g ELEPHA |
| senf | 5949040204953 | 60,00 | 10,00 | ntl: TRAJNO SLANO PECIVO ELEPHANT PRETZEL 75 g MED, SENF I LUK; gavranovic: PECIVO KOMADIĆI MED,SENF I LUK 75g ELEPHANT; tommy: SNACK MED SENF LUK 75 g ELEPHA; boso: KREKE ELEPHANT 75 g MED SENF LUK; stridon: ALKA ELEPHANT TS PECIVO-KOMAD.S OKUS.MEDA 14\*75 g; ribola: PERECI ME.SE.LU.75 g ELEPHANT; plodine: PEREC KOMADICI S OKUSOM MEDA,SENFA I LUKA 75 G ELEPHANT; konzum: PER LOMLJ MED SENF LUK 75 g ELEPHANT; ktc: ELEPHANT KOMADIĆI MED,SENF I LUK 75g; kaufland: Elephant Komadići med,senf i luk75g |
| pileca_prsa | 3856020257064 | 57,00 | 14,00 | ribola: ŠUNKA PILEĆA 60 g LINO PODRAVKA; tommy: PILEĆA PRSA 60 G LINO NARESCI PODRAVKA; spar: PILEĆA PRSA LINO NJUPAL. 60 g; plodine: LINO PILECA PRSA 60 G PODRAVKA; ktc: PILEĆA PRSA 60g LINO; konzum: LINO PILEĆA PRSA 60 g; stridon: LINO PILEĆA ŠUNKA 60 g (10) PODRAVKA |
| majoneza | 3856015324689 | 81,00 | 14,00 | konzum: MAJONEZA ČILI PVC 85g ZVIJEZDA; trgovina-krk: MAJONEZA ČILI 85G; boso: MAJON ZVIJE 85 g DELIK.ČILI; jadranka_trgovina: MAJONEZA 85G ČILI VREĆICA ZVIJEZDA; lorenco: ZVIJEZDA MAJONEZA ČILI 85G; metro: 85G ZVIJEZDA MAJONEZA ČILI; roto: MAJONEZA ČILI PVC 85g ZVIJEZDA (25); studenac: MAJONEZA ČILI 85g ZVIJ.; branka: MAJONEZA ČILI 85g; djelo_vodice: ČILI MAJONEZA 85g; gavranovic: MAJONEZA CHILLI VREĆICA 85g ZVIJEZDA; zabac: CHILI MAJONEZA 75% 85 G; stridon: MAJONEZA ČILI ZVIJEZDA 85 g (25); vrutak: N-MAJONEZA ZVIJEZDA 85G -25/1 ČILI; trgocentar: MAJONEZA ČILI 85G ,ZVIJEZDA; ribola: MAJONEZA ČILI 85 g ZVIJEZDA; spar: MAJONEZA CHILI ZVIJEZDA 85 g; kaufland: Zvijezda majoneza čili 85 g; ktc: MAJONEZA ČILI 85g ZVIJEZDA; lidl: Zvijezda Majoneza Čili; tommy: MAJONEZA ČILI 85 G ZVIJEZDA |
| sol | 9001414046241 | 75,00 | 25,00 | spar: MORSKA SOL KOTANY 120g; tommy: SOL MORSKA JODIRANA 120 g KOTAN; vrutak: KOTANYI 100ML MORSKA SOL SITNA STAKLO -4/1-; konzum: MORSKA SOL BOČ 120 g KOTANYI; bure: SOL SITNA 100ml STAKLO; plodine: MORSKA SOL 120 G BOCICA KOTANYI; kaufland: Kotanyi Sol morska sitna jodirana 120g; metro: 120G KOTANYI MORSKA SOL BOČICA |
| pileca_prsa | 3850159123306 | 59,00 | 35,00 | trgocentar: PILEĆA PRSA 100G, VINDIJA; stridon: PILEĆA PRSA 100 g VINDIJA; jadranka_trgovina: SALAMA PILEĆA PRSA 100G CEKIN VINDIJA; kaufland: Cekin Pileća prsa 100 g; konzum: PRSA PILEĆA U OVITKU NAR 100g; lorenco: PILEĆA PRSA 100g; vrutak: VIN PILEĆA PRSA 100G; ribola: PIL.PRS.U OV.100 g VINDIJA; djelo_vodice: PILEĆA PRSA 100G VIN.; plodine: PILECA PRSA 100 G VINDIJA; tommy: PILEĆA PRSA NARESCI 100 g; ktc: PILEĆA PRSA 100g VINDIJA; spar: PILEĆA PRSA 100 g; ntl: SALAMA PRSA PILEĆA 100 g VINDIVAC; studenac: PIL. PRSA U OVIT. 10 0g VINDVAC; trgovina-krk: SALAMA PILEĆA PRSA 100 g VIND; gavranovic: CEKIN PILEĆA PRSA NAREZAK 100g |

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
| tvrdi_sir | strong | ktc: SIR EMMENTALER CCA 3kg SPOMLEK |
| tjestenina | strong | plodine: TJ.CACCAV.TRIC.3 KOM 120 G |
| tvrdi_sir | strong | plodine: SIR EMMENTALER BLOK 2,15 KG SALZBURGMILCH |
| jogurt | strong | spar: JOG.GRČKI TIP 10%NP BIO 400 g |
| tjestenina | strong | tommy: TJ.VITA FIDELINI 61 250 g MLIN; lorenco: MLI.VITA KOREN.FIDELINI 61 250g; djelo_vodice: TJ.VITA FIDELINI MRKVA 250G |
| tvrdi_sir | strong | spar: CHEDDAR MINI VINTAGE 200 g; kaufland: The old farm.Sir Cheddar Vintage50% 200g |
| pileca_prsa | strong | plodine: PILECI FILE ODRESCI 400 G AIA; spar: PILEĆI ODRESCI FILEA 400 g; konzum: ODRESCI PILEĆEG FILEA 400g AIA |
| tjestenina | strong | trgovina-krk: LAZANJE GASTRO TS |
| tjestenina | strong | eurospin: \*LASAGNE PEČENE |
| tjestenina | strong | lorenco: REZANCI ŠIROKI 400g STARA PUŠNICA |
| tjestenina | weak | djelo_vodice: TJE.GOMITI 27 500G PAGANI; ribola: ULTRA-GOM.RIG.500g |
| tjestenina | strong | konzum: TIJESTO LASAGNE 500 g DE CECCO; vrutak: TJEST LASAGNE br. 502 500G DE CECCO -24/1-; plodine: LASAGNE 500 G DE CECCO TJESTENINA |
| tjestenina | strong | stridon: DOMAĆE ŠKOLJKICE KAKAO PRELJEV 205G (16) CONVOCO |
| tvrdi_sir | strong | plodine: SIR CHEDDAR BIJELI 200 G DUBLIN DAIRY EUROSER |
| tvrdi_sir | strong | konzum: SIR MAASDAM 300 g DELISO |
| tjestenina | strong | plodine: TJESTENINA VIJAK 500 G PASTARIA PIK VRECICA; bure: TJ.VIJAK 500G DURUM TONKA; gavranovic: TJ.PAŠTARIA 500g VIJAK; studenac: TJ. PAŠTARIA DURUM VIJAK 500 g; tommy: TJ.DURUM VIJAK 500 g PAŠTARIJ |
| jogurt | strong | kaufland: KLC.Muesli pločica marelica+jog.30g |
| tvrdi_sir | strong | tommy: SIR EMMENTAL 300 g MEGGLE |
| tjestenina | strong | plodine: TJ. INTEGR.DITALI 454G MISURA |
| tjestenina | strong | tommy: FUŽI S TARTUFATOM |
| tvrdi_sir | strong | dukat: PRESIDENT EDAM CCA 2.7kg |
| tvrdi_sir | strong | spar: Sir Emmentaler Illertaler |
| tjestenina | strong | studenac: TJ. FIAMMA BR.7 BUCATINI 500 g |
| tvrdi_sir | strong | spar: SIR CHEDDAR CRVENI REZAN.150 g |
| tvrdi_sir | strong | konzum: SIR WHITE CHEDDAR NAR DELISO 200 g |
| tjestenina | strong | studenac: 16794 LAZANJE TIKVIC E I PROVOLA 350 g |
| tjestenina | strong | plodine: TJ.CHITARRINE 250 G, CAMERINO |
| tjestenina | strong | konzum: TIJESTO ŠURLE 500g KLARA M; ribola: TJ.ŠURLE 500 g KLAR A MARIĆ; spar: TJ.KL.MARIĆ ŠURLE 500 g; bure: TJ.ŠURLE 500 g KLARAMARIĆ; tommy: TJ.ŠURLE 500 g KLARA M; metro: 500G KLARA M. ŠURLE BEZ JAJA; jadranka_trgovina: TJESTENINA ŠURLE 500G KLARA; kaufland: Klara M šurle 500g; plodine: TJESTENINA SURLE 500 G KLARA MARIC; studenac: TJ. ŠURLE KLARA M. 500 g; lorenco: ŠURLE 500g; djelo_vodice: ŠURLE K.M. 500G; roto: TIJESTO ŠURLE 500G KLARA M (10); vrutak: TJEST KLARA M ŠURLE 500G-10/1- 112 |
| tvrdi_sir | strong | spar: SIR CHEDD.MATURE PRESID.200 g; vrutak: N-SIR PRESIDENT CHEDDAR MATURE 200G; plodine: SIR CHEDDAR MATURE 200 G PRESIDENT DUKAT; tommy: SIR CHEDDAR MATUR 200 g PRESID; konzum: SIR POLU CHEDDAR MATURE 200g; studenac: SIR CHEDDAR MATURE PRESIDENT 200 g; dukat: PRESIDENT CHEDDAR ZRELI 200g |
| mlijeko | strong | plodine: MLIJ.DUKAT 0.5% 1 L BOCA DUKAT(660KOM/PAL); ribola: MLIJ.TR.0,5% 1L BO.D |

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
| unknown → ostalo | 1 |
| unknown → pice | 1 |
| ostalo → unknown | 1 |

Vraćeno u `hrana` s „cvijet“ u nazivu: **78**. 20 primjera:

| lanac | naziv | kategorija | prije |
|---|---|---|---|
| konzum | SOL SOLNI CVIJET 150g SOLANA PAG | HRANA | ostalo |
| zabac | Cvijetni med Varžak 450g | Umaci i namazi | ostalo |
| trgocentar | ČAJ KAMILICA CVIJET 50G | Hrana | ostalo |
| trgocentar | MED CVIJETNI LIVADA 900G, APIMEL (12) | Hrana | ostalo |
| kaufland | KBio.Šećer od kokosovog cvijeta 250g | HRANA | ostalo |
| metro | BEGONIJA CVIJET - KOM | hrana | ostalo |
| metro | 1L TE VODA OD CVIJETA RUŽE | hrana | ostalo |
| branka | ČAJ KAMILICA CVIJET 40g | HRANA | ostalo |
| plodine | SOL CVIJETNA 125 G SOLANA PAG |  | unknown |
| trgovina-krk | KLINČIĆ CVIJET 50 g | Hrana | ostalo |
| metro | 100G TIKVICA CVIJET | hrana | ostalo |
| bure | MED CVIJETNI 900 g PIP LOT:17.08.28 | HRANA | ostalo |
| ktc | ČAJ BAZGA CVIJET 40g AGRISTAR | HRANA | ostalo |
| metro | 60G TIKVICA CVIJET | hrana | ostalo |
| metro | TIKVICA CVIJET - KOM | hrana | ostalo |
| ktc | ČAJ KAMILICA CVIJET 50g AGRISTAR | HRANA | ostalo |
| jadranka_trgovina | MED CVIJETNI 450G | HRANA | ostalo |
| ribola | LAVANDIN CVIJET 20 g LUXOR | HRANA | ostalo |
| ntl | BROKULA CVIJET 2,5kg ZMH | Hrana | ostalo |
| lorenco | MED CVJETNI 459 GRAMA |  | ostalo |

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
| plodine | JUHA KREM RAJCICA 500 ML PODRAVKA |
| plodine | RAJCICA TERNETTO 250 G |
| konzum | RAJČICA PASIRANA 500g PODRAVKA |
| konzum | RAJČICA PASIRANA 700g STAR |
| kaufland | Podravka Ćufte u umaku od rajčice 400g |
| kaufland | Cirio Rajčica sjeckana luk i češnj.390g |
| spar | PESTO SPAR RAJČICA,BOS.190 g |
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
| spar | PATE RIO MARE TUNA MRKVA 100 g |
| kaufland | KBio.Snack kukur.sa prosom i mrkvom30g |
| studenac | SOK VINDI A+C+E NARANČA MRKVA 0,5 l |
| kaufland | B.aktiv LGG jog jab.dinja mrkva 330g PET |
| konzum | KAŠICA HIPP TELET RIŽ MRKV 190g |
| kaufland | KLC. Grašak-mrkva 1 kg |
| plodine | MRKVA BABY ARANCIO 200 G |
| spar | Salata mrkva-jabuka |
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
| plodine | KRASTAVCI DELIKATES 680 G CAMPO |
| kaufland | Podravka krastavci delikates 670g/370g |
| studenac | SOK LIMUN KRASTAVAC TOCO 0,5 l |
| plodine | KISELI KRASTAVCI 680 G I KLASA CAMPO |
| kaufland | Zvijezda Krastavci delikates 350g/170g |
| spar | KRASTAVCI PODRAVKA DELIK.330 g |
| spar | KRASTAVCI ZVIJEZDA KLAS.670 g |
| tommy | KRASTAVCI 6-9 cm 680 g T! |
| kaufland | Podravka Krastavci kiseli 330g/175g |
| plodine | KRASTAVCI 1500 G STAKLO PODRAVKA |

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
| konzum | LUK PRAH 70g SOTINAC |
| plodine | PECENI KIKIRIKI PAPIKA LUK MIX 400 G YUMMY |
| konzum | ČIPS CRUNCHIPS SIR LUK 130g |
| spar | ZAČIN LUK GRANULE 22 g |
| konzum | KVIKI GRIC VRHNJE I LUK 50G PODRAVKA |
| plodine | CIPS VRHNJE LUK TUBA 100 G BITS BYTES |
| plodine | CVARCI LUK I PAPRIKA VRECICA PRESANI 100 G PIVAC |
| kaufland | KLC.Čips kis.vrh i luk,rebrasti 150g |

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
| studenac | ČIPI ČIPS PAPRIKA XXL 210 g |
| kaufland | Pringles Čips paprika 125 g |
| spar | NAMAZ NATURETA PAPRIKA 290 g |
| konzum | PAPRIKA SLATKA 500g ŠAFRAM |
| plodine | MASLINE ZELENE S PAPRIKOM 700 G ZVIJEZDA |
| kaufland | Pom-Bär Snack paprika 50g |
| plodine | MARINIRANA CRVENA PAPRIKA 720 G CAMPO |
| studenac | ZAČIN PAPRIKA SLATKA MLJEVENA 10 |
| studenac | GASTRO PAPRIKA PEČENA |

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
| konzum | MJEŠAVINA BULGUR I TIKVICA 350g |
| plodine | PASTA S KOZICAMA I TIKVICAMA |
| plodine | RIZOTO S PILETINOM I TIKVICAMA PLODINE |
| studenac | RIŽOTO PILETINA I TIKVICE kg |
| tommy | TIKVICE PEČENE PORCIJA |
| plodine | PASTA S KOZICAMA I TIKVICAMA PORCIJA |
| tommy | TIKVICE PEČENE |
| spar | OROZOTTO TIKVICE BOS.300 g |

