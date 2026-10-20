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
| med | 456 | 403 | 82 | 57 | 4 |
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
| griz | 38 | 29 | 9 | 9 | 0 |
| riza | 452 | 443 | 16 | 9 | 0 |
| margarin | 99 | 90 | 9 | 9 | 0 |
| papar | 241 | 239 | 13 | 8 | 6 |
| vanilin_secer | 70 | 63 | 10 | 8 | 1 |
| rajcica_konzerva | 191 | 184 | 7 | 7 | 0 |
| kiselo_vrhnje | 127 | 120 | 7 | 7 | 0 |
| slanina | 705 | 698 | 12 | 7 | 0 |
| palenta | 83 | 76 | 7 | 7 | 0 |
| pileca_prsa | 228 | 224 | 11 | 6 | 2 |
| jaja | 347 | 342 | 29 | 6 | 1 |
| mozzarella | 211 | 205 | 10 | 6 | 0 |
| parmezan | 111 | 105 | 6 | 6 | 0 |
| krastavac | 72 | 66 | 18 | 6 | 0 |
| junetina | 288 | 283 | 6 | 5 | 0 |
| ocat | 121 | 116 | 14 | 5 | 0 |
| pasirana_rajcica | 139 | 134 | 7 | 5 | 0 |
| kukuruz | 157 | 152 | 8 | 5 | 0 |
| grasak | 152 | 147 | 6 | 5 | 0 |
| mljeveno_meso | 106 | 101 | 5 | 5 | 0 |
| kecap | 177 | 172 | 13 | 5 | 0 |
| grah | 401 | 398 | 17 | 4 | 1 |
| kiseli_kupus | 131 | 128 | 9 | 4 | 1 |
| brasno | 383 | 379 | 9 | 4 | 0 |
| koncentrat_rajcice | 40 | 36 | 4 | 4 | 0 |
| prasak_za_pecivo | 48 | 44 | 4 | 4 | 0 |
| jabuka | 394 | 390 | 4 | 4 | 0 |
| senf | 136 | 135 | 6 | 3 | 2 |
| zobene_pahuljice | 69 | 67 | 4 | 3 | 1 |
| svinjetina | 454 | 451 | 3 | 3 | 0 |
| sol | 160 | 161 | 2 | 2 | 3 |
| krumpir | 238 | 236 | 3 | 2 | 0 |
| slanutak | 121 | 119 | 3 | 2 | 0 |
| ulje | 166 | 164 | 5 | 2 | 0 |
| limun | 98 | 96 | 2 | 2 | 0 |
| mrkva | 121 | 119 | 2 | 2 | 0 |
| luk | 207 | 205 | 7 | 2 | 0 |
| tuna | 448 | 448 | 51 | 1 | 1 |
| gljive | 112 | 112 | 3 | 1 | 1 |
| naranca | 112 | 111 | 2 | 1 | 0 |
| rajcica | 201 | 200 | 8 | 1 | 0 |
| zelena_salata | 73 | 72 | 1 | 1 | 0 |
| persin | 62 | 61 | 1 | 1 | 0 |
| secer | 226 | 225 | 3 | 1 | 0 |

30 nasumičnih promijenjenih grupa (s više od jednog lanca):

| namirnica | grupa | promjena | lanaca | % naziva namirnice | % isključenog naziva | nazivi |
|---|---|---|---|---|---|---|
| jogurt | 3870311003185 | član → ambiguous | 8 | 13,00 | 0,00 | dukat: DOMAĆE BLAGO AYRAN 1.9% m.m. 225 g HR; jadranka_trgovina: MLIJEČNI NAPITAK AYRAN 225G DOMAĆE BLAGO DUKAT; tommy: JOGURT AYRAN 225 g DOMAĆE BLAGO; ntl: AYRAN 1,9% mm 225 g DOMAĆE BLAGO DUKAT; vrutak: DUKAT AYRAN 225G 1,9%MM DOMAĆE BLAGO -20/1- 32368; ktc: AYRAN 225g DUKAT; spar: AYRAN 1,9% DOMAĆE BLAGO 225 g; metro: 225G DOMAĆE BLAGO AYRAN 1,9%MM |
| tjestenina | 8008857300634 | član → ambiguous | 2 | 50,00 | 0,00 | jadranka_trgovina: TJESTENINA CAVATAPPI 63 500G REGGIA; bure: TJ.CAVATAPPI 63 500 g |
| tjestenina | 3858881682801 | član → ambiguous | 2 | 50,00 | 0,00 | ribola: TJ.ŠPAGETI 400 g BEZJAJA BR.10 TJ.CETIN; tommy: TJ.ŠPAG. 10 400 g BEZ JAJA CE |
| med | 5900658735505 | član → ambiguous | 6 | 33,00 | 0,00 | ktc: MEDENJACI 400g LAMBERTZ TAMNA ČOKOLADA; trgocentar: MED.LAMBERTZ POLONIA ZARTBITTE 400G (10); ntl: MEDENJACI MIX S TAMNOM ČOKOLADOM 400 g LAMBERTZ; ribola: MED.SRC.TAM.ČO.400 g ULTRA; djelo_vodice: LAMBERTZ SRCA TAMNA ČOK. 400G; gavranovic: MEDENJACI MIX 400g TAMNA ČOKOLADA LAMBERTZ |
| tvrdi_sir | 8721800082110 | član → ambiguous | 16 | 6,00 | 0,00 | spar: SIR LEERDAMMER ORIGINAL 250 g; plodine: SIR EMMENTALER ORIGINAL 250 G LEERDAMMER; tommy: SIR LEERDAMMER ORIGINAL 250 g DUKAT; boso: SIR LEERDAMMER 250 g ORIGINAL; studenac: SIR LEERDAMMER ORGINAL 250 g; gavranovic: SIR LEERDAMMER ORIGINAL 250g; jadranka_trgovina: SIR LEERDAMMER ORIGINAL 250G; ribola: SIR LEERDAM.250 g DU; ktc: SIR LEERDAMMER 250g DUKAT; lorenco: LEERDAMMER ORIGINAL 250G; vrutak: SIR LEERDAMMER ORIGINAL 250G -12/1-; trgovina-krk: SIR LEERDAMMER ORIGINAL 250 gr; branka: SIR LEERDAMMER ORIGINAL 250g; dukat: LEERDAMMER ORIGINAL 250g; konzum: SIR POLUTVRDI 250g LEERDAMMER; kaufland: Leerdammer Sir kravlji 45% Original 250g |
| pileca_prsa | 3850159113383 | član → ambiguous | 15 | 13,00 | 0,00 | konzum: ODRESCI PILEĆEG FILE OD PRSA 400g; trgovina-krk: PILEĆI ODRESCI OD FILEA PRSIJU 400 g VIND; vrutak: N-VIN.PIL.ODRESCI 400G OD FILEA PRSIJU; plodine: PILECI ODRESCI FILEA 400 G VINDIJA; tommy: PILEĆI ODR./FILE PRSIJU 400 g; spar: PILEĆI ODRESCI OD FILEA 400 g; studenac: ODRES. PIL.FILEA OD PRSA 400g; trgocentar: PILEĆI FILE OD PRSA 400G,VINDIJA; kaufland: Cekin odresci pilećeg filea od prsa 400g; lorenco: ODRESCI PILEĆEg FILEA OD PRSA 400g; metro: 400GR ODRESCI PILEĆEG FILEA; djelo_vodice: VIN.ODRESCI FILE PRSIJU 400G; ntl: PILEĆI ODRESCI OD FILE-A PRSIJU 400 g VINDIJA; ribola: PIL.ODRE.FIL.400 g VNDIJA; gavranovic: CEKIN PILEĆI ODRESCI OD FILEA PRSIJU 400g |
| tjestenina | 8005121000221 | član → ambiguous | 4 | 50,00 | 0,00 | djelo_vodice: ELICOIDALI 500g; stridon: ELICODIALI 22 500G (24) DIVELLA (IT); branka: TJESTENINA ELICODIALI 500g; vrutak: TJEST DIVELLA 500G ELICOIDALI 22 -24/1- |
| svinjetina | 3859893378447 | član → ambiguous | 2 | 50,00 | 0,00 | metro: CCA12KG SVINJ.BUT SK OBRAĐEN; studenac: SVINJSKI BUT SK U KOŽI DALM.OBR MM |
| jogurt | 3850257061067 | član → ambiguous | 3 | 33,00 | 0,00 | spar: JOG.TEKUĆI 2,8% KRALJ.KRAV 1kg; ktc: JOGURT TEKUĆI 2,8% M.M. 1kg; kaufland: Kravica Kraljica Tek.jog.2,8%m.m.1kg PET |
| jaja | 8699462605148 | član → ambiguous | 2 | 50,00 | 0,00 | branka: JAJE PRINCESS SUPRISE 15g; stridon: PRINCESS MILKY CREAM 15 g (24) |
| papar | 3859891493609 | član → ambiguous | 8 | 25,00 | 0,00 | ribola: KIS.KUP.CR PAP 250 g; lorenco: PREM.SAL.MADIG PAPAR+CRV.PAPR.250g; spar: KUPUS KIS ČEŠNJ,PAP.CR.P 250 g; konzum: KUPUS KIS PAPRIKA ČEŠNJAK PAPAR 250g; plodine: PREMIUM SALATA KIS.KUPUS S CES.,PAP.I CRVENOM PAPRIKOM 250GR; studenac: SALATA KIS. ZELJE ČEŠ/PAP/C.PA 250 g; tommy: SAL.KIS.KUPUS 250g CRV.PAPR.; kaufland: Sal.kis.kup.češ.pap.i crv.pap.250g/220g |
| jogurt | 3850108037654 | član → ambiguous | 8 | 38,00 | 0,00 | stridon: Z BREGOV EUFORIJA CRISPY MIX 150 g (kokos-nugat); lorenco: EUFORIJA KREM JOG.KOKOS I NOUG.150g; trgovina-krk: FRESKA EUFORIJA CRISPY MIX 150g; ribola: JOG.CRIS.MIX 150 g V INDIJA; branka: JOGURT EUFORIJA CRISPY MIX 150g; plodine: Z.BREGOV EUFORIJA CRISPY MIX 150 G VINDIJA; studenac: JOGURT EUFORIJA CRIS Z BREGOV 150g; tommy: JOGURT EUFORIJA 150 g CRISPY MIX Z BREGOV |
| vrhnje_za_kuhanje | 4034900027801 | član → ambiguous | 2 | 50,00 | 0,00 | roto: VRHNJE ZA KUH CREME CUISINE 15% BM 1L (12); metro: 1L MEGGLE CREME CUISINE |
| tjestenina | 3859888499102 | član → ambiguous | 7 | 29,00 | 0,00 | lorenco: LJILJANI 500g KLARA MARIĆ; ribola: TJ.LJILJANI 500 g KLARA MARIĆ; studenac: TJESTENINA LJILJANI 500g KLARA MARIĆ; tommy: TJ.LJILJANI 500 g KLARA M; kaufland: Klara M ljiljani 500g; konzum: TIJESTO LJILJANI 500g KLARA M; vrutak: TJEST KLARA M LJILJANI 500G -10/1 111 |
| tjestenina | 3838700010480 | član → ambiguous | 4 | 25,00 | 0,00 | tommy: TJ.REZANCI VALJANI 400 G ZLATO; bure: TJ.REZANCI 400g VALJANI; spar: TJE.ZL.POLJE VALJANI REZ.400 g; konzum: TJEST. FETTUCCINE 8 JAJ 400g ZLATOPOLJE |
| grasak | 3838977044508 | član → ambiguous | 4 | 25,00 | 0,00 | ribola: POLI GREEN 220 g PER UTNINA; tommy: POLI GREEN MINI 220 g; studenac: POLI GREEN MINI 220 g; kaufland: Poli Salama od graška Green 220g |
| krastavac | 3858891564364 | član → ambiguous | 4 | 25,00 | 0,00 | vrutak: KRASTAVCI I.KL (3-6CM) 1500ML1400G (NETO 800G) ULTRA+ -6/1; trgocentar: ULTRA KRASTAVCI (3-6) 1400G-800G (6); ribola: ULT.PL.1400g KRASTAVCI; djelo_vodice: KRASTAVCI ULTRA 1500ML |
| dodatak_jelima | 40804873 | član → ambiguous | 3 | 33,00 | 0,00 | bure: JOGURT SALAT.250 ml KUHNE; lorenco: SALATFIX JOGURT 250ML; studenac: DODATAK JELIMA DRES. JOGURT 250 ml |
| svinjetina | 3850139523423 | član → ambiguous | 2 | 50,00 | 0,00 | studenac: SVJEŽA SVINJSKA REBRA PIK VRBOVEC; konzum: SV REBRA |
| grah | 8000627300431 | član → ambiguous | 3 | 67,00 | 33,00 | ntl: GRAH ZRNAŠ NISKI 250G; plodine: GRAH ZRNAS NISKI; trgovina-krk: SJEME GRAH ZRNAŠ 250 g MARCON |
| med | 5900658800807 | član → ambiguous | 3 | 33,00 | 0,00 | konzum: KEKS SPRING PVC 350 g LAMBERTZ; djelo_vodice: LAMBERTZ SPRING COOKIES 350G; trgocentar: MED.LAMBERTZ SPRING COOKIES 350G(6) |
| grasak | 8000627400339 | član → ambiguous | 2 | 50,00 | 50,00 | ntl: GRAŠAK ČUDO KELVEDONA 250 G; plodine: SJEME GRASAK CUDO KLEVEDONA |
| tjestenina | 8076802085868 | član → ambiguous | 6 | 33,00 | 0,00 | lorenco: TJEST.PIPETTE RIGATE 500 g BARI; ribola: TJ.BARILLA PIP 500 g PIPETTE RIGATE; spar: TJES.BARILLA PIPETTE RIGT.500g; tommy: TJ. BARILLA PIPETTE RIGATE BR.86 500 g; plodine: TJESTENINA PIPETE RIGATE 86 500 G BARILA KUTIJA; kaufland: Barilla Tjes.Pipette Rigate 500g |
| med | 3850220408806 | član → ambiguous | 3 | 33,00 | 0,00 | konzum: MARINIRANI PILEĆI MINI FILE 400g; spar: PILEĆI MARINIRANI FILE 400 g; trgovina-krk: MARINIRANI PILEĆI MINI FILE MEĐ.PILE 400G |
| tuna | 8004030860025 | izvan → član | 7 | 57,00 | 14,00 | kaufland: Rio Mare Insal.sal.tuna cous cous2x160g; konzum: TUNJ SALATA COUS COUS 2X160g RIO MARE; lorenco: TUNA -COUS-COUS SAL.2\*160g BOWL.; plodine: TUNA COUS-COUS SAL.2X160G BOWL; metro: 160GX2 RIO MARE INSALA.CUS CUS; spar: TUNA SAL.RIO MARE COUS 2X160 g; tommy: TUNA SALATA CUS CUS 2X160 G RIO MARE |
| tjestenina | 8008857300603 | član → ambiguous | 4 | 50,00 | 0,00 | vrutak: TJEST REGGIA 500G GOMITI RIGATI U-21127 -24/1-; trgocentar: GOMITI RIGATI 500G; jadranka_trgovina: TJESTENINA GOMITI RIGATI 60 500G REGGIA; bure: TJ.GOMITI 60 500 g RIGATI REGGIA |
| tjestenina | 3838700015669 | član → ambiguous | 7 | 43,00 | 0,00 | branka: TJESTENINA GRANDE ZLATICA 45 400g; lorenco: GRANDE ZLATICA BR.45 400 g; tommy: TJ. ZLATICA ŠIROKA 400 g ZLATO P; studenac: TJ. ZL. POLJE BR.45 REZANCI 400 g; trgocentar: ZP TJEST.ZLATICA 45 400G (15) PODRAVKA; spar: TJES.ZL.POLJE REZA.KUKUR.400 g; konzum: TJEST. ZLATICA 45 400g ZP |
| riza | 8710447482179 | član → ambiguous | 2 | 50,00 | 0,00 | lorenco: DOVE SAPUN TEK LOT.FLOiR.MILK 500ML; plodine: DOVE TEK.SAP. REFIL 500 ML LOT.FLOWER RICE MILK |
| med | 3850220428507 | član → ambiguous | 3 | 33,00 | 0,00 | konzum: MEĐ.PILE PILEĆI MIX MINI 500 g; plodine: MEDJIMURSKO PILE PILECI MIX MINI 500 G PERUTNINA; spar: PILEĆI MINI MIX 500 g |
| slatko_vrhnje | 3850104230585 | član → ambiguous | 5 | 20,00 | 0,00 | ribola: ŠLAG TEK.BILJNI 1l P ODRAVKA; stridon: DOLCELA ŠLAG 5 TEK. BILJ. ŠLAG 1 L PODRAVKA (12); ktc: ŠLAG PRIPRAVAK 1L DOLCELA; lorenco: ŠLAg 1 L PODRAVKA; djelo_vodice: VRHNJE ZA ŠLAG 1L PODRAVKA |

## 4. Pileća prsa: stanje

Atribut `stanje`: smrznuto ako naziv sadrži SMRZ, LEDO, FROZ, ZAMRZ ili BRAZIL, inače svježe; zadano svježe. Granice po stanju (`plausible_by`): svježe 3–20 €/kg, smrznuto 2–12 €/kg. „Jeli“ ostaje isključeno. Prije (jedna granica 5–20 €/kg) je odbačeno 528 od 10.613 cijena po kg.

| stanje | proizvoda | min €/kg | max €/kg | izvan granica | cijena | medijan €/kg |
|---|---|---|---|---|---|---|
| smrznuto | 30 | 2,00 | 12,00 | 30 | 324 | 6,99 |
| svjeze | 259 | 3,00 | 20,00 | 14 | 10289 | 9,39 |

## 10. Filtar hrane: neprehrana u kategoriji hrane

- Strogi popis (igrač, svijeć, baterij, sjeme, cvijet, salvet, ukrasn) vrijedi za sve proizvode s `is_food = true`; pogođeni idu u `ostalo` ili `kucanstvo` (`category_source = 'words'`).
- Širi popis (posuđe, krpe, kozmetika, higijena, cvijeće…) vrijedi za ručne iznimke u `category_map.yaml` (`_chain_verify`): Gavranović „Hrana“, Boso „ZELENI PROGRAM“, Studenac „HRANA“ i Plodine naslijeđene preko EAN-a.
- Jestivo usprkos riječi ostaje hrana (šećerni ukrasi, čokolada, Dr. Oetker, bomboni s igračkom).
- „ČAŠA“ je neprehrana samo kao „ČAŠE“, „+ ČAŠ…“ ili „ČAŠA ZA“ (moja dopuna), pa „SLADOLED ČAŠA“ ostaje hrana; „KALUP“ samo kao „KALUP ZA“.

Promjene skupine (prije → poslije):

| promjena | proizvoda |
|---|---|
| hrana → kucanstvo | 421 |
| kucanstvo → unknown | 334 |
| hrana → ostalo | 289 |
| unknown → kucanstvo | 65 |
| hrana → higijena | 59 |
| hrana → kozmetika | 48 |
| alkohol → kucanstvo | 38 |
| kucanstvo → alkohol | 23 |
| pice → ostalo | 18 |
| unknown → kozmetika | 8 |
| unknown → higijena | 7 |
| hrana → unknown | 6 |
| pice → kucanstvo | 5 |
| hrana → kucni_ljubimci | 3 |
| djeca → higijena | 1 |
| pice → unknown | 1 |
| unknown → ostalo | 1 |

20 nasumičnih proizvoda koji su bili hrana ili piće, a sada nisu:

| lanac | naziv | kategorija | prije | poslije | izvor |
|---|---|---|---|---|---|
| konzum | ČAJ CVIJET BAZGE EKO 40g DARVITALIS | HRANA | hrana | ostalo | words |
| branka | ČAJ NEVEN CVIJET S/C 30g | HRANA | hrana | ostalo | words |
| gavranovic | CVIJET 59cm 2-KTD7795 rasprodaja | Hrana | hrana | ostalo | words |
| gavranovic | BOŽ.STOLNJAK SHINE 140X180cm -rasprodaja | Hrana | hrana | kucanstvo | words |
| gavranovic | ČETKICA KOZMETIČKA 10632 | Hrana | hrana | higijena | words |
| boso | BUČINO SJEME 150 g II KL | VOĆE | hrana | ostalo | words |
| lidl | Plišana igračka sa slatkišima | Hrana | hrana | ostalo | words |
| gavranovic | TACNA I PODMETAČ PAPIRNATI OFFER-rasprodaja | Hrana | hrana | kucanstvo | words |
| branka | ČAJ KAMILICA CVIJET 40g | HRANA | hrana | ostalo | words |
| plodine | BORMIOLI CASE ZA VODU 6/1 260 ML FLORA PLAVE |  | hrana | kucanstvo | ean_inherited |
| gavranovic | KOŠARICE PAPIRNATE 150kom 3,5cm-rasprodaja | Hrana | hrana | kucanstvo | words |
| gavranovic | CVIJET 45cm A2070047 2023. rasprodaja | Hrana | hrana | ostalo | words |
| ntl | CVIJETAČA SM 2,5KG ZMH | Hrana | hrana | ostalo | words |
| boso | SJEME GARDEN CINIJA NANA TH.MIX | ZELENI PROGRAM | hrana | ostalo | words |
| boso | SJEME GARDEN MRKVA FLAKKEE | ZELENI PROGRAM | hrana | ostalo | words |
| gavranovic | ŽARULJA AVIDE E-27 40W | Hrana | hrana | kucanstvo | words |
| gavranovic | STOLNJAK 130x220cm PVC | Hrana | hrana | kucanstvo | words |
| trgocentar | BROKULA CVIJET 2,5KG,ZMH | Hrana | hrana | ostalo | words |
| boso | SJEME GARDEN KRAST.SUNČ.POTOK | ZELENI PROGRAM | hrana | ostalo | words |
| tommy | ČAJ KAMILICA CVIJET 80 g AGRIS | PAKIRANA HRANA I PIĆE | pice | ostalo | words |

20 nasumičnih „hrana“ proizvoda koji i dalje izgledaju neprehrambeno (od 590; u Koraku 2C ih je bilo 2.168, ali s drugim popisom za izvještaj):

| lanac | naziv | kategorija | skupina | izvor |
|---|---|---|---|---|
| metro | 0,7L J.DANIEL'S WH+2 ČAŠE KUT. | piće | pice | chain |
| spar | BOMBONI S IGRAČ. PIŠTOLJ 20 g | Hrana | hrana | chain |
| djelo_vodice | LIKER JAGERMEISTER 0,7L + 2 ČAŠE | BILJNI LIKERI | alkohol | chain |
| lorenco | PETRA CVIJET.S VOĆ.NAMAZOM OD MAREL |  | hrana | ean_inherited |
| spar | LIKER PELINOVA 0,7 L + 2 ČAŠE | Pića | alkohol | chain |
| ntl | PJENUŠAC DJEČJI SPUŽVA BOB 0,75 L | Piće | alkohol | chain |
| trgovina-krk | KRUH SJEME 400 g SVJ. PEČ. BEZ GLUTENA RATV | Hrana | hrana | chain |
| vrutak | N-GAV KULENOV CVIJET NAREZAK 80G | MESO | hrana | chain |
| tommy | PAKET MILKA MIX 96 g + IGRAČKA | PAKIRANA HRANA I PIĆE | pice | chain |
| konzum | UKRASNI CVJETIĆI 3g DR.OETKER | HRANA | hrana | chain |
| roto | RUM BARCELO IMPERIAL ONYX 0,70 + 2 ČAŠE gift box (6)\* | ŽESTOKO | alkohol | chain |
| zabac | BOSANSKI LONAC 400G, BAKINA KUHINJA | Smrznuta hrana | hrana | chain |
| tommy | KOBASICA KULEN CVIJET NAR.80 g | HLAĐENO I SMRZNUTO | hrana | chain |
| ktc | JOHNNIE WALKER RED 0,7+ 2 ČAŠE\*\* | PIĆA | alkohol | chain |
| studenac | WHISKEY JAMESON 2 ČAŠE 0,7 l | PIĆE | alkohol | chain |
| lorenco | MED CVIJETNI SA SOKOM OD LIMUNA |  | hrana | ean_inherited |
| kaufland | Badel prima brand 35% 0,7 l + 2 čaše | PIĆE | alkohol | chain |
| spar | CVIJET SOLI ADRIATIQ BIO 125 g | Hrana | hrana | chain |
| ntl | LIKER PELINKOVAC ANTIQUE 0,7L + ČAŠE BADEL 1862 | Piće | alkohol | chain |
| ktc | JAJA S BOMBONIMA 10g SPUŽVA BOB | HRANA | hrana | chain |

## 11. Pokrivenost (zadani izbor, cijela Hrvatska)

74 aktivnih namirnica. Stupci lanaca: broj proizvoda u zadanom izboru (bez rasprodaje i `price_suspect`, sa zadanim atributima). Veleprodaja (Metro) nije uključena.

**Procjena, nije primijenjeno:** strogo pozitivni `food_unverified` (proizvod nepoznate skupine ulazi ako naziv počinje riječju namirnice, cijena je u granicama i gramatura je poznata). Stupac „+Plodine“ je dobitak proizvoda za Plodine, „lanaca (strogo)“ broj lanaca s tim pravilom, a zadnji stupac novi lanci.

| namirnica | lanaca | plodine | konzum | spar | lidl | kaufland | tommy | studenac | eurospin | +Plodine | lanaca (strogo) | novi lanci |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| brasno | 26 | 32 | 38 | 41 | 6 | 34 | 23 | 23 | 6 | 23 | 26 |  |
| secer | 26 | 5 | 4 | 5 | 3 | 5 | 5 | 7 | 4 | 3 | 26 |  |
| sol | 26 | 22 | 20 | 21 | 5 | 21 | 13 | 15 | 3 | 7 | 26 |  |
| ulje | 26 | 7 | 10 | 14 | 9 | 13 | 8 | 5 | 3 | 5 | 26 |  |
| maslinovo_ulje | 26 | 47 | 59 | 54 | 19 | 35 | 48 | 29 | 8 | 39 | 26 |  |
| maslac | 27 | 21 | 22 | 27 | 13 | 22 | 18 | 17 | 6 | 23 | 27 |  |
| margarin | 25 | 26 | 16 | 19 | 12 | 19 | 29 | 17 | 3 | 6 | 25 |  |
| mlijeko | 27 | 23 | 17 | 24 | 13 | 19 | 18 | 21 | 3 | 2 | 27 |  |
| jogurt | 27 | 58 | 62 | 54 | 49 | 76 | 60 | 41 | 22 | 26 | 27 |  |
| kiselo_vrhnje | 26 | 20 | 29 | 26 | 20 | 30 | 21 | 19 | 6 | 12 | 26 |  |
| vrhnje_za_kuhanje | 27 | 18 | 17 | 18 | 9 | 16 | 17 | 16 | 3 | 2 | 27 |  |
| slatko_vrhnje | 24 | 6 | 3 | 5 | 4 | 6 | 6 | 5 | 2 | 1 | 24 |  |
| svjezi_sir | 26 | 17 | 26 | 28 | 19 | 25 | 19 | 13 | 6 | 14 | 26 |  |
| tvrdi_sir | 26 | 51 | 152 | 82 | 48 | 73 | 76 | 78 | 34 | 11 | 26 |  |
| mozzarella | 26 | 11 | 15 | 19 | 22 | 18 | 27 | 9 | 11 | 18 | 26 |  |
| parmezan | 25 | 6 | 5 | 7 | 14 | 8 | 9 | 3 | 8 | 5 | 25 |  |
| jaja | 25 | 14 | 27 | 24 | 32 | 30 | 43 | 41 | 6 | 17 | 25 |  |
| luk | 21 | 1 | 3 | 4 | 7 | 7 | 4 | 5 | 2 | 3 | 21 |  |
| cesnjak | 21 | 0 | 1 | 2 | 3 | 2 | 2 | 3 | 1 | 3 | 22 | plodine |
| krumpir | 24 | 7 | 10 | 10 | 8 | 12 | 19 | 13 | 59 | 13 | 24 |  |
| rajcica | 20 | 0 | 2 | 7 | 4 | 5 | 9 | 8 | 4 | 6 | 21 | plodine |
| pasirana_rajcica | 26 | 30 | 27 | 20 | 8 | 21 | 25 | 18 | 5 | 13 | 26 |  |
| rajcica_konzerva | 25 | 18 | 24 | 25 | 4 | 16 | 20 | 13 | 5 | 8 | 25 |  |
| koncentrat_rajcice | 25 | 8 | 7 | 8 | 1 | 6 | 12 | 10 | 0 | 1 | 25 |  |
| mrkva | 23 | 0 | 5 | 3 | 4 | 6 | 8 | 5 | 62 | 3 | 24 | plodine |
| paprika | 22 | 1 | 7 | 11 | 9 | 8 | 11 | 8 | 5 | 14 | 22 |  |
| krastavac | 23 | 0 | 2 | 7 | 4 | 3 | 3 | 2 | 3 | 4 | 24 | plodine |
| tikvica | 19 | 0 | 2 | 2 | 3 | 2 | 4 | 2 | 4 | 1 | 20 | plodine |
| kupus | 19 | 0 | 4 | 6 | 4 | 4 | 4 | 5 | 3 | 3 | 20 | plodine |
| kiseli_kupus | 25 | 10 | 10 | 11 | 4 | 6 | 18 | 10 | 5 | 6 | 25 |  |
| zelena_salata | 18 | 0 | 1 | 1 | 2 | 6 | 6 | 4 | 6 | 0 | 18 |  |
| rukola | 10 | 0 | 0 | 1 | 1 | 0 | 0 | 1 | 2 | 0 | 11 | lorenco |
| matovilac | 9 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 10 | lorenco |
| radic | 17 | 0 | 2 | 2 | 1 | 1 | 1 | 4 | 7 | 1 | 18 | plodine |
| endivija | 12 | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 12 |  |
| spinat | 25 | 4 | 3 | 4 | 4 | 5 | 10 | 7 | 80 | 2 | 25 |  |
| persin | 15 | 0 | 0 | 1 | 1 | 0 | 1 | 1 | 1 | 2 | 16 | plodine |
| gljive | 24 | 2 | 4 | 6 | 3 | 3 | 11 | 12 | 78 | 5 | 24 |  |
| riza | 26 | 48 | 63 | 66 | 20 | 45 | 70 | 28 | 19 | 36 | 26 |  |
| tjestenina | 26 | 109 | 139 | 136 | 63 | 160 | 108 | 72 | 50 | 118 | 26 |  |
| griz | 23 | 7 | 1 | 3 | 2 | 2 | 3 | 3 | 1 | 3 | 23 |  |
| palenta | 26 | 9 | 12 | 13 | 3 | 7 | 18 | 11 | 4 | 5 | 26 |  |
| zobene_pahuljice | 25 | 16 | 13 | 10 | 4 | 9 | 11 | 11 | 2 | 5 | 25 |  |
| krusne_mrvice | 25 | 9 | 15 | 14 | 3 | 7 | 9 | 7 | 2 | 8 | 25 |  |
| kvasac | 27 | 11 | 13 | 10 | 5 | 12 | 10 | 8 | 3 | 0 | 27 |  |
| prasak_za_pecivo | 24 | 5 | 7 | 5 | 1 | 7 | 5 | 6 | 0 | 1 | 24 |  |
| vanilin_secer | 23 | 12 | 8 | 12 | 4 | 14 | 9 | 7 | 0 | 2 | 23 |  |
| kakao | 25 | 5 | 4 | 8 | 2 | 4 | 6 | 4 | 1 | 11 | 25 |  |
| cokolada_za_kuhanje | 24 | 5 | 9 | 6 | 5 | 5 | 8 | 3 | 2 | 2 | 24 |  |
| pileca_prsa | 23 | 5 | 15 | 13 | 5 | 9 | 15 | 18 | 32 | 5 | 23 |  |
| piletina | 24 | 16 | 39 | 25 | 16 | 32 | 31 | 63 | 80 | 10 | 24 |  |
| mljeveno_meso | 20 | 7 | 7 | 9 | 7 | 6 | 5 | 11 | 15 | 0 | 20 |  |
| svinjetina | 23 | 2 | 24 | 36 | 7 | 16 | 35 | 61 | 55 | 23 | 23 |  |
| junetina | 19 | 5 | 13 | 23 | 1 | 14 | 32 | 56 | 38 | 5 | 20 | stridon |
| slanina | 25 | 40 | 55 | 53 | 23 | 34 | 36 | 66 | 26 | 19 | 25 |  |
| sunka | 25 | 66 | 74 | 103 | 81 | 76 | 89 | 79 | 34 | 13 | 25 |  |
| tuna | 25 | 62 | 96 | 87 | 29 | 40 | 67 | 44 | 17 | 41 | 25 |  |
| grah | 26 | 29 | 49 | 38 | 14 | 31 | 31 | 24 | 11 | 40 | 26 |  |
| leca | 26 | 13 | 16 | 16 | 4 | 14 | 13 | 11 | 3 | 9 | 26 |  |
| slanutak | 26 | 12 | 17 | 15 | 4 | 11 | 15 | 12 | 3 | 10 | 26 |  |
| kukuruz | 26 | 12 | 14 | 23 | 9 | 14 | 19 | 12 | 3 | 10 | 26 |  |
| grasak | 27 | 15 | 16 | 20 | 7 | 16 | 25 | 18 | 6 | 16 | 27 |  |
| banana | 20 | 0 | 2 | 3 | 2 | 2 | 3 | 5 | 2 | 1 | 21 | plodine |
| jabuka | 21 | 1 | 13 | 21 | 14 | 22 | 23 | 20 | 73 | 23 | 21 |  |
| limun | 22 | 0 | 3 | 3 | 6 | 4 | 6 | 3 | 69 | 8 | 23 | plodine |
| naranca | 21 | 0 | 1 | 6 | 3 | 3 | 7 | 6 | 62 | 14 | 22 | plodine |
| papar | 26 | 43 | 48 | 58 | 5 | 45 | 56 | 38 | 7 | 20 | 26 |  |
| mljevena_paprika | 26 | 17 | 17 | 18 | 3 | 18 | 18 | 14 | 4 | 4 | 26 |  |
| dodatak_jelima | 26 | 21 | 29 | 25 | 7 | 16 | 25 | 18 | 3 | 8 | 26 |  |
| ocat | 26 | 18 | 15 | 16 | 4 | 13 | 16 | 11 | 2 | 7 | 26 |  |
| med | 26 | 53 | 67 | 42 | 9 | 30 | 44 | 29 | 5 | 31 | 26 |  |
| senf | 26 | 34 | 33 | 32 | 8 | 43 | 22 | 21 | 1 | 6 | 26 |  |
| majoneza | 26 | 39 | 28 | 38 | 18 | 37 | 48 | 35 | 5 | 8 | 26 |  |
| kecap | 26 | 19 | 28 | 27 | 8 | 24 | 26 | 17 | 3 | 11 | 26 |  |

Namirnice bez ijednog proizvoda u Plodinama (zadano): 15 od 74 (cesnjak, rajcica, mrkva, krastavac, tikvica, kupus, zelena_salata, rukola, matovilac, radic, endivija, persin, banana, limun, naranca). Svježe voće i povrće Plodina (bez kategorije i EAN-a) `plan_basket` ipak koristi (`food_unverified`, pravilo prve ili druge riječi); u ovoj tablici i u `find_products` nije.
