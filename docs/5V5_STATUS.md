# Korak 5V5: nalazi stvarnog testa na mealmeter.vercel.app

Test: palačinke za 4 osobe, Osijek, already_have sol, ulje i šećer, uz Nutellu. Lokalno ponovljeno na sažetoj bazi.

| točka | stanje |
|---|---|
| 1 Lorenco u usporedbi trgovina | gotovo: popravljeno, test i zlatni scenarij |
| 2 dva lanca iste cijene "spojena" | gotovo: izlaz je bio ispravan; uputa poslužitelja |
| 3 Kaufland Osijek: mlijeko 2,8 % i Nutella | gotovo: stvarni cjenik |
| 5V6 uz jednaku cijenu veće pakiranje | gotovo |

Ništa nije deployano.

## 1. Lorenco u usporedbi (7,88 €)

**Uzrok:** filtar se nije izgubio između pune i sažete baze (obje imaju `clean.chains.data_quality = 'suspect'` za
Lorenco). Od Koraka 5B plan_basket je `data_quality` gledao samo pri izboru `best_store`, a popis trgovina
(`stores`), usporedba lanaca (`comparison`, `more_chains`, `incomplete`) i alternativa marke iz druge trgovine gradili
su se od svih trgovina, pa i od Lorencova nacionalnog cjenika bez lokacije. Lokalno ponovljeno: Lorenco je bio prvi
redak usporedbe (7,88 €), ispred Kauflanda (7,98 €).

**Popravak:** lanci s `data_quality = 'suspect'` izbacuju se već pri dohvaćanju kandidata (`basket._prepare`,
`_free_rows`), pa ne postaju trgovine ni alternative. Ako korisnik izričito traži Lorenca (`store`), dobiva
upozorenje "nepouzdane podatke" i nema košarice. Metro (veleprodaja, `store_type = 'cash_and_carry'`) je i prije
bio izvan košarice (SQL kandidata, `include_wholesale = False`) i nije se pojavljivao.

**Provjera:**
- `tests/test_step5v5.py::test_suspect_and_wholesale_never_in_basket`: Lorenco (nacionalno) i Metro u Osijeku su
  najjeftiniji, ali nisu nigdje u izlazu (best_store, stores, comparison, more_chains, incomplete, alternative), uz
  already_have i alternative. Izričito traženi Lorenco daje upozorenje.
- Zlatni scenariji: dodan `basket_palacinke_nutella_osijek` (21 scenarij). Test zlatnih izlaza (`MM_GOLDEN=1`) sada
  provjerava i da nijedan izlaz plan_basketa ne sadrži `"lorenco"` ni `"metro"`. Na punoj bazi razlikovalo se 7
  scenarija plan_basketa, sve zbog Lorenca: 3 su ga imala u usporedbi, a 4 u `more_chains`. Zlatni izlazi su
  ponovno zapisani iz pune baze, a sažeta baza daje **21/21 jednako**.
- Stvarni scenarij nakon popravka: najbolja je Kaufland (7,98 €), Lidl ima isti iznos u svom retku; Lorenca nema.
- pytest: 976 prolazi.

## 2. Dva lanca iste cijene

Izlaz plan_basketa već ima **zaseban redak po lancu** s vlastitim adresama. Stvarni scenarij, lokalno:
`{"chain": "kaufland", "addresses": ["Josipa Reihl-Kira 40"], "total_to_buy": 7.98, ...}` i
`{"chain": "lidl", "addresses": ["Svetog Leopolda Bogdana Mandića 33 A", "Ulica J. J. Strossmayera 350"],
"total_to_buy": 7.98, ...}`. `merge_same_chain` spaja samo trgovine istog lanca (lanac je dio ključa). Redak
"Kaufland i Lidl (Sv. L. B. Mandića 33A, Strossmayerova 350)" je napisao AI kad je sažimao dva retka istog iznosa.

**Popravak:** pravilo 8 uputa poslužitelja (hr i en): svaki lanac u svoj redak sa svojim adresama, i kad je iznos
isti; nikad ne spajati lance ni miješati adrese. Testovi: `test_descriptions_bilingual` traži to pravilo, a
`tests/test_step5v5.py::test_comparison_rows_per_chain_with_own_addresses` provjerava da dva lanca istog iznosa
imaju dva retka i da su adrese svakog retka iz trgovina tog lanca.

## 3. Kaufland Osijek: mlijeko 2,8 % 1 l i Nutella (stvarni cjenik)

Kaufland ima u Osijeku dvije trgovine: 3130 (Josipa Reihl-Kira 40) i 6430 (Svilajska Ulica 37). Obje imaju iste cijene.

Izvorni retci, `data/raw/2026-10-20/kaufland/` (isto u arhivi od 19.10., osim zapisa količine "0,600" → "0.600"):

```
products.csv  product_id,barcode,name,brand,category,unit,quantity
              20956196,3877000214129,"Milkland Mlijeko 2,8%mm UHT 1L TETRA_OC",Milkland,HRANA,KOM,1
              03300056,80135876,Nutella 400g,Nutella,HRANA,KOM,0.400
              00147377,8000500179864,Nutella Namaz od lješnjaka 600 g,Nutella,HRANA,KOM,0.600
prices.csv    store_id,product_id,price,unit_price,best_price_30,anchor_price,special_price
              3130,20956196,0.39,0.39,,0.39,
              3130,03300056,4.99,12.48,,4.39,
              3130,00147377,4.99,8.32,,5.19,
              (6430: isti retci)
```

U bazi (`clean.prices`): datum 20.10.2026., `stale_days` 0, `price_eff` = price (nema akcijske cijene).

| proizvod | Kaufland Osijek | Kaufland u svim trgovinama (20.10.) | isti EAN u drugim lancima |
|---|---|---|---|
| Milkland mlijeko 2,8 % 1 l | 0,39 € | 0,39 € u 42 trgovine | Konzum 0,39 € |
| Nutella 400 g | 4,99 € (sidrena cijena 4,39) | 4,99 € u 53 trgovine | najčešće 4,99 € (NTL od 4,39, Branka 5,49) |
| Nutella 600 g | 4,99 € (sidrena cijena 5,19) | 4,99 € u 22 trgovine | 5,19-8,79 € (Studenac 5,19, Konzum 5,49, Plodine 6,89, Spar 6,99) |

**Zaključak:** sve tri cijene su stvarne cijene iz Kauflandova službenog cjenika, isti dan u svim navedenim
trgovinama. Nutella 600 g po 4,99 € neobično je jeftina (jednako kao 400 g), ali nije greška učitavanja: tako piše u
cjeniku, bez akcijske cijene. Napomena: za 300 g plan_basket uz jednaku cijenu bira manje pakiranje (400 g). Za
korisnika je 600 g za isti novac bolja kupnja; to sada nije označeno.

## 5V6. Uz jednaku cijenu bira se veće pakiranje

**Pravilo (`basket.choose_product`):** od pakiranja koja pokrivaju potrebnu količinu bira se najjeftinije (cijena
pakiranja). Uz jednaku cijenu bira se ono s **većom** količinom, a uz jednaku cijenu i količinu ostaje redoslijed
redaka (product_id). Prije je uz jednaku cijenu birano manje pakiranje. Slučaj "veće pakiranje unutar +10 %
cijene, a jeftinije po jedinici" nije diran.

**Test:** `tests/test_step5v5.py::test_equal_price_prefers_larger_pack`. Nutella 400 g i 600 g, obje 4,99 €, za
300 g: bira se 600 g. Ista cijena i ista količina: redoslijed product_id. Jeftinije pakiranje i dalje pobjeđuje.
Kad ništa ne pokriva količinu, vrijedi najjeftinije po jedinici, kao i prije. Stari test
`test_cheapest_covering_pack_absolute` je tvrdio "ista cijena: manje" i promijenjen je u "veće".

**Zlatni izlazi:** na punoj bazi razlikovalo se 5 od 21 scenarija; skripta je svaku promjenu usporedila sa starim
izlazom. Svaka promijenjena stavka ima istu cijenu pakiranja i veću količinu, a nijedan `total_to_buy` (trgovine i
usporedba) se nije promijenio:

| scenarij | promjena |
|---|---|
| basket_palacinke_nutella_osijek | Kaufland: Nutella 400 g → Nutella 600 g (4,99 €); utrošak 3,74 → 2,50 €. Nutella više nema jeftinijih alternativa, pa je detaljan odgovor manji i u skraćeni popis `stores` stane i Lidl (isti iznos 7,98 €). |
| basket_varivo_slavonski_brod | Lidl (najbolja): Krumpir 800 g → Krumpir 1 kg (0,89 €); utrošak 0,45 → 0,36 €, alternative i `size_note` preračunati prema 1 kg |
| basket_lidl_varivo_zagreb | isto (Krumpir 800 g → 1 kg, 0,89 €); odgovor više nije skraćen (`truncated` nestao) |
| basket_bolonjez_zagreb, basket_already_have_zagreb | u dva lanca iz usporedbe utrošak (total_used) je niži (6,77 → 6,21 €, 6,38 → 5,96 €); `total_to_buy` je isti, jer je izabrano veće pakiranje iste cijene |

Zlatni izlazi su ponovno zapisani iz pune baze. Promijenilo se točno ovih 5 datoteka, a sažeta baza daje
**21/21 jednako**. pytest: 977 prolazi.
