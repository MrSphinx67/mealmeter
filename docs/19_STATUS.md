# Korak 19: bez učitavanja SDK-a za prompts/resources i notifikacije, zahtjevi koji vise

## Polazište (produkcijski logovi 20.11. 18:39 – 21.11. 18:39 UTC)

Analiza `vercel logs` (runtime + requests, 719 + 449 zapisa, tri produkcijska deploya, svi s kodom Koraka 18):

| | broj | CPU |
|---|---:|---:|
| POST /mcp brzi put | 257 | 0,3 s |
| POST /mcp preko SDK-a, nije alat (hladna instanca) | 52 | 105,9 s |
| "Task timed out after 60 seconds", SDK učitan | 74 | 147,6 s (samo učitavanje SDK-a) |
| "Task timed out after 60 seconds", bez SDK-a | 49 | – |
| tools/call (plan_basket 5, list_stores 3, list_staples 1) | 9 | 21,1 s |
| hladni startovi (`cold=1`) | 56 (+74 vjerojatnih bez zapisa) | 20,4 s (+~26 s) |

Ukupno ~321 s CPU-a, od toga **79 % učitavanje MCP SDK-a** (127×, medijan 2,03 s), a samo 1 od 127 učitavanja bio je
tools/call. Prethodnih ~25 h isto (574 s, SDK 84,5 %). Zahtjevi koji vise postoje od 14.11. (i prije Koraka 18), a u
logovima gotovo nema odgovora 202. Redak zahtjeva nije imao JSON-RPC metodu, pa se uzrok nije mogao potvrditi.

## Uzroci

1. **prompts/list, resources/list, resources/templates/list učitavaju SDK.** initialize je najavljivao `prompts` i
   `resources` (MCPServer ih najavljuje jer ima rukovatelje), klijenti ih nakon spajanja traže, a brzi put je
   odgovarao samo na initialize, tools/list, ping i notifikacije. Potvrđeno lokalno i na previewu starog koda:
   `prompts/list` 2,9 s (`sdk loaded ms=2308 cpu_ms=2198`), a ostali zahtjevi ~1 ms.
2. **Zahtjevi koji vise do 60 s.** Na previewu starog koda (vercel-runtime 0.24.1, python3.12, kao produkcija) se
   **nisu ponovili** ni u jednom od ovih oblika: Claudeov niz (initialize, notifications/initialized, tools/list,
   prompts/list, resources/list, resources/templates/list, ping, notifications/cancelled, tools/call ×2,
   notifications/progress), chunked tijelo, HTTP/2, `Expect: 100-continue`, 5 notifikacija na istoj keep-alive vezi
   (HTTP/1.1), 5 multipleksiranih na jednoj HTTP/2 vezi, nalet od 5 paralelnih zahtjeva (kao Claude Code), tijelo
   koje kasni 3 s, klijent koji prekine usred tijela, tijelo koje nikad ne završi. Svaka notifikacija vratila je 202
   za 0,08–0,45 s, a u logovima previewa nije bilo "Task timed out". Što je provjereno:
   - **naši ASGI odgovori**: `http.response.start` (202, `content-type: application/json`, `content-length: 0`), pa
     `http.response.body` s praznim tijelom; `more_body` je sad i izričito `False` (prije izostavljen, što je po
     ASGI-ju isto). SDK vraća iste bajtove (test bajt po bajt).
   - **Vercelov omotač** (`vercel_runtime/vc_init.py`, `ASGIMiddleware`, uz ugrađeni uvicorn 0.24.1 s h11): poruke
     odgovora prosljeđuje uvicornu bez posebne obrade praznih tijela, a invokacija završava ("end" preko IPC-a) tek
     kad ASGI aplikacija vrati. Lokalno, pod istim ugrađenim uvicornom (h11), 202 s praznim tijelom završi za 1 ms.
     U produkciji "Task timed out" zahtjevi nemaju redak RequestLog-a, dakle **zapela je naša aplikacija prije
     povratka, a ne platforma nakon njega**.
   - **SDK**: `stateless_http=True, json_response=True`, pa na POST nikad ne otvara SSE tok; GET/DELETE /mcp već
     dobivaju 405 (McpPostOnly). Na notifikaciju SDK odmah vraća 202.
   - **Tijelo zahtjeva**: Vercelov edge prima cijelo tijelo prije poziva funkcije. Tijelo koje nikad ne završi nije
     stiglo do funkcije, a tijelo koje je klijent prekinuo stiglo je skraćeno (`rpc=invalid-json`, 400 od SDK-a).
     Stari kod je nepotpuno tijelo (`http.disconnect`) slao SDK-u, koji bi ga učitao i čekao.

   Točan uzrok u produkciji pokazat će novi zapis: `rpc`, `id`, `path`, a za zahtjev koji visi `timeout=1 phase=...`.

## Izmjene

0. **Zapis zahtjeva** (`web.RequestLog`, `web.rpc_info`): `rpc=<JSON-RPC metoda>` (`invalid-json`, `batchN`,
   `response`), za tools/call `name=<alat>`, `id=<id>` (`-` za notifikaciju; samo `[A-Za-z0-9_./:-]`, najviše 32
   znaka) i `path=fast|sdk`. Argumenti alata se ne zapisuju. Primjer s previewa:
   ```
   http POST /mcp status=200 ms=2 cpu_ms=2 ip=31.217.2.x rpc=initialize id=0 path=fast cold=1 boot_cpu_ms=395
   http POST /mcp status=202 ms=0 cpu_ms=0 ip=31.217.2.x rpc=notifications/initialized id=- path=fast
   http POST /mcp status=200 ms=0 cpu_ms=0 ip=31.217.2.x rpc=prompts/list id=2 path=fast
   http POST /mcp status=200 ms=2313 cpu_ms=2245 ip=31.217.2.x rpc=tools/call name=list_staples id=6 path=sdk
   ```
1. **Mogućnosti**: initialize (i server/discover za 2026-07-28) najavljuju samo `tools` (`server._tools_only_capabilities`
   omata `get_capabilities` niske razine). Rukovatelji ostaju, pa SDK na prompts/list, resources/list i
   resources/templates/list i dalje vraća prazan popis. Brzi put na njih odgovara iz snimke (`mcp_static.json`,
   novi ključ `empty_lists`, `--write-static`), bajt po bajt kao SDK; s `cursor` ili protokolom 2026-07-28 ide SDK-u.
   Uz to, ono što SDK bez sesija daje jednako ide brzim putem (provjereno bajt po bajt):
   - zahtjevi sa zaglavljem `Mcp-Session-Id` (SDK ga zanemaruje);
   - svaka notifikacija, i s dodatnim poljima ili nepoznatom `notifications/*` metodom (202);
   - JSON-RPC odgovor klijenta (`id` + `result`/`error`, 202).

   Na SDK i dalje idu: notifikacija s nepodržanim `MCP-Protocol-Version` (400), bez prihvatljivog `Accept` (406),
   batch i parametri koji nisu objekt.
2. **Zahtjevi koji vise** (`web.Light`, `web.RequestLog`, `api/index.py`):
   - čitanje tijela POST /mcp najviše `MM_BODY_TIMEOUT` (zadano 10 s): 408, `phase=body_timeout`, bez SDK-a;
   - prekinuta veza prije kraja tijela (`http.disconnect`) se više ne šalje SDK-u: zapis `status=499
     phase=disconnect`, bez odgovora;
   - čuvar vremena: `MM_REQUEST_TIMEOUT=50` na Vercelu (ispod `maxDuration` 60 s, lokalno isključen). Zahtjev koji
     traje dulje prekida se (`asyncio.timeout`), klijent dobiva 504 (JSON-RPC greška `timeout`, s id-jem zahtjeva) ako
     odgovor još nije počeo, a redak ima `timeout=1 phase=<body|sdk_load|sdk|send> body=<primljeno>/<content-length>`.
     Funkcija tako vraća prije Vercelovog ubijanja: zapis postoji, a instanca ostaje topla.

Rezultati alata se ne mijenjaju (zlatni izlazi prije == poslije, vidi Provjeru).

## Preview (stari kod `db8b16e` naspram ovog koraka)

Oba deploya iz istog builda (`vercel@65.11.0 build` + `deploy --prebuilt`, python3.12, sažeta baza 20.11.2026.,
paket 202,8 / 202,3 MB), zahtjevi preko `vercel curl` (zaštita previewa), trajanje = `time_total` curla s ovog računala
(uključuje mrežu, ~0,2 s):

| zahtjev | stari: status, s | novi: status, s | novi: zapis |
|---|---|---|---|
| initialize (hladno) | 200, 0,57 | 200, 0,56 | fast, cpu 2 ms |
| notifications/initialized | 202, 0,47 | 202, 0,38 | fast |
| tools/list | 200, 0,23 | 200, 0,37 | fast |
| prompts/list | **200, 2,94 (SDK)** | 200, 0,39 | **fast**, cpu 0 ms |
| resources/list | 200, 0,23 | 200, 0,47 | fast |
| resources/templates/list | 200, 0,26 | 200, 0,22 | fast |
| ping | 200, 0,28 | 200, 0,21 | fast |
| notifications/cancelled | 202, 0,38 | 202, 0,22 | fast |
| tools/call list_staples | 200, 0,37 | 200, 2,52 | **sdk** (prvo učitavanje: `sdk loaded cpu_ms=2121`) |
| tools/call plan_basket | 200, 1,61 | 200, 1,36 | sdk, cpu 1094 ms |
| notifications/progress | 202, 0,21 | 202, 0,22 | fast |

Na novom previewu: 30 zapisa, **0 "Task timed out", jedno `sdk loaded` (prvi tools/call)**, svi ostali
`path=fast`. Na starom: 0 "Task timed out", `sdk loaded` na prompts/list. Varijante (chunked, HTTP/2, `Expect`,
keep-alive, multipleksiranje, nalet od 5) na oba: sve 202/200 za 0,2–0,45 s. Oba previewa su nakon testa obrisana.

Nije testirano: pravi Claude Code klijent spojen na preview. Za to treba tajna za zaobilaženje zaštite u MCP
zaglavlju, a njezino čitanje iz postavki projekta nije bilo dopušteno.

## Očekivani učinak

Na produkcijskom uzorku (321 s dnevno) otpada ~126 učitavanja SDK-a koja nisu tools/call, ~250 s (~78 %). SDK ostaje
za prvi tools/call na instanci (~9 dnevno, najviše ~18 s). Ako se zastoji nastave, čuvar vremena sprječava ubijanje
instance: manje hladnih startova (bili su ~47 s, 14 %), a zapis pokazuje fazu.

Preostalo: tijelo koje je klijent prekinuo stiže skraćeno, pa ga SDK odbija greškom parsiranja (400), a na hladnoj
instanci ga pritom učita. Poruke greške dolaze iz pydantic-corea, pa ih brzi put ne ponavlja bajt po bajt.

## Provjera

- `uv run pytest -q`: 1526 passed, 7 skipped (novo: `tests/test_step19.py`, 10 testova: samo `tools` u initialize i
  server/discover, 30 novih oblika bajt po bajt kao SDK, Claudeov niz kroz VercelApp bez SDK-a do tools/call uz `rpc`,
  `id`, `path` u zapisu, `rpc_info` bez argumenata, prekid veze usred tijela (499, bez SDK-a), tijelo koje ne stiže
  (408), čuvar vremena u SDK-u i u tijelu (504, `timeout=1 phase=...`) i nakon početka odgovora, `MM_REQUEST_TIMEOUT`
  ispod `maxDuration`, stvarni uvicorn (h11) bez zastoja i s prekinutom vezom; u `test_step18_cpu.py`
  resources/list i tools/list s `Mcp-Session-Id` sada očekuju brzi put).
- Zlatni izlazi, lokalna baza od 20.11.2026. (prvo punjenje iz arhive, bez carry-forwarda), 28 scenarija:
  stari kod (`db8b16e`) == novi kod na punoj bazi, bajt po bajt; sažeta == puna (`golden.py --check`, 28/28).
  Zapisani zlatni izlazi su vraćeni na commitane (workflow ih piše iz produkcijske baze).
- `MM_GOLDEN=1 uv run pytest -q` (s tim zlatnim izlazima): 1530 passed, 3 failed (`test_golden_bolonjez_osijek_10`,
  `test_golden_grah_suho_all_chains`, `test_golden_bolonjez_junece`). Isti padovi i sa starim kodom na istoj bazi:
  test očekuje Lidl, kojeg u toj lokalnoj bazi (bez carry-forwarda) za te gradove nema; nisu posljedica ovog koraka.
- Ručnog deploya na produkciju nije bilo; sljedeće zakazano pokretanje workflowa ide s ovim promjenama.

## Usput uočeno (nije dio ovog koraka)

- Arhiva cijene.dev od **21.11.2026.**: `jadranka_trgovina/stores.csv` i 34.462 retka u `prices.csv` imaju prazan
  `store_id`. `build_compact.py` zato pada na provjeri view-ova (`prices: view se razlikuje od pune baze`, 10.458
  čistih cijena bez trgovine). Zakazano pokretanje koje učita tu arhivu vjerojatno neće deployati.
- `vercel.json` traži `regions: ["fra1"]`, a produkcijski logovi su iz `iad1`.
