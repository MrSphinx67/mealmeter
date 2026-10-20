# Pregled za razgovor: Korak 2F (arhiva 2026-10-20; `scripts/review_2f.py`, odluke 81–86)

## 1. Lažni EAN-ovi

Po lancu i razlogu (EAN-ova, proizvoda): eurospin dummy_list: 1 / 83; plodine repeated_digit: 1 / 1. Eurospinove mrkve i krumpir više nemaju begonija (`test_eurospin_no_begonia`).

## 2. i 3. Testovi

- „špageti“ ne vraća „TJESTENINA BUCATINI 500 G RISCOSSA“; proizvod bez traženog oblika ispada: prolazi (2 passed in 2.88s)
- „KRASTAVAC SALATAR kom“ (globalni EAN, na komad) je krastavac, „PAPRIKA AJVAR kom“ nije: prolazi (1 passed in 1.75s)

Lijevak, konačno (zbroj 8 lanaca), prije → poslije točke 3: rajcica 54 → 54, mrkva 41 → 41, krastavac 30 → 37, luk 43 → 48, paprika 77 → 77, tikvica 23 → 23. Po fazama: `docs/data/funnel_*_2f3.json`.

## 4. Slabi članovi koji izgledaju krivo (38 od 446; riječ namirnice nije među prve tri ni u jednom nazivu)

| namirnica | nazivi po lancu |
|---|---|
| tjestenina | kaufland: Farina Speciale Krupica durum 1 kg; konzum: KRUPICA DURUM ZA TJEST 1 kg FARINA |
| tjestenina | trgovina-krk: CJEDILO ZA RIŽU I TJESTENINU 25X13 KB; gavranovic: CJEDILO ZA RIŽU |
| riza | stridon: PENNE RIGATE MAIS/RISO 400 GR (12) DIVELLA (IT); ntl: TJESTENINA PENNE ZITI RIGATE BEZ GLUTENA 4 |
| jogurt | trgocentar: MED.LAMBERTZ CRISPY WAFERS WITH LIME YOGURTCREAM 200G (30); djelo_vodice: LAMBERTZ WAFER YOGU |
| maslac | studenac: KEKS GALETTES 130 g; plodine: KEKS GALETTES 130 G BONNE MAMAN; lorenco: LA GALETTE ALL BUTTER S |
| papar | spar: TUNA RIO MARE LIMUN PAP.3X65 g; konzum: TUNJ U MASL ULJ LIMUN PAPAR 3X52g RM |
| maslac | konzum: PECIVO GOLOSINI S MARELICOM 200G RUGGERI; ntl: PECIVO GOLOSINI S MASLACEM I PUNJENJEM OD MARELICE |
| tjestenina | dm: ALB-GOLD eko fusilli od heljde bg 250 g; spar: TJES.HELJDA ALB GOLD BG.250 g |
| tvrdi_sir | kaufland: Le Rustique Sir polutv.Raclette26%mm140g; plodine: SIR RACLETTE REZANI 140 G LE RUSTIQUE; konzu |
| margarin | studenac: KORA ZA BAKLAVU RAMA 500 g; kaufland: Ana Kore za baklavu 500 g; konzum: KORA ZA BAKLAVU 500g A |
| sunka | metro: 500GR VINDON DELUXE ŠUNKA NARE; trgocentar: DELUXE PILEĆA CLASSIC 500G |
| mlijeko | plodine: SISAC ANTI-COLIK SILIKON 2/2 MLIJEKO; kaufland: Baby Nova sisač anti-kolik ml vel 2 2/1; tommy:  |
| med | ribola: AIRW.LIQ.DROP.33,5 g LIM/MED; plodine: AIRWAV.HONEY LEM.DR. 33,5 G |
| maslac | ribola: PETIT BEUR.PRE.250 g KOESTLIN; stridon: PREMIUM PETIT BEU. 13% MASLACA KOESTLIN 250 g (16) |
| ocat | bure: LUK 1550 g SREDNJI CITRES; stridon: CITRES LUK SREDNJI U OCTU 1550 g; metro: 1550G CITRES LUK SREDN |
| tjestenina | dm: ALB-GOLD eko fusilli kukur/riža bg 250 g; spar: TJES.KUK.RIŽA ALB GO.BG.250 g |
| med | ntl: ŽARDINJERA S POD. LM 40 MEDIT. SMEĐA; trgovina-krk: ŽARDINJERA S PODM. L40 CM MED-SMEĐA |
| tvrdi_sir | vrutak: SIR S MASLINAMA 125G GLIGORA POLUTVRDI KRAVLJI -12/1; lorenco: SIR S MASLINAMA 125g GLIGORA; spar |
| riza | trgovina-krk: SHAKER + BOJA + MAGIČNA RIŽA ORIO; ntl: MAGIČNI USKRŠNJI SHAKER 7/1 |
| maslac | konzum: PECIVO GOLOSINI S ČOKOLADOM 200G RUGGERI; ntl: MINI CROASANI S MASLACEM PUNJENI ČOKOLADOM 200 g G |

## 6. Lidl: mlijeko, ulje, brašno, šećer (unit_suspect: pack_source unit i omjer izvan 0.6–1.6x medijana)
Ukupno je `unit_suspect` 267 Lidlovih proizvoda. **Pogađa i ispravne jeftine** (trajno mlijeko 0,52 €/l, kristal šećer): prijedlog je 0,3–3x.

| namirnica | naziv | unit | izvor | kom | €/jed | omjer | suspect |
|---|---|---|---|---|---|---|---|
| brasno | Bio brašno od pira SK2 | 1kg | unit | 1 | 1,99 | 2,40 | DA |
| brasno | Brašno TIP 400 oštro, 1kg | 1kg | name | 1 | 0,75 | 0,90 |  |
| brasno | Brašno TIP 400 oštro, 5kg | 5kg | name | 1 | 0,56 | 0,67 |  |
| brasno | Brašno TIP 550 glatko, 1kg | 1kg | name | 1 | 0,75 | 0,90 |  |
| brasno | Brašno TIP 550 glatko, 5kg | 5kg | name | 1 | 0,72 | 0,87 |  |
| brasno | Brašno tip 550 glatko | 3000g | unit | 1 | 0,55 | 0,66 | DA |
| brasno | Brašno tip 550 glatko | 4x1kg | unit | 1 | 0,54 | 0,65 | DA |
| brasno | Integralno brašno | 1kg | unit | 1 | 0,99 | 1,19 |  |
| brasno | Kukuruzno brašno, 1kg | 1kg | name | 1 | 0,99 | 1,19 |  |
| brasno | Pirovo brašno tip 630 | 1kg | unit | 1 | 1,29 | 1,55 |  |
| mlijeko | 'z bregov Mlij. pr. nap. čoko-kiki. | 500ml | unit | 1 | 3,98 | 2,74 | DA |
| mlijeko | 'z bregov Svježe mlijeko 1,5% m.m. | 1l | unit | 1 | 1,45 | 1,00 |  |
| mlijeko | 'z bregov Svježe mlijeko 3,2% m.m. | 1l | unit | 1 | 1,49 | 1,03 |  |
| mlijeko | 'z bregov Svježe mlijeko 3,2% m.m. | 1,75l | unit | 1 | 1,37 | 0,94 |  |
| mlijeko | 'z bregov Trajno mlijeko | 2l | unit | 1 | 0,84 | 0,58 | DA |
| mlijeko | 'z bregov Trajno mlijeko 2,8% m.m. | 1l | unit | 1 | 1,02 | 0,70 |  |
| mlijeko | Dukat Trajno mlijeko 2,8%, 1l-boca | 1l | name | 1 | 1,19 | 0,82 |  |
| mlijeko | ESL - Svježe mlijeko 3,2% | 1l | unit | 1 | 0,99 | 0,68 |  |
| mlijeko | Kravica Kraljica UHT mlijeko 2,8% | 1l | unit | 1 | 0,69 | 0,48 | DA |
| mlijeko | Križevačka mljekara Trajno mlijeko | 1l | unit | 1 | 0,52 | 0,36 | DA |
| mlijeko | Milkland trajno mlijeko 2,8% | 1l | unit | 1 | 0,39 | 0,27 | DA |
| mlijeko | Mozzarella od bivoljeg mlijeka | 500g | unit | 1 | - | - |  |
| mlijeko | Namaz od obranog mlijeka i kakaa | 750g | unit | 1 | - | - |  |
| mlijeko | Svježe mlijeko 3,2% m.m. | 1l | unit | 1 | 1,15 | 0,79 |  |
| mlijeko | Trajno mlijeko 1,5% | 1l | unit | 1 | 0,95 | 0,66 |  |
| mlijeko | Trajno mlijeko 2,8% | 1l | unit | 3 | 0,44–0,54 | 0,37 | DA |
| mlijeko | Trajno mlijeko 2,8% AK | 1l | unit | 1 | 0,67 | 0,46 | DA |
| mlijeko | Trajno mlijeko 2,8% m.m. | 1l | unit | 3 | 0,65–0,71 | 0,49 | DA |
| mlijeko | Trajno mlijeko 3,5% | 1l | unit | 1 | 1,09 | 0,75 |  |
| mlijeko | Trajno mlijeko bez lakt. 1,5% m.m. | 1l | unit | 1 | 1,29 | 0,89 |  |
| mlijeko | Trajno mlijeko bez laktoze 2,8%m.m | 1l | unit | 1 | 1,49 | 1,03 |  |
| secer | Agragold Šećer | 1kg | unit | 1 | 0,99 | 0,26 | DA |
| secer | Agragold Šećer u kocki | 0,5kg | unit | 1 | 1,98 | 0,52 | DA |
| secer | Agragold Šećer u prahu | 500g | unit | 1 | 1,30 | 0,34 | DA |
| secer | Kiara Kristal šećer 1kg | 1kg | name | 1 | 0,99 | 0,26 |  |
| secer | Smeđi šećer | 500g | unit | 1 | 1,98 | 0,52 | DA |
| secer | Viro Kristalni šećer | 1kg | unit | 1 | 0,75 | 0,20 | DA |
| secer | Šećer u kocki | 500g | unit | 1 | 2,58 | 0,68 |  |
| secer | Šećer u prahu | 500g | unit | 1 | 1,98 | 0,52 | DA |
| ulje | Maria Orginal XXL (suncokret. ulje) | 5x200g | unit | 1 | - | - |  |
| ulje | Oljarna Petovar Salatno ulje | 1l | unit | 1 | 3,49 | 2,07 | DA |
| ulje | Sunce Vinkovaca Hl. preš. sunc.ulje | 1l | unit | 1 | 2,29 | 1,36 |  |
| ulje | Suncokretovo ulje | 1l | unit | 2 | 1,49 | 0,88 |  |
| ulje | Tena suncokretovo ulje | 1l | unit | 1 | 1,45 | 0,86 |  |
| ulje | Zvijezda Suncokretovo ulje | 1,2l | unit | 1 | 1,54 | 0,91 |  |
| ulje | Zvijezda Suncokretovo ulje | 1l | unit | 1 | 1,69 | 1,00 |  |
| ulje | Zvijezda Suncokretovo ulje | 4x1l | unit | 1 | 1,50 | 0,89 |  |
| ulje | Zvijezda Suncokretovo ulje RETRO | 1,2l | unit | 1 | 1,54 | 0,91 |  |

## Košarice u Osijeku

**Palačinke (4 osobe)**: kaufland, Josipa Reihl-Kira 40 · 7/7 · total_to_buy **6,07 €**, total_used 1,31 € · 20.10.2026.
Stavke (cost_pack/cost_used €): brašno glatko: KLC.NMNP.Brašno glatko pšen.T- 0,75/0,19; mlijeko: Rosa trajno mlijeko 2,8% 1 L_O 0,65/0,33; jaja: KONES BI Jaja M razred 10/1 1,85/0,55; šećer: Agragold Šećer kristal 1kg_OC 0,65/0,01; sol: Sol tuzlanska sitna 500 g 0,49/0,00; ulje: KLC.Suncokretovo ulje 1L PET_O 1,49/0,04; vanilin šećer: Dolcela Vanilin šećer 8g 0,19/0,19.

**Špageti bolonjez (4 osobe)**: konzum, Trg Ante Starčevića 10 · 7/7 · total_to_buy **14,33 €**, total_used 7,69 € · 20.10.2026.
Stavke (cost_pack/cost_used €): špageti: TIJESTO SPAGHETTI 400g GRANO D 0,80/0,80; mljeveno meso: MIJEŠANO MLJEVENO MESO 750 g K 4,39/2,93; rajčica: RAJČICA PASIR GARDEN GOOD 700  1,69/1,69; luk: LUK CRVENI 0,12/0,12; maslinovo ulje: ULJE MASLIN EX DJ TRAD 0.25L O 3,99/0,72; parmezan: SIR TVRDI GRANA PADANO LISTIĆI 2,85/1,43; sol: SOL KAMENA VREĆ 1 kg SLOVA 0,49/0,00.
