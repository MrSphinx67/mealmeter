# Jutarnji pregled: Korak 2C (arhiva 2026-10-19)

Izvještaj generira `scripts/morning_review.py`. Točke 4 i 5 čekaju potvrdu vlasnika.

## 4. Pileća prsa: „Jeli“ (ČEKA POTVRDU)

`plausible_per_unit: [5, 20]` €/kg je primijenjen: izvan granica je 528 od 10613 cijena po kg preostalih (neisključenih) proizvoda.

Sve grupe s „jeli“ ili „je li“ u nazivu. To je Gavrilovićeva linija **Jeli**: delikatesna pileća prsa (narezak od 350 g i štruca od 2,6 kg), a ne svježi file. **Privremeno su isključene** iz `pileca_prsa` (`must_not_match: jeli\b, je li\b`) dok ne potvrdiš. Ako ih treba vratiti, dovoljno je obrisati ta dva uzorka u `staples.yaml`.

| grupa | nazivi | lanci | min €/kg | medijan €/kg | max €/kg | cijena |
|---|---|---|---|---|---|---|
| stridon:jeli pileca prsa 2600 g gavrilovic | JELI PILEĆA PRSA 2600 g GAVRILOVIĆ | stridon | 2,30 | 2,81 | 4,00 | 9 |
| trgovina-krk:jeli pileca prsa 2600 gr | JELI PILEĆA PRSA 2600 gr | trgovina-krk | 4,23 | 4,23 | 4,38 | 11 |
| branka:salama prsa pileca jeli gavrilovic | SALAMA PRSA PILEĆA JELI GAVRILOVIĆ | branka | 9,49 | 9,74 | 9,99 | 2 |
| 3858892724316 | JELI PILEĆA PRSA 2600G,GAVRILOVIĆ; PILEĆA PRSA JELI GAV RILOVIĆ; PILEĆA PRSA JELI GAVRILOVIĆ; PRSA PILEĆA JELI 2600 g; PRSA PILEĆA JELI kg; Pileća prsa Jeli | konzum, ktc, ribola, spar, studenac, trgocentar | 3,84 | 10,29 | 11,69 | 205 |
| gavranovic:gav jeli pileca prsa delikates | GAV.JELI PILEĆA PRSA DELIKATES | gavranovic | 10,49 | 10,49 | 10,49 | 44 |
| tommy:pileca prsa jeli gavrilovic | PILEĆA PRSA JELI GAVRILOVIĆ | tommy | 9,99 | 10,49 | 10,99 | 81 |
| ntl:prsa pileca jeli kg gavrilovic | PRSA PILEĆA JELI kg GAVRILOVIĆ | ntl | 10,49 | 10,49 | 10,49 | 2 |
| 3858892722572 | ŠUNKA JELI PIL. PRSA; ŠUNKA PILEĆA PRSA JELI | djelo_vodice, studenac | 10,69 | 11,04 | 11,39 | 2 |
| 3858892724392 | GAV.JELI PILEĆA PRSA 350g; Gavrilović Jeli Pileća prsa 350 g; JELI PILECA PRSA 350 G GAVRILOVIC; PILEĆA PRSA 350 g JE LI GAVRILOVIĆ; PILEĆA PRSA 350G JELI; PILEĆA PRSA 350g JELI GAVRILOVIĆ; PILEĆA PRSA JELI 350 g; PRSA PILEĆA JELI 350 g; PRSA PILEĆA JELI 350g | djelo_vodice, gavranovic, kaufland, konzum, ktc, plodine, ribola, spar, studenac | 8,11 | 11,11 | 13,40 | 310 |

Napomena: štruca od 2,6 kg ima 2,30–4,38 €/kg, pa vjerojatno nosi cijenu po kg kao cijenu pakiranja (lanac je cijenu po kg upisao kao cijenu proizvoda).

**Upozorenje uz granicu od 5 €/kg:** ispod nje su i stvarna svježa prsa po akcijskoj ili diskontnoj cijeni (Konzum K Plus 4,69 €/kg u 184 trgovine, Eurospin 4,99 €/kg). Ona sada postaju `price_suspect` i u košarici su samo rezerva. Prijedlog: donja granica 2,5 ili 3 €/kg. Najčešće cijene izvan granica:

| lanac | naziv | min €/kg | max €/kg | cijena |
|---|---|---|---|---|
| konzum | PRSA PILEĆA K PLUS BEZ KOŽE | 4,69 | 4,69 | 184 |
| konzum | PILEĆI FILE OD PRSA VAKUUM | 2,99 | 4,99 | 95 |
| tommy | PILEĆI FILE BRAZILSKI SMRZNUTI | 4,25 | 4,99 | 83 |
| eurospin | DOMAĆI PIL. FILE OD PRSA OBIT. PAK. | 4,99 | 4,99 | 43 |
| eurospin | DOMAĆI PIL. FILE OD PRSA OBIT.RFZ | 4,99 | 4,99 | 43 |
| stanic | PILEĆI FILE SMRZNUTI | 2,75 | 2,75 | 29 |
| roto | PILEĆI FILE SVJEŽI sniženje (12) | 2,50 | 2,50 | 9 |
| metro | 2,5KG UKR. PILEĆI FILE SMRZ | 31,50 | 31,50 | 7 |
| metro | CCA5KG MC PILEĆI FILE MAP | 4,99 | 4,99 | 7 |
| studenac | PILECI FILE SMRZ.STANIC | 3,92 | 3,98 | 5 |
| trgovina-krk | PILEĆI FILE ZA GASTRO 1 kg | 1,95 | 4,08 | 4 |
| konzum | PILEĆI FILE SOLJENI 6X2 BRAZIL | 3,28 | 4,11 | 4 |
| studenac | GASTRO PILEĆI FILE PEČENI | 209,90 | 209,90 | 2 |
| branka | -PRSA PILEĆA SVJEŽA | 4,79 | 4,79 | 2 |
| studenac | PILEĆI FILE BRAZIL 2KG LEDO | 4,91 | 4,91 | 2 |

## 5. Luk: nazivi s bojom (ČEKA POTVRDU, mapiranje nije mijenjano)

Svi različiti nazivi kandidata za `luk` (`must_match` luk/kapula) koji sadrže crveni, ljubičasti, srebrenac, žuti ili bijeli, uz trenutni status, vrstu iz naziva, raspon cijene po kg (s pretpostavljenih 500 g za „rukavac“) i broj lanaca. `vrsta`: crveni = crven|ljubičast, žuti = žut|srebren, bijeli = bijel.

| naziv | status | vrsta | min €/kg | max €/kg | lanaca | lanci |
|---|---|---|---|---|---|---|
| LUK BIJELI (ČEŠNJAK) DOMAĆI RF | isključen | - | 3,05 | 3,05 | 1 | tommy |
| LUK BIJELI (ČEŠNJAK) RFS | isključen | - | 2,19 | 2,19 | 1 | tommy |
| LUK CRVENI OGULJENI REZANI 5 kg | isključen | - | 2,12 | 2,12 | 1 | tommy |
| LUK LJUBIČ./BIJELI ZA GASTRO 1 kg | luk | bijeli | 0,68 | 1,30 | 1 | trgovina-krk |
| 10KG LUK CRVENI | luk | crveni | 0,74 | 0,74 | 1 | metro |
| 10KG LUK CRVENI 50/70 VC KL II | luk | crveni | 0,74 | 0,74 | 1 | metro |
| 10KG LUK CRVENI 60/80 VC | luk | crveni | 0,74 | 0,74 | 1 | metro |
| 1KG LUK CRVEN SLATKI 50-70 VC | luk | crveni | 3,28 | 3,28 | 1 | metro |
| 5KG LUK CRVENI 4 MR | luk | crveni | 0,91 | 0,91 | 1 | metro |
| 5KG LUK LJUBIČASTI - VC | luk | crveni | 1,59 | 1,59 | 1 | metro |
| 5KG LUK LJUBIČASTI 50-70 | luk | crveni | 1,40 | 1,40 | 1 | metro |
| BIO LUK LJUBIČASTI NP 500 g | luk | crveni | 2,98 | 3,18 | 1 | spar |
| KAPULA (CRVENI LUK) SNIŽENO | luk | crveni | 0,40 | 0,40 | 1 | tommy |
| KAPULA LJUBIČASTA | luk | crveni | 1,59 | 1,63 | 2 | bure, lorenco |
| KAPULA LJUBIČASTA (CRVENI LUK) | luk | crveni | 1,19 | 1,39 | 1 | tommy |
| LUK CRVENI | luk | crveni | 0,49 | 0,95 | 6 | gavranovic, konzum, ktc, ntl, trgocentar, trgovina-krk |
| LUK CRVENI (20) | luk | crveni | 0,75 | 0,75 | 1 | roto |
| LUK CRVENI (PT) | luk | crveni | 0,49 | 0,49 | 1 | trgocentar |
| LUK CRVENI 1 kg BIO ZONE | luk | crveni | 1,69 | 1,69 | 1 | konzum |
| LUK CRVENI 1KG EKOZONA | luk | crveni | 1,99 | 2,19 | 1 | tommy |
| LUK CRVENI 1kg | luk | crveni | 1,05 | 1,05 | 1 | ktc |
| LUK CRVENI 2,5 kg | luk | crveni | 1,08 | 1,08 | 1 | ntl |
| LUK CRVENI 2,5 kg SNIŽENJE | luk | crveni | 0,40 | 0,48 | 1 | ntl |
| LUK CRVENI 2,50 kg | luk | crveni | 0,96 | 0,96 | 1 | trgovina-krk |
| LUK CRVENI 2,5kg | luk | crveni | 1,30 | 1,30 | 1 | gavranovic |
| LUK CRVENI 2,5kg SNIŽENJE | luk | crveni | 0,74 | 0,74 | 1 | gavranovic |
| LUK CRVENI 2kg | luk | crveni | 1,00 | 1,00 | 1 | ktc |
| LUK CRVENI 4/1 | luk | crveni |  |  | 1 | ribola |
| LUK CRVENI 5/1 | luk | crveni | 0,53 | 0,53 | 1 | ntl |
| LUK CRVENI 5/1 NTL | luk | crveni | 0,33 | 0,33 | 1 | trgovina-krk |
| LUK CRVENI 5KG | luk | crveni | 0,46 | 0,46 | 1 | trgocentar |
| LUK CRVENI 5kg | luk | crveni | 0,80 | 0,80 | 1 | ktc |
| LUK CRVENI AGROVIR | luk | crveni | 0,69 | 1,25 | 1 | stridon |
| LUK CRVENI BIM | luk | crveni | 0,66 | 0,86 | 1 | stridon |
| LUK CRVENI II KL | luk | crveni | 0,49 | 0,49 | 1 | boso |
| LUK CRVENI II KL HR | luk | crveni | 0,53 | 0,53 | 1 | boso |
| LUK CRVENI KLIPER 1 KG | luk | crveni | 1,25 | 1,45 | 1 | tommy |
| LUK CRVENI PAK 1 kg | luk | crveni | 0,99 | 0,99 | 1 | trgovina-krk |
| LUK CRVENI PAK. 1 kg | luk | crveni | 0,99 | 0,99 | 1 | ntl |
| LUK CRVENI PAK. 1 kg SNIŽENJE | luk | crveni | 0,50 | 0,50 | 1 | ntl |
| LUK CRVENI PAKIR.1kg | luk | crveni | 1,29 | 1,45 | 1 | gavranovic |
| LUK CRVENI PAKIR.1kg SNIŽENJE | luk | crveni | 0,79 | 0,84 | 1 | gavranovic |
| LUK CRVENI RUKAVAC 3/1 VOĆ. STUDENAC | luk | crveni | 2,38 | 2,62 | 1 | studenac |
| LUK CRVENI RUKAVAC 4/1 | luk | crveni | 1,98 | 2,90 | 3 | gavranovic, ntl, trgovina-krk |
| LUK CRVENI RUKAVAC 4/1 SNIŽENJE | luk | crveni | 1,00 | 1,00 | 1 | ntl |
| LUK CRVENI RUKAVAC KOM | luk | crveni | 1,78 | 1,78 | 1 | ktc |
| LUK CRVENI SNIŽENI kg | luk | crveni | 0,59 | 0,59 | 1 | studenac |
| LUK CRVENI SNIŽENJE | luk | crveni | 0,20 | 0,71 | 2 | gavranovic, ntl |
| LUK CRVENI SNIŽENO | luk | crveni | 0,30 | 0,50 | 1 | ktc |
| LUK CRVENI ZA GASTRO 1 kg | luk | crveni | 0,26 | 1,89 | 1 | trgovina-krk |
| LUK CRVENI kg | luk | crveni | 0,84 | 0,84 | 1 | studenac |
| LUK LJUBICASTI | luk | crveni | 1,19 | 1,19 | 1 | plodine |
| LUK LJUBICASTI 1 KG | luk | crveni | 0,99 | 1,29 | 1 | plodine |
| LUK LJUBICASTI 500G | luk | crveni | 1,86 | 2,46 | 1 | plodine |
| LUK LJUBIČAST RUKAVAC VH 4/1 | luk | crveni | 2,58 | 2,58 | 1 | spar |
| LUK LJUBIČASTI | luk | crveni | 0,99 | 1,89 | 7 | gavranovic, konzum, ktc, ntl, ribola, trgovina-krk, vrutak |
| LUK LJUBIČASTI (10) | luk | crveni | 1,01 | 1,01 | 1 | roto |
| LUK LJUBIČASTI (PT) | luk | crveni | 1,39 | 1,39 | 1 | trgocentar |
| LUK LJUBIČASTI - KG | luk | crveni | 1,16 | 1,16 | 1 | metro |
| LUK LJUBIČASTI 1kg | luk | crveni | 1,09 | 1,09 | 1 | eurospin |
| LUK LJUBIČASTI 4/1 | luk | crveni |  |  | 1 | ribola |
| LUK LJUBIČASTI AGROVIR | luk | crveni | 1,27 | 2,20 | 1 | stridon |
| LUK LJUBIČASTI II KL | luk | crveni | 0,99 | 1,69 | 1 | boso |
| LUK LJUBIČASTI KG | luk | crveni | 0,93 | 0,93 | 1 | metro |
| LUK LJUBIČASTI PAKIRANI 1KG | luk | crveni | 1,49 | 1,49 | 1 | djelo_vodice |
| LUK LJUBIČASTI RUKAVAC 4/1 | luk | crveni | 1,98 | 3,78 | 5 | branka, eurospin, gavranovic, ntl, trgovina-krk |
| LUK LJUBIČASTI RUKAVAC 4/1 SNIŽENJE | luk | crveni | 1,98 | 2,40 | 1 | gavranovic |
| LUK LJUBIČASTI RUKAVAC 4/1SNIŽENJE | luk | crveni | 1,40 | 1,40 | 1 | ntl |
| LUK LJUBIČASTI RUKAVAC KOM | luk | crveni | 2,38 | 2,38 | 1 | ktc |
| LUK LJUBIČASTI SNIŽ.kg | luk | crveni | 0,90 | 0,99 | 1 | studenac |
| LUK LJUBIČASTI SNIŽENJE | luk | crveni | 0,25 | 1,16 | 2 | gavranovic, ntl |
| LUK LJUBIČASTI SNIŽENO | luk | crveni | 0,40 | 0,40 | 1 | ktc |
| LUK LJUBIČASTI VH 1 kg | luk | crveni | 1,29 | 1,29 | 1 | spar |
| LUK LJUBIČASTI kg | luk | crveni | 1,29 | 1,42 | 1 | studenac |
| LUK LJUBIČASTI rfz | luk | crveni | 0,99 | 0,99 | 1 | eurospin |
| LUK LJUBIČASTI Š-27 | luk | crveni | 1,59 | 1,69 | 1 | branka |
| LUK LJUBIČASTI- KG | luk | crveni | 1,53 | 1,53 | 1 | metro |
| Luk crveni 1kg | luk | crveni | 0,79 | 0,89 | 2 | kaufland, lidl |
| Luk crveni 2kg | luk | crveni | 0,77 | 0,80 | 2 | kaufland, lidl |
| Luk crveni 5kg | luk | crveni | 0,39 | 0,59 | 2 | kaufland, lidl |
| Luk crveni rinfuza | luk | crveni | 0,79 | 0,79 | 1 | lidl |
| Luk crveni_OC | luk | crveni | 0,79 | 0,79 | 1 | kaufland |
| Luk ljubičasti | luk | crveni | 1,09 | 1,09 | 1 | kaufland |
| Luk ljubičasti 1kg | luk | crveni | 0,99 | 0,99 | 1 | lidl |
| Luk ljubičasti rfs | luk | crveni | 1,29 | 1,49 | 1 | spar |
| Luk ljubičasti rinfuza | luk | crveni | 1,09 | 1,09 | 1 | lidl |
| Luk ljubičasti rukavac | luk | crveni | 2,58 | 2,58 | 1 | kaufland |
| N-LUK CRVENI (ŽUTI) | luk | crveni |  |  | 1 | vrutak |
| KAPULA MLADA LJUBIČASTA | luk | mladi | 1,39 | 1,59 | 1 | tommy |
| \*KAPULA ŽUTA 1 kg | luk | zuti | 1,25 | 1,25 | 1 | ribola |
| \*LUK SREBRENAC 4/1 | luk | zuti |  |  | 1 | ribola |
| BIO LUK ŽUTI 500 g | luk | zuti | 2,78 | 2,78 | 1 | tommy |
| BIO LUK ŽUTI NATUR PUR 1 kg | luk | zuti | 1,69 | 1,79 | 1 | spar |
| KAPULA BIJELA-SREBRENAC | luk | zuti |  |  | 1 | lorenco |
| KAPULA SREBRENAC kg | luk | zuti | 1,68 | 1,68 | 1 | studenac |
| KAPULA ŽUTA | luk | zuti | 0,84 | 0,84 | 1 | ribola |
| KAPULA ŽUTA (CRV.LUK) | luk | zuti | 0,79 | 0,79 | 1 | tommy |
| KAPULA ŽUTA EMM | luk | zuti | 0,84 | 0,84 | 1 | ribola |
| KBio.Luk žuti 1kg | luk | zuti | 1,99 | 1,99 | 1 | kaufland |
| KBio.Luk žuti 500g | luk | zuti | 3,58 | 3,58 | 1 | kaufland |
| LUK SREBRENAC | luk | zuti | 1,79 | 3,45 | 9 | gavranovic, konzum, ktc, ntl, plodine, ribola, trgocentar, trgovina-krk, vrutak |
| LUK SREBRENAC (10) | luk | zuti | 1,83 | 1,83 | 1 | roto |
| LUK SREBRENAC (PT) | luk | zuti | 2,09 | 2,29 | 1 | trgocentar |
| LUK SREBRENAC 3/1 | luk | zuti |  |  | 1 | djelo_vodice |
| LUK SREBRENAC 500G | luk | zuti | 2,22 | 2,46 | 1 | plodine |
| LUK SREBRENAC AGROVIR | luk | zuti | 4,71 | 4,71 | 1 | stridon |
| LUK SREBRENAC RFS | luk | zuti | 1,49 | 1,79 | 2 | eurospin, tommy |
| LUK SREBRENAC SNIŽENJE | luk | zuti | 1,00 | 1,84 | 2 | gavranovic, ntl |
| LUK SREBRENAC SNIŽENO | luk | zuti | 1,00 | 1,00 | 1 | ktc |
| LUK SREBRENAC kg | luk | zuti | 3,29 | 3,69 | 1 | studenac |
| LUK ZUTI | luk | zuti | 0,79 | 0,84 | 1 | plodine |
| LUK ZUTI 1 KG | luk | zuti | 0,89 | 0,99 | 1 | plodine |
| LUK ZUTI 1 KG GIRO | luk | zuti | 1,79 | 1,95 | 1 | plodine |
| LUK ŽUTI 1 kg | luk | zuti | 1,09 | 1,29 | 1 | konzum |
| LUK ŽUTI 1kg | luk | zuti | 0,79 | 1,69 | 2 | branka, eurospin |
| LUK ŽUTI 2kg | luk | zuti | 0,75 | 0,75 | 1 | eurospin |
| LUK ŽUTI PAKIRANI 1KG | luk | zuti | 1,29 | 1,29 | 1 | djelo_vodice |
| LUK ŽUTI RUKAVAC 4/1 | luk | zuti | 1,98 | 1,98 | 1 | eurospin |
| LUK ŽUTI RUKAVAC VH 4/1 | luk | zuti | 1,98 | 1,98 | 1 | spar |
| LUK ŽUTI SVJ 40/60 II KL V-V | luk | zuti | 0,56 | 0,56 | 1 | studenac |
| LUK ŽUTI SVJ II KL V-V | luk | zuti | 1,55 | 1,55 | 1 | studenac |
| LUK ŽUTI VH 1 kg | luk | zuti | 0,99 | 0,99 | 1 | spar |
| LUK ŽUTI rfz | luk | zuti | 0,64 | 0,64 | 1 | eurospin |
| Luk rukavac žuti kom | luk | zuti | 1,98 | 1,98 | 1 | kaufland |
| Luk srebrenac | luk | zuti | 1,99 | 2,99 | 2 | kaufland, spar |
| Luk srebrenac rinfuza | luk | zuti | 1,99 | 1,99 | 1 | lidl |
| Luk srebrenac, slatki | luk | zuti | 2,19 | 2,19 | 1 | lidl |
| Luk žuti rfs | luk | zuti | 0,39 | 0,84 | 1 | spar |

Zapažanja (bez promjene mapiranja):
- „LUK BIJELI (ČEŠNJAK)“ je češnjak; isključen je kroz `cesnjak`. Vrsta `bijeli` zato pogađa samo „LUK LJUBIČ./BIJELI ZA GASTRO“, koji je ljubičasti luk: kratica „ljubič.“ ne pogađa `ljubicast`.
- „LUK SREBRENAC“ postoji u 20-ak lanaca i **jest u namirnici** (vrsta `zuti`): uzorak `srebrn` u `must_not_match` ne pogađa „srebrenac“ (srebr-e-nac), pa ništa ne isključuje. Ako je srebrenac trebao biti isključen, uzorak bi bio `srebren`.
- Pakiranja bez gramature („LUK SREBRENAC 4/1“, „3/1“) nemaju cijenu po kg; `packaged` (500 g) vrijedi samo za „rukavac“.
- Metroove vreće od 10 kg imaju oko 0,74 €/kg, a „slatki“ crveni luk 3,28 €/kg.

## 0. Filtar hrane

Proizvodi bez korisne kategorije lanca (nema je, ili je „Ostalo“) po lancu: koliko ih je naslijedilo skupinu preko globalnog EAN-a (većinska skupina u lancima s kategorijom, > 50 %), koliko ih je razvrstano popisom riječi i koliko ostaje `unknown`.

| lanac | proizvoda | bez kategorije | EAN | udio EAN | riječi | unknown |
|---|---|---|---|---|---|---|
| plodine | 76495 | 76495 | 22769 | 29.8 % | 3835 | 49891 |
| lorenco | 17443 | 17443 | 12444 | 71.3 % | 262 | 4737 |
| trgovina-krk | 33795 | 14462 | 3468 | 24.0 % | 1137 | 9857 |
| ntl | 18315 | 8004 | 2487 | 31.1 % | 392 | 5125 |
| gavranovic | 15144 | 5504 | 2022 | 36.7 % | 170 | 3312 |
| stridon | 31596 | 3023 | 983 | 32.5 % | 202 | 1838 |
| zabac | 3333 | 547 | 363 | 66.4 % | 7 | 177 |
| vrutak | 14246 | 67 | 50 | 74.6 % | 0 | 17 |
| djelo_vodice | 10768 | 58 | 49 | 84.5 % | 0 | 9 |
| dm | 21712 | 38 | 0 | 0.0 % | 0 | 38 |
| roto | 9201 | 26 | 10 | 38.5 % | 0 | 16 |
| stanic | 2601 | 10 | 2 | 20.0 % | 1 | 7 |
| boso | 9257 | 3 | 0 | 0.0 % | 0 | 3 |

Proizvodi izvan zadanog izbora (`find_products`/`get_prices` bez `include_*`), po skupini. Nijedan nije obrisan iz baze.

| skupina | proizvoda | iz kategorije | preko EAN-a | iz riječi |
|---|---|---|---|---|
| kucanstvo | 86825 | 70829 | 14725 | 1271 |
| unknown | 75027 | 0 | 0 | 0 |
| kozmetika | 46158 | 39839 | 4948 | 1371 |
| alkohol | 30147 | 26628 | 2676 | 843 |
| ostalo | 15956 | 12791 | 931 | 2234 |
| higijena | 8233 | 7418 | 776 | 39 |
| djeca | 1977 | 1856 | 93 | 28 |
| kucni_ljubimci | 1541 | 1269 | 52 | 220 |

20 nasumičnih proizvoda s `is_food = true` čiji naziv izgleda neprehrambeno (od 2168 koje pogađa `food.SUSPECT_NONFOOD_REGEX`):

| lanac | naziv | kategorija lanca | skupina | izvor |
|---|---|---|---|---|
| gavranovic | SLADOLED KING DESIRE 450ml ČAŠA LEDO | Hrana | hrana | chain |
| ktc | JACK DANIEL S 0,7L + 1 ČAŠA | PIĆA | alkohol | chain |
| plodine | WHISKEY JAMESON 0,7 L + 2 CASE |  | alkohol | ean_inherited |
| studenac | IGRAČKA HUGI WUGI BLOW BUBBLE 12/1 | HRANA | hrana | chain |
| konzum | MEDENJACI DEKORAT SET 480 G LAMBERTZ | HRANA | hrana | chain |
| ribola | ABC 100G SPUŽVA BOB | HRANA | hrana | chain |
| gavranovic | SVIJEĆA ROĐENDANSKA 10kom-rasprodaja | Hrana | hrana | chain |
| roto | WHISKEY JACK DANIELS HONEY 0,70 + 2 ČAŠE (6)\* | ŽESTOKO | alkohol | chain |
| ntl | IGRAČKA FINGER SLUG VELIKI | Ostalo | hrana | ean_inherited |
| ktc | ČOK BOMONI 80g SA GLAZB. IGRAČKOM | HRANA | hrana | chain |
| vrutak | \*TEMPRANILLO CASA SOLAR 0.75L COSECHEROS ZOZP SUHO 2025 -6/1- | VINO INOZEMNO | alkohol | chain |
| boso | SJEME GARDEN KRAST.DUGI ZELENI | ZELENI PROGRAM | hrana | chain |
| branka | ČAJ LIPA CVIJET 50g | HRANA | hrana | chain |
| jadranka_trgovina | LIKER PELINKOVAC 0,7L VERSUS + 2 ČAŠE PROMO | PIĆE | alkohol | chain |
| boso | SJEME GARDEN PRKOS FIORI DOPPI | ZELENI PROGRAM | hrana | chain |
| gavranovic | VREĆICA UKRASNA ZA BOCU 12x36x9cm BIJELA/SIVA - rasprodaja | Hrana | hrana | chain |
| gavranovic | BATERIJE PHILIPS 6F22 9V 1/1-rasprodaja | Hrana | hrana | chain |
| trgovina-krk | JIM BEAM 0,7L + 1 ČAŠE | Piće | alkohol | chain |
| gavranovic | SCABIOSA CVIJET - rasprodaja | Hrana | hrana | chain |
| konzum | KRUH KALUP 600g MARYMAT | HRANA | hrana | chain |

## 1. Jaja

Uzgoj iz naziva: BIO/EKO → bio (prvi, jer „EKO … SLOBODNI UZGOJ“ je ekološki), KAVEZNI → kavezni, PODNI → podni, SLOBODNI → slobodni, inače `nepoznato`. Grupe su `jaja:<veličina>:<uzgoj>` (`get_prices` prima i `jaja:m` za sve uzgoje), a `plan_basket` vraća `attributes` odabranog proizvoda (velicina, uzgoj).

Nazivi u `jaja:m` s krajnjim cijenama po jajetu (≥ 1,00 ili ≤ 0,16 €; 1,30 € je Metroov karton, a 0,10 € je bila donja granica starog raspona):

| lanac | naziv | komada | cijena € | €/kom | trgovina |
|---|---|---|---|---|---|
| metro | 10/1 PERFA JAJA M | 10,00 | 44,10 | 4,41 | 5 |
| metro | 10/1 ARO JAJA A KL M | 10,00 | 44,04 | 4,40 | 7 |
| metro | 10/1 ŽITO JAJA M | 10,00 | 44,04 | 4,40 | 5 |
| metro | 15/1 MC JAJA PODNI UZGOJ M | 15,00 | 45,36 | 3,02 | 7 |
| metro | 30/1 ARO JAJA A KL M | 30,00 | 39,00 | 1,30 | 7 |
| studenac | SVJEŽA JAJA 10/1, RAZRED M | 10,00 | 1,59 | 0,16 | 1 |
| lidl | PERFA Jaja podni uzgoj razred M | 15,00 | 2,25 | 0,15 | 116 |
| lidl | Žito Jaja razred M | 18,00 | 2,75 | 0,15 | 116 |
| lidl | Kones Bi Jaja, razred M | 10,00 | 1,45 | 0,14 | 116 |
| stridon | SVJEŽA JAJA A KLASE RAZRED M 10/1 PERFA | 10,00 | 0,16 | 0,02 | 1 |
| jadranka_trgovina | JAJA SVJEŽA 30/1 KLASA A, RAZRED M | 30,00 | 0,26 | 0,01 | 1 |

Distribucija cijene po jajetu (provjerena hrana, 491 različitih parova proizvod × cijena): 5. percentil **0,19**, medijan 0,31, 95. percentil **0,47** €. **Primijenjeno: `plausible_per_unit: [0.19, 0.47]`** (prije [0.1, 1.5]). Bio i dio slobodnog uzgoja su iznad 0,47 €; ako ih želiš u zadanom izboru, gornja granica bi trebala biti oko 0,55 €.

| uzgoj | proizvoda | p5 | medijan | p95 | izvan granica |
|---|---|---|---|---|---|
| nepoznato | 320 | 0,19 | 0,31 | 0,42 | 25 |
| podni | 118 | 0,19 | 0,33 | 0,48 | 11 |
| kavezni | 24 | 0,16 | 0,25 | 0,29 | 2 |
| slobodni | 18 | 0,30 | 0,37 | 1,20 | 1 |
| bio | 11 | 0,34 | 0,47 | 0,53 | 5 |

Klase (veličina:uzgoj) i broj različitih proizvoda: `-:bio` 10, `-:kavezni` 3, `-:nepoznato` 40, `-:podni` 13, `-:slobodni` 3, `l:kavezni` 6, `l:nepoznato` 102, `l:podni` 41, `l:slobodni` 5, `m:bio` 1, `m:kavezni` 15, `m:nepoznato` 165, `m:podni` 56, `m:slobodni` 10, `s:nepoznato` 5, `s:podni` 2, `xl:nepoznato` 8, `xl:podni` 6

## 2. Zadane varijante

Zadano isključene varijante (vraćaju se samo kad je atribut izričito zadan) i broj grupa (EAN ili lanac + naziv) s tom vrijednošću:

| namirnica | varijanta | grupa | primjer |
|---|---|---|---|
| brasno | tip=integralno | 34 | 1KG FARINA BRAŠ.PŠ.CRNO T-1100 |
| brasno | gluten=bez | 5 | BRASNO BEZ GLUTENA 1 KG NUTRIFREE |
| brasno | vrsta=kukuruzno | 13 | 1KG PODRAVKA BRAŠNO KUKURUZNO |
| brasno | vrsta=pirovo | 33 | BIO BRAŠNO PIR PUN.ZRNO 1 kg |
| brasno | vrsta=razeno | 11 | 900G FARINA RAŽENO BRAŠ T 1250 |
| brasno | vrsta=heljdino | 10 | BRASNO HELJDA 1 KG FARINA SPECIALE |
| secer | vrsta=smedi | 70 | \*\*UGO. ŠEĆER SMEĐI 200/1 LOGO VRIJEME ZA KAVU\*\* |
| secer | vrsta=u_prahu | 22 | \*NE\*ŠEĆER U PRAHU U PET BOČICI 250g |
| secer | vrsta=kocke | 13 | 1KG RIOBA ŠEĆER KOCKA BIJELI |
| ulje | vrsta=avokado | 0 |  |
| ulje | vrsta=sezam | 5 | 2,5L DIAMOND SEZAMOVO ULJE |
| ulje | vrsta=kokos | 6 | Encian ulje kokosa 1 l |
| ulje | vrsta=grozde | 1 | ULJE KOŠTICA GROŽĐA 1 L FARCHI |
| ulje | vrsta=specijalno | 3 | 500ML MC ORAHOVO ULJE |
| ulje | vrsta=omegol | 2 | 1L ZVIJEZDA ULJE OMEGOL |
| ulje | vrsta=mediteran | 2 | ULJE 1L MEDITERAN ZVIJEZDA |
| ulje | presanje=hladno | 5 | Sunce Vinkovaca Hl. preš. sunc.ulje |
| rajcica | vrsta=cherry | 58 | \*RAJČIC CHERRY RFS |
| rajcica | vrsta=datterino | 1 | RAJČICA CHERRY DATERINO 500g SG |
| rajcica | vrsta=harmony | 4 | 500G RAJČICA TREŠNJAR HARMONY |
| rajcica | vrsta=campari | 2 | RAJČICA CAMPARI 400G SNIŽENJE |

- brašno: `vrsta` bez oznake je `psenicno` (zadano); heljdino više nije u `must_not_match`, nego je varijanta.
- šećer: `vrsta` bez oznake je `bijeli`.
- ulje: Zvijezda Omegol i Mediteran su `vrsta=omegol|mediteran`, hladno prešano je `presanje=hladno`.
- rajčica: cherry (i koktel, cocktail, mini), datterino, harmony i campari su izvan zadanog izbora.

**Riža i „oro“:** nijedan proizvod ne dobiva `parboiled` bez riječi „parboiled“ u nazivu (test `test_riza_oro_alone_not_parboiled`). Grupa 8001860190520 prikazuje se kao „Riso Scotti riža oro dugog zrna“, ali isti EAN u 10 lanaca glasi „RIŽA ORO PARBOILED“, pa je skupni atribut `parboiled` s izvorom `name`. To nisam mijenjao: Scotti Oro jest parboiled riža.

Izvor atributa za 10 grupa riže (`find_products(ingredient="riza")`):

| id | naziv | atributi | izvor (how, naziv) |
|---|---|---|---|
| 8001860100017 | Riso Scotti riža originario okr.zrno 1kg | vrsta=originario | vrsta: name („RIŽA ORIGINARIO 1 kg SCOTTI“) |
| 3838700540291 | RIŽA ZA DOMAĆA JELA ZLATO POLJE PODRAVKA 1 kg (12) | vrsta=originario | vrsta: name („RIŽA ZL.POLJE 1 kg (OKRUGLO ZRNO)“) |
| 3838700540369 | RIŽA ZLATO POLJE BLAZINICA PODRAVKA 800 g (9) |  |  |
| 8001860201011 | Riso Scotti riža arborio dugo zrno 1kg | vrsta=arborio | vrsta: name („RIŽA ARBORIO 1 kg SCOTTI“) |
| 8001860190520 | Riso Scotti riža oro dugog zrna 1kg | vrsta=parboiled | vrsta: name („RIŽA SCOTTI ORO 1 kg PARBOILED“) |
| 3838700540314 | RIŽA BIJELA 800 g VREĆICA ZLATO POLJE | vrsta=dugo_zrno | vrsta: name („Zlato polje riža dugo zrno pvc 800 g“) |
| 3838700540482 | RIŽA ZL POLJE ST ANDREA 500G KUT (18) |  |  |
| 5410673007490 | RIZA PARABOILED DUGO ZRNO VRECICA 500 G BENS ORIGINAL | vrsta=dugo_zrno | vrsta: name („RIŽA DUGO ZRNO 500 g 4 VREĆICE BEN S“) |
| 3838700540406 | RIŽA ZL POLJE ST ANDREA 1KG KUT VAK (12) |  |  |
| 3838700540604 | RIŽA ARBORIO VAKUMIRANA 1000 g PODRA | vrsta=arborio | vrsta: name („RIZA ARBORIO 1 KG VP ZLATO POLJE“) |

## 3. Kakao

Pozitivno podudaranje: naziv počinje s „kakao“ ili sadrži „kakao prah“, „prah kakao“, „kakao u prahu“ (i „kakao u pr.“), „kakao za kolače“. Isključeno: tortela, tortin, muffin, krema, benquick, napitak, choco box, te (moja dopuna) desert, kolač, rolice, šnite, biskvit, krafne, tabla (čokolada), instant i vending napitci, Dolce Gusto, „XXL“ i Lumpi (instant napitak).

Grupa prije: **173**, poslije: **31**.

Top 10:

| id | naziv | pakiranje | lanaca | €/kg |
|---|---|---|---|---|
| 3858881044012 | KAKAO PRAH KANDIT 100G -12/1- SMANJENE MASTI 16-18% | 100 g | 21 | 16,60–30,80 |
| 3850102110292 | KAKAO PRAH 100G (21), KRAŠ (PAL-90) | 100 g | 20 | 17,90–30,90 |
| 5997381346917 | KAKAO DR OETKER ZA KOLAČE 70G-16/1- | 70 g | 14 | 19,00–38,71 |
| 3858881773608 | KAKAO U PRAHU ANAMARIJA 100 g | 100 g | 9 | 9,30–30,50 |
| 3858891566221 | ULTRA KAKAO U PRAHU 100G ,ANAMARIJA | 100 g | 5 | 8,30–23,90 |
| 3850334055149 | KAKAO PRAH SWEET CHEF 250G (12) | 250 g | 2 | 17,32–21,16 |
| 3858890134360 | EKO KAKAO U PR.200 g EKOZONA | 200 g | 2 | 26,25–38,45 |
| 3850102945085 | KAKAO PRAH 100 g KRAŠ (21) | 100 g | 2 | 14,90–24,30 |
| 9100000963976 | KAKAO PRAH S-BUDGET 250 g | 250 g | 1 | 19,92–19,92 |
| 4002309015217 | KAKAO SUCHARD BENSDORP 125 g | 125 g | 1 | 35,92–35,92 |

## 6. Sol i soljenka

`soljenk` više nije u `must_not_match`. Novo polje `require_pack: [soljenk]`: soljenka ispada iz soli samo ako nema gramature (`drop_reason = 'bez_gramature'`, prazna posuda).

Test „SOL MORSKA SITNA 250G SOLJENKA“: u soli (vrutak: sol); testovi `test_sol_soljenka_*`.

Svi proizvodi soli sa „soljenk“ (20):

| lanac | naziv | g | status |
|---|---|---|---|
| jadranka_trgovina | SOL SITNA MORSKA 250g PAG91 SOLJENKA | 250,00 | sol |
| konzum | SOL MORSKA SITNA SOLJENKA 250g SOLANA NIN | 250,00 | sol |
| konzum | SOL SOLJENKA 250g PVC SOLANA PAG | 250,00 | sol |
| konzum | SOL SOLJENKA 450g PVC SOLANA PAG | 450,00 | sol |
| ktc | SOL MORSKA 250G,SOLJENKA | 250,00 | sol |
| lorenco | SOL MORSKA KUHINJ.250G-SOLJENKA | 250,00 | sol |
| plodine | SOL 250 G SITNA SOLJENKA PAG 91 | 250,00 | sol |
| plodine | SOL 500 G SITNA SOLJENKA TEGLICA PAG 91 | 500,00 | sol |
| plodine | SOL LIGHT 250 G SOLJENKA PVC SOLANA PAG | 250,00 | sol |
| plodine | SOL SITNA SOLJENKA 250 G | 250,00 | sol |
| plodine | SOL SITNA SOLJENKA 450 G SOLANA PAG | 450,00 | sol |
| plodine | SOL SOLJENKA SITNA 250 G PLODINE | 250,00 | sol |
| roto | SOL SOLJENKA 250g PVC SOLANA PAG (12) | 250,00 | sol |
| stridon | SOL MORSKA SOLJENKA 250 gr (12) | 250,00 | sol |
| tommy | SOL SITNA SOLJENKA 250 g PAG | 250,00 | sol |
| tommy | SOL SITNA SOLJENKA 450 g | 450,00 | sol |
| trgovina-krk | SOL 250 g SOLJENKE PAG | 250,00 | sol |
| trgovina-krk | SOL 250 g SOLJENKE PAG 91 | 250,00 | sol |
| vrutak | SOL KAMENA 250G SOLJENKA -15/1- TUZLA | 250,00 | sol |
| vrutak | SOL MORSKA SITNA 250G SOLJENKA -12/1- PAG | 250,00 | sol |

## 7. Mlijeko

Zadano `vrsta=trajno, mast=2.8` (`default_attributes`), a masnoća 2,8–3,8 % je zamjenjiva (`substitutes: {mast: [2.8, 3.2, 3.5, 3.8]}`). Svježe i trajno su zasebne vrste (nisu zamjenjive). `plan_basket` vraća `applied_attributes` i `accepted_values` po sastojku, te `attributes` (vrsta, mast) odabranog proizvoda; zamjena ide u `notes`. Novo prepoznavanje: „TR“ = trajno, „SV.“ = svježe.

Isključeni krivi pogoci: palačinke s mlijekom, acidofilno, kiselo („KIS.“), protein, „ČOKOL.“.

Proizvodi po vrsti i masnoći (`-` = nije u nazivu; bez vrste ne ulaze u zadani izbor):

| vrsta | mast | proizvoda |
|---|---|---|
| - | - | 78 |
| - | 0 | 15 |
| - | 0.5 | 7 |
| - | 0.9 | 8 |
| - | 1.5 | 45 |
| - | 2.8 | 78 |
| - | 3.2 | 8 |
| - | 3.5 | 24 |
| - | 3.8 | 36 |
| svjeze | - | 15 |
| svjeze | 1.5 | 30 |
| svjeze | 3.2 | 127 |
| svjeze | 3.5 | 1 |
| svjeze | 3.8 | 1 |
| trajno | - | 42 |
| trajno | 0 | 3 |
| trajno | 0.5 | 10 |
| trajno | 0.9 | 24 |
| trajno | 1.5 | 39 |
| trajno | 2.8 | 200 |
| trajno | 3.5 | 27 |
| trajno | 3.8 | 53 |

Primjer: `plan_basket` 0,5 l mlijeka u Osijeku (prvih 8 trgovina):

| lanac | adresa | proizvod | vrsta | mast | € | zamjena |
|---|---|---|---|---|---|---|
| lidl | Ulica J. J. Strossmayera 350 | Križevačka mljekara Trajno mlijeko | trajno | 2.8 | 0,52 |  |
| lidl | Zeleno Polje 8 A | Križevačka mljekara Trajno mlijeko | trajno | 2.8 | 0,52 |  |
| lidl | Svetog Leopolda Bogdana Mandića 33 A | Križevačka mljekara Trajno mlijeko | trajno | 2.8 | 0,52 |  |
| eurospin | Ulica Josipa Jurja Strossmayera 343A | MLIJEKO TRAJNO 2,8% m.m.1l | trajno | 2.8 | 0,62 |  |
| eurospin | Ulica 3 gardijske brigade „Kune“ 30 | MLIJEKO TRAJNO 2,8% m.m.1l | trajno | 2.8 | 0,62 |  |
| ntl | Dobra ulica 2, Brijest, Osijek | MLIJEKO TRAJNO 2,8 % m. m. 1L TOJETO | trajno | 2.8 | 0,65 |  |
| ntl | P.E.SAVOJSKOG 38 | MLIJEKO TRAJNO 2,8 % m. m. 1L TOJETO | trajno | 2.8 | 0,65 |  |
| ntl | LOSINJSKA 43 | MLIJEKO TRAJNO 2,8 % m. m. 1L TOJETO | trajno | 2.8 | 0,65 |  |

## 8. Peršin i svježe bilje

Peršin: `unit: kg`, `pantry: true` (u ukupno ulazi utrošeni dio). Proizvodi bez gramature i bez cijene po kg (vezice, komadi) se ne pretvaraju: nemaju cijenu po kg, pa ne ulaze u usporedbu ni u košaricu, a jedinica „vezica“ u receptu daje grešku (nema pretpostavljene mase). Drugog svježeg bilja u rječniku još nema (bosiljak, kopar i vlasac su samo isključenja kod drugih namirnica).

| proizvodi | broj | min €/kg | medijan €/kg | max €/kg | primjer |
|---|---|---|---|---|---|
| bez cijene po kg (vezica/komad) | 12 |  |  |  | BIO PERŠIN FRANCUSKI U TEGLAMA |
| cijena po kg | 49 | 0,20 | 6,36 | 27,96 | 500G PERŠIN KORIJEN |

`plan_basket` 20 g peršina u Zagrebu: stridon, „PERŠIN KORJEN AGROVIR“, pakiranje 0,04 €, utrošeno (u ukupno) 0,04 €.

## 9. Pretvorba mjera (PROCJENE, za pregled)

`data/units.yaml` i `src/mealmeter/units.py` (`convert(amount, unit, staple)` → (količina, g|ml, upozorenja)). `plan_basket` prima ove mjere; svaka pretvorba vraća upozorenje s korištenom vrijednošću. Namirnica bez gustoće računa se s 1 g/ml (uz upozorenje), a namirnica u komadima (jaja) ne može se mjeriti žlicom.

| mjera | ml | aliasi | procjena |
|---|---|---|---|
| zlica | 15,0 | žlica, žlice, žlicu, jušna žlica, jušne žlice, velika žlica | da |
| zlicica | 5,0 | žličica, žličice, čajna žličica, čajne žličice, mala žlica | da |
| salica | 250,0 | šalica, šalice, šalicu | da |
| dcl | 100,0 | dcl, decilitar, decilitra | da |
| prstohvat | 0,5 | prstohvat, prstohvata | da |
| casa | 200,0 | čaša, čaše, čašu | da |

| namirnica | g/ml | 1 žlica | 1 žličica | 1 šalica | procjena |
|---|---|---|---|---|---|
| brasno | 0,55 | 8,2 g | 2,8 g | 137,5 g | da |
| secer | 0,85 | 12,8 g | 4,2 g | 212,5 g | da |
| sol | 1,20 | 18,0 g | 6,0 g | 300,0 g | da |
| ulje | 0,92 | 15,0 ml | 5,0 ml | 250,0 ml | da |
| mlijeko | 1,03 | 15,0 ml | 5,0 ml | 250,0 ml | da |
| maslac | 0,95 | 14,2 g | 4,8 g | 237,5 g | da |
| riza | 0,85 | 12,8 g | 4,2 g | 212,5 g | da |

## 10. Kvasac, prašak za pecivo, vanilin šećer: granice po vrećici

Automatske granice (0,25x–4x medijana) su ugašene; cijena se uspoređuje po vrećici (`compare_by: pack`), a granice su `plausible_per_pack` (`clean.staple_rules.range_source = 'pack'`). Prijedlog iz podataka: 5. percentil do 1,25 × 95. percentila cijene **pojedinačnih vrećica**, zaokruženo na 0,05 €. `price_suspect` je cijena po vrećici iznad gornje granice, ili pojedinačna vrećica ispod donje; rinfuza i višestruka pakiranja smiju biti jeftinija po vrećici (prije je zato 18 % kvasca bilo odbačeno).

| namirnica | pojedinačnih vrećica | p5 € | medijan € | p95 € | max € | granice € | odbačeno prije | odbačeno sada |
|---|---|---|---|---|---|---|---|---|
| kvasac | 185 | 0,30 | 0,61 | 0,99 | 24,49 | 0,30–1,25 | 2250 / 12364 (18,2 %) | 156 / 12364 (1,3 %) |
| prasak_za_pecivo | 62 | 0,11 | 0,20 | 0,29 | 0,39 | 0,10–0,40 | 10 / 6024 (0,2 %) | 21 / 6024 (0,3 %) |
| vanilin_secer | 143 | 0,12 | 0,24 | 0,65 | 1,69 | 0,10–0,85 | 333 / 9639 (3,5 %) | 176 / 9639 (1,8 %) |

Najčešće cijene izvan granica:

| namirnica | lanac | naziv | vrećica | cijena € | €/vrećica | trgovina |
|---|---|---|---|---|---|---|
| kvasac | kaufland | KLC.Suhi kvasac 7 g | 1,00 | 0,13 | 0,13 | 53 |
| kvasac | ribola | KVASAC SUH.10g ALEVA | 1,43 | 0,36 | 0,25 | 32 |
| kvasac | ktc | KVASAC SVJEŽI 50g(2\*25g) DUOS | 1,19 | 0,35 | 0,29 | 18 |
| kvasac | ribola | KVASAC SUH.10g ALEVA | 1,43 | 0,37 | 0,26 | 13 |
| kvasac | roto | KVASAC SVJEŽI 42g HARMER (24) | 1,00 | 0,24 | 0,24 | 9 |
| prasak_za_pecivo | stridon | PRAŠAK ZA PECIVO 13 g BONITO (60) | 1,08 | 0,07 | 0,06 | 12 |
| prasak_za_pecivo | metro | 1KG ARO PRAŠAK ZA PECIVO | 83,33 | 35,38 | 0,42 | 7 |
| prasak_za_pecivo | metro | 12GX6 DOLCELA PRAŠAK ZA PECIVO | 6,00 | 32,40 | 5,40 | 2 |
| vanilin_secer | gavranovic | KOTANYI BOURBON VANILIN ŠEĆER 10g | 1,25 | 1,19 | 0,95 | 121 |
| vanilin_secer | eurospin | VANILIN AROMA (5VRE.)2G | 0,25 | 0,39 | 1,56 | 43 |
| vanilin_secer | stridon | VANILIN ŠEĆER 10 g BONITO (55) | 1,25 | 0,07 | 0,06 | 4 |
| vanilin_secer | metro | 6X8G DOLCELA VANILIN ŠEĆER 5+1 | 6,00 | 24,30 | 4,05 | 2 |
| vanilin_secer | stridon | DOLCELA VANILIN ŠEĆER 8 g 10kom PODRAVKA | 1,00 | 1,59 | 1,59 | 2 |

Napomena: donja granica kvasca (0,30 €) pogađa i vjerojatno stvarne cijene trgovačkih marki (Kaufland 0,13 €, Harmer 0,24 €). Ako su to stvarne cijene, donja granica bi trebala biti oko 0,10 €.

## 11. Oblik mahunarki, kukuruza i gljiva

Heuristika: konzerva ako naziv ili stupac `unit` sadrži LIM, LIMENK, OC.MASA, OCIJE, STAKLO, VAKUM ili NALJEV (uz postojeće oznake: konz, ocij., neto, 400/240 g…). Smrznuto ako sadrži LEDO, SMRZ, FROZY, FRESCO ili ZAMRZ. Suho (`dry_rule`, `how = heuristic`) ako je pakiranje 400–1000 g, nema oznaka konzerve ni smrznutog, a `unit` je rinfuza ili naziv sadrži PVC, VREĆICA, NATURA, VEDRINI, PRIMAVITA ili ADVENT. Vrećica i PVC više sami ne znače suho, nego samo uz taj uvjet. Gljive nemaju `dry_rule` (500 g u vrećici su svježi šampinjoni). Stupac `unit` u ovoj arhivi nikad ne sadrži LIM ni RINF (KOM/KG), pa provjera stupca zasad ništa ne mijenja.

Broj grupa po obliku, sada (prije); vrijednost grupe je ona s najviše proizvoda:

| namirnica | konzerva | suho | smrznuto | svjeze | nepoznato |
|---|---|---|---|---|---|
| gljive | 7 (7) | 1 (1) | 1 (1) | 17 (17) | 90 (90) |
| grah | 72 (72) | 38 (28) | 4 (4) | 1 (1) | 303 (313) |
| grasak | 24 (24) | 6 (4) | 27 (19) | 0 (0) | 96 (106) |
| kukuruz | 27 (27) | 0 (0) | 6 (5) | 2 (2) | 125 (126) |
| leca | 11 (10) | 17 (11) | 0 (0) | 0 (0) | 104 (111) |
| slanutak | 20 (20) | 10 (7) | 2 (2) | 0 (0) | 95 (98) |

20 nasumičnih grupa: **konzerva**

| namirnica | grupa | naziv | g | izvor |
|---|---|---|---|---|
| grah | 3856003929698 | GRAH CRVENI 400g-ocijeđene mase 240g ZORELA | 240,00 | naziv |
| grasak | 3083680538404 | N-GRAŠAK BONDUELLE 200G(NETTO 130G) -12/1 | 200,00 | naziv |
| slanutak | 3856022650931 | SLANUTAK 400 G CAMPO KUHANI STERILIZIRANI | 400,00 | naziv |
| kukuruz | 3859891493371 | Kukuruz kuhani vakum 2/1 | 400,00 | naziv |
| kukuruz | 3856015305718 | KUKURUZ 340G LIM.ZVIJEZDA | 340,00 | naziv |
| grah | 3858891568539 | ULTRA GRAH CRVENI 400G/240G (24) ( 1728 PAL) | 400,00 | naziv |
| grah | 3850104020728 | Podravka crveni grah, lim 800g/460g | 800,00 | naziv |
| grah | 3850104025389 | Podravka grah smeđi 800g/460g | 800,00 | naziv |
| grah | 3856022650832 | GRAH SMEDJI 800 G CAMPO KUHANI STERILIZIRANI | 800,00 | naziv |
| grasak | 3850104050800 | GRAŠAK PODRAVKA 4200G -2/1- | 4200,00 | naziv |
| grasak | 3850104050855 | GRAšAK 4,2KG LIM IIK PODR. | 4200,00 | naziv |
| grasak | 3017800127964 | GRAŠAK 400g/270g | 400,00 | naziv |
| leca | 8017596014825 | LEĆA ZELENA 400g/240g | 400,00 | naziv |
| grah | 3856003929704 | GRAH BIJELI 800g-ocijeđena masa 480g ZORELA | 480,00 | naziv |
| grah | 3858886520979 | GRAH CRVENI 2500G/1500G,MARI | 2500,00 | naziv |
| grasak | 3856003912102 | GRAŠAK ZORELA 400g- ocjeđena masa 265g | 265,00 | naziv |
| kukuruz | 8017596108258 | KUKURUZ SLATKI 340g/285g | 340,00 | naziv |
| grah | 3858883225228 | GRAH ŠARENI 400g/240g O.M. CANNELLINI | 400,00 | naziv |
| grah | 8717496900166 | KONZ. GRAH SMEĐI BIOVEGA 400g/240g | 400,00 | naziv |
| leca | 8001300243120 | LEĆA DESPAR KUHANA 400 g | 400,00 | naziv |

20 nasumičnih grupa: **suho**

| namirnica | grupa | naziv | g | izvor |
|---|---|---|---|---|
| grah | gavranovic:grah zelencak rfs | GRAH ZELENČAK RFS |  | naziv |
| grah | 3859888609761 | GRAH BIJELI 500 g SUHI MARCO POLO | 500,00 | naziv |
| grasak | 3859891427932 | GRASAK SUHI-POLOVICE |  | naziv |
| grah | trgocentar:grah tresnjevac rinfuza pt | GRAH TREŠNJEVAC RINFUZA (PT) |  | naziv |
| slanutak | 3859890587026 | SLANUTAK NATURA 500g | 500,00 | heuristika |
| grah | gavranovic:grah sareni rinfuza | GRAH ŠARENI RINFUZA |  | naziv |
| grah | 3859890118039 | GRAH ŠARENI KANADA RFS |  | naziv |
| grah | 3858882920315 | GRAH MUNGO SOJA ZELENA 500g PRIMAVITA ADVENT | 500,00 | heuristika |
| grah | tommy:grah tresnjevac rfs | GRAH TREŠNJEVAC RFS |  | naziv |
| leca | 3859890630784 | Vedrini Leća zelena 1 kg | 1000,00 | heuristika |
| grah | 3858889330001 | Grah šareni RFS |  | naziv |
| leca | bure:leca rfs | LEĆA RFS |  | naziv |
| grah | gavranovic:grah zelencak rfs snizenje | GRAH ZELENČAK RFS SNIŽENJE |  | naziv |
| grah | ribola:grah bijeli rfs | GRAH BIJELI RFS |  | naziv |
| grah | 3858889333484 | Vedrini Grah crveni 1 kg | 1000,00 | heuristika |
| gljive | 3859889098243 | SAMPINJONI RINFUZO |  | naziv |
| grah | trgocentar:grah tresnjevac rinfuza | GRAH TREŠNJEVAC RINFUZA |  | naziv |
| leca | vrutak:leca zelena rinfuza | LEĆA ZELENA RINFUZA |  | naziv |
| leca | trgovina-krk:leca zelena rfs | LEĆA ZELENA RFS |  | naziv |
| slanutak | 3858889331015 | Vedrini Slanutak 1 kg | 1000,00 | heuristika |

20 nasumičnih grupa: **smrznuto**

| namirnica | grupa | naziv | g | izvor |
|---|---|---|---|---|
| grasak | 3850116058627 | ZAMRZ LEDO 700 g GRAŠAK XXL | 700,00 | naziv |
| grasak | 3859889284585 | N-GRAŠAK FROZY 400G -10/1- | 400,00 | naziv |
| slanutak | tommy:brudet od hobotnice sa grahom i slanutkom smrz | BRUDET OD HOBOTNICE SA GRAHOM I SLANUTKOM SMRZ. |  | naziv |
| grah | tommy:grah s kob smrz | GRAH S KOB.SMRZ. |  | naziv |
| grasak | 3858891042558 | GRAŠAK 2.5kg FROZY | 2500,00 | naziv |
| grasak | 3850116036502 | GRAŠAK 2,5KG LEDO | 2500,00 | naziv |
| kukuruz | 5999553897074 | KUKURUZ SMRZ. 2,5 kg DELTA | 2500,00 | naziv |
| grasak | 3858893738893 | GRAŠAK SMRZNUTI FROSTITA 400 g | 400,00 | naziv |
| grasak | 8600038002285 | ZAMRZ PIK B 450 g GRAŠAK | 450,00 | naziv |
| grasak | trgocentar:grasak smrznuti 2 5kg euro alfa | GRAŠAK SMRZNUTI 2,5KG EURO ALFA | 2500,00 | naziv |
| grasak | 3877000505487 | GRAŠAK SMRZNUTI 1000 g AG | 1000,00 | naziv |
| grasak | 3877000505791 | GRAŠAK SMRZNUTI 400 g AG | 400,00 | naziv |
| grasak | 3850116609287 | GRAŠAK 2.5KG LEDO | 2500,00 | naziv |
| grasak | 3850116053165 | ZAMRZ LEDO 400 g GRAŠAK | 400,00 | naziv |
| grasak | 3435649848435 | VERNET GRAŠAK 400g SMRZ. | 400,00 | naziv |
| grah | 3850116053134 | GRAH 400g LEDO | 400,00 | naziv |
| grasak | 3858892941645 | GRAŠAK SMRZNUTI 400 g T! | 400,00 | naziv |
| grasak | lidl:grasak smrznuto | Grašak, smrznuto | 1000,00 | naziv |
| kukuruz | 3858891042794 | FROZY KUKURUZ ŠEĆERAC ZMH HORVAT (2,5kg) | 2500,00 | naziv |
| grasak | 3850116104362 | FRESCO GRAŠAK 2500G LEDO | 2500,00 | naziv |

Zapažanja:
- Većina preostalih `nepoznato` su konzerve bez oznake u nazivu („GRAH ZVIJEZDA 420 g“, „GRAŠAK 400 g ZVIJEZDA“, „KUKURUZ ŠEĆERAC 340g“). Dodatni signal mogao bi biti tipična gramatura limenke (212/340/400/425 g) uz marku konzervi, ali to nije dio zadane heuristike.
- Krivi pogoci u uzorku (gotova jela): „GRAH S KOB.SMRZ.“ („KOB.“ nije `kobasic`) i „SIPA SA SLANUTKOM SMRZ.“; nisu ispravljeni u ovom koraku.

## 12. cijene.dev bez API ključa

Provjereno 2026-10-20 (curl, bez zaglavlja `Authorization`):

| zahtjev | HTTP | napomena |
|---|---|---|
| GET https://api.cijene.dev/v0/list | 200 | JSON s popisom arhiva (~70 kB) |
| HEAD https://api.cijene.dev/v0/archive/2026-10-19.zip | 200 | content-length 128.905.233 |
| GET …/2026-10-19.zip, Range: bytes=0-1023 | 206 | application/zip |
| HEAD https://api.cijene.dev/v0/archive/2026-10-20.zip | 200 | objavljena u 14:26 |

Ključ nije potreban, pa `update.py` nije mijenjan; zapis je u SCHEMA.md (Dnevno ažuriranje).
