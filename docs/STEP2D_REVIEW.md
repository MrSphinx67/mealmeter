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
| margarin | 99 | 90 | 9 | 9 | 0 |
| griz | 38 | 29 | 9 | 9 | 0 |
| riza | 452 | 443 | 16 | 9 | 0 |
| papar | 241 | 239 | 13 | 8 | 6 |
| vanilin_secer | 70 | 63 | 10 | 8 | 1 |
| kiselo_vrhnje | 127 | 120 | 7 | 7 | 0 |
| palenta | 83 | 76 | 7 | 7 | 0 |
| slanina | 705 | 698 | 12 | 7 | 0 |
| rajcica_konzerva | 191 | 184 | 7 | 7 | 0 |
| pileca_prsa | 228 | 224 | 11 | 6 | 2 |
| jaja | 347 | 342 | 29 | 6 | 1 |
| parmezan | 111 | 105 | 6 | 6 | 0 |
| krastavac | 72 | 66 | 18 | 6 | 0 |
| mozzarella | 211 | 205 | 10 | 6 | 0 |
| ocat | 121 | 116 | 14 | 5 | 0 |
| kecap | 177 | 172 | 13 | 5 | 0 |
| kukuruz | 157 | 152 | 8 | 5 | 0 |
| pasirana_rajcica | 139 | 134 | 7 | 5 | 0 |
| mljeveno_meso | 106 | 101 | 5 | 5 | 0 |
| junetina | 288 | 283 | 6 | 5 | 0 |
| grasak | 152 | 147 | 6 | 5 | 0 |
| kiseli_kupus | 131 | 128 | 9 | 4 | 1 |
| grah | 401 | 398 | 17 | 4 | 1 |
| jabuka | 394 | 390 | 4 | 4 | 0 |
| brasno | 383 | 379 | 9 | 4 | 0 |
| koncentrat_rajcice | 40 | 36 | 4 | 4 | 0 |
| prasak_za_pecivo | 48 | 44 | 4 | 4 | 0 |
| senf | 136 | 135 | 6 | 3 | 2 |
| zobene_pahuljice | 69 | 67 | 4 | 3 | 1 |
| svinjetina | 454 | 451 | 3 | 3 | 0 |
| sol | 160 | 161 | 2 | 2 | 3 |
| limun | 98 | 96 | 2 | 2 | 0 |
| mrkva | 121 | 119 | 2 | 2 | 0 |
| slanutak | 121 | 119 | 3 | 2 | 0 |
| ulje | 166 | 164 | 5 | 2 | 0 |
| krumpir | 238 | 236 | 3 | 2 | 0 |
| luk | 207 | 205 | 7 | 2 | 0 |
| gljive | 112 | 112 | 3 | 1 | 1 |
| tuna | 448 | 448 | 51 | 1 | 1 |
| persin | 62 | 61 | 1 | 1 | 0 |
| naranca | 112 | 111 | 2 | 1 | 0 |
| zelena_salata | 73 | 72 | 1 | 1 | 0 |
| secer | 226 | 225 | 3 | 1 | 0 |
| rajcica | 201 | 200 | 8 | 1 | 0 |

30 nasumičnih promijenjenih grupa (s više od jednog lanca):

| namirnica | grupa | promjena | lanaca | % naziva namirnice | % isključenog naziva | nazivi |
|---|---|---|---|---|---|---|
| jogurt | 3870311003185 | član → ambiguous | 8 | 13,00 | 0,00 | dukat: DOMAĆE BLAGO AYRAN 1.9% m.m. 225 g HR; jadranka_trgovina: MLIJEČNI NAPITAK AYRAN 225G DOMAĆE BLAGO DUKAT; ktc: AYRAN 225g DUKAT; vrutak: DUKAT AYRAN 225G 1,9%MM DOMAĆE BLAGO -20/1- 32368; ntl: AYRAN 1,9% mm 225 g DOMAĆE BLAGO DUKAT; spar: AYRAN 1,9% DOMAĆE BLAGO 225 g; metro: 225G DOMAĆE BLAGO AYRAN 1,9%MM; tommy: JOGURT AYRAN 225 g DOMAĆE BLAGO |
| tjestenina | 8008857300634 | član → ambiguous | 2 | 50,00 | 0,00 | bure: TJ.CAVATAPPI 63 500 g; jadranka_trgovina: TJESTENINA CAVATAPPI 63 500G REGGIA |
| tjestenina | 3858881682801 | član → ambiguous | 2 | 50,00 | 0,00 | tommy: TJ.ŠPAG. 10 400 g BEZ JAJA CE; ribola: TJ.ŠPAGETI 400 g BEZJAJA BR.10 TJ.CETIN |
| med | 5900658735505 | član → ambiguous | 6 | 33,00 | 0,00 | ntl: MEDENJACI MIX S TAMNOM ČOKOLADOM 400 g LAMBERTZ; trgocentar: MED.LAMBERTZ POLONIA ZARTBITTE 400G (10); ribola: MED.SRC.TAM.ČO.400 g ULTRA; djelo_vodice: LAMBERTZ SRCA TAMNA ČOK. 400G; gavranovic: MEDENJACI MIX 400g TAMNA ČOKOLADA LAMBERTZ; ktc: MEDENJACI 400g LAMBERTZ TAMNA ČOKOLADA |
| tvrdi_sir | 8721800082110 | član → ambiguous | 16 | 6,00 | 0,00 | ribola: SIR LEERDAM.250 g DU; studenac: SIR LEERDAMMER ORGINAL 250 g; gavranovic: SIR LEERDAMMER ORIGINAL 250g; jadranka_trgovina: SIR LEERDAMMER ORIGINAL 250G; konzum: SIR POLUTVRDI 250g LEERDAMMER; kaufland: Leerdammer Sir kravlji 45% Original 250g; tommy: SIR LEERDAMMER ORIGINAL 250 g DUKAT; spar: SIR LEERDAMMER ORIGINAL 250 g; plodine: SIR EMMENTALER ORIGINAL 250 G LEERDAMMER; boso: SIR LEERDAMMER 250 g ORIGINAL; vrutak: SIR LEERDAMMER ORIGINAL 250G -12/1-; trgovina-krk: SIR LEERDAMMER ORIGINAL 250 gr; ktc: SIR LEERDAMMER 250g DUKAT; lorenco: LEERDAMMER ORIGINAL 250G; branka: SIR LEERDAMMER ORIGINAL 250g; dukat: LEERDAMMER ORIGINAL 250g |
| pileca_prsa | 3850159113383 | član → ambiguous | 15 | 13,00 | 0,00 | trgocentar: PILEĆI FILE OD PRSA 400G,VINDIJA; kaufland: Cekin odresci pilećeg filea od prsa 400g; ntl: PILEĆI ODRESCI OD FILE-A PRSIJU 400 g VINDIJA; studenac: ODRES. PIL.FILEA OD PRSA 400g; spar: PILEĆI ODRESCI OD FILEA 400 g; ribola: PIL.ODRE.FIL.400 g VNDIJA; gavranovic: CEKIN PILEĆI ODRESCI OD FILEA PRSIJU 400g; trgovina-krk: PILEĆI ODRESCI OD FILEA PRSIJU 400 g VIND; vrutak: N-VIN.PIL.ODRESCI 400G OD FILEA PRSIJU; konzum: ODRESCI PILEĆEG FILE OD PRSA 400g; lorenco: ODRESCI PILEĆEg FILEA OD PRSA 400g; metro: 400GR ODRESCI PILEĆEG FILEA; djelo_vodice: VIN.ODRESCI FILE PRSIJU 400G; tommy: PILEĆI ODR./FILE PRSIJU 400 g; plodine: PILECI ODRESCI FILEA 400 G VINDIJA |
| tjestenina | 8005121000221 | član → ambiguous | 4 | 50,00 | 0,00 | vrutak: TJEST DIVELLA 500G ELICOIDALI 22 -24/1-; stridon: ELICODIALI 22 500G (24) DIVELLA (IT); branka: TJESTENINA ELICODIALI 500g; djelo_vodice: ELICOIDALI 500g |
| svinjetina | 3859893378447 | član → ambiguous | 2 | 50,00 | 0,00 | studenac: SVINJSKI BUT SK U KOŽI DALM.OBR MM; metro: CCA12KG SVINJ.BUT SK OBRAĐEN |
| jogurt | 3850257061067 | član → ambiguous | 3 | 33,00 | 0,00 | kaufland: Kravica Kraljica Tek.jog.2,8%m.m.1kg PET; spar: JOG.TEKUĆI 2,8% KRALJ.KRAV 1kg; ktc: JOGURT TEKUĆI 2,8% M.M. 1kg |
| jaja | 8699462605148 | član → ambiguous | 2 | 50,00 | 0,00 | stridon: PRINCESS MILKY CREAM 15 g (24); branka: JAJE PRINCESS SUPRISE 15g |
| papar | 3859891493609 | član → ambiguous | 8 | 25,00 | 0,00 | plodine: PREMIUM SALATA KIS.KUPUS S CES.,PAP.I CRVENOM PAPRIKOM 250GR; kaufland: Sal.kis.kup.češ.pap.i crv.pap.250g/220g; ribola: KIS.KUP.CR PAP 250 g; lorenco: PREM.SAL.MADIG PAPAR+CRV.PAPR.250g; studenac: SALATA KIS. ZELJE ČEŠ/PAP/C.PA 250 g; tommy: SAL.KIS.KUPUS 250g CRV.PAPR.; spar: KUPUS KIS ČEŠNJ,PAP.CR.P 250 g; konzum: KUPUS KIS PAPRIKA ČEŠNJAK PAPAR 250g |
| jogurt | 3850108037654 | član → ambiguous | 8 | 38,00 | 0,00 | stridon: Z BREGOV EUFORIJA CRISPY MIX 150 g (kokos-nugat); lorenco: EUFORIJA KREM JOG.KOKOS I NOUG.150g; ribola: JOG.CRIS.MIX 150 g V INDIJA; branka: JOGURT EUFORIJA CRISPY MIX 150g; studenac: JOGURT EUFORIJA CRIS Z BREGOV 150g; plodine: Z.BREGOV EUFORIJA CRISPY MIX 150 G VINDIJA; tommy: JOGURT EUFORIJA 150 g CRISPY MIX Z BREGOV; trgovina-krk: FRESKA EUFORIJA CRISPY MIX 150g |
| vrhnje_za_kuhanje | 4034900027801 | član → ambiguous | 2 | 50,00 | 0,00 | roto: VRHNJE ZA KUH CREME CUISINE 15% BM 1L (12); metro: 1L MEGGLE CREME CUISINE |
| tjestenina | 3859888499102 | član → ambiguous | 7 | 29,00 | 0,00 | lorenco: LJILJANI 500g KLARA MARIĆ; studenac: TJESTENINA LJILJANI 500g KLARA MARIĆ; vrutak: TJEST KLARA M LJILJANI 500G -10/1 111; konzum: TIJESTO LJILJANI 500g KLARA M; ribola: TJ.LJILJANI 500 g KLARA MARIĆ; tommy: TJ.LJILJANI 500 g KLARA M; kaufland: Klara M ljiljani 500g |
| tjestenina | 3838700010480 | član → ambiguous | 4 | 25,00 | 0,00 | tommy: TJ.REZANCI VALJANI 400 G ZLATO; bure: TJ.REZANCI 400g VALJANI; konzum: TJEST. FETTUCCINE 8 JAJ 400g ZLATOPOLJE; spar: TJE.ZL.POLJE VALJANI REZ.400 g |
| grasak | 3838977044508 | član → ambiguous | 4 | 25,00 | 0,00 | tommy: POLI GREEN MINI 220 g; kaufland: Poli Salama od graška Green 220g; studenac: POLI GREEN MINI 220 g; ribola: POLI GREEN 220 g PER UTNINA |
| krastavac | 3858891564364 | član → ambiguous | 4 | 25,00 | 0,00 | ribola: ULT.PL.1400g KRASTAVCI; djelo_vodice: KRASTAVCI ULTRA 1500ML; vrutak: KRASTAVCI I.KL (3-6CM) 1500ML1400G (NETO 800G) ULTRA+ -6/1; trgocentar: ULTRA KRASTAVCI (3-6) 1400G-800G (6) |
| dodatak_jelima | 40804873 | član → ambiguous | 3 | 33,00 | 0,00 | studenac: DODATAK JELIMA DRES. JOGURT 250 ml; bure: JOGURT SALAT.250 ml KUHNE; lorenco: SALATFIX JOGURT 250ML |
| svinjetina | 3850139523423 | član → ambiguous | 2 | 50,00 | 0,00 | studenac: SVJEŽA SVINJSKA REBRA PIK VRBOVEC; konzum: SV REBRA |
| grah | 8000627300431 | član → ambiguous | 3 | 67,00 | 33,00 | ntl: GRAH ZRNAŠ NISKI 250G; trgovina-krk: SJEME GRAH ZRNAŠ 250 g MARCON; plodine: GRAH ZRNAS NISKI |
| med | 5900658800807 | član → ambiguous | 3 | 33,00 | 0,00 | trgocentar: MED.LAMBERTZ SPRING COOKIES 350G(6); konzum: KEKS SPRING PVC 350 g LAMBERTZ; djelo_vodice: LAMBERTZ SPRING COOKIES 350G |
| grasak | 8000627400339 | član → ambiguous | 2 | 50,00 | 50,00 | ntl: GRAŠAK ČUDO KELVEDONA 250 G; plodine: SJEME GRASAK CUDO KLEVEDONA |
| tjestenina | 8076802085868 | član → ambiguous | 6 | 33,00 | 0,00 | lorenco: TJEST.PIPETTE RIGATE 500 g BARI; kaufland: Barilla Tjes.Pipette Rigate 500g; plodine: TJESTENINA PIPETE RIGATE 86 500 G BARILA KUTIJA; ribola: TJ.BARILLA PIP 500 g PIPETTE RIGATE; tommy: TJ. BARILLA PIPETTE RIGATE BR.86 500 g; spar: TJES.BARILLA PIPETTE RIGT.500g |
| med | 3850220408806 | član → ambiguous | 3 | 33,00 | 0,00 | trgovina-krk: MARINIRANI PILEĆI MINI FILE MEĐ.PILE 400G; spar: PILEĆI MARINIRANI FILE 400 g; konzum: MARINIRANI PILEĆI MINI FILE 400g |
| tuna | 8004030860025 | izvan → član | 7 | 57,00 | 14,00 | kaufland: Rio Mare Insal.sal.tuna cous cous2x160g; konzum: TUNJ SALATA COUS COUS 2X160g RIO MARE; spar: TUNA SAL.RIO MARE COUS 2X160 g; tommy: TUNA SALATA CUS CUS 2X160 G RIO MARE; lorenco: TUNA -COUS-COUS SAL.2\*160g BOWL.; plodine: TUNA COUS-COUS SAL.2X160G BOWL; metro: 160GX2 RIO MARE INSALA.CUS CUS |
| tjestenina | 8008857300603 | član → ambiguous | 4 | 50,00 | 0,00 | vrutak: TJEST REGGIA 500G GOMITI RIGATI U-21127 -24/1-; bure: TJ.GOMITI 60 500 g RIGATI REGGIA; trgocentar: GOMITI RIGATI 500G; jadranka_trgovina: TJESTENINA GOMITI RIGATI 60 500G REGGIA |
| tjestenina | 3838700015669 | član → ambiguous | 7 | 43,00 | 0,00 | branka: TJESTENINA GRANDE ZLATICA 45 400g; spar: TJES.ZL.POLJE REZA.KUKUR.400 g; tommy: TJ. ZLATICA ŠIROKA 400 g ZLATO P; konzum: TJEST. ZLATICA 45 400g ZP; lorenco: GRANDE ZLATICA BR.45 400 g; studenac: TJ. ZL. POLJE BR.45 REZANCI 400 g; trgocentar: ZP TJEST.ZLATICA 45 400G (15) PODRAVKA |
| riza | 8710447482179 | član → ambiguous | 2 | 50,00 | 0,00 | lorenco: DOVE SAPUN TEK LOT.FLOiR.MILK 500ML; plodine: DOVE TEK.SAP. REFIL 500 ML LOT.FLOWER RICE MILK |
| med | 3850220428507 | član → ambiguous | 3 | 33,00 | 0,00 | konzum: MEĐ.PILE PILEĆI MIX MINI 500 g; spar: PILEĆI MINI MIX 500 g; plodine: MEDJIMURSKO PILE PILECI MIX MINI 500 G PERUTNINA |
| slatko_vrhnje | 3850104230585 | član → ambiguous | 5 | 20,00 | 0,00 | stridon: DOLCELA ŠLAG 5 TEK. BILJ. ŠLAG 1 L PODRAVKA (12); ktc: ŠLAG PRIPRAVAK 1L DOLCELA; lorenco: ŠLAg 1 L PODRAVKA; djelo_vodice: VRHNJE ZA ŠLAG 1L PODRAVKA; ribola: ŠLAG TEK.BILJNI 1l P ODRAVKA |

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
| studenac | RUKOLA POSUDICA SNIŽ. 100 g | HRANA | hrana | kucanstvo | words |
| gavranovic | ULOŠCI FEMME 8/1 SUPER NTL | Hrana | hrana | higijena | words |
| gavranovic | GRANA RUŽE S PUPOM 68cm, 2 CVIJETA, KREM rasprodaja | Hrana | hrana | ostalo | words |
| gavranovic | SYOSS ŠAMPON COLOR GUARD 440 ml | Hrana | hrana | kozmetika | words |
| gavranovic | ŽARULJA PHILIPS LED A55 9W (65 W) E27 | Hrana | hrana | kucanstvo | words |
| gavranovic | POSUDA ZA ČUVANJE DUBOKA 575 ml-rasprodaja | Hrana | hrana | kucanstvo | words |
| gavranovic | IGR.BALONI ZA PUHANJE rasprodaja | Hrana | hrana | ostalo | words |
| tommy | ZAČIN SJEME SEZAMA 40 g UBENA | PAKIRANA HRANA I PIĆE | pice | ostalo | words |
| plodine | GRANA RUZE S PUPOM 68CM KREM 196 IC |  | hrana | ostalo | ean_inherited |
| gavranovic | TANJUR MELAMINE | Hrana | hrana | kucanstvo | words |
| gavranovic | BOŽ.UKRAS PATULJAK 35cm 2023-rasprodaja | Hrana | hrana | kucanstvo | words |
| gavranovic | BOŽ.UKRASNA GRANČICA 22cm 2023-rasprodaja | Hrana | hrana | kucanstvo | words |
| gavranovic | GLISS ŠAMPON OIL NUTRITIVE 250ml | Hrana | hrana | kozmetika | words |
| lorenco | SOLNI CVIJET 125g VREĆICA |  | hrana | unknown | none |
| ktc | PRALINE MINI CVIJET 120g KAMILA | HRANA | hrana | ostalo | words |
| gavranovic | POSUDA ZA ČUVANJE DUBOKA 1075 ml-rasprodaja | Hrana | hrana | kucanstvo | words |
| gavranovic | UPALJAČ GRADOVI | Hrana | hrana | kucanstvo | words |
| ntl | BROKULA CVIJET 2,5kg ZMH | Hrana | hrana | ostalo | words |
| ntl | SELAGINELA DECO BOŽIĆ FI 9 | Ostalo | hrana | kucanstvo | ean_inherited |
| gavranovic | BOŽ.UKRAS SOB 16X10X14cm 2023-rasprodaja | Hrana | hrana | kucanstvo | words |

20 nasumičnih „hrana“ proizvoda koji i dalje izgledaju neprehrambeno (od 590; u Koraku 2C ih je bilo 2.168, ali s drugim popisom za izvještaj):

| lanac | naziv | kategorija | skupina | izvor |
|---|---|---|---|---|
| spar | WHISKEY SHANKYS + ČAŠE | Pića | alkohol | chain |
| metro | 0,7L JAMESON + 2 ČAŠE | piće | alkohol | chain |
| djelo_vodice | LIKER JAGERMEISTER 0,7L + 2 ČAŠE | BILJNI LIKERI | alkohol | chain |
| spar | CVIJET SOLI ADRIATIQ BIO 250 g | Hrana | hrana | chain |
| metro | 0,7L J.WALKER WHISKY RL+2 ČAŠE | piće | alkohol | chain |
| stridon | PJENUŠAC FREIXENET CARTA NEVADA POK.PAKET+2 ČAŠE | PIĆA | alkohol | chain |
| trgovina-krk | KRUH SJEME 400 g SVJ. PEČ. BEZ GLUTENA RATV | Hrana | hrana | chain |
| vrutak | N-GAV KULENOV CVIJET NAREZAK 80G | MESO | hrana | chain |
| tommy | PAKET MILKA MIX 96 g + IGRAČKA | PAKIRANA HRANA I PIĆE | pice | chain |
| plodine | CVIJET SOLI 125 G SOLANA NIN |  | hrana | ean_inherited |
| lorenco | CVIJET SOLI KUTIJICA 125g |  | hrana | ean_inherited |
| zabac | BOSANSKI LONAC 400G, BAKINA KUHINJA | Smrznuta hrana | hrana | chain |
| tommy | KOBASICA KULEN CVIJET NAR.80 g | HLAĐENO I SMRZNUTO | hrana | chain |
| roto | WHISKEY JACK DANIELS 0,70 GUITAR CASE (1)\* | ŽESTOKO | alkohol | chain |
| studenac | WHISKEY JAMESON 2 ČAŠE 0,7 l | PIĆE | alkohol | chain |
| roto | RAKIJA ZLATNA DUNJA 0,70 + 2 ČAŠE(1)\* | ŽESTOKO | alkohol | chain |
| kaufland | Badel prima brand 35% 0,7 l + 2 čaše | PIĆE | alkohol | chain |
| lorenco | SUNCOKRETOVO SJEME OLJUŠTENE PEČENE |  | hrana | ean_inherited |
| stridon | SVINJSKA CRIJEVA 34/36 10M POSUDA RADAUER | HRANA | hrana | chain |
| roto | COGNAC MARTELL VS+2 ČAŠE 0,70 (6)\* | ŽESTOKO | alkohol | chain |
