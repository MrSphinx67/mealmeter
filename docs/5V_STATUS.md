# Korak 5V: Vercel (sažeta baza)

| točka | stanje |
|---|---|
| 0 ograničenja Vercela (službena dokumentacija) | gotovo |
| 1 api/index.py (ASGI, lifespan, compact) | gotovo: uvicorn s --lifespan off i on: /healthz 200, plan_basket 200 (~0,85 s) |
| 2 vercel.json i veličina paketa | gotovo: procjena paketa ≈ 306 MB od 500 MB (vidi niže) |
| 3 GitHub Actions (2x dnevno) | gotovo: .github/workflows/update.yml (nije pokrenuto) |
| 4 postavke (hostovi, rate limit, IP zaglavlje) | gotovo: TRUSTED_PROXY=vercel (x-vercel-forwarded-for), zadane postavke u api/index.py |
| 5 docs/DEPLOY.md | - |

Ništa nije deployano.

## 0. Python funkcije na Hobby planu (provjereno 22.10.2026. u službenoj dokumentaciji)

| svojstvo | vrijednost | izvor |
|---|---|---|
| veličina paketa (nekomprimirano) | **500 MB** za Python (250 MB ostali runtimeovi); "Large functions" do 5 GB (beta, uz Fluid compute) | [Functions limits](https://vercel.com/docs/functions/limitations), [Python runtime](https://vercel.com/docs/functions/runtimes/python) |
| trajanje, s Fluid compute (zadano za nove projekte od 23.4.2025.) | **300 s zadano i najviše** | [Functions limits](https://vercel.com/docs/functions/limitations), [Duration](https://vercel.com/docs/functions/configuring-functions/duration), [Fluid compute](https://vercel.com/docs/fluid-compute) |
| trajanje bez Fluid compute | trenutna dokumentacija ga ne navodi; stariji changelog kaže 10 s zadano i do 60 s (možda zastarjelo, nije potvrđeno) | [Changelog: Hobby do 60 s](https://vercel.com/changelog/vercel-functions-for-hobby-can-now-run-up-to-60-seconds) |
| memorija | **2 GB / 1 vCPU** (zadano i najviše) | [Functions limits](https://vercel.com/docs/functions/limitations) |
| Python | **3.12 (zadano), 3.13, 3.14** | [Python runtime](https://vercel.com/docs/functions/runtimes/python) |
| tijelo zahtjeva/odgovora | 4,5 MB | [Functions limits](https://vercel.com/docs/functions/limitations) |
| ulazna točka | `app.py`/`index.py`/... ili `api/*.py`, varijabla `app` (ASGI ili WSGI) | [Python runtime](https://vercel.com/docs/functions/runtimes/python), [/api direktorij](https://vercel.com/docs/functions/runtimes/python/api-directory) |
| paket | Python nema tree-shakinga: ulaze sve datoteke projekta dostupne pri buildu; `excludeFiles` / `includeFiles` u `vercel.json` (`functions`) | [Python runtime](https://vercel.com/docs/functions/runtimes/python) |
| IP klijenta | `x-forwarded-for` (Vercel ga prepisuje, "do not forward external IPs", sprječava lažiranje); `x-vercel-forwarded-for` i `x-real-ip` su isti | [Request headers](https://vercel.com/docs/headers/request-headers) |

Posljedice za Mealmeter: sažeta baza (212 MB) i ovisnosti (oko 100 MB) stanu u 500 MB, a puna baza (1,1 GB) mora biti
isključena iz paketa. plan_basket (~0,9 s) je daleko ispod 300 s, a RSS (~370 MB) daleko ispod 2 GB. Dokumentacija ne
navodi šalje li Python runtime ASGI lifespan, pa ga omotač pokreće sam (5-0).

## 2. Paket (lokalna procjena; Vercel CLI nije instaliran, a `vercel build` traži povezan projekt)

`vercel.json`: funkcija `api/index.py`, `includeFiles` = `src/**`, `data/compact.duckdb`, `data/*.yaml`; `excludeFiles`
isključuje punu bazu, `data/raw`, testove, dokumente i skripte; `maxDuration` 60 s; sve putanje se prepisuju na
`/api/index`. `.vercelignore` sprječava slanje pune baze i arhiva pri `vercel deploy` bez `--prebuilt`.

| dio | MB |
|---|---|
| ovisnosti bez razvojnih (`uv export --no-dev`, cp312 manylinux; duckdb .so 58 MB) | 93 |
| data/compact.duckdb (20.10.2026.) | 213 |
| src/ i data/*.yaml | 0,4 |
| **ukupno (procjena)** | **≈ 306 od 500** |

Rezerva je ~190 MB; sažeta baza raste s brojem proizvoda i trgovina, pa CI provjerava veličinu (točka 3).

## 3. GitHub Actions (`.github/workflows/update.yml`)

U 13:30 i 21:30 UTC i ručno (workflow_dispatch, uz opciju force):
1. Prethodna puna baza vraća se iz Actions cachea, da update.py ima s čime usporediti i odakle prenositi cijene.
2. `update.py`: pad ukupnih redaka ili lanaca > 20 % → izlazni kod 2 i kraj. Pad pojedinog lanca > 20 % ili nestali
   lanac (u update.py samo upozorenje) ovdje također prekida deploy. Arhiva koja je već učitana → ništa dalje.
3. `build_compact.py`, zatim zlatni izlazi: `--write` na punoj bazi i `--check` na sažetoj. Dnevni podaci se mijenjaju,
   pa se ne uspoređuje s jučerašnjim datotekama, nego potvrđuje da sažeta baza daje iste izlaze kao puna; zatim pytest.
4. `vercel pull/build --prod` (paket > 490 MB prekida), `vercel deploy --prebuilt --prod`.
Tajne: VERCEL_TOKEN, VERCEL_ORG_ID, VERCEL_PROJECT_ID. Baze se ne commitaju (> 100 MB).

## 4. Postavke na Vercelu (zadane u `api/index.py`, mogu se promijeniti u Project Settings -> Environment Variables)

| varijabla | zadano | zašto |
|---|---|---|
| MM_ALLOWED_HOSTS | `*.vercel.app` | Host zaglavlje Vercelove domene; za vlastitu domenu dodaj je zarezom |
| MM_ALLOWED_ORIGINS | `https://claude.ai,https://*.claude.ai,https://*.vercel.app` | preglednički klijenti; Claude konektor zove s poslužitelja, bez Origina |
| TRUSTED_PROXY | `vercel` | IP iz `x-vercel-forwarded-for` (pa `x-real-ip`, `x-forwarded-for`). Vercel prepisuje `x-forwarded-for` i ne prosljeđuje vanjske IP-ove. `CF-Connecting-IP` se ne čita, jer bi ga klijent na Vercelu mogao sam poslati. |
| MM_RATE_IP / MM_RATE_SESSION / MM_RATE_GLOBAL | 60 / 30 / 600 u minuti | brojači su u memoriji jedne instance; uz više instanci (Fluid compute) ograničenje je po instanci, a za strogo ograničenje treba Vercel Firewall |
| MM_DB, MM_DUCKDB_TEMP | `data/compact.duckdb`, `/tmp` | sažeta baza samo za čitanje; jedino je /tmp zapisiv |
