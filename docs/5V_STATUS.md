# Korak 5V: Vercel (sažeta baza)

| točka | stanje |
|---|---|
| 0 ograničenja Vercela (službena dokumentacija) | gotovo |
| 1 api/index.py (ASGI, lifespan, compact) | gotovo: uvicorn s --lifespan off i on: /healthz 200, plan_basket 200 (~0,85 s) |
| 2 vercel.json i veličina paketa | - |
| 3 GitHub Actions (2x dnevno) | - |
| 4 postavke (hostovi, rate limit, IP zaglavlje) | - |
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
