# Korak 22: datoteke lanca nedostaju (trgovina-krk, arhiva 24.11.2026.)

## Polazište

Workflow je pao na arhivi od 24.11.2026.: `IO Error: No files found that match the pattern
data/raw/2026-11-24/trgovina-krk/prices.csv` (u provjeri praznog `store_id`, Korak 20). U arhivi (179.321.503 B,
25 lanaca) mapa `trgovina-krk/` ima **samo `stores.csv`** (1098 B, 14 trgovina, bajt za bajt isti kao 21.11.);
`products.csv` i `prices.csv` nema. Svi ostali lanci imaju sve tri datoteke.

## Popravak (općenito pravilo)

- `build.CHAIN_FILES`: potrebne datoteke lanca i stupci koje učitavanje i izgradnja čitaju.
- `build.chain_file_problems`: prije bilo kakvog čitanja lanca provjerava svaku datoteku: nedostaje, prazna (0 B ili
  samo zaglavlje), nečitljiva (DuckDB greška pri sniffanju ili nedostaju stupci). Jeftino: zaglavlje i prvi redak.
- `build.load_raw`: lanac s problemom se ne učitava i dodaje se u `broken_chains` ({chain, problems}). Ostatak lanca
  (provjera praznog `store_id`, neparsabilne cijene, učitavanje) radi se u jednoj transakciji (`_load_chain`): CSV
  greška tek dalje u datoteci (`build.CSV_ERRORS`: IO, InvalidInput, Conversion, Binder, Parser) poništava lanac i
  zapisuje ga kao nečitljiv. OutOfMemory i prekid nisu u `CSV_ERRORS` i i dalje ruše izgradnju; `BadPriceError` i
  dalje blokira bazu.
- `stores` i `products` se učitavaju po nazivu stupca (CHAIN_FILES), ne `SELECT *`: dodatni ili drukčije poredani
  stupci ne pomiču vrijednosti (shema sirovih tablica ista kao prije).
- Izostavljeni lanac nema redaka u novoj arhivi, pa ga `chain_report` javlja kao "nema u arhivi" i cijeli ide kroz
  carry-forward (najviše `CARRY_DAYS`). Ako se ne učita nijedan lanac, `ValueError` kao i prije.
- `update.py`: `  ! …`, `::warning title=Datoteke lanca <lanac>::…` i redak u `GITHUB_STEP_SUMMARY`
  (`build.describe_broken_chain`), exit 0. Memorija polja (`remember_fields`, seed) preskače praznu ili nečitljivu
  `products.csv` uz log; `extract` prepoznaje mapu lanca po bilo kojoj od tri datoteke, ne samo po `prices.csv`.

## Provjera (bez lokalne pune izgradnje)

- `tests/test_step22.py` (19 testova + 1 preskočen bez lokalne arhive). Fixture
  `tests/fixtures/krk_2026-11-24/trgovina-krk/stores.csv` je stvarna datoteka iz arhive. Pokriva: stvarni 24.11.
  (nedostaju products i prices), nedostaje prices/stores/products, prazna datoteka (0 B i samo zaglavlje), nedostaje
  stupac, binarno smeće, CSV greška u zadnjem od 60.001 retka (rollback, lanac prvi po redu), svi lanci neispravni,
  dodatni/preslagani stupci, seed s praznom `products.csv`, `extract` s jednim lancem bez `prices.csv`; update.py kroz
  dva dana (stvarni 24.11., bez stores.csv, prazna prices.csv): exit 0, upozorenja, sažetak, cijene lanca od 23.11.
  prenesene i u `clean.prices`.
- Stvarna arhiva 24.11. preuzeta, raspakirana **samo `trgovina-krk/`**: `chain_file_problems` →
  `["nedostaje products.csv", "nedostaje prices.csv"]`.
- pytest: 1559 passed, 8 skipped.
