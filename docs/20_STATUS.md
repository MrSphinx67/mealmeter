# Korak 20: prazan store_id (jadranka_trgovina, arhiva 21.11.2026.)

## Polazište

Arhiva od 21.11.2026., lanac `jadranka_trgovina`: **8 od 18 trgovina** u `stores.csv` i **34.462 od 133.151 retka
cijena (25,9 %)** nemaju šifru trgovine (`store_id` prazan, šifra je završila u stupcu `address`, a grad je "Roba").
Dan ranije (20.11.) tih je 8 trgovina (051, 508, 511, 513, 539, 540, 554, 558) imalo 34.459 redaka. Izgradnja je pala
u `build_compact` na provjeri view-ova: 10.458 čistih cijena bez trgovine.

## Popravak

- `build.load_raw`: retci cijena i trgovine s praznim `store_id` (`EMPTY_STORE_SQL`) preskaču se, a za svaki takav
  lanac dodaje se zapis u `empty_stores` ({chain, prices, total, pct, stores, stores_total, dropped}). Te trgovine
  nemaju redaka u novoj arhivi, pa ih `update.carry_forward` prenosi po trgovini od jučer, s jučerašnjom adresom.
- Kad je takvih redaka više od `MAX_EMPTY_STORE_SHARE = 0.5` redaka cijena lanca, lanac se uopće ne učitava
  (`dropped`). Tada cijeli lanac ide kroz carry-forward kao da nije objavio cjenik (`chain_report`: "nema u arhivi").
  Baza se zbog toga ne blokira. Ako se ne učita nijedan lanac, diže se `ValueError`.
- Provjera neparsabilnih cijena (Korak 18) broji samo retke koji imaju trgovinu.
- `update.py`: `  ! …` u ispisu, `::warning title=Prazan store_id <lanac>::…` i redak u `GITHUB_STEP_SUMMARY`
  (`build.describe_empty_stores`). Izlazni kod ostaje 0.

## Provjera (bez lokalne pune izgradnje)

- `tests/test_step20.py` (7 testova). Fixture `tests/fixtures/jadranka_2026-11` sadrži stvarne `stores.csv` oba dana
  i doslovne retke za 40 šifri. Pokriva: retke i trgovine preskočene na stvarnom 21.11.; prag (točno 50 % prolazi,
  više od toga izostavlja lanac, i to i kad je izostavljeni lanac prvi); slučaj bez ijednog lanca; update.py kroz dva
  dana. Tamo svih 8 trgovina dobiva sve svoje cijene od 20.11., nema čistih cijena bez trgovine, a `build_compact`
  prolazi provjeru view-ova. Kad je iznad praga, lanac se prenosi cijeli, uz exit 0.
- Stvarna arhiva 21.11., **samo jadrankini CSV-ovi** (DuckDB `memory_limit` 1 GB, 1 dretva): 34.462 od 133.151 retka,
  8 od 18 trgovina, ispod praga.
- Punu bazu gradi GitHub Actions (lokalna izgradnja je prekinuta zbog nedostatka memorije).
- `uv run pytest -q` (bez MM_GOLDEN): 1533 passed, 7 skipped. Golden testovi idu u CI-ju.
