# Korak 4B: stanje

| točka | stanje |
|---|---|
| 1 upute i opisi alata | gotovo |
| 2 plan_basket (summary_hr, alternative, free_text, spajanje trgovina) | gotovo (uz pack_size u stavkama) |
| 3 nove namirnice (čokoladni namaz, džem) | gotovo (uz Lino Ladu kao sinonim) |
| 4 višestruka pakiranja iz stupca unit | gotovo |
| 5 jaja plausible_by | gotovo |
| 6 koherentnost EAN grupe | gotovo, docs/ean_incoherent.md (411 razdvojenih grupa, 220 izdvojenih lanaca) |
| 7 pravila (tjestenina, med, mlijeko, slanina, krastavac) | gotovo (slanina: `carsko`; krastavac i `ult\b`) |
| 8 rate limit (IP, sesija, globalno) | gotovo (HTTP je stateless, pa Mcp-Session-Id šalje samo klijent koji ga sam postavi) |
| 9 zamjena datoteke baze bez restarta | gotovo (ATTACH u novoj instanci u memoriji, zbog predmemorije instanci DuckDB-a) |
| 10 smoke_4b i shelf_check.csv | gotovo: docs/smoke_4b.md, data/eval/shelf_check.csv (22 stavke, stupci police prazni) |

Baza je ponovno izgrađena (19.10. pa 20.10., carry-forward 99 trgovina / 589 037 cijena; 16 616 090 cijena).
Smoke je pronašao i ispravio: maslinovo ulje bez `tost`/`uljem`, šećer bez ksilitola/eritritola, summary_hr
postavlja pitanje o obliku kad košarice nema.

Hosting: nije dirano.
