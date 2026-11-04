# Korak 14: pad workflowa update 4.11.2026. (izlazni kod 1)

## Uzrok

Oba pokretanja 4.11. (41907137664 schedule, 41908255062 workflow_dispatch) pala su u koraku
**Zlatni izlazi (puna == sažeta baza)**: `golden.py --check` na sažetoj bazi dao je 26/27, razlika samo u
`basket_palacinke_nutella_osijek`, `items[6].alternatives[0]` (alternativa tražene marke Nutella iz druge
trgovine, `other_store`). Nije exit 2/4 iz update.py ni bundlea; Lorenco je samo upozorenje; testovi i deploy nisu
ni pokrenuti.

- 41907137664: puna ntl NAMAZ NUTELLA 400g (3,74 €) -> sažeta kaufland Nutella 600 g (3,74 €, utrošak 2,50 €)
- 41908255062: puna konzum NAMAZ NUTELLA 400g STAKLO -> sažeta ntl NAMAZ NUTELLA 400g FERRERO (obje 3,74 €)

`_brand_substitutions` (basket.py) birao je `min(offers, key=cost_pack)` nad skupom `branded` (ključevi
`(chain, store_id)`). Kod jednake cijene pakiranja `min` vraća prvi, a redoslijed skupa stringova ovisi o
`PYTHONHASHSEED`, koji je drukčiji u svakom procesu. `--write` i `--check` su dva procesa, pa su se razišli čim su
u gradu dva lanca imala Nutellu po istoj cijeni (4.11. tri lanca po 3,74 €). Cjenik 28.10. nije imao izjednačenje,
pa lokalno 27/27 i uz pet različitih seedova.

Nije uzrok test koji ovisi o dnevnim podacima: koraci workflowa ne traže imenovane lance. Testovi s imenovanim
lancima (test_step5p/6/7/9/10, npr. grah suho) traže `MM_GOLDEN=1` i u workflowu se preskaču (7 skipped);
testovi koji se izvode u workflowu (test_step8, test_update, test_step12, test_step5v) grade sintetičke baze u
`tmp_path`. Zlatni korak u workflowu uspoređuje punu i sažetu bazu istog dana (`--write` pa `--check`), pa ne
ovisi o tome koji je lanac objavio cjenik.

## Popravak

- `_brand_substitutions`: deterministički ključ `(cost_pack, cost_used, (chain, store_id), product_id)`. Kod
  jednake cijene pakiranja ide manji utrošak (veće pakiranje, kaufland 600 g), zatim lanac i trgovina. Ponude se
  uzimaju samo iz trgovina koje imaju stavku.
- `tests/test_step14.py`: sve permutacije redoslijeda `branded` daju istu alternativu; sa starim kodom oba testa
  padaju.
- Vercel CLI fiksiran na `vercel@65.11.0` (zadnji uspješni deploy 4.11. 01:40), umjesto `@latest`.

## Provjera (cjenik 28.10.)

- `uv run pytest -q`: 1408 passed, 7 skipped, izlazni kod 0
- `golden.py --write` (puna, PYTHONHASHSEED=11), pa `--check` na sažetoj s PYTHONHASHSEED=1 i 2: 27/27, 27/27;
  zlatni JSON-ovi nepromijenjeni
- `MM_GOLDEN=1 uv run pytest -q`: 1415 passed, izlazni kod 0
- ručni deploy nije rađen; sljedeće zakazano pokretanje workflowa ide s popravkom
