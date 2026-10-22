# Korak 6: priprema za javnu objavu

| točka | stanje |
|---|---|
| 0 grah "nedostaje" u Lidlu, Eurospinu, NTL-u i Rotu | gotovo: pravilo oblika popravljeno, test i zlatni scenarij |
| 1 NTL Osijek: 34 trgovine, na karti ~18 | provjereno: grad je iz cjenika, bez popravka |
| 2 tajne u Git povijesti | provjereno: nema tajni |
| 3 LICENSE i navod izvora podataka | gotovo, ali **tekst licence podataka je drukčiji od traženog** (vidi dolje) |
| 4 README.md | gotovo |

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

## 2. Tajne u Git povijesti

Pregledani su svi commitovi (`--all`, 129 commitova, jedna grana `master`).

- **gitleaks 8.21.2** (službeno izdanje s GitHuba, SHA-256 provjeren prema `checksums.txt`):
  `gitleaks git --log-opts="--all" --redact .` → "129 commits scanned, no leaks found".
- **Datoteke:** nijedna `.env*`, `.vercel/`, `*.pem`, `id_rsa`, `.npmrc` ni `.netrc` nikad nije bila u povijesti
  (`git log --all --name-only`). `.gitignore` isključuje `.env`, `.env*`, `.vercel/` i baze.
- **Ručna pretraga** dodanih redaka (`git log --all -p`) za `api_key`, `secret`, `token`, `password`/`lozinka`,
  `bearer`, `Authorization:`, `PRIVATE KEY`, `ghp_`, `github_pat_`, `sk-…`, `AKIA…`, `xox[bp]-`, JWT (`eyJ…`),
  `prj_…`, `team_…`: nema vrijednosti. `VERCEL_TOKEN`, `VERCEL_ORG_ID` i `VERCEL_PROJECT_ID` pojavljuju se samo kao
  `${{ secrets.… }}` u `.github/workflows/update.yml` i kao upute u `docs/DEPLOY.md`.

**Nije tajna, ali postaje javno objavom:**
- autor commitova je `MrSphinx67 <282975938+MrSphinx67@users.noreply.github.com>` (sve commitove);
- lokalna putanja `/home/fran-mostarkic/mealmeter/...` u `docs/smoke_4b.md`, `docs/smoke_4c.md` i `docs/smoke_5b.md`
  (korisničko ime na računalu). Ništa od toga nije mijenjano; za e-poštu bi trebalo prepisati povijest, što nisam radio.

**Provjera:** pytest izlazni kod 0.

## 3. LICENSE i navod izvora podataka

**LICENSE** već postoji (od ranije, nepromijenjen): MIT, "Copyright (c) 2026 Fran Mostarkić".

**Licenca podataka, provjereno 22.10.2026. na izvoru (ne iz sjećanja):**
- `https://cijene.dev` i `https://cijene.dev/uvjeti-koristenja` (DobarKod) **ne navode licencu** za podatke. Uvjeti,
  točka 4 (Intelektualno vlasništvo): "Podaci dostupni putem Usluge prikupljeni su iz javno dostupnih izvora."
  i "Korisnik može slobodno koristiti podatke u svojim aplikacijama, ali bez izričitog jamstva točnosti." Točka 3.3:
  za veće potrebe kontaktirati pružatelja za komercijalni plan.
- Repozitorij `github.com/senko/cijene-api`: kod je AGPL-3.0, a **CC BY-NC-SA 4.0 vrijedi samo za
  `enrichment/products.csv`** ("Pročišćeni CSV podaci o proizvodima (`enrichment/products.csv`) dostupni su pod CC
  BY-NC-SA licencom."). Mealmeter tu datoteku ne koristi, nego dnevne arhive `api.cijene.dev/v0/archive/<datum>.zip`.
- `archive-info.txt` u dnevnoj arhivi ne spominje licencu.

Zato tekst "licenca CC BY-NC-SA 4.0" za podatke Mealmetera ne bi bio točan i nisam ga upisao. Upisano je:

> Podaci: cijene.dev (DobarKod), prema uvjetima korištenja (https://cijene.dev/uvjeti-koristenja). /
> Data: cijene.dev (DobarKod), under its terms of use (https://cijene.dev/uvjeti-koristenja).

Ako ipak želiš navesti CC BY-NC-SA 4.0 (npr. kao strožu pretpostavku), to je jedna konstanta (`server.DATA_NOTE`) i
dva retka na početnoj stranici (`server.HOME_HTML`). Najsigurnije je pitati DobarKod (info@dobarkod.hr).

**Gdje:**
- odgovor svakog alata: `note` (= `PRICE_NOTE`) sada završava s `DATA_NOTE` (find_products, get_prices, plan_basket);
- početna stranica `/`: redak "Podaci: … Kod: licenca MIT." i "Data: … Code: MIT license.", s poveznicom na uvjete.

**Posljedica:** `note` je dulji za ~190 B. `prices_ean_osijek` i `prices_class_jaja_m` su već bili na granici od
20 KB (`truncated: true`), pa sada imaju jednu trgovinu manje u popisu. Zlatni izlazi su ponovno zapisani; osim `note`
razlika je samo ta jedna trgovina u ta dva scenarija.

**Provjera:** `tests/test_step6.py::test_data_attribution_in_tools_and_home`; pytest izlazni kod 0 (994 prolazi,
2 preskočena); uz `MM_GOLDEN=1` na sažetoj bazi izlazni kod 0.

## 4. README.md

Prepisan, hrvatski pa engleski u istoj datoteci: što je Mealmeter, dodavanje u Claude
(`https://mealmeter.vercel.app/mcp`), primjer pitanja i odgovora, izvor podataka i licence, ograničenja, privatnost,
lokalno pokretanje i osvježavanje (GitHub Actions → Vercel).

- Primjer je stvarni izlaz `plan_basket` iz točke 0 (Osijek, 500 g kuhanog graha, suhi; cjenik od 20.10.2026.).
  Odgovor je napisan kao primjer onoga što asistent kaže; brojke su iz alata.
- Licenca podataka je napisana kao u točki 3 (uvjeti korištenja cijene.dev), ne CC BY-NC-SA 4.0.
- Ograničenja: "točnost nije izmjerena" je točno: `data/eval/shelf_check.csv` (provjera na polici) još nema
  popunjenih cijena s police.
- Privatnost prema kodu: `server._as_result` zapisuje samo alat, status i trajanje, a HTTP zapis ima `anon_ip`
  (IPv4 /24, IPv6 /48).
- Izbačeni su detalji za razvoj (ograničenja broja upita, `MM_ALLOWED_HOSTS`, tunel, ChatGPT); ostaju u kodu i
  `docs/DEPLOY.md`.

**Provjera:** pytest izlazni kod 0.
