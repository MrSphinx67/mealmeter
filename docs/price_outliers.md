# Odbačene cijene po namirnici

Generirano skriptom `scripts/staple_reports.py` iz arhive 2026-10-19. Za svaku namirnicu s više od 5 %
cijena izvan granica (`price_suspect`) ispisano je 15 grupa proizvoda s najviše odbačenih cijena.
Granice su ručne (`plausible_per_unit` u staples.yaml), po vrećici (`plausible_per_pack`: skupo iznad
gornje, jeftino samo pojedinačna vrećica ispod donje) ili automatske (0,25x–4x medijana namirnice).
Odbačena cijena ne ulazi u raspon cijena ni u plan_basket. Česte odbačene grupe obično su krivi pogoci
rječnika (→ `must_not_match`) ili krivo pročitana gramatura.

| namirnica | granice | €/jed | odbačeno | od | % |
|---|---|---|---|---|---|
| banana | auto | 0,37–5,96 /kg | 154 | 3255 | 4.7 |
| brasno | manual | 0,40–6,00 /kg | 318 | 40707 | 0.8 |
| cesnjak | auto | 1,15–18,36 /kg | 19 | 2876 | 0.7 |
| cokolada_za_kuhanje | auto | 4,66–74,52 /kg | 35 | 9340 | 0.4 |
| dodatak_jelima | auto | 2,35–37,52 /kg | 362 | 19135 | 1.9 |
| endivija | auto | 1,11–17,80 /kg | 4 | 223 | 1.8 |
| gljive | auto | 1,04–16,72 /kg | 23 | 5736 | 0.4 |
| grah | auto | 0,74–11,80 /kg | 412 | 34459 | 1.2 |
| grasak | auto | 0,93–14,92 /kg | 87 | 15871 | 0.5 |
| griz | auto | 0,80–12,72 /kg | 76 | 3295 | 2.3 |
| jabuka | auto | 0,42–6,76 /kg | 40 | 20475 | 0.2 |
| jaja | manual | 0,19–0,47 /kom | 2285 | 15365 | 14.9 |
| jogurt | auto | 0,86–13,72 /kg | 192 | 59574 | 0.3 |
| junetina | auto | 3,37–53,96 /kg | 13 | 8225 | 0.2 |
| kakao | auto | 5,72–91,60 /kg | 20 | 5554 | 0.4 |
| kecap | auto | 0,99–15,92 /kg | 828 | 21274 | 3.9 |
| kiseli_kupus | auto | 0,55–8,72 /kg | 212 | 9396 | 2.3 |
| kiselo_vrhnje | auto | 1,25–19,96 /kg | 29 | 20873 | 0.1 |
| koncentrat_rajcice | auto | 2,73–43,60 /kg | 40 | 5800 | 0.7 |
| krastavac | auto | 0,47–7,56 /kg | 1 | 3471 | 0.0 |
| krumpir | auto | 0,23–3,72 /kg | 125 | 12875 | 1.0 |
| krusne_mrvice | auto | 0,95–15,28 /kg | 449 | 9040 | 5.0 |
| kukuruz | auto | 1,31–21,04 /kg | 52 | 13403 | 0.4 |
| kupus | auto | 0,20–3,16 /kg | 169 | 5700 | 3.0 |
| kvasac | pack | 0,30–1,25 /vrecica | 156 | 12364 | 1.3 |
| leca | auto | 0,94–15,12 /kg | 339 | 8589 | 3.9 |
| limun | auto | 0,50–7,96 /kg | 126 | 5456 | 2.3 |
| luk | auto | 0,31–5,00 /kg | 757 | 13450 | 5.6 |
| majoneza | auto | 3,13–50,04 /kg | 90 | 27363 | 0.3 |
| margarin | auto | 1,19–19,04 /kg | 11 | 18547 | 0.1 |
| maslac | manual | 6,00–40,00 /kg | 991 | 20393 | 4.9 |
| maslinovo_ulje | manual | 4,00–60,00 /l | 130 | 29159 | 0.4 |
| matovilac | auto | 1,50–24,00 /kg | 1 | 455 | 0.2 |
| med | auto | 3,05–48,80 /kg | 646 | 32125 | 2.0 |
| mlijeko | manual | 0,50–4,00 /l | 1126 | 39919 | 2.8 |
| mljevena_paprika | auto | 4,62–74,00 /kg | 32 | 12476 | 0.3 |
| mljeveno_meso | auto | 2,22–35,48 /kg | 1 | 8120 | 0.0 |
| mozzarella | auto | 3,49–55,80 /kg | 8 | 17544 | 0.0 |
| mrkva | auto | 0,32–5,16 /kg | 285 | 6700 | 4.3 |
| naranca | auto | 0,37–5,96 /kg | 92 | 5178 | 1.8 |
| ocat | auto | 0,35–5,56 /l | 593 | 14281 | 4.2 |
| palenta | auto | 0,59–9,52 /kg | 20 | 8838 | 0.2 |
| papar | auto | 12,81–205,00 /kg | 856 | 30386 | 2.8 |
| paprika | auto | 0,75–11,96 /kg | 114 | 13789 | 0.8 |
| parmezan | auto | 6,47–103,60 /kg | 1 | 6680 | 0.0 |
| pasirana_rajcica | auto | 0,69–11,12 /kg | 27 | 15661 | 0.2 |
| persin | auto | 1,59–25,44 /kg | 8 | 1796 | 0.4 |
| pileca_prsa | manual | 5,00–20,00 /kg | 528 | 10613 | 5.0 |
| piletina | auto | 1,20–19,16 /kg | 461 | 24432 | 1.9 |
| prasak_za_pecivo | pack | 0,10–0,40 /vrecica | 21 | 6024 | 0.3 |
| radic | auto | 1,25–19,96 /kg | 0 | 1249 | 0.0 |
| rajcica | auto | 0,88–14,00 /kg | 97 | 12076 | 0.8 |
| rajcica_konzerva | auto | 0,89–14,16 /kg | 37 | 14103 | 0.3 |
| riza | auto | 0,97–15,56 /kg | 268 | 47173 | 0.6 |
| rukola | auto | 1,50–24,00 /kg | 0 | 632 | 0.0 |
| secer | manual | 0,60–8,00 /kg | 369 | 17665 | 2.1 |
| senf | auto | 2,42–38,76 /kg | 676 | 19919 | 3.4 |
| slanina | auto | 5,35–85,56 /kg | 1124 | 32933 | 3.4 |
| slanutak | auto | 0,94–15,12 /kg | 322 | 9557 | 3.4 |
| slatko_vrhnje | auto | 2,49–39,80 /l | 2 | 1959 | 0.1 |
| sol | manual | 0,20–8,00 /kg | 802 | 17144 | 4.7 |
| spinat | auto | 0,90–14,32 /kg | 135 | 4834 | 2.8 |
| sunka | auto | 3,85–61,56 /kg | 2951 | 63224 | 4.7 |
| svinjetina | auto | 1,47–23,56 /kg | 158 | 13606 | 1.2 |
| svjezi_sir | auto | 1,61–25,80 /kg | 155 | 19675 | 0.8 |
| tikvica | auto | 0,42–6,76 /kg | 23 | 2886 | 0.8 |
| tjestenina | auto | 0,94–15,12 /kg | 1889 | 118896 | 1.6 |
| tuna | auto | 5,20–83,12 /kg | 225 | 47378 | 0.5 |
| tvrdi_sir | auto | 3,65–58,40 /kg | 487 | 72309 | 0.7 |
| ulje | manual | 1,00–12,00 /l | 585 | 13817 | 4.2 |
| vanilin_secer | pack | 0,10–0,85 /vrecica | 176 | 9639 | 1.8 |
| vrhnje_za_kuhanje | auto | 1,65–26,32 /l | 0 | 7578 | 0.0 |
| zelena_salata | auto | 0,83–13,28 /kg | 0 | 830 | 0.0 |
| zobene_pahuljice | auto | 0,74–11,92 /kg | 288 | 7467 | 3.9 |

## jaja (`jaja`): 14.9 % odbačeno, granice 0,19–0,47 €/kom

| naziv | odbačenih cijena | lanaca | €/jed (medijan) | raspon | pakiranje |
|---|---|---|---|---|---|
| Lukač Jaja podni uzgoj, razred S | 118 | 2 | 0,12 | 0,11–0,12 | 20 kom |
| Kones Bi Jaja, razred M | 116 | 1 | 0,14 | 0,14–0,14 | 10 kom |
| Jaja | 116 | 1 | 0,15 | 0,15–0,15 | 10 kom |
| Gala Jaja iz podnog uzgoja | 116 | 1 | 0,15 | 0,15–0,15 | 10 kom |
| Žito Jaja iz podnog uzgoja razred S | 116 | 1 | 0,16 | 0,16–0,16 | 10 kom |
| Jaja razred M | 116 | 1 | 0,18 | 0,18–0,18 | 30 kom |
| Žito Jaja razred S | 116 | 1 | 0,18 | 0,18–0,18 | 10 kom |
| Žito Jaja razred M | 116 | 1 | 0,15 | 0,15–0,15 | 18 kom |
| PERFA Jaja podni uzgoj razred M | 116 | 1 | 0,15 | 0,15–0,15 | 15 kom |
| Lukač Jaja, razred S | 116 | 1 | 0,17 | 0,17–0,17 | 30 kom |
| Piko Jaja razred S, Klasa A | 116 | 1 | 0,18 | 0,18–0,18 | 10 kom |
| Jaja iz kaveznog uzgoja, razred "S" | 116 | 1 | 0,10 | 0,10–0,10 | 10 kom |
| Jaja razred M, klasa A, 30 komada | 116 | 1 | 0,15 | 0,15–0,15 | 30 kom |
| Oregon Jaja iz kaveznog uzgoja | 116 | 1 | 0,15 | 0,15–0,15 | 30 kom |
| JAJA M RAZRED 6/1 PODNI UZGOJ VRANA | 87 | 1 | 0,51 | 0,48–0,53 | – |

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
