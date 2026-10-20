# Pregled za razgovor: Korak 2D (arhiva 2026-10-20)

## Košarice u Osijeku (najbolja trgovina; generira `scripts/review_for_chat.py`, detalji u STEP2D_REVIEW.md)

**Palačinke (4 osobe)**: spar, Strossmayerova 167 · 7/7 sastojaka · ukupno 5,95 € (cijela pakiranja 6,94 €) · 20.10.2026.

| sastojak | proizvod | pakiranje | cost_pack € | cost_used € | pouzdanost |
|---|---|---|---|---|---|
| brašno glatko | BRAŠ.PŠ.GLATKO T-550 POD 1 kg | 1 x 1000 g | 0,69 | 0,17 | high/name |
| mlijeko | MLIJEKO UHT 2,8% Z BREGO.0,5 L | 1 x 500 ml | 0,99 | 0,99 | high/name |
| jaja | JAJA SPAR M RAZRED 6/1 | 1 x 6 kom | 1,59 | 0,80 | high/name |
| šećer | ŠEĆER KRISTAL S-BUDGET 1 kg | 1 x 1000 g | 0,99 | 0,01 | high/name |
| sol | SOL KUHINJ. TUZLA SITNA 250 g | 1 x 250 g | 0,99 | 0,00 | high/name |
| ulje | ULJE SUNCOKRET.S-BUDGET 1 L | 1 x 1000 ml | 1,49 | 0,04 | high/name |
| vanilin šećer | VANILIN ŠEĆER PODR.DOLCELA 8 g | 1 x 1 vrecica | 0,20 | 0,20 | high/name |

**Špageti bolonjez (4 osobe)**: lidl, Zeleno Polje 8 A · 7/7 sastojaka · ukupno 14,76 € (cijela pakiranja 15,73 €) · 20.10.2026.

| sastojak | proizvod | pakiranje | cost_pack € | cost_used € | pouzdanost |
|---|---|---|---|---|---|
| špageti | Špageti od durum pšenice 500g | 1 x 500 g | 0,89 | 0,71 | high/name |
| mljeveno meso | Mljeveno miješano meso LIGHT | 1 x 500 g | 4,79 | 4,79 | high/unit |
| rajčica | Pasirana rajčica "Rustica" | 1 x 720 g | 1,39 | 1,35 | high/unit |
| luk | Luk 750g | 1 x 750 g | 1,19 | 0,24 | high/name |
| maslinovo ulje | Maslinovo ulje SK4 | 1 x 500 ml | 4,49 | 0,40 | high/unit |
| parmezan | Grana padano 20mj. dozrijevan | 1 x 90 g | 1,99 | 1,11 | high/unit |
| sol | Pag 91 Kuh. morska sol sitna doz. | 1 x 250 g | 0,99 | 0,02 | high/unit |

- nije povezano: bosiljak (nepoznata namirnica 'bosiljak' (nema je u staples.yaml))

## Mjere i težine komada (data/units.yaml, sve procjene)

Mjere: zlica 15 ml, zlicica 5 ml, salica 250 ml, dcl 100 ml, prstohvat 0,5 ml, casa 200 ml.

| namirnica | g/ml | namirnica | g/ml | namirnica | g/ml |
|---|---|---|---|---|---|
| brasno | 0,55 | riza | 0,85 | mljevena_paprika | 0,45 |
| secer | 0,85 | kakao | 0,45 | papar | 0,50 |
| sol | 1,20 | med | 1,40 | ocat | 1,01 |
| ulje | 0,92 | prasak_za_pecivo | 0,80 | dodatak_jelima | 0,90 |
| mlijeko | 1,03 | griz | 0,65 | zobene_pahuljice | 0,36 |
| maslac | 0,95 | krusne_mrvice | 0,45 | persin | 0,25 |

| komad | g | komad | g | komad | g |
|---|---|---|---|---|---|
| persin (vezica) | 50 | paprika | 150 | krastavac | 300 |
| luk | 150 | tikvica | 250 | kupus (glavica) | 1500 |
| cesnjak (češanj) | 5 | jabuka | 180 | zelena_salata (glavica) | 400 |
| mrkva | 100 | limun | 120 | jaja | 60 |
| krumpir | 200 | naranca | 200 |  |  |
| rajcica | 120 | banana | 150 |  |  |

## Pokrivenost (točka 11)

Lanaca s barem jednim proizvodom u zadanom izboru, i broj proizvoda po lancu. „+Plod“ je procjena dobitka za Plodine uz strogo pozitivni `food_unverified` (nije primijenjeno).

| namirnica | lanaca | plodi | konzu | spar | lidl | kaufl | tommy | stude | euros | +Plod |
|---|---|---|---|---|---|---|---|---|---|---|
| brasno | 25 | 32 | 38 | 41 | 6 | 34 | 23 | 23 | 6 | 23 |
| secer | 25 | 5 | 4 | 5 | 3 | 5 | 5 | 7 | 4 | 3 |
| sol | 25 | 22 | 20 | 21 | 5 | 21 | 13 | 15 | 3 | 7 |
| ulje | 25 | 7 | 10 | 14 | 9 | 13 | 8 | 5 | 3 | 5 |
| maslinovo_ulje | 25 | 48 | 61 | 54 | 19 | 35 | 48 | 29 | 8 | 38 |
| maslac | 26 | 20 | 21 | 26 | 13 | 22 | 18 | 17 | 6 | 23 |
| margarin | 24 | 26 | 16 | 19 | 12 | 19 | 30 | 18 | 3 | 6 |
| mlijeko | 26 | 23 | 16 | 24 | 13 | 19 | 18 | 21 | 3 | 2 |
| jogurt | 26 | 57 | 63 | 54 | 49 | 76 | 60 | 41 | 22 | 27 |
| kiselo_vrhnje | 25 | 20 | 29 | 26 | 20 | 30 | 21 | 19 | 6 | 12 |
| vrhnje_za_kuhanje | 26 | 18 | 17 | 18 | 9 | 16 | 17 | 16 | 3 | 2 |
| slatko_vrhnje | 23 | 6 | 3 | 5 | 4 | 6 | 6 | 5 | 2 | 1 |
| svjezi_sir | 25 | 18 | 27 | 29 | 20 | 26 | 20 | 14 | 6 | 14 |
| tvrdi_sir | 25 | 51 | 151 | 82 | 48 | 73 | 76 | 78 | 34 | 11 |
| mozzarella | 25 | 11 | 15 | 19 | 22 | 18 | 27 | 9 | 11 | 18 |
| parmezan | 24 | 6 | 5 | 7 | 14 | 8 | 9 | 3 | 8 | 5 |
| jaja | 24 | 14 | 27 | 24 | 32 | 30 | 43 | 41 | 6 | 17 |
| luk | 21 | 1 | 3 | 4 | 7 | 7 | 4 | 5 | 2 | 4 |
| cesnjak | 20 | 0 | 1 | 2 | 3 | 2 | 2 | 3 | 1 | 3 |
| krumpir | 23 | 7 | 10 | 10 | 8 | 13 | 19 | 13 | 59 | 13 |
| rajcica | 19 | 0 | 3 | 7 | 4 | 5 | 9 | 8 | 4 | 6 |
| pasirana_rajcica | 25 | 30 | 27 | 20 | 8 | 21 | 25 | 18 | 5 | 13 |
| rajcica_konzerva | 24 | 18 | 24 | 25 | 4 | 16 | 20 | 13 | 4 | 8 |
| koncentrat_rajcice | 24 | 8 | 7 | 8 | 1 | 6 | 12 | 10 | 0 | 1 |
| mrkva | 22 | 0 | 5 | 4 | 4 | 6 | 8 | 5 | 62 | 3 |
| paprika | 21 | 1 | 8 | 11 | 9 | 8 | 11 | 8 | 5 | 14 |
| krastavac | 23 | 0 | 2 | 7 | 4 | 3 | 3 | 2 | 3 | 4 |
| tikvica | 19 | 0 | 2 | 2 | 3 | 2 | 4 | 2 | 4 | 1 |
| kupus | 19 | 0 | 4 | 6 | 4 | 4 | 4 | 5 | 3 | 3 |
| kiseli_kupus | 24 | 10 | 10 | 11 | 4 | 6 | 18 | 10 | 5 | 6 |
| zelena_salata | 18 | 0 | 1 | 1 | 1 | 6 | 6 | 4 | 6 | 0 |
| rukola | 9 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 2 | 0 |
| matovilac | 9 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 3 | 0 |
| radic | 17 | 0 | 2 | 2 | 1 | 1 | 1 | 4 | 7 | 1 |
| endivija | 12 | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 0 |
| spinat | 24 | 4 | 3 | 4 | 4 | 5 | 10 | 7 | 79 | 2 |
| persin | 15 | 0 | 0 | 1 | 1 | 0 | 1 | 1 | 1 | 2 |
| gljive | 23 | 2 | 4 | 7 | 3 | 3 | 10 | 12 | 77 | 5 |
| riza | 25 | 48 | 63 | 66 | 20 | 45 | 70 | 28 | 19 | 36 |
| tjestenina | 25 | 109 | 138 | 137 | 63 | 160 | 108 | 72 | 50 | 118 |
| griz | 23 | 7 | 1 | 3 | 2 | 2 | 3 | 3 | 1 | 3 |
| palenta | 25 | 9 | 12 | 13 | 3 | 7 | 18 | 11 | 4 | 5 |
| zobene_pahuljice | 25 | 16 | 13 | 10 | 4 | 9 | 11 | 11 | 2 | 5 |
| krusne_mrvice | 24 | 9 | 15 | 14 | 3 | 7 | 9 | 7 | 2 | 8 |
| kvasac | 26 | 11 | 13 | 10 | 5 | 12 | 10 | 8 | 3 | 0 |
| prasak_za_pecivo | 23 | 5 | 7 | 5 | 1 | 7 | 5 | 6 | 0 | 1 |
| vanilin_secer | 22 | 12 | 8 | 12 | 4 | 14 | 9 | 7 | 0 | 2 |
| kakao | 24 | 5 | 4 | 8 | 2 | 4 | 6 | 4 | 1 | 11 |
| cokolada_za_kuhanje | 23 | 5 | 9 | 6 | 5 | 5 | 8 | 3 | 2 | 2 |
| pileca_prsa | 23 | 5 | 15 | 13 | 5 | 9 | 15 | 18 | 32 | 5 |
| piletina | 23 | 16 | 38 | 25 | 16 | 32 | 31 | 63 | 80 | 10 |
| mljeveno_meso | 20 | 7 | 7 | 9 | 7 | 6 | 5 | 11 | 15 | 0 |
| svinjetina | 22 | 2 | 23 | 36 | 7 | 16 | 35 | 61 | 55 | 23 |
| junetina | 19 | 5 | 13 | 23 | 1 | 14 | 32 | 56 | 38 | 5 |
| slanina | 24 | 38 | 55 | 53 | 23 | 34 | 36 | 66 | 26 | 21 |
| sunka | 24 | 65 | 75 | 102 | 81 | 76 | 89 | 79 | 34 | 13 |
| tuna | 24 | 62 | 97 | 87 | 29 | 40 | 67 | 44 | 17 | 41 |
| grah | 25 | 29 | 49 | 38 | 14 | 31 | 31 | 24 | 11 | 40 |
| leca | 25 | 13 | 16 | 16 | 4 | 14 | 13 | 11 | 3 | 9 |
| slanutak | 25 | 12 | 17 | 15 | 4 | 11 | 15 | 12 | 3 | 10 |
| kukuruz | 25 | 12 | 14 | 23 | 9 | 14 | 19 | 12 | 3 | 10 |
| grasak | 26 | 15 | 16 | 20 | 7 | 16 | 25 | 18 | 6 | 16 |
| banana | 20 | 0 | 2 | 3 | 2 | 2 | 3 | 5 | 2 | 1 |
| jabuka | 21 | 1 | 13 | 21 | 14 | 22 | 23 | 20 | 73 | 23 |
| limun | 22 | 0 | 3 | 3 | 6 | 4 | 6 | 3 | 69 | 8 |
| naranca | 21 | 0 | 1 | 6 | 3 | 3 | 7 | 6 | 62 | 14 |
| papar | 25 | 43 | 48 | 58 | 5 | 45 | 56 | 38 | 7 | 20 |
| mljevena_paprika | 25 | 17 | 17 | 18 | 3 | 18 | 18 | 14 | 4 | 4 |
| dodatak_jelima | 25 | 21 | 29 | 25 | 7 | 16 | 25 | 18 | 3 | 8 |
| ocat | 25 | 17 | 15 | 16 | 4 | 13 | 16 | 11 | 2 | 8 |
| med | 25 | 53 | 66 | 42 | 9 | 30 | 44 | 29 | 5 | 31 |
| senf | 25 | 34 | 33 | 32 | 8 | 43 | 22 | 21 | 1 | 6 |
| majoneza | 25 | 39 | 28 | 38 | 18 | 37 | 48 | 35 | 6 | 8 |
| kecap | 25 | 19 | 28 | 27 | 8 | 24 | 26 | 17 | 3 | 11 |

## Dnevno ažuriranje (točka 13)

`scripts/update.py` uzima najnoviju arhivu iz /v0/list; zapis: `docs/data/update_2026-10-20.txt`.

```
  datum:           2026-10-20
  lanaca:          27
  trgovina:        1452
  proizvoda:       474121
  redaka cijena:   16944700 (-371547 naspram 2026-10-19)
  ! nedostaje lanac stanic
  ! gavranovic: redaka cijena 1125955 -> 854124
  ! metro: redaka cijena 73590 -> 12954
  UKUPNO (27 lanaca, -1)           1452   -60     474121   -3405   16944700  -371547
```
