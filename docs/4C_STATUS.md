# Korak 4C: stanje

| točka | stanje |
|---|---|
| 1 alternative po pravilima glavnog izbora, samo jeftinije | gotovo |
| 2 jaja (M/L, bolji od kaveznog, bez zaokruživanja, [0.08, 0.55]) | gotovo (preferred_tiers, quality_rank; cijena po komadu na 4 decimale) |
| 3 marka u nazivu sastojka (data/brands) | gotovo (data/brands.yaml, 30 marki) |
| 4 free_text (okusi, grickalice, prve tri riječi, needs_confirmation) | gotovo (min. pakiranje: 25 % medijana kandidata u gradu) |
| 5 vrećice iz rinfuze (udio gramaže) | gotovo; Lidl "Vanilin šećer", 80 g iz stupca unit: 1 vrećica = 0,04 € (pakiranje 0,39 €) |
| 6 veličina odgovora (sažete ostale trgovine, detail) | gotovo: 7 sastojaka ≈ 2,3 KB sažeto, ≈ 17 KB uz detail=true |
| 7 dvosmislen sastojak: ask_user, "Bez graha" | gotovo (genitive u staples.yaml) |
| 8 smoke_4c | - |
| 9 Lidl sirovi retci (samo čitanje) | gotovo: docs/lidl_raw_check.md; jedna greška parsera ("Suncokretovo ulje 20g Lidla" -> 20 g), nije ispravljena |

Hosting: nije dirano.
