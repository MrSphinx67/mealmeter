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
| maslac | 3023470001015 | 33,00 | studenac: KEKS GALETTES 130 g; lorenco: LA GALETTE ALL BUTTER ST MICHEL 130; plodine: KEKS GALETTES 130 G BONNE MAMAN |
| svjezi_sir | 3850355007561 | 50,00 | plodine: SIR SVJEZI ZAGREBACKI 220 G PRESIDENT; ribola: SIR SV.ZAG.B.LA.220gPRESIDENT; lidl: President Zag.svj. sir bez laktoze; stridon: PRESIDENT ZAGREBAČKI SIR BEZ LAKTOZE 220 g DUKAT |
| tvrdi_sir | 3859892884413 | 33,00 | ribola: SIR MEDITER.200 g PAŠKA; studenac: SIR MEDITERANO 200 g; tommy: SIR MEDITERANO 200 g PAŠKA SIRANA; jadranka_trgovina: SIR TVRDI MEDITERANO 200G PAŠKA SIRANA; konzum: SIR TVRDI MEDITERANO 200 g PAŠKA SIR; lorenco: MEDITENO 200GR PAŠKA SIRANA |
| tvrdi_sir | 3859891700622 | 43,00 | ribola: SIR OTOČAN 300 g MIH; studenac: SIR OTOČAN 300 g; tommy: SIR OTOČAN 300 g MIH; plodine: SIR OTOCAN 1/8 300 G; roto: SIR TVRDI OTOČAN 300g MIH (16); jadranka_trgovina: SIR TVRDI OTOČAN 300G MIH; konzum: SIR TVRDI OTOČAN 300g MIH |
| slatko_vrhnje | 4034900027733 | 38,00 | trgovina-krk: VRHNJE BILJNO PATISSERIE 25% B.M. 1L MEGGL; bure: VRHNJE ZA ŠLAG 1 kg MEGGL.LOT:270128; metro: 1L CREME PATISSERIE 25%; plodine: CREME PATISSERIE 1 L MEGGLE; lorenco: VRHNJE ZA ŠLAg 1000ML MEGGLE; roto: ŠLAG BRIK MEGGLE 1,0 (12); kaufland: Creme Patisserie slatko vrhnje 25 % 1 l; spar: PRIP.ZA ŠLAG CREME PA.25% 1 L |
| tvrdi_sir | 8410285102733 | 50,00 | konzum: SIR POLUTV S TARTUFIMA 200 g PRESIDE; spar: SIR S TARTUFIMA PRESID.200 g |
| tjestenina | 3859888231023 | 50,00 | kaufland: Clarum fidelini sitni 400 g; ntl: TJEST.FIDELINI SITNI 400 g CLARUM |
| tjestenina | 8005121030969 | 50,00 | stridon: TAGLIOLINI UOVO ((96) 500G DIVELLA (12) (IT); branka: \*NE\*TJESTENINA DIVELLA TAGLIOLINI 500g |
| med | 42212218 | 50,00 | plodine: AIRWAV.HONEY LEM.DR. 33,5 G; ribola: AIRW.LIQ.DROP.33,5 g LIM/MED |
| vanilin_secer | 9001414502389 | 50,00 | lorenco: BOURBON VANILIN ŠEĆER 10g; tommy: VANILIN ŠEĆER BOURBON 10 g KOT; trgocentar: KOTANYI BURBON,VANILIN ŠEĆER 10G VREĆICA; plodine: VANILIJIN SECER BOURBON 10 G KOTANYI; studenac: ZAČIN BOURBON VANILI N ŠEĆER 10 g KOT.; gavranovic: KOTANYI BOURBON VANILIN ŠEĆER 10g |
| kiseli_kupus | 3859891496921 | 33,00 | ntl: KUPUS KISELI MIX ZA SARMU 1,6 kg; gavranovic: ZELJE KISELO MIX ZA SARMU 1,6 KG MADIG; kaufland: Madig Mix za sarmu 1,6 kg |
| junetina | 3850139411164 | 50,00 | studenac: JUNEĆA LOPATICA B.K. PIK; konzum: JUN LOPATICA BK |
| tvrdi_sir | 3228023910039 | 25,00 | kaufland: President sir Ementaler 250g; plodine: EMENTALER PRESIDENT 250 G DUKAT; tommy: SIR EMENTAL 250 g PRESIDENT; ntl: SIR EMENTALER PRESIDENT 250 g DUKAT; trgovina-krk: SIR PRESIDENT EMENTALER 250 g DUKAT; studenac: SIR EMMENTAL PRESID. 250 g; vrutak: SIR PRESIDENT EMENTALER 250G -12/1-; ktc: SIR PRESIDENT EMENTALER 250g; spar: SIR EMMENTAL PRESIDENT 250 g; trgocentar: PRESIDENT EMENTALER 250G, DUKAT; ribola: SIR EMEN.250 g PRESI; konzum: SIR TVRDI EMENTAL PRES 250g DUKAT |
| margarin | 8719200266582 | 25,00 | spar: NAMAZ BECEL CLASSIC 225 g; zabac: BECEL margarina 225G; ktc: BECEL NAMAZ CLASSIC 225g; kaufland: Becel Namaz masni 225g vg. |
| griz | 3858881081598 | 27,00 | ntl: GRIS PŠENIČNI 400 g FRANCK; trgovina-krk: GRIZ INSTANT 400 g KUT. FRAN; vrutak: GRIS FRANCK INST 400G -14/1-; stanic: GRIZ INSTANT 400 g FRANCK; metro: 400G FRANCK GRIS INSTANT VREĆI; gavranovic: PŠ.GRIZ FRANCK 400g; ktc: GRIS PŠENIČNI 400g FRANCK; plodine: PSENICNA KRUPICA INSTANT 400 G GRIS FRANCK; kaufland: Franck instant gris 400 g; ribola: GRIS PŠ.KRUP. 400 g FRANCK; studenac: GRIS INSTANT FRANCK 400 g; konzum: KRUPICA PŠENIČNA 400g FRANCK; roto: KRUPICA PŠENIČNA 400G FRANCK (14); tommy: GRIZ INSTANT 400 g FRANCK; branka: GRIS INSTANT PŠENIČNI 400G FRANCK; jadranka_trgovina: PŠENIČNI GRIZ INSTANT 400G FRANCK; lorenco: INST.GRIS 400 g FRANK; spar: GRIS INSTANT FRANCK 400 g; djelo_vodice: GRIS 400G FRANCK; bure: GRIS 400 g FRANCK; stridon: GRIS INSTANT 400 g FRANCK (14); trgocentar: GRIS PŠENIČNI 400G, FRANCK |
| dodatak_jelima | 3856020263416 | 29,00 | vrutak: N-VEGETA PODR 190G POVRTNA PASTA -12/1- TUBA; tommy: POVRTNA PASTA 190G TUBA PODRAVKA; bure: PASTA POVRTNA 190 g; konzum: PASTA POVRĆE TUBA 190g PODRAVKA; spar: VEGETA NAT.PASTA POVRTNA 190 g; branka: PASTA POVRTNA 190g TUBA; kaufland: Vegeta Natur Pasta povrtna 190g; ktc: PASTA POVRTNA 190g PODRAVKA; ntl: PASTA POVRTNA 190 g PODRAVKA; plodine: PASTA POVRTNA TUBA 190 G PODRAVKA; trgocentar: POVRTNA PASTA 190G TUBA,PODRAVKA (12); lorenco: POVRTNA PASTA 190g TUBA; trgovina-krk: PASTA POVRTNA VEGETA NATUR 190 gr TUBA; djelo_vodice: PASTA POVRTNA 190 G TUBA |
| maslinovo_ulje | 3859890446538 | 50,00 | ribola: ULJE EDM 500 ml ZLATNO ORGULA; jadranka_trgovina: MASLINOVO ULJE 0,5L EXTRA DJEVIČANSKO ZLATNO ORGULA |
| krumpir | 3859893072031 | 50,00 | lorenco: LIČKI KRUMPIR 5/1; metro: 10KG LIČKI KRUMPIR CRVENI |
| mrkva | 3859893211331 | 33,00 | spar: KUKURUZ ŠEĆERAC 3/1; plodine: MRKVA 500 G; metro: 6/1 JABUKA CRIPS PINK KOM PD |
| tvrdi_sir | 3858881194885 | 33,00 | plodine: SIR KRAVLJI 230 G AGROLAGUNA; studenac: SIR KRAVLJI ŠPIN 230 g; jadranka_trgovina: SIR TVRDI KRAVLJI 230G ŠPIN AGROLAGUNA; kaufland: Špin Sir tvrdi istarski kravlji45%mm230g; konzum: SIR TVRDI KRAVLJI 230G ŠPIN; vrutak: SIR KRAVLJI ŠPIN 230G -16/1; bure: SIR KRAVLJI 230G LOT:24157; djelo_vodice: SIR KRAVLJI 230G ŠPIN; metro: 230G ŠPIN KRAVLJI SIR |
| med | 5900658716801 | 25,00 | trgovina-krk: MEDENJACI S VOĆ. PUNJ. 200 gr PRE. ČOKOL. LAMBERTZ; ribola: MED.MIX VOĆE 200 g ULTRA; djelo_vodice: MEDENJACI 200G LAMBERTZ MULTIFRUIT; plodine: MEDENJACI PUNJENI JABUKOM I TRESNJOM 200 G LAMBERTZ |
| svjezi_sir | 3850355002498 | 50,00 | metro: 375GR PRESIDENT ZAG.SV.SIR 25%; ntl: SIR PRESIDENT ZAGREBAČKI 375 g DUKAT; ribola: SIR SVJ.ZAGR.375 g P; lorenco: DUKAT ZAGREBAČKI SIR 375g; roto: SIR SVJEŽI ZAGREB PRESIDENT 375g (9); kaufland: President Zagrebački svj. sir 25%mm 375g; spar: SIR SVJ.ZAGREBAČKI DUKAT 375 g; studenac: SIR ZAGREBAČKI DUKAT375 g; tommy: SIR SVJEŽI ZAGREBAČKI 375 g; trgovina-krk: SIR SVJEŽI ZAGREBAČKI 375 g DUKAT; stanic: PRESIDENT ZAGREBAČKI SIR 375 g, DUKAT; ktc: SIR SVJ.ZAGREBAČKI 375g DUKAT PRESIDENT; stridon: PRESIDENT ZAGREBAČKI SVJEŽI SIR 375 g DUKAT; trgocentar: SIR ZAGREBAČKI 375G 25% (8) DUKAT; gavranovic: SIR ZAGREBAČKI PRESIDENT SVJEŽI 375g 25%MM; konzum: SIR SVJ ZAGREB PRESIDENT 375g; bure: SIR SV.ZAGREB.375 g LOT:25102026; dukat: PRESIDENT ZAGREBAČKI SIR 375g; branka: SIR PRESIDENT ZAGREBAČKI 375g; djelo_vodice: ZAGREBAČKI SVJEŽI SIR 375G PRESIDENT; lidl: Dukat President Zagrebački sir; plodine: SIR SVJEZI ZAGREBACKI 375 G DUKAT; vrutak: N-SIR DUKAT ZAGREBAČKI 375G25%MM PRESIDENT -9/1-; boso: SIR SVJEŽ 375 g PRES.ZAGREBAČ |
| svjezi_sir | 4002174015008 | 50,00 | kaufland: Kerniger svježi zrnati sir 20% mm 200 g; trgovina-krk: SIR SVIJEŽI KERNINGER FRISCH ZRNATI STANIĆ |
| tvrdi_sir | 3859893066795 | 50,00 | vrutak: SIR 3\*1/8(675G) POKLON KUTIJKOLAN/ML.TRAPIST/DINARSKI 5/1; lorenco: KOMPLET OSMINA KMD 675g |
| tjestenina | 8005121031010 | 50,00 | stridon: PAPPARDELLE UOVO (101) 500 GR (12) DIVELLA (IT); branka: TJESTENINA DIVELLA PAPPARDELLE 500g |
| kecap | 50157655 | 50,00 | kaufland: Heinz ketchup blagi 342 g; bure: HEINZ KETCH. 342 g BLAGI |
| tjestenina | 3859889154598 | 50,00 | branka: TJESTENINA REZANCI SITNI S JAJIMA 400g; ktc: FIDELINI JUŠNI KRATKI 400g |
| tjestenina | 8076809523776 | 45,00 | konzum: TIJESTO FETTUCCINE LC 500g BARILLA; metro: 500G BARILLA FETTUCCIN BEZ JAJ; roto: TIJESTO FETTUCCINE LC 500G BARILLA (12); tommy: TJ.BARILLA FETTUCCINE 500 g; lorenco: TJEST.PAPPARDELLE 500 g; plodine: TJESENINA FETTUCCINE 500 G BARILLA KUTIJA; ktc: BARILLA FETTUCCINE 500g; spar: TJES.BARILLA FETTUCCINE 500 g; ribola: TJ.BARILLA PAPPARDEL LE 500G; jadranka_trgovina: TJESTENINA FETUCCINE 500G BARILLA; trgovina-krk: TJEST. FETTUCCINE 500 g AWT |
| dodatak_jelima | 8600947030317 | 25,00 | stanic: ZAČIN ZA RIBLJU JUHU 90 g; kaufland: Aleva dod. jelima za riblju juhu 90 g; boso: DODAT ALEVA 90 g ZA RIB.JUHU; ntl: DODATAK JELIMA SA ZAČINIMA ZA RIBLJU JUHU 90g ALEVA |
| tjestenina | 8004350130556 | 45,00 | ntl: TJEST. PASTA ZARA CHIFFERI RIGATI 500G; lorenco: TJEST. 55 CHIFF RIg 500 g; roto: TIJESTO CHIFFERI RIGATI 55 500g ZARA (10); trgovina-krk: PASTA ZARA 055 CHIFFERI RIGATI 500G; djelo_vodice: PASTA ZARA CHIFFERI 500G; zabac: PASTA ZARA CHIFFERI RIGATI 500 G; konzum: TIJESTO CHIFFERI RIGATI 55 500g ZARA; ribola: TJ.CHIFFERI 55 500 g RIGATI PASTA ZARA; kaufland: Pasta Zara 055 chifferi rigati b.j.500g; studenac: TJ. PASTA ZARA CHIFF RIGATI BR. 55 500 g; branka: TJESTENINA PASTA ZARA CHIFFERI RIGATI 500g |

30 grupa koje prelaze iz člana (2D) u `ambiguous`:

| namirnica | grupa | m % | x % | nazivi po lancu |
|---|---|---|---|---|
| med | 4000521010294 | 63,00 | 31,00 | metro: 300G VITALIS CRUN PLUS MED/BAD; kaufland: Dr.Oetker vitalis crunchy med badem 300g; jadranka_trgovina: MUESLI CRUNCHY PLUS MED BADEM 300G VITALIS; konzum: MUESLI KNUSPER MED BADEM 300g VITALI; lorenco: DR.OETKER CRUNCHY PLUS MED BADEM; djelo_vodice: MUSLI CRUNCHY MED BADEM 300g; vrutak: MUSLI DR OETKER 300G MED I BADEM CRUNCHY PLUS -8/1-; spar: MUSLI VITALIS MED,BADEM 300 g; bure: MUESLI VITALIS 300 gHONEY-ALMOND; trgocentar: VITALIS CRUNCHY PLUS MED BADEM 300G, DR.OETKER; ribola: MUESLI CHR.MED 300 g VITALIS DR OETKER; tommy: MUESLI CRUN.PL. MED 300 g DR.O; roto: MUESLI KNUSPER MED BADEM 300G VITALI (8); studenac: MUESLI MED BADEM VITALIS 300 g; plodine: MUSLI PLUS MED BADEM 300 G CRUNCHY DR OETKER; trgovina-krk: MUSLI CRUNCHY PLUS MED BADEM 300 g DR OETKER |
| med | 5949040205158 | 75,00 | 17,00 | gavranovic: PECIVO TWIST MORSKA SOL I MED 180g - ELEPHANT; tommy: SNACK SOL MED 180 g ELEPHANT; djelo_vodice: ELEPHANT TWIST - MORSKA SOL i MED 180G; ntl: TRAJNO PEC. ELEP.TWIST - MORSKA SOL I MED 180g; plodine: KREKER MORSKA SOL I MED 180 G ELEPHANT; stanic: ELEPHANT TWIST - MORSKA SOL I MED 180 g; spar: PECIV.ELEP.TWIST SOL-MED 180 g; ktc: ELEPHANT TWIST MORSKA SOL I MED 180g; kaufland: Elephant Pecivo sl.morska sol,med180 g; konzum: KREKE TWIST SOL I MED 180 g ELEPHANT; metro: 180G ELEPHANT TWIST SOL I MED; ribola: KREK.M.SOL&MED 180 g ELEPHANT |
| sol | 9001414040034 | 69,00 | 31,00 | kaufland: Kotanyi himalajska sol 120 g bočica; spar: SOL HIMALAJ.SITNA KOTANY120 g; djelo_vodice: HIMALAJSKA SOL 100ML; studenac: ZAČIN HIMALAJSKA SOL 120 g KOT.; bure: SOL HIMALAJSKA 100 ml STAKLO; plodine: HIMALAJSKA SOL 120 G KOTANY BOCICA; ribola: SOL HIMALAJSKA 120 g STAKLO KOTANYI; branka: SOL HIMALAJSKA BOČICA 120g; trgovina-krk: ZAČIN SOL HIMALAJSKA BOČICA KOTA; konzum: HIMALAJSKA SOL BOČ 120G KOTANYI; ktc: SOL HIMALAJSKA 100mL ST KOTANYI; lorenco: HIMALAJSKA SOL JODIRANA STAKLO 100; tommy: SOL HIMALAJSKA STAK. 120 g KOT |
| zobene_pahuljice | 8595054907761 | 67,00 | 25,00 | kaufland: Dobre Pahuljice zobene bobič.voće 300g; tommy: ZOBENE PAH. ŠUM.VOĆE 300 g DOB; zabac: Dobre zobene pahuljice 300g BERRIES; branka: PAHULJICE ZOBENE BERRIES 300g; vrutak: ZOBENE PAHULJICE 300G BERRIES; konzum: PAHULJICE ZOBENE BERRIES 300g; spar: DOBRE ZOBENE PAH.BOB.VOĆ.300 g; plodine: ZOBENE PAHULJICE SUMSKO VOCE 300 G BIOPLOD; ribola: PAHULJ.ZO.BO.300 g D OBRE PAHULJICE; lorenco: DOBRE ZOBENE PAHULJICE 300g BERRIES; ntl: PAHULJICE ZOBENE BERRIES 300 g DOBRE; gavranovic: ZOBENE PAHULJICE DOBRE BERRIES 300g |
| sol | 3856020222314 | 80,00 | 20,00 | ribola: SOL MORSKA 100 g VE GETA MAESTRO; plodine: MORSKA SOL MLINAC 100 G VEGETA MAESTRO; konzum: ZAČIN SOL MORSKA ML 100g VEGETA MAESTRO; lorenco: VEGETA MAESTRO MORSKA SOL 100G; ktc: MORSKA SOL GRUBO MLJEVENA 100g PODRAVKA; stridon: VEGETA MAESTRO MORSKA SOL M.100 G (6) PODRAVKA; tommy: VEGETA MAESTRO MORSKA SOL GRUBO MLJEVENA 100G; spar: ZAČ.SOL MORSKA VEG.MAES.100 g; bure: SOL MORSKA 100 g KRUNA PODR.; djelo_vodice: MORSKA SOL GRUBO MLJEVENA VEGETA MAESTRO BOČICA 100G |
| papar | 9001414274057 | 80,00 | 20,00 | plodine: SPICES DRINKS PAPAR CRNI, ZRNO 50 G; spar: ZAČ. PAPAR S&D CRNI ZRNO 50 g; ntl: ZAČIN ZA KOKTELE SPICES & DRINKS PAPAR CRNI 50 g KOTANYI; lorenco: PAPAR CRNI ZRNO SiD STAKLO 100ML; kaufland: Kotany papar crni zrno, bočica 50 g |
| papar | 9001414050026 | 54,00 | 46,00 | trgovina-krk: PAPAR ZELENI U SALAMURI 100 g KOTAN; ribola: PAPAR ZEL.SAL. 100 g KOTANYI; spar: ZAČ.PAPAR ZELEN.KOTANYI 100 g; tommy: ZAČIN PAPAR ZEL/SAL. 100 g KOT; bure: PAPAR ZELENI 100 g SALAMURA UG.; djelo_vodice: PAPAR ZEL.SALAMURA; trgocentar: KOTANY ZELENI PAPAR U ZRNU 100G; lorenco: ZELENI PAPAR 100 g KOTANYI; metro: 100G KOTANYI PAPAR ZELENI U SA; vrutak: KOTANYI 100G PAPAR ZELENI USALAMURI -24/1-; roto: PAPAR ZELENI U SALAMURI 100g KOTANYI (24); gavranovic: KOTANYI PAPAR ZEL.U SALAMURI 100g; studenac: ZAČIN PAPAR ZELENI U SALAMURI 100 g KO |
| tjestenina | 8008857300771 | 83,00 | 17,00 | jadranka_trgovina: TJESTENINA SPAGHETTI TAGLIATI 077 500G REGGIA; ntl: TJESTENINA TAGLAITI 500g REGGIA; trgovina-krk: TJEST. TAGLIATI 500 g REGGIA NTL; trgocentar: SPAGETTI TAGLIATI 77 (SITNI REZANCI) 500G PASTA REGGIA (24); bure: TJ.FIDELINI 77 500 gREGGIA (SPAGET.TAGLI; ribola: TJ.SPAGHETTI 500 g TAGLIATI JUHA REGGIA |
| kiseli_kupus | 3859891493098 | 56,00 | 11,00 | studenac: KIS. ZELJE MIX ZA SARMU 1100 g; gavranovic: ZELJE KISELO MIX ZA SARMU 1KG MADIG; lorenco: MADIG MIX ZA SARMU 1000g; eurospin: KUPUS KISELI MIX ZA SARMU 1kg; spar: KUPUS KIS.MIX ZA SARMU 1 kg; tommy: KUPUS KIS. MIX ZA SARMU 1000 g; trgovina-krk: KUPUS KISELI MIX MADIG ZA SARMU 1 kg NTL; konzum: KUPUS KISELI MIX ZA SARMU MADIG; plodine: SARMA MIX 1 KG KISELI KUPUS MADIG |
| sol | 3870009000144 | 80,00 | 20,00 | vrutak: SOL KAMENA 250G SOLJENKA -15/1- TUZLA; kaufland: Tuzla kuhinjska sol jodirana 250g; spar: SOL KUHINJ. TUZLA SITNA 250 g; ktc: SOL KAMENA DOZA 250g TUZLA; plodine: SOL KUHINJSKA JODIRANA 250 G TULJAK TUZLA |
| med | 5900617037152 | 86,00 | 14,00 | kaufland: Sante Granola Gold med i oraš.plod.300g; plodine: MUESLI GRANOLA MED I ORASASTI PLODOVI 300 G SANTE; tommy: MUESLI GRAN. NUT/MED 300 g SAN; spar: GRAN.SANTE ORAŠ.PLOD.MED 300 g; jadranka_trgovina: ŽITARICE GRANOLA GOLD ORASI+MED 300G SANTE; konzum: MUESLI GRANOLA ORAŠ PLOD MED 300g SANTE; ribola: GRANOLA 300 g ORAH/ MED SANTE |
| majoneza | 3856015304339 | 86,00 | 14,00 | kaufland: Zvijezda čili majoneza tuba 165g; studenac: MAJONEZA ZV. 165G ČILI TUBA; vrutak: N-MAJONEZA ZVIJEZDA 165G -12/1 ČILI TUBA; plodine: MAJONEZA CILI 165 G TUBA ZVIJEZDA; roto: MAJONEZA ČILI 165G ZVIJEZDA (12); konzum: MAJONEZA ČILI 165g ZVIJEZDA; trgocentar: MAJONEZA CHILI 165G TUBA (12) ZVIJEZDA; stridon: MAJONEZA ČILI TUBA 165 g (12) ZVIJEZDA; gavranovic: MAJONEZA CHILLI 165g ZVIJEZDA; lorenco: ZVIJEZDA ČILI MAJONEZA 165g; branka: MAJONEZA ČILI 165g; trgovina-krk: MAJONEZA ČILI 165 g ZVIJ; ktc: MAJONEZA TUBA ČILI 165g ZVIJEZDA; jadranka_trgovina: MAJONEZA 165G ČILI TUBA ZVIJEZDA |
| kukuruz | 3859893512254 | 70,00 | 30,00 | gavranovic: KUKURUZ PEČENI SLANI BBQ 60g NATURA; plodine: KUKURUZ PECENI SLANI BBQ 60 G SUPER SNACK NATURA; spar: KUKURUZ PEČ.SLANI NATURA 60 g; lorenco: KUKURUZ PEČENI SALNI BBQ 60g S.SNAC; studenac: KUKURUZ PEČ.SL. NATURA 60 g; trgocentar: KUKURUZ PEČENI SLANI 60G BBQ SUPER SNACK; trgovina-krk: KUKURUZ PS BBQ NATURA 60 g; vrutak: N-KUKURUZ NATURA 60G PEČENI SLANI BBQ -20/1- SUPER SNACK; jadranka_trgovina: KUKURUZ PEČENI SLANI BBQ 60G; ribola: KUKURUZ PEČENI 60 g SLANI NATURA |
| papar | 9001414040867 | 60,00 | 10,00 | branka: \*NE\*PAPAR MJEŠAVINA 35G STAKLO KOTANYI; trgovina-krk: ZAČIN MJEŠAVINA PAPRA STAKLO 40 g KOTANY; vrutak: KOTANYI 40G PAPAR ŠARENAMJEŠAVINA STAKLO -4/1-; spar: ZAČ.PAPAR MJEŠ.KOTANYI 40 g; plodine: PAPAR MIX 40 G STAKLO KOTANYI; gavranovic: KOTANYI PAPAR MJEŠAVINA STAKLO 40g; lorenco: ZAČIN MJEŠ. PAPRA 35 g KOTANYI; bure: ZAČIN MJEŠ.PAPRA 100g; studenac: ZAČIN PAPAR ŠARENI 40 g KOT.; tommy: ZAČIN PAPAR MJEŠ.40 g KOTANY |
| tuna | 8004030860025 | 0,00 | 86,00 | kaufland: Rio Mare Insal.sal.tuna cous cous2x160g; konzum: TUNJ SALATA COUS COUS 2X160g RIO MARE; lorenco: TUNA -COUS-COUS SAL.2\*160g BOWL.; tommy: TUNA SALATA CUS CUS 2X160 G RIO MARE; spar: TUNA SAL.RIO MARE COUS 2X160 g; metro: 160GX2 RIO MARE INSALA.CUS CUS; plodine: TUNA COUS-COUS SAL.2X160G BOWL |
| grah | 3083680001793 | 67,00 | 17,00 | konzum: GRAH BIJELI RAJČICA 430/200g BONDUELLE; vrutak: N-GRAH BIJELI BONDUELLE 400G S RAJČICOM; plodine: BRETONA BIJELI GRAH U UMAKU OD RAJCICE 430 G; lorenco: BONDUELLE BIJELI GRAH S RAJČ.400g; spar: GRAH BONDUELLE BRETONA 430 g; kaufland: Bonduelle Bretona 430g/200g |
| piletina | 3850159113154 | 60,00 | 20,00 | konzum: PILE GAVELINO POD VINDIJA; spar: PILE GAVELINO; ribola: GAVELINO VINDIJA; studenac: PILE GAVELINO VINDIJA KOKA kg; plodine: GAVELINO PILE ZA PECENJE CEKIN (11315) |
| jaja | 5200701000063 | 67,00 | 17,00 | trgovina-krk: SRCE JAJE PEPPA PIG 10G; vrutak: SRCE PL. PEPPA PIG 10G; studenac: BOM. JAJE PEPA PIG 10 g; ribola: PEPPA PIG JAJE 10 g; konzum: JAJE S BOMBONIMA PEPA PIG 10g; ntl: JAJE IZNENAĐENJA 10 g MIX LICENCA |
| papar | 9001414440834 | 86,00 | 14,00 | lorenco: PAPAR CRVENI ZRNO KOKTEL SND ST 100; gavranovic: KOTANYI PAPAR CRVENI ZRNO 25g SPICE DRINKS; spar: ZAČIN PAPAR CRVENI ZRNO 25 g; ntl: ZAČIN ZA KOKTELE SPICES & DRINKS PAPAR CRVENI 25 g KOTANYI; plodine: SPICES DRINKS PAPAR CRVENI ZRNO 25 G; konzum: PAPAR CRVENI ZRNO S&D 25g KONTAYI; vrutak: KOTANYI KOKTEL PAPAR CRVENI SPICE i DRINKS 25G ZRNO |
| tjestenina | 8710605028430 | 71,00 | 29,00 | ntl: TJESTENINA OD PŠ. BRAŠNA S JAJIMA 250G NIKAS; konzum: TJESTENINA S JAJIMA GNIJEZDA GO TAN 250g; kaufland: Go Tan tjest.s jajima za Wok 250 g; ribola: TJEST.GO TAN 250g; plodine: TJESTENINA S JAJIMA GNIJEZDA 250 G NOODLES GO TAN; vrutak: TJESTENINA GO-TAN 250G EGG WOK NOODLES -8/1-; spar: TJESTENINA GOTAN NEST 250 g |
| dodatak_jelima | 3856020228910 | 90,00 | 10,00 | kaufland: Vegeta Natur Grill Burger classic 30 g; plodine: VEGETA NATUR BURGER 30 G CLASSIC; trgocentar: VEGETA NATUR BURGER CLASSIC VR.30G (18) (PAL 252) PODRAVKA; tommy: VEGETA NATUR BURGER VR.30 g PO; stridon: VEGETA NATUR BURGER CLASSIC 30 g (18); bure: VEGETA VR.BURG. 30 gCLASSIC; konzum: ZAČIN BURGER CLASSIC VR 30g VEGETA NATUR; lorenco: VEGETA NATUR BURGER CLASSIC VR.30g; trgovina-krk: VEGETA NATUR BURGER CLASSIC 30 g VREĆICA POD; spar: ZAČIN VEGETA NATUR BURGER 30 g |
| sol | 3856020267216 | 83,00 | 17,00 | spar: ZAČ.V.MAEST.SITNA MOR.SOL 110g; bure: VEGETA MAESTRO 110g SITNA SOL; plodine: VEGETA MAESTRO SITNA MORSKA SOL POSIPAC 110 G BOCICA; lorenco: VEGETA MAESTRO SITNA MORSKA SOL; tommy: VEGETA MAESTRO SITNA MORSKA SOL POSIPAČ 110 g; konzum: SOL SITNA MORSKA 110g VEGETA MAESTRO |
| piletina | 3850159142321 | 77,00 | 15,00 | stridon: CEKIN KRILCA BUCKET 500 g 14232 VINDIJA; vrutak: N-VIN KRILCA BUCKET 500G -4/1-; jadranka_trgovina: KRILCA BUCKET CEKIN 500G VINDIJA; kaufland: Cekin Pečena pileća krilca 500 g; ktc: CEKIN KIDS BUCKET KRILCA 500g; ntl: KRILCA PILEĆA PEČENA SM 500 g CEKIN; boso: KRILCA CEKIN 500 g BUCKET; trgocentar: CEKIN KRILCA BUCKET 500G; spar: PILE.KRILCA BUCKET CEKIN 500 g; ribola: PIL.KRIL.BUCK. 500 gVINDIJA; plodine: CEKIN KRILCA BUCKET 500 G; branka: KRILCA BUCKET CEKIN 500g; trgovina-krk: CEKIN KRILCA BUCKET 500G |
| maslac | 3856015325419 | 86,00 | 14,00 | ktc: MARGO S MASLACEM 225g ZVIJEZDA; tommy: MARGO S MASLACEM 225 G; lorenco: MARGO S MASLACEM 225G ZVIJEZDA; boso: MARG. MARGO 225 g S MASLACEM; branka: MARGARIN MARGO MASLAC 225g; kaufland: Margo Namaz miješani s maslacem 225g; trgovina-krk: MARGO S MASLACEM 225 gr; stridon: MARGO S MASLACEM 225 g ZVIJEZDA (16); konzum: MARGO S MASLACEM 225g; plodine: MARGO S MASLACEM 225 G ZVIJEZDA; trgocentar: MARGO S MASLACEM 225G (16),ZVIJEZDA; vrutak: N-MARGO S MASLACEM 225G -16/1-; spar: NAMAZ MARGO S MASLACEM 225 g; jadranka_trgovina: MARGARIN MARGO S MASLACEM 225G ZVIJEZDA |
| senf | 5949040202058 | 61,00 | 22,00 | konzum: KREKER MED I SENF 70 g ELEPHANT; ktc: ELEPHANT MED,SENF I LUK 70g; lorenco: ALKA ELEPH.TS PECIVO 70g; djelo_vodice: ELEPHANT TRAJNO SLANO PECIVO - MED, SENF i LUK 70g; plodine: SNACK MED/SENF/LUK 70 G ELEPHANT; spar: KRE.ELEPHANT SENF&MED&LUK 70 g; studenac: KREK. ELEPHANT SENFLUK 70 g; stanic: ELEPHANT PECIVO MED, SENF, LUK 70 g; branka: PECIVO ALKA ELEPHANT MED-SENF-LUK 70g; trgovina-krk: ELEPHANT TRAJNO SLANO PECIVO - MED,SENF I LUK 70 g; vrutak: ELEPHANT 70G TRAJNO SLANO PECIVO ALKA MED, SENF, LUK; ntl: TRAJNO SLANO PECIVO ELEPHANT 70 g MED,SENF I LUK; kaufland: Elephant slano pecivo med senf i luk 70g; metro: 70G ELEPHANT FLAT MED SENF LUK; ribola: KREK.MED SEN.LU.70 g ELEPHANT; boso: KREKE ELEPHANT 70 g MED SENF LUK; jadranka_trgovina: GRICKALICE ELEPHANT MED, SENF I LUK 70G; tommy: SNACK MED SENF LUK 70 g ELEPHA |
| senf | 5949040204953 | 60,00 | 10,00 | stridon: ALKA ELEPHANT TS PECIVO-KOMAD.S OKUS.MEDA 14\*75 g; konzum: PER LOMLJ MED SENF LUK 75 g ELEPHANT; ktc: ELEPHANT KOMADIĆI MED,SENF I LUK 75g; kaufland: Elephant Komadići med,senf i luk75g; ribola: PERECI ME.SE.LU.75 g ELEPHANT; plodine: PEREC KOMADICI S OKUSOM MEDA,SENFA I LUKA 75 G ELEPHANT; ntl: TRAJNO SLANO PECIVO ELEPHANT PRETZEL 75 g MED, SENF I LUK; gavranovic: PECIVO KOMADIĆI MED,SENF I LUK 75g ELEPHANT; boso: KREKE ELEPHANT 75 g MED SENF LUK; tommy: SNACK MED SENF LUK 75 g ELEPHA |
| pileca_prsa | 3856020257064 | 57,00 | 14,00 | tommy: PILEĆA PRSA 60 G LINO NARESCI PODRAVKA; spar: PILEĆA PRSA LINO NJUPAL. 60 g; ktc: PILEĆA PRSA 60g LINO; ribola: ŠUNKA PILEĆA 60 g LINO PODRAVKA; plodine: LINO PILECA PRSA 60 G PODRAVKA; konzum: LINO PILEĆA PRSA 60 g; stridon: LINO PILEĆA ŠUNKA 60 g (10) PODRAVKA |
| majoneza | 3856015324689 | 81,00 | 14,00 | branka: MAJONEZA ČILI 85g; djelo_vodice: ČILI MAJONEZA 85g; gavranovic: MAJONEZA CHILLI VREĆICA 85g ZVIJEZDA; studenac: MAJONEZA ČILI 85g ZVIJ.; zabac: CHILI MAJONEZA 75% 85 G; stridon: MAJONEZA ČILI ZVIJEZDA 85 g (25); vrutak: N-MAJONEZA ZVIJEZDA 85G -25/1 ČILI; konzum: MAJONEZA ČILI PVC 85g ZVIJEZDA; boso: MAJON ZVIJE 85 g DELIK.ČILI; jadranka_trgovina: MAJONEZA 85G ČILI VREĆICA ZVIJEZDA; trgovina-krk: MAJONEZA ČILI 85G; lorenco: ZVIJEZDA MAJONEZA ČILI 85G; metro: 85G ZVIJEZDA MAJONEZA ČILI; roto: MAJONEZA ČILI PVC 85g ZVIJEZDA (25); kaufland: Zvijezda majoneza čili 85 g; trgocentar: MAJONEZA ČILI 85G ,ZVIJEZDA; ribola: MAJONEZA ČILI 85 g ZVIJEZDA; spar: MAJONEZA CHILI ZVIJEZDA 85 g; ktc: MAJONEZA ČILI 85g ZVIJEZDA; lidl: Zvijezda Majoneza Čili; tommy: MAJONEZA ČILI 85 G ZVIJEZDA |
| sol | 9001414046241 | 75,00 | 25,00 | konzum: MORSKA SOL BOČ 120 g KOTANYI; bure: SOL SITNA 100ml STAKLO; plodine: MORSKA SOL 120 G BOCICA KOTANYI; kaufland: Kotanyi Sol morska sitna jodirana 120g; spar: MORSKA SOL KOTANY 120g; tommy: SOL MORSKA JODIRANA 120 g KOTAN; vrutak: KOTANYI 100ML MORSKA SOL SITNA STAKLO -4/1-; metro: 120G KOTANYI MORSKA SOL BOČICA |
| pileca_prsa | 3850159123306 | 59,00 | 35,00 | konzum: PRSA PILEĆA U OVITKU NAR 100g; lorenco: PILEĆA PRSA 100g; djelo_vodice: PILEĆA PRSA 100G VIN.; vrutak: VIN PILEĆA PRSA 100G; ribola: PIL.PRS.U OV.100 g VINDIJA; plodine: PILECA PRSA 100 G VINDIJA; tommy: PILEĆA PRSA NARESCI 100 g; trgocentar: PILEĆA PRSA 100G, VINDIJA; jadranka_trgovina: SALAMA PILEĆA PRSA 100G CEKIN VINDIJA; kaufland: Cekin Pileća prsa 100 g; stridon: PILEĆA PRSA 100 g VINDIJA; ktc: PILEĆA PRSA 100g VINDIJA; spar: PILEĆA PRSA 100 g; ntl: SALAMA PRSA PILEĆA 100 g VINDIVAC; gavranovic: CEKIN PILEĆA PRSA NAREZAK 100g; studenac: PIL. PRSA U OVIT. 10 0g VINDVAC; trgovina-krk: SALAMA PILEĆA PRSA 100 g VIND |

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
| tvrdi_sir | strong | ktc: SIR EMMENTALER CCA 3kg SPOMLEK |
| tjestenina | strong | plodine: TJ.CACCAV.TRIC.3 KOM 120 G |
| tvrdi_sir | strong | plodine: SIR EMMENTALER BLOK 2,15 KG SALZBURGMILCH |
| jogurt | strong | spar: JOG.GRČKI TIP 10%NP BIO 400 g |
| tjestenina | strong | lorenco: MLI.VITA KOREN.FIDELINI 61 250g; djelo_vodice: TJ.VITA FIDELINI MRKVA 250G; tommy: TJ.VITA FIDELINI 61 250 g MLIN |
| tvrdi_sir | strong | kaufland: The old farm.Sir Cheddar Vintage50% 200g; spar: CHEDDAR MINI VINTAGE 200 g |
| pileca_prsa | strong | konzum: ODRESCI PILEĆEG FILEA 400g AIA; spar: PILEĆI ODRESCI FILEA 400 g; plodine: PILECI FILE ODRESCI 400 G AIA |
| tjestenina | strong | trgovina-krk: LAZANJE GASTRO TS |
| tjestenina | strong | eurospin: \*LASAGNE PEČENE |
| tjestenina | strong | lorenco: REZANCI ŠIROKI 400g STARA PUŠNICA |
| tjestenina | weak | ribola: ULTRA-GOM.RIG.500g; djelo_vodice: TJE.GOMITI 27 500G PAGANI |
| tjestenina | strong | plodine: LASAGNE 500 G DE CECCO TJESTENINA; konzum: TIJESTO LASAGNE 500 g DE CECCO; vrutak: TJEST LASAGNE br. 502 500G DE CECCO -24/1- |
| tjestenina | strong | stridon: DOMAĆE ŠKOLJKICE KAKAO PRELJEV 205G (16) CONVOCO |
| tvrdi_sir | strong | plodine: SIR CHEDDAR BIJELI 200 G DUBLIN DAIRY EUROSER |
| tvrdi_sir | strong | konzum: SIR MAASDAM 300 g DELISO |
| tjestenina | strong | tommy: TJ.DURUM VIJAK 500 g PAŠTARIJ; studenac: TJ. PAŠTARIA DURUM VIJAK 500 g; plodine: TJESTENINA VIJAK 500 G PASTARIA PIK VRECICA; bure: TJ.VIJAK 500G DURUM TONKA; gavranovic: TJ.PAŠTARIA 500g VIJAK |
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
| tjestenina | strong | studenac: TJ. ŠURLE KLARA M. 500 g; plodine: TJESTENINA SURLE 500 G KLARA MARIC; lorenco: ŠURLE 500g; djelo_vodice: ŠURLE K.M. 500G; tommy: TJ.ŠURLE 500 g KLARA M; vrutak: TJEST KLARA M ŠURLE 500G-10/1- 112; roto: TIJESTO ŠURLE 500G KLARA M (10); metro: 500G KLARA M. ŠURLE BEZ JAJA; jadranka_trgovina: TJESTENINA ŠURLE 500G KLARA; kaufland: Klara M šurle 500g; konzum: TIJESTO ŠURLE 500g KLARA M; ribola: TJ.ŠURLE 500 g KLAR A MARIĆ; spar: TJ.KL.MARIĆ ŠURLE 500 g; bure: TJ.ŠURLE 500 g KLARAMARIĆ |
| tvrdi_sir | strong | plodine: SIR CHEDDAR MATURE 200 G PRESIDENT DUKAT; dukat: PRESIDENT CHEDDAR ZRELI 200g; studenac: SIR CHEDDAR MATURE PRESIDENT 200 g; konzum: SIR POLU CHEDDAR MATURE 200g; vrutak: N-SIR PRESIDENT CHEDDAR MATURE 200G; spar: SIR CHEDD.MATURE PRESID.200 g; tommy: SIR CHEDDAR MATUR 200 g PRESID |
| mlijeko | strong | ribola: MLIJ.TR.0,5% 1L BO.D; plodine: MLIJ.DUKAT 0.5% 1 L BOCA DUKAT(660KOM/PAL) |

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
| kozmetika → hrana | 1 |
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
| tommy | RAJČICA PASIRANA 500 g FRUCTAL |
| plodine | RAJCICA TERNETTO 250 G |
| konzum | RAJČICA PASIRANA 500g PODRAVKA |
| konzum | RAJČICA PASIRANA 700g STAR |
| kaufland | Podravka Ćufte u umaku od rajčice 400g |
| kaufland | Cirio Rajčica sjeckana luk i češnj.390g |
| tommy | RAJČICA COCKTAIL 400g TREŠNJAR |
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
| plodine | GRASAK MRKVA 400 G O'PLANT |
| spar | KAŠICA HIPP MLADA MRKV.125 g |
| kaufland | Vindi višnja,limun,mrkva 2 l brick |
| plodine | SOK JABUKA MRKVA BIO 200 ML HIPP |
| studenac | TJ. MARODI R.KAŠ. S MRKVOM 400 g |
| plodine | GRASAK MRKVA 450 G PODRAVKA |
| tommy | KEKS NUTRI MRKVA 133 g JAFFA |
| plodine | GRASAK-MRKVA FRIZO 400 G PLODINE |
| kaufland | Koleda jušni rez. s mrkvom i jajima 400g |
| plodine | TJESTENINA KRUZICI S MRKVOM 250 G KLARA MARIC |

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
| plodine | KIS.KRASTAVCI 180G DELIKATES INTERMIMS STAKLO |
| plodine | KRASTAVCI DELIKATES 680 G CAMPO |
| kaufland | KLC.Krastavci kiseli 670g/360g_OC |
| studenac | SOK LIMUN KRASTAVAC TOCO 1,5 l |
| plodine | KISELI KRASTAVCI 670 G II KLASA ZVIJEZDA |
| tommy | KRASTAVCI KIS. 6-9cm 670 g T! |
| spar | KRASTAVCI SPAR KORN.CHIL.350 g |
| konzum | KRASTAVAC K PLUS I KL 350g |
| plodine | KIS.KRASTAVCI EXC.350 G DOORA |
| plodine | DOVE SAPUN 90G KRASTAVAC SVJEZI |

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
| plodine | SALATA ZELENA 100 G |
| kaufland | Salata zelena rucola 125g |
| spar | Salata zelena sa sirom |
| lidl | Salata Iceberg |
| plodine | SALATA ZELENA BIO 100G |
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
| kaufland | KLC.Snack potato kis.vrhnje i luk 125g |
| kaufland | Čipi Čips sir i luk 120g |
| plodine | KREKER LUK 100 G TUC |
| spar | FLIPS BOBI RINGS VRH.-LUK 70 g |
| tommy | ČIPS RIŽA VRH/LUK 60 g RICE UP |
| konzum | LUK U GRANULAMA 40g BOČ KOTANYI |
| plodine | KIKIRIKI U HRSKAVOM OMOTACU LUK I VRHNJE 150 G BITS BYTES |
| konzum | PERECI LOMLJENI MINI MED SENF LUK 125g ELEPHANT |
| spar | PAŠ.S LUK. I BUČ.SJ.150 g |
| studenac | KREKER TUC LUK 100 g |

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
| plodine | RIZOTO S PILETINOM I TIKVICAMA PLODINE |
| tommy | TIKVICE PEČENE PORCIJA |
| studenac | RIŽOTO S PILETINOM I TIKVICAMA 2,5 kg |
| plodine | PASTA S KOZICAMA I TIKVICAMA |
| studenac | 16794 LAZANJE TIKVIC E I PROVOLA 350 g |
| plodine | RIZOTO S PILETINOM I TIKVICAMA PORCIJA |
| plodine | RIZOTO S PILETINOM I TIKVICAMA 2,5 KG AMERICAN DONUT |
| plodine | PASTA S KOZICAMA I TIKVICAMA PORCIJA |
| konzum | MJEŠAVINA BULGUR I TIKVICA 350g |
| spar | OROZOTTO TIKVICE BOS.300 g |


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
