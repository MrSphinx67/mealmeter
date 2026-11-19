# Korak 18: manje Active CPU-a na Vercelu

(Ispravak ažuriranja od 18.11.2026., također označen kao Korak 18, opisan je u `docs/17_STATUS.md`.)

Vercelovi logovi: Claude šalje nalete jeftinih `POST /mcp` (initialize, tools/list, notifications), često na hladnoj
instanci ("StreamableHTTP session manager started"), a stvarnih poziva alata je malo. Hobby ima 4 h Active CPU-a
mjesečno, a trošili smo 15–50 min dnevno.

## Mjerenje

`scripts/cpu_profile.py`: svaki scenarij u novom procesu (hladni start), `taskset -c 0` (1 vCPU),
`MM_DUCKDB_MEMORY=300MB`, `MM_DB=data/compact.duckdb` (cjenik 17.11.2026.), aplikacija `app` iz `api/index.py`
izravno kroz ASGI. CPU = `time.process_time()` procesa (sve dretve, i DuckDB-ove), medijan od 5 pokretanja.
"Prije" = kod iz 06a2fc0 s dotad zadanim `MM_DUCKDB_THREADS=2`; "poslije" = ovaj korak (`MM_DUCKDB_THREADS=1` u
`api/index.py`). Lokalni CPU je brži od Vercelovog, pa su apsolutni brojevi manji od stvarnih; omjeri vrijede.

plan_basket (1.) = bolonjez, Zagreb (prvi alat na instanci), (2.) = palačinke, Osijek; get_prices EAN, Osijek;
find_products brašno, Osijek. "topli" = isti zahtjev na već pokrenutoj instanci.

| scenarij | korak | prije: CPU ms | prije: stvarno ms | poslije: CPU ms | poslije: stvarno ms |
|---|---|---:|---:|---:|---:|
| claude | import (api/index.py) | 999 | 1011 | **2** | 2 |
| claude | initialize | 14 | 14 | **1** | 1 |
| claude | notifications/initialized | 1 | 1 | **0** | 0 |
| claude | tools/list | 2 | 2 | **0** | 0 |
| claude | plan_basket (1.) | 3845 | 3872 | **3663** | 3692 |
| claude | plan_basket (2.) | 1411 | 1417 | **1157** | 1163 |
| claude | get_prices | 1150 | 1155 | **1143** | 1149 |
| claude | find_products | 377 | 378 | **324** | 332 |
| claude | initialize (topli) | 2 | 2 | **1** | 1 |
| claude | tools/list (topli) | 3 | 3 | **1** | 1 |
| cheap | import (api/index.py) | 1018 | 1023 | **2** | 2 |
| cheap | initialize | 14 | 14 | **1** | 1 |
| cheap | notifications/initialized | 1 | 1 | **0** | 0 |
| cheap | tools/list | 2 | 2 | **0** | 0 |
| cheap | GET /mcp (405) | 0 | 0 | **0** | 0 |
| cheap | GET /.well-known (404) | 0 | 0 | **0** | 0 |
| web | import (api/index.py) | 1012 | 1014 | **2** | 2 |
| web | GET / | 443 | 447 | **26** | 26 |
| web | GET /healthz | 3 | 3 | **0** | 0 |
| open | import mealmeter.server | 937 | 948 | **1036** | 1042 |
| open | otvaranje baze + datum | 412 | 418 | **31** | 31 |

`python -X importtime` za `api/index.py`: **prije ~1330 ms** vlastitog vremena importa, od toga MCP SDK ~1070 ms
kumulativno (`mcp_types` ~620 ms: pydantic modeli svih verzija protokola, `mcp.client` ~300 ms koji `mcp.server`
uvozi), pydantic ~95 ms, duckdb ~85 ms, mealmeter ~30 ms, yaml ~17 ms. **Poslije ~58 ms**, 104 modula, sve
standardna biblioteka i `mealmeter.web` (logging, json, re, pathlib); duckdb, mcp, pydantic i starlette se ne uvoze.

Prvi plan_basket prije (profil, cProfile): ~1,05 s čitanje yaml-ova čistim Pythonom (`yaml.safe_load`, staples.yaml
92 KB, category_map.yaml 68 KB...), ~0,6 s kompajliranje ~550 regexa u `load_staples` (samo provjera da se daju
kompajlirati), ~0,4 s otvaranje baze, od čega ~0,35 s `max(date)` nad view-om `clean.prices` (datum cjenika).

## Izmjene

1. **Lagani ulaz bez SDK-a** (`src/mealmeter/web.py`, `api/index.py` -> `web.VercelApp`). Omotači (RequestLog,
   HostGuard, RateLimit, McpPostOnly), `/healthz` i `/` premješteni su iz `server.py` u `web.py` (server ih i dalje
   izvozi pod istim imenima). `web.Light` odgovara bez MCP SDK-a, duckdb-a i baze na:
   - `initialize`, `tools/list`, `ping`, `notifications/*`: iz snimke SDK-ovih odgovora
     (`src/mealmeter/mcp_static.json`, `python -m mealmeter.server --write-static`); `protocolVersion` je tražena
     verzija iz handshakea (2024-11-05 ... 2025-11-25), inače 2025-11-25, kao SDK. Samo zahtjevi koje bi SDK
     (stateless, JSON odgovori) prihvatio: Accept i Content-Type kao u SDK-u, bez `Mcp-Session-Id`,
     `MCP-Protocol-Version` odsutan ili iz handshakea, jedan JSON-RPC objekt bez dodatnih polja; sve ostalo
     (tools/call, batch, 2026-07-28, cursor, nevaljani oblik) ide SDK-u, koji vraća i odgovarajuću grešku;
   - `GET /`, `GET /healthz`: datum cjenika i starost iz `data/compact_meta.json`;
   - nepoznate putanje (i `/.well-known/oauth-*`): isti JSON 404 kao Starlette aplikacija SDK-a;
   - `GET/HEAD/DELETE /mcp`: 405 kao prije (McpPostOnly).
   SDK aplikacija (`server.sdk_app`, s `LifespanOnDemand` oko nje) učitava se pri prvom zahtjevu koji je treba
   (zapis `sdk loaded ms=... cpu_ms=...`); ASGI lifespan platforme je ne učitava.
2. **Upute i opisi alata** ne ovise o bazi (bili su statični i prije); snimka se mijenja samo s njima. Test
   `test_static_snapshot_is_current` uspoređuje snimku sa SDK-om, a `test_fast_reply_matches_sdk_byte_for_byte` 31
   oblik zahtjeva: gdje brzi put odgovara, status, zaglavlja i tijelo su bajt po bajt kao iz SDK-a. Nakon promjene
   `INSTRUCTIONS`/`DESCRIPTIONS`/potpisa alata ili nadogradnje `mcp`: `uv run python -m mealmeter.server --write-static`.
3. **Metapodaci sažete baze** (`build_compact.compact_meta`, `data/compact_meta.json`, u `vercel.json`
   includeFiles): `build_id`, `date`, `date_hr` (isti izraz kao `server._price_list_date`), `updated`, `loaded_at`
   (kao `/healthz`). Zapisuju se nakon obje datoteke baze. `/healthz`, `/`, `convert_units` i `list_staples` ih
   koriste bez otvaranja baze. Pri prvom otvaranju baze (`server._con`) ostaje provjera oznake izgradnje između dvije
   datoteke (`CompactMismatch`, Korak 12), a uz nju se oznaka uspoređuje i s metapodacima: ista izgradnja -> datum
   cjenika iz metapodataka (bez `max(date)`, otvaranje 412 -> 31 ms); druga -> upozorenje `compact_meta: ...`,
   metapodaci se odbacuju i datum se čita iz baze. Puna baza i fixture nemaju metapodatke (sve kao prije).
4. **yaml s libyaml** (`normalize.load_yaml`, `yaml.CSafeLoader` kad postoji): isti rezultat kao `yaml.safe_load` za
   sve yaml-ove (test), ~1,05 s -> ~0,12 s pri prvom učitavanju.
5. **Provjera regexa namirnica** premještena iz `load_staples` u `staples.check_regexes`, koju poziva pytest (prije
   deploya u workflowu); pri hladnom startu se više ne kompajlira ~550 regexa (~0,6 s). Ostale skupe stvari po
   zahtjevu nisam našao: yaml-ovi, namirnice, marke i regexi su već bili u `lru_cache` (jednom po procesu).
6. **`MM_DUCKDB_THREADS=1` na Vercelu** (`api/index.py`; lokalno zadano ostaje 2). Na jednoj jezgri je s jednom
   dretvom i manje CPU-a i kraće stvarno vrijeme (CPU / stvarno ms):

| korak | prije, 2 dretve | prije, 1 dretva | poslije, 2 dretve | poslije, 1 dretva |
|---|---:|---:|---:|---:|
| plan_basket (1.) | 3845 / 3872 | 3137 / 3161 | 4293 / 4323 | 3663 / 3692 |
| plan_basket (2.) | 1411 / 1417 | 1088 / 1089 | 1452 / 1459 | 1157 / 1163 |
| get_prices | 1150 / 1155 | 1024 / 1028 | 1245 / 1261 | 1143 / 1149 |
| find_products | 377 / 378 | 311 / 314 | 397 / 398 | 324 / 332 |
| otvaranje baze + datum | 412 / 418 | 391 / 394 | 34 / 34 | 31 / 31 |

7. **Logovi**: svaki HTTP redak ima `cpu_ms` (CPU procesa za trajanja zahtjeva), prvi zahtjev instance `cold=1
   boot_cpu_ms=...` (CPU prije prvog zahtjeva: interpreter i import); `tool=...` retci imaju `cpu_ms`. Logging
   (INFO, samo poruka, stderr) postavlja `api/index.py` kao što ga je prije postavljao SDK (`configure_logging`), jer
   se SDK sada ne uvozi za jeftine zahtjeve. Primjer:
   ```
   http POST /mcp status=200 ms=1 cpu_ms=1 ip=203.0.113.x cold=1 boot_cpu_ms=148
   sdk loaded ms=1060 cpu_ms=1055
   tool=plan_basket status=ok ms=2508 cpu_ms=2491 calls=1
   http POST /mcp status=200 ms=3573 cpu_ms=3550 ip=203.0.113.x
   ```

Rezultati alata se ne mijenjaju: zlatni izlazi (28 scenarija, `golden.run`) prije i poslije su jednaki bajt po bajt
na sažetoj i na punoj bazi, a sažeta == puna.

## Procjena dnevne potrošnje

Uzorak: 1.000 jeftinih zahtjeva (topli initialize / tools/list / notifications, prosjek), 100 hladnih startova
(import + prvi initialize) i 100 poziva plan_basket, od kojih je pola prvi alat na instanci (prije: otvaranje baze,
yaml, regexi; poslije: učitavanje SDK-a + otvaranje baze), a pola na toploj instanci. Lokalni CPU:

| | prije | poslije |
|---|---:|---:|
| 1.000 jeftinih zahtjeva | 2,0 s | 0,7 s |
| 100 hladnih startova | 103,2 s | 0,3 s |
| 100 × plan_basket (50 prvih, 50 toplih) | 262,8 s | 241,0 s |
| **ukupno** | **368 s (6,1 min)** | **242 s (4,0 min), −34 %** |

Ovisno o udjelu prvih poziva: svi topli 246 -> 117 s (−53 %), svi prvi 490 -> 367 s (−25 %). Hladni start bez
alata pao je s ~1 s na ~3 ms, pa ušteda raste s brojem hladnih startova: svakih 100 dodatnih je prije bilo ~103 s, sada
~0,3 s. Stvarna potrošnja (15–50 min dnevno) veća je od modela (sporiji vCPU, više hladnih startova); novi `cpu_ms` i
`cold=1` u logovima pokazat će stvarnu raspodjelu.

Najveći preostali trošak hladnog starta s alatom je učitavanje MCP SDK-a za `tools/call` (~1,05 s, u retku
`sdk loaded`); u modelu 50 × 1,05 s = ~52 s dnevno. Izbjeći ga znači poslužiti i tools/call bez SDK-a (vlastita
provjera argumenata prema JSON shemi alata), što ovaj korak nije radio. Drugi kandidat je get_prices po EAN-u (~1,1 s
na toploj instanci).

## Provjera

- `uv run pytest -q`: 1516 passed, 7 skipped (novo: `tests/test_step18_cpu.py`, 15 testova: snimka == SDK, brzi put
  bajt po bajt kao SDK za 31 oblik zahtjeva, iste putanje i statusi kao lokalni HTTP bez učitavanja SDK-a, lifespan
  bez SDK-a, tools/call kroz VercelApp, novi proces bez duckdb/mcp/pydantic/starlette/mealmeter.server uz cpu_ms i
  cold=1, metapodaci iz builda, /healthz, / i list_staples/convert_units bez otvaranja baze, metapodaci druge
  izgradnje odbačeni, CompactMismatch i dalje pri prvom otvaranju, libyaml == safe_load, check_regexes, cpu_ms u
  zapisu alata, vercel.json i MM_DUCKDB_THREADS)
- `MM_GOLDEN=1 uv run pytest -q`: 1523 passed
- zlatni izlazi: prije == poslije (sažeta i puna baza), sažeta == puna, 28/28
- `data/compact.duckdb` ponovno izgrađen istim `build_compact.py` (s metapodacima, cjenik 17.11.2026.)
- ručni deploy nije rađen; sljedeće zakazano pokretanje workflowa ide s ovim promjenama (build_compact u workflowu
  zapisuje i `compact_meta.json`)
