# Korak 6: priprema za javnu objavu

| točka | stanje |
|---|---|
| 0 grah "nedostaje" u Lidlu, Eurospinu, NTL-u i Rotu | gotovo: pravilo oblika popravljeno, test i zlatni scenarij |
| 1 NTL Osijek: 34 trgovine, na karti ~18 | provjereno: grad je iz cjenika, bez popravka |

Ništa nije deployano.

## 0. Suhi grah u Lidlu, Eurospinu, NTL-u i Rotu

Upit: `plan_basket` (Osijek, grah 500 g, `form: "suho"`), puna baza od 20.10.2026. Količina je količina gotovog
graha, pa je potrebno 200 g suhog (prinos 2,5x).

**Prije:** usporedba je imala Konzum, Spar, Plodine i Kaufland; Lidl i Eurospin su bili u `incomplete` ("nedostaje:
grah"). NTL i Roto nisu veći lanci (`MAJOR_CHAINS`), pa se u `incomplete` ne ispisuju; nije ih bilo ni u
`more_chains`, dakle ni oni nisu imali suhi grah.

**Sirovi nazivi.** Sva četiri lanca imaju suhi grah (pretraga `grah|pasulj|bean|fižol` u `products`; "pasulj" i
"fižol" se ne pojavljuju, "bean" samo u Jelly Beans, kavi i viskiju). Primjeri, s brojem trgovina u Osijeku:

| lanac | proizvod | pakiranje | trgovine u Osijeku |
|---|---|---|---|
| lidl | Grah trešnjevac | 500g | 3 |
| lidl | Grah bijeli; Grah trešnjevac 12/1 | ca. 1kg | 3 |
| eurospin | GRAH BORLOTTI ŠARENI 500g; GRAH BORLOTTI ŠARENI 1kg; GRAH TETOVAC BIJELI 1kg | 0,5 / 1 kg | 2 |
| ntl | GRAH PINTO 1 kg; GRAH BIJELI 1 kg; GRAH ŠARENI 1 kg; GRAH ZELENČEK 500 G | 1 kg / 0,5 kg | 34 (vidi točku 1) |
| roto | GRAH ŠARENI RIAL 1000g (8) | 1 kg | 1 |

**Zašto ih staples.yaml nije prihvaćao.** `must_match`, `must_not_match`, `plausible` i `is_food` nisu bili uzrok:
svi ti proizvodi su bili `grah`, nisu isključeni (`excluded = false`, `drop_reason` prazan) i jesu hrana. Uzrok je
atribut `oblik`: naziv ne kaže "suho", pa je oblik bio `nepoznato`, a `form: "suho"` traži `oblik = suho`.
`dry_rule` je oblik `suho` davao samo kad je uz pakiranje 400-1000 g i unit rinfuza ili naziv sadrži PVC, vrećicu ili
jednu od četiri marke (Natura, Vedrini, Primavita, Advent). Zato je u Konzumu prolazio samo "GRAH PINTO VEDRINI 500 g",
a "GRAH GARDEN GOOD ŠARENI 500g" nije. Pravilo je bilo prestrogo u svim lancima: 509 proizvoda graha imalo je oblik
`nepoznato`, među njima 76 pakiranja od točno 500 g ili 1 kg, gotovo sve suhi grah.

**Popravak** (`staples.yaml`, `staples.form_heuristic`):
- `dry_rule.pack_exact: [500, 1000]`: pakiranje od točno 500 g ili 1 kg, bez oznake konzerve ili smrznutog u nazivu i
  stupcu unit, i bez `not_words` (gastro, varivo, kobas), je `suho`. Konzerve su 400-480 g ili 800-850 g (i "400/240 g"
  s ocijeđenom masom), pa ih pravilo ne pogađa. Vrijedi za grah, leću i slanutak. Grašak i kukuruz ga nemaju, jer je
  grašak od 1 kg obično smrznut ("GRAŠAK GARDEN GOOD 1kg", "Grašak" 1kg u Lidlu).
- Grah, nove oznake konzerve: `OM` (ocijeđena masa: "Bijeli grah, OM 240g"), "u slanoj vodi" i "sterilizirani".

**Učinak na punoj bazi** (usporedba s atributima prije popravka): `nepoznato → suho` 192 proizvoda (grah 74, leća 80,
slanutak 38), `nepoznato → konzerva` 14 (Lidlovi OM i sterilizirani, "u slanoj vodi"). Ručno pregledana su sva 192
naziva: svi su suhe mahunarke (Garden Good, K-Classic, Spar, Marjan voće, Zlatno zrno, dmBio, Eurospin, NTL...).
Ostaju `nepoznato`: Lidl "Grah trešnjevac" 800g (Campo Largo, vjerojatno suh, ali 800 g je i limenka), NTL "GRAH
PINTO"/"GRAH ŠARENI" bez gramature (na vagu) i Zorela 480 g (vjerojatno staklenka).

**Poslije:** Konzum 1,19 €, Spar 1,19 €, Kaufland 1,49 €, Lidl 1,49 € (Grah trešnjevac 500g), Plodine 1,51 €, Eurospin
1,59 € (Borlotti 500g); u `more_chains` Roto 2,16 € (Rial 1000g) i NTL 2,69 € (Zelenček 500 G). `incomplete` je prazan.

**Provjera:**
- `tests/test_step6.py`: `pack_exact` (NTL, Lidl, Eurospin, Roto, leća, slanutak; 800 g, 480 g, gastro, varivo, 1 L i
  grašak ostaju bez oblika) i nove oznake konzerve.
- Zlatni scenarij `basket_grah_suho_osijek` (22 scenarija); test uz `MM_GOLDEN=1` provjerava da su Lidl, Eurospin, NTL
  i Roto u usporedbi i da je `incomplete` prazan. Ostalih 21 zlatnih izlaza je nepromijenjeno nakon ponovne izgradnje.
- Puna baza ponovno izgrađena (`scripts/build_clean.py`), sažeta baza (`scripts/build_compact.py`) također.
- pytest: izlazni kod 0 (993 prolazi, 2 preskočena); uz `MM_GOLDEN=1` na punoj bazi izlazni kod 0. Sažeta baza
  (91,8 MB): `golden.py --check` 22/22 jednako.

## 1. NTL Osijek: 34 trgovine u izlazu, ~18 na karti

**Kako se određuje grad.** Za NTL se grad ne izvodi ni iz adrese ni iz poštanskog broja: `clean.stores.city` je
stupac `city` iz NTL-ova `stores.csv` (cijene.dev), a `city_key` je samo `norm_text` toga (bez aliasa; Kaufland je
jedini lanac kojem se grad popunjava iz adrese). `n_stores_city` broji trgovine lanca u gradu koje imaju proizvod.

**Nalaz.** U `data/raw/2026-10-20/ntl/stores.csv` 34 retka imaju `city = Osijek`, sve tipa `minimarket`, s 34 različite
adrese (npr. A. Kanižlića 31, Anina 83, Divaltova 183, Dobra ulica 2 Brijest, Tvrđavica 47, Svilajska 36). Sve 34
trgovine imaju cijene u dnevnom cjeniku (npr. "GRAH PINTO 1 kg" u svih 34). Adrese su u Osijeku ili njegovim
prigradskim naseljima (Brijest, Tvrđavica, Bosutsko naselje), pa grad nije pogrešno pripisan. Brojevi trgovina imaju
više serija (202xx, 203xx, 205xx, 206xx-207xx); NTL je savez trgovaca, pa je moguće da karta na ntl.hr prikazuje samo
dio prodajnih mjesta (format ili članice). Karta na ntl.hr učitava trgovine dinamički, pa je ovdje nisam mogao
usporediti redak po redak.

**Zaključak:** 34 je broj koji NTL sam objavljuje u cjeniku za Osijek. Nema očitog i malog popravka; ništa nije
promijenjeno. Ako treba, sljedeći korak je usporedba s popisom s karte (ručno, iz preglednika).

**Provjera:** pytest izlazni kod 0.
