# Pregled Koraka 2D (arhiva 2026-10-19)

Izvještaj generira `scripts/step2d_review.py` nad izgrađenom bazom.

## 1. Pripadnost grupe (EAN) namirnici

Grupa pripada namirnici (`clean.staple_groups.status = 'member'`) ako naziv prolazi pravila u više od 50 % lanaca grupe i nijedan isključeni naziv nema udio ≥ 25 % lanaca; inače je `ambiguous` i nije u zadanom izboru (`find_products(include_ambiguous=True)` je vraća); `excluded` ako nijedan naziv ne prolazi. Prije: dovoljan je bio jedan naziv, a bilo koji isključeni naziv rušio je cijelu grupu. Atributi grupe (`clean.staple_group_attrs`): vrijednost iz naziva ima prednost pred zadanom, zatim broj lanaca. Neprehrambeni član (kategorija) ne računa se kao pogodak naziva.

**Cijena pravila:** grupe u kojima većina lanaca proizvod zove skraćeno ili samo markom ispadaju („PRAŠ. PEC. 12 g Dr.Oetker“, „FUŽI 250g AURELIA“, „PASTA ZARA 573 SPIRALI“, „SIR ORODUR“), jer `must_match` ne pogađa takve nazive. Najviše gubi tjestenina (nazivi oblika bez riječi tjestenina). Rješenje bi bili sinonimi oblika u `must_match` (fuži, spirali, penne…) ili niži prag za grupe bez isključenih naziva; nisam ih uvodio jer pravilo traži većinu.

Namirnice s promjenama (broj grupa):

| namirnica | članova prije | članova sada | dvosmislenih | ispalo | ušlo |
|---|---|---|---|---|---|
| tjestenina | 1429 | 1229 | 223 | 202 | 2 |
| tvrdi_sir | 992 | 870 | 124 | 123 | 1 |
| jogurt | 397 | 337 | 127 | 63 | 3 |
| med | 462 | 409 | 82 | 57 | 4 |
| cokolada_za_kuhanje | 57 | 35 | 22 | 22 | 0 |
| dodatak_jelima | 106 | 86 | 32 | 20 | 0 |
| svjezi_sir | 155 | 135 | 31 | 20 | 0 |
| mljevena_paprika | 103 | 84 | 20 | 19 | 0 |
| piletina | 609 | 593 | 23 | 18 | 2 |
| sunka | 919 | 902 | 20 | 17 | 0 |
| slatko_vrhnje | 38 | 25 | 13 | 13 | 0 |
| mlijeko | 246 | 234 | 27 | 12 | 0 |
| maslinovo_ulje | 344 | 333 | 14 | 11 | 0 |
| majoneza | 185 | 177 | 18 | 10 | 2 |
| vrhnje_za_kuhanje | 80 | 70 | 10 | 10 | 0 |
| maslac | 193 | 185 | 27 | 9 | 1 |
| margarin | 99 | 90 | 9 | 9 | 0 |
| riza | 452 | 443 | 16 | 9 | 0 |
| griz | 38 | 29 | 9 | 9 | 0 |
| papar | 241 | 239 | 13 | 8 | 6 |
| vanilin_secer | 70 | 63 | 10 | 8 | 1 |
| rajcica_konzerva | 191 | 184 | 7 | 7 | 0 |
| mozzarella | 213 | 206 | 9 | 7 | 0 |
| kiselo_vrhnje | 127 | 120 | 7 | 7 | 0 |
| palenta | 83 | 76 | 7 | 7 | 0 |
| slanina | 705 | 698 | 12 | 7 | 0 |
| pileca_prsa | 228 | 224 | 11 | 6 | 2 |
| jaja | 343 | 338 | 29 | 6 | 1 |
| krastavac | 72 | 66 | 18 | 6 | 0 |
| parmezan | 113 | 107 | 6 | 6 | 0 |
| pasirana_rajcica | 139 | 134 | 7 | 5 | 0 |
| junetina | 288 | 283 | 6 | 5 | 0 |
| kecap | 175 | 170 | 13 | 5 | 0 |
| grasak | 152 | 147 | 6 | 5 | 0 |
| kukuruz | 157 | 152 | 8 | 5 | 0 |
| ocat | 121 | 116 | 14 | 5 | 0 |
| mljeveno_meso | 106 | 101 | 5 | 5 | 0 |
| kiseli_kupus | 131 | 128 | 9 | 4 | 1 |
| grah | 404 | 401 | 17 | 4 | 1 |
| brasno | 383 | 379 | 9 | 4 | 0 |
| koncentrat_rajcice | 40 | 36 | 4 | 4 | 0 |
| jabuka | 394 | 390 | 4 | 4 | 0 |
| prasak_za_pecivo | 48 | 44 | 4 | 4 | 0 |
| senf | 132 | 131 | 9 | 3 | 2 |
| zobene_pahuljice | 69 | 67 | 4 | 3 | 1 |
| mrkva | 122 | 119 | 3 | 3 | 0 |
| persin | 65 | 62 | 3 | 3 | 0 |
| svinjetina | 454 | 451 | 3 | 3 | 0 |
| sol | 160 | 161 | 2 | 2 | 3 |
| ulje | 166 | 164 | 5 | 2 | 0 |
| krumpir | 238 | 236 | 3 | 2 | 0 |
| slanutak | 126 | 124 | 3 | 2 | 0 |
| limun | 98 | 96 | 2 | 2 | 0 |
| luk | 207 | 205 | 7 | 2 | 0 |
| gljive | 113 | 113 | 3 | 1 | 1 |
| tuna | 448 | 448 | 51 | 1 | 1 |
| zelena_salata | 73 | 72 | 1 | 1 | 0 |
| naranca | 113 | 112 | 2 | 1 | 0 |
| rajcica | 201 | 200 | 8 | 1 | 0 |
| secer | 226 | 225 | 3 | 1 | 0 |

30 nasumičnih promijenjenih grupa (s više od jednog lanca):

| namirnica | grupa | promjena | lanaca | % naziva namirnice | % isključenog naziva | nazivi |
|---|---|---|---|---|---|---|
| papar | 9001414041130 | izvan → član | 21 | 67,00 | 5,00 | trgocentar: KOTANYI MJEŠAVINA PAPRA ŠARENA MLINAC 365; tommy: ZAČIN PAPAR ŠARENI ML. 35 g KOTANYI; metro: 35G KOTANYI MLINAC MJEŠAVI.PAP; ribola: PAPAR ŠAR.MLIN. 35 g KOTANYI; roto: PAPAR MJEŠAVINA 35G MLINAC KOTANY (8); branka: PAPAR MJEŠAVINA MLINAC KOTANYI 35g; spar: ZAČ.PAPAR ŠARENI KOTANYI 35 g; trgovina-krk: ZAČIN MLINAC MJEŠAVINA PAPRA 35 g KOTANY; ntl: MJEŠ.PAPRA 35 g MLINAC KOTANY; bure: MLINAC PAPAR ŠARENI ZRNO 35 g KOTANYI; vrutak: KOTANYI MLINAC 35G MJEŠAVINAPAPRA - 4/1-; plodine: PAPAR MIX 35 G MLINAC KOTANYI; lorenco: ZAČIN MJEŠ. PAPRA MLINAC 40 g; boso: ZAČIN KOTAN 35 g PAPAR ŠAR.MLI; djelo_vodice: MLINAC PAPAR ŠARENI 35G; kaufland: Kotanyi mlinac papar šareni 35 g; ktc: PAPAR ŠARENI ZRNO MLINAC 35g KOTANYI; studenac: ZAČIN MLINAC PAPAR ŠAR. U ZRNU 35 g KO; gavranovic: KOTANYI PAPAR MJ.MLINAC 35g; jadranka_trgovina: PAPAR ŠARENI 35g MLINAC KOTANYI; konzum: PAPAR MJEŠAVINA 35g MLINAC KOTANY |
| tvrdi_sir | 3850355007264 | član → ambiguous | 12 | 8,00 | 0,00 | tommy: SIR RIBANAC 1KG PRESIDENT; ktc: SIR RIBANAC 1kg PRESIDENT; metro: 1KG PRESIDENT RIBANAC; roto: SIR TVRDI RIBANI 1000g DUKAT (12); stridon: PRESIDENT RIBANAC SVJEŽE RIBAN DUKAT; bure: SIR RIBANAC 1 kg LOT:05012027; gavranovic: SIR PRESIDENT RIBANAC 1kg; studenac: SIR RIBANAC cca 1 kg; djelo_vodice: SIR RIBANAC RIBANI 1KG PRESIDENT; ntl: SIR RIBANAC PRESIDENT 1kg DUKAT; trgovina-krk: SIR PARMEZAN PRESIDENT RIBANI 1 kg LURA; dukat: PRESIDENT RIBANAC SVJEŽE RIBANI 1kg |
| majoneza | 3856015317308 | član → ambiguous | 2 | 50,00 | 0,00 | metro: 400G ZVIJEZDA DELIKATES MAJON; djelo_vodice: MAJONEZA 400G ZVIJEZDA |
| brasno | 8008696021189 | član → ambiguous | 2 | 50,00 | 0,00 | konzum: SMJESA ZA KRUH 1KG NUTRIFREE; plodine: BRASNO BEZ GLUTENA 1 KG NUTRIFREE |
| tjestenina | 5948935000236 | član → ambiguous | 2 | 50,00 | 0,00 | lorenco: KUKURUZNA TJESTENINA BG-COR.RIg 500; trgocentar: PASTA D'ORO CORNETTI RIGATI 500G (12) BEZ GLUTENA |
| jogurt | 3850354001560 | član → ambiguous | 16 | 13,00 | 0,00 | studenac: JOGURT ACIDOFIL DUKAT 180 g; dukat: DUKAT ACIDOFIL 3.2% 180g; gavranovic: ACIDOFIL 180g DUKAT; tommy: ACIDOFIL 180 g DUKAT; plodine: ACIDOFIL 180 G DUKAT; ribola: ACIDOFIL 180 g DUKAT; jadranka_trgovina: ACIDOFIL 180g DUKAT; trgocentar: ACIDOFIL 3,2% MM 180 GR (20)DUKAT; djelo_vodice: ACIDOFIL 3,2% 180G DUKAT; konzum: ACIDOFIL 3.2% 180g ČAŠA; trgovina-krk: MLIJEKO ACIDOFIL 180 g LURA; ntl: JOGURT ACIDOFIL 180 g DUKAT; roto: ACIDOFIL 3,2% 180g ČAŠA (20); boso: ACIDO DUKAT 180 g ACIDOFIL; ktc: ACIDOFIL 180g DUKAT; spar: ACIDOFIL DUKAT 180 g |
| kecap | 3856020275730 | član → ambiguous | 10 | 30,00 | 0,00 | tommy: KETCHUP LJUTI PAPRIKA 310 g PODR; plodine: KETCHUP LJUTI 310 G ZIK ZAK PODRAVKA; spar: KETC.ZIK ZAK PODR.LJUTI 310 g; ktc: ZIK ZAK LJUTI 310g PODRAVKA; studenac: KETCHUP ZIK ZAK LJUTI 310g; kaufland: Zik Zak Umak od paprike ljuti 310g vg.; roto: ZIK ZAK LJUTI 310G PODRAVKA (6); jadranka_trgovina: UMAK ZIK ZAK LJUTI 310G PODRAVKA; konzum: UMAK ZIK ZAK LJUTI 310 g PODRAVKA; lidl: ZIK ZAK paprika ljuti umak |
| tjestenina | 3858894930586 | član → ambiguous | 5 | 20,00 | 0,00 | konzum: ŠKOLJKICE 350 g KARLA; plodine: SKOLJKICE 350 G KARLA; ktc: ŠKOLJKICE KARLA 350g; kaufland: Karla Tjestenina školjkice 350 g; spar: TJESTEN. ŠKOLJKICE KARLA 350 g |
| margarin | 8719200266582 | član → ambiguous | 4 | 25,00 | 0,00 | zabac: BECEL margarina 225G; ktc: BECEL NAMAZ CLASSIC 225g; kaufland: Becel Namaz masni 225g vg.; spar: NAMAZ BECEL CLASSIC 225 g |
| krumpir | 3859893072031 | član → ambiguous | 2 | 50,00 | 0,00 | metro: 10KG LIČKI KRUMPIR CRVENI; lorenco: LIČKI KRUMPIR 5/1 |
| tjestenina | 8005121031126 | član → ambiguous | 3 | 33,00 | 0,00 | stridon: FETTUCCINE UOVO MS (112)250 GR (20) DIVELLA (IT); plodine: TJESTEINA FETTUCCINE S JAJIMA 250 G DIVELLA; branka: \*NE\*TJESTENINA DIVELLA FETTUCCINE 250g |
| tvrdi_sir | 3858891770222 | član → ambiguous | 7 | 14,00 | 0,00 | lorenco: SIR S PAPRIKOM 125g SIRANA GLIGORA; trgovina-krk: SIR S CHILIJEM 125 g GLIGO; vrutak: SIR S CHILLIJEM 125G -12/1GLIGORA; ktc: SIR KRAVLJI S CHILIJEM 125g GLIGORA; plodine: SIR SA CHILLIJEM 125 G SIRANA GLIGORA; jadranka_trgovina: SIR TVRDI S CHILIJEM 125G GLIGORA; spar: SIR S CHILLIJEM GLIGORA 125 g |
| maslinovo_ulje | 3859890446538 | član → ambiguous | 2 | 50,00 | 0,00 | ribola: ULJE EDM 500 ml ZLATNO ORGULA; jadranka_trgovina: MASLINOVO ULJE 0,5L EXTRA DJEVIČANSKO ZLATNO ORGULA |
| piletina | 3838977056945 | član → ambiguous | 11 | 9,00 | 0,00 | jadranka_trgovina: DIMLJENA PILEĆA KOBASICA 210G PICKIES PERUTNINA; konzum: PICKIES PILE DIM KOB CHILI&SIR 210 g; ktc: PIL.DIMLJ.KOBASICA CHILI&SIR 210g PIPO; ntl: KOBASICA PILEĆA DIMLJENA SIR I ČILI 210 g PICKIES PERUTNINA; spar: KOB.DIM.PIL. CHILI I SIR 210 g; tommy: KOBASICA PILEĆA CHILI&SIR 210 g PICKIES; boso: KOBAS PICKIES 210 g PIL.CH&SIR; vrutak: N-PICKIES PILEĆA KOBASICA 210G CHILLI SIR DIMLJENA -10/1-; plodine: PICKIES PILECA DIMLJENA KOBASICA CHILI SIR 210G; trgocentar: PICKIES PIL.DIM.KOB.CHILI&SIR 210G; trgovina-krk: PICKIES PIL. DIM. KOBASICA CHILLI&SIR 210G |
| tjestenina | 3856020278922 | član → ambiguous | 5 | 40,00 | 0,00 | konzum: TIJESTO CAPPELLETTI DURUM 500 g ZP; spar: TJE.ZLATO POLJ.CAPPELETT.500 g; plodine: TJESTENINA CAPPELLETTI DURUM 500 G ZLATO POLJE; kaufland: Zlato polje Tjestenina cappelletti 500 g; tommy: TJ. CAPPELLETTI DURUM 500 g ZLATO P |
| slanutak | 3856020261269 | član → ambiguous | 5 | 20,00 | 0,00 | konzum: MEDALJONI BROKULA O'PLANT 400g; tommy: VEGE MEDALJONI BROKULA/SLAN O'PLANT 400 g PODRAVKA; ktc: O"PLANT VEG NUGG BROKULA 400g PODRAVKA; plodine: VEGGIE NUGGETS BROKULA I SLANUTAK 400 G O'PLANT PODRAVKA; spar: BROKULA O´PLANT NUGGETS 400 g |
| vanilin_secer | 9001414711804 | član → ambiguous | 12 | 8,00 | 0,00 | trgovina-krk: LIMUN AROMATI.ŠEĆER VREĆ.50 g; gavranovic: KOTANYI VANILIN ŠEĆER AROMA LIMUNA 50g; studenac: ZAČIN ŠEĆER S PR. AROM. LIM. 50 g KOT; tommy: ŠEĆER AROMA LIMUN 50 g KOTANYI; lorenco: LIMUN AROMATIZIRANI ŠEĆER; ribola: ŠEĆER LIMUN 50 g PRIR. AROMA KOTANYI; spar: ŠEĆ.S PRIR.ARO.LIM.KOTANY 50 g; bure: LIMUN AROMA.50 g ŠEĆER KOTANYI; konzum: ŠEĆER S AROM LIMUN 50G KOTANYI; kaufland: Kotanyi Šećer s prir.aromom limuna 50g; plodine: SECER S AROMOM LIMUNA 50 G KOTANYI; branka: ŠEĆER S PRIRODNOM AROMOM LIMUN 50g |
| svjezi_sir | 3850355007561 | član → ambiguous | 4 | 50,00 | 0,00 | lidl: President Zag.svj. sir bez laktoze; stridon: PRESIDENT ZAGREBAČKI SIR BEZ LAKTOZE 220 g DUKAT; plodine: SIR SVJEZI ZAGREBACKI 220 G PRESIDENT; ribola: SIR SV.ZAG.B.LA.220gPRESIDENT |
| jogurt | 3831051018549 | član → ambiguous | 2 | 50,00 | 0,00 | ktc: MYTHOS GRČKI TIP 0%mm 150g; zabac: MYTOS GRČKI JOGURT 0%m.m. 150g |
| tjestenina | 3872882000532 | član → ambiguous | 3 | 33,00 | 0,00 | tommy: TJ.FAŽOLI 400 g FIOLI; plodine: TJESTENINA FIOLI FAZOLI 400 G RAGUSA; kaufland: Fioli fažoli 400 g |
| tjestenina | 3838700015669 | član → ambiguous | 7 | 43,00 | 0,00 | studenac: TJ. ZL. POLJE BR.45 REZANCI 400 g; trgocentar: ZP TJEST.ZLATICA 45 400G (15) PODRAVKA; konzum: TJEST. ZLATICA 45 400g ZP; spar: TJES.ZL.POLJE REZA.KUKUR.400 g; branka: TJESTENINA GRANDE ZLATICA 45 400g; tommy: TJ. ZLATICA ŠIROKA 400 g ZLATO P; lorenco: GRANDE ZLATICA BR.45 400 g |
| sol | 3858892060193 | član → ambiguous | 2 | 50,00 | 0,00 | lorenco: CVIJET SOLI-ZIP 500g; metro: 500G SOL. NIN BIO CVIJET SOLI |
| jogurt | 3870085030530 | član → ambiguous | 2 | 50,00 | 0,00 | ribola: JOG.2,8% 330g MEGGLE; kaufland: Meggle tekući jogurt 2,8% m.m. 330 g PET |
| pasirana_rajcica | 3856020220976 | član → ambiguous | 2 | 50,00 | 0,00 | ribola: BIO PAS.RAJČIC 500 g TETRA BRIK PODRAVK; stridon: BIO PASIRANA RAJČICA HR 500 g PODRAVKA |
| persin | 9001414024560 | član → ambiguous | 16 | 6,00 | 0,00 | ribola: PERšIN SJEC.KOT.100g; trgovina-krk: ZAČIN PERŠIN 1200 ml KOTANY; gavranovic: KOTANYI PERŠIN GASTRO 100g; trgocentar: PERŠIN 106G, KOTANYI; konzum: PERŠIN 100g GASTRO KOTANYI; lorenco: ZAČIN PERŠIN KOTANYI 1200ml; metro: 100G KOTANYI PERŠIN 1,2L; bure: PERŠIN GASTRO 125 g KOTANY UG.; djelo_vodice: PERŠIN GASTRO; vrutak: KOTANYI GASTRO 115G -6/1-PERŠIN; tommy: ZAČIN PERŠIN 100 g KOTANYI; jadranka_trgovina: MIRODIJE PERŠIN 100g 1200ML GASTRO DOZA KOTANYI; roto: PERŠIN 100G GASTRO KOTANYI (6); spar: ZAČ.PERŠIN KOTANYI GAST.100 g; branka: PERŠIN SJECKANI 1200ml GASTRO; ntl: MIROD.PERŠIN 100 g DOZA KOTANY |
| tjestenina | 3859888433724 | član → ambiguous | 4 | 25,00 | 0,00 | plodine: REZANCI SIROKI RAVNI JAJCANI XXL 600 G; boso: TJEST KOLEDA 600 g RAVNI REZ.XXL; ntl: TJ. ŠIROKI RAVNI REZ S JAJIMA 600 g KOLEDA; spar: REZAN.ŠIR.RAV.KOLEDA XXL 600 g |
| tjestenina | 8004350130464 | član → ambiguous | 7 | 43,00 | 0,00 | zabac: PASTA ZARA PENNINE 500 G; konzum: TIJESTO PENINE 46 500g ZARA; trgovina-krk: TJESTENINA PENNINE 46 -500 g ZARA; branka: TJESTENINA PASTA ZARA PENNINE 500g; ribola: TJ.PENNE 46 500 g P ASTA ZARA; roto: TIJESTO PENINE 46 500g ZARA (10); lorenco: PASTA ZARA 046 PENNINE 500g |
| med | 3850220428507 | član → ambiguous | 3 | 33,00 | 0,00 | konzum: MEĐ.PILE PILEĆI MIX MINI 500 g; spar: PILEĆI MINI MIX 500 g; plodine: MEDJIMURSKO PILE PILECI MIX MINI 500 G PERUTNINA |
| med | 3870545000080 | član → ambiguous | 4 | 50,00 | 0,00 | djelo_vodice: KRASTAVAC S MEDOM I PAPRIKOM 540g; stridon: KRASTA. S MEDOM I PAP. OC.MASA 290G 540G VITA. (6); kaufland: Vitaminka Krastavac med i paprika 540g; spar: KRAST.VITAMIN. MED PAPR.540 g |
| jabuka | 3859892553012 | član → ambiguous | 3 | 33,00 | 0,00 | trgovina-krk: METAR POTEZNI 3m; ntl: JABUKA CRVENA 5 kg; branka: METAR POTEZNI 3m |
