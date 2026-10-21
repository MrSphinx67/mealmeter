# Nekoherentne EAN grupe (Korak 4B.6)

Baza: `data/mealmeter.duckdb`, skripta `scripts/ean_incoherent.py`, pravilo `build.ean_coherence`.

Grupa istog globalnog EAN-a u >= 2 lanca je nekoherentna kad nijedna riječ naziva nije u nazivima >= 50 %
lanaca (i barem dva lanca). Riječ je "u nazivu" i kao kratica ("REB" / "REBRA") ili uz razliku u slovu-dva;
kandidati su riječi od >= 3 slova s markom, jer je strogo pravilo (>= 4 slova, bez marke) označilo ~1 550
grupa, uglavnom isti proizvod. Takva grupa se razdvaja po lancu + name_norm (`ean_global = false`,
`ean_incoherent = true`). U koherentnoj grupi s >= 3 lanca izdvaja se lanac koji ne dijeli nijednu riječ
ni s jednim drugim lancem (razlog `outlier`). Poznata cijena: sinonimi bez zajedničke riječi (GLJIVE /
ŠAMPINJONI, ZELJE / KUPUS KIS.) također se razdvajaju; tada se svaki lanac procjenjuje po svom nazivu.

| razlog | grupa | proizvoda |
|---|---|---|
| group | 411 | 839 |
| outlier | 220 | 224 |

## Po lancu

| lanac | razdvojenih grupa | izdvojen iz grupe | proizvoda |
|---|---|---|---|
| boso | 17 | 5 | 22 |
| branka | 34 | 4 | 38 |
| bure | 58 | 18 | 76 |
| djelo_vodice | 15 | 10 | 25 |
| dm | 5 | 1 | 6 |
| eurospin | 12 | 5 | 17 |
| gavranovic | 44 | 13 | 57 |
| jadranka_trgovina | 19 | 2 | 21 |
| kaufland | 8 | 4 | 12 |
| konzum | 21 | 2 | 23 |
| ktc | 12 | 7 | 19 |
| lidl | 2 | 0 | 2 |
| lorenco | 38 | 12 | 50 |
| metro | 19 | 5 | 24 |
| ntl | 53 | 8 | 61 |
| plodine | 152 | 15 | 167 |
| ribola | 23 | 17 | 40 |
| roto | 5 | 4 | 9 |
| spar | 21 | 10 | 31 |
| stanic | 2 | 0 | 2 |
| stridon | 67 | 20 | 87 |
| studenac | 64 | 13 | 77 |
| tommy | 17 | 6 | 23 |
| trgocentar | 5 | 6 | 11 |
| trgovina-krk | 103 | 30 | 133 |
| vrutak | 18 | 1 | 19 |
| zabac | 5 | 6 | 11 |

## 30 primjera (20 razdvojenih grupa, 10 izdvojenih lanaca)

| EAN | razlog | nazivi |
|---|---|---|
| 3850307785219 | group | gavranovic: WC SET SPACE 50x80/40x60cm; trgovina-krk: KUPAONSKI TEPIH 50X80X/40X60 |
| 5010103800259 | group | bure: WHISKI J&B 0,7 l RARE; roto: WHISKEY J&B 0,7 (12)*; studenac: VISKI J&B 0,7L |
| 3831002406593 | group | spar: VINO MOVIA MERLOT TURNO 0,75L; vrutak: *DE BAGUER RED GORIŠKA 0.75L 2018 -6/1- |
| 8015817002309 | group | bure: KOKTEL LIMUN 0,7 l; roto: MIXER PURE LEMON JUICE 99,5% 0,7 (6) * |
| 8015361978136 | group | bure: TEĆA+POKL.16cm; jadranka_trgovina: POSUDA S RUČKOM 16CM INDUKCIJA 652419 COOKSTONE |
| 3858893723943 | group | dm: KH-7 Trio pack XXL 3X750 ml OS; konzum: KH-7 ODMAŠ+KAMEN+ODST MRLJ 3X750 ml |
| 8593419414466 | group | plodine: SIMAX VATROSTALNA POSUDA CETVRTASTA S POKLOPCEM 8 L; trgovina-krk: ZDJELA 8 L 7296-7306 COME |
| 8001133351603 | group | ntl: POSUDA STAKLENA S POKLOPCEM 21*13CM; trgovina-krk: FRIGOVERE PRAVOK 21*13 PLAVI IVMAR |
| 3858884125268 | group | gavranovic: KONOP ZA ROBU 10m; trgovina-krk: ŠPAGA ZA VEŠ 10 m 5268 MISST |
| 8015361486167 | group | bure: OTVARAČ 3u1 15 cm; trgovina-krk: VADIČEP ZA BOCE 15CM |
| 8004360074567 | group | gavranovic: ČAŠE 6/1 VIŠENAMJENSKA 390ml; trgovina-krk: GARN. ČAŠA DOTS ROCK 6/1 390 ml NTL |
| 9780201379624 | group | plodine: NIVEA STALAK WINTER FACIAL; vrutak: *PIVO KASTEEL DISCOVERY 4*0.33L + ČAŠA -6/1- |
| 3830055807449 | group | ntl: SUPER E 25EUR VALUE/GIFT CARD; studenac: POKL. KARTICA SUPER E 25 EUR |
| 3830055807395 | group | ntl: SUPERCARD BLACK 100EUR VALUE/GIFT CARD; studenac: POKL. KARTICA SUPER. BL. 100 EUR |
| 3850223297179 | group | gavranovic: IGR.SET ZA UREĐIVANJE KOSE; jadranka_trgovina: SARA S BRAIDED LOCKS |
| 8721037416887 | group | boso: IGRAČ PUHALICA 60 ml SORT 26; ntl: BALONI OD SAPUNICE 60ml Art.M16200220 |
| 3859893725142 | group | kaufland: B!te me Kol.lješ.mas.bio bez glu.2x20g; vrutak: KEKS BITEME LAVA NOUGAT RUSH 40g -24/1- |
| 8593410066510 | group | bure: ČAŠE ZA VINO 6/1 450 ml DORA; jadranka_trgovina: ČAŠA STRIX 450ML 6/1 |
| 3838929568120 | group | djelo_vodice: IZOLA BRAND 3PACK; ribola: SKUŠA IZOLA3/1 375 g POVRĆE DELAMARIS |
| 3856025896039 | group | ntl: STOLNJAK 140*180CM PVC; plodine: IGR SET ZA RIBOLOV |
| 4101540701610 | outlier | stridon: MEKANI BISKVIT 400 g (3) — ostaje: djelo_vodice: KOLAČ KUGLOF 400GR; eurospin: KOLAČ MRAMORNI 400g; ktc: KUGLOF KOLAČ 400g; lorenco: KUGLOF KOLAČ 400g; ribola: KUGLOF KOLAČ 400 g ULTRA; studenac: KUGLOF MRAMORNI KUCHENMAISTER 400 g; tommy: KOLAČ KUGLOF 400 g KUECHENMEIS; trgocentar: ULTRA K |
| 3858890572865 | outlier | trgovina-krk: TREGERI ZA PAKTREGER 2X100 cm ROX — ostaje: jadranka_trgovina: PAUK 2X100CM TRAKA ZA PRIČVRŠČIVANJE; plodine: PAUK 2X100 CM |
| 4023103073241 | outlier | lorenco: SPUŽVICE 10/1 VIL. — ostaje: trgocentar: RAINBOW SPUŽVA ABRAZIVNA 10KOM(40); trgovina-krk: SPUŽVA ABRAZIVNA RAINBOW 10/1 |
| 3858892259320 | outlier | lorenco: ČO.VEZ.HRV.ZNAMEN.100g — ostaje: konzum: ČOKOLADA CROATIA 100g VRSNA; vrutak: ČOK CROATIA 100G |
| 8410387002184 | outlier | plodine: BISKV. MRAMORNI 240 G MONTES LARA — ostaje: djelo_vodice: KOLAČ MARBLE 240G KOREKT; ntl: KOLAČ MARBLE 240G; ribola: MARBLE KOLAČ 240 g KOREKT ZAGREB |
| 8692952065415 | outlier | trgovina-krk: GARN. ČAŠA 6/1 205 CC SDF20156 NTL — ostaje: bure: ČAŠE ZA VODU 6/1 SEDEF; gavranovic: ČAŠE ZA VODU 6/1 205 ml; stridon: ČAŠE STAKLO SET 6KOM 205ML Z5388E OFFERTISSIMA |
| 3850116990163 | outlier | studenac: LAZANJE 450 g — ostaje: branka: LASAGNE BOLOGNESE 450g; djelo_vodice: LASAGNE 450G LEDO; gavranovic: LASAGNE BOLONESE 450g LEDO; jadranka_trgovina: LASAGNE BOLOGNESE 450G LEDO; kaufland: Ledo Lasagne Bolognese 450 g; konzum: LASAGNE 450g LEDO; ktc: LASAGNE BOLOGNESE 450g LEDO; lorenco: LAS |
| 3859890630562 | outlier | boso: MESO ŠVARG kg ŠVARGL — ostaje: djelo_vodice: DATULJA 200G VEDRINI; kaufland: Vedrini Datulja 200g; konzum: DATULJA S KOŠTICOM VEDRINI 200 g; lorenco: DATULJE 200g; plodine: DATULJA 200 G VEDRINI PRIMORAC; stridon: DATULJA 200 g VEDRINI 1993 |
| 8012566004097 | outlier | tommy: METVICA 30 g — ostaje: metro: 30G MENTA- L'INSALATA; plodine: ZACIN MENTA 30G. |
| 3870634073766 | outlier | stridon: LAMPAŠ K5 20.5 cm OFFERTISIMA — ostaje: lidl: Lumen Lampion s religijskim motivom; plodine: LAMPION K5 290 G 20,5 CM 50 SATI GORENJA; tommy: LAMPION K5; trgovina-krk: LAMPION K5 |
