# Granice po namirnici

Generirano skriptom `scripts/staple_reports.py` iz `staples.yaml` i arhive 2026-10-19.

- `min_pack`/`max_pack`: dopušteno pakiranje u g, ml ili kom (za jaja broj komada); izvan raspona
  proizvod dobiva `drop_reason='pakiranje'`. Vrijednosti su prijedlog iz Koraka 2A2 i čekaju pregled.
- granice cijene: `manual` = `plausible_per_unit` iz staples.yaml (vlasnik: mlijeko, brašno, šećer,
  sol, ulje, maslinovo ulje, maslac; prijedlog: jaja), `auto` = 0,25x–4x medijana cijene po jedinici
  namirnice u ovoj arhivi. Cijena izvan granica je `price_suspect`.

| namirnica | jedinica | min_pack | max_pack | €/jed min | €/jed max | granice |
|---|---|---|---|---|---|---|
| banana | kg | – | – | 0,37 | 5,96 | auto |
| brasno | kg | 500 | 5000 | 0,40 | 6,00 | manual |
| cesnjak | kg | – | – | 1,15 | 18,46 | auto |
| cokolada_za_kuhanje | kg | – | – | 4,66 | 74,52 | auto |
| dodatak_jelima | kg | 50 | 2000 | 2,35 | 37,52 | auto |
| endivija | kg | – | – | 1,11 | 17,80 | auto |
| gljive | kg | – | – | 1,04 | 16,72 | auto |
| grah | kg | 150 | 5000 | 0,74 | 11,80 | auto |
| grasak | kg | 150 | 5000 | 0,93 | 14,92 | auto |
| griz | kg | 200 | 2000 | 0,80 | 12,72 | auto |
| jabuka | kg | – | – | 0,42 | 6,76 | auto |
| jaja | kom | 4 | 30 | 0,10 | 1,50 | manual |
| jogurt | kg | 150 | 1000 | 0,86 | 13,72 | auto |
| junetina | kg | – | – | 3,37 | 53,96 | auto |
| kakao | kg | 50 | 1000 | 2,94 | 47,08 | auto |
| kecap | kg | – | – | 0,99 | 15,92 | auto |
| kiseli_kupus | kg | – | – | 0,55 | 8,72 | auto |
| kiselo_vrhnje | kg | 150 | 1000 | 1,25 | 19,96 | auto |
| koncentrat_rajcice | kg | 50 | 1000 | 2,73 | 43,60 | auto |
| krastavac | kg | – | – | 0,47 | 7,56 | auto |
| krumpir | kg | – | – | 0,23 | 3,72 | auto |
| krusne_mrvice | kg | 200 | 2000 | 0,95 | 15,28 | auto |
| kukuruz | kg | 150 | 5000 | 1,31 | 21,04 | auto |
| kupus | kg | – | – | 0,20 | 3,16 | auto |
| kvasac | vrecica | – | – | 0,11 | 1,76 | auto |
| leca | kg | 150 | 5000 | 0,94 | 15,12 | auto |
| limun | kg | – | – | 0,50 | 7,96 | auto |
| luk | kg | – | – | 0,31 | 5,00 | auto |
| majoneza | kg | – | – | 3,13 | 50,04 | auto |
| margarin | kg | 200 | 1000 | 1,19 | 19,04 | auto |
| maslac | kg | 100 | 1000 | 6,00 | 40,00 | manual |
| maslinovo_ulje | l | 250 | 5000 | 4,00 | 60,00 | manual |
| matovilac | kg | – | – | 1,50 | 24,00 | auto |
| med | kg | – | – | 3,05 | 48,80 | auto |
| mlijeko | l | 500 | 2000 | 0,50 | 4,00 | manual |
| mljevena_paprika | kg | 20 | 500 | 4,62 | 74,00 | auto |
| mljeveno_meso | kg | 300 | 2000 | 2,22 | 35,48 | auto |
| mozzarella | kg | 100 | 1000 | 3,49 | 55,80 | auto |
| mrkva | kg | – | – | 0,32 | 5,16 | auto |
| naranca | kg | – | – | 0,37 | 5,96 | auto |
| ocat | l | 500 | 3000 | 0,35 | 5,56 | auto |
| palenta | kg | 200 | 2000 | 0,59 | 9,52 | auto |
| papar | kg | 10 | 500 | 12,81 | 205,00 | auto |
| paprika | kg | – | – | 0,75 | 11,96 | auto |
| parmezan | kg | 50 | 1000 | 6,47 | 103,60 | auto |
| pasirana_rajcica | kg | 200 | 3000 | 0,69 | 11,12 | auto |
| persin | kom | – | – | – | – | – |
| pileca_prsa | kg | 250 | 3000 | 2,37 | 37,96 | auto |
| piletina | kg | – | – | 1,20 | 19,16 | auto |
| prasak_za_pecivo | vrecica | – | – | 0,04 | 0,72 | auto |
| radic | kg | – | – | 1,25 | 19,96 | auto |
| rajcica | kg | – | – | 0,88 | 14,00 | auto |
| rajcica_konzerva | kg | 200 | 5000 | 0,89 | 14,16 | auto |
| riza | kg | 250 | 5000 | 0,97 | 15,56 | auto |
| rukola | kg | – | – | 1,50 | 24,00 | auto |
| secer | kg | 250 | 5000 | 0,60 | 8,00 | manual |
| senf | kg | – | – | 2,42 | 38,76 | auto |
| slanina | kg | – | – | 5,35 | 85,56 | auto |
| slanutak | kg | 150 | 5000 | 0,94 | 15,12 | auto |
| slatko_vrhnje | l | 200 | 1000 | 2,49 | 39,80 | auto |
| sol | kg | 250 | 5000 | 0,20 | 8,00 | manual |
| spinat | kg | – | – | 0,90 | 14,32 | auto |
| sunka | kg | – | – | 3,85 | 61,56 | auto |
| svinjetina | kg | – | – | 1,47 | 23,56 | auto |
| svjezi_sir | kg | 150 | 1000 | 1,61 | 25,80 | auto |
| tikvica | kg | – | – | 0,42 | 6,76 | auto |
| tjestenina | kg | 250 | 5000 | 0,94 | 15,12 | auto |
| tuna | kg | 50 | 1000 | 5,20 | 83,12 | auto |
| tvrdi_sir | kg | 100 | 1000 | 3,65 | 58,40 | auto |
| ulje | l | 500 | 5000 | 1,00 | 12,00 | manual |
| vanilin_secer | vrecica | – | – | 0,04 | 0,72 | auto |
| vrhnje_za_kuhanje | l | 200 | 1000 | 1,65 | 26,32 | auto |
| zelena_salata | kg | – | – | 0,83 | 13,28 | auto |
| zobene_pahuljice | kg | 250 | 2000 | 0,74 | 11,92 | auto |
