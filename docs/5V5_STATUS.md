# Korak 5V5: nalazi stvarnog testa na mealmeter.vercel.app

Test: palačinke za 4 osobe, Osijek, already_have sol, ulje i šećer, uz Nutellu. Lokalno ponovljeno na sažetoj bazi.

| točka | stanje |
|---|---|
| 1 Lorenco u usporedbi trgovina | gotovo: popravljeno, test i zlatni scenarij |
| 2 dva lanca iste cijene "spojena" | gotovo: izlaz je bio ispravan; uputa poslužitelja |
| 3 Kaufland Osijek: mlijeko 2,8 % i Nutella | - |

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
