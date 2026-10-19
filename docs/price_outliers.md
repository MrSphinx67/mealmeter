# Odbačene cijene po namirnici

Generirano skriptom `scripts/staple_reports.py` iz arhive 2026-10-19. Za svaku namirnicu s više od 5 %
cijena izvan granica (`price_suspect`) ispisano je 15 grupa proizvoda s najviše odbačenih cijena.
Granice su ručne (`plausible_per_unit` u staples.yaml) ili automatske (0,25x–4x medijana namirnice).
Odbačena cijena ne ulazi u raspon cijena ni u plan_basket. Česte odbačene grupe obično su krivi pogoci
rječnika (→ `must_not_match`) ili krivo pročitana gramatura.

| namirnica | granice | €/jed | odbačeno | od | % |
|---|---|---|---|---|---|
| banana | auto | 0,37–5,96 /kg | 154 | 3255 | 4.7 |
| brasno | manual | 0,40–6,00 /kg | 312 | 39703 | 0.8 |
| cesnjak | auto | 1,15–18,46 /kg | 19 | 2880 | 0.7 |
| cokolada_za_kuhanje | auto | 4,66–74,52 /kg | 35 | 9372 | 0.4 |
| dodatak_jelima | auto | 2,35–37,52 /kg | 362 | 19135 | 1.9 |
| endivija | auto | 1,11–17,80 /kg | 4 | 223 | 1.8 |
| gljive | auto | 1,04–16,72 /kg | 23 | 5736 | 0.4 |
| grah | auto | 0,74–11,80 /kg | 412 | 34459 | 1.2 |
| grasak | auto | 0,93–14,92 /kg | 87 | 15879 | 0.5 |
| griz | auto | 0,80–12,72 /kg | 76 | 3295 | 2.3 |
| jabuka | auto | 0,42–6,76 /kg | 40 | 20475 | 0.2 |
| jaja | manual | 0,10–1,50 /kom | 316 | 15530 | 2.0 |
| jogurt | auto | 0,86–13,72 /kg | 192 | 59574 | 0.3 |
| junetina | auto | 3,37–53,96 /kg | 13 | 8225 | 0.2 |
| kakao | auto | 2,94–47,08 /kg | 362 | 22777 | 1.6 |
| kecap | auto | 0,99–15,92 /kg | 828 | 21361 | 3.9 |
| kiseli_kupus | auto | 0,55–8,72 /kg | 212 | 9396 | 2.3 |
| kiselo_vrhnje | auto | 1,25–19,96 /kg | 29 | 20873 | 0.1 |
| koncentrat_rajcice | auto | 2,73–43,60 /kg | 40 | 5800 | 0.7 |
| krastavac | auto | 0,47–7,56 /kg | 1 | 3471 | 0.0 |
| krumpir | auto | 0,23–3,72 /kg | 125 | 12875 | 1.0 |
| krusne_mrvice | auto | 0,95–15,28 /kg | 449 | 9040 | 5.0 |
| kukuruz | auto | 1,31–21,04 /kg | 52 | 13403 | 0.4 |
| kupus | auto | 0,20–3,16 /kg | 169 | 5700 | 3.0 |
| kvasac | auto | 0,11–1,76 /vrecica | 2250 | 12364 | 18.2 |
| leca | auto | 0,94–15,12 /kg | 339 | 8589 | 3.9 |
| limun | auto | 0,50–7,96 /kg | 126 | 5456 | 2.3 |
| luk | auto | 0,31–5,00 /kg | 757 | 13450 | 5.6 |
| majoneza | auto | 3,13–50,04 /kg | 90 | 27363 | 0.3 |
| margarin | auto | 1,19–19,04 /kg | 11 | 18547 | 0.1 |
| maslac | manual | 6,00–40,00 /kg | 991 | 20393 | 4.9 |
| maslinovo_ulje | manual | 4,00–60,00 /l | 130 | 29159 | 0.4 |
| matovilac | auto | 1,50–24,00 /kg | 1 | 455 | 0.2 |
| med | auto | 3,05–48,80 /kg | 799 | 32429 | 2.5 |
| mlijeko | manual | 0,50–4,00 /l | 1155 | 40489 | 2.9 |
| mljevena_paprika | auto | 4,62–74,00 /kg | 32 | 12476 | 0.3 |
| mljeveno_meso | auto | 2,22–35,48 /kg | 1 | 8120 | 0.0 |
| mozzarella | auto | 3,49–55,80 /kg | 8 | 17544 | 0.0 |
| mrkva | auto | 0,32–5,16 /kg | 285 | 6700 | 4.3 |
| naranca | auto | 0,37–5,96 /kg | 92 | 5178 | 1.8 |
| ocat | auto | 0,35–5,56 /l | 593 | 14537 | 4.1 |
| palenta | auto | 0,59–9,52 /kg | 20 | 8838 | 0.2 |
| papar | auto | 12,81–205,00 /kg | 856 | 30386 | 2.8 |
| paprika | auto | 0,75–11,96 /kg | 114 | 13789 | 0.8 |
| parmezan | auto | 6,47–103,60 /kg | 1 | 6680 | 0.0 |
| pasirana_rajcica | auto | 0,69–11,12 /kg | 27 | 15661 | 0.2 |
| pileca_prsa | auto | 2,37–37,96 /kg | 4 | 11275 | 0.0 |
| piletina | auto | 1,20–19,16 /kg | 461 | 24432 | 1.9 |
| prasak_za_pecivo | auto | 0,04–0,72 /vrecica | 10 | 6024 | 0.2 |
| radic | auto | 1,25–19,96 /kg | 0 | 1249 | 0.0 |
| rajcica | auto | 0,88–14,00 /kg | 97 | 12076 | 0.8 |
| rajcica_konzerva | auto | 0,89–14,16 /kg | 37 | 14103 | 0.3 |
| riza | auto | 0,97–15,56 /kg | 268 | 47623 | 0.6 |
| rukola | auto | 1,50–24,00 /kg | 0 | 632 | 0.0 |
| secer | manual | 0,60–8,00 /kg | 369 | 17665 | 2.1 |
| senf | auto | 2,42–38,76 /kg | 676 | 19919 | 3.4 |
| slanina | auto | 5,35–85,56 /kg | 1124 | 32933 | 3.4 |
| slanutak | auto | 0,94–15,12 /kg | 322 | 9557 | 3.4 |
| slatko_vrhnje | auto | 2,49–39,80 /l | 2 | 1959 | 0.1 |
| sol | manual | 0,20–8,00 /kg | 803 | 15748 | 5.1 |
| spinat | auto | 0,90–14,32 /kg | 135 | 4834 | 2.8 |
| sunka | auto | 3,85–61,56 /kg | 2951 | 63225 | 4.7 |
| svinjetina | auto | 1,47–23,56 /kg | 158 | 13606 | 1.2 |
| svjezi_sir | auto | 1,61–25,80 /kg | 155 | 19675 | 0.8 |
| tikvica | auto | 0,42–6,76 /kg | 23 | 2886 | 0.8 |
| tjestenina | auto | 0,94–15,12 /kg | 1889 | 118896 | 1.6 |
| tuna | auto | 5,20–83,12 /kg | 225 | 47378 | 0.5 |
| tvrdi_sir | auto | 3,65–58,40 /kg | 487 | 72309 | 0.7 |
| ulje | manual | 1,00–12,00 /l | 586 | 13818 | 4.2 |
| vanilin_secer | auto | 0,04–0,72 /vrecica | 333 | 9674 | 3.4 |
| vrhnje_za_kuhanje | auto | 1,65–26,32 /l | 0 | 7578 | 0.0 |
| zelena_salata | auto | 0,83–13,28 /kg | 0 | 830 | 0.0 |
| zobene_pahuljice | auto | 0,74–11,92 /kg | 288 | 7467 | 3.9 |

## kvasac (`kvasac`): 18.2 % odbačeno, granice 0,11–1,76 €/vrecica

| naziv | odbačenih cijena | lanaca | €/jed (medijan) | raspon | pakiranje |
|---|---|---|---|---|---|
| KVASAC INSTANT 100 g DOLCELA | 446 | 13 | 0,09 | 0,08–0,10 | 100 g |
| KVASAC INSTANT 100 g DR.OETKER | 446 | 9 | 0,10 | 0,07–0,10 | 100 g |
| KVASAC INSTANT 450 g DOLCELA | 333 | 14 | 0,08 | 0,04–0,10 | 450 g |
| KVASAC SUHI 500 g DI-GO | 311 | 8 | 0,08 | 0,04–0,10 | 500 g |
| KVASAC INSTANT 450 g DR.OETKER | 251 | 8 | 0,08 | 0,06–0,10 | 450 g |
| SUHI KVAS 7 G DR.OETKER 50/1 | 155 | 1 | 0,01 | 0,01–0,01 | 350 g |
| KVASAC DI-GO INS.SUH.PEK.125 g | 129 | 2 | 0,10 | 0,09–0,10 | 125 g |
| BRAŠNO KARLA GLATKO T-550 1kg+DIGO KVASAC U LIMENCI | 38 | 1 | 0,01 | 0,01–0,01 | 1000 g |
| SUH.KVASAC 500g DORA MAYO | 37 | 2 | 0,06 | 0,04–0,07 | 500 g |
| KVASAC SV.42 g DR.OE TKER | 37 | 1 | 0,09 | 0,08–0,09 | 42 g |
| KVASAC SVJEŽI 500g FERMIPAN DUOS | 22 | 1 | 0,08 | 0,08–0,08 | 500 g |
| KVASAC 500G,KVASAC | 12 | 3 | 0,08 | 0,01–0,10 | 500 g |
| 42G DI-GO DOMAĆI SVJ. KVAS. | 7 | 1 | 19,50 | 19,50–19,50 | 42 g |
| 7GX5 DR.OETKER KVASAC(4+1) | 7 | 1 | 4,84 | 4,84–4,84 | 35 g |
| 42G DI-GO DOMAĆI SVJ. KVAS. | 7 | 1 | 24,49 | 24,49–24,49 | 42 g |

## luk (crveni/žuti) (`luk`): 5.6 % odbačeno, granice 0,31–5,00 €/kg

| naziv | odbačenih cijena | lanaca | €/jed (medijan) | raspon | pakiranje |
|---|---|---|---|---|---|
| LUK CRVENI SNIŽENJE | 343 | 1 | 0,20 | 0,20–0,25 | – |
| LUK MLADI VEZICA KOM | 167 | 1 | 7,42 | 7,42–7,42 | – |
| LUK MLADI | 120 | 1 | 7,69 | 7,69–8,79 | – |
| LUK BORETTANE RFS | 51 | 1 | 9,99 | 9,99–9,99 | – |
| MLADI LUK - KG | 21 | 1 | 6,21 | 6,21–6,21 | – |
| LUK MLADI | 13 | 1 | 6,29 | 6,29–6,29 | – |
| 500G LUK CHALOTA MR | 7 | 1 | 7,74 | 7,74–7,74 | 500 g |
| 500G LUK ECHALION | 6 | 1 | 6,68 | 6,68–6,68 | 500 g |
| 500G LUK CHATA | 6 | 1 | 6,78 | 6,78–6,78 | 500 g |
| 500G LUK GUARNICION | 5 | 1 | 5,28 | 5,28–5,28 | 500 g |
| LUK MLADI | 4 | 1 | 5,39 | 5,39–5,39 | – |
| LUK 1550 g SREDNJI CITRES | 3 | 1 | 6,32 | 6,19–6,32 | 1550 g |
| LUK MLADI SNIŽENJE | 2 | 1 | 5,70 | 5,61–5,78 | – |
| MLADI LUK | 2 | 1 | 5,39 | 5,39–5,39 | – |
| LUK MLADI AGROVIR | 1 | 1 | 5,25 | 5,25–5,25 | – |

## sol (`sol`): 5.1 % odbačeno, granice 0,20–8,00 €/kg

| naziv | odbačenih cijena | lanaca | €/jed (medijan) | raspon | pakiranje |
|---|---|---|---|---|---|
| HIMALAJSKA SOL 390 G CAPE HERB SPICE | 150 | 1 | 15,36 | 11,51–16,38 | 390 g |
| SOL HIMALAJSKA SITNA 250g ŠAFRAM | 134 | 6 | 11,16 | 9,00–11,96 | 250 g |
| Himalajska kamena sol | 116 | 1 | 9,50 | 9,50–9,50 | 420 g |
| GRUBA KRISTAL.MORSKA SOL-TULJAK 500 | 110 | 2 | 8,58 | 8,14–9,10 | 500 g |
| SOL SA SMANJ UDJEL NATRIJA 250g | 105 | 1 | 9,96 | 9,96–10,60 | 250 g |
| SITNA MORSKA SOL-TULJAK 500g BIO | 80 | 2 | 8,18 | 8,14–8,70 | 500 g |
| SOL GRUBO MLJEVENA 300 G STAKLO SOLANA NIN | 21 | 1 | 17,70 | 17,70–18,57 | 300 g |
| 1KG SOL.NIN SITNA KUH.SOL VR | 7 | 1 | 8,88 | 8,88–8,88 | 1000 g |
| 500G SOL. NIN BIO CVIJET SOLI | 7 | 1 | 32,26 | 32,26–32,26 | 500 g |
| 1KG SOL.PAG MORSKA KRUPNA VREĆ | 7 | 1 | 9,30 | 9,30–9,30 | 1000 g |
| 1KG SOL.PAG MORSKA SITNA VREĆ | 7 | 1 | 9,00 | 9,00–9,00 | 1000 g |
| 250G SOL. NIN BIO CVIJET SOLI | 7 | 1 | 490,00 | 490,00–490,00 | 250 g |
| 570G MALDON MORSKA SOL KRIST. | 7 | 1 | 30,68 | 30,68–30,68 | 570 g |
| 250G SOL. NIN BIO CVIJET SOLI | 7 | 1 | 49,00 | 49,00–49,00 | 250 g |
| 500G MALDON M.SOL KRIST.DIMLJ. | 7 | 1 | 49,98 | 49,98–49,98 | 500 g |
