# Pregled osnovnih namirnica

Generirano skriptom `scripts/staples_review.py` iz `src/mealmeter/staples.yaml` i arhive 2026-10-19.

**Ovo je prijedlog za ručni pregled**: za svaku namirnicu označi koji kandidati ne pripadaju
(→ dodaj `must_not_match`) i koji nedostaju (→ proširi `must_match`), pa ponovno pokreni skriptu.

Kandidati su grupe proizvoda (isti EAN, lanac + naziv bez EAN-a, ili klasa za jaja), poredane po
relevantnosti, broju lanaca i trgovina. Prikazuje se zadani izbor: bez rasprodaje (SNIŽENJE), bez
zadano isključenih varijanti i bez pakiranja izvan raspona. `€/jed` ne uključuje cijene izvan
`plausible_per_unit`; ⚠N je broj takvih (odbačenih) cijena u grupi. `pouzdanost` je
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
- [rajčica (konzerva: sjeckana, pelati, polpa)](#rajcica_konzerva) (`rajcica_konzerva`)
- [koncentrat rajčice](#koncentrat_rajcice) (`koncentrat_rajcice`)
- [mrkva](#mrkva) (`mrkva`)
- [paprika (svježa)](#paprika) (`paprika`)
- [krastavac (svježi)](#krastavac) (`krastavac`)
- [tikvica](#tikvica) (`tikvica`)
- [kupus (svježi)](#kupus) (`kupus`)
- [kiseli kupus](#kiseli_kupus) (`kiseli_kupus`)
- [zelena salata (glavice)](#zelena_salata) (`zelena_salata`)
- [rukola](#rukola) (`rukola`)
- [matovilac](#matovilac) (`matovilac`)
- [radič](#radic) (`radic`)
- [endivija](#endivija) (`endivija`)
- [špinat](#spinat) (`spinat`)
- [peršin](#persin) (`persin`)
- [gljive (šampinjoni)](#gljive) (`gljive`)
- [riža](#riza) (`riza`)
- [tjestenina](#tjestenina) (`tjestenina`)
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
- [senf](#senf) (`senf`)
- [majoneza](#majoneza) (`majoneza`)
- [kečap](#kecap) (`kecap`)

<a id="brasno"></a>
## brašno (`brasno`)

jedinica: **kg** · loose_produce: **false** · grupa: **374** · isključenih grupa: **106** · plausible: **0.4–6 €/kg** · pakiranje: **500–5000** · zadano bez: **tip=integralno, gluten=bez**

sinonimi: brasno, psenicno brasno  
must_match: `brasn | bras\b`
  
atributi: tip = glatko, ostro, polubijelo, integralno; vrsta = psenicno, pirovo, razeno, kukuruzno; gluten = bez; oznaka = t400, t550, t850, t1100, 00

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3858884172569 | PŠENIČNO BRAŠNO 1KG GLATKO T-550,ČAKOVEČKI MLINOVI | 1 kg | 20 | 861 | 0,75–1,69 /kg | high/name | oznaka=t550, tip=glatko, vrsta=psenicno |
| 2 | 3850104052552 | BRAŠNO KUKURUZNO 1KG (10) (PAL 60), PODRAVKA | 1 kg | 19 | 674 | 1,21–1,89 /kg | high/name | vrsta=kukuruzno |
| 3 | 3850104223624 | BRAŠNO GLATKO T-550 1KG (10) (PAL 60) PODRAVKA | 1 kg | 18 | 1167 | 0,62–0,83 /kg | high/name | oznaka=t550, tip=glatko, vrsta=psenicno |
| 4 | 3850104223631 | BRAŠNO PŠEN. T-400 OŠTRO 1 KG (10) (PAL60) PODRAVKA | 1 kg | 17 | 926 | 0,69–0,83 /kg | high/name | oznaka=t400, vrsta=psenicno, tip=ostro |
| 5 | 3858884172637 | BRASNO T-400 1 KG CAKOVECKI MLINOVI - OSTRO ZA KOLACE | 1 kg | 16 | 953 | 0,82–0,83 /kg ⚠9 | high/name | oznaka=t400, tip=ostro, vrsta=psenicno |
| 6 | 3858884172583 | BRAŠNO PŠENIČNO T-400 ZA DIZANA TIJESTA 1KG ČAKOVEČKI MLINOV | 1 kg | 16 | 895 | 1,09–1,92 /kg | high/name | oznaka=t400, vrsta=psenicno |
| 7 | 3858884172521 | BRAŠNO PŠENIČNO GLATKO T-550, 5KG ČAKOVEČKI MLINOVI(PAL200) | 5 kg | 16 | 703 | 0,71–0,80 /kg ⚠4 | high/name | tip=glatko, oznaka=t550, vrsta=psenicno |
| 8 | 3850104223617 | PŠEN.BRAŠNO T 550 GLATKO 2 KG PODRAVKA(6) (PAL 48) | 2 kg | 15 | 823 | 0,56–0,82 /kg | high/name | oznaka=t550, tip=glatko, vrsta=psenicno |
| 9 | 3850104063084 | BRAŠNO PODR 1KG POLUBIJELO T-850 -10/1- | 1 kg | 15 | 468 | 1,07–1,72 /kg | high/name | oznaka=t850, vrsta=psenicno, tip=polubijelo |
| 10 | 3850104223648 | PŠEN.BRAŠNO T -400 OŠTRO 2 KG, PODRAVKA(6) (PAL 48) | 2 kg | 14 | 694 | 0,45–0,85 /kg | high/name | oznaka=t400, tip=ostro, vrsta=psenicno |
| 11 | 3858884172576 | BRAŠNO ZA TANKA TIJESTA 1 kg T- 700 ČAKOVEČKI MLI | 1 kg | 12 | 643 | 1,09–1,69 /kg | high/name |  |
| 12 | 3850104423659 | BRAŠNO GL.T-550 5 kg PŠ.BIJELO PODRAVKA | 5 kg | 11 | 286 | 0,54–1,03 /kg | high/name | oznaka=t550, vrsta=psenicno, tip=glatko |
| 13 | 3858884172538 | BRAŠNO OŠTRO ZA KOLAČE T-400 5KG,ČAKOVEČKI MLINOVI | 5 kg | 10 | 381 | 0,75–0,84 /kg | high/name | oznaka=t400, tip=ostro |
| 14 | 3858884170169 | BRAŠNO KUKURUZNO 1KG ČAKOVEČKI MLIN (10) | 1 kg | 9 | 420 | 1,31–1,79 /kg | high/name | vrsta=kukuruzno |
| 15 | 3858884175751 | BRAŠNO PŠENIČNO T-550 ZA PIZZU 1KG ČAKOVEČKI MLINOVI | 1 kg | 9 | 405 | 1,39–1,95 /kg | high/name | vrsta=psenicno, oznaka=t550 |
| 16 | 3859891753246 | N-BRAŠNO ULTRA 1KG GLATKO T-550 -10/1- | 1 kg | 8 | 161 | 0,68–0,80 /kg | high/ean | oznaka=t550, vrsta=psenicno, tip=glatko |
| 17 | 3850104065019 | BRAŠNO RAŽENO 900G T-1250 PODRAVKA | 900 g | 8 | 36 | 1,31–2,54 /kg | high/name | vrsta=razeno |
| 18 | 3850104423604 | PŠEN.BRAŠNO T -400 OŠTRO 5 KG, PODRAVKA | 5 kg | 7 | 190 | 0,62–0,83 /kg | high/name | oznaka=t400, vrsta=psenicno, tip=ostro |
| 19 | 3858887101009 | BRAŠNO FARINA SPECIALE PŠENIČNO TIP 00 1kg (10) | 1 kg | 6 | 443 | 0,99–1,65 /kg | high/name | oznaka=00, vrsta=psenicno |
| 20 | 3858884175768 | BRAŠNO ZA BUREK POLUBIJ. T-700 1 kg | 1 kg | 6 | 180 | 1,43–1,79 /kg | high/name | vrsta=psenicno |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| SMJESA ZA KRUH (BEZGLUTENSKO BRAŠNO) DR.SCHÄR MIX B 1KG (10) | 15 | `mix\b` |
| KOKOS BRAŠNO 200G (10), ŠAFRAM | 14 | `kokos` |
| HELJDINO BRAŠNO 1 kg PODRAVKA (10) | 13 | `heljd` |
| SUPERFOODS eko kokosovo brašno 250g | 10 | `kokos` |
| KOKOS BRAŠNO 200G(20) NATURA, MARJAN VOĆE | 8 | `kokos` |
| Š EXTRA KOKOS BRAŠNO ŠAFRAM 200 g (10) | 8 | `kokos` |
| BRAŠNO MIX IT 500G BEZ GLUTENA -10/1 DR.SCHAR | 7 | `mix\b` |
| N-TOAST KLARA ZP 500G S INTEG. BRAŠNOM -8/1- | 7 | `toast` |
| ULTRA KOKOS BRAŠNO 200G, ŠAFRAM (10) | 7 | `kokos` |
| BIO BRAŠNO ZOBENO 250 g ENCIAN | 6 | `zob` |

</details>

<a id="secer"></a>
## šećer (`secer`)

jedinica: **kg** · loose_produce: **false** · grupa: **234** · isključenih grupa: **113** · plausible: **0.6–8 €/kg** · pakiranje: **250–5000** · zadano bez: **vrsta=smedi, vrsta=u_prahu, vrsta=kocke**

sinonimi: secer  
must_match: `secer\b`
  
atributi: vrsta = u_prahu, smedi, kocke, bijeli

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 9007829025017 | Agragold Šećer kristal 1kg_OC | 1 kg | 11 | 392 | 0,65–1,33 /kg | high/name | vrsta=bijeli |
| 2 | 3859893641008 | ŠEĆER KRISTAL VIROVITICA 1kg (10) | 1 kg | 10 | 759 | 0,75–0,99 /kg | high/name | vrsta=bijeli |
| 3 | 3830049080018 | ŠEĆER BIJELI KRISTAL 1KG DIAMANT | 1 kg | 10 | 334 | 0,79–1,33 /kg | high/name | vrsta=bijeli |
| 4 | 8436560216964 | SECER BIJELI 1 KG JUST SUGAR | 1 kg | 7 | 229 | 0,89–1,33 /kg | high/name | vrsta=bijeli |
| 5 | 4000521730000 | ŽELIRNI ŠEĆER EXTRA 500G 2:1, DR.OETKER | 500 g | 7 | 151 | 6,46–7,98 /kg ⚠7 | high/name |  |
| 6 | 3859888112049 | ŠEĆER KRISTAL 1KG (10), VIROVITICA(960) | 1 kg | 7 | 77 | 0,79–1,33 /kg | high/name | vrsta=bijeli |
| 7 | 4000521011314 | Dr.Oetker Šećer želirni sa stevijom 350g | 350 g | 6 | 115 | – ⚠115 | – |  |
| 8 | 3850291200637 | ŠEĆER UGOST.BIJELI 4gr.600/1 FRANCK (1) | 2,4 kg | 5 | 58 | 3,31–5,41 /kg | high/name | vrsta=bijeli |
| 9 | 8594000230250 | ŠEĆER KRISTAL 1 kg TEREO | 1 kg | 4 | 165 | 0,89–0,99 /kg | high/name | vrsta=bijeli |
| 10 | 3858891761169 | ŠEĆER BREZIN-XYLITOL 350g GREEN LAB | 350 g | 4 | 75 | – ⚠75 | – |  |
| 11 | 3850291049489 | ŠEĆER BIJELI UGOSTITELJSKI 600X4G FRANCK | 2,4 kg | 4 | 9 | 2,50–3,75 /kg ⚠5 | high/name | vrsta=bijeli |
| 12 | 9012501003276 | ŠEĆER 25/1 BIJELI KRISTALNI |  | 3 | 32 | 0,92–1,00 /kg | low/unit_price | vrsta=bijeli |
| 13 | 9007829021019 | ŠEĆER KRISTAL AGRAG. 1 kg | 1 kg | 3 | 23 | 0,69–1,31 /kg | high/name | vrsta=bijeli |
| 14 | 8436560216452 | 1KG JUST SUGAR BIJEL KRI.ŠEĆER | 1 kg | 3 | 14 | 0,99 /kg ⚠1 | high/name | vrsta=bijeli |
| 15 | 3858884353753 | DOZATOR ZA ŠEĆER 6,5 X 15cm |  | 3 | 12 | – | – |  |
| 16 | 8436560216568 | JUST SUGAR 1kg ŠEĆER KRISTAL | 1 kg | 3 | 3 | 1,06–1,33 /kg | high/name | vrsta=bijeli |
| 17 | 3859888616271 | SECER 1 KG | 1 kg | 2 | 96 | 0,80–1,06 /kg | high/name |  |
| 18 | 9007829023099 | KIARA BIJELI KRISTALNI ŠEĆER 1kg | 1 kg | 2 | 29 | 0,99–1,33 /kg | high/name | vrsta=bijeli |
| 19 | 4337182260042 | 1KG ARO BIJELI KRISTAL ŠEĆER | 1 kg | 2 | 8 | 0,90–0,94 /kg | high/name | vrsta=bijeli |
| 20 | 8436585140022 | ŠEĆER 1 kg | 1 kg | 1 | 343 | 0,99 /kg | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| LIMUN ŠEĆER 10G (50) PODRAVKA (PAL 468) | 19 | `limun` |
| DOLCELA VANILIN ŠEĆER 8 g 5+1 GRATIS PODRAVKA (44) | 18 | `vanilin` |
| RUM ŠEĆER 10G (50) PODRAVKA (PAL 468) | 18 | `rum\b` |
| DOLCELA LIMUN ŠEĆER 10 g 3 PAK (26) PODRAVKA | 17 | `limun` |
| DOLCELA VANILIN ŠEĆER 8 g PODRAVKA (44) | 17 | `vanilin` |
| DOLCELA RUM ŠEĆER 10 g 3 PAK (26) PODRAVKA | 15 | `rum\b` |
| ŠEĆER CIMET 10G 3PAK DOLCELA PODRAVKA | 14 | `cimet` |
| VANILIN ŠEĆER DR OETKER 8G -50/1- | 12 | `vanilin` |
| VANILIN ŠEĆER BURBON 10G(50) DR.OETKER | 11 | `vanilin` |
| KOTANYI VANILIN ŠEĆER AROMA LIMUNA 50g | 10 | `vanilin` |

</details>

<a id="sol"></a>
## sol (`sol`)

jedinica: **kg** · loose_produce: **false** · grupa: **162** · isključenih grupa: **258** · plausible: **0.2–8 €/kg** · pakiranje: **250–5000** · zadano bez: **vrsta=himalajska, vrsta=smanjeni_natrij** · **pantry**

sinonimi: sol, kuhinjska sol  
must_match: `sol\b`
  
atributi: vrsta = smanjeni_natrij, morska, himalajska, kamena, jodirana; zrno = sitna, krupna

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3859888155114 | SOL KUHINJSKA SITNA MORSKA KUTIJA 1KG, SOLANA PAG | 1 kg | 20 | 836 | 0,66–1,39 /kg | high/name | zrno=sitna, vrsta=morska |
| 2 | 3870009000014 | SOL KUHINJSKA KAMENA 1KG (10), TUZLA | 1 kg | 16 | 1131 | 0,59–1,09 /kg | high/name | vrsta=kamena, zrno=sitna |
| 3 | 3859888155107 | SOL KUHINJSKA KRUPNA MORSKA KUTIJA 1KG, SOLANA PAG | 1 kg | 14 | 534 | 0,85–1,31 /kg | high/name | zrno=krupna, vrsta=morska |
| 4 | 3870009000328 | SOL KUHINJSKA KAMENA VARENA 5KG, TUZLA | 5 kg | 12 | 576 | 0,38–0,74 /kg | high/name | vrsta=kamena, zrno=sitna |
| 5 | 3859888817005 | SOL SITNA MORSKA 1KG KK PAG91 (960KG=1 PAL) | 1 kg | 11 | 582 | 0,69–1,39 /kg | high/name | zrno=sitna, vrsta=morska |
| 6 | 3859888155435 | SOL MORSKA KRUPNA 5KG PVC SOLANA (24) | 5 kg | 10 | 167 | 0,53–0,94 /kg | high/name | zrno=krupna, vrsta=morska |
| 7 | 3859888155398 | SOL KUHINJSKA MORSKA SITNA 5KG, SOLANA PAG | 5 kg | 9 | 237 | 0,44–0,92 /kg | high/name | zrno=sitna, vrsta=morska |
| 8 | 3859888155442 | SOL KUHINJSKA MORSKA KRUPNA PVC 1KG, SOLANA PAG(12) | 1 kg | 9 | 212 | 0,49–3,26 /kg | high/name | zrno=krupna, vrsta=morska |
| 9 | 3859888817036 | Pag 91 kuhinj. morska sol krupna 1kg PVC | 1 kg | 8 | 494 | 0,49–0,99 /kg | high/name | zrno=krupna, vrsta=morska |
| 10 | 3859888595118 | SOL MORSKA SITNA PVC 1kg SOLANA NIN | 1 kg | 8 | 446 | 0,79–1,19 /kg | high/name | zrno=sitna, vrsta=morska |
| 11 | 3859888817012 | Pag 91 kuhins. morska sol krupna 1 kg kk | 1 kg | 8 | 440 | 0,74–1,15 /kg | high/name | zrno=krupna, vrsta=morska |
| 12 | 3859888155077 | SOL KUHINJSKA MORSKA PVC 1KG, SOLANA PAG (10)(PAL800) | 1 kg | 8 | 365 | 0,62–0,99 /kg | high/name | zrno=sitna, vrsta=morska |
| 13 | 3859888817029 | Pag 91 kuh. morska sol sitna 1kg pvc | 1 kg | 7 | 581 | 0,49–1,09 /kg | high/name | zrno=sitna, vrsta=morska |
| 14 | 3859892380533 | KUHINJSKA SOL 1KG (20) ULTRA (740PAL) | 1 kg | 7 | 76 | 0,51–0,74 /kg | high/name | zrno=sitna |
| 15 | 3859888817135 | Pag 91 kuh.morska sol sitna 5 kg, pvc | 5 kg | 6 | 380 | 0,31–0,60 /kg | high/name | zrno=sitna, vrsta=morska |
| 16 | 3859888595989 | SOL SITNA MORSKA BIO 600 G SOLANA NIN | 600 g | 6 | 238 | 0,83–4,48 /kg | high/name | zrno=sitna, vrsta=morska |
| 17 | 3858881730014 | SOL KUHINJSKA JODIRANA KAMENA 1KG (20), DERMA | 1 kg | 6 | 128 | 0,99–1,89 /kg | high/ean | vrsta=kamena |
| 18 | 3859888817159 | SOL MORSKA 5 kg KRUPNA PAG 91( 1/1 ) | 5 kg | 5 | 351 | 0,34–0,60 /kg | high/name | zrno=krupna, vrsta=morska |
| 19 | 3859888155589 | SOL MORSKA SITNA CA/MG 1kg SOL PAG | 1 kg | 4 | 290 | 1,05–2,09 /kg | high/name | zrno=sitna, vrsta=morska |
| 20 | 3859888595996 | SOL GRUBA MORSKA BIO 600 G SOLANA NIN | 600 g | 4 | 182 | 3,32–4,32 /kg | high/name | vrsta=morska, zrno=krupna |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| ČIPS ČIPI ČIPS 120G SOL I PAPAR ULTRA REBRASTI -20/1- CHIO | 17 | `papar` |
| TRAJNO PEC. ELEP.TWIST - MORSKA SOL I MED 180g | 12 | `med\b` |
| KOTANYI 185G PAPAR CRNI MLJEV 50G + SOL 135G GRATIS -1/1- | 11 | `papar` |
| SOL MORSKA SITNA 250G SOLJENKA -12/1- PAG | 11 | `soljenk` |
| SOL SITNA MORSKA 250g PAG91 SOLJENKA | 10 | `soljenk` |
| TRAJNO PEC. ELEP.TWIST - MORSKA SOL I MED 160g | 10 | `med\b` |
| N-*PIVO SOL 0.33L -24/1- 4.5%ALC BOCA | 9 | `pivo` |
| KOTANYI MLINAC 65G PAPAR I SOL - 4/1- | 8 | `papar` |
| MIRODIJE CHILI I SOL MLINAC 40G VEGETA MAESTRO PODRAVKA | 8 | `chili` |
| KREKER MOR.SOL 70 g BOOM BOX ATLANTIC | 7 | `kreker` |

</details>

<a id="ulje"></a>
## ulje (suncokretovo/biljno) (`ulje`)

jedinica: **l** · loose_produce: **false** · grupa: **170** · isključenih grupa: **787** · plausible: **1–12 €/l** · pakiranje: **500–5000** · zadano bez: **vrsta=avokado, vrsta=sezam, vrsta=kokos, vrsta=grozde, vrsta=specijalno**

sinonimi: ulje, suncokretovo ulje, biljno ulje, jestivo ulje  
must_match: `ulje\b`
  
atributi: vrsta = avokado, sezam, kokos, grozde, specijalno, suncokretovo, repicino, biljno

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
| 9 | 3856015312044 | Zvijezda Ulje suncokretovo XXL 4x1 L | 4 l | 8 | 457 | 1,25–1,67 /l | high/name | vrsta=suncokretovo |
| 10 | 8600498170029 | ULJE SUNCOKRET 1L DIJAMANT (15) | 1 l | 4 | 114 | 1,49–1,72 /l | high/name | vrsta=suncokretovo |
| 11 | 3858891568386 | ULTRA SUNCOKRETOVO ULJE 1L (15) (750 PAL) | 1 l | 4 | 68 | 1,49–1,69 /l | high/name | vrsta=suncokretovo |
| 12 | 3856003920145 | ULJE SUNCOKRETOVO 1 L ZORELA | 1 l | 3 | 475 | 1,49–1,69 /l | high/name | vrsta=suncokretovo |
| 13 | 3859894292001 | ULJE SUNCOKRET PLUTUS OILUS 1 L | 1 l | 3 | 131 | 1,56–1,69 /l | high/name | vrsta=suncokretovo |
| 14 | 3857500104335 | ULJE SUNCE VINKOVACA 5L HLADNO PREŠANO (1) | 5 l | 3 | 65 | 1,55–2,90 /l | high/name | vrsta=suncokretovo |
| 15 | 3858883227079 | ULJE SUNCOKRETOVO 1 l BAKINA KUHINJA, HR | 1 l | 3 | 34 | 1,49–2,12 /l | high/name | vrsta=suncokretovo |
| 16 | 3858882210034 | ULJE SUNCOKRETOVO 1L ZVIJEZDA | 1 l | 3 | 9 | 1,70–1,72 /l ⚠7 | high/name | vrsta=suncokretovo |
| 17 | 3858894591787 | ULTRA SUNCOKRETOVO ULJE 1L(15) PAL 765 | 1 l | 3 | 6 | 1,59–1,69 /l | high/name | vrsta=suncokretovo |
| 18 | 3856015326652 | ULJE SUNCOKRET 1 L + 200 mL gratis ZVIJEZDA (12) | 1,2 l | 2 | 134 | 1,54–3,45 /l | high/unit | vrsta=suncokretovo |
| 19 | 3856003944523 | ULJE SUNCOKRET 1L ZORELA | 1 l | 2 | 133 | 1,59–1,69 /l | high/name | vrsta=suncokretovo |
| 20 | 8007153008374 | ULJE MIX SJEMEN. 1 l FIOR DI VITA FARCH | 1 l | 2 | 46 | 2,89–6,25 /l | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| ULJE MASLINOVO EXTRA DJEVICANSKO 1 L ZVIJEZDA STAKLO | 22 | `masli` |
| ULJE MASLINOVO EXTRA DJEVICANSKO 0.5 L ZVIJEZDA STAKLO | 19 | `masli` |
| N-ULJE MASL. 1L ORGULA TRADICIJA EXTRA DJEVIČANSKO -6/1- EKO | 16 | `dev` |
| ULJE BUCINO 500 ML ZVIJEZDA STAKLO | 16 | `bucin` |
| RIO MARE TUNA MAS.ULJE 2x80 g OC.MASA 104 g (48) | 12 | `mas\b` |
| RIO MARE TUNA MASL.ULJE 3X80G OC.MASA 156G (32) | 12 | `masl\b` |
| ULJE MASLINOVO 1 L BLAGO TRENTON UG. | 10 | `masli` |
| ULJE MASLINOVO S OKUSOM CRNOG TARTUFA 100 ML ZIGANTE | 10 | `masli` |
| N-ULJE MASL. 0.25L ORGULA TRADICIJA EXTRA DJEVIČANSKO -12/1- EKO | 9 | `dev` |
| N-ULJE MASL. 0.75L ORGULA TRADICIJA EXTRA DJEVIČANSKO -6/1- EKO | 9 | `dev` |

</details>

<a id="maslinovo_ulje"></a>
## maslinovo ulje (`maslinovo_ulje`)

jedinica: **l** · loose_produce: **false** · grupa: **344** · isključenih grupa: **78** · plausible: **4–60 €/l** · pakiranje: **250–5000**

sinonimi: maslinovo ulje, maslinovo  
must_match: `maslinovo ulje | ulje maslinovo | masl ulje | ulje masl | ekstra devicansko | extra devicansko | extra virgin`
  
atributi: kvaliteta = ekstra_djevicansko, djevicansko

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3858882211550 | ULJE MASLINOVO EXTRA DJEVICANSKO 1 L ZVIJEZDA STAKLO | 1 l | 22 | 885 | 10,99–21,80 /l | high/name | kvaliteta=ekstra_djevicansko |
| 2 | 3858882211574 | ULJE MASLINOVO EXTRA DJEVICANSKO 0.5 L ZVIJEZDA STAKLO | 500 ml | 19 | 901 | 12,20–20,78 /l | high/name | kvaliteta=ekstra_djevicansko |
| 3 | 3859890446217 | N-ULJE MASL. 1L ORGULA TRADICIJA EXTRA DJEVIČANSKO -6/1- EKO | 1 l | 16 | 869 | 5,99–16,99 /l | high/name | kvaliteta=ekstra_djevicansko |
| 4 | 3859888906051 | ULJE MASLINOVO 1 L BLAGO TRENTON UG. | 1 l | 10 | 563 | 6,16–9,55 /l ⚠1 | high/name |  |
| 5 | 80053835 | ULJE MASLINOVO EXTRA DJEVICANSKO 1 L MONINI STAKLO | 1 l | 9 | 800 | 7,99–15,59 /l | high/name | kvaliteta=ekstra_djevicansko |
| 6 | 3858881192713 | ULJE MASLINOVO EXTRA DJEVICANSKO 750 ML OL ISTRIA | 750 ml | 9 | 600 | 26,59–35,99 /l | high/name | kvaliteta=ekstra_djevicansko |
| 7 | 3859890446200 | N-ULJE MASL. 1L ORGULA HARMONIJA EXTRA DJEVIČANSKO -6/1 EKO | 1 l | 9 | 431 | 6,19–16,19 /l | high/name | kvaliteta=djevicansko |
| 8 | 3859890446545 | N-ULJE MASL. 750ML ORGULA ZLATNO EXTRA DJEVIČANSKO -6/1- EKO | 750 ml | 9 | 403 | 13,32–21,05 /l | high/name | kvaliteta=ekstra_djevicansko |
| 9 | 3859890446026 | N-ULJE MASL. 0.25L ORGULA TRADICIJA EXTRA DJEVIČANSKO -12/1- EKO | 250 ml | 9 | 304 | 13,88–21,56 /l ⚠4 | high/name | kvaliteta=ekstra_djevicansko |
| 10 | 3859888295025 | ULJE MASLINOVO EKSTRA DJEVICANSKO 0,75 L PZ MARINA | 750 ml | 8 | 544 | 20,92–24,25 /l | high/name | kvaliteta=ekstra_djevicansko |
| 11 | 3858881192485 | ULJE MASLINOVO EXTRA DJEVICANSKO 0,25 L OL ISTRIA | 250 ml | 8 | 471 | 34,40–46,36 /l | high/name | kvaliteta=djevicansko |
| 12 | 3859890446019 | N-ULJE MASL. 0.75L ORGULA TRADICIJA EXTRA DJEVIČANSKO -6/1- EKO | 750 ml | 8 | 420 | 11,68–17,99 /l | high/name | kvaliteta=ekstra_djevicansko |
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
| RIB. K. TUNA RIO MARE MASL. ULJE 2 X 80 g ORB | 9 | `tuna` |
| RIO MARE TUNA MASL.ULJE 3X80G OC.MASA 156G (32) | 9 | `tuna` |
| ULJE MASLINOVO S OKUSOM CRNOG TARTUFA 100 ML ZIGANTE | 8 | `okus` |
| MASLINOVO ULJE S OKUSOM BIJELOG TARTUFA 60 ML ZIGANTE | 7 | `okus` |
| ULJE MASLINOVO S OKUSOM BIJELOG TARTUFA 100 ML ZIGANTE | 7 | `okus` |
| ULJE MASLINOVO S OKUSOM CRNOG TARTUFA 60 ML ZIGANTE | 7 | `okus` |
| RIB.K.TUNA 160 g ( 104 g) RIO MARE MASL.ULJE ORBI | 6 | `tuna` |
| TUNA FILETI MASL. ULJE AQ 105g/73,5g | 5 | `tuna` |
| KREKER CRICH MASLINOVO ULJE/RUŽMARIN 250G | 4 | `kreker` |
| TUNA MASLINOVO ULJE 2X160 G RIO MARE | 4 | `tuna` |

</details>

<a id="maslac"></a>
## maslac (`maslac`)

jedinica: **kg** · loose_produce: **false** · grupa: **198** · isključenih grupa: **265** · plausible: **6–40 €/kg** · pakiranje: **100–1000**

sinonimi: maslac, puter, butter  
must_match: `maslac | puter\b | butter\b | markenbutter`
  
atributi: vrsta = slani, neslani

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850108060102 | MASLAC 250 g ZBREGOVLOT:1626022111 | 250 g | 20 | 1355 | 9,96–18,72 /kg | high/name |  |
| 2 | 3850355000999 | N-DUKAT MASLAC 250G I KLASA-20/1- 603 | 250 g | 18 | 1167 | 7,56–17,64 /kg | high/name |  |
| 3 | 3850108060126 | MASLAC 'Z BREGOV 125 G VINDIJA | 125 g | 17 | 694 | 11,12–22,00 /kg | high/name |  |
| 4 | 3850355003969 | Dukat maslac I klase 82% mm 125 g | 125 g | 16 | 680 | 15,12–25,20 /kg | high/name |  |
| 5 | 3858888590345 | Zdenka Maslac min.82% m.m. 250g | 250 g | 13 | 687 | 7,40–21,16 /kg | high/name |  |
| 6 | 3858885565612 | PUTER ŠTANGICA 180 g (3X60 g) TVOJIH 5 MINUTA | 180 g | 11 | 521 | 9,94–16,61 /kg | high/name |  |
| 7 | 4002174000233 | MASLAC 250 G BAYERNLAND STANIC | 250 g | 10 | 497 | 7,16–25,96 /kg ⚠31 | high/name |  |
| 8 | 3155250367094 | PRESIDENT MASLAC S MORSKOM SOLI 250 g DUKAT (12) | 250 g | 9 | 249 | 12,72–18,76 /kg | high/name | vrsta=slani |
| 9 | 4006496018129 | MASLAC 250 g (82 % m.m.) JAEGER ALPINETTA | 250 g | 7 | 649 | 6,76–11,96 /kg ⚠46 | high/name |  |
| 10 | 5740900400016 | N-MASLAC 200G LURPAK -20/1- | 200 g | 7 | 342 | 9,45–17,95 /kg | high/name |  |
| 11 | 4033854001431 | MASLAC 250 g DEUTSCHE MARKENBUTTER | 250 g | 7 | 192 | 7,08–14,72 /kg | high/name |  |
| 12 | 3228022910023 | MASLAC PRESIDENT 200G -20/1- 51157 | 200 g | 7 | 174 | 16,70–25,75 /kg | high/name |  |
| 13 | 4034900004925 | Meggle Premium maslac 82% m.m. 200 g | 200 g | 6 | 435 | 13,95–22,45 /kg | high/name |  |
| 14 | 3228022000298 | MASLAC LIGHT - NESLANI 250G PRESIDENT | 250 g | 6 | 196 | 17,16–18,76 /kg | high/name | vrsta=neslani |
| 15 | 3228022020050 | MASLAC PDT MOTTE MEKI NESLANI 250G 82%MM -12/1- | 250 g | 6 | 74 | 16,36–21,56 /kg | high/name | vrsta=neslani |
| 16 | 3859892380106 | N-MASLAC 250G DOMAĆA KRAVICA81013 /81014 -40/1 | 250 g | 6 | 71 | 9,56–11,96 /kg | high/name |  |
| 17 | 4034900004932 | MASLAC PREMIUM 82% MM 250 g MEGGL | 250 g | 5 | 255 | 13,16–17,56 /kg | high/name |  |
| 18 | 4006496012028 | MASLAC BURRO BAVARESE 250g | 250 g | 5 | 190 | 6,36–11,96 /kg ⚠155 | high/name |  |
| 19 | 5907627470771 | Maslac od kozijeg mlijeka 125 g | 125 g | 4 | 253 | 14,32–18,32 /kg | high/name | vrsta=slani |
| 20 | 5011308303200 | UMAK MILD BUTTER CHICKEN 450 G PATAK'S | 450 g | 4 | 163 | 10,42–12,87 /kg ⚠5 | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| GRICKALICE SMOKICE MASLAC 85G ŠTARK | 17 | `smokic` |
| Margo Namaz miješani s maslacem 225g | 14 | `namaz` |
| KEKSI JAFFA BUTTONS KIKIRIKI MASLAC 95GK | 12 | `kikiriki` |
| KEKSI PETIT BEURE S MASLACEM BEZ GLUTENA 130G BALVITEN | 12 | `keks` |
| KOKICE BOBI GOTOVE S OKUSOM MASLACA 100G | 11 | `kokic` |
| KOKICE ZA MIKROVALNU POP!!! CORN MASLAC 240 g 3X80 g | 10 | `kokic` |
| MASLAC SA ZAČINSKIM BILJEM 125g MEGL (8) | 10 | `zacinsk` |
| KOKICE ZA MIKROV MASLAC 80 g POPCORN | 9 | `kokic` |
| KOKICE ZA MIKROVALNU S MASLACEM 300 g 3X100 g MOGYI | 9 | `kokic` |
| SLADOLED MACHO KIKIRIKI MASLAC KARAMELA SENDVIČ 129 ml LEDO | 9 | `kikiriki` |

</details>

<a id="margarin"></a>
## margarin (`margarin`)

jedinica: **kg** · loose_produce: **false** · grupa: **100** · isključenih grupa: **0** · pakiranje: **200–1000**

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
| 8 | 3856015305534 | N-MARGARIN ZVIJEZDA STOLNI 250G S AROMOM VANILIJE -24/1- | 250 g | 16 | 496 | 3,12–6,36 /kg ⚠2 | high/name |  |
| 9 | 3858883227406 | MARGARINSKI NAMAZ MARGARITA 500 G BAKINA KUHINJA STANIC | 500 g | 15 | 850 | 1,98–6,58 /kg | high/name |  |
| 10 | 3856015332974 | MARGARIN MARGO BUTTERY 400G ZVIJEZDA | 400 g | 14 | 606 | 3,73–7,48 /kg | high/name |  |
| 11 | 3856015325419 | MARGARIN MARGO S MASLACEM 225G ZVIJEZDA | 225 g | 14 | 602 | 6,18–12,40 /kg | high/name |  |
| 12 | 3858883228885 | MARGARIN ZA KOLAČE I KUHANJE 250 g BAKINA KUHINJ | 250 g | 13 | 738 | 2,76–6,56 /kg | high/name |  |
| 13 | 8585037200491 | MARGARIN ZA JELO I KUHANJE 250g FC | 250 g | 12 | 612 | 2,36–4,08 /kg | high/name |  |
| 14 | 8719200264915 | MARGARIN RAMA CLASS. 225 g | 225 g | 12 | 523 | 3,96–9,33 /kg | high/name |  |
| 15 | 8719200198869 | MARGARIN RAMA ZA KOLAČE 250 g STANI | 250 g | 10 | 549 | 2,36–7,96 /kg | high/name |  |
| 16 | 8719200265097 | MARGARIN RAMA CLASSIC 400 g STANI | 400 g | 10 | 410 | 4,22–8,73 /kg | high/name |  |
| 17 | 3856015323989 | STOLNI MARGARIN 4x250 g SUPER PONUDA ZVIJEZDA (8) | 1 kg | 10 | 367 | 2,99–4,49 /kg | high/name |  |
| 18 | 8719200265127 | MARGARIN RAMA NAMAZ BUTTERY 400G | 400 g | 8 | 388 | 4,22–7,85 /kg | high/name |  |
| 19 | 3856015325389 | MARGO NATURAL 225g ZVIJEZDA LIGHT | 225 g | 8 | 199 | 3,96–7,07 /kg | high/name |  |
| 20 | 8719200239883 | NAMAZ MARGARINSKI RAMA CLASSIC 225 g | 225 g | 7 | 424 | 4,84–7,96 /kg | high/name |  |

<a id="mlijeko"></a>
## mlijeko (`mlijeko`)

jedinica: **l** · loose_produce: **false** · grupa: **258** · isključenih grupa: **401** · plausible: **0.5–4 €/l** · pakiranje: **500–2000** · zadano bez: **laktoza=bez**

sinonimi: mlijeko, kravlje mlijeko  
must_match: `mlijek`
  
atributi: mast = 0, 0.5, 0.9, 1.5, 2.8, 3.2, 3.5, 3.8; vrsta = trajno, svjeze; laktoza = bez

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850108011845 | N-*MLIJEKO Z BREGOV SVJEŽE 3.2%MM 1L 21 DAN 1184 -6/1-PET | 1 l | 23 | 1322 | 1,27–1,95 /l | high/name | vrsta=svjeze, mast=3.2 |
| 2 | 3850354016830 | N-MLIJEKO DUKAT 1.00L 2.8%MM EDGE -12/1- 11214 | 1 l | 23 | 1320 | 0,78–1,03 /l | high/name | vrsta=trajno, mast=2.8 |
| 3 | 3850108020656 | N-MLIJEKO Z BREGOV 2.00L 2.80%MM -6/1- ČEP VINDIJA 2065 | 2 l | 23 | 1298 | 0,81–1,22 /l | high/name | mast=2.8, vrsta=trajno |
| 4 | 3850108020908 | MLIJEKO ZBREGOV 2.8% MM SA ČEPOM 1L (12), VINDIJA | 1 l | 23 | 1290 | 0,85–1,03 /l | high/name | vrsta=trajno, mast=2.8 |
| 5 | 3838800040578 | MLIJEKO ALPSKO 3,5% 1 L LJUBLJANSKE MLEKARNE(780/PAL) | 1 l | 22 | 918 | 1,39–2,16 /l | high/name | mast=3.5, vrsta=trajno |
| 6 | 3850354006053 | MLIJEKO TRAJNO 2.8% MM 1 L DUKAT BOCA ( 6 ) | 1 l | 21 | 1375 | 0,85–1,19 /l | high/name | vrsta=trajno, mast=2.8 |
| 7 | 3850108011760 | N-*MLIJEKO Z BREGOV SVJEŽE 3.2%MM 1.75L 1176 -6/1-PET | 1,75 l | 21 | 1232 | 1,14–1,77 /l ⚠5 | high/name | vrsta=svjeze, mast=3.2 |
| 8 | 3850354000501 | N-MLIJEKO DUKAT 1.00L 3.2%MM SVJEŽE -12/1- 120 | 1 l | 21 | 1022 | 0,89–1,69 /l | high/name | vrsta=svjeze, mast=3.2 |
| 9 | 3850108020557 | MLIJEKO Z BREGOV 2,8% MM 500 ml SLIM TRAJNO VI | 500 ml | 21 | 956 | 1,70–2,78 /l | high/name | mast=2.8, vrsta=trajno |
| 10 | 3850354006091 | MLIJEKO TRAJNO 3,8%MM 1L HDPE BOCA LACTALIS DUKAT | 1 l | 21 | 890 | 1,31–2,30 /l | high/name | vrsta=trajno, mast=3.8 |
| 11 | 3850108011814 | N-*MLIJEKO Z BREGOV SVJEŽE 3.2%MM 1L 1181 -6/1-PET | 1 l | 20 | 1133 | 1,29–2,02 /l | high/name | vrsta=svjeze, mast=3.2 |
| 12 | 3850354016878 | Dukat trajno mlijeko 2,8% 0,5 l EDGE | 500 ml | 20 | 1047 | 1,36–3,04 /l | high/name | mast=2.8, vrsta=trajno |
| 13 | 3850354016090 | N-*MLIJEKO DUKAT 1.50L 3.2%MMPET-6/1-SVJEŽE MLIJEKO 10140 | 1,5 l | 20 | 837 | 1,19–1,73 /l | high/name | vrsta=svjeze, mast=3.2 |
| 14 | 3850108021592 | MLIJEKO TRAJNO LIGHT 0,9% mm 1L S ČEPOM TE VINDIJA | 1 l | 18 | 935 | 1,33–2,05 /l | high/name | vrsta=trajno, mast=0.9 |
| 15 | 3850354006831 | MLIJEKO DUKAT 0.50L 3.8%MM TRAJNO BOCA -8/1- | 500 ml | 17 | 862 | 1,58–2,98 /l | high/name | mast=3.8, vrsta=trajno |
| 16 | 3850108021295 | N-MLIJEKO Z BREGOV 1.00L VITAMIN D 2,80%MM ČEP UHT | 1 l | 17 | 664 | 0,85–1,17 /l | high/name | mast=2.8, vrsta=trajno |
| 17 | 3850354016854 | N-MLIJEKO DUKAT 1.00L 3,8%MM EDGE -12/1- 11217 | 1 l | 17 | 654 | 1,39–2,25 /l | high/name | vrsta=trajno, mast=3.8 |
| 18 | 3850108020502 | *MLIJEKO ZBREGOV 1 L 2,8% ČEP KLI-KLA (12) VINDIJA | 1 l | 16 | 990 | 0,85–1,16 /l | high/name | mast=2.8, vrsta=trajno |
| 19 | 3850108011067 | N-*MLIJEKO Z BREGOV SVJEŽE 1.5%MM 1L 1106 -6/1-PET | 1 l | 16 | 769 | 1,45–1,85 /l | high/name | vrsta=svjeze, mast=1.5 |
| 20 | 3850108020892 | N-MLIJEKO Z BREGOV 1.00L 1%MM TRAJNO ČEP SLIM -12/1- 2089 | 1 l | 16 | 656 | 1,19–2,05 /l | high/name | vrsta=trajno |

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

jedinica: **kg** · loose_produce: **false** · grupa: **398** · isključenih grupa: **384** · pakiranje: **150–1000** · zadano bez: **laktoza=bez**

sinonimi: jogurt, tekuci jogurt  
must_match: `jogurt`
  
atributi: vrsta = grcki, tekuci, cvrsti; laktoza = bez; mast = 0.1, 0.9, 1.5, 2.8, 3.2

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850354016021 | N-*DUKAT JOGURT 1000G TEKUĆI-6/1- 2.8%MM 32363 | 1 kg | 24 | 1293 | 1,35–3,19 /kg | high/name | mast=2.8, vrsta=tekuci |
| 2 | 3850354010784 | Dukatos grčki tip jogurta 9,7% 450g kant | 450 g | 24 | 1047 | 4,33–7,76 /kg | high/name | vrsta=grcki |
| 3 | 3850108037388 | N-*JOGURT VINDIJA 1000G 2.8%MM 3738 PET -6/1- | 1 kg | 23 | 1286 | 1,75–3,09 /kg | high/name | mast=2.8, vrsta=tekuci |
| 4 | 3850108030174 | N-JOGURT VINDIJA 900G 3.2%MM ČVRSTI KANTICA -6/1-3017 | 900 g | 22 | 1073 | 2,28–3,43 /kg | high/name | mast=3.2, vrsta=cvrsti |
| 5 | 3850108037289 | N-JOGURT VINDIJA180G 3.2MM ČVRSTI PET 3728 -20/1- | 180 g | 21 | 1204 | 2,44–3,67 /kg | high/name | mast=3.2, vrsta=cvrsti |
| 6 | 3850354016007 | N-*DUKAT JOGURT 330G TEKUĆI2.8% MM -8/1- 13356/13714 -12/1- | 330 g | 21 | 660 | 3,00–5,30 /kg | high/name | mast=2.8, vrsta=tekuci |
| 7 | 3850354001133 | JOGURT ČVRSTI 180G 3,2%MM (20) DUKAT | 180 g | 20 | 1188 | 2,44–2,72 /kg | high/name | vrsta=cvrsti, mast=3.2 |
| 8 | 3850108030242 | N-JOGURT VILIKIS 150G NATUR3024 GRČKI TIP JOGURTA -12/1 | 150 g | 20 | 1167 | 5,67–9,00 /kg | high/name | vrsta=grcki |
| 9 | 3850108037371 | N-*JOGURT VINDIJA 500G 2.8%MM 3737 PET -6/1- | 500 g | 20 | 796 | 2,38–4,18 /kg | high/name | mast=2.8, vrsta=tekuci |
| 10 | 3850108030136 | JOGURT Z BREGOV 2,8% MM 180 g VINDIJ | 180 g | 19 | 911 | 1,94–2,94 /kg | high/name | mast=2.8, vrsta=tekuci |
| 11 | 3850108032505 | N-JOGURT VINDIJA 200G 3250 2,8%MM TTOP -12/1- | 200 g | 19 | 794 | 2,30–3,50 /kg | high/name | mast=2.8, vrsta=tekuci |
| 12 | 3850108030020 | N-JOGURT VINDIJA 200G 2.8%MM-20/1- 3002 ČAŠICA | 200 g | 19 | 741 | 2,00–3,20 /kg | high/name | mast=2.8, vrsta=tekuci |
| 13 | 3850354000921 | N-DUKAT JOGURT TEKUĆI 180G2,8%MM -20/1- 358 357 | 180 g | 18 | 1226 | 2,44–2,72 /kg | high/name | mast=2.8, vrsta=tekuci |
| 14 | 3850354019121 | DUKAT B.AKTIV JOGURT 1.5%MM 150G -20/1- | 150 g | 18 | 1098 | 3,27–7,93 /kg | high/name | mast=1.5 |
| 15 | 3850354009924 | N-DUKAT JOGURT ČVRSTI 3,2%MM800G MAXI PAKIRANJE KANTICA | 800 g | 18 | 803 | 1,49–3,36 /kg | high/name | mast=3.2, vrsta=cvrsti |
| 16 | 3850354016014 | N-*DUKAT JOGURT 500G TEKUĆI 2.8%MM -8/1- 32362 BOCA | 500 g | 18 | 666 | 2,38–3,98 /kg | high/name | mast=2.8, vrsta=tekuci |
| 17 | 3850108037395 | JOGURT TEKUĆI LIGHT 0,9% mm 1000 g PET VINDIJA | 1 kg | 17 | 886 | 1,99–3,09 /kg | high/name | mast=0.9, vrsta=tekuci |
| 18 | 3850354009177 | Dukat tekući jogurt MAXI 2,8% mm 230 g | 230 g | 17 | 822 | 2,57–5,17 /kg | high/name | mast=2.8, vrsta=tekuci |
| 19 | 3850108030303 | JOGURT TEKUĆI 0.9%MM LIGHT 200g Z'BREGOV VINDIJA | 200 g | 16 | 641 | 2,25–3,20 /kg | high/name | mast=0.9, vrsta=tekuci |
| 20 | 3856015325358 | MARGARIN MARGO S JOGURTOM 225g ZVIJEZDA | 225 g | 16 | 576 | 4,00–7,96 /kg | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| Dukatos Voćni jogurt SK2 | 21 | `vocn` |
| JOGURT JOGO JAGODA 1KG PET DUKAT (6)* | 19 | `jagod` |
| JOGURT VOĆNI JOGO JAGODA, BRES.Š.V.150 g DUKAT | 18 | `vocn` |
| JOGURT JAGODA DUKATOS 150 g DUKAT | 17 | `jagod` |
| VOCNI JOGURT MARELICA/JAGODA 150 G DUKAT | 17 | `vocn` |
| JOGURT VOĆNI ŠUMSKO VOĆE 1 kg PET DUKAT | 16 | `vocn` |
| N-DUKAT JOGURT DUKATOS 150GBADEM-PISTACIJA GRČKI TIP 13261 | 16 | `pistacij` |
| B.aktiv LGG jogurt acai š.voće 330 g PET | 14 | `voce` |
| SLADOLED KORNET KING JOGURT-ŠUM.VOĆE 167ml LEDO | 14 | `voce` |
| DUKATINO VOĆNI JOGURT MIX 125G,(20) DUKAT | 13 | `vocn` |

</details>

<a id="kiselo_vrhnje"></a>
## kiselo vrhnje (`kiselo_vrhnje`)

jedinica: **kg** · loose_produce: **false** · grupa: **127** · isključenih grupa: **20** · pakiranje: **150–1000**

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
| 13 | 3850354002055 | VRHNJE KISELO 20% 200g DUKAT (20) | 200 g | 18 | 1155 | 4,95–9,45 /kg | high/name | mast=20 |
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
| GRICKALICE CLIPSY MAX SOUR CREAM KISELO VRHNJE 25G | 9 | `grickal` |
| ČIPS OD RIŽE VLASAC I KISELO VRHNJE 60 g B. YOND LIVITY | 6 | `vlasac` |
| ČIPS CRUNCHIPS X-CUT KISELO VRHNJE 130 gr | 4 | `cips` |
| ČIPS MAX KISELO VRHNJE 70 g CLIPSY | 4 | `cips` |
| DVOPEK BRUSCHETTE CHEDDAR I KISELO VRHNJE 140g MARETI | 2 | `bruschett` |
| CHIO CIPS LECA S KIS.VRHNJEM 65 G | 1 | `cips` |
| CIPS POMSTICKS KISELO VRHNJE 85 G LORENZ | 1 | `cips` |
| CIPS PRINGLES HOT KISELO VRHNJE 160 G | 1 | `cips` |
| Chio Čips Oven baked kis.vrhnje&luk 100g | 1 | `luk\b` |
| Doritos Čips Tortilja kiselo vrhnje 90g | 1 | `cips` |

</details>

<a id="vrhnje_za_kuhanje"></a>
## vrhnje za kuhanje (`vrhnje_za_kuhanje`)

jedinica: **l** · loose_produce: **false** · grupa: **80** · isključenih grupa: **0** · pakiranje: **200–1000**

sinonimi: vrhnje za kuhanje, kuhinjsko vrhnje  
must_match: `vrhnje za kuhanje | vrhnje za kuh | vrh za kuh | kuhinjsko vrhnje | vrhnje kuhanje`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850354017158 | VRHNJE ZA KUHANJE BRZO & FINO 500 g EDGE DUKAT | 500 g | 23 | 1244 | 5,58 /l | high/name |  |
| 2 | 3850354008606 | VRHNJE ZA KUHANJE 20%MM 500G BOCA BRZO&FINO DUKAT | 500 g | 20 | 1075 | 7,58–8,18 /l | high/name |  |
| 3 | 3850108033571 | N-VRHNJE ZA KUH VINDIJA 500ML 20% mm-12/1- | 500 ml | 20 | 1052 | 5,30–8,58 /l | high/name |  |
| 4 | 3850354001232 | VRHNJE ZA KUHANJE 20% 200G DUKAT (24) | 200 g | 19 | 1197 | – /kg | high/name |  |
| 5 | 3850108033892 | VRHNJE ZA KUHANJE UHT 0,2L Z'BREGOV VINDIJA | 200 ml | 17 | 1206 | 4,95–8,95 /l | high/name |  |
| 6 | 3850108033472 | VRHNJE ZA KUHANJE BEZ LAKTOZE OSMIJEH 200 ML Z'BREGOV | 200 ml | 16 | 427 | 4,95–9,75 /l | high/name |  |
| 7 | 3850354017257 | BRZO&FINO VRHNJE ZA KUHANJE 1 kg DUKAT (12) 11449 | 1 kg | 15 | 307 | 3,79–6,99 /l | high/name |  |
| 8 | 3850354007975 | VRHNJE ZA KUH 20% BRZO&FINO 3X200G (7) | 600 g | 13 | 648 | – /kg | high/name |  |
| 9 | 3850354017172 | BRZO&FINO VRHNJE ZA KUHANJE LAGANO 500G (12) | 500 g | 13 | 632 | – /kg | high/name |  |
| 10 | 3850354017295 | VRHNJE ZA KUHANJE LAGANO (bez laktoze) B&F 500g DUKAT | 500 g | 13 | 394 | 8,34 /l | high/name |  |
| 11 | 3850108033588 | VRHNJE ZA KUHANJE 20% MM 200 ml SLIM VINDIJA | 200 ml | 12 | 342 | 4,95–10,45 /l | high/name |  |
| 12 | 3870085021835 | VRHNJE ZA KUHANJE 20 % 0,5L MEGGLE (12) | 500 ml | 9 | 599 | 5,56–7,38 /l | high/name |  |
| 13 | 3850108033489 | Z bregov Vrhnje za kuhanje bez laktoze 20% m.m. 0,2 l | 200 ml | 9 | 204 | 3,45–10,60 /l | high/name |  |
| 14 | 5411188120988 | Alpro rižino vrhnje za kuhanje 250 ml | 250 ml | 8 | 415 | 6,84–11,96 /l | high/name |  |
| 15 | 3850354012641 | VRHNJE ZA KUHANJE B&F LAGANI 10% 200 g DUKA | 200 g | 8 | 243 | – /kg | high/name |  |
| 16 | 3850108033526 | Z`bregov Vrhnje za kuhanje 20% 1L UHT | 1 l | 8 | 175 | 3,98–7,59 /l | high/name |  |
| 17 | 3870085021811 | VRHNJE ZA KUH. 20%mmMEGGLE 200 ml | 200 ml | 6 | 384 | 6,45–9,45 /l | high/name |  |
| 18 | 3850257061203 | VRHNJE ZA KUHANJE 20% 0,5 L KRAVICA KRALJICA | 500 ml | 5 | 246 | 5,58–7,98 /l | high/name |  |
| 19 | 3856003914106 | VRHNJE ZA KUHANJE 10% MM 200 ml NTL DUKA | 200 g | 4 | 408 | 5,25–6,05 /l | high/name |  |
| 20 | 3858883523188 | VRHNJE ZA KUH.200 g DUKAT LOT:02012027 | 200 g | 4 | 75 | – /kg | high/name |  |

<a id="slatko_vrhnje"></a>
## slatko vrhnje (`slatko_vrhnje`)

jedinica: **l** · loose_produce: **false** · grupa: **38** · isključenih grupa: **0** · pakiranje: **200–1000**

sinonimi: slatko vrhnje, vrhnje za slag  
must_match: `slatko vrhnje | vrhnje slatko | vrhnje za slag | slag vrhnje | vrhnje za tuc`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850354001348 | VRHNJE ZA ŠLAG 33%MM 500G BRZO&FINO DUKAT | 500 g | 20 | 839 | – /kg | high/name |  |
| 2 | 3850108033663 | N-VRHNJE ZA ŠLAG VINDIJA 3366 500ML 36%MM UHT SLIM -16/1 -12/1- | 500 ml | 17 | 803 | 6,38–11,70 /l | high/name |  |
| 3 | 3850108033694 | N-VRHNJE ZA ŠLAG VINDIJA 200ML UHT -21/1- | 200 ml | 14 | 700 | 10,95–14,45 /l | high/name |  |
| 4 | 3850354001317 | VRHNJE ZA ŠLAG 33%MM 200g BRZO&FINO DUKAT | 200 g | 13 | 533 | – /kg | high/name |  |
| 5 | 3850108033816 | Z bregov vrhnje za šlag 36%mm 0,2L | 200 ml | 8 | 229 | 7,30–17,95 /l | high/name |  |
| 6 | 3850354003236 | VRHNJE ZA ŠLAG NA BILJNOJ BAZI 1L DECORO DUKAT | 1 l | 7 | 33 | 2,52–5,09 /l | high/name |  |
| 7 | 4014500033921 | SLATKO VRHNJE 200 ML ZOTT STANIC | 200 ml | 3 | 182 | 6,65–12,65 /l | high/name |  |
| 8 | 3850108033649 | Vindija Vrhnje za šlag 36% 1 L | 1 l | 3 | 88 | 6,92–8,49 /l | high/name |  |
| 9 | 3858883523171 | VRHNJE ZA ŠLAG 500 g33%MM LOT:16102026 | 500 g | 3 | 68 | – /kg | high/name |  |
| 10 | 3838800050270 | MU ALP.VRHNJE ZA ŠLAG 1L | 1 l | 3 | 9 | 6,49 /l | high/name |  |
| 11 | 4036500001212 | VRHNJE SLATKO 30% 200 g OMIRA | 200 g | 2 | 49 | – /kg | high/name |  |
| 12 | 8003180908311 | ZAMJENA ZA VRHNJE ZA ŠLAG 500mL | 500 ml | 2 | 36 | 3,80–3,98 /l | high/name |  |
| 13 | 3850354017233 | VRHNJE ZA ŠLAG VANILIJA 500g DUKAT | 500 g | 2 | 3 | – /kg | high/ean |  |
| 14 | lidl:0026724 | Trajno vrhnje za šlag s 30% m.m. | 200 g | 1 | 116 | – /kg | high/unit |  |
| 15 | 4056489317999 | Vrhnje za šlag | 1 kg | 1 | 116 | – /kg | high/unit |  |
| 16 | 40894355 | Vrhnje za šlag 36% | 500 g | 1 | 116 | – /kg | high/unit |  |
| 17 | lidl:0052366 | Vrhnje za šlag bez laktoze | 200 g | 1 | 116 | – /kg | high/unit |  |
| 18 | 9100000091952 | SLATKO VRHNJE S-BUDGET 0,5 L | 500 ml | 1 | 67 | 6,78 /l | high/name |  |
| 19 | 8017596123169 | VRHNJE ZA ŠLAG 200ml | 200 ml | 1 | 43 | 6,75 /l | high/name |  |
| 20 | 9006207003241 | SVJEŽE VRHNJE ZA ŠLAG 36% m.m.250ml | 250 ml | 1 | 43 | 6,76 /l | high/name |  |

<a id="svjezi_sir"></a>
## svježi sir (`svjezi_sir`)

jedinica: **kg** · loose_produce: **false** · grupa: **155** · isključenih grupa: **66** · pakiranje: **150–1000**

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
| 8 | 3850108058390 | SIR SVJEŽI POSNI PROTEIN 250 gr Z BREGOV VINDI | 250 g | 14 | 411 | 4,76–7,96 /kg | high/name | mast=posni |
| 9 | 4002174080945 | KERNIGER- ZRNATI SVJEŽI SIR 200 g BAYERNLAND | 200 g | 11 | 458 | 6,45–16,45 /kg | high/name |  |
| 10 | 3850108058321 | SIR SVJEŽI POSNI BBL 500g ZBREGOV VINDIJA | 500 g | 11 | 347 | 4,78–7,10 /kg | high/name | mast=posni |
| 11 | 3858888590215 | Zdenka svježi sir 500gr. Posni pl-posuda | 500 g | 7 | 222 | 3,38–7,18 /kg | high/name | mast=posni |
| 12 | 8585002519511 | Meggle Sir svježi zrnati Prot.20%m.m380g | 380 g | 6 | 591 | 6,03–10,24 /kg | high/name |  |
| 13 | 3850108058345 | SIR SVJEŽI POLUMASNI 250 g Z BREGOV VINDIJA | 250 g | 6 | 167 | 2,12–7,80 /kg | high/name |  |
| 14 | 5900531001512 | SIR SVJEŽI ZRNATI 20 % mm 200 g DAIRLY | 200 g | 5 | 585 | 4,95–8,25 /kg | high/name |  |
| 15 | 3858888598679 | SIR SVJEŽI 500 g SPORT ZDENKA | 500 g | 5 | 341 | 3,98–6,58 /kg | high/name |  |
| 16 | 3858888590222 | Zdenka svježi sir 500gr. Masni pl-posuda | 500 g | 5 | 265 | 3,98–5,30 /kg | high/name | mast=masni |
| 17 | 3858883522129 | PRESIDENT SVJEŽI SIR POSNI LIGHT 500 g DUKAT | 500 g | 5 | 78 | 4,98–6,38 /kg | high/name | mast=posni |
| 18 | 3859892380090 | N-SIR SVJEŽI POLUMASNI 25%MM500G - 5868 6/1 DOM.KRAV. | 500 g | 5 | 73 | 3,98–4,98 /kg | high/name |  |
| 19 | 3856003930021 | SIR SVJEŽI POLUMASNI 500g 15% MM TO JE TO VINDIJA | 500 g | 4 | 486 | 3,58–4,98 /kg | high/name |  |
| 20 | 3870085020227 | SVJEZI SIR POSNI 450 G MEGGLE | 450 g | 4 | 302 | 5,44–6,20 /kg | high/name | mast=posni |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| N-DUKAT DUKATINO SVJEŽI SIR SVOĆEM 6*50G -6/1- | 16 | `dukatino` |
| ČIPS ČIPI ČIPS 130G SVJEŽI SIR I MLADI LUK -20/1- CHIO | 15 | `luk\b` |
| PRESIDENT SVJEŽI SIR I VRHNJE 200 g DUKAT | 13 | `vrhnje` |
| SIR SVJEZI ZRNATI VLASAC 200 G PRESIDENT DUKAT | 11 | `vlasac` |
| PRESIDENT KREM SVJEŽI SIR 500 gr DUKAT | 10 | `krem\b` |
| PRESIDENT SVJEŽI SIR I VRHNJE 450 g DUKAT | 10 | `vrhnje` |
| SIR SVJEŽI KREM VIVIS 200 g VINDIJA | 6 | `krem\b` |
| SVJEZI SIR S VRHNJEM 450 G MEGGLE | 6 | `vrhnje` |
| DOMAĆE KISELO VRHNJE ZA SVJEŽI SIR 25%MM 300G, VINDIJA | 5 | `vrhnje` |
| N-ŠTRUKLI SA SVJ.SIR. SLATKI VINDIJA 600G -12/1- SMRZNUTO | 5 | `strukli` |

</details>

<a id="tvrdi_sir"></a>
## tvrdi sir (gauda, trapist, edamac) (`tvrdi_sir`)

jedinica: **kg** · loose_produce: **false** · grupa: **992** · isključenih grupa: **14** · pakiranje: **100–1000**

sinonimi: tvrdi sir, gauda, gouda, trapist, edamac, edamer, polutvrdi sir  
must_match: `gauda | gouda | trapist | edamac | edamer | tvrdi sir | sir tvrdi | polutvrdi | polutv\b | tilzit`
  
atributi: vrsta = gauda, trapist, edamac, tilzit; oblik = ribani, narezani

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850355007080 | N-SIR PRESIDENT GOUDA 150G SLICE-10/1- | 150 g | 20 | 875 | 17,27–26,80 /kg | high/name | vrsta=gauda, oblik=narezani |
| 2 | 3850355007325 | N-SIR PRESIDENT GOUDA 400G -8/1- 15022 15042 - | 400 g | 20 | 789 | 9,73–17,98 /kg | high/name | vrsta=gauda |
| 3 | 3850108053913 | Vindija Tilzit sir rezani 45% mm 150 g | 150 g | 19 | 858 | 17,27–24,60 /kg | high/name | vrsta=tilzit, oblik=narezani |
| 4 | 3850355007301 | SIR PRESIDENT GOUDA 250G -12/1 15021/15041 | 250 g | 19 | 833 | 11,16–18,36 /kg | high/name | vrsta=gauda |
| 5 | 3850108058215 | Vindija Gouda sir rezani 45% mm 150 g | 150 g | 17 | 965 | 16,60–24,60 /kg | high/name | vrsta=gauda, oblik=narezani |
| 6 | 3850108057997 | Vindija Sir Tilzit polutvrdi45%mm 200g | 200 g | 17 | 614 | 14,95–22,50 /kg | high/name | vrsta=tilzit |
| 7 | 3850355007141 | PRESIDENT TILZIT SLICE 150 g (10) DUKAT | 150 g | 17 | 608 | 17,27–26,80 /kg | high/name | vrsta=tilzit, oblik=narezani |
| 8 | 3850108057980 | Vindija Sir Gauda polutvrdi45%mm200g | 200 g | 16 | 555 | 14,95–22,50 /kg | high/name | vrsta=gauda |
| 9 | 3850355007103 | SIR SIRELA PRESIDENT SANDWICH GOUDA 120 g DUKA | 120 g | 16 | 542 | 18,25–29,08 /kg | high/name | vrsta=gauda, oblik=narezani |
| 10 | 3850108055696 | N-SIR VINDIJA GOUDA RIBANI 200G -10/1- | 200 g | 15 | 546 | 14,95–26,25 /kg | high/name | oblik=ribani, vrsta=gauda |
| 11 | 3850355007387 | SIR TILZIT 400 G PRESIDENT DUKAT | 400 g | 13 | 539 | 9,73–16,88 /kg | high/name | vrsta=tilzit |
| 12 | 3858888597955 | SIR SPORT TRAPIST 45%MM 400 g 1/5 KOLUTA EGALIZIRANI ZDENKA | 400 g | 13 | 469 | 12,38–25,98 /kg | high/name | vrsta=trapist |
| 13 | 3858888590475 | SIR EDAMAC 400g ZDENKA EGALIZIRANO | 400 g | 12 | 502 | 12,48–17,73 /kg | high/name | vrsta=edamac |
| 14 | 3850355007165 | SIR PRESIDENT TRAPIST 500G GRAND OVAL SIRELA VP. -6/1 | 500 g | 12 | 411 | 11,58–18,78 /kg | high/name | vrsta=trapist |
| 15 | 3859892884390 | SIR TVRDI TRAPIST 200G PAŠKA SIRANA | 200 g | 11 | 571 | 22,45–34,65 /kg | high/name | vrsta=trapist |
| 16 | 3850108057362 | Vindija Sir Trapist varaždin.45%mm 280g | 280 g | 11 | 303 | 14,25–20,32 /kg | high/name | vrsta=trapist |
| 17 | 3858888597740 | SIR ZDENKA EDAMAC 150 g EGALIZIRANI- REZANI ZDEN | 150 g | 10 | 367 | 11,47–25,93 /kg | high/name | vrsta=edamac |
| 18 | 3858888590505 | SIR POLUTV GOUDA 400g ZDENKA | 400 g | 10 | 363 | 12,48–17,63 /kg | high/name | vrsta=gauda |
| 19 | 4770299047890 | Džiugas Sir tvrdi 12mj. 40% mm 180 g | 180 g | 9 | 442 | 14,94–22,50 /kg | high/name |  |
| 20 | 3850355002719 | SIR POLUTV GOUDA CCA 3kg DUKAT |  | 8 | 440 | 4,49–6,49 /kg | low/unit_price | vrsta=gauda |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| SIR TOPLJENI GOUDA 150 G PRESI | 22 | `topljen` |
| SIR TVRDI SNACK MR BOKUNIĆ 100g | 2 | `snack` |
| SNACK GOUDA CUBES MIX DELICAC 100 g | 2 | `snack` |
| SNACK GOUDA CUBES SALAM 100 g DELI Q | 2 | `snack` |
| SNACK GOUDA/CHEDDAR 100 G DELI Q | 2 | `snack` |
| Deli Q Snack Sir gouda&cheddar red 60g | 1 | `snack` |
| Deli Q Snack Sir gouda&pesto gr.red60g | 1 | `snack` |
| KLC.Topljeni sirni listići edamer 200g | 1 | `topljen` |
| KLC.Topljeni sirni listići gouda 200g | 1 | `topljen` |
| NAMAZ SIR.GOUDA RUPP 175 g | 1 | `namaz` |

</details>

<a id="mozzarella"></a>
## mozzarella (`mozzarella`)

jedinica: **kg** · loose_produce: **false** · grupa: **213** · isključenih grupa: **47** · pakiranje: **100–1000**

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
| 9 | 3858888599478 | SIR REZANI MOZZARELLA 150 G ZDENKA | 150 g | 5 | 213 | 13,93–21,93 /kg | high/name |  |
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
| 20 | 8001665724814 | RAVIOLI RAJCICA/MOZZARELLA 250 G RANA | 250 g | 2 | 187 | 11,16 /kg | high/name |  |

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

jedinica: **kg** · loose_produce: **false** · grupa: **113** · isključenih grupa: **12** · pakiranje: **50–1000**

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
| 6 | 5292874000032 | RIBAN.PARMEZAN GREEN VIE 100 g | 100 g | 4 | 245 | 13,80–17,90 /kg | high/name | oblik=ribani |
| 7 | 8002710410027 | SIR RIBANI GRANA PADANO 50G ZANETTI | 50 g | 4 | 161 | 21,00–33,80 /kg | high/name | oblik=ribani |
| 8 | 8011661000737 | SIR GRANA PADANO PARMA 200 g | 200 g | 3 | 173 | 24,95–34,45 /kg | high/name |  |
| 9 | 8002710402008 | SIR TVRDI 200G PARMIGIANO REGGIANO ZANETTI | 200 g | 3 | 146 | 26,15–44,95 /kg | high/name |  |
| 10 | 8000430395587 | GRANA PADANO 100 G GALBANI DUKAT | 100 g | 3 | 49 | 25,20–34,90 /kg | high/name |  |
| 11 | 8004673600125 | SIR GRANA PADANO 200 G LATTERIA SORESINA S.C.A. | 200 g | 2 | 170 | 21,45–25,95 /kg | high/name |  |
| 12 | 8002710420132 | SIR PARMEZAN GRANELLO 80G RIBANI | 80 g | 2 | 157 | 11,13–17,37 /kg | high/name | oblik=ribani |
| 13 | 8003518100622 | GRANA PADANO GIRA i GRATTA 150g | 150 g | 2 | 40 | 42,07–43,27 /kg | high/name |  |
| 14 | 18000430396376 | SIR GALBANI 60 g GRANA PADANO | 60 g | 2 | 13 | 26,50–36,67 /kg | high/name |  |
| 15 | 8002503211138 | SIR GRANA PADANO 200g LOT:006238 | 200 g | 2 | 5 | 25,00–29,95 /kg | high/name |  |
| 16 | 3850334350756 | SIR TVRDI GRANA PADANO K PLUS 200g | 200 g | 1 | 188 | 19,95–30,95 /kg | high/name |  |
| 17 | 3856025828696 | GRANA PADANO 200 G 40 MJ. SELECTION | 200 g | 1 | 155 | 22,45 /kg | high/name |  |
| 18 | 3856025828672 | GRANA PADANO RIBANI 100 G SELECTION | 100 g | 1 | 155 | 23,90 /kg | high/name | oblik=ribani |
| 19 | 8002710410041 | SIR RIBANI GRANA PADANO 100 G ZANETTI | 100 g | 1 | 155 | 25,90 /kg | high/name | oblik=ribani |
| 20 | 3856025841503 | PARMIGIANO REGGIANO DOP 30 M 180 G SELECTION | 180 g | 1 | 154 | 36,06 /kg | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| N-UMAK MUTTI 400G SA PARMEZANOM -6/1- STAKLENKA | 6 | `umak` |
| INZERSDORFER UMAK BOLOGNESE GOVEDINA PARMEZAN 400g | 3 | `umak` |
| GRANA PADANO SNACK 5x20 g AGRIFORM | 2 | `snack` |
| RIŽOT S PARMEZANOM I CARNAROLI RIŽOM 210 g NIKA | 2 | `rizot` |
| CRVENI UMAK S PARMEZANOM 400G MUTTI | 1 | `umak` |
| KREKERI RIŽINI BUDDY PARMEZAN I ZAČINI 60G | 1 | `kreker` |
| Krem. umak od parmezana i tartufa | 1 | `umak` |
| PROTEIN ČIPS PARMEZAN 60 g RICE UP | 1 | `cips` |
| RIBEZ ZA PARMEZAN URBAN SHADES | 1 | `ribez` |
| SALAMA S PARMEZANOM 75 g | 1 | `salama` |

</details>

<a id="jaja"></a>
## jaja (`jaja`)

jedinica: **kom** · loose_produce: **false** · grupa: **348** · isključenih grupa: **885** · plausible: **0.1–1.5 €/kom** · pakiranje: **4–30** · grupira po: **velicina**

sinonimi: jaja, jaje, kokosja jaja  
must_match: `jaja\b | jaje\b`
  
atributi: velicina = xl, l, m, s; uzgoj = slobodni, podni, bio

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | jaja:m | N-JAJA LUKAČ A KLASA 10KOM RAZRED M KAVEZNI UZGOJ -18/1 | 10 kom | 24 | 1335 | 0,14–1,30 /kom ⚠27 | high/name | velicina=m, uzgoj=podni |
| 2 | jaja:l | N-JAJA LUKAČ A KLASA 10KOM RAZRED L KAVEZNI UZGOJ - 18/1 | 10 kom | 21 | 1171 | 0,10–0,47 /kom ⚠27 | high/name | velicina=l, uzgoj=podni |
| 3 | jaja:xl | JAJA XL RAZRED 10/1 PODNI UZGOJ VRANA |  | 6 | 207 | 0,30–0,51 /kom | high/name | velicina=xl, uzgoj=podni |
| 4 | 3858895340025 | Gala Jaja svj.Aklas.Mraz.podni uzgoj10/1 | 10 kom | 3 | 177 | 0,19–0,30 /kom | high/name | uzgoj=podni |
| 5 | jaja:s | Žito Jaja iz podnog uzgoja razred S | 10 kom | 3 | 128 | 0,11–0,26 /kom | high/name | velicina=s, uzgoj=podni |
| 6 | 8714786243552 | LICEN.JAJE MIX 10 g AJAX DISTRIBUCIJA | 10 g | 3 | 88 | – | – |  |
| 7 | 3857500131508 | SVJEŽA JAJA RAZL. VEL. BIO 6/1 |  | 2 | 110 | 0,47–0,53 /kom | high/name | uzgoj=bio |
| 8 | 3858894520121 | KOŠARICA PLETENA - JAJA U BOJI |  | 2 | 88 | – | – |  |
| 9 | 3858894522439 | JAJA U TUBI - CRNA I ZLATNA 6KOM | 6 kom | 2 | 85 | – ⚠85 | – |  |
| 10 | 3858895340018 | JAJA SVJEŽA A KL.RAZ.L MP PODNI UZGOJ 10/1 |  | 2 | 67 | 0,30–0,33 /kom | high/name | uzgoj=podni |
| 11 | 5200701008243 | JAJE FUNKY PAW PATROL LIZALICA 10G -12/1- | 10 g | 2 | 29 | – | – |  |
| 12 | 8697422659873 | JAJE JR.EGG + BOMBONI 10g | 10 g | 2 | 10 | – | – |  |
| 13 | 3858894522422 | JAJA U TUBI LJUBIČASTA- 6 KOM | 6 kom | 2 | 7 | – ⚠7 | – |  |
| 14 | 8681812047364 | JAJE SURPRISE EGG 4g LAIRMAK | 4 g | 2 | 5 | – | – |  |
| 15 | 8697422654533 | JAJE PUPPY+ BOMBON 10g | 10 g | 2 | 4 | – | – |  |
| 16 | 5907707051661 | BOJE ZA JAJA 5/1 |  | 2 | 3 | 0,28 /kom | high/name |  |
| 17 | 8699462605148 | JAJE PRINCESS SUPRISE 15g | 15 g | 2 | 3 | – | – |  |
| 18 | 8697422658043 | JAJE TOY JOY + BOMBON 10g | 10 g | 2 | 3 | – | – |  |
| 19 | 8695504151109 | CHOCO JAJE TOTO 20g | 20 g | 2 | 2 | – | – |  |
| 20 | 3859892521035 | Jaja iz kaveznog uzgoja, razred "S" | 10 kom | 1 | 116 | 0,10 /kom | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| JAJE ČOKOLADNO KINDER SURPRISE 20G T1x192 | 15 | `coko` |
| N-ČOK.JAJE MICKEY MOUSE 20GRATTOUILLE -48/1- | 14 | `cok\b` |
| ČOKOLADNO JAJE HOT WHEELS 20g ZAINI | 12 | `coko` |
| N-ČOK.JAJE PRINCES -SHIMMERiSHINE20G -48/1- | 11 | `cok\b` |
| N-FERRERO KINDER JOY 20G JAJE IZNENAĐENJA -72/2/1- -24/1- | 8 | `ferrero` |
| N-FERRERO KINDER ČOK JAJE 20G LEI -72/1- | 8 | `ferrero` |
| ČOKOLADNA JAJA PUNJ. ML. ČOK. GIANDUA 120 g DUPIN | 8 | `coko` |
| ČOKOLADNA JAJA PUNJENA ASSORTED 120 g DUPIN | 8 | `coko` |
| COKOLADNA JAJA USKRSNJA MINI 100 G MILKA | 7 | `coko` |
| JAJA KL. A RAZ. M 10/1 IZ ŠTALSKOG (PODNOG) UZGOJA LUNETA | 7 | `luneta` |

</details>

<a id="luk"></a>
## luk (crveni/žuti) (`luk`)

jedinica: **kg** · loose_produce: **true** · grupa: **207** · isključenih grupa: **36** · zadano bez: **vrsta=mladi, vrsta=ljutika**

sinonimi: luk, crveni luk, zuti luk, kapula  
must_match: `luk\b | kapula`
  
atributi: vrsta = mladi, ljutika, crveni, zuti, bijeli

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3859889644716 | LUK LJUBIČASTI RUKAVAC 4/1 |  | 4 | 519 | 2,58–3,78 /kg | low/assumed | vrsta=crveni |
| 2 | 3859889644709 | LUK CRVENI RUKAVAC 4/1 |  | 4 | 339 | 1,98–2,90 /kg | low/assumed | vrsta=crveni |
| 3 | 3859891348275 | LUK CRVENI PAK. 1 kg | 1 kg | 2 | 463 | 0,99–1,45 /kg | high/name | vrsta=crveni |
| 4 | 3858890133004 | LUK CRVENI 1KG EKOZONA | 1 kg | 2 | 206 | 1,49–2,19 /kg | high/name | vrsta=crveni |
| 5 | 3850334173034 | LUK LJUBIČASTI (10) |  | 2 | 192 | 1,01–1,29 /kg | low/unit_price | vrsta=crveni |
| 6 | 3850334386205 | LUK SREBRENAC (10) |  | 2 | 118 | 1,83–1,99 /kg | low/unit_price | vrsta=zuti |
| 7 | 3859891254354 | LUK CRVENI 2kg | 2 kg | 2 | 82 | 0,80–1,00 /kg | high/name | vrsta=crveni |
| 8 | 3859889644051 | LUK CRVENI PAK 1 kg | 1 kg | 2 | 58 | 0,89–0,99 /kg | high/name | vrsta=crveni |
| 9 | 3859891815135 | LUK LJUBIČASTI RUKAVAC 4/1 |  | 2 | 58 | 1,98 /kg | low/assumed | vrsta=crveni |
| 10 | 3856017200318 | LUK ŽUTI RUKAVAC 4/1 |  | 2 | 45 | 1,98 /kg | low/assumed | vrsta=zuti |
| 11 | 3857500102126 | LUK ŽUTI PAKIRANI 1KG | 1 kg | 2 | 4 | 1,25–1,29 /kg | high/name | vrsta=zuti |
| 12 | 3859894214188 | *LUK SREBRENAC 4/1 |  | 2 | 4 | – | – | vrsta=zuti |
| 13 | 3859894214232 | LUK RUKAVAC MIX 5/1 |  | 2 | 3 | 3,38 /kg | low/assumed |  |
| 14 | 3859894214133 | LUK CHARLOTTE 500G | 500 g | 2 | 2 | 4,98 /kg ⚠1 | high/name |  |
| 15 | ntl:248675 | LUK CRVENI |  | 1 | 343 | 0,49–0,59 /kg | low/unit_price | vrsta=crveni |
| 16 | ntl:248676 | LUK LJUBIČASTI |  | 1 | 343 | 1,09–1,19 /kg | low/unit_price | vrsta=crveni |
| 17 | ntl:246142 | LUK SREBRENAC |  | 1 | 343 | 2,49 /kg | low/unit_price | vrsta=zuti |
| 18 | ntl:022066 | LUK LJUBIČASTI RUKAVAC 4/1SNIŽENJE |  | 1 | 258 | 1,40 /kg | low/assumed | vrsta=crveni |
| 19 | 3850334386182 | LUK CRVENI |  | 1 | 188 | 0,79 /kg | low/unit_price | vrsta=crveni |
| 20 | 3850334049667 | LUK ŽUTI 1 kg | 1 kg | 1 | 181 | 1,09–1,29 /kg | high/name | vrsta=zuti |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| LUK REZANI 3000G TERMIČKI OBRAĐEN -5/1- VREĆA | 6 | `termick` |
| LUK KOCKICE SMRZNUTI 2,5KG LEDO | 4 | `smrz` |
| ZAČIN LUK PRŽENI 1000 g KOTANY | 4 | `przeni` |
| IGRAČKA LUK I STRIJELA AY32-1A NIRD | 3 | `igrack` |
| LUK DINSTANI 3 kg C.A.K. | 3 | `dinst` |
| CITRES LUK SREDNJI U OCTU 1550 g | 2 | `octu` |
| LUK DINSTANI 2,6KG PODRAVKA | 2 | `dinst` |
| LUK KOCKICE 2.5KG LEDO | 2 | `ledo\b` |
| LUK U GRANULAMA ST. | 2 | `granul` |
| SREBNI LUK U NALJEVU 560g | 2 | `naljev` |

</details>

<a id="cesnjak"></a>
## češnjak (`cesnjak`)

jedinica: **kg** · loose_produce: **true** · grupa: **57** · isključenih grupa: **20**

sinonimi: cesnjak, bijeli luk  
must_match: `cesnjak | cesnjaka`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3830054730205 | ČEŠNJAK SJECKANI U ULJU 1KG MODIMA | 1 kg | 3 | 38 | 5,18–6,69 /kg | high/name |  |
| 2 | 3850334173287 | ČEŠNJAK RFZ (10) |  | 2 | 148 | 3,99–4,34 /kg | low/unit_price |  |
| 3 | 5411361032336 | ČEŠNJAK DS 1kg ARDO | 1 kg | 2 | 3 | 5,49–6,29 /kg | high/ean |  |
| 4 | ntl:024796 | ČEŠNJAK RFS |  | 1 | 342 | 4,99 /kg | low/unit_price |  |
| 5 | plodine:110801 | CESNJAK RINFUZO |  | 1 | 149 | 3,49 /kg | low/unit_price |  |
| 6 | 3858893252634 | Češnjak VH rfs |  | 1 | 144 | 5,49 /kg | low/unit_price |  |
| 7 | gavranovic:071145 | ČEŠNJAK |  | 1 | 124 | 4,59–6,29 /kg | low/unit_price |  |
| 8 | gavranovic:089992 | ČEŠNJAK 250g | 250 g | 1 | 124 | 6,20–7,56 /kg | high/name |  |
| 9 | lidl:0082712 | Češnjak | 250 g | 1 | 116 | 5,56 /kg | high/unit |  |
| 10 | lidl:0084614 | Bio češnjak 150g | 150 g | 1 | 116 | 9,93 /kg | high/name |  |
| 11 | lidl:0082711 | Češnjak domaći 200g | 200 g | 1 | 116 | 9,95 /kg | high/name |  |
| 12 | 3858890139280 | BIO CESNJAK EKOZONA |  | 1 | 116 | – | – |  |
| 13 | 6917986800682 | CESNJAK 500 G | 500 g | 1 | 106 | 4,68–5,30 /kg | high/name |  |
| 14 | tommy:10030072 | ČEŠNJAK MLADI |  | 1 | 73 | 5,49–5,99 /kg | low/unit_price |  |
| 15 | ribola:0112349 | ČEŠNJAK |  | 1 | 61 | 3,99–6,05 /kg | low/unit_price |  |
| 16 | 3859889884129 | Češnjak mrežica 500g | 500 g | 1 | 53 | 7,98 /kg | high/name |  |
| 17 | eurospin:080159501 | ČEŠNJAK RFZ |  | 1 | 43 | 4,49 /kg | low/unit_price |  |
| 18 | ktc:00117 | ČEŠNJAK |  | 1 | 30 | 4,29 /kg | low/unit_price |  |
| 19 | studenac:082830 | ČEŠNJAK kg |  | 1 | 20 | 3,69–4,06 /kg | low/unit_price |  |
| 20 | stridon:106166 | ČEŠNJAK AGROVIR |  | 1 | 14 | 3,65–5,59 /kg | low/unit_price |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| MIRODIJE ČEŠNJAK U GRANULAMA 500g ŠAFRAM | 7 | `granul` |
| ZAČIN ČEŠNJAK U GRANULAMA 920 g KOTANY | 6 | `granul` |
| ČEŠNJAK U GRANULAMA 1kg ALU KOTANYI (10) | 5 | `granul` |
| ZAČIN ČEŠNJAK GRAN.1 kg NADAL | 3 | `zacin` |
| ČEŠNJAK GRANULE 830G NADALINA (10) | 3 | `granul` |
| MIRODIJE ČEŠNJAK U GRANULAMA 750G PODRAVKA | 2 | `granul` |
| SJEME CESNJAK BIJELI 500G | 2 | `sjeme\b` |
| SJEME CESNJAK CRVENI 500G | 2 | `sjeme\b` |
| ČEŠNJAK U GRANULAMA 1000 g HOD | 2 | `granul` |
| PASTA ČEŠNJAK 680g STAKLO | 1 | `pasta` |

</details>

<a id="krumpir"></a>
## krumpir (`krumpir`)

jedinica: **kg** · loose_produce: **true** · grupa: **238** · isključenih grupa: **198**

sinonimi: krumpir, krompir, kumpir  
must_match: `krumpir`
  
atributi: namjena = kuhanje, pecenje, salata; vrsta = mladi, crveni, zuti, bijeli

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3859893072024 | KRUMPIR LIČKI 2,5 kg AGROVEL. | 2,5 kg | 8 | 377 | 1,20–1,76 /kg | high/name |  |
| 2 | 3859893051111 | KRUMPIR PAK. ZA KUHANJE 2,5 kg | 2,5 kg | 4 | 243 | 0,80–1,40 /kg | high/name | namjena=kuhanje |
| 3 | 8028772001904 | KRUMPIR GIRO 4 KG OPRAN | 4 kg | 3 | 275 | 1,25–1,65 /kg | high/name |  |
| 4 | 3859893051098 | KRUMPIR PAK. ZA PEČENJE 2,5 kg | 2,5 kg | 3 | 253 | 1,00–1,40 /kg | high/name | namjena=pecenje |
| 5 | 3859893051104 | KRUMPIR PAK. ZA SALATU 2,5 kg | 2,5 kg | 2 | 231 | 1,08–1,40 /kg | high/name | namjena=salata |
| 6 | 8028772002000 | KRUMPIR 2 KG GIRO OPRANI | 2 kg | 2 | 211 | 1,35–1,80 /kg | high/name |  |
| 7 | 3858890133011 | BIO KRUMPIR 1 KG EKOZONA | 1 kg | 2 | 169 | 1,39–2,19 /kg | high/name |  |
| 8 | 3859892278021 | KRUMPIR BIJELI 5 kg NTL | 5 kg | 2 | 130 | 0,62–0,80 /kg | high/ean | vrsta=bijeli |
| 9 | 3859891254200 | KRUMPIR 3kg ZA PEČENJE | 3 kg | 2 | 82 | 0,59–1,00 /kg | high/name | namjena=pecenje |
| 10 | 3859891254194 | Krumpir za kuhanje 3kg | 3 kg | 2 | 73 | 0,90–1,00 /kg | high/name | namjena=kuhanje |
| 11 | 3859891254422 | Krumpir oprani - vrećica 5 kg | 5 kg | 2 | 69 | 0,80–0,90 /kg | high/name |  |
| 12 | 3858885876053 | KRUMPIR MLADI RFZ |  | 2 | 10 | 0,72–3,45 /kg | low/unit_price | vrsta=mladi |
| 13 | 3859893072031 | LIČKI KRUMPIR 5/1 | 10 kg | 2 | 7 | 0,48–0,99 /kg | high/name |  |
| 14 | ntl:248145 | KRUMPIR |  | 1 | 343 | 0,59–0,89 /kg | low/unit_price |  |
| 15 | ntl:020788 | KRUMPIR CRVENI |  | 1 | 343 | 0,59–0,89 /kg | low/unit_price | vrsta=crveni |
| 16 | 3859891568161 | KRUMPIR 2,5 kg ZORELA | 2,5 kg | 1 | 343 | 0,76–1,08 /kg | high/name |  |
| 17 | 3850334386120 | KRUMPIR 5 kg | 5 kg | 1 | 188 | 0,70 /kg | high/name |  |
| 18 | 3856017203005 | KRUMPIR KLIPER 1.5 kg | 1,5 kg | 1 | 188 | 0,99–1,19 /kg | high/name |  |
| 19 | 3850334449702 | KRUMPIR ZA PEČENJE I PRŽENJE 2.5 kg | 2,5 kg | 1 | 188 | 1,08–1,28 /kg | high/name | namjena=pecenje |
| 20 | 3850334151476 | KRUMPIR ZA KUHANJE 2.5 kg | 2,5 kg | 1 | 180 | 1,08–1,28 /kg | high/name | namjena=kuhanje |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| PEKARSKI KRUMPIR, KRIŠKE S KOROM 2,5 KG LEDO | 9 | `pekarsk` |
| KRUMPIR PEKARSKI ZAČINJENI 750g LEDO | 8 | `pekarsk` |
| KROKETI KRUMPIROVI 2,5kg LEDO | 4 | `ledo` |
| KRUMPIR KRIŠKE JACKET WEDGES 2500 g ( ZAPRIMATI NA KG ) | 4 | `kriske` |
| KRUMPIR PIRE 3KG VR PODRAVKA (1) | 4 | `pire` |
| KRUMPIR BATAT 1000 g | 3 | `batat` |
| KRUMPIR PLOŠKE WEDGES 2,5 kg MCCAIN | 3 | `ploske` |
| LEDO KRUMPIR POMMES FRITES 1KG (10) | 3 | `ledo` |
| PIRE KRUMPIR GRANULE 4x1 kg PODRAVKA | 3 | `pire` |
| KRUMPIR BATAT (7) | 2 | `batat` |

</details>

<a id="rajcica"></a>
## rajčica (svježa) (`rajcica`)

jedinica: **kg** · loose_produce: **true** · grupa: **201** · isključenih grupa: **201**

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
| 6 | 8437007225402 | RAJČICA CRNA 500 g | 500 g | 2 | 25 | 4,98–6,14 /kg | high/name |  |
| 7 | 3859890369066 | RAJČICA COCTAIL 500g NTL | 500 g | 2 | 6 | 4,06–10,38 /kg | high/name |  |
| 8 | ntl:245794 | RAJČICA |  | 1 | 343 | 2,69–2,99 /kg | low/unit_price |  |
| 9 | ntl:248683 | RAJČICA GRAPOLO |  | 1 | 343 | 2,69–2,99 /kg | low/unit_price | vrsta=grozd |
| 10 | 3613070000428 | RAJČICA CHERRY 500 g | 500 g | 1 | 343 | 7,98 /kg | high/name | vrsta=cherry |
| 11 | 3850334401465 | RAJČICA BEEF |  | 1 | 154 | 2,89–3,49 /kg | low/unit_price |  |
| 12 | 3830070890020 | BIO RAJCICA 500G | 500 g | 1 | 147 | 3,46–3,98 /kg | high/name |  |
| 13 | 3858885877289 | Rajčica rfs |  | 1 | 144 | 1,99 /kg | low/unit_price |  |
| 14 | 3858893251705 | Rajčica grapolo rfs |  | 1 | 144 | 2,49–2,59 /kg | low/unit_price | vrsta=grozd |
| 15 | 3856021219177 | RAJČICA KOKTEL S BUDGET 500 g | 500 g | 1 | 144 | 4,98–5,78 /kg | high/name | vrsta=cherry |
| 16 | 3856021206702 | RAJČICA KOKTEL VH 500 g | 500 g | 1 | 144 | 5,98 /kg | high/name | vrsta=cherry |
| 17 | 3856021216169 | RAJČICA CHERRY VH 500 g | 500 g | 1 | 144 | 7,58 /kg | high/name | vrsta=cherry |
| 18 | 8436591072157 | BIO RAJCICA GRAPPOLO 500G | 500 g | 1 | 142 | 3,98–6,16 /kg | high/name |  |
| 19 | 8715817000090 | RAJCICA KOKTEL 500G | 500 g | 1 | 142 | 4,38–6,50 /kg | high/name | vrsta=cherry |
| 20 | 8057960790283 | RAJCICA GRAPOLO |  | 1 | 139 | 2,49 /kg | low/unit_price | vrsta=grozd |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| KONCENTRAT RAJČICE ST. PODRAVKA 720 g (12) | 16 | `koncentr` |
| RAJČICA KONCENTRAT 4500G 28-30% LIM. PODRAVKA | 14 | `koncentr` |
| RAJČICA PASIRANA 3X200G,PODRAVKA (8) (PAL 120) | 14 | `pasir` |
| RAJČICA MUTTI 700G PASIRANA BOCA-12/1- 63070 | 13 | `mutti` |
| RAJČICA PODR 680G PASSATA -12/1- PASIRANA BOCA | 12 | `pasir` |
| N-RAJČICA PODR 500G PASIRANA TETRA BRIK -12/1- | 11 | `pasir` |
| RAJČICA GIANA 680G PASIRANA -12/1- STAKLO | 11 | `pasir` |
| PASIRANA RAJČICA BRIKGIANA 500G 1/12 | 10 | `pasir` |
| PELAT RAJČICA 800 g PODRAVKA OC. MASA 480 g | 10 | `pelat` |
| KONCENTRAT RAJČICE LIM. 850 g PODRAVKA | 7 | `koncentr` |

</details>

<a id="pasirana_rajcica"></a>
## pasirana rajčica (`pasirana_rajcica`)

jedinica: **kg** · loose_produce: **false** · grupa: **140** · isključenih grupa: **4** · pakiranje: **200–3000**

sinonimi: pasirana rajcica, passata, rajcica pasirana  
must_match: `pasirana rajcica | rajcica pasirana | pasir rajcica | rajcica pasir | passata`

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
| 14 | 8033837720720 | RAJČICA PASIRANA 690ml ROSSOGARGANO | 690 g | 6 | 469 | 2,52–4,19 /kg | high/name |  |
| 15 | 3838945042505 | PASIRANA RAJČICA CLASSIC 750 ml FRUCTAL | 750 ml | 6 | 292 | – /l | high/name |  |
| 16 | 3838945042512 | PASIRANA RAJČICA PIZZA 750 ml FRUCTAL | 750 ml | 6 | 285 | – /l | high/name |  |
| 17 | 8005110860508 | PASIRANA RAJČICA MUTTI 500G TETRAPACK | 500 ml | 6 | 241 | 2,18–3,98 /kg | high/name |  |
| 18 | 8000320990113 | RAJČICA PASIRANA CLIMATE 500G CIRIO BRIK | 500 ml | 6 | 221 | 1,66–2,18 /kg | high/name |  |
| 19 | 8001440002199 | RAJČICA PASIRA.500 ml BRIK VALFRUTTA | 500 ml | 6 | 215 | 2,18 /kg | high/name |  |
| 20 | 8001440132391 | PASIRANA RAJCICA NA PARI 700 ML VALFRUTTA | 700 ml | 6 | 146 | 3,07 /kg | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| PASIRANA RAJČICA S BOSILJKOM BOCA 400G MUTTI | 5 | `bosiljk` |
| MUTTI PASIRANA RAJČICA S BOSILJKOM | 2 | `bosiljk` |
| KLC.Rajčica pasir.Rustica s bosiljk 690g | 1 | `bosiljk` |
| RAJČICA PASIR. S BOSILJKOM PETTI 500 ml BOCA PROFUMATO | 1 | `bosiljk` |

</details>

<a id="rajcica_konzerva"></a>
## rajčica (konzerva: sjeckana, pelati, polpa) (`rajcica_konzerva`)

jedinica: **kg** · loose_produce: **false** · grupa: **191** · isključenih grupa: **1** · pakiranje: **200–5000**

sinonimi: rajcica konzerva, sjeckana rajcica, pelati, polpa, rajcica u konzervi  
must_match: `pelat | polpa | sjeckana rajcic | rajcica sjeckan | sjeck rajcic | rajcica sjeck | sjec rajcic | rajcica sjec | rajcica u komad | rajcica komadi | cijela rajcica | rajcica cijela | rajcica oljust | oljustena rajcic`
  
atributi: oblik = pelati, polpa, sjeckana, nepoznato

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850104073724 | RAJČICA PELAT LIMENKA 400G/240G (12)PODRAVKA (PAL 96) | 400 g | 21 | 880 | 3,13–6,63 /kg | high/name | oblik=pelati |
| 2 | 8005110060007 | PELATI U SOKU OD RAJČICE KONZERVA 400G MUTTI | 400 g | 17 | 761 | 3,65–5,88 /kg | high/name | oblik=pelati |
| 3 | 3850104238802 | RAJCICA SJECKANA LIMENKA 400 G PODRAVKA | 400 g | 17 | 695 | 3,73–7,45 /kg | high/name | oblik=sjeckana |
| 4 | 3850104073212 | PELAT RAJČICA 800 g PODRAVKA OC. MASA 480 g | 800 g | 15 | 477 | 1,88–5,51 /kg | high/name | oblik=pelati |
| 5 | 3850104220616 | SJEC.RAJČICA TETRA RECART 390G (16) PODRAVKA | 390 g | 14 | 403 | 2,56–9,13 /kg | high/name | oblik=sjeckana |
| 6 | 3856020222260 | BIO SJECKANA RAJČICA 400 g HR PODRAVKA | 400 g | 12 | 410 | 4,80–7,05 /kg | high/name | oblik=sjeckana |
| 7 | 3856020235987 | BIO PELAT 400 g OC. MASA 240 g PODRAVKA | 400 g | 10 | 185 | 2,97–7,30 /kg | high/name | oblik=pelati |
| 8 | 3850104073717 | PELATI RAJČICE LIM. 2.49 kg OC.MASA 1395 g | 2,49 kg | 9 | 31 | 1,76–4,42 /kg | high/name | oblik=pelati |
| 9 | 8005110050008 | RAJČICA MUTTI 800G PELATI-12/1- LIMENKA 51102 | 800 g | 7 | 317 | 1,60–4,74 /kg | high/name | oblik=pelati |
| 10 | 8000320010118 | RAJČICA SJECKANA CIRIO 400G U | 400 g | 7 | 222 | 2,00–4,65 /kg | high/name | oblik=sjeckana |
| 11 | 8000320010026 | Cirio pelati oljuštene rajčice 400g/250g | 400 g | 6 | 226 | 2,63–4,98 /kg | high/name | oblik=pelati |
| 12 | 8033837720003 | SJECKANA RAJČICA 400g ROSSO GARGANO | 400 g | 5 | 399 | 2,43–4,38 /kg | high/name | oblik=sjeckana |
| 13 | 3856020280390 | RAJČICA SJECKANA S BOSILJAKOM I ORIGANOM 400G PODRAVKA | 400 g | 5 | 181 | 4,72–5,80 /kg | high/name | oblik=sjeckana |
| 14 | 8009755006000 | RAJČICA FIAMMA 400G PELAT-24/1- 0339021 | 400 g | 5 | 172 | 2,33–3,47 /kg | high/name | oblik=pelati |
| 15 | 8001440110351 | RAJČICA VALFRUTTA 400G PELATI | 400 g | 5 | 129 | 2,97–5,63 /kg | high/name | oblik=pelati |
| 16 | 8000320010033 | RAJČICA CIRIO PELATI CIJELI800G -12/1 | 800 g | 5 | 67 | 2,61–4,74 /kg | high/name | oblik=pelati |
| 17 | 3856003902103 | RAJČICA PELATI 400g ZORELA-OCIJEĐENA MASA 240g | 240 g | 4 | 449 | 2,13–4,96 /kg | high/name | oblik=pelati |
| 18 | 8001440118401 | RAJCICA SJECKANA 2X330 ML VALFRUTTA | 660 ml | 4 | 138 | – /l | high/name | oblik=sjeckana |
| 19 | 8001440111143 | RAJČICA SJECKANA CUBETTI 400g VALFRUTTA | 400 g | 4 | 108 | 2,97–4,98 /kg | high/name | oblik=sjeckana |
| 20 | 8005110043109 | RAJČICA PELAT 2,5kg MUTTI (6) | 2,5 kg | 4 | 39 | 3,18–3,60 /kg | high/name | oblik=pelati |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| UMAK POLPA DATTERINO 360 g AGROMONTE | 1 | `umak` |

</details>

<a id="koncentrat_rajcice"></a>
## koncentrat rajčice (`koncentrat_rajcice`)

jedinica: **kg** · loose_produce: **false** · grupa: **40** · isključenih grupa: **0** · pakiranje: **50–1000**

sinonimi: koncentrat rajcice, pire od rajcice  
must_match: `koncentrat rajcic | rajcica koncentrat | konc rajcic | rajcica konc | dupli konc`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850104053221 | RAJČICA KONCENTRAT TUBA 190G (24), PODRAVKA (PAL 76) | 190 g | 25 | 1403 | 6,95–17,11 /kg | high/name |  |
| 2 | 3850104053214 | RAJČICA KONCENTRAT TUBA 120G (24), PODRAVKA | 120 g | 20 | 748 | 9,67–19,08 /kg | high/name |  |
| 3 | 3850104268533 | RAJČICA KONCENTRAT 300G, PODRAVKA (12) (PAL 48) | 300 g | 18 | 626 | 7,50–13,30 /kg | high/name |  |
| 4 | 3856020269166 | KONCENTRAT RAJCICA 370G STAKLENKA PODRAVKA | 370 g | 18 | 459 | 6,73–10,24 /kg | high/name |  |
| 5 | 3856020269197 | KONCENTRAT RAJČICE ST. PODRAVKA 720 g (12) | 720 g | 18 | 236 | 5,13–8,32 /kg ⚠4 | high/name |  |
| 6 | 3856020269135 | KONCENTRAT RAJČICE STAKLO 210G (12) PODRAVKA | 210 g | 11 | 259 | 8,14–13,38 /kg | high/name |  |
| 7 | 8001440127007 | VALFRUTTA DVOSTRUK.KONC.RAJČICE TUBA 130G (24) | 130 g | 10 | 95 | 6,38–10,15 /kg ⚠1 | high/name |  |
| 8 | 3850104053153 | KONC. RAJČICE 460 g LIM. PODRAVKA (12) | 460 g | 9 | 193 | 3,67–8,85 /kg | high/name |  |
| 9 | 8005110120015 | DVOSTRUKI KONCENTRAT RAJČICE 200 g MUTTI | 200 g | 8 | 215 | 8,95–13,95 /kg | high/name |  |
| 10 | 3850104053177 | KONCENTRAT RAJČICE LIM. 850 g PODRAVKA | 850 g | 8 | 34 | 3,73–7,09 /kg | high/name |  |
| 11 | 80042532 | DUPLI KONCENTRAT RAJCICE 130 G MUTTI | 130 g | 4 | 359 | 10,15–15,00 /kg | high/name |  |
| 12 | 80042518 | KONCENTRAT RAJČICE TROSTRUKI 280g MUTTI | 280 g | 4 | 146 | 12,82–15,32 /kg | high/name |  |
| 13 | 8009755007076 | RAJČICA KONCENTRAT 400g FIAMMA | 400 g | 4 | 140 | 2,97–7,23 /kg | high/name |  |
| 14 | 3850104053146 | KONCENTRAT RAJCICA 260 G LIMENKA PODRAVKA | 260 g | 4 | 98 | 6,31–9,00 /kg | high/name |  |
| 15 | 3856003945896 | RAJČICA KONCENTRAT 200 g ZORELA | 200 g | 3 | 455 | 6,95–7,95 /kg | high/name |  |
| 16 | 3859890236924 | RAJČICA KONCE. 200 g VM2 | 200 g | 2 | 41 | 6,60–7,95 /kg | high/name |  |
| 17 | 4007415006098 | KONC.RAJČICA 850 ml MIKADO | 850 ml | 2 | 11 | – /l | high/ean |  |
| 18 | 3831029509062 | RAJČICA KONCETRAT NATURETA 180 g TUBA ORBI | 180 g | 2 | 2 | 11,00–11,44 /kg | high/name |  |
| 19 | 3838900843208 | RAJČICA KONCE TUBA GARDEN GOOD 200 g | 200 g | 1 | 184 | 6,95–7,40 /kg | high/name |  |
| 20 | 3856025853049 | RAJCICA KONCENTRAT 200 G TUBA CAMPO | 200 g | 1 | 154 | 6,45 /kg | high/name |  |

<a id="mrkva"></a>
## mrkva (`mrkva`)

jedinica: **kg** · loose_produce: **true** · grupa: **122** · isključenih grupa: **41**

sinonimi: mrkva, mrkvu, mrkve  
must_match: `mrkv`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850334021243 | MRKVA PAKIRANA 1kg | 1 kg | 3 | 195 | 1,05–1,61 /kg | high/ean |  |
| 2 | 3859889644105 | MRKVA PAKIRANA 1 kg | 1 kg | 2 | 351 | 1,39–1,49 /kg | high/name |  |
| 3 | 3859889644099 | MRKVA 500 g | 500 g | 2 | 351 | 2,38–2,90 /kg | high/name |  |
| 4 | 3850334173126 | MRKVA (5) |  | 2 | 196 | 0,55–0,85 /kg | low/unit_price |  |
| 5 | 3858885876923 | Mrkva rfs | 5 kg | 2 | 151 | 1,04 /kg ⚠144 | high/name |  |
| 6 | 3856028689522 | MRKVA ŽUTA 500 g | 500 g | 2 | 133 | 2,18 /kg | high/name |  |
| 7 | 3859891082063 | MRKVA PAKIRANA 1 kg | 1 kg | 2 | 62 | 1,29–1,61 /kg | high/name |  |
| 8 | 3858885875162 | Mrkva košarica 1kg | 1 kg | 2 | 55 | 1,29–1,79 /kg | high/name |  |
| 9 | 3857500129802 | MRKVA VOĆARNA STUDENCA 1 kg | 1 kg | 2 | 22 | 1,29–1,49 /kg | high/name |  |
| 10 | 3870547029782 | MRKVA NANTES STANDARD |  | 2 | 12 | – | – |  |
| 11 | 3859894093066 | MRKVA 2kg ZEMLJA PORIJEKLA HRVATSKA | 2 kg | 2 | 8 | 1,00–1,15 /kg | high/name |  |
| 12 | 3850104282676 | MRKVA KOCKE LIM. 4.1kg PODRAVKA | 4,1 kg | 2 | 3 | 2,27–2,43 /kg | high/name |  |
| 13 | 5411361008409 | MRKVA 2,5 kg BABY ARDO UG. | 2,5 kg | 2 | 2 | 1,80–2,00 /kg | high/ean |  |
| 14 | 3859891246755 | MRKVA 500 g | 500 g | 2 | 2 | 1,96–1,98 /kg | high/name |  |
| 15 | ntl:248678 | MRKVA |  | 1 | 343 | 0,89 /kg | low/unit_price |  |
| 16 | 3859891082858 | MRKVA PAKIRANA 1 KG | 1 kg | 1 | 155 | 1,29 /kg | high/name |  |
| 17 | 3858889117916 | MRKVA S BUDGET 1 kg | 1 kg | 1 | 144 | 1,29–1,39 /kg | high/name |  |
| 18 | 3856021206849 | MRKVA VH 500 g | 500 g | 1 | 143 | 1,78 /kg | high/name |  |
| 19 | 9100000016207 | BIO MRKVA NATUR PUR 500 g | 500 g | 1 | 142 | 2,98–3,18 /kg | high/name |  |
| 20 | plodine:111801 | MRKVA RINFUZO |  | 1 | 139 | 0,89 /kg | low/unit_price |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| SMRZ. MRKVA KOCKA 2,5kg LEDO | 7 | `kocka` |
| GRAŠAK MRKVA KOCKE ZMH HORVAT (2,5kg) | 4 | `grasak` |
| GRAŠAK-MRKVA 2.5kg LEDO | 4 | `grasak` |
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

jedinica: **kg** · loose_produce: **true** · grupa: **240** · isključenih grupa: **153**

sinonimi: paprika, babura, svjeza paprika  
must_match: `paprik | babur`
  
atributi: boja = crvena, zuta, zelena; vrsta = babura, rog, ljuta

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3858885876060 | PAPRIKA BABURA RFZ (10) |  | 4 | 348 | 2,29–2,75 /kg | low/unit_price | vrsta=babura |
| 2 | 3850334079893 | *PAPRIKE TRICO.500 g | 500 g | 4 | 281 | 3,38–6,50 /kg | high/ean |  |
| 3 | 3859892029500 | PAPRIKA MIX |  | 2 | 196 | 5,38–6,38 /kg | low/unit_price |  |
| 4 | 3850334173430 | PAPRIKA CRVENA (5) |  | 2 | 163 | 2,84–5,19 /kg | low/unit_price | boja=crvena |
| 5 | 3850334173164 | PAPRIKA ZELENA (5) |  | 2 | 138 | 2,71–3,99 /kg | low/unit_price | boja=zelena |
| 6 | 3858885877135 | PAPRIKA ROG CRVENA KL II |  | 2 | 16 | 1,89–9,00 /kg | low/unit_price | vrsta=rog, boja=crvena |
| 7 | ntl:245788 | PAPRIKA ROG CRVENA |  | 1 | 343 | 1,99–2,49 /kg | low/unit_price | vrsta=rog, boja=crvena |
| 8 | ntl:248680 | PAPRIKA BABURA |  | 1 | 343 | 2,29–2,49 /kg | low/unit_price | vrsta=babura |
| 9 | ntl:244179 | PAPRIKA CRVENA |  | 1 | 343 | 3,69–3,99 /kg | low/unit_price | boja=crvena |
| 10 | 8033737509999 | PAPRIKA SEMAFOR CCA 500 G |  | 1 | 342 | 5,98 /kg | low/unit_price |  |
| 11 | ntl:008560 | PAPRIKA MIX 300G | 300 g | 1 | 342 | 9,97 /kg | high/name |  |
| 12 | 3850334386267 | PAPRIKA ROG CRVENA |  | 1 | 166 | 2,29–2,75 /kg | low/unit_price | vrsta=rog, boja=crvena |
| 13 | ntl:244178 | PAPRIKA ZELENA |  | 1 | 162 | 2,99 /kg | low/unit_price | boja=zelena |
| 14 | 3613075000003 | PAPRIKA ROGA CRVENA 500G. | 500 g | 1 | 155 | 2,98 /kg | high/name | vrsta=rog, boja=crvena |
| 15 | 3856025896879 | PAPRIKA ZUTA BABURA 720 G CAMPO | 720 g | 1 | 155 | 3,46 /kg | high/name | vrsta=babura, boja=zuta |
| 16 | 4052963159017 | PAPRIKA ROGA ZUTA 500 G | 500 g | 1 | 155 | 3,98 /kg | high/name | vrsta=rog, boja=zuta |
| 17 | 8033100010022 | PAPRIKA CHILI CRVENA VEZ. |  | 1 | 153 | – | – | boja=crvena |
| 18 | plodine:112740 | PAPRIKA ROGA LJUTA 200G | 200 g | 1 | 152 | 7,95–9,95 /kg | high/name | vrsta=rog |
| 19 | 8057960790092 | PAPRIKA ROGA CRVENA |  | 1 | 151 | 2,29 /kg | low/unit_price | vrsta=rog, boja=crvena |
| 20 | plodine:112712 | PAPRIKA BABURA |  | 1 | 145 | 1,49 /kg | low/unit_price | vrsta=babura |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| PAPRIKA FILET CRVENA 660G/300G (12), PODRAVKA | 11 | `filet` |
| PAPRIKA FILE ŽUTA 670G OC.MASA 350G (12) ZVIJEZDA | 10 | `zvijezda` |
| PEČENA PAPRIKA 650G/400G (12) PODRAVKA | 10 | `pecen` |
| Šafram paprika zač. mljev. slatka 500 g | 9 | `slatka` |
| N-PAPRIKA ZVIJEZDA PEČENA 540G (310G OČIŠ.MASE) -12/1- | 8 | `pecen` |
| PAPRIKA PODR 4000G FILETI CRVENA -2/1- LIMENKA | 8 | `filet` |
| PAPRIKA FILET ŽUTA 650G VITAM. OC.MASA 360 G (6) | 7 | `filet` |
| PAPRIKA REZANA 680 g PODRAVKA (12) OS.MASA 350 g | 7 | `rezan` |
| PAPRIKA SLATKA MLJEVENA 1000g ŠAFRAM | 7 | `mljeven` |
| PAPRIKA MLJEVENA ZAČINSKA LJUTA 500G, ŠAFRAM | 6 | `mljeven` |

</details>

<a id="krastavac"></a>
## krastavac (svježi) (`krastavac`)

jedinica: **kg** · loose_produce: **true** · grupa: **72** · isključenih grupa: **86**

sinonimi: krastavac, krastavci, svjezi krastavac  
must_match: `krastav`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3858891564432 | KRASTAVCI 680G (6-9cm) 720ML ULTRA PLUS EVERYDAYS | 680 g | 7 | 77 | 2,21–3,75 /kg | high/name |  |
| 2 | 3858891564388 | ULTRA KRASTAVCI (3-6) 2300G -1300G (6) | 2,3 kg | 7 | 37 | 1,94–3,08 /kg | high/name |  |
| 3 | 3858891564357 | KRASTAVCI 680G 720ML (3-6cm) ULTRA PLUS | 680 g | 6 | 76 | 3,29–4,25 /kg | high/name |  |
| 4 | 3858885876077 | KRASTAVAC RFZ (10) |  | 2 | 153 | 1,69–1,89 /kg | low/unit_price |  |
| 5 | 8595241528878 | KRASTAVCI 6-9cm 670g/360g | 670 g | 2 | 6 | 1,93–2,97 /kg | high/name |  |
| 6 | 3858886520320 | KRASTAVCI 4 kg MARI UG. | 4 kg | 2 | 4 | 1,61–1,66 /kg | high/name |  |
| 7 | 5319990747365 | KRASTAVCI 4,1kg BONVITA VM2 | 4,2 kg | 2 | 2 | 1,55–2,02 /kg | high/name |  |
| 8 | ntl:248144 | KRASTAVAC |  | 1 | 343 | 1,79–1,89 /kg | low/unit_price |  |
| 9 | 3850334173409 | KRASTAVAC |  | 1 | 184 | 1,89–2,25 /kg | low/unit_price |  |
| 10 | 3850334072078 | KRASTAVAC K PLUS REZANI 670G/360g | 670 g | 1 | 162 | 2,97–3,21 /kg | high/name |  |
| 11 | 3857500059284 | KRASTAVAC 3/1 |  | 1 | 155 | – | – |  |
| 12 | 3858889112263 | KRASTAVCI S-BUDGET 6-9 670 g | 670 g | 1 | 144 | 2,07 /kg | high/name |  |
| 13 | 3858889112256 | KRASTAVCI S-BUDGET 3-6 670 g | 670 g | 1 | 143 | 2,91 /kg | high/name |  |
| 14 | 3830070890273 | BIO KRASTAVAC 500G | 500 g | 1 | 139 | 2,98–5,18 /kg | high/name |  |
| 15 | plodine:113101 | KRASTAVAC |  | 1 | 134 | 1,69 /kg | low/unit_price |  |
| 16 | gavranovic:071176 | KRASTAVAC |  | 1 | 122 | 2,49–2,59 /kg | low/unit_price |  |
| 17 | lidl:0082225 | Krastavac | 1 kg | 1 | 116 | 1,79 /kg | high/unit |  |
| 18 | 4056489008644 | Krastavac 750g | 750 g | 1 | 116 | 2,39–2,92 /kg | high/name |  |
| 19 | lidl:0084535 | Bio krastavac | 1 kom | 1 | 116 | – /kom | high/unit |  |
| 20 | 3858889116759 | KRASTAVCI S-BUDGET 6-9 2350 g | 2,35 kg | 1 | 99 | 2,46 /kg | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| KRASTAVCI PASTERIZIRANI 670G/370G (12), PODRAVKA (PAL 48) | 13 | `pasterizir` |
| N-KRASTAVCI ZVIJEZDA 670G DELIK.1.KLASA -12/1- | 13 | `delik\b` |
| KRASTAVCI KLASIK 660G/330G(12) PODRAVKA (PAL 48) | 11 | `podravka` |
| N-KRASTAVCI ZVIJEZDA 670G(330G)KLASIK DRUGA KLASA | 8 | `zvijezda` |
| KRASTAVCI LIM 4 kg PODRAVKA (6) OC MASA 2000 g | 7 | `masa\b` |
| KRASTAVCI ST. 2450 g VEN. PODRAVKA OC.MASA 1300 g | 7 | `masa\b` |
| KRASTAVCI DELIKA. 680 g OC.MASA 370 g VITAMI. (6) | 6 | `masa\b` |
| KRASTAVCI ST. 1500 g VEN. PODRAVKA OC.MASA 800 g | 6 | `masa\b` |
| N-KRASTAVCI ZVIJEZDA 540G PREMIUM (290G OČIŠ.MASE) -12/1- | 6 | `mase\b` |
| KRASTAVCI PODRAVKA 4.2 kg OC MASA 2.2 kg (2) | 5 | `masa\b` |

</details>

<a id="tikvica"></a>
## tikvica (`tikvica`)

jedinica: **kg** · loose_produce: **true** · grupa: **53** · isključenih grupa: **9**

sinonimi: tikvica, tikvice  
must_match: `tikvic`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | ntl:248685 | TIKVICA |  | 1 | 343 | 1,49–1,69 /kg | low/unit_price |  |
| 2 | 3850334173195 | TIKVICE |  | 1 | 188 | 1,69–2,05 /kg | low/unit_price |  |
| 3 | 3857500059277 | TIKVICA 3/1 |  | 1 | 155 | – | – |  |
| 4 | 8057960790139 | TIKVICA ZELENA |  | 1 | 151 | 1,09–1,49 /kg | low/unit_price |  |
| 5 | 3858893251774 | Tikvice rfs |  | 1 | 144 | 1,69–1,79 /kg | low/unit_price |  |
| 6 | 8435320673221 | BIO TIKVICE NATUR PUR 500 g | 500 g | 1 | 142 | 4,58 /kg | high/name |  |
| 7 | 8437007908084 | BIO TIKVICA 500G. | 500 g | 1 | 135 | 3,58 /kg | high/name |  |
| 8 | gavranovic:072061 | TIKVICA |  | 1 | 119 | 2,19–5,39 /kg | low/unit_price |  |
| 9 | lidl:0082345 | Tikvica | 1 kg | 1 | 116 | 1,19–1,69 /kg | high/unit |  |
| 10 | lidl:0084545 | Bio tikvica 500g | 500 g | 1 | 116 | 3,78 /kg | high/name |  |
| 11 | tommy:10000094 | TIKVICE |  | 1 | 87 | 1,69–1,89 /kg | low/unit_price |  |
| 12 | 8009735185039 | BIO TIKVICE PAKIRANE 500 g | 500 g | 1 | 72 | 5,78 /kg ⚠7 | high/name |  |
| 13 | 3858890133028 | TIKVICA 500G EKOZONA | 500 g | 1 | 72 | 5,78 /kg ⚠7 | high/name |  |
| 14 | plodine:111827 | BIO TIKVICA 500G | 500 g | 1 | 69 | 3,44–3,98 /kg | high/name |  |
| 15 | ribola:0109321 | TIKVICA |  | 1 | 61 | 1,69–2,50 /kg | low/unit_price |  |
| 16 | kaufland:09700763 | Tikvica |  | 1 | 53 | 1,69 /kg | low/unit_price |  |
| 17 | 8024581000398 | KBio.Tikvica 500g | 500 g | 1 | 53 | 4,58 /kg | high/name |  |
| 18 | 3856028689386 | TIKVICA 500 g BIO ZONE | 500 g | 1 | 48 | 4,58 /kg | high/name |  |
| 19 | eurospin:080062402 | TIKVICE rfz |  | 1 | 43 | 1,49 /kg | low/unit_price |  |
| 20 | 8001553802860 | TIKVICA |  | 1 | 43 | – | – |  |

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

jedinica: **kg** · loose_produce: **true** · grupa: **116** · isključenih grupa: **18**

sinonimi: kupus, glavica kupusa  
must_match: `kupus`
  
atributi: vrsta = crveni, bijeli, kineski, mladi

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3858885876169 | KUPUS BIJELI - KG |  | 4 | 221 | 0,68–0,79 /kg | low/unit_price | vrsta=bijeli |
| 2 | 3850334173348 | KUPUS CRVENI (25) |  | 2 | 179 | 0,89–1,16 /kg | low/unit_price | vrsta=crveni |
| 3 | 3858885876718 | KUPUS CRVENI - KG |  | 2 | 151 | 0,80–0,99 /kg | low/unit_price | vrsta=crveni |
| 4 | 3850334386168 | KUPUS KINESKI KOM (25) |  | 2 | 110 | 1,69 /kg | low/unit_price | vrsta=kineski |
| 5 | 3858885876152 | KUPUS MLADI SVJEŽI (9) |  | 2 | 16 | 0,49–0,67 /kg ⚠4 | low/unit_price | vrsta=mladi |
| 6 | ntl:248543 | KUPUS |  | 1 | 343 | 0,59–0,79 /kg | low/unit_price |  |
| 7 | ntl:248673 | KUPUS CRVENI |  | 1 | 343 | 0,99 /kg | low/unit_price | vrsta=crveni |
| 8 | 3850334173119 | KUPUS SVJEŽI |  | 1 | 188 | 0,79 /kg | low/unit_price |  |
| 9 | 3850334173393 | KUPUS SVJEŽI MLADI |  | 1 | 170 | 1,09 /kg | low/unit_price | vrsta=mladi |
| 10 | ntl:027829 | KUPUS KINESKI |  | 1 | 162 | 2,29 /kg | low/unit_price | vrsta=kineski |
| 11 | plodine:110102 | KUPUS ZELENI |  | 1 | 152 | 0,79 /kg | low/unit_price |  |
| 12 | 3859894356031 | KUPUS KINESKI VH kom |  | 1 | 139 | – | – | vrsta=kineski |
| 13 | gavranovic:071183 | KUPUS |  | 1 | 122 | 0,79–1,39 /kg | low/unit_price |  |
| 14 | 53112132 | KUPUS CRVENI |  | 1 | 122 | 0,79 /kg | low/unit_price | vrsta=crveni |
| 15 | gavranovic:071184 | KUPUS MLADI |  | 1 | 122 | 0,89–1,35 /kg | low/unit_price | vrsta=mladi |
| 16 | gavranovic:071182 | KUPUS CRVENI |  | 1 | 122 | 1,29–1,89 /kg | low/unit_price | vrsta=crveni |
| 17 | gavranovic:162556 | KUPUS KINESKI |  | 1 | 122 | – ⚠122 | – | vrsta=kineski |
| 18 | plodine:958005 | KUPUS SA KOBASICAMA PORCIJA GASTRO |  | 1 | 121 | – | – |  |
| 19 | lidl:0082955 | Kupus bijeli | 1 kg | 1 | 116 | 0,79 /kg | high/unit | vrsta=bijeli |
| 20 | lidl:0082945 | Kupus crveni | 1 kg | 1 | 116 | 0,79 /kg | high/unit | vrsta=crveni |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| REZAČ KUPUSA S DVA NOŽA 45341 FAC | 4 | `rezac` |
| CRVENA KUPUS SALATA | 1 | `salata` |
| KUPUS REZANI 500 g | 1 | `rezani` |
| Kupus bijeli rezani | 1 | `rezani` |
| Kupus bijeli ribani-Julienne | 1 | `julienne` |
| Kupus bijeli salata | 1 | `salata` |
| Kupus crveni rezani | 1 | `rezani` |
| Kupus crveni ribani | 1 | `ribani` |
| Kupus crveni ribani-Julienne | 1 | `julienne` |
| Kupus crveni salata | 1 | `salata` |

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
| 3 | 3831029504586 | KUPUS KISELI 530g NATURETA ocijeđene mase 300g | 530 g | 6 | 297 | 3,96–5,64 /kg | high/name |  |
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
## zelena salata (glavice) (`zelena_salata`)

jedinica: **kg** · loose_produce: **true** · grupa: **73** · isključenih grupa: **2**

sinonimi: zelena salata, lollo, salata, iceberg, ledenka, kristalka, puterica  
must_match: `salata iceberg | iceberg salata | salata ledenk | ledenk | salata kristalk | kristalka salata | salata puteric | puterica | salata zelena puteric | lollo | zelena salata | salata zelena | salata glav`
  
atributi: vrsta = iceberg, kristalka, puterica, lollo

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3859889558891 | SALATA ICEBERG KOMAD (12) |  | 2 | 194 | 5,63–6,83 /kg | low/unit_price | vrsta=iceberg |
| 2 | 4232300003122 | SALATA ICEBERG kom |  | 2 | 21 | – | – | vrsta=iceberg |
| 3 | 8033650133431 | SALATA ICEBERG KOM |  | 1 | 342 | 3,32 /kg | low/unit_price | vrsta=iceberg |
| 4 | 8058056198877 | SALATA ICEBERG KOM |  | 1 | 155 | – | – | vrsta=iceberg |
| 5 | plodine:111305 | SALATA KRISTALKA -KOMAD |  | 1 | 155 | – | – | vrsta=kristalka |
| 6 | spar:178388 | SALATA ICEBERG kom |  | 1 | 144 | – | – | vrsta=iceberg |
| 7 | gavranovic:141336 | SALATA ICEBERG KOM |  | 1 | 119 | – | – | vrsta=iceberg |
| 8 | gavranovic:158919 | SALATA PUTERICA 1KOM | 1 kom | 1 | 119 | – /kom | high/name | vrsta=puterica |
| 9 | lidl:0082031 | Salata Iceberg | 1 kom | 1 | 116 | – /kom | high/unit | vrsta=iceberg |
| 10 | lidl:0082071 | Salata puterica | 1 kom | 1 | 116 | – /kom | high/unit | vrsta=puterica |
| 11 | tommy:10000062 | SALATA KRISTALKA SVJ. KOM |  | 1 | 87 | – | – | vrsta=kristalka |
| 12 | tommy:10000653 | SALATA ICEBERG SVJ. KOM |  | 1 | 86 | – | – | vrsta=iceberg |
| 13 | tommy:10510656 | SALATA PUTERICA S KORIJENOM |  | 1 | 72 | – | – | vrsta=puterica |
| 14 | tommy:10019228 | SALATA PUTERICA SVJ. KOM |  | 1 | 72 | – | – | vrsta=puterica |
| 15 | ntl:002085 | SALATA PUTERICA KOM |  | 1 | 53 | 2,24–2,44 /kg | low/unit_price | vrsta=puterica |
| 16 | 3859891811137 | Salata Iceberg |  | 1 | 53 | – | – | vrsta=iceberg |
| 17 | 3858893252450 | Salata zelena kristal kom |  | 1 | 53 | – | – | vrsta=kristalka |
| 18 | 3859891811168 | Salata zelena puterica kom |  | 1 | 53 | – | – | vrsta=puterica |
| 19 | kaufland:09701482 | Salata zelena endivija kom |  | 1 | 52 | – | – |  |
| 20 | 8001553801382 | SALATA PUTERICA |  | 1 | 43 | – | – | vrsta=puterica |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| SJEME SALATA KRISTALKA | 1 | `sjeme` |
| Salata zelena sa sirom | 1 | `sa sirom` |

</details>

<a id="rukola"></a>
## rukola (`rukola`)

jedinica: **kg** · loose_produce: **true** · grupa: **19** · isključenih grupa: **2**

sinonimi: rukola, rikola, rucola  
must_match: `rukol | rikol | rucola`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | lidl:0082135 | Salata rukola | 125 g | 1 | 116 | 6,00–10,32 /kg | high/unit |  |
| 2 | 8001553801689 | RUKOLA |  | 1 | 43 | – | – |  |
| 3 | 8001553801696 | RUKOLA |  | 1 | 43 | – | – |  |
| 4 | spar:37156 | Rukola-parmezan |  | 1 | 23 | 10,61 /kg | low/unit_price |  |
| 5 | boso:302096 | RUKOLA 100 G KOM II KL | 100 g | 1 | 13 | 9,90 /kg | high/name |  |
| 6 | ribola:0116466 | RIKOLA II KL |  | 1 | 7 | 5,24 /kg | low/unit_price |  |
| 7 | studenac:147293 | RUKOLA RFZ |  | 1 | 6 | – | – |  |
| 8 | vrutak:750228 | SALATA RIKOLA RINFUZA1# CCA 1KG |  | 1 | 4 | – | – |  |
| 9 | bure:2099800001636 | RIKOLA SVJ. |  | 1 | 3 | 7,99–8,25 /kg | low/unit_price |  |
| 10 | studenac:119862 | RUKOLA POSUDICA SNIŽ. 100 g | 100 g | 1 | 3 | 9,00 /kg | high/name |  |
| 11 | trgocentar:2504243 | RIKOLA |  | 1 | 1 | 5,88 /kg | low/unit_price |  |
| 12 | stridon:068389 | RIKOLA AGROVIR |  | 1 | 1 | 5,97 /kg | low/unit_price |  |
| 13 | bure:792009000010 | RIKOLA 100g | 100 g | 1 | 1 | 7,60 /kg | high/name |  |
| 14 | trgocentar:4833295 | RIKOLA 100G (PT) | 100 g | 1 | 1 | 13,90 /kg | high/name |  |
| 15 | lorenco:508 | RIKOLA 100g | 100 g | 1 | 1 | 17,10 /kg | high/name |  |
| 16 | lorenco:415 | RIKOLA |  | 1 | 1 | – | – |  |
| 17 | lorenco:2000582 | RIKOLA,MATOVILAC |  | 1 | 1 | – | – |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| SJEME RUKOLA | 1 | `sjeme` |
| SJEME RUKOLA DIVLJA | 1 | `sjeme` |

</details>

<a id="matovilac"></a>
## matovilac (`matovilac`)

jedinica: **kg** · loose_produce: **true** · grupa: **22** · isključenih grupa: **3**

sinonimi: matovilac, motovilac  
must_match: `matovil | motovil`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | eurospin:080312101 | MATOVILAC 250g | 250 g | 1 | 43 | 10,76 /kg | high/name |  |
| 2 | 8001553801795 | MATOVILAC |  | 1 | 43 | – | – |  |
| 3 | 8001553801764 | MATOVILAC |  | 1 | 43 | – | – |  |
| 4 | 3858885877555 | MATOVILAC RFZ (1) |  | 1 | 9 | 7,48 /kg | low/unit_price |  |
| 5 | 8012566001041 | 500G MATOVILAC L'INSALATE KL I | 500 g | 1 | 7 | 11,72 /kg | high/name |  |
| 6 | trgovina-krk:0140077 | MATOVILAC ZA GASTRO 1 kg | 1 kg | 1 | 4 | 5,16–10,75 /kg | high/name |  |
| 7 | trgovina-krk:0030189 | MATOVILAC |  | 1 | 3 | 12,89 /kg | low/unit_price |  |
| 8 | vrutak:750223 | MATOVILAC |  | 1 | 3 | – | – |  |
| 9 | bure:2079800007425 | MATOVILAC SV. |  | 1 | 2 | 10,89–10,99 /kg | low/unit_price |  |
| 10 | studenac:119861 | MATOVILAC POSUDICA SNIŽ. 100 g | 100 g | 1 | 1 | 8,00 /kg | high/name |  |
| 11 | stridon:106184 | MATOVILAC AGROVIR |  | 1 | 1 | 10,89 /kg | low/unit_price |  |
| 12 | 3850334173133 | MATOVILAC RFZ |  | 1 | 1 | 11,15 /kg | low/unit_price |  |
| 13 | trgocentar:0396087 | MATOVILAC 100G | 100 g | 1 | 1 | 12,90 /kg | high/name |  |
| 14 | stridon:106414 | MATOVILAC 100 g AGROVIR | 100 g | 1 | 1 | 13,30 /kg | high/name |  |
| 15 | branka:3306/5871 | MATOVILAC 125g | 125 g | 1 | 1 | 14,32 /kg | high/name |  |
| 16 | lorenco:505 | MATOVILAC 100g | 100 g | 1 | 1 | 16,80 /kg | high/name |  |
| 17 | trgocentar:4833350 | MATOVILAC 100G (PT) | 100 g | 1 | 1 | 16,90 /kg | high/name |  |
| 18 | trgocentar:0079545 | MATOVILAC |  | 1 | 1 | – ⚠1 | – |  |
| 19 | lorenco:412 | MATOVILAC |  | 1 | 1 | – | – |  |
| 20 | lorenco:2000582 | RIKOLA,MATOVILAC |  | 1 | 1 | – | – |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| MATOVILAC RADIČ 125g VOĆARN SNIŽ | 1 | `radic` |
| SJEME MATOVILAC HOLANDSKI | 1 | `sjeme` |
| SJEME MATOVILAC ZLICAR | 1 | `sjeme` |

</details>

<a id="radic"></a>
## radič (`radic`)

jedinica: **kg** · loose_produce: **true** · grupa: **45** · isključenih grupa: **6**

sinonimi: radic, cikorija  
must_match: `radic\b | radica\b | cikorij`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850334386274 | RADIČ KOM |  | 1 | 178 | 8,59 /kg | low/unit_price |  |
| 2 | ntl:245283 | RADIČ |  | 1 | 162 | 4,99 /kg | low/unit_price |  |
| 3 | 3858885877265 | Radič rfs |  | 1 | 119 | 4,99 /kg | low/unit_price |  |
| 4 | gavranovic:090298 | RADIČ |  | 1 | 119 | – | – |  |
| 5 | lidl:0082120 | Radić | 1 kg | 1 | 116 | 3,99 /kg | high/unit |  |
| 6 | 8057960790313 | RADIC CRVENI |  | 1 | 99 | 2,79 /kg | low/unit_price |  |
| 7 | kaufland:09700774 | Radič crveni |  | 1 | 52 | 3,99 /kg | low/unit_price |  |
| 8 | 8001553818397 | RADIČ |  | 1 | 43 | – | – |  |
| 9 | 8001553818427 | RADIČ |  | 1 | 43 | – | – |  |
| 10 | 8001553818373 | RADIČ |  | 1 | 43 | – | – |  |
| 11 | 8001553818342 | RADIČ |  | 1 | 43 | – | – |  |
| 12 | 8001553818328 | RADIČ |  | 1 | 43 | – | – |  |
| 13 | 8001553801818 | RADIČ |  | 1 | 43 | – | – |  |
| 14 | 8001553818014 | RADIČ |  | 1 | 43 | – | – |  |
| 15 | tommy:10009221 | RADIČ |  | 1 | 39 | 3,89–4,39 /kg | low/unit_price |  |
| 16 | ktc:00152 | RADIČ |  | 1 | 25 | 2,29–5,99 /kg | low/unit_price |  |
| 17 | studenac:146811 | RADIČ kg |  | 1 | 19 | 1,99–2,19 /kg | low/unit_price |  |
| 18 | spar:50997 | Kristal,radić rezani |  | 1 | 14 | 6,63 /kg | low/unit_price |  |
| 19 | 8717154170016 | SALATA CIKORIJA 500 grama | 500 g | 1 | 10 | 4,98 /kg | high/name |  |
| 20 | trgovina-krk:0000626 | RADIČ |  | 1 | 10 | 7,29 /kg | low/unit_price |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| MATOVILAC RADIČ 125g VOĆARN SNIŽ | 1 | `matovil` |
| SJEME RADIC DIVLJI | 1 | `sjeme` |
| SJEME RADIC GRUMOLO VERDE | 1 | `sjeme` |
| SJEME RADIC PAN DI ZUCHER | 1 | `sjeme` |
| SJEME RADIC TRZASKI SALATNIK | 1 | `sjeme` |
| SJEME RADIC VERONA | 1 | `sjeme` |

</details>

<a id="endivija"></a>
## endivija (`endivija`)

jedinica: **kg** · loose_produce: **true** · grupa: **24** · isključenih grupa: **5**

sinonimi: endivija, frize, frise  
must_match: `endivij | frisee | frize\b`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | plodine:111323 | SALATA ENDIVIJA KOMAD |  | 1 | 155 | – | – |  |
| 2 | gavranovic:158278 | SALATA ENDIVIJA 1KOM | 1 kom | 1 | 119 | – /kom | high/name |  |
| 3 | spar:184145 | SALATA ENDIVIJA kom |  | 1 | 119 | – | – |  |
| 4 | lidl:0082041 | Salata endivija | 1 kom | 1 | 116 | – /kom | high/unit |  |
| 5 | 3850334181978 | SALATA ENDIVIJA KOMAD |  | 1 | 112 | 4,45 /kg | low/unit_price |  |
| 6 | ntl:067427 | SALATA ENDIVIJA KOM |  | 1 | 82 | 2,98–3,23 /kg | low/unit_price |  |
| 7 | 8001553801702 | SALATA ENDIVIJA SCAROLA |  | 1 | 43 | – | – |  |
| 8 | ktc:383630 | SALATA ENDIVIJA KOM |  | 1 | 25 | – | – |  |
| 9 | trgovina-krk:2046657 | SALATA ENDIVIJA KOM |  | 1 | 13 | – | – |  |
| 10 | gavranovic:072060 | SALATA ENDIVIJA |  | 1 | 7 | 1,92–2,79 /kg | low/unit_price |  |
| 11 | 8425779007401 | SALATA FRISEE - KOM KL I |  | 1 | 6 | 8,23 /kg | low/unit_price |  |
| 12 | trgocentar:0410373 | SALATA ENDIVIJA |  | 1 | 4 | 2,70 /kg | low/unit_price |  |
| 13 | metro:264585 | SALATA ENDIVIJA -KG |  | 1 | 3 | 1,85 /kg | low/unit_price |  |
| 14 | tommy:10503195 | SALATA ENDIVIJA KOM |  | 1 | 3 | – | – |  |
| 15 | trgovina-krk:0000635 | SALATA ENDIVIJA |  | 1 | 2 | 3,89 /kg | low/unit_price |  |
| 16 | trgocentar:4832337 | SALATA ENDIVIJA (PT) |  | 1 | 2 | – | – |  |
| 17 | branka:3306/1138 | SALATA ENDIVIJA KOM |  | 1 | 2 | – | – |  |
| 18 | studenac:091091 | SALATA ENDIVIJA |  | 1 | 1 | 1,99 /kg | low/unit_price |  |
| 19 | lorenco:2005134 | SALATA ENDIVIJA |  | 1 | 1 | – | – |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| FRISEE RADIČ 180 g VOĆARNA SNIŽ | 1 | `radic` |
| SJEME ENDIVIJA DJECJA GLAVA | 1 | `sjeme` |
| SJEME ENDIVIJA ESKARIOL ZELENA | 1 | `sjeme` |
| SJEME ENDIVIJA ESKARIOL ZUTA | 1 | `sjeme` |
| SJEME ENDIVIJA KOPICA | 1 | `sjeme` |

</details>

<a id="spinat"></a>
## špinat (`spinat`)

jedinica: **kg** · loose_produce: **true** · grupa: **112** · isključenih grupa: **13**

sinonimi: spinat, blitva  
must_match: `spinat | blitv`
  
atributi: oblik = smrznuti, baby

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850116053288 | ŠPINAT BRIKET DS 650G LEDO | 650 g | 18 | 692 | 3,43–7,37 /kg | high/name | oblik=smrznuti |
| 2 | 3850116053042 | BLITVA BRIKET 650 g (10) LEDO | 650 g | 18 | 636 | 4,49–7,37 /kg | high/name | oblik=smrznuti |
| 3 | 3850116804590 | BLITVA LIST BRIKET 2.5 kg UGOSTITELJSKI LEDO | 10 kg | 8 | 141 | 2,08–3,42 /kg ⚠122 | high/name | oblik=smrznuti |
| 4 | 5412532129053 | BLITVA LIST 4*2,5 kg FLANDERS BEST ZMH HORVAT | 2,5 kg | 6 | 26 | 1,66–2,76 /kg ⚠6 | high/name | oblik=smrznuti |
| 5 | 3850116850702 | ŠPINAT BRIKET FINO SJECKANI 2.5 KG LEDO | 2,5 kg | 5 | 153 | 1,60–3,49 /kg | high/ean | oblik=smrznuti |
| 6 | 3850116818726 | ŠPINAT LIST BRIKET 2,5 kg LEDO | 2,5 kg | 4 | 35 | 2,28–3,72 /kg | high/name | oblik=smrznuti |
| 7 | 5411361199701 | BLITVA PORCIJE 2,5kg ARDO CAK | 2,5 kg | 3 | 91 | 1,56–2,60 /kg | high/name |  |
| 8 | 3850116880549 | BLITVA BRIKETI 750 g LEDO | 750 g | 3 | 8 | 3,56–4,07 /kg | high/name | oblik=smrznuti |
| 9 | 5411683230441 | ŠPINAT LIST SMRZ. 2,5 kg DELTA | 2,5 kg | 2 | 36 | 1,56–2,00 /kg | high/name | oblik=smrznuti |
| 10 | 3850116037523 | ŠPINAT FINO SJEC.BRIKET 2,5 kg | 2,5 kg | 2 | 21 | 1,94–2,12 /kg ⚠1 | high/name | oblik=smrznuti |
| 11 | 3850116814773 | ŠPINAT BRIKETI 750 g LEDO | 750 g | 2 | 11 | 2,83–3,63 /kg | high/name | oblik=smrznuti |
| 12 | 5412532870054 | ŠPINAT SJECKANI SMRZ 2,5KG (4) | 2,5 kg | 2 | 10 | 1,65–1,96 /kg | high/name | oblik=smrznuti |
| 13 | 3858891042480 | ŠPINAT SJEĆENI 2,5KG FROZY | 2,5 kg | 2 | 3 | 2,30–2,50 /kg | high/name |  |
| 14 | 5412532900058 | ŠPINAT 2,5KG MLJEV. | 2,5 kg | 2 | 2 | 1,30–2,12 /kg | high/name |  |
| 15 | 3858887470228 | BLITVA PORCIJE 2,5KG FLANDERS BEST | 2,5 kg | 2 | 2 | 2,00–2,12 /kg | high/name |  |
| 16 | 3850334385925 | BLITVA VEZANA KOM |  | 1 | 187 | 2,58–4,78 /kg | low/unit_price |  |
| 17 | 8015021000108 | SPINAT 500 G | 500 g | 1 | 155 | 3,98 /kg | high/name |  |
| 18 | 3858893251552 | Blitva rfs |  | 1 | 144 | 2,99 /kg | low/unit_price |  |
| 19 | 3859894356017 | BLITVA VH 500 g | 500 g | 1 | 144 | 3,98 /kg | high/name |  |
| 20 | 3859893446306 | BLITVA VEZICA |  | 1 | 127 | – | – |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| BUREK ŠPINAT I SIR 190G DS PEKAR TOMO | 1 | `burek` |
| BUREK ŠPINAT I SIR peč PT | 1 | `burek` |
| PALACINKE SPINAT FETA SIR 2 X 90 G GASTRO PLODINE | 1 | `sir\b` |
| ROLICA ŠPINAT RICOTTA I FETA SIR 100g | 1 | `sir\b` |
| SAVIJAČA ŠPINAT 600 g MINUTE | 1 | `savijac` |
| SAVIJAČA-ŠPINAT/FETA SIR 125g WOLF | 1 | `savijac` |
| SJEME BLITVA SREB. 25g SJEMENARNA | 1 | `sjeme\b` |
| SJEME BLITVA SREBRNOLISNA | 1 | `sjeme\b` |
| SJEME BLITVA TAMNOZELENA | 1 | `sjeme\b` |
| SJEME SPINAT MATADOR | 1 | `sjeme\b` |

</details>

<a id="persin"></a>
## peršin (`persin`)

jedinica: **kom** · loose_produce: **true** · grupa: **65** · isključenih grupa: **3**

sinonimi: persin  
must_match: `persin`
  
atributi: dio = korijen, list

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3870547029850 | PERŠIN BERLINSKI POLUDUGI STANDARD |  | 2 | 10 | – | – | dio=korijen |
| 2 | 3870547029867 | PERŠIN LISNATI - DOMAĆI LIŠČAR - STANDARD vrećica |  | 2 | 7 | – | – | dio=list |
| 3 | 3859891136254 | PERSIN KORJEN LIST KOM CCA. 250 G |  | 1 | 155 | – | – | dio=list |
| 4 | gavranovic:072047 | PERŠIN LIST |  | 1 | 118 | – /kg | low/unit_price | dio=list |
| 5 | lidl:0082766 | Peršin korijen list 250g | 250 g | 1 | 116 | – /kg | high/name | dio=korijen |
| 6 | lidl:0083435 | Peršin list 50g | 50 g | 1 | 116 | – /kg | high/name | dio=list |
| 7 | 8058056197740 | PERSIN LIST 500G. | 500 g | 1 | 94 | – /kg | high/name | dio=list |
| 8 | 3856028690184 | PERŠIN SVJEŽI ZB BIO ZONE |  | 1 | 60 | – | – |  |
| 9 | ribola:0112331 | PERŠIN LIST PAK100 g | 100 g | 1 | 59 | – /kg | high/name | dio=list |
| 10 | 3859891689187 | Peršin korijen 500g | 500 g | 1 | 52 | – /kg | high/name | dio=korijen |
| 11 | 3859891904297 | Peršin list rfs |  | 1 | 48 | – /kg | low/unit_price | dio=list |
| 12 | 3859892705282 | BIO PERŠIN FRANCUSKI U TEGLAMA |  | 1 | 43 | – | – |  |
| 13 | 8001553803041 | PERŠIN |  | 1 | 43 | – | – |  |
| 14 | 8057960790252 | PERSIN LIST |  | 1 | 37 | – /kg | low/unit_price | dio=list |
| 15 | ktc:166138 | PERŠIN LIST PAK.50g | 50 g | 1 | 25 | – /kg | high/name | dio=list |
| 16 | ktc:614345 | PERŠIN KORIJEN 300g | 300 g | 1 | 22 | – /kg | high/name | dio=korijen |
| 17 | 3857500129833 | PERŠIN KOR LIS 250 gVOĆARNA STUDENAC |  | 1 | 20 | – | – |  |
| 18 | ktc:00149 | PERŠIN KORJEN+LIST |  | 1 | 20 | – /kg | low/unit_price | dio=list |
| 19 | tommy:10007271 | PERŠIN LIST |  | 1 | 13 | – /kg | low/unit_price | dio=list |
| 20 | ktc:614367 | PERŠIN KORIJEN LIST 300g | 300 g | 1 | 11 | – /kg | high/name | dio=korijen |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| SJEME PERSIN GIGANTE | 1 | `sjeme` |
| SJEME PERSIN KORIJENAS | 1 | `sjeme` |
| SJEME PERSIN LISNATI | 1 | `sjeme` |

</details>

<a id="gljive"></a>
## gljive (šampinjoni) (`gljive`)

jedinica: **kg** · loose_produce: **true** · grupa: **113** · isključenih grupa: **10**

sinonimi: gljive, sampinjoni, bukovace  
must_match: `sampinjon | gljiv | bukovac`
  
atributi: oblik = konzerva, smrznuto, suho, svjeze, nepoznato; vrsta = sampinjoni, bukovace

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3859889614115 | ŠAMPINJONI 500G BEZ KORIJENA(PODLOŽAK) 1150 | 500 g | 7 | 115 | 3,98–6,58 /kg | high/name | vrsta=sampinjoni, oblik=nepoznato (zadano) |
| 2 | 3859889614108 | ŠAMPINJONI SVJ.1000 g FRIDRIH | 1 kg | 4 | 169 | 3,32–4,09 /kg | high/name | vrsta=sampinjoni, oblik=nepoznato (zadano) |
| 3 | 3850334013576 | GLJIVA ŠAMPINJON 500 grama (8) | 500 g | 3 | 198 | 2,82–4,98 /kg | high/name | vrsta=sampinjoni, oblik=nepoznato (zadano) |
| 4 | 3858891564739 | ŠAMPINJONI REZANI 800G ULTRA | 800 g | 3 | 52 | 2,86–3,98 /kg | high/name | vrsta=sampinjoni, oblik=nepoznato (zadano) |
| 5 | 8594012792326 | ŠAMPINJONI GIANA REZANI 800 g | 800 g | 3 | 26 | 3,24–5,24 /kg | high/name | vrsta=sampinjoni, oblik=nepoznato (zadano) |
| 6 | 4007415005688 | ŠAMPINJONI REZANI U SL.OTOP.800 g AIPK | 800 g | 3 | 12 | 1,16–3,74 /kg | high/name | vrsta=sampinjoni, oblik=nepoznato (zadano) |
| 7 | 3859889614252 | ŠAMPINJONI RFS FRIDRIH |  | 2 | 149 | 2,99–3,95 /kg | low/unit_price | vrsta=sampinjoni, oblik=svjeze |
| 8 | 3859889267007 | ŠAMPINJONI VH 500 g | 500 g | 2 | 145 | 3,78–4,48 /kg | high/name | vrsta=sampinjoni, oblik=nepoznato (zadano) |
| 9 | 3859892060176 | ŠAMPINJONI MIX 500G GEA | 500 g | 2 | 145 | 4,58–4,98 /kg | high/name | vrsta=sampinjoni, oblik=nepoznato (zadano) |
| 10 | 8710609361427 | ŠAMPINJONI REZ. 2,55 kg LIMBUR | 2,55 kg | 2 | 48 | 2,69–3,25 /kg | high/name | vrsta=sampinjoni, oblik=konzerva |
| 11 | 3859889614719 | BUKOVAČE PAK.500g FRIDRIH | 500 g | 2 | 16 | 4,98–5,90 /kg | high/name | vrsta=bukovace, oblik=nepoznato (zadano) |
| 12 | 3859891246014 | GLJIVE SVJ.500 g ZKM | 500 g | 2 | 3 | 4,80–5,28 /kg | high/name | vrsta=sampinjoni, oblik=nepoznato (zadano) |
| 13 | 8032484130135 | ŠAMPINJONI PAKIRANI.500g | 500 g | 2 | 2 | 3,68–4,78 /kg | high/name | vrsta=sampinjoni, oblik=nepoznato (zadano) |
| 14 | 3859891581016 | ŠAMPINJONI 500 g | 500 g | 1 | 343 | 4,18–4,38 /kg | high/name | vrsta=sampinjoni, oblik=nepoznato (zadano) |
| 15 | 5907700040082 | SAMPINJONI 500 G BIJELI | 500 g | 1 | 155 | 3,78 /kg | high/name | vrsta=sampinjoni, oblik=nepoznato (zadano) |
| 16 | 3858893060048 | SAMPINJONI SMEDJI 500 G | 500 g | 1 | 144 | 4,38–4,78 /kg | high/name | vrsta=sampinjoni, oblik=nepoznato (zadano) |
| 17 | 3856021233296 | BUKOVAČA VH 500 g. | 500 g | 1 | 144 | 4,98 /kg | high/name | vrsta=bukovace, oblik=nepoznato (zadano) |
| 18 | 3859890284239 | ŠAMPINJONI 1 kg | 1 kg | 1 | 142 | 3,49 /kg | high/name | vrsta=sampinjoni, oblik=nepoznato (zadano) |
| 19 | 3859892060053 | BUKOVACE 500 G | 500 g | 1 | 125 | 4,58–5,38 /kg | high/name | vrsta=bukovace, oblik=nepoznato (zadano) |
| 20 | gavranovic:072057 | ŠAMPINJONI |  | 1 | 119 | 4,49–5,49 /kg | low/unit_price | vrsta=sampinjoni, oblik=nepoznato (zadano) |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| ŠAMPINJONI REZANI 2.55 kg (1) POD.OC.MASA 1330 g | 7 | `masa\b` |
| MJEŠAVINA GLJIVA SA VRGANJIMA MODIMA 2,5 KG | 5 | `mjesav` |
| MJEŠAVINA GLJIVA SMRZ INTER ALFA 2,5kg (4) | 3 | `mjesav` |
| MJEŠAVINA GLJIVA UG LEDO 2.5kg (4) | 2 | `ledo` |
| Rezani šampinjoni 530 g staklo | 2 | `staklo` |
| GLJIVE MJEŠAVINA SPAR 750 g | 1 | `mjesav` |
| GLJIVE ŠUMSKE MJEŠAVINA SMRZ 2,5kg(3) | 1 | `mjesav` |
| JUHA GLJIVE, 1 kg, PODRAVKA | 1 | `juha` |
| Mješavina gljiva SK1 | 1 | `mjesav` |
| ŠAMPINJONI 850G LIM | 1 | `lim\b` |

</details>

<a id="riza"></a>
## riža (`riza`)

jedinica: **kg** · loose_produce: **false** · grupa: **456** · isključenih grupa: **262** · pakiranje: **250–5000** · zadano bez: **vrsta=integralna**

sinonimi: riza  
must_match: `riza\b | rize\b | rizi\b | riso\b | rice\b`
  
atributi: vrsta = basmati, jasmin, arborio, carnaroli, originario, parboiled, integralna, dugo_zrno

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 8001860100017 | Riso Scotti riža originario okr.zrno 1kg | 1 kg | 21 | 1152 | 2,25–5,40 /kg | high/name | vrsta=originario |
| 2 | 3838700540291 | RIŽA ZA DOMAĆA JELA ZLATO POLJE PODRAVKA 1 kg (12) | 1 kg | 19 | 919 | 2,07–4,39 /kg | high/name | vrsta=originario |
| 3 | 3838700540369 | RIŽA ZLATO POLJE BLAZINICA PODRAVKA 800 g (9) | 800 g | 17 | 547 | 1,25–4,00 /kg | high/name |  |
| 4 | 8001860201011 | Riso Scotti riža arborio dugo zrno 1kg | 1 kg | 16 | 961 | 2,95–5,99 /kg | high/name | vrsta=arborio |
| 5 | 8001860190520 | Riso Scotti riža oro dugog zrna 1kg | 1 kg | 16 | 802 | 2,25–4,79 /kg | high/name | vrsta=parboiled |
| 6 | 3838700540314 | RIŽA BIJELA 800 g VREĆICA ZLATO POLJE | 800 g | 16 | 747 | 1,94–4,19 /kg | high/name | vrsta=dugo_zrno |
| 7 | 3838700540482 | RIŽA ZL POLJE ST ANDREA 500G KUT (18) | 500 g | 15 | 545 | 3,90–6,78 /kg | high/name |  |
| 8 | 5410673007490 | RIZA PARABOILED DUGO ZRNO VRECICA 500 G BENS ORIGINAL | 500 g | 13 | 658 | 6,70–8,98 /kg | high/name | vrsta=dugo_zrno |
| 9 | 3838700540406 | RIŽA ZL POLJE ST ANDREA 1KG KUT VAK (12) | 1 kg | 13 | 576 | 2,36–5,55 /kg | high/name |  |
| 10 | 3838700540604 | RIŽA ARBORIO VAKUMIRANA 1000 g PODRA | 1 kg | 13 | 489 | 2,36–6,99 /kg | high/name | vrsta=arborio |
| 11 | 3838700540413 | RIŽA ZL POLJE ZA DOM JELA 1KG KUT VAK (12) | 1 kg | 12 | 514 | 2,39–4,49 /kg | high/name |  |
| 12 | 5410673007476 | RIZA DUGO ZRNO PARBOILED 500 G BENS ORIGINAL | 500 g | 12 | 464 | 5,52–9,18 /kg | high/name | vrsta=parboiled |
| 13 | 3858889360954 | RIŽA NATUREL 1kg KUTIJA za domaća jela | 1 kg | 12 | 410 | 2,39–5,76 /kg | high/name |  |
| 14 | 8001420001594 | RIŽA GALLO ORIGINARIO 1KG -12/1- 1151 | 1 kg | 11 | 611 | 3,19–5,29 /kg | high/name | vrsta=originario |
| 15 | 3838700540383 | RIŽA PARBOILED DZ ZLATO POLJE 800G (12) | 800 g | 11 | 579 | 2,61–4,90 /kg | high/name | vrsta=parboiled |
| 16 | 3859888279445 | RIZA RIO PAK DUGO ZRNO 1 KG PVC | 1 kg | 11 | 463 | 1,19–2,29 /kg ⚠4 | high/name | vrsta=dugo_zrno |
| 17 | 3858889360978 | RIŽA NATUREL ZA DOM. JELA 1 kg SAM. VREĆICA AWT | 1 kg | 11 | 412 | 1,85–4,51 /kg | high/name |  |
| 18 | 5010338303273 | JAP SUSHI RIŽA 500G BLUE -10/1- DRAGON | 500 g | 11 | 262 | 3,00–10,90 /kg | high/name |  |
| 19 | 8001860010019 | RIŽA SCOTTI 1 kg CARNAROLI NKAS | 1 kg | 11 | 229 | 4,99–7,59 /kg ⚠4 | high/name | vrsta=carnaroli |
| 20 | 3859888163676 | RIŽA I KLASA 950 g ŠAFRAM (24) | 950 g | 11 | 121 | 2,09–3,15 /kg | high/name | vrsta=dugo_zrno |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| COKOLADA MLIJECNA COKOLADA RIZA 26 G DORINA | 17 | `cokolad` |
| KREKER OD RIZE SA SJEMENKAMA 100 G B.YOND-LIVITY | 13 | `kreker` |
| TJESTENINA OD RIŽE RICE VERMICELLI 250G YOUWOK | 13 | `tjestenin` |
| ČIPS OD RIŽE SIR CHEDDAR I CHUTNEY 60 g B. YOND LIVITY | 13 | `cips` |
| KREKER OD RIŽE SA SEZAMOM BEZ GLUTENA 100 g (12) | 12 | `kreker` |
| NAPITAK OD RIŽE ORIGINAL ALPRO 1 L ENCIAN | 12 | `napitak` |
| NATUREL KRE. BEZ GLU. RICE SNACK CLA. 100 g (12) | 12 | `snack` |
| ČIPS OD RIŽE VLASAC I KISELO VRHNJE 60 g B. YOND LIVITY | 12 | `cips` |
| MIKADO ČOKOLADA RIŽA 75G, (12)ZVEČEVO | 11 | `cokolad` |
| MISURA KEKSI KAKAO-RIŽA BEZ MLIJEK I JAJA 120G (12) | 11 | `mlijek` |

</details>

<a id="tjestenina"></a>
## tjestenina (`tjestenina`)

jedinica: **kg** · loose_produce: **false** · grupa: **1436** · isključenih grupa: **312** · pakiranje: **250–5000** · zadano bez: **vrsta=integralna, vrsta=bez_glutena**

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
| 9 | 8076802085912 | BARILLA PIPE RIGATE 91 (PUŽIĆ) TJESTENINA 500G | 500 g | 17 | 814 | 2,36–5,12 /kg | high/name | oblik=puzici |
| 10 | 8076809523721 | TJESTENINA TAGLIATELLE SA SPINATOM 500 G BARILLA KUTIJA | 500 g | 17 | 698 | 5,86–9,32 /kg | high/name | oblik=tagliatelle |
| 11 | 8076800195132 | TJESTENINA BAVETTE LINGUINE 13 500g BARILLA | 500 g | 17 | 649 | 2,18–4,98 /kg | high/name |  |
| 12 | 8076809580144 | BARILLA FARFALLE 65 (LEPTIRIĆI) TJESTENINA 500G (12) AWT | 500 g | 16 | 723 | 2,70–6,88 /kg | high/name | oblik=farfalle |
| 13 | 8076800105988 | TJESTENINA FUSILLI 98 1 KG BARILLA KUTIJA | 1 kg | 15 | 865 | 1,84–4,62 /kg | high/name | oblik=fusilli |
| 14 | 8076800105056 | TJESTENINA SPAGHETTI 5 1 KG BARILLA KUTIJA | 1 kg | 15 | 754 | 1,85–4,21 /kg | high/name | oblik=spageti |
| 15 | 8076800105032 | TJESTENINA SPAGHETTINI 3 1 KG BARILLA KUTIJA | 1 kg | 15 | 486 | 2,99–4,62 /kg | high/name | oblik=spageti |
| 16 | 3859893944352 | TAGLIATELLE VALJANA JAJ.TJES.400g MARODI | 400 g | 15 | 399 | 7,48–9,95 /kg | high/name | oblik=tagliatelle |
| 17 | 8076800105735 | TJESTENINA PENNE RIGATE 73 1 KG BARILLA KUTIJA | 1 kg | 14 | 779 | 1,85–4,62 /kg | high/name | oblik=penne |
| 18 | 8076809523714 | TJESTENINA TAGLIATELLE 500 G BARILLA KUTIJA | 500 g | 14 | 612 | 5,86–8,30 /kg | high/name | oblik=tagliatelle |
| 19 | 3859888666054 | TJEST MARODI CHIFFERINI RIGATI/ PUŽIĆI MALI 400G -12/1 | 400 g | 14 | 305 | 2,47–5,98 /kg | high/name | oblik=puzici |
| 20 | 8717228380174 | TJESTENINA OD RIŽE RICE VERMICELLI 250G YOUWOK | 250 g | 13 | 551 | 7,60–13,96 /kg | high/name | oblik=tagliatelle |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| BISTRA JUHA S TJEST.45G (16) (PAL 145) PODRAVKA | 18 | `juha` |
| TALIANETTA MAKARONI BOLOGNESE VR.160G (12) PODRAVKA | 18 | `tal?ianetta` |
| ARGETA SALATA PILETINA TJESTENINA 160 G ATLANTIC | 16 | `piletin` |
| TALIANETTA TJESTENINA SA 4 SIRA VR.145G (12) PODRAVKA | 15 | `tal?ianetta` |
| GOVEĐA JUHA S TJESTENINOM 65G (35) (PAL 108), PODRAVKA | 13 | `juha` |
| KOKOŠJA JUHA S TJESTENINOM 62G (35) (PAL 108), PODRAVKA | 13 | `juha` |
| FANT ŠPAGETE BOLOGNESE PODRAVKA 58 g (20) | 12 | `bolognese` |
| KAISER FRANZ JOSEF TUNA SALATA FUSILLI 160G(12) | 12 | `salata` |
| GOVEĐA JUHA S TJESTENINOM I MESOM 60G (16) (PAL 145), PODRAVKA | 9 | `juha` |
| KOKOŠJA JUHA S TJESTENINOM I MESOM 60G (16) (PAL 145), PODRAVKA | 9 | `juha` |

</details>

<a id="griz"></a>
## griz (`griz`)

jedinica: **kg** · loose_produce: **false** · grupa: **39** · isključenih grupa: **31** · pakiranje: **200–2000**

sinonimi: griz, psenicna krupica  
must_match: `griz\b | psenicna krupica`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3838700075106 | PŠENIČNA KRUPICA BEBE GRIZ 250G ZLATO POLJE | 250 g | 12 | 480 | 2,96–6,08 /kg | high/name |  |
| 2 | 3858884170015 | PŠENIČNA KRUPICA 1kg T-400 ČAKOVEC | 1 kg | 10 | 477 | 0,99–2,09 /kg | high/name |  |
| 3 | 3838700540086 | PŠENIČNA KRUPICA BEBE GRIZ 450G ZLATO POLJE | 450 g | 6 | 321 | 3,24–3,82 /kg | high/name |  |
| 4 | 3858894591725 | ULTRA PLUS PŠENIČNA KRUPICA 1KG (GRIS) | 1 kg | 6 | 75 | 0,99–1,10 /kg | high/name |  |
| 5 | 3858881327177 | N-PŠENIČNI GRIZ KLARA ZP 1KG -20/1- | 1 kg | 5 | 57 | 0,83–2,49 /kg | high/name |  |
| 6 | 3858881327184 | PŠENIČNA KRUPICA 500 g KLARA AA1070 | 500 g | 4 | 167 | 2,38–3,98 /kg | high/name |  |
| 7 | 3858891971896 | GRIZ PIR ORGANSKI NUTRIGOLD 500 g | 500 g | 4 | 66 | 4,50–6,34 /kg | high/name |  |
| 8 | 3858887101511 | GRIZ PŠENIČNI TENA 1 kg | 1 kg | 3 | 187 | 1,10–1,55 /kg | high/name |  |
| 9 | 3858891970813 | RIŽIN GRIZ NUTRIGOLD 1 kg (8) | 1 kg | 3 | 133 | 2,09–3,79 /kg | high/name |  |
| 10 | 3858893691426 | PŠENIČNA KRUPICA XXL 1kg ŠAFRAM | 1 kg | 3 | 44 | 0,85–1,49 /kg | high/name |  |
| 11 | 3858881504189 | GRIZ PŠENIČNI KARLA 1 kg | 1 kg | 2 | 175 | 1,06–1,19 /kg | high/name |  |
| 12 | 3859891976331 | GRIZ INTEGRALNI PIR EKO 500 G EKO-JAZO | 500 g | 2 | 86 | 3,30–6,38 /kg | high/name |  |
| 13 | 3856031211765 | PSENICNA KRUPICA GRIS 1 KG OHO! | 1 kg | 1 | 155 | 0,99 /kg | high/name |  |
| 14 | 3856018214383 | PSENICNA KRUPICA GRIS 1 KG PLODINE | 1 kg | 1 | 155 | 0,99 /kg | high/name |  |
| 15 | 3858891975429 | GRIZ PSENICNI INTEGRALNI BIO 500 G NUTRIGOLD | 500 g | 1 | 121 | 3,18 /kg | high/name |  |
| 16 | 4056489073642 | Pšenična krupica TIP 400, 1kg | 1 kg | 1 | 116 | 0,99 /kg | high/name |  |
| 17 | 3858887100866 | PŠENIČNA KRUPICA 1 kg BELJE | 1 kg | 1 | 87 | 1,09 /kg | high/name |  |
| 18 | 3859893165320 | KLC.NMNP.Pšenična krupica Gris 1kg_OC | 1 kg | 1 | 53 | 0,99 /kg | high/name |  |
| 19 | 3859890160427 | Farina pšenična krupica -gris 1 kg | 1 kg | 1 | 53 | 1,19 /kg | high/name |  |
| 20 | 3858881509818 | PŠENIČNA KRUPICA-GRIZ 1kg | 1 kg | 1 | 43 | 0,99 /kg | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| DESERT MLIJEČNI BELRISO GRIZ ČOKOLADA CIMET 130g | 8 | `desert` |
| DESERT MLIJEČNI BELRISO GRIZ JAGODA/ŠUMSKO VOĆE 130g | 7 | `desert` |
| Hipp bio kašica laku n.ban.griz kak.190g | 7 | `kasica` |
| N-PUDING DR. OETKER 400G GRIZ PROTEIN -6/1- | 5 | `puding` |
| PUDING GRIZ HIGH PROTEIN 65 G DR.OETKER | 5 | `puding` |
| Hipp bio kašica laku noć ban. griz 190g | 4 | `kasica` |
| Maggi Juha s mini griz okruglicama 34 g | 4 | `juha` |
| JUHA S GRIZ OKRUGLICAMA 47 G MAGGI | 3 | `juha` |
| HIPP BIO MK JABUKA/KRUŠ/GRIZ 190g | 2 | `hipp` |
| JUHA KNEDLICE 52 g MESNE/GRIZ PODRAVKA | 2 | `knedl` |

</details>

<a id="palenta"></a>
## palenta (kukuruzna krupica) (`palenta`)

jedinica: **kg** · loose_produce: **false** · grupa: **83** · isključenih grupa: **0** · pakiranje: **200–2000**

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
| 7 | 3838700540116 | PALENTA INSTANT VR. PODRAVKA 250 g | 250 g | 10 | 418 | 3,00–4,88 /kg | high/name |  |
| 8 | 3858884176048 | KUK. KRUPICA 450 G CAKOVECKI MLINOVI | 450 g | 9 | 274 | 1,89–4,42 /kg | high/name |  |
| 9 | 3858893691365 | PALENTA XXL BRZA PRIPREMA 1000 G (5) | 1 kg | 7 | 257 | 0,89–1,49 /kg | high/name |  |
| 10 | 3858891564517 | KUKURUZNA KRUPICA PALENTA 400G ULTRA PLUS | 400 g | 6 | 73 | 1,40–2,47 /kg | high/name |  |
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

jedinica: **kg** · loose_produce: **false** · grupa: **69** · isključenih grupa: **20** · pakiranje: **250–2000**

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
| KEKS PLAZMA WELLNESS 210g ZOBENE PAHULJICE | 4 | `keks` |
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

jedinica: **kg** · loose_produce: **false** · grupa: **109** · isključenih grupa: **19** · pakiranje: **200–2000**

sinonimi: krusne mrvice, prezle, mrvice  
must_match: `krusne mrvice | mrvice krusne | mrvice\b | prezle | panko`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3858881322011 | MRVICE KRUŠNE KLARA ZP 500G -42/1- | 500 g | 18 | 884 | 2,98–6,35 /kg | high/name |  |
| 2 | 3858881322059 | N-MRVICE KRUŠNE KLARA ZP 250G -60/1- | 250 g | 15 | 814 | 3,96–7,80 /kg | high/name |  |
| 3 | 3858881322233 | MRVICE KRUŠNE KLARA ZP 1KG-15/1- A51338 | 1 kg | 12 | 381 | 2,59–6,29 /kg | high/name |  |
| 4 | 5902898827163 | MRVICE PANKO ZA SUSHI 200G HOUSE OF ASIA | 200 g | 10 | 368 | 9,95–15,25 /kg ⚠275 | high/name |  |
| 5 | 3856016904644 | MRVICE KRUŠNE KLARA ZP XXL 600G -15/1 | 600 g | 9 | 409 | 3,75–4,98 /kg | high/name |  |
| 6 | 8715035809703 | N-PANKO MRVICE KIKKOMAN 227G SITNE -12/1- | 227 g | 7 | 164 | 10,44–14,93 /kg ⚠97 | high/name |  |
| 7 | 5999568625037 | It`s Us krušne mrvice bez glutena 300g | 300 g | 6 | 97 | 14,97 /kg ⚠44 | high/name |  |
| 8 | 3858881324060 | N-MRVICE KRUŠNE ULTRA+ KLARA ZP 480G A51926 -42/1- | 480 g | 5 | 73 | 2,44–3,31 /kg | high/name |  |
| 9 | 3858881324039 | MRVICE KRUŠNE ULTRA+ KLARA ZP240G A51925 -60/1- | 240 g | 5 | 72 | 2,79–3,96 /kg | high/name |  |
| 10 | 3858884717487 | KRUŠNE MRVICE 500 g BABIĆ | 500 g | 4 | 191 | 3,50–5,00 /kg | high/name |  |
| 11 | 3858881121713 | KRUSNE MRVICE 500 G MLINAR | 500 g | 4 | 80 | 1,72–3,98 /kg | high/name |  |
| 12 | 3850104065149 | KRUšNE MRVICE 250g P ODRAVKA | 250 g | 4 | 29 | 2,32–3,48 /kg | high/name |  |
| 13 | 3850334343741 | KRUŠNE MRVICE RIAL 500g (20) | 500 g | 4 | 12 | 1,78–2,69 /kg | high/name |  |
| 14 | 3856003930953 | MRVICE KRUŠNE 500 g PANEA NTL | 500 g | 3 | 475 | 2,30–2,78 /kg | high/name |  |
| 15 | 3856003930946 | KRUŠNE MRVICE 200 g PANEA NTL | 200 g | 3 | 395 | 1,95–3,95 /kg | high/name |  |
| 16 | 3859892992033 | KRUSNE MRVICE SA SEZAMOM 500 G MOJ KRUH | 500 g | 3 | 298 | 2,26–3,30 /kg | high/name |  |
| 17 | 3859892992026 | KRUSNE MRVICE 500 G MOJ KRUH | 500 g | 3 | 281 | 1,96–3,58 /kg | high/name |  |
| 18 | 3858884717494 | KRUŠNE MRVICE 250 g BABIĆ | 250 g | 3 | 150 | 4,44–6,60 /kg | high/name |  |
| 19 | 3850135250057 | KRUSNE MRVICE 500 G PIK | 500 g | 3 | 116 | 1,72–3,98 /kg | high/name |  |
| 20 | 8008698004753 | KRUSNE MRVICE 300G BEZ GLUTENA DR SCHAER | 300 g | 3 | 95 | 9,97–11,63 /kg | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| DEKOR DR OETKER 80G -10/1- KAKAO MRVICE | 17 | `dekor` |
| DEKOR DR OETKER 80G ŠARENE MRVICE-10/1 | 17 | `dekor` |
| BOMBONI ŠARENE MRVICE 100 g | 6 | `saren` |
| DRAŽE ČOKOLADNE MRVICE 100 g KRAŠ (18) | 4 | `coko` |
| Bauckhof eko mrvice od kukuruza 200g | 2 | `kukuruz` |
| .KOZICE S PANKO MRVICAMA 200g | 1 | `kozic` |
| 720G KOTANYI ŠARENE ŠEĆ MRVICE | 1 | `saren` |
| 800G MC COKO MRVICE TAM GOC FO | 1 | `coko` |
| GASTRO NUGGETSI PILEĆI U PANKO PANADI | 1 | `nugget` |
| KLC. Čokoladne mrvice mliječ. čok. 400 g | 1 | `coko` |

</details>

<a id="kvasac"></a>
## kvasac (`kvasac`)

jedinica: **vrecica** · loose_produce: **false** · grupa: **60** · isključenih grupa: **1**

sinonimi: kvasac, germa  
must_match: `kvasac | kvas\b`
  
atributi: vrsta = suhi, svjezi

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3859889940085 | DI GO INSTANT SUHI PEKARSKI KVASAC 7 g | 7 g | 21 | 959 | 0,56–0,99 /vrecica | high/name | vrsta=suhi |
| 2 | 3850104266577 | DOLCELA INSTANT SUHI KVASAC 7 g 4+1 GRATIS, PODRAVKA | 35 g | 20 | 1079 | 0,31–0,63 /vrecica | high/name | vrsta=suhi |
| 3 | 3858887683444 | DI-GO pekarski svježi kvasac 42g | 42 g | 19 | 1354 | 0,11–1,09 /vrecica | high/name | vrsta=svjezi |
| 4 | 3850104266003 | KVASAC SUHI INSTANT 7g DOLCELA PODRAVKA | 7 g | 18 | 1145 | 0,39–0,79 /vrecica | high/name | vrsta=suhi |
| 5 | 3859889940153 | DI-GO INST. SUHI PEKARSKI KVASAC 7 g 4+1 GRAT (10) | 35 g | 17 | 858 | 0,12–0,78 /vrecica | high/name | vrsta=suhi |
| 6 | 4000521024444 | KVASAC DR OETKER 35G INSTANT 4+1 5*7G -50/1- | 35 g | 16 | 1011 | 0,25–0,55 /vrecica | high/name | vrsta=suhi |
| 7 | 4000521000349 | KVASAC SUHI INSTANT 7g DR.OETKER | 7 g | 15 | 1025 | 0,35–0,75 /vrecica ⚠155 | high/name | vrsta=suhi |
| 8 | 8690770323045 | KVASAC DR OETKER 100G INSTANT-30/1- | 100 g | 15 | 534 | 0,11–0,15 /vrecica ⚠446 | high/name | vrsta=suhi |
| 9 | 3850104266027 | KVASAC SUHI INSTANT 450G DOLCELA PODRAVKA | 450 g | 14 | 333 | – ⚠333 | – | vrsta=suhi |
| 10 | 3850104266034 | INSTANT SUHI KVASAC 100G (30),PODRAVKA | 100 g | 13 | 449 | 0,11 /vrecica ⚠446 | high/name | vrsta=suhi |
| 11 | 3859889940108 | 500G DI-GO KVASAC SUHI PEKARSKI | 500 g | 12 | 443 | 0,11–0,12 /vrecica ⚠311 | high/name | vrsta=suhi |
| 12 | 4003834000112 | KVASAC SVJEŽI 42G DR.OETKER -24/1- | 42 g | 11 | 477 | 0,39–0,59 /vrecica ⚠37 | high/name | vrsta=svjezi |
| 13 | 3859889940849 | KVASAC DI-GO INS.SUH.PEK.125 g | 125 g | 10 | 467 | 0,11–0,14 /vrecica ⚠129 | high/name | vrsta=suhi |
| 14 | 8690770323052 | KVASAC INSTANT 450 G DR OETKER | 450 g | 8 | 251 | – ⚠251 | – | vrsta=suhi |
| 15 | 3859889940832 | N-KVASAC DIGO 42G SVJEŽI -24/1-+-/PEKARSTVO | 42 g | 7 | 88 | 0,12–0,99 /vrecica | high/name | vrsta=svjezi |
| 16 | 3850114203142 | KVASAC SVJEŽI 50g(2*25g) DUOS | 50 g | 5 | 259 | 0,29–0,43 /vrecica | high/name | vrsta=svjezi |
| 17 | 8600947081913 | KVASAC ALEVA SUHI 10 g | 10 g | 4 | 53 | 0,18–0,34 /vrecica | high/name | vrsta=suhi |
| 18 | 8008698005828 | KVASAC SUHI BEZ GLUTENA 20 G DR.SCHAR | 20 g | 3 | 196 | 0,59–0,68 /vrecica | high/name | vrsta=suhi |
| 19 | 3859889940887 | DI-GO DOMAĆI SVJEŽI KVASAC 42 g (40) | 42 g | 3 | 20 | 0,65–0,99 /vrecica | high/name | vrsta=svjezi |
| 20 | 3858887680627 | KVASAC SVJEŽI DI GO 500 g (20) | 500 g | 3 | 12 | – ⚠12 | – | vrsta=svjezi |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| KAPSULE PIVSKI KVASAC 80/1 | 1 | `kapsul` |

</details>

<a id="prasak_za_pecivo"></a>
## prašak za pecivo (`prasak_za_pecivo`)

jedinica: **vrecica** · loose_produce: **false** · grupa: **48** · isključenih grupa: **0**

sinonimi: prasak za pecivo, praska za pecivo  
must_match: `prasak za pecivo | pr za pecivo | prasak pecivo | backpulver`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850104242175 | PRAŠAK ZA PECIVO DOLCELA 5+1 GRATIS 6X12g PODRAVKA | 72 g | 23 | 863 | 0,08–0,33 /vrecica | high/name |  |
| 2 | 3850104216770 | PRAŠAK ZA PECIVO 12G,(48) PODRAVKA (PAL 441) | 12 g | 18 | 1181 | 0,12–0,39 /vrecica | high/name |  |
| 3 | 5997381375498 | PRAŠAK ZA PECIVO DR OETKER 12G -50/1- | 12 g | 14 | 1033 | 0,16–0,30 /vrecica | high/name |  |
| 4 | 3850104219535 | PRAŠAK ZA PECIVO 1kg PODRAVKA (4) | 1 kg | 7 | 31 | 0,05–0,07 /vrecica ⚠1 | high/name |  |
| 5 | 3856020275501 | PRAŠAK ZA PECIVO PODR 72G 6-PACK -16/1- 6*12G | 72 g | 6 | 660 | 0,16–0,25 /vrecica | high/name |  |
| 6 | 5997381375511 | PRASAK ZA PECIVO 5+1 72 G DR.OETKER | 72 g | 6 | 416 | 0,08–0,19 /vrecica | high/name |  |
| 7 | 5997381375504 | PRAŠAK ZA PECIVO 12 g 5+1 GRATIS DR.OETKER | 72 g | 6 | 404 | 0,17–0,22 /vrecica | high/name |  |
| 8 | 3858891565514 | PRAŠAK ZA PECIVO 12G 5/1 60G ULTRA PLUS | 60 g | 5 | 72 | 0,07–0,24 /vrecica | high/name |  |
| 9 | 5997381317641 | PRAŠAK ZA PECIVO 5+1 GRATIS 72G (16)DR.OETKER | 72 g | 5 | 24 | 0,15–0,24 /vrecica | high/name |  |
| 10 | 3856003939703 | PRAŠAK ZA PECIVO (5 x 12g) 60g FINETA | 60 g | 4 | 477 | 0,07–0,14 /vrecica | high/name |  |
| 11 | 3856020254643 | DOLCELA PRAŠAK ZA PECIVO 12 g 10 pak (48) PODRAVKA | 120 g | 4 | 216 | 0,14–0,18 /vrecica | high/name |  |
| 12 | 3850334197665 | PRAŠAK ZA PECIVO 60g 5X12g SWEET CHEF (36) | 60 g | 3 | 184 | 0,07–0,11 /vrecica | high/name |  |
| 13 | 3856003939697 | PRAŠAK ZA PECIVO FINETA 12 g NTL | 12 g | 3 | 172 | 0,13–0,19 /vrecica | high/name |  |
| 14 | 3858881580138 | PRAŠAK ZA PECIVO 5x13g 65g | 65 g | 3 | 60 | 0,09–0,18 /vrecica | high/name |  |
| 15 | 3858881588196 | PRAŠAK ZA PECIVO 1 kg NADALINA | 1 kg | 3 | 23 | 0,06–0,12 /vrecica | high/name |  |
| 16 | 8606104332430 | PRAŠAK ZA PECIVO 5+1 GRATIS 60g | 60 g | 3 | 4 | 0,08–0,10 /vrecica | high/name |  |
| 17 | 38389719 | PRAŠAK ZA PECIVO 12 g PODRAVKA (48) | 12 g | 2 | 21 | 0,14–0,19 /vrecica | high/name |  |
| 18 | 5997381346870 | PRAŠAK ZA PECIVO 6+2GR 96G DR.OETKER | 96 g | 2 | 6 | 0,12–0,24 /vrecica | high/name |  |
| 19 | 5997381375528 | PRAŠAK ZA PECIVO 6X12g DR OETKER | 72 g | 1 | 184 | 0,17–0,18 /vrecica | high/name |  |
| 20 | 3856018261172 | PRASAK ZA PECIVO 5X12 G B B | 60 g | 1 | 155 | 0,10 /vrecica | high/name |  |

<a id="vanilin_secer"></a>
## vanilin šećer (`vanilin_secer`)

jedinica: **vrecica** · loose_produce: **false** · grupa: **70** · isključenih grupa: **20**

sinonimi: vanilin secer, vanilin  
must_match: `vanilin secer | vanilinski secer | secer vanilin | vanilin\b`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3856020258726 | DOLCELA VANILIN ŠEĆER 8 g 5+1 GRATIS PODRAVKA (44) | 48 g | 21 | 858 | 0,08–0,33 /vrecica | high/name |  |
| 2 | 3856020258511 | DOLCELA VANILIN ŠEĆER 8 g PODRAVKA (44) | 8 g | 20 | 1202 | 0,12–0,39 /vrecica | high/name |  |
| 3 | 5997381375542 | VANILIN ŠEĆER DR OETKER 8G -50/1- | 8 g | 13 | 1014 | 0,15–0,30 /vrecica | high/name |  |
| 4 | 5997381337779 | VANILIN ŠEĆER BURBON 10G(50) DR.OETKER | 10 g | 13 | 640 | 0,29–0,55 /vrecica | high/name |  |
| 5 | 9001414410127 | ZAČIN VANILIN ŠEĆER BOURBON KOTANYI 20 g | 20 g | 11 | 261 | 0,19–0,48 /vrecica ⚠1 | high/name |  |
| 6 | 5997381375566 | Dr.Oetker vanilin šećer 6x8g 1 gratis | 48 g | 8 | 461 | 0,15–0,22 /vrecica | high/name |  |
| 7 | 5997381345750 | VANILIN ŠEČER BOURBON X3 30G (18) DR OETKER | 36 g | 8 | 257 | 0,24–0,42 /vrecica | high/name |  |
| 8 | 3850104242151 | VANILIN ŠEĆER 10 g 5+1 GRATIS 4F PODRAV | 60 g | 8 | 196 | 0,08–0,19 /vrecica | high/name |  |
| 9 | 3850104018886 | VANILIN ŠEĆER 1kg PODRAVKA (4) | 1 kg | 8 | 33 | 0,05–0,06 /vrecica ⚠30 | high/name |  |
| 10 | 3856020275532 | DOLCELA VANILIN ŠEĆER 8 g 6 PAK PODRAVKA (16) | 48 g | 7 | 656 | 0,16–0,25 /vrecica | high/name |  |
| 11 | 5997381375573 | Dr. Oetker vanilin šećer 10x8g 2 gratis | 80 g | 7 | 482 | 0,11–0,20 /vrecica | high/name |  |
| 12 | 3850104018862 | VANILIN ŠEĆER 10 g PODRAVKA (48) | 10 g | 6 | 192 | 0,10–0,23 /vrecica | high/name |  |
| 13 | 9001414502389 | KOTANYI BURBON,VANILIN ŠEĆER 10G VREĆICA | 10 g | 6 | 155 | 0,52–0,71 /vrecica ⚠122 | high/name |  |
| 14 | 3856020270742 | VANILIN ŠEĆER U PRAHU 100 g DOLCELA | 100 g | 6 | 73 | 0,06–0,11 /vrecica | high/name |  |
| 15 | 3858891565507 | VANILIN ŠEĆER 10G 5/1 50G ULTRA PLUS | 50 g | 6 | 71 | 0,06–0,19 /vrecica | high/name |  |
| 16 | 5997381375559 | VANILIN ŠEĆER 5+1 DR.OETKER 8 g | 48 g | 5 | 383 | 0,17–0,22 /vrecica | high/name |  |
| 17 | 3856020260767 | DOLCELA VANILIN ŠEĆER 8 g 10kom PODRAVKA | 80 g | 5 | 228 | 0,16–0,18 /vrecica ⚠3 | high/name |  |
| 18 | 9001414611791 | *NE*VANILIN AROMATIZIRANI ŠEĆER VREĆICA 70g | 70 g | 5 | 178 | 0,09–0,14 /vrecica | high/name |  |
| 19 | 3850334197696 | VANILIN ŠEĆER 50g 5X10g SWEET CHEF (36) | 50 g | 4 | 185 | 0,06–0,15 /vrecica | high/name |  |
| 20 | 5997381358279 | VANILIN ŠEĆER 40G XXL (25) DR.OETKER | 40 g | 4 | 46 | 0,06–0,17 /vrecica | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| KEKS LILLY VANILIN 220g KRAŠ (16) | 12 | `keks` |
| SLADILO SWEET ZERO VANILIN 8 g DR.OETKER | 9 | `sladil` |
| VANILIN KIFLICE 400G VOPEX | 5 | `kiflic` |
| KEKS LILLY VANILIN KRAŠ 220 g (16) | 4 | `keks` |
| MJEŠ ZA VANILIN KIFLICE 360 g OETKER | 2 | `kiflic` |
| PETRA VANILIN KIFLICE 220g | 2 | `kiflic` |
| PUDING VANILIN 1 kg DOLCELA | 2 | `puding` |
| DR g VANILIN KIFLICE 250g | 1 | `kiflic` |
| K PLUS VANILIN KIFLICE 300 g | 1 | `kiflic` |
| KEKSI VANILIN KIFLICE 300 g RADNI | 1 | `kiflic` |

</details>

<a id="kakao"></a>
## kakao (prah) (`kakao`)

jedinica: **kg** · loose_produce: **false** · grupa: **207** · isključenih grupa: **569** · pakiranje: **50–1000**

sinonimi: kakao, kakao prah  
must_match: `kakao\b`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3858881044012 | KAKAO PRAH KANDIT 100G -12/1- SMANJENE MASTI 16-18% | 100 g | 21 | 1058 | 16,60–30,80 /kg | high/name |  |
| 2 | 3850102110292 | KAKAO PRAH 100G (21), KRAŠ (PAL-90) | 100 g | 20 | 894 | 17,90–30,90 /kg | high/name |  |
| 3 | 5997381346917 | KAKAO DR OETKER ZA KOLAČE 70G-16/1- | 70 g | 14 | 561 | 19,00–38,71 /kg | high/name |  |
| 4 | 3858881773608 | KAKAO U PRAHU ANAMARIJA 100 g | 100 g | 9 | 569 | 9,30–30,50 /kg | high/name |  |
| 5 | 5310115008194 | TORTELA KAKAO 240G -12/1ULTRA+ | 240 g | 5 | 71 | 6,08–8,54 /kg | high/name |  |
| 6 | 3858891566221 | ULTRA KAKAO U PRAHU 100G ,ANAMARIJA | 100 g | 5 | 70 | 8,30–23,90 /kg | high/name |  |
| 7 | 8004333017058 | PRALINE KAKAO BOŽIĆ 200 g ROVELLI | 200 g | 3 | 267 | 14,95–17,45 /kg | high/name |  |
| 8 | 3838900033203 | KAKAO BENQUICK CHOCO BOX 400g | 400 g | 3 | 37 | 10,73–12,48 /kg | high/name |  |
| 9 | 3850334072450 | KAKAO LUMPI VREĆICA 350G (8) | 350 g | 2 | 179 | 6,03–7,29 /kg | high/name |  |
| 10 | 3850334055149 | KAKAO PRAH SWEET CHEF 250G (12) | 250 g | 2 | 119 | 17,32–21,16 /kg | high/name |  |
| 11 | 3856021228872 | SAVIJ.VAN.KAKAO S-BUDGET 500 g | 500 g | 2 | 80 | 4,58–5,18 /kg | high/name |  |
| 12 | 3858890134360 | EKO KAKAO U PR.200 g EKOZONA | 200 g | 2 | 51 | 26,25–38,45 /kg | high/name |  |
| 13 | 8004333017003 | PRALINE KAKAO BOŽIĆ 400 g ROVELLI | 400 g | 2 | 39 | 13,73–16,23 /kg | high/name |  |
| 14 | 8019980032743 | KRAFNE KAKAO BEZ GLUTENA 111 g | 111 g | 2 | 23 | 17,93–35,95 /kg | high/name |  |
| 15 | 3850102945085 | KAKAO PRAH 100 g KRAŠ (21) | 100 g | 2 | 20 | 14,90–24,30 /kg ⚠7 | high/name |  |
| 16 | 3850120601239 | MOTO KAKAO 192G (12) KRAŠ (PAL-100) | 192 g | 2 | 19 | 8,07–11,93 /kg | high/name |  |
| 17 | 3890000472580 | KAKAO TABLA ZA JELO I KUHANJE CRNA 250g CREMONTE | 250 g | 2 | 12 | 5,40–7,56 /kg | high/name |  |
| 18 | 3858891046815 | KNEDLE SA KAKAO KREMOM 1000G FROZY | 1 kg | 2 | 10 | 2,99–3,31 /kg | high/name |  |
| 19 | 3850120590298 | BRUNDO KAKAO 300 G (12) KRAŠ (PAL-24) | 300 g | 2 | 7 | 6,97–8,97 /kg | high/name |  |
| 20 | 4002575583731 | MINI JAJA MARCIPAN KAKAO 125 g | 125 g | 2 | 7 | 8,00–20,72 /kg | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| VAFEL KAKAO PRUTICI FRONDI 250 G KRAS | 23 | `vafel` |
| KEKS KAROLINA 288G MOTO KAKAO -18/1- | 20 | `keks` |
| PREKRAŠNI KOLAČIĆI KEKS KAKAO 220G (10) (PAL40) KRAŠ | 20 | `keks` |
| DORINA ČOKOLADICA KREM KAKAO 38 g (24) | 19 | `cokolad` |
| LEDOLETTA KAKAO KREM 800g | 19 | `krem\b` |
| DEKOR DR OETKER 80G -10/1- KAKAO MRVICE | 18 | `dekor` |
| N-KEKS KAROLINA 192G MOTO KAKAO -12/1- | 18 | `keks` |
| VAFEL KAKAO I MLIJEKO PRUTICI FRONDI 225 G KRAS | 18 | `vafel` |
| CROISSANT KAKAO 240G MULTIPACK 7 DAY'S CHIPITA | 17 | `croissant` |
| CROISSANT MIDI KAKAO 60g 7 DAY'S CHIPITA | 16 | `croissant` |

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
| 5 | 3877000595778 | ČOKOLADA ZA KUHANJE 300 g LA BOMBA | 300 g | 6 | 588 | 10,30–14,00 /kg | high/name |  |
| 6 | 8004735020861 | ČOK ZA KUHANJE TAMNA 50% 200g ZAINI | 200 g | 6 | 211 | 5,00–44,95 /kg ⚠1 | high/name |  |
| 7 | 3856003953419 | ČOKOLADA ZA KUHANJE 300 g (14) SMIJEŠAK | 300 g | 5 | 499 | 10,30–14,00 /kg | high/name |  |
| 8 | 3850102018857 | ČOKOLADA ZA KUHANJE RUM 200 g KRAŠ | 200 g | 5 | 240 | 14,95–24,95 /kg | high/name |  |
| 9 | 3850102018864 | ČOKOLADA ZA KUH. PREM. 200 g KRAŠ | 200 g | 5 | 238 | 14,95–24,95 /kg | high/name |  |
| 10 | 7613035587793 | COK. ZA KUH. MILK 170 G DESSERT NESTLE | 170 g | 4 | 218 | 19,76–34,41 /kg ⚠2 | high/name |  |
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

jedinica: **kg** · loose_produce: **false** · grupa: **235** · isključenih grupa: **123** · pakiranje: **250–3000**

sinonimi: pileca prsa, pileci file, piletina file  
must_match: `pilec prsa | pileca prsa | pileci file | pilec file | prsa pilec | file pilec | pileci filet | pil prsa | pil file`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850159110986 | N-VIN.PILEĆI FILE 500G -10/1- 11098 | 500 g | 17 | 954 | 9,98–15,78 /kg | high/name |  |
| 2 | 3858892724392 | PILEĆA PRSA 350 g JE LI GAVRILOVIĆ | 350 g | 9 | 310 | 8,11–13,40 /kg | high/name |  |
| 3 | 3850220115827 | PILEĆI FILE PERUTNINA 500g (6) | 500 g | 8 | 629 | 9,54–14,98 /kg | high/name |  |
| 4 | 3858892724316 | JELI PILEĆA PRSA 2600G,GAVRILOVIĆ | 2,6 kg | 7 | 217 | 3,84–10,50 /kg | high/name |  |
| 5 | 3850159110122 | PILECA PRSA BEZ KOZE PODLOZAK CEKIN 11012 |  | 6 | 391 | 6,49–9,95 /kg | low/unit_price |  |
| 6 | 3850159120329 | CEKIN PILEĆA PRSA U OVITKU, KOKA-VINDIJA | 1 kg | 5 | 134 | 9,89–11,69 /kg | high/ean |  |
| 7 | 3850159111327 | CEKIN PILEĆI FILE OD PRSIJU SMRZNUTO PODLOŽAK, KOKA |  | 5 | 24 | 11,38–15,99 /kg | low/unit_price |  |
| 8 | 3850159110580 | PILEĆI FILE OD PRSA OB PAK PODL KOKA |  | 4 | 312 | 10,59–14,19 /kg | low/unit_price |  |
| 9 | 3850159110313 | PILEĆI FILE OD PRSIJU SVJEŽE RFS, VINDIJA |  | 4 | 113 | 8,99–13,99 /kg | low/unit_price |  |
| 10 | 7894904055906 | SMRZNUTI PIL.FILE 2kg SEARA | 2 kg | 4 | 36 | 2,75–8,74 /kg | high/ean |  |
| 11 | 3850159110139 | PILEĆA PRSA SVJEŽA,KOKA RFZ |  | 3 | 108 | 5,99–8,99 /kg | low/unit_price |  |
| 12 | 3831006602717 | PILEĆI FILE 500 g NA PODLOŠKU DELAM | 500 g | 3 | 5 | 10,78–12,78 /kg | high/name |  |
| 13 | 3850220428491 | PILEĆI FILE MIX 600 g | 600 g | 2 | 133 | 8,32–8,98 /kg | high/name |  |
| 14 | 3850220114608 | PILEĆI FILE PERUTNINA RFZ (5) |  | 2 | 118 | 5,49–6,51 /kg | low/unit_price |  |
| 15 | 3850159118036 | PRSA PILEĆA K PLUS BEZ KOŽE |  | 1 | 187 | 4,69–7,49 /kg | low/unit_price |  |
| 16 | plodine:185801 | PILECI FILE RINFUZA |  | 1 | 143 | 7,39 /kg | low/unit_price |  |
| 17 | 3856021216923 | PILEĆI FILE S BUDGET |  | 1 | 143 | 7,39 /kg | low/unit_price |  |
| 18 | 93850220153464 | Pileća prsa PP |  | 1 | 140 | 14,19–14,49 /kg | low/unit_price |  |
| 19 | plodine:977808 | PILECI FILE I ZAPECENO MJESANO POVRCE PORCIJA |  | 1 | 125 | – | – |  |
| 20 | gavranovic:121976 | CEKIN PILEĆA PRSA BEZ KOŽE SVJEŽA PODLOŽAK (11012) |  | 1 | 124 | 9,29 /kg | low/unit_price |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| SALAMA PILEĆA PRSA U OVITKU 500 g VINDIJA | 17 | `salam` |
| PILEĆA PRSA 220 g POLI KIDS PERUTNINA | 14 | `kids` |
| N-VIN.PIL.FILE ZABATAK 500G (PODLOŽAK) | 13 | `zabatak` |
| SALAMA SLIM&FIT PILEĆA PRSA 400G | 11 | `salam` |
| DIMLJENA PILECA PRSA NAREZAK 100 G PERUTNINA | 8 | `narezak` |
| PRSA PILEĆA SLIM&FIT NARZAK 100 g PERUTNINA | 8 | `narzak` |
| DIMCEK DIMLJENA PILECA PRSA 250 G CEKIN (12203) VINDIJA | 7 | `dimcek` |
| PILEĆI FILE SVJEŽI MINI 400G CEKIN | 6 | `mini\b` |
| CHEF PIL FILE ZABATKA 400G CEKIN VINDIJA | 5 | `zabatk` |
| FILE PILECEG ZABATKA 500 G PERUTNINA | 5 | `zabatk` |

</details>

<a id="piletina"></a>
## piletina (cijelo pile, batak, zabatak, krila) (`piletina`)

jedinica: **kg** · loose_produce: **false** · grupa: **615** · isključenih grupa: **212**

sinonimi: piletina, pile, pileci batak, pileca krila, zabatak  
must_match: `pile\b | pilec batak | pileci batak | batak | zabatak | pilec krila | pileca krila | krilca | pileca zadnja | pilece meso | pilec zadnj`
  
atributi: dio = cijelo, batak, zabatak, krila

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850159111013 | CEKIN GRILL PILE SMRZNUTO, KOKA VINDIJA | 1 kg | 10 | 48 | 2,92–5,38 /kg | high/ean | dio=cijelo |
| 2 | 3850159112829 | PILE KOKA 1 kg SVJ.HRVATSKO | 1 kg | 9 | 428 | 3,18–3,32 /kg | high/ean | dio=cijelo |
| 3 | 3850220115773 | Međimursko pile - pileći batak 500g | 500 g | 7 | 635 | 3,98–6,98 /kg | high/name | dio=batak |
| 4 | 3850159110269 | PILECA KRILA PODLOZAK CEKIN (11026) |  | 7 | 344 | 5,49–7,89 /kg | low/unit_price | dio=krila |
| 5 | 3850159110054 | PILECI BATAK-ZABATAK PODLOZAK CEKIN (11005) | 1 kg | 7 | 317 | 4,79–6,89 /kg | high/ean | dio=batak |
| 6 | 3850159110085 | PILECI ZABATAK PODLOZAK CEKIN (11008) | 1 kg | 7 | 181 | 4,19–6,89 /kg | high/ean | dio=zabatak |
| 7 | 3850220115858 | PILEĆA KRILA 500 g SVJEŽA PERUTNINA | 500 g | 6 | 551 | 3,98–7,58 /kg | high/name | dio=krila |
| 8 | 3850159113123 | PILE ROSTER CEKIN (11312) |  | 6 | 363 | 3,18–3,98 /kg | low/unit_price | dio=cijelo |
| 9 | 3850159142345 | PILEĆA KRILCA NAVIJAČKI BUCKET 650 g | 650 g | 6 | 196 | 9,22–17,37 /kg | high/name | dio=krila |
| 10 | 3850159113130 | PILE KALIB.1000 g VINDIJA | 1 kg | 6 | 151 | 3,31–3,32 /kg | high/name | dio=cijelo |
| 11 | 3850159111051 | CEKIN PILEĆI BATAK I ZABATAK PODLOŽAK SMRZNUTO, KOKA-VINDIJA | 1 kg | 6 | 29 | 4,39–6,29 /kg | high/ean | dio=batak |
| 12 | 3850220115780 | Međimursko pile - pileći zabatak 500g | 500 g | 5 | 484 | 3,98–7,58 /kg | high/name | dio=zabatak |
| 13 | 3850159110597 | BATAK OBITELJSKO PAK IR.podl. |  | 5 | 261 | 4,19–6,19 /kg | low/unit_price | dio=batak |
| 14 | 3850159110511 | BATAK PILECI PODLOZAK CEKIN (11051) |  | 5 | 250 | 5,79–6,89 /kg | low/unit_price | dio=batak |
| 15 | 3850159150197 | ALABAMA BBQ PILECA KRILCA 450 G VINDIJA | 450 g | 5 | 158 | 4,87–11,76 /kg | high/name | dio=krila |
| 16 | 3850159111518 | BATAK KOKA 1 kg PIL.PODL.SM | 1 kg | 5 | 44 | 5,79–9,95 /kg | high/ean | dio=batak |
| 17 | 3850220111157 | PILE GRIL MEĐIMURSKO PODL PERUTNINA | 1 kg | 4 | 241 | 2,80–3,31 /kg | high/ean | dio=cijelo |
| 18 | 3850159113567 | PILEĆI BATAK ZABATAK OTKOŠTENI S KOŽOM |  | 4 | 185 | 7,69–9,59 /kg | low/unit_price | dio=batak |
| 19 | 3850159114557 | OTKOŠTENI BATAK/ZABATAK S KOŽOM RFS SVJ ,VINDIJA |  | 4 | 102 | 6,49–8,39 /kg | low/unit_price | dio=batak |
| 20 | 3850159111082 | CEKIN PILEĆI ZABATAK PODLOŽAK SMRZNUTO , KOKA | 1 kg | 4 | 27 | 5,39–6,05 /kg | high/name | dio=zabatak |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| KRILCA PILEĆA PEČENA SM 500 g CEKIN | 12 | `pecen` |
| N-VIN.PIL.BATAK I FILE ZABATKA (PODLOŽAK) | 5 | `file\b` |
| GAVELINO PILE ZA PECENJE CEKIN (11315) | 4 | `pecen` |
| PURECI BATAK MINI PAK VINDON (40400) | 4 | `mini\b` |
| PUREĆI BATAK OB.PAK PAK. VINDIJA kg | 4 | `purec` |
| 1KG KOTANYI ZAČIN PILEĆ KRILCA | 3 | `kotanyi` |
| PILECA MINI KRILCA 450 G PERUTNINA | 3 | `mini\b` |
| 1KG PIL.KRILCA ZAČ. SOUS VIDE | 2 | `zac\b` |
| BATAK ZABAT PIL BK MARINIR 400 g | 2 | `marinir` |
| CCA1,9 PUREĆI BATAK/ZABATAK VP | 2 | `purec` |

</details>

<a id="mljeveno_meso"></a>
## mljeveno meso (`mljeveno_meso`)

jedinica: **kg** · loose_produce: **false** · grupa: **106** · isključenih grupa: **0** · pakiranje: **300–2000** · zadano: **vrsta=mijesano**

sinonimi: mljeveno meso, mljeveno, mljeveno mesano meso  
must_match: `mljeveno meso | meso mljeveno | mljeveno mijesano | mljeveno junece | mljeveno svinjsko | mljeveno purece | mljeveno pilece | mljeveno telece | mljev meso`
  
atributi: vrsta = mijesano, junece, svinjsko, purece, pilece, telece

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850339413043 | PURECE MLJEVENO MESO 500 G VINDON (41304) | 500 g | 18 | 981 | 9,98–13,98 /kg | high/name | vrsta=purece |
| 2 | 3850139540642 | N-MLJEVENO MESO PIK 540G MIJEŠANO -4/1- MAP | 540 g | 8 | 484 | 7,57–12,20 /kg | high/name | vrsta=mijesano |
| 3 | 3850139540635 | PIK MLJEVENO MIJEŠANO MESO 540g | 540 g | 6 | 419 | 7,39–10,91 /kg | high/name | vrsta=mijesano |
| 4 | 3850139443448 | MIJEŠANO MLJEVENO MESO 850 g (MA) MP PIK | 850 g | 6 | 297 | 7,40–9,75 /kg | high/name | vrsta=mijesano |
| 5 | 3850139540598 | SVINJSKO MLJEVENO MESO 540g PIK | 540 g | 4 | 369 | 3,87–4,11 /kg | high/name | vrsta=svinjsko |
| 6 | 3850139435917 | MIJEŠ MLJEV MESO 850g MA PIK VRBOVEC (6) | 850 g | 4 | 320 | 4,69–10,46 /kg | high/name | vrsta=mijesano |
| 7 | 3850139446517 | MIJESANO MLJEVENO MESO E540 G LIGHT | 540 g | 2 | 265 | 11,09–11,65 /kg | high/name | vrsta=mijesano |
| 8 | 3858890183573 | MIJESANO MLJEVENO MESO E450 G MAP | 450 g | 2 | 159 | 6,64–9,98 /kg | high/name | vrsta=mijesano |
| 9 | 3858881612198 | MIJESANO MLJEVENO MESO E850 G MAP | 850 g | 2 | 157 | 7,05–8,58 /kg | high/name | vrsta=mijesano |
| 10 | 3850139415438 | JUN MLJEV MESO 850g MA PIK VRBOVEC | 850 g | 2 | 117 | 11,52–12,24 /kg | high/name | vrsta=mijesano (zadano) |
| 11 | 3859893068461 | MIJEŠANO MLJEVENO MESO 450 g | 450 g | 2 | 57 | 8,20–9,31 /kg | high/name | vrsta=mijesano |
| 12 | 3850139286281 | MIJEŠANO MLJEVENO MESO 1 KG | 1 kg | 2 | 14 | 6,29–7,49 /kg | high/name | vrsta=mijesano |
| 13 | 3850139280371 | MIJEŠANO MLJEVENO MESO 750 g K PLUS | 750 g | 1 | 182 | 5,85 /kg | high/name | vrsta=mijesano |
| 14 | 3856031235877 | MIJESANO MLJEVENO MESO E500 G | 500 g | 1 | 155 | 6,38 /kg | high/name | vrsta=mijesano |
| 15 | 3858891913209 | MIJESANO MLJEVENO MESO E540 G RAVLIC | 540 g | 1 | 150 | 7,39 /kg | high/name | vrsta=mijesano |
| 16 | 3850139521177 | MIJESANO MLJEVENO MESO E540 G+ 50 G GRATIS | 540 g | 1 | 148 | 5,89 /kg | high/name | vrsta=mijesano |
| 17 | 3858881619043 | MIJESANO MLJEVENO MESO E500 G MAP | 500 g | 1 | 148 | 7,96 /kg | high/name | vrsta=mijesano |
| 18 | 3859892369323 | MIJEŠANO MLJEVENO MESO 450 g | 450 g | 1 | 143 | 8,87 /kg | high/name | vrsta=mijesano |
| 19 | 3856021210303 | Miješano mljeveno meso |  | 1 | 140 | 10,29 /kg | low/unit_price | vrsta=mijesano |
| 20 | lidl:0004935 | Mljeveno miješano meso XXL, 1kg | 1 kg | 1 | 116 | 5,39–6,69 /kg | high/name | vrsta=mijesano |

<a id="svinjetina"></a>
## svinjetina (svježe meso) (`svinjetina`)

jedinica: **kg** · loose_produce: **false** · grupa: **454** · isključenih grupa: **87**

sinonimi: svinjetina, svinjsko meso, svinjski vrat, svinjski but, svinjska lopatica, svinjski kotlet  
must_match: `svinjetin | svinjski vrat | svinjski but | svinjska lopatic | svinjski kotlet | svinjsko meso | svinjski file | svinjska rebra | svinjski karee | svinjski lungic | sv vrat | sv but | sv lopatic | sv kotlet | sv karee`
  
require_any: `gulas | but\b | lopatic | ramstek | file | rebr | vrat | juh | prsa | kotlet | karee`
  
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
| 9 | 3858881612389 | CCA2,5KG SVINJSKI VRAT BK VP |  | 2 | 109 | 4,35–5,49 /kg | low/unit_price | dio=vrat |
| 10 | 3850139523010 | SVINJSKI BUT SK U KOŽI DALM.OBR PIK |  | 2 | 104 | 4,91–5,89 /kg | low/unit_price | dio=but |
| 11 | 3850139523003 | SVINJSKI BUT SK U KOŽI NEOB. RAV. R |  | 2 | 103 | 3,49–4,65 /kg | low/unit_price | dio=but |
| 12 | 3850139523423 | SVJEŽA SVINJSKA REBRA PIK VRBOVEC |  | 2 | 103 | 5,99–6,99 /kg | low/unit_price | dio=rebra |
| 13 | 3850139431469 | SV LOPATICA BK 4D UVOZ (VAK) |  | 2 | 16 | 4,38 /kg | low/unit_price | dio=lopatica |
| 14 | 3850139540918 | CCA0,5KG SVINJSKI FILE VP | 1 kg | 2 | 16 | 8,13–11,49 /kg ⚠8 | high/name | dio=file |
| 15 | 3850139436914 | SVINJSKI VRAT BEZ KOSTI PIK |  | 2 | 7 | – | – | dio=vrat |
| 16 | 3859893378447 | SVINJSKI BUT SK U KOŽI DALM.OBR MM |  | 2 | 5 | 4,04–4,91 /kg | low/unit_price | dio=but |
| 17 | 3850139540925 | SVINJSKI FILE VAC |  | 1 | 186 | 5,99–10,99 /kg | low/unit_price | dio=file |
| 18 | 3850139445770 | SV VRAT BK ODR 560g PIK | 560 g | 1 | 177 | 7,66 /kg | high/name | dio=vrat |
| 19 | 3850139442106 | SV.BUT BK ODREZAK E400 G MAP | 400 g | 1 | 148 | 7,93 /kg | high/name | dio=but |
| 20 | 3856021231254 | SVINJSKI FILE HR VP |  | 1 | 135 | 8,89 /kg | low/unit_price | dio=file |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| GOTOVA JELA AJINOMOTO RAMEN SVINJETINA 62G JUHA U ČAŠI | 5 | `juha` |
| RAMEN JUHA U ČAŠI SVINJETINA 62G,SALVIA | 2 | `juha` |
| SVINJSKO MESO ZA GULAŠ 400g PIVAC | 2 | `gulas` |
| CCA0 5KG SVINJETINA GULAŠ MAP | 1 | `gulas` |
| DIMLJENA SVINJSKA REBRA VAC | 1 | `dimljen` |
| DIMLJENI SV.VRAT BK U MREŽICI KUDELIĆ | 1 | `dimljen` |
| DIMLJENI SV.VRAT SLJEME BK 1/2 | 1 | `dimljen` |
| DIMLJENI SVINJSKI VRAT 1/1 PIVAC | 1 | `dimljen` |
| DIMLJENI SVINJSKI VRAT 1/1 VP GUSTI PIVAC | 1 | `dimljen` |
| DIMLJENI SVINJSKI VRAT 1/2 PIVAC | 1 | `dimljen` |

</details>

<a id="junetina"></a>
## junetina / govedina (svježe meso) (`junetina`)

jedinica: **kg** · loose_produce: **false** · grupa: **288** · isključenih grupa: **39**

sinonimi: junetina, govedina, junece meso, govede meso, junetina za gulas  
must_match: `junec | junetin | govedin | junec but | junec vrat | junec lopatic | junec gulas | junec ramstek | junec rebr | junec file | junec meso | goveda prsa | govede meso`
  
require_any: `gulas | but\b | lopatic | ramstek | file | rebr | vrat | juh | prsa`
  
atributi: dio = but, vrat, lopatica, gulas, file, rebra

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850139425635 | JUNECI FILEKI 600 G PIK VRBOVEC | 600 g | 5 | 145 | 11,05–17,15 /kg | high/name | dio=file |
| 2 | 3858881610309 | JUNEĆI BUT BK ODR 450 g PIVAC | 450 g | 3 | 163 | 17,76–23,88 /kg | high/name | dio=but |
| 3 | 8003449000268 | JUNEĆI FILEKI 1KG EURO ALFA | 1 kg | 3 | 6 | 7,19–7,89 /kg | high/name | dio=file |
| 4 | 3859894430052 | JUNEĆE GULAŠ KOCKE 400 g MAP | 400 g | 2 | 265 | 15,23–17,48 /kg | high/name | dio=gulas |
| 5 | 3858881617988 | JUNECI RAMSTEK E275 G | 275 g | 2 | 205 | 27,96 /kg | high/name | dio=file |
| 6 | 3850139401547 | Juneći vrat bez kosti |  | 2 | 196 | 12,99–13,99 /kg | low/unit_price | dio=vrat |
| 7 | 3858890182651 | PPK JUNEĆE MESO ZA GULAŠ 400 g | 400 g | 2 | 152 | 14,98–19,63 /kg | high/name | dio=gulas |
| 8 | 3850139411164 | JUNEĆA LOPATICA B.K. PIK |  | 2 | 109 | 13,49 /kg | low/unit_price | dio=lopatica |
| 9 | 3850139523119 | JUNEĆI VRAT BK RFZ |  | 2 | 108 | 6,99 /kg ⚠6 | low/unit_price | dio=vrat |
| 10 | 3850139456424 | JUNEĆE GULAŠ KOCKE PIK VRBOVEC kg |  | 2 | 9 | 19,49 /kg | low/unit_price | dio=gulas |
| 11 | 3856021210310 | Junetina za gulaš |  | 1 | 138 | 16,29 /kg | low/unit_price | dio=gulas |
| 12 | 3856021210327 | Juneća rebra |  | 1 | 136 | 12,79 /kg | low/unit_price | dio=rebra |
| 13 | 3856021210426 | Juneći but odrezak |  | 1 | 132 | 18,89 /kg | low/unit_price | dio=but |
| 14 | 3856021232343 | JUNEĆE GULAŠ KOCKE 400 g | 400 g | 1 | 128 | 13,48 /kg | high/name | dio=gulas |
| 15 | plodine:185126 | JUNECI FILEKI /TRIPICE/ |  | 1 | 127 | 5,90 /kg | low/unit_price | dio=file |
| 16 | 3856021210334 | Juneća prsa |  | 1 | 127 | 11,79 /kg | low/unit_price | dio=rebra |
| 17 | 3856031235976 | JUNECI BUT E450 G | 450 g | 1 | 126 | 18,87 /kg | high/name | dio=but |
| 18 | lidl:0001388 | Juneće meso za gulaš | 400 g | 1 | 116 | 17,48 /kg | high/unit | dio=gulas |
| 19 | 3859892958633 | Juneća rebra |  | 1 | 112 | 10,99 /kg | low/unit_price | dio=rebra |
| 20 | 3859893251306 | Juneći but bez kosti |  | 1 | 112 | 17,49 /kg | low/unit_price | dio=but |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| INSTANT JUHA S REZANCIMA GOVEDINA 5/1 375G INDOMIE | 6 | `instant` |
| JUHA S REZANCIMA OKUSA GOVEDINE 70g INDO MIE AWT | 6 | `juha` |
| INDOMIE INSTANT JUHA S REZANCIMA S OKUSOM GOVEDINA 10/1 750g | 5 | `instant` |
| JUHA INST. NOODLES GOVEDINA 4X70 gr NTL | 2 | `juha` |
| JUHA.INST.NOODLES GOVEDINA 70g NTL | 2 | `juha` |
| JUNECE KOSTI HRPTA I VRATA MM | 2 | `mm\b` |
| CCA 5KG JUNEĆI BUT BK VP SMRZ. | 1 | `cca\b` |
| CCA 5KG JUNEĆI VRAT BK VP | 1 | `cca\b` |
| INDOMIE JUHA S REZ.GOVEDINA 3U1 | 1 | `juha` |
| INST.JUHA S OKUSOM GOVEDINE 17 | 1 | `juha` |

</details>

<a id="slanina"></a>
## slanina / panceta (`slanina`)

jedinica: **kg** · loose_produce: **false** · grupa: **705** · isključenih grupa: **75**

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
| 8 | 3858889495113 | PANCETA DALMATINSKA REZANA 80G MAP (12) | 80 g | 9 | 412 | 27,38–46,13 /kg | high/name | oblik=narezana |
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
| 20 | 3850133816750 | PANCETA NAREZAK DOBRO 150 g | 150 g | 6 | 160 | 15,27–28,60 /kg | high/name | oblik=narezana |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| KREKERI SALTAS BACON 100G KOESTLIN | 19 | `kreker` |
| GRAH SA SLANINOM 400 G CARNEX ALCA | 18 | `grah` |
| GOTOVA JELA GRAH S DIMLJENOM SLANINOM 300G GAVRILOVIĆ | 17 | `grah` |
| KREKER TUC 100G BACON/ŠPEK -24/1- | 17 | `kreker` |
| N-ČIPS PRINGLES 165G BACON -19/1- | 8 | `cips` |
| CIPS POMSTICKS SLANINA 85 G LORENZ | 4 | `cips` |
| ČIPS HRUSK REBRASTI BACON 150 g VREĆICA NTL | 4 | `cips` |
| Pivac Roštilj kobasica sir i špek 360 g | 3 | `kobas` |
| SMOKI CHIO TACCOS BACON 65 g INTERSNACK | 3 | `smoki` |
| ALTROKE KOBASICA SVJEZA PANCETA I LUK 290G MAP PISINIUM | 2 | `kobas` |

</details>

<a id="sunka"></a>
## šunka (kuhana) (`sunka`)

jedinica: **kg** · loose_produce: **false** · grupa: **919** · isključenih grupa: **199**

sinonimi: sunka, kuhana sunka  
must_match: `sunka\b | sunke\b | sunk\b`
  
atributi: vrsta = kuhana, pileca, pureca, delikates; oblik = narezana

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850139360516 | ŠUNKA KUHANA NAR 125g MA PIK VRBOVEC (10) | 125 g | 22 | 1051 | 15,92–24,72 /kg | high/name | vrsta=kuhana, oblik=narezana |
| 2 | 3850139250671 | N-VRB ŠUNKA FINA 150G PIK NAREZAK -10/1 | 150 g | 22 | 970 | 16,60–27,27 /kg | high/name | oblik=narezana |
| 3 | 3850139171051 | SUNKA U OVITKU NAREZAK 125 G MA PIK VRBOVEC | 125 g | 20 | 994 | 11,92–24,72 /kg | high/name | oblik=narezana |
| 4 | 3850159128813 | PUREĆA DELUXE ŠUNKA CLASSIC 100 g VINDON 12881 | 100 g | 19 | 926 | 15,90–31,90 /kg | high/name | vrsta=pureca |
| 5 | 3850139173550 | ŠUNKA U OVITKU 350G PIK VRBOVEC (12) | 350 g | 19 | 793 | 9,97–16,71 /kg | high/name |  |
| 6 | 3858890209679 | N-GAV ŠUNKA MANDOLINA 340G-24/1 LIM GAVRILOVIĆ | 340 g | 19 | 688 | 13,21–24,09 /kg | high/name |  |
| 7 | 3858892721292 | ŠUNKA U OVITKU 350G GAVRILOVIĆ (6) | 350 g | 19 | 664 | 11,54–17,11 /kg | high/name |  |
| 8 | 3850139520453 | ŠUNKA PUREĆA DIMLJENA 100 g MA PIK VRBOVEC | 100 g | 18 | 902 | 12,90–35,90 /kg | high/name | vrsta=pureca, oblik=narezana |
| 9 | 3850139520316 | ŠUNKA PUREĆA CLASSIC 100 g MA PIK VRBOVEC | 100 g | 18 | 873 | 14,90–30,90 /kg | high/name | vrsta=pureca, oblik=narezana |
| 10 | 3850159123153 | N-VIN PILEĆA DE LUX ŠUNKA CLASSIC 100G -10/1- | 100 g | 17 | 862 | 18,50–27,90 /kg | high/name | vrsta=pileca |
| 11 | 3858881227927 | ŠUNKA NAREZAK LIM. GAVRILOVIĆ 150 g | 150 g | 17 | 806 | 11,27–18,60 /kg | high/name | oblik=narezana |
| 12 | 3850139350401 | PECENA SUNKA 125 G NAREZAK PIK VRBOVEC | 125 g | 16 | 771 | 17,52–30,32 /kg | high/name | oblik=narezana |
| 13 | 3850139171723 | N-VRB ŠUNKA PIK DELIKATES 150G NAREZAK -10/1 | 150 g | 16 | 620 | 13,73–24,60 /kg | high/name | vrsta=delikates, oblik=narezana |
| 14 | 3858890203295 | PURECA SUNKA STANCIJA NAREZAK 100 G GAVRILOVIC | 100 g | 14 | 580 | 6,90–30,90 /kg | high/name | vrsta=pureca, oblik=narezana |
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
| FANT ZAPECENA TJESTENINA SUNKA I SIR 40 G | 7 | `sir\b` |
| SENDVIČ PANE AMORE ŠUNKA SIR 130G (6) | 6 | `sendvic` |
| SALATA TJESTENINA ŠUNK STRIBOR 255 g | 5 | `salata` |
| KREKERI CROCO SUNKA 100 G | 4 | `kreker` |
| SENDVIČ ŠUNKA SIR PAK 215g MLINAR | 4 | `sendvic` |

</details>

<a id="tuna"></a>
## tuna (konzerva) (`tuna`)

jedinica: **kg** · loose_produce: **false** · grupa: **449** · isključenih grupa: **229** · pakiranje: **50–1000**

sinonimi: tuna, tunjevina  
must_match: `tuna\b | tune\b | tunj`
  
atributi: oblik = komadi, file, sjeckana; preljev = ulje, vlastiti_sok

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 8004030595033 | TUNA KOMADI NATURALE RIO MARE 160 g (OCIJEĐENA MASA 122 g) ORBICO | 160 g | 21 | 1225 | 10,94–40,75 /kg | high/name | preljev=vlastiti_sok, oblik=komadi |
| 2 | 3856020263096 | EVA TUNA FILETI U BILJNOM ULJU 100G (30) (PAL 161) | 100 g | 21 | 923 | 26,90–46,50 /kg | high/name | preljev=ulje, oblik=file |
| 3 | 8004030595002 | TUNA KOMADI U SUNCOKRET. ULJU RIO MARE 160 g (OCIJEĐENA NASA 122 g) ORBICO | 160 g | 20 | 1236 | 10,94–43,66 /kg | high/name | preljev=ulje, oblik=komadi |
| 4 | 3850104267031 | EVA TUNA KOMADIĆI USITNJ.160G/112G, (48) (PAL 54)PODRAVKA | 160 g | 20 | 798 | 9,06–17,81 /kg | high/name | preljev=ulje, oblik=komadi |
| 5 | 8594012796515 | TUNA ŽUTOPERAJNA ODREZ. U SUNC. ULJU 170g (OCJ. MASA 120g)GIANA | 170 g | 18 | 836 | 11,12–24,08 /kg | high/name | preljev=ulje, oblik=file |
| 6 | 8004030345775 | N-TUNA RIO MARE 3*80G (NETTO3*52G)U MAS.ULJU -6/1 | 240 g | 18 | 776 | 20,79–47,37 /kg ⚠1 | high/name | preljev=ulje |
| 7 | 8004030100213 | N-TUNA RIO MARE 2*80G(NETTO 2*52G)U MAS.ULJU-24/1 | 160 g | 16 | 719 | 17,44–52,79 /kg | high/name | preljev=ulje |
| 8 | 3856020263126 | EVA TUNA FILETI U MASLINOVOM ULJU 100G (30)(PAL690) PODRAVKA | 100 g | 16 | 454 | 15,00–44,90 /kg | high/name | preljev=ulje, oblik=file |
| 9 | 8004030044005 | RIB.K.TUNA 160 g ( 104 g) RIO MARE MASL.ULJE ORBI | 160 g | 16 | 444 | 19,88–41,25 /kg ⚠2 | high/name | preljev=ulje |
| 10 | 8595241527901 | TUNA ODREZAK U MASLINOVOM ULJU FRANZ JOSEF 150g-ocijeđ.mase 102g | 150 g | 15 | 795 | 14,60–28,33 /kg | high/name | preljev=ulje |
| 11 | 3856020278229 | TUNA STEAK KOMADI U BILJNOM ULJU 160g EVA PODRAVKA | 160 g | 14 | 750 | 8,44–28,06 /kg | high/name | preljev=ulje, oblik=komadi |
| 12 | 8004030005051 | N-TUNA RIO MARE ULJE 4*80G UMASLINOVOM ULJ(NETTO 4*52G) | 320 g | 14 | 749 | 15,59–34,34 /kg | high/name | preljev=ulje |
| 13 | 3850160108064 | TUNA FILET BILJNO ULJE 105 G ADRIATIC QUEEN SARDINA POSTIRA | 105 g | 14 | 690 | 36,10–77,41 /kg | high/name | preljev=ulje, oblik=file |
| 14 | 3856020263218 | EVA TUNA U UMAKU OD RAJČICE 100G (30)(PAL690) PODRAVKA | 100 g | 14 | 411 | 19,50–26,90 /kg | high/name |  |
| 15 | 80040248 | RIB.K.TUNA MASL.ULJE 80 g ( 0,052 g) RIO MARE ORBI | 80 g | 14 | 363 | 12,50–63,27 /kg | high/name | preljev=ulje |
| 16 | 3850104231506 | EVA TUNA KOMADI U ULJU 160G/112G (24) (PAL 117) PODRAVKA | 160 g | 14 | 336 | 10,62–27,81 /kg ⚠1 | high/name | preljev=ulje, oblik=komadi |
| 17 | 8004030344570 | N-TUNA RIO MARE NATURALE4*80G (NETTO 4*56G)-12/1 3503 | 320 g | 13 | 628 | 15,59–42,81 /kg | high/name | preljev=vlastiti_sok |
| 18 | 3850160108538 | TUNA FILET MASLINOVOM ULJE 105 G ADRIATIC QUEEN SARDINA POST | 105 g | 13 | 545 | 21,71–71,97 /kg | high/name | preljev=ulje, oblik=file |
| 19 | 8595241527857 | TUNA FRANZ JOSEF U SUNCOK.ULJU 4X80g - ocijeđ mase 4X52g | 320 g | 12 | 566 | 7,81–23,51 /kg | high/name | preljev=ulje |
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

jedinica: **kg** · loose_produce: **false** · grupa: **403** · isključenih grupa: **182** · pakiranje: **150–5000**

sinonimi: grah, grah zrno, crveni grah, bijeli grah  
must_match: `grah\b | graha\b | grah zrn`
  
atributi: vrsta = bijeli, crveni, sareni, smedi, crni; oblik = konzerva, smrznuto, svjeze, suho, nepoznato

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850104025389 | GRAH SMEĐI 800g LIM.PODRAVKA-ocijeđene mase 460g | 800 g | 23 | 1390 | 2,06–6,07 /kg | high/name | oblik=konzerva, vrsta=smedi |
| 2 | 3850104020780 | GRAH BIJELI 800 g LIM PODRAVKA OC MASA 460 g (12) | 800 g | 23 | 1014 | 1,95–5,63 /kg | high/name | oblik=konzerva, vrsta=bijeli |
| 3 | 3850104024870 | GRAH SMEĐI 400g LIM.PODRAVKA-ocijeđene mase 230g | 400 g | 22 | 1099 | 2,38–7,61 /kg | high/name | oblik=konzerva, vrsta=smedi |
| 4 | 3850104020759 | GRAH CRVENI 400g LIM PODRAVKA-OCIJEĐENA MASA 230g | 400 g | 21 | 882 | 2,38–8,65 /kg | high/name | oblik=konzerva, vrsta=crveni |
| 5 | 3850104020728 | GRAH CRVENI 800 g LIM PODRAVKA OC MASA 460 g (12) | 800 g | 20 | 767 | 2,74–6,50 /kg | high/name | oblik=konzerva, vrsta=crveni |
| 6 | 3850104020797 | GRAH BIJELI 400g LIM.PODRAVKA-OCIJEĐENA MASA 230g | 400 g | 19 | 855 | 2,23–7,61 /kg | high/name | oblik=konzerva, vrsta=bijeli |
| 7 | 3856015309679 | N-GRAH SMEĐI ZVIJEZDA 800G 480G ČVRSTE TVARI -12/1- | 800 g | 14 | 607 | 2,11–4,15 /kg | high/name | oblik=nepoznato (zadano), vrsta=smedi |
| 8 | 8595241511276 | GRAH ŠARENI 800 gr (OCJ. MASA 480 g) GIANA | 800 g | 12 | 653 | 1,13–4,15 /kg | high/name | oblik=nepoznato (zadano), vrsta=sareni |
| 9 | 3850104025396 | GRAH SMEĐI 2500 g OCJ.MASA 1450 g PODRAVKA | 2,5 kg | 11 | 42 | 2,11–4,27 /kg | high/name | oblik=konzerva, vrsta=smedi |
| 10 | 3859893124501 | GRAH ŠARENI 500G NATURA, MARJAN VOĆE | 500 g | 10 | 393 | 1,98–4,98 /kg | high/name | oblik=nepoznato (zadano), vrsta=sareni |
| 11 | 3856015309648 | N-GRAH SMEĐI ZVIJEZDA 400G 240G ČVRSTE TVARI -12/1- | 400 g | 10 | 329 | 1,85–5,79 /kg | high/name | oblik=nepoznato (zadano), vrsta=smedi |
| 12 | 3856020243432 | GRAH CRNI LIMENKA 400 g PODR | 400 g | 10 | 226 | 2,38–5,48 /kg | high/name | oblik=nepoznato (zadano), vrsta=crni |
| 13 | 3850104275654 | GRAH CRV 2500 g NETO OC MASA 1450 g PODRAVKA (6) | 2,5 kg | 10 | 28 | 2,38–3,40 /kg ⚠4 | high/name | oblik=konzerva, vrsta=crveni |
| 14 | 3083680009508 | N-GRAH BONDUELLE 400G CRVENI(NETTO 240G) -12/1 | 400 g | 9 | 379 | 4,22–8,96 /kg | high/name | oblik=nepoznato (zadano), vrsta=crveni |
| 15 | 3850104283536 | GRAH BIJELI KRUPNI 400 g (OCJ. MASA 230 g) PODRA | 400 g | 8 | 424 | 3,00–3,98 /kg | high/name | oblik=nepoznato (zadano), vrsta=bijeli |
| 16 | 3083680496117 | GRAH CRVENI 200/120g BONDUELLE | 200 g | 8 | 317 | 3,95–9,75 /kg | high/name | oblik=nepoznato (zadano), vrsta=crveni |
| 17 | 3859890236375 | GRAH ŠARENI 800G/480G, LARA(792) | 800 g | 7 | 58 | 1,86–3,31 /kg | high/name | oblik=nepoznato (zadano), vrsta=sareni |
| 18 | 3850104020766 | GRAH BIJELI LIM. 2.5 kg PODRAVKA OC. MASA 1450 g | 2,5 kg | 7 | 15 | 1,48–2,88 /kg | high/name | oblik=konzerva, vrsta=bijeli |
| 19 | 8594012794948 | GRAH SARENI 400 G GIANA LIMENKA | 400 g | 6 | 253 | 1,22–2,73 /kg | high/name | oblik=nepoznato (zadano), vrsta=sareni |
| 20 | 3858894141869 | GRAH ŠARENI E BUONO 800 g 12/1 | 800 g | 6 | 252 | 1,24–3,73 /kg | high/name | oblik=nepoznato (zadano), vrsta=sareni |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| GRAH S KOBASICOM 400G (15), (PAL 81)PODRAVKA | 22 | `kobasic` |
| GOT. JELO GRAH S KOBAS. CARNEX 400 g | 21 | `carnex` |
| GRAH S GAVRILOVIĆ KOBASICOM 300g GAVRILOVIĆ | 21 | `kobasic` |
| GRAH S HAMBURGEROM 400G (15) (PAL 81), PODRAVKA | 21 | `hamburger` |
| FANT ZA GRAH I VARIVA 60G (20) (PAL 145) PODRAVKA | 20 | `variva` |
| GOT. JELO GRAH SA SLAN. CARNEX 400 g | 20 | `carnex` |
| GOTOVA JELA GRAH S DIMLJENOM SLANINOM 300G GAVRILOVIĆ | 20 | `slanin` |
| GRAH CRVENI I KUKUR. U MEKSIČ.UMAKU 430g BONDUELE - ocijeđena masa 200g | 16 | `umak` |
| TUNA SALATA GRAH BOWL 160G INSALATISSIME RIO MARE | 16 | `salata` |
| N-GRAH S DIMLJENIM SV.REBRIMA BK 300G GAVRILOVIĆ -16/1 | 14 | `gavrilovic` |

</details>

<a id="leca"></a>
## leća (`leca`)

jedinica: **kg** · loose_produce: **false** · grupa: **137** · isključenih grupa: **139** · pakiranje: **150–5000**

sinonimi: leca, lece  
must_match: `leca\b | lece\b | leca zelena | leca crvena`
  
atributi: vrsta = zelena, crvena, crna, smeda; oblik = konzerva, smrznuto, svjeze, suho, nepoznato

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850104272356 | LEĆA LIM 400 g NETO OC.MASA 240 g (12) PODRAVKA | 400 g | 18 | 489 | 2,97–8,71 /kg | high/name | oblik=konzerva |
| 2 | 3859891427307 | LEĆA ZELENA 500G NATURA MARJAN VOĆE | 500 g | 11 | 372 | 3,10–4,72 /kg | high/name | oblik=nepoznato (zadano), vrsta=zelena |
| 3 | 3859890587019 | LEĆA CRVENA 500G NATURA MARJAN VOĆE | 500 g | 11 | 329 | 2,78–4,98 /kg | high/name | oblik=nepoznato (zadano), vrsta=crvena |
| 4 | 3859891427611 | LECA ZELENA RINF. |  | 6 | 101 | 2,04–3,49 /kg | low/unit_price | oblik=nepoznato (zadano), vrsta=zelena |
| 5 | 8003716003053 | LEĆA 240 g LIM. STRAINESSE VM2 | 400 g | 6 | 41 | 2,65–5,46 /kg | high/name | oblik=nepoznato (zadano) |
| 6 | 3859890630777 | LEĆA ZELENA VEDRINI 500 g | 500 g | 4 | 232 | 2,04–3,78 /kg | high/name | oblik=nepoznato (zadano), vrsta=zelena |
| 7 | 3859890630807 | LEĆA CRVENA 500 g PRIMORAC D.O.O. | 500 g | 4 | 193 | 1,96–3,18 /kg | high/name | oblik=nepoznato (zadano), vrsta=crvena |
| 8 | 3858882920353 | LEĆA SMEĐA 500g PRIMAVITA ADVENT | 500 g | 4 | 163 | 2,78–5,18 /kg | high/name | oblik=nepoznato (zadano), vrsta=smeda |
| 9 | 3859891427604 | LECA CRVENA RFZ |  | 4 | 78 | 1,52–2,79 /kg | low/unit_price | oblik=suho, vrsta=crvena |
| 10 | 3872084000644 | LEĆA ZELENA 500 g EUROCOMPANY | 500 g | 4 | 71 | 3,38–4,30 /kg | high/name | oblik=nepoznato (zadano), vrsta=zelena |
| 11 | 3872084001061 | LEĆA CRVENA 500 g EUROCOMPANY | 500 g | 3 | 230 | 2,50–4,50 /kg | high/name | oblik=nepoznato (zadano), vrsta=crvena |
| 12 | 3858886175513 | EKO BIO LEĆA 500 g CRVENA BIOVEGA | 500 g | 3 | 191 | 3,58–5,70 /kg | high/name | oblik=nepoznato (zadano), vrsta=crvena |
| 13 | 3858882920360 | LEĆA CRVENA 500g PRIMAVITA ADVENT | 500 g | 3 | 153 | 2,00–5,50 /kg | high/name | oblik=nepoznato (zadano), vrsta=crvena |
| 14 | 3858889333798 | LEĆA CRNA BELUGA VEDRINI 1000 g | 1 kg | 3 | 109 | 3,03–3,69 /kg | high/name | oblik=nepoznato (zadano), vrsta=crna |
| 15 | 3859888609686 | LEĆA 500 g MARCO POLO | 500 g | 3 | 61 | 3,64–5,98 /kg | high/name | oblik=nepoznato (zadano) |
| 16 | 3083680996044 | Leća – Bonduelle – 265 g | 400 g | 3 | 47 | 4,47–6,73 /kg | high/name | oblik=nepoznato (zadano) |
| 17 | 8595241513225 | LEĆA U SLANOM NALJEVU 425ml (OCJ. MASA 240 ML) GIANA | 400 g | 3 | 18 | 1,98–3,47 /kg | high/name | oblik=nepoznato (zadano) |
| 18 | 8009755002903 | LEĆA FIAMMA 400G-24/1- 0334032 | 400 g | 3 | 11 | 1,00–2,47 /kg | high/name | oblik=nepoznato (zadano) |
| 19 | 3859891324293 | LEĆA ZELENA 500 g | 500 g | 2 | 464 | 3,78–4,78 /kg | high/name | oblik=nepoznato (zadano), vrsta=zelena |
| 20 | 3858886175520 | BIO LEĆA ZELENA 500 g EKOZONA | 500 g | 2 | 213 | 4,78–7,18 /kg | high/name | oblik=nepoznato (zadano), vrsta=zelena |

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
| ČIPS OD LEĆE BIO VELIS 30 gr | 4 | `cips` |
| Dimmidisi Juha od leće 620g | 3 | `juha` |
| Hipp Dječja hrana povr.leća,riža190g BIO | 3 | `hipp` |

</details>

<a id="slanutak"></a>
## slanutak (`slanutak`)

jedinica: **kg** · loose_produce: **false** · grupa: **126** · isključenih grupa: **28** · pakiranje: **150–5000**

sinonimi: slanutak, leblebija, cicer  
must_match: `slanut | leblebij | cicer`
  
atributi: oblik = konzerva, smrznuto, svjeze, suho, nepoznato

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850104272349 | SLANUT. LIM 400 g NETO OC.MASA 240 g (12) PODRAVKA | 400 g | 21 | 801 | 2,97–7,88 /kg | high/name | oblik=konzerva |
| 2 | 3850104275609 | SLANUTAK 800 g LIMENKA ( OCJ. MASA 480 g) PODRA | 800 g | 15 | 423 | 2,61–3,99 /kg | high/name | oblik=konzerva |
| 3 | 3859890587026 | SLANUTAK 500 G MARJAN VOCE PVC | 500 g | 9 | 350 | 2,98–4,58 /kg | high/name | oblik=nepoznato (zadano) |
| 4 | 8595241504872 | Giana slanutak 400g/240g | 400 g | 8 | 197 | 2,23–5,38 /kg | high/name | oblik=nepoznato (zadano) |
| 5 | 3859891496839 | Slanutak kuhani vakum 350g | 350 g | 6 | 320 | 3,97–5,11 /kg | high/name | oblik=konzerva |
| 6 | 3083681003949 | Bonduelle Slanutak Vapeur 310g/265g | 310 g | 6 | 260 | 4,22–6,74 /kg | high/name | oblik=nepoznato (zadano) |
| 7 | 8001440009969 | SLANUTAK 400g VALFRUTTA-ocijeđena masa 250g | 400 g | 6 | 206 | 2,65–6,21 /kg | high/name | oblik=nepoznato (zadano) |
| 8 | 8003716003046 | SLANUTAK 240 g LIM. STRAINESSE VM2 | 400 g | 6 | 11 | 2,23–5,25 /kg | high/name | oblik=nepoznato (zadano) |
| 9 | 3856020232306 | SLANUTAK LIM.2500 g OC.MASA 1450 g (6) PODRAVKA | 2,5 kg | 6 | 8 | 2,60–3,88 /kg | high/name | oblik=konzerva |
| 10 | 3083681068146 | N-SLANUTAK BONDUELLE 160G 2*80G -6/1- | 160 g | 5 | 263 | 8,44–12,44 /kg ⚠35 | high/name | oblik=nepoznato (zadano) |
| 11 | 3872084000651 | SLANUTAK 500 g EUROCOMPANY | 500 g | 5 | 204 | 2,22–4,18 /kg | high/name | oblik=nepoznato (zadano) |
| 12 | 3831029510266 | SLANUTAK 300 g NATU RETA | 300 g | 5 | 33 | 8,63–9,97 /kg | high/name | oblik=nepoznato (zadano) |
| 13 | 8076809575157 | TJ.BARILLA SLANUTAK B.G. 250 g | 250 g | 4 | 168 | 13,28–14,00 /kg ⚠159 | high/name | oblik=nepoznato (zadano) |
| 14 | 3858894141777 | SLANUTAK 400/240 g E BUONO | 400 g | 4 | 128 | 1,98–2,63 /kg | high/name | oblik=nepoznato (zadano) |
| 15 | 3858886175537 | EKO SLANUTAK 500 g E KOZONA | 500 g | 4 | 42 | 4,50–6,10 /kg | high/name | oblik=nepoznato (zadano) |
| 16 | 4007415018176 | SLANUTAK 2650 ml LIM.MIKADO | 2,65 l | 4 | 14 | – /l | high/ean | oblik=nepoznato (zadano) |
| 17 | 3859890630517 | SLANUTAK 500 G VEDRINI | 500 g | 3 | 553 | 2,38–3,38 /kg | high/name | oblik=nepoznato (zadano) |
| 18 | 8001440001376 | SLANUTAK 360g VALFRUTTA-ocijeđena masa 230g | 360 g | 3 | 161 | 4,06–6,92 /kg | high/name | oblik=konzerva |
| 19 | 3017800252451 | SLANUTAK 300g/265g D AUCY | 340 g | 3 | 160 | 2,91–5,25 /kg | high/name | oblik=nepoznato (zadano) |
| 20 | 3859890587651 | SLANUTAK RINF. |  | 3 | 60 | 2,09–3,19 /kg | low/unit_price | oblik=nepoznato (zadano) |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| SALATA INSALATISSIME RIO MARE SLANUTAK 160g | 11 | `salata` |
| ARGETA POVRTNI NAMAZ SLANUTAK 95 G ATLANTIC | 10 | `namaz` |
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

jedinica: **kg** · loose_produce: **false** · grupa: **157** · isključenih grupa: **133** · pakiranje: **150–5000**

sinonimi: kukuruz, kukuruz secerac  
must_match: `kukuruz secerac | kukuruz sladak | secerac | kukuruz\b | kukuruza\b`
  
atributi: oblik = konzerva, smrznuto, svjeze, suho, nepoznato

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850104063435 | KUKURUZ ŠEĆERAC 340 g PODRAVKA (10) OC. MASA 280 g | 340 g | 21 | 1213 | 3,53–7,41 /kg | high/name | oblik=konzerva |
| 2 | 3858882217071 | KUKURUZ ŠEĆERAC 340G OC.MASA 285G ZVIJEZDA (12) | 340 g | 19 | 849 | 4,91–10,21 /kg | high/name | oblik=nepoznato (zadano) |
| 3 | 3083680053303 | KUKURUZ ŠEĆERAC BONDUELLE GOLD 340 g (OCJ. MASA 285 g.) ORBICO | 340 g | 18 | 973 | 4,68–9,09 /kg | high/name | oblik=konzerva |
| 4 | 3850104221682 | KUKURUZ ŠEĆERAC 150G/140G, PODRAVKA(12) (PAL 210) | 150 g | 16 | 562 | 7,93–11,07 /kg | high/name | oblik=konzerva |
| 5 | 3083680074094 | N-KUKURUZ ŠEĆERAC 170G (NETTOMASA 140G)BONDUELLE-12/1 0504 | 170 g | 12 | 525 | 7,00–12,29 /kg | high/name | oblik=konzerva |
| 6 | 3083681024258 | KUKURUZ BONDUELLE GOLD 670 g. (OCJ. MASA 570 g.) ORBICO | 670 g | 11 | 401 | 3,21–6,12 /kg | high/name | oblik=nepoznato (zadano) |
| 7 | 3859891493371 | KUKURUZ KUHANI ŠEĆER 400g MADIG | 400 g | 9 | 519 | 4,47–8,88 /kg | high/name | oblik=konzerva |
| 8 | 3083680015424 | KUKURUZ ŠEĆERAC BONDUELLE 530 g (OCJ. MASA 360 g) ORB | 530 g | 9 | 359 | 3,75–7,36 /kg | high/name | oblik=nepoznato (zadano) |
| 9 | 8594012793385 | KUKURUZ ŠEĆERAC 285g OCIJEĐENA MASA | 340 g | 8 | 233 | 3,47–4,97 /kg | high/name | oblik=nepoznato (zadano) |
| 10 | 3083681170658 | N-KUKURUZ ŠEĆERAC 510G 3*170G POSEBNA CIJENA | 510 g | 7 | 292 | 6,25–10,57 /kg | high/name | oblik=nepoznato (zadano) |
| 11 | 3859892245283 | KUKURUZ ŠEĆERAC 425ML(340G NETTO) EVERY DAYS -12/1 ULTRA+ | 340 g | 7 | 77 | 2,91–5,85 /kg | high/name | oblik=nepoznato (zadano) |
| 12 | 3850104209307 | KUKURUZ ŠEĆERAC LIMENKA 2150G/1775G PODRAVKA | 2,15 kg | 6 | 9 | 4,02–5,34 /kg | high/name | oblik=konzerva |
| 13 | 3083681068184 | N-KUKURUZ ŠEĆERAC BONDUELLE 170G 2*85G -6/1- | 160 g | 5 | 285 | 6,81–19,35 /kg | high/name | oblik=nepoznato (zadano) |
| 14 | 3859890236559 | KUKURUZ ŠEĆERAC LARA 2200G -6/1- | 2,2 kg | 5 | 19 | 2,50–3,27 /kg | high/name | oblik=nepoznato (zadano) |
| 15 | 3850116998114 | KUKURUZ ŠEĆERAC 2,5 kg LEDO | 2,5 kg | 4 | 35 | 2,00–3,92 /kg | high/name | oblik=smrznuto |
| 16 | 3856003909850 | KUKURUZ ŠEĆERAC 340g ZORELA-OCIJEĐENA MASA 285g | 285 g | 3 | 476 | 2,91–4,21 /kg | high/name | oblik=nepoznato (zadano) |
| 17 | 3858888530709 | KUKURUZ ŠEĆERAC 3/1 SVJEŽI |  | 3 | 135 | 3,98 /kg | low/unit_price | oblik=nepoznato (zadano) |
| 18 | 3859890236443 | KUKURUZ ŠEĆERAC LARA 340G -24/1- | 340 g | 3 | 35 | 3,53–4,38 /kg | high/name | oblik=nepoznato (zadano) |
| 19 | 3858883228519 | KUKURUZ ŠEĆERAC 400 g BAKINA KUHINJA | 400 g | 3 | 31 | 1,98–2,97 /kg | high/name | oblik=nepoznato (zadano) |
| 20 | 3859891767199 | KUKURUZ ŠEĆERAC 3/1 |  | 3 | 22 | – | – | oblik=nepoznato (zadano) |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| N-SALATA RIO MARE 160G-18/1 KUKURUZ S TUNJEVINOM | 13 | `salata` |
| KUKURUZ ZA KOKICE SLANI ZA MIKROV. PEĆNICU 3*80GR CHIO | 11 | `kokic` |
| KUKURUZ KOKICAR 400 G NATURA MARJAN VOCE | 9 | `kokic` |
| KUKURUZ KOKIČAR CHIO 80G ZA MIKROVALNU SLANI -36/1- | 9 | `kokic` |
| KUKURUZ ZA KOKICE 200G (12), ŠAFRAM | 9 | `kokic` |
| BONDUELLE MJEŠANA SALATA CRVENI GRAH + KUKURUZ ČILI MEXICO 430G/200G | 8 | `salata` |
| KUKURUZ ZA KOKICE S MASLACEM ZA MIKROVALNU 80G CHIO | 8 | `kokic` |
| KUKURUZ KOKICAR 200 g MARJAN VOCE | 7 | `kokic` |
| KUKURUZ ZA KOKICE CHIO 200 g INTERS | 7 | `kokic` |
| N-KUKURUZ PEČENI SUPER SNACK 60G SLANI NATURA -20/1- | 7 | `snack` |

</details>

<a id="grasak"></a>
## grašak (`grasak`)

jedinica: **kg** · loose_produce: **false** · grupa: **151** · isključenih grupa: **97** · pakiranje: **150–5000**

sinonimi: grasak  
must_match: `grasak | graska\b`
  
atributi: oblik = konzerva, smrznuto, svjeze, suho, nepoznato

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850116053165 | N-LEDO GRAŠAK 400G -18/1- 065672 | 400 g | 21 | 1263 | 3,00–6,48 /kg | high/name | oblik=smrznuto |
| 2 | 3850104050862 | GRAŠAK 420 g LIMENKA I KVAL. OCJ. MASA 260 g PODRA | 420 g | 21 | 1077 | 2,48–7,65 /kg | high/name | oblik=konzerva |
| 3 | 3850104050053 | GRAŠAK U LIMENCI 850G/520G I KVALITETA (6),(PAL 96) PODRAVKA | 850 g | 19 | 676 | 2,12–6,33 /kg | high/name | oblik=konzerva |
| 4 | 3858882217057 | ZVIJEZDA GRAŠAK 400G/ 265G (12) ZVIJEZDA | 400 g | 16 | 709 | 3,73–6,75 /kg | high/name | oblik=konzerva |
| 5 | 3850104050046 | GRAŠAK 280 g LIMENKA I KVAL. OCJ. MASA 160 g PODRAVKA | 280 g | 16 | 655 | 2,79–9,94 /kg | high/name | oblik=konzerva |
| 6 | 3083680538404 | GRAŠAK BONDUELLE 200 g OCJ. MASA 130 g ORBICO | 200 g | 14 | 564 | 5,95–9,75 /kg | high/name | oblik=konzerva |
| 7 | 3083680047364 | GRAŠAK BONDULLE 400 g (OCJ. MASA 265 g) ORBI | 400 g | 13 | 729 | 3,98–8,11 /kg | high/name | oblik=konzerva |
| 8 | 3850116058627 | ZAMRZ LEDO 700 g GRAŠAK XXL | 700 g | 12 | 409 | 3,41–4,99 /kg | high/name | oblik=smrznuto |
| 9 | 3858883228762 | GRAŠAK 400 g SM BAKINA KUHINJA STANIĆ | 400 g | 10 | 467 | 2,23–3,33 /kg | high/name | oblik=nepoznato (zadano) |
| 10 | 3850116035451 | GRAŠAK 2,5 kg LEDO*** | 2,5 kg | 9 | 55 | 1,92–4,60 /kg | high/name | oblik=smrznuto |
| 11 | 3856020279004 | O`Plant Grašak mladi smrznuti 400 g | 400 g | 8 | 350 | 2,80–4,47 /kg | high/name | oblik=nepoznato (zadano) |
| 12 | 3850104050800 | GRAŠAK 4,2kg LIM.PODRAVKA - ocijeđene mase 2300g | 4,2 kg | 8 | 25 | 1,78–2,62 /kg | high/name | oblik=konzerva |
| 13 | 3850116876320 | FRESCO GRAŠAK 400G (22) LEDO | 400 g | 7 | 203 | 2,97–5,23 /kg | high/name | oblik=smrznuto |
| 14 | 3858885110065 | GRAŠAK MLADI SMRZNUTI 450G, PODRAVKA | 450 g | 7 | 195 | 1,76–4,11 /kg | high/name | oblik=nepoznato (zadano) |
| 15 | 3859889284585 | N-GRAŠAK FROZY 400G -10/1- | 400 g | 6 | 41 | 2,97–3,33 /kg | high/name | oblik=nepoznato (zadano) |
| 16 | 3850116613956 | GRAŠAK SMRZ.450 g U-GR LEDO | 450 g | 6 | 25 | 3,53–4,71 /kg | high/name | oblik=smrznuto |
| 17 | 3083681036800 | GRAŠAK BONDUELLE VAPEUR 400 g | 400 g | 5 | 251 | 2,97–5,48 /kg | high/name | oblik=nepoznato (zadano) |
| 18 | 3850354013730 | GRAŠAK FINI SMRZ 450 g BRZO&FINO | 450 g | 5 | 157 | 3,00–4,56 /kg | high/name | oblik=nepoznato (zadano) |
| 19 | 3083681168594 | N-GRAŠAK BONDUELLE 600G 3*200G POSEBNA CIJENA | 600 g | 5 | 153 | 5,32–8,82 /kg | high/name | oblik=nepoznato (zadano) |
| 20 | 3083680004275 | XXXX GRAŠAK BONDUELE 800G | 800 g | 5 | 141 | 2,65–6,58 /kg | high/name | oblik=nepoznato (zadano) |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| N-LEDO GRAŠAK MRKVA 400G -18/1- | 21 | `mrkv` |
| GRAŠAK MRKVA FRESCO 400G L LEDO (22) | 9 | `mrkv` |
| GRAŠAK-MRKVA 400G BAKINA KUHINJA,STANIĆ | 9 | `mrkv` |
| O`Plant Grašak i mrkva smrznuti 400 g | 7 | `mrkv` |
| GRAŠAK I MRKVA SMRZNUTO 450G, PODRAVKA | 6 | `mrkv` |
| N-GRAŠAK MRKVA FROZY 400G -10/1- | 6 | `mrkv` |
| PROTEINSKI SNACK OD GRAŠKA 100G ENCIAN | 6 | `snack` |
| FRESCO GRAŠAK-MRKVA 2.5KG LEDO | 5 | `mrkv` |
| GRAŠAK+MRKVA KOCKA 400 g BONDUELLE | 5 | `mrkv` |
| GRAŠAK MRKVA KOCKE ZMH HORVAT (2,5kg) | 4 | `mrkv` |

</details>

<a id="banana"></a>
## banana (`banana`)

jedinica: **kg** · loose_produce: **true** · grupa: **60** · isključenih grupa: **33**

sinonimi: banana, banane  
must_match: `banan`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850334173539 | BANANA |  | 2 | 197 | 1,34–1,79 /kg | low/unit_price |  |
| 2 | ntl:245063 | BANANA |  | 1 | 343 | 1,29–1,59 /kg | low/unit_price |  |
| 3 | konzum:90720080 | BANANA BIO |  | 1 | 158 | 1,49 /kg | low/unit_price |  |
| 4 | 3858885879986 | Banana |  | 1 | 144 | 0,89–1,49 /kg | low/unit_price |  |
| 5 | 3830036310906 | Bio banana |  | 1 | 143 | 1,99 /kg | low/unit_price |  |
| 6 | plodine:100101 | BANANA SORTA CAVENDISH |  | 1 | 126 | 1,44 /kg | low/unit_price |  |
| 7 | gavranovic:071137 | BANANA |  | 1 | 125 | 1,85–1,99 /kg | low/unit_price |  |
| 8 | 4304493274099 | Banana | 1 kg | 1 | 116 | 1,44 /kg | high/unit |  |
| 9 | 4335619068865 | Bio banana | 1 kg | 1 | 116 | 1,49–1,99 /kg | high/unit |  |
| 10 | plodine:100169 | BIO BANANA SORTA CAVENDISH |  | 1 | 111 | 1,79 /kg | low/unit_price |  |
| 11 | tommy:10000969 | BANANA II KAT |  | 1 | 87 | 1,02 /kg | low/unit_price |  |
| 12 | tommy:10000001 | BANANA |  | 1 | 87 | 1,45 /kg | low/unit_price |  |
| 13 | tommy:10005221 | BIO BANANA |  | 1 | 74 | 1,99–2,19 /kg | low/unit_price |  |
| 14 | ribola:0112227 | BANANA II.KL |  | 1 | 61 | 1,03–1,27 /kg | low/unit_price |  |
| 15 | ribola:0112226 | BANANA |  | 1 | 61 | 1,46–1,75 /kg | low/unit_price |  |
| 16 | kaufland:09700781 | Banane |  | 1 | 53 | 1,44 /kg | low/unit_price |  |
| 17 | kaufland:00019299 | KBio.Banana kg |  | 1 | 51 | 1,99 /kg | low/unit_price |  |
| 18 | eurospin:080022402 | BANANE rfz |  | 1 | 43 | 1,34 /kg | low/unit_price |  |
| 19 | eurospin:080360801 | BIO BANANA RINFUZA |  | 1 | 43 | 1,99 /kg | low/unit_price |  |
| 20 | ktc:00101 | BANANA |  | 1 | 30 | 1,46 /kg | low/unit_price |  |

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

jedinica: **kg** · loose_produce: **true** · grupa: **394** · isključenih grupa: **43**

sinonimi: jabuka, jabuke  
must_match: `jabuk`
  
atributi: vrsta = zlatni_delicious, idared, granny_smith, crvena

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3857500007445 | JABUKA CRVENA 2 kg | 2 kg | 3 | 181 | 1,10 /kg | high/ean | vrsta=crvena |
| 2 | 3850334173614 | JABUKA ZLATNI DELIŠES (7) |  | 2 | 197 | 1,29–2,05 /kg | low/unit_price | vrsta=zlatni_delicious |
| 3 | 3850334386069 | JABUKA GALA (7) |  | 2 | 197 | 1,69–2,05 /kg | low/unit_price | vrsta=crvena |
| 4 | 3858893252320 | Jabuka Granny S.rfs |  | 2 | 196 | 1,69–1,99 /kg | low/unit_price | vrsta=granny_smith |
| 5 | 3850334173713 | JABUKA IDARED (7) |  | 2 | 194 | 1,69–2,05 /kg | low/unit_price | vrsta=idared |
| 6 | 3850334173812 | JABUKA JONAGOLD (7) |  | 2 | 193 | 1,75–2,15 /kg | low/unit_price | vrsta=crvena |
| 7 | 3859893211157 | JABUKA CRVENA 2kg PVC | 2 kg | 2 | 172 | 1,00–1,10 /kg | high/name | vrsta=crvena |
| 8 | 3850334049087 | JABUKA ZELENA 2 kg | 2 kg | 2 | 164 | 1,10 /kg | high/name |  |
| 9 | 3850334173621 | JABUKA GRANNY SMITH (7) |  | 2 | 148 | 1,79–1,83 /kg | low/unit_price | vrsta=granny_smith |
| 10 | 3859893211324 | BIO JABUKA CRVENA PODLOZAK |  | 2 | 143 | 2,88 /kg | low/unit_price | vrsta=crvena |
| 11 | 3857500007438 | JABUKA ZELENA 2 kg NTL | 2 kg | 2 | 131 | 1,10 /kg | high/name |  |
| 12 | 3858893251644 | Jabuka Braeburn rfs |  | 2 | 113 | 1,69 /kg | low/unit_price |  |
| 13 | 3859893211348 | BIO JABUKA 500 g | 500 g | 2 | 79 | 4,18–4,72 /kg | high/name |  |
| 14 | 3850334049117 | JABUKA PAKIRANA 2 kg VOĆARNA STUDENCA | 2 kg | 2 | 27 | 1,00–1,09 /kg | high/name | vrsta=crvena |
| 15 | ntl:004016 | JABUKA GALA |  | 1 | 343 | 0,99–1,69 /kg | low/unit_price | vrsta=crvena |
| 16 | ntl:245071 | JABUKA IDARED |  | 1 | 343 | 1,39–1,69 /kg | low/unit_price | vrsta=idared |
| 17 | ntl:247441 | JABUKA JONAGOLD |  | 1 | 343 | 1,39–1,69 /kg | low/unit_price | vrsta=crvena |
| 18 | ntl:246876 | JABUKA ZLATNI DELIŠES |  | 1 | 343 | 1,39–1,69 /kg | low/unit_price | vrsta=zlatni_delicious |
| 19 | ntl:244256 | JABUKA CRVENI DELIŠES |  | 1 | 343 | 1,79 /kg | low/unit_price | vrsta=crvena |
| 20 | ntl:245804 | JABUKA GRANNY SMITH |  | 1 | 343 | 1,79 /kg | low/unit_price | vrsta=granny_smith |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| LEDOLETTE JABUKA KARAMELA LEDO 800 g | 8 | `ledolette` |
| -ČAJ JABUKA CIMET 20/1 DAR PRIRODE AROMA OMOTAČ | 1 | `cimet` |
| JABUKA MIX PODLOZAK | 1 | `mix\b` |
| Jabuka pakirana mix 1kg | 1 | `mix\b` |
| LIKER JABUKA-CIMET INCANTO 1,0 (6)* | 1 | `cimet` |
| MUFFIN JABUKA CIMET 105 G | 1 | `muffin` |
| PALAČINKE JABUKA CIMET 6x90 g MINUTE | 1 | `cimet` |
| PITA JABUKA 1000 g | 1 | `pita\b` |
| PJESCANIK JABUKA CRVENI | 1 | `pjescanik` |
| PJESCANIK JABUKA DIM. 85X76X17 CM 461 DOH | 1 | `pjescanik` |

</details>

<a id="limun"></a>
## limun (`limun`)

jedinica: **kg** · loose_produce: **true** · grupa: **99** · isključenih grupa: **24**

sinonimi: limun, limuni  
must_match: `limun\b | limuna\b | limuni\b`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3858885878088 | LIMUN 500 grama | 500 g | 3 | 540 | 1,98–3,18 /kg | high/name |  |
| 2 | 3859891246663 | LIMUN 500G | 500 g | 3 | 5 | 2,66–5,70 /kg | high/name |  |
| 3 | 3856003908327 | LIMUN 500g PAKIRANI | 500 g | 2 | 135 | 2,18–2,98 /kg | high/name |  |
| 4 | 3859894214171 | LIMUN 500 g | 500 g | 2 | 62 | 2,78–3,58 /kg | high/name |  |
| 5 | 8437022068602 | N-LIMUN 500G | 500 g | 2 | 24 | 2,78–3,98 /kg | high/name |  |
| 6 | 3850334173737 | LIMUN 500g AGROVIR | 500 g | 2 | 12 | 2,66–3,50 /kg | high/name |  |
| 7 | 3859891246168 | LIMUN 1 kg | 1 kg | 2 | 4 | 1,69–2,24 /kg | high/name |  |
| 8 | ntl:248674 | LIMUN |  | 1 | 343 | 1,49 /kg | low/unit_price |  |
| 9 | 3856017202480 | LIMUN |  | 1 | 184 | 1,49 /kg | low/unit_price |  |
| 10 | 3830070890006 | BIO LIMUN 500 G | 500 g | 1 | 155 | 3,98 /kg | high/name |  |
| 11 | 3859893696268 | LIMUN DOMACI 1 KG | 1 kg | 1 | 145 | 1,29–2,39 /kg | high/name |  |
| 12 | 3858885878071 | Limun rfs |  | 1 | 144 | 1,49 /kg | low/unit_price |  |
| 13 | plodine:100294 | LIMUN PRIMOFIORI NATALIA 500 G | 500 g | 1 | 144 | 1,98–2,18 /kg | high/name |  |
| 14 | 8475843257966 | LIMUN S BUDGET 500 g | 500 g | 1 | 143 | 2,78 /kg | high/name |  |
| 15 | 8412345904752 | BIO LIMUN NATUR PUR 500 g | 500 g | 1 | 143 | 4,58–4,78 /kg | high/name |  |
| 16 | 8019796770204 | LIMUN EKO 500 grama | 500 g | 1 | 142 | 3,58–4,30 /kg | high/name |  |
| 17 | plodine:102304 | LIMUN |  | 1 | 141 | 1,49 /kg | low/unit_price |  |
| 18 | 0843702206000 | LIMUN VERNA NATALIA 500 G | 500 g | 1 | 141 | 1,78–2,28 /kg | high/name |  |
| 19 | plodine:100313 | LIMUN VERNA 500 G | 500 g | 1 | 131 | 2,18–2,68 /kg | high/name |  |
| 20 | 8028873003234 | LIMUN 500G | 500 g | 1 | 126 | 2,38 /kg | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| CEDEVITA LIMUN 900G PRAŠK.NAPITAK | 13 | `cedevit` |
| CEDEVITA LIMUN 1000 G XXL | 4 | `cedevit` |
| CEVITANA LIMUN 500 g | 4 | `cevitana` |
| CEVITANA LIMUN VITAMINKA 920 g (5) | 4 | `cevitana` |
| CEDEVITA LIMUN 1000 g ATLANTIC | 3 | `cedevit` |
| CEDEVITA LIMUN 500 g | 2 | `cedevit` |
| CEDEVITA LIMUN 900 g + ČAŠA | 2 | `cedevit` |
| CEVITANA LIMUN 1200g | 2 | `cevitana` |
| ENTELVITA LIMUN 1000g STARO | 2 | `entelvit` |
| ENTELVITA LIMUN 500g STARO | 2 | `entelvit` |

</details>

<a id="naranca"></a>
## naranča (`naranca`)

jedinica: **kg** · loose_produce: **true** · grupa: **113** · isključenih grupa: **36**

sinonimi: naranca, narance  
must_match: `naranc`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3856003907184 | NARANČA 2KG | 2 kg | 3 | 101 | 0,80–1,75 /kg | high/ean |  |
| 2 | ntl:248679 | NARANČA |  | 1 | 343 | 1,29–1,49 /kg | low/unit_price |  |
| 3 | 3858885876961 | NARANČA |  | 1 | 188 | 1,49 /kg | low/unit_price |  |
| 4 | plodine:102306 | NARANCA |  | 1 | 148 | 0,89–1,49 /kg | low/unit_price |  |
| 5 | 7427245230277 | NARANCA 2KG | 2 kg | 1 | 145 | 1,40 /kg | high/name |  |
| 6 | plodine:100285 | NARANCA NAVEL 2 KG | 2 kg | 1 | 144 | 1,25–1,33 /kg | high/name |  |
| 7 | plodine:100209 | NARANCA NAVELINA 2KG | 2 kg | 1 | 144 | 1,25–1,35 /kg | high/name |  |
| 8 | plodine:100530 | NARANCA NATALIA NAVELATE 2 KG | 2 kg | 1 | 144 | 1,35–1,50 /kg | high/name |  |
| 9 | 8437022068152 | NARANČA S BUDGET 2 kg | 2 kg | 1 | 144 | 1,49 /kg | high/name |  |
| 10 | 3858893252542 | Naranča rfs |  | 1 | 144 | 1,49 /kg | low/unit_price |  |
| 11 | plodine:100517 | NARANCA NATALIA 2 KG VALENCIA | 2 kg | 1 | 132 | 0,93–1,60 /kg | high/name |  |
| 12 | gavranovic:072036 | NARANČA |  | 1 | 119 | 1,49–2,69 /kg | low/unit_price |  |
| 13 | gavranovic:072038 | NARANČA CRVENA |  | 1 | 119 | 2,15–2,25 /kg | low/unit_price |  |
| 14 | spar:152288 | Naranča Natalia rfs |  | 1 | 119 | 2,29 /kg | low/unit_price |  |
| 15 | lidl:0080135 | Naranča | 1 kg | 1 | 116 | 0,99–1,49 /kg | high/unit |  |
| 16 | lidl:0080142 | Naranča 2kg | 2 kg | 1 | 116 | 1,74 /kg | high/name |  |
| 17 | lidl:0081532 | Bio naranča 1kg | 1 kg | 1 | 116 | 2,49 /kg | high/name |  |
| 18 | 8423466000155 | NARANCA ZA CIJEDENJE 1,5KG | 1,5 kg | 1 | 111 | 1,99 /kg | high/name |  |
| 19 | 8713037001668 | BIO NARANČA 1 kg | 1 kg | 1 | 101 | 3,99 /kg | high/name |  |
| 20 | 8014914018701 | SORBET NARANCA I DUMBIR |  | 1 | 101 | – | – |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| CEDEVITA NARANČA 900G PRAŠK.NAPITAK | 13 | `cedevit` |
| CEDEVITA NARANCA 1000 G XXL | 5 | `cedevit` |
| CEVITANA NARANČA 500gr (12) | 5 | `cevitana` |
| CEVITANA NARANČA VITAMINKA 920 g (5) | 4 | `cevitana` |
| MEDENJACI NARANČA 500G SWISLION | 3 | `medenjac` |
| CEDEVITA NARANČA 900 g + ČAŠA | 2 | `cedevit` |
| ENTELVITA NARANČA 1000g STARO | 2 | `entelvit` |
| ENTELVITA NARANČA 500g STARO | 2 | `entelvit` |
| BATAT NARANČASTI 500G EKOZONA | 1 | `narancast` |
| CEDEVITA NARANČA 1/1 kg (5) | 1 | `cedevit` |

</details>

<a id="papar"></a>
## papar (`papar`)

jedinica: **kg** · loose_produce: **false** · grupa: **241** · isključenih grupa: **126** · pakiranje: **10–500** · **pantry**

sinonimi: papar, crni papar  
must_match: `papar\b`
  
atributi: oblik = mljeveni, zrno, mlinac; vrsta = crni, bijeli, sareni

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 9001414041116 | ZAČIN MLINAC PAPAR CRNI U ZRNU 36 g KOTANY | 36 g | 20 | 904 | 96,67–152,50 /kg | high/name | vrsta=crni, oblik=zrno |
| 2 | 3859888163089 | PAPAR CRNI MLJEVENI 50G ŠAFRAM (25) | 50 g | 18 | 950 | 24,80–45,60 /kg ⚠1 | high/name | vrsta=crni, oblik=mljeveni |
| 3 | 9001414040409 | ZAČIN PAPAR CRNI MLJEVENI STAKLO 50 g KOTANY | 50 g | 18 | 760 | 60,00–95,80 /kg | high/name | vrsta=crni, oblik=mljeveni |
| 4 | 3859888163034 | PAPAR CRNI MLJEVENI 100 G VRECICA SAFRAM | 100 g | 18 | 713 | 21,00–34,90 /kg | high/name | vrsta=crni, oblik=mljeveni |
| 5 | 9001414015469 | KOTANYI PAPAR CRNI MLJEVENI VREĆICA 17G (25) | 17 g | 18 | 654 | 53,53–111,18 /kg | high/name | vrsta=crni, oblik=mljeveni |
| 6 | 3850104294426 | PAPAR CRNI MLJEVENI 20 G VRECICA MAESTRO VEGETA PODRAVKA | 20 g | 17 | 694 | 44,50–92,50 /kg | high/name | vrsta=crni, oblik=mljeveni |
| 7 | 3850104294617 | PAPAR CRNI MLJEVENI 100 G VRECICA MAESTRO VEGETA PODRAVKA | 100 g | 16 | 638 | 23,50–45,90 /kg | high/name | vrsta=crni, oblik=mljeveni |
| 8 | 3850104294419 | PAPAR CRNI ZRNO 15 G VRECICA MAESTRO VEGETA PODRAVKA | 15 g | 16 | 635 | 42,67–179,00 /kg | high/name | vrsta=crni, oblik=zrno |
| 9 | 9001414015117 | PAPAR SARENI MJESAVINA U ZRNU 16 G VRECICA KOTANYI | 16 g | 15 | 764 | 56,88–124,38 /kg | high/name | vrsta=sareni, oblik=zrno |
| 10 | 3859888163119 | PAPAR CRNI U ZRNU 50G (25), ŠAFRAM | 50 g | 15 | 715 | 23,80–49,80 /kg | high/name | oblik=zrno, vrsta=crni |
| 11 | 9001414040089 | PAPAR CAYENNE MLJEVENI 38 G STAKLO KOTANYI | 38 g | 15 | 691 | 57,63–78,68 /kg | high/name | oblik=mljeveni |
| 12 | 3850104294730 | PAPAR SARENI 40 G MLINAC MAESTRO VEGETA PODRAVKA | 40 g | 14 | 635 | 52,25–119,75 /kg | high/name | vrsta=sareni, oblik=mlinac |
| 13 | 9001414010075 | PAPAR ZELENI ZRNO 12 G VRECICA KOTANYI | 12 g | 14 | 524 | 75,83–165,83 /kg | high/name | oblik=zrno |
| 14 | 3850104294501 | PAPAR BIJELI MLJEVENI 20 G MAESTRO VEGETA PODRAVKA | 20 g | 14 | 441 | 62,50–114,50 /kg | high/name | vrsta=bijeli, oblik=mljeveni |
| 15 | 9001414040799 | PAPAR S CESNJAKOM 72 G STAKLO KOTANYI | 70 g | 14 | 388 | 20,97–62,71 /kg | high/name |  |
| 16 | 3856020233051 | VEGETA MAESTRO CRNI PAPAR ZRNO MLIN 42g PODRAVKA | 42 g | 13 | 574 | 35,71–109,29 /kg | high/name | vrsta=crni, oblik=zrno |
| 17 | 3859888163096 | PAPAR CRNI MLJEVENI 10G (100), ŠAFRAM | 10 g | 13 | 397 | 40,00–75,00 /kg | high/name | oblik=mljeveni, vrsta=crni |
| 18 | 9001414015452 | PAPAR CRNI ZRNO 17 G VRECICA KOTANYI | 17 g | 12 | 489 | 53,53–105,29 /kg ⚠1 | high/name | vrsta=crni, oblik=zrno |
| 19 | 3850104294822 | CRNI PAPAR MLJ.VREĆ.50G (20) (PAL 145),PODRAVKA | 50 g | 12 | 448 | 34,00–55,80 /kg | high/name | vrsta=crni, oblik=mljeveni |
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

jedinica: **kg** · loose_produce: **false** · grupa: **103** · isključenih grupa: **11** · pakiranje: **20–500** · **pantry**

sinonimi: mljevena paprika, slatka paprika, ljuta paprika, aleva paprika  
must_match: `paprika mljevena | mljevena paprika | paprika slatka mlj | paprika ljuta mlj | paprika mlj | mlj paprika | aleva paprika | paprika slatka | paprika ljuta | slatka paprika | ljuta paprika`
  
atributi: vrsta = slatka, ljuta, dimljena

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3859888163065 | PAPRIKA SLATKA MLJEVENA 100 G VRECICA SAFRAM | 100 g | 18 | 1197 | 11,30–25,50 /kg | high/name | vrsta=slatka |
| 2 | 3859888163058 | PAPRIKA LJUTA MLJEVENA 100 G VRECICA SAFRAM | 100 g | 18 | 1129 | 12,90–22,50 /kg | high/name | vrsta=ljuta |
| 3 | 3850104294631 | PAPRIKA SLATKA MLJEVENA VRECICA100 G MAESTRO VEGETA PODRAVKA | 100 g | 18 | 772 | 9,90–21,90 /kg | high/name | vrsta=slatka |
| 4 | 3850104294624 | PAPRIKA LJUTA MLJEVENA 100 G MAESTRO VEGETA PODRAVKA | 100 g | 17 | 579 | 9,90–19,90 /kg ⚠1 | high/name | vrsta=ljuta |
| 5 | 3859888163072 | PAPRIKA SLATKA MLJEVENA 200 G VRECICA SAFRAM | 200 g | 14 | 545 | 13,45–20,95 /kg | high/name | vrsta=slatka |
| 6 | 3850104294648 | PAPRIKA SLATKA MLJEVENA 200 G MAESTRO VEGETA PODRAVKA | 200 g | 13 | 457 | 8,20–44,75 /kg | high/name | vrsta=slatka |
| 7 | 3850104294594 | PAPRIKA SLATKA MLJEVENA 50 G VRECICA MAESTRO VEGETA PODRAVKA | 50 g | 12 | 547 | 13,20–23,00 /kg | high/name | vrsta=slatka |
| 8 | 3859888163317 | PAPRIKA SLATKA MLJEVENA DELIKATES 100 G VRECICA SAFRAM | 100 g | 10 | 367 | 11,90–23,90 /kg ⚠1 | high/name | vrsta=slatka |
| 9 | 9001414119211 | PAPRIKA LJUTA MLJEVENA 35 G VRECICA KOTANYI | 35 g | 10 | 312 | 23,14–39,71 /kg | high/name | vrsta=ljuta |
| 10 | 9001414119204 | PAPRIKA SLATKA MLJEVENA DELIKATES 35 G VRECICA KOTANYI | 35 g | 10 | 289 | 20,29–39,71 /kg | high/name | vrsta=slatka |
| 11 | 3850104294600 | PAPRIKA SLATKA MLJEVENA 400 G VRECICA MAESTRO VEGETA PODRAVK | 400 g | 10 | 142 | 6,25–14,98 /kg ⚠14 | high/name | vrsta=slatka |
| 12 | 3859890104124 | PAPRIKA MLJEVENA ZAČINSKA LJUTA 500G, ŠAFRAM | 500 g | 8 | 144 | 12,20–18,38 /kg | high/name | vrsta=ljuta |
| 13 | 9001414009208 | PAPRIKA SLATKA MLJEVENA 100 G VRECICA KOTANYI | 100 g | 7 | 404 | 15,90–28,90 /kg | high/name | vrsta=slatka |
| 14 | 3858881083127 | ZAČIN PAPRIKA SLATKAFRANCK 100 g | 100 g | 7 | 178 | 15,90–20,50 /kg ⚠1 | high/name | vrsta=slatka |
| 15 | 3859890104698 | PAPRIKA SLATKA MLJEVENA 100G ULTRA PLUS | 100 g | 7 | 75 | 7,90–13,90 /kg | high/name | vrsta=slatka |
| 16 | 3859892109868 | Š EXTRA PAPRIKA SLATKA ŠAFRAM 100 g (20) | 100 g | 7 | 63 | 7,50–10,60 /kg | high/name | vrsta=slatka |
| 17 | 9001414119242 | KOTANYI 45G PAPRIKA SLATKAZAČINSKA -25/1- VREĆICA | 45 g | 6 | 318 | 13,78–30,89 /kg | high/name | vrsta=slatka |
| 18 | 3858881735378 | PAPRIKA SLATKA ZAČIN 70G DERMA (20) | 70 g | 6 | 235 | 12,71–21,29 /kg ⚠4 | high/name | vrsta=slatka |
| 19 | 3858881582019 | ZAČIN PAPRIKA SLATKANADALINA 100 g | 100 g | 6 | 217 | 13,50–21,50 /kg | high/name | vrsta=slatka |
| 20 | 9001414008140 | PAPRIKA SLATKA ZACINSKA XXL PACK 150 G KOTANYI | 150 g | 6 | 181 | 6,67–25,93 /kg | high/name | vrsta=slatka |

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

jedinica: **kg** · loose_produce: **false** · grupa: **106** · isključenih grupa: **107** · pakiranje: **50–2000** · **pantry**

sinonimi: dodatak jelima, vegeta, univerzalni dodatak jelima  
must_match: `vegeta\b | dodatak jelima | univerzalni dodatak | dodatak za jela`

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850104008597 | VEGETA 250G (16), PODRAVKA (PAL 102) | 250 g | 25 | 1363 | 6,88–11,16 /kg | high/name |  |
| 2 | 3850104047046 | VEGETA 1KG (10), PODRAVKA (PAL-60) | 1 kg | 22 | 989 | 5,36–11,19 /kg | high/name |  |
| 3 | 3850104260872 | VEGETA 400G VREĆICA PODRAVKA PROMO | 400 g | 20 | 1342 | 6,23–10,97 /kg | high/name |  |
| 4 | 3850104008443 | VEGETA 500G (12), PODRAVKA (PAL 80) | 500 g | 20 | 865 | 7,08–10,18 /kg | high/name |  |
| 5 | 3850104008054 | VEGETA 75G (35), PODRAVKA (PAL 102) | 75 g | 17 | 818 | 6,67–21,20 /kg | high/name |  |
| 6 | 3850104248832 | VEGETA NATUR VREĆICA 150G (12) PODRAVKA (PAL 85) | 150 g | 17 | 757 | 9,73–18,93 /kg | high/name |  |
| 7 | 3850104255274 | VEGETA BOČICA 200G, PODRAVKA(12) (PAL 126) | 200 g | 17 | 736 | 11,95–14,45 /kg | high/name |  |
| 8 | 3850104216466 | N-VEGETA PODR 250G+50G GRATIS -16/1- VREĆICA | 250 g | 16 | 1111 | 7,80–11,48 /kg | high/name |  |
| 9 | 3850104249600 | N-VEGETA PODR 400G STAKLO DOZA -8/1- | 400 g | 16 | 605 | 8,95–11,25 /kg | high/name |  |
| 10 | 3850104273483 | VEGETA MEDITER. DELTAPA. VREĆ. 100 g (12) PODRAVKA | 100 g | 16 | 599 | 10,70–17,50 /kg | high/name |  |
| 11 | 3850104226212 | VEGETA 150G, PODRAVKA, (12) ZIPP (PAL 85) | 150 g | 15 | 709 | 10,60–15,93 /kg | high/name |  |
| 12 | 3850104273490 | VEGETA PIKANT DELTA. VREĆICA 100 g (12) PODRAVKA | 100 g | 15 | 449 | 9,00–18,40 /kg | high/name |  |
| 13 | 3856020270544 | VEGETA 200 g FINO MLJEVENA PODRAVKA | 200 g | 14 | 620 | 8,45–14,90 /kg | high/name |  |
| 14 | 3850104254444 | VEGETA PODR 300G NATUR DOZA -12/1- | 300 g | 14 | 575 | 10,60–13,70 /kg | high/name |  |
| 15 | 3850104047077 | VEGETA 2KG (8), PODRAVKA (PAL 24) | 2 kg | 14 | 110 | 5,78–8,29 /kg | high/name |  |
| 16 | 3850104257933 | VEGETA NATUR 75G (12) PODRAVKA (PAL 100) | 75 g | 12 | 330 | 8,67–23,87 /kg | high/name |  |
| 17 | 3856020235109 | VEGETA NATUR TEK.DODATAK JELIMA 170ML (12) (PAL 90) | 170 ml | 8 | 282 | – /l | high/name |  |
| 18 | 3856020278199 | VEGETA NATUR PASTA PAPRIKA BLAGA 190G (TUBA) | 190 g | 7 | 276 | 9,95–14,16 /kg | high/name |  |
| 19 | 3856020221799 | VEGETA NATUR SALATA 60 g PODRAVKA | 60 g | 7 | 38 | 16,50–36,50 /kg ⚠2 | high/name |  |
| 20 | 3856020276669 | VEGETA DIMLJENA 200 G VRECICA | 200 g | 6 | 373 | 7,95–11,75 /kg | high/name |  |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| VEGETA TWIST KRUMPIR VREĆICA 30G(18) (PAL 242) | 19 | `twist` |
| VEGETA GRILL CLASSIC VREĆICA 30G (18) (PAL 252) | 18 | `grill` |
| VEGETA TWIST ZA PILETINU VREĆICA 30G (18) (PAL 252) | 18 | `twist` |
| VEGETA GRILL VRATINA 30G (18) (PAL 252) | 13 | `grill` |
| VEGETA NATUR GRILL CLASSIC POSIPAČ 80G ,PODRAVKA | 13 | `grill` |
| VEGETA GRILL MARINADA CLASSIC 75 g (20) | 12 | `marinad` |
| VEGETA NATUR GRILL POVRĆE 30G (18) (PAL 252) PODRAVKA | 12 | `grill` |
| VEGETA GRILL MARINADA BBQ 75 g (20) | 11 | `marinad` |
| VEGETA GRILL MARINADA PIKANTNA 75GR (20) | 11 | `marinad` |
| VEGETA TWIST ZLATN.PILETINA 30G (18) (PAL 18) PODRAVKA | 11 | `twist` |

</details>

<a id="ocat"></a>
## ocat (alkoholni/vinski) (`ocat`)

jedinica: **l** · loose_produce: **false** · grupa: **127** · isključenih grupa: **156** · pakiranje: **500–3000** · **pantry**

sinonimi: ocat, alkoholni ocat, vinski ocat, kvasina  
must_match: `ocat\b | octa\b | kvasin`
  
atributi: vrsta = alkoholni, vinski

| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |
|---|---|---|---|---|---|---|---|---|
| 1 | 3850164310111 | N-OCAT BADEL ALKOHOLNI 1.0L-12/1- | 1 l | 22 | 1302 | 1,19–1,99 /l | high/name | vrsta=alkoholni |
| 2 | 3850164321117 | KISKO VINSKI OCAT 1L (12), BADEL | 1 l | 22 | 922 | 1,59–3,49 /l | high/name | vrsta=vinski |
| 3 | 3850164310180 | OCAT BADEL ALKOHOLNI 3.0L BALON (9%) | 3 l | 21 | 1116 | 0,96–1,70 /l | high/name | vrsta=alkoholni |
| 4 | 3850164310142 | OCAT KISKO ALKOHOLNI 0,5L LABUD | 500 ml | 21 | 788 | 1,68–3,18 /l | high/name | vrsta=alkoholni |
| 5 | 3858882210928 | OCAT ALKOHOLNI 1 l PET ZVIJEZDA | 1 l | 19 | 862 | 0,96–1,69 /l ⚠4 | high/name | vrsta=alkoholni |
| 6 | 3858882211154 | N-OCAT ZVIJEZDA VINSKI 1L -12/1-CRNO VINO | 1 l | 18 | 707 | 1,63–2,59 /l ⚠4 | high/name | vrsta=vinski |
| 7 | 3850164321148 | OCAT VINSKI KISKO 500 ml BADE | 500 ml | 17 | 821 | 2,24–3,98 /l | high/name | vrsta=vinski |
| 8 | 3850164331116 | OCAT KVASINA 6% 1L KISKO BADEL | 1 l | 13 | 660 | 1,59–2,49 /l | high/name | vrsta=vinski |
| 9 | 3858882211727 | OCAT ALKOHOLNI OCAT 3 l ZVIJEZDA (1) | 3 l | 13 | 443 | 0,88–1,50 /l ⚠4 | high/name | vrsta=alkoholni |
| 10 | 3859891093922 | ULTRA OCAT VINSKI 1L, PREHRANA (6) | 1 l | 8 | 84 | 0,89–1,69 /l | high/name | vrsta=vinski |
| 11 | 3850164321186 | OCAT VINSKI 3L KISKO BADEL | 3 l | 8 | 64 | 1,13–1,80 /l | high/name | vrsta=vinski |
| 12 | 3859891093908 | ULTRA OCAT ALKOHOLNI 1L, PREHRANA (6) (750PAL) | 1 l | 7 | 78 | 0,69–1,49 /l ⚠2 | high/name | vrsta=alkoholni |
| 13 | 3858889640018 | SEGESTICA ALKOHOLNI OCAT 9% 1L (12) | 1 l | 6 | 198 | 0,93–1,59 /l | high/name | vrsta=alkoholni |
| 14 | 3858889640032 | SEGESTICA VINSKI OCAT 1L (12) LABUD | 1 l | 6 | 150 | 1,33–1,97 /l ⚠1 | high/name | vrsta=vinski |
| 15 | 3859891093007 | OCAT ALKOHOLNI PREHRANA 9% 1 L | 1 l | 5 | 194 | 0,69–1,25 /l | high/name | vrsta=alkoholni |
| 16 | 3858889362545 | NATUREL ALKOHOLNI OCAT 1 L (9 %) | 1 l | 5 | 82 | 0,89–1,39 /l | high/name | vrsta=alkoholni |
| 17 | 3859892999063 | OCAT VIROVITIČKI PRIRODNI VINSKI 1 L | 1 l | 5 | 78 | 1,33–2,49 /l | high/name | vrsta=vinski |
| 18 | 3859891093205 | OCAT VINSKI 1L PREH | 1 l | 5 | 44 | 0,99–1,79 /l | high/ean | vrsta=vinski |
| 19 | 3858889362569 | NATUREL VINSKI OCAT 1 L (6 %) | 1 l | 4 | 79 | 1,19–1,99 /l | high/name | vrsta=vinski |
| 20 | 3856003946244 | OCAT ALKOHOLNI ZORELA 3L | 3 l | 3 | 466 | 0,83–0,96 /l | high/name | vrsta=alkoholni |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| OCAT JABUČNI 1L 5% KISKO LABUD | 21 | `jabuc` |
| OCAT BADEL JABUČNI 0.5L-12/1- | 20 | `jabuc` |
| JABUČNI PRIRODNI OCAT 1L (15), ZVIJEZDA | 16 | `jabuc` |
| Encian Ocat jabučni 0,7l staklo | 14 | `jabuc` |
| OCAT ACETO BALSAMICO 0,5L (12) ZVIJEZDA | 11 | `bals` |
| OCAT ACETO BALSAMICO 250ML ORO DUE VITTORIE | 11 | `bals` |
| OCAT MAUTNER 500ML JABUČNI BARRIQUE -6/1- | 11 | `jabuc` |
| Mautner Ocat jabučni 5% oct.kisel.500ml | 10 | `jabuc` |
| Mautner Markhof Ocat jabučni 5% 1 l | 9 | `jabuc` |
| SEGESTICA JABUČNI OCAT 1L (12) LABUD | 8 | `jabuc` |

</details>

<a id="med"></a>
## med (`med`)

jedinica: **kg** · loose_produce: **false** · grupa: **488** · isključenih grupa: **131**

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
| TRAJNO SLANO PECIVO ELEPHANT PRETZEL 125 g MED, SENF I LUK | 12 | `senf` |
| UMAK BBQ MED 345 g PODRAVKA | 12 | `umak` |
| KREKER MORSKA SOL I MED 180 G ELEPHANT | 11 | `kreker` |
| SNACK MORSKA SOL I MED 160 G ELEPHANT TWIST | 9 | `snack` |
| TRAJNO SLANO PECIVO ELEPHANT PRETZEL 75 g MED, SENF I LUK | 9 | `senf` |

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
| 10 | 7613287084644 | SENF THOMY 100 g BLAGI LOT:618768839 | 100 g | 16 | 476 | 9,90–21,90 /kg ⚠4 | high/name |  |
| 11 | 9001414040713 | Kotanyi gorušica zrno staklo 79 g | 79 g | 14 | 426 | 33,54–38,61 /kg ⚠288 | high/name |  |
| 12 | 4025891136153 | Jutro Senf u krigli srednje ljuti 250 g | 250 g | 13 | 567 | 6,36–11,96 /kg | high/name |  |
| 13 | 3830003054475 | SENF 290 G NATURETA STAKLO | 290 g | 13 | 318 | 3,45–9,97 /kg | high/name |  |
| 14 | 3850104023064 | SENF ESTRAGON PVC 2.5 KG PODRAVKA (6) | 2,5 kg | 13 | 36 | 2,71–4,86 /kg | high/name |  |
| 15 | 9011900184401 | Mautner Markhof Senf estragon stak.350g | 350 g | 12 | 538 | 5,11–8,54 /kg | high/name |  |
| 16 | 9011900139616 | Mautner Markhof Senf estragon tuba 200 g | 200 g | 12 | 455 | 7,00–11,45 /kg | high/name |  |
| 17 | 4025891004254 | SENF JUTRO 250ML KRIGLA-12/1- | 250 g | 12 | 212 | 10,00–11,16 /kg | high/name |  |
| 18 | 3856020268909 | SENF ESTRAGON SQUEEZE 310G PODRAVKA (6) | 310 g | 11 | 420 | 6,13–8,74 /kg | high/name |  |
| 19 | 7610100999093 | Thomy senf delikatesni staklenka 700 g | 700 g | 11 | 185 | 5,36–8,27 /kg ⚠6 | high/name |  |
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
| 2 | 3858882210263 | MAJONEZA DELIKATES 165 G TUBA ZVIJEZDA | 165 g | 22 | 1395 | 13,94–20,55 /kg | high/name |  |
| 3 | 3856015325228 | MAJONEZA DELIKATES 85 g VREĆICA ZVIJEZDA | 85 g | 22 | 1391 | 8,82–18,59 /kg | high/name |  |
| 4 | 3856015321879 | MAJONEZA DELIKATES 620g STAKLENKA ZVIJEZDA | 620 g | 22 | 1377 | 6,34–11,60 /kg | high/name |  |
| 5 | 7613287084606 | THOMY MAJONEZA DELIKATESNA TUBA 165G (20), NESTLE | 165 g | 21 | 1237 | 10,85–21,15 /kg | high/name |  |
| 6 | 3858890178678 | MAJONEZA THOMY DOYPACK VREĆICA S ČEPOM 263 g ALCA | 263 g | 21 | 913 | 9,47–16,69 /kg | high/name |  |
| 7 | 3856015322098 | N-MAJONEZA ZVIJEZDA 270G-12/1- DOYPACK | 270 g | 21 | 851 | 8,48–15,89 /kg | high/name |  |
| 8 | 3856015316660 | GASTRO SALATNA MAJONEZA ZVIJEZDA 15 g (100) | 15 g | 21 | 797 | 14,67–32,67 /kg | high/name |  |
| 9 | 3858882219020 | N-MAJONEZA ZVIJEZDA 400G DELIKATES -8/1- | 400 g | 20 | 1170 | 8,98–14,23 /kg | high/name |  |
| 10 | 3858882210324 | MAJONEZA LAGANA U FOLIJI 95G (25), ZVIJEZDA | 95 g | 19 | 881 | 9,37–16,74 /kg | high/name |  |
| 11 | 3856015333926 | MAJONEZA DELIKATES ZVIJEZDA 165g+110g GRATIS TUBA ZVIJEZDA | 165 g | 15 | 952 | 15,09–18,12 /kg | high/name |  |
| 12 | 3856015321244 | N-MAJONEZA ZVIJEZDA 255G DELIKATES -12/1- | 255 g | 15 | 536 | 11,96–16,82 /kg | high/name |  |
| 13 | 3856015321909 | N-MAJONEZA ZVIJEZDA 620G LIGHT- 6/1- STAKLENKA | 620 g | 15 | 392 | 6,92–10,79 /kg | high/name |  |
| 14 | 3858890178692 | MAJONEZA THOMY 611 g+150 g GRATIS STAKLO ALCA | 611 g | 14 | 405 | 4,09–11,93 /kg ⚠1 | high/name |  |
| 15 | 8445292265522 | MAJONEZA THOMY 80 G VRECICA NESTLE | 80 g | 13 | 1067 | 8,75–22,38 /kg | high/name |  |
| 16 | 7613287084545 | MAJONEZA THOMY 265 G TUBA NESTLE | 265 g | 13 | 573 | 13,55–17,70 /kg ⚠4 | high/name |  |
| 17 | 8445291689152 | MAJONEZA THOMY 170G DOYPACK -18/1- | 170 g | 13 | 485 | 13,47–16,41 /kg ⚠2 | high/name |  |
| 18 | 7613035904958 | MAJONEZA 380G DOYPACK XL VREĆICA S ČEPOM THOMY | 380 g | 13 | 453 | 7,87–13,13 /kg ⚠2 | high/name |  |
| 19 | 3858882212946 | MAJONEZA 2KG GASTRO SALATNA ZVIJEZDA | 2 kg | 13 | 63 | 3,33–4,82 /kg | high/name |  |
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

jedinica: **kg** · loose_produce: **false** · grupa: **176** · isključenih grupa: **43**

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
| 6 | 3856015316752 | GASTRO KETCHUP ZVIJEZDA 15 g (100) | 15 g | 18 | 486 | 13,33 /kg ⚠479 | high/name | vrsta=blagi |
| 7 | 3850104268915 | KETCHUP LJUTI 500G(6) (PAL 85) PODRAVKA | 500 g | 17 | 698 | 3,38–4,98 /kg | high/name | vrsta=ljuti |
| 8 | 8715700421469 | KETCHUP BLAGI HEINZ 570 G | 570 g | 15 | 710 | 5,07–9,63 /kg | high/name | vrsta=blagi |
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
| 19 | 3856020273910 | KETCHUP LJUTI 310 G PODRAVKA | 310 g | 8 | 411 | 1,58–5,71 /kg | high/name | vrsta=ljuti |
| 20 | 8005110004674 | N-KETCHUP MUTTI 300G -6/1- BOCA | 300 g | 8 | 311 | 6,63–10,63 /kg | high/name | vrsta=blagi |

<details><summary>Najčešće isključeni (top 10)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| Zvijezda ketchup i majoneza tuba 165 g | 16 | `majonez` |
| CHIO TIP TOP CUBICS KETCHUP INTERSNACK 50 g (30) | 15 | `chio` |
| FLIPS DINI 30G MARBO KETCHUP-35/1- | 14 | `flips` |
| MAJONEZA S KETCHUP THOMY TUBA 190G THOMY (10) | 13 | `majonez` |
| CHIO KROKI KROKET KETCHUP V. INTERSNACK 120 g (10) | 12 | `chio` |
| GRICKALICE POM BAR KETCHUP 50G CHIO | 12 | `chio` |
| Chio Chips Čips ketchup style 130 g | 11 | `chio` |
| GRICKALICE KROKI KROKET TROKI KETCHUP 110G CHIO | 10 | `chio` |
| FLIPS STIX KETCHUP 35 g BOBI | 8 | `bobi` |
| FLIPS BOBI 40 g TOBY KETCHUP | 7 | `bobi` |

</details>
