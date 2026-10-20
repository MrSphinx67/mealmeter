# Pregled Koraka 2D (arhiva 2026-10-19)

Izvještaj generira `scripts/step2d_review.py` nad izgrađenom bazom.

## 1. Pripadnost grupe (EAN) namirnici

Grupa pripada namirnici (`clean.staple_groups.status = 'member'`) ako naziv prolazi pravila u više od 50 % lanaca grupe i nijedan isključeni naziv nema udio ≥ 25 % lanaca; inače je `ambiguous` i nije u zadanom izboru (`find_products(include_ambiguous=True)` je vraća); `excluded` ako nijedan naziv ne prolazi. Prije: dovoljan je bio jedan naziv, a bilo koji isključeni naziv rušio je cijelu grupu. Atributi grupe (`clean.staple_group_attrs`): vrijednost iz naziva ima prednost pred zadanom, zatim broj lanaca. Neprehrambeni član (kategorija) ne računa se kao pogodak naziva.

**Cijena pravila:** grupe u kojima većina lanaca proizvod zove skraćeno ili samo markom ispadaju („PRAŠ. PEC. 12 g Dr.Oetker“, „FUŽI 250g AURELIA“, „PASTA ZARA 573 SPIRALI“, „SIR ORODUR“), jer `must_match` ne pogađa takve nazive. Najviše gubi tjestenina (nazivi oblika bez riječi tjestenina). Rješenje bi bili sinonimi oblika u `must_match` (fuži, spirali, penne…) ili niži prag za grupe bez isključenih naziva; nisam ih uvodio jer pravilo traži većinu.

Namirnice s promjenama (broj grupa):

| namirnica | članova prije | članova sada | dvosmislenih | ispalo | ušlo |
|---|---|---|---|---|---|
| tjestenina | 1429 | 1229 | 223 | 202 | 2 |
| tvrdi_sir | 986 | 864 | 125 | 123 | 1 |
| jogurt | 396 | 336 | 127 | 63 | 3 |
| med | 462 | 409 | 82 | 57 | 4 |
| cokolada_za_kuhanje | 57 | 35 | 22 | 22 | 0 |
| svjezi_sir | 154 | 134 | 31 | 20 | 0 |
| dodatak_jelima | 106 | 86 | 32 | 20 | 0 |
| mljevena_paprika | 103 | 84 | 20 | 19 | 0 |
| piletina | 609 | 593 | 23 | 18 | 2 |
| sunka | 919 | 902 | 20 | 17 | 0 |
| slatko_vrhnje | 38 | 25 | 13 | 13 | 0 |
| mlijeko | 246 | 234 | 27 | 12 | 0 |
| maslinovo_ulje | 342 | 331 | 15 | 11 | 0 |
| majoneza | 189 | 181 | 18 | 10 | 2 |
| vrhnje_za_kuhanje | 80 | 70 | 10 | 10 | 0 |
| maslac | 193 | 185 | 27 | 9 | 1 |
| margarin | 99 | 90 | 9 | 9 | 0 |
| griz | 38 | 29 | 9 | 9 | 0 |
| riza | 452 | 443 | 16 | 9 | 0 |
| papar | 241 | 239 | 13 | 8 | 6 |
| vanilin_secer | 70 | 63 | 10 | 8 | 1 |
| rajcica_konzerva | 191 | 184 | 7 | 7 | 0 |
| palenta | 83 | 76 | 7 | 7 | 0 |
| slanina | 705 | 698 | 12 | 7 | 0 |
| kiselo_vrhnje | 127 | 120 | 7 | 7 | 0 |
| pileca_prsa | 228 | 224 | 11 | 6 | 2 |
| jaja | 343 | 338 | 29 | 6 | 1 |
| parmezan | 111 | 105 | 6 | 6 | 0 |
| mozzarella | 211 | 205 | 10 | 6 | 0 |
| krastavac | 72 | 66 | 18 | 6 | 0 |
| grasak | 152 | 147 | 6 | 5 | 0 |
| kecap | 177 | 172 | 13 | 5 | 0 |
| mljeveno_meso | 106 | 101 | 5 | 5 | 0 |
| kukuruz | 157 | 152 | 8 | 5 | 0 |
| ocat | 121 | 116 | 14 | 5 | 0 |
| junetina | 288 | 283 | 6 | 5 | 0 |
| pasirana_rajcica | 139 | 134 | 7 | 5 | 0 |
| kiseli_kupus | 131 | 128 | 9 | 4 | 1 |
| grah | 401 | 398 | 17 | 4 | 1 |
| koncentrat_rajcice | 40 | 36 | 4 | 4 | 0 |
| brasno | 383 | 379 | 9 | 4 | 0 |
| prasak_za_pecivo | 48 | 44 | 4 | 4 | 0 |
| jabuka | 394 | 390 | 4 | 4 | 0 |
| senf | 136 | 135 | 6 | 3 | 2 |
| zobene_pahuljice | 69 | 67 | 4 | 3 | 1 |
| mrkva | 122 | 119 | 3 | 3 | 0 |
| svinjetina | 454 | 451 | 3 | 3 | 0 |
| persin | 64 | 61 | 3 | 3 | 0 |
| sol | 160 | 161 | 2 | 2 | 3 |
| luk | 207 | 205 | 7 | 2 | 0 |
| krumpir | 238 | 236 | 3 | 2 | 0 |
| limun | 98 | 96 | 2 | 2 | 0 |
| ulje | 166 | 164 | 5 | 2 | 0 |
| slanutak | 121 | 119 | 3 | 2 | 0 |
| gljive | 112 | 112 | 3 | 1 | 1 |
| tuna | 448 | 448 | 51 | 1 | 1 |
| secer | 226 | 225 | 3 | 1 | 0 |
| naranca | 112 | 111 | 2 | 1 | 0 |
| zelena_salata | 73 | 72 | 1 | 1 | 0 |
| rajcica | 201 | 200 | 8 | 1 | 0 |

30 nasumičnih promijenjenih grupa (s više od jednog lanca):

| namirnica | grupa | promjena | lanaca | % naziva namirnice | % isključenog naziva | nazivi |
|---|---|---|---|---|---|---|
| tvrdi_sir | 3858881196650 | član → ambiguous | 6 | 33,00 | 0,00 | vrutak: SIR S TARTUFIMA ŠPIN 230G -16/1; konzum: SIR TVRDI S TARTUFIMA 230g; metro: 230G ŠPIN SIR S TARTUFIMA; plodine: SIR S TARTUFIMA 230 G AGROLAGUNA; spar: SIR KRAVLJI ŠPIN TARTUF. 230 g; jadranka_trgovina: SIR TVRDI KRAVLJI S TARTUFIMA 230G ŠPIN |
| tjestenina | 3838700011463 | član → ambiguous | 7 | 14,00 | 0,00 | gavranovic: TJ.ZP REZANCI DOMAĆI JUŠNI 250g; studenac: REZANCI DOMAĆI ZA JUHU 250G; plodine: TJESTENINA REZANCI GNIJEZDA 250G VRECICA ZLATNO POLJE; ktc: REZANCI JUŠNI DOMAĆI JAJ.250g ZLATOPOLJE; tommy: TJ. JUŠNI DOMAĆI REZANCI 250 g ZP; konzum: TJE REZAN GNJEZ DOM JAJ 250g ZLATOPOLJE; spar: TJE.ZL.POLJE JUŠ.REZANCI 250 g |
| med | 3858889333774 | član → ambiguous | 4 | 25,00 | 0,00 | ribola: DATULJ MEDJOUL 500 gSVJEŽA; metro: 500G DATULJA MEDJOUL SVJEŽA; plodine: DATULJA MEDJOOL SVJEZA 500 G; konzum: DATULJA MEDJ SVJ 500g |
| tvrdi_sir | 3858891773872 | član → ambiguous | 5 | 20,00 | 0,00 | konzum: SIR TVRDI JADRANSKI 190 g GLIGORA; vrutak: SIR JADRANSKI GLIGORA 190G -8/1-; spar: SIR JADRANSKI GLIGORA 190 g; tommy: SIR JADRANSKI 190 g GLIGORA; ribola: SIR JADRAN.190 g GLIGORA |
| tjestenina | 3859888499874 | član → ambiguous | 15 | 20,00 | 0,00 | studenac: TJ. FUŽI 500 g; ribola: TJ.FUŽI ISTAR. 500 g KLARA MARIĆ; lorenco: DOMAĆI ISTARSKI FUŽI 500g; roto: TIJESTO FUŽI 500g KLARA M (10); bure: TJ.FUŽI 500 g ISTARSKI; spar: TJ.KL.MARIĆ FUŽI ISTARS.500 g; djelo_vodice: TJE.ISTARSKI FUŽI 500G KLARA; plodine: TJESTENINA DOMACI ISTARSKI FUZI 500 G KLARA MARIC; konzum: TIJESTO FUŽI 500g KLARA M; metro: 500G KLARA M. DOM IST FUŽ JAJA; stanic: DOMAĆI ISTARSKI FUŽI 500 g KLARA MARIĆ; jadranka_trgovina: TJESTENINA FUŽI ISTARSKI 500g KLARA MARIĆ; tommy: TJ.DOM.ISTAR. FUŽI 500 g KLAR; kaufland: Klara M domaći istarski fuži 500g; vrutak: TJEST KLARA M DOMAĆI ISTARSKI FUŽI 500G -10/1 108 |
| tjestenina | 3859889154567 | član → ambiguous | 2 | 50,00 | 0,00 | lorenco: DOMAĆI FIDELINI MRKVA 250g; plodine: TJESTENINA DOMACI FIDELINI MRKVA 250 G RAGUSA VRECICA |
| griz | 3858881327290 | član → ambiguous | 4 | 25,00 | 0,00 | djelo_vodice: PŠENIČNI GRIZ 1KG ULTRA; ribola: GRIS PŠ.KRUP 1 kg ULTRA; bure: PŠEN.KRUPICA 1 kg ULTRA; trgocentar: ULTRA KRUPICA PŠENIČNA 1KG, KLARA (20)(GRIS) |
| tjestenina | 3858881323063 | član → ambiguous | 8 | 25,00 | 0,00 | gavranovic: TJ.KLARA 500g REZANCI ŠIROKI; plodine: TJ.REZANCI SIROKI 500 G KLARA VRECICA; lorenco: REZANCI ŠIROKI KLARA; trgovina-krk: TIJ.REZANCI ŠIROKI 500G KLARA; trgocentar: REZANAC ŠIROKI TJESTENINA 0,500KG, KLARA(7); tommy: TJ.REZANCI ŠIROKI 500 g KLARA; vrutak: N-TJEST.KLARA ZP REZAN.ŠIROKI 500G -7/1- A60001; studenac: TJ.KLARA REZANCI 500 |
| slatko_vrhnje | 3850354017233 | član → ambiguous | 2 | 50,00 | 0,00 | ribola: VRH.ZA ŠLAG VAN.500gDUKAT; gavranovic: VRHNJE ZA ŠLAG VANILIJA 500g DUKAT |
| jogurt | 3850354017745 | član → ambiguous | 5 | 20,00 | 0,00 | ribola: JOG.500g BOT.RUŽA SENSIA FIBERS; stridon: SENSIA FIBERS BOTANICAL RUŽA 500g; gavranovic: JOGURT SENSIA BOTANICAL RUŽA 500g; lorenco: SENSIA FIBERS BOTANICA RUŽA; tommy: SENSIA FIBERS BOTANICAL RUŽA 500 g |
| tjestenina | 3858894930586 | član → ambiguous | 5 | 20,00 | 0,00 | konzum: ŠKOLJKICE 350 g KARLA; kaufland: Karla Tjestenina školjkice 350 g; spar: TJESTEN. ŠKOLJKICE KARLA 350 g; ktc: ŠKOLJKICE KARLA 350g; plodine: SKOLJKICE 350 G KARLA |
| pasirana_rajcica | 8003496005308 | član → ambiguous | 2 | 50,00 | 0,00 | tommy: RAJČICA PAS. IL DELIC. 500 g; trgovina-krk: RAJČICA PASIRANA PETTI 500 gr BRIK DELICATO |
| med | 3838977041477 | član → ambiguous | 10 | 10,00 | 0,00 | trgovina-krk: MEDALJONI PILEĆI PANIRANI SA SIROM 500g PERUTNINA; lorenco: PILEĆI MEDALJ.SA SIROM 500g PERUTNI; ribola: PIL.MED.SIR 500 g PE RUTNINA; vrutak: N-PER MEDALJONI PILEĆI 500G SA SIROM -14/1-; studenac: PIL. MEDALJ. SIR PAN. SMRZ. 500 g; boso: PILEĆI PIPO 500 g MEDALJ.SA SIR.; plodine: SMRZNUTI PILECI MEDALJONI SA SIROM 500 G PERUTNINA; kaufland: Perutnina Pileći medaljoni sir 500 g; tommy: PILEĆI MEDALJONI SA SIROM 500g; ntl: MEDALJONI PILEĆI PANIRANI SA SIROM SM 500 g PERUTNINA |
| majoneza | 7613287084491 | član → ambiguous | 4 | 50,00 | 0,00 | spar: MAJONEZA THOMY DELI.TUBA 280 g; metro: 280G THOMY MAJONEZA DELIGHT; plodine: DELIGHT TUBA 280 G THOMY; kaufland: Thomy mayonnaise delight Tube 280 g. |
| tjestenina | 3858881323216 | član → ambiguous | 7 | 43,00 | 0,00 | stridon: TJ.VIJCI 133 KLARA 500 g A60020; gavranovic: TJ.KLARA 500g VIJAK; vrutak: N-TJEST.KLARA ZP VIJAK BR. 13329040. 500G -24/1- A60020; trgocentar: VIJAK 133 TJESTENINA 0,500KG (24), KLARA; trgovina-krk: TIJ.VIJAK 500G KLARA; ntl: TJEST.VIJAK 133 500 g ZP KLARA; lorenco: VIJCI 500g KLARA |
| griz | 3858881086401 | član → ambiguous | 15 | 7,00 | 0,00 | stridon: INSTANT GRIS 200 g VREĆ. FRANCK (16); trgocentar: GRIS INST.V.200G(16), FRANCK; ktc: GRIS INSTANT 200g FRANCK; lorenco: INSTANT GRIS 200g FRANCK; spar: GRIS INSTANT FRANCK 200 g; branka: GRIS INSTANT 200 g; tommy: GRIZ INSTANT VR.200 g FRANCK; vrutak: GRIS FRANCK INST 200G -16/1-; roto: KRUPICA PŠEN GRIS 200G FRANCK (14); ribola: GRIS PŠ.KRUP. 200 g FRANCK; bure: GRIS 200 g FRANCK; studenac: GRIS INSTANT FRANCK 200 g; plodine: GRIS INSTANT 200 G FRANCK; trgovina-krk: GRIS INST V.200 FRANCK; konzum: KRUPICA PŠEN GRIS 200g FRANCK |
| junetina | 3859893373831 | član → ambiguous | 2 | 50,00 | 0,00 | eurospin: CHUCK EYE STEAK JUNEĆI VRAT 235g; konzum: CHUCK EYE STEAK 235 g SKIN |
| tjestenina | 3859893533402 | član → ambiguous | 9 | 22,00 | 0,00 | lorenco: AURELIA MAKARUNI 250g; ribola: MAKARUNI SVJ.250 g AURELIA; branka: MAKARUNI SVJEŽI 250g; djelo_vodice: TJESTENINA MAKARUNI 250G AURELIA; jadranka_trgovina: TJESTENINA MAKARUNI SVJEŽI 250G AURELIA; plodine: AURELIA MAKARUNI 250 G; konzum: MAKARUNI SVJEŽI 250g AURELIA; vrutak: N-MAKARUNI SVJEŽI AURELIA 250G -8/1-; tommy: MAKARUNI SVJEŽI 250 g AURELIA |
| vrhnje_za_kuhanje | 5411188132455 | član → ambiguous | 6 | 17,00 | 0,00 | tommy: VRHNJE OD ZOBI 250 ml ALPRO; ribola: VRH. ZA KUH. 250 ml ZOBENO APLRO; dm: alpro za kuhanje od zobi 0,25 l; konzum: KREMA ZA KUHANJE ZOB 250 ml ALPRO; spar: ZOB.PROIZ.ZA KUH.ALPRO 0,25 L; plodine: ZOB ZA KUHANJE 250 ML ALPRO |
| tvrdi_sir | 3859889426619 | član → ambiguous | 2 | 50,00 | 0,00 | plodine: SIR PRAMENKO 1/4 PASKA SIRANA; konzum: SIR TVRDI PRAMENKO VAC PAŠKA SIRANA |
| tvrdi_sir | 3850355001811 | član → ambiguous | 14 | 7,00 | 0,00 | trgocentar: PRESIDENT SIR ZA PIZZU 350G, DUKAT; plodine: SIR PIZZA PRESIDENT 350 G DUKAT; lorenco: SIR ZA PIZZU 350g SIRELA; ribola: SIR ZA PIZZU 350g PD; trgovina-krk: SIR ZA PIZZU PRESIDENT 350 g DUKAT; konzum: SIR POLUTV PRESIDENT ZA PIZZU 350g; kaufland: President Sir za pizzu 350 g; studenac: SIR ZA PIZZU DUKAT 350 g; spar: SIR ZA PIZZU PRESIDENT 350 g; dukat: PDT SIR ZA PIZZU A LA MARGARITA 350 g; tommy: SIR ZA PIZZU 350 g PRESIDENT; ktc: SIR ZA PIZZU 350g PRESIDENT DUKAT; vrutak: N-SIR PRESIDENT 350G ZA PIZZU RIBANI -8/1- 15033; ntl: SIR ZA PIZZU PRESIDENT 350 g DUKAT |
| tjestenina | 3859890293286 | član → ambiguous | 2 | 50,00 | 0,00 | trgovina-krk: TJEST. ŠURLICE KRČKE 500g SMR. MARIOLINA; tommy: KRČKE ŠURLICE 500 g MARIOLINA |
| palenta | 3859891976324 | član → ambiguous | 2 | 50,00 | 0,00 | dm: EKO JAZO EKO krupica kukuruzna 500g; plodine: KUKURUZNA KRUPICA EKO 500 G EKO-JAZO |
| jogurt | 3850354019084 | član → ambiguous | 19 | 16,00 | 0,00 | tommy: YOSHAKE LIMUN CHEESECAKE DUKAT 300 g; trgovina-krk: DUKAT YOSHAKE LEMON CHEESECAKE 300G; branka: NAPITAK YOSHAKE LIMUN CHEESECAKE 300g; djelo_vodice: YOSHAKE LIMUN CHEESECAKE 300G DUKAT; jadranka_trgovina: JOGURT DUKAT YOSHAKE 300G LEMON CHEESECAKE DUKAT; plodine: YOSHAKE LIMUN - CHEESECAKE 300 G DUKAT; boso: JOGUR DUKAT 300 g YOSH.LIM.CHEES; dukat: DUKAT YOSHAKE LIMUN CHEESECAKE 300g; gavranovic: YOSHAKE LEMON CHEESECAKE 300g DUKAT; stridon: YOSHAKE LIMUN CHEESCAKE 300 g DUKAT; ribola: YOSH.LI/CHE.300 g DU KAT; vrutak: N-\*DUKAT YOSHAKE 300G LIMUN CHEESECAKE -8/1-; studenac: YOSHAKE CHEESECAKEE 300 g DUKAT; trgocentar: DUKAT YOSHAKE CHEESECAKE 300G; kaufland: Dukat Jogurt limun Yoshake 300g; ntl: JOGURT YOSHAKE LIMUN CHEESECAKE 300 g DUKAT; spar: YOSHAKE LIMUN/CHEE.DUKAT 300 g; ktc: DUKAT YOSHAKE LEMON CHEESECAKE 300g; konzum: JOG YOSHAKE LEMON CHEES 300 g DUKAT |
| ulje | 3858885153116 | član → ambiguous | 2 | 50,00 | 50,00 | dm: Biofarm Natura line ulje cr.kima 60 kps; spar: KAPSULE ULJE CRNOG KIMA 60/1 |
| mljevena_paprika | 3859892109233 | član → ambiguous | 7 | 14,00 | 0,00 | branka: PAPRIKA TUCANA 35g BOČICA; spar: TUCANA PAPRIKA ŠAFRAM 35 g; studenac: PAPRIKA TUCANA 35g; trgocentar: PAPRIKA TUCANA 35G U ST.BOČICI ,ŠAFRAM; vrutak: PAPRIKA TUCANA ŠAFRAM 35GSTAKLO; trgovina-krk: PAPRIKA TUCANA 35 g ŠAFRA; jadranka_trgovina: PAPRIKA LJUTA TUCANA 35G ST ŠAFRAM |
| tjestenina | 3859888666030 | član → ambiguous | 18 | 22,00 | 0,00 | kaufland: Marodi male krpice s jajima 400 g; studenac: TJ. MARODI M. KRPICE JAJA 400 g; konzum: TIJESTO KRPICE MALE JAJ 400g MARODI; metro: 400G MARODI MALE KRPICE S JAJ; ntl: TJ.MALE KRPICE 400g MARODI; djelo_vodice: MALE KRPICE 400G MARODI; boso: TJEST MARODI 400 g MALE KRP.JAJ.; branka: TJESTENINA KRPICE MALE JAJA 400G; gavranovic: TJ.MARODI 400g KRPICE MALE S JAJIMA; ktc: KRPICE MALE DOM.S JAJIMA 400g MARODI; stridon: MALE KRPICE S JAJIMA 400 g MARODI; bure: TJ. MALE KRPICE 400 g; trgovina-krk: TJEST. KRPICE MALE S JAJIMA 400 g MAR; vrutak: TJEST MARODI KRPICE MALE400G-12/1; trgocentar: MARODI MALE KRPICE S JAJIMA 400G (12) (PAL 90); lorenco: MALE KRP.SA SVJ.JAJ.MARODI 400g; roto: TIJESTO KRPICE MALE JAJ 400g MARODI (12); tommy: TJ.MALE KRPICE 400 g MARODI |
| vanilin_secer | 3850104249488 | član → ambiguous | 6 | 33,00 | 0,00 | konzum: VANILIN ŠEĆER BOURBON 10g DOLCELA; ribola: BOURBON VANILIJA POD .; kaufland: Dolcela burbon vanilin šećer 10 g; lorenco: BURBON VANILIJA ŠEĆER 10g; plodine: DOLCELA VAN.SEC.BUR.10G; studenac: ŠEĆER BOURBON VANILI JA 10G |
| tjestenina | 8004350130242 | član → ambiguous | 4 | 50,00 | 0,00 | studenac: TJESTENINA PERLINE 500g PASTA ZARA; trgovina-krk: TJESTENINA PASTA ZARA 024 PERLINE 500G; konzum: TIJESTO PERLINE 24 500g PASTA ZARA; lorenco: TJ.24 PERLINE 500g |
| vanilin_secer | 9001414711811 | član → ambiguous | 10 | 10,00 | 0,00 | ribola: ŠEĆER NARANČA 50 g PRIR. AROMA KOTANY; tommy: ŠEĆER AROMA NARANČA 50 g KOTAN; konzum: ŠEĆER S AROMOM NARANČE 50G KOTANYI; bure: NARANDŽA AROMA.50 g ŠEĆER KOTANYI; plodine: SECER S AROMOM NARANCE 50 G KOTANYI; spar: ŠEĆ.S PRIR.ARO.NAR.KOTANY 50 g; kaufland: Kotanyi Šećer s prir.aromom naranče 50g; studenac: ZAČIN ŠEĆER S PR. AROM. NAR. 50 g KOT; lorenco: ORANGE AROMATIZIRANI ŠEĆER; gavranovic: KOTANYI VANILIN ŠEĆER AROMA NARANČA 50g |

## 4. Pileća prsa: stanje

Atribut `stanje`: smrznuto ako naziv sadrži SMRZ, LEDO, FROZ, ZAMRZ ili BRAZIL, inače svježe; zadano svježe. Granice po stanju (`plausible_by`): svježe 3–20 €/kg, smrznuto 2–12 €/kg. „Jeli“ ostaje isključeno. Prije (jedna granica 5–20 €/kg) je odbačeno 528 od 10.613 cijena po kg.

| stanje | proizvoda | min €/kg | max €/kg | izvan granica | cijena | medijan €/kg |
|---|---|---|---|---|---|---|
| smrznuto | 30 | 2,00 | 12,00 | 30 | 324 | 6,99 |
| svjeze | 259 | 3,00 | 20,00 | 14 | 10289 | 9,39 |
