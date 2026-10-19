# Pregled osnovnih namirnica

Generirano skriptom `scripts/staples_review.py` iz `src/mealmeter/staples.yaml` i arhive 2026-10-19. **Ovo je prijedlog za ručni pregled**:
za svaku namirnicu označi koji kandidati ne pripadaju (→ dodaj `must_not_match`) i koji nedostaju
(→ proširi `must_match`), pa ponovno pokreni skriptu.

Kandidati su grupe proizvoda (isti EAN, ili lanac + naziv bez EAN-a), poredane po broju lanaca i
trgovina. Cijena po jedinici je u jedinici namirnice gdje postoji; `pouzdanost` je
`unit_confidence/pack_source`. „Isključeni“ su grupe koje pogađa `must_match`, ali i `must_not_match`;
uz svaku je uzorak koji ju je isključio.

## Sadržaj

- [brašno](#brasno) (`brasno`)
- [šećer](#secer) (`secer`)
- [sol](#sol) (`sol`)
- [ulje (suncokretovo/biljno)](#ulje) (`ulje`)
- [maslinovo ulje](#maslinovo_ulje) (`maslinovo_ulje`)
- [maslac](#maslac) (`maslac`)
- [margarin](#margarin) (`margarin`)
- [mlijeko](#mlijeko) (`mlijeko`)
- [jogurt](#jogurt) (`jogurt`)
- [kiselo vrhnje](#kiselo_vrhnje) (`kiselo_vrhnje`)
- [vrhnje za kuhanje](#vrhnje_za_kuhanje) (`vrhnje_za_kuhanje`)
- [slatko vrhnje](#slatko_vrhnje) (`slatko_vrhnje`)
- [svježi sir](#svjezi_sir) (`svjezi_sir`)
- [tvrdi sir (gauda, trapist, edamac)](#tvrdi_sir) (`tvrdi_sir`)
- [mozzarella](#mozzarella) (`mozzarella`)
- [parmezan](#parmezan) (`parmezan`)
- [jaja](#jaja) (`jaja`)
- [luk (crveni/žuti)](#luk) (`luk`)
- [češnjak](#cesnjak) (`cesnjak`)
- [krumpir](#krumpir) (`krumpir`)
- [rajčica (svježa)](#rajcica) (`rajcica`)
- [pasirana rajčica](#pasirana_rajcica) (`pasirana_rajcica`)
- [koncentrat rajčice](#koncentrat_rajcice) (`koncentrat_rajcice`)
- [mrkva](#mrkva) (`mrkva`)
- [paprika (svježa)](#paprika) (`paprika`)
- [krastavac (svježi)](#krastavac) (`krastavac`)
- [tikvica](#tikvica) (`tikvica`)
- [kupus (svježi)](#kupus) (`kupus`)
- [kiseli kupus](#kiseli_kupus) (`kiseli_kupus`)
- [zelena salata](#zelena_salata) (`zelena_salata`)
- [špinat](#spinat) (`spinat`)
- [peršin](#persin) (`persin`)
- [gljive (šampinjoni)](#gljive) (`gljive`)
- [riža](#riza) (`riza`)
- [tjestenina](#tjestenina) (`tjestenina`)
- [kruh](#kruh) (`kruh`)
- [griz](#griz) (`griz`)
- [palenta (kukuruzna krupica)](#palenta) (`palenta`)
- [zobene pahuljice](#zobene_pahuljice) (`zobene_pahuljice`)
- [krušne mrvice](#krusne_mrvice) (`krusne_mrvice`)
- [kvasac](#kvasac) (`kvasac`)
- [prašak za pecivo](#prasak_za_pecivo) (`prasak_za_pecivo`)
- [vanilin šećer](#vanilin_secer) (`vanilin_secer`)
- [kakao (prah)](#kakao) (`kakao`)
- [čokolada za kuhanje](#cokolada_za_kuhanje) (`cokolada_za_kuhanje`)
- [pileća prsa / file](#pileca_prsa) (`pileca_prsa`)
- [piletina (cijelo pile, batak, zabatak, krila)](#piletina) (`piletina`)
- [mljeveno meso](#mljeveno_meso) (`mljeveno_meso`)
- [svinjetina (svježe meso)](#svinjetina) (`svinjetina`)
- [junetina / govedina (svježe meso)](#junetina) (`junetina`)
- [slanina / panceta](#slanina) (`slanina`)
- [šunka (kuhana)](#sunka) (`sunka`)
- [tuna (konzerva)](#tuna) (`tuna`)
- [grah](#grah) (`grah`)
- [leća](#leca) (`leca`)
- [slanutak](#slanutak) (`slanutak`)
- [kukuruz šećerac (konzerva)](#kukuruz) (`kukuruz`)
- [grašak](#grasak) (`grasak`)
- [banana](#banana) (`banana`)
- [jabuka](#jabuka) (`jabuka`)
- [limun](#limun) (`limun`)
- [naranča](#naranca) (`naranca`)
- [papar](#papar) (`papar`)
- [mljevena paprika (začin)](#mljevena_paprika) (`mljevena_paprika`)
- [dodatak jelima (Vegeta i sl.)](#dodatak_jelima) (`dodatak_jelima`)
- [ocat (alkoholni/vinski)](#ocat) (`ocat`)
- [med](#med) (`med`)
- [kava](#kava) (`kava`)
- [senf](#senf) (`senf`)
- [majoneza](#majoneza) (`majoneza`)
- [kečap](#kecap) (`kecap`)
- [voda (negazirana)](#voda) (`voda`)

<a id="brasno"></a>
## brašno (`brasno`)

jedinica: **kg** · loose_produce: **false** · grupa: **443** · isključenih grupa: **109**

sinonimi: brasno, psenicno brasno  
must_match: `brasn | bras\b`
atributi: tip = glatko, ostro, polubijelo, integralno; vrsta = psenicno, pirovo, razeno, kukuruzno; oznaka = t400, t550, t850, t1100, 00

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3858884172569 | PŠENIČNO BRAŠNO 1KG GLATKO T-550,ČAKOVEČKI MLINOVI | 1 kg | 20 | 861 | 0,75–1,69 /kg | high/name | tip=glatko, vrsta=psenicno, oznaka=t550 |
| 2 | 3850104052552 | BRAŠNO KUKURUZNO 1KG (10) (PAL 60), PODRAVKA | 1 kg | 19 | 674 | 1,21–1,89 /kg | high/name | vrsta=kukuruzno |
| 3 | 3850104223624 | BRAŠNO GLATKO T-550 1KG (10) (PAL 60) PODRAVKA | 1 kg | 18 | 1167 | 0,62–0,83 /kg | high/name | oznaka=t550, tip=glatko, vrsta=psenicno |
| 4 | 3850104223631 | BRAŠNO PŠEN. T-400 OŠTRO 1 KG (10) (PAL60) PODRAVKA | 1 kg | 17 | 926 | 0,69–0,83 /kg | high/name | tip=ostro, vrsta=psenicno, oznaka=t400 |
| 5 | 3858884172637 | BRASNO T-400 1 KG CAKOVECKI MLINOVI - OSTRO ZA KOLACE | 1 kg | 16 | 953 | 0,82–162,25 /kg | high/name | oznaka=t400, tip=ostro, vrsta=psenicno |
| 6 | 3858884172583 | BRAŠNO PŠENIČNO T-400 ZA DIZANA TIJESTA 1KG ČAKOVEČKI MLINOV | 1 kg | 16 | 895 | 1,09–1,92 /kg | high/name | vrsta=psenicno, oznaka=t400 |
| 7 | 3858884172521 | BRAŠNO PŠENIČNO GLATKO T-550, 5KG ČAKOVEČKI MLINOVI(PAL200) | 5 kg | 16 | 703 | 0,71–16,00 /kg | high/name | oznaka=t550, tip=glatko, vrsta=psenicno |
| 8 | 3850104223617 | PŠEN.BRAŠNO T 550 GLATKO 2 KG PODRAVKA(6) (PAL 48) | 2 kg | 15 | 823 | 0,56–0,82 /kg | high/name | tip=glatko, vrsta=psenicno, oznaka=t550 |
| 9 | 3838700295269 | PIROVO INTEGRALNO BRAŠNO PODRAVKA 1 kg (10) | 1 kg | 15 | 606 | 2,00–2,99 /kg | high/name | vrsta=pirovo, tip=integralno |
| 10 | 3850104223648 | PŠEN.BRAŠNO T -400 OŠTRO 2 KG, PODRAVKA(6) (PAL 48) | 2 kg | 14 | 694 | 0,45–0,85 /kg | high/name | tip=ostro, vrsta=psenicno, oznaka=t400 |
| 11 | 3858884172576 | BRAŠNO ZA TANKA TIJESTA 1 kg T- 700 ČAKOVEČKI MLI | 1 kg | 12 | 643 | 1,09–1,69 /kg | high/name |  |
| 12 | 3850104423659 | BRAŠNO GL.T-550 5 kg PŠ.BIJELO PODRAVKA | 5 kg | 11 | 286 | 0,54–1,03 /kg | high/name | oznaka=t550, tip=glatko, vrsta=psenicno |
| 13 | 3858884172538 | BRAŠNO OŠTRO ZA KOLAČE T-400 5KG,ČAKOVEČKI MLINOVI | 5 kg | 10 | 381 | 0,75–0,84 /kg | high/name | oznaka=t400, tip=ostro |
| 14 | 3858884170169 | BRAŠNO KUKURUZNO 1KG ČAKOVEČKI MLIN (10) | 1 kg | 9 | 420 | 1,31–1,79 /kg | high/name | vrsta=kukuruzno |
| 15 | 3858884175751 | BRAŠNO PŠENIČNO T-550 ZA PIZZU 1KG ČAKOVEČKI MLINOVI | 1 kg | 9 | 405 | 1,39–1,95 /kg | high/name | oznaka=t550, vrsta=psenicno |
| 16 | 3858884172590 | BRASNO T-550 25 KG GLATKO CAKOVECK MLINOVI | 25 kg | 9 | 143 | 0,03–1,04 /kg | high/name | tip=glatko, vrsta=psenicno, oznaka=t550 |
| 17 | 3859891753246 | N-BRAŠNO ULTRA 1KG GLATKO T-550 -10/1- | 1 kg | 8 | 161 | 0,68–0,80 /kg | high/ean | tip=glatko, vrsta=psenicno, oznaka=t550 |
| 18 | 3850104065019 | BRAŠNO RAŽENO 900G T-1250 PODRAVKA | 900 g | 8 | 36 | 1,31–2,54 /kg | high/name | vrsta=razeno |
| 19 | 3850104423604 | PŠEN.BRAŠNO T -400 OŠTRO 5 KG, PODRAVKA | 5 kg | 7 | 190 | 0,62–0,83 /kg | high/name | oznaka=t400, tip=ostro, vrsta=psenicno |
| 20 | 3858890102994 | SUPERFOODS eko proseno brašno 250g | 250 g | 7 | 187 | 9,24–11,96 /kg | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| BRAŠ.PŠE.T-1100 PODRAVKA 1 kg | 16 | `pse\b` |
| BRAŠNO PŠE. T-850 1 kg | 15 | `pse\b` |
| SMJESA ZA KRUH (BEZGLUTENSKO BRAŠNO) DR.SCHÄR MIX B 1KG (10) | 15 | `mix\b` |
| KOKOS BRAŠNO 200 g ŠAFRAM (10) | 14 | `kokos` |
| HELJDINO BRAŠNO 1 kg PODRAVKA (10) | 13 | `heljd` |
| SUPERFOODS eko kokosovo brašno 250g | 10 | `kokos` |
| KOKOS BRAŠNO 200G(20) NATURA, MARJAN VOĆE | 8 | `kokos` |
| Š EXTRA KOKOS BRAŠNO ŠAFRAM 200 g (10) | 8 | `kokos` |
| BRAŠNO MIX IT 500G BEZ GLUTENA -10/1 DR.SCHAR | 7 | `mix\b` |
| N-TOAST KLARA ZP 500G S INTEG. BRAŠNOM -8/1- | 7 | `toast` |

</details>

<a id="secer"></a>
## šećer (`secer`)

jedinica: **kg** · loose_produce: **false** · grupa: **362** · isključenih grupa: **102**

sinonimi: secer  
must_match: `secer\b`
atributi: vrsta = u_prahu, smedi, kocke, bijeli

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3859889425063 | ŠEĆER ENCIAN 500G SMEĐI TAMNI MUSCOVADO - TRSKA | 500 g | 19 | 752 | 6,38–9,38 /kg | high/name | vrsta=smedi |
| 2 | 3859889425742 | ŠEĆER ENCIAN 500G SMEĐIDEMERARA 071004 | 500 g | 17 | 596 | 3,98–6,98 /kg | high/name | vrsta=smedi |
| 3 | 3858881087460 | ŠEĆER U PRAHU 250 g FRANCK VREĆ. (10) | 250 g | 16 | 1058 | 3,76–5,16 /kg | high/name | vrsta=u_prahu |
| 4 | 3858881087477 | ŠEĆER U PRAHU 500 g FRANCK VREĆ. (10) | 500 g | 15 | 754 | 3,18–4,98 /kg | high/name | vrsta=u_prahu |
| 5 | 3859890118145 | ŠEĆER SMEĐI OD ŠEĆERNE TRSKE 1000G | 1 kg | 15 | 303 | 2,59–4,49 /kg | high/name | vrsta=smedi |
| 6 | 5010651001115 | ŠEĆER SMEĐI 500G BILLINGTON'S DEMERARA CANE SUGAR -10/1 | 500 g | 12 | 538 | 3,48–5,98 /kg | high/name | vrsta=smedi |
| 7 | 3859888279476 | SECER KOCKA BIJELA 500 G RIO PAK | 500 g | 11 | 733 | 2,66–5,50 /kg | high/name | vrsta=kocke |
| 8 | 9007829025017 | Agragold Šećer kristal 1kg_OC | 1 kg | 11 | 392 | 0,65–1,33 /kg | high/name | vrsta=bijeli |
| 9 | 3859893641008 | Viro Šećer bijeli kristal 1 kg_OC | 1 kg | 10 | 759 | 0,75–0,99 /kg | high/name | vrsta=bijeli |
| 10 | 3830049080018 | ŠEĆER BIJELI KRISTAL 1KG DIAMANT | 1 kg | 10 | 334 | 0,79–1,33 /kg | high/name | vrsta=bijeli |
| 11 | 3859892259518 | ŠEĆER BIJELI U KOCKI 500G LARA -7/1- | 500 g | 10 | 91 | 4,30–6,18 /kg | high/name | vrsta=kocke |
| 12 | 3859892259877 | ŠEĆER SMEĐI 500 g U KOCKI LARA | 500 g | 10 | 87 | 0,20–7,38 /kg | high/name | vrsta=smedi |
| 13 | 5010651001146 | SECER SMEDJI 1 KG DEMERARA BILLINGTON | 1 kg | 9 | 526 | 3,49–5,29 /kg | high/name | vrsta=smedi |
| 14 | 3858890100723 | Encian bio šećer kokosove palme 200g | 200 g | 9 | 274 | 16,25–23,45 /kg | high/name |  |
| 15 | 3856020238520 | NARANČA ŠEĆER 10 g DOLCELA | 10 g | 9 | 183 | 33,00–45,00 /kg | high/name |  |
| 16 | 3859888163218 | ŠEĆER U PRAHU 500G (10), ŠAFRAM | 500 g | 9 | 144 | 2,66–79,50 /kg | high/name | vrsta=u_prahu |
| 17 | 3859888279698 | ŠEĆER SMEĐI RIO-PAK TURBINADO 750 g | 750 g | 8 | 568 | 2,15–3,13 /kg | high/name | vrsta=smedi |
| 18 | 3858890100969 | ŠEĆER SMEĐI SVIJETLI NERAF. MUSCOVADO 500 g ENCIAN | 500 g | 8 | 353 | 5,58–8,58 /kg | high/name | vrsta=smedi |
| 19 | 3859888163669 | ŠEĆER U PRAHU ŠAFRAM 200G-12/1- | 200 g | 8 | 196 | 3,30–6,75 /kg | high/name | vrsta=u_prahu |
| 20 | 3859890236696 | ŠEĆER BIJELI U KOCKI 500 g LARA VM2 | 500 g | 8 | 78 | 4,98–7,36 /kg | high/name | vrsta=kocke |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| DOLCELA VANILIN ŠEĆER 8 g 5+1 GRATIS PODRAVKA (44) | 20 | `vanilin` |
| DOLCELA VANILIN ŠEĆER 8 g PODRAVKA (44) | 19 | `vanilin` |
| LIMUN ŠEĆER 10G (50) PODRAVKA (PAL 468) | 19 | `limun` |
| RUM ŠEĆER 10G (50) PODRAVKA (PAL 468) | 18 | `rum\b` |
| DOLCELA LIMUN ŠEĆER 10 g 3 PAK (26) PODRAVKA | 17 | `limun` |
| DOLCELA RUM ŠEĆER 10 g 3 PAK (26) PODRAVKA | 15 | `rum\b` |
| ŠEĆER CIMET 10G 3PAK DOLCELA PODRAVKA | 14 | `cimet` |
| VANILIN ŠEĆER BOUR. DOLCELA 10 g 3/1 | 13 | `vanilin` |
| VANILIN ŠEĆER DR OETKER 8G -50/1- | 12 | `vanilin` |
| KOTANYI VANILIN ŠEĆER AROMA LIMUNA 50g | 11 | `vanilin` |

</details>

<a id="sol"></a>
## sol (`sol`)

jedinica: **kg** · loose_produce: **false** · grupa: **306** · isključenih grupa: **357**

sinonimi: sol, kuhinjska sol  
must_match: `sol\b`
atributi: vrsta = morska, himalajska, kamena, jodirana; zrno = sitna, krupna

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3870009000328 | SOL KUHINJSKA KAMENA VARENA 5KG, TUZLA | 5 kg | 12 | 576 | 0,38–0,74 /kg | high/name | vrsta=kamena, zrno=sitna |
| 2 | 3859888155343 | SOL KUHINJSKA MORSKA KRUPNA 10KG, SOLANA PAG | 10 kg | 11 | 179 | 0,30–0,65 /kg | high/name | zrno=krupna, vrsta=morska |
| 3 | 3859888155435 | SOL MORSKA KRUPNA 5KG PVC SOLANA (24) | 5 kg | 10 | 167 | 0,53–0,94 /kg | high/name | vrsta=morska, zrno=krupna |
| 4 | 3859888155398 | SOL KUHINJSKA MORSKA SITNA 5KG, SOLANA PAG | 5 kg | 9 | 237 | 0,44–0,92 /kg | high/name | vrsta=morska, zrno=sitna |
| 5 | 3859888155442 | SOL KUHINJSKA MORSKA KRUPNA PVC 1KG, SOLANA PAG(12) | 1 kg | 9 | 212 | 0,49–3,26 /kg | high/name | zrno=krupna, vrsta=morska |
| 6 | 75001629 | N-*PIVO SOL 0.33L -24/1- 4.5%ALC BOCA | 330 ml | 9 | 75 | 3,27–6,52 /l | high/name |  |
| 7 | 3859888817036 | Pag 91 kuhinj. morska sol krupna 1kg PVC | 1 kg | 8 | 494 | 0,49–0,99 /kg | high/name | zrno=krupna, vrsta=morska |
| 8 | 3859888595118 | SOL MORSKA SITNA PVC 1kg SOLANA NIN | 1 kg | 8 | 446 | 0,79–1,19 /kg | high/name | zrno=sitna, vrsta=morska |
| 9 | 3859888155077 | SOL KUHINJSKA MORSKA PVC 1KG, SOLANA PAG (10)(PAL800) | 1 kg | 8 | 365 | 0,62–0,99 /kg | high/name | vrsta=morska, zrno=sitna |
| 10 | 3858881734517 | NITRITNA SOL 1KG, DERMA (20) | 1 kg | 8 | 158 | 1,65–37,25 /kg | high/ean |  |
| 11 | 3870009000045 | SOL KUHINJSKA KAMENA 10KG,TUZLA | 10 kg | 8 | 111 | 0,32–0,67 /kg | high/name | vrsta=kamena, zrno=sitna |
| 12 | 3859888155039 | SOL SITNA MORSKA 25KG VREĆA PAG91 (1PAL=1000KG) | 25 kg | 8 | 62 | 0,02–0,42 /kg | high/name | zrno=sitna, vrsta=morska |
| 13 | 3859888817029 | Pag 91 kuh. morska sol sitna 1kg pvc | 1 kg | 7 | 581 | 0,49–1,09 /kg | high/name | vrsta=morska, zrno=sitna |
| 14 | 3858890104455 | SOL HIMALAJSKA JODIRANA SITNA 500 G ENCIAN | 500 g | 7 | 358 | 5,30–6,38 /kg | high/name | vrsta=himalajska, zrno=sitna |
| 15 | 3858890104479 | SOL HIMALAJSKA JODIRANA KRUPNA 500 G ENCIAN | 500 g | 7 | 143 | 5,02–6,18 /kg | high/name | vrsta=himalajska, zrno=krupna |
| 16 | 3859888155022 | SOL KUHINJSKA MORSKA 10KG, SOLANA PAG (PAL95) | 10 kg | 7 | 113 | 0,57–0,75 /kg | high/name | zrno=sitna, vrsta=morska |
| 17 | 3859892380533 | KUHINJSKA SOL 1KG (20) ULTRA (740PAL) | 1 kg | 7 | 76 | 0,51–0,74 /kg | high/name | zrno=sitna |
| 18 | 3859888155350 | SOL MORSKA KRUPNA SOLANA PAG vreća 25kg (1) | 25 kg | 7 | 17 | 0,01–0,48 /kg | high/name | vrsta=morska, zrno=krupna |
| 19 | 3859888817135 | Pag 91 kuh.morska sol sitna 5 kg, pvc | 5 kg | 6 | 380 | 0,31–0,60 /kg | high/name | vrsta=morska, zrno=sitna |
| 20 | 3859888595989 | SOL SITNA MORSKA BIO 600 G SOLANA NIN | 600 g | 6 | 238 | 0,83–4,48 /kg | high/name | zrno=sitna, vrsta=morska |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| Finish sol za perilicu posuđa 1,5 kg | 20 | `posuda` |
| SOL KUHINJSKA SITNA MORSKA KUTIJA 1KG, SOLANA PAG | 20 | `kutija` |
| SOMAT SOL ZA ZAŠTITU STROJA 1.5KG (8), HENKEL | 19 | `somat` |
| ČIPS ČIPI ČIPS 120G SOL I PAPAR ULTRA REBRASTI -20/1- CHIO | 18 | `papar` |
| SOL KAMENA 1KG TUZLA -10/1- KUTIJA | 16 | `kutija` |
| Kotanyi kuhinjska sol bocica 135 g | 15 | `bocic` |
| SOL KUHINJSKA KRUPNA MORSKA KUTIJA 1KG, SOLANA PAG | 14 | `kutija` |
| Kotanyi himalajska sol 120 g bočica | 13 | `bocic` |
| SOL ZA PERILICU POSUĐA 1,5 kg LIKVI | 13 | `posuda` |
| TRAJNO PEC. ELEP.TWIST - MORSKA SOL I MED 180g | 12 | `med\b` |

</details>

<a id="ulje"></a>
## ulje (suncokretovo/biljno) (`ulje`)

jedinica: **l** · loose_produce: **false** · grupa: **565** · isključenih grupa: **1043**

sinonimi: ulje, suncokretovo ulje, biljno ulje, jestivo ulje  
must_match: `ulje\b`
atributi: vrsta = suncokretovo, repicino, biljno

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3858882210010 | ULJE SUNCOKRET PVC 1L (15) (PAL 675), ZVIJEZDA | 1 l | 21 | 1356 | 1,59–1,72 /l | high/name | vrsta=suncokretovo |
| 2 | 3858882213011 | N-ULJE ZVIJEZDA OMEGOL 1.00L-15/1- | 1 l | 20 | 930 | 1,59–3,09 /l | high/name | vrsta=biljno |
| 3 | 3850171710010 | N-ULJE SUNCOKRET 1L TENA-10/1 (pal.750kom) | 1 l | 19 | 1041 | 1,30–1,72 /l | high/name | vrsta=suncokretovo |
| 4 | 3858882210065 | ULJE BILJNO PVC 1L (15), ZVIJEZDA | 1 l | 18 | 739 | 1,69–2,49 /l | high/name | vrsta=biljno |
| 5 | 3856015313249 | ULJE SUNCOKRET 1,2L (12) (PAL 540) ZVIJEZDA | 1,2 l | 17 | 776 | 1,37–1,72 /l | high/name | vrsta=suncokretovo |
| 6 | 3858882211345 | N-ULJE ZVIJEZDA 3L SUNCOKRET- 4/1- PET | 3 l | 14 | 379 | 1,60–2,41 /l | high/name | vrsta=suncokretovo |
| 7 | 3856015309273 | ULJE ZVIJEZDA 1L MEDITERAN-15/1 | 1 l | 13 | 596 | 2,75–4,09 /l | high/name |  |
| 8 | 3857500104311 | ULJE SUNCOKRETOVO HLADNO PREŠANO 1 L SUNCE VINKOVACA | 1 l | 12 | 800 | 1,53–4,09 /l | high/name | vrsta=suncokretovo |
| 9 | 5310001139773 | ULJE ZA DJECU 200 mL BECUTAN | 200 ml | 10 | 184 | 10,00–24,95 /l | high/name |  |
| 10 | 8006540124758 | Pantene ulje Keratin Protect 100ml | 100 ml | 9 | 272 | 45,80–96,40 /l | high/name |  |
| 11 | 80020073 | SRED.ZA ČIŠČ. PRONTO ULJE RESTAURIANJE NAMJEŠTAJA 100ML | 100 ml | 9 | 135 | 36,40–71,90 /l | high/name |  |
| 12 | 3856015312044 | Zvijezda Ulje suncokretovo XXL 4x1 L | 4 l | 8 | 457 | 1,25–1,67 /l | high/name | vrsta=suncokretovo |
| 13 | 8717228380105 | ULJE ZA WOK 250ML YOUWOK | 250 ml | 8 | 271 | 8,00–22,64 /l | high/name |  |
| 14 | 3858892691809 | ULJE SUN SUPER 100 ml MRKVA ZLATNO ZA UBRZ. TAMNJ. OLI | 100 ml | 7 | 258 | 71,40–112,90 /l | high/name |  |
| 15 | 3858892696231 | GLOW ULJE ZA UBRZANO TAMNJENJE SUPER COCO 100ML | 100 ml | 7 | 194 | 72,50–112,90 /l | high/name |  |
| 16 | 3858892695005 | OLIVAL ULJE ZA ZASTITU OD SUNCA F30 200 ML | 200 ml | 7 | 175 | 69,95–84,95 /l | high/name |  |
| 17 | 3858892691779 | ULJE SUN SUPER MRKVA 100 ml ZA UBRZ. TAMNJ. OLI | 100 ml | 7 | 164 | 79,90–111,90 /l | high/name |  |
| 18 | 5310001166380 | N-ULJE BECUTAN 200ML ZA DJECU-12/1- | 200 ml | 7 | 124 | 18,90–74,75 /l | high/name |  |
| 19 | 3858882214933 | ULJE SUNCOKRET 10L PET ZVIJEZDA (1) | 10 l | 7 | 17 | 1,69–2,06 /l | high/name | vrsta=suncokretovo |
| 20 | 3858892695012 | ULJE ZA SUN. 200 ml OLIVAL SUN SPF 50 | 200 ml | 6 | 81 | 74,95–94,95 /l | high/name | vrsta=suncokretovo |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| ULJE MASLINOVO EXTRA DJEVICANSKO 1 L ZVIJEZDA STAKLO | 22 | `maslin` |
| ULJE MASLINOVO EXTRA DJEVICANSKO 0.5 L ZVIJEZDA STAKLO | 19 | `maslin` |
| ULJE ZA TIJELO ALOA VERA 300ML JOHNSON BABY | 18 | `baby` |
| N-ULJE MASL. 1L ORGULA TRADICIJA EXTRA DJEVIČANSKO -6/1- EKO | 16 | `masl\b` |
| ULJE BUCINO 500 ML ZVIJEZDA STAKLO | 16 | `bucin` |
| RIO MARE TUNA MAS.ULJE 2x80 g OC.MASA 104 g (48) | 12 | `mas\b` |
| RIO MARE TUNA MASL.ULJE 3X80G OC.MASA 156G (32) | 12 | `masl\b` |
| ULJE ZA MASAŽU 200 ml NIVEA BABY | 12 | `baby` |
| JOHNSON BABY ULJE 300ML BEDTIME -12/1- | 11 | `baby` |
| NIVEA SUN ULJE PROTECT&BRONZ SPF 30 200 ml BEIE | 11 | `nivea` |

</details>

<a id="maslinovo_ulje"></a>
## maslinovo ulje (`maslinovo_ulje`)

jedinica: **l** · loose_produce: **false** · grupa: **377** · isključenih grupa: **82**

sinonimi: maslinovo ulje, maslinovo  
must_match: `maslinovo ulje | ulje maslinovo | masl ulje | ulje masl | ekstra devicansko | extra devicansko | extra virgin`
atributi: kvaliteta = ekstra_djevicansko, djevicansko

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3858882211550 | ULJE MASLINOVO EXTRA DJEVICANSKO 1 L ZVIJEZDA STAKLO | 1 l | 22 | 885 | 10,99–21,80 /l | high/name | kvaliteta=ekstra_djevicansko |
| 2 | 3858882211574 | ULJE MASLINOVO EXTRA DJEVICANSKO 0.5 L ZVIJEZDA STAKLO | 500 ml | 19 | 901 | 12,20–20,78 /l | high/name | kvaliteta=ekstra_djevicansko |
| 3 | 3859890446217 | N-ULJE MASL. 1L ORGULA TRADICIJA EXTRA DJEVIČANSKO -6/1- EKO | 1 l | 16 | 869 | 5,99–16,99 /l | high/name | kvaliteta=ekstra_djevicansko |
| 4 | 3859888906051 | ULJE MASLINOVO 1 L BLAGO TRENTON UG. | 1 l | 10 | 563 | 3,98–9,55 /l | high/name |  |
| 5 | 80053835 | ULJE MASLINOVO EXTRA DJEVICANSKO 1 L MONINI STAKLO | 1 l | 9 | 800 | 7,99–15,59 /l | high/name | kvaliteta=ekstra_djevicansko |
| 6 | 3858881192713 | ULJE MASLINOVO EXTRA DJEVICANSKO 750 ML OL ISTRIA | 750 ml | 9 | 600 | 26,59–35,99 /l | high/name | kvaliteta=ekstra_djevicansko |
| 7 | 3859890446200 | N-ULJE MASL. 1L ORGULA HARMONIJA EXTRA DJEVIČANSKO -6/1 EKO | 1 l | 9 | 431 | 6,19–16,19 /l | high/name | kvaliteta=ekstra_djevicansko |
| 8 | 3859890446019 | N-ULJE MASL. 0.75L ORGULA TRADICIJA EXTRA DJEVIČANSKO -6/1- EKO | 750 ml | 9 | 421 | 11,68–14066,67 /l | high/name | kvaliteta=ekstra_djevicansko |
| 9 | 3859890446545 | N-ULJE MASL. 750ML ORGULA ZLATNO EXTRA DJEVIČANSKO -6/1- EKO | 750 ml | 9 | 403 | 13,32–21,05 /l | high/name | kvaliteta=ekstra_djevicansko |
| 10 | 3859890446026 | N-ULJE MASL. 0.25L ORGULA TRADICIJA EXTRA DJEVIČANSKO -12/1- EKO | 250 ml | 9 | 304 | 13,88–66,00 /l | high/name | kvaliteta=ekstra_djevicansko |
| 11 | 3859888295025 | ULJE MASLINOVO EKSTRA DJEVICANSKO 0,75 L PZ MARINA | 750 ml | 8 | 544 | 20,92–24,25 /l | high/name | kvaliteta=ekstra_djevicansko |
| 12 | 3858881192485 | ULJE MASLINOVO EXTRA DJEVICANSKO 0,25 L OL ISTRIA | 250 ml | 8 | 471 | 34,40–46,36 /l | high/name | kvaliteta=ekstra_djevicansko |
| 13 | 3858881192706 | ULJE MASLINOVO EXTRA DJEVICANSKO 0,5 L OL ISTRIA | 500 ml | 8 | 411 | 23,98–39,98 /l | high/name | kvaliteta=ekstra_djevicansko |
| 14 | 3856015327710 | ULJE MASLINOVO EX DJ 0.25L ZVIJEZDA | 250 ml | 8 | 237 | 17,96–24,92 /l | high/name | kvaliteta=ekstra_djevicansko |
| 15 | 8007153005434 | MASLINOVO ULJE EXTRA VERGINE 1 L FARCHIONI STAKLO | 1 l | 7 | 651 | 7,99–13,19 /l | high/name | kvaliteta=ekstra_djevicansko |
| 16 | 3859888295032 | ULJE MASLINOVO EKSTRA DJEVICANSKO 0,5 L PZ MARINA | 500 ml | 7 | 428 | 17,98–28,98 /l | high/name | kvaliteta=djevicansko |
| 17 | 3859888295513 | N-ULJE MASL. 0.25L PZ MARINAEXTRA DJEVIČANSKO -12/1 | 250 ml | 7 | 395 | 16,76–35,80 /l | high/name | kvaliteta=ekstra_djevicansko |
| 18 | 3859890446187 | N-ULJE MASL. 0.5L ORGULA BIO ORGANIC EXTRA DJEVIČANSKO -12/1- EKO | 500 ml | 7 | 253 | 5,30–20,58 /l | high/name | kvaliteta=ekstra_djevicansko |
| 19 | 3859888906037 | ULJE MASLINOVO 1 l EKTRA.DJEV. TRENTON | 1 l | 7 | 240 | 8,49–13,99 /l | high/name | kvaliteta=djevicansko |
| 20 | 3858891566825 | ULJE MASL. 1L ULTRA + EXTRA DJEVIČANSKO -6/1- EKO | 1 l | 7 | 76 | 7,48–14,49 /l | high/name | kvaliteta=ekstra_djevicansko |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| RIB. K. TUNA RIO MARE MASL. ULJE 2 X 80 g ORB | 10 | `tuna` |
| RIO MARE TUNA MASL.ULJE 3X80G OC.MASA 156G (32) | 9 | `tuna` |
| ULJE MASLINOVO S OKUSOM CRNOG TARTUFA 100 ML ZIGANTE | 9 | `okus` |
| ULJE MASLINOVO S OKUSOM CRNOG TARTUFA 60 ML ZIGANTE | 8 | `okus` |
| MASLINOVO ULJE S OKUSOM BIJELOG TARTUFA 60 ML ZIGANTE | 7 | `okus` |
| ULJE MASLINOVO S OKUSOM BIJELOG TARTUFA 100 ML ZIGANTE | 7 | `okus` |
| RIB.K.TUNA 160 g ( 104 g) RIO MARE MASL.ULJE ORBI | 6 | `tuna` |
| TUNA MASLINOVO ULJE RIO MARE 4X80g ORBICO | 6 | `tuna` |
| TUNA FILETI MASL. ULJE AQ 105g/73,5g | 5 | `tuna` |
| TUNA MASLINOVO ULJE 2X160 G RIO MARE | 5 | `tuna` |

</details>

<a id="maslac"></a>
## maslac (`maslac`)

jedinica: **kg** · loose_produce: **false** · grupa: **339** · isključenih grupa: **299**

sinonimi: maslac, puter, butter  
must_match: `maslac | puter\b | butter\b | markenbutter`
atributi: vrsta = slani, neslani

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850108060102 | MASLAC 250 g ZBREGOVLOT:1626022111 | 250 g | 20 | 1355 | 9,96–18,72 /kg | high/name |  |
| 2 | 3850355000999 | N-DUKAT MASLAC 250G I KLASA-20/1- 603 | 250 g | 18 | 1167 | 7,56–17,64 /kg | high/name |  |
| 3 | 3850108060126 | MASLAC 'Z BREGOV 125 G VINDIJA | 125 g | 17 | 694 | 11,12–22,00 /kg | high/name |  |
| 4 | 3850355003969 | Dukat maslac I klase 82% mm 125 g | 125 g | 16 | 680 | 15,12–25,20 /kg | high/name |  |
| 5 | 3850355001521 | MASLAC I KLASA 20g FOLIJA DUKAT (80) | 20 g | 14 | 616 | 19,50–39,50 /kg | high/name |  |
| 6 | 3858888590345 | Zdenka Maslac min.82% m.m. 250g | 250 g | 13 | 687 | 7,40–21,16 /kg | high/name |  |
| 7 | 3858885565612 | PUTER ŠTANGICA 180 g (3X60 g) TVOJIH 5 MINUTA | 180 g | 12 | 639 | 9,94–37,50 /kg | high/name |  |
| 8 | 3850108060157 | MASLAC ZBREGOV 10g VINDIJA (100) | 10 g | 12 | 277 | 30,00–52,00 /kg | high/name |  |
| 9 | 3850108060188 | `z bregov Maslac 82%m.m. 15 g | 15 g | 12 | 119 | 8,67–34,67 /kg | high/name |  |
| 10 | 40349251 | MASLAC SA ZAČINSKIM BILJEM 125g MEGL (8) | 125 g | 11 | 538 | 8,72–36,56 /kg | high/name |  |
| 11 | 4002174000233 | MASLAC 250 G BAYERNLAND STANIC | 250 g | 10 | 497 | 5,96–25,96 /kg | high/name |  |
| 12 | 3155250367094 | PRESIDENT MASLAC S MORSKOM SOLI 250 g DUKAT (12) | 250 g | 9 | 249 | 12,72–18,76 /kg | high/name | vrsta=slani |
| 13 | 8602300205059 | BOMBON BUTTER CANDIE 100g PIONIR | 100 g | 9 | 194 | 9,00–18,50 /kg | high/name |  |
| 14 | 4006496018129 | MASLAC 250 g (82 % m.m.) JAEGER ALPINETTA | 250 g | 7 | 649 | 4,48–11,96 /kg | high/name |  |
| 15 | 5740900400016 | N-MASLAC 200G LURPAK -20/1- | 200 g | 7 | 342 | 9,45–17,95 /kg | high/name |  |
| 16 | 4033854001431 | MASLAC 250 g DEUTSCHE MARKENBUTTER | 250 g | 7 | 192 | 7,08–14,72 /kg | high/name |  |
| 17 | 3228022910023 | MASLAC PRESIDENT 200G -20/1- 51157 | 200 g | 7 | 174 | 16,70–25,75 /kg | high/name |  |
| 18 | 4034900004925 | Meggle Premium maslac 82% m.m. 200 g | 200 g | 6 | 435 | 13,95–22,45 /kg | high/name |  |
| 19 | 40349060 | MASLAC ALPENBUTTER 82% M.M. 20 g MEGGLE | 20 g | 6 | 239 | 10,50–29,50 /kg | high/name |  |
| 20 | 3228022000298 | MASLAC LIGHT - NESLANI 250G PRESIDENT | 250 g | 6 | 196 | 17,16–18,76 /kg | high/name | vrsta=neslani |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| GRICKALICE SMOKICE MASLAC 85G ŠTARK | 17 | `smokic` |
| Margo Namaz miješani s maslacem 225g | 14 | `namaz` |
| KEKSI JAFFA BUTTONS KIKIRIKI MASLAC 95GK | 12 | `kikiriki` |
| KEKSI PETIT BEURE S MASLACEM BEZ GLUTENA 130G BALVITEN | 12 | `keks` |
| KOKICE GOTOVE S OKUSOM MASLACA 100g BOBI | 11 | `kokic` |
| KOKICE ZA MIKROVALNU POP!!! CORN MASLAC 240 g 3X80 g | 10 | `kokic` |
| GEL ZA TUŠIRANJE SHEA BUTTER 250 ml NIVEA | 9 | `shea` |
| KOKICE ZA MIKROV MASLAC 80 g POPCORN | 9 | `kokic` |
| KOKICE ZA MIKROVALNU S MASLACEM 300 g 3X100 g MOGYI | 9 | `kokic` |
| KUKURUZ ZA KOKICE S MASLACEM ZA MIKROVALNU 80G CHIO | 9 | `kokic` |

</details>

<a id="margarin"></a>
## margarin (`margarin`)

jedinica: **kg** · loose_produce: **false** · grupa: **100** · isključenih grupa: **7**

sinonimi: margarin  
must_match: `margarin | margo\b | rama\b`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3856015327284 | MARGARIN MARGO NOVA 225g ZVIJEZDA (16) | 225 g | 23 | 1381 | 4,40–7,96 /kg | high/name |  |
| 2 | 3856015327253 | MARGARIN MARGO NOVA 400g ZVIJEZDA (16) | 400 g | 23 | 1376 | 3,62–7,48 /kg | high/name |  |
| 3 | 3858882210102 | MARGARIN STOLNI SPECIJAL 250G ZVIJEZDA | 250 g | 19 | 1261 | 3,00–5,88 /kg | high/name |  |
| 4 | 3856015301901 | N-MARGARIN ZVIJEZDA 250G 60%MM KLASIK SA SMANJ.UDJELOM MASTI | 250 g | 19 | 1044 | 2,76–5,68 /kg | high/name |  |
| 5 | 3858882211611 | N-MARGARIN ZVIJEZDA 250G ZA KREME AROMA SLATKOG VRHNJA -24/1- | 250 g | 18 | 842 | 3,56–6,36 /kg | high/name |  |
| 6 | 3858882210553 | MARGARIN STOLNI SPECIJAL 500G ZVIJEZDA | 500 g | 17 | 677 | 2,66–5,16 /kg | high/name |  |
| 7 | 3856015325358 | MARGARIN MARGO S JOGURTOM 225g ZVIJEZDA | 225 g | 16 | 576 | 4,00–7,96 /kg | high/name |  |
| 8 | 3856015305534 | N-MARGARIN ZVIJEZDA STOLNI 250G S AROMOM VANILIJE -24/1- | 250 g | 16 | 496 | 1,16–6,36 /kg | high/name |  |
| 9 | 3858883227406 | MARGARINSKI NAMAZ MARGARITA 500 G BAKINA KUHINJA STANIC | 500 g | 15 | 850 | 1,98–6,58 /kg | high/name |  |
| 10 | 3856015332974 | MARGARIN MARGO BUTTERY 400G ZVIJEZDA | 400 g | 14 | 606 | 3,73–7,48 /kg | high/name |  |
| 11 | 3856015325419 | MARGARIN MARGO S MASLACEM 225G ZVIJEZDA | 225 g | 14 | 602 | 6,18–12,40 /kg | high/name |  |
| 12 | 3858882213677 | MARGARIN MARGO CLASSIC 15g ZVIJEZDA (60) | 15 g | 14 | 258 | 22,67–38,00 /kg | high/name |  |
| 13 | 8585037200491 | MARGARIN ZA JELO I KUHANJE 250g FC | 250 g | 12 | 612 | 2,36–4,08 /kg | high/name |  |
| 14 | 8719200264915 | MARGARIN RAMA CLASSIC 225g | 225 g | 12 | 523 | 3,96–9,33 /kg | high/name |  |
| 15 | 8719200265097 | MARGARIN RAMA CLASSIC 400 g STANI | 400 g | 10 | 410 | 4,22–8,73 /kg | high/name |  |
| 16 | 3856015323989 | STOLNI MARGARIN 4x250 g SUPER PONUDA ZVIJEZDA (8) | 1 kg | 10 | 367 | 2,99–4,49 /kg | high/name |  |
| 17 | 8719200265127 | MARGARIN RAMA NAMAZ BUTTERY 400G | 400 g | 8 | 388 | 4,22–7,85 /kg | high/name |  |
| 18 | 3856015325389 | MARGO NATURAL 225g ZVIJEZDA LIGHT | 225 g | 8 | 199 | 3,96–7,07 /kg | high/name |  |
| 19 | 8719200239883 | NAMAZ MARGARINSKI RAMA CLASSIC 225 g | 225 g | 7 | 424 | 4,84–7,96 /kg | high/name |  |
| 20 | 3858883221077 | MARGARINSKI NAMAZ MARGARITA 250 G BAKINA KUHINJA | 250 g | 7 | 235 | 3,96–7,24 /kg | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| MARGARIN ZA KOLAČE I KUHANJE 250 g BAKINA KUHINJ | 12 | `kolac` |
| MARGARIN RAMA ZA KOLAČE 250 g STANI | 10 | `kolac` |
| MARGARIN ZA KOLAČE I KUHANJE 500 g BAKINA KUHINJA | 5 | `kolac` |
| MARGARIN ZA KOLAČE 250G,(40) BAKINA KUHINJA | 3 | `kolac` |
| MARGARIN AIMA ZA KOLAČE 250 gr 60%. | 2 | `kolac` |
| N-MARGARIN RAMA 250G ZA KOLAČE | 2 | `kolac` |
| MARGARIN ZA KOLAČE 500G (20), BAKINA KUHINJA | 1 | `kolac` |

</details>

<a id="mlijeko"></a>
## mlijeko (`mlijeko`)

jedinica: **l** · loose_produce: **false** · grupa: **440** · isključenih grupa: **601**

sinonimi: mlijeko, kravlje mlijeko  
must_match: `mlijek`
atributi: mast = 0.5, 0.9, 1.5, 2.8, 3.2, 3.5, 3.8; vrsta = trajno, svjeze; laktoza = bez

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850108011845 | N-*MLIJEKO Z BREGOV SVJEŽE 3.2%MM 1L 21 DAN 1184 -6/1-PET | 1 l | 23 | 1322 | 1,27–1,95 /l | high/name | vrsta=svjeze, mast=3.2 |
| 2 | 3850354016830 | N-MLIJEKO DUKAT 1.00L 2.8%MM EDGE -12/1- 11214 | 1 l | 23 | 1320 | 0,78–1,03 /l | high/name | vrsta=trajno, mast=2.8 |
| 3 | 3850108020656 | N-MLIJEKO Z BREGOV 2.00L 2.80%MM -6/1- ČEP VINDIJA 2065 | 2 l | 23 | 1298 | 0,81–1,22 /l | high/name | vrsta=trajno, mast=2.8 |
| 4 | 3850108020908 | MLIJEKO ZBREGOV 2.8% MM SA ČEPOM 1L (12), VINDIJA | 1 l | 23 | 1290 | 0,85–1,03 /l | high/name | vrsta=trajno, mast=2.8 |
| 5 | 3850354017103 | MLIJEKO DUKAT 1.00L 1.5%MM EDGE LAGANO JUTRO TRAJNO -12/1 | 1 l | 23 | 1073 | 1,49–2,65 /l | high/name | laktoza=bez, mast=1.5, vrsta=trajno |
| 6 | 3838800040578 | MLIJEKO ALPSKO 3,5% 1 L LJUBLJANSKE MLEKARNE(780/PAL) | 1 l | 22 | 918 | 1,39–2,16 /l | high/name | vrsta=trajno, mast=3.5 |
| 7 | 3850354006053 | MLIJEKO TRAJNO 2.8% MM 1 L DUKAT BOCA ( 6 ) | 1 l | 21 | 1375 | 0,85–1,19 /l | high/name | vrsta=trajno, mast=2.8 |
| 8 | 3850108011760 | N-*MLIJEKO Z BREGOV SVJEŽE 3.2%MM 1.75L 1176 -6/1-PET | 1,75 l | 21 | 1232 | 1,14–1600,00 /l | high/name | mast=3.2, vrsta=svjeze |
| 9 | 3850108023572 | UHT EFEKT MLIJEKO BEZ LAKTOZE 1L SLIM S ČEPOM,VINDIJA | 1 l | 21 | 1222 | 1,39–2,65 /l | high/name | laktoza=bez, vrsta=trajno, mast=2.8 |
| 10 | 3850354000501 | N-MLIJEKO DUKAT 1.00L 3.2%MM SVJEŽE -12/1- 120 | 1 l | 21 | 1022 | 0,89–1,69 /l | high/name | vrsta=svjeze, mast=3.2 |
| 11 | 3850108020557 | MLIJEKO Z BREGOV 2,8% MM 500 ml SLIM TRAJNO VI | 500 ml | 21 | 956 | 1,70–2,78 /l | high/name | vrsta=trajno, mast=2.8 |
| 12 | 3850354006091 | MLIJEKO TRAJNO 3,8%MM 1L HDPE BOCA LACTALIS DUKAT | 1 l | 21 | 890 | 1,31–2,30 /l | high/name | vrsta=trajno, mast=3.8 |
| 13 | 3850108011814 | N-*MLIJEKO Z BREGOV SVJEŽE 3.2%MM 1L 1181 -6/1-PET | 1 l | 20 | 1133 | 1,29–2,02 /l | high/name | vrsta=svjeze, mast=3.2 |
| 14 | 3850354016878 | Dukat trajno mlijeko 2,8% 0,5 l EDGE | 500 ml | 20 | 1047 | 1,36–3,04 /l | high/name | vrsta=trajno, mast=2.8 |
| 15 | 3850354016090 | N-*MLIJEKO DUKAT 1.50L 3.2%MMPET-6/1-SVJEŽE MLIJEKO 10140 | 1,5 l | 20 | 837 | 1,19–1,73 /l | high/name | vrsta=svjeze, mast=3.2 |
| 16 | 3850354006077 | N-MLIJEKO DUKAT 8.00L 2.8%MMTRAJNO 8*1.00L BOCA -1/1- | 8 l | 19 | 749 | 0,75–8,24 /l | high/name | mast=2.8, vrsta=trajno |
| 17 | 3850354017080 | MLIJEKO DUKAT 1.00L 0%MM LAGANO JUTRO TRAJNO -12/1 11219 | 1 l | 19 | 671 | 1,49–2,43 /l | high/name | laktoza=bez, vrsta=trajno |
| 18 | 3850108020922 | N-MLIJEKO Z BREGOV 6*1.00L 2,8%MM UHT TE | 6 l | 18 | 1290 | 0,78–1,12 /l | high/name | vrsta=trajno, mast=2.8 |
| 19 | 3850108021592 | MLIJEKO TRAJNO LIGHT 0,9% mm 1L S ČEPOM TE VINDIJA | 1 l | 18 | 935 | 1,33–2,05 /l | high/name | vrsta=trajno, mast=0.9 |
| 20 | 3850354017042 | MLIJEKO DUKAT 1.00L LAGANO JUTRO 3,8%MM -24/1-TRAJNO EDGE 10214 | 1 l | 18 | 732 | 1,49–2,39 /l | high/name | vrsta=trajno, mast=3.8 |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| DUKAT ČOKOLADNO MLIJEKO 0.5 L EDGE (12) | 22 | `cokolad` |
| MLIJEKO ČOKOLADNO ZBREGOV 2%MM 0.5L SLIM (16), VINDIJA | 20 | `cokolad` |
| ČOKOLADNO MLIJEKO BOCA 0,5L (6) DUKAT | 20 | `cokolad` |
| N-MLIJEKO Z BREGOV 1.00L KOZJE 2.8%MM S ČEPOM UHT -12/1- | 19 | `kozje` |
| MLIJEKO ČOKOLADNO KOKOS 500 ml DUKAT | 18 | `cokolad` |
| N-MLIJEKO DUKAT 1.00L ČOK. -6/1- BOCA | 18 | `cok\b` |
| VAFEL KAKAO I MLIJEKO PRUTICI FRONDI 225 G KRAS | 18 | `kakao` |
| MLIJEKO KOZJE 2,8% MM 500 ml TRAJNO VINDIJA | 17 | `kozje` |
| MLIJEKO ČOKOLADNO 200ML DUKAT (24) | 17 | `cokolad` |
| JUNIOR MLIJEKO ČOKOLADA 0.2L 11234 DUKAT (24) | 16 | `cokolad` |

</details>

<a id="jogurt"></a>
## jogurt (`jogurt`)

jedinica: **kg** · loose_produce: **false** · grupa: **471** · isključenih grupa: **373**

sinonimi: jogurt, tekuci jogurt  
must_match: `jogurt`
atributi: vrsta = grcki, tekuci, cvrsti; mast = 0.1, 0.9, 1.5, 2.8, 3.2

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850354016021 | N-*DUKAT JOGURT 1000G TEKUĆI-6/1- 2.8%MM 32363 | 1 kg | 24 | 1293 | 1,35–3,19 /kg | high/name | mast=2.8, vrsta=tekuci |
| 2 | 3850354010784 | Dukatos grčki tip jogurta 9,7% 450g kant | 450 g | 24 | 1047 | 4,33–7,76 /kg | high/name | vrsta=grcki |
| 3 | 3850108037388 | N-*JOGURT VINDIJA 1000G 2.8%MM 3738 PET -6/1- | 1 kg | 23 | 1286 | 1,75–3,09 /kg | high/name | mast=2.8, vrsta=tekuci |
| 4 | 3850354009764 | JOGURT BADEM PISTACIJA DUKATOS 150 g DUKAT | 150 g | 23 | 1111 | 5,00–8,33 /kg | high/name | vrsta=grcki |
| 5 | 3850108030174 | N-JOGURT VINDIJA 900G 3.2%MM ČVRSTI KANTICA -6/1-3017 | 900 g | 22 | 1073 | 2,28–3,43 /kg | high/name | mast=3.2, vrsta=cvrsti |
| 6 | 3850108037289 | N-JOGURT VINDIJA180G 3.2MM ČVRSTI PET 3728 -20/1- | 180 g | 21 | 1204 | 2,44–3,67 /kg | high/name | mast=3.2, vrsta=cvrsti |
| 7 | 3850354010920 | N-DUKAT JOGURT DUKATOS 150G CRNI RIBIZL/CIMET -6/1- | 150 g | 21 | 897 | 5,00–8,33 /kg | high/name |  |
| 8 | 3850354016007 | N-*DUKAT JOGURT 330G TEKUĆI2.8% MM -8/1- 13356/13714 -12/1- | 330 g | 21 | 660 | 3,00–5,30 /kg | high/name | mast=2.8, vrsta=tekuci |
| 9 | 3850354001133 | JOGURT ČVRSTI 180G 3,2%MM (20) DUKAT | 180 g | 20 | 1188 | 2,44–2,72 /kg | high/name | mast=3.2, vrsta=cvrsti |
| 10 | 3850108030242 | N-JOGURT VILIKIS 150G NATUR3024 GRČKI TIP JOGURTA -12/1 | 150 g | 20 | 1167 | 5,67–9,00 /kg | high/name | vrsta=grcki |
| 11 | 3850354016038 | N-*DUKAT JOGURT 1500G 2,8%MM-6/1- 32364 | 1,5 kg | 20 | 985 | 1,29–2,66 /kg | high/name | mast=2.8, vrsta=tekuci |
| 12 | 3850108037371 | N-*JOGURT VINDIJA 500G 2.8%MM 3737 PET -6/1- | 500 g | 20 | 796 | 2,38–4,18 /kg | high/name | mast=2.8, vrsta=tekuci |
| 13 | 3850108030136 | JOGURT Z BREGOV 2,8% MM 180 g VINDIJ | 180 g | 19 | 911 | 1,94–2,94 /kg | high/name | mast=2.8, vrsta=tekuci |
| 14 | 3850108032505 | N-JOGURT VINDIJA 200G 3250 2,8%MM TTOP -12/1- | 200 g | 19 | 794 | 2,30–3,50 /kg | high/name | mast=2.8, vrsta=tekuci |
| 15 | 3850108037265 | N-*JOGURT VINDIJA 1750G 2.8%MM 3726 PET -6/1- | 1,75 kg | 19 | 763 | 0,68–3,00 /kg | high/name | mast=2.8, vrsta=tekuci |
| 16 | 3850108030020 | N-JOGURT VINDIJA 200G 2.8%MM-20/1- 3002 ČAŠICA | 200 g | 19 | 741 | 2,00–3,20 /kg | high/name | mast=2.8, vrsta=tekuci |
| 17 | 3850354018186 | DUKAT LAGANO JUTRO JOGURT NATUR 330G TT -8/1- | 330 g | 19 | 675 | 3,61–5,73 /kg | high/name | vrsta=tekuci |
| 18 | 3850354000921 | N-DUKAT JOGURT TEKUĆI 180G2,8%MM -20/1- 358 357 | 180 g | 18 | 1226 | 2,44–2,72 /kg | high/name | mast=2.8, vrsta=tekuci |
| 19 | 3850354019121 | DUKAT B.AKTIV JOGURT 1.5%MM 150G -20/1- | 150 g | 18 | 1098 | 3,27–7,93 /kg | high/name | mast=1.5 |
| 20 | 3850354009924 | N-DUKAT JOGURT ČVRSTI 3,2%MM800G MAXI PAKIRANJE KANTICA | 800 g | 18 | 803 | 1,49–3,36 /kg | high/name | mast=3.2, vrsta=cvrsti |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| Dukatos Voćni jogurt SK2 | 21 | `vocn` |
| JOGURT JOGO JAGODA 1KG PET DUKAT (6)* | 19 | `jagod` |
| JOGURT VOĆNI JOGO JAGODA, BRES.Š.V.150 g DUKAT | 18 | `vocn` |
| Dukatos jogurt jagoda 8% mm 150 g | 17 | `jagod` |
| VOCNI JOGURT MARELICA/JAGODA 150 G DUKAT | 17 | `vocn` |
| JOGURT VOĆNI ŠUMSKO VOĆE 1 kg PET DUKAT | 16 | `vocn` |
| DUKATINO VOĆNI JOGURT MIX 125G,(20) DUKAT | 15 | `vocn` |
| B.aktiv LGG jogurt acai š.voće 330 g PET | 14 | `voce` |
| SLADOLED KORNET KING JOGURT-ŠUM.VOĆE 167ml LEDO | 14 | `voce` |
| JOGURT PROTEIN SKYR ISLANDSKI 200G Z'BREGOV VINDIJA | 13 | `protein` |

</details>

<a id="kiselo_vrhnje"></a>
## kiselo vrhnje (`kiselo_vrhnje`)

jedinica: **kg** · loose_produce: **false** · grupa: **130** · isključenih grupa: **20**

sinonimi: kiselo vrhnje, vrhnje kiselo  
must_match: `kiselo vrhnje | vrhnje kiselo | kis vrhnje | vrhnje kis | mileram`
atributi: mast = 12, 20

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850354009863 | Dukat kiselo vrhnje 12% mm 900 g kantica | 900 g | 23 | 684 | 3,28–5,43 /kg | high/name | mast=12 |
| 2 | 3850354009887 | Dukat kiselo vrhnje 20% mm 900 g kantica | 900 g | 22 | 1009 | 3,54–6,10 /kg | high/name | mast=20 |
| 3 | 3850108033106 | N-VRHNJE KISELO VINDIJA 200G20%MM -20/1- 3310 | 200 g | 21 | 1001 | 3,30–9,45 /kg | high/name | mast=20 |
| 4 | 3850354002024 | KISELO VRHNJE 12%MM 200G (20) DUKAT | 200 g | 20 | 1228 | 3,45–5,55 /kg | high/name | mast=12 |
| 5 | 3850108036480 | DOMAĆE KISELO VRHNJE ZA SVJEŽI SIR 25%MM 300G, VINDIJA | 300 g | 20 | 1187 | 3,93–8,17 /kg | high/name |  |
| 6 | 3850108033007 | N-VRHNJE KISELO VINDIJA 200G12%MM -20/1- 3300 | 200 g | 20 | 1172 | 3,95–6,00 /kg | high/name | mast=12 |
| 7 | 3850108036381 | N-VRHNJE KISELO VINDIJA 900G24%MM KANTICA -6/1- | 900 g | 20 | 947 | 4,32–6,88 /kg | high/name |  |
| 8 | 3850354000471 | VRHNJE KISELO 12% 400g BRZO&FIN DUKA | 400 g | 20 | 836 | 2,80–6,73 /kg | high/name | mast=12 |
| 9 | 3850108036442 | N-MILERAM VINDIJA 400G 22% MM VRHNJE KISELO -12/1- 3644 | 400 g | 20 | 833 | 4,98–7,98 /kg | high/name |  |
| 10 | 3850354009900 | KISELO VRHNJE MILERAM 22% 400G DUKAT (6) | 400 g | 19 | 1080 | 4,72–8,23 /kg | high/name |  |
| 11 | 3850354018087 | DUKAT BRZO I FINO BAKINO KISELO VRHNJE 300G (12) | 300 g | 19 | 822 | 4,97–8,63 /kg | high/name |  |
| 12 | 3850108036398 | VRHNJE KISELO MILERAM 22% mm 900 g VINDIJA | 900 g | 19 | 514 | 4,43–6,66 /kg | high/name |  |
| 13 | 3850354002055 | KISELO VRHNJE 20% 200GR (20)DUKAT | 200 g | 18 | 1155 | 4,95–9,45 /kg | high/name | mast=20 |
| 14 | 3850108036473 | N-VRHNJE KISELO VINDIJA 900G12%MM KANTICA -6/1- 3647 | 900 g | 15 | 357 | 4,43–5,77 /kg | high/name | mast=12 |
| 15 | 3850108036411 | KISELO VRHNJE 25% MM 900 g KANTICA VINDIJA | 900 g | 13 | 261 | 3,58–6,99 /kg | high/name |  |
| 16 | 3850354006336 | VRHNJE KISELO 12% 200G 3/1 BRZO&FINO | 600 g | 10 | 423 | 3,98–13,45 /kg | high/name | mast=12 |
| 17 | 3870085020753 | Meggle Vrhnje kiselo 12% mm 180g_OC | 180 g | 7 | 456 | 4,39–5,50 /kg | high/name | mast=12 |
| 18 | 8601500120735 | Moja Kravica Vrhnje kiselo 12%m.m. 750g | 750 g | 6 | 119 | 2,65–3,59 /kg | high/name | mast=12 |
| 19 | 3859892184803 | VRHNJE KISELO 180G 12%MM 3905 DOMAĆA KRAVICA -20/1 | 180 g | 6 | 71 | 3,67–4,72 /kg | high/name | mast=12 |
| 20 | 3850354004134 | BAKINO KISELO VRHNJE 25% 850 G BRZO FINO | 850 g | 5 | 330 | 4,46–5,87 /kg | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| GRICKALICE CLIPSY MAX SOUR CREAM KISELO VRHNJE 25G | 12 | `grickal` |
| ČIPS OD RIŽE VLASAC I KISELO VRHNJE 60 g B. YOND LIVITY | 6 | `vlasac` |
| ČIPS CRUNCHIPS X-CUT KISELO VRHNJE 130 gr | 5 | `cips` |
| ČIPS MAX KISELO VRHNJE 70 g CLIPSY | 5 | `cips` |
| CIPS POMSTICKS KISELO VRHNJE 85 G LORENZ | 4 | `cips` |
| DVOPEK BRUSCHETTE CHEDDAR I KISELO VRHNJE 140g MARETI | 2 | `bruschett` |
| CHIO CIPS LECA S KIS.VRHNJEM 65 G | 1 | `cips` |
| CIPS PRINGLES HOT KISELO VRHNJE 160 G | 1 | `cips` |
| Chio Čips Oven baked kis.vrhnje&luk 100g | 1 | `luk\b` |
| Doritos Čips Tortilja kiselo vrhnje 90g | 1 | `cips` |

</details>

<a id="vrhnje_za_kuhanje"></a>
## vrhnje za kuhanje (`vrhnje_za_kuhanje`)

jedinica: **l** · loose_produce: **false** · grupa: **80** · isključenih grupa: **0**

sinonimi: vrhnje za kuhanje, kuhinjsko vrhnje  
must_match: `vrhnje za kuhanje | vrhnje za kuh | vrh za kuh | kuhinjsko vrhnje | vrhnje kuhanje`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850354017158 | VRHNJE ZA KUHANJE BRZO & FINO 500 g EDGE DUKAT | 500 g | 23 | 1244 | 5,58 /l | high/name |  |
| 2 | 3850354008606 | VRHNJE ZA KUHANJE 20%MM 500G BOCA BRZO&FINO DUKAT | 500 g | 20 | 1075 | 7,58–8,18 /l | high/name |  |
| 3 | 3850108033571 | N-VRHNJE ZA KUH VINDIJA 500ML 20% mm-12/1- | 500 ml | 20 | 1052 | 5,30–8,58 /l | high/name |  |
| 4 | 3850354001232 | VRHNJE ZA KUHANJE 20% 200G DUKAT (24) | 200 g | 19 | 1197 | 4,45–9,25 /kg | high/name |  |
| 5 | 3850108033892 | VRHNJE ZA KUHANJE UHT 0,2L Z'BREGOV VINDIJA | 200 ml | 17 | 1206 | 4,95–8,95 /l | high/name |  |
| 6 | 3850108033472 | VRHNJE ZA KUHANJE BEZ LAKTOZE OSMIJEH 200 ML Z'BREGOV | 200 ml | 16 | 427 | 4,95–9,75 /l | high/name |  |
| 7 | 3850354017257 | BRZO&FINO VRHNJE ZA KUHANJE 1 kg DUKAT (12) 11449 | 1 kg | 15 | 307 | 3,79–6,99 /l | high/name |  |
| 8 | 3850354007975 | VRHNJE ZA KUH 20% BRZO&FINO 3X200G (7) | 600 g | 13 | 648 | 4,32–7,75 /kg | high/name |  |
| 9 | 3850354017172 | BRZO&FINO VRHNJE ZA KUHANJE LAGANO 500G (12) | 500 g | 13 | 632 | 5,28–7,98 /kg | high/name |  |
| 10 | 3850354017295 | VRHNJE ZA KUHANJE LAGANO (bez laktoze) B&F 500g DUKAT | 500 g | 13 | 394 | 8,34 /l | high/name |  |
| 11 | 3850108033588 | VRHNJE ZA KUHANJE 20% MM 200 ml SLIM VINDIJA | 200 ml | 12 | 342 | 4,95–10,45 /l | high/name |  |
| 12 | 3870085021835 | VRHNJE ZA KUHANJE 20 % 0,5L MEGGLE (12) | 500 ml | 9 | 599 | 5,56–7,38 /l | high/name |  |
| 13 | 3850108033489 | Z bregov Vrhnje za kuhanje bez laktoze 20% m.m. 0,2 l | 200 ml | 9 | 204 | 3,45–10,60 /l | high/name |  |
| 14 | 5411188120988 | RIZINO VRHNJE ZA KUHANJE 250 ML ALPRO | 250 ml | 8 | 415 | 6,84–11,96 /l | high/name |  |
| 15 | 3850354012641 | VRHNJE ZA KUHANJE B&F LAGANI 10% 200 g DUKA | 200 g | 8 | 243 | 5,95–8,75 /kg | high/name |  |
| 16 | 3850108033526 | Z`bregov Vrhnje za kuhanje 20% 1L UHT | 1 l | 8 | 175 | 3,98–7,59 /l | high/name |  |
| 17 | 3870085021811 | VRHNJE ZA KUH. 20%mmMEGGLE 200 ml | 200 ml | 6 | 384 | 6,45–9,45 /l | high/name |  |
| 18 | 3850257061203 | VRHNJE ZA KUHANJE 20% 0,5 L KRAVICA KRALJICA | 500 ml | 5 | 246 | 5,58–7,98 /l | high/name |  |
| 19 | 3856003914106 | VRHNJE ZA KUHANJE 10% MM 200 ml NTL DUKA | 200 g | 4 | 408 | 5,25–6,05 /l | high/name |  |
| 20 | 3858883523188 | VRHNJE ZA KUH.200 g DUKAT LOT:02012027 | 200 g | 4 | 75 | 4,90–7,95 /kg | high/name |  |

<a id="slatko_vrhnje"></a>
## slatko vrhnje (`slatko_vrhnje`)

jedinica: **l** · loose_produce: **false** · grupa: **44** · isključenih grupa: **0**

sinonimi: slatko vrhnje, vrhnje za slag  
must_match: `slatko vrhnje | vrhnje slatko | vrhnje za slag | slag vrhnje | vrhnje za tuc`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850354001348 | VRHNJE ZA ŠLAG 33%MM 500G BRZO&FINO DUKAT | 500 g | 20 | 839 | 4,80–10,50 /kg | high/name |  |
| 2 | 3850108033663 | N-VRHNJE ZA ŠLAG VINDIJA 3366 500ML 36%MM UHT SLIM -16/1 -12/1- | 500 ml | 17 | 803 | 6,38–11,70 /l | high/name |  |
| 3 | 3850108033694 | N-VRHNJE ZA ŠLAG VINDIJA 200ML UHT -21/1- | 200 ml | 14 | 700 | 10,95–14,45 /l | high/name |  |
| 4 | 3850354001317 | VRHNJE ZA ŠLAG 33%MM 200g BRZO&FINO DUKAT | 200 g | 13 | 533 | 7,15–15,45 /kg | high/name |  |
| 5 | 3850108033816 | Z bregov vrhnje za šlag 36%mm 0,2L | 200 ml | 8 | 229 | 7,30–17,95 /l | high/name |  |
| 6 | 3850354003236 | VRHNJE ZA ŠLAG NA BILJNOJ BAZI 1L DECORO DUKAT | 1 l | 7 | 33 | 2,52–5,09 /l | high/name |  |
| 7 | 4014500033921 | SLATKO VRHNJE 200 ML ZOTT STANIC | 200 ml | 3 | 182 | 6,65–12,65 /l | high/name |  |
| 8 | 3850108033649 | Vindija Vrhnje za šlag 36% 1 L | 1 l | 3 | 88 | 6,92–8,49 /l | high/name |  |
| 9 | 3858883523171 | VRHNJE ZA ŠLAG 500 g33%MM LOT:16102026 | 500 g | 3 | 68 | 6,70–9,38 /kg | high/name |  |
| 10 | 3838800050270 | MU ALP.VRHNJE ZA ŠLAG 1L | 1 l | 3 | 9 | 6,49 /l | high/name |  |
| 11 | 4036500001212 | VRHNJE SLATKO 30% 200 g OMIRA | 200 g | 2 | 49 | 8,45–10,25 /kg | high/name |  |
| 12 | 8003180908311 | ZAMJENA ZA VRHNJE ZA ŠLAG 500mL | 500 ml | 2 | 36 | 3,80–3,98 /l | high/name |  |
| 13 | 3850354017233 | VRHNJE ZA ŠLAG VANILIJA 500g DUKAT | 500 g | 2 | 3 | 7,56–7,96 /kg | high/ean |  |
| 14 | 4056489317999 | Vrhnje za šlag | 1 kg | 1 | 116 | 4,59 /kg | high/unit |  |
| 15 | lidl:0026724 | Trajno vrhnje za šlag s 30% m.m. | 200 g | 1 | 116 | 5,25–6,75 /kg | high/unit |  |
| 16 | 40894355 | Vrhnje za šlag 36% | 500 g | 1 | 116 | 6,78 /kg | high/unit |  |
| 17 | lidl:0052366 | Vrhnje za šlag bez laktoze | 200 g | 1 | 116 | 7,45 /kg | high/unit |  |
| 18 | 9100000091952 | SLATKO VRHNJE S-BUDGET 0,5 L | 500 ml | 1 | 67 | 6,78 /l | high/name |  |
| 19 | 8017596123169 | VRHNJE ZA ŠLAG 200ml | 200 ml | 1 | 43 | 6,75 /l | high/name |  |
| 20 | 9006207003241 | SVJEŽE VRHNJE ZA ŠLAG 36% m.m.250ml | 250 ml | 1 | 43 | 6,76 /l | high/name |  |

<a id="svjezi_sir"></a>
## svježi sir (`svjezi_sir`)

jedinica: **kg** · loose_produce: **false** · grupa: **191** · isključenih grupa: **51**

sinonimi: svjezi sir, kravlji sir  
must_match: `svjezi sir | sir svjezi | svj sir | sir svj | zrnati sir | sirni namaz svjezi`
atributi: mast = posni, masni

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850355002498 | PRESIDENT ZAGREBAČKI SVJEŽI SIR 375 g DUKAT | 375 g | 24 | 1399 | 6,11–10,53 /kg | high/name |  |
| 2 | 3850355000814 | N-SIR DUKAT PRESIDENT 200G SVJ ZRNATI SIRELA -6/1- | 200 g | 22 | 1196 | 8,95–16,45 /kg | high/name |  |
| 3 | 3850108058352 | SVJEŽI SIR Z BREGOV POLUMASNI 500G, VINDIJA | 500 g | 21 | 1232 | 4,50–6,78 /kg | high/name |  |
| 4 | 3850355005673 | SIR SVJEŽI ZRNATI BEZ LAKTOZE PRESIDENT 200 g DUKAT | 200 g | 21 | 717 | 8,25–15,95 /kg | high/name |  |
| 5 | 3850355002993 | SIR SVJEŽI POSNI PRESIDENT 10 % 200 g DUKAT | 200 g | 20 | 852 | 5,95–10,95 /kg | high/name | mast=posni |
| 6 | 3850108058420 | SIR SVJEŽI U SIRNOJ MARAMI VARAŽDINSKI 800 g VINDIJA | 800 g | 19 | 734 | 4,99–8,56 /kg | high/name |  |
| 7 | 3850355001026 | SIR SVJEŽI POSNI 500g 10%mm PRESIDENT DUKAT | 500 g | 18 | 1047 | 3,58–7,18 /kg | high/name | mast=posni |
| 8 | 3850354015116 | N-DUKAT DUKATINO SVJEŽI SIR SVOĆEM 6*50G -6/1- | 300 g | 18 | 844 | 3,63–12,63 /kg | high/name |  |
| 9 | 3850108058390 | SIR SVJEŽI POSNI PROTEIN 250 gr Z BREGOV VINDI | 250 g | 14 | 411 | 4,76–7,96 /kg | high/name | mast=posni |
| 10 | 4002174080945 | KERNIGER- ZRNATI SVJEŽI SIR 200 g BAYERNLAND | 200 g | 11 | 458 | 6,45–16,45 /kg | high/name |  |
| 11 | 3850108058321 | SIR SVJEŽI POSNI BBL 500g ZBREGOV VINDIJA | 500 g | 11 | 347 | 4,78–7,10 /kg | high/name | mast=posni |
| 12 | 3858888590215 | Zdenka svježi sir 500gr. Posni pl-posuda | 500 g | 7 | 222 | 3,38–7,18 /kg | high/name | mast=posni |
| 13 | 3850261359761 | N-ŠTRUKLI SA SVJ.SIR. SLATKI VINDIJA 600G -12/1- SMRZNUTO | 600 g | 7 | 78 | 6,42–10,07 /kg | high/name |  |
| 14 | 8585002519511 | Meggle Sir svježi zrnati Prot.20%m.m380g | 380 g | 6 | 591 | 6,03–10,24 /kg | high/name |  |
| 15 | 3850108058345 | SIR SVJEŽI POLUMASNI 250 g Z BREGOV VINDIJA | 250 g | 6 | 167 | 2,12–7,80 /kg | high/name |  |
| 16 | 5900531001512 | SIR SVJEŽI ZRNATI 20 % mm 200 g DAIRLY | 200 g | 5 | 585 | 4,95–8,25 /kg | high/name |  |
| 17 | 3858888598679 | SVJEZI SIR SPORT 500 G ZDENKA | 500 g | 5 | 341 | 3,98–6,58 /kg | high/name |  |
| 18 | 3858888590222 | Zdenka svježi sir 500gr. Masni pl-posuda | 500 g | 5 | 265 | 3,98–5,30 /kg | high/name | mast=masni |
| 19 | 3858883522129 | PRESIDENT SVJEŽI SIR POSNI LIGHT 500 g DUKAT | 500 g | 5 | 78 | 4,98–6,38 /kg | high/name | mast=posni |
| 20 | 3859892380090 | N-SIR SVJEŽI POLUMASNI 25%MM500G - 5868 6/1 DOM.KRAV. | 500 g | 5 | 73 | 3,98–4,98 /kg | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| ČIPS ČIPI ČIPS 130G SVJEŽI SIR I MLADI LUK -20/1- CHIO | 15 | `luk\b` |
| PRESIDENT SVJEŽI SIR I VRHNJE 200 g DUKAT | 13 | `vrhnje` |
| SIR SVJEZI ZRNATI VLASAC 200 G PRESIDENT DUKAT | 11 | `vlasac` |
| PRESIDENT KREM SVJEŽI SIR 500 gr DUKAT | 10 | `krem\b` |
| PRESIDENT SVJEŽI SIR I VRHNJE 450 g DUKAT | 10 | `vrhnje` |
| SIR SVJEŽI KREM VIVIS PROTEIN 100 g VINDIJA | 8 | `krem\b` |
| Meggle svježi sir s vrhnjem 450 g | 6 | `vrhnje` |
| SIR SVJEŽI KREM VIVIS 200 g VINDIJA | 6 | `krem\b` |
| DOMAĆE KISELO VRHNJE ZA SVJEŽI SIR 25%MM 300G, VINDIJA | 5 | `vrhnje` |
| SIR SVJEŽI KREM POVRĆE VIVIS 200 g VINDIJA | 5 | `krem\b` |

</details>

<a id="tvrdi_sir"></a>
## tvrdi sir (gauda, trapist, edamac) (`tvrdi_sir`)

jedinica: **kg** · loose_produce: **false** · grupa: **1040** · isključenih grupa: **25**

sinonimi: tvrdi sir, gauda, gouda, trapist, edamac, edamer, polutvrdi sir  
must_match: `gauda | gouda | trapist | edamac | edamer | tvrdi sir | sir tvrdi | polutvrdi | polutv\b | tilzit`
atributi: vrsta = gauda, trapist, edamac, tilzit; oblik = narezani

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850355007080 | N-SIR PRESIDENT GOUDA 150G SLICE-10/1- | 150 g | 20 | 875 | 17,27–26,80 /kg | high/name | oblik=narezani, vrsta=gauda |
| 2 | 3850355007325 | N-SIR PRESIDENT GOUDA 400G -8/1- 15022 15042 - | 400 g | 20 | 789 | 9,73–17,98 /kg | high/name | vrsta=gauda |
| 3 | 3850108053913 | Vindija Tilzit sir rezani 45% mm 150 g | 150 g | 19 | 858 | 17,27–24,60 /kg | high/name | oblik=narezani, vrsta=tilzit |
| 4 | 3850355007301 | SIR PRESIDENT GOUDA 250G -12/1 15021/15041 | 250 g | 19 | 833 | 11,16–18,36 /kg | high/name | vrsta=gauda |
| 5 | 3850108058215 | Vindija Gouda sir rezani 45% mm 150 g | 150 g | 17 | 965 | 16,60–24,60 /kg | high/name | vrsta=gauda, oblik=narezani |
| 6 | 3850108057997 | Vindija Sir Tilzit polutvrdi45%mm 200g | 200 g | 17 | 614 | 14,95–22,50 /kg | high/name | vrsta=tilzit |
| 7 | 3850355007141 | PRESIDENT TILZIT SLICE 150 g (10) DUKAT | 150 g | 17 | 608 | 17,27–26,80 /kg | high/name | oblik=narezani, vrsta=tilzit |
| 8 | 3850108057980 | Vindija Sir Gauda polutvrdi45%mm200g | 200 g | 16 | 555 | 14,95–22,50 /kg | high/name | vrsta=gauda |
| 9 | 3850355007103 | SIR SIRELA PRESIDENT SANDWICH GOUDA 120 g DUKA | 120 g | 16 | 542 | 18,25–29,08 /kg | high/name | vrsta=gauda, oblik=narezani |
| 10 | 3850355007387 | SIR TILZIT 400 G PRESIDENT DUKAT | 400 g | 13 | 539 | 9,73–16,88 /kg | high/name | vrsta=tilzit |
| 11 | 3858888597955 | SIR SPORT TRAPIST 45%MM 400 g 1/5 KOLUTA EGALIZIRANI ZDENKA | 400 g | 13 | 469 | 12,38–25,98 /kg | high/name | vrsta=trapist |
| 12 | 3858888590475 | SIR EDAMAC 400g ZDENKA EGALIZIRANO | 400 g | 12 | 502 | 12,48–17,73 /kg | high/name | vrsta=edamac |
| 13 | 3850355007165 | SIR PRESIDENT TRAPIST 500G GRAND OVAL SIRELA VP. -6/1 | 500 g | 12 | 411 | 11,58–18,78 /kg | high/name | vrsta=trapist |
| 14 | 3859892884390 | SIR TVRDI TRAPIST 200G PAŠKA SIRANA | 200 g | 11 | 571 | 22,45–34,65 /kg | high/name | vrsta=trapist |
| 15 | 3850108057362 | Vindija Sir Trapist varaždin.45%mm 280g | 280 g | 11 | 303 | 14,25–20,32 /kg | high/name | vrsta=trapist |
| 16 | 3858888597740 | SIR ZDENKA EDAMAC 150 g EGALIZIRANI- REZANI ZDEN | 150 g | 10 | 367 | 11,47–25,93 /kg | high/name | vrsta=edamac |
| 17 | 3858888590505 | SIR POLUTV GOUDA 400g ZDENKA | 400 g | 10 | 363 | 12,48–17,63 /kg | high/name | vrsta=gauda |
| 18 | 3850108053906 | SIR TILZIT 2,5 kg | 2,5 kg | 9 | 518 | 4,00–6,48 /kg | high/ean | vrsta=tilzit |
| 19 | 4770299047890 | Džiugas Sir tvrdi 12mj. 40% mm 180 g | 180 g | 9 | 442 | 14,94–22,50 /kg | high/name |  |
| 20 | 3850355002719 | CCA2,7KG GOUDA | 2,7 kg | 8 | 440 | 1,66–2,40 /kg | high/ean | vrsta=gauda |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| SIR TOPLJENI GOUDA 150 G PRESI | 22 | `topljen` |
| N-SIR VINDIJA GOUDA RIBANI 200G -10/1- | 15 | `ribani\b` |
| SIR TVRDI RIBANI 40G DOMAĆA KRAVICA -25/1- ULTRA+ | 3 | `ribani\b` |
| RIBANI EKSTRA TVRDI SIR 40 G VINDIJA | 2 | `ribani\b` |
| SIR TVRDI SNACK MR BOKUNIĆ 100g | 2 | `snack` |
| SNACK GOUDA CUBES MIX DELICAC 100 g | 2 | `snack` |
| SNACK GOUDA CUBES SALAM 100 g DELI Q | 2 | `snack` |
| SNACK GOUDA/CHEDDAR 100 G DELI Q | 2 | `snack` |
| Deli Q Snack Sir gouda&cheddar red 60g | 1 | `snack` |
| Deli Q Snack Sir gouda&pesto gr.red60g | 1 | `snack` |

</details>

<a id="mozzarella"></a>
## mozzarella (`mozzarella`)

jedinica: **kg** · loose_produce: **false** · grupa: **235** · isključenih grupa: **47**

sinonimi: mozzarella, mocarela  
must_match: `mozzarel | mozarel | mocarel`
atributi: oblik = ribana, kuglica

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 8000430133035 | SIR MEKI MOZZARELLA 125g GALBANI DUK (12) | 125 g | 20 | 953 | 7,52–24,72 /kg | high/name |  |
| 2 | 3870085050019 | SIR MEKI MOZZARELLA 125G MEGGLE (20) | 125 g | 12 | 741 | 10,80–19,12 /kg | high/name |  |
| 3 | 8000430132045 | N-SIR MOZZARELLA CUCINA 400G DUKAT GALBANI-5/1 | 400 g | 12 | 514 | 11,98–18,73 /kg | high/name |  |
| 4 | 8595021607786 | SIR MOZZARELLINE BOCCONCINI 200G DUKAT GALBANI-6/1 | 200 g | 12 | 407 | 8,64–20,95 /kg | high/name | oblik=kuglica |
| 5 | 8595021607632 | N-SIR MOZZARELLA GALBANI 2*100G DUO PACK | 200 g | 11 | 372 | 7,45–20,10 /kg | high/name |  |
| 6 | 8595021608363 | N-SIR MOZZARELLA DUKAT PERLINE 150G GALBANI -101- | 150 g | 9 | 355 | 18,60–25,27 /kg | high/name | oblik=kuglica |
| 7 | 4006496029101 | SIR MEKI MINI MOZZARELLA 125 g MEGGL | 125 g | 7 | 391 | 15,12–19,12 /kg | high/name | oblik=kuglica |
| 8 | 8000430132267 | MOZZARELA GALB. 150G MINI LOT:29062024 | 150 g | 5 | 223 | 17,80–26,27 /kg | high/name | oblik=kuglica |
| 9 | 3858888599478 | SIR MOZZARELLA 150 g ZDENKA REZANI | 150 g | 5 | 213 | 13,93–21,93 /kg | high/name |  |
| 10 | 3856003951200 | SIR MOZZARELLA POLUTVRDI MASNI 300G TO JE TO ZDENKA | 300 g | 4 | 346 | 12,00–14,63 /kg | high/name |  |
| 11 | 4006496023468 | SIR MOZZARELLA JAEGER 45 % mm 125 g MONTEVERDI | 125 g | 4 | 330 | 7,92–10,48 /kg | high/name |  |
| 12 | 3856003951194 | SIR MOZZARELLA POLUTVRDI REZANI 100G TO JE TO ZDENKA | 100 g | 4 | 288 | 14,00–16,50 /kg | high/name |  |
| 13 | 4002174066017 | MOZZARELLA 1KG BAYERNLAND LOT:250920 | 1 kg | 4 | 80 | 7,95–14,99 /kg | high/name |  |
| 14 | 4002174088958 | SIR MOZZARELLA 125 g BAYERLAND STANI | 125 g | 4 | 64 | 10,80–21,52 /kg | high/name |  |
| 15 | 5292874000063 | PROIZ BILJ BAZ OKUS MOZZARELLA 250g | 250 g | 3 | 270 | 9,96–10,88 /kg | high/name |  |
| 16 | 3858888599454 | SIR POLUTV MOZZARELLA 300g ZDENKA | 300 g | 3 | 182 | 13,97–18,30 /kg | high/name |  |
| 17 | 4040900117480 | SIR MOZZARELLA 200 g PALADIN | 200 g | 3 | 153 | 17,95–22,55 /kg | high/name |  |
| 18 | 3870128037175 | SIR MOZZARELLA 350 g GERLAND | 350 g | 3 | 150 | 11,97–21,69 /kg | high/name |  |
| 19 | 4008432027110 | SIR MEKI PUNOMASNI MOZZARELLA CAMMINO RIBANI 200 g GOLDSTEIG | 200 g | 3 | 149 | 13,25–16,45 /kg | high/name | oblik=ribana |
| 20 | 4020420112349 | SIR MOZZARELLA ALPINETA 1,5 KG JAGER | 1,5 kg | 2 | 336 | 3,99–5,99 /kg | high/ean |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| N-LEDO PIZZA MOZZARELLA 325G -5/1- | 14 | `pizza` |
| N-VIN.PANIRANA MOZZARELLA 500G SMRZ. -6/1- | 14 | `panir` |
| JUHA KREM RAJČICA/MOZZARELLA 23G FINI MINI PODRAVKA | 9 | `krem\b` |
| Salata svježa sa mozzarella sirom 170g | 7 | `salata` |
| N-PIZZA RISTORANTE MOZZARELLA 355G -7/1- DR.OETKER | 5 | `pizza` |
| JUHA PODR 80G KREM OD RAJČICE S MOZZARELLOM -16/1- | 4 | `krem\b` |
| TRAMEZZINI MOZZARELLA I RAJCICA 140 G PANE AMORE | 3 | `tramezzin` |
| BRUSCHETTE KRAMBALS RAJČICA I MOZZARELLA 70G | 1 | `bruschett` |
| Calzone s rajčicom i mozzarellom | 1 | `mozzarellom` |
| GASTRO SALATA POMADORA MOZARELA | 1 | `salata` |

</details>

<a id="parmezan"></a>
## parmezan (`parmezan`)

jedinica: **kg** · loose_produce: **false** · grupa: **129** · isključenih grupa: **8**

sinonimi: parmezan, parmigiano, grana padano  
must_match: `parmezan | parmigian | grana padano`
atributi: oblik = ribani

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 8000430388367 | SIR GALBANI GRANA PADANO 200g DUKAT | 200 g | 11 | 381 | 23,45–43,45 /kg | high/name |  |
| 2 | 8002226006837 | SIR STA GRANA PADANO 200G-20/1- 086001 | 200 g | 9 | 213 | 25,85–43,95 /kg | high/name |  |
| 3 | 8000430395600 | SIR PARMIGIANO REGGIANO GALBANI 100G -10/1- | 100 g | 8 | 263 | 37,90–49,90 /kg | high/name |  |
| 4 | 8002710412007 | SIR TVRDI GRANA PADANO 200g ZANETTI (25) | 200 g | 7 | 303 | 19,95–32,45 /kg | high/name |  |
| 5 | 8000430393361 | N-SIR GALBANI GRANA PADANO 60G DUKAT -14/1 | 60 g | 7 | 170 | 33,17–44,83 /kg | high/name |  |
| 6 | 5292874000032 | GreenVie parmezan ribani 100 g | 100 g | 4 | 245 | 13,80–17,90 /kg | high/name | oblik=ribani |
| 7 | 8002710410027 | SIR RIBANI GRANA PADANO 50G ZANETTI | 50 g | 4 | 161 | 21,00–33,80 /kg | high/name | oblik=ribani |
| 8 | 8011661000737 | SIR GRANA PADANO PARMA 200 g | 200 g | 3 | 173 | 24,95–34,45 /kg | high/name |  |
| 9 | 8002710402008 | SIR TVRDI 200G PARMIGIANO REGGIANO ZANETTI | 200 g | 3 | 146 | 26,15–44,95 /kg | high/name |  |
| 10 | 8001860257773 | RIŽOT S PARMEZANOM I CARNAROLI RIŽOM 210 g NIKA | 210 g | 3 | 79 | 13,90–14,24 /kg | high/name |  |
| 11 | 8000430395587 | GRANA PADANO 100 G GALBANI DUKAT | 100 g | 3 | 49 | 25,20–34,90 /kg | high/name |  |
| 12 | 9002055002269 | SALAMA S PARMEZANOM 75 g | 75 g | 2 | 204 | 23,87–31,87 /kg | high/name |  |
| 13 | 8004673600125 | SIR GRANA PADANO 200 G LATTERIA SORESINA S.C.A. | 200 g | 2 | 170 | 21,45–25,95 /kg | high/name |  |
| 14 | 8002710420132 | SIR PARMEZAN GRANELLO 80G RIBANI | 80 g | 2 | 157 | 11,13–17,37 /kg | high/name | oblik=ribani |
| 15 | 5051126811525 | RIBEZ ZA PARMEZAN URBAN SHADES |  | 2 | 63 | – | – |  |
| 16 | 8003518100622 | GRANA PADANO GIRA i GRATTA 150g | 150 g | 2 | 40 | 42,07–43,27 /kg | high/name |  |
| 17 | 3858883521177 | PARMEZAN RIBANAC 40 g SIRELA | 40 g | 2 | 19 | 26,50–37,25 /kg | high/name |  |
| 18 | 18000430396376 | SIR GALBANI 60 g GRANA PADANO | 60 g | 2 | 13 | 26,50–36,67 /kg | high/name |  |
| 19 | 8002503211138 | SIR GRANA PADANO 200g LOT:006238 | 200 g | 2 | 5 | 25,00–29,95 /kg | high/name |  |
| 20 | 3850334350756 | SIR TVRDI GRANA PADANO K PLUS 200g | 200 g | 1 | 188 | 19,95–30,95 /kg | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| N-UMAK MUTTI 400G SA PARMEZANOM -6/1- STAKLENKA | 6 | `umak` |
| INZERSDORFER UMAK BOLOGNESE GOVEDINA PARMEZAN 400g | 3 | `umak` |
| GRANA PADANO SNACK 5x20 g AGRIFORM | 2 | `snack` |
| CRVENI UMAK S PARMEZANOM 400G MUTTI | 1 | `umak` |
| KREKERI RIŽINI BUDDY PARMEZAN I ZAČINI 60G | 1 | `kreker` |
| Krem. umak od parmezana i tartufa | 1 | `umak` |
| PROTEIN ČIPS PARMEZAN 60 g RICE UP | 1 | `cips` |
| UMAK PARMIGIANO REGGIANO 180 G RANA PASTIFICIO RANA SPA | 1 | `umak` |

</details>

<a id="jaja"></a>
## jaja (`jaja`)

jedinica: **kom** · loose_produce: **false** · grupa: **542** · isključenih grupa: **931**

sinonimi: jaja, jaje, kokosja jaja  
must_match: `jaja\b | jaje\b`
atributi: velicina = xl, l, m, s; uzgoj = slobodni, podni, bio

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3859889055772 | N-JAJA PERFA AKLASARAZRED M 10KOM -18/1 | 10 kom | 6 | 138 | 0,19–0,28 /kom | high/name | velicina=m |
| 2 | 3859890606178 | JAJA SVJEŽA L 10/1 KOKA TOMCRO (18) |  | 6 | 102 | – | – | velicina=l |
| 3 | 3859889074476 | JAJA SVJEŽA M 10/1 AGROKOKA PULA |  | 5 | 235 | – | – | velicina=m |
| 4 | 3859890606161 | JAJA M RAZRED 10/1 KOKA TOMCRO |  | 5 | 95 | – | – | velicina=m |
| 5 | 3859889055765 | N-JAJA PERFA AKLASARAZRED L 10KOM -18/1 | 10 kom | 5 | 18 | 0,26–0,35 /kom | high/ean | velicina=l |
| 6 | 3857500091703 | JAJA AGROKLASTER M 10/1 SLOBODAN UZGOJ |  | 4 | 230 | – | – | uzgoj=slobodni, velicina=m |
| 7 | 8000500381960 | COKO.JAJE ROCHER 212,5 G FERRERO | 212,5 g | 4 | 164 | 18,78–75,25 /kg | high/name |  |
| 8 | 4008033415101 | ŽLIČICE ZA JAJA 6/1 FACKELMANN | 6 kom | 4 | 138 | 0,27–0,44 /kom | high/ean |  |
| 9 | 3859891082780 | JAJA L 10/1 PODNI UZGO LOT:13.11.2026. |  | 4 | 101 | – | – | uzgoj=podni, velicina=l |
| 10 | 3859891082797 | JAJA M 10/1 PODNI UZGOJ LOT:09 07 2024 |  | 4 | 100 | – | – | velicina=m, uzgoj=podni |
| 11 | 4008033491167 | JAJE ZA CAJ RF |  | 4 | 82 | – | – |  |
| 12 | 3859892582197 | JAJA SVJ M 10/1 SLOBODNI UZGOJ TOMAŽIN |  | 4 | 78 | – | – | uzgoj=slobodni, velicina=m |
| 13 | 3859892208080 | Svježa jaja slobodan uzgoj, klasa L 10/1 |  | 4 | 21 | – | – | velicina=l, uzgoj=slobodni |
| 14 | 3856023036710 | Jaje dekorativno 12 cm 36710 1 kom. | 1 kom | 4 | 6 | 0,55–3,42 /kom | high/ean |  |
| 15 | 3859889611459 | JAJA M RAZRED 18/1 ŽITO | 18 kom | 3 | 289 | 0,15–0,30 /kom | high/ean | velicina=m |
| 16 | 3859889074193 | JAJA SVJEŽA L 10/1 AGROKOKA PULA |  | 3 | 251 | – | – | velicina=l |
| 17 | 3859889057011 | Perfa svježa jaja klasa A razred M | 10 kom | 3 | 219 | 0,22–0,25 /kom | high/unit | velicina=m |
| 18 | 3859890576617 | JAJA L RAZRED 10/1 PODNI UZGOJ GALOV |  | 3 | 201 | – | – | velicina=l, uzgoj=podni |
| 19 | 3859889711579 | Žito Jaja svježa M raz. podni uz.10/1 |  | 3 | 170 | – | – | velicina=m, uzgoj=podni |
| 20 | 3859889711593 | Žito Jaja svježa L raz. podni uzgoj 10/1 |  | 3 | 168 | – | – | uzgoj=podni, velicina=l |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| JAJE ČOKOLADNO KINDER SURPRISE 20G T1x192 | 15 | `cokolad` |
| N-ČOK.JAJE MICKEY MOUSE 20GRATTOUILLE -48/1- | 14 | `cok\b` |
| ČOKOLADNO JAJE HOT WHEELS 20g ZAINI | 12 | `cokolad` |
| N-ČOK.JAJE PRINCES -SHIMMERiSHINE20G -48/1- | 11 | `cok\b` |
| JAJA A KLASA RAZRED M PODNI UZGOJ 10/1 GALA | 9 | `gala\b` |
| N-FERRERO KINDER JOY 20G JAJE IZNENAĐENJA -72/2/1- -24/1- | 8 | `iznenad` |
| N-FERRERO KINDER ČOK JAJE 20G LEI -72/1- | 8 | `cok\b` |
| ČOKOLADNA JAJA PUNJ. ML. ČOK. GIANDUA 120 g DUPIN | 8 | `cokolad` |
| ČOKOLADNA JAJA PUNJENA ASSORTED 120 g DUPIN | 8 | `cokolad` |
| BOJA ZA USKRŠNJA JAJA -ZELENA | 7 | `boja` |

</details>

<a id="luk"></a>
## luk (crveni/žuti) (`luk`)

jedinica: **kg** · loose_produce: **true** · grupa: **195** · isključenih grupa: **50**

sinonimi: luk, crveni luk, zuti luk, kapula  
must_match: `luk\b | kapula`
atributi: vrsta = mladi, crveni, zuti, bijeli

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3859891348275 | LUK CRVENI PAK. 1 kg | 1 kg | 2 | 463 | 0,99–1,45 /kg | high/name | vrsta=crveni |
| 2 | 3858890133004 | LUK CRVENI 1KG EKOZONA | 1 kg | 2 | 206 | 1,49–2,19 /kg | high/name | vrsta=crveni |
| 3 | 3858893252184 | LUK MLADI - VEZICA |  | 2 | 197 | – | – | vrsta=mladi |
| 4 | 3850334173034 | LUK LJUBIČASTI (10) |  | 2 | 192 | 1,01–1,29 /kg | low/unit_price | vrsta=crveni |
| 5 | 3850334386205 | LUK SREBRENAC (10) |  | 2 | 118 | 1,83–1,99 /kg | low/unit_price | vrsta=zuti |
| 6 | 3859891254354 | LUK CRVENI 2kg | 2 kg | 2 | 82 | 0,80–1,00 /kg | high/name | vrsta=crveni |
| 7 | 3859889644051 | LUK CRVENI PAK 1 kg | 1 kg | 2 | 58 | 0,89–0,99 /kg | high/name | vrsta=crveni |
| 8 | 8000523000909 | LUK BORETTANSKI U ACETU 540G CITRES | 540 g | 2 | 5 | 9,24–10,74 /kg | high/name |  |
| 9 | 3857500102126 | LUK ŽUTI PAKIRANI 1KG | 1 kg | 2 | 4 | 1,25–1,29 /kg | high/name | vrsta=zuti |
| 10 | 3859894214188 | *LUK SREBRENAC 4/1 |  | 2 | 4 | – | – | vrsta=zuti |
| 11 | 3859894214133 | LUK CHARLOTTE 500G | 500 g | 2 | 2 | 4,98–5,98 /kg | high/name |  |
| 12 | ntl:001117 | LUK CRVENI SNIŽENJE |  | 1 | 343 | 0,20–0,25 /kg | low/unit_price | vrsta=crveni |
| 13 | ntl:248675 | LUK CRVENI |  | 1 | 343 | 0,49–0,59 /kg | low/unit_price | vrsta=crveni |
| 14 | ntl:248676 | LUK LJUBIČASTI |  | 1 | 343 | 1,09–1,19 /kg | low/unit_price | vrsta=crveni |
| 15 | ntl:001119 | LUK MLADI SNIŽENJE |  | 1 | 343 | 1,60–2,00 /kg | low/unit_price | vrsta=mladi |
| 16 | ntl:246142 | LUK SREBRENAC |  | 1 | 343 | 2,49 /kg | low/unit_price | vrsta=zuti |
| 17 | ntl:248677 | LUK MLADI |  | 1 | 343 | 4,99 /kg | low/unit_price | vrsta=mladi |
| 18 | ntl:001118 | LUK LJUBIČASTI SNIŽENJE |  | 1 | 258 | 0,25–0,40 /kg | low/unit_price | vrsta=crveni |
| 19 | ntl:026665 | LUK CRVENI 2,5 kg SNIŽENJE | 2,5 kg | 1 | 258 | 0,40–0,48 /kg | high/name | vrsta=crveni |
| 20 | ntl:001100 | LUK SREBRENAC SNIŽENJE |  | 1 | 258 | 1,00–1,60 /kg | low/unit_price | vrsta=zuti |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| LUK REZANI 3000G TERMIČKI OBRAĐEN -5/1- VREĆA | 6 | `termick` |
| IGRAČKA LUK I STRIJELA AY32-1A NIRD | 4 | `igrack` |
| LUK CRVENI RUKAVAC 4/1 | 4 | `rukavac` |
| LUK KOCKICE SMRZNUTI 2,5KG LEDO | 4 | `smrz` |
| LUK LJUBIČASTI RUKAVAC 4/1 | 4 | `rukavac` |
| ZAČIN LUK PRŽENI 1000 g KOTANY | 4 | `przeni` |
| LUK DINSTANI 3 kg C.A.K. | 3 | `dinst` |
| CITRES LUK SREDNJI U OCTU 1550 g | 2 | `octu` |
| LUK DINSTANI 2,6KG PODRAVKA | 2 | `dinst` |
| LUK KOCKICE 2.5KG LEDO | 2 | `ledo\b` |

</details>

<a id="cesnjak"></a>
## češnjak (`cesnjak`)

jedinica: **kg** · loose_produce: **true** · grupa: **59** · isključenih grupa: **20**

sinonimi: cesnjak, bijeli luk  
must_match: `cesnjak | cesnjaka`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3830054730205 | ČEŠNJAK SJECKANI U ULJU 1KG MODIMA | 1 kg | 3 | 38 | 5,18–6,69 /kg | high/name |  |
| 2 | 3850334173287 | ČEŠNJAK RFZ (10) |  | 2 | 148 | 3,99–4,34 /kg | low/unit_price |  |
| 3 | 5411361032336 | ČEŠNJAK DS 1kg ARDO | 1 kg | 2 | 3 | 5,49–6,29 /kg | high/ean |  |
| 4 | ntl:001225 | ČEŠNJAK SNIŽENJE |  | 1 | 343 | 1,60–2,00 /kg | low/unit_price |  |
| 5 | ntl:022041 | ČEŠNJAK 250 g SNIŽENJE | 250 g | 1 | 343 | 2,40–2,80 /kg | high/name |  |
| 6 | ntl:024796 | ČEŠNJAK RFS |  | 1 | 342 | 4,99 /kg | low/unit_price |  |
| 7 | plodine:110801 | CESNJAK RINFUZO |  | 1 | 149 | 3,49 /kg | low/unit_price |  |
| 8 | 3858893252634 | Češnjak VH rfs |  | 1 | 144 | 5,49 /kg | low/unit_price |  |
| 9 | gavranovic:098826 | ČEŠNJAK RINF SNIŽENJE |  | 1 | 124 | 2,89–4,19 /kg | low/unit_price |  |
| 10 | gavranovic:107576 | ČEŠNJAK 250g SNIŽENJE | 250 g | 1 | 124 | 4,20–4,76 /kg | high/name |  |
| 11 | gavranovic:071145 | ČEŠNJAK |  | 1 | 124 | 4,59–6,29 /kg | low/unit_price |  |
| 12 | gavranovic:089992 | ČEŠNJAK 250g | 250 g | 1 | 124 | 6,20–7,56 /kg | high/name |  |
| 13 | lidl:0082712 | Češnjak | 250 g | 1 | 116 | 5,56 /kg | high/unit |  |
| 14 | lidl:0084614 | Bio češnjak 150g | 150 g | 1 | 116 | 9,93 /kg | high/name |  |
| 15 | lidl:0082711 | Češnjak domaći 200g | 200 g | 1 | 116 | 9,95 /kg | high/name |  |
| 16 | 3858890139280 | BIO CESNJAK EKOZONA |  | 1 | 116 | – | – |  |
| 17 | 6917986800682 | CESNJAK 500 G | 500 g | 1 | 106 | 4,68–5,30 /kg | high/name |  |
| 18 | tommy:10030072 | ČEŠNJAK MLADI |  | 1 | 73 | 5,49–5,99 /kg | low/unit_price |  |
| 19 | ribola:0112349 | ČEŠNJAK |  | 1 | 61 | 3,99–6,05 /kg | low/unit_price |  |
| 20 | 3859889884129 | Češnjak mrežica 500g | 500 g | 1 | 53 | 7,98 /kg | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| MIRODIJE ČEŠNJAK U GRANULAMA 500g ŠAFRAM | 7 | `granul` |
| ZAČIN ČEŠNJAK U GRANULAMA 920 g KOTANY | 6 | `granul` |
| ČEŠNJAK U GRANULAMA 1kg ALU KOTANYI (10) | 5 | `granul` |
| ZAČIN ČEŠNJAK GRAN.1 kg NADAL | 3 | `zacin` |
| ČEŠNJAK GRANULE 830G NADALINA (10) | 3 | `granul` |
| ČEŠNJAK SJEMENSKI BIJELI 500g | 3 | `sjemensk` |
| ČEŠNJAK SJEMENSKI CRVENI 500g | 3 | `sjemensk` |
| MIRODIJE ČEŠNJAK U GRANULAMA 750G PODRAVKA | 2 | `granul` |
| ČEŠNJAK U GRANULAMA 1000 g HOD | 2 | `granul` |
| PASTA ČEŠNJAK 680g STAKLO | 1 | `pasta` |

</details>

<a id="krumpir"></a>
## krumpir (`krumpir`)

jedinica: **kg** · loose_produce: **true** · grupa: **268** · isključenih grupa: **179**

sinonimi: krumpir, krompir, kumpir  
must_match: `krumpir`
atributi: vrsta = mladi, crveni, zuti, bijeli

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3859893072024 | KRUMPIR LIČKI 2,5 kg AGROVEL. | 2,5 kg | 8 | 377 | 1,20–1,76 /kg | high/name |  |
| 2 | 3859893051111 | KRUMPIR PAK. ZA KUHANJE 2,5 kg | 2,5 kg | 4 | 243 | 0,80–1,40 /kg | high/name |  |
| 3 | 8028772001904 | KRUMPIR GIRO 4 KG OPRAN | 4 kg | 3 | 275 | 1,25–1,65 /kg | high/name |  |
| 4 | 3859893051098 | KRUMPIR PAK. ZA PEČENJE 2,5 kg | 2,5 kg | 3 | 253 | 1,00–1,40 /kg | high/name |  |
| 5 | 3859893051104 | KRUMPIR PAK. ZA SALATU 2,5 kg | 2,5 kg | 2 | 231 | 1,08–1,40 /kg | high/name |  |
| 6 | 8028772002000 | KRUMPIR 2 KG GIRO OPRANI | 2 kg | 2 | 211 | 1,35–1,80 /kg | high/name |  |
| 7 | 3858890133011 | BIO KRUMPIR 1 KG EKOZONA | 1 kg | 2 | 169 | 1,39–2,19 /kg | high/name |  |
| 8 | 3859892278021 | KRUMPIR BIJELI 5 kg NTL | 5 kg | 2 | 130 | 0,62–0,80 /kg | high/ean | vrsta=bijeli |
| 9 | 3871832023782 | KRUMPIRUŠA JAMI 10x90 g | 900 g | 2 | 126 | 4,43 /kg | high/name |  |
| 10 | 3859891254200 | KRUMPIR 3kg ZA PEČENJE | 3 kg | 2 | 82 | 0,59–1,00 /kg | high/name |  |
| 11 | 3859891254194 | KRUMPIR 3kg ZA KUHANJE | 3 kg | 2 | 73 | 0,90–1,00 /kg | high/name |  |
| 12 | 3859891254422 | Krumpir oprani - vrećica 5 kg | 5 kg | 2 | 69 | 0,80–0,90 /kg | high/name |  |
| 13 | 5412873163136 | PEKARSKI KRUMPIR S KOŽOM GIDRAN 2,5kg (4) | 2,5 kg | 2 | 11 | 1,70–1,96 /kg | high/name |  |
| 14 | 3858885876053 | Krumpir mladi rfs |  | 2 | 10 | 0,72–3,45 /kg | low/unit_price | vrsta=mladi |
| 15 | 3859893072031 | LIČKI KRUMPIR 5/1 | 10 kg | 2 | 7 | 0,48–0,99 /kg | high/name |  |
| 16 | ntl:001113 | KRUMPIR MLADI SNIŽENJE |  | 1 | 343 | 0,20–0,34 /kg | low/unit_price | vrsta=mladi |
| 17 | ntl:107669 | KRUMPIR CRVENI SNIŽENJE |  | 1 | 343 | 0,30 /kg | low/unit_price | vrsta=crveni |
| 18 | ntl:001110 | KRUMPIR SNIŽENJE |  | 1 | 343 | 0,30 /kg | low/unit_price |  |
| 19 | ntl:248145 | KRUMPIR |  | 1 | 343 | 0,59–0,89 /kg | low/unit_price |  |
| 20 | ntl:020788 | KRUMPIR CRVENI |  | 1 | 343 | 0,59–0,89 /kg | low/unit_price | vrsta=crveni |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| PEKARSKI KRUMPIR, KRIŠKE S KOROM 2,5 KG LEDO | 9 | `ledo` |
| KRUMPIR PEKARSKI ZAČINJENI 750g LEDO | 8 | `ledo` |
| KRUMPIR KRIŠKE JACKET WEDGES 2500 g ( ZAPRIMATI NA KG ) | 4 | `kriske` |
| KRUMPIR PIRE 3KG VR PODRAVKA (1) | 4 | `pire` |
| KRUMPIROVI KROKETI 2.5KG LEDO | 4 | `ledo` |
| GNJEČILICA KRUMPIRA INOX 26,5X8CM ACER | 3 | `gnjecil` |
| KRUMPIR BATAT 1000 g | 3 | `batat` |
| KRUMPIR PLOŠKE WEDGES 2,5 kg MCCAIN | 3 | `ploske` |
| LEDO KRUMPIR POMMES FRITES 1KG (10) | 3 | `ledo` |
| PIRE KRUMPIR GRANULE 4x1 kg PODRAVKA | 3 | `pire` |

</details>

<a id="rajcica"></a>
## rajčica (svježa) (`rajcica`)

jedinica: **kg** · loose_produce: **true** · grupa: **216** · isključenih grupa: **191**

sinonimi: rajcica, paradajz, pomidor  
must_match: `rajcic | paradajz | pomidor`
atributi: vrsta = cherry, sljiva, grozd

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3859890369059 | RAJČICA HARMONY 500 g TREŠNJAR | 500 g | 7 | 853 | 5,58–9,18 /kg | high/name |  |
| 2 | 3859889267656 | Rajčica koktel grappolo 500g | 500 g | 3 | 228 | 5,38–5,98 /kg | high/name | vrsta=cherry |
| 3 | 8437016787120 | 500G RAJČICA CHERRY PD KL II | 500 g | 3 | 33 | 4,34–7,46 /kg | high/ean | vrsta=cherry |
| 4 | 3850334173416 | RAJČICA GRAPOLO (6) |  | 2 | 197 | 2,49–3,05 /kg | low/unit_price | vrsta=grozd |
| 5 | 3859892668013 | RAJČICA CHERRY 500g STJEMA | 500 g | 2 | 184 | 3,58–4,98 /kg | high/name | vrsta=cherry |
| 6 | 8005110170300 | RAJČICA SJEC.SIT.MUTTI 3X400 g | 1,2 kg | 2 | 30 | 4,53–4,74 /kg | high/name |  |
| 7 | 8437007225402 | RAJČICA CRNA 500 g | 500 g | 2 | 25 | 4,98–6,14 /kg | high/name |  |
| 8 | 3859890369066 | RAJČICA COCTAIL 500g NTL | 500 g | 2 | 6 | 4,06–10,38 /kg | high/name |  |
| 9 | ntl:001125 | RAJČICA GRAPOLO SNIŽENJE |  | 1 | 343 | 0,70–1,40 /kg | low/unit_price | vrsta=grozd |
| 10 | ntl:025493 | PAPRIKA PARADAJZERICA SNIŽENJE |  | 1 | 343 | 1,20 /kg | low/unit_price |  |
| 11 | ntl:001093 | RAJČICA SNIŽENJE |  | 1 | 343 | 1,20–1,40 /kg | low/unit_price |  |
| 12 | ntl:113044 | RAJČICA ŠLJIVARICA SNIŽENJE |  | 1 | 343 | 1,20 /kg | low/unit_price | vrsta=sljiva |
| 13 | ntl:245794 | RAJČICA |  | 1 | 343 | 2,69–2,99 /kg | low/unit_price |  |
| 14 | ntl:248683 | RAJČICA GRAPOLO |  | 1 | 343 | 2,69–2,99 /kg | low/unit_price | vrsta=grozd |
| 15 | ntl:026677 | RAJČICA HARMONY 500 g SNIŽENJE | 500 g | 1 | 343 | 2,80–4,00 /kg | high/name |  |
| 16 | ntl:026673 | RAJČICA CHERRY 250 g SNIŽENJE | 250 g | 1 | 343 | 3,20 /kg | high/name | vrsta=cherry |
| 17 | ntl:022080 | RAJČICA CHERRY 500 g SNIŽENJE | 500 g | 1 | 343 | 3,20–5,40 /kg | high/name | vrsta=cherry |
| 18 | ntl:105021 | RAJČICA CAMPARI 400G SNIŽENJE | 400 g | 1 | 343 | 3,50–5,00 /kg | high/name |  |
| 19 | ntl:112424 | RAJČICA CHERRY 250 G RAJSKA SNIŽENJE | 250 g | 1 | 343 | 5,60–8,00 /kg | high/name | vrsta=cherry |
| 20 | 3613070000428 | RAJČICA CHERRY 500 g | 500 g | 1 | 343 | 7,98 /kg | high/name | vrsta=cherry |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| KONCENTRAT RAJČICE ST. PODRAVKA 720 g (12) | 16 | `koncentr` |
| RAJČICA KONCENTRAT 4500G 28-30% LIM. PODRAVKA | 14 | `koncentr` |
| RAJČICA PASIRANA 3X200G,PODRAVKA (8) (PAL 120) | 14 | `pasir` |
| RAJČICA MUTTI 700G PASIRANA BOCA-12/1- 63070 | 13 | `pasir` |
| RAJČICA PODR 680G PASSATA -12/1- PASIRANA BOCA | 12 | `pasir` |
| N-RAJČICA PODR 500G PASIRANA TETRA BRIK -12/1- | 11 | `pasir` |
| RAJČICA GIANA 680G PASIRANA -12/1- STAKLO | 11 | `pasir` |
| PASIRANA RAJČICA BRIKGIANA 500G 1/12 | 10 | `pasir` |
| PELAT RAJČICA 800 g PODRAVKA OC. MASA 480 g | 8 | `pelat` |
| KONCENTRAT RAJČICE LIM. 850 g PODRAVKA | 7 | `koncentr` |

</details>

<a id="pasirana_rajcica"></a>
## pasirana rajčica (`pasirana_rajcica`)

jedinica: **kg** · loose_produce: **false** · grupa: **158** · isključenih grupa: **6**

sinonimi: pasirana rajcica, passata, rajcica pasirana  
must_match: `pasirana rajcica | rajcica pasirana | pasir rajcica | rajcica pasir | passata | polpa`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850104073656 | RAJČICA PASIRANA 500ML TETRA (12), PODRAVKA (PAL 108) | 500 g | 23 | 1374 | 1,58–2,58 /kg | high/name |  |
| 2 | 3850104213120 | PASIRANA RAJCICA 200 G TETRA BRIK PODRAVKA | 200 g | 19 | 981 | 2,75–5,45 /kg | high/name |  |
| 3 | 80042563 | PASIRANA RAJČICA STAKLO 700g MUTTI | 700 g | 17 | 829 | 2,27–5,41 /kg | high/name |  |
| 4 | 3850104238260 | RAJČICA PASIRANA 3X200G,PODRAVKA (8) (PAL 120) | 600 g | 17 | 751 | 2,87–4,47 /kg | high/name |  |
| 5 | 3850104242915 | RAJČICA PODR 680G PASSATA -12/1- PASIRANA BOCA | 680 g | 14 | 718 | 3,51–4,57 /kg | high/name |  |
| 6 | 8005110630408 | RAJČICA PASIRANA 400 g MUTTI STAKLO | 400 g | 11 | 671 | 3,73–5,98 /kg | high/name |  |
| 7 | 8595241508351 | PASIRANA RAJČICA BRIKGIANA 500G 1/12 | 500 g | 11 | 534 | 0,80–2,18 /kg | high/name |  |
| 8 | 8595241530345 | RAJČICA PASIRANA 680 g STAKLO GIANA | 680 g | 11 | 426 | 2,19–3,37 /kg | high/name |  |
| 9 | 3838945029155 | PASIRANA RAJCICA 500 ML FRUCTAL | 500 ml | 10 | 382 | 1,98–2,18 /kg | high/name |  |
| 10 | 3856020239695 | RAJCICA PASIRIRANA 690 G BIO PODRAVKA | 690 g | 10 | 307 | 3,07–4,86 /kg | high/name |  |
| 11 | 3856020280321 | PASIRANA RAJČICA STAKLO 400g PODRAVKA | 400 g | 8 | 625 | 4,72–5,88 /kg | high/name |  |
| 12 | 8005110004766 | RAJČICA PASIRANA ČEP 500 g MUTTI | 500 g | 7 | 71 | 2,10–2,90 /kg | high/name |  |
| 13 | 3858894142132 | RAJČICA PASIRANA 500 g E BUONO | 500 g | 6 | 501 | 0,98–2,18 /kg | high/name |  |
| 14 | 8033837720720 | Rosso Gargano Rajčica pasirana 690g | 690 g | 6 | 469 | 2,52–4,19 /kg | high/name |  |
| 15 | 3838945042505 | PASIRANA RAJCICA CLASSIC 750 ML FRUCTAL | 750 ml | 6 | 292 | 1,59–3,05 /l | high/name |  |
| 16 | 3838945042512 | PASIRANA RAJCICA PIZZA 750 ML FRUCTAL | 750 ml | 6 | 285 | 1,59–3,05 /l | high/name |  |
| 17 | 8005110860508 | PASIRANA RAJČICA MUTTI 500G TETRAPACK | 500 ml | 6 | 241 | 2,18–3,98 /kg | high/name |  |
| 18 | 8000320990113 | RAJČICA PASIRANA CLIMATE 500G CIRIO BRIK | 500 ml | 6 | 221 | 1,66–2,18 /kg | high/name |  |
| 19 | 8001440002199 | RAJČICA PASIRA.500 ml BRIK VALFRUTTA | 500 ml | 6 | 215 | 2,18 /kg | high/name |  |
| 20 | 8001440132391 | PASIRANA RAJCICA NA PARI 700 ML VALFRUTTA | 700 ml | 6 | 146 | 3,07 /kg | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| PASIRANA RAJČICA S BOSILJKOM BOCA 400G MUTTI | 5 | `bosiljk` |
| MUTTI PASIRANA RAJČICA S BOSILJKOM | 2 | `bosiljk` |
| Mutti Polpa Rajč.sit.sjec.s bosiljk.400g | 2 | `bosiljk` |
| KLC.Rajčica pasir.Rustica s bosiljk 690g | 1 | `bosiljk` |
| RAJČICA PASIR. S BOSILJKOM PETTI 500 ml BOCA PROFUMATO | 1 | `bosiljk` |
| UMAK POLPA DATTERINO 360 g AGROMONTE | 1 | `umak` |

</details>

<a id="koncentrat_rajcice"></a>
## koncentrat rajčice (`koncentrat_rajcice`)

jedinica: **kg** · loose_produce: **false** · grupa: **49** · isključenih grupa: **0**

sinonimi: koncentrat rajcice, pire od rajcice  
must_match: `koncentrat rajcic | rajcica koncentrat | konc rajcic | rajcica konc | dupli konc`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850104053221 | RAJČICA KONCENTRAT TUBA 190G (24), PODRAVKA (PAL 76) | 190 g | 25 | 1403 | 6,95–17,11 /kg | high/name |  |
| 2 | 3850104053214 | RAJČICA KONCENTRAT TUBA 120G (24), PODRAVKA | 120 g | 20 | 748 | 9,67–19,08 /kg | high/name |  |
| 3 | 3850104268533 | RAJČICA KONCENTRAT 300G, PODRAVKA (12) (PAL 48) | 300 g | 18 | 626 | 7,50–13,30 /kg | high/name |  |
| 4 | 3856020269166 | KONCENTRAT RAJCICA 370G STAKLENKA PODRAVKA | 370 g | 18 | 459 | 6,73–10,24 /kg | high/name |  |
| 5 | 3856020269197 | KONCENTRAT RAJČICE ST. PODRAVKA 720 g (12) | 720 g | 18 | 236 | 5,13–130,21 /kg | high/name |  |
| 6 | 3850104073984 | RAJČICA KONCENTRAT 4500G 28-30% LIM. PODRAVKA | 4,5 kg | 15 | 57 | 0,74–6,76 /kg | high/name |  |
| 7 | 3856020269135 | KONCENTRAT RAJČICE STAKLO 210G (12) PODRAVKA | 210 g | 11 | 259 | 8,14–13,38 /kg | high/name |  |
| 8 | 8001440127007 | VALFRUTTA DVOSTRUK.KONC.RAJČICE TUBA 130G (24) | 130 g | 10 | 95 | 2,23–10,15 /kg | high/name |  |
| 9 | 3850104053153 | KONC. RAJČICE 460 g LIM. PODRAVKA (12) | 460 g | 9 | 193 | 3,67–8,85 /kg | high/name |  |
| 10 | 8005110120015 | DVOSTRUKI KONCENTRAT RAJČICE 200 g MUTTI | 200 g | 8 | 215 | 8,95–13,95 /kg | high/name |  |
| 11 | 3850104053177 | KONCENTRAT RAJČICE LIM. 850 g PODRAVKA | 850 g | 8 | 34 | 3,73–7,09 /kg | high/name |  |
| 12 | 80042532 | DUPLI KONCENTRAT RAJCICE 130 G MUTTI | 130 g | 4 | 359 | 10,15–15,00 /kg | high/name |  |
| 13 | 80042518 | KONCENTRAT RAJČICE TROSTRUKI 280g MUTTI | 280 g | 4 | 146 | 12,82–15,32 /kg | high/name |  |
| 14 | 8009755007076 | RAJČICA KONCENTRAT 400g FIAMMA | 400 g | 4 | 140 | 2,97–7,23 /kg | high/name |  |
| 15 | 3850104053146 | KONCENTRAT RAJCICA 260 G LIMENKA PODRAVKA | 260 g | 4 | 98 | 6,31–9,00 /kg | high/name |  |
| 16 | 4007415006111 | RAJČICA KONCENTRAT 4250ML 28-30% MIKADO (PAL 180KOM) | 4,25 l | 4 | 64 | 2,22–2,62 /kg | high/name |  |
| 17 | 3856003945896 | RAJČICA KONCENTRAT 200 g ZORELA | 200 g | 3 | 455 | 6,95–7,95 /kg | high/name |  |
| 18 | 3859890118923 | KONCENTRAT RAJČICE 4500g LARA | 4,5 kg | 3 | 10 | 2,93–4,44 /kg | high/name |  |
| 19 | 3859890236924 | RAJČICA KONCE. 200 g VM2 | 200 g | 2 | 41 | 6,60–7,95 /kg | high/name |  |
| 20 | 4007415006098 | KONC.RAJČICA 850 ml MIKADO | 850 ml | 2 | 11 | 3,35–3,40 /l | high/ean |  |

<a id="mrkva"></a>
## mrkva (`mrkva`)

jedinica: **kg** · loose_produce: **true** · grupa: **125** · isključenih grupa: **43**

sinonimi: mrkva, mrkvu, mrkve  
must_match: `mrkv`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850334021243 | MRKVA PAKIRANA 1kg | 1 kg | 3 | 195 | 1,05–1,61 /kg | high/ean |  |
| 2 | 3859889644105 | MRKVA PAKIRANA 1 kg | 1 kg | 2 | 351 | 1,39–1,49 /kg | high/name |  |
| 3 | 3859889644099 | MRKVA 500 g | 500 g | 2 | 351 | 2,38–2,90 /kg | high/name |  |
| 4 | 3850334173126 | MRKVA (5) |  | 2 | 196 | 0,55–0,85 /kg | low/unit_price |  |
| 5 | 3858885876923 | Mrkva rfs | 5 kg | 2 | 151 | 0,10–1,04 /kg | high/ean |  |
| 6 | 3856028689522 | MRKVA ŽUTA 500 g | 500 g | 2 | 133 | 2,18 /kg | high/name |  |
| 7 | 3859891082063 | MRKVA PAKIRANA 1 kg | 1 kg | 2 | 62 | 1,29–1,61 /kg | high/name |  |
| 8 | 3858885875162 | Mrkva košarica 1kg | 1 kg | 2 | 55 | 1,29–1,79 /kg | high/name |  |
| 9 | 3857500129802 | MRKVA VOĆARNA STUDENCA 1 kg | 1 kg | 2 | 22 | 1,29–1,49 /kg | high/name |  |
| 10 | 3870547029782 | MRKVA NANTES STANDARD |  | 2 | 12 | – | – |  |
| 11 | 3859894093066 | MRKVA 2kg ZEMLJA PORIJEKLA HRVATSKA | 2 kg | 2 | 8 | 1,00–1,15 /kg | high/name |  |
| 12 | 3850104282676 | MRKVA KOCKE LIM. 4.1kg PODRAVKA | 4,1 kg | 2 | 3 | 2,27–2,43 /kg | high/name |  |
| 13 | 5411361008409 | MRKVA 2,5 kg BABY ARDO UG. | 2,5 kg | 2 | 2 | 1,80–2,00 /kg | high/ean |  |
| 14 | 3859891246755 | MRKVA 500 g | 500 g | 2 | 2 | 1,96–1,98 /kg | high/name |  |
| 15 | ntl:001120 | MRKVA SNIŽENJE |  | 1 | 343 | 0,50 /kg | low/unit_price |  |
| 16 | ntl:248678 | MRKVA |  | 1 | 343 | 0,89 /kg | low/unit_price |  |
| 17 | ntl:022074 | MRKVA 500 g SNIŽENJE | 500 g | 1 | 343 | 1,20–1,40 /kg | high/name |  |
| 18 | ntl:010212 | MRKVA 1 kg SNIŽENJE | 1 kg | 1 | 258 | 0,70–0,80 /kg | high/name |  |
| 19 | 3859891082858 | MRKVA PAKIRANA 1 KG | 1 kg | 1 | 155 | 1,29 /kg | high/name |  |
| 20 | 3858889117916 | MRKVA S BUDGET 1 kg | 1 kg | 1 | 144 | 1,29–1,39 /kg | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| SMRZ. MRKVA KOCKA 2,5kg LEDO | 7 | `kocka` |
| GRAŠAK MRKVA KOCKE ZMH HORVAT (2,5kg) | 4 | `grasak` |
| GRAŠAK-MRKVA 2,5KG LEDO | 4 | `grasak` |
| MRKVA BABY UG 2.5 kg 9000199 LEDO | 3 | `ledo` |
| GRAŠAK-MRKVA MIKS SMRZ. 2.5 kg | 2 | `grasak` |
| MRKVA KOCKA 2,5 kg | 2 | `kocka` |
| MRKVA KOCKA 2,5KG FROZY,ZMH | 2 | `kocka` |
| MRKVA KOCKA SMRZNUTA 2,5kg (4) | 2 | `kocka` |
| 2KG MRKVA MIX | 1 | `mix\b` |
| GRAŠAK MRKVA 2,5kg | 1 | `grasak` |

</details>

<a id="paprika"></a>
## paprika (svježa) (`paprika`)

jedinica: **kg** · loose_produce: **true** · grupa: **249** · isključenih grupa: **148**

sinonimi: paprika, babura, svjeza paprika  
must_match: `paprik | babur`
atributi: boja = crvena, zuta, zelena; vrsta = babura, rog, ljuta

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3858885876060 | PAPRIKA BABURA RFZ (10) |  | 4 | 348 | 2,29–2,75 /kg | low/unit_price | vrsta=babura |
| 2 | 3850334079893 | *PAPRIKE TRICO.500 g | 500 g | 4 | 281 | 3,38–6,50 /kg | high/ean |  |
| 3 | 6007788002800 | PAPRIKA PEPPADEW LJUTA CRVENA RINFUZO 3 KG (NETTO 1,2 KG) | 3 kg | 4 | 172 | 5,66–15,83 /kg | high/name | vrsta=ljuta, boja=crvena |
| 4 | 3859892029500 | PAPRIKA MIX |  | 2 | 196 | 5,38–6,38 /kg | low/unit_price |  |
| 5 | 3850334173430 | PAPRIKA CRVENA (5) |  | 2 | 163 | 2,84–5,19 /kg | low/unit_price | boja=crvena |
| 6 | 6007788005641 | PAPRIKA PEPPADEW LJUTA ZUTA RINFUZO 3 KG (NETTO 1,2 KG) | 3 kg | 2 | 163 | 5,66–6,33 /kg | high/name | vrsta=ljuta, boja=zuta |
| 7 | 3850334173164 | PAPRIKA ZELENA (5) |  | 2 | 138 | 2,71–3,99 /kg | low/unit_price | boja=zelena |
| 8 | 3858885877135 | PAPRIKA ROG CRVENA KL II |  | 2 | 16 | 1,89–9,00 /kg | low/unit_price | boja=crvena, vrsta=rog |
| 9 | 3856020289225 | PAPRIKA U SENFU 1,5 kg PODR. | 1,5 kg | 2 | 5 | 10,25–10,33 /kg | high/name |  |
| 10 | 3858881588141 | PAPRIKA LJUTA 1KG NADALINA | 1 kg | 2 | 2 | 11,31–11,94 /kg | high/name | vrsta=ljuta |
| 11 | ntl:001124 | PAPRIKA BABURA SNIŽENJE |  | 1 | 343 | 0,80–1,20 /kg | low/unit_price | vrsta=babura |
| 12 | ntl:025493 | PAPRIKA PARADAJZERICA SNIŽENJE |  | 1 | 343 | 1,20 /kg | low/unit_price |  |
| 13 | ntl:001060 | PAPRIKA ZELENA SNIŽENJE |  | 1 | 343 | 1,40–1,60 /kg | low/unit_price | boja=zelena |
| 14 | ntl:001061 | PAPRIKA CRVENA SNIŽENJE |  | 1 | 343 | 1,60 /kg | low/unit_price | boja=crvena |
| 15 | ntl:105160 | PAPRIKA SEMAFOR CCA 500 G SNIŽENJE |  | 1 | 343 | 1,60–3,60 /kg | low/unit_price |  |
| 16 | ntl:245788 | PAPRIKA ROG CRVENA |  | 1 | 343 | 1,99–2,49 /kg | low/unit_price | vrsta=rog, boja=crvena |
| 17 | ntl:248680 | PAPRIKA BABURA |  | 1 | 343 | 2,29–2,49 /kg | low/unit_price | vrsta=babura |
| 18 | ntl:244179 | PAPRIKA CRVENA |  | 1 | 343 | 3,69–3,99 /kg | low/unit_price | boja=crvena |
| 19 | ntl:111926 | PAPRIKA MIX 300G SNIŽENJE | 300 g | 1 | 343 | 4,67–6,67 /kg | high/name |  |
| 20 | 8033737509999 | PAPRIKA SEMAFOR CCA 500 G |  | 1 | 342 | 5,98 /kg | low/unit_price |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| PAPRIKA CRVENA FILET ST. 660 g OCJ. MASA 300 g PODRAVKA | 10 | `filet` |
| PAPRIKA FILET LIMENKA 4000g ocijeđene mase 2300g PODRAVKA | 10 | `filet` |
| PAPRIKA PEČENA 650 g OCJ. MASA 400 g PODRAV | 10 | `pecen` |
| Šafram paprika zač. mljev. slatka 500 g | 9 | `slatka` |
| PAPRIKA FILE ŽUTA 670G OC.MASA 350G (12) ZVIJEZDA | 8 | `zvijezda` |
| PAPRIKA MLJEVEN SLATKA 1000 g ŠAFRAM | 7 | `mljeven` |
| PAPRIKA REZANA ST. 680 g OCJ. MASA 350 g PODRAVKA | 7 | `rezan` |
| N-PAPRIKA ZVIJEZDA PEČENA 540G (310G OČIŠ.MASE) -12/1- | 6 | `pecen` |
| PAPRIKA FILET ŽUTA 650G VITAM. OC.MASA 360 G (6) | 6 | `filet` |
| PAPRIKA MLJEVENA ZAČINSKA LJUTA 500G, ŠAFRAM | 6 | `mljeven` |

</details>

<a id="krastavac"></a>
## krastavac (svježi) (`krastavac`)

jedinica: **kg** · loose_produce: **true** · grupa: **68** · isključenih grupa: **136**

sinonimi: krastavac, krastavci, svjezi krastavac  
must_match: `krastav`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3858885876077 | KRASTAVAC RFZ (10) |  | 2 | 153 | 1,69–1,89 /kg | low/unit_price |  |
| 2 | 3858886520320 | KRASTAVCI 4 kg MARI UG. | 4 kg | 2 | 4 | 1,61–1,66 /kg | high/name |  |
| 3 | 5319990747365 | KRASTAVCI 4,1kg BONVITA VM2 | 4,1 kg | 2 | 2 | 1,55–2,02 /kg | high/name |  |
| 4 | ntl:001109 | KRASTAVAC SNIŽENJE |  | 1 | 343 | 0,50–0,80 /kg | low/unit_price |  |
| 5 | ntl:248144 | KRASTAVAC |  | 1 | 343 | 1,79–1,89 /kg | low/unit_price |  |
| 6 | 3850334173409 | KRASTAVAC |  | 1 | 184 | 1,89–2,25 /kg | low/unit_price |  |
| 7 | 3857500059284 | KRASTAVAC 3/1 |  | 1 | 155 | – | – |  |
| 8 | 3858889112263 | KRASTAVCI S-BUDGET 6-9 670 g | 670 g | 1 | 144 | 2,07 /kg | high/name |  |
| 9 | 3858889112256 | KRASTAVCI S-BUDGET 3-6 670 g | 670 g | 1 | 143 | 2,91 /kg | high/name |  |
| 10 | 3830070890273 | BIO KRASTAVAC 500G | 500 g | 1 | 139 | 2,98–5,18 /kg | high/name |  |
| 11 | plodine:113101 | KRASTAVAC |  | 1 | 134 | 1,69 /kg | low/unit_price |  |
| 12 | gavranovic:071177 | KRASTAVAC SNIŽENJE |  | 1 | 122 | 1,52–1,62 /kg | low/unit_price |  |
| 13 | gavranovic:071176 | KRASTAVAC |  | 1 | 122 | 2,49–2,59 /kg | low/unit_price |  |
| 14 | lidl:0084535 | Bio krastavac | 1 kom | 1 | 116 | 1,29 /kom | high/unit |  |
| 15 | lidl:0082225 | Krastavac | 1 kg | 1 | 116 | 1,79 /kg | high/unit |  |
| 16 | 4056489008644 | Krastavac 750g | 750 g | 1 | 116 | 2,39–2,92 /kg | high/name |  |
| 17 | 3858889116759 | KRASTAVCI S-BUDGET 6-9 2350 g | 2,35 kg | 1 | 99 | 2,46 /kg | high/name |  |
| 18 | tommy:10058840 | KRASTAVCI SNIŽENO |  | 1 | 87 | 0,85–0,95 /kg | low/unit_price |  |
| 19 | tommy:10000059 | KRASTAVCI |  | 1 | 87 | 1,69–1,89 /kg | low/unit_price |  |
| 20 | 3858892946176 | KRASTAVCI 6-9 cm 680 g DELICATO | 680 g | 1 | 87 | 2,04 /kg | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| KRASTAVCI KLASIK 660 g OCJ. MASA 330 g PODRA | 13 | `masa\b` |
| KRASTAVCI 4000 g OCIJEĐ.MASA 2000 g LIMENKA PODRAVKA | 12 | `masa\b` |
| KRASTAVCI ST. 670 g PODRAVKA (12) OC.MASA 370 g | 12 | `masa\b` |
| N-KRASTAVCI ZVIJEZDA 670G DELIK.1.KLASA -12/1- | 11 | `delik\b` |
| KRASTAVCI ST. 1500 g VEN. PODRAVKA OC.MASA 800 g | 10 | `masa\b` |
| KRASTAVCI ST. 2450 g VEN. PODRAVKA OC.MASA 1300 g | 10 | `masa\b` |
| N-KRASTAVCI ZVIJEZDA 670G(330G)KLASIK DRUGA KLASA | 8 | `zvijezda` |
| KRASTAVCI DELIKA. 680 g OC.MASA 370 g VITAMI. (6) | 5 | `masa\b` |
| KRASTAVCI KIS 2300 g ULTRA | 5 | `kis\b` |
| KRASTAVCI KIS. 680 g II KL. ULTRA | 5 | `kis\b` |

</details>

<a id="tikvica"></a>
## tikvica (`tikvica`)

jedinica: **kg** · loose_produce: **true** · grupa: **53** · isključenih grupa: **9**

sinonimi: tikvica, tikvice  
must_match: `tikvic`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | ntl:001127 | TIKVICA SNIŽENJE |  | 1 | 343 | 0,50–0,80 /kg | low/unit_price |  |
| 2 | ntl:248685 | TIKVICA |  | 1 | 343 | 1,49–1,69 /kg | low/unit_price |  |
| 3 | 3850334173195 | TIKVICE |  | 1 | 188 | 1,69–2,05 /kg | low/unit_price |  |
| 4 | 3857500059277 | TIKVICA 3/1 |  | 1 | 155 | – | – |  |
| 5 | 8057960790139 | TIKVICA ZELENA |  | 1 | 151 | 1,09–1,49 /kg | low/unit_price |  |
| 6 | 3858893251774 | Tikvice rfs |  | 1 | 144 | 1,69–1,79 /kg | low/unit_price |  |
| 7 | 8435320673221 | BIO TIKVICE NATUR PUR 500 g | 500 g | 1 | 142 | 4,58 /kg | high/name |  |
| 8 | 8437007908084 | BIO TIKVICA 500G. | 500 g | 1 | 135 | 3,58 /kg | high/name |  |
| 9 | gavranovic:090404 | TIKVICA SNIŽENJE |  | 1 | 119 | 1,35–3,15 /kg | low/unit_price |  |
| 10 | gavranovic:072061 | TIKVICA |  | 1 | 119 | 2,19–5,39 /kg | low/unit_price |  |
| 11 | lidl:0082345 | Tikvica | 1 kg | 1 | 116 | 1,19–1,69 /kg | high/unit |  |
| 12 | lidl:0084545 | Bio tikvica 500g | 500 g | 1 | 116 | 3,78 /kg | high/name |  |
| 13 | tommy:10006996 | TIKVICE SNIŽENO |  | 1 | 87 | 0,85–0,95 /kg | low/unit_price |  |
| 14 | tommy:10000094 | TIKVICE |  | 1 | 87 | 1,69–1,89 /kg | low/unit_price |  |
| 15 | 8009735185039 | BIO TIKVICE PAKIRANE 500 g | 500 g | 1 | 72 | 5,78–6,78 /kg | high/name |  |
| 16 | 3858890133028 | TIKVICA 500G EKOZONA | 500 g | 1 | 72 | 5,78–6,78 /kg | high/name |  |
| 17 | plodine:111827 | BIO TIKVICA 500G | 500 g | 1 | 69 | 3,44–3,98 /kg | high/name |  |
| 18 | ribola:0109321 | TIKVICA |  | 1 | 61 | 1,69–2,50 /kg | low/unit_price |  |
| 19 | kaufland:09700763 | Tikvica |  | 1 | 53 | 1,69 /kg | low/unit_price |  |
| 20 | 8024581000398 | KBio.Tikvica 500g | 500 g | 1 | 53 | 4,58 /kg | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| SJEME TIKVICA BIJELA | 1 | `sjeme` |
| SJEME TIKVICA BIJELA - BIANCA DA TRIESTE | 1 | `sjeme` |
| SJEME TIKVICA UKRASNA MIX | 1 | `sjeme` |
| SJEME TIKVICA ZELENA | 1 | `sjeme` |
| SJEME TIKVICA ZELENA SAN PASQUALE | 1 | `sjeme` |
| TIKVICA CVIJET - KOM | 1 | `cvijet` |
| TIKVICA UKRASNA MALA | 1 | `ukrasn` |
| TIKVICE PEČENE | 1 | `pecen` |
| TIKVICE PEČENE PORCIJA | 1 | `pecen` |

</details>

<a id="kupus"></a>
## kupus (svježi) (`kupus`)

jedinica: **kg** · loose_produce: **true** · grupa: **120** · isključenih grupa: **133**

sinonimi: kupus, glavica kupusa  
must_match: `kupus`
atributi: vrsta = crveni, bijeli, kineski, mladi

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3858885876169 | KUPUS SVJEŽI (25) |  | 4 | 221 | 0,68–0,79 /kg | low/unit_price | vrsta=bijeli |
| 2 | 3850334173348 | KUPUS CRVENI (25) |  | 2 | 179 | 0,89–1,16 /kg | low/unit_price | vrsta=crveni |
| 3 | 3858885876718 | KUPUS CRVENI - KG |  | 2 | 151 | 0,80–0,99 /kg | low/unit_price | vrsta=crveni |
| 4 | 3850334386168 | KUPUS KINESKI KOM (25) |  | 2 | 110 | 1,69 /kg | low/unit_price | vrsta=kineski |
| 5 | 3858885876152 | KUPUS MLADI SVJEŽI (9) |  | 2 | 16 | 0,49–3,20 /kg | low/unit_price | vrsta=mladi |
| 6 | ntl:001115 | KUPUS CRVENI SNIŽENJE |  | 1 | 343 | 0,50 /kg | low/unit_price | vrsta=crveni |
| 7 | ntl:248543 | KUPUS |  | 1 | 343 | 0,59–0,79 /kg | low/unit_price |  |
| 8 | ntl:248673 | KUPUS CRVENI |  | 1 | 343 | 0,99 /kg | low/unit_price | vrsta=crveni |
| 9 | ntl:001112 | KUPUS SNIŽENJE |  | 1 | 258 | 0,20–0,25 /kg | low/unit_price |  |
| 10 | 3850334173119 | KUPUS SVJEŽI |  | 1 | 188 | 0,79 /kg | low/unit_price |  |
| 11 | 3850334173393 | KUPUS SVJEŽI MLADI |  | 1 | 170 | 1,09 /kg | low/unit_price | vrsta=mladi |
| 12 | ntl:027829 | KUPUS KINESKI |  | 1 | 162 | 2,29 /kg | low/unit_price | vrsta=kineski |
| 13 | plodine:110102 | KUPUS ZELENI |  | 1 | 152 | 0,79 /kg | low/unit_price |  |
| 14 | 3859894356031 | KUPUS KINESKI VH kom |  | 1 | 139 | – | – | vrsta=kineski |
| 15 | gavranovic:106841 | KUPUS MLADI SNIŽENJE |  | 1 | 122 | 0,57–0,84 /kg | low/unit_price | vrsta=mladi |
| 16 | gavranovic:092456 | KUPUS SNIŽENJE |  | 1 | 122 | 0,61–0,83 /kg | low/unit_price |  |
| 17 | gavranovic:071183 | KUPUS |  | 1 | 122 | 0,79–1,39 /kg | low/unit_price |  |
| 18 | 53112132 | KUPUS CRVENI |  | 1 | 122 | 0,79 /kg | low/unit_price | vrsta=crveni |
| 19 | gavranovic:098517 | KUPUS CRVENI SNIŽENJE |  | 1 | 122 | 0,79–1,19 /kg | low/unit_price | vrsta=crveni |
| 20 | gavranovic:071184 | KUPUS MLADI |  | 1 | 122 | 0,89–1,35 /kg | low/unit_price | vrsta=mladi |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| KUPUS KISELI REZANI OGULIN 500g. | 9 | `kisel` |
| KUPUS KISELI REZANI 500g VŽ KISELO ZELJE (20) | 8 | `kisel` |
| KUPUS KISELI MADIG GLAVE ZIP | 5 | `kisel` |
| KUPUS KISELI MIX MADIG ZA SARMU 1 kg NTL | 5 | `kisel` |
| REZAČ KUPUSA S DVA NOŽA 45341 FAC | 5 | `rezac` |
| KUPUS KIS.1/2 REZANI CIBURIPRODUKT | 4 | `kis\b` |
| KUPUS KISELI REZ 500 g (450 g OC.M) AGROVIR | 4 | `kisel` |
| KISELI KUPUS 500G PRIMOŠTENSKI | 3 | `kisel` |
| KISELI KUPUS NATURETA 530 g | 3 | `kisel` |
| KISELI KUPUS REZANI 500G KRAUT | 3 | `kisel` |

</details>

<a id="kiseli_kupus"></a>
## kiseli kupus (`kiseli_kupus`)

jedinica: **kg** · loose_produce: **false** · grupa: **132** · isključenih grupa: **10**

sinonimi: kiseli kupus  
must_match: `kiseli kupus | kupus kiseli | kis kupus | kupus kis | kiselo zelje`
atributi: oblik = glavice, rezani

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3859891093304 | KUPUS KISELI REZANI 500g VŽ KISELO ZELJE (20) | 500 g | 10 | 526 | 1,98–2,90 /kg | high/name | oblik=rezani |
| 2 | 3859891493036 | KUPUS KISELI REZANI OGULIN 500g. | 500 g | 9 | 347 | 1,60–2,62 /kg | high/name | oblik=rezani |
| 3 | 3831029504586 | KUPUS KISELI 530g NATURETA ocijeđene mase 300g | 530 g | 6 | 297 | 3,96–9,30 /kg | high/name |  |
| 4 | 3859891093328 | KUPUS KISELI GLAVICE (RAZNI PROIZVOĐAČI) | 1,5 kg | 6 | 209 | 0,99–1,59 /kg | high/unit | oblik=glavice |
| 5 | 3859891493012 | KUPUS KIS.GLAVE 1kg MADIG | 1 kg | 5 | 220 | 1,34–2,29 /kg | high/ean | oblik=glavice |
| 6 | 3859888562233 | KUPUS KISELI 500 g PZ PRIMOŠTE | 500 g | 5 | 195 | 2,38–3,58 /kg | high/name |  |
| 7 | 3859894109019 | KISELO ZELJE OGULINSKO REZANO 500g | 500 g | 5 | 41 | 1,58–2,98 /kg | high/name | oblik=rezani |
| 8 | 3859889781046 | KUPUS KISELI REZANI 500g CIBURI | 500 g | 4 | 179 | 1,98–4,00 /kg | high/ean | oblik=rezani |
| 9 | 3859890799016 | DOMAĆE KISELO ZELJE REZANO 500G KISKO | 500 g | 4 | 31 | 1,98–2,78 /kg | high/name | oblik=rezani |
| 10 | 3857000000250 | KUPUS KISELI REZ 500 g (450 g OC.M) AGROVIR | 500 g | 4 | 20 | 1,58–2,80 /kg | high/name | oblik=rezani |
| 11 | 3856003911952 | KUPUS KISELI REZANI 500 g ZORELA | 500 g | 3 | 476 | 1,98–2,78 /kg | high/name | oblik=rezani |
| 12 | 3859889040020 | KUPUS KISELI RIBANI 500 g | 1 kg | 3 | 273 | 2,99–3,18 /kg | high/name | oblik=rezani |
| 13 | 3859889040037 | KISELI KUPUS REZANI 500G OGULIN | 500 g | 3 | 270 | 2,38–2,98 /kg | high/ean | oblik=rezani |
| 14 | 3850334091697 | KUPUS KISELI REZANI 500g (20) | 500 g | 3 | 194 | 1,98–2,60 /kg | high/name | oblik=rezani |
| 15 | 3857500050502 | KISELI KUPUS REZANI 500G KRAUT | 500 g | 3 | 169 | 2,38–3,99 /kg | high/name | oblik=rezani |
| 16 | 3859889634021 | KUPUS KISELI REZANI VARAŽDINSKI 500g | 500 g | 3 | 46 | 1,78–2,18 /kg | high/name | oblik=rezani |
| 17 | 3859891493470 | 1KG KUPUS KIS. REZANI U RASOLU | 1 kg | 3 | 33 | 1,69–2,19 /kg | high/name | oblik=rezani |
| 18 | 3859890799030 | DOMAĆE KISELO ZELJE GLAVICE, KISKO |  | 3 | 13 | 2,30–2,43 /kg | low/unit_price | oblik=glavice |
| 19 | 3850334101754 | KUPUS KISELI GLAVE (20) |  | 2 | 190 | 1,99–2,15 /kg | low/unit_price | oblik=glavice |
| 20 | 3859889293037 | KUPUS KIS. 1/1 AGROPROM | 1 kg | 2 | 155 | 1,99–2,39 /kg | high/ean |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| SARMA MIX 1 KG KISELI KUPUS MADIG | 6 | `sarma\b` |
| PREMIUM SALATA KIS.KUPUS S BUC.ULJEM I CESNJAKOM 250 GR | 4 | `premium` |
| PREMIUM SALATA KIS.KUPUS S CES.,PAP.I CRVENOM PAPRIKOM 250GR | 4 | `premium` |
| PREMIUM SALATA KIS.KUPUS S CESNJ. I PAPROM 250 GR | 4 | `premium` |
| PREMIUM SAL. KIS.KUPUS S EX.DJE. MASL. ULJEM I CES. 250G | 3 | `sal\b` |
| MADIG SALATA KISELI KUPUS S BUC.ULJEM I CESNJAKOM 500 GR | 2 | `salata` |
| KIS. KUPUS MIX SARMA 1 KG -AGROPROM | 1 | `sarma\b` |
| KIS. KUPUS MIX SARMA 1KG SPRAJA | 1 | `sarma\b` |
| SALATA KISELI KUPUS | 1 | `salata` |
| SALATA OD KIS.KUPUSA 1 kg TK | 1 | `salata` |

</details>

<a id="zelena_salata"></a>
## zelena salata (`zelena_salata`)

jedinica: **kg** · loose_produce: **true** · grupa: **142** · isključenih grupa: **17**

sinonimi: zelena salata, salata, matovilac, rikola, rukola  
must_match: `zelena salata | salata zelena | ledena salata | salata ledena | kristal salata | matovilac | rikola | rukola | radic | endivij | lollo | puterica | salata glavica`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | ntl:022083 | RUKOLA 100 g SNIŽENJE | 100 g | 1 | 343 | 5,00–6,00 /kg | high/name |  |
| 2 | ntl:104818 | SALATA ENDIVIJA KOM SNIŽENJE |  | 1 | 343 | – | – |  |
| 3 | ntl:110343 | SALATA PUTERICA KOM SNIŽENJE |  | 1 | 343 | – | – |  |
| 4 | ntl:002648 | MATOVILAC 100 g SNIŽENJE | 100 g | 1 | 258 | 6,00–7,00 /kg | high/name |  |
| 5 | ntl:001086 | RADIČ SNIŽENJE |  | 1 | 232 | 1,60 /kg | low/unit_price |  |
| 6 | 3850334386274 | RADIČ KOM |  | 1 | 178 | 8,59 /kg | low/unit_price |  |
| 7 | ntl:245283 | RADIČ |  | 1 | 162 | 4,99 /kg | low/unit_price |  |
| 8 | plodine:111323 | SALATA ENDIVIJA KOMAD |  | 1 | 155 | – | – |  |
| 9 | gavranovic:046982 | MATOVILAC 100g SNIŽENJE | 100 g | 1 | 120 | 12,10–14,70 /kg | high/name |  |
| 10 | gavranovic:158279 | SALATA ENDIVIJA 1 KOM SNIŽENO | 1 kom | 1 | 119 | 1,21–2,31 /kom | high/name |  |
| 11 | gavranovic:158921 | SALATA PUTERICA 1KOM SNIŽENJE | 1 kom | 1 | 119 | 1,37 /kom | high/name |  |
| 12 | gavranovic:158919 | SALATA PUTERICA 1KOM | 1 kom | 1 | 119 | 1,99 /kom | high/name |  |
| 13 | gavranovic:158278 | SALATA ENDIVIJA 1KOM | 1 kom | 1 | 119 | 2,05–3,49 /kom | high/name |  |
| 14 | 3858885877265 | Radič rfs |  | 1 | 119 | 4,99 /kg | low/unit_price |  |
| 15 | gavranovic:110949 | RADIČ - SNIŽENJE |  | 1 | 119 | 5,88 /kg | low/unit_price |  |
| 16 | gavranovic:121668 | RUKOLA 100g SNIŽENJE | 100 g | 1 | 119 | 7,20–13,70 /kg | high/name |  |
| 17 | gavranovic:090298 | RADIČ |  | 1 | 119 | – | – |  |
| 18 | spar:184145 | SALATA ENDIVIJA kom |  | 1 | 119 | – | – |  |
| 19 | lidl:0082041 | Salata endivija | 1 kom | 1 | 116 | 0,99 /kom | high/unit |  |
| 20 | lidl:0082071 | Salata puterica | 1 kom | 1 | 116 | 0,99 /kom | high/unit |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| SJEME ENDIVIJA DJECJA GLAVA | 1 | `sjeme` |
| SJEME ENDIVIJA ESKARIOL ZELENA | 1 | `sjeme` |
| SJEME ENDIVIJA ESKARIOL ZUTA | 1 | `sjeme` |
| SJEME ENDIVIJA KOPICA | 1 | `sjeme` |
| SJEME MATOVILAC | 1 | `sjeme` |
| SJEME MATOVILAC HOLANDSKI | 1 | `sjeme` |
| SJEME MATOVILAC HOLANDSKI | 1 | `sjeme` |
| SJEME MATOVILAC ZLICAR | 1 | `sjeme` |
| SJEME RADIC DIVLJI | 1 | `sjeme` |
| SJEME RADIC GRUMOLO VERDE | 1 | `sjeme` |

</details>

<a id="spinat"></a>
## špinat (`spinat`)

jedinica: **kg** · loose_produce: **true** · grupa: **118** · isključenih grupa: **8**

sinonimi: spinat, blitva  
must_match: `spinat | blitv`
atributi: oblik = smrznuti, baby

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850116053288 | ŠPINAT BRIKET DS 650G LEDO | 650 g | 18 | 692 | 3,43–7,37 /kg | high/name | oblik=smrznuti |
| 2 | 3850116053042 | BLITVA BRIKET 650 g (10) LEDO | 650 g | 18 | 636 | 4,49–7,37 /kg | high/name | oblik=smrznuti |
| 3 | 3850116804590 | BLITVA LIST BRIKET 2.5 kg UGOSTITELJSKI LEDO | 10 kg | 8 | 141 | 0,40–3,42 /kg | high/name | oblik=smrznuti |
| 4 | 5412532129053 | BLITVA LIST 4*2,5 kg FLANDERS BEST ZMH HORVAT | 2,5 kg | 6 | 26 | 0,44–2,76 /kg | high/name | oblik=smrznuti |
| 5 | 3850116850702 | ŠPINAT BRIKET FINO SJECKANI 2.5 KG LEDO | 2,5 kg | 5 | 153 | 1,60–3,49 /kg | high/ean | oblik=smrznuti |
| 6 | 3850116818726 | ŠPINAT LIST BRIKET 2,5 kg LEDO | 2,5 kg | 4 | 35 | 2,28–3,72 /kg | high/name | oblik=smrznuti |
| 7 | 5411361199701 | BLITVA PORCIJE 2,5kg ARDO CAK | 2,5 kg | 3 | 91 | 1,56–2,60 /kg | high/name |  |
| 8 | 3850116880549 | BLITVA BRIKETI 750 g LEDO | 750 g | 3 | 8 | 3,56–4,07 /kg | high/name | oblik=smrznuti |
| 9 | 5411683230441 | ŠPINAT LIST SMRZ. 2,5 kg DELTA | 2,5 kg | 2 | 36 | 1,56–2,00 /kg | high/name | oblik=smrznuti |
| 10 | 3850116037523 | ŠPINAT FINO SJEC.BRIKET 2,5 kg | 2,5 kg | 2 | 21 | 0,74–2,12 /kg | high/name | oblik=smrznuti |
| 11 | 3850116814773 | ŠPINAT BRIKETI 750 g LEDO | 750 g | 2 | 11 | 2,83–3,63 /kg | high/name | oblik=smrznuti |
| 12 | 5412532870054 | ŠPINAT SJECKANI SMRZ 2,5KG (4) | 2,5 kg | 2 | 10 | 1,65–1,96 /kg | high/name | oblik=smrznuti |
| 13 | 3858891042480 | ŠPINAT SJEĆENI 2,5KG FROZY | 2,5 kg | 2 | 3 | 2,30–2,50 /kg | high/name |  |
| 14 | 5412532900058 | ŠPINAT 2,5KG MLJEV. | 2,5 kg | 2 | 2 | 1,30–2,12 /kg | high/name |  |
| 15 | 3858887470228 | BLITVA PORCIJE 2,5KG FLANDERS BEST | 2,5 kg | 2 | 2 | 2,00–2,12 /kg | high/name |  |
| 16 | ntl:022093 | ŠPINAT 400 g SNIŽENJE | 400 g | 1 | 343 | 1,95–3,00 /kg | high/name |  |
| 17 | ntl:001068 | BLITVA SNIŽENJE |  | 1 | 232 | 1,60 /kg | low/unit_price |  |
| 18 | 3850334385925 | BLITVA VEZANA KOM |  | 1 | 187 | 2,58–4,78 /kg | low/unit_price |  |
| 19 | 8015021000108 | SPINAT 500 G | 500 g | 1 | 155 | 3,98 /kg | high/name |  |
| 20 | 3858893251552 | Blitva rfs |  | 1 | 144 | 2,99 /kg | low/unit_price |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| BUREK ŠPINAT I SIR 190G DS PEKAR TOMO | 1 | `burek` |
| BUREK ŠPINAT I SIR peč PT | 1 | `burek` |
| PALACINKE SPINAT FETA SIR 2 X 90 G GASTRO PLODINE | 1 | `sir\b` |
| ROLICA ŠPINAT RICOTTA I FETA SIR 100g | 1 | `sir\b` |
| SAVIJAČA ŠPINAT 600 g MINUTE | 1 | `savijac` |
| SAVIJAČA-ŠPINAT/FETA SIR 125g WOLF | 1 | `savijac` |
| TAGLIATELLE ŠPINAT KM 500G | 1 | `tagliatell` |
| ŠPINAT KREM SPAR 600 g | 1 | `krem\b` |

</details>

<a id="persin"></a>
## peršin (`persin`)

jedinica: **kom** · loose_produce: **true** · grupa: **17** · isključenih grupa: **52**

sinonimi: persin  
must_match: `persin`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3870547029850 | PERŠIN BERLINSKI POLUDUGI STANDARD |  | 2 | 10 | – | – |  |
| 2 | 3870547029867 | PERŠIN LISNATI - DOMAĆI LIŠČAR - STANDARD vrećica |  | 2 | 7 | – | – |  |
| 3 | 3856028690184 | PERŠIN SVJEŽI ZB BIO ZONE |  | 1 | 60 | – | – |  |
| 4 | 3859892705282 | BIO PERŠIN FRANCUSKI U TEGLAMA |  | 1 | 43 | – | – |  |
| 5 | 8001553803041 | PERŠIN |  | 1 | 43 | – | – |  |
| 6 | 3857500129833 | PERŠIN KOR LIS 250 gVOĆARNA STUDENAC |  | 1 | 20 | – | – |  |
| 7 | trgovina-krk:0138451 | PERŠIN ZA GASTRO 1 kg | 1 kg | 1 | 7 | 0,96–51,79 /kg | high/name |  |
| 8 | metro:270250 | FRANCUSKI PERŠIN - KG |  | 1 | 6 | 4,28 /kg | low/unit_price |  |
| 9 | studenac:012313 | PERŠIN SNIŽENI 100 g | 100 g | 1 | 6 | 9,70 /kg | high/name |  |
| 10 | stridon:106192 | PERŠIN KORJEN AGROVIR |  | 1 | 2 | 1,92 /kg | low/unit_price |  |
| 11 | stridon:107948 | PERŠIN FRANCUSKI AGROVIR |  | 1 | 2 | 5,86 /kg | low/unit_price |  |
| 12 | tommy:10023174 | PERŠIN |  | 1 | 1 | 0,20 /kg | low/unit_price |  |
| 13 | trgocentar:4746090 | PERŠIN FRANCUSKI |  | 1 | 1 | 5,15 /kg | low/unit_price |  |
| 14 | ntl:092665 | PERŠIN KORJEN 250 G | 250 g | 1 | 1 | 27,96 /kg | high/name |  |
| 15 | lorenco:2005117 | KORJEN PERŠINA |  | 1 | 1 | – | – |  |
| 16 | lorenco:502 | PERŠIN FRANCUSKI |  | 1 | 1 | – | – |  |
| 17 | 9001414024560 | PERŠIN GASTRO | 100 g | 16 | 224 | 53,52–82,92 /kg | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| 500G PERŠIN KORIJEN | 1 | `korijen` |
| METRO - PERŠIN LIST - KG | 1 | `list\b` |
| PERSIN KORJEN LIST KOM CCA. 250 G | 1 | `list\b` |
| PERSIN LIST | 1 | `list\b` |
| PERSIN LIST 500G. | 1 | `list\b` |
| PERŠIN KOR. LIST. 250 g SNIŽENI | 1 | `list\b` |
| PERŠIN KORIJEN | 1 | `korijen` |
| PERŠIN KORIJEN | 1 | `korijen` |
| PERŠIN KORIJEN | 1 | `korijen` |
| PERŠIN KORIJEN | 1 | `korijen` |

</details>

<a id="gljive"></a>
## gljive (šampinjoni) (`gljive`)

jedinica: **kg** · loose_produce: **true** · grupa: **114** · isključenih grupa: **11**

sinonimi: gljive, sampinjoni, bukovace  
must_match: `sampinjon | gljiv | bukovac`
atributi: vrsta = sampinjoni, bukovace

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3859889614115 | ŠAMPINJONI 500G BEZ KORIJENA(PODLOŽAK) 1150 | 500 g | 7 | 115 | 3,98–6,58 /kg | high/name | vrsta=sampinjoni |
| 2 | 3859889614108 | ŠAMPINJONI SVJ.1000 g FRIDRIH | 1 kg | 4 | 169 | 3,32–4,09 /kg | high/name | vrsta=sampinjoni |
| 3 | 4007415005664 | ŠAMPINJONI REZANI 400/230g (12) | 425 ml | 4 | 13 | 3,76 /kg | high/name | vrsta=sampinjoni |
| 4 | 3850334013576 | GLJIVA ŠAMPINJON 500 grama (8) | 500 g | 3 | 198 | 2,82–4,98 /kg | high/name | vrsta=sampinjoni |
| 5 | 3858891564739 | ŠAMPINJONI REZANI 800G ULTRA | 800 g | 3 | 52 | 2,86–3,98 /kg | high/name | vrsta=sampinjoni |
| 6 | 8594012792326 | ŠAMPINJONI GIANA REZANI 800 g | 800 g | 3 | 26 | 3,24–5,24 /kg | high/name | vrsta=sampinjoni |
| 7 | 4007415005688 | ŠAMPINJONI REZANI U SL.OTOP.800 g AIPK | 850 g | 3 | 12 | 1,16–3,25 /kg | high/name | vrsta=sampinjoni |
| 8 | 3859889614252 | ŠAMPINJONI RFS FRIDRIH |  | 2 | 149 | 2,99–3,95 /kg | low/unit_price | vrsta=sampinjoni |
| 9 | 3859889267007 | ŠAMPINJONI VH 500 g | 500 g | 2 | 145 | 3,78–4,48 /kg | high/name | vrsta=sampinjoni |
| 10 | 3859892060176 | ŠAMPINJONI MIX 500G GEA | 500 g | 2 | 145 | 4,58–4,98 /kg | high/name | vrsta=sampinjoni |
| 11 | 8710609361427 | ŠAMPINJONI REZ. 2,55 kg LIMBUR | 2,55 kg | 2 | 48 | 2,94–4,97 /kg | high/name | vrsta=sampinjoni |
| 12 | 3859889614719 | BUKOVAČE PAK.500g FRIDRIH | 500 g | 2 | 16 | 4,98–5,90 /kg | high/name | vrsta=bukovace |
| 13 | 3859891246014 | GLJIVE SVJ.500 g ZKM | 500 g | 2 | 3 | 4,80–5,28 /kg | high/name | vrsta=sampinjoni |
| 14 | 8032484130135 | ŠAMPINJONI PAKIRANI.500g | 500 g | 2 | 2 | 3,68–4,78 /kg | high/name | vrsta=sampinjoni |
| 15 | ntl:022092 | ŠAMPINJONI 500 g SNIŽENJE | 500 g | 1 | 343 | 2,00–3,20 /kg | high/name | vrsta=sampinjoni |
| 16 | ntl:022091 | ŠAMPINJONI 250 g SNIŽENJE | 250 g | 1 | 343 | 2,80–4,00 /kg | high/name | vrsta=sampinjoni |
| 17 | 3859891581016 | ŠAMPINJONI 500 g | 500 g | 1 | 343 | 4,18–4,38 /kg | high/name | vrsta=sampinjoni |
| 18 | ntl:010192 | BUKOVAČE 250 g SNIŽENJE | 250 g | 1 | 258 | 3,20–4,80 /kg | high/name | vrsta=bukovace |
| 19 | 5907700040082 | SAMPINJONI 500 G BIJELI | 500 g | 1 | 155 | 3,78 /kg | high/name | vrsta=sampinjoni |
| 20 | 3858893060048 | SAMPINJONI SMEDJI 500 G | 500 g | 1 | 144 | 4,38–4,78 /kg | high/name | vrsta=sampinjoni |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| ŠAMPINJONI REZANI 2.55 kg (1) POD.OC.MASA 1330 g | 7 | `masa\b` |
| MJEŠAVINA GLJIVA SA VRGANJIMA MODIMA 2,5 KG | 5 | `mjesav` |
| MJEŠAVINA GLJIVA SMRZ INTER ALFA 2,5kg (4) | 3 | `mjesav` |
| MJEŠAVINA GLJIVA UG LEDO 2.5kg (4) | 2 | `ledo` |
| ŠAMPINJONI ZORELA 800g REZANI- ocjeđena masa 420g | 2 | `masa\b` |
| GLJIVE MJEŠAVINA SPAR 750 g | 1 | `mjesav` |
| GLJIVE ŠUMSKE MJEŠAVINA SMRZ 2,5kg(3) | 1 | `mjesav` |
| JUHA GLJIVE, 1 kg, PODRAVKA | 1 | `juha` |
| Mješavina gljiva SK1 | 1 | `mjesav` |
| Rezani šampinjoni 530 g staklo | 1 | `staklo` |

</details>

<a id="riza"></a>
## riža (`riza`)

jedinica: **kg** · loose_produce: **false** · grupa: **517** · isključenih grupa: **298**

sinonimi: riza  
must_match: `riza\b | rize\b | rizi\b | riso\b | rice\b`
atributi: vrsta = basmati, jasmin, arborio, parboiled, integralna, dugo_zrno, okrugla, sushi

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 8001860100017 | Riso Scotti riža originario okr.zrno 1kg | 1 kg | 21 | 1152 | 2,25–5,40 /kg | high/name | vrsta=arborio |
| 2 | 3838700540369 | RIŽA ZLATO POLJE BLAZINICA PODRAVKA 800 g (9) | 800 g | 17 | 547 | 1,25–4,00 /kg | high/name |  |
| 3 | 8001860201011 | Riso Scotti riža arborio dugo zrno 1kg | 1 kg | 16 | 961 | 2,95–5,99 /kg | high/name | vrsta=arborio |
| 4 | 8001860190520 | Riso Scotti riža oro dugog zrna 1kg | 1 kg | 16 | 802 | 2,25–4,79 /kg | high/name | vrsta=parboiled |
| 5 | 3838700540314 | RIŽA BIJELA 800 g VREĆICA ZLATO POLJE | 800 g | 16 | 747 | 1,94–4,19 /kg | high/name | vrsta=okrugla |
| 6 | 3838700540482 | RIŽA ZL POLJE ST ANDREA 500G KUT (18) | 500 g | 15 | 545 | 3,90–6,78 /kg | high/name |  |
| 7 | 3858890104509 | RIŽA SMEĐA VAKUMIRANA 900 g ENCIAN | 900 g | 15 | 507 | 2,46–7,21 /kg | high/name | vrsta=integralna |
| 8 | 3838700540406 | RIŽA ZL POLJE ST ANDREA 1KG KUT VAK (12) | 1 kg | 13 | 576 | 2,36–5,55 /kg | high/name |  |
| 9 | 8717228380174 | TJESTENINA OD RIŽE RICE VERMICELLI 250G YOUWOK | 250 g | 13 | 551 | 7,60–13,96 /kg | high/name |  |
| 10 | 3838700540604 | RIŽA ARBORIO VAKUMIRANA 1000 g PODRA | 1 kg | 13 | 489 | 2,36–6,99 /kg | high/name | vrsta=arborio |
| 11 | 8001420001594 | RIŽA GALLO ORIGINARIO 1KG -12/1- 1151 | 1 kg | 11 | 611 | 3,19–5,29 /kg | high/name | vrsta=arborio |
| 12 | 3838700540383 | RIŽA PARBOILED DZ ZLATO POLJE 800G (12) | 800 g | 11 | 579 | 2,61–4,90 /kg | high/name | vrsta=parboiled |
| 13 | 3859888279445 | RIZA RIO PAK DUGO ZRNO 1 KG PVC | 1 kg | 11 | 463 | 1,19–33,75 /kg | high/name | vrsta=dugo_zrno |
| 14 | 5010338303273 | JAP SUSHI RIŽA 500G BLUE -10/1- DRAGON | 500 g | 11 | 262 | 3,00–10,90 /kg | high/name | vrsta=sushi |
| 15 | 8001860010019 | RIŽA SCOTTI 1 kg CARNAROLI NKAS | 1 kg | 11 | 229 | 4,99–119,75 /kg | high/name | vrsta=arborio |
| 16 | 3859888163676 | RIŽA I KLASA 950 g ŠAFRAM (24) | 950 g | 11 | 121 | 2,09–3,15 /kg | high/name | vrsta=dugo_zrno |
| 17 | 8001420002911 | RIŽA GALLO ARBORIO D.ZRNO 1 kg | 1 kg | 10 | 481 | 2,29–5,75 /kg | high/name | vrsta=arborio |
| 18 | 8001420003666 | RIZA BLOND RISOTTI 1 KG RISO GALLO | 1 kg | 9 | 641 | 2,89–5,29 /kg | high/name |  |
| 19 | 8001420000788 | RIŽA INTEGRO DUGO ZRNO PARB. 1KG KK RISOGALLO | 1 kg | 9 | 562 | 2,99–5,75 /kg | high/name | vrsta=integralna |
| 20 | 5060194790069 | RIZA ZA SUSHI 500 G SAITAKU | 500 g | 9 | 274 | 2,00–9,28 /kg | high/name | vrsta=sushi |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| COKOLADA MLIJECNA COKOLADA RIZA 26 G DORINA | 19 | `cokolad` |
| RIŽA ZA DOMAĆA JELA ZLATO POLJE PODRAVKA 1 kg (12) | 19 | `jela\b` |
| ČOKOLADA DORINA RIŽA 220 g KRAŠ | 15 | `cokolad` |
| KREKER OD RIZE SA SJEMENKAMA 100 G B.YOND-LIVITY | 13 | `kreker` |
| RIŽA DUGO ZRNO PARBOILED 500G VREĆICA UNCLE BEN'S | 13 | `ben\b` |
| ČIPS OD RIŽE SIR CHEDDAR I CHUTNEY 60 g B. YOND LIVITY | 13 | `cips` |
| KREKER OD RIŽE SA SEZAMOM BEZ GLUTENA 100 g (12) | 12 | `kreker` |
| MIKADO ČOKOLADA RIŽA 75G, (12)ZVEČEVO | 12 | `cokolad` |
| NAPITAK OD RIŽE ORIGINAL ALPRO 1 L ENCIAN | 12 | `napitak` |
| NATUREL KRE. BEZ GLU. RICE SNACK CLA. 100 g (12) | 12 | `snack` |

</details>

<a id="tjestenina"></a>
## tjestenina (`tjestenina`)

jedinica: **kg** · loose_produce: **false** · grupa: **1543** · isključenih grupa: **308**

sinonimi: tjestenina, pasta, spageti, penne, fusilli, makaroni  
must_match: `tjestenin | spaget | spaghett | penne | fusill | makaron | tagliatell | farfalle | rigatoni | linguine | tortiglioni | puzic | svrdl | mascice | leptiric | pipe rigate | sedanini | tjest\b`
atributi: oblik = spageti, penne, fusilli, makaroni, tagliatelle, farfalle, puzici; vrsta = integralna, bez_glutena, s_jajima

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 8076802085738 | BARILLA PENNE RIGATE 73 (MAKARON) TJESTENINA 500G (30) | 500 g | 23 | 1384 | 2,38–4,78 /kg | high/name | oblik=penne |
| 2 | 8076802085981 | BARILLA FUSSILI 98 (VIJAK) TJESTENINA 500G (30) | 500 g | 22 | 1398 | 1,90–5,02 /kg | high/name | oblik=fusilli |
| 3 | 8076800195057 | TJESTENINA SPAGHETTI 5 500 G BARILLA KUTIJA | 500 g | 21 | 1398 | 2,12–4,12 /kg | high/name | oblik=spageti |
| 4 | 3859888666399 | TJEST MARODI SPAGHETTI n.5 400G -24/1- | 400 g | 21 | 759 | 2,47–5,63 /kg | high/name | oblik=spageti |
| 5 | 3859888666061 | TJEST MARODI CHIFFERI RIGATI / PUŽIĆI SREDNJI 400G-12/1 | 400 g | 21 | 727 | 2,47–5,98 /kg | high/name | oblik=puzici |
| 6 | 3859888666382 | MARODI PENNE RIGATE 400G,(12) (PAL 56) | 400 g | 21 | 609 | 2,47–5,63 /kg | high/name | oblik=penne |
| 7 | 3859888666085 | MARODI TJESTENINA SVRDLA 400G (10) (PAL 50) | 400 g | 20 | 1104 | 2,47–5,63 /kg | high/name | oblik=fusilli |
| 8 | 8076800195033 | N-TJEST BARILLA 3 500G -24/1-U-1324 SPAGHETTI VERMICELLI | 500 g | 18 | 931 | 2,18–4,68 /kg | high/name | oblik=spageti |
| 9 | 8076809529419 | TJESTENINA INTEGRALNA SPAGHETTI 5 500 G BARILLA KUTIJA | 500 g | 18 | 816 | 3,98–7,02 /kg | high/name | vrsta=integralna, oblik=spageti |
| 10 | 8076802085912 | BARILLA PIPE RIGATE 91 (PUŽIĆ) TJESTENINA 500G | 500 g | 17 | 814 | 2,36–5,12 /kg | high/name | oblik=puzici |
| 11 | 8076809523721 | TJESTENINA TAGLIATELLE SA SPINATOM 500 G BARILLA KUTIJA | 500 g | 17 | 698 | 5,86–9,32 /kg | high/name | oblik=tagliatelle |
| 12 | 8076800195132 | TJESTENINA BAVETTE LINGUINE 13 500g BARILLA | 500 g | 17 | 649 | 2,18–4,98 /kg | high/name |  |
| 13 | 8076809529457 | TJESTENINA INTEGRALNA FUSILLI 500 G BARILLA KUTIJA | 500 g | 16 | 740 | 3,98–7,60 /kg | high/name | vrsta=integralna, oblik=fusilli |
| 14 | 8076809580144 | BARILLA FARFALLE 65 (LEPTIRIĆI) TJESTENINA 500G (12) AWT | 500 g | 16 | 723 | 2,70–6,88 /kg | high/name | oblik=farfalle |
| 15 | 8076809545457 | TIJESTO PENNE RIGATE GLUTEN FREE BARILLA 400G (14) | 400 g | 16 | 677 | 8,73–219,38 /kg | high/name | oblik=penne, vrsta=bez_glutena |
| 16 | 8076800105988 | TJESTENINA FUSILLI 98 1 KG BARILLA KUTIJA | 1 kg | 15 | 865 | 1,84–4,62 /kg | high/name | oblik=fusilli |
| 17 | 8076800105056 | TJESTENINA SPAGHETTI 5 1 KG BARILLA KUTIJA | 1 kg | 15 | 754 | 1,85–4,21 /kg | high/name | oblik=spageti |
| 18 | 8076809545440 | TIJESTO SPAGHETTI GLUTEN FREE 400G BARILLA (12) | 400 g | 15 | 693 | 6,73–219,38 /kg | high/name | vrsta=bez_glutena, oblik=spageti |
| 19 | 3850104230981 | TALIANETTA PODR 160G MAKARONI NAPOLITANA -12/1- | 160 g | 15 | 660 | 9,31–19,06 /kg | high/name | oblik=makaroni |
| 20 | 8076800105032 | TJESTENINA SPAGHETTINI 3 1 KG BARILLA KUTIJA | 1 kg | 15 | 486 | 2,99–4,62 /kg | high/name | oblik=spageti |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| TALIANETTA MAKARONI BOLOGNESE VR.160G (12) PODRAVKA | 19 | `bolognese` |
| BISTRA JUHA S TJEST.45G (16) (PAL 145) PODRAVKA | 18 | `juha` |
| ARGETA SALATA PILETINA TJESTENINA 160 G ATLANTIC | 16 | `piletin` |
| TALIANETTA TJESTENINA SA 4 SIRA VR.145G (12) PODRAVKA | 15 | `sira\b` |
| FANT ŠPAGETE BOLOGNESE PODRAVKA 58 g (20) | 14 | `bolognese` |
| GOVEĐA JUHA S TJESTENINOM 65G (35) (PAL 108), PODRAVKA | 13 | `juha` |
| KOKOŠJA JUHA S TJESTENINOM 62G (35) (PAL 108), PODRAVKA | 13 | `juha` |
| KAISER FRANZ JOSEF TUNA SALATA FUSILLI 160G(12) | 12 | `salata` |
| TALIANETTA TJESTENINA CARBONARA 160 G PODRAVKA | 10 | `carbonara` |
| GOVEĐA JUHA S TJESTENINOM I MESOM 60G (16) (PAL 145), PODRAVKA | 9 | `juha` |

</details>

<a id="kruh"></a>
## kruh (`kruh`)

jedinica: **kg** · loose_produce: **false** · grupa: **2990** · isključenih grupa: **378**

sinonimi: kruh  
must_match: `kruh\b | kruha\b`
atributi: vrsta = bijeli, polubijeli, crni, kukuruzni, razeni, mijesani; oblik = rezani

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 8008698024065 | KRUH BEZ GLUTENA 250G PANBIANCO DR.SCHAER -6/1- -8/1- | 250 g | 20 | 757 | 7,80–12,36 /kg | high/name | oblik=rezani, vrsta=bijeli |
| 2 | 8008698024188 | KRUH BEZ GLUTENA 250G PANRUSTICO DR.SCHAER -6/1- -8/1- | 250 g | 19 | 561 | 9,16–14,36 /kg | high/name | oblik=rezani |
| 3 | 4000446001735 | KRUH TRAJNI RAŽENI 3 VRSTE ŽITARICA 500g MESTEMACHER | 500 g | 18 | 771 | 3,38–6,98 /kg | high/name | vrsta=razeni |
| 4 | 4000446011376 | KRUH PROTEIN. 250 g MESTEMACHER ENCIAN | 250 g | 17 | 924 | 7,96–30,24 /kg | high/name |  |
| 5 | 8008698005576 | KRUH BEZ GLUTENA CLASSICO MASTRO PANETTIERE 300G DR.SCHAR | 300 g | 16 | 593 | 3,30–67,50 /kg | high/name | oblik=rezani, vrsta=bijeli |
| 6 | 4000446001780 | KRUH TRAJNI 500G FITNESS MESTERMACHER -9/1- | 500 g | 15 | 497 | 3,38–6,58 /kg | high/name |  |
| 7 | 4000446001742 | KRUH TRAJNI SA SUNCOKRETOM 500g MESTEMACHER | 500 g | 15 | 290 | 3,50–6,58 /kg | high/name | vrsta=razeni |
| 8 | 3856016906549 | KRUH FINI DOMAĆI NAR. 700 g A27043 ZP KLARA | 700 g | 14 | 807 | 2,56–5,50 /kg | high/name | oblik=rezani |
| 9 | 3856016906556 | KRUH KLARA RUSTIKA 500g NAR PAK KLARA | 500 g | 14 | 739 | 3,32–6,38 /kg | high/name | oblik=rezani |
| 10 | 4000446001728 | KRUH TRAJNI 500G RAŽENI-12/1- MESTEMACHER | 500 g | 14 | 376 | 3,38–6,98 /kg | high/name | vrsta=razeni |
| 11 | 5907653104091 | Balviten Kruh bijeli rezani bez glu.190g | 190 g | 13 | 592 | 7,37–14,32 /kg | high/name | vrsta=bijeli, oblik=rezani |
| 12 | 3856016906563 | KRUH KLARA RAŽENA RUSTIKA NAREZANI 500 gr | 500 g | 13 | 586 | 1,70–4,98 /kg | high/name | oblik=rezani, vrsta=razeni |
| 13 | 3856016906617 | KRUH KUKURUZNI MIJESANI REZANI PAKIRANI 600 G | 600 g | 13 | 546 | 1,70–5,48 /kg | high/name | vrsta=kukuruzni, oblik=rezani |
| 14 | 3830043040339 | KRUH DOM.KUKURUZNI REZ.400g TVOJIH 5 MIN | 400 g | 12 | 683 | 4,47–9,23 /kg | high/name | vrsta=kukuruzni, oblik=rezani |
| 15 | 3856016906624 | KRUH SA SJEMENKAMA NAREZANI 500 g A27049 KLARA | 500 g | 12 | 533 | 3,98–6,38 /kg | high/name | oblik=rezani |
| 16 | 8008698002599 | KRUH BEZ GLUTENA LANDBROT/PANE CASERECCIO 240G -5/1 DR.SCH | 240 g | 12 | 509 | 13,25–22,88 /kg | high/name | vrsta=bijeli |
| 17 | 8008698007389 | KRUH BEZ GLUTENA CEREALE MASTRO PANETTIERE 300G DR.SCHAR | 300 g | 12 | 495 | 10,93–69,00 /kg | high/name |  |
| 18 | 4000446011574 | KRUH PROTEINSKI S BADEMIMA 250G MESTEMACHER | 250 g | 12 | 332 | 9,16–18,20 /kg | high/name |  |
| 19 | 3856016907492 | ZLATNA KORA NAREZANI KRUH A27241 600 g KLARA | 600 g | 11 | 687 | 3,32–5,15 /kg | high/name | oblik=rezani |
| 20 | 3856016906716 | KRUH BIJELI REZANI PAKIRANI 500 G | 500 g | 11 | 441 | 2,38–4,58 /kg | high/name | vrsta=bijeli, oblik=rezani |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| BIO MJESAVINA ZA MEDITERANSKI KRUH 400 G DI-GO | 7 | `mjesavin` |
| BIO MJESAVINA ZA MULTIGRAIN KRUH 400 G DI-GO | 7 | `mjesavin` |
| BIO MJESAVINA ZA FINI DOMACI KRUH 400 G DI-GO | 6 | `mjesavin` |
| PVC KOSARICA ZA KRUH | 6 | `kosar` |
| TOST KRUH-PAN CARE 285 G MULINO BIANCO | 6 | `tost\b` |
| TOST SUPER SENDVIC KRUH 750 G OLZ | 6 | `tost\b` |
| MJEŠAVINA ZA KRUH BEZ GLUT SJEM. 500 g | 5 | `mjesavin` |
| MJEŠAVINA ZA MEDITERANSKI KRUH 400G DI-GO -10/1- 51031 | 5 | `mjesavin` |
| FACKELMANN KOSARICA ZA KRUH 23*18*9 CM | 4 | `kosar` |
| KALUP ZA KRUH/KOLAČ 33X14X7 cm GRANIT BASIC B EMO | 4 | `kalup` |

</details>

<a id="griz"></a>
## griz (`griz`)

jedinica: **kg** · loose_produce: **false** · grupa: **45** · isključenih grupa: **31**

sinonimi: griz, psenicna krupica  
must_match: `griz\b | psenicna krupica`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3838700075106 | PŠENIČNA KRUPICA BEBE GRIZ 250G ZLATO POLJE | 250 g | 12 | 480 | 2,96–6,08 /kg | high/name |  |
| 2 | 3858884170015 | PŠENIČNA KRUPICA 1kg T-400 ČAKOVEC | 1 kg | 10 | 477 | 0,99–2,09 /kg | high/name |  |
| 3 | 3838700540086 | PŠENIČNA KRUPICA BEBE GRIZ 450G ZLATO POLJE | 450 g | 7 | 322 | 3,18–3,82 /kg | high/name |  |
| 4 | 3858894591725 | ULTRA PLUS PŠENIČNA KRUPICA 1KG (GRIS) | 1 kg | 6 | 75 | 0,99–1,10 /kg | high/name |  |
| 5 | 3858881327177 | N-PŠENIČNI GRIZ KLARA ZP 1KG -20/1- | 1 kg | 5 | 57 | 0,83–2,49 /kg | high/name |  |
| 6 | 3858881327184 | PŠENIČNA KRUPICA 500 g KLARA AA1070 | 500 g | 4 | 167 | 2,38–3,98 /kg | high/name |  |
| 7 | 4000521029500 | HIGH PROTEIN GRIZ 95 G DR OETKER | 95 g | 4 | 119 | 17,37–29,16 /kg | high/name |  |
| 8 | 3858891971896 | GRIZ PIR ORGANSKI NUTRIGOLD 500 g | 500 g | 4 | 66 | 4,50–6,34 /kg | high/name |  |
| 9 | 3858887101511 | GRIZ PŠENIČNI TENA 1 kg | 1 kg | 3 | 187 | 1,10–1,55 /kg | high/name |  |
| 10 | 3858891970813 | RIŽIN GRIZ NUTRIGOLD 1 kg (8) | 1 kg | 3 | 133 | 2,09–3,79 /kg | high/name |  |
| 11 | 3858893691426 | PŠENIČNA KRUPICA XXL 1kg ŠAFRAM | 1 kg | 3 | 44 | 0,85–1,49 /kg | high/name |  |
| 12 | 3858881504189 | GRIZ PŠENIČNI KARLA 1 kg | 1 kg | 2 | 175 | 1,06–1,19 /kg | high/name |  |
| 13 | 3859891976331 | GRIZ INTEGRALNI PIR EKO 500 G EKO-JAZO | 500 g | 2 | 86 | 3,30–6,38 /kg | high/name |  |
| 14 | 3856031211765 | PSENICNA KRUPICA GRIS 1 KG OHO! | 1 kg | 1 | 155 | 0,99 /kg | high/name |  |
| 15 | 3856018214383 | PSENICNA KRUPICA GRIS 1 KG PLODINE | 1 kg | 1 | 155 | 0,99 /kg | high/name |  |
| 16 | 3858891975429 | GRIZ PSENICNI INTEGRALNI BIO 500 G NUTRIGOLD | 500 g | 1 | 121 | 3,18 /kg | high/name |  |
| 17 | 4056489073642 | Pšenična krupica TIP 400, 1kg | 1 kg | 1 | 116 | 0,99 /kg | high/name |  |
| 18 | 3858887100866 | PŠENIČNA KRUPICA 1 kg BELJE | 1 kg | 1 | 87 | 1,09 /kg | high/name |  |
| 19 | 3859893165320 | KLC.NMNP.Pšenična krupica Gris 1kg_OC | 1 kg | 1 | 53 | 0,99 /kg | high/name |  |
| 20 | 3859890160427 | Farina pšenična krupica -gris 1 kg | 1 kg | 1 | 53 | 1,19 /kg | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| DJ HRANA HIPP 190G BANANA GRIZ KAKAO -6/1- BIO | 9 | `hipp` |
| DESERT MLIJEČNI BELRISO GRIZ ČOKOLADA CIMET 130g | 8 | `desert` |
| DESERT MLIJEČNI BELRISO GRIZ JAGODA/ŠUMSKO VOĆE 130g | 7 | `desert` |
| PUDING GRIZ HIGH PROTEIN 65 G DR.OETKER | 6 | `puding` |
| N-PUDING DR. OETKER 400G GRIZ PROTEIN -6/1- | 5 | `puding` |
| Hipp bio kašica laku noć ban. griz 190g | 4 | `kasica` |
| Maggi Juha s mini griz okruglicama 34 g | 4 | `juha` |
| DJ HRANA HIPP 190G JABUKABRESKVA GRIZ -6/1- BIO | 3 | `hipp` |
| MLIJECNI DESERT GRIZ 4X100 G NESTLE | 3 | `desert` |
| Maggi juha s griz okruglicama 47 g | 3 | `juha` |

</details>

<a id="palenta"></a>
## palenta (kukuruzna krupica) (`palenta`)

jedinica: **kg** · loose_produce: **false** · grupa: **88** · isključenih grupa: **0**

sinonimi: palenta, pura, kukuruzna krupica, kukuruzni griz  
must_match: `palent | polent | kukuruzna krupica | kukuruzni griz | kuk krupica`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3858881080744 | N-PALENTA FRANCK INST 450G -12/1- VREĆICA | 450 g | 21 | 792 | 1,89–4,04 /kg | high/name |  |
| 2 | 8000271000015 | KUKURUZNA KRUPICA PALENTA 1KG NUOVA DE FRANCESCHI | 1 kg | 15 | 802 | 1,29–2,92 /kg | high/name |  |
| 3 | 3858881086456 | PALENTA INS. 200 g VREĆICA FRANC | 200 g | 15 | 594 | 3,45–5,95 /kg | high/name |  |
| 4 | 3850104053429 | KUKURUZNA KRUPICA PALENTA 1KG PODRAVKA | 1 kg | 15 | 372 | 1,19–2,29 /kg | high/name |  |
| 5 | 3838700540147 | PALENTA 450 g ZLATO POLJE PODRAVKA | 450 g | 14 | 640 | 1,89–4,11 /kg | high/name |  |
| 6 | 3859890104001 | PALENTA INSTANT 450G (10), ŠAFRAM | 450 g | 12 | 398 | 1,89–3,53 /kg | high/name |  |
| 7 | 3838700540116 | PALENTA 250 g ZLATO POLJE PODRAVKA | 250 g | 10 | 418 | 3,00–4,88 /kg | high/name |  |
| 8 | 3858884176048 | KUK. KRUPICA 450 G CAKOVECKI MLINOVI | 450 g | 9 | 274 | 1,89–4,42 /kg | high/name |  |
| 9 | 3858893691365 | PALENTA XXL BRZA PRIPREMA 1000 G (5) | 1 kg | 7 | 257 | 0,89–1,49 /kg | high/name |  |
| 10 | 3858891564517 | ULTRA INSTANT PALENTA 400GR.(12) (1080 #) | 400 g | 6 | 73 | 1,40–2,47 /kg | high/name |  |
| 11 | 3858881327153 | KUKURUZNA KRUPICA 1000 g KLARA AA1069 | 1 kg | 5 | 156 | 1,80–2,89 /kg | high/name |  |
| 12 | 3859892259426 | 1KG LARA KUKURUZNA KRUPICA PVC | 1 kg | 5 | 88 | 1,05–1,99 /kg | high/name |  |
| 13 | 3856003914595 | KUKURUZNA KRUPICA 750g TO JE TO | 750 g | 4 | 490 | 1,59–1,67 /kg | high/name |  |
| 14 | 3858887101801 | Tena Palenta kukuruz.krupica bijela 500g | 500 g | 4 | 308 | 2,38–3,30 /kg | high/name |  |
| 15 | 3831001801122 | KUKURUZNA KRUPICA 1 kg MLINOTEST | 1 kg | 4 | 151 | 1,00–3,69 /kg | high/name |  |
| 16 | 8000786100248 | PALENTA BEZ GLUTENA INSTANT 500G (20) | 500 g | 4 | 110 | 2,88–3,74 /kg | high/name |  |
| 17 | 3858891569901 | KUKURUZNA KRUPICA PALENTA KUHARELA 400G ULTRA PLUS | 400 g | 4 | 65 | 1,22–1,90 /kg | high/name |  |
| 18 | 3856003914601 | PALENTA INSTANT 500 g TO JE TO VREĆICA NTL | 500 g | 3 | 473 | 1,18–1,90 /kg | high/name |  |
| 19 | 3858881327160 | KUKURUZNA KRUPICA 500 g KLARA AA1068 | 500 g | 3 | 120 | 1,98–3,38 /kg | high/name |  |
| 20 | 3859893567032 | PALENTA BIJELA 500 g IZIDOR | 500 g | 3 | 88 | 2,38–3,38 /kg | high/name |  |

<a id="zobene_pahuljice"></a>
## zobene pahuljice (`zobene_pahuljice`)

jedinica: **kg** · loose_produce: **false** · grupa: **72** · isključenih grupa: **20**

sinonimi: zobene pahuljice, zobene, zob  
must_match: `zobene pahuljice | zob pahuljice | pahuljice zobene | zobene\b | ovsene`
atributi: vrsta = sitne, krupne

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 4008713702804 | N-ZOBENE PAHULJICE BRUEGGEN EXTRA 500G -20/1- | 500 g | 18 | 1185 | 1,90–3,50 /kg | high/name | vrsta=sitne |
| 2 | 4013138008851 | ZOBENE PAHULJICE SITNE 500G WURZENER ENCIAN | 500 g | 15 | 660 | 1,98–4,58 /kg | high/name | vrsta=sitne |
| 3 | 4013138003740 | PAHULJICE ZOBENE KRUPNE 500 g WURZENER ENCIAN | 500 g | 13 | 758 | 2,12–4,90 /kg | high/name | vrsta=krupne |
| 4 | 4008713713947 | N-ZOBENE PAHULJICE BRUGGEN 500G CIJELE -15/1- / -20/1- | 500 g | 11 | 387 | 1,98–3,50 /kg | high/name | vrsta=krupne |
| 5 | 4000540080100 | ZOBENE PAHULJICE INTEGRALNE MEKE 500G KOLLN | 500 g | 11 | 256 | 4,70–6,38 /kg | high/name |  |
| 6 | 3858886175230 | ZOBENE PAHULJICE 500G SITNE EKOZONA 10/1 | 500 g | 7 | 278 | 3,18–4,98 /kg | high/name | vrsta=sitne |
| 7 | 3858888737801 | MEKINJE ZOBENE 500G EKOZONA 10/1 | 500 g | 7 | 257 | 3,80–6,48 /kg | high/name |  |
| 8 | 3858891566153 | ZOBENE PAHULJICE 500G ULTRA FIT U-20706 -12/1- | 500 g | 7 | 75 | 1,86–3,10 /kg | high/name | vrsta=krupne |
| 9 | 3858882921091 | ZOBENE PAHULJICE SITNE 500g PRIMAVITA ADVENT | 500 g | 6 | 270 | 2,66–3,98 /kg | high/name | vrsta=sitne |
| 10 | 3858886175247 | ZOBENE PAHULJICE 500G KRUPNE EKOZONA -6/1 | 500 g | 6 | 263 | 3,18–4,98 /kg | high/name | vrsta=krupne |
| 11 | 3858882921084 | ZOBENE PAHULJICE KRUPNE 500G PRIMAVITA | 500 g | 6 | 115 | 2,78–3,90 /kg | high/name | vrsta=krupne |
| 12 | 4000540050103 | ZOBENE PAHULJICE KOLLN 500 G | 500 g | 4 | 158 | 4,38–6,38 /kg | high/name |  |
| 13 | 3858894620425 | ZOBENE PAHULJICE SITNE XXL ENCIAN 2 kg | 2 kg | 4 | 105 | 1,90–3,30 /kg | high/name | vrsta=sitne |
| 14 | 4400045232613 | ZOBENE PAHULJICE 500G WURZENER KRUPNI TIP | 500 g | 4 | 21 | 3,28–4,98 /kg | high/name | vrsta=krupne |
| 15 | 4008713011289 | ZOBENE PAHULJICE CIJELE 500G | 500 g | 4 | 9 | 2,18–3,88 /kg | high/name |  |
| 16 | 3859889259781 | ZOBENE PAHULJICE VR. 1 kg (15) PODRAVKA | 1 kg | 4 | 8 | 2,09–2,54 /kg | high/name |  |
| 17 | 3838900820704 | ZOBENE PAHULJICE RISE & SMILE SITNE 500g | 500 g | 3 | 198 | 0,86–1,98 /kg | high/name | vrsta=sitne |
| 18 | 8595054907723 | ZOBENE PAHULJICE NATURAL 350 G BIOPLOD | 350 g | 3 | 149 | 7,69–9,11 /kg | high/name |  |
| 19 | 3859893457807 | ZOBENE PAHULJICE SITNE BEZ GLUTENA 500 G GRANA | 500 g | 3 | 145 | 2,30–5,98 /kg | high/name | vrsta=sitne |
| 20 | 3858894620449 | ZOBENE PAHULJICE KRUPNE XXL ENCIAN 2 kg | 2 kg | 3 | 26 | 1,90–3,30 /kg | high/name | vrsta=krupne |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| ZOBENE PAHULJICE SUMSKO VOCE 300 G BIOPLOD | 11 | `voce` |
| ZOBENE PAHULJICE COKOLADA 300 G BIOPLOD | 10 | `cokolad` |
| KEKS PLAZMA WELLNESS 210g ZOBENE PAHULJICE | 5 | `keks` |
| MB ZOBENE PLOCICE - COKOLADA S KOM. VOĆA | 2 | `cokolad` |
| MB ZOBENE PLOCICE - COKOLADA S NARANCOM | 2 | `cokolad` |
| MB ZOBENE PLOCICE - SMOOTHIE ŠUMSKO VOĆE | 2 | `voce` |
| ZOBENE PLOCICE BEZ DODANOG SECERA MARELICA 50 G MA BAKER | 2 | `ploc` |
| KEKS ZOBENE PAHULJICE 250 G BISCOLETTI | 1 | `keks` |
| MB ZOBENE PLOCICE - BOBICASTO VOćE BOROV | 1 | `voce` |
| MB ZOBENE PLOCICE - COKOLADA S KOM.BEL.Č | 1 | `cokolad` |

</details>

<a id="krusne_mrvice"></a>
## krušne mrvice (`krusne_mrvice`)

jedinica: **kg** · loose_produce: **false** · grupa: **136** · isključenih grupa: **12**

sinonimi: krusne mrvice, prezle, mrvice  
must_match: `krusne mrvice | mrvice krusne | mrvice\b | prezle | panko`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3858881322011 | MRVICE KRUŠNE KLARA ZP 500G -42/1- | 500 g | 18 | 884 | 2,98–6,35 /kg | high/name |  |
| 2 | 3858881322059 | N-MRVICE KRUŠNE KLARA ZP 250G -60/1- | 250 g | 15 | 814 | 3,96–7,80 /kg | high/name |  |
| 3 | 3858881322233 | MRVICE KRUŠNE KLARA ZP 1KG-15/1- A51338 | 1 kg | 12 | 381 | 2,59–6,29 /kg | high/name |  |
| 4 | 5902898827163 | MRVICE PANKO ZA SUSHI 200G HOUSE OF ASIA | 200 g | 10 | 368 | 9,95–15,75 /kg | high/name |  |
| 5 | 3856016904644 | MRVICE KRUŠNE KLARA ZP XXL 600G -15/1 | 600 g | 9 | 409 | 3,75–4,98 /kg | high/name |  |
| 6 | 5010338014902 | PANKO BREADCRUMB MIX 120G BLUE DRAGON 12/1- | 120 g | 8 | 279 | 24,83–39,92 /kg | high/name |  |
| 7 | 8715035809703 | N-PANKO MRVICE KIKKOMAN 227G SITNE -12/1- | 227 g | 7 | 164 | 10,44–19,34 /kg | high/name |  |
| 8 | 5999568625037 | It`s Us krušne mrvice bez glutena 300g | 300 g | 6 | 97 | 14,97–19,30 /kg | high/name |  |
| 9 | 3858881324060 | N-MRVICE KRUŠNE ULTRA+ KLARA ZP 480G A51926 -42/1- | 480 g | 5 | 73 | 2,44–3,31 /kg | high/name |  |
| 10 | 3858881324039 | MRVICE KRUŠNE ULTRA+ KLARA ZP240G A51925 -60/1- | 240 g | 5 | 72 | 2,79–3,96 /kg | high/name |  |
| 11 | 3858884717487 | KRUšNE MRVICE 500 g BABIĆ | 500 g | 4 | 191 | 3,50–5,00 /kg | high/name |  |
| 12 | 3858881121713 | KRUSNE MRVICE 500 G MLINAR | 500 g | 4 | 80 | 1,72–3,98 /kg | high/name |  |
| 13 | 3850104065149 | KRUŠNE MRVICE 250 g PODRAVKA | 250 g | 4 | 29 | 2,32–3,48 /kg | high/name |  |
| 14 | 3850334343741 | KRUŠNE MRVICE RIAL 500g (20) | 500 g | 4 | 12 | 1,78–2,69 /kg | high/name |  |
| 15 | 3856003930953 | MRVICE KRUŠNE 500 g PANEA NTL | 500 g | 3 | 475 | 2,30–2,78 /kg | high/name |  |
| 16 | 3856003930946 | KRUŠNE MRVICE 200 g PANEA NTL | 200 g | 3 | 395 | 1,95–3,95 /kg | high/name |  |
| 17 | 3859892992033 | KRUSNE MRVICE SA SEZAMOM 500 G MOJ KRUH | 500 g | 3 | 298 | 2,26–3,30 /kg | high/name |  |
| 18 | 3859892992026 | KRUSNE MRVICE 500 G MOJ KRUH | 500 g | 3 | 281 | 1,96–3,58 /kg | high/name |  |
| 19 | 3858884717494 | KRUŠNE MRVICE 250 g BABIĆ | 250 g | 3 | 150 | 4,44–6,60 /kg | high/name |  |
| 20 | 3850135250057 | KRUSNE MRVICE 500 G PIK | 500 g | 3 | 116 | 1,72–3,98 /kg | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| DEKOR DR OETKER 80G -10/1- KAKAO MRVICE | 17 | `dekor` |
| DEKOR DR OETKER 80G ŠARENE MRVICE-10/1 | 17 | `dekor` |
| BOMBONI ŠARENE MRVICE 100 g | 6 | `saren` |
| DRAŽE ČOKOLADNE MRVICE 100 g KRAŠ (18) | 5 | `cokolad` |
| 720G KOTANYI ŠARENE ŠEĆ MRVICE | 1 | `saren` |
| KLC. Čokoladne mrvice mliječ. čok. 400 g | 1 | `cokolad` |
| KLC.Čokoladne mrvice 100g | 1 | `cokolad` |
| KLC.čokola.mrvice.mliječna.čokolada.100g | 1 | `cokolad` |
| KLC.čokoladn.mrvice.bijela.čokolada.100g | 1 | `cokolad` |
| KLC.čokoladne.mrvice.crna.čokolada.100g | 1 | `cokolad` |

</details>

<a id="kvasac"></a>
## kvasac (`kvasac`)

jedinica: **kg** · loose_produce: **false** · grupa: **60** · isključenih grupa: **1**

sinonimi: kvasac, germa  
must_match: `kvasac | kvas\b`
atributi: vrsta = suhi, svjezi

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3859889940085 | DI GO INSTANT SUHI PEKARSKI KVASAC 7 g | 7 g | 21 | 959 | 80,00–141,43 /kg | high/name | vrsta=suhi |
| 2 | 3850104266577 | DOLCELA INSTANT SUHI KVASAC 7 g 4+1 GRATIS, PODRAVKA | 7 g | 20 | 1079 | 60,00–451,43 /kg | high/name | vrsta=suhi |
| 3 | 3858887683444 | DI-GO pekarski svježi kvasac 42g | 42 g | 19 | 1354 | 4,52–25,95 /kg | high/name | vrsta=svjezi |
| 4 | 3850104266003 | KVASAC SUHI INSTANT 7g DOLCELA PODRAVKA | 7 g | 18 | 1145 | 55,71–112,86 /kg | high/name | vrsta=suhi |
| 5 | 3859889940153 | DI-GO INST. SUHI PEKARSKI KVASAC 7 g 4+1 GRAT (10) | 7 g | 17 | 858 | 17,09–3880,00 /kg | high/name | vrsta=suhi |
| 6 | 4000521024444 | KVASAC DR OETKER 35G INSTANT 4+1 5*7G -50/1- | 35 g | 16 | 1011 | 43,14–377,14 /kg | high/name | vrsta=suhi |
| 7 | 4000521000349 | KVASAC SUHI INSTANT 7g DR.OETKER | 7 g | 15 | 1025 | 50,00–107,14 /kg | high/name | vrsta=suhi |
| 8 | 8690770323045 | KVASAC DR OETKER 100G INSTANT-30/1- | 100 g | 15 | 534 | 9,90–20,90 /kg | high/name | vrsta=suhi |
| 9 | 3850104266027 | KVASAC SUHI INSTANT 450G DOLCELA PODRAVKA | 450 g | 14 | 333 | 5,56–14,91 /kg | high/name | vrsta=suhi |
| 10 | 3850104266034 | INSTANT SUHI KVASAC 100G (30),PODRAVKA | 100 g | 13 | 449 | 11,30–15,50 /kg | high/name | vrsta=suhi |
| 11 | 3859889940108 | 500G DI-GO KVASAC SUHI PEKARSKI | 500 g | 12 | 443 | 6,00–16,98 /kg | high/name | vrsta=suhi |
| 12 | 4003834000112 | KVASAC SVJEŽI 42G DR.OETKER -24/1- | 42 g | 11 | 477 | 9,29–14,05 /kg | high/name | vrsta=svjezi |
| 13 | 3859889940849 | KVASAC DI-GO INS.SUH.PEK.125 g | 125 g | 10 | 467 | 12,72–20,40 /kg | high/name | vrsta=suhi |
| 14 | 8690770323052 | INSTANT KVASAC 450 g DR.OETKER | 450 g | 8 | 251 | 7,98–14,42 /kg | high/name | vrsta=suhi |
| 15 | 3859889940832 | N-KVASAC DIGO 42G SVJEŽI -24/1-+-/PEKARSTVO | 42 g | 7 | 88 | 13,33–23,57 /kg | high/name | vrsta=svjezi |
| 16 | 3850114203142 | KVASAC SVJEŽI 50g(2*25g) DUOS | 50 g | 5 | 259 | 7,00–10,20 /kg | high/name | vrsta=svjezi |
| 17 | 8600947081913 | KVASAC ALEVA SUHI 10 g | 10 g | 4 | 53 | 26,00–49,00 /kg | high/name | vrsta=suhi |
| 18 | 8008698005828 | KVASAC SUHI BEZ GLUTENA 20 G DR.SCHAR | 20 g | 3 | 196 | 84,00–97,50 /kg | high/name | vrsta=suhi |
| 19 | 3859889940887 | DI-GO DOMAĆI SVJEŽI KVASAC 42 g (40) | 42 g | 3 | 20 | 15,48–23,50 /kg | high/name | vrsta=svjezi |
| 20 | 3858887680627 | KVASAC SVJEŽI DI GO 500 g (20) | 500 g | 3 | 12 | 2,02–2,38 /kg | high/name | vrsta=svjezi |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| KAPSULE PIVSKI KVASAC 80/1 | 1 | `kapsul` |

</details>

<a id="prasak_za_pecivo"></a>
## prašak za pecivo (`prasak_za_pecivo`)

jedinica: **kg** · loose_produce: **false** · grupa: **48** · isključenih grupa: **0**

sinonimi: prasak za pecivo, praska za pecivo  
must_match: `prasak za pecivo | pr za pecivo | prasak pecivo | backpulver`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850104242175 | PRAŠAK ZA PECIVO DOLCELA 5+1 GRATIS 6X12g PODRAVKA | 12 g | 23 | 863 | 12,50–104,17 /kg | high/name |  |
| 2 | 3850104216770 | PRAŠAK ZA PECIVO 12G,(48) PODRAVKA (PAL 441) | 12 g | 18 | 1181 | 10,00–32,50 /kg | high/name |  |
| 3 | 5997381375498 | PRAŠAK ZA PECIVO DR OETKER 12G -50/1- | 12 g | 14 | 1033 | 13,33–25,00 /kg | high/name |  |
| 4 | 3850104219535 | PRAŠAK ZA PECIVO 1kg PODRAVKA (4) | 1 kg | 7 | 31 | 3,50–5,84 /kg | high/name |  |
| 5 | 3856020275501 | PRAŠAK ZA PECIVO PODR 72G 6-PACK -16/1- 6*12G | 12 g | 6 | 660 | 13,75–124,17 /kg | high/name |  |
| 6 | 5997381375511 | PRASAK ZA PECIVO 5+1 72 G DR.OETKER | 72 g | 6 | 416 | 6,81–104,17 /kg | high/name |  |
| 7 | 5997381375504 | PRAŠAK ZA PECIVO 12 g 5+1 GRATIS DR.OETKER | 12 g | 6 | 404 | 13,61–108,33 /kg | high/name |  |
| 8 | 3858891565514 | PRAŠAK ZA PECIVO 12G 5/1 60G ULTRA PLUS | 60 g | 5 | 72 | 5,83–36,67 /kg | high/name |  |
| 9 | 5997381317641 | PRAŠAK ZA PECIVO 5+1 GRATIS 72G (16)DR.OETKER | 72 g | 5 | 24 | 12,36–95,83 /kg | high/name |  |
| 10 | 3856003939703 | PRAŠAK ZA PECIVO (5 x 12g) 60g FINETA | 60 g | 4 | 477 | 5,83–12,17 /kg | high/name |  |
| 11 | 3856020254643 | DOLCELA PRAŠAK ZA PECIVO 12 g 10 pak (48) PODRAVKA | 12 g | 4 | 216 | 11,58–132,50 /kg | high/name |  |
| 12 | 3850334197665 | PRAŠAK ZA PECIVO 60g 5X12g SWEET CHEF (36) | 60 g | 3 | 184 | 6,00–8,83 /kg | high/name |  |
| 13 | 3856003939697 | PRAŠAK ZA PECIVO FINETA 12 g NTL | 12 g | 3 | 172 | 10,83–15,83 /kg | high/name |  |
| 14 | 3858881580138 | PRAŠAK ZA PECIVO 5x13g 65g | 65 g | 3 | 60 | 7,69–15,23 /kg | high/name |  |
| 15 | 3858881588196 | PRAŠAK ZA PECIVO 1 kg NADALINA | 1 kg | 3 | 23 | 4,64–9,99 /kg | high/name |  |
| 16 | 8606104332430 | PRAŠAK ZA PECIVO 5+1 GRATIS 60g | 10 g | 3 | 4 | 6,50–73,00 /kg | high/name |  |
| 17 | 38389719 | PRAŠAK ZA PECIVO 12 g PODRAVKA (48) | 12 g | 2 | 21 | 11,67–15,83 /kg | high/name |  |
| 18 | 5997381346870 | PRAŠAK ZA PECIVO 6+2GR 96G DR.OETKER | 2 g | 2 | 6 | 495,00–970,00 /kg | high/name |  |
| 19 | 5997381375528 | PRAŠAK ZA PECIVO 6X12g DR OETKER | 72 g | 1 | 184 | 13,75–14,58 /kg | high/name |  |
| 20 | 3856018261172 | PRASAK ZA PECIVO 5X12 G B B | 60 g | 1 | 155 | 8,17 /kg | high/name |  |

<a id="vanilin_secer"></a>
## vanilin šećer (`vanilin_secer`)

jedinica: **kg** · loose_produce: **false** · grupa: **85** · isključenih grupa: **6**

sinonimi: vanilin secer, vanilin  
must_match: `vanilin secer | vanilinski secer | secer vanilin | vanilin\b`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3856020258726 | DOLCELA VANILIN ŠEĆER 8 g 5+1 GRATIS PODRAVKA (44) | 8 g | 21 | 858 | 12,50–243,75 /kg | high/name |  |
| 2 | 3856020258511 | DOLCELA VANILIN ŠEĆER 8 g PODRAVKA (44) | 8 g | 20 | 1202 | 15,00–48,75 /kg | high/name |  |
| 3 | 5997381375542 | VANILIN ŠEĆER DR OETKER 8G -50/1- | 8 g | 13 | 1014 | 19,00–37,50 /kg | high/name |  |
| 4 | 5997381337779 | VANILIN ŠEĆER BURBON 10G(50) DR.OETKER | 10 g | 13 | 640 | 36,00–69,00 /kg | high/name |  |
| 5 | 5997381369626 | SLADILO SWEET ZERO VANILIN 8 g DR.OETKER | 8 g | 11 | 449 | 41,25–81,25 /kg | high/name |  |
| 6 | 9001414410127 | KOTANYI 20G BOURBON VANILIN ŠEĆER -25/1- | 20 g | 11 | 261 | 4,85–59,50 /kg | high/name |  |
| 7 | 5997381375566 | Dr.Oetker vanilin šećer 6x8g 1 gratis | 8 g | 8 | 461 | 18,33–162,50 /kg | high/name |  |
| 8 | 5997381345750 | VANILIN ŠEČER BOURBON X3 30G (18) DR OETKER | 36 g | 8 | 257 | 29,44–53,00 /kg | high/name |  |
| 9 | 3850104242151 | VANILIN ŠEĆER 10 g 5+1 GRATIS 4F PODRAV | 10 g | 8 | 196 | 16,50–1450,00 /kg | high/name |  |
| 10 | 3850104018886 | VANILIN ŠEĆER 1kg PODRAVKA (4) | 1 kg | 8 | 33 | 4,44–7,09 /kg | high/name |  |
| 11 | 3856020275532 | DOLCELA VANILIN ŠEĆER 8 g 6 PAK PODRAVKA (16) | 8 g | 7 | 656 | 20,63–186,25 /kg | high/name |  |
| 12 | 5997381375573 | Dr. Oetker vanilin šećer 10x8g 2 gratis | 80 g | 7 | 482 | 16,13–142,50 /kg | high/name |  |
| 13 | 3850104018862 | VANILIN ŠEĆER 10 g PODRAVKA (48) | 10 g | 6 | 192 | 13,00–29,00 /kg | high/name |  |
| 14 | 9001414502389 | KOTANYI BURBON,VANILIN ŠEĆER 10G VREĆICA | 10 g | 6 | 155 | 65,00–119,00 /kg | high/name |  |
| 15 | 3856020270742 | VANILIN ŠEĆER U PRAHU 100 g DOLCELA | 100 g | 6 | 73 | 7,60–14,20 /kg | high/name |  |
| 16 | 3858891565507 | VANILIN ŠEĆER 10G 5/1 50G ULTRA PLUS | 50 g | 6 | 71 | 7,80–44,00 /kg | high/name |  |
| 17 | 5997381375559 | VANILIN ŠEĆER 5+1 DR.OETKER 8 g | 8 g | 5 | 383 | 20,42–161,25 /kg | high/name |  |
| 18 | 3830056440348 | VANILIN KIFILICE 400g VOPEX | 400 g | 5 | 381 | 5,23–8,98 /kg | high/name |  |
| 19 | 3856020260767 | DOLCELA VANILIN ŠEĆER 8 g 10kom PODRAVKA | 8 g | 5 | 228 | 17,37–211,25 /kg | high/name |  |
| 20 | 9001414611791 | *NE*VANILIN AROMATIZIRANI ŠEĆER VREĆICA 70g | 70 g | 5 | 178 | 11,43–17,00 /kg | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| KEKS LILLY VANILIN 220g KRAŠ (16) | 12 | `keks` |
| KEKS LILLY VANILIN KRAŠ 220 g (16) | 4 | `keks` |
| PUDING VANILIN 1 kg DOLCELA | 2 | `puding` |
| KEKSI VANILIN KIFLICE 300 g RADNI | 1 | `keks` |
| ŠLAG KREMA VANILIN 45 g PODRAVKA | 1 | `krema` |
| ŠLAG KREMA VANILIN 45g PODRAVKA | 1 | `krema` |

</details>

<a id="kakao"></a>
## kakao (prah) (`kakao`)

jedinica: **kg** · loose_produce: **false** · grupa: **268** · isključenih grupa: **548**

sinonimi: kakao, kakao prah  
must_match: `kakao\b`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3858881044012 | KAKAO PRAH KANDIT 100G -12/1- SMANJENE MASTI 16-18% | 100 g | 21 | 1058 | 16,60–30,80 /kg | high/name |  |
| 2 | 5997381346917 | KAKAO DR OETKER ZA KOLAČE 70G-16/1- | 70 g | 14 | 561 | 19,00–38,71 /kg | high/name |  |
| 3 | 3858881773608 | KAKAO U PRAHU ANAMARIJA 100 g | 100 g | 9 | 569 | 9,30–30,50 /kg | high/name |  |
| 4 | 3856020282882 | MUFFINS CLASSIC KAKAO 300 g DOLCELA | 300 g | 6 | 462 | 8,30–9,50 /kg | high/name |  |
| 5 | 5310115001096 | TORTINA KAKAO 200 g (6) VINCINNI MADIS | 200 g | 6 | 111 | 5,95–12,50 /kg | high/name |  |
| 6 | 5310115006404 | TORTINA PLUS KAKAO 300 g VINCI | 300 g | 5 | 100 | 7,50–12,30 /kg | high/name |  |
| 7 | 5310115008194 | TORTELA KAKAO 240G -12/1ULTRA+ | 240 g | 5 | 71 | 6,08–8,54 /kg | high/name |  |
| 8 | 3858891566221 | ULTRA KAKAO U PRAHU 100G ,ANAMARIJA | 100 g | 5 | 70 | 8,30–23,90 /kg | high/name |  |
| 9 | 3856003937242 | JASTUČIĆI PUNJENJI KAKAO KREMOM PILLOWS 250g SMIJEŠAK | 250 g | 4 | 483 | 8,76–10,60 /kg | high/name |  |
| 10 | 3858892322369 | KESTEN ŠTAPIĆI KAKAO 80G SANA DELIKATESE DS | 80 g | 4 | 254 | 24,88–39,88 /kg | high/name |  |
| 11 | 8710447485323 | KREMA VASELINE KAKAO 100 ml | 100 ml | 4 | 205 | 29,50–49,50 /l | high/name |  |
| 12 | 8004333017058 | PRALINE KAKAO BOŽIĆ 200 g ROVELLI | 200 g | 3 | 267 | 14,95–17,45 /kg | high/name |  |
| 13 | 9004380181206 | KAVA LEDENA KAKAO 230 ml | 230 ml | 3 | 110 | 8,65–10,22 /l | high/name |  |
| 14 | 3838900033203 | KAKAO BENQUICK CHOCO BOX 400g | 400 g | 3 | 37 | 10,73–12,48 /kg | high/name |  |
| 15 | 8693029702912 | TODAY DONUT KAKAO ELVAN 6x50 g (12) | 300 g | 3 | 10 | 3,80–13,60 /kg | high/name |  |
| 16 | 3850334072450 | KAKAO LUMPI VREĆICA 350G (8) | 350 g | 2 | 179 | 6,03–7,29 /kg | high/name |  |
| 17 | 3850334055149 | KAKAO PRAH SWEET CHEF 250G (12) | 250 g | 2 | 119 | 17,32–21,16 /kg | high/name |  |
| 18 | 3856021228872 | SAVIJ.VAN.KAKAO S-BUDGET 500 g | 500 g | 2 | 80 | 4,58–5,18 /kg | high/name |  |
| 19 | 3859889106306 | PECIVO ČAJNO KAKAO BŠ 34 g DELICIA | 34 g | 2 | 54 | 22,06–30,88 /kg | high/name |  |
| 20 | 3858890134360 | EKO KAKAO U PR.200 g EKOZONA | 200 g | 2 | 51 | 26,25–38,45 /kg | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| VAFEL KAKAO PRUTICI FRONDI 250 G KRAS | 23 | `vafel` |
| KAKAO PRAH 100G (21), KRAŠ (PAL-90) | 20 | `kras\b` |
| KEKS KAROLINA 288G MOTO KAKAO -18/1- | 20 | `keks` |
| PREKRAŠNI KOLAČIĆI KEKS KAKAO 220G (10) (PAL40) KRAŠ | 20 | `keks` |
| DORINA ČOKOLADICA KREM KAKAO 38 g (24) | 19 | `cokolad` |
| LEDOLETTA KAKAO KREM 800g | 19 | `krem\b` |
| DEKOR DR OETKER 80G -10/1- KAKAO MRVICE | 18 | `dekor` |
| N-KEKS KAROLINA 192G MOTO KAKAO -12/1- | 18 | `keks` |
| VAFEL KAKAO I MLIJEKO PRUTICI FRONDI 225 G KRAS | 18 | `vafel` |
| CROISSANT KAKAO 240G MULTIPACK 7 DAY'S CHIPITA | 17 | `croissant` |

</details>

<a id="cokolada_za_kuhanje"></a>
## čokolada za kuhanje (`cokolada_za_kuhanje`)

jedinica: **kg** · loose_produce: **false** · grupa: **57** · isključenih grupa: **0**

sinonimi: cokolada za kuhanje, cokolada za kolace  
must_match: `cokolada za kuhanje | cokolada za kuh | cok za kuh | cokolada za kolace | cokolada za pecenje | kuhinjska cokolada | za kuhanje cokolada`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3858881048997 | KANDIT DESSERT CHEF ČOKOLADA ZA KUHANJE 300G (20) | 300 g | 22 | 1225 | 8,83–22,30 /kg | high/name |  |
| 2 | 3858881040298 | DESSERT CHEF COKOLADA ZA KUHANJE 200 G KANDIT | 200 g | 21 | 1053 | 10,50–25,45 /kg | high/name |  |
| 3 | 3850102008643 | DORINA BIJELA ČOKOLADA ZA KUHANJE 200 g (12) KRAŠ | 200 g | 16 | 633 | 9,95–31,95 /kg | high/name |  |
| 4 | 3850102008681 | DORINA ČOKOLADA ZA KUHANJE 400 g (8) KRAŠ | 400 g | 7 | 153 | 5,98–20,48 /kg | high/name |  |
| 5 | 3877000595778 | ČOKOLADA ZA KUH.XXL 300 g LA BOMBA | 300 g | 6 | 588 | 10,30–14,00 /kg | high/name |  |
| 6 | 8004735020861 | ČOK ZA KUHANJE TAMNA 50% 200g ZAINI | 200 g | 6 | 211 | 5,00–99,75 /kg | high/name |  |
| 7 | 3856003953419 | ČOKOLADA ZA KUHANJE 300 g (14) SMIJEŠAK | 300 g | 5 | 499 | 10,30–14,00 /kg | high/name |  |
| 8 | 3850102018857 | ČOKOLADA ZA KUHANJE RUM 200 g KRAŠ | 200 g | 5 | 240 | 14,95–24,95 /kg | high/name |  |
| 9 | 3850102018864 | ČOKOLADA ZA KUH. PREM. 200 g KRAŠ | 200 g | 5 | 238 | 14,95–24,95 /kg | high/name |  |
| 10 | 7613035587793 | COK. ZA KUH. MILK 170 G DESSERT NESTLE | 170 g | 4 | 218 | 0,80–34,41 /kg | high/name |  |
| 11 | 8004735065077 | ČOK.ZA KUHANJE BIJELA 200g EMILIA | 200 g | 4 | 129 | 15,00–53,45 /kg | high/name |  |
| 12 | 3858891563046 | COK.ZA KUH.200G ULTRA PLUS | 200 g | 4 | 61 | 5,95–8,05 /kg | high/name |  |
| 13 | 8606103719218 | ČOKOLADA ZA KUHANJE I JELO 200G KONDI | 200 g | 4 | 10 | 7,45–11,05 /kg | high/name |  |
| 14 | 3856003953402 | ČOKOLADA ZA KUHANJE 100 g SMIJEŠAK | 100 g | 3 | 369 | 9,90–14,90 /kg | high/name |  |
| 15 | 3850334100764 | ČOKOLADA ZA KUHANJE 43% 350g SWEET CHEF (9) | 350 g | 3 | 198 | 10,43–18,30 /kg | high/name |  |
| 16 | 3877000595464 | ČOKOLADA ZA KUH.200 g LA BOMBA | 200 g | 2 | 73 | 10,50–16,45 /kg | high/name |  |
| 17 | 3856024703420 | ARO ČOKOLADA ZA KUHANJE BIJELA 200G | 200 g | 2 | 8 | 23,05–29,00 /kg | high/name |  |
| 18 | 3856003915035 | ČOKOLADA ZA KUHANJE 100 g SMIJEŠAK | 100 g | 2 | 3 | 9,10–9,90 /kg | high/name |  |
| 19 | 3850334044129 | ČOKOLADA ZA KUHANJE 52% 200G SWEET CHEF | 200 g | 1 | 184 | 17,45 /kg | high/name |  |
| 20 | 3856018244984 | COKOLADA ZA KUHANJE BAKE AND ROLL 350 G | 350 g | 1 | 155 | 10,49 /kg | high/name |  |

<a id="pileca_prsa"></a>
## pileća prsa / file (`pileca_prsa`)

jedinica: **kg** · loose_produce: **false** · grupa: **277** · isključenih grupa: **106**

sinonimi: pileca prsa, pileci file, piletina file  
must_match: `pilec prsa | pileca prsa | pileci file | pilec file | prsa pilec | file pilec | pileci filet | pil prsa | pil file`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850159110986 | N-VIN.PILEĆI FILE 500G -10/1- 11098 | 500 g | 17 | 954 | 9,98–15,78 /kg | high/name |  |
| 2 | 3858892724392 | PILEĆA PRSA 350 g JE LI GAVRILOVIĆ | 350 g | 9 | 310 | 8,11–13,40 /kg | high/name |  |
| 3 | 3850220115827 | PILEĆI FILE PERUTNINA 500g (6) | 500 g | 8 | 629 | 9,54–14,98 /kg | high/name |  |
| 4 | 3856020279929 | PILEĆA PRSA FIT&FINA NAR 100 g PODR | 100 g | 7 | 382 | 16,50–26,50 /kg | high/name |  |
| 5 | 3856020257064 | PILEĆA PRSA 60 G LINO NARESCI PODRAVKA | 60 g | 7 | 348 | 22,17–38,17 /kg | high/name |  |
| 6 | 3858892724316 | JELI PILEĆA PRSA 2600G,GAVRILOVIĆ | 2,6 kg | 7 | 217 | 3,84–10,50 /kg | high/name |  |
| 7 | 3850220115797 | FILE PILECEG ZABATKA 500 G PERUTNINA | 500 g | 6 | 621 | 7,18–11,18 /kg | high/name |  |
| 8 | 3850159110122 | PILECA PRSA BEZ KOZE PODLOZAK CEKIN 11012 |  | 6 | 391 | 6,49–9,95 /kg | low/unit_price |  |
| 9 | 3850159150531 | CHEF PIL FILE ZABATKA 400G CEKIN VINDIJA | 400 g | 6 | 86 | 12,48–13,98 /kg | high/name |  |
| 10 | 3850159120329 | CCA1,5KG CEKIN PIL. PRSA U OV. | 1,5 kg | 5 | 134 | 8,36–10,27 /kg | high/name |  |
| 11 | 3850159111327 | CCA0,5 KG PIL.FILE PODLOŽAK | 500 g | 5 | 24 | 22,76–31,98 /kg | high/ean |  |
| 12 | 3850159110580 | CCA1KG PILEĆI FILE | 1 kg | 4 | 312 | 10,59–14,19 /kg | high/ean |  |
| 13 | 3850159110313 | PILEĆI FILE OD PRSIJU SVJEŽE RFS, VINDIJA |  | 4 | 113 | 8,99–13,99 /kg | low/unit_price |  |
| 14 | 7894904055906 | SMRZNUTI PIL.FILE 2kg SEARA | 2 kg | 4 | 36 | 2,75–8,74 /kg | high/ean |  |
| 15 | 3850159110139 | PILEĆA PRSA SVJEŽA,KOKA RFZ |  | 3 | 108 | 5,99–8,99 /kg | low/unit_price |  |
| 16 | 3831006602717 | PILEĆI FILE 500 g NA PODLOŠKU DELAM | 500 g | 3 | 5 | 10,78–12,78 /kg | high/name |  |
| 17 | 3850220427579 | PILEĆI FILE SMRZNUTI 5kg PERUTNINA (2) | 10 kg | 2 | 146 | 4,50–6,20 /kg | high/name |  |
| 18 | 3850220428491 | PILEĆI FILE MIX 600 g | 600 g | 2 | 133 | 8,32–8,98 /kg | high/name |  |
| 19 | 3850220114608 | PILEĆI FILE PERUTNINA RFZ (5) |  | 2 | 118 | 5,49–6,51 /kg | low/unit_price |  |
| 20 | 3850220117517 | FILE PILEĆEG BATKA ZABATKA 500 g SVJEŽI PERUTNINA | 500 g | 2 | 79 | 8,38–11,98 /kg | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| SALAMA PILEĆA PRSA U OVITKU 500 g VINDIJA | 17 | `salam` |
| SALAMA PRSA PILEĆA 100 g VINDIVAC | 15 | `salam` |
| PILEĆA PRSA 220 g POLI KIDS PERUTNINA | 14 | `kids` |
| N-VIN.PIL.FILE ZABATAK 500G (PODLOŽAK) | 13 | `zabatak` |
| PRSA PILEĆA SLIM&FIT NARZAK 100 g PERUTNINA | 12 | `narzak` |
| SALAMA SLIM&FIT PILEĆA PRSA 400G | 11 | `salam` |
| DIMLJENA PILECA PRSA NAREZAK 100 G PERUTNINA | 9 | `narezak` |
| DIMCEK DIMLJENA PILECA PRSA 250 G CEKIN (12203) VINDIJA | 7 | `dimcek` |
| POESIE DELI SAUCE PILEĆI FILE 85G -23/1- VREĆICA | 7 | `poesie` |
| PILEĆI FILE SVJEŽI MINI 400G CEKIN | 6 | `mini\b` |

</details>

<a id="piletina"></a>
## piletina (cijelo pile, batak, zabatak, krila) (`piletina`)

jedinica: **kg** · loose_produce: **false** · grupa: **649** · isključenih grupa: **249**

sinonimi: piletina, pile, pileci batak, pileca krila, zabatak  
must_match: `pile\b | pilec batak | pileci batak | batak | zabatak | pilec krila | pileca krila | krilca | pileca zadnja | pilece meso | pilec zadnj`
atributi: dio = cijelo, batak, zabatak, krila

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850159111013 | CCA1-1,5KG PILE GRILL SMRZ | 1 kg | 10 | 48 | 2,67–5,25 /kg | high/name | dio=cijelo |
| 2 | 3850159112829 | CCA1,6KG CEKIN HRVATSKO PILE | 1 kg | 9 | 428 | 2,08–3,32 /kg | high/name | dio=cijelo |
| 3 | 3850220115773 | Međimursko pile - pileći batak 500g | 500 g | 7 | 635 | 3,98–6,98 /kg | high/name | dio=batak |
| 4 | 3850159110269 | PILECA KRILA PODLOZAK CEKIN (11026) |  | 7 | 344 | 5,49–7,89 /kg | low/unit_price | dio=krila |
| 5 | 3850159110054 | PILECI BATAK-ZABATAK PODLOZAK CEKIN (11005) | 1 kg | 7 | 317 | 4,79–6,89 /kg | high/ean | dio=batak |
| 6 | 3850159110085 | PILECI ZABATAK PODLOZAK CEKIN (11008) | 1 kg | 7 | 181 | 4,19–6,89 /kg | high/ean | dio=zabatak |
| 7 | 3850220115858 | PILEĆA KRILA 500 g SVJEŽA PERUTNINA | 500 g | 6 | 551 | 3,98–7,58 /kg | high/name | dio=krila |
| 8 | 3850159113123 | CCA1,8KG PILE ROSTER | 1,8 kg | 6 | 363 | 1,77–2,21 /kg | high/ean | dio=cijelo |
| 9 | 3850159142345 | PILEĆA KRILCA NAVIJAČKI BUCKET 650 g | 650 g | 6 | 196 | 9,22–17,37 /kg | high/name | dio=krila |
| 10 | 3850159113130 | PILE KALIB.1000 g VINDIJA | 1 kg | 6 | 151 | 3,31–3,32 /kg | high/name | dio=cijelo |
| 11 | 3850159111051 | CEKIN PILEĆI BATAK I ZABATAK PODLOŽAK SMRZNUTO, KOKA-VINDIJA | 1 kg | 6 | 29 | 4,39–6,29 /kg | high/ean | dio=batak |
| 12 | 3850220115780 | Međimursko pile - pileći zabatak 500g | 500 g | 5 | 484 | 3,98–7,58 /kg | high/name | dio=zabatak |
| 13 | 3850159110597 | CCA1-1,2KG PILEĆI BATAK | 1,2 kg | 5 | 261 | 3,49–5,16 /kg | high/ean | dio=batak |
| 14 | 3850159110511 | BATAK PILECI PODLOZAK CEKIN (11051) |  | 5 | 250 | 5,79–6,89 /kg | low/unit_price | dio=batak |
| 15 | 3850159150197 | ALABAMA BBQ PILECA KRILCA 450 G VINDIJA | 450 g | 5 | 158 | 4,87–11,76 /kg | high/name | dio=krila |
| 16 | 3850159111518 | BATAK KOKA 1 kg PIL.PODL.SM | 1 kg | 5 | 44 | 5,79–9,95 /kg | high/ean | dio=batak |
| 17 | 3850220111157 | PILE GRIL MEĐIMURSKO PODL PERUTNINA | 1 kg | 4 | 241 | 2,80–3,31 /kg | high/ean | dio=cijelo |
| 18 | 3850159113567 | PILEĆI BATAK ZABATAK OTKOŠTENI S KOŽOM |  | 4 | 185 | 7,69–9,59 /kg | low/unit_price | dio=batak |
| 19 | 3850159114557 | OTKOŠTENI BATAK/ZABATAK S KOŽOM RFS SVJ ,VINDIJA |  | 4 | 102 | 6,49–8,39 /kg | low/unit_price | dio=batak |
| 20 | 3850159111082 | CCA0,5KG PILEĆI ZABATAK PODL. | 1 kg | 4 | 27 | 6,00–11,56 /kg | high/name | dio=zabatak |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| KRILCA PILEĆA PEČENA SM 500 g CEKIN | 12 | `pecen` |
| HRANA ZA MAČKE SM PILE JET POV 1,5 kg FRISKIES | 6 | `hrana` |
| N-VIN.PIL.BATAK I FILE ZABATKA (PODLOŽAK) | 5 | `file\b` |
| GAVELINO PILE ZA PECENJE CEKIN (11315) | 4 | `pecen` |
| HRANA ZA MAČKE SM PILE POV 300g FRISKIES | 4 | `hrana` |
| PURECI BATAK MINI PAK VINDON (40400) | 4 | `mini\b` |
| PUREĆI BATAK OB.PAK PAK. VINDIJA kg | 4 | `purec` |
| 1KG KOTANYI ZAČIN PILEĆ KRILCA | 3 | `kotanyi` |
| FRISKIES ADL MAČKA MESO&PILE&POVRĆE 1,5KG | 3 | `friskies` |
| PILECA MINI KRILCA 450 G PERUTNINA | 3 | `mini\b` |

</details>

<a id="mljeveno_meso"></a>
## mljeveno meso (`mljeveno_meso`)

jedinica: **kg** · loose_produce: **false** · grupa: **108** · isključenih grupa: **0**

sinonimi: mljeveno meso, mljeveno, mljeveno mesano meso  
must_match: `mljeveno meso | meso mljeveno | mljeveno mijesano | mljeveno junece | mljeveno svinjsko | mljeveno purece | mljeveno pilece | mljeveno telece | mljev meso`
atributi: vrsta = mijesano, junece, svinjsko, purece, pilece, telece

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850339413043 | PURECE MLJEVENO MESO 500 G VINDON (41304) | 500 g | 18 | 981 | 9,98–13,98 /kg | high/name | vrsta=purece |
| 2 | 3850159112423 | N-VIN. PILEĆE MLJEVENO MESO 450G -4/1- | 450 g | 11 | 327 | 7,31–11,98 /kg | high/name | vrsta=pilece |
| 3 | 3850139540642 | N-MLJEVENO MESO PIK 540G MIJEŠANO -4/1- MAP | 540 g | 8 | 484 | 7,57–12,20 /kg | high/name | vrsta=mijesano |
| 4 | 3850139540635 | PIK MLJEVENO MIJEŠANO MESO 540g | 540 g | 6 | 419 | 7,39–10,91 /kg | high/name | vrsta=mijesano |
| 5 | 3850139443448 | MIJEŠANO MLJEVENO MESO 850 g (MA) MP PIK | 850 g | 6 | 297 | 7,40–9,75 /kg | high/name | vrsta=mijesano |
| 6 | 3850139540628 | N-MLJEVENO MESO PIK 540G JUNEĆE -4/1- MAP | 540 g | 6 | 279 | 10,54–14,91 /kg | high/name | vrsta=junece |
| 7 | 3850139540598 | SVINJSKO MLJEVENO MESO 540g PIK | 540 g | 4 | 369 | 3,87–4,11 /kg | high/name | vrsta=svinjsko |
| 8 | 3850139435917 | MIJEŠ MLJEV MESO 850g MA PIK VRBOVEC (6) | 850 g | 4 | 320 | 4,69–10,46 /kg | high/name | vrsta=mijesano |
| 9 | 3850139446517 | MIJESANO MLJEVENO MESO E540 G LIGHT | 540 g | 2 | 265 | 11,09–11,65 /kg | high/name | vrsta=mijesano |
| 10 | 3858890183573 | MIJESANO MLJEVENO MESO E450 G MAP | 450 g | 2 | 159 | 6,64–9,98 /kg | high/name | vrsta=mijesano |
| 11 | 3858881612198 | MIJESANO MLJEVENO MESO E850 G MAP | 850 g | 2 | 157 | 7,05–8,58 /kg | high/name | vrsta=mijesano |
| 12 | 3858881613805 | PPK JUNEĆE MLJEVENO MESO 450 g | 450 g | 2 | 136 | 9,98–12,42 /kg | high/name | vrsta=junece |
| 13 | 3850139415438 | JUN MLJEV MESO 850g MA PIK VRBOVEC | 850 g | 2 | 117 | 11,52–12,24 /kg | high/name |  |
| 14 | 3859893068461 | MIJEŠANO MLJEVENO MESO 450 g | 450 g | 2 | 57 | 8,20–9,31 /kg | high/name | vrsta=mijesano |
| 15 | 3850139286281 | MIJEŠANO MLJEVENO MESO 1 KG | 1 kg | 2 | 14 | 6,29–7,49 /kg | high/name | vrsta=mijesano |
| 16 | 3850339413081 | PUREĆE MLJEVENO MESO 700g | 700 g | 1 | 184 | 7,56 /kg | high/name | vrsta=purece |
| 17 | 3850139280371 | MIJEŠANO MLJEVENO MESO 750 g K PLUS | 750 g | 1 | 182 | 5,85 /kg | high/name | vrsta=mijesano |
| 18 | 3856031235877 | MIJESANO MLJEVENO MESO E500 G | 500 g | 1 | 155 | 6,38 /kg | high/name | vrsta=mijesano |
| 19 | 3856031235891 | JUNECE MLJEVENO MESO E500 G | 500 g | 1 | 155 | 11,98 /kg | high/name | vrsta=junece |
| 20 | 3856031235914 | SVINJSKO MLJEVENO MESO E500 G | 500 g | 1 | 154 | 3,98 /kg | high/name | vrsta=svinjsko |

<a id="svinjetina"></a>
## svinjetina (svježe meso) (`svinjetina`)

jedinica: **kg** · loose_produce: **false** · grupa: **488** · isključenih grupa: **99**

sinonimi: svinjetina, svinjsko meso, svinjski vrat, svinjski but, svinjska lopatica, svinjski kotlet  
must_match: `svinjetin | svinjski vrat | svinjski but | svinjska lopatic | svinjski kotlet | svinjsko meso | svinjski file | svinjska rebra | svinjski karee | svinjski lungic | sv vrat | sv but | sv lopatic | sv kotlet | sv karee`
atributi: dio = vrat, but, lopatica, kotlet, rebra, file

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850139540444 | N-SVINJSKI VRAT SK PIK 640G ODREZAK -3/1- MAP | 640 g | 7 | 308 | 6,08–9,98 /kg | high/name | dio=vrat |
| 2 | 3850139437508 | SV VRAT SK NAR 640g PIK VRBOVEC (6) | 640 g | 6 | 561 | 6,08–9,67 /kg | high/name | dio=vrat |
| 3 | 3850139540901 | SVINJSKI FILE VP PIK VRBOVEC kg |  | 5 | 86 | 5,99–11,89 /kg | low/unit_price | dio=file |
| 4 | 3858890182606 | PPK SVINJSKI BUT BK ODREZAK 600 g | 600 g | 3 | 156 | 6,65–8,15 /kg | high/name | dio=but |
| 5 | 3850139541441 | N-SVINJSKI VRAT BK ODR PIK 560G (MA) MP -3/1- | 560 g | 3 | 4 | 9,09–9,45 /kg | high/name | dio=vrat |
| 6 | 3850139437942 | MARIN SVINJSKA REBRA(VAKM) (5) |  | 2 | 195 | 6,51–9,59 /kg | low/unit_price | dio=rebra |
| 7 | 3831020349414 | SVINJSKI VRAT MARINIRANI 460 g | 460 g | 2 | 188 | 11,93–15,63 /kg | high/name | dio=vrat |
| 8 | 3850139281453 | SV BUT BK 4D I KAT (20) |  | 2 | 113 | 2,99–4,38 /kg | low/unit_price | dio=but |
| 9 | 3858881612389 | CCA2,5KG SVINJSKI VRAT BK VP | 2,5 kg | 2 | 109 | 1,74–2,20 /kg | high/ean | dio=vrat |
| 10 | 3850139523010 | SVINJSKI BUT SK U KOŽI DALM.OBR PIK |  | 2 | 104 | 4,91–5,89 /kg | low/unit_price | dio=but |
| 11 | 3850139523003 | SVINJSKI BUT SK U KOŽI NEOB. RAV. R |  | 2 | 103 | 3,49–4,65 /kg | low/unit_price | dio=but |
| 12 | 3850139523423 | SVJEŽA SVINJSKA REBRA PIK VRBOVEC |  | 2 | 103 | 5,99–6,99 /kg | low/unit_price | dio=rebra |
| 13 | 3850139431469 | SV LOPATICA BK 4D UVOZ (VAK) |  | 2 | 16 | 4,38 /kg | low/unit_price | dio=lopatica |
| 14 | 3850139540918 | CCA0,5KG SVINJSKI FILE VP | 1 kg | 2 | 16 | 11,49–229,75 /kg | high/name | dio=file |
| 15 | 3850139436914 | SVINJSKI VRAT BEZ KOSTI PIK |  | 2 | 7 | – | – | dio=vrat |
| 16 | 3859893378447 | SVINJSKI BUT SK U KOŽI DALM.OBR MM | 12 kg | 2 | 5 | 0,34–0,41 /kg | high/name | dio=but |
| 17 | 3850139540925 | SVINJSKI FILE VAC |  | 1 | 186 | 5,99–10,99 /kg | low/unit_price | dio=file |
| 18 | 3850139445770 | SV VRAT BK ODR 560g PIK | 560 g | 1 | 177 | 7,66 /kg | high/name | dio=vrat |
| 19 | 3850139442106 | SV.BUT BK ODREZAK E400 G MAP | 400 g | 1 | 148 | 7,93 /kg | high/name | dio=but |
| 20 | 3856021231254 | SVINJSKI FILE HR VP |  | 1 | 135 | 8,89 /kg | low/unit_price | dio=file |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| ZAČIN ZA SVINJETINU 30G VEGETA NATUR (18) | 13 | `zacin` |
| HAŠE OD SVINJETIN LIM.200 g PODRAVKA | 11 | `lim\b` |
| GOTOVA JELA AJINOMOTO RAMEN SVINJETINA 62G JUHA U ČAŠI | 8 | `juha` |
| ZACIN ZA SVINJETINU QUICK EASY 30 G KOTANYI | 8 | `kotanyi` |
| Ajinmoto Gyoza sa svinjetinom 600 g | 3 | `svinjetinom` |
| HRANA ZA PSE GOVEDINA I SVINJETINA 7 kg PREMIUM KONY | 3 | `pse\b` |
| SVINJETINA TRGANA SPORO KUHANA 500 g VAK PIK ( PULLED PORK ) | 3 | `kuhan` |
| BIBIGO GYOZA SA SVINJETINOM 600g | 2 | `svinjetinom` |
| HRANA ZA MAČKE GOVEDINA I SVINJETINA 2 kg KONY | 2 | `macke` |
| POSLASTICA ZA PSE GOVEDINA I SVINJETINA 100 g PREMIUM KONY | 2 | `pse\b` |

</details>

<a id="junetina"></a>
## junetina / govedina (svježe meso) (`junetina`)

jedinica: **kg** · loose_produce: **false** · grupa: **74** · isključenih grupa: **387**

sinonimi: junetina, govedina, junece meso, govede meso, junetina za gulas  
must_match: `junetin | govedin | junec but | junec vrat | junec lopatic | junec gulas | junec ramstek | junec rebr | junec file | junec meso | goveda prsa | govede meso | junec\b`
atributi: dio = but, vrat, lopatica, gulas, file, rebra

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3856021210310 | Junetina za gulaš |  | 1 | 138 | 16,29 /kg | low/unit_price | dio=gulas |
| 2 | plodine:897198 | EMPANADA S JUNETINOM 75 G SPICY FLUXUS | 75 g | 1 | 121 | 15,87 /kg | high/name |  |
| 3 | plodine:901318 | JUNETINA S GRASKOM I MRKVOM I PIRE KRUMPIR PORCIJA |  | 1 | 121 | – | – |  |
| 4 | 4056489686194 | Empanadas s junetinom | 200 g | 1 | 116 | 14,95 /kg | high/unit |  |
| 5 | 4056489883388 | Sušena Angus govedina | 70 g | 1 | 116 | 25,57 /kg | high/unit |  |
| 6 | plodine:896904 | PROLJETNE ROLICE JUNETINA I CURRY SPICY100 G FLUXUS | 100 g | 1 | 108 | 10,50–14,30 /kg | high/name |  |
| 7 | tommy:10020769 | GOVEĐA PRSA |  | 1 | 63 | 4,25 /kg | low/unit_price | dio=rebra |
| 8 | eurospin:070029101 | MIX JUNETINE ZA JUHU |  | 1 | 43 | 8,99 /kg | low/unit_price |  |
| 9 | 3379670024072 | GOVEDINA USOLJENA 340g | 340 g | 1 | 43 | 9,97 /kg | high/name |  |
| 10 | eurospin:910164401 | MIX JUNETINE ZA JUHU (S REBRIMA) |  | 1 | 43 | 10,49 /kg | low/unit_price | dio=rebra |
| 11 | 3379670024324 | GOVEDINA USOLJENA LIGHT 340g | 340 g | 1 | 43 | 11,74 /kg | high/name |  |
| 12 | 8006013986234 | *MEZZELUNE JUNETINA MERLOT 250g. | 250 g | 1 | 43 | 12,76 /kg | high/name |  |
| 13 | 8017596107596 | INSTANT TJESTENINA GOVEDINA 65g | 65 g | 1 | 43 | 15,23 /kg | high/name |  |
| 14 | eurospin:070209001 | MLADA JUNETINA BUT RUŽA BK |  | 1 | 43 | 16,99 /kg | low/unit_price | dio=but |
| 15 | 3379670026182 | USOLJENA GOVEDINA LIGHT 200G | 200 g | 1 | 43 | 19,95 /kg | high/name |  |
| 16 | 8013554114187 | BURRITO S JUNETINOM 320 g | 320 g | 1 | 28 | 21,84–27,78 /kg | high/name |  |
| 17 | 3858892822715 | SUŠENA GOVEDINA ANDRO NAR 90g | 90 g | 1 | 15 | 44,33 /kg | high/name |  |
| 18 | plodine:185166 | JUNETINA BK 2 |  | 1 | 14 | 12,00 /kg | low/unit_price |  |
| 19 | ribola:0122385 | GOVEDINA SUHA BEZ KOSTI |  | 1 | 10 | 9,29 /kg | low/unit_price |  |
| 20 | studenac:173298 | JUNETINA S GRAŠKOM I MRKVOM kg |  | 1 | 8 | 5,40–10,00 /kg | low/unit_price |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| HRANA ZA MAČKE FANTASTIC GOVEDINA 85 g FELIX | 17 | `macke` |
| HRANA ZA MAČKE FRISKIES GOVEDINA 85 g MOKRA ALCA | 17 | `macke` |
| HRANA ZA MAČ. WHISKAS 1,4 kg DRY GOVEDINA1+ ATL | 16 | `hrana` |
| PEDIGREE MH ZA PSE GOVEDINA 100G VREĆICA | 14 | `pse\b` |
| HRANA ZA MAČ. DREAMIES GOVEDINA 60 g ATLA | 12 | `hrana` |
| HRANA ZA MAČKE 1+ GOVEDINA 300 g WHISKAS | 12 | `macke` |
| WHISKAS MH ZA MAČKE 1+ GOVEDINA U UMAKU 85G VREĆICA | 12 | `macke` |
| HRANA ZA MAČKE PURE DELIGHT VR GOVEDINA 85g WHISKAS | 11 | `macke` |
| POSLASTICA ZA PSE RODEO GOVEDINA 123 g PEDIGREE | 11 | `pse\b` |
| HRANA ZA PSE ADULT GOVEDINA/POVRĆE 500 g PEDIGREE | 10 | `pse\b` |

</details>

<a id="slanina"></a>
## slanina / panceta (`slanina`)

jedinica: **kg** · loose_produce: **false** · grupa: **704** · isključenih grupa: **79**

sinonimi: slanina, panceta, spek, bacon  
must_match: `slanin | pancet | spek\b | bacon`
atributi: oblik = narezana, kockice

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850133800827 | N-SLANINA NAREZAK 90G -14/1- DOBRO | 90 g | 19 | 817 | 13,22–44,33 /kg | high/name | oblik=narezana |
| 2 | 3850133808014 | SLAVONSKA SLANINA NARESCI 250 g DOBRO 26568 | 250 g | 12 | 523 | 16,00–36,76 /kg | high/name | oblik=narezana |
| 3 | 3856020272760 | PODRAVSKI ŠPEK 350 GR VP PODRAVKA | 350 g | 11 | 543 | 14,26–22,43 /kg | high/name |  |
| 4 | 3850133817474 | ŠPEK KARE NARESCI 90G DOBRO -14/1- | 90 g | 11 | 290 | 26,56–34,33 /kg | high/name | oblik=narezana |
| 5 | 3850133813292 | N-PANCETA NARESCI 90G DOBRO -14/1- | 90 g | 11 | 278 | 11,89–47,67 /kg | high/name | oblik=narezana |
| 6 | 3858894290307 | ISTARSKA PANCETA NAREZAK 230 g PISINUM GP531 | 230 g | 10 | 408 | 23,87–46,91 /kg | high/name | oblik=narezana |
| 7 | 3850257053253 | BELJE BARANJSKA SLANINA NAREZAK 100G MAP -7/1- | 100 g | 9 | 637 | 24,10–38,90 /kg | high/name | oblik=narezana |
| 8 | 3858889495113 | DALMATINSKA PANCETA REZANA 80 G VOSTANE | 80 g | 9 | 412 | 27,38–46,13 /kg | high/name | oblik=narezana |
| 9 | 3858881227408 | PANCETA DALMATINSKA NARESCI 100g GAVRILOVIĆ | 100 g | 9 | 411 | 23,90–34,90 /kg | high/name | oblik=narezana |
| 10 | 3858884931890 | ISTARSKA PANCETA NAREZAK MAP 80 g PISINIUM GP203 | 80 g | 9 | 262 | 24,88–48,63 /kg | high/name | oblik=narezana |
| 11 | 3856020245559 | PANCETA NARESCI MAJSTOR 80 g PODRAVKA | 80 g | 9 | 240 | 21,50–41,88 /kg | high/name | oblik=narezana |
| 12 | 3858894291809 | ISTARSKA PANCETA S OKUSOM TARTUFA MAP 80 G PISINIUM | 80 g | 8 | 301 | 32,38–53,13 /kg | high/name |  |
| 13 | 3850139030266 | DALMATINSKA PANCETA CCA 350G VAK.-PIK |  | 8 | 267 | 20,99–64,26 /kg | low/unit_price |  |
| 14 | 3850133800834 | N-PANCETA ROLANA NAREZAK 90G-14/1- DOBRO | 90 g | 8 | 221 | 10,33–36,89 /kg | high/name | oblik=narezana |
| 15 | 3856020241605 | HAMBURGER PODRAVSKI ŠPEK 100G PODRAVKA | 100 g | 8 | 198 | 20,80–29,90 /kg | high/name | oblik=narezana |
| 16 | 3850139522037 | PIK PANCETA 100 G PIK VRBOVEC | 100 g | 8 | 190 | 19,10–35,90 /kg | high/name | oblik=narezana |
| 17 | 3858884937298 | ISTARSKA PANCETA VP 200 g kom PISINIUM GP338 | 200 g | 7 | 293 | 25,65–39,45 /kg | high/name |  |
| 18 | 3859892946197 | ŠPEK DOMAĆI DIMLJENI E100 g MAP MEDVEN | 100 g | 7 | 290 | 22,90–36,90 /kg | high/name | oblik=narezana |
| 19 | 3859893167249 | HISTRIS ISTARSKA PANCETA 80G -8/1- | 80 g | 6 | 328 | 32,38–52,38 /kg | high/name |  |
| 20 | 3850133816750 | PANCETA NARESCI 150 g DOBRO | 150 g | 6 | 160 | 15,27–28,60 /kg | high/name | oblik=narezana |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| KREKERI SALTAS BACON 100G KOESTLIN | 19 | `kreker` |
| GRAH SA SLANINOM CARNEX 400 g (11) | 18 | `grah` |
| GOTOVA JELA GRAH S DIMLJENOM SLANINOM 300G GAVRILOVIĆ | 17 | `grah` |
| KREKER TUC 100G BACON/ŠPEK -24/1- | 17 | `kreker` |
| N-ČIPS PRINGLES 165G BACON -19/1- | 8 | `cips` |
| CIPS POMSTICKS SLANINA 85 G LORENZ | 4 | `cips` |
| ČIPS HRUSK REBRASTI BACON 150 g VREĆICA NTL | 4 | `cips` |
| POSLASTICA ZA PSE BACON STRIP 100 g SUPER PAWER | 3 | `pse\b` |
| Pivac Roštilj kobasica sir i špek 360 g | 3 | `kobas` |
| SMOKI CHIO TACCOS BACON 65 g INTERSNACK | 3 | `smoki` |

</details>

<a id="sunka"></a>
## šunka (kuhana) (`sunka`)

jedinica: **kg** · loose_produce: **false** · grupa: **921** · isključenih grupa: **199**

sinonimi: sunka, kuhana sunka  
must_match: `sunka\b | sunke\b | sunk\b`
atributi: vrsta = kuhana, pileca, pureca, delikates; oblik = narezana

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850139360516 | ŠUNKA KUHANA NAR 125g MA PIK VRBOVEC (10) | 125 g | 22 | 1051 | 15,92–24,72 /kg | high/name | vrsta=kuhana, oblik=narezana |
| 2 | 3850139250671 | N-VRB ŠUNKA FINA 150G PIK NAREZAK -10/1 | 150 g | 22 | 970 | 16,60–27,27 /kg | high/name | oblik=narezana |
| 3 | 3850139171051 | SUNKA U OVITKU NAREZAK 125 G MA PIK VRBOVEC | 125 g | 20 | 994 | 11,92–24,72 /kg | high/name | oblik=narezana |
| 4 | 3850159128813 | PUREĆA DELUXE ŠUNKA CLASSIC 100 g VINDON 12881 | 100 g | 19 | 926 | 15,90–31,90 /kg | high/name | vrsta=pureca |
| 5 | 3850139173550 | PIK ŠUNKA U OVITKU 350G,PIK VRBOVEC, | 350 g | 19 | 793 | 9,97–16,71 /kg | high/name |  |
| 6 | 3858890209679 | N-GAV ŠUNKA MANDOLINA 340G-24/1 LIM GAVRILOVIĆ | 340 g | 19 | 688 | 13,21–24,09 /kg | high/name |  |
| 7 | 3858892721292 | ŠUNKA U OVITKU 350G GAVRILOVIĆ (6) | 350 g | 19 | 664 | 11,54–17,11 /kg | high/name |  |
| 8 | 3850139520453 | ŠUNKA PUREĆA DIMLJENA 100 g MA PIK VRBOVEC | 100 g | 18 | 902 | 12,90–35,90 /kg | high/name | vrsta=pureca, oblik=narezana |
| 9 | 3850139520316 | ŠUNKA PUREĆA CLASSIC 100 g MA PIK VRBOVEC | 100 g | 18 | 873 | 14,90–30,90 /kg | high/name | oblik=narezana, vrsta=pureca |
| 10 | 3850159123153 | N-VIN PILEĆA DE LUX ŠUNKA CLASSIC 100G -10/1- | 100 g | 17 | 862 | 18,50–27,90 /kg | high/name | vrsta=pileca |
| 11 | 3858881227927 | ŠUNKA NAREZAK LIM. GAVRILOVIĆ 150 g | 150 g | 17 | 806 | 11,27–18,60 /kg | high/name | oblik=narezana |
| 12 | 3850139350401 | PECENA SUNKA 125 G NAREZAK PIK VRBOVEC | 125 g | 16 | 771 | 17,52–30,32 /kg | high/name | oblik=narezana |
| 13 | 3850139171723 | N-VRB ŠUNKA PIK DELIKATES 150G NAREZAK -10/1 | 150 g | 16 | 620 | 13,73–24,60 /kg | high/name | oblik=narezana, vrsta=delikates |
| 14 | 3858890203295 | PURECA SUNKA STANCIJA NAREZAK 100 G GAVRILOVIC | 100 g | 14 | 580 | 6,90–30,90 /kg | high/name | oblik=narezana, vrsta=pureca |
| 15 | 3858886467731 | ŠUNKA NAREZAK LIMENKA 150 G (15) PODRAVKA | 150 g | 14 | 507 | 10,27–16,60 /kg | high/name | oblik=narezana |
| 16 | 3858890207002 | N-GAV ŠUNKA NAREZAK PIKANT 150G -45/1- | 150 g | 14 | 471 | 10,13–18,60 /kg | high/name | oblik=narezana |
| 17 | 3858886465713 | SUNKA U OVITKU 350 G PODRAVKA | 350 g | 14 | 389 | 8,80–16,26 /kg | high/name |  |
| 18 | 3856020241452 | N-DAN ŠUNKA U OVITKU 100G NARESCI VP -10/1- | 100 g | 14 | 385 | 17,90–22,90 /kg | high/name | oblik=narezana |
| 19 | 3850139522754 | ŠUNKA U OVITKU SLJEME 350 g (12) PIK VRBOVEC | 350 g | 13 | 591 | 7,11–12,26 /kg | high/name |  |
| 20 | 3858892721315 | SUNKA ZA PIZZU 350 G GAVRILOVIC | 350 g | 13 | 565 | 8,54–11,49 /kg | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| SIR TOPLJENI ZDENKA ŠUNKA 140 g ZDENKA | 17 | `sir\b` |
| N-VIVIS SVJEŽI KREM SIR 100G5892 ŠUNKA -22/1- | 16 | `sir\b` |
| SIR ABC SUNKA 100 G BELJE ZVIJEZDA | 13 | `sir\b` |
| KREKERI TUC BACON ŠUNKA 100G | 8 | `kreker` |
| SIRNI NAMAZ 150G ŠUNKA Z'BREGOV VINDIJA | 8 | `namaz` |
| FANT ZAP.TJ.ŠUNKA, SIR 40 g PODRAVKA (24) | 7 | `sir\b` |
| SENDVIČ PANE AMORE ŠUNKA SIR 130G (6) | 6 | `sendvic` |
| SALATA TJESTENINA ŠUNK STRIBOR 255 g | 5 | `salata` |
| KREKERI CROCO SUNKA 100 G | 4 | `kreker` |
| POSLASTICA ZA MAČKE FELIX PLAY TUBES PURETINA&ŠUNKA 50G | 4 | `macke` |

</details>

<a id="tuna"></a>
## tuna (konzerva) (`tuna`)

jedinica: **kg** · loose_produce: **false** · grupa: **490** · isključenih grupa: **242**

sinonimi: tuna, tunjevina  
must_match: `tuna\b | tune\b | tunj`
atributi: oblik = komadi, file, sjeckana; preljev = ulje, vlastiti_sok

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 8004030595033 | TUNA KOMADI NATURALE RIO MARE 160 g (OCIJEĐENA MASA 122 g) ORBICO | 160 g | 21 | 1225 | 10,94–40,75 /kg | high/name | preljev=vlastiti_sok, oblik=komadi |
| 2 | 3856020263096 | EVA TUNA FILETI U BILJNOM ULJU 100G (30) (PAL 161) | 100 g | 21 | 923 | 30,90–62,71 /kg | high/name | oblik=file, preljev=ulje |
| 3 | 8004030595002 | TUNA KOMADI U SUNCOKRET. ULJU RIO MARE 160 g (OCIJEĐENA NASA 122 g) ORBICO | 160 g | 20 | 1236 | 10,94–43,66 /kg | high/name | preljev=ulje, oblik=komadi |
| 4 | 3850104267031 | EVA TUNA KOMADIĆI USITNJ.160G/112G, (48) (PAL 54)PODRAVKA | 160 g | 20 | 798 | 9,06–25,45 /kg | high/name | preljev=ulje, oblik=komadi |
| 5 | 8594012796515 | TUNA ŽUTOPERAJNA ODREZ. U SUNC. ULJU 170g (OCJ. MASA 120g)GIANA | 170 g | 18 | 836 | 12,88–31,27 /kg | high/name | preljev=ulje, oblik=file |
| 6 | 8004030345775 | N-TUNA RIO MARE 3*80G (NETTO3*52G)U MAS.ULJU -6/1 | 240 g | 18 | 776 | 20,79–106,58 /kg | high/name | preljev=ulje |
| 7 | 8004030100213 | N-TUNA RIO MARE 2*80G(NETTO 2*52G)U MAS.ULJU-24/1 | 160 g | 16 | 719 | 17,44–52,79 /kg | high/name | preljev=ulje |
| 8 | 3856020263126 | EVA TUNA FILETI U MASLINOVOM ULJU 100G (30)(PAL690) PODRAVKA | 100 g | 16 | 454 | 18,52–61,29 /kg | high/name | preljev=ulje, oblik=file |
| 9 | 8004030044005 | N-TUNA RIO MARE 160G U MAS.ULJU(netto 104g) -12/1 | 160 g | 16 | 444 | 19,88–41,25 /kg | high/name | preljev=ulje |
| 10 | 8595241527901 | TUNA ODREZAK U MASLINOVOM ULJU FRANZ JOSEF 150g-ocijeđ.mase 102g | 150 g | 15 | 795 | 14,60–32,84 /kg | high/name | preljev=ulje |
| 11 | 3856020278229 | TUNA STEAK KOMADI U BILJNOM ULJU 160g EVA PODRAVKA | 160 g | 14 | 750 | 8,44–35,48 /kg | high/name | preljev=ulje, oblik=komadi |
| 12 | 8004030005051 | N-TUNA RIO MARE ULJE 4*80G UMASLINOVOM ULJ(NETTO 4*52G) | 320 g | 14 | 749 | 15,59–34,34 /kg | high/name | preljev=ulje |
| 13 | 3850160108064 | TUNA FILET BILJNO ULJE 105 G ADRIATIC QUEEN SARDINA POSTIRA | 105 g | 14 | 690 | 36,10–77,41 /kg | high/name | preljev=ulje, oblik=file |
| 14 | 3856020263218 | EVA TUNA U UMAKU OD RAJČICE 100G (30)(PAL690) PODRAVKA | 100 g | 14 | 411 | 19,50–36,43 /kg | high/name |  |
| 15 | 80040248 | RIB.K.TUNA MASL.ULJE 80 g ( 0,052 g) RIO MARE ORBI | 80 g | 14 | 363 | 17,37–63,27 /kg | high/name | preljev=ulje |
| 16 | 3850104231506 | EVA TUNA KOMADI U ULJU 160G/112G (24) (PAL 117) PODRAVKA | 160 g | 14 | 336 | 10,62–166,61 /kg | high/name | oblik=komadi, preljev=ulje |
| 17 | 8004030344570 | N-TUNA RIO MARE NATURALE4*80G (NETTO 4*56G)-12/1 3503 | 320 g | 13 | 628 | 15,59–42,81 /kg | high/name | preljev=vlastiti_sok |
| 18 | 3850160108538 | TUNA FILET MASLINOVOM ULJE 105 G ADRIATIC QUEEN SARDINA POST | 105 g | 13 | 545 | 21,71–71,97 /kg | high/name | oblik=file, preljev=ulje |
| 19 | 8595241527857 | TUNA FRANZ JOSEF U SUNCOK.ULJU 4X80g - ocijeđ mase 4X52g | 320 g | 12 | 566 | 12,47–23,51 /kg | high/name | preljev=ulje |
| 20 | 8004030381681 | N-TUNA RIO MARE 2*160G MASLINULJE-24/1(NETTO2*104G) 35006 | 320 g | 12 | 490 | 21,22–36,01 /kg | high/name | preljev=ulje |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| ART PAŠTETA TUNA 100 g GAVRILOVIĆ (16) | 24 | `pasteta` |
| EVA TUNA S POVRĆEM U UMAKU OD RAJČICE 100G (30)(PAL690) | 22 | `povrce` |
| PAŠTETA TUNA 95G ARGETA DROGA KOLINSKA | 22 | `pasteta` |
| N-PAŠTETA RIO MARE 100G TUNA-12/1- TUBA 35050 | 20 | `pasteta` |
| EVA TUNA PAŠTETA CLASSIC 95G (22) (PAL 1449PODRAVKA | 19 | `pasteta` |
| N-PAŠTETA ARGETA 45G TUNA -20/1- | 19 | `pasteta` |
| N-PAŠTETA GAVRILOVIĆ TUNA 100G JUNIOR -16/1- | 19 | `pasteta` |
| RIB.K. EVA TUNA SALATA MEDITERANA 160 g PODR | 19 | `salata` |
| TUNA SALATA MEXICO 185 GR (48) (PAL 63) | 19 | `salata` |
| EVA TUNA SALATA MEXICANA 160G (8) (PAL 297)=PODRAVKA, | 17 | `salata` |

</details>

<a id="grah"></a>
## grah (`grah`)

jedinica: **kg** · loose_produce: **false** · grupa: **417** · isključenih grupa: **191**

sinonimi: grah, grah zrno, crveni grah, bijeli grah  
must_match: `grah\b | graha\b | grah zrn`
atributi: vrsta = bijeli, crveni, sareni, smedi, crni; oblik = konzerva

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850104025389 | GRAH SMEĐI 800g LIM.PODRAVKA-ocijeđene mase 460g | 460 g | 23 | 1390 | 2,06–6,07 /kg | high/name | oblik=konzerva, vrsta=smedi |
| 2 | 3850104020780 | GRAH BIJELI 800g LIM.PODRAVKA-ocijeđene mase 460g | 460 g | 23 | 1014 | 1,95–5,63 /kg | high/name | vrsta=bijeli, oblik=konzerva |
| 3 | 3850104024870 | GRAH SMEĐI 400g LIM.PODRAVKA-ocijeđene mase 230g | 230 g | 22 | 1099 | 2,38–8,13 /kg | high/name | vrsta=smedi, oblik=konzerva |
| 4 | 3850104020759 | GRAH CRVENI 400g LIM PODRAVKA-OCIJEĐENA MASA 230g | 400 g | 21 | 882 | 3,23–8,65 /kg | high/name | vrsta=crveni, oblik=konzerva |
| 5 | 3850104020728 | GRAH CRVENI 800 g LIM PODRAVKA OC MASA 460 g (12) | 800 g | 20 | 767 | 2,86–6,50 /kg | high/name | oblik=konzerva, vrsta=crveni |
| 6 | 3850104020797 | GRAH BIJELI 400g LIM.PODRAVKA-OCIJEĐENA MASA 230g | 400 g | 19 | 855 | 2,23–8,13 /kg | high/name | vrsta=bijeli, oblik=konzerva |
| 7 | 3856015309679 | N-GRAH SMEĐI ZVIJEZDA 800G 480G ČVRSTE TVARI -12/1- | 800 g | 14 | 607 | 2,11–4,98 /kg | high/name | vrsta=smedi, oblik=konzerva |
| 8 | 8595241511276 | GRAH ŠARENI 800 gr (OCJ. MASA 480 g) GIANA | 800 g | 12 | 653 | 1,49–4,77 /kg | high/name | vrsta=sareni, oblik=konzerva |
| 9 | 3850104025396 | GRAH SMEĐI 2500 g OCJ.MASA 1450 g PODRAVKA | 2,5 kg | 11 | 42 | 2,11–5,80 /kg | high/name | vrsta=smedi, oblik=konzerva |
| 10 | 3859893124501 | GRAH ŠARENI 500G NATURA, MARJAN VOĆE | 500 g | 10 | 393 | 1,98–4,98 /kg | high/name | vrsta=sareni |
| 11 | 3856015309648 | N-GRAH SMEĐI ZVIJEZDA 400G 240G ČVRSTE TVARI -12/1- | 400 g | 10 | 329 | 1,85–6,63 /kg | high/name | oblik=konzerva, vrsta=smedi |
| 12 | 3856020243432 | GRAH CRNI LIMENKA 400 g PODR | 400 g | 10 | 226 | 2,38–5,48 /kg | high/name | oblik=konzerva, vrsta=crni |
| 13 | 3850104275654 | GRAH CRV 2500 g NETO OC MASA 1450 g PODRAVKA (6) | 2,5 kg | 10 | 28 | 2,38–49,90 /kg | high/name | oblik=konzerva, vrsta=crveni |
| 14 | 3083680496117 | CRVENI GRAH 120 g LIM.BONDUELLE | 200 g | 9 | 386 | 3,95–15,75 /kg | high/name | oblik=konzerva, vrsta=crveni |
| 15 | 3083680009508 | N-GRAH BONDUELLE 400G CRVENI(NETTO 240G) -12/1 | 400 g | 9 | 379 | 4,22–9,67 /kg | high/name | vrsta=crveni |
| 16 | 3850104283536 | GRAH BIJELI KRUPNI 400 g (OCJ. MASA 230 g) PODRA | 400 g | 8 | 424 | 3,00–3,98 /kg | high/name | vrsta=bijeli, oblik=konzerva |
| 17 | 3859890236375 | GRAH ŠARENI 800G/480G, LARA(792) | 800 g | 7 | 58 | 2,13–3,31 /kg | high/name | vrsta=sareni |
| 18 | 3850104020766 | GRAH BIJELI LIM. 2.5 kg PODRAVKA OC. MASA 1450 g | 2,5 kg | 7 | 15 | 1,48–2,88 /kg | high/name | vrsta=bijeli, oblik=konzerva |
| 19 | 8594012794948 | GRAH SARENI 400 G GIANA LIMENKA | 400 g | 6 | 253 | 1,22–2,73 /kg | high/name | vrsta=sareni, oblik=konzerva |
| 20 | 3858894141869 | GRAH ŠARENI E BUONO 800 g 12/1 | 800 g | 6 | 252 | 1,24–3,73 /kg | high/name | vrsta=sareni |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| FANT ZA GRAH I VARIVA 60G (20) (PAL 145) PODRAVKA | 24 | `variva` |
| GRAH S KOBASICOM 400G (15), (PAL 81)PODRAVKA | 22 | `kobasic` |
| GOT. JELO GRAH S KOBAS. CARNEX 400 g | 21 | `carnex` |
| GRAH S GAVRILOVIĆ KOBASICOM 300g GAVRILOVIĆ | 21 | `kobasic` |
| GRAH S HAMBURGEROM 400G (15) (PAL 81), PODRAVKA | 21 | `hamburger` |
| GOT. JELO GRAH SA SLAN. CARNEX 400 g | 20 | `carnex` |
| GOTOVA JELA GRAH S DIMLJENOM SLANINOM 300G GAVRILOVIĆ | 20 | `slanin` |
| GRAH CRVENI I KUKUR. U MEKSIČ.UMAKU 430g BONDUELE - ocijeđena masa 200g | 16 | `umak` |
| TUNA SALATA GRAH BOWL 160G INSALATISSIME RIO MARE | 16 | `salata` |
| N-GRAH S DIMLJENIM SV.REBRIMA BK 300G GAVRILOVIĆ -16/1 | 14 | `gavrilovic` |

</details>

<a id="leca"></a>
## leća (`leca`)

jedinica: **kg** · loose_produce: **false** · grupa: **144** · isključenih grupa: **139**

sinonimi: leca, lece  
must_match: `leca\b | lece\b | leca zelena | leca crvena`
atributi: vrsta = zelena, crvena, crna, smeda; oblik = konzerva

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850104272356 | LEĆA LIM 400 g NETO OC.MASA 240 g (12) PODRAVKA | 400 g | 18 | 489 | 2,97–9,25 /kg | high/name | oblik=konzerva |
| 2 | 3859891427307 | LEĆA ZELENA 500G NATURA MARJAN VOĆE | 500 g | 11 | 372 | 3,10–4,72 /kg | high/name | vrsta=zelena |
| 3 | 3859890587019 | LEĆA CRVENA 500G NATURA MARJAN VOĆE | 500 g | 11 | 329 | 2,78–4,98 /kg | high/name | vrsta=crvena |
| 4 | 3859891427611 | LECA ZELENA RINF. |  | 6 | 101 | 2,04–3,49 /kg | low/unit_price | vrsta=zelena |
| 5 | 8003716003053 | LEĆA 240 g LIM. STRAINESSE VM2 | 400 g | 6 | 41 | 2,65–5,46 /kg | high/name | oblik=konzerva |
| 6 | 3859890630777 | LEĆA ZELENA VEDRINI 500 g | 500 g | 4 | 232 | 2,04–3,78 /kg | high/name | vrsta=zelena |
| 7 | 3859890630807 | LEĆA CRVENA 500 g PRIMORAC D.O.O. | 500 g | 4 | 193 | 1,96–3,18 /kg | high/name | vrsta=crvena |
| 8 | 3858882920353 | LEĆA SMEĐA 500g PRIMAVITA ADVENT | 500 g | 4 | 163 | 2,78–5,18 /kg | high/name | vrsta=smeda |
| 9 | 3859891427604 | LECA CRVENA RFZ |  | 4 | 78 | 1,52–2,79 /kg | low/unit_price | vrsta=crvena |
| 10 | 3872084000644 | LEĆA ZELENA 500 g EUROCOMPANY | 500 g | 4 | 71 | 3,38–4,30 /kg | high/name | vrsta=zelena |
| 11 | 3872084001061 | LEĆA CRVENA 500 g EUROCOMPANY | 500 g | 3 | 230 | 2,50–4,50 /kg | high/name | vrsta=crvena |
| 12 | 3858886175513 | EKO BIO LEĆA 500 g CRVENA BIOVEGA | 500 g | 3 | 191 | 3,58–5,70 /kg | high/name | vrsta=crvena |
| 13 | 3858882920360 | LEĆA CRVENA 500g PRIMAVITA ADVENT | 500 g | 3 | 153 | 2,00–5,50 /kg | high/name | vrsta=crvena |
| 14 | 3858889333798 | LEĆA CRNA BELUGA VEDRINI 1000 g | 1 kg | 3 | 109 | 3,03–3,69 /kg | high/name | vrsta=crna |
| 15 | 3859888609686 | LEĆA 500 g MARCO POLO | 500 g | 3 | 61 | 3,64–5,98 /kg | high/name |  |
| 16 | 3083680996044 | Leća – Bonduelle – 265 g | 400 g | 3 | 47 | 4,47–6,73 /kg | high/name |  |
| 17 | 8595241513225 | LEĆA U SLANOM NALJEVU 425ml (OCJ. MASA 240 ML) GIANA | 400 g | 3 | 18 | 1,98–3,47 /kg | high/name |  |
| 18 | 8009755002903 | LEĆA FIAMMA 400G-24/1- 0334032 | 240 g | 3 | 11 | 1,67–2,47 /kg | high/name |  |
| 19 | 3859891324293 | LEĆA ZELENA 500 g | 500 g | 2 | 464 | 3,78–4,78 /kg | high/name | vrsta=zelena |
| 20 | 3858886175520 | BIO LEĆA ZELENA 500 g EKOZONA | 500 g | 2 | 213 | 4,78–7,18 /kg | high/name | vrsta=zelena |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| TUNA SALATA LEĆA 160G INSALATISSIME RIO MARE | 11 | `salata` |
| PROTEINSKI SNACK OD CRVENE LEĆE BIO 90G ENCIAN | 8 | `snack` |
| JUHA OD RAJČICE I LEĆE 420 g O'PLANT PODRAVKA | 7 | `juha` |
| Chio Chips Čips od leće paprika 65 g | 6 | `cips` |
| ČIPS OD LEĆE I KRUMPIRA 40G EKOZONA -8/1- | 6 | `cips` |
| Chio Chips Čips leća, k.vrhnje i luk 65g | 5 | `cips` |
| ČIPS OD LEĆE CHIO MORSKA SOL 65g | 5 | `cips` |
| Hipp EKO obrok leća riža/povrće 190 g 6+ | 4 | `hipp` |
| ČIPS OD LEĆE BIO VELIS 30 gr | 4 | `cips` |
| Dimmidisi Juha od leće 620g | 3 | `juha` |

</details>

<a id="slanutak"></a>
## slanutak (`slanutak`)

jedinica: **kg** · loose_produce: **false** · grupa: **126** · isključenih grupa: **28**

sinonimi: slanutak, leblebija, cicer  
must_match: `slanut | leblebij | cicer`
atributi: oblik = konzerva

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850104272349 | SLANUT. LIM 400 g NETO OC.MASA 240 g (12) PODRAVKA | 400 g | 21 | 801 | 2,97–8,71 /kg | high/name | oblik=konzerva |
| 2 | 3850104275609 | SLANUTAK 800 g LIMENKA ( OCJ. MASA 480 g) PODRA | 800 g | 15 | 423 | 2,61–6,65 /kg | high/name | oblik=konzerva |
| 3 | 3859890587026 | SLANUTAK 500 G MARJAN VOCE PVC | 500 g | 9 | 350 | 2,98–4,58 /kg | high/name |  |
| 4 | 8595241504872 | Giana slanutak 400g/240g | 400 g | 8 | 197 | 2,23–5,38 /kg | high/name |  |
| 5 | 3859891496839 | Slanutak kuhani vakum 350g | 350 g | 6 | 320 | 3,97–5,11 /kg | high/name | oblik=konzerva |
| 6 | 3083681003949 | Bonduelle Slanutak Vapeur 310g/265g | 310 g | 6 | 260 | 4,22–9,40 /kg | high/name |  |
| 7 | 8001440009969 | SLANUTAK 400g VALFRUTTA-ocijeđena masa 250g | 400 g | 6 | 206 | 2,65–6,21 /kg | high/name | oblik=konzerva |
| 8 | 8003716003046 | SLANUTAK 240 g LIM. STRAINESSE VM2 | 400 g | 6 | 11 | 2,23–5,25 /kg | high/name | oblik=konzerva |
| 9 | 3856020232306 | SLANUTAK LIM.2500 g OC.MASA 1450 g (6) PODRAVKA | 2,5 kg | 6 | 8 | 2,60–3,88 /kg | high/name | oblik=konzerva |
| 10 | 3083681068146 | N-SLANUTAK BONDUELLE 160G 2*80G -6/1- | 160 g | 5 | 263 | 8,44–24,46 /kg | high/name |  |
| 11 | 3872084000651 | Perfect Day Slanutak 500 g | 500 g | 5 | 204 | 2,22–4,18 /kg | high/name |  |
| 12 | 3831029510266 | SLANUTAK 300 g NATU RETA | 300 g | 5 | 33 | 8,63–9,97 /kg | high/name |  |
| 13 | 8076809575157 | TJ.BARILLA SLANUTAK B.G. 250 g | 250 g | 4 | 168 | 13,28–23,40 /kg | high/name |  |
| 14 | 3858894141777 | E buono slanutak 400 g | 400 g | 4 | 128 | 1,98–2,63 /kg | high/ean |  |
| 15 | 3858886175537 | EKO SLANUTAK 500 g E KOZONA | 500 g | 4 | 42 | 4,50–6,10 /kg | high/name |  |
| 16 | 4007415018176 | SLANUTAK 2650 ml LIM.MIKADO | 2,65 l | 4 | 14 | 1,35–1,58 /l | high/ean | oblik=konzerva |
| 17 | 3859890630517 | SLANUTAK 500 G VEDRINI | 500 g | 3 | 553 | 2,38–3,38 /kg | high/name |  |
| 18 | 8001440001376 | SLANUTAK 360g VALFRUTTA-ocijeđena masa 230g | 360 g | 3 | 161 | 4,06–8,22 /kg | high/name | oblik=konzerva |
| 19 | 3017800252451 | SLANUTAK 300g/265g D AUCY | 340 g | 3 | 160 | 2,91–5,62 /kg | high/name |  |
| 20 | 3859890587651 | SLANUTAK RINF. |  | 3 | 60 | 2,09–3,19 /kg | low/unit_price |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| ARGETA POVRTNI NAMAZ SLANUTAK 95 G ATLANTIC | 11 | `namaz` |
| SALATA INSALATISSIME RIO MARE SLANUTAK 160g | 11 | `salata` |
| HUMMUS ZRNA SLANUTAK 250 G SANA DELIKATESE | 7 | `hummus` |
| BRAŠNO OD SLANUTKA ADVENT 500 G | 2 | `brasno` |
| NAMAZ OD SLANUTKA S KOKOŠJIM OKUSOM 95 g ARGETA | 2 | `namaz` |
| NAMAZ OD SLANUTKA S KOKOŠJIM OKUSOM PIKANT 95 g AR | 2 | `namaz` |
| SALATA PILETINA,KUSKUS,SLANUT,RAJ 300G | 2 | `salata` |
| .JUHA SLANUTAK 500g | 1 | `juha` |
| BRASNO OD SLANUTKA 500 G NUTRIGOLD | 1 | `brasno` |
| FALAFEL KUGLICE SLANUTAK/GRAŠAK 350 g SANA | 1 | `falafel` |

</details>

<a id="kukuruz"></a>
## kukuruz šećerac (konzerva) (`kukuruz`)

jedinica: **kg** · loose_produce: **false** · grupa: **192** · isključenih grupa: **122**

sinonimi: kukuruz, kukuruz secerac  
must_match: `kukuruz secerac | kukuruz sladak | secerac | kukuruz\b | kukuruza\b`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850104063435 | KUKURUZ ŠEĆERAC 340 g PODRAVKA (10) OC. MASA 280 g | 340 g | 21 | 1213 | 3,53–7,46 /kg | high/name |  |
| 2 | 3858882217071 | KUKURUZ ŠEĆERAC 340G OC.MASA 285G ZVIJEZDA (12) | 340 g | 19 | 849 | 4,91–12,18 /kg | high/name |  |
| 3 | 3850104221682 | KUKURUZ ŠEĆERAC 150G/140G, PODRAVKA(12) (PAL 210) | 150 g | 19 | 697 | 7,93–11,79 /kg | high/name |  |
| 4 | 3083680053303 | KUKURUZ ŠEĆERAC BONDUELLE GOLD 340 g (OCJ. MASA 285 g.) ORBICO | 285 g | 18 | 973 | 4,68–9,09 /kg | high/name |  |
| 5 | 3083680074094 | N-KUKURUZ ŠEĆERAC 170G (NETTOMASA 140G)BONDUELLE-12/1 0504 | 170 g | 14 | 749 | 7,00–14,21 /kg | high/name |  |
| 6 | 3083681024258 | KUKURUZ BONDUELLE GOLD 670 g. (OCJ. MASA 570 g.) ORBICO | 670 g | 11 | 401 | 3,21–6,12 /kg | high/name |  |
| 7 | 3859891493371 | KUKURUZ KUHANI ŠEĆER 400g MADIG | 400 g | 9 | 519 | 4,47–8,88 /kg | high/name |  |
| 8 | 3083680015424 | KUKURUZ ŠEĆERAC BONDUELLE 530 g (OCJ. MASA 360 g) ORB | 530 g | 9 | 359 | 3,75–7,36 /kg | high/name |  |
| 9 | 3856021305191 | CHIO KUKURUZ ZA MKV EXTRA CHEESE 80G (36) | 80 g | 8 | 330 | 9,88–18,13 /kg | high/name |  |
| 10 | 8594012793385 | KUKURUZ ŠEĆERAC 285g OCIJEĐENA MASA | 340 g | 8 | 233 | 3,47–4,97 /kg | high/name |  |
| 11 | 3083681170658 | N-KUKURUZ ŠEĆERAC 510G 3*170G POSEBNA CIJENA | 140 g | 7 | 292 | 6,25–24,93 /kg | high/name |  |
| 12 | 5997347540151 | KUKURUZ PRŽ. SLANI S OKUSOM ČILIJA 55 g MOGYI | 55 g | 7 | 280 | 9,82–18,00 /kg | high/name |  |
| 13 | 3859892245283 | KUKURUZ ŠEĆERAC 425ML(340G NETTO) EVERY DAYS -12/1 ULTRA+ | 340 g | 7 | 77 | 2,91–5,85 /kg | high/name |  |
| 14 | 3850104209307 | KUKURUZ ŠEĆER LIM 2.150 g PODRAVKA OC.MASA 1775 g | 2,15 kg | 7 | 11 | 4,02–4674,42 /kg | high/name |  |
| 15 | 3083681068184 | N-KUKURUZ ŠEĆERAC BONDUELLE 170G 2*85G -6/1- | 160 g | 5 | 285 | 6,81–22,71 /kg | high/name |  |
| 16 | 3850116998114 | KUKURUZ ŠEĆERAC (4x2,5kg) UG LEDO | 2,5 kg | 5 | 36 | 1,04–3,92 /kg | high/name |  |
| 17 | 3859890236559 | KUKURUZ ŠEĆERAC LARA 2200G -6/1- | 2,2 kg | 5 | 19 | 2,50–3,27 /kg | high/name |  |
| 18 | 3856003909850 | KUKURUZ ŠEĆERAC 340g ZORELA-OCIJEĐENA MASA 285g | 285 g | 3 | 476 | 2,91–4,21 /kg | high/name |  |
| 19 | 3858888530709 | KUKURUZ ŠEĆERAC 3/1 SVJEŽI |  | 3 | 135 | 3,98 /kg | low/unit_price |  |
| 20 | 3859890236443 | KUKURUZ ŠEĆERAC LARA 340G -24/1- | 340 g | 3 | 35 | 3,53–4,38 /kg | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| N-SALATA RIO MARE 160G-18/1 KUKURUZ S TUNJEVINOM | 13 | `salata` |
| KUKURUZ ZA KOKICE SLANI ZA MIKROV. PEĆNICU 3*80GR CHIO | 11 | `kokice` |
| N-KUKURUZ NATURA 60G PEČENI SLANI BBQ -20/1- SUPER SNACK | 10 | `snack` |
| KUKURUZ KOKICAR 400 G NATURA MARJAN VOCE | 9 | `kokic` |
| KUKURUZ KOKIČAR CHIO 80G ZA MIKROVALNU SLANI -36/1- | 9 | `kokic` |
| KUKURUZ ZA KOKICE 200G (12), ŠAFRAM | 9 | `kokice` |
| BONDUELLE MJEŠANA SALATA CRVENI GRAH + KUKURUZ ČILI MEXICO 430G/200G | 8 | `salata` |
| KUKURUZ ZA KOKICE S MASLACEM ZA MIKROVALNU 80G CHIO | 8 | `kokice` |
| N-KUKURUZ PEČENI SUPER SNACK 60G SLANI NATURA -20/1- | 8 | `snack` |
| KUKURUZ KOKICAR 200 g MARJAN VOCE | 7 | `kokic` |

</details>

<a id="grasak"></a>
## grašak (`grasak`)

jedinica: **kg** · loose_produce: **false** · grupa: **164** · isključenih grupa: **102**

sinonimi: grasak  
must_match: `grasak | graska\b`
atributi: oblik = smrznuti, konzerva

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850116053165 | N-LEDO GRAŠAK 400G -18/1- 065672 | 400 g | 21 | 1263 | 3,00–6,48 /kg | high/name | oblik=smrznuti |
| 2 | 3850104050862 | GRAŠAK 420 g LIMENKA I KVAL. OCJ. MASA 260 g PODRA | 260 g | 21 | 1077 | 2,48–7,65 /kg | high/name | oblik=konzerva |
| 3 | 3850104050053 | GRAŠAK U LIMENCI 850G/520G I KVALITETA (6),(PAL 96) PODRAVKA | 850 g | 19 | 676 | 2,12–6,52 /kg | high/name | oblik=konzerva |
| 4 | 3858882217057 | ZVIJEZDA GRAŠAK 400G/ 265G (12) ZVIJEZDA | 400 g | 16 | 709 | 3,73–7,89 /kg | high/name | oblik=konzerva |
| 5 | 3850104050046 | GRAŠAK 280 g LIMENKA I KVAL. OCJ. MASA 160 g PODRAVKA | 280 g | 16 | 655 | 2,79–9,94 /kg | high/name | oblik=konzerva |
| 6 | 3083680538404 | GRAŠAK BONDUELLE 200 g OCJ. MASA 130 g ORBICO | 200 g | 15 | 718 | 5,95–13,77 /kg | high/name | oblik=konzerva |
| 7 | 3083680047364 | GRAŠAK BONDULLE 400 g (OCJ. MASA 265 g) ORBI | 400 g | 13 | 729 | 3,98–8,75 /kg | high/name | oblik=konzerva |
| 8 | 3850116058627 | ZAMRZ LEDO 700 g GRAŠAK XXL | 700 g | 12 | 409 | 3,41–4,99 /kg | high/name | oblik=smrznuti |
| 9 | 3858883228762 | GRAŠAK 400 g SM BAKINA KUHINJA STANIĆ | 400 g | 10 | 467 | 2,23–3,33 /kg | high/name |  |
| 10 | 3850116035451 | GRAŠAK 2,5 kg LEDO*** | 2,5 kg | 9 | 55 | 1,92–4,60 /kg | high/name | oblik=smrznuti |
| 11 | 3856020279004 | O`Plant Grašak mladi smrznuti 400 g | 400 g | 8 | 350 | 2,80–4,47 /kg | high/name | oblik=smrznuti |
| 12 | 3850104050800 | GRAŠAK 4,2kg LIM.PODRAVKA - ocijeđene mase 2300g | 4,2 kg | 8 | 25 | 1,78–3,63 /kg | high/name | oblik=konzerva |
| 13 | 3850116876320 | FRESCO GRAŠAK 400G (22) LEDO | 400 g | 7 | 203 | 2,97–5,23 /kg | high/name | oblik=smrznuti |
| 14 | 3858885110065 | GRAŠAK MLADI SMRZNUTI 450G, PODRAVKA | 450 g | 7 | 195 | 1,76–4,11 /kg | high/name | oblik=smrznuti |
| 15 | 3859889284585 | N-GRAŠAK FROZY 400G -10/1- | 400 g | 6 | 41 | 2,97–3,33 /kg | high/name |  |
| 16 | 3850116613956 | GRAŠAK SMRZ.450 g U-GR LEDO | 450 g | 6 | 25 | 3,53–4,71 /kg | high/name | oblik=smrznuti |
| 17 | 3083681036800 | GRAŠAK BONDUELLE VAPEUR 400 g | 400 g | 5 | 251 | 2,97–5,48 /kg | high/name |  |
| 18 | 3850354013730 | GRAŠAK FINI SMRZ 450 g BRZO&FINO | 450 g | 5 | 157 | 3,00–4,56 /kg | high/name | oblik=smrznuti |
| 19 | 3083681168594 | N-GRAŠAK BONDUELLE 600G 3*200G POSEBNA CIJENA | 130 g | 5 | 153 | 5,32–30,69 /kg | high/name |  |
| 20 | 3083680004275 | GRAŠAK LIM 530g BONDUELLE | 800 g | 5 | 141 | 2,65–6,58 /kg | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| N-LEDO GRAŠAK MRKVA 400G -18/1- | 21 | `mrkv` |
| GRAŠAK MRKVA FRESCO 400G L LEDO (22) | 9 | `mrkv` |
| GRAŠAK- MRKVA 400G, BAKINA KUHINJA - OC | 9 | `mrkv` |
| O`Plant Grašak i mrkva smrznuti 400 g | 7 | `mrkv` |
| GRAŠAK I MRKVA SMRZNUTO 450G, PODRAVKA | 6 | `mrkv` |
| N-GRAŠAK MRKVA FROZY 400G -10/1- | 6 | `mrkv` |
| PROTEINSKI SNACK OD GRAŠKA 100G ENCIAN | 6 | `snack` |
| FRESCO GRAŠAK-MRKVA 2.5KG LEDO | 5 | `mrkv` |
| GRAŠAK+MRKVA KOCKA 400 g BONDUELLE | 5 | `mrkv` |
| HRANA ZA MAČKE MH ONE MM ONE ADULT PILETINA&GRAŠAK 85G | 5 | `macke` |

</details>

<a id="banana"></a>
## banana (`banana`)

jedinica: **kg** · loose_produce: **true** · grupa: **62** · isključenih grupa: **48**

sinonimi: banana, banane  
must_match: `banan`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850334173539 | BANANA |  | 2 | 197 | 1,34–1,79 /kg | low/unit_price |  |
| 2 | ntl:001069 | BANANA SNIŽENJE |  | 1 | 343 | 0,60–1,00 /kg | low/unit_price |  |
| 3 | ntl:245063 | BANANA |  | 1 | 343 | 1,29–1,59 /kg | low/unit_price |  |
| 4 | konzum:01411643 | BANANA SNIŽENJE |  | 1 | 184 | 1,19 /kg | low/unit_price |  |
| 5 | konzum:90720080 | BANANA BIO |  | 1 | 158 | 1,49 /kg | low/unit_price |  |
| 6 | 3858885879986 | Banana |  | 1 | 144 | 0,89–1,49 /kg | low/unit_price |  |
| 7 | 3830036310906 | Bio banana |  | 1 | 143 | 1,99 /kg | low/unit_price |  |
| 8 | 3830061866072 | COKO BANANA TORTA 800 G | 800 g | 1 | 134 | 13,74 /kg | high/name |  |
| 9 | plodine:100101 | BANANA SORTA CAVENDISH |  | 1 | 126 | 1,44 /kg | low/unit_price |  |
| 10 | gavranovic:071138 | BANANA SNIŽENJE |  | 1 | 125 | 1,18–1,52 /kg | low/unit_price |  |
| 11 | gavranovic:071137 | BANANA |  | 1 | 125 | 1,85–1,99 /kg | low/unit_price |  |
| 12 | 4304493274099 | Banana | 1 kg | 1 | 116 | 1,44 /kg | high/unit |  |
| 13 | 4335619068865 | Bio banana | 1 kg | 1 | 116 | 1,49–1,99 /kg | high/unit |  |
| 14 | plodine:100169 | BIO BANANA SORTA CAVENDISH |  | 1 | 111 | 1,79 /kg | low/unit_price |  |
| 15 | plodine:896208 | DONUT BANANA TOCKICE 54 G LA LORRAINE | 54 g | 1 | 96 | 9,81–12,22 /kg | high/name |  |
| 16 | tommy:10000360 | BANANA SNIŽENO |  | 1 | 87 | 0,73 /kg | low/unit_price |  |
| 17 | tommy:10000969 | BANANA II KAT |  | 1 | 87 | 1,02 /kg | low/unit_price |  |
| 18 | tommy:10000001 | BANANA |  | 1 | 87 | 1,45 /kg | low/unit_price |  |
| 19 | tommy:10005221 | BIO BANANA |  | 1 | 74 | 1,99–2,19 /kg | low/unit_price |  |
| 20 | ribola:0112227 | BANANA II.KL |  | 1 | 61 | 1,03–1,27 /kg | low/unit_price |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| CHOCO BANANA ORIGINAL MEGA PACK 544 g KANDIT | 7 | `choco` |
| BANANA CHIPS RINFUZA, MARJAN VOĆE | 5 | `chips` |
| SLADOLED BANANKO LEDO M3 | 4 | `sladoled` |
| SLADOLED BANANA CRUNCH MACHO LEDO | 3 | `sladoled` |
| KREM BANANA CHOCO ROYAL 500 g (25) | 2 | `choco` |
| KREM BANANANICA BIJELA 500 g (25) | 2 | `krem\b` |
| KRUH BANANA PAK. 500 g BRIOŠ | 2 | `kruh` |
| BANANA CHIPS | 1 | `chips` |
| BANANA CHIPS | 1 | `chips` |
| BANANA CHIPS (SUŠENI) | 1 | `chips` |

</details>

<a id="jabuka"></a>
## jabuka (`jabuka`)

jedinica: **kg** · loose_produce: **true** · grupa: **402** · isključenih grupa: **38**

sinonimi: jabuka, jabuke  
must_match: `jabuk`
atributi: vrsta = zlatni_delicious, idared, granny_smith, crvena

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3857500007445 | JABUKA CRVENA 2 kg | 2 kg | 3 | 181 | 1,10 /kg | high/ean | vrsta=crvena |
| 2 | 3850334173614 | JABUKA ZLATNI DELIŠES (7) |  | 2 | 197 | 1,29–2,05 /kg | low/unit_price | vrsta=zlatni_delicious |
| 3 | 3850334386069 | JABUKA GALA (7) |  | 2 | 197 | 1,69–2,05 /kg | low/unit_price | vrsta=crvena |
| 4 | 3858893252320 | Jabuka Granny Smith |  | 2 | 196 | 1,69–1,99 /kg | low/unit_price | vrsta=granny_smith |
| 5 | 3850334173713 | JABUKA IDARED (7) |  | 2 | 194 | 1,69–2,05 /kg | low/unit_price | vrsta=idared |
| 6 | 3850334173812 | JABUKA JONAGOLD (7) |  | 2 | 193 | 1,75–2,15 /kg | low/unit_price | vrsta=crvena |
| 7 | 3859893211157 | JABUKA CRVENA 2kg PVC | 2 kg | 2 | 172 | 1,00–1,10 /kg | high/name | vrsta=crvena |
| 8 | 3850334049087 | JABUKA ZELENA 2 kg | 2 kg | 2 | 164 | 1,10 /kg | high/name |  |
| 9 | 3850334173621 | JABUKA GRANNY SMITH (7) |  | 2 | 148 | 1,79–1,83 /kg | low/unit_price | vrsta=granny_smith |
| 10 | 3859893211324 | BIO JABUKA CRVENA PODLOZAK |  | 2 | 143 | 2,88 /kg | low/unit_price | vrsta=crvena |
| 11 | 3857500007438 | JABUKA ZELENA 2 kg NTL | 2 kg | 2 | 131 | 1,10 /kg | high/name |  |
| 12 | 5998588114941 | PJESCANIK JABUKA DIM. 85X76X17 CM 461 DOH |  | 2 | 130 | – | – |  |
| 13 | 3858893251644 | Jabuka Braeburn rfs |  | 2 | 113 | 1,69 /kg | low/unit_price |  |
| 14 | 3859893211348 | BIO JABUKA 500 g | 500 g | 2 | 79 | 4,18–4,72 /kg | high/name |  |
| 15 | 3850334049117 | JABUKA PAKIRANA 2 kg VOĆARNA STUDENCA | 2 kg | 2 | 27 | 1,00–1,09 /kg | high/name | vrsta=crvena |
| 16 | ntl:001077 | JABUKA IDARED SNIŽENJE |  | 1 | 343 | 0,50–0,90 /kg | low/unit_price | vrsta=idared |
| 17 | ntl:001103 | JABUKA JONAGOLD SNIŽENJE |  | 1 | 343 | 0,60–0,80 /kg | low/unit_price | vrsta=crvena |
| 18 | ntl:001063 | JABUKA CRVENI DELIŠES SNIŽENJE |  | 1 | 343 | 0,80 /kg | low/unit_price | vrsta=crvena |
| 19 | ntl:001101 | JABUKA ZLATNI DELIŠES SNIŽENJE |  | 1 | 343 | 0,80–0,90 /kg | low/unit_price | vrsta=zlatni_delicious |
| 20 | ntl:004016 | JABUKA GALA |  | 1 | 343 | 0,99–1,69 /kg | low/unit_price | vrsta=crvena |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| LEDOLETTE JABUKA KARAMELA 800 g LEDO | 8 | `ledolette` |
| -ČAJ JABUKA CIMET 20/1 DAR PRIRODE AROMA OMOTAČ | 1 | `cimet` |
| HIPP JABUKA BANANA-KEKS 190 | 1 | `keks` |
| JABUKA MIX PODLOZAK | 1 | `mix\b` |
| Jabuka pakirana mix 1kg | 1 | `mix\b` |
| LIKER JABUKA-CIMET INCANTO 1,0 (6)* | 1 | `cimet` |
| MUFFIN JABUKA CIMET 105 G | 1 | `cimet` |
| PALAČINKE JABUKA CIMET 6x90 g MINUTE | 1 | `cimet` |
| PITA JABUKA 1000 g | 1 | `pita\b` |
| Pita jabuka 95 g | 1 | `pita\b` |

</details>

<a id="limun"></a>
## limun (`limun`)

jedinica: **kg** · loose_produce: **true** · grupa: **112** · isključenih grupa: **23**

sinonimi: limun, limuni  
must_match: `limun\b | limuna\b | limuni\b`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3858885878088 | LIMUN 500 grama | 500 g | 3 | 540 | 1,98–3,18 /kg | high/name |  |
| 2 | 3859891246663 | LIMUN 500G | 500 g | 3 | 5 | 2,66–5,70 /kg | high/name |  |
| 3 | 3856003908327 | LIMUN 500g PAKIRANI | 500 g | 2 | 135 | 2,18–2,98 /kg | high/name |  |
| 4 | 3856003908419 | ENTELVITA LIMUN 500g STARO | 500 g | 2 | 92 | 5,98 /kg | high/name |  |
| 5 | 3859894214171 | LIMUN 500 g | 500 g | 2 | 62 | 2,78–3,58 /kg | high/name |  |
| 6 | 3856003909539 | ENTELVITA LIMUN 1000g STARO | 1 kg | 2 | 48 | 3,09–4,99 /kg | high/name |  |
| 7 | 8437022068602 | N-LIMUN 500G | 500 g | 2 | 24 | 2,78–3,98 /kg | high/name |  |
| 8 | 3850334173737 | LIMUN 500g AGROVIR | 500 g | 2 | 12 | 2,66–3,50 /kg | high/name |  |
| 9 | 3859891246168 | LIMUN 1 kg | 1 kg | 2 | 4 | 1,69–2,24 /kg | high/name |  |
| 10 | 8691959412505 | VIM LIMUN 500g PRENS | 500 g | 2 | 3 | 1,72–3,58 /kg | high/name |  |
| 11 | ntl:001116 | LIMUN SNIŽENJE |  | 1 | 343 | 0,70–1,00 /kg | low/unit_price |  |
| 12 | ntl:248674 | LIMUN |  | 1 | 343 | 1,49 /kg | low/unit_price |  |
| 13 | ntl:104209 | MUFFIN LIMUN 80 g PAN PEK | 80 g | 1 | 186 | 14,88 /kg | high/name |  |
| 14 | 3856017202480 | LIMUN |  | 1 | 184 | 1,49 /kg | low/unit_price |  |
| 15 | 3830070890006 | BIO LIMUN 500 G | 500 g | 1 | 155 | 3,98 /kg | high/name |  |
| 16 | 3856025866117 | NAPOLITANKE LIMUN 700 G BISCOLETTI | 700 g | 1 | 155 | 3,99 /kg | high/name |  |
| 17 | 3859893696268 | LIMUN DOMACI 1 KG | 1 kg | 1 | 145 | 1,29–2,39 /kg | high/name |  |
| 18 | 3858885878071 | Limun rfs |  | 1 | 144 | 1,49 /kg | low/unit_price |  |
| 19 | plodine:100294 | LIMUN PRIMOFIORI NATALIA 500 G | 500 g | 1 | 144 | 1,98–2,18 /kg | high/name |  |
| 20 | 8475843257966 | LIMUN S BUDGET 500 g | 500 g | 1 | 143 | 2,78 /kg | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| CEDEVITA LIMUN 900G PRAŠK.NAPITAK | 13 | `napitak` |
| CEDEVITA LIMUN 1000 G XXL | 4 | `cedevita` |
| CEVITANA LIMUN 500 g | 4 | `cevitana` |
| CEVITANA LIMUN VITAMINKA 920 g (5) | 4 | `cevitana` |
| OCJEĐIVAČ LIMUNA 12CM DVODJELNI PVC FACKELMANN | 4 | `ocjed` |
| CEDEVITA LIMUN 1000 g ATLANTIC | 3 | `cedevita` |
| CJEDILO LIMUNA INOX NIDA | 3 | `cjedil` |
| OCJEDJIVAC LIMUNA | 3 | `ocjed` |
| CEDEVITA LIMUN 500 g | 2 | `cedevita` |
| CEDEVITA LIMUN 900 g + ČAŠA | 2 | `cedevita` |

</details>

<a id="naranca"></a>
## naranča (`naranca`)

jedinica: **kg** · loose_produce: **true** · grupa: **115** · isključenih grupa: **36**

sinonimi: naranca, narance  
must_match: `naranc`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3856003907184 | NARANČA 2KG | 2 kg | 3 | 101 | 0,80–1,75 /kg | high/ean |  |
| 2 | ntl:001121 | NARANČA SNIŽENJE |  | 1 | 343 | 0,70–1,00 /kg | low/unit_price |  |
| 3 | ntl:248679 | NARANČA |  | 1 | 343 | 1,29–1,49 /kg | low/unit_price |  |
| 4 | ntl:001224 | NARANČA CRVENA SNIŽENJE |  | 1 | 258 | 0,44 /kg | low/unit_price |  |
| 5 | 3858885876961 | NARANČA |  | 1 | 188 | 1,49 /kg | low/unit_price |  |
| 6 | 3870622003034 | COKO-NARANCA TORTA 750 G | 750 g | 1 | 155 | 14,65 /kg | high/name |  |
| 7 | plodine:102306 | NARANCA |  | 1 | 148 | 0,89–1,49 /kg | low/unit_price |  |
| 8 | 7427245230277 | NARANCA 2KG | 2 kg | 1 | 145 | 1,40 /kg | high/name |  |
| 9 | plodine:100285 | NARANCA NAVEL 2 KG | 2 kg | 1 | 144 | 1,25–1,33 /kg | high/name |  |
| 10 | plodine:100209 | NARANCA NAVELINA 2KG | 2 kg | 1 | 144 | 1,25–1,35 /kg | high/name |  |
| 11 | plodine:100530 | NARANCA NATALIA NAVELATE 2 KG | 2 kg | 1 | 144 | 1,35–1,50 /kg | high/name |  |
| 12 | 8437022068152 | NARANČA S BUDGET 2 kg | 2 kg | 1 | 144 | 1,49 /kg | high/name |  |
| 13 | 3858893252542 | Naranča rfs |  | 1 | 144 | 1,49 /kg | low/unit_price |  |
| 14 | plodine:100517 | NARANCA NATALIA 2 KG VALENCIA | 2 kg | 1 | 132 | 0,93–1,60 /kg | high/name |  |
| 15 | gavranovic:072037 | NARANČA SNIŽENJE |  | 1 | 119 | 1,35–1,73 /kg | low/unit_price |  |
| 16 | gavranovic:134009 | NARANČA CRVENA SNIŽENJE |  | 1 | 119 | 1,42–1,62 /kg | low/unit_price |  |
| 17 | gavranovic:072036 | NARANČA |  | 1 | 119 | 1,49–2,69 /kg | low/unit_price |  |
| 18 | gavranovic:072038 | NARANČA CRVENA |  | 1 | 119 | 2,15–2,25 /kg | low/unit_price |  |
| 19 | spar:152288 | Naranča Natalia rfs |  | 1 | 119 | 2,29 /kg | low/unit_price |  |
| 20 | lidl:0080135 | Naranča | 1 kg | 1 | 116 | 0,99–1,49 /kg | high/unit |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| CEDEVITA NARANČA 900G PRAŠK.NAPITAK | 13 | `napitak` |
| CEDEVITA NARANCA 1000 G XXL | 5 | `cedevita` |
| CEVITANA NARANČA 500gr (12) | 5 | `cevitana` |
| CEVITANA NARANČA VITAMINKA 920 g (5) | 4 | `cevitana` |
| MEDENJACI NARANČA 500G SWISLION | 3 | `medenjac` |
| CEDEVITA NARANČA 900 g + ČAŠA | 2 | `cedevita` |
| ENTELVITA NARANČA 1000g STARO | 2 | `entelvit` |
| ENTELVITA NARANČA 500g STARO | 2 | `entelvit` |
| BATAT NARANČASTI 500G EKOZONA | 1 | `narancast` |
| BUKET NARANČASTI | 1 | `narancast` |

</details>

<a id="papar"></a>
## papar (`papar`)

jedinica: **kg** · loose_produce: **false** · grupa: **284** · isključenih grupa: **167**

sinonimi: papar, crni papar  
must_match: `papar\b`
atributi: oblik = mljeveni, zrno, mlinac; vrsta = crni, bijeli, sareni

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 9001414041116 | ZAČIN MLINAC PAPAR CRNI U ZRNU 36 g KOTANY | 36 g | 20 | 904 | 96,67–152,50 /kg | high/name | vrsta=crni, oblik=zrno |
| 2 | 3859888163089 | PAPAR CRNI MLJEVENI 50G ŠAFRAM (25) | 50 g | 18 | 950 | 24,80–396,00 /kg | high/name | vrsta=crni, oblik=mljeveni |
| 3 | 9001414040409 | ZAČIN PAPAR CRNI MLJEVENI STAKLO 50 g KOTANY | 50 g | 18 | 760 | 60,00–95,80 /kg | high/name | oblik=mljeveni, vrsta=crni |
| 4 | 3859888163034 | PAPAR CRNI MLJEVENI 100 G VRECICA SAFRAM | 100 g | 18 | 713 | 21,00–34,90 /kg | high/name | vrsta=crni, oblik=mljeveni |
| 5 | 9001414015469 | KOTANYI PAPAR CRNI MLJEVENI VREĆICA 17G (25) | 17 g | 18 | 654 | 53,53–111,18 /kg | high/name | vrsta=crni, oblik=mljeveni |
| 6 | 3850104294426 | PAPAR CRNI MLJEVENI 20 G VRECICA MAESTRO VEGETA PODRAVKA | 20 g | 17 | 694 | 44,50–92,50 /kg | high/name | oblik=mljeveni, vrsta=crni |
| 7 | 3850104294617 | PAPAR CRNI MLJEVENI 100 G VRECICA MAESTRO VEGETA PODRAVKA | 100 g | 16 | 638 | 23,50–45,90 /kg | high/name | oblik=mljeveni, vrsta=crni |
| 8 | 3850104294419 | PAPAR CRNI ZRNO 15 G VRECICA MAESTRO VEGETA PODRAVKA | 15 g | 16 | 635 | 42,67–179,00 /kg | high/name | vrsta=crni, oblik=zrno |
| 9 | 9001414015117 | PAPAR SARENI MJESAVINA U ZRNU 16 G VRECICA KOTANYI | 16 g | 15 | 764 | 56,88–124,38 /kg | high/name | vrsta=sareni, oblik=zrno |
| 10 | 3859888163119 | PAPAR CRNI U ZRNU 50G (25), ŠAFRAM | 50 g | 15 | 715 | 23,80–49,80 /kg | high/name | vrsta=crni, oblik=zrno |
| 11 | 9001414040089 | PAPAR CAYENNE MLJEVENI 38 G STAKLO KOTANYI | 38 g | 15 | 691 | 57,63–78,68 /kg | high/name | oblik=mljeveni |
| 12 | 3850104294730 | PAPAR SARENI 40 G MLINAC MAESTRO VEGETA PODRAVKA | 40 g | 14 | 635 | 52,25–119,75 /kg | high/name | vrsta=sareni, oblik=mlinac |
| 13 | 9001414010075 | PAPAR ZELENI ZRNO 12 G VRECICA KOTANYI | 12 g | 14 | 524 | 75,83–165,83 /kg | high/name | oblik=zrno |
| 14 | 3850104294501 | PAPAR BIJELI MLJEVENI 20 G MAESTRO VEGETA PODRAVKA | 20 g | 14 | 441 | 62,50–114,50 /kg | high/name | oblik=mljeveni, vrsta=bijeli |
| 15 | 9001414040799 | PAPAR S CESNJAKOM 72 G STAKLO KOTANYI | 70 g | 14 | 388 | 20,97–62,71 /kg | high/name |  |
| 16 | 3856020233051 | VEGETA MAESTRO CRNI PAPAR ZRNO MLIN 42g PODRAVKA | 42 g | 13 | 574 | 35,71–109,29 /kg | high/name | vrsta=crni, oblik=zrno |
| 17 | 3859888163096 | PAPAR CRNI MLJEVENI 10G (100), ŠAFRAM | 10 g | 13 | 397 | 40,00–75,00 /kg | high/name | vrsta=crni, oblik=mljeveni |
| 18 | 9001414015452 | PAPAR CRNI ZRNO 17 G VRECICA KOTANYI | 17 g | 12 | 489 | 8,51–105,29 /kg | high/name | oblik=zrno, vrsta=crni |
| 19 | 3850104294822 | CRNI PAPAR MLJ.VREĆ.50G (20) (PAL 145),PODRAVKA | 50 g | 12 | 448 | 34,00–55,80 /kg | high/name | oblik=mljeveni, vrsta=crni |
| 20 | 9001414040423 | KOTANYI 54G PAPAR BIJELI -4/MLJEVENI STAKLO | 54 g | 12 | 367 | 66,48–82,00 /kg | high/name | oblik=mljeveni, vrsta=bijeli |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| PAPAR MIX 35 G MLINAC KOTANYI | 15 | `mix\b` |
| PAPAR MIX 40 G MLINAC SAFRAM | 14 | `mix\b` |
| PAPAR ZELENI U SALAMURI 100g KOTANYI (24) | 13 | `salam` |
| KOTANYI 185G PAPAR CRNI MLJEV 50G + SOL 135G GRATIS -1/1- | 12 | `sol\b` |
| ČIPS ČIPI ČIPS 120G SOL I PAPAR ULTRA REBRASTI -20/1- CHIO | 12 | `sol\b` |
| PAPAR ZELENI U SALAMURI 500g KOTANYI (12) | 9 | `salam` |
| KOTANYI MLINAC 65G PAPAR I SOL - 4/1- | 8 | `sol\b` |
| PAPAR MIX 40 G STAKLO KOTANYI | 7 | `mix\b` |
| ZAČIN ZA KOKTELE SPICES & DRINKS PAPAR CRVENI 25 g KOTANYI | 7 | `zacin za` |
| GRICKALICE VENERE SNACK KURKUMA/PAPAR BEZ GLUTENA 50G SCOTTI | 6 | `snack` |

</details>

<a id="mljevena_paprika"></a>
## mljevena paprika (začin) (`mljevena_paprika`)

jedinica: **kg** · loose_produce: **false** · grupa: **122** · isključenih grupa: **11**

sinonimi: mljevena paprika, slatka paprika, ljuta paprika, aleva paprika  
must_match: `paprika mljevena | mljevena paprika | paprika slatka mlj | paprika ljuta mlj | paprika mlj | mlj paprika | aleva paprika | paprika slatka | paprika ljuta | slatka paprika | ljuta paprika`
atributi: vrsta = slatka, ljuta, dimljena

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3859888163065 | PAPRIKA SLATKA MLJEVENA 100 G VRECICA SAFRAM | 100 g | 18 | 1197 | 11,30–25,50 /kg | high/name | vrsta=slatka |
| 2 | 3859888163058 | PAPRIKA LJUTA MLJEVENA 100 G VRECICA SAFRAM | 100 g | 18 | 1129 | 12,90–22,50 /kg | high/name | vrsta=ljuta |
| 3 | 3850104294631 | PAPRIKA SLATKA MLJEVENA VRECICA100 G MAESTRO VEGETA PODRAVKA | 100 g | 18 | 772 | 9,90–21,90 /kg | high/name | vrsta=slatka |
| 4 | 3850104294624 | PAPRIKA LJUTA MLJEVENA 100 G MAESTRO VEGETA PODRAVKA | 100 g | 17 | 579 | 9,90–99,00 /kg | high/name | vrsta=ljuta |
| 5 | 3859888163072 | PAPRIKA SLATKA MLJEVENA 200 G VRECICA SAFRAM | 200 g | 14 | 545 | 13,45–20,95 /kg | high/name | vrsta=slatka |
| 6 | 3850104294648 | PAPRIKA SLATKA MLJEVENA 200 G MAESTRO VEGETA PODRAVKA | 200 g | 13 | 457 | 8,20–44,75 /kg | high/name | vrsta=slatka |
| 7 | 3850104294594 | PAPRIKA SLATKA MLJEVENA 50 G VRECICA MAESTRO VEGETA PODRAVKA | 50 g | 12 | 547 | 13,20–23,00 /kg | high/name | vrsta=slatka |
| 8 | 3859888163317 | PAPRIKA SLATKA MLJEVENA DELIKATES 100 G VRECICA SAFRAM | 100 g | 10 | 367 | 11,90–99,00 /kg | high/name | vrsta=slatka |
| 9 | 9001414119211 | PAPRIKA LJUTA MLJEVENA 35 G VRECICA KOTANYI | 35 g | 10 | 312 | 23,14–39,71 /kg | high/name | vrsta=ljuta |
| 10 | 9001414119204 | PAPRIKA SLATKA MLJEVENA DELIKATES 35 G VRECICA KOTANYI | 35 g | 10 | 289 | 20,29–39,71 /kg | high/name | vrsta=slatka |
| 11 | 3850104294600 | PAPRIKA SLATKA MLJEVENA 400 G VRECICA MAESTRO VEGETA PODRAVK | 400 g | 10 | 142 | 2,50–14,98 /kg | high/name | vrsta=slatka |
| 12 | 3859888163041 | PAPRIKA MLJEVEN SLATKA 1000 g ŠAFRAM | 1 kg | 9 | 35 | 11,13–15,99 /kg | high/name | vrsta=slatka |
| 13 | 3859890104124 | PAPRIKA MLJEVENA ZAČINSKA LJUTA 500G, ŠAFRAM | 500 g | 8 | 144 | 12,20–18,38 /kg | high/name | vrsta=ljuta |
| 14 | 9001414009208 | PAPRIKA SLATKA MLJEVENA 100 G VRECICA KOTANYI | 100 g | 7 | 404 | 15,90–28,90 /kg | high/name | vrsta=slatka |
| 15 | 3858881083127 | ZAČIN PAPRIKA SLATKAFRANCK 100 g | 100 g | 7 | 178 | 15,90–99,00 /kg | high/name | vrsta=slatka |
| 16 | 3859890104698 | PAPRIKA SLATKA MLJEVENA 100G ULTRA PLUS | 100 g | 7 | 75 | 7,90–13,90 /kg | high/name | vrsta=slatka |
| 17 | 3859892109868 | Š EXTRA PAPRIKA SLATKA ŠAFRAM 100 g (20) | 100 g | 7 | 63 | 7,50–10,60 /kg | high/name | vrsta=slatka |
| 18 | 9001414119242 | KOTANYI 45G PAPRIKA SLATKAZAČINSKA -25/1- VREĆICA | 45 g | 6 | 318 | 13,78–30,89 /kg | high/name | vrsta=slatka |
| 19 | 3858881735378 | PAPRIKA SLATKA ZAČIN 70G DERMA (20) | 70 g | 6 | 235 | 12,71–300,00 /kg | high/name | vrsta=slatka |
| 20 | 3858881582019 | ZAČIN PAPRIKA SLATKANADALINA 100 g | 100 g | 6 | 217 | 13,50–21,50 /kg | high/name | vrsta=slatka |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| ČIPS LAY´S LJUTA PAPRIKA 60 g | 6 | `cips` |
| Lay Chips Classic ljuta paprika | 4 | `chips` |
| HUMMUS LJUTA PAPRIKA 190g | 1 | `hummus` |
| KREKER TAKO PAPRIKA LJUTA 170g | 1 | `kreker` |
| KREKER TAKO PAPRIKA LJUTA 70g | 1 | `kreker` |
| PAPRIKA LJUTA kom | 1 | `kom\b` |
| PAPRIKA MLJEVENA SLATKA 1 kg ZA PEČENJE | 1 | `pecen` |
| SIR TVRDI OVCJI LJUTA PAPRIKA DIABLO 200 G VEGA SOTUELAMOS | 1 | `sir\b` |
| ČIPS DORITOS LJUTA PAPRIKA 90g | 1 | `cips` |
| ČIPS LJUTA PAPRIKA 130g | 1 | `cips` |

</details>

<a id="dodatak_jelima"></a>
## dodatak jelima (Vegeta i sl.) (`dodatak_jelima`)

jedinica: **kg** · loose_produce: **false** · grupa: **97** · isključenih grupa: **125**

sinonimi: dodatak jelima, vegeta, univerzalni dodatak jelima  
must_match: `vegeta\b | dodatak jelima | univerzalni dodatak | dodatak za jela`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850104008597 | VEGETA 250G (16), PODRAVKA (PAL 102) | 250 g | 25 | 1363 | 6,88–11,16 /kg | high/name |  |
| 2 | 3850104047046 | VEGETA 1KG (10), PODRAVKA (PAL-60) | 1 kg | 22 | 989 | 5,36–11,19 /kg | high/name |  |
| 3 | 3850104260872 | VEGETA 400G VREĆICA PODRAVKA PROMO | 400 g | 20 | 1342 | 6,23–10,97 /kg | high/name |  |
| 4 | 3850104008443 | VEGETA 500G (12), PODRAVKA (PAL 80) | 500 g | 20 | 865 | 7,08–10,18 /kg | high/name |  |
| 5 | 3850104008054 | VEGETA 75G (35), PODRAVKA (PAL 102) | 75 g | 17 | 818 | 6,67–21,20 /kg | high/name |  |
| 6 | 3850104255274 | VEGETA BOČICA 200G, PODRAVKA(12) (PAL 126) | 200 g | 17 | 736 | 11,95–14,45 /kg | high/name |  |
| 7 | 3850104216466 | N-VEGETA PODR 250G+50G GRATIS -16/1- VREĆICA | 250 g | 16 | 1111 | 7,80–11,48 /kg | high/name |  |
| 8 | 3850104249600 | N-VEGETA PODR 400G STAKLO DOZA -8/1- | 400 g | 16 | 605 | 8,95–11,25 /kg | high/name |  |
| 9 | 3850104226212 | VEGETA 150G, PODRAVKA, (12) ZIPP (PAL 85) | 150 g | 15 | 709 | 10,60–15,93 /kg | high/name |  |
| 10 | 3856020270544 | VEGETA FINO MLJEVENA 200 g PODRAVKA | 200 g | 14 | 620 | 8,45–14,90 /kg | high/name |  |
| 11 | 3850104047077 | VEGETA 2KG (8), PODRAVKA (PAL 24) | 2 kg | 14 | 110 | 5,78–8,29 /kg | high/name |  |
| 12 | 3856020276669 | VEGETA DIMLJENA 200 G VRECICA | 200 g | 6 | 373 | 7,95–11,75 /kg | high/name |  |
| 13 | 3856020276690 | VEGETA SLATKA CHILI PAPRICICA 200 G VRECICA | 200 g | 6 | 364 | 10,45–11,75 /kg | high/name |  |
| 14 | 3858891569888 | KUHARELA DODATAK JELIMA S POVRĆEM 250G (20) | 250 g | 6 | 74 | 2,76–5,00 /kg | high/name |  |
| 15 | 3856003915356 | DODATAK JELIMA 500g TO JE TO S POVRĆEM | 500 g | 4 | 495 | 2,58–3,30 /kg | high/name |  |
| 16 | 3856003915349 | DODATAK JELIMA 250g TO JE TO S POVRĆEM | 250 g | 4 | 495 | 3,20–3,96 /kg | high/name |  |
| 17 | 3856003939932 | DODATAK JELIMA S POVRĆEM 1kg TOJETO | 1 kg | 4 | 449 | 2,19–2,99 /kg | high/name |  |
| 18 | 3856020245337 | VEGETA eko dodatak jelima s povrć.120g T | 120 g | 4 | 106 | 10,75–22,42 /kg | high/name |  |
| 19 | 3858891569895 | KUHARELA DODATAK JELIMA S POVRĆEM 500G (12) | 500 g | 4 | 71 | 2,38–4,70 /kg | high/name |  |
| 20 | 8600947042129 | DODATAK JELIMA ZA GOVEĐI GULAŠ 35*50g ALEVA | 50 g | 3 | 95 | 0,49–25,00 /kg | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| VEGETA GRILL CLASSIC VREĆICA 30G (18) (PAL 252) | 19 | `grill` |
| VEGETA TWIST KRUMPIR VREĆICA 30G(18) (PAL 242) | 19 | `twist` |
| VEGETA TWIST ZA PILETINU VREĆICA 30G (18) (PAL 252) | 19 | `twist` |
| VEGETA NATUR VREĆICA 150G (12) PODRAVKA (PAL 85) | 17 | `natur` |
| VEGETA NATUR GRILL VRATINA 30g PODRAVKA | 16 | `natur` |
| ZAČIN MEDITERAN 100G VEGETA NATUR (12) | 16 | `natur` |
| ZAČIN CHILI VR 100g VEGETA NATUR | 15 | `natur` |
| VEGETA PODR 300G NATUR DOZA -12/1- | 14 | `natur` |
| VEGETA TWIST ZA SALATU 30 g VREĆICA PODRA | 14 | `twist` |
| MIRODIJE MAJČINA DUŠICA USITNJENA 5G VEGETA MAESTRO | 13 | `maestro` |

</details>

<a id="ocat"></a>
## ocat (alkoholni/vinski) (`ocat`)

jedinica: **l** · loose_produce: **false** · grupa: **233** · isključenih grupa: **130**

sinonimi: ocat, alkoholni ocat, vinski ocat, kvasina  
must_match: `ocat\b | octa\b | kvasin`
atributi: vrsta = alkoholni, vinski

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850164310111 | N-OCAT BADEL ALKOHOLNI 1.0L-12/1- | 1 l | 22 | 1302 | 1,19–1,99 /l | high/name | vrsta=alkoholni |
| 2 | 3850164321117 | KISKO VINSKI OCAT 1L (12), BADEL | 1 l | 22 | 922 | 1,59–3,49 /l | high/name | vrsta=vinski |
| 3 | 3850164310180 | OCAT BADEL ALKOHOLNI 3.0L BALON (9%) | 3 l | 21 | 1116 | 0,96–1,70 /l | high/name | vrsta=alkoholni |
| 4 | 3850164310142 | OCAT KISKO ALKOHOLNI 0,5L LABUD | 500 ml | 21 | 788 | 1,68–3,18 /l | high/name | vrsta=alkoholni |
| 5 | 3850164310197 | OCAT BADEL ALKOHOLNI 5.0L BALON (9%) | 5 l | 20 | 826 | 0,91–1,58 /l | high/name | vrsta=alkoholni |
| 6 | 3858882210928 | OCAT ALKOHOLNI 1 l PET ZVIJEZDA | 1 l | 19 | 862 | 0,96–19,25 /l | high/name | vrsta=alkoholni |
| 7 | 3858882211154 | N-OCAT ZVIJEZDA VINSKI 1L -12/1-CRNO VINO | 1 l | 18 | 707 | 1,63–32,50 /l | high/name | vrsta=vinski |
| 8 | 3850164321148 | OCAT VINSKI KISKO 500 ml BADE | 500 ml | 17 | 821 | 2,24–3,98 /l | high/name | vrsta=vinski |
| 9 | 3850164331116 | OCAT KVASINA 6% 1L KISKO BADEL | 1 l | 13 | 660 | 1,59–2,49 /l | high/name | vrsta=vinski |
| 10 | 3858882211727 | OCAT ALKOHOLNI OCAT 3 l ZVIJEZDA (1) | 3 l | 13 | 443 | 0,88–19,08 /l | high/name | vrsta=alkoholni |
| 11 | 5010338101749 | OCAT OD RIZE JAPANSKI 150 ML BLUE DRAGON | 150 ml | 10 | 349 | 11,60–17,67 /l | high/name |  |
| 12 | 5060194790014 | OCAT RICE VINEGAR 150 ml SAITAKU | 150 ml | 8 | 304 | 3,33–20,60 /l | high/name |  |
| 13 | 3859891093922 | ULTRA OCAT VINSKI 1L, PREHRANA (6) | 1 l | 8 | 84 | 0,89–1,69 /l | high/name | vrsta=vinski |
| 14 | 3850164321186 | OCAT VINSKI 3L KISKO BADEL | 3 l | 8 | 64 | 1,13–1,80 /l | high/name | vrsta=vinski |
| 15 | 3859891093908 | ULTRA OCAT ALKOHOLNI 1L, PREHRANA (6) (750PAL) | 1 l | 7 | 78 | 0,29–1,49 /l | high/name | vrsta=alkoholni |
| 16 | 3858889640018 | SEGESTICA ALKOHOLNI OCAT 9% 1L (12) | 1 l | 6 | 198 | 0,93–1,59 /l | high/name | vrsta=alkoholni |
| 17 | 3858889640032 | SEGESTICA VINSKI OCAT 1L (12) LABUD | 1 l | 6 | 150 | 0,09–1,97 /l | high/name | vrsta=vinski |
| 18 | 3859891093007 | OCAT ALKOHOLNI PREHRANA 9% 1 L | 1 l | 5 | 194 | 0,69–1,25 /l | high/name | vrsta=alkoholni |
| 19 | 3858889362545 | NATUREL ALKOHOLNI OCAT 1 L (9 %) | 1 l | 5 | 82 | 0,89–1,39 /l | high/name | vrsta=alkoholni |
| 20 | 3859892999063 | OCAT VIROVITIČKI PRIRODNI VINSKI 1 L | 1 l | 5 | 78 | 1,33–2,49 /l | high/name | vrsta=vinski |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| OCAT JABUČNI 1L 5% KISKO LABUD | 21 | `jabuc` |
| OCAT BADEL JABUČNI 0.5L-12/1- | 20 | `jabuc` |
| JABUČNI PRIRODNI OCAT 1L (15), ZVIJEZDA | 16 | `jabuc` |
| Encian Ocat jabučni 0,7l staklo | 14 | `jabuc` |
| OCAT ACETO BALSAMICO 0,5L (12) ZVIJEZDA | 11 | `balsam` |
| OCAT ACETO BALSAMICO 250ML ORO DUE VITTORIE | 11 | `balsam` |
| OCAT MAUTNER 500ML JABUČNI BARRIQUE -6/1- | 11 | `jabuc` |
| Mautner Ocat jabučni 5% oct.kisel.500ml | 10 | `jabuc` |
| Mautner Markhof Ocat jabučni 5% 1 l | 9 | `jabuc` |
| SEGESTICA JABUČNI OCAT 1L (12) LABUD | 8 | `jabuc` |

</details>

<a id="med"></a>
## med (`med`)

jedinica: **kg** · loose_produce: **false** · grupa: **612** · isključenih grupa: **239**

sinonimi: med, pcelinji med  
must_match: `med\b | meda\b`
atributi: vrsta = livadni, bagremov, kestenov, kaduljin, lipov, sumski

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 38500213 | MED CVJETNI VRCANI 20 g PVC PODRAVKA (96) | 20 g | 16 | 450 | 11,00–24,50 /kg | high/name | vrsta=livadni |
| 2 | 3859888851061 | MED CVIJETNI LIVADA 900G, APIMEL (12) | 900 g | 13 | 381 | 4,43–7,88 /kg | high/name | vrsta=livadni |
| 3 | 3859888851535 | MED APIMEL 900G S DODATKOM KADULJE -12/1- | 900 g | 11 | 394 | 9,99–15,32 /kg | high/name | vrsta=kaduljin |
| 4 | 3859888851016 | MED APIMEL 900G BAGREM -12/1- | 900 g | 11 | 354 | 7,21–13,32 /kg | high/name | vrsta=bagremov |
| 5 | 3859888851023 | MED APIMEL 450G BAGREM -12/1- | 450 g | 10 | 278 | 11,09–17,53 /kg | high/name | vrsta=bagremov |
| 6 | 3859888851078 | MED CVJETNI (LIVADA) 450g APIMEL | 450 g | 10 | 266 | 8,33–19,98 /kg | high/name | vrsta=livadni |
| 7 | 3859888500013 | MED CVIJETNI 900 g PIP LOT:17.08.28 | 900 g | 9 | 523 | 3,43–10,02 /kg | high/name | vrsta=livadni |
| 8 | 3859888500044 | MED BAGREM 900 g PIPLOT:21.07.28 | 900 g | 9 | 443 | 4,99–12,66 /kg | high/name | vrsta=bagremov |
| 9 | 3859888851542 | MED APIMEL 450G S DODATKOM KADULJE -12/1- | 450 g | 9 | 272 | 11,53–18,42 /kg | high/name | vrsta=kaduljin |
| 10 | 3859888500020 | MED CVIJETNI 450 g PIP LOT:24.06.28 | 450 g | 8 | 393 | 4,20–12,67 /kg | high/name | vrsta=livadni |
| 11 | 3859888851511 | MED UG. CVJETNI 12G ULTRA LOT:L16-85 | 12 g | 8 | 310 | 6,67–29,17 /kg | high/name | vrsta=livadni |
| 12 | 3859888851030 | MED APIMEL 250G BAGREM -12/1- | 250 g | 8 | 238 | 13,00–17,16 /kg | high/name | vrsta=bagremov |
| 13 | 3859888851085 | MED CVJETNI (LIVADA) 250g APIMEL | 250 g | 7 | 305 | 10,08–16,76 /kg | high/name | vrsta=livadni |
| 14 | 3859888851337 | MED PREMIUM S LAVANDOM 450 G APIMEL | 450 g | 7 | 287 | 12,09–18,20 /kg | high/name |  |
| 15 | 3859888851559 | MED S DODATKOM KADULJE 250 G APIMEL | 250 g | 7 | 264 | 11,56–20,36 /kg | high/name | vrsta=kaduljin |
| 16 | 3859888500082 | MED LIPA 450 g PIP LOT:19.01.28 | 450 g | 7 | 197 | 11,49–17,76 /kg | high/name | vrsta=lipov |
| 17 | 3859888673847 | MED VARŽAK 900G CVJETNI -8/1- | 900 g | 7 | 161 | 6,32–11,67 /kg | high/name | vrsta=livadni |
| 18 | 3859888500075 | MED LIPA 900 g PIP LOT:16.04.28 | 900 g | 6 | 326 | 7,67–14,43 /kg | high/name | vrsta=lipov |
| 19 | 3859888851047 | MED APIMEL 900G LIPA -12/1- | 900 g | 6 | 125 | 11,64–16,43 /kg | high/name | vrsta=lipov |
| 20 | 3859888851054 | API MEL MED LIPOV 450 G | 450 g | 6 | 96 | 11,80–18,42 /kg | high/name | vrsta=lipov |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| ELEPHANT 70G TRAJNO SLANO PECIVO ALKA MED, SENF, LUK | 16 | `senf` |
| FILTER ČAJ KAMILICA-ĐUMBIR-MED 40G OMOT (10), FRANCK | 16 | `caj\b` |
| KEKSI BELVITA BREAKFAST MED&ORASI 225G | 15 | `keks` |
| MUSLI DR OETKER 300G MED I BADEM CRUNCHY PLUS -8/1- | 15 | `musli` |
| N-DUKAT JOGURT DUKATOS 150GLIMUN-KOLAČ-MED GRČKI TIP | 15 | `jogurt` |
| GEL ZA TUŠ. JOHNSON VITA RICH LT MED JOGURT 400ML | 12 | `jogurt` |
| TRAJNO SLANO PECIVO ELEPHANT PRETZEL 125 g MED, SENF I LUK | 12 | `senf` |
| UMAK BBQ MED PODRAVKA 345 g | 12 | `umak` |
| KREKER MORSKA SOL I MED 180 G ELEPHANT | 11 | `kreker` |
| BOJA ZA KOSU SYOSS COLOR 8-7 MED PLAVA 115ml AWT | 10 | `kosu` |

</details>

<a id="kava"></a>
## kava (`kava`)

jedinica: **kg** · loose_produce: **false** · grupa: **1168** · isključenih grupa: **455**

sinonimi: kava, mljevena kava, kava u zrnu  
must_match: `kava\b | kave\b | kafa\b | cafe\b | caffe\b | espresso\b`
atributi: oblik = mljevena, zrno, instant

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3858881080263 | JUBILARNA KAVA MLJEVENA VAKUMIRANA 250G (24), FRANCK | 250 g | 23 | 1432 | 17,96–30,60 /kg | high/name | oblik=mljevena |
| 2 | 3858881085589 | N-KAVA FRANCK 175G MLJEVENA JUBILARNA -12/1- | 175 g | 23 | 1371 | 19,94–35,71 /kg | high/name | oblik=mljevena |
| 3 | 3838471022699 | KAVA MLJEVENA BARCAFFE CLASSIC 175 g | 175 g | 22 | 1408 | 21,09–34,23 /kg | high/name | oblik=mljevena |
| 4 | 3858881085596 | N-KAVA FRANCK 400G MLJEVENA JUBILARNA -10/1- | 400 g | 22 | 1403 | 15,73–26,48 /kg | high/name | oblik=mljevena |
| 5 | 3838471032308 | KAVA MLJ. BARCAFFE CLASSIC 400g ATLANTIC | 400 g | 22 | 1285 | 14,98–28,48 /kg | high/name | oblik=mljevena |
| 6 | 3850291052380 | KAVA GLORIA MLJEVENA VR 400g (10) | 400 g | 21 | 1117 | 14,72–23,73 /kg | high/name | oblik=mljevena |
| 7 | 3858881084872 | N-KAVA GLORIA 250G MLJEVENA -12/1- VREĆICA | 250 g | 20 | 1282 | 15,96–25,96 /kg | high/name | oblik=mljevena |
| 8 | 3858881085602 | KAVA GLORIA MLJEV.V.175G(12), FRANCK | 175 g | 20 | 1105 | 15,14–32,29 /kg | high/name | oblik=mljevena |
| 9 | 3858881775275 | KAVA MINAS MLJEVENA FO ANAMARIJA 400 g (18) | 400 g | 20 | 1103 | 7,73–24,23 /kg | high/name | oblik=mljevena |
| 10 | 3858881088184 | KAVA GLORIA MLJEVENA VR 500g (10) | 500 g | 20 | 889 | 13,06–24,78 /kg | high/name | oblik=mljevena |
| 11 | 3858881087644 | KAVA MLJEVENA CREMA VAKUMIRANA 250 G FRANCK | 250 g | 19 | 884 | 17,96–27,56 /kg | high/name | oblik=mljevena |
| 12 | 3838471021272 | N-KAVA BARCAFFE 500G CLASSIC -15/1- MLJEVENA | 500 g | 19 | 829 | 15,38–27,98 /kg | high/name | oblik=mljevena |
| 13 | 3858881080119 | ESPRESSO MLJEVENA VAKUMIRANA KAVA 250G (24), FRANCK | 250 g | 19 | 765 | 30,84–71,84 /kg | high/name | oblik=mljevena |
| 14 | 3850291051956 | KAVA MLJEVENA CREMA VRECICA 400 G FRANCK | 400 g | 18 | 937 | 16,23–26,48 /kg | high/name | oblik=mljevena |
| 15 | 3858881087637 | N-KAVA FRANCK 175G CREMA -12/1- MLJEVENA | 175 g | 18 | 902 | 25,09–32,29 /kg | high/name | oblik=mljevena |
| 16 | 3838471049474 | KAVA BARCAFFE 200G BC CLASSIC -6/1- LIMENKA | 200 g | 18 | 838 | 39,95–59,45 /kg | high/name | oblik=instant |
| 17 | 3858881083646 | KAVA FRANCK 18G 3U1 INST -20/3/1- ( 60G KUTIJA ) | 18 g | 18 | 798 | 16,11–30,56 /kg | high/name | oblik=instant |
| 18 | 8711000532904 | N-KAVA JACOBS 200G CRONAT GOLD -6/1- STAKLENKA | 200 g | 17 | 1077 | 62,40–94,95 /kg | high/name | oblik=instant |
| 19 | 3850291055213 | KAVA INSTANT 100 G CLASSIC LIMENKA FRANCK | 100 g | 17 | 897 | 35,90–56,90 /kg | high/name | oblik=instant |
| 20 | 3838471028844 | KAVA BARCAFFE 8G BLACK N EASY -10/1- 10*8G KUTIJA (120) | 8 g | 17 | 793 | 5,00–81,25 /kg | high/name | oblik=mljevena |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| KAVA ZA FILTER APARATE VAKUMIRANA 250G (12), FRANCK | 20 | `aparat` |
| Vindija 'z Bregov Ledena Kava Caffe Latte 250 Ml | 19 | `ledena` |
| KAVA FRANCK NOTA ESPRESSO 16 KAPSULA 112G DG COMP. | 17 | `kapsul` |
| KAVA FILTER FRANCK B.KOF.250 g | 16 | `filter` |
| KAVA LEDENA LANDESSA ESPRESSO 230 ML | 15 | `ledena` |
| LEDENA KAVA DOUBLE ESPRESSO 250 ml HELL | 15 | `ledena` |
| NAPITAK MLIJEČNI LEDENA KAVA 0,235 L VINDIJA | 15 | `napitak` |
| KAVA NESCAFE DOLCE GUSTO CAFE AU LAIT 16 KAPSULA 160G | 14 | `kapsul` |
| KAVA NESCAFE DOLCE GUSTO ESPRESSO INTENSO 16 KAPSULA 112G | 14 | `kapsul` |
| NAPITAK MLIJEČNI LEDENA KAVA 1L VINDIJA | 14 | `napitak` |

</details>

<a id="senf"></a>
## senf (`senf`)

jedinica: **kg** · loose_produce: **false** · grupa: **133** · isključenih grupa: **17**

sinonimi: senf, gorusica  
must_match: `senf\b | gorusic | dijon`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850104023484 | Podravka senf estragon 350 g staklenka | 350 g | 24 | 1393 | 5,11–10,83 /kg | high/name |  |
| 2 | 3850104023033 | SENF ESTRAGON PVC 140 g PODRAVKA (15) | 140 g | 21 | 1265 | 8,57–19,93 /kg | high/name |  |
| 3 | 3850104023415 | Podravka senf estragon 700 g staklenka | 700 g | 20 | 610 | 3,41–7,91 /kg | high/name |  |
| 4 | 3850104268069 | UMAK SENF ESTRAGON TUBA PODRAVKA 200 g | 200 g | 19 | 686 | 8,00–12,95 /kg | high/name |  |
| 5 | 7613287084163 | SENF 200G BLAGI THOMY TUBA NESTLE | 200 g | 18 | 1009 | 8,45–14,95 /kg | high/name |  |
| 6 | 3856015332523 | SENF DELIKATES 290 g STAKLO ZVIJEZDA | 290 g | 18 | 867 | 5,48–10,31 /kg | high/name |  |
| 7 | 3856015332493 | N-SENF ZVIJEZDA 190G DELIKATES -12/1- | 190 g | 18 | 842 | 7,32–12,05 /kg | high/name |  |
| 8 | 3850104092176 | SENF ESTRAGON BOČICA 200G (12), PODRAVKA | 200 g | 18 | 550 | 9,70–15,95 /kg | high/name |  |
| 9 | 3850104023019 | SENF ESTRAGON 100 g TUBA PODRAVKA (24) | 100 g | 16 | 825 | 10,50–20,90 /kg | high/name |  |
| 10 | 7613287084644 | SENF THOMY 100 g BLAGI LOT:618768839 | 100 g | 16 | 476 | 9,90–360,00 /kg | high/name |  |
| 11 | 9001414040713 | Kotanyi gorušica zrno staklo 79 g | 79 g | 14 | 426 | 33,54–44,18 /kg | high/name |  |
| 12 | 4025891136153 | Jutro Senf u krigli srednje ljuti 250 g | 250 g | 13 | 567 | 6,36–11,96 /kg | high/name |  |
| 13 | 3830003054475 | SENF 290 G NATURETA STAKLO | 290 g | 13 | 318 | 3,45–9,97 /kg | high/name |  |
| 14 | 3850104023064 | SENF ESTRAGON PVC 2.5 KG PODRAVKA (6) | 2,5 kg | 13 | 36 | 2,71–4,86 /kg | high/name |  |
| 15 | 9011900184401 | Mautner Markhof Senf estragon stak.350g | 350 g | 12 | 538 | 5,11–8,54 /kg | high/name |  |
| 16 | 9011900139616 | Mautner Markhof Senf estragon tuba 200 g | 200 g | 12 | 455 | 7,00–11,45 /kg | high/name |  |
| 17 | 4025891004254 | SENF JUTRO 250ML KRIGLA-12/1- | 250 g | 12 | 212 | 10,00–11,16 /kg | high/name |  |
| 18 | 3856020268909 | SENF ESTRAGON SQUEEZE 310G PODRAVKA (6) | 310 g | 11 | 420 | 6,13–8,74 /kg | high/name |  |
| 19 | 7610100999093 | Thomy senf delikatesni staklenka 700 g | 700 g | 11 | 185 | 0,66–133,93 /kg | high/name |  |
| 20 | 7613287203786 | Thomy Senf delikat.bez gl.340g STAKLO | 340 g | 10 | 451 | 8,21–9,68 /kg | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| GRICKALICE ELEPHANT MED, SENF I LUK 70G | 15 | `grickal` |
| SNACK MED SENF LUK 125 g ELEPH | 7 | `snack` |
| SNACK MED SENF LUK 75 g ELEPHA | 7 | `snack` |
| VEGETA GRILL MARINADA SENF MEDITERANSKO BILJE 75 G | 7 | `marinad` |
| GORUŠICA SJEMENKE ŠAFRAM 100G -20/1- | 4 | `sjeme` |
| SENF MINI FELIX 18 g PAGO | 3 | `felix` |
| N-ČIPS LAYS 120G MAXX SLATKI SENF -24/1- | 2 | `cips` |
| SENF ESTRAGON 1,2kg FELIX | 2 | `felix` |
| SENF FELIX 18G -100/1- | 2 | `felix` |
| CHIO CHIPS SENF 150g | 1 | `chips` |

</details>

<a id="majoneza"></a>
## majoneza (`majoneza`)

jedinica: **kg** · loose_produce: **false** · grupa: **185** · isključenih grupa: **22**

sinonimi: majoneza, majonez  
must_match: `majonez`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 8607100571137 | MAJONEZA 611G THOMY STAKLENKA NESTLE | 611 g | 23 | 878 | 5,71–13,08 /kg | high/name |  |
| 2 | 3858882210263 | MAJONEZA DELIKATES TUBA 165 g ZVIJEZDA | 165 g | 22 | 1395 | 13,94–20,55 /kg | high/name |  |
| 3 | 3856015325228 | MAJONEZA DELIKATES 85 G VRECICA ZVIJEZDA | 85 g | 22 | 1391 | 8,82–18,59 /kg | high/name |  |
| 4 | 3856015321879 | MAJONEZA DELIKATES 620g STAKLENKA ZVIJEZDA | 620 g | 22 | 1377 | 6,34–11,60 /kg | high/name |  |
| 5 | 7613287084606 | THOMY MAJONEZA DELIKATESNA TUBA 165G (20), NESTLE | 165 g | 21 | 1237 | 10,85–21,15 /kg | high/name |  |
| 6 | 3858890178678 | MAJONEZA THOMY DOYPACK VREĆICA S ČEPOM 263 g ALCA | 263 g | 21 | 913 | 9,47–16,69 /kg | high/name |  |
| 7 | 3856015322098 | N-MAJONEZA ZVIJEZDA 270G-12/1- DOYPACK | 270 g | 21 | 851 | 8,48–15,89 /kg | high/name |  |
| 8 | 3856015316660 | MAJONEZA ZVIJEZDA 15G SALATNA GASTRO -100/1 | 15 g | 21 | 797 | 14,67–32,67 /kg | high/name |  |
| 9 | 3858882219020 | N-MAJONEZA ZVIJEZDA 400G DELIKATES -8/1- | 400 g | 20 | 1170 | 8,98–14,23 /kg | high/name |  |
| 10 | 3858882210324 | MAJONEZA LAGANA U FOLIJI 95G (25), ZVIJEZDA | 95 g | 19 | 881 | 9,37–16,74 /kg | high/name |  |
| 11 | 3856015333926 | MAJONEZA DELIKATES ZVIJEZDA 165g+110g GRATIS TUBA ZVIJEZDA | 165 g | 15 | 952 | 15,09–18,12 /kg | high/name |  |
| 12 | 3856015321244 | N-MAJONEZA ZVIJEZDA 255G DELIKATES -12/1- | 255 g | 15 | 536 | 11,96–16,82 /kg | high/name |  |
| 13 | 3856015321909 | N-MAJONEZA ZVIJEZDA 620G LIGHT- 6/1- STAKLENKA | 620 g | 15 | 392 | 6,92–10,79 /kg | high/name |  |
| 14 | 3858890178692 | MAJONEZA THOMY 611 g+150 g GRATIS STAKLO ALCA | 611 g | 14 | 405 | 2,11–11,93 /kg | high/name |  |
| 15 | 8445292265522 | MAJONEZA THOMY 80 G VRECICA NESTLE | 80 g | 13 | 1067 | 8,75–22,38 /kg | high/name |  |
| 16 | 7613287084545 | MAJONEZA THOMY 265 G TUBA NESTLE | 265 g | 13 | 573 | 13,55–285,85 /kg | high/name |  |
| 17 | 8445291689152 | MAJONEZA THOMY 170G DOYPACK -18/1- | 170 g | 13 | 485 | 0,42–16,41 /kg | high/name |  |
| 18 | 7613035904958 | MAJONEZA 380G DOYPACK XL VREĆICA S ČEPOM THOMY | 380 g | 13 | 453 | 0,48–13,13 /kg | high/name |  |
| 19 | 3858882212946 | MAJONEZA SALATNA GASTRO 2kg ZVIJEZDA | 2 kg | 13 | 63 | 3,33–4,82 /kg | high/name |  |
| 20 | 3856015333148 | N-MAJONEZA ZVIJEZDA 270G + 230G GRATIS-12/1- DOYPACK | 270 g | 12 | 660 | 11,07–14,04 /kg | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| MAJONEZA CHILLI VREĆICA 85g ZVIJEZDA | 20 | `chilli` |
| N-MAJONEZA ZVIJEZDA 85G PRŽENI LUK -25/1- FOLIJA | 16 | `luk\b` |
| Zvijezda ketchup i majoneza tuba 165 g | 16 | `ketchup` |
| MAJONEZA CHILI 165G TUBA (12) ZVIJEZDA | 14 | `chili` |
| MAJONEZA S KETCHUP THOMY TUBA 190G THOMY (10) | 13 | `ketchup` |
| N-PAŠTETA RIO MARE 100G TUNA I MAJONEZA -12/1- TUBA | 9 | `tuna` |
| MAJONEZA VREĆ 80 g CHILLI THOMY | 4 | `chilli` |
| MAJONEZA MINI FELIX 18 g PAGO | 3 | `felix` |
| N-MAJONEZA THOMY 190G TOP2 MAJONEZA + KETCHUP -10/1- | 3 | `ketchup` |
| MAJONEZA MINI 18G FELIX | 2 | `felix` |

</details>

<a id="kecap"></a>
## kečap (`kecap`)

jedinica: **kg** · loose_produce: **false** · grupa: **181** · isključenih grupa: **38**

sinonimi: kecap, ketchup  
must_match: `kecap | ketchup | kecup`
atributi: vrsta = blagi, ljuti

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3858882210874 | N-KETCHUP ZVIJEZDA 500G -8/1-BLAGI | 500 g | 21 | 1382 | 2,78–5,76 /kg | high/name | vrsta=blagi |
| 2 | 3858882210898 | N-KETCHUP ZVIJEZDA 500G -8/1-LJUTI | 500 g | 21 | 1198 | 2,78–5,76 /kg | high/name | vrsta=ljuti |
| 3 | 3858882210881 | N-KETCHUP ZVIJEZDA 1000G BLAGI-8/1 | 1 kg | 20 | 1182 | 2,19–4,29 /kg | high/name | vrsta=blagi |
| 4 | 3850104268731 | KETCHUP BLAGI 500 G (6) PODRAVKA (PAL 85) | 500 g | 20 | 989 | 2,38–4,78 /kg | high/name | vrsta=blagi |
| 5 | 3850104240836 | KETCHUP BLAGI 1000 GR -PODRAVKA(6) (PAL 60) | 1 kg | 18 | 677 | 2,09–3,69 /kg | high/name | vrsta=blagi |
| 6 | 3856015316752 | KETCHUP ZVIJEZDA 15G -100/1- BLAGI | 15 g | 18 | 486 | 13,33–26,00 /kg | high/name | vrsta=blagi |
| 7 | 3850104268915 | KETCHUP LJUTI 500G(6) (PAL 85) PODRAVKA | 500 g | 17 | 698 | 3,38–4,98 /kg | high/name | vrsta=ljuti |
| 8 | 8715700421469 | KETCHUP BLAGI 570 g HEINZ | 570 g | 15 | 710 | 5,07–9,63 /kg | high/name | vrsta=blagi |
| 9 | 8715700421551 | HEINZ KETCHUP BLAGI 450G, ORBICO | 450 g | 14 | 728 | 4,42–8,27 /kg | high/name | vrsta=blagi |
| 10 | 3856015323200 | N-KETCHUP KIDS ZVIJEZDA 500G -8/1-BLAGI | 500 g | 14 | 624 | 2,78–5,76 /kg | high/name | vrsta=blagi |
| 11 | 3856020255961 | KETCHUP PODRAVKA 500G JALAPENO -6/1- | 500 g | 14 | 442 | 3,38–4,98 /kg | high/name |  |
| 12 | 3856015329134 | KETCHUP BLAGI BEZ DODANOG ŠEĆERA 500 g ZVIJEZDA | 500 g | 13 | 597 | 2,78–6,00 /kg | high/name | vrsta=blagi |
| 13 | 4006824991278 | N-KETCHUP DEVELEY 450G -8/1- | 450 g | 13 | 487 | 5,76–9,98 /kg | high/name |  |
| 14 | 5900783009564 | KEČAP KETCHUP LJUTI 455G HEINZ | 455 g | 13 | 463 | 4,37–8,18 /kg | high/name | vrsta=ljuti |
| 15 | 8715700421483 | Heinz Ketchup blagi XXL 1 kg | 1 kg | 11 | 631 | 4,00–7,09 /kg | high/name | vrsta=blagi |
| 16 | 8715700420363 | KETCHUP HEINZ 570G LJUTI-12/1- | 570 g | 9 | 560 | 5,07–8,75 /kg | high/name | vrsta=ljuti |
| 17 | 3850104268939 | KETCHUP PODRAVKA PIZZA 500 g | 500 g | 9 | 253 | 3,38–4,40 /kg | high/name |  |
| 18 | 3856020273880 | KETCHUP BLAGI 310 G PODRAVKA | 310 g | 8 | 487 | 4,81–5,97 /kg | high/name | vrsta=blagi |
| 19 | 3856020273910 | Podravka Ketchup ljuti 310 g | 310 g | 8 | 411 | 1,58–5,71 /kg | high/name | vrsta=ljuti |
| 20 | 8005110004674 | N-KETCHUP MUTTI 300G -6/1- BOCA | 300 g | 8 | 311 | 6,63–10,63 /kg | high/name | vrsta=blagi |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| Zvijezda ketchup i majoneza tuba 165 g | 16 | `majonez` |
| FLIPS TIP TOP 50G CUBICS KETCHUP -30/1- CHIO | 15 | `flips` |
| FLIPS DINI 30G MARBO KETCHUP-35/1- | 14 | `flips` |
| MAJONEZA S KETCHUP THOMY TUBA 190G THOMY (10) | 13 | `majonez` |
| FLIPS KROKI KROKET KETCHUP 120 G CHIO | 12 | `flips` |
| GRICKALICE POM BAR KETCHUP 50G CHIO | 12 | `grickal` |
| Chio Chips Čips ketchup style 130 g | 11 | `chips` |
| GRICKALICE KROKI KROKET TROKI KETCHUP 110G CHIO | 10 | `grickal` |
| FLIPS STIX KETCHUP 35 g BOBI | 8 | `flips` |
| BOBI FLIPS KETCHUP TOBY 40 G | 7 | `flips` |

</details>

<a id="voda"></a>
## voda (negazirana) (`voda`)

jedinica: **l** · loose_produce: **false** · grupa: **547** · isključenih grupa: **452**

sinonimi: voda, negazirana voda, izvorska voda  
must_match: `voda\b | vode\b`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 5449000034335 | Glaceau Voda za piće Smartwater 0,6L PET | 600 ml | 21 | 679 | 1,92–2,82 /l | high/name |  |
| 2 | 90311208 | VODA ROMERQUELLE 0,50 L NEGAZIRANA PVC COC | 500 ml | 19 | 770 | 1,78–2,70 /l | high/name |  |
| 3 | 9031100004187 | N-*VODA ROMERQUELLE 1.50L NEGAZIRANA -6/1- | 1,5 l | 19 | 527 | 0,52–1,03 /l | high/name |  |
| 4 | 3856022300188 | N-*VODA STUDENA 0.50L IZVORSKA -12/1- PET | 500 ml | 18 | 1078 | 0,80–2,18 /l | high/name |  |
| 5 | 5449000243089 | Glaceau Voda za piće Smartwater 1,1L PET | 1,1 l | 18 | 586 | 1,20–1354,55 /l | high/name |  |
| 6 | 3856022300157 | N-*VODA STUDENA 1.50L IZVORSKA -6/1- PET | 1,5 l | 17 | 1065 | 0,46–0,92 /l | high/name |  |
| 7 | 3875000184336 | VODA GAZ.0,5L SENSATION ASIA LIMET-KIWANO JAM.PET | 500 ml | 16 | 1149 | 1,80–2,98 /l | high/name |  |
| 8 | 3856022300867 | N-VODA STUDENAC 1.00L -12/1- ( POVRATNA AMBALAŽA ) | 1 l | 12 | 645 | 0,40–0,75 /l | high/name |  |
| 9 | 3875000184947 | VODA GAZ. MIN. SENSATION MANGO MARAKUJA 0,5L PET JAMNICA | 500 ml | 12 | 534 | 1,90–2,74 /l | high/name |  |
| 10 | 3858890879827 | MIN.VODA SENSATION LUBENICA LIMETA 1,5L | 1,5 l | 12 | 346 | 0,86–1,50 /l | high/name |  |
| 11 | 3872252000070 | *VODA LEDA 0.50L IZVORSKA -12/1- 114# | 500 ml | 11 | 570 | 0,72–2,04 /l | high/name |  |
| 12 | 4015600572969 | ORAL B VODA ZA USTA 500 ML PROEXP PROFPROT | 500 ml | 11 | 239 | 5,70–14,98 /l | high/name |  |
| 13 | 3850322007624 | KALA PRIRODNA IZVORSKA VODA 0.5 l (12) | 500 ml | 10 | 244 | 1,06–2,24 /l | high/name |  |
| 14 | 9031100003494 | VODA ROMERQUELLE 0.33L NEGAZIRANA -20/1- (POVRATNA AMBALAŽA ) | 330 ml | 10 | 111 | 2,18–6,03 /l | high/name |  |
| 15 | 3872252000018 | *VODA LEDA 1.50L IZVORSKA -6/1- 84# | 1,5 l | 9 | 558 | 0,35–0,72 /l | high/name |  |
| 16 | 3838471061407 | FUNK.VODA DONATURA.KLEKA 0,5 L | 500 ml | 9 | 491 | 3,38–4,38 /l | high/name |  |
| 17 | 3850322007600 | KALA PRIRODNA IZVORSKA VODA 1.5 l (6) | 1,5 l | 9 | 252 | 0,43–0,88 /l | high/name |  |
| 18 | 3858884603674 | Goda prirodna izvorska voda 6 l PET | 6 l | 9 | 210 | 0,22–0,48 /l | high/name |  |
| 19 | 9031100003517 | VODA ROMERQUELLE 0.75L NEGAZIRANA -12/1- ( POVRATNA AMBALAŽA ) | 750 ml | 9 | 26 | 1,35–1,72 /l | high/ean |  |
| 20 | 3872252000087 | VODA PRIRODNA IZVORSKA 5L | 5 l | 8 | 227 | 0,20–0,38 /l | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| N-*VODA JANA 0.50L PRIRODNA RČ MINERALNA -12/1- | 21 | `mineral` |
| Jana Negazirana mineral. voda, 1,5l | 20 | `mineral` |
| VODA NEGAZIRANA PRIRODNA MINERALNA CETINA 1,5 L PET | 20 | `mineral` |
| JAMNIČKA KISELICA GAZIRANA VODA PET 0.5L (12), JAMNICA | 18 | `gazir` |
| VODA NEGAZIRANA PRIRODNA MINERALNA CETINA 0,5 L | 18 | `mineral` |
| JAMNIČKA KISELICA GAZIRANA VODA 1L,(12) JAMNICA | 17 | `gazir` |
| VODA NEG.1,5L SARA PRIRODNA MINERALNA | 17 | `mineral` |
| VODA ROMERQUELLE 0,50 L GAZIRANA PVC COCA | 17 | `gazir` |
| *VODA ROMERQUELLE 0.50L LIMUNSKA TRAVA -12/1- GAZIRANA | 16 | `gazir` |
| N-*VODA CETINA 0.75L PRIRODNA MINERALNA -6/1- PET | 16 | `mineral` |

</details>
