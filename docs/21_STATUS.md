# Korak 21: MCP 2026-07-28 (server/discover, subscriptions/listen) na brzom putu

## Polazište (produkcijski logovi 22./23.11.2026., 24 h)

Claude sada govori novu verziju protokola **2026-07-28**: nema više `initialize` handshakea, svaki zahtjev nosi
`params._meta` (`io.modelcontextprotocol/protocolVersion`, `clientCapabilities`, `clientInfo`) i zaglavlja
`MCP-Protocol-Version` i `Mcp-Method`. Brzi put (Korak 18/19) znao je samo verzije handshakea, pa je **sve** iz nove
ere išlo SDK-u:

| rpc | broj | put | trošak |
|---|---|---|---|
| subscriptions/listen | 247 | sdk | svaki 50,0 s do čuvara vremena (`timeout=1 phase=sdk`), ukupno 12.350 s instance |
| server/discover | 106 | sdk | na hladnoj instanci učitava SDK (~2,1 s CPU-a; 19 učitavanja, 37 s CPU-a u danu) |
| tools/list | 68 | sdk | |
| tools/call | 1 | sdk | |

Razgovor izgleda ovako: `server/discover` (id `server-discover-probe-1`) → `tools/list` → `subscriptions/listen`
(id `listen:0`). SDK (`MCPServer`, pretplate uključene po zadanom) otvorio je SSE tok, poslao
`notifications/subscriptions/acknowledged` i držao ga otvorenog; nakon 50 s naš čuvar ga je prekinuo ("ASGI callable
returned without completing response"), a klijent ga je ponovno otvorio (`listen:1`, `:2`, … najviše `listen:12`).
12.350 s × 2 GB ≈ **6,9 GB-h provisioned memory dnevno** (gornja granica, ako se tokovi ne preklapaju na istoj
instanci; Hobby uključuje 360 GB-h mjesečno).

## Specifikacija (2026-07-28)

Pročitano: modelcontextprotocol.io/specification/2026-07-28 (changelog, basic/transports/streamable-http,
basic/patterns/subscriptions, server/discover, schema).

- `server/discover`: "Servers **MUST** implement". Rezultat: `supportedVersions`, `capabilities`, `instructions`,
  `resultType`, `ttlMs`, `cacheScope`, a podaci o poslužitelju u `_meta["io.modelcontextprotocol/serverInfo"]`.
- `subscriptions/listen` otvara dugotrajan tok obavijesti (zamjenjuje `resources/subscribe` i GET tok). Ne postoji
  posebna sposobnost `subscriptions`. Obavijesti se najavljuju postojećim zastavicama (`tools.listChanged`,
  `prompts.listChanged`, `resources.subscribe/listChanged`), a poslužitelj "**MUST NOT** send notification types the
  client has not explicitly requested".
- Spec ne propisuje izričito što odgovara poslužitelj bez obavijesti. Pravilo za nepoznatu metodu: "**MUST** respond
  with `404 Not Found` and a JSON-RPC error with code `-32601`". Definicija `MethodNotFoundError` obuhvaća i metodu
  "gated behind a server capability the server did not advertise".
- Tok koji se zatvori bez završnog rezultata je "unexpected disconnect, which the client **MAY** treat as a trigger
  to reconnect". Upravo to se događalo kad je čuvar vremena prekidao tok. Uredno zatvaranje s rezultatom je
  dopušteno, ali bi klijent koji želi obavijesti tada vjerojatno odmah otvorio novi tok, pa se ponavljanje ne bi
  zaustavilo.
- Uklonjeno u 2026-07-28: `initialize`, `ping`, `logging/setLevel`, `resources/subscribe`/`unsubscribe`.
  Novo: `server/discover`, `subscriptions/listen`.

**Odabrano:** pretplate se ne najavljuju (`tools.listChanged: false`), a `subscriptions/listen` odmah dobiva
`-32601 Method not found` uz HTTP 404, kao JSON i bez SSE toka. To je trajna greška ("nema te metode"), a ne prekid
veze, pa za nju ne vrijedi pravilo o ponovnom spajanju.

## SDK (mcp 2.3.0)

- `MCPServer(subscriptions=False)` ostavlja `subscriptions/listen` neposluženim. SDK tada sam vraća 404 -32601, a
  `server/discover` (`get_capabilities(protocol_version=2026-07-28)`) najavljuje `tools.listChanged = false`. Bez
  toga je najavljivao `listChanged: true` jer je listen bio poslužen. Promjena je u `server.create_server`.
- Oblik koji SDK provjerava: `Mcp-Method` mora biti jednak metodi u tijelu, `MCP-Protocol-Version` jednak
  `_meta.protocolVersion`, a ponovljeno zaglavlje daje HEADER_MISMATCH. Listen bez `text/event-stream` u `Accept` daje
  406. Listen bez filtra `notifications` daje -32602, jer se parametri provjeravaju prije "method not found".
  Notifikacija dobiva 202 bez `content-type`.
- U ovoj eri SDK piše JSON s `json.dumps` (`\u` escape), a ne kao pydantic u eri handshakea. Brzi put piše jednako.

## Promjene

- `server.static_snapshot` / `--write-static`: snimka `modern[<verzija>]` sadrži `results` za `server/discover`,
  `tools/list`, `prompts/list`, `resources/list` i `resources/templates/list`, te `errors` (status, error) za
  `subscriptions/listen`, `ping`, `initialize`, `logging/setLevel`, `resources/subscribe` i `resources/unsubscribe`.
  Snimka se uzima iz SDK-a; `_post` više ne šalje `http.disconnect`, jer bi SSE put SDK-a inače prekinuo obradu.
- `web._modern_reply` (iz `fast_reply`, kad je `MCP-Protocol-Version` verzija iz snimke): odgovara iz snimke bez
  učitavanja SDK-a. Prihvaća samo oblike koje SDK obrađuje jednako, a sve ostalo ide SDK-u: `Mcp-Method` različit od
  tijela, ponovljeno zaglavlje za usmjeravanje, `_meta` s drugom verzijom, bez `clientCapabilities`, s `logLevel` ili
  drugim ključem `io.modelcontextprotocol/*`, `clientInfo` bez `version`, nepoznati parametri (npr. `cursor`), listen
  bez filtra ili bez SSE u Accept, `tools/call`. Notifikacije moderne ere dobivaju 202.
- Zapis zahtjeva: zahtjev moderne ere koji ipak ide SDK-u ima `why=<razlog>` (`meta_key`, `mcp_method`, `caps`,
  `filter`, `accept_sse`, `params`, `dup_header`, …; bez sadržaja). Ako stvarni Claude pošalje oblik koji brzi put
  ne pozna, log pokazuje zašto.
- Usput (dogovoreno 21.11.): `update.build_database` nakon neuspjele izgradnje briše i DuckDB-ovu mapu za
  prelijevanje `<baza>.tmp-<datum>.tmp/`. Nakon OOM-a 21.11. ondje je ostalo ~1,3 GB.

Stara era (initialize, tools/list, … s verzijama 2024-11-05 do 2025-11-25) je nepromijenjena. Njezina snimka je ista
kao prije, `initialize` i dalje najavljuje `tools.listChanged: false`.

## Memorija funkcije (2 GB → 1 GB?)

Ne može ni na jednom planu, pa `vercel.json` nije mijenjan. Izvor: vercel.com/docs/functions/configuring-functions/memory
i /docs/functions/limitations:
- Hobby: "they will always execute with 2 GB (1 vCPU)", "Hobby users cannot configure this size".
- Pro/Enterprise (Fluid compute): samo Standard 2 GB / 1 vCPU (zadano) ili Performance 4 GB / 2 vCPU, u Settings →
  Functions → Function CPU. Opcije od 1 GB nema; 1024 MB postoji samo za projekte s Hobby plana stvorene prije
  8.11.2019.
- "You cannot set your memory size using `vercel.json`. If you try to do so, you will receive a warning at build time."

Provisioned memory se zato smanjuje skraćivanjem trajanja instance: listen sada traje ~0 ms umjesto 50 s.

## Preview (ovaj kod, 23.11.2026.)

`vercel@65.11.0 build` + `deploy --prebuilt`, sažeta baza od 20.11.2026. (paket 202,9 MB), zahtjevi preko `vercel
curl`. Trajanje je `time_total` curla s ovog računala, uključuje mrežu (~0,2 s). Niz kakav šalje Claude, verzija
2026-07-28 s `_meta` (clientCapabilities s `elicitation` i `extensions`):

| zahtjev | status | s | zapis |
|---|---|---|---|
| server/discover (`server-discover-probe-1`, hladno) | 200 | 0,46 | fast, cpu 2 ms, cold=1 |
| server/discover (brojčani id) | 200 | 0,34 | fast |
| tools/list | 200 | 0,34 | fast |
| subscriptions/listen (`listen:0`) | **404 -32601** | **0,32** | **fast**, cpu 0 ms |
| notifications/initialized | 202 | 0,34 | fast |
| prompts/list | 200 | 0,22 | fast |
| ping | 404 -32601 | 0,34 | fast |
| tools/call list_staples | 200 | 2,68 | sdk (`sdk loaded cpu_ms=2264`) |
| tools/call plan_basket | 200 | 1,93 | sdk, cpu 1692 ms |
| server/discover (`server-discover-probe-2`) | 200 | 0,23 | fast |
| subscriptions/listen (`listen:1`) | 404 -32601 | 0,22 | fast |

Nijedan `timeout=1`, nijedan "ASGI callable returned without completing response". SDK se učitao jednom, na prvom
tools/call. Stara era na istom previewu: initialize 200 (0,26 s), GET /mcp 405 `allow=POST`. Preview je nakon testa
obrisan, a na produkciju ništa nije ručno deployano.

**Nije provjereno:** pravi Claude klijent spojen na preview (zaštita deploya, kao u Koraku 19). Ne znam ponavlja li
Claude listen nakon 404. Po specifikaciji to je trajna greška, a ponavljanje je predviđeno samo za prekinut tok.
Provjera nakon sljedećeg zakazanog deploya: u produkcijskim logovima `rpc=subscriptions/listen` treba imati
`status=404 ms=0 path=fast` i samo `id=listen:0` po razgovoru. Ako se pojave `listen:1`, `:2`, … u kratkim
razmacima, klijent ponavlja i treba drugi odgovor.

## Provjera

- `tests/test_step21.py` (7 testova):
  - snimka jednaka trenutnom SDK-u;
  - discover bez pretplata, listen nije poslužen;
  - 42 oblika moderne ere bajt po bajt kao SDK (status, zaglavlja, tijelo). 28 ih ide brzim putem, 14 SDK-u s
    razlogom `why`;
  - ponovljena zaglavlja idu SDK-u;
  - Claudeov niz kroz VercelApp: sve osim tools/call bez SDK-a i ispod 0,5 s, listen daje 404 JSON;
  - `why=` u zapisu;
  - brisanje DuckDB-ove mape za prelijevanje.
- `tests/test_step19.py`: notifikacija s `MCP-Protocol-Version: 2026-07-28` sada ide brzim putem (prije SDK-u).
- Zlatni izlazi, lokalna baza od 20.11.2026., 28 scenarija: stari kod (`302581c`) == novi kod na punoj bazi
  (28/28), sažeta == puna (`golden.py --check`, `MM_DUCKDB_MEMORY=300MB`, 28/28). Zapisani zlatni izlazi su vraćeni
  na commitane.
- `uv run pytest -q`: 1540 passed, 7 skipped (bez MM_GOLDEN).
