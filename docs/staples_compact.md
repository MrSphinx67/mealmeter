# Pregled osnovnih namirnica (sažeto)

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
- [maslac](#maslac) (`maslac`)
- [mlijeko](#mlijeko) (`mlijeko`)
- [jaja](#jaja) (`jaja`)
- [luk (crveni/žuti)](#luk) (`luk`)
- [krumpir](#krumpir) (`krumpir`)
- [riža](#riza) (`riza`)
- [tjestenina](#tjestenina) (`tjestenina`)
- [rajčica (svježa)](#rajcica) (`rajcica`)
- [kakao (prah)](#kakao) (`kakao`)
- [peršin](#persin) (`persin`)
- [pileća prsa / file](#pileca_prsa) (`pileca_prsa`)

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

<details><summary>Najčešće isključeni (top 5)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| SMJESA ZA KRUH (BEZGLUTENSKO BRAŠNO) DR.SCHÄR MIX B 1KG (10) | 15 | `mix\b` |
| KOKOS BRAŠNO 200G (10), ŠAFRAM | 14 | `kokos` |
| HELJDINO BRAŠNO 1 kg PODRAVKA (10) | 13 | `heljd` |
| SUPERFOODS eko kokosovo brašno 250g | 10 | `kokos` |
| KOKOS BRAŠNO 200G(20) NATURA, MARJAN VOĆE | 8 | `kokos` |

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

<details><summary>Najčešće isključeni (top 5)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| LIMUN ŠEĆER 10G (50) PODRAVKA (PAL 468) | 19 | `limun` |
| DOLCELA VANILIN ŠEĆER 8 g 5+1 GRATIS PODRAVKA (44) | 18 | `vanilin` |
| RUM ŠEĆER 10G (50) PODRAVKA (PAL 468) | 18 | `rum\b` |
| DOLCELA LIMUN ŠEĆER 10 g 3 PAK (26) PODRAVKA | 17 | `limun` |
| DOLCELA VANILIN ŠEĆER 8 g PODRAVKA (44) | 17 | `vanilin` |

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

<details><summary>Najčešće isključeni (top 5)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| ČIPS ČIPI ČIPS 120G SOL I PAPAR ULTRA REBRASTI -20/1- CHIO | 17 | `papar` |
| TRAJNO PEC. ELEP.TWIST - MORSKA SOL I MED 180g | 12 | `med\b` |
| KOTANYI 185G PAPAR CRNI MLJEV 50G + SOL 135G GRATIS -1/1- | 11 | `papar` |
| SOL MORSKA SITNA 250G SOLJENKA -12/1- PAG | 11 | `soljenk` |
| SOL SITNA MORSKA 250g PAG91 SOLJENKA | 10 | `soljenk` |

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

<details><summary>Najčešće isključeni (top 5)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| ULJE MASLINOVO EXTRA DJEVICANSKO 1 L ZVIJEZDA STAKLO | 22 | `masli` |
| ULJE MASLINOVO EXTRA DJEVICANSKO 0.5 L ZVIJEZDA STAKLO | 19 | `masli` |
| N-ULJE MASL. 1L ORGULA TRADICIJA EXTRA DJEVIČANSKO -6/1- EKO | 16 | `dev` |
| ULJE BUCINO 500 ML ZVIJEZDA STAKLO | 16 | `bucin` |
| RIO MARE TUNA MAS.ULJE 2x80 g OC.MASA 104 g (48) | 12 | `mas\b` |

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

<details><summary>Najčešće isključeni (top 5)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| GRICKALICE SMOKICE MASLAC 85G ŠTARK | 17 | `smokic` |
| Margo Namaz miješani s maslacem 225g | 14 | `namaz` |
| KEKSI JAFFA BUTTONS KIKIRIKI MASLAC 95GK | 12 | `kikiriki` |
| KEKSI PETIT BEURE S MASLACEM BEZ GLUTENA 130G BALVITEN | 12 | `keks` |
| KOKICE BOBI GOTOVE S OKUSOM MASLACA 100G | 11 | `kokic` |

</details>

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

<details><summary>Najčešće isključeni (top 5)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| DUKAT ČOKOLADNO MLIJEKO 0.5 L EDGE (12) | 22 | `cokolad` |
| MLIJEKO ČOKOLADNO ZBREGOV 2%MM 0.5L SLIM (16), VINDIJA | 20 | `cokolad` |
| ČOKOLADNO MLIJEKO BOCA 0,5L (6) DUKAT | 20 | `cokolad` |
| N-MLIJEKO Z BREGOV 1.00L KOZJE 2.8%MM S ČEPOM UHT -12/1- | 19 | `kozje` |
| MLIJEKO ČOKOLADNO KOKOS 500 ml DUKAT | 18 | `cokolad` |

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

<details><summary>Najčešće isključeni (top 5)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| N-FERRERO KINDER JAJE SURPRISE 20G -72/1- | 15 | `ferrero` |
| N-ČOK.JAJE MICKEY MOUSE 20GRATTOUILLE -48/1- | 14 | `cok\b` |
| ČOKOLADNO JAJE HOT WHEELS 20g ZAINI | 12 | `coko` |
| N-ČOK.JAJE PRINCES -SHIMMERiSHINE20G -48/1- | 11 | `cok\b` |
| N-FERRERO KINDER JOY 20G JAJE IZNENAĐENJA -72/2/1- -24/1- | 8 | `ferrero` |

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

<details><summary>Najčešće isključeni (top 5)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| LUK REZANI 3000G TERMIČKI OBRAĐEN -5/1- VREĆA | 6 | `termick` |
| LUK KOCKICE SMRZNUTI 2,5KG LEDO | 4 | `smrz` |
| ZAČIN LUK PRŽENI 1000 g KOTANY | 4 | `przeni` |
| IGRAČKA LUK I STRIJELA AY32-1A NIRD | 3 | `igrack` |
| LUK DINSTANI 3 kg C.A.K. | 3 | `dinst` |

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

<details><summary>Najčešće isključeni (top 5)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| PEKARSKI KRUMPIR, KRIŠKE S KOROM 2,5 KG LEDO | 9 | `pekarsk` |
| KRUMPIR PEKARSKI ZAČINJENI 750g LEDO | 8 | `pekarsk` |
| KROKETI KRUMPIROVI 2,5kg LEDO | 4 | `ledo` |
| KRUMPIR KRIŠKE JACKET WEDGES 2500 g ( ZAPRIMATI NA KG ) | 4 | `kriske` |
| KRUMPIR PIRE 3KG VR PODRAVKA (1) | 4 | `pire` |

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

<details><summary>Najčešće isključeni (top 5)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| COKOLADA MLIJECNA COKOLADA RIZA 26 G DORINA | 17 | `cokolad` |
| KREKER OD RIZE SA SJEMENKAMA 100 G B.YOND-LIVITY | 13 | `kreker` |
| TJESTENINA OD RIŽE RICE VERMICELLI 250G YOUWOK | 13 | `tjestenin` |
| ČIPS OD RIŽE SIR CHEDDAR I CHUTNEY 60 g B. YOND LIVITY | 13 | `cips` |
| KREKER OD RIŽE SA SEZAMOM BEZ GLUTENA 100 g (12) | 12 | `kreker` |

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

<details><summary>Najčešće isključeni (top 5)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| JUHA BISTRA S TJESTENINOM VREĆICA 45 g PODRAVKA | 18 | `juha` |
| TALIANETTA MAKARONI BOLOGNESE VR.160G (12) PODRAVKA | 18 | `tal?ianetta` |
| ARGETA SALATA PILETINA TJESTENINA 160 G ATLANTIC | 16 | `piletin` |
| TALIANETTA TJESTENINA SA 4 SIRA VR.145G (12) PODRAVKA | 15 | `tal?ianetta` |
| GOVEĐA JUHA S TJESTENINOM 65G (35) (PAL 108), PODRAVKA | 13 | `juha` |

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

<details><summary>Najčešće isključeni (top 5)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| KONCENTRAT RAJČICE ST. PODRAVKA 720 g (12) | 16 | `koncentr` |
| RAJČICA KONCENTRAT 4500G 28-30% LIM. PODRAVKA | 14 | `koncentr` |
| RAJČICA PASIRANA 3X200G,PODRAVKA (8) (PAL 120) | 14 | `pasir` |
| RAJČICA MUTTI 700G PASIRANA BOCA-12/1- 63070 | 13 | `mutti` |
| RAJČICA PODR 680G PASSATA -12/1- PASIRANA BOCA | 12 | `pasir` |

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

<details><summary>Najčešće isključeni (top 5)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| VAFEL KAKAO PRUTICI FRONDI 250 G KRAS | 23 | `vafel` |
| KEKS KAROLINA 288G MOTO KAKAO -18/1- | 20 | `keks` |
| PREKRAŠNI KOLAČIĆI KEKS KAKAO 220G (10) (PAL40) KRAŠ | 20 | `keks` |
| DORINA ČOKOLADICA KREM KAKAO 38 g (24) | 19 | `cokolad` |
| LEDOLETTA KAKAO KREM 800g | 19 | `krem\b` |

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

<details><summary>Najčešće isključeni (top 5)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| SJEME PERSIN GIGANTE | 1 | `sjeme` |
| SJEME PERSIN KORIJENAS | 1 | `sjeme` |
| SJEME PERSIN LISNATI | 1 | `sjeme` |

</details>

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

<details><summary>Najčešće isključeni (top 5)</summary>

| naziv | lanaca | isključio |
|---|---|---|
| SALAMA PILEĆA PRSA U OVITKU 500 g VINDIJA | 17 | `salam` |
| PILEĆA PRSA 220 g POLI KIDS PERUTNINA | 14 | `kids` |
| N-VIN.PIL.FILE ZABATAK 500G (PODLOŽAK) | 13 | `zabatak` |
| SALAMA SLIM&FIT PILEĆA PRSA 400G | 11 | `salam` |
| DIMLJENA PILECA PRSA NAREZAK 100 G PERUTNINA | 8 | `narezak` |

</details>
