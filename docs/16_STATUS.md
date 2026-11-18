# Korak 16: granica veličine paketa na Vercelu (500 MB za Python?)

## Dokumentacija

[Vercel Functions limitations](https://vercel.com/docs/functions/limitations) (zadnja izmjena 24.8.2026.) i
[Python runtime](https://vercel.com/docs/functions/runtimes/python) (12.8.2026.): "For Python functions, the maximum
uncompressed size is 500 MB" (redovno, nije beta); "Large functions" do 5 GB su beta (fluid compute,
`VERCEL_SUPPORT_LARGE_FUNCTIONS`). Hobby: 2 GB memorije, 300 s. Ograničenja po datoteci stranica ne navodi.

## Što stvarno radi `vercel build`

Najnoviji stabilni CLI je **66.0.0** (objavljen 18.11.2026., novi "native" CLI); workflow ima 65.11.0 (Korak 14).
Probni build s privremenom datotekom od 60 MB u paketu (280 MB), oba CLI-ja isto:

    Bundle size (275.86 MB) exceeds the standard size; optimizing dependencies.
    Error: [LAMBDA_SIZE_EXCEEDED] Total bundle size (280.01 MB) exceeds the maximum function size (225 MB) even after
    optimizing dependencies.

Granica od 225 MB je prag Python buildera (`LAMBDA_SIZE_THRESHOLD_BYTES = 225 * 1024 * 1024` u `@vercel/python`,
65.11.0; 66.0.0 javlja isti broj). Iznad praga builder izbacuje javne pakete s kompatibilnim wheelom i instalira ih pri
hladnom startu (uv u paketu), a ostatak (naše baze, duckdb bez manylinux 2.17 wheela) mora stati u 225 MB (Korak 5V2).
500 MB iz dokumentacije za naš paket dakle ne vrijedi. Large functions (beta) ne koristimo.

## Preview s anchor_price po trgovini

Sažeta baza uz `MM_COMPACT_ANCHOR=1` (neprehrambeni proizvodi i dalje izbačeni), bez
`VERCEL_SUPPORT_LARGE_FUNCTIONS`, build i deploy s CLI-jem 66.0.0 kao preview:

- compact.duckdb 52,5 MB, compact_prices.duckdb 72,0 MB (obje < 95 MB, podjela nije trebala)
- paket **217,4 MB** (do 225 MB: 7,6 MB, 3,4 %); deploy READY, `get_prices` vraća anchor_price po trgovini
- lokalno: golden 27/27 (mijenjaju se samo `prices_*`: anchor_price), brzina 17,9 s / RSS 575 MB (kao bez njega)

Hladni start na previewu (`curl time_total`, isti zahtjevi):

| | odmah nakon deploya | nakon 16 min mirovanja |
|---|---|---|
| prvi plan_basket (palačinke, Osijek) | 2,09 s | **6,41 s** |
| /healthz | 0,25 s | 0,24 s |
| drugi plan_basket | 1,21 s | 1,10 s |
| get_prices jaja:m (Zagreb) | 2,77 s | 2,23 s |

Preview je obrisan (`vercel remove`); produkcija nije dirana.

## Odluka

Rezerva od 3,4 % s anchor_price premala je za bazu koja raste sa cjenikom, pa:
- **Zadano bez anchor_price** (kao Korak 15): `build_compact.NO_ANCHOR_COLS`; **`MM_COMPACT_ANCHOR=1`** ga sprema po
  trgovini (view ga tada vraća). `golden.py` iz `get_prices` uklanja anchor_price osim uz `MM_COMPACT_ANCHOR=1`.
  Testovi: `test_step15.py::test_compact_default_without_anchor`, `::test_compact_anchor_option_keeps_price_per_store`.
- **CLI ostaje 65.11.0** (granica je u 66.0.0 ista).
- **Granice** (`vercel_bundle_size.py` zadano i workflow): blokada **220 MB**, upozorenje **200 MB** (prije 190);
  datoteka 95 / 65 MB. Iznad 225 MB Vercel ionako odbija build, a produkcija ostaje na zadnjoj verziji.

## Stanje (cjenik 17.11., zadano bez anchor_price)

- compact.duckdb 53,8 MB, compact_prices.duckdb 54,5 MB
- paket (`vercel build --prod`, CLI 65.11.0): **201,1 MB**: `::warning::` (iznad 200), do blokade 18,9 MB
  (između izgradnji ±1 MB: Korak 15 199,9 MB)

## Provjera

- `golden.py --write` (puna) pa `--check` (sažeta): 27/27; zlatni JSON-ovi jednaki Koraku 15
- `uv run pytest -q`: 1447 passed, 7 skipped
- `MM_GOLDEN=1 uv run pytest -q`: 1454 passed
- ručni deploy na produkciju nije rađen; sljedeće zakazano pokretanje workflowa ide s ovim promjenama
